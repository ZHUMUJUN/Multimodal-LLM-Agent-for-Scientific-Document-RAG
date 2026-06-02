import logging
from typing import List

import config
from core.logging_utils import log_event
from core.tool_policy import ToolPolicy, get_tool_execution_context
from core.web_search import web_search
from db.parent_store_manager import ParentStoreManager
from langchain_core.tools import tool
from mcp_servers.client import MCPFilesystemClient
from retrieval import RetrievalPipeline

logger = logging.getLogger(__name__)


class ToolFactory:

    def __init__(self, collection, collection_name: str, parent_store_path: str | None = None, figure_index=None):
        self.collection = collection
        self.collection_name = collection_name
        self.parent_store_manager = ParentStoreManager(parent_store_path) if parent_store_path else ParentStoreManager()
        self.retrieval_pipeline = RetrievalPipeline(collection, collection_name)
        self.filesystem_client = MCPFilesystemClient() if config.MCP_FILESYSTEM_ENABLED else None
        self.figure_index = figure_index
        self.tool_policy = ToolPolicy()

    def _check_tool_policy(self, tool_name: str, args: dict):
        decision = self.tool_policy.evaluate(tool_name, args)
        execution_context = get_tool_execution_context()
        log_event(
            logger,
            "tool_policy.decision",
            collection=self.collection_name,
            tool_name=tool_name,
            worker_role=execution_context.worker_role if execution_context else "",
            allowed_tools=list(execution_context.allowed_tools) if execution_context else [],
            risk=decision.risk,
            allowed=decision.allowed,
            reason=decision.reason,
            arg_keys=sorted(decision.sanitized_args.keys()),
        )
        return decision

    def _tool_blocked(self, tool_name: str, reason: str) -> str:
        return f"TOOL_BLOCKED_BY_POLICY: {tool_name}: {reason}"

    def _search_child_chunks(self, query: str, limit: int) -> str:
        """Search child chunks for the most relevant excerpts."""
        decision = self._check_tool_policy("search_child_chunks", {"query": query, "limit": limit})
        if not decision.allowed:
            return self._tool_blocked("search_child_chunks", decision.reason)
        query = decision.sanitized_args.get("query", query)
        limit = int(decision.sanitized_args.get("limit", limit))
        try:
            results = self.retrieval_pipeline.search(query, limit)
            log_event(
                logger,
                "retrieval.search_child_chunks",
                collection=self.collection_name,
                query=query,
                limit=limit,
                result_count=len(results),
            )
            if not results:
                return "NO_RELEVANT_CHUNKS"

            return "\n\n".join([
                f"Parent ID: {doc.metadata.get('parent_id', '')}\n"
                f"File Name: {doc.metadata.get('source', '')}\n"
                f"Content: {doc.page_content.strip()}"
                for doc in results
            ])

        except Exception as exc:
            log_event(logger, "retrieval.search_failed", collection=self.collection_name, query=query, error=str(exc))
            return f"RETRIEVAL_ERROR: {str(exc)}"

    def _retrieve_many_parent_chunks(self, parent_ids: List[str]) -> str:
        """Retrieve multiple full parent chunks by their IDs."""
        decision = self._check_tool_policy("retrieve_parent_chunks", {"parent_ids": parent_ids})
        if not decision.allowed:
            return self._tool_blocked("retrieve_parent_chunks", decision.reason)
        parent_ids = decision.sanitized_args.get("parent_ids", parent_ids)
        try:
            ids = [parent_ids] if isinstance(parent_ids, str) else list(parent_ids)
            raw_parents = self.parent_store_manager.load_content_many(ids)
            log_event(
                logger,
                "retrieval.retrieve_many_parent_chunks",
                collection=self.collection_name,
                requested=len(ids),
                returned=len(raw_parents),
            )
            if not raw_parents:
                return "NO_PARENT_DOCUMENTS"

            return "\n\n".join([
                f"Parent ID: {doc.get('parent_id', 'n/a')}\n"
                f"File Name: {doc.get('metadata', {}).get('source', 'unknown')}\n"
                f"Content: {doc.get('content', '').strip()}"
                for doc in raw_parents
            ])

        except Exception as exc:
            log_event(logger, "retrieval.retrieve_many_failed", collection=self.collection_name, error=str(exc))
            return f"PARENT_RETRIEVAL_ERROR: {str(exc)}"

    def _retrieve_parent_chunks(self, parent_id: str) -> str:
        """Retrieve a full parent chunk by its ID."""
        decision = self._check_tool_policy("retrieve_parent_chunks", {"parent_id": parent_id})
        if not decision.allowed:
            return self._tool_blocked("retrieve_parent_chunks", decision.reason)
        parent_id = decision.sanitized_args.get("parent_id", parent_id)
        try:
            parent = self.parent_store_manager.load_content(parent_id)
            log_event(logger, "retrieval.retrieve_parent_chunk", collection=self.collection_name, parent_id=parent_id)
            if not parent:
                return "NO_PARENT_DOCUMENT"

            return (
                f"Parent ID: {parent.get('parent_id', 'n/a')}\n"
                f"File Name: {parent.get('metadata', {}).get('source', 'unknown')}\n"
                f"Content: {parent.get('content', '').strip()}"
            )

        except Exception as exc:
            log_event(logger, "retrieval.retrieve_parent_failed", collection=self.collection_name, parent_id=parent_id, error=str(exc))
            return f"PARENT_RETRIEVAL_ERROR: {str(exc)}"

    def _filesystem_list_directory(self, path: str = ".") -> str:
        """List files and directories from the project repository for report, benchmark, or repo structure questions."""
        decision = self._check_tool_policy("filesystem_list_directory", {"path": path})
        if not decision.allowed:
            return self._tool_blocked("filesystem_list_directory", decision.reason)
        path = decision.sanitized_args.get("path", path)
        if self.filesystem_client is None:
            return "MCP_FILESYSTEM_DISABLED"
        try:
            payload = self.filesystem_client.call_tool("list_directory", {"path": path})
            log_event(
                logger,
                "mcp.filesystem.list_directory",
                collection=self.collection_name,
                path=path,
                result_count=len(payload.get("entries", [])),
            )
            return self.filesystem_client.to_text(payload)
        except Exception as exc:
            log_event(logger, "mcp.filesystem.list_directory_failed", collection=self.collection_name, path=path, error=str(exc))
            return f"MCP_FILESYSTEM_ERROR: {str(exc)}"

    def _filesystem_read_text_file(self, path: str, max_chars: int = config.MCP_FILESYSTEM_MAX_READ_CHARS) -> str:
        """Read a text file from the project repository, including markdown reports, JSON outputs, and source files."""
        decision = self._check_tool_policy("filesystem_read_text_file", {"path": path, "max_chars": max_chars})
        if not decision.allowed:
            return self._tool_blocked("filesystem_read_text_file", decision.reason)
        path = decision.sanitized_args.get("path", path)
        max_chars = int(decision.sanitized_args.get("max_chars", max_chars))
        if self.filesystem_client is None:
            return "MCP_FILESYSTEM_DISABLED"
        try:
            payload = self.filesystem_client.call_tool("read_text_file", {"path": path, "max_chars": max_chars})
            log_event(
                logger,
                "mcp.filesystem.read_text_file",
                collection=self.collection_name,
                path=path,
                truncated=payload.get("truncated", False),
            )
            return self.filesystem_client.to_text(payload)
        except Exception as exc:
            log_event(logger, "mcp.filesystem.read_text_file_failed", collection=self.collection_name, path=path, error=str(exc))
            return f"MCP_FILESYSTEM_ERROR: {str(exc)}"

    def _filesystem_search_text(self, query: str, path: str = ".", glob: str = "*", max_results: int = config.MCP_FILESYSTEM_MAX_SEARCH_RESULTS) -> str:
        """Search repo-local text files for keywords. Use this for finding benchmark reports, Phoenix config, or file references."""
        decision = self._check_tool_policy(
            "filesystem_search_text",
            {"query": query, "path": path, "glob": glob, "max_results": max_results},
        )
        if not decision.allowed:
            return self._tool_blocked("filesystem_search_text", decision.reason)
        query = decision.sanitized_args.get("query", query)
        path = decision.sanitized_args.get("path", path)
        glob = decision.sanitized_args.get("glob", glob)
        max_results = int(decision.sanitized_args.get("max_results", max_results))
        if self.filesystem_client is None:
            return "MCP_FILESYSTEM_DISABLED"
        try:
            payload = self.filesystem_client.call_tool(
                "search_text",
                {"query": query, "path": path, "glob": glob, "max_results": max_results},
            )
            log_event(
                logger,
                "mcp.filesystem.search_text",
                collection=self.collection_name,
                path=path,
                query=query,
                result_count=payload.get("result_count", 0),
            )
            return self.filesystem_client.to_text(payload)
        except Exception as exc:
            log_event(logger, "mcp.filesystem.search_text_failed", collection=self.collection_name, path=path, query=query, error=str(exc))
            return f"MCP_FILESYSTEM_ERROR: {str(exc)}"

    def _filesystem_write_text_file(self, path: str, content: str, overwrite: bool = False) -> str:
        """Write a UTF-8 text file inside the configured agent workspace write root."""
        decision = self._check_tool_policy(
            "filesystem_write_text_file",
            {"path": path, "content_chars": len(content or ""), "overwrite": overwrite},
        )
        if not decision.allowed:
            return self._tool_blocked("filesystem_write_text_file", decision.reason)
        if self.filesystem_client is None:
            return "MCP_FILESYSTEM_DISABLED"
        try:
            payload = self.filesystem_client.call_tool(
                "write_text_file",
                {"path": path, "content": content, "overwrite": overwrite},
            )
            log_event(
                logger,
                "mcp.filesystem.write_text_file",
                collection=self.collection_name,
                path=path,
                size_bytes=payload.get("size_bytes"),
            )
            return self.filesystem_client.to_text(payload)
        except Exception as exc:
            log_event(logger, "mcp.filesystem.write_text_file_failed", collection=self.collection_name, path=path, error=str(exc))
            return f"MCP_FILESYSTEM_ERROR: {str(exc)}"

    def _web_search(self, query: str) -> str:
        """Search the public web when local retrieved evidence is missing, stale, or outside the knowledge base.

        Use this Corrective RAG fallback only for external or time-sensitive questions such as latest trends, 2026 ecosystem changes, prices, official websites, public facts, or when repeated local document search returns insufficient evidence. Do not use it for ordinary questions that can be answered from the selected local collection.
        """
        decision = self._check_tool_policy("web_search", {"query": query})
        if not decision.allowed:
            return self._tool_blocked("web_search", decision.reason)
        query = decision.sanitized_args.get("query", query)
        if not config.CRAG_ENABLED:
            return "WEB_SEARCH_DISABLED"
        log_event(
            logger,
            "crag.web_search",
            collection=self.collection_name,
            provider=config.CRAG_PROVIDER,
            query=query,
            max_results=config.CRAG_MAX_RESULTS,
        )
        return web_search(query)

    def _search_figures(self, query: str, limit: int = 5) -> str:
        """Search PDF figures, tables, page screenshots, and embedded images with CLIP.

        Use this tool for visual questions about figures, tables, architecture diagrams, plots, curves, page images, or captions. For Chinese questions, translate the visual intent into concise English keywords before calling this tool when possible, then combine the returned image path, page number, caption, and nearby text with normal document retrieval.
        """
        decision = self._check_tool_policy("search_figures", {"query": query, "limit": limit})
        if not decision.allowed:
            return self._tool_blocked("search_figures", decision.reason)
        query = decision.sanitized_args.get("query", query)
        limit = int(decision.sanitized_args.get("limit", limit))
        if self.figure_index is None:
            return "FIGURE_SEARCH_DISABLED"
        try:
            return self.figure_index.search_to_text(query=query, limit=limit)
        except Exception as exc:
            log_event(logger, "multimodal.search_figures_failed", collection=self.collection_name, query=query, error=str(exc))
            return f"FIGURE_SEARCH_ERROR: {str(exc)}"

    def create_tools(self) -> List:
        search_tool = tool("search_child_chunks")(self._search_child_chunks)
        retrieve_tool = tool("retrieve_parent_chunks")(self._retrieve_parent_chunks)
        tools = [search_tool, retrieve_tool]

        if self.filesystem_client is not None:
            filesystem_list_tool = tool("filesystem_list_directory")(self._filesystem_list_directory)
            filesystem_read_tool = tool("filesystem_read_text_file")(self._filesystem_read_text_file)
            filesystem_search_tool = tool("filesystem_search_text")(self._filesystem_search_text)
            tools.extend([filesystem_list_tool, filesystem_read_tool, filesystem_search_tool])
            if config.MCP_FILESYSTEM_WRITE_ENABLED:
                filesystem_write_tool = tool("filesystem_write_text_file")(self._filesystem_write_text_file)
                tools.append(filesystem_write_tool)

        if config.CRAG_ENABLED:
            web_search_tool = tool("web_search")(self._web_search)
            tools.append(web_search_tool)

        if config.MULTIMODAL_ENABLED and self.figure_index is not None:
            figure_search_tool = tool("search_figures")(self._search_figures)
            tools.append(figure_search_tool)

        return tools
