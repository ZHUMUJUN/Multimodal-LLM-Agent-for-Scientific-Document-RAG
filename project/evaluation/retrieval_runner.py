import json
import os
import statistics
import time
from datetime import datetime
from pathlib import Path

import config
from core.logging_utils import log_event
from db.vector_db_manager import VectorDbManager
from retrieval import RetrievalPipeline

from .schemas import load_cases

import logging

logger = logging.getLogger(__name__)


def _first_hit_rank(expected_sources: list[str], retrieved_sources: list[str]) -> int | None:
    expected = {source for source in expected_sources if source}
    if not expected:
        return None
    for index, source in enumerate(retrieved_sources, start=1):
        if source in expected:
            return index
    return None


def _source_recall_at_k(expected_sources: list[str], retrieved_sources: list[str]) -> float | None:
    expected = {source for source in expected_sources if source}
    if not expected:
        return None
    retrieved = {source for source in retrieved_sources if source}
    return len(expected & retrieved) / len(expected)


def _average_precision_at_k(expected_sources: list[str], retrieved_sources: list[str]) -> float | None:
    expected = {source for source in expected_sources if source}
    if not expected:
        return None
    seen: set[str] = set()
    hit_count = 0
    precision_sum = 0.0
    for index, source in enumerate(retrieved_sources, start=1):
        if source in expected and source not in seen:
            seen.add(source)
            hit_count += 1
            precision_sum += hit_count / index
    return precision_sum / len(expected)


def _dcg(relevances: list[int]) -> float:
    import math

    return sum(rel / math.log2(index + 2) for index, rel in enumerate(relevances))


def _ndcg_at_k(expected_sources: list[str], retrieved_sources: list[str]) -> float | None:
    expected = {source for source in expected_sources if source}
    if not expected:
        return None
    seen: set[str] = set()
    relevances = []
    for source in retrieved_sources:
        if source in expected and source not in seen:
            relevances.append(1)
            seen.add(source)
        else:
            relevances.append(0)
    ideal_hits = min(len(expected), len(retrieved_sources))
    ideal = [1] * ideal_hits + [0] * max(len(retrieved_sources) - ideal_hits, 0)
    ideal_dcg = _dcg(ideal)
    return _dcg(relevances) / ideal_dcg if ideal_dcg else 0.0


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * percentile
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    weight = rank - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _keyword_overlap(expected_keywords: list[str], content: str) -> dict:
    normalized_content = (content or "").lower()
    expected = [keyword.lower() for keyword in expected_keywords if keyword]
    matched = [keyword for keyword in expected if keyword in normalized_content]
    total = len(expected)
    ratio = round(len(matched) / total, 4) if total else 0.0
    return {
        "matched_keywords": matched,
        "match_count": len(matched),
        "match_ratio": ratio,
    }


