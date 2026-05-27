import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from evaluation.retrieval_report import render_retrieval_markdown_report


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a markdown report from retrieval benchmark JSON files.")
    parser.add_argument("reports", nargs="+", help="One or more retrieval benchmark JSON report paths.")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional markdown output path. Prints to stdout when omitted.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    markdown = render_retrieval_markdown_report(args.reports)
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
        print(args.output)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
