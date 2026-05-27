# Agentic RAG Feature Benchmark

Generated at: `2026-05-07T15:13:03`
Dataset: `/home/suity/worksapce/PycharmProjects/FindJob/agentic-rag-for-dummies-main/project/evaluation/datasets/agentic_feature_eval.jsonl`

## Summary

| Config | Cases | Avg latency ms | Max latency ms | Keyword coverage | Ragas | Avg workers | Avg tool calls | Reflections | Follow-up searches | Models |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|
| skills_only | 3 | 34933.07 | 65730.02 | 0.9333 | answer_relevancy=0.2865, faithfulness=0.1111 | 2.33 | 5 | 0 | 0 | gemini-2.5-flash:3 |
| plus_reflection | 3 | 44278.48 | 55436.24 | 0.8857 | answer_relevancy=0.4838, faithfulness=0.2453 | 2.33 | 9 | 6 | 0 | gemini-2.5-flash:3 |
| plus_roles | 3 | 41942.86 | 51551.21 | 1.0 | answer_relevancy=0.3079, faithfulness=0.2065 | 2.33 | 7 | 7 | 0 | gemini-2.5-flash:3 |
| router_simple_cost | 3 | 27113.62 | 41272.91 | 1.0 | answer_relevancy=0.2466, faithfulness=0.4384 | 2.33 | 5.33 | 0 | 0 | gemini-2.5-flash:3 |

## Per-Case Results

### skills_only

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 65730.02 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | research_worker, research_worker, research_worker, research_worker, research_worker | 10 | 0 | 0 | gemini-2.5-flash |
| paper_method | 17588.25 | 0.8 | ECA-SPM, MGFF, DINOv3, Adapter | research_worker | 2 | 0 | 0 | gemini-2.5-flash |
| simple_definition | 21480.94 | 1.0 | DinoCloudNet, 云分割, DINOv3 | research_worker | 3 | 0 | 0 | gemini-2.5-flash |

### plus_reflection

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 55436.24 | 0.8571 | DinoCloudNet, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | research_worker, research_worker, research_worker, research_worker, research_worker | 14 | 5 | 0 | gemini-2.5-flash |
| paper_method | 37740.32 | 0.8 | ECA-SPM, MGFF, DINOv3, Adapter | research_worker | 10 | 0 | 0 | gemini-2.5-flash |
| simple_definition | 39658.88 | 1.0 | DinoCloudNet, 云分割, DINOv3 | research_worker | 3 | 1 | 0 | gemini-2.5-flash |

### plus_roles

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 51551.21 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | paper_overview_worker, research_worker, method_worker, data_eval_worker, data_eval_worker | 14 | 5 | 0 | gemini-2.5-flash |
| paper_method | 45871.46 | 1.0 | ECA-SPM, MGFF, DINOv3, backbone, Adapter | method_worker | 4 | 1 | 0 | gemini-2.5-flash |
| simple_definition | 28405.92 | 1.0 | DinoCloudNet, 云分割, DINOv3 | research_worker | 3 | 1 | 0 | gemini-2.5-flash |

### router_simple_cost

| Case | Latency ms | Coverage | Hit keywords | Workers | Tools | Reflections | Follow-up | Model |
|---|---:|---:|---|---|---:|---:|---:|---|
| paper_multi_aspect | 41272.91 | 1.0 | DinoCloudNet, DINOv3, ECA-SPM, MGFF, CloudSEN12, mIoU, mDice | paper_overview_worker, research_worker, method_worker, data_eval_worker, data_eval_worker | 11 | 0 | 0 | gemini-2.5-flash |
| paper_method | 18443.24 | 1.0 | ECA-SPM, MGFF, DINOv3, backbone, Adapter | method_worker | 2 | 0 | 0 | gemini-2.5-flash |
| simple_definition | 21624.72 | 1.0 | DinoCloudNet, 云分割, DINOv3 | research_worker | 3 | 0 | 0 | gemini-2.5-flash |
