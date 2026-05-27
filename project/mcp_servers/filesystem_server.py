import fnmatch
import os
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import config
from mcp.server.fastmcp import FastMCP

TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
DEFAULT_IGNORES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "node_modules",
}


def _normalize_roots() -> list[Path]:
    roots: list[Path] = []
    for raw_path in config.MCP_FILESYSTEM_ALLOWED_ROOTS:
        resolved = Path(raw_path).expanduser().resolve()
        if resolved.exists() and resolved not in roots:
            roots.append(resolved)
    if not roots:
        roots.append(Path(os.path.dirname(config.__file__)).resolve().parent)
    return roots


ALLOWED_ROOTS = _normalize_roots()
PROJECT_ROOT = PROJECT_DIR.parent

server = FastMCP(
    name=config.MCP_FILESYSTEM_SERVER_NAME,
    instructions=(
        "Filesystem MCP server restricted to the current repository. "
        "Use it for project-local file discovery, reading text files, and simple text search."
    ),
)


def _path_is_allowed(candidate: Path) -> bool:
    return any(candidate == root or root in candidate.parents for root in ALLOWED_ROOTS)


def _resolve_user_path(user_path: str | None) -> Path:
    raw = (user_path or ".").strip()
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    resolved = candidate.resolve()
    if not _path_is_allowed(resolved):
        allowed = ", ".join(str(root) for root in ALLOWED_ROOTS)
        raise ValueError(f"Path '{raw}' is outside the allowed roots: {allowed}")
    return resolved


def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def _preview_text(path: Path, limit: int) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")
    if len(content) <= limit:
        return content
    return f"{content[:limit]}\n\n...[truncated at {limit} chars]"


@server.tool(description="List a directory inside the allowed repository roots.")
def list_directory(path: str = ".") -> dict[str, Any]:
    target = _resolve_user_path(path)
    if not target.exists():
        raise ValueError(f"Path does not exist: {target}")
    if not target.is_dir():
        raise ValueError(f"Path is not a directory: {target}")

    entries = []
    for child in sorted(target.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        if child.name in DEFAULT_IGNORES:
            continue
        entries.append(
            {
                "name": child.name,
                "path": str(child),
                "type": "directory" if child.is_dir() else "file",
                "size_bytes": child.stat().st_size if child.is_file() else None,
            }
        )
    return {
        "path": str(target),
        "allowed_roots": [str(root) for root in ALLOWED_ROOTS],
        "entries": entries,
    }


@server.tool(description="Read a UTF-8 text file inside the allowed repository roots.")
def read_text_file(path: str, max_chars: int = config.MCP_FILESYSTEM_MAX_READ_CHARS) -> dict[str, Any]:
    target = _resolve_user_path(path)
    if not target.exists():
        raise ValueError(f"Path does not exist: {target}")
    if not target.is_file():
        raise ValueError(f"Path is not a file: {target}")
    if not _is_text_file(target):
        raise ValueError(f"Only text-like files are supported: {target.name}")

    full_text = target.read_text(encoding="utf-8", errors="replace")
    preview = full_text if len(full_text) <= max(1, max_chars) else f"{full_text[:max_chars]}\n\n...[truncated at {max_chars} chars]"
    return {
        "path": str(target),
        "size_bytes": target.stat().st_size,
        "truncated": len(preview) < len(full_text),
        "content": preview,
    }


@server.tool(description="Search for a substring or glob-like pattern across text files in the allowed repository roots.")
def search_text(
    query: str,
    path: str = ".",
    glob: str = "*",
    max_results: int = config.MCP_FILESYSTEM_MAX_SEARCH_RESULTS,
) -> dict[str, Any]:
    target = _resolve_user_path(path)
    if not target.exists():
        raise ValueError(f"Path does not exist: {target}")

    needle = query.strip()
    if not needle:
        raise ValueError("query must not be empty")

    max_results = max(1, max_results)
    results = []
    files_scanned = 0

    walker = [target] if target.is_file() else target.rglob("*")
    for candidate in walker:
        if len(results) >= max_results:
            break
        if candidate.name in DEFAULT_IGNORES or not candidate.is_file():
            continue
        if not fnmatch.fnmatch(candidate.name, glob):
            continue
        if not _path_is_allowed(candidate.resolve()) or not _is_text_file(candidate):
            continue
        if candidate.stat().st_size > config.MCP_FILESYSTEM_SEARCH_MAX_FILE_SIZE:
            continue

        files_scanned += 1
        try:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if needle.lower() in line.lower():
                results.append(
                    {
                        "path": str(candidate),
                        "line_number": line_number,
                        "line": line.strip(),
                    }
                )
                if len(results) >= max_results:
                    break

    return {
        "query": needle,
        "path": str(target),
        "glob": glob,
        "files_scanned": files_scanned,
        "result_count": len(results),
        "results": results,
    }


def main() -> None:
    server.run(transport=config.MCP_FILESYSTEM_TRANSPORT)


if __name__ == "__main__":
    main()
