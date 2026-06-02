from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class WorkerSpec:
    role: str
    description: str = ""
    triggers: list[str] = field(default_factory=list)
    skill_affinity: list[str] = field(default_factory=list)
    default_for_skills: list[str] = field(default_factory=list)
    expected_output: str = "Answer the assigned question using retrieved evidence."
    allowed_tools: list[str] = field(default_factory=list)
    max_tool_calls: int = 8
    priority: int = 0


class WorkerRegistry:
    """Loads planner worker definitions from YAML files."""

    def __init__(self, specs_dir: str):
        self.specs_dir = Path(specs_dir)
        self._specs: dict[str, WorkerSpec] = {}
        self.reload()

    def reload(self) -> None:
        specs: dict[str, WorkerSpec] = {}
        if self.specs_dir.exists():
            for path in sorted(self.specs_dir.glob("*.yaml")):
                with path.open("r", encoding="utf-8") as handle:
                    data = yaml.safe_load(handle) or {}
                role = str(data.get("role") or path.stem).strip()
                if not role:
                    continue
                specs[role] = WorkerSpec(
                    role=role,
                    description=str(data.get("description") or ""),
                    triggers=[str(item).lower() for item in data.get("triggers", [])],
                    skill_affinity=[str(item) for item in data.get("skill_affinity", [])],
                    default_for_skills=[str(item) for item in data.get("default_for_skills", [])],
                    expected_output=str(data.get("expected_output") or "Answer the assigned question using retrieved evidence."),
                    allowed_tools=[str(item) for item in data.get("allowed_tools", [])],
                    max_tool_calls=int(data.get("max_tool_calls", 8)),
                    priority=int(data.get("priority", 0)),
                )
        self._specs = specs

    @property
    def specs(self) -> dict[str, WorkerSpec]:
        return dict(self._specs)

    def get(self, role: str) -> WorkerSpec | None:
        return self._specs.get(role)

    def list_specs(self) -> list[dict]:
        return [
            {
                "role": spec.role,
                "description": spec.description,
                "triggers": spec.triggers,
                "skill_affinity": spec.skill_affinity,
                "default_for_skills": spec.default_for_skills,
                "expected_output": spec.expected_output,
                "allowed_tools": spec.allowed_tools,
                "max_tool_calls": spec.max_tool_calls,
                "priority": spec.priority,
            }
            for spec in sorted(self._specs.values(), key=lambda item: item.role)
        ]

    def select_role(self, query: str, active_skill: str = "") -> str:
        if not self._specs:
            return "research_worker"

        text = (query or "").lower()
        best_role = "research_worker" if "research_worker" in self._specs else next(iter(self._specs))
        best_score = 0
        for spec in self._specs.values():
            trigger_hits = sum(1 for trigger in spec.triggers if trigger and trigger in text)
            if trigger_hits == 0:
                continue
            score = trigger_hits * 10 + spec.priority
            if active_skill and active_skill in spec.skill_affinity:
                score += 2
            if score > best_score:
                best_score = score
                best_role = spec.role
        if best_score > 0:
            return best_role

        for spec in self._specs.values():
            if active_skill and active_skill in spec.default_for_skills:
                return spec.role
        return best_role

    def expected_output_for_role(self, role: str) -> str:
        spec = self.get(role)
        if spec:
            return spec.expected_output
        fallback = self.get("research_worker")
        return fallback.expected_output if fallback else "Answer the assigned question using retrieved evidence."
