import logging
import uuid

import config
from core.logging_utils import log_event
from core.observability import Observability
from db.parent_store_manager import ParentStoreManager
from db.vector_db_manager import VectorDbManager
from document_chunker import DocumentChuncker
from multimodal import ClipFigureIndex
from providers import ProviderFactory
from rag_agent.graph import create_agent_graph
from rag_agent.tools import ToolFactory

logger = logging.getLogger(__name__)


class RAGSystem:

    def __init__(
        self,
        collection_key: str = config.DEFAULT_COLLECTION,
        vector_db: VectorDbManager | None = None,
        model_name: str | None = None,
    ):
        self.collection_key = config.normalize_collection_name(collection_key)
        self.model_name = model_name or config.LLM_MODEL
        self.collection_name = config.get_vector_collection_name(self.collection_key)
        self.markdown_dir = config.get_markdown_dir(self.collection_key)
        self.parent_store_path = config.get_parent_store_path(self.collection_key)
        self.vector_db = vector_db or VectorDbManager()
        self.parent_store = ParentStoreManager(self.parent_store_path)
        self.chunker = DocumentChuncker()
        self.figure_index = ClipFigureIndex(self.collection_key, self.vector_db.client) if config.MULTIMODAL_ENABLED else None
        self.observability = Observability()
        self.agent_graph = None
        self.default_thread_id = str(uuid.uuid4())
        self.recursion_limit = config.GRAPH_RECURSION_LIMIT

    def initialize(self):
        self.vector_db.create_collection(self.collection_name)
        collection = self.vector_db.get_collection(self.collection_name)

        llm = ProviderFactory.create_chat_model(model_name=self.model_name)
        tools = ToolFactory(
            collection,
            collection_name=self.collection_name,
            parent_store_path=self.parent_store_path,
            figure_index=self.figure_index,
        ).create_tools()
        self.agent_graph = create_agent_graph(llm, tools)
        log_event(
            logger,
            "rag.initialized",
            collection=self.collection_key,
            vector_collection=self.collection_name,
            provider=config.LLM_PROVIDER,
            model=self.model_name,
        )

    def get_config(self, thread_id: str | None = None):
        cfg = {
            "configurable": {"thread_id": thread_id or self.default_thread_id},
            "recursion_limit": self.recursion_limit,
        }
        handler = self.observability.get_handler()
        if handler:
            cfg["callbacks"] = [handler]
        return cfg

    def reset_thread(self, thread_id: str | None = None):
        active_thread_id = thread_id or self.default_thread_id
        try:
            self.agent_graph.checkpointer.delete_thread(active_thread_id)
        except Exception as exc:
            log_event(logger, "rag.thread.reset_failed", collection=self.collection_key, thread_id=active_thread_id, error=str(exc))
        if thread_id is None:
            self.default_thread_id = str(uuid.uuid4())
