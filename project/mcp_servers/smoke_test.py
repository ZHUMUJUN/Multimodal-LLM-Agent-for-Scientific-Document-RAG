from pathlib import Path

import anyio
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = REPO_ROOT / "project"
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"


async def _run() -> None:
    server = StdioServerParameters(
        command=str(VENV_PYTHON),
        args=["mcp_servers/filesystem_server.py"],
        cwd=PROJECT_DIR,
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", [tool.name for tool in tools.tools])

            listing = await session.call_tool("list_directory", {"path": "project/evaluation"})
            print("LIST_DIRECTORY:", listing.model_dump())

            content = await session.call_tool(
                "read_text_file",
                {"path": "project/evaluation/datasets/public_light_pollution_retrieval_eval.jsonl", "max_chars": 400},
            )
            print("READ_TEXT_FILE:", content.model_dump())

            search = await session.call_tool(
                "search_text",
                {"path": "project/README.md", "query": "Phoenix", "glob": "*.md", "max_results": 5},
            )
            print("SEARCH_TEXT:", search.model_dump())


if __name__ == "__main__":
    anyio.run(_run)
