import json

from pydantic import BaseModel, Field

import config


class BenchmarkCase(BaseModel):
    case_id: str = Field(alias="id")
    collection: str = Field(default=config.DEFAULT_COLLECTION)
    question: str
    ground_truth: str = ""
    expected_sources: list[str] = Field(default_factory=list)
    expected_keywords: list[str] = Field(default_factory=list)
    question_type: str = "single_hop"
    expected_route: str = ""
    notes: str = ""

    model_config = {"populate_by_name": True}


def load_cases(dataset_path: str) -> list[BenchmarkCase]:
    cases: list[BenchmarkCase] = []
    with open(dataset_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            payload = json.loads(line)
            cases.append(BenchmarkCase.model_validate(payload))
    if not cases:
        raise ValueError(f"No benchmark cases found in dataset: {dataset_path}")
    return cases
