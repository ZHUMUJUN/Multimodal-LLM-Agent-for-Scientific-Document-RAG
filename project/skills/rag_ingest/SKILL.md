---
name: rag_ingest
description: Guide document ingestion into the RAG platform, including PDF validation, Markdown conversion, parent/child chunking, indexing, and collection isolation.
aliases:
  - 文档入库
  - ingest
  - index docs
triggers:
  - 入库
  - 上传
  - 导入
  - 建索引
  - 重新索引
  - collection
  - chunk
  - PDF 转 Markdown
allowed_tools:
  - filesystem_list_directory
  - filesystem_read_text_file
  - filesystem_search_text
retrieval_mode: baseline_hybrid
---

## Goal

Help operate or explain the document ingestion workflow for this RAG platform.

## Workflow

1. Confirm collection name and input file type.
2. For PDFs, validate file extension and readability before ingestion.
3. Convert PDFs to Markdown.
4. Split into parent chunks by Markdown headers and child chunks for retrieval.
5. Index child chunks into Qdrant hybrid retrieval.
6. Store parent chunks in the collection-specific parent store.
7. Report added/skipped files and collection document count.

## Operational Commands

- API ingestion:
  `curl -X POST "http://127.0.0.1:8000/ingest?collection=<name>" -F "files=@/path/to/file.pdf"`
- Gradio ingestion:
  Upload files in the UI and choose the target collection.

## Safety

- Do not claim a document was ingested unless the service reports success.
- Keep collections isolated. Do not mix customer/private corpora unless explicitly requested.
- If the user asks to ingest local files through chat, explain that files must be uploaded through `/ingest` or Gradio.

