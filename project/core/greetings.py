import re


GREETING_PATTERN = re.compile(
    r"^\s*(hi|hello|hey|yo|你好|您好|嗨|哈喽|早上好|下午好|晚上好)[!！,.，。?\s]*$",
    re.IGNORECASE,
)


def is_greeting_only(message: str) -> bool:
    return bool(GREETING_PATTERN.match((message or "").strip()))


def greeting_response() -> str:
    return "你好，我可以基于已上传的文档回答问题。请先上传 PDF/Markdown，或直接提出一个具体问题。"
