import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from evaluation.runner import run_benchmark


def parse_args():
    parser = argparse.ArgumentParser(description="Run baseline vs rerank benchmark for the Agentic RAG platform.")
    parser.add_argument(
        "--dataset",
        default=config.EVAL_DEFAULT_DATASET,
        help="Path to a JSONL benchmark dataset.",
    )
    parser.add_argument(
        "--mode",
        action="append",
        dest="modes",
        help="Retrieval mode to benchmark. Repeat for multiple modes. Defaults to baseline_hybrid and hybrid_rerank.",
    )
    parser.add_argument(
        "--output-dir",
        default=config.EVAL_OUTPUT_DIR,
        help="Directory used to write benchmark JSON files.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="How many retrieved chunks to capture in benchmark output.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    modes = args.modes or ["baseline_hybrid", "hybrid_rerank"]
    generated = run_benchmark(
        dataset_path=args.dataset,
        modes=modes,
        output_dir=args.output_dir,
        top_k=args.top_k,
    )
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
