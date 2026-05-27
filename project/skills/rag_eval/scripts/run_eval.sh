#!/usr/bin/env bash
set -euo pipefail

DATASET="${1:-project/evaluation/datasets/sample_eval.jsonl}"

python project/evaluation/run_benchmark.py \
  --dataset "$DATASET" \
  --mode baseline_hybrid \
  --mode hybrid_rerank

