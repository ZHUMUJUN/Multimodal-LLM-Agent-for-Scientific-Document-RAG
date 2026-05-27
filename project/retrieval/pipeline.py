import logging

import config
from core.logging_utils import log_event
from core.tracing import add_span_attributes, start_span
from retrieval.reranker import CrossEncoderReranker

logger = logging.getLogger(__name__)


class RetrievalPipeline:

    def __init__(self, collection, collection_name: str):
        self.collection = collection
        self.collection_name = collection_name
        self._reranker = None

    def _get_reranker(self):
        if self._reranker is None:
            self._reranker = CrossEncoderReranker(config.RERANKER_MODEL)
        return self._reranker

    def search(self, query: str, limit: int):
        candidate_limit = max(limit, min(config.RERANK_MAX_CANDIDATES, limit * config.RERANK_CANDIDATE_MULTIPLIER))
        with start_span(
            "retrieval.search",
            collection=self.collection_name,
            retrieval_mode=config.RETRIEVAL_MODE,
            requested_k=limit,
            candidate_limit=candidate_limit,
            reranker_enabled=config.RERANKER_ENABLED,
        ) as span:
            docs = self.collection.similarity_search(
                query,
                k=candidate_limit,
                score_threshold=config.SIMILARITY_SCORE_THRESHOLD,
            )

            log_event(
                logger,
                "retrieval.hybrid_search",
                collection=self.collection_name,
                query=query,
                mode=config.RETRIEVAL_MODE,
                requested=limit,
                retrieved=len(docs),
                candidate_limit=candidate_limit,
            )
            add_span_attributes(span, retrieved_candidates=len(docs))

            if config.RETRIEVAL_MODE != "hybrid_rerank" or not config.RERANKER_ENABLED:
                returned = docs[:limit]
                add_span_attributes(span, returned_count=len(returned))
                return returned

            ranked = self._get_reranker().rerank(query, docs)
            reranked_docs = [doc for doc, _score in ranked[:limit]]
            top_scores = [float(score) for _doc, score in ranked[: min(limit, 3)]]
            log_event(
                logger,
                "retrieval.reranked",
                collection=self.collection_name,
                query=query,
                reranker_model=config.RERANKER_MODEL,
                candidate_count=len(docs),
                returned=len(reranked_docs),
                top_scores=top_scores,
            )
            add_span_attributes(
                span,
                reranker_model=config.RERANKER_MODEL,
                returned_count=len(reranked_docs),
            )
            return reranked_docs
