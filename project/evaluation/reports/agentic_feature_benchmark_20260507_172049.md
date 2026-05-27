# Agentic RAG Feature Benchmark

Generated at: `2026-05-07T17:20:49`
Dataset: `/home/suity/worksapce/PycharmProjects/FindJob/agentic-rag-for-dummies-main/project/evaluation/datasets/agentic_feature_eval.jsonl`

## Summary

| Config | Cases | Avg latency ms | Max latency ms | Keyword coverage | Ragas | Judge overall | Avg workers | Avg tool calls | Reflections | Follow-up searches | Models |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| skills_only | 1 | 52343.69 | 52343.69 | 1.0 | answer_relevancy=-0.0446, faithfulness=0.0000 | 3.8 | 5 | 12 | 0 | 0 | gemini-2.5-flash:1 |

## LLM-as-Judge

| Config | Method | Dataset | Metrics | Grounding | Chinese | Overall |
|---|---:|---:|---:|---:|---:|---:|
| skills_only | 5.0 | 2.0 | 5.0 | 3.0 | 5.0 | 3.8 |

## Per-Case Results

### skills_only

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 52343.69 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | research_worker, research_worker, research_worker, research_worker, research_worker | 12 | 0 | 0 | gemini-2.5-flash |
