import logging

import config
from core.logging_utils import log_event
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

logger = logging.getLogger(__name__)


class VectorDbManager:
    _client_cache: dict[str, QdrantClient] = {}
    _dense_cache: dict[str, HuggingFaceEmbeddings] = {}
    _sparse_cache: dict[str, FastEmbedSparse] = {}

    def __init__(self, db_path: str = config.QDRANT_DB_PATH):
        self.db_path = db_path

        if db_path not in self._client_cache:
            self._client_cache[db_path] = QdrantClient(path=db_path)
        if config.DENSE_MODEL not in self._dense_cache:
            self._dense_cache[config.DENSE_MODEL] = HuggingFaceEmbeddings(model_name=config.DENSE_MODEL)
        if config.SPARSE_MODEL not in self._sparse_cache:
            self._sparse_cache[config.SPARSE_MODEL] = FastEmbedSparse(model_name=config.SPARSE_MODEL)

        self._client = self._client_cache[db_path]
        self._dense_embeddings = self._dense_cache[config.DENSE_MODEL]
        self._sparse_embeddings = self._sparse_cache[config.SPARSE_MODEL]

    def create_collection(self, collection_name: str):
        if self._client.collection_exists(collection_name):
            log_event(logger, "qdrant.collection.exists", collection=collection_name)
            return

        vector_size = len(self._dense_embeddings.embed_query("test"))
        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(size=vector_size, distance=qmodels.Distance.COSINE),
            sparse_vectors_config={config.SPARSE_VECTOR_NAME: qmodels.SparseVectorParams()},
        )
        log_event(logger, "qdrant.collection.created", collection=collection_name, vector_size=vector_size)

    def delete_collection(self, collection_name: str):
        if self._client.collection_exists(collection_name):
            self._client.delete_collection(collection_name)
            log_event(logger, "qdrant.collection.deleted", collection=collection_name)

    def get_collection(self, collection_name: str) -> QdrantVectorStore:
        return QdrantVectorStore(
            client=self._client,
            collection_name=collection_name,
            embedding=self._dense_embeddings,
            sparse_embedding=self._sparse_embeddings,
            retrieval_mode=RetrievalMode.HYBRID,
            sparse_vector_name=config.SPARSE_VECTOR_NAME,
        )

    @property
    def client(self) -> QdrantClient:
        return self._client

    def list_collections(self, prefix: str = config.COLLECTION_PREFIX) -> list[str]:
        collections = self._client.get_collections().collections
        return sorted(
            item.name for item in collections
            if item.name.startswith(prefix)
        )

    def count_documents(self, collection_name: str) -> int:
        if not self._client.collection_exists(collection_name):
            return 0
        info = self._client.get_collection(collection_name)
        return info.points_count or 0
