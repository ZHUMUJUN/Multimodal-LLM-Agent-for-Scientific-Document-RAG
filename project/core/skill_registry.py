import logging
import re
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from core.logging_utils import log_event

logger = logging.getLogger(__name__)


FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)


@dataclass(frozen=True)
class AgentSkill:
    name: str
    description: str
    path: Path
    instructions: str
    allowed_tools: list[str]
    retrieval_mode: str
    triggers: list[str]
    aliases: list[str]
    version: str

    def prompt_context(self) -> str:
        allowed = ", ".join(self.allowed_tools) if self.allowed_tools else "all project tools"
        return (
            f"# Active Agent Skill: {self.name}\n\n"
            f"Description: {self.description}\n"
            f"Skill version: {self.version}\n"
            f"Preferred retrieval mode: {self.retrieval_mode}\n"
            f"Allowed tool family: {allowed}\n\n"
            f"{self.instructions.strip()}"
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "allowed_tools": self.allowed_tools,
            "retrieval_mode": self.retrieval_mode,
            "triggers": self.triggers,
            "aliases": self.aliases,
            "version": self.version,
            "path": str(self.path),
        }


@dataclass(frozen=True)
class SkillMatch:
    skill: AgentSkill
    score: int
    reasons: list[str]


class SkillRegistry:
    """Filesystem-backed Agent Skill registry.

    The registry follows the common SKILL.md progressive-disclosure pattern:
    discovery uses frontmatter metadata, while full instructions are only
    loaded for the active skill.
    """

    def __init__(self, skills_dir: str | Path):
        self.skills_dir = Path(skills_dir)
        self._skills: dict[str, AgentSkill] = {}
        self.reload()

    def reload(self) -> None:
        self._skills = {}
        if not self.skills_dir.exists():
            log_event(logger, "skills.dir_missing", skills_dir=str(self.skills_dir))
            return

        for skill_file in sorted(self.skills_dir.glob("*/SKILL.md")):
            try:
                skill = self._load_skill(skill_file)
                self._skills[skill.name] = skill
            except Exception as exc:
                log_event(logger, "skills.load_failed", path=str(skill_file), error=str(exc))

        log_event(logger, "skills.loaded", skills_dir=str(self.skills_dir), count=len(self._skills))

    def list_skills(self) -> list[dict[str, Any]]:
        return [skill.metadata() for skill in sorted(self._skills.values(), key=lambda item: item.name)]

    def get(self, name: str | None) -> AgentSkill | None:
        if not name:
            return None
        normalized = self._normalize_name(name)
        if normalized in self._skills:
            return self._skills[normalized]
        for skill in self._skills.values():
            if normalized in {self._normalize_name(alias) for alias in skill.aliases}:
                return skill
        return None

    def parse_command(self, message: str) -> tuple[str | None, str]:
        """Support direct invocation like `/paper_qa_zh 中文问题...`."""
        text = (message or "").strip()
        match = re.match(r"^/(?:skill:)?([a-zA-Z0-9_-]+)\s*(.*)$", text, re.DOTALL)
        if not match:
            return None, text
        return match.group(1), match.group(2).strip()

    def select(self, message: str, requested: str | None = None) -> SkillMatch | None:
        requested_skill = self.get(requested)
        if requested_skill is not None:
            return SkillMatch(skill=requested_skill, score=100, reasons=["requested"])

        text = (message or "").strip()
        if not text:
            return None

        lowered = text.lower()
        best: SkillMatch | None = None
        for skill in self._skills.values():
            score = 0
            reasons: list[str] = []

            for alias in skill.aliases:
                alias_text = alias.strip()
                if alias_text and alias_text.lower() in lowered:
                    score += 5
                    reasons.append(f"alias:{alias}")

            for trigger in skill.triggers:
                trigger_text = trigger.strip()
                if not trigger_text:
                    continue
                if trigger_text.lower() in lowered or trigger_text in text:
                    score += 3 if len(trigger_text) > 1 else 1
                    reasons.append(f"trigger:{trigger_text}")

            if skill.name.replace("_", "-") in lowered or skill.name in lowered:
                score += 5
                reasons.append("name")

            if score > 0 and (best is None or score > best.score):
                best = SkillMatch(skill=skill, score=score, reasons=reasons)

        if best and best.score >= 3:
            return best
        return None

    def _load_skill(self, skill_file: Path) -> AgentSkill:
        raw = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_PATTERN.match(raw)
        if not match:
            raise ValueError("SKILL.md must start with YAML frontmatter")

        metadata = yaml.safe_load(match.group(1)) or {}
        body = match.group(2).strip()
        name = self._normalize_name(metadata.get("name") or skill_file.parent.name)
        description = str(metadata.get("description") or "").strip()
        if not description:
            raise ValueError("Skill description is required")

        return AgentSkill(
            name=name,
            description=description,
            path=skill_file,
            instructions=body,
            allowed_tools=self._as_list(metadata.get("allowed_tools")),
            retrieval_mode=str(metadata.get("retrieval_mode") or "auto").strip(),
            triggers=self._as_list(metadata.get("triggers")),
            aliases=self._as_list(metadata.get("aliases")),
            version=str(metadata.get("version") or hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]),
        )

    @staticmethod
    def _as_list(value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()]

    @staticmethod
    def _normalize_name(name: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]+", "-", (name or "").strip().lower()).strip("-")
