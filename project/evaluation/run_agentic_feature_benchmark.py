import argparse
import json
import os
import shutil
import statistics
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from dotenv import load_dotenv

load_dotenv(PROJECT_DIR / ".env")

import config


def _load_cases(path: Path) -> list[dict]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    if not cases:
        raise ValueError(f"No cases found in {path}")
    return cases


def _keyword_coverage(answer: str, keywords: list[str]) -> tuple[float, list[str]]:
    if not keywords:
        return 0.0, []
    lowered = (answer or "").lower()
    hits = [keyword for keyword in keywords if keyword.lower() in lowered]
    return round(len(hits) / len(keywords), 4), hits


def _copy_qdrant_db(source: Path) -> Path:
    target = Path("/tmp") / f"agentic_feature_qdrant_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    for lock_name in [".lock", ".lock.stale"]:
        (target / lock_name).unlink(missing_ok=True)
    return target


def _apply_config(overrides: dict):
    for key, value in overrides.items():
        setattr(config, key, value)


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() == "true"


def _summarize_run(
    config_name: str,
    case_results: list[dict],
    ragas_summary: dict | None = None,
    judge_summary: dict | None = None,
) -> dict:
    latencies = [item["latency_ms"] for item in case_results]
    keyword_scores = [item["keyword_coverage"] for item in case_results]
    return {
        "config": config_name,
        "case_count": len(case_results),
        "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
        "max_latency_ms": round(max(latencies), 2) if latencies else 0,
        "avg_keyword_coverage": round(statistics.mean(keyword_scores), 4) if keyword_scores else 0,
        "avg_worker_count": round(statistics.mean(item.get("worker_count", 0) for item in case_results), 2),
        "avg_tool_call_count": round(statistics.mean(item.get("tool_call_count", 0) for item in case_results), 2),
        "reflection_count": sum(item.get("reflection_count", 0) for item in case_results),
        "reflection_search_count": sum(item.get("reflection_search_count", 0) for item in case_results),
        "selected_models": dict(Counter(item.get("selected_model") or "none" for item in case_results)),
        "worker_roles": dict(Counter(role for item in case_results for role in item.get("worker_roles", []))),
        "ragas": ragas_summary or {},
        "llm_judge": judge_summary or {},
    }


