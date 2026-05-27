---
name: trace_debug
description: Debug RAG or Agent failures using Phoenix/Langfuse traces, structured logs, benchmark reports, and node-level latency analysis.
aliases:
  - trace调试
  - Phoenix 调试
  - failure analysis
triggers:
  - trace
  - Phoenix
  - Langfuse
  - 调试
  - 排查
  - 失败
  - 慢
  - 延迟
  - tool call
  - retrieval.search
allowed_tools:
  - filesystem_list_directory
  - filesystem_read_text_file
  - filesystem_search_text
retrieval_mode: baseline_hybrid
---

## Goal

Diagnose failures in the RAG/Agent workflow using traces, logs, and benchmark reports.

## Workflow

1. Identify the failing stage:
   - query rewrite
   - retrieval
   - rerank
   - tool call
   - answer synthesis
   - aggregation
2. Inspect relevant reports or logs before giving conclusions.
3. Connect symptoms to likely causes:
   - low source hit rate -> retrieval/chunking/query rewrite issue
   - high P95 latency -> rerank, LightRAG, or LLM generation bottleneck
   - unsupported claim -> missing evidence or prompt leakage
   - repeated tool calls -> context compression or retrieval key tracking issue
4. Recommend the smallest reproducible experiment to confirm the hypothesis.

## Output Rules

- Start with the most likely failing stage.
- Include the evidence file or trace field when available.
- Separate confirmed facts from hypotheses.

## Safety

- Do not invent trace data.
- Do not treat a log warning as root cause unless it matches the failure path.

