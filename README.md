# Multimodal LLM Agent for Scientific Document RAG

A research-document RAG and Agent Harness platform for paper understanding, multimodal evidence retrieval, tool-safe agent execution, and badcase-driven evaluation.

This project extends a basic Agentic RAG workflow into a more production-oriented system. The focus is not only on answering questions over PDFs, but on making each agent run traceable, controllable, evaluable, and reusable for data construction and model alignment.

## What This Project Does

- Converts scientific PDFs into Markdown with structure-aware or fast parsing modes.
- Builds parent-child text indexes for high-recall retrieval and grounded generation.
- Indexes PDF figures, page screenshots, captions, and nearby context with CLIP for text-to-image evidence retrieval.
- Uses Qdrant hybrid retrieval with dense vectors and BM25 sparse vectors.
- Adds optional cross-encoder reranking and Self-RAG reflection.
- Uses LangGraph to orchestrate query rewrite, planner-worker fan-out, tool execution, reflection, and answer aggregation.
- Adds an Agent Harness layer with run trace, memory, declarative skills, declarative worker specs, tool policy, human approval, workspace sandbox, trajectory evaluation, and badcase regression.

## Key Features

| Area | Capability |
|---|---|
| Document parsing | PyMuPDF / PyMuPDF4LLM PDF-to-Markdown conversion with `layout` and `fast` modes |
| Text retrieval | Parent-child chunking, dense retrieval, BM25 sparse retrieval, Qdrant hybrid search |
| Reranking | CrossEncoder reranker for candidate reordering |
| Multimodal retrieval | CLIP-based figure, table, page screenshot, caption, and context indexing |
| Agent orchestration | LangGraph query rewrite, Planner-Worker fan-out, Reflection, aggregation |
| Agent Harness | Run trace, SQLite memory store, declarative skills, worker YAML specs |
| Tool safety | Tool policy, risk levels, approval queue, filesystem sandbox |
| Evaluation | Retrieval benchmark, Ragas, LLM-as-judge, trajectory eval, skill regression, badcase regression |
| Interfaces | Gradio UI, FastAPI API, streaming chat endpoint |
| Providers | Ollama, OpenAI-compatible local vLLM, OpenAI, Google Gemini, optional LightRAG |

## Why This Is More Than A RAG Demo

Most RAG demos focus on the retrieval-answering path:

```text
PDF -> chunks -> vector database -> retrieve -> answer
```

This project adds a harness layer around the agent:

```text
User query
  -> skill selection
  -> memory context
  -> query rewrite
  -> planner-worker task assignment
  -> tool policy decision
  -> retrieval / figure search / filesystem MCP / optional web fallback
  -> reflection
  -> answer aggregation
  -> run trace
  -> trajectory evaluation
  -> badcase regression
```

The goal is to make the agent system suitable for high-quality data construction and safety-oriented iteration:

- Every run has a `run_id`.
- Tool calls are audited by policy.
- High-risk tools can require human approval.
- Filesystem access is restricted by a workspace sandbox.
- Skills and worker roles are declared in files instead of hardcoded in prompts.
- Badcases can be converted into regression cases.
- Trajectories can be scored, not just final answers.

## Architecture

```text
Gradio / FastAPI
  -> PlatformService
  -> RAGSystem per collection
  -> LangGraph Agent
     -> Query Rewrite
     -> Planner-Worker Fan-out
     -> ToolNode with policy-wrapped tools
     -> Reflection
     -> Aggregation

Retrieval Layer
  -> Markdown parsing
  -> Parent chunks saved in parent store
  -> Child chunks embedded into Qdrant
  -> Dense vector + BM25 sparse vector
  -> Optional reranker
  -> Optional CLIP figure collection

Harness Layer
  -> SkillRegistry
  -> WorkerRegistry
  -> MemoryStore
  -> ToolPolicy
  -> WorkspaceSandbox
  -> TrajectoryEval
  -> BadcaseRegression
```

## Repository Structure

```text
.
├── AGENTIC_RAG_PLATFORM_PLAN.md
├── project/
│   ├── api/                         # FastAPI schemas and routes
│   ├── agents/specs/                # Declarative worker YAML specs
│   ├── core/
│   │   ├── rag_system.py            # Per-collection RAG system
│   │   ├── memory_store.py          # SQLite run trace and memory store
│   │   ├── skill_registry.py        # SKILL.md registry
│   │   ├── worker_registry.py       # Worker spec registry
│   │   ├── tool_policy.py           # Tool risk and approval policy
│   │   └── workspace_sandbox.py     # Filesystem access guard
│   ├── db/                          # Qdrant and parent-store managers
│   ├── evaluation/                  # Retrieval, answer, trajectory, skill, badcase eval
│   ├── mcp_servers/                 # Repository-local filesystem MCP server
│   ├── multimodal/                  # CLIP figure indexing and search
│   ├── rag_agent/                   # LangGraph graph, nodes, edges, tools, state
│   ├── retrieval/                   # Hybrid retrieval and reranking pipeline
│   ├── services/                    # PlatformService orchestration
│   └── skills/                      # Agent skills
├── requirements.txt
└── requirements-eval.txt
```