def run_retrieval_benchmark(
    dataset_path: str,
    modes: list[str],
    output_dir: str | None = None,
    top_k: int = 5,
) -> list[Path]:
    dataset_path = os.path.abspath(dataset_path)
    cases = load_cases(dataset_path)
    output_root = Path(output_dir or config.EVAL_OUTPUT_DIR)
    output_root.mkdir(parents=True, exist_ok=True)

    vector_db = VectorDbManager()
    previous_mode = config.RETRIEVAL_MODE
    generated_paths: list[Path] = []
    run_started_at = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        for mode in modes:
            config.RETRIEVAL_MODE = mode
            case_results: list[dict] = []

            for case in cases:
                collection_name = config.get_vector_collection_name(case.collection)
                collection = vector_db.get_collection(collection_name)
                pipeline = RetrievalPipeline(collection, collection_name)

                started = time.perf_counter()
                docs = pipeline.search(case.question, top_k)
                latency_ms = round((time.perf_counter() - started) * 1000, 2)

                retrieved_sources = [doc.metadata.get("source", "") for doc in docs]
                hit_rank = _first_hit_rank(case.expected_sources, retrieved_sources)
                hit = hit_rank is not None
                source_recall = _source_recall_at_k(case.expected_sources, retrieved_sources)
                average_precision = _average_precision_at_k(case.expected_sources, retrieved_sources)
                ndcg = _ndcg_at_k(case.expected_sources, retrieved_sources)
                ranked_docs = []
                for index, doc in enumerate(docs):
                    overlap = _keyword_overlap(case.expected_keywords, doc.page_content)
                    ranked_docs.append(
                        {
                            "rank": index + 1,
                            "source": doc.metadata.get("source", ""),
                            "parent_id": doc.metadata.get("parent_id", ""),
                            "preview": doc.page_content[:220].replace("\n", " ").strip(),
                            **overlap,
                        }
                    )

                top1_keyword_ratio = ranked_docs[0]["match_ratio"] if ranked_docs else 0.0

                case_results.append(
                    {
                        "id": case.case_id,
                        "collection": config.normalize_collection_name(case.collection),
                        "question": case.question,
                        "ground_truth": case.ground_truth,
                        "expected_sources": case.expected_sources,
                        "expected_keywords": case.expected_keywords,
                        "latency_ms": latency_ms,
                        "source_hit": hit,
                        "first_hit_rank": hit_rank,
                        "source_recall_at_k": round(source_recall, 4) if source_recall is not None else None,
                        "average_precision_at_k": round(average_precision, 4) if average_precision is not None else None,
                        "ndcg_at_k": round(ndcg, 4) if ndcg is not None else None,
                        "top1_keyword_ratio": top1_keyword_ratio,
                        "retrieved": ranked_docs,
                    }
                )

            latencies = [item["latency_ms"] for item in case_results]
            hit_count = sum(1 for item in case_results if item["source_hit"])
            reciprocal_ranks = [
                (1 / item["first_hit_rank"]) if item["first_hit_rank"] else 0.0
                for item in case_results
            ]
            recalls = [
                item["source_recall_at_k"]
                for item in case_results
                if item["source_recall_at_k"] is not None
            ]
            average_precisions = [
                item["average_precision_at_k"]
                for item in case_results
                if item["average_precision_at_k"] is not None
            ]
            ndcgs = [
                item["ndcg_at_k"]
                for item in case_results
                if item["ndcg_at_k"] is not None
            ]
            top1_keyword_ratios = [item["top1_keyword_ratio"] for item in case_results]

            summary = {
                "dataset_path": dataset_path,
                "mode": mode,
                "top_k": top_k,
                "case_count": len(case_results),
                "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
                "p95_latency_ms": round(_percentile(latencies, 0.95), 2),
                "source_hit_rate": round(hit_count / len(case_results), 4) if case_results else 0,
                "source_recall_at_k": round(statistics.mean(recalls), 4) if recalls else 0,
                "mrr": round(statistics.mean(reciprocal_ranks), 4) if reciprocal_ranks else 0,
                "map_at_k": round(statistics.mean(average_precisions), 4) if average_precisions else 0,
                "ndcg_at_k": round(statistics.mean(ndcgs), 4) if ndcgs else 0,
                "avg_top1_keyword_ratio": round(statistics.mean(top1_keyword_ratios), 4) if top1_keyword_ratios else 0,
            }

            payload = {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "benchmark_type": "retrieval",
                "retrieval_mode": mode,
                "reranker_enabled": config.RERANKER_ENABLED,
                "reranker_model": config.RERANKER_MODEL,
                "top_k": top_k,
                "summary": summary,
                "cases": case_results,
            }

            report_path = output_root / f"retrieval_benchmark_{mode}_{run_started_at}.json"
            with open(report_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)

            log_event(
                logger,
                "evaluation.retrieval_benchmark_completed",
                mode=mode,
                dataset=dataset_path,
                report_path=str(report_path),
                case_count=len(case_results),
                source_hit_rate=summary["source_hit_rate"],
                mrr=summary["mrr"],
                avg_top1_keyword_ratio=summary["avg_top1_keyword_ratio"],
            )
            generated_paths.append(report_path)
    finally:
        config.RETRIEVAL_MODE = previous_mode

    return generated_paths