def _write_markdown_report(report_path: Path, payload: dict) -> None:
    lines = [
        "# Agentic RAG Feature Benchmark",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Dataset: `{payload['dataset_path']}`",
        "",
        "## Summary",
        "",
        "| Config | Cases | Avg latency ms | Max latency ms | Keyword coverage | Ragas | Judge overall | Avg workers | Avg tool calls | Reflections | Follow-up searches | Models |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in payload["summary"]:
        ragas = item.get("ragas", {})
        ragas_text = ", ".join(
            f"{key}={value:.4f}" for key, value in ragas.get("scores", {}).items() if isinstance(value, (int, float))
        ) or ragas.get("skipped_reason", "not-run")
        judge = item.get("llm_judge", {})
        judge_overall = judge.get("scores", {}).get("overall", "")
        lines.append(
            "| {config} | {case_count} | {avg_latency_ms} | {max_latency_ms} | {avg_keyword_coverage} | {ragas_text} | {judge_overall} | {avg_worker_count} | {avg_tool_call_count} | {reflection_count} | {reflection_search_count} | {models} |".format(
                config=item["config"],
                case_count=item["case_count"],
                avg_latency_ms=item["avg_latency_ms"],
                max_latency_ms=item["max_latency_ms"],
                avg_keyword_coverage=item["avg_keyword_coverage"],
                ragas_text=ragas_text,
                judge_overall=judge_overall,
                avg_worker_count=item["avg_worker_count"],
                avg_tool_call_count=item["avg_tool_call_count"],
                reflection_count=item["reflection_count"],
                reflection_search_count=item["reflection_search_count"],
                models=", ".join(f"{k}:{v}" for k, v in item["selected_models"].items()),
            )
        )

    lines.extend(["", "## LLM-as-Judge", ""])
    lines.append("| Config | Method | Dataset | Metrics | Grounding | Chinese | Overall |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for item in payload["summary"]:
        scores = item.get("llm_judge", {}).get("scores", {})
        lines.append(
            "| {config} | {method} | {dataset} | {metrics} | {grounding} | {chinese} | {overall} |".format(
                config=item["config"],
                method=scores.get("method_accuracy", ""),
                dataset=scores.get("dataset_completeness", ""),
                metrics=scores.get("metric_correctness", ""),
                grounding=scores.get("evidence_grounding", ""),
                chinese=scores.get("chinese_clarity", ""),
                overall=scores.get("overall", ""),
            )
        )

    lines.extend(["", "## Per-Case Results", ""])
    for run in payload["runs"]:
        lines.extend([f"### {run['config']}", ""])
        lines.append("| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |")
        lines.append("|---|---:|---:|---|---|---:|---:|---:|---|")
        for case in run["cases"]:
            lines.append(
                "| {case_id} | {latency_ms} | {coverage} | {hits} | {workers} | {tools} | {reflections} | {followups} | {model} |".format(
                    case_id=case["id"],
                    latency_ms=case["latency_ms"],
                    coverage=case["keyword_coverage"],
                    hits=", ".join(case["hit_keywords"]),
                    workers=", ".join(case.get("worker_roles", [])),
                    tools=case.get("tool_call_count", 0),
                    reflections=case.get("reflection_count", 0),
                    followups=case.get("reflection_search_count", 0),
                    model=case.get("selected_model") or "",
                )
            )
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Benchmark Reflection, Planner-Worker roles, and model routing.")
    parser.add_argument("--dataset", default=str(PROJECT_DIR / "evaluation" / "datasets" / "agentic_feature_eval.jsonl"))
    parser.add_argument("--output-dir", default=str(PROJECT_DIR / "evaluation" / "reports"))
    parser.add_argument("--copy-qdrant", action="store_true", default=True)
    parser.add_argument("--no-copy-qdrant", action="store_false", dest="copy_qdrant")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N cases.")
    parser.add_argument("--top-k", type=int, default=5, help="Retrieved contexts per case for Ragas.")
    parser.add_argument(
        "--configs",
        default="",
        help="Comma-separated config names to run. Defaults to all.",
    )
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cases = _load_cases(dataset_path)
    if args.limit > 0:
        cases = cases[: args.limit]

    if args.copy_qdrant:
        config.QDRANT_DB_PATH = str(_copy_qdrant_db(Path(config.QDRANT_DB_PATH)))

    # Import after QDRANT_DB_PATH is set because VectorDbManager has a config-based default.
    from evaluation.llm_judge import run_judge
    from evaluation.runner import _try_run_ragas
    from providers import ProviderFactory
    from retrieval import RetrievalPipeline
    from services.platform_service import PlatformService

    config.LIGHTRAG_ENABLED = _env_bool("LIGHTRAG_ENABLED", False)
    config.RETRIEVAL_MODE = os.environ.get("RETRIEVAL_MODE", config.RETRIEVAL_MODE)
    config.RERANKER_ENABLED = _env_bool("RERANKER_ENABLED", config.RERANKER_ENABLED)
    config.SKILLS_ENABLED = True
    config.LLM_MODEL = os.environ.get("LLM_MODEL", config.LLM_MODEL)
    config.LARGE_LLM_MODEL = os.environ.get("LARGE_LLM_MODEL", config.LARGE_LLM_MODEL)
    config.SMALL_LLM_MODEL = os.environ.get("SMALL_LLM_MODEL", config.SMALL_LLM_MODEL)

    run_configs = [
        ("skills_only", {"REFLECTION_ENABLED": False, "MULTI_AGENT_PLANNER_ENABLED": False, "MODEL_ROUTER_ENABLED": False}),
        ("plus_reflection", {"REFLECTION_ENABLED": True, "MULTI_AGENT_PLANNER_ENABLED": False, "MODEL_ROUTER_ENABLED": False}),
        ("plus_roles", {"REFLECTION_ENABLED": True, "MULTI_AGENT_PLANNER_ENABLED": True, "MODEL_ROUTER_ENABLED": False}),
        ("router_simple_cost", {"REFLECTION_ENABLED": False, "MULTI_AGENT_PLANNER_ENABLED": True, "MODEL_ROUTER_ENABLED": True}),
    ]
    selected_configs = {item.strip() for item in args.configs.split(",") if item.strip()}
    if selected_configs:
        run_configs = [(name, overrides) for name, overrides in run_configs if name in selected_configs]
        unknown_configs = selected_configs - {name for name, _ in run_configs}
        if unknown_configs:
            raise ValueError(f"Unknown configs: {', '.join(sorted(unknown_configs))}")

    print(
        "provider={provider} llm={llm} large={large} small={small} retrieval={retrieval} reranker={reranker} cases={cases} configs={configs}".format(
            provider=config.LLM_PROVIDER,
            llm=config.LLM_MODEL,
            large=config.LARGE_LLM_MODEL,
            small=config.SMALL_LLM_MODEL,
            retrieval=config.RETRIEVAL_MODE,
            reranker=config.RERANKER_ENABLED,
            cases=len(cases),
            configs=",".join(name for name, _ in run_configs),
        ),
        flush=True,
    )
    runs = []
    summaries = []
    for config_name, overrides in run_configs:
        _apply_config(overrides)
        service = PlatformService()
        case_results = []
        for case in cases:
            print(f"running config={config_name} case={case['id']}", flush=True)
            started = time.perf_counter()
            error = ""
            try:
                response = service.chat(
                    collection=case["collection"],
                    message=case["question"],
                    session_id=f"agentic-feature-{config_name}-{case['id']}",
                )
            except Exception as exc:
                response = {"answer": "", "worker_roles": []}
                error = f"{type(exc).__name__}: {exc}"
            latency_ms = round((time.perf_counter() - started) * 1000, 2)
            coverage, hits = _keyword_coverage(response.get("answer", ""), case.get("expected_keywords", []))
            retrieved_contexts: list[str] = []
            retrieved_sources: list[str] = []
            if not error:
                try:
                    rag_system = service._get_system(
                        case["collection"],
                        response.get("selected_model") or config.LLM_MODEL,
                    )
                    collection = service.vector_db.get_collection(rag_system.collection_name)
                    retrieved_docs = RetrievalPipeline(collection, rag_system.collection_name).search(
                        case["question"],
                        args.top_k,
                    )
                    retrieved_contexts = [doc.page_content for doc in retrieved_docs]
                    retrieved_sources = [doc.metadata.get("source", "") for doc in retrieved_docs]
                except Exception as exc:
                    error = f"{type(exc).__name__}: {exc}"
            case_results.append(
                {
                    "id": case["id"],
                    "collection": case["collection"],
                    "question": case["question"],
                    "ground_truth": case.get("ground_truth", ""),
                    "latency_ms": latency_ms,
                    "answer_length": len(response.get("answer", "") or ""),
                    "keyword_coverage": coverage,
                    "hit_keywords": hits,
                    "expected_keywords": case.get("expected_keywords", []),
                    "active_skill": response.get("active_skill"),
                    "selected_model": response.get("selected_model"),
                    "model_route_reasons": response.get("model_route_reasons", []),
                    "worker_roles": response.get("worker_roles", []),
                    "worker_count": response.get("worker_count", 0),
                    "tool_call_count": response.get("tool_call_count", 0),
                    "reflection_count": response.get("reflection_count", 0),
                    "reflection_search_count": response.get("reflection_search_count", 0),
                    "retrieved_contexts": retrieved_contexts,
                    "retrieved_sources": retrieved_sources,
                    "error": error,
                    "answer": response.get("answer", ""),
                }
            )
            if error:
                print(f"failed config={config_name} case={case['id']} error={error}", flush=True)
            else:
                print(
                    "finished config={config_name} case={case_id} latency_ms={latency_ms} coverage={coverage}".format(
                        config_name=config_name,
                        case_id=case["id"],
                        latency_ms=latency_ms,
                        coverage=coverage,
                    ),
                    flush=True,
                )
        print(f"running ragas config={config_name}", flush=True)
        ragas_summary = _try_run_ragas(
            case_results,
            llm=ProviderFactory.create_chat_model(),
            embeddings=service.vector_db._dense_embeddings,
        )
        print(f"finished ragas config={config_name} summary={ragas_summary}", flush=True)
        print(f"running llm_judge config={config_name}", flush=True)
        judge_summary = run_judge(case_results, llm=ProviderFactory.create_chat_model())
        print(f"finished llm_judge config={config_name} summary={judge_summary}", flush=True)
        runs.append({"config": config_name, "cases": case_results, "ragas": ragas_summary, "llm_judge": judge_summary})
        summaries.append(_summarize_run(config_name, case_results, ragas_summary, judge_summary))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset_path": str(dataset_path),
        "qdrant_db_path": config.QDRANT_DB_PATH,
        "summary": summaries,
        "runs": runs,
    }
    json_path = output_dir / f"agentic_feature_benchmark_{timestamp}.json"
    md_path = output_dir / f"agentic_feature_benchmark_{timestamp}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_markdown_report(md_path, payload)
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
