import logging
import json
import tempfile
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path

import config
from core.document_manager import DocumentManager
from core.greetings import greeting_response, is_greeting_only
from core.lightrag_client import LightRAGClient
from core.logging_utils import log_event
from core.metadata_queries import (
    format_collection_file_list_response,
    is_collection_file_list_query,
)
from core.model_router import route_model
from core.retrieval_router import route_question
from core.skill_registry import SkillRegistry
from core.tracing import add_span_attributes, start_span
from core.rag_system import RAGSystem
from db.vector_db_manager import VectorDbManager
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _message_content_from_output(output) -> str:
    if not isinstance(output, dict):
        return ""
    messages = output.get("messages") or []
    if not messages:
        return ""
    last_message = messages[-1]
    return getattr(last_message, "content", "") or ""


class PlatformService:

    def __init__(self):
        self.vector_db = VectorDbManager()
        self._systems: dict[tuple[str, str], RAGSystem] = {}
        self.lightrag_client = LightRAGClient() if config.LIGHTRAG_ENABLED else None
        self.skill_registry = SkillRegistry(config.SKILLS_DIR) if config.SKILLS_ENABLED else None

    def _get_system(self, collection: str, model_name: str | None = None) -> RAGSystem:
        collection_key = config.normalize_collection_name(collection)
        selected_model = model_name or config.LLM_MODEL
        cache_key = (collection_key, selected_model)
        if cache_key not in self._systems:
            rag_system = RAGSystem(collection_key=collection_key, vector_db=self.vector_db, model_name=selected_model)
            rag_system.initialize()
            self._systems[cache_key] = rag_system
        return self._systems[cache_key]

    def list_collections(self) -> list[dict]:
        collections = {}
        vector_collections = self.vector_db.list_collections()
        for vector_collection in vector_collections:
            if vector_collection == config.COLLECTION_PREFIX:
                name = config.DEFAULT_COLLECTION
            elif vector_collection.startswith(f"{config.COLLECTION_PREFIX}_"):
                name = vector_collection.removeprefix(f"{config.COLLECTION_PREFIX}_")
            else:
                name = vector_collection

            collections[name] = {
                "name": name,
                "vector_collection": vector_collection,
                "document_count": len(list(Path(config.get_markdown_dir(name)).glob("*.md"))),
            }

        for path in Path(config.MARKDOWN_ROOT_DIR).glob("*"):
            if path.is_dir() and path.name not in collections:
                collections[path.name] = {
                    "name": path.name,
                    "vector_collection": config.get_vector_collection_name(path.name),
                    "document_count": len(list(path.glob("*.md"))),
                }

        if not collections:
            collections[config.DEFAULT_COLLECTION] = {
                "name": config.DEFAULT_COLLECTION,
                "vector_collection": config.get_vector_collection_name(config.DEFAULT_COLLECTION),
                "document_count": 0,
            }

        return sorted(collections.values(), key=lambda item: item["name"])

    def get_documents(self, collection: str) -> list[str]:
        collection_key = config.normalize_collection_name(collection)
        markdown_dir = Path(config.get_markdown_dir(collection_key))
        if not markdown_dir.exists():
            return []
        return sorted([path.name.replace(".md", ".pdf") for path in markdown_dir.glob("*.md")])

    def search_figures(self, collection: str, query: str, limit: int = 5) -> dict:
        collection_key = config.normalize_collection_name(collection)
        rag_system = self._get_system(collection_key)
        if rag_system.figure_index is None:
            return {
                "collection": collection_key,
                "enabled": False,
                "query": query,
                "results": [],
            }
        results = rag_system.figure_index.search(query=query, limit=limit)
        return {
            "collection": collection_key,
            "enabled": True,
            "query": query,
            "results": results,
        }

    def add_documents(self, collection: str, document_paths, progress_callback=None) -> dict:
        with start_span("documents.ingest", collection=config.normalize_collection_name(collection)) as span:
            rag_system = self._get_system(collection)
            doc_manager = DocumentManager(rag_system)
            added, skipped = doc_manager.add_documents(document_paths, progress_callback=progress_callback)
            documents = doc_manager.get_markdown_files()
            add_span_attributes(
                span,
                collection=rag_system.collection_key,
                documents_added=added,
                documents_skipped=skipped,
                document_count=len(documents),
            )
            return {
                "collection": rag_system.collection_key,
                "added": added,
                "skipped": skipped,
                "documents": documents,
            }

    def ingest_uploads(self, collection: str, uploads) -> dict:
        temp_paths = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for upload in uploads:
                filename = Path(upload.filename or f"upload_{len(temp_paths)}.bin").name
                temp_path = Path(temp_dir) / filename
                temp_path.write_bytes(upload.file.read())
                temp_paths.append(str(temp_path))
            return self.add_documents(collection, temp_paths)

    def list_skills(self) -> list[dict]:
        if self.skill_registry is None:
            return []
        return self.skill_registry.list_skills()

    def _skill_collection_context(self, collection_key: str, active_skill) -> str:
        if active_skill is None or active_skill.name not in {"paper_qa_zh", "literature_compare"}:
            return ""

        documents = self.get_documents(collection_key)
        if not documents:
            return "\n\nCollection Context: No documents are currently listed in the selected collection."

        document_list = "\n".join(f"- {name}" for name in documents[:20])
        if len(documents) == 1:
            return (
                "\n\nCollection Context:\n"
                f"The selected collection contains exactly one document:\n{document_list}\n"
                "Resolve references such as '这篇论文', '该论文', 'this paper', or 'the paper' to this document. "
                "Do not ask for clarification solely because the user omitted the paper title."
            )

        return (
            "\n\nCollection Context:\n"
            f"The selected collection contains {len(documents)} documents:\n{document_list}\n"
            "If the user uses an ambiguous reference such as '这篇论文' and no conversation context identifies one document, ask for clarification."
        )

    def chat(self, collection: str, message: str, session_id: str | None = None, skill_name: str | None = None) -> dict:
        collection_key = config.normalize_collection_name(collection)
        active_session_id = session_id or str(uuid.uuid4())
        clean_message = (message or "").strip()
        requested_skill = skill_name

        if self.skill_registry is not None:
            command_skill, command_message = self.skill_registry.parse_command(clean_message)
            if command_skill:
                requested_skill = requested_skill or command_skill
                clean_message = command_message

        skill_match = self.skill_registry.select(clean_message, requested=requested_skill) if self.skill_registry is not None else None
        active_skill = skill_match.skill if skill_match else None
        skill_context = active_skill.prompt_context() if active_skill else ""
        skill_context += self._skill_collection_context(collection_key, active_skill)
        skill_payload = {
            "active_skill": active_skill.name if active_skill else None,
            "skill_reasons": skill_match.reasons if skill_match else [],
        }
        model_payload = {
            "selected_model": None,
            "model_route_reasons": [],
            "model_complexity": None,
        }

        with start_span(
            "chat.request",
            collection=collection_key,
            session_id=active_session_id,
            message_length=len(clean_message),
            active_skill=active_skill.name if active_skill else "",
        ) as span:
            if is_greeting_only(clean_message):
                reply = greeting_response()
                log_event(logger, "chat.greeting", collection=collection_key, session_id=active_session_id)
                add_span_attributes(span, route="greeting", answer_length=len(reply))
                return {
                    "collection": collection_key,
                    "session_id": active_session_id,
                    "answer": reply,
                    **skill_payload,
                }

            if is_collection_file_list_query(clean_message):
                files = self.get_documents(collection_key)
                reply = format_collection_file_list_response(collection_key, files)
                log_event(
                    logger,
                    "chat.metadata_file_list",
                    collection=collection_key,
                    session_id=active_session_id,
                    file_count=len(files),
                )
                add_span_attributes(
                    span,
                    route="metadata_file_list",
                    file_count=len(files),
                    answer_length=len(reply),
                )
                return {
                    "collection": collection_key,
                    "session_id": active_session_id,
                    "answer": reply,
                    **skill_payload,
                }

            route_decision = None
            resolved_mode = config.RETRIEVAL_MODE
            if active_skill and active_skill.retrieval_mode in config.SKILL_RETRIEVAL_MODES:
                resolved_mode = active_skill.retrieval_mode
                add_span_attributes(
                    span,
                    skill_name=active_skill.name,
                    skill_retrieval_mode=resolved_mode,
                    skill_reasons=",".join(skill_match.reasons if skill_match else []),
                )
            elif config.RETRIEVAL_MODE == "router":
                route_decision = route_question(clean_message)
                resolved_mode = route_decision.mode
                add_span_attributes(
                    span,
                    routing_mode="router",
                    resolved_mode=resolved_mode,
                    route_reasons=",".join(route_decision.reasons),
                )

            model_decision = route_model(
                clean_message,
                skill_name=active_skill.name if active_skill else None,
                retrieval_mode=resolved_mode,
                reflection_enabled=config.REFLECTION_ENABLED,
            )
            model_payload = {
                "selected_model": model_decision.selected_model,
                "model_route_reasons": model_decision.reasons,
                "model_complexity": model_decision.complexity,
            }
            add_span_attributes(
                span,
                selected_model=model_decision.selected_model,
                model_complexity=model_decision.complexity,
                model_route_reasons=",".join(model_decision.reasons),
            )

            if resolved_mode == "lightrag":
                if self.lightrag_client is None:
                    raise RuntimeError("Resolved retrieval mode is lightrag but LIGHTRAG_ENABLED=false")
                response = self.lightrag_client.query(
                    query=clean_message,
                    include_references=True,
                    include_chunk_content=False,
                )
                answer = response.get("response", "").strip()
                references = response.get("references") or []
                source_lines = []
                for ref in references:
                    file_path = ref.get("file_path", "")
                    if file_path:
                        source_lines.append(f"- {Path(file_path).name}")
                if source_lines:
                    answer = f"{answer}\n\n---\n**Sources:**\n" + "\n".join(dict.fromkeys(source_lines))
                log_event(
                    logger,
                    "chat.completed_lightrag",
                    collection=collection_key,
                    session_id=active_session_id,
                    reference_count=len(references),
                    answer_length=len(answer or ""),
                )
                add_span_attributes(span, route="lightrag", answer_length=len(answer or ""))
                return {
                    "collection": collection_key,
                    "session_id": active_session_id,
                    "answer": answer,
                    "retrieval_mode": config.RETRIEVAL_MODE,
                    "resolved_retrieval_mode": resolved_mode,
                    "routing_reasons": route_decision.reasons if route_decision else [],
                    **skill_payload,
                    **model_payload,
                }

            rag_system = self._get_system(collection_key, model_name=model_decision.selected_model)
            add_span_attributes(
                span,
                route="rag",
                resolved_retrieval_mode=resolved_mode,
                model=model_decision.selected_model,
                provider=config.LLM_PROVIDER,
            )

            previous_mode = config.RETRIEVAL_MODE
            try:
                config.RETRIEVAL_MODE = resolved_mode
                result = rag_system.agent_graph.invoke(
                    {
                        "messages": [HumanMessage(content=clean_message)],
                        "active_skill": active_skill.name if active_skill else "",
                        "skill_context": skill_context,
                    },
                    rag_system.get_config(thread_id=active_session_id),
                )
                answer = result["messages"][-1].content
                agent_answers = result.get("agent_answers", [])
                worker_roles = [item.get("worker_role", "research_worker") for item in agent_answers if isinstance(item, dict)]
                tool_call_count = sum(int(item.get("tool_call_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                reflection_count = sum(int(item.get("reflection_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                reflection_search_count = sum(int(item.get("reflection_search_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                log_event(
                    logger,
                    "chat.completed",
                    collection=rag_system.collection_key,
                    session_id=active_session_id,
                    answer_length=len(answer or ""),
                    worker_roles=worker_roles,
                    tool_call_count=tool_call_count,
                    reflection_count=reflection_count,
                    reflection_search_count=reflection_search_count,
                )
                add_span_attributes(
                    span,
                    answer_length=len(answer or ""),
                    worker_count=len(worker_roles),
                    tool_call_count=tool_call_count,
                    reflection_count=reflection_count,
                    reflection_search_count=reflection_search_count,
                )
                return {
                    "collection": rag_system.collection_key,
                    "session_id": active_session_id,
                    "answer": answer,
                    "retrieval_mode": previous_mode,
                    "resolved_retrieval_mode": resolved_mode,
                    "routing_reasons": route_decision.reasons if route_decision else [],
                    "worker_roles": worker_roles,
                    "worker_count": len(worker_roles),
                    "tool_call_count": tool_call_count,
                    "reflection_count": reflection_count,
                    "reflection_search_count": reflection_search_count,
                    **skill_payload,
                    **model_payload,
                }
            except Exception as exc:
                error = str(exc)
                log_event(
                    logger,
                    "chat.failed",
                    collection=rag_system.collection_key,
                    session_id=active_session_id,
                    error=error,
                )
                add_span_attributes(span, error=error)
                if config.LLM_PROVIDER == "ollama" and "connection refused" in error.lower():
                    answer = (
                        "本地 Ollama 服务没有启动，当前无法调用大模型。"
                        "请先运行 `ollama serve`，并确认 `ollama list` 里有配置的模型。"
                    )
                elif config.LLM_PROVIDER == "ollama" and "not found" in error.lower():
                    answer = (
                        f"本地 Ollama 没有找到模型 `{config.LLM_MODEL}`。"
                        f"请先运行 `ollama pull {config.LLM_MODEL}`，或把 `LLM_MODEL` 改成本机已有模型。"
                    )
                else:
                    answer = f"聊天链路执行失败：{error}"
                return {
                    "collection": rag_system.collection_key,
                    "session_id": active_session_id,
                    "answer": answer,
                    "retrieval_mode": previous_mode,
                    "resolved_retrieval_mode": resolved_mode,
                    "routing_reasons": route_decision.reasons if route_decision else [],
                    **skill_payload,
                    **model_payload,
                }
            finally:
                config.RETRIEVAL_MODE = previous_mode
                rag_system.observability.flush()

    async def chat_stream(
        self,
        collection: str,
        message: str,
        session_id: str | None = None,
        skill_name: str | None = None,
    ) -> AsyncGenerator[str, None]:
        collection_key = config.normalize_collection_name(collection)
        active_session_id = session_id or str(uuid.uuid4())
        clean_message = (message or "").strip()
        requested_skill = skill_name

        if self.skill_registry is not None:
            command_skill, command_message = self.skill_registry.parse_command(clean_message)
            if command_skill:
                requested_skill = requested_skill or command_skill
                clean_message = command_message

        skill_match = self.skill_registry.select(clean_message, requested=requested_skill) if self.skill_registry is not None else None
        active_skill = skill_match.skill if skill_match else None
        skill_context = active_skill.prompt_context() if active_skill else ""
        skill_context += self._skill_collection_context(collection_key, active_skill)
        skill_payload = {
            "active_skill": active_skill.name if active_skill else None,
            "skill_reasons": skill_match.reasons if skill_match else [],
        }
        yield _sse("skill_selected", {"collection": collection_key, "session_id": active_session_id, **skill_payload})

        try:
            if is_greeting_only(clean_message):
                answer = greeting_response()
                yield _sse("answer_delta", {"text": answer})
                yield _sse("done", {"collection": collection_key, "session_id": active_session_id, "answer": answer, **skill_payload})
                return

            if is_collection_file_list_query(clean_message):
                files = self.get_documents(collection_key)
                answer = format_collection_file_list_response(collection_key, files)
                yield _sse("answer_delta", {"text": answer})
                yield _sse("done", {"collection": collection_key, "session_id": active_session_id, "answer": answer, **skill_payload})
                return

            route_decision = None
            resolved_mode = config.RETRIEVAL_MODE
            if active_skill and active_skill.retrieval_mode in config.SKILL_RETRIEVAL_MODES:
                resolved_mode = active_skill.retrieval_mode
            elif config.RETRIEVAL_MODE == "router":
                route_decision = route_question(clean_message)
                resolved_mode = route_decision.mode

            model_decision = route_model(
                clean_message,
                skill_name=active_skill.name if active_skill else None,
                retrieval_mode=resolved_mode,
                reflection_enabled=config.REFLECTION_ENABLED,
            )
            model_payload = {
                "selected_model": model_decision.selected_model,
                "model_route_reasons": model_decision.reasons,
                "model_complexity": model_decision.complexity,
            }
            yield _sse(
                "model_routed",
                {
                    "retrieval_mode": config.RETRIEVAL_MODE,
                    "resolved_retrieval_mode": resolved_mode,
                    "routing_reasons": route_decision.reasons if route_decision else [],
                    **model_payload,
                },
            )

            if resolved_mode == "lightrag":
                if self.lightrag_client is None:
                    raise RuntimeError("Resolved retrieval mode is lightrag but LIGHTRAG_ENABLED=false")
                yield _sse("retrieval_started", {"mode": "lightrag"})
                response = self.lightrag_client.query(
                    query=clean_message,
                    include_references=True,
                    include_chunk_content=False,
                )
                answer = response.get("response", "").strip()
                yield _sse("answer_delta", {"text": answer})
                yield _sse(
                    "done",
                    {
                        "collection": collection_key,
                        "session_id": active_session_id,
                        "answer": answer,
                        "retrieval_mode": config.RETRIEVAL_MODE,
                        "resolved_retrieval_mode": resolved_mode,
                        "routing_reasons": route_decision.reasons if route_decision else [],
                        **skill_payload,
                        **model_payload,
                    },
                )
                return

            rag_system = self._get_system(collection_key, model_name=model_decision.selected_model)
            previous_mode = config.RETRIEVAL_MODE
            final_output = {}
            final_answer = ""
            emitted_nodes: set[str] = set()
            try:
                config.RETRIEVAL_MODE = resolved_mode
                input_state = {
                    "messages": [HumanMessage(content=clean_message)],
                    "active_skill": active_skill.name if active_skill else "",
                    "skill_context": skill_context,
                }
                run_config = rag_system.get_config(thread_id=active_session_id)
                async for event in rag_system.agent_graph.astream_events(input_state, run_config, version="v2"):
                    event_name = event.get("event", "")
                    node_name = event.get("name", "")
                    data = event.get("data") or {}

                    if event_name == "on_chain_start" and node_name not in emitted_nodes:
                        emitted_nodes.add(node_name)
                        if node_name == "rewrite_query":
                            yield _sse("retrieval_started", {"stage": "rewrite_query"})
                        elif node_name == "plan_worker_tasks":
                            yield _sse("worker_started", {"stage": "plan_worker_tasks"})
                        elif node_name == "agent":
                            yield _sse("worker_started", {"stage": "agent"})
                        elif node_name == "reflect_answer":
                            yield _sse("reflection_started", {"stage": "reflect_answer"})
                        elif node_name == "aggregate_answers":
                            yield _sse("answer_started", {"stage": "aggregate_answers"})

                    if event_name == "on_chain_end":
                        output = data.get("output")
                        if isinstance(output, dict):
                            if output.get("messages"):
                                final_output = output
                                candidate = _message_content_from_output(output)
                                if candidate:
                                    final_answer = candidate
                            if node_name == "aggregate_answers":
                                candidate = _message_content_from_output(output)
                                if candidate:
                                    final_answer = candidate

                agent_answers = final_output.get("agent_answers", []) if isinstance(final_output, dict) else []
                worker_roles = [item.get("worker_role", "research_worker") for item in agent_answers if isinstance(item, dict)]
                tool_call_count = sum(int(item.get("tool_call_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                reflection_count = sum(int(item.get("reflection_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                reflection_search_count = sum(int(item.get("reflection_search_count", 0) or 0) for item in agent_answers if isinstance(item, dict))
                yield _sse("answer_delta", {"text": final_answer})
                yield _sse(
                    "done",
                    {
                        "collection": rag_system.collection_key,
                        "session_id": active_session_id,
                        "answer": final_answer,
                        "retrieval_mode": previous_mode,
                        "resolved_retrieval_mode": resolved_mode,
                        "routing_reasons": route_decision.reasons if route_decision else [],
                        "worker_roles": worker_roles,
                        "worker_count": len(worker_roles),
                        "tool_call_count": tool_call_count,
                        "reflection_count": reflection_count,
                        "reflection_search_count": reflection_search_count,
                        **skill_payload,
                        **model_payload,
                    },
                )
            finally:
                config.RETRIEVAL_MODE = previous_mode
                rag_system.observability.flush()
        except Exception as exc:
            yield _sse(
                "error",
                {
                    "collection": collection_key,
                    "session_id": active_session_id,
                    "error": f"{type(exc).__name__}: {exc}",
                    **skill_payload,
                },
            )

    def reset(self, collection: str, session_id: str | None = None) -> dict:
        rag_system = self._get_system(collection)
        active_session_id = session_id or rag_system.default_thread_id
        rag_system.reset_thread(session_id)
        new_session_id = session_id or rag_system.default_thread_id
        log_event(logger, "chat.reset", collection=rag_system.collection_key, session_id=active_session_id)
        return {
            "collection": rag_system.collection_key,
            "session_id": new_session_id,
        }

    def clear_collection(self, collection: str) -> dict:
        rag_system = self._get_system(collection)
        doc_manager = DocumentManager(rag_system)
        doc_manager.clear_all()
        return {
            "collection": rag_system.collection_key,
            "documents": doc_manager.get_markdown_files(),
        }

    def health(self) -> dict:
        collections = self.list_collections()
        return {
            "status": "ok",
            "provider": config.LLM_PROVIDER,
            "model": config.LLM_MODEL,
            "model_router_enabled": config.MODEL_ROUTER_ENABLED,
            "small_model": config.SMALL_LLM_MODEL,
            "large_model": config.LARGE_LLM_MODEL,
            "retrieval_mode": config.RETRIEVAL_MODE,
            "reflection_enabled": config.REFLECTION_ENABLED,
            "max_reflection_rounds": config.MAX_REFLECTION_ROUNDS,
            "multi_agent_planner_enabled": config.MULTI_AGENT_PLANNER_ENABLED,
            "reranker_enabled": config.RERANKER_ENABLED,
            "reranker_model": config.RERANKER_MODEL,
            "phoenix_enabled": config.PHOENIX_ENABLED,
            "phoenix_project": config.PHOENIX_PROJECT_NAME,
            "mcp_filesystem_enabled": config.MCP_FILESYSTEM_ENABLED,
            "skills_enabled": config.SKILLS_ENABLED,
            "skills": self.list_skills(),
            "lightrag_enabled": config.LIGHTRAG_ENABLED,
            "lightrag_base_url": config.LIGHTRAG_BASE_URL,
            "lightrag_query_mode": config.LIGHTRAG_QUERY_MODE,
            "crag_enabled": config.CRAG_ENABLED,
            "crag_provider": config.CRAG_PROVIDER,
            "crag_max_results": config.CRAG_MAX_RESULTS,
            "multimodal_enabled": config.MULTIMODAL_ENABLED,
            "clip_model": config.CLIP_MODEL,
            "figure_index_page_screenshots": config.FIGURE_INDEX_PAGE_SCREENSHOTS,
            "figure_index_embedded_images": config.FIGURE_INDEX_EMBEDDED_IMAGES,
            "default_collection": config.DEFAULT_COLLECTION,
            "collections": len(collections),
        }
