import json
import logging
import os
import statistics
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import config
from core.logging_utils import log_event
from providers import ProviderFactory
from retrieval import RetrievalPipeline
from services.platform_service import PlatformService

from .schemas import load_cases

logger = logging.getLogger(__name__)

def _try_run_ragas(case_results: list[dict], llm=None, embeddings=None) -> dict:
    eligible = [
        {
            "user_input": item["question"],
            "response": item["answer"],
            "retrieved_contexts": item["retrieved_contexts"],
            "reference": item["ground_truth"],
        }
        for item in case_results
        if item.get("ground_truth", "").strip()
    ]

    if not eligible:
        return {
            "enabled": False,
            "available": False,
            "evaluated_cases": 0,
            "scores": {},
            "skipped_reason": "No cases with non-empty ground_truth were found.",
        }

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.embeddings import LangchainEmbeddingsWrapper
        from ragas.llms import LangchainLLMWrapper
        from ragas.metrics import answer_relevancy, faithfulness
    except ImportError as exc:
        return {
            "enabled": False,
            "available": False,
            "evaluated_cases": len(eligible),
            "scores": {},
            "skipped_reason": f"Ragas dependencies are missing: {exc}",
        }

    try:
        dataset = Dataset.from_list(eligible)
        ragas_llm = LangchainLLMWrapper(llm or ProviderFactory.create_chat_model())
        ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
        metrics = [
            deepcopy(answer_relevancy),
            deepcopy(faithfulness),
        ]
        metrics[0].llm = ragas_llm
        metrics[0].embeddings = ragas_embeddings
        metrics[1].llm = ragas_llm
        result = evaluate(
            dataset,
            metrics=metrics,
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            show_progress=False,
            raise_exceptions=False,
        )
        if hasattr(result, "to_pandas"):
            summary = result.to_pandas().mean(numeric_only=True).to_dict()
        elif isinstance(result, dict):
            summary = result
        else:
            summary = {"raw": str(result)}
        normalized = {key: float(value) for key, value in summary.items() if isinstance(value, (int, float))}
        if not normalized and "raw" in summary:
            normalized = {"raw": summary["raw"]}
        return {
            "enabled": True,
            "available": True,
            "evaluated_cases": len(eligible),
            "scores": normalized,
        }
    except Exception as exc:
        return {
            "enabled": True,
            "available": False,
            "evaluated_cases": len(eligible),
            "scores": {},
            "skipped_reason": f"Ragas evaluation failed: {exc}",
        }


def run_benchmark(
    dataset_path: str,
    modes: list[str],
    output_dir: str | None = None,
    top_k: int = 5,
) -> list[Path]:
    dataset_path = os.path.abspath(dataset_path)
    cases = load_cases(dataset_path)
    output_root = Path(output_dir or config.EVAL_OUTPUT_DIR)
    output_root.mkdir(parents=True, exist_ok=True)

    previous_mode = config.RETRIEVAL_MODE
    generated_paths: list[Path] = []
    run_started_at = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        for mode in modes:
            config.RETRIEVAL_MODE = mode
            try:
                service = PlatformService()
            except RuntimeError as exc:
                if "already accessed by another instance of Qdrant client" in str(exc):
                    raise RuntimeError(
                        "Benchmark cannot start while another local Qdrant-backed process is running. "
                        "Stop `python app.py` or `python api_server.py`, then rerun the benchmark."
                    ) from exc
                raise
            case_results: list[dict] = []

            for case in cases:
                started = time.perf_counter()
                response = service.chat(
                    collection=case.collection,
                    message=case.question,
                    session_id=f"benchmark-{mode}-{case.case_id}",
                )
                latency_ms = round((time.perf_counter() - started) * 1000, 2)

                rag_system = service._get_system(case.collection)
                collection = service.vector_db.get_collection(rag_system.collection_name)
                retrieved_docs = RetrievalPipeline(collection, rag_system.collection_name).search(case.question, top_k)
                retrieved_contexts = [doc.page_content for doc in retrieved_docs]
                sources = [doc.metadata.get("source", "") for doc in retrieved_docs]

                case_results.append(
                    {
                        "id": case.case_id,
                        "collection": config.normalize_collection_name(case.collection),
                        "question": case.question,
                        "answer": response["answer"],
                        "ground_truth": case.ground_truth,
                        "expected_sources": case.expected_sources,
                        "notes": case.notes,
                        "latency_ms": latency_ms,
                        "answer_length": len(response["answer"] or ""),
                        "retrieved_contexts": retrieved_contexts,
                        "retrieved_sources": sources,
                    }
                )

            latencies = [item["latency_ms"] for item in case_results]
            ragas_summary = _try_run_ragas(
                case_results,
                llm=ProviderFactory.create_chat_model(),
                embeddings=service.vector_db._dense_embeddings,
            )
            summary = {
                "dataset_path": dataset_path,
                "mode": mode,
                "case_count": len(case_results),
                "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
                "p95_latency_ms": round(max(latencies), 2) if latencies else 0,
                "avg_answer_length": round(statistics.mean(item["answer_length"] for item in case_results), 2),
                "ragas": ragas_summary,
            }

            payload = {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "retrieval_mode": mode,
                "model": config.LLM_MODEL,
                "provider": config.LLM_PROVIDER,
                "reranker_enabled": config.RERANKER_ENABLED,
                "reranker_model": config.RERANKER_MODEL,
                "top_k": top_k,
                "summary": summary,
                "cases": case_results,
            }

            report_path = output_root / f"benchmark_{mode}_{run_started_at}.json"
            with open(report_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)
            log_event(
                logger,
                "evaluation.benchmark_completed",
                mode=mode,
                dataset=dataset_path,
                report_path=str(report_path),
                case_count=len(case_results),
            )
            generated_paths.append(report_path)
    finally:
        config.RETRIEVAL_MODE = previous_mode

    return generated_paths
