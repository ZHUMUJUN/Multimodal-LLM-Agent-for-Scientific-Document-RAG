# Agentic RAG Feature Benchmark

Generated at: `2026-05-07T14:33:05`
Dataset: `/home/suity/worksapce/PycharmProjects/FindJob/agentic-rag-for-dummies-main/project/evaluation/datasets/agentic_feature_eval.jsonl`

## Summary

| Config | Cases | Avg latency ms | Max latency ms | Keyword coverage | Avg workers | Avg tool calls | Reflections | Follow-up searches | Models |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| skills_only | 3 | 36223.42 | 56161.77 | 0.7556 | 2.33 | 5 | 0 | 0 | gemini-2.5-flash:3 |
| plus_reflection | 3 | 42654.25 | 69479.01 | 0.7556 | 2.33 | 8 | 7 | 0 | gemini-2.5-flash:3 |
| plus_roles | 3 | 54834.95 | 84588.34 | 0.8889 | 2.33 | 6.33 | 7 | 0 | gemini-2.5-flash:3 |
| router_simple_cost | 3 | 42394.09 | 71484.03 | 0.8889 | 2.33 | 7.33 | 0 | 0 | gemini-2.5-flash:3 |

## Per-Case Results

### skills_only

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 56161.77 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | research_worker, research_worker, research_worker, research_worker, research_worker | 10 | 0 | 0 | gemini-2.5-flash |
| paper_method | 16459.15 | 0.6 | ECA-SPM, MGFF, DINOv3 | research_worker | 2 | 0 | 0 | gemini-2.5-flash |
| simple_definition | 36049.33 | 0.6667 | DinoCloudNet, DINOv3 | research_worker | 3 | 0 | 0 | gemini-2.5-flash |

### plus_reflection

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 69479.01 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | research_worker, research_worker, research_worker, research_worker, research_worker | 17 | 5 | 0 | gemini-2.5-flash |
| paper_method | 25469.9 | 0.6 | ECA-SPM, MGFF, Adapter | research_worker | 3 | 1 | 0 | gemini-2.5-flash |
| simple_definition | 33013.84 | 0.6667 | DinoCloudNet, DINOv3 | research_worker | 4 | 1 | 0 | gemini-2.5-flash |

### plus_roles

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 84588.34 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | paper_overview_worker, research_worker, method_worker, data_eval_worker, data_eval_worker | 13 | 5 | 0 | gemini-2.5-flash |
| paper_method | 29061.79 | 1.0 | ECA-SPM, MGFF, DINOv3, backbone, Adapter | method_worker | 3 | 1 | 0 | gemini-2.5-flash |
| simple_definition | 50854.72 | 0.6667 | DinoCloudNet, DINOv3 | research_worker | 3 | 1 | 0 | gemini-2.5-flash |

### router_simple_cost

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 71484.03 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | paper_overview_worker, research_worker, method_worker, data_eval_worker, data_eval_worker | 14 | 0 | 0 | gemini-2.5-flash |
| paper_method | 18804.99 | 1.0 | ECA-SPM, MGFF, DINOv3, backbone, Adapter | method_worker | 2 | 0 | 0 | gemini-2.5-flash |
| simple_definition | 36893.26 | 0.6667 | DinoCloudNet, DINOv3 | research_worker | 6 | 0 | 0 | gemini-2.5-flash |
