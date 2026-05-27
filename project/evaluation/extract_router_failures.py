import argparse
import json
from pathlib import Path


def load_report(file_path: str) -> dict:
    with Path(file_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def classify_failure(case: dict) -> str:
    if case.get("route_hit") is False:
        return "rule_misroute"
    if not case.get("source_hit", True):
        return "retrieval_miss"
    if case.get("keyword_hit_rate", 1.0) < 0.5:
        return "answer_incomplete"
    if case.get("latency_ms", 0) > 5000:
        return "high_latency"
    return "manual_review"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract router benchmark bad cases into a markdown review file.")
    parser.add_argument("--report", required=True, help="Benchmark JSON report produced by light_answer_runner.")
    parser.add_argument("--output", default=None)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    payload = load_report(args.report)
    cases = payload.get("cases", [])
    failures = []
    for case in cases:
        if case.get("route_hit") is False or not case.get("source_hit", True) or case.get("keyword_hit_rate", 1.0) < 0.5:
            annotated = dict(case)
            annotated["failure_type"] = classify_failure(case)
            failures.append(annotated)

    failures = sorted(failures, key=lambda item: (item["failure_type"], item.get("latency_ms", 0)), reverse=True)[: args.limit]

    lines = [
        "# Router Failure Analysis",
        "",
        f"- Source report: `{args.report}`",
        f"- Failure count captured: `{len(failures)}`",
        "",
    ]
    for item in failures:
        lines.extend(
            [
                f"## {item.get('id')}",
                "",
                f"- Failure Type: `{item['failure_type']}`",
                f"- Question Type: `{item.get('question_type', 'unknown')}`",
                f"- Expected Route: `{item.get('expected_route', '')}`",
                f"- Resolved Mode: `{item.get('resolved_mode', '')}`",
                f"- Source Hit: `{item.get('source_hit')}`",
                f"- Keyword Hit Rate: `{item.get('keyword_hit_rate')}`",
                f"- Latency ms: `{item.get('latency_ms')}`",
                f"- Question: {item.get('question', '')}",
                f"- Answer: {item.get('answer', '').replace(chr(10), ' ')}",
                "",
            ]
        )

    output_path = Path(args.output) if args.output else Path(args.report).with_name("router_failures.md")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
