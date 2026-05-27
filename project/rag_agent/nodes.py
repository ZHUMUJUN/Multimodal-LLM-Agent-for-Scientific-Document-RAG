import logging
from typing import Literal, Set
import config
from core.logging_utils import log_event
from core.tracing import add_span_attributes, start_span
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage, AIMessage, ToolMessage
from langgraph.types import Command
from .graph_state import State, AgentState
from .schemas import QueryAnalysis, ReflectionDecision, WorkerTask
from .prompts import *
from utils import estimate_context_tokens
from config import BASE_TOKEN_THRESHOLD, TOKEN_GROWTH_FACTOR

logger = logging.getLogger(__name__)

def _worker_role_for_query(query: str, active_skill: str) -> str:
    text = (query or "").lower()
    if active_skill == "literature_compare" or any(key in text for key in ["compare", "comparison", "difference", "versus", "related work", "对比", "比较"]):
        return "comparison_worker"
    if any(key in text for key in ["dataset", "metric", "experiment", "benchmark", "miou", "mdice", "accuracy", "result", "数据", "指标", "实验"]):
        return "data_eval_worker"
    if any(key in text for key in ["method", "architecture", "module", "contribution", "innovation", "adapter", "方法", "创新", "贡献", "模块"]):
        return "method_worker"
    if any(key in text for key in ["background", "motivation", "introduction", "problem", "背景", "动机"]):
        return "paper_overview_worker"
    if any(key in text for key in ["limitation", "failure", "future", "局限", "失败"]):
        return "limitation_worker"
    return "research_worker"


def _expected_output_for_role(role: str) -> str:
    outputs = {
        "paper_overview_worker": "Summarize the research background, motivation, problem setting, and main paper content with cited evidence.",
        "method_worker": "Extract the method, architecture, key modules, and innovations with exact technical terms.",
        "data_eval_worker": "Extract datasets, benchmarks, metrics, numeric results, and evaluation setup.",
        "comparison_worker": "Compare the requested papers or methods across explicit axes and mark missing evidence.",
        "limitation_worker": "Extract limitations, failure cases, assumptions, and future work only when supported.",
        "research_worker": "Answer the assigned question using retrieved evidence.",
    }
    return outputs.get(role, outputs["research_worker"])

def summarize_history(state: State, llm):
    if len(state["messages"]) < 4:
        return {"conversation_summary": ""}
    
    relevant_msgs = [
        msg for msg in state["messages"][:-1]
        if isinstance(msg, (HumanMessage, AIMessage)) and not getattr(msg, "tool_calls", None)
    ]

    if not relevant_msgs:
        return {"conversation_summary": ""}
    
    conversation = "Conversation history:\n"
    for msg in relevant_msgs[-6:]:
        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        conversation += f"{role}: {msg.content}\n"

    summary_response = llm.with_config(temperature=0.2).invoke([SystemMessage(content=get_conversation_summary_prompt()), HumanMessage(content=conversation)])
    return {"conversation_summary": summary_response.content, "agent_answers": [{"__reset__": True}]}

def rewrite_query(state: State, llm):
    last_message = state["messages"][-1]
    conversation_summary = state.get("conversation_summary", "")
    skill_context = state.get("skill_context", "")

    context_section = (f"Conversation Context:\n{conversation_summary}\n" if conversation_summary.strip() else "") + f"User Query:\n{last_message.content}\n"

    llm_with_structure = llm.with_config(temperature=0.1).with_structured_output(QueryAnalysis)
    with start_span("agent.query_rewrite", original_query_length=len(last_message.content or "")) as span:
        response = llm_with_structure.invoke([SystemMessage(content=get_rewrite_query_prompt(skill_context)), HumanMessage(content=context_section)])
        log_event(
            logger,
            "agent.query_rewrite",
            original_query=last_message.content,
            question_is_clear=response.is_clear,
            rewritten_questions=response.questions,
        )
        add_span_attributes(
            span,
            question_is_clear=response.is_clear,
            rewritten_question_count=len(response.questions or []),
            active_skill=state.get("active_skill", ""),
        )

        if response.questions and response.is_clear:
            delete_all = [RemoveMessage(id=m.id) for m in state["messages"] if not isinstance(m, SystemMessage)]
            return {"questionIsClear": True, "messages": delete_all, "originalQuery": last_message.content, "rewrittenQuestions": response.questions}

        clarification = response.clarification_needed if response.clarification_needed and len(response.clarification_needed.strip()) > 10 else "I need more information to understand your question."
        return {"questionIsClear": False, "messages": [AIMessage(content=clarification)]}

def request_clarification(state: State):
    return {}

