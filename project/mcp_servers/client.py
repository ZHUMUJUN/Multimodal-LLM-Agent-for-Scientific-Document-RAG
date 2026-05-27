import json
from pathlib import Path
from typing import Any

import anyio
import config
from core.tracing import add_span_attributes, start_span
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = REPO_ROOT / "project"
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"


class MCPFilesystemClient:
    async def _call_tool_async(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        server = StdioServerParameters(
            command=str(VENV_PYTHON),
            args=["mcp_servers/filesystem_server.py"],
            cwd=PROJECT_DIR,
        )

        async with stdio_client(server) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                payload = result.structuredContent or {}
                if not payload:
                    text_parts = [
                        block.text for block in result.content if getattr(block, "type", None) == "text" and getattr(block, "text", None)
                    ]
                    payload = {"text": "\n\n".join(text_parts)}
                payload["is_error"] = bool(result.isError)
                return payload

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        with start_span("mcp.filesystem.call", tool_name=tool_name) as span:
            result = anyio.run(self._call_tool_async, tool_name, arguments)
            add_span_attributes(span, is_error=result.get("is_error", False))
            return result

    @staticmethod
    def to_text(payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2)
