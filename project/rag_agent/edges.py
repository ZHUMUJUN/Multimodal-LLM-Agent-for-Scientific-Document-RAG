from typing import Literal
from langgraph.types import Send
from .graph_state import State, AgentState
import config

def route_after_rewrite(state: State) -> Literal["request_clarification", "plan_worker_tasks"]:
    if not state.get("questionIsClear", False):
        return "request_clarification"
    return "plan_worker_tasks"

def route_after_planner(state: State) -> Literal["agent"]:
    tasks = state.get("worker_tasks") or [
        {
            "role": "research_worker",
            "task": query,
            "search_query": query,
            "expected_output": "Answer the question using retrieved evidence.",
            "allowed_tools": [],
            "max_tool_calls": config.MAX_TOOL_CALLS,
        }
        for query in state.get("rewrittenQuestions", [])
    ]
    return [
        Send(
            "agent",
            {
                "question": task.get("task") or task.get("search_query") or "",
                "question_index": idx,
                "worker_role": task.get("role", "research_worker"),
                "search_query": task.get("search_query", ""),
                "expected_output": task.get("expected_output", ""),
                "allowed_tools": task.get("allowed_tools", []),
                "max_tool_calls": int(task.get("max_tool_calls", config.MAX_TOOL_CALLS) or config.MAX_TOOL_CALLS),
                "messages": [],
                "active_skill": state.get("active_skill", ""),
                "skill_context": state.get("skill_context", ""),
                "skill_allowed_tools": state.get("skill_allowed_tools", []),
            },
        )
        for idx, task in enumerate(tasks)
    ]
    
def route_after_orchestrator_call(state: AgentState) -> Literal["tool", "fallback_response", "reflect_answer", "collect_answer"]:
    iteration = state.get("iteration_count", 0)
    tool_count = state.get("tool_call_count", 0)
    max_tool_calls = int(state.get("max_tool_calls", config.MAX_TOOL_CALLS) or config.MAX_TOOL_CALLS)

    if iteration >= config.MAX_ITERATIONS or tool_count > max_tool_calls:
        return "fallback_response"

    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None) or []

    if not tool_calls:
        if config.REFLECTION_ENABLED and state.get("reflection_count", 0) < config.MAX_REFLECTION_ROUNDS:
            return "reflect_answer"
        return "collect_answer"
    
    return "tools"

def route_after_reflection(state: AgentState) -> Literal["orchestrator", "collect_answer"]:
    if state.get("reflection_should_search", False):
        return "orchestrator"
    return "collect_answer"
