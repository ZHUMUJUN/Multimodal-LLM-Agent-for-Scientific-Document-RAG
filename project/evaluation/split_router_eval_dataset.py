import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def load_jsonl(path: str) -> list[dict]:
    records = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def save_jsonl(records: list[dict], path: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for item in records:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split router eval dataset into dev/test with per-type stratification.")
    parser.add_argument(
        "--input",
        default="project/evaluation/datasets/public_light_pollution_router_eval_30.jsonl",
    )
    parser.add_argument("--dev-output", default="project/evaluation/datasets/public_light_pollution_router_eval_dev.jsonl")
    parser.add_argument("--test-output", default="project/evaluation/datasets/public_light_pollution_router_eval_test.jsonl")
    parser.add_argument("--dev-ratio", type=float, default=0.4)
    parser.add_argument("--seed", type=int, default=2333)
    args = parser.parse_args()

    records = load_jsonl(args.input)
    rng = random.Random(args.seed)
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in records:
        key = (item.get("question_type", "unknown"), item.get("expected_route", ""))
        grouped[key].append(item)

    dev_records = []
    test_records = []
    for items in grouped.values():
        rng.shuffle(items)
        split_index = max(1, int(len(items) * args.dev_ratio)) if len(items) > 1 else 1
        dev_records.extend(items[:split_index])
        test_records.extend(items[split_index:])

    save_jsonl(dev_records, args.dev_output)
    save_jsonl(test_records, args.test_output)

    summary = {
        "input_count": len(records),
        "dev_count": len(dev_records),
        "test_count": len(test_records),
        "dev_output": args.dev_output,
        "test_output": args.test_output,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
