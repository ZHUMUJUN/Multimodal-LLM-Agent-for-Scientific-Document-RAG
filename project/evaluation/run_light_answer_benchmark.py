import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from evaluation.light_answer_runner import run_light_answer_benchmark


def parse_args():
    parser = argparse.ArgumentParser(description="Run a lightweight answer benchmark with Ragas evaluation.")
    parser.add_argument(
        "--dataset",
        default=str(Path(config.EVAL_DEFAULT_DATASET).with_name("public_light_pollution_answer_eval.jsonl")),
        help="Path to a JSONL answer benchmark dataset.",
    )
    parser.add_argument(
        "--mode",
        action="append",
        dest="modes",
        help="Retrieval mode to benchmark. Repeat for multiple modes.",
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
    return parser.parse_args()


def main():
    args = parse_args()
    modes = args.modes or ["baseline_hybrid"]
    generated = run_light_answer_benchmark(
        dataset_path=args.dataset,
        modes=modes,
        output_dir=args.output_dir,
        top_k=args.top_k,
    )
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
