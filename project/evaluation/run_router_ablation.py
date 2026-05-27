import argparse
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from evaluation.light_answer_runner import run_light_answer_benchmark
from evaluation.report import render_markdown_report


def parse_args():
    parser = argparse.ArgumentParser(description="Run router ablation benchmark with custom retrieval modes.")
    parser.add_argument(
        "--dataset",
        default=str(Path(config.EVAL_DEFAULT_DATASET).with_name("public_light_pollution_router_eval_test.jsonl")),
    )
    parser.add_argument("--modes", nargs="+", default=["baseline_hybrid", "lightrag", "router"])
    parser.add_argument("--output-dir", default=config.EVAL_OUTPUT_DIR)
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--markdown-output", default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    reports = run_light_answer_benchmark(
        dataset_path=args.dataset,
        modes=args.modes,
        output_dir=args.output_dir,
        top_k=args.top_k,
    )
    markdown = render_markdown_report(reports)
    markdown_path = Path(args.markdown_output) if args.markdown_output else Path(args.output_dir) / "router_ablation.md"
    markdown_path.write_text(markdown, encoding="utf-8")

    payload = {
        "dataset": args.dataset,
        "modes": args.modes,
        "reports": [str(report) for report in reports],
        "markdown_output": str(markdown_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
