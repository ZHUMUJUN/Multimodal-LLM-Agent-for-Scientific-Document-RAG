import logging
import sys
import tempfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from core.logging_utils import log_event, run_context, set_event_sink
from core.memory_store import MemoryStore
from core.tool_policy import ToolPolicy, set_approval_handlers, tool_execution_context
from core.workspace_sandbox import SandboxViolation, WorkspaceSandbox
from core.worker_registry import WorkerRegistry
from evaluation.badcase_utils import append_badcase_files, build_badcase_payload
from evaluation.run_badcase_regression import run_badcase_regression
from evaluation.skill_regression import run_skill_regression
from evaluation.trajectory_eval import evaluate_run_trace


logger = logging.getLogger("harness_smoke")


def test_memory_trace_and_eval() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = MemoryStore(str(Path(temp_dir) / "memory.db"))
        set_event_sink(store.record_logged_event)
        run_id = store.start_run(
            session_id="smoke-session",
            collection="default",
            message="Explain the method and benchmark.",
            active_skill="paper_qa_zh",
            model="smoke-model",
            retrieval_mode="baseline_hybrid",
        )

        with run_context(run_id):
            log_event(logger, "agent.query_rewrite", original_query="Explain the method and benchmark.")
            log_event(
                logger,
                "agent.worker_tasks_planned",
                worker_roles=["method_worker", "data_eval_worker"],
                task_count=2,
            )
            log_event(logger, "memory.context_loaded", memory_count=1, scopes=["session:smoke-session"])
            log_event(
                logger,
                "tool_policy.decision",
                tool_name="search_child_chunks",
                worker_role="method_worker",
                allowed_tools=["search_child_chunks"],
                allowed=True,
                risk="low",
            )
            log_event(logger, "agent.reflect_answer", evidence_score=0.9, should_search_again=False)
            log_event(logger, "agent.aggregate_answers", answer_count=2)

        store.write_memory(
            scope="session:smoke-session",
            key="preferred_answer_style",
            value="Concise, evidence-grounded Chinese answer.",
            importance=0.9,
            source_run_id=run_id,
        )
        assert store.search_memories("Chinese", scope="session:smoke-session")
        store.write_memory(scope="session:smoke-session", key="short_lived", value="expire me", importance=0.0, ttl_seconds=1)

        store.finish_run(
            run_id,
            status="completed",
            answer="This is a sufficiently long smoke-test answer grounded in retrieved evidence.",
            summary={"tool_call_count": 1, "worker_count": 2},
            resolved_retrieval_mode="baseline_hybrid",
        )
        trace = store.export_run(run_id)
        result = evaluate_run_trace(trace)
        assert result["trajectory_score"] >= 0.8, result
        assert result["checks"]["has_tool_policy"], result
        deleted = store.prune_memories(expired_only=False, max_importance=0.1)
        assert deleted >= 1
        store.close()
        set_event_sink(None)


def test_tool_policy_blocks_high_risk_by_default() -> None:
    old_crag_enabled = config.CRAG_ENABLED
    old_allow_high_risk = config.TOOL_POLICY_ALLOW_HIGH_RISK
    try:
        config.CRAG_ENABLED = True
        config.TOOL_POLICY_ALLOW_HIGH_RISK = False
        decision = ToolPolicy().evaluate("web_search", {"query": "latest agent harness"})
        assert not decision.allowed
        assert decision.risk == "high"
    finally:
        config.CRAG_ENABLED = old_crag_enabled
        config.TOOL_POLICY_ALLOW_HIGH_RISK = old_allow_high_risk


