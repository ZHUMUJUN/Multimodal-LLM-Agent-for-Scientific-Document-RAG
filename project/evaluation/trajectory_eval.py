import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from core.memory_store import MemoryStore


def _payload(event: dict) -> dict:
    return event.get("payload") or {}


def evaluate_run_trace(trace: dict[str, Any]) -> dict[str, Any]:
    run = trace.get("run") or {}
    events = trace.get("events") or []
    event_names = [event.get("event", "") for event in events]
    event_counts = Counter(event_names)

    policy_events = [event for event in events if event.get("event") == "tool_policy.decision"]
    blocked_tools = [
        event for event in policy_events
        if _payload(event).get("allowed") is False
    ]
    error_events = [
        event for event in events
        if any(token in (event.get("event") or "") for token in ("failed", "error"))
    ]
    worker_roles = []
    for event in events:
        if event.get("event") == "agent.worker_tasks_planned":
            roles = _payload(event).get("worker_roles") or []
            worker_roles.extend(roles)

    summary = run.get("summary") or {}
    tool_call_count = int(summary.get("tool_call_count") or len(policy_events))
    answer = run.get("answer") or ""

    checks = {
        "has_query_rewrite": event_counts["agent.query_rewrite"] > 0,
        "has_worker_planning": event_counts["agent.worker_tasks_planned"] > 0,
        "has_memory_context": event_counts["memory.context_loaded"] > 0,
        "has_tool_policy": len(policy_events) > 0,
        "has_worker_tool_policy_context": any(_payload(event).get("worker_role") for event in policy_events),
        "has_tool_activity": tool_call_count > 0,
        "has_reflection": event_counts["agent.reflect_answer"] > 0,
        "has_aggregation": event_counts["agent.aggregate_answers"] > 0,
        "has_nonempty_answer": len(answer.strip()) >= 20,
        "has_errors": len(error_events) > 0,
        "has_blocked_tools": len(blocked_tools) > 0,
    }

    score = 1.0
    penalties = []
    if not checks["has_query_rewrite"]:
        score -= 0.12
        penalties.append("missing query rewrite")
    if not checks["has_worker_planning"]:
        score -= 0.12
        penalties.append("missing worker planning")
    if not checks["has_tool_policy"]:
        score -= 0.10
        penalties.append("missing tool policy audit")
    if checks["has_tool_policy"] and not checks["has_worker_tool_policy_context"]:
        score -= 0.05
        penalties.append("tool policy audit missing worker context")
    if not checks["has_tool_activity"]:
        score -= 0.10
        penalties.append("no tool activity")
    if checks["has_blocked_tools"]:
        score -= min(0.20, 0.05 * len(blocked_tools))
        penalties.append("blocked tool calls present")
    if checks["has_errors"]:
        score -= min(0.30, 0.10 * len(error_events))
        penalties.append("runtime error events present")
    if not checks["has_nonempty_answer"]:
        score -= 0.15
        penalties.append("empty or very short answer")

    return {
        "run_id": run.get("run_id"),
        "status": run.get("status"),
        "collection": run.get("collection"),
        "active_skill": run.get("active_skill"),
        "model": run.get("model"),
        "resolved_retrieval_mode": run.get("resolved_retrieval_mode"),
        "trajectory_score": round(max(0.0, min(1.0, score)), 3),
        "checks": checks,
        "penalties": penalties,
        "event_counts": dict(event_counts),
        "worker_roles": worker_roles,
        "tool_call_count": tool_call_count,
        "blocked_tool_count": len(blocked_tools),
        "error_event_count": len(error_events),
    }


def evaluate_run(memory_db_path: str, run_id: str) -> dict[str, Any]:
    store = MemoryStore(memory_db_path)
    try:
        return evaluate_run_trace(store.export_run(run_id))
    finally:
        store.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate one persisted agent trajectory.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--memory-db", default=config.MEMORY_DB_PATH)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    result = evaluate_run(args.memory_db, args.run_id)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
