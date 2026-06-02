import fnmatch
import os
from pathlib import Path

import config


class SandboxViolation(ValueError):
    pass


class WorkspaceSandbox:
    """Central path policy for agent-visible filesystem access."""

    def __init__(
        self,
        *,
        read_roots: list[str] | None = None,
        write_root: str | None = None,
        blocked_patterns: list[str] | None = None,
    ):
        self.read_roots = self._normalize_roots(read_roots or config.MCP_FILESYSTEM_ALLOWED_ROOTS)
        self.write_root = Path(write_root or config.WORKSPACE_WRITE_ROOT).expanduser().resolve()
        self.blocked_patterns = [pattern.lower() for pattern in (blocked_patterns or config.WORKSPACE_BLOCKED_PATH_PATTERNS)]
        self.workspace_root = Path(config.WORKSPACE_ROOT).expanduser().resolve()

    @staticmethod
    def _normalize_roots(raw_roots: list[str]) -> list[Path]:
        roots = []
        for raw_path in raw_roots:
            resolved = Path(raw_path).expanduser().resolve()
            if resolved.exists() and resolved not in roots:
                roots.append(resolved)
        if not roots:
            roots.append(Path(os.path.dirname(config.__file__)).resolve().parent)
        return roots

    def describe(self) -> dict:
        return {
            "read_roots": [str(root) for root in self.read_roots],
            "write_root": str(self.write_root),
            "blocked_patterns": self.blocked_patterns,
        }

    def resolve_read_path(self, user_path: str | None = ".", *, must_exist: bool = False) -> Path:
        resolved = self._resolve_path(user_path)
        if must_exist and not resolved.exists():
            raise SandboxViolation(f"Path does not exist: {resolved}")
        if not self._is_under_any(resolved, self.read_roots):
            allowed = ", ".join(str(root) for root in self.read_roots)
            raise SandboxViolation(f"Path is outside workspace read roots: {allowed}")
        self._assert_not_blocked(resolved)
        return resolved

    def resolve_write_path(self, user_path: str | None) -> Path:
        resolved = self._resolve_path(user_path, base=self.write_root)
        if not self._is_under_any(resolved, [self.write_root]):
            raise SandboxViolation(f"Write path is outside workspace write root: {self.write_root}")
        self._assert_not_blocked(resolved)
        return resolved

    def _resolve_path(self, user_path: str | None, *, base: Path | None = None) -> Path:
        raw = (user_path or ".").strip()
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = (base or self.workspace_root) / candidate
        return candidate.resolve()

    @staticmethod
    def _is_under_any(candidate: Path, roots: list[Path]) -> bool:
        return any(candidate == root or root in candidate.parents for root in roots)

    def _assert_not_blocked(self, path: Path) -> None:
        lowered_parts = [part.lower() for part in path.parts]
        lowered_name = path.name.lower()
        lowered_path = str(path).lower()
        for pattern in self.blocked_patterns:
            if (
                fnmatch.fnmatch(lowered_name, pattern)
                or fnmatch.fnmatch(lowered_path, pattern)
                or any(fnmatch.fnmatch(part, pattern) for part in lowered_parts)
            ):
                raise SandboxViolation(f"Path is blocked by workspace sandbox pattern: {pattern}")


_default_sandbox: WorkspaceSandbox | None = None


def get_workspace_sandbox() -> WorkspaceSandbox:
    global _default_sandbox
    if _default_sandbox is None:
        _default_sandbox = WorkspaceSandbox()
    return _default_sandbox