def plan_worker_tasks(state: State):
    questions = state.get("rewrittenQuestions", [])
    active_skill = state.get("active_skill", "")
    if not questions:
        return {"worker_tasks": []}

    tasks = []
    for question in questions:
        role = _worker_role_for_query(question, active_skill) if config.MULTI_AGENT_PLANNER_ENABLED else "research_worker"
        tasks.append(
            WorkerTask(
                role=role,
                task=question,
                search_query=question,
                expected_output=_expected_output_for_role(role),
            ).model_dump()
        )

    log_event(
        logger,
        "agent.worker_tasks_planned",
        original_query=state.get("originalQuery", ""),
        task_count=len(tasks),
        worker_roles=[task["role"] for task in tasks],
    )
    return {"worker_tasks": tasks}

# --- Agent Nodes ---
def orchestrator(state: AgentState, llm_with_tools):
    context_summary = state.get("context_summary", "").strip()
    skill_context = state.get("skill_context", "")
    sys_msg = SystemMessage(content=get_orchestrator_prompt(skill_context))
    summary_injection = (
        [HumanMessage(content=f"[COMPRESSED CONTEXT FROM PRIOR RESEARCH]\n\n{context_summary}")]
        if context_summary else []
    )
    iteration = 1 if not state.get("messages") else state.get("iteration_count", 0) + 1
    with start_span("agent.orchestrator", iteration=iteration, question_length=len(state["question"] or "")) as span:
        if not state.get("messages"):
            human_msg = HumanMessage(
                content=(
                    f"Worker role: {state.get('worker_role', 'research_worker')}\n"
                    f"Worker task: {state['question']}\n"
                    f"Initial search query: {state.get('search_query') or state['question']}\n"
                    f"Expected output: {state.get('expected_output') or 'Answer using retrieved evidence.'}"
                )
            )
            force_tool = HumanMessage(
                content=(
                    "YOU MUST CALL THE MOST RELEVANT TOOL AS THE FIRST STEP. "
                    "Use 'search_child_chunks' for document-content questions. "
                    "Use filesystem tools for repository, report, benchmark, config, or file questions."
                )
            )
            response = llm_with_tools.invoke([sys_msg] + summary_injection + [human_msg, force_tool])
            log_event(
                logger,
                "agent.orchestrator",
                question=state["question"],
                worker_role=state.get("worker_role", "research_worker"),
                iteration=1,
                tool_calls=[tc["name"] for tc in (response.tool_calls or [])],
            )
            add_span_attributes(span, tool_call_count=len(response.tool_calls or []), worker_role=state.get("worker_role", "research_worker"))
            return {"messages": [human_msg, response], "tool_call_count": len(response.tool_calls or []), "iteration_count": 1}

        if state.get("reflection_should_search", False):
            follow_up = HumanMessage(
                content=(
                    "Reflection found missing or weakly supported aspects. "
                    "You MUST call search_child_chunks now using the focused follow-up query below before answering again.\n\n"
                    f"Follow-up retrieval instruction:\n{state['messages'][-1].content}"
                )
            )
            response = llm_with_tools.invoke([sys_msg] + summary_injection + state["messages"] + [follow_up])
            tool_calls = response.tool_calls if hasattr(response, "tool_calls") else []
            log_event(
                logger,
                "agent.orchestrator_reflection_followup",
                question=state["question"],
                worker_role=state.get("worker_role", "research_worker"),
                iteration=iteration,
                tool_calls=[tc["name"] for tc in tool_calls] if tool_calls else [],
            )
            add_span_attributes(span, tool_call_count=len(tool_calls) if tool_calls else 0, worker_role=state.get("worker_role", "research_worker"))
            return {
                "messages": [follow_up, response],
                "tool_call_count": len(tool_calls) if tool_calls else 0,
                "iteration_count": 1,
                "reflection_should_search": False,
            }

        response = llm_with_tools.invoke([sys_msg] + summary_injection + state["messages"])
        tool_calls = response.tool_calls if hasattr(response, "tool_calls") else []
        log_event(
            logger,
            "agent.orchestrator",
            question=state["question"],
            worker_role=state.get("worker_role", "research_worker"),
            iteration=iteration,
            tool_calls=[tc["name"] for tc in tool_calls] if tool_calls else [],
        )
        add_span_attributes(span, tool_call_count=len(tool_calls) if tool_calls else 0, worker_role=state.get("worker_role", "research_worker"))
        return {"messages": [response], "tool_call_count": len(tool_calls) if tool_calls else 0, "iteration_count": 1}

