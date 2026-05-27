from dataclasses import dataclass, field

import config


@dataclass(frozen=True)
class ModelRouteDecision:
    selected_model: str
    complexity: str
    estimated_cost_level: str
    reasons: list[str] = field(default_factory=list)


def route_model(
    question: str,
    skill_name: str | None = None,
    retrieval_mode: str | None = None,
    reflection_enabled: bool | None = None,
) -> ModelRouteDecision:
    """Choose an LLM for the request.

    v1 is deliberately conservative: structured-output-heavy paths stay on
    the large model, while simple non-skill requests can use the small model
    only when MODEL_ROUTER_ENABLED=true.
    """
    if not config.MODEL_ROUTER_ENABLED:
        return ModelRouteDecision(
            selected_model=config.LLM_MODEL,
            complexity="default",
            estimated_cost_level="default",
            reasons=["model_router_disabled"],
        )

    text = (question or "").strip()
    reasons: list[str] = []

    if reflection_enabled:
        reasons.append("reflection_enabled")
    if skill_name in {"paper_qa_zh", "literature_compare"}:
        reasons.append(f"skill:{skill_name}")
    if len(text) > 120:
        reasons.append("long_query")
    if any(token in text for token in ["比较", "对比", "创新", "数据集", "指标", "背景", "why", "compare", "dataset", "metric"]):
        reasons.append("multi_aspect_or_research_query")

    if reasons:
        return ModelRouteDecision(
            selected_model=config.LARGE_LLM_MODEL,
            complexity="high",
            estimated_cost_level="high",
            reasons=reasons,
        )

    if retrieval_mode == "lightrag":
        return ModelRouteDecision(
            selected_model=config.SMALL_LLM_MODEL,
            complexity="medium",
            estimated_cost_level="low",
            reasons=["lightrag_handles_retrieval"],
        )

    return ModelRouteDecision(
        selected_model=config.SMALL_LLM_MODEL,
        complexity="low",
        estimated_cost_level="low",
        reasons=["simple_query"],
    )
