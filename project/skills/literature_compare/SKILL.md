---
name: literature_compare
description: Compare multiple academic papers or technical reports across methods, datasets, metrics, assumptions, limitations, and use cases.
aliases:
  - 文献对比
  - 论文对比
  - literature review
triggers:
  - 比较
  - 对比
  - 差异
  - 区别
  - 共同点
  - related work
  - 综述
  - 哪两篇
  - 哪些文档
allowed_tools:
  - search_child_chunks
  - retrieve_parent_chunks
retrieval_mode: hybrid_rerank
---

## Goal

Compare papers or documents using grounded evidence from the indexed corpus.

## Workflow

1. Identify the compared entities: papers, methods, datasets, metrics, or concepts.
2. Rewrite the query into separate retrieval questions when the comparison has multiple axes.
3. Retrieve evidence for each entity independently before synthesizing.
4. Build the comparison around explicit axes:
   - problem setting
   - method or architecture
   - data and evaluation protocol
   - metrics and reported results
   - limitations
   - when to use each approach
5. If evidence for one side is missing, mark it as missing instead of balancing with assumptions.

## Output Rules

- Use Chinese by default.
- Prefer a compact comparison table when there are two or more entities.
- Keep English technical terms and metric names.
- End with source filenames when available.

## Safety

- Do not infer superiority unless the evidence directly compares the methods or metrics.
- Do not normalize metrics across papers unless their evaluation settings match.

