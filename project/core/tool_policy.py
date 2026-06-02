from dataclasses import dataclass, field
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import json
from typing import Any, Callable

import config
from core.logging_utils import get_current_run_id
from core.workspace_sandbox import SandboxViolation, get_workspace_sandbox


@dataclass(frozen=True)
class ToolRule:
    risk: str = "low"
    allowed: bool = True
    max_query_chars: int | None = None
    max_path_chars: int | None = None
    allowed_when: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class ToolPolicyDecision:
    allowed: bool
    risk: str
    reason: str
    sanitized_args: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolExecutionContext:
    worker_role: str = ""
    allowed_tools: tuple[str, ...] = ()


_tool_execution_context: ContextVar[ToolExecutionContext | None] = ContextVar("tool_execution_context", default=None)
_approval_checker: Callable[[str], bool] | None = None
_approval_requester: Callable[[str, str | None, str, str, dict[str, Any], str], None] | None = None


@contextmanager
def tool_execution_context(worker_role: str = "", allowed_tools: list[str] | tuple[str, ...] | None = None):
    context = ToolExecutionContext(worker_role=worker_role or "", allowed_tools=tuple(allowed_tools or ()))
    token = _tool_execution_context.set(context)
    try:
        yield
    finally:
        _tool_execution_context.reset(token)


def get_tool_execution_context() -> ToolExecutionContext | None:
    return _tool_execution_context.get()


def set_approval_handlers(
    *,
    checker: Callable[[str], bool] | None = None,
    requester: Callable[[str, str | None, str, str, dict[str, Any], str], None] | None = None,
) -> None:
    global _approval_checker, _approval_requester
    _approval_checker = checker
    _approval_requester = requester


def approval_id_for(run_id: str | None, tool_name: str, args: dict[str, Any]) -> str:
    canonical = json.dumps(
        {"tool_name": tool_name, "args": args},
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return f"appr_{digest}"


class ToolPolicy:
    """Central policy gate for tools before the LLM-triggered call executes."""

    def __init__(self, rules: dict[str, ToolRule] | None = None):
        self.rules = rules or default_tool_rules()

    def evaluate(self, tool_name: str, args: dict[str, Any]) -> ToolPolicyDecision:
        if not config.TOOL_POLICY_ENABLED:
            return ToolPolicyDecision(True, "unknown", "policy disabled", dict(args))

        rule = self.rules.get(tool_name, ToolRule())
        sanitized_args = dict(args)
        risk = rule.risk
        execution_context = get_tool_execution_context()

        if (
            config.TOOL_POLICY_ENFORCE_WORKER_ALLOWED_TOOLS
            and execution_context is not None
            and execution_context.allowed_tools
            and tool_name not in execution_context.allowed_tools
        ):
            role = execution_context.worker_role or "worker"
            return ToolPolicyDecision(False, risk, f"{tool_name} is not allowed for {role}", sanitized_args)

        if not rule.allowed:
            return ToolPolicyDecision(False, risk, f"{tool_name} is disabled by policy", sanitized_args)

        if risk in config.TOOL_APPROVAL_REQUIRED_RISKS and not config.TOOL_POLICY_ALLOW_HIGH_RISK:
            approval_id = approval_id_for(get_current_run_id(), tool_name, sanitized_args)
            if _approval_checker is not None and _approval_checker(approval_id):
                return ToolPolicyDecision(True, risk, f"approved:{approval_id}", sanitized_args)
            reason = f"{tool_name} requires human approval for {risk} risk"
            if config.TOOL_APPROVAL_ENABLED and _approval_requester is not None:
                _approval_requester(
                    approval_id,
                    get_current_run_id(),
                    tool_name,
                    risk,
                    sanitized_args,
                    reason,
                )
                return ToolPolicyDecision(False, risk, f"pending_approval:{approval_id}", sanitized_args)
            return ToolPolicyDecision(False, risk, f"{tool_name} is {risk} risk and requires explicit enablement", sanitized_args)

        max_query_chars = rule.max_query_chars or config.TOOL_POLICY_MAX_QUERY_CHARS
        for query_key in ("query", "search_query"):
            value = sanitized_args.get(query_key)
            if isinstance(value, str) and len(value) > max_query_chars:
                sanitized_args[query_key] = value[:max_query_chars]

        max_path_chars = rule.max_path_chars or config.TOOL_POLICY_MAX_PATH_CHARS
        for path_key in ("path", "file_path"):
            value = sanitized_args.get(path_key)
            if isinstance(value, str):
                if len(value) > max_path_chars:
                    return ToolPolicyDecision(False, risk, f"{path_key} is too long", sanitized_args)
                if "\x00" in value:
                    return ToolPolicyDecision(False, risk, f"{path_key} contains invalid characters", sanitized_args)
                try:
                    get_workspace_sandbox().resolve_read_path(value, must_exist=False)
                except SandboxViolation as exc:
                    return ToolPolicyDecision(False, risk, str(exc), sanitized_args)

        return ToolPolicyDecision(True, risk, "allowed", sanitized_args)


def default_tool_rules() -> dict[str, ToolRule]:
    return {
        "search_child_chunks": ToolRule(risk="low", max_query_chars=config.TOOL_POLICY_MAX_QUERY_CHARS),
        "retrieve_parent_chunks": ToolRule(risk="low"),
        "search_figures": ToolRule(risk="low", max_query_chars=config.TOOL_POLICY_MAX_QUERY_CHARS),
        "filesystem_list_directory": ToolRule(risk="medium", max_path_chars=config.TOOL_POLICY_MAX_PATH_CHARS),
        "filesystem_read_text_file": ToolRule(risk="medium", max_path_chars=config.TOOL_POLICY_MAX_PATH_CHARS),
        "filesystem_search_text": ToolRule(
            risk="medium",
            max_query_chars=config.TOOL_POLICY_MAX_QUERY_CHARS,
            max_path_chars=config.TOOL_POLICY_MAX_PATH_CHARS,
        ),
        "web_search": ToolRule(
            risk="high",
            allowed=config.CRAG_ENABLED,
            max_query_chars=config.TOOL_POLICY_MAX_QUERY_CHARS,
            notes="External network search can leak sensitive prompts or retrieve untrusted text.",
        ),
        "filesystem_write_text_file": ToolRule(
            risk="high",
            allowed=config.MCP_FILESYSTEM_WRITE_ENABLED,
            max_path_chars=config.TOOL_POLICY_MAX_PATH_CHARS,
            notes="Workspace writes must stay inside WORKSPACE_WRITE_ROOT.",
        ),
    }
