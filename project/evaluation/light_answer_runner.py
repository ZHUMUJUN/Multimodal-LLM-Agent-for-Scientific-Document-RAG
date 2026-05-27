import json
import logging
import os
import statistics
import time
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from datasets import Dataset
from langchain_core.messages import HumanMessage
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import answer_relevancy, faithfulness

import config
from core.lightrag_client import LightRAGClient
from core.logging_utils import log_event
from core.retrieval_router import route_question
from db.vector_db_manager import VectorDbManager
from providers.factory import ProviderFactory
from retrieval import RetrievalPipeline

from .schemas import load_cases

logger = logging.getLogger(__name__)


ANSWER_PROMPT = """You are answering questions for a retrieval benchmark.
Use only the provided context.
If the context is insufficient, say that the context is insufficient.
Answer in concise Chinese in 2-4 sentences.

Question:
{question}

Context:
{context}
"""


def _normalize_source_name(value: str) -> str:
    return Path(value or "").name.replace(".pdf", "").replace(".md", "").strip().lower()


def _is_source_hit(expected_sources: list[str], retrieved_sources: list[str]) -> bool:
    if not expected_sources:
        return False
    expected = {_normalize_source_name(item) for item in expected_sources if item}
    retrieved = {_normalize_source_name(item) for item in retrieved_sources if item}
    return bool(expected & retrieved)


def _keyword_hit_rate(expected_keywords: list[str], answer: str) -> float:
    if not expected_keywords:
        return 0.0
    normalized_answer = (answer or "").lower()
    matched = sum(1 for keyword in expected_keywords if keyword and keyword.lower() in normalized_answer)
    return round(matched / len(expected_keywords), 4)


