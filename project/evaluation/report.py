import json
from pathlib import Path


def _load_report(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def render_markdown_report(report_paths: list[str | Path]) -> str:
    reports = [_load_report(path) for path in report_paths]
    if not reports:
        raise ValueError("At least one benchmark report is required.")

    lines = ["# Benchmark Report", ""]
    lines.append("| Mode | Cases | Avg Latency (ms) | Source Hit Rate | Avg Keyword Hit Rate | Avg Answer Length | Routing | Ragas |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    for report in reports:
        summary = report["summary"]
        ragas = summary.get("ragas", {})
        routing = summary.get("routing") or {}
        routing_text = "-"
        if routing:
            distribution = ", ".join(
                f"{mode}={count}" for mode, count in sorted((routing.get("route_distribution") or {}).items())
            )
            routing_text = "route_hit_rate={rate:.4f}; {distribution}".format(
                rate=routing.get("route_hit_rate", 0.0),
                distribution=distribution or "no-routes",
            )
        ragas_text = ", ".join(
            f"{key}={value:.4f}" for key, value in ragas.get("scores", {}).items() if isinstance(value, (int, float))
        ) or ragas.get("skipped_reason", "not-run")
        lines.append(
            "| {mode} | {case_count} | {avg_latency_ms} | {source_hit_rate} | {avg_keyword_hit_rate} | {avg_answer_length} | {routing_text} | {ragas_text} |".format(
                mode=report["retrieval_mode"],
                case_count=summary["case_count"],
                avg_latency_ms=summary["avg_latency_ms"],
                source_hit_rate=summary.get("source_hit_rate", "-"),
                avg_keyword_hit_rate=summary.get("avg_keyword_hit_rate", "-"),
                avg_answer_length=summary["avg_answer_length"],
                routing_text=routing_text,
                ragas_text=ragas_text,
            )
        )

    lines.extend(["", "## Question-Type Summary", ""])
    lines.append("| Mode | Question Type | Cases | Avg Latency (ms) | Source Hit Rate | Avg Keyword Hit Rate |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for report in reports:
        for question_type, summary in (report["summary"].get("question_type_summary") or {}).items():
            lines.append(
                "| {mode} | {question_type} | {case_count} | {avg_latency_ms} | {source_hit_rate} | {avg_keyword_hit_rate} |".format(
                    mode=report["retrieval_mode"],
                    question_type=question_type,
                    case_count=summary.get("case_count", 0),
                    avg_latency_ms=summary.get("avg_latency_ms", 0),
                    source_hit_rate=summary.get("source_hit_rate", 0),
                    avg_keyword_hit_rate=summary.get("avg_keyword_hit_rate", 0),
                )
            )

    lines.extend(["", "## Per-case Details", ""])
    for report in reports:
        lines.append(f"### {report['retrieval_mode']}")
        lines.append("")
        lines.append("| Case ID | Type | Question | Resolved Mode | Route Hit | Source Hit | Latency (ms) | Sources |")
        lines.append("| --- | --- | --- | --- | --- | --- | ---: | --- |")
        for case in report["cases"]:
            question = case["question"].replace("\n", " ").strip()
            sources = ", ".join(source for source in case["retrieved_sources"] if source) or "-"
            route_hit = case.get("route_hit")
            route_hit_text = "-" if route_hit is None else str(route_hit)
            lines.append(
                f"| {case['id']} | {case.get('question_type', '-')} | {question} | {case.get('resolved_mode', report['retrieval_mode'])} | {route_hit_text} | {case.get('source_hit', '-')} | {case['latency_ms']} | {sources} |"
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"
