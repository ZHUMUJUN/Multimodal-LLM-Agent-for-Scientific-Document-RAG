from __future__ import annotations

import httpx

import config


def _format_results(results: list[dict]) -> str:
    if not results:
        return "NO_WEB_RESULTS"

    lines = []
    for idx, item in enumerate(results, start=1):
        title = item.get("title") or item.get("name") or "Untitled"
        url = item.get("url") or item.get("link") or ""
        content = item.get("content") or item.get("snippet") or item.get("description") or ""
        lines.append(
            f"[Web Result {idx}]\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Content: {content}"
        )
    return "\n\n".join(lines)


def tavily_search(query: str) -> str:
    if not config.TAVILY_API_KEY:
        return "WEB_SEARCH_ERROR: TAVILY_API_KEY is not configured."

    payload = {
        "api_key": config.TAVILY_API_KEY,
        "query": query,
        "search_depth": config.CRAG_SEARCH_DEPTH,
        "max_results": config.CRAG_MAX_RESULTS,
        "include_answer": False,
        "include_raw_content": False,
    }
    with httpx.Client(timeout=config.CRAG_TIMEOUT_SECONDS) as client:
        response = client.post("https://api.tavily.com/search", json=payload)
        response.raise_for_status()
        data = response.json()
    return _format_results(data.get("results", []))


def serper_search(query: str) -> str:
    if not config.SERPER_API_KEY:
        return "WEB_SEARCH_ERROR: SERPER_API_KEY is not configured."

    headers = {"X-API-KEY": config.SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": config.CRAG_MAX_RESULTS}
    with httpx.Client(timeout=config.CRAG_TIMEOUT_SECONDS) as client:
        response = client.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return _format_results(data.get("organic", []))


def web_search(query: str) -> str:
    provider = config.CRAG_PROVIDER.lower()
    try:
        if provider == "tavily":
            return tavily_search(query)
        if provider == "serper":
            return serper_search(query)
        return f"WEB_SEARCH_ERROR: Unsupported CRAG_PROVIDER: {config.CRAG_PROVIDER}"
    except Exception as exc:
        return f"WEB_SEARCH_ERROR: {type(exc).__name__}: {exc}"
