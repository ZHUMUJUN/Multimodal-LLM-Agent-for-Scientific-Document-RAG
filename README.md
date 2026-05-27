# 多模态 LLM Agent 与科研文档检索增强系统

一个面向科研论文和技术文档的多模态 Agentic RAG 平台。项目围绕长文档问答、论文图表检索、多路混合召回、Agent 任务规划、答案自检、评测与可观测性构建，提供 FastAPI、Gradio、MCP filesystem tools、Skill registry 和离线评测脚本。

## Features

- **LangGraph Agent Runtime**：基于显式 `AgentState` 构建 query rewrite、planner-worker、reflection、aggregation 等图工作流。
- **Planner-Worker 拆解**：面向科研问题中的背景、方法、实验数据、对比、局限等维度进行任务拆分和并行检索。
- **Hybrid Retrieval**：支持 Qdrant dense retrieval、BM25 sparse retrieval、结构化 parent/child chunk 检索。
- **CrossEncoder Reranker**：对 hybrid retrieval 的候选结果做精排，提升 MRR/nDCG。
- **Multimodal Figure Retrieval**：基于 CLIP 对 PDF 页面截图、图表和图注建立 text-to-image 检索能力。
- **Self-RAG Reflection**：对草稿答案做完整性、证据支撑和缺失维度检查，必要时触发补充检索。
- **MCP Filesystem Tools**：提供 `list_directory`、`read_text_file`、`search_text` 等受限文件工具。
- **Skill Registry**：通过 `SKILL.md` 注册论文问答、文献对比、RAG 评测、文档入库、trace debug 等能力。
- **Observability**：支持 Phoenix/OpenTelemetry 与 Langfuse tracing hook。
- **Evaluation**：包含 retrieval benchmark、answer benchmark、Ragas/LLM-as-judge 报告生成脚本和历史评测报告。

## Repository Layout

```text
.
├── project/
│   ├── api/                    # FastAPI app and request/response schemas
│   ├── core/                   # platform service, RAG runtime, tracing, routing
│   ├── db/                     # Qdrant vector DB manager and parent store
│   ├── evaluation/             # datasets, benchmark runners, reports
│   ├── mcp_servers/            # filesystem MCP server and smoke test
│   ├── multimodal/             # CLIP figure/page retrieval
│   ├── providers/              # LLM provider factory
│   ├── rag_agent/              # LangGraph state, nodes, edges, tools
│   ├── retrieval/              # hybrid retrieval and reranker pipeline
│   ├── services/               # PlatformService
│   ├── skills/                 # Agent skills
│   ├── test_corpus/            # lightweight public markdown cache
│   └── ui/                     # Gradio UI
├── requirements.txt
├── requirements-eval.txt
├── Agentic_Rag_For_Dummies.ipynb
└── Observability_Guide.ipynb
```

## What Is Included

This repository includes source code, configuration examples, lightweight public markdown cache, benchmark datasets, evaluation reports, notebooks, and startup scripts.

The following generated/local artifacts are intentionally excluded:

- `.venv/`
- local `.env`
- `project/qdrant_db/`
- generated `project/markdown_docs/`
- generated `project/parent_store/`
- generated `project/figure_store/`
- raw PDF files
- runtime logs and caches

## Requirements

- Python 3.10+
- An LLM provider:
  - Ollama, or
  - OpenAI-compatible endpoint, or
  - Google Gemini, or
  - local vLLM OpenAI-compatible server
- Optional GPU for faster embedding/reranking/multimodal indexing.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp project/.env.example project/.env
```

Optional evaluation dependencies:

```bash
pip install -r requirements-eval.txt
```

## LLM Configuration

Default configuration uses Ollama:

```bash
ollama serve
ollama pull qwen3:14b
```

Common `.env` values:

```bash
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:14b
SMALL_LLM_MODEL=qwen2.5:1.5b
RERANKER_ENABLED=true
MCP_FILESYSTEM_ENABLED=true
SKILLS_ENABLED=true
MULTIMODAL_ENABLED=true
```

For a local vLLM OpenAI-compatible endpoint:

```bash
LLM_PROVIDER=local-vllm
LOCAL_VLLM_BASE_URL=http://127.0.0.1:8001/v1
LOCAL_VLLM_API_KEY=dummy
```

## Start FastAPI

```bash
cd project
../.venv/bin/python api_server.py
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

List skills:

```bash
curl http://127.0.0.1:8000/skills
```

Example chat call after documents are ingested:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "public_light_pollution_corpus",
    "message": "Which document describes artificial light at night as a global disruptor?",
    "session_id": "demo-session"
  }'
```

## Start Gradio UI

```bash
source .venv/bin/activate
python project/app.py
```

Open:

```text
http://127.0.0.1:7860
```

## Ingest the Lightweight Public Corpus

The repository includes `project/test_corpus/markdown_cache/` so the public test corpus can be ingested without committing raw PDFs.

```bash
source .venv/bin/activate
python project/test_corpus/ingest_public_corpus.py \
  --collection public_light_pollution_corpus \
  --clear
```

This creates local generated stores such as `project/qdrant_db/`, `project/parent_store/`, and optionally `project/figure_store/`. These are ignored by git.

## MCP Filesystem Smoke Test

```bash
source .venv/bin/activate
python project/mcp_servers/smoke_test.py
```

Expected output includes:

- registered tools: `list_directory`, `read_text_file`, `search_text`
- a directory listing under `project/evaluation`
- a short read from an evaluation dataset
- a text search in `project/README.md`

## Retrieval Benchmark

After ingesting the public corpus:

```bash
cd project
../.venv/bin/python evaluation/run_retrieval_benchmark.py \
  --dataset evaluation/datasets/public_light_pollution_retrieval_eval.jsonl \
  --mode baseline_hybrid \
  --top-k 5 \
  --output-dir evaluation/reports
```

To compare baseline and rerank:

```bash
../.venv/bin/python evaluation/run_retrieval_benchmark.py \
  --dataset evaluation/datasets/public_light_pollution_retrieval_eval.jsonl \
  --mode baseline_hybrid \
  --mode hybrid_rerank \
  --top-k 5 \
  --output-dir evaluation/reports
```

Generate markdown report:

```bash
../.venv/bin/python evaluation/generate_retrieval_report.py \
  evaluation/reports/retrieval_benchmark_baseline_hybrid_*.json \
  evaluation/reports/retrieval_benchmark_hybrid_rerank_*.json \
  --output evaluation/reports/retrieval_compare_metrics.md
```

## Skills

Bundled skills:

- `paper_qa_zh`: Chinese QA over English academic papers.
- `literature_compare`: compare papers by method, dataset, metric, assumption, limitation, and use case.
- `rag_eval`: explain or run evaluation workflows.
- `rag_ingest`: guide document ingestion and collection management.
- `trace_debug`: debug RAG/Agent failures through traces and reports.

Skill files live under:

```text
project/skills/*/SKILL.md
```

## Observability

Phoenix tracing can be enabled with:

```bash
export PHOENIX_ENABLED=true
export PHOENIX_COLLECTOR_ENDPOINT=http://127.0.0.1:6006/v1/traces
export PHOENIX_PROJECT_NAME=agentic-rag-platform
```

The tracing helpers are implemented in:

```text
project/core/tracing.py
project/core/observability.py
```

## License

MIT. See `LICENSE`.

