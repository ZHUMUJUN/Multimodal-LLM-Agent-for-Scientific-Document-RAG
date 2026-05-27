import time
from pathlib import Path
from typing import Any

import requests

import config


class LightRAGClient:
    def __init__(self, base_url: str | None = None, timeout: int | None = None):
        self.base_url = (base_url or config.LIGHTRAG_BASE_URL).rstrip("/")
        self.timeout = timeout or config.LIGHTRAG_TIMEOUT_SECONDS

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        response = requests.request(
            method,
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/health")

    def pipeline_status(self) -> dict[str, Any]:
        return self._request("GET", "/documents/pipeline_status")

    def clear_documents(self) -> dict[str, Any]:
        return self._request("DELETE", "/documents")

    def insert_text(self, text: str, file_source: str = "") -> dict[str, Any]:
        return self._request(
            "POST",
            "/documents/text",
            json={
                "text": text,
                "file_source": file_source,
            },
        )

    def insert_texts(self, texts: list[str], file_sources: list[str] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"texts": texts}
        if file_sources is not None:
            payload["file_sources"] = file_sources
        return self._request("POST", "/documents/texts", json=payload)

    def query(
        self,
        query: str,
        mode: str | None = None,
        include_references: bool = True,
        include_chunk_content: bool = False,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "query": query,
            "mode": mode or config.LIGHTRAG_QUERY_MODE,
            "top_k": config.LIGHTRAG_TOP_K,
            "chunk_top_k": config.LIGHTRAG_CHUNK_TOP_K,
            "include_references": include_references,
            "include_chunk_content": include_chunk_content,
            "response_type": "Multiple Paragraphs",
        }
        if conversation_history:
            payload["conversation_history"] = conversation_history
        return self._request("POST", "/query", json=payload)

    def wait_until_idle(self, timeout_seconds: int | None = None, poll_interval: float = 2.0) -> dict[str, Any]:
        timeout_seconds = timeout_seconds or self.timeout
        deadline = time.monotonic() + timeout_seconds
        last_status: dict[str, Any] = {}
        while time.monotonic() < deadline:
            last_status = self.pipeline_status()
            if not last_status.get("busy", False):
                return last_status
            time.sleep(poll_interval)
        raise TimeoutError(f"LightRAG pipeline did not become idle within {timeout_seconds} seconds")

    @staticmethod
    def load_markdown_collection(collection: str) -> list[tuple[str, str]]:
        markdown_dir = Path(config.get_markdown_dir(collection))
        if not markdown_dir.exists():
            return []
        documents: list[tuple[str, str]] = []
        for path in sorted(markdown_dir.glob("*.md")):
            documents.append((path.read_text(encoding="utf-8"), path.name))
        return documents
