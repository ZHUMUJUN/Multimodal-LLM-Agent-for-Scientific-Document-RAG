---
name: paper_qa_zh
description: Chinese question answering over English academic papers with bilingual query rewriting, cross-lingual retrieval, Chinese final answers, and original evidence citation.
aliases:
  - paper qa
  - 论文问答
  - 文献问答
triggers:
  - 论文
  - 文献
  - paper
  - article
  - 实验
  - 数据集
  - 指标
  - SOTA
  - mIoU
  - benchmark
allowed_tools:
  - search_child_chunks
  - retrieve_parent_chunks
retrieval_mode: hybrid_rerank
---

## Goal

Answer Chinese user questions over English academic papers and technical reports. The user usually asks in Chinese, while source documents are often English PDFs converted to Markdown.

## Workflow

1. Detect the user language and source language. Assume final answers should be Chinese unless the user asks otherwise.
2. Rewrite the query into retrieval-friendly forms:
   - Preserve the original Chinese intent.
   - Generate one or more English search queries for the paper corpus.
   - Keep technical terms, datasets, metrics, model names, author names, and abbreviations in English.
3. Retrieve with the English query first when the corpus is English. Use Chinese intent as secondary semantic context.
4. Prefer evidence from original paper text. Do not treat generated summaries as stronger than source chunks.
5. Rerank with the original Chinese question plus English evidence when possible.
6. Answer in Chinese, but keep important English terms in parentheses, for example `deformable attention` or `mIoU`.
7. End with a `Sources` section containing only source filenames when available.

## Output Rules

- Start directly with the answer.
- Use concise paragraphs and short lists.
- Preserve exact numbers, dataset names, method names, and limitations.
- If the corpus lacks evidence for a claim, say the current documents do not support it.
- If the user asks for "这篇论文/这个方法", resolve the reference from conversation context or ask for clarification.

## Safety

- Do not invent paper claims, metrics, datasets, author names, publication venues, or SOTA status.
- Do not translate technical terms in a way that hides the original English term.
- Do not cite a source unless it appears in retrieved evidence.
