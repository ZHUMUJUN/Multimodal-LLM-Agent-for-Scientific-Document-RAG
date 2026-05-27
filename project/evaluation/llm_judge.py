from __future__ import annotations

import statistics
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field


class JudgeScore(BaseModel):
    method_accuracy: int = Field(ge=1, le=5, description="Accuracy of methods, modules, terminology, and architecture details.")
    dataset_completeness: int = Field(ge=1, le=5, description="Completeness of datasets, benchmarks, and experimental setup.")
    metric_correctness: int = Field(ge=1, le=5, description="Correctness of metrics, numeric results, and comparisons.")
    evidence_grounding: int = Field(ge=1, le=5, description="Whether claims are supported by retrieved contexts and ground truth.")
    chinese_clarity: int = Field(ge=1, le=5, description="Clarity and usefulness of the Chinese answer.")
    overall: float = Field(ge=1, le=5, description="Overall quality score from 1 to 5.")
    rationale: str = Field(default="", description="Brief explanation of the score.")


def _truncate(text: str, max_chars: int) -> str:
    text = text or ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def _judge_prompt() -> str:
    return """You are an expert evaluator for Chinese scientific-paper QA over retrieved English paper context.

Score the answer from 1 to 5 on these dimensions:
- method_accuracy: Are methods, modules, terminology, and architecture details accurate?
- dataset_completeness: Are datasets, benchmarks, and experimental setup covered when relevant?
- metric_correctness: Are metrics and numeric results correct when relevant?
- evidence_grounding: Are claims supported by retrieved_contexts and ground_truth rather than invented?
- chinese_clarity: Is the Chinese answer clear and useful?

Use retrieved_contexts as the evidence source and ground_truth as the reference answer. Penalize unsupported extra claims, missing requested aspects, wrong module names, and wrong numeric values.
Return only the structured score."""


def judge_case(llm, case_result: dict[str, Any]) -> dict[str, Any]:
    contexts = case_result.get("retrieved_contexts") or []
    context_text = "\n\n".join(
        f"[Context {idx}]\n{_truncate(context, 3000)}"
        for idx, context in enumerate(contexts[:5], start=1)
    ) or "No retrieved context was provided."
    payload = f"""Question:
{case_result.get("question", "")}

Answer:
{_truncate(case_result.get("answer", ""), 6000)}

Ground truth:
{_truncate(case_result.get("ground_truth", ""), 6000)}

Retrieved contexts:
{context_text}
"""
    scorer = llm.with_config(temperature=0).with_structured_output(JudgeScore)
    score = scorer.invoke([SystemMessage(content=_judge_prompt()), HumanMessage(content=payload)])
    return score.model_dump()


def run_judge(case_results: list[dict[str, Any]], llm) -> dict[str, Any]:
    eligible = [
        item
        for item in case_results
        if item.get("ground_truth", "").strip() and item.get("answer", "").strip()
    ]
    if not eligible:
        return {
            "enabled": False,
            "evaluated_cases": 0,
            "scores": {},
            "skipped_reason": "No cases with answer and ground_truth were found.",
        }

    judged_cases = []
    for item in eligible:
        try:
            score = judge_case(llm, item)
            judged_cases.append({"id": item.get("id", ""), **score})
        except Exception as exc:
            judged_cases.append({"id": item.get("id", ""), "error": f"{type(exc).__name__}: {exc}"})

    numeric_keys = [
        "method_accuracy",
        "dataset_completeness",
        "metric_correctness",
        "evidence_grounding",
        "chinese_clarity",
        "overall",
    ]
    scores = {}
    for key in numeric_keys:
        values = [float(item[key]) for item in judged_cases if isinstance(item.get(key), (int, float))]
        if values:
            scores[key] = round(statistics.mean(values), 4)

    return {
        "enabled": True,
        "evaluated_cases": len(eligible),
        "scores": scores,
        "cases": judged_cases,
    }
