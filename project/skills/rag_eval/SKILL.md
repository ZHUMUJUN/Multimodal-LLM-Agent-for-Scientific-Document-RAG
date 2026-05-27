---
name: rag_eval
description: Run or explain RAG evaluation workflows, including retrieval benchmarks, answer benchmarks, Ragas reports, latency, source hit rate, MRR, and failure analysis.
aliases:
  - rag评测
  - benchmark
  - eval
triggers:
  - 评测
  - benchmark
  - Ragas
  - 命中率
  - MRR
  - source hit
  - latency
  - P95
  - 失败样例
allowed_tools:
  - filesystem_list_directory
  - filesystem_read_text_file
  - filesystem_search_text
retrieval_mode: baseline_hybrid
---

## Goal

Operate and interpret the RAG platform's evaluation layer.

## Workflow

1. Identify the evaluation target:
   - retrieval quality
   - answer quality
   - router ablation
   - LightRAG comparison
   - latency or service benchmark
2. Locate the dataset and report files before answering.
3. Report concrete metrics:
   - source hit rate
   - MRR
   - keyword hit rate
   - answer relevancy
   - faithfulness
   - avg/P95 latency
4. Explain metric trade-offs. For example, rerank may improve precision while adding latency.
5. Include failure cases and next actions when available.

## Commands

- Retrieval benchmark:
  `python project/evaluation/run_retrieval_benchmark.py --dataset project/evaluation/datasets/public_light_pollution_retrieval_eval.jsonl`
- Baseline vs rerank benchmark:
  `python project/evaluation/run_benchmark.py --dataset project/evaluation/datasets/sample_eval.jsonl --mode baseline_hybrid --mode hybrid_rerank`
- Router answer benchmark:
  `python project/evaluation/run_router_answer_benchmark.py --dataset project/evaluation/datasets/public_light_pollution_router_eval_6_real.jsonl`

## Safety

- Do not average metrics across incompatible datasets.
- Do not claim Ragas success if the report says Ragas failed or was skipped.
- Always mention the dataset size when interpreting metrics.