def fallback_response(state: AgentState, llm):
    seen = set()
    unique_contents = []
    for m in state["messages"]:
        if isinstance(m, ToolMessage) and m.content not in seen:
            unique_contents.append(m.content)
            seen.add(m.content)

    context_summary = state.get("context_summary", "").strip()

    context_parts = []
    if context_summary:
        context_parts.append(f"## Compressed Research Context (from prior iterations)\n\n{context_summary}")
    if unique_contents:
        context_parts.append(
            "## Retrieved Data (current iteration)\n\n" +
            "\n\n".join(f"--- DATA SOURCE {i} ---\n{content}" for i, content in enumerate(unique_contents, 1))
        )

    context_text = "\n\n".join(context_parts) if context_parts else "No data was retrieved from the documents."

    prompt_content = (
        f"USER QUERY: {state.get('question')}\n\n"
        f"{context_text}\n\n"
        f"INSTRUCTION:\nProvide the best possible answer using only the data above."
    )
    response = llm.invoke([SystemMessage(content=get_fallback_response_prompt(state.get("skill_context", ""))), HumanMessage(content=prompt_content)])
    return {"messages": [response]}

def reflect_answer(state: AgentState, llm):
    draft = state["messages"][-1].content if state.get("messages") else ""
    tool_contents = []
    for msg in state.get("messages", []):
        if isinstance(msg, ToolMessage):
            tool_contents.append(msg.content)

    evidence_text = "\n\n".join(tool_contents[-6:]) if tool_contents else "No retrieved tool evidence is available."
    prompt_content = f"""Worker role: {state.get('worker_role', 'research_worker')}
Worker task: {state.get('question', '')}
Expected output: {state.get('expected_output', '')}

Compressed context:
{state.get('context_summary', '') or 'None'}

Retrieved evidence:
{evidence_text}

Draft answer:
{draft}

Return a structured reflection decision."""

    llm_with_structure = llm.with_config(temperature=0).with_structured_output(ReflectionDecision)
    with start_span("agent.reflect_answer", question=state.get("question", "")) as span:
        try:
            decision = llm_with_structure.invoke([
                SystemMessage(content=get_reflection_prompt(state.get("skill_context", ""))),
                HumanMessage(content=prompt_content),
            ])
            should_search = (
                bool(decision.should_search_again)
                and decision.evidence_score < config.MIN_EVIDENCE_SCORE
                and bool(decision.follow_up_queries or decision.missing_aspects or decision.unsupported_claims)
            )
            log_event(
                logger,
                "agent.reflect_answer",
                question=state.get("question"),
                worker_role=state.get("worker_role", "research_worker"),
                is_answer_complete=decision.is_answer_complete,
                evidence_score=decision.evidence_score,
                should_search_again=should_search,
                missing_aspects=decision.missing_aspects,
                unsupported_claims=decision.unsupported_claims,
                follow_up_queries=decision.follow_up_queries,
            )
            add_span_attributes(
                span,
                is_answer_complete=decision.is_answer_complete,
                evidence_score=float(decision.evidence_score),
                should_search_again=should_search,
                missing_count=len(decision.missing_aspects or []),
                unsupported_count=len(decision.unsupported_claims or []),
            )
            if should_search:
                follow_up_queries = decision.follow_up_queries or decision.missing_aspects
                reflection_message = HumanMessage(
                    content=(
                        "Missing or weakly supported aspects:\n"
                        + "\n".join(f"- {item}" for item in (decision.missing_aspects or []))
                        + "\n\nFocused follow-up retrieval queries:\n"
                        + "\n".join(f"- {query}" for query in follow_up_queries[:3])
                    )
                )
                return {
                    "messages": [reflection_message],
                    "reflection_should_search": True,
                    "reflection_count": 1,
                    "reflection_search_count": 1,
                }
            return {"reflection_should_search": False, "reflection_count": 1}
        except Exception as exc:
            log_event(
                logger,
                "agent.reflect_failed",
                question=state.get("question"),
                error=str(exc),
            )
            add_span_attributes(span, reflection_error=str(exc))
            return {"reflection_should_search": False, "reflection_count": 1}

def should_compress_context(state: AgentState) -> Command[Literal["compress_context", "orchestrator"]]:
    messages = state["messages"]

    new_ids: Set[str] = set()
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                if tc["name"] == "retrieve_parent_chunks":
                    raw = tc["args"].get("parent_id") or tc["args"].get("id") or tc["args"].get("ids") or []
                    if isinstance(raw, str):
                        new_ids.add(f"parent::{raw}")
                    else:
                        new_ids.update(f"parent::{r}" for r in raw)

                elif tc["name"] == "search_child_chunks":
                    query = tc["args"].get("query", "")
                    if query:
                        new_ids.add(f"search::{query}")
            break

    updated_ids = state.get("retrieval_keys", set()) | new_ids

    current_token_messages = estimate_context_tokens(messages)
    current_token_summary = estimate_context_tokens([HumanMessage(content=state.get("context_summary", ""))])
    current_tokens = current_token_messages + current_token_summary

    max_allowed = BASE_TOKEN_THRESHOLD + int(current_token_summary * TOKEN_GROWTH_FACTOR)

    goto = "compress_context" if current_tokens > max_allowed else "orchestrator"
    return Command(update={"retrieval_keys": updated_ids}, goto=goto)