def test_tool_approval_queue() -> None:
    old_crag_enabled = config.CRAG_ENABLED
    old_allow_high_risk = config.TOOL_POLICY_ALLOW_HIGH_RISK
    old_approval_enabled = config.TOOL_APPROVAL_ENABLED
    try:
        config.CRAG_ENABLED = True
        config.TOOL_POLICY_ALLOW_HIGH_RISK = False
        config.TOOL_APPROVAL_ENABLED = True
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(str(Path(temp_dir) / "memory.db"))
            set_approval_handlers(
                checker=store.is_tool_approved,
                requester=lambda approval_id, run_id, tool_name, risk, args, reason: store.create_tool_approval(
                    approval_id=approval_id,
                    run_id=run_id,
                    tool_name=tool_name,
                    risk=risk,
                    args=args,
                    reason=reason,
                ),
            )
            run_id = store.start_run(session_id="approval-smoke", collection="default", message="search web")
            with run_context(run_id):
                decision = ToolPolicy().evaluate("web_search", {"query": "latest harness"})
            assert not decision.allowed
            assert decision.reason.startswith("pending_approval:"), decision
            approval_id = decision.reason.split(":", 1)[1]
            assert store.get_tool_approval(approval_id)["status"] == "pending"
            store.resolve_tool_approval(approval_id, status="approved", resolved_by="smoke")
            with run_context(run_id):
                approved = ToolPolicy().evaluate("web_search", {"query": "latest harness"})
            assert approved.allowed
            assert approved.reason.startswith("approved:"), approved
            store.close()
            set_approval_handlers(checker=None, requester=None)
    finally:
        config.CRAG_ENABLED = old_crag_enabled
        config.TOOL_POLICY_ALLOW_HIGH_RISK = old_allow_high_risk
        config.TOOL_APPROVAL_ENABLED = old_approval_enabled


def test_tool_policy_enforces_worker_allowed_tools() -> None:
    with tool_execution_context(worker_role="method_worker", allowed_tools=["search_child_chunks"]):
        decision = ToolPolicy().evaluate("retrieve_parent_chunks", {"parent_id": "p1"})
    assert not decision.allowed
    assert "method_worker" in decision.reason


def test_workspace_sandbox_blocks_sensitive_paths() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        allowed = root / "allowed.txt"
        blocked = root / ".env"
        allowed.write_text("ok", encoding="utf-8")
        blocked.write_text("SECRET=1", encoding="utf-8")
        sandbox = WorkspaceSandbox(read_roots=[str(root)], write_root=str(root / "workspace"), blocked_patterns=[".env"])
        assert sandbox.resolve_read_path(str(allowed), must_exist=True).name == "allowed.txt"
        write_target = sandbox.resolve_write_path("reports/out.txt")
        assert str(write_target).startswith(str(root / "workspace"))
        try:
            sandbox.resolve_read_path(str(blocked), must_exist=True)
        except SandboxViolation:
            pass
        else:
            raise AssertionError("sandbox should block .env")


def test_badcase_eval_case_export() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        run = {
            "run_id": "run-smoke",
            "session_id": "s1",
            "collection": "default",
            "message": "question?",
            "answer": "wrong answer",
            "summary": {"tool_call_count": 1},
        }
        payload, eval_case = build_badcase_payload(run, note="missed evidence", expected_answer="right answer", tags=["smoke"])
        dataset_path, eval_path = append_badcase_files(
            payload,
            eval_case,
            dataset_path=str(Path(temp_dir) / "badcases.jsonl"),
            eval_dataset_path=str(Path(temp_dir) / "badcase_eval.jsonl"),
        )
        assert Path(dataset_path).read_text(encoding="utf-8").strip()
        assert '"reference_answer": "right answer"' in Path(eval_path).read_text(encoding="utf-8")
        report = run_badcase_regression(dataset_path=eval_path, dry_run=True)
        assert report["case_count"] == 1
        assert report["results"][0]["status"] == "loaded"


def test_worker_registry_loads_specs() -> None:
    registry = WorkerRegistry(config.WORKER_SPECS_DIR)
    specs = registry.specs
    assert "method_worker" in specs
    assert "data_eval_worker" in specs
    assert registry.select_role("Compare method architecture and benchmark result", "literature_compare") == "comparison_worker"
    assert registry.select_role("What is this paper about?", "paper_qa_zh") == "research_worker"
    assert registry.select_role("Show benchmark metrics", "rag_eval") == "data_eval_worker"
    assert registry.expected_output_for_role("method_worker")


def test_skill_regression() -> None:
    result = run_skill_regression()
    assert result["ok"], result
    assert result["skill_count"] >= 1


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    test_memory_trace_and_eval()
    test_tool_policy_blocks_high_risk_by_default()
    test_tool_approval_queue()
    test_tool_policy_enforces_worker_allowed_tools()
    test_workspace_sandbox_blocks_sensitive_paths()
    test_badcase_eval_case_export()
    test_worker_registry_loads_specs()
    test_skill_regression()
    print("harness smoke tests passed")


if __name__ == "__main__":
    main()
