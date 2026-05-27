import re


FILE_LIST_PATTERNS = [
    re.compile(r"(当前|这个|该)?(集合|知识库).*(有|包含|包括).*(哪些|什么).*(文件|文档)", re.IGNORECASE),
    re.compile(r"(集合|知识库).*(文件|文档).*(列表|清单)", re.IGNORECASE),
    re.compile(r"(目前|当前).*(文件|文档).*(有哪些|列表|清单)", re.IGNORECASE),
    re.compile(r"(list|show).*(files|documents)", re.IGNORECASE),
    re.compile(r"(what|which).*(files|documents).*(in|inside).*(collection|knowledge base)", re.IGNORECASE),
]


def is_collection_file_list_query(message: str) -> bool:
    text = (message or "").strip()
    return any(pattern.search(text) for pattern in FILE_LIST_PATTERNS)


def format_collection_file_list_response(collection: str, files: list[str]) -> str:
    if not files:
        return f"当前集合 `{collection}` 里还没有文件。你可以先上传 PDF 或 Markdown 文档。"

    lines = "\n".join(f"- {name}" for name in files)
    return f"当前集合 `{collection}` 包含以下文件：\n\n{lines}"