def compress_context(state: AgentState, llm):
    messages = state["messages"]
    existing_summary = state.get("context_summary", "").strip()

    if not messages:
        return {}

    conversation_text = f"USER QUESTION:\n{state.get('question')}\n\nConversation to compress:\n\n"
    if existing_summary:
        conversation_text += f"[PRIOR COMPRESSED CONTEXT]\n{existing_summary}\n\n"

    for msg in messages[1:]:
        if isinstance(msg, AIMessage):
            tool_calls_info = ""
            if getattr(msg, "tool_calls", None):
                calls = ", ".join(f"{tc['name']}({tc['args']})" for tc in msg.tool_calls)
                tool_calls_info = f" | Tool calls: {calls}"
            conversation_text += f"[ASSISTANT{tool_calls_info}]\n{msg.content or '(tool call only)'}\n\n"
        elif isinstance(msg, ToolMessage):
            tool_name = getattr(msg, "name", "tool")
            conversation_text += f"[TOOL RESULT — {tool_name}]\n{msg.content}\n\n"

    with start_span("agent.context_compress", previous_message_count=len(messages)) as span:
        summary_response = llm.invoke([SystemMessage(content=get_context_compression_prompt(state.get("skill_context", ""))), HumanMessage(content=conversation_text)])
        new_summary = summary_response.content
        log_event(
            logger,
            "agent.context_compressed",
            question=state.get("question"),
            previous_message_count=len(messages),
        )
        add_span_attributes(span, summary_length=len(new_summary or ""))

    retrieved_ids: Set[str] = state.get("retrieval_keys", set())
    if retrieved_ids:
        parent_ids = sorted(r for r in retrieved_ids if r.startswith("parent::"))
        search_queries = sorted(r.replace("search::", "") for r in retrieved_ids if r.startswith("search::"))

        block = "\n\n---\n**Already executed (do NOT repeat):**\n"
        if parent_ids:
            block += "Parent chunks retrieved:\n" + "\n".join(f"- {p.replace('parent::', '')}" for p in parent_ids) + "\n"
        if search_queries:
            block += "Search queries already run:\n" + "\n".join(f"- {q}" for q in search_queries) + "\n"
        new_summary += block

        return {"context_summary": new_summary, "messages": [RemoveMessage(id=m.id) for m in messages[1:]]}

def collect_answer(state: AgentState):
    last_message = state["messages"][-1]
    is_valid = isinstance(last_message, AIMessage) and last_message.content and not last_message.tool_calls
    answer = last_message.content if is_valid else "Unable to generate an answer."
    log_event(
        logger,
        "agent.answer_collected",
        question=state["question"],
        answer_length=len(answer or ""),
    )
    return {
        "final_answer": answer,
        "agent_answers": [
            {
                "index": state["question_index"],
                "question": state["question"],
                "answer": answer,
                "worker_role": state.get("worker_role", "research_worker"),
                "tool_call_count": state.get("tool_call_count", 0),
                "reflection_count": state.get("reflection_count", 0),
                "reflection_search_count": state.get("reflection_search_count", 0),
            }
        ]
    }
# --- End of Agent Nodes---

def aggregate_answers(state: State, llm):
    if not state.get("agent_answers"):
        return {"messages": [AIMessage(content="No answers were generated.")]}

    sorted_answers = sorted(state["agent_answers"], key=lambda x: x["index"])

    formatted_answers = ""
    for i, ans in enumerate(sorted_answers, start=1):
        formatted_answers += (f"\nAnswer {i}:\n"f"{ans['answer']}\n")

    user_message = HumanMessage(content=f"""Original user question: {state["originalQuery"]}\nRetrieved answers:{formatted_answers}""")
    with start_span("agent.aggregate_answers", answer_count=len(sorted_answers)) as span:
        synthesis_response = llm.invoke([SystemMessage(content=get_aggregation_prompt(state.get("skill_context", ""))), user_message])
        log_event(
            logger,
            "agent.aggregate_answers",
            original_query=state["originalQuery"],
            answer_count=len(sorted_answers),
        )
        add_span_attributes(span, output_length=len(synthesis_response.content or ""))
        return {"messages": [AIMessage(content=synthesis_response.content)]}