def _build_question_type_summary(case_results: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in case_results:
        grouped[item.get("question_type") or "unknown"].append(item)

    summary: dict[str, dict] = {}
    for question_type, items in grouped.items():
        latencies = [item["latency_ms"] for item in items]
        summary[question_type] = {
            "case_count": len(items),
            "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
            "source_hit_rate": round(statistics.mean(1 if item["source_hit"] else 0 for item in items), 4),
            "avg_keyword_hit_rate": round(statistics.mean(item["keyword_hit_rate"] for item in items), 4),
        }
    return summary


def _build_routing_summary(case_results: list[dict]) -> dict:
    routed_cases = [item for item in case_results if item.get("expected_route")]
    if not routed_cases:
        return {}

    route_hits = [1 if item.get("route_hit") else 0 for item in routed_cases]
    distribution = Counter(item.get("resolved_mode") or "unknown" for item in routed_cases)
    by_type: dict[str, list[int]] = defaultdict(list)
    for item in routed_cases:
        by_type[item.get("question_type") or "unknown"].append(1 if item.get("route_hit") else 0)

    return {
        "expected_route_coverage": len(routed_cases),
        "route_hit_rate": round(statistics.mean(route_hits), 4) if route_hits else 0.0,
        "route_distribution": dict(distribution),
        "route_hit_rate_by_type": {
            question_type: round(statistics.mean(scores), 4)
            for question_type, scores in by_type.items()
        },
    }


def _generate_answer(llm, question: str, contexts: list[str]) -> str:
    context_text = "\n\n".join(
        f"[Context {index + 1}]\n{content}" for index, content in enumerate(contexts) if content.strip()
    )
    if not context_text.strip():
        return "当前检索上下文不足，无法给出可靠回答。"

    prompt = ANSWER_PROMPT.format(question=question, context=context_text[:12000])
    response = llm.invoke([HumanMessage(content=prompt)])
    return getattr(response, "content", str(response)).strip()


def _run_ragas(case_results: list[dict], llm, embeddings) -> dict:
    eligible = [
        {
            "user_input": item["question"],
            "response": item["answer"],
            "retrieved_contexts": item["retrieved_contexts"],
            "reference": item["ground_truth"],
        }
        for item in case_results
        if item.get("ground_truth", "").strip()
    ]

    if not eligible:
        return {
            "enabled": False,
            "available": False,
            "evaluated_cases": 0,
            "scores": {},
            "skipped_reason": "No cases with non-empty ground_truth were found.",
        }

    ragas_llm = LangchainLLMWrapper(llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    metrics = [
        deepcopy(answer_relevancy),
        deepcopy(faithfulness),
    ]
    metrics[0].llm = ragas_llm
    metrics[0].embeddings = ragas_embeddings
    metrics[1].llm = ragas_llm
    try:
        dataset = Dataset.from_list(eligible)
        result = evaluate(
            dataset,
            metrics=metrics,
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            show_progress=False,
            raise_exceptions=False,
        )
        summary = result.to_pandas().mean(numeric_only=True).to_dict() if hasattr(result, "to_pandas") else {}
        normalized = {
            key: float(value)
            for key, value in summary.items()
            if isinstance(value, (int, float))
        }
        return {
            "enabled": True,
            "available": True,
            "evaluated_cases": len(eligible),
            "scores": normalized,
        }
    except Exception as exc:
        return {
            "enabled": True,
            "available": False,
            "evaluated_cases": len(eligible),
            "scores": {},
            "skipped_reason": f"Ragas evaluation failed: {exc}",
        }


def run_light_answer_benchmark(
    dataset_path: str,
    modes: list[str],
    output_dir: str | None = None,
    top_k: int = 4,
) -> list[Path]:
    dataset_path = os.path.abspath(dataset_path)
    cases = load_cases(dataset_path)
    output_root = Path(output_dir or config.EVAL_OUTPUT_DIR)
    output_root.mkdir(parents=True, exist_ok=True)

    vector_db = VectorDbManager()
    llm = ProviderFactory.create_chat_model()
    lightrag_client = LightRAGClient() if config.LIGHTRAG_ENABLED else None
    previous_mode = config.RETRIEVAL_MODE
    generated_paths: list[Path] = []
    run_started_at = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        for mode in modes:
            config.RETRIEVAL_MODE = mode
            case_results: list[dict] = []

            for case in cases:
                route_decision = route_question(case.question) if mode == "router" else None
                resolved_mode = route_decision.mode if route_decision else mode

                if resolved_mode == "lightrag":
                    if lightrag_client is None:
                        raise RuntimeError("LightRAG benchmark requested but LIGHTRAG_ENABLED=false")
                    query_started = time.perf_counter()
                    response = lightrag_client.query(
                        query=case.question,
                        include_references=True,
                        include_chunk_content=True,
                    )
                    total_latency_ms = round((time.perf_counter() - query_started) * 1000, 2)
                    answer = response.get("response", "").strip()
                    references = response.get("references") or []
                    contexts = []
                    sources = []
                    for ref in references:
                        file_path = ref.get("file_path", "")
                        if file_path:
                            sources.append(Path(file_path).name)
                        contexts.extend(ref.get("content") or [])
                    retrieval_latency_ms = total_latency_ms
                    answer_latency_ms = 0.0
                else:
                    collection_name = config.get_vector_collection_name(case.collection)
                    collection = vector_db.get_collection(collection_name)
                    pipeline = RetrievalPipeline(collection, collection_name)
                    previous_case_mode = config.RETRIEVAL_MODE
                    try:
                        config.RETRIEVAL_MODE = resolved_mode

                        retrieval_started = time.perf_counter()
                        docs = pipeline.search(case.question, top_k)
                        retrieval_latency_ms = round((time.perf_counter() - retrieval_started) * 1000, 2)

                        contexts = [doc.page_content for doc in docs]
                        sources = [doc.metadata.get("source", "") for doc in docs]

                        answer_started = time.perf_counter()
                        answer = _generate_answer(llm, case.question, contexts)
                        answer_latency_ms = round((time.perf_counter() - answer_started) * 1000, 2)
                    finally:
                        config.RETRIEVAL_MODE = previous_case_mode

                source_hit = _is_source_hit(case.expected_sources, sources)
                keyword_hit_rate = _keyword_hit_rate(case.expected_keywords, answer)
                route_hit = None
                if case.expected_route:
                    route_hit = resolved_mode == case.expected_route

                case_results.append(
                    {
                        "id": case.case_id,
                        "collection": config.normalize_collection_name(case.collection),
                        "question": case.question,
                        "question_type": case.question_type,
                        "answer": answer,
                        "ground_truth": case.ground_truth,
                        "expected_sources": case.expected_sources,
                        "expected_keywords": case.expected_keywords,
                        "expected_route": case.expected_route,
                        "notes": case.notes,
                        "resolved_mode": resolved_mode,
                        "route_reasons": route_decision.reasons if route_decision else [],
                        "route_hit": route_hit,
                        "retrieval_latency_ms": retrieval_latency_ms,
                        "answer_latency_ms": answer_latency_ms,
                        "latency_ms": round(retrieval_latency_ms + answer_latency_ms, 2),
                        "answer_length": len(answer or ""),
                        "source_hit": source_hit,
                        "keyword_hit_rate": keyword_hit_rate,
                        "retrieved_contexts": contexts,
                        "retrieved_sources": sources,
                    }
                )

            latencies = [item["latency_ms"] for item in case_results]
            ragas_summary = _run_ragas(case_results, llm=llm, embeddings=vector_db._dense_embeddings)
            summary = {
                "dataset_path": dataset_path,
                "mode": mode,
                "case_count": len(case_results),
                "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
                "p95_latency_ms": round(max(latencies), 2) if latencies else 0,
                "avg_answer_length": round(statistics.mean(item["answer_length"] for item in case_results), 2),
                "source_hit_rate": round(
                    statistics.mean(1 if item["source_hit"] else 0 for item in case_results),
                    4,
                ) if case_results else 0.0,
                "avg_keyword_hit_rate": round(
                    statistics.mean(item["keyword_hit_rate"] for item in case_results),
                    4,
                ) if case_results else 0.0,
                "question_type_summary": _build_question_type_summary(case_results),
                "routing": _build_routing_summary(case_results),
                "ragas": ragas_summary,
            }

            payload = {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "benchmark_type": "light_answer",
                "retrieval_mode": mode,
                "model": config.LLM_MODEL,
                "provider": config.LLM_PROVIDER,
                "reranker_enabled": config.RERANKER_ENABLED,
                "reranker_model": config.RERANKER_MODEL,
                "top_k": top_k,
                "summary": summary,
                "cases": case_results,
            }

            report_path = output_root / f"light_answer_benchmark_{mode}_{run_started_at}.json"
            with open(report_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)

            log_event(
                logger,
                "evaluation.light_answer_benchmark_completed",
                mode=mode,
                dataset=dataset_path,
                report_path=str(report_path),
                case_count=len(case_results),
            )
            generated_paths.append(report_path)
    finally:
        config.RETRIEVAL_MODE = previous_mode

    return generated_paths
