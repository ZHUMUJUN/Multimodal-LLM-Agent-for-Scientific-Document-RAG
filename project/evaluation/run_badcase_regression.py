import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from evaluation.trajectory_eval import evaluate_run_trace


def _load_jsonl(path: str, limit: int | None = None) -> list[dict]:
    items = []
    data_path = Path(path)
    if not data_path.exists():
        return items
    for line in data_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        items.append(json.loads(line))
        if limit and len(items) >= limit:
            break
    return items


def run_badcase_regression(
    *,
    dataset_path: str = config.BADCASE_EVAL_DATASET_PATH,
    output_path: str | None = None,
    limit: int | None = None,
    dry_run: bool = False,
) -> dict:
    cases = _load_jsonl(dataset_path, limit=limit)
    report = {
        "dataset_path": dataset_path,
        "case_count": len(cases),
        "dry_run": dry_run,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": [],
    }
    if dry_run:
        report["results"] = [
            {
                "id": case.get("id"),
                "question": case.get("question"),
                "collection": case.get("collection"),
                "status": "loaded",
            }
            for case in cases
        ]
    else:
        from services.platform_service import PlatformService

        service = PlatformService()
        for case in cases:
            response = service.chat(
                collection=case.get("collection") or config.DEFAULT_COLLECTION,
                message=case.get("question") or "",
            )
            run_id = response.get("run_id")
            trajectory = service.evaluate_run_trace(run_id) if run_id else {}
            report["results"].append(
                {
                    "id": case.get("id"),
                    "source_run_id": case.get("source_run_id"),
                    "new_run_id": run_id,
                    "answer": response.get("answer"),
                    "reference_answer": case.get("reference_answer"),
                    "trajectory": trajectory,
                    "status": "completed",
                }
            )

    if output_path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run badcase regression cases through the Agent Harness.")
    parser.add_argument("--dataset", default=config.BADCASE_EVAL_DATASET_PATH)
    parser.add_argument("--output", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    report = run_badcase_regression(
        dataset_path=args.dataset,
        output_path=args.output or None,
        limit=args.limit or None,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
