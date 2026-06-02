import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from core.skill_registry import SkillRegistry
from core.tool_policy import default_tool_rules
from core.worker_registry import WorkerRegistry


def run_skill_regression(skills_dir: str = config.SKILLS_DIR, worker_specs_dir: str = config.WORKER_SPECS_DIR) -> dict:
    registry = SkillRegistry(skills_dir)
    worker_registry = WorkerRegistry(worker_specs_dir)
    known_tools = set(default_tool_rules())

    failures = []
    warnings = []
    alias_owners: dict[str, list[str]] = defaultdict(list)
    trigger_owners: dict[str, list[str]] = defaultdict(list)

    skills = registry.list_skills()
    for skill in skills:
        name = skill["name"]
        if not skill.get("description"):
            failures.append(f"{name}: missing description")
        if not skill.get("version"):
            failures.append(f"{name}: missing version")
        if not skill.get("triggers") and not skill.get("aliases"):
            warnings.append(f"{name}: no triggers or aliases")
        for tool_name in skill.get("allowed_tools", []):
            if tool_name not in known_tools:
                failures.append(f"{name}: unknown allowed tool {tool_name}")
        for alias in skill.get("aliases", []):
            alias_owners[alias.lower()].append(name)
        for trigger in skill.get("triggers", []):
            trigger_owners[trigger.lower()].append(name)

    for alias, owners in alias_owners.items():
        if len(owners) > 1:
            warnings.append(f"alias '{alias}' is shared by {owners}")
    for trigger, owners in trigger_owners.items():
        if len(owners) > 2:
            warnings.append(f"trigger '{trigger}' is broad/shared by {owners}")

    for worker in worker_registry.list_specs():
        role = worker["role"]
        if not worker.get("expected_output"):
            failures.append(f"{role}: missing expected_output")
        if int(worker.get("max_tool_calls") or 0) <= 0:
            failures.append(f"{role}: max_tool_calls must be positive")
        for tool_name in worker.get("allowed_tools", []):
            if tool_name not in known_tools:
                failures.append(f"{role}: unknown allowed tool {tool_name}")

    return {
        "ok": not failures,
        "skill_count": len(skills),
        "worker_count": len(worker_registry.specs),
        "known_tools": sorted(known_tools),
        "failures": failures,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run static regression checks for agent skills and worker specs.")
    parser.add_argument("--skills-dir", default=config.SKILLS_DIR)
    parser.add_argument("--worker-specs-dir", default=config.WORKER_SPECS_DIR)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    result = run_skill_regression(args.skills_dir, args.worker_specs_dir)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
