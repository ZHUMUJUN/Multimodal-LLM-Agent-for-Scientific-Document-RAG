import os
import config
import pymupdf.layout
import pymupdf4llm
import time
from pathlib import Path
import glob
import tiktoken
import logging

from core.logging_utils import log_event

os.environ["TOKENIZERS_PARALLELISM"] = "false"

logger = logging.getLogger(__name__)


def _choose_pdf_parse_mode(pdf_path: Path, doc) -> tuple[str, int]:
    configured_mode = config.PDF_PARSE_MODE
    if configured_mode in {"fast", "layout"}:
        return configured_mode, sum(len(page.get_images(full=True)) for page in doc)

    image_count = sum(len(page.get_images(full=True)) for page in doc)
    file_mb = pdf_path.stat().st_size / 1024 / 1024
    if file_mb >= config.PDF_FAST_PARSE_FILE_MB or image_count >= config.PDF_FAST_PARSE_IMAGE_COUNT:
        return "fast", image_count
    return "layout", image_count


def _fast_pdf_to_markdown(doc) -> str:
    page_blocks = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            page_blocks.append(f"# Page {page_number}\n\n{text}")
    return "\n\n---\n\n".join(page_blocks)


def pdf_to_markdown(pdf_path, output_dir):
    started_at = time.perf_counter()
    pdf_path = Path(pdf_path)
    doc = pymupdf.open(pdf_path)
    parse_mode, image_count = _choose_pdf_parse_mode(pdf_path, doc)

    if parse_mode == "fast":
        md = _fast_pdf_to_markdown(doc)
    else:
        md = pymupdf4llm.to_markdown(doc, header=False, footer=False, page_separators=True, ignore_images=True, write_images=False, image_path=None)

    md_cleaned = md.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
    output_path = Path(output_dir) / Path(doc.name).stem
    Path(output_path).with_suffix(".md").write_bytes(md_cleaned.encode('utf-8'))
    log_event(
        logger,
        "pdf.converted_to_markdown",
        file=pdf_path.name,
        parse_mode=parse_mode,
        pages=doc.page_count,
        images=image_count,
        markdown_chars=len(md_cleaned),
        elapsed_seconds=round(time.perf_counter() - started_at, 3),
    )

def pdfs_to_markdowns(path_pattern, output_dir=None, overwrite: bool = False):
    output_dir = Path(output_dir or config.MARKDOWN_ROOT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in map(Path, glob.glob(path_pattern)):
        md_path = (output_dir / pdf_path.stem).with_suffix(".md")
        if overwrite or not md_path.exists():
            pdf_to_markdown(pdf_path, output_dir)

def estimate_context_tokens(messages: list) -> int:
    try:
        encoding = tiktoken.encoding_for_model("gpt-4")
    except:
        encoding = tiktoken.get_encoding("cl100k_base")
    return sum(len(encoding.encode(str(msg.content))) for msg in messages if hasattr(msg, 'content') and msg.content)