## Document Ingestion

PDF ingestion uses two parsing modes:

```text
layout mode:
  PyMuPDF4LLM -> structure-aware Markdown

fast mode:
  PyMuPDF page.get_text("text") -> page-level plain text Markdown
```

Then the system builds a parent-child index:

```text
Markdown
  -> Markdown header splitter
  -> parent chunks
  -> recursive child chunks
  -> child dense embedding: sentence-transformers/all-mpnet-base-v2
  -> child sparse embedding: Qdrant/bm25
  -> Qdrant hybrid collection
  -> parent chunks saved as JSON and linked by parent_id
```

For figures and tables, the multimodal path runs separately:

```text
PDF pages / embedded images
  -> screenshot or image extraction
  -> caption and nearby text context
  -> CLIP image embedding
  -> Qdrant figure collection
```

## Agent Harness Design

### Declarative Worker Specs

Worker roles are defined under `project/agents/specs/*.yaml`.

Examples:

- `method_worker`
- `data_eval_worker`
- `comparison_worker`
- `limitation_worker`
- `paper_overview_worker`
- `research_worker`

Each spec can declare triggers, skill affinity, allowed tools, max tool calls, priority, and expected output. This keeps role design explicit and auditable.

### Skills

Skills live under `project/skills/*/SKILL.md`. A skill can provide task-specific instructions, aliases, triggers, preferred retrieval mode, and allowed tool families.

This follows the same idea as modern coding-agent systems: keep reusable task knowledge in declarative skill files and load it only when needed.

### Tool Policy And Sandbox

Tools are wrapped by policy checks before execution. The policy can decide:

- whether a tool is allowed
- whether the tool is low, medium, or high risk
- whether human approval is required
- whether arguments need to be sanitized
- whether filesystem paths stay inside allowed roots

This is especially important for MCP filesystem tools, write tools, and web-search fallback.

### Run Trace And Memory

The SQLite-backed memory store records:

- run metadata
- events
- tool approvals
- memory items
- active skill
- selected collection
- answer summary

This makes it possible to debug not only the final answer, but also the trajectory that produced it.

## Evaluation

The project includes several evaluation paths:

```bash
python project/evaluation/run_retrieval_benchmark.py
python project/evaluation/run_benchmark.py
python project/evaluation/run_agentic_feature_benchmark.py
python project/evaluation/trajectory_eval.py --run-id <RUN_ID>
python project/evaluation/skill_regression.py
python project/evaluation/run_badcase_regression.py
```

Evaluation dimensions include:

- retrieval recall and ranking quality
- answer faithfulness
- citation grounding
- tool usage trajectory
- worker planning
- reflection behavior
- skill loading
- badcase regression stability

## Quick Start

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional evaluation dependencies:

```bash
pip install -r requirements-eval.txt
```

### Configure

```bash
cp project/.env.example project/.env
```

Common local configuration:

```bash
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:14b
PDF_PARSE_MODE=auto
RETRIEVAL_MODE=hybrid_rerank
MULTIMODAL_ENABLED=true
SKILLS_ENABLED=true
TOOL_APPROVAL_ENABLED=true
```

### Run Gradio

```bash
python project/app.py
```

### Run FastAPI

```bash
python project/api_server.py
```

Main endpoints:

- `GET /health`
- `GET /collections`
- `GET /skills`
- `GET /runs`
- `GET /runs/{run_id}`
- `POST /ingest`
- `POST /chat`
- `POST /chat/stream`
- `POST /figures/search`
- `GET /tool-approvals`
- `POST /tool-approvals/{approval_id}/resolve`

## Example Use Cases

- Ask method, experiment, comparison, and limitation questions over scientific papers.
- Retrieve text evidence and figure/table evidence together.
- Build citation-grounded QA data from paper evidence.
- Analyze badcases such as retrieval miss, citation mismatch, hallucinated metrics, and unsupported claims.
- Evaluate whether an agent used the right tools and worker roles, not only whether the final answer looks fluent.
- Debug RAG failures from run traces and benchmark reports.

## Notes

- Local Qdrant uses embedded storage. Avoid running multiple processes against the same local Qdrant path at the same time.
- `.env`, `.venv`, `agent_memory.db`, local Qdrant data, parent stores, figure stores, Markdown caches, PDFs, and model weights are intentionally ignored.
- Root README is a portfolio-level overview. Detailed API and configuration documentation is in `project/README.md`.

## License

MIT License.
