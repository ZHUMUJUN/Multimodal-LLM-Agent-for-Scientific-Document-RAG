import json
from pathlib import Path
from typing import Any


def build_badcase_payload(
    run: dict[str, Any],
    *,
    note: str = "",
    expected_answer: str = "",
    tags: list[str] | None = None,
) -> tuple[dict, dict]:
    run_id = run.get("run_id")
    eval_case = {
        "id": f"badcase:{run_id}",
        "question": run.get("message"),
        "reference_answer": expected_answer,
        "collection": run.get("collection"),
        "source_run_id": run_id,
        "tags": tags or [],
        "metadata": {
            "note": note,
            "model_answer": run.get("answer"),
            "session_id": run.get("session_id"),
            "summary": run.get("summary") or {},
        },
    }
    payload = {
        "run_id": run_id,
        "session_id": run.get("session_id"),
        "collection": run.get("collection"),
        "question": run.get("message"),
        "answer": run.get("answer"),
        "expected_answer": expected_answer,
        "note": note,
        "tags": tags or [],
        "summary": run.get("summary") or {},
        "eval_case": eval_case,
    }
    return payload, eval_case


def append_badcase_files(
    payload: dict,
    eval_case: dict,
    *,
    dataset_path: str,
    eval_dataset_path: str,
) -> tuple[str, str]:
    output_path = Path(dataset_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.open("a", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str) + "\n"
    )

    eval_output_path = Path(eval_dataset_path)
    eval_output_path.parent.mkdir(parents=True, exist_ok=True)
    eval_output_path.open("a", encoding="utf-8").write(
        json.dumps(eval_case, ensure_ascii=False, sort_keys=True, default=str) + "\n"
    )
    return str(output_path), str(eval_output_path)
