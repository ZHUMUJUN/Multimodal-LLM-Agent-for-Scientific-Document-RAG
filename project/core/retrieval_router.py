import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    mode: str
    question_type: str
    confidence: float
    reasons: list[str]


RELATION_PATTERNS = (
    ("relation", re.compile(r"(关系|关联|联系|链路|路径|上下游)"), 2),
    ("comparison", re.compile(r"(比较|对比|差异|区别|共同点|分别|各自)"), 2),
    ("causality", re.compile(r"(影响|如何影响|为什么|为何|导致|原因|后果)"), 1),
    ("cross_doc", re.compile(r"(哪两篇|哪两个|哪些文档|哪篇.*哪篇|一个.*另一个|同时提到|串起来)"), 2),
    ("multi_clause", re.compile(r"(并且|以及|同时|再|然后|一方面|另一方面)"), 1),
)


def route_question(question: str) -> RouteDecision:
    text = (question or "").strip()
    if not text:
        return RouteDecision(
            mode="baseline_hybrid",
            question_type="single_hop",
            confidence=0.5,
            reasons=["empty_question"],
        )

    score = 0
    reasons: list[str] = []
    for label, pattern, weight in RELATION_PATTERNS:
        if pattern.search(text):
            score += weight
            reasons.append(label)

    # Questions that mention multiple cited works or entities plus a connective are more likely
    # to require cross-document reasoning rather than local chunk lookup.
    if len(re.findall(r"(Gaia|Hipparcos|Paranal|space objects|skyglow|biodiversity|anthropogenic photons)", text)) >= 2:
        if re.search(r"(和|与|及|以及|比较|对比|区别|共同|关系)", text):
            score += 1
            reasons.append("multi_entity")

    if score >= 2:
        return RouteDecision(
            mode="lightrag",
            question_type="multi_hop_relation",
            confidence=min(0.95, 0.55 + score * 0.08),
            reasons=reasons or ["heuristic_multi_hop"],
        )

    return RouteDecision(
        mode="baseline_hybrid",
        question_type="single_hop",
        confidence=max(0.55, 0.8 - score * 0.1),
        reasons=reasons or ["local_fact_lookup"],
    )
