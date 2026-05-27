import json
from pathlib import Path


def _load_report(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def render_retrieval_markdown_report(report_paths: list[str | Path]) -> str:
    reports = [_load_report(path) for path in report_paths]
    if not reports:
        raise ValueError("At least one retrieval benchmark report is required.")

    lines = ["# Retrieval Benchmark Report", ""]
    lines.append("| Mode | Cases | Avg Latency (ms) | P95 Latency (ms) | Hit@K | Recall@K | MRR | MAP@K | nDCG@K | Avg Top1 Keyword Ratio |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    for report in reports:
        summary = report["summary"]
        lines.append(
            "| {mode} | {case_count} | {avg_latency_ms} | {p95_latency_ms} | {source_hit_rate} | {source_recall_at_k} | {mrr} | {map_at_k} | {ndcg_at_k} | {avg_top1_keyword_ratio} |".format(
                mode=report["retrieval_mode"],
                case_count=summary["case_count"],
                avg_latency_ms=summary["avg_latency_ms"],
                p95_latency_ms=summary["p95_latency_ms"],
                source_hit_rate=summary["source_hit_rate"],
                source_recall_at_k=summary.get("source_recall_at_k", "-"),
                mrr=summary["mrr"],
                map_at_k=summary.get("map_at_k", "-"),
                ndcg_at_k=summary.get("ndcg_at_k", "-"),
                avg_top1_keyword_ratio=summary["avg_top1_keyword_ratio"],
            )
        )

    if len(reports) >= 2:
        baseline = reports[0]["summary"]
        lines.extend(["", "## Delta vs First Report", ""])
        lines.append("| Mode | Hit@K Δ | Recall@K Δ | MRR Δ | MAP@K Δ | nDCG@K Δ | Latency Δ (ms) |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for report in reports[1:]:
            summary = report["summary"]
            lines.append(
                "| {mode} | {hit_delta:+.4f} | {recall_delta:+.4f} | {mrr_delta:+.4f} | {map_delta:+.4f} | {ndcg_delta:+.4f} | {latency_delta:+.2f} |".format(
                    mode=report["retrieval_mode"],
                    hit_delta=summary["source_hit_rate"] - baseline["source_hit_rate"],
                    recall_delta=summary.get("source_recall_at_k", 0) - baseline.get("source_recall_at_k", 0),
                    mrr_delta=summary["mrr"] - baseline["mrr"],
                    map_delta=summary.get("map_at_k", 0) - baseline.get("map_at_k", 0),
                    ndcg_delta=summary.get("ndcg_at_k", 0) - baseline.get("ndcg_at_k", 0),
                    latency_delta=summary["avg_latency_ms"] - baseline["avg_latency_ms"],
                )
            )

    lines.extend(["", "## Per-case Details", ""])
    for report in reports:
        lines.append(f"### {report['retrieval_mode']}")
        lines.append("")
        lines.append("| Case ID | Question | Hit | First Hit Rank | Recall@K | AP@K | nDCG@K | Top1 Keyword Ratio | Retrieved Sources |")
        lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |")
        for case in report["cases"]:
            retrieved_sources = ", ".join(item["source"] for item in case["retrieved"] if item["source"]) or "-"
            question = case["question"].replace("\n", " ").strip()
            hit_rank = case["first_hit_rank"] if case["first_hit_rank"] is not None else "-"
            lines.append(
                f"| {case['id']} | {question} | {case['source_hit']} | {hit_rank} | {case.get('source_recall_at_k', '-')} | {case.get('average_precision_at_k', '-')} | {case.get('ndcg_at_k', '-')} | {case['top1_keyword_ratio']} | {retrieved_sources} |"
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"
