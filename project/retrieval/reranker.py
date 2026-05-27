import logging

from core.logging_utils import log_event
from sentence_transformers import CrossEncoder
import torch

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    _model_cache: dict[str, CrossEncoder] = {}
    _device_cache: dict[str, str] = {}

    def __init__(self, model_name: str):
        self.model_name = model_name
        if model_name not in self._model_cache:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model_cache[model_name] = CrossEncoder(model_name, device=device)
            self._device_cache[model_name] = device
            log_event(logger, "retrieval.reranker_loaded", model=model_name, device=device)
        self.model = self._model_cache[model_name]
        self.device = self._device_cache[model_name]

    def rerank(self, query: str, docs):
        if not docs:
            return []

        pairs = [(query, doc.page_content) for doc in docs]
        scores = self.model.predict(pairs, batch_size=16, show_progress_bar=False)
        ranked = sorted(
            zip(docs, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )
        return ranked
