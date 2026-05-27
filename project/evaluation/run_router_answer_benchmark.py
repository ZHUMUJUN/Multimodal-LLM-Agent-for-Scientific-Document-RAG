import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from evaluation.light_answer_runner import run_light_answer_benchmark
from evaluation.report import render_markdown_report


def parse_args():
    parser = argparse.ArgumentParser(description="Run baseline vs LightRAG vs router answer benchmark.")
    parser.add_argument(
        "--dataset",
        default=str(Path(config.EVAL_DEFAULT_DATASET).with_name("public_light_pollution_router_eval_30.jsonl")),
        help="Path to a JSONL answer benchmark dataset.",
    )
    parser.add_argument(
        "--output-dir",
        default=config.EVAL_OUTPUT_DIR,
        help="Directory used to write benchmark JSON files.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="How many retrieved chunks to use for answer generation.",
    )
    parser.add_argument(
        "--markdown-output",
        default=None,
        help="Optional markdown output path. Defaults to router_compare_<timestamp>.md under output-dir.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    reports = run_light_answer_benchmark(
        dataset_path=args.dataset,
        modes=["baseline_hybrid", "lightrag", "router"],
        output_dir=args.output_dir,
        top_k=args.top_k,
    )
    markdown = render_markdown_report(reports)

    if args.markdown_output:
        output_path = Path(args.markdown_output)
    else:
        first_report = Path(reports[0])
        run_suffix = first_report.stem.split("_")[-1]
        output_path = Path(args.output_dir) / f"router_compare_{run_suffix}.md"

    output_path.write_text(markdown, encoding="utf-8")
    for report in reports:
        print(report)
    print(output_path)


if __name__ == "__main__":
    main()
