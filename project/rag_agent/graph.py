from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode
from functools import partial
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import logging

import config as app_config
from core.logging_utils import log_event
from core.tool_policy import tool_execution_context
from .graph_state import State
from .nodes import *
from .edges import *

logger = logging.getLogger(__name__)
_tool_executor = ThreadPoolExecutor(max_workers=max(1, app_config.WORKER_MAX_CONCURRENCY))


def create_agent_graph(llm, tools_list):
    llm_with_tools = llm.bind_tools(tools_list)
    tool_node = ToolNode(tools_list)

    def policy_tool_node(state, config=None):
        worker_role = state.get("worker_role", "research_worker")
        allowed_tools = state.get("allowed_tools", [])
        max_attempts = max(1, app_config.WORKER_MAX_RETRIES + 1)
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                with tool_execution_context(worker_role=worker_role, allowed_tools=allowed_tools):
                    future = _tool_executor.submit(tool_node.invoke, state, config=config)
                    result = future.result(timeout=app_config.WORKER_TIMEOUT_SECONDS)
                if attempt > 1:
                    log_event(logger, "worker.tool_node.retry_recovered", worker_role=worker_role, attempt=attempt)
                return result
            except FutureTimeoutError as exc:
                last_error = exc
                log_event(
                    logger,
                    "worker.tool_node.timeout",
                    worker_role=worker_role,
                    attempt=attempt,
                    timeout_seconds=app_config.WORKER_TIMEOUT_SECONDS,
                )
            except Exception as exc:
                last_error = exc
                log_event(
                    logger,
                    "worker.tool_node.failed",
                    worker_role=worker_role,
                    attempt=attempt,
                    error=str(exc),
                )
            if attempt < max_attempts:
                log_event(logger, "worker.tool_node.retrying", worker_role=worker_role, next_attempt=attempt + 1)
        raise RuntimeError(f"Tool node failed after {max_attempts} attempts for {worker_role}: {last_error}")

    checkpointer = InMemorySaver()

    print("Compiling agent graph...")
    agent_builder = StateGraph(AgentState)
    agent_builder.add_node("orchestrator", partial(orchestrator, llm_with_tools=llm_with_tools))
    agent_builder.add_node("tools", policy_tool_node)
    agent_builder.add_node("compress_context", partial(compress_context, llm=llm))
    agent_builder.add_node("fallback_response", partial(fallback_response, llm=llm))
    agent_builder.add_node("reflect_answer", partial(reflect_answer, llm=llm))
    agent_builder.add_node(should_compress_context) 
    agent_builder.add_node(collect_answer)
    
    agent_builder.add_edge(START, "orchestrator")    
    agent_builder.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator_call,
        {
            "tools": "tools",
            "fallback_response": "fallback_response",
            "reflect_answer": "reflect_answer",
            "collect_answer": "collect_answer",
        },
    )
    agent_builder.add_conditional_edges("reflect_answer", route_after_reflection, {"orchestrator": "orchestrator", "collect_answer": "collect_answer"})
    agent_builder.add_edge("tools", "should_compress_context")
    agent_builder.add_edge("compress_context", "orchestrator")
    agent_builder.add_edge("fallback_response", "collect_answer")
    agent_builder.add_edge("collect_answer", END)
    
    agent_subgraph = agent_builder.compile()
    
    graph_builder = StateGraph(State)
    graph_builder.add_node("summarize_history", partial(summarize_history, llm=llm))
    graph_builder.add_node("rewrite_query", partial(rewrite_query, llm=llm))
    graph_builder.add_node(plan_worker_tasks)
    graph_builder.add_node(request_clarification)
    graph_builder.add_node("agent", agent_subgraph)
    graph_builder.add_node("aggregate_answers", partial(aggregate_answers, llm=llm))
    
    graph_builder.add_edge(START, "summarize_history")
    graph_builder.add_edge("summarize_history", "rewrite_query")
    graph_builder.add_conditional_edges("rewrite_query", route_after_rewrite, {"request_clarification": "request_clarification", "plan_worker_tasks": "plan_worker_tasks"})
    graph_builder.add_conditional_edges("plan_worker_tasks", route_after_planner)
    graph_builder.add_edge("request_clarification", "rewrite_query")
    graph_builder.add_edge(["agent"], "aggregate_answers")
    graph_builder.add_edge("aggregate_answers", END)

    agent_graph = graph_builder.compile(checkpointer=checkpointer, interrupt_before=["request_clarification"])

    print("✓ Agent graph compiled successfully.")
    return agent_graph
