import os
import re

# --- Directory Configuration ---
_BASE_DIR = os.path.dirname(__file__)

MARKDOWN_ROOT_DIR = os.path.join(_BASE_DIR, "markdown_docs")
PARENT_STORE_ROOT = os.path.join(_BASE_DIR, "parent_store")
QDRANT_DB_PATH = os.path.join(_BASE_DIR, "qdrant_db")
SKILLS_DIR = os.environ.get("AGENT_SKILLS_DIR", os.path.join(_BASE_DIR, "skills"))
FIGURE_ROOT_DIR = os.environ.get("FIGURE_ROOT_DIR", os.path.join(_BASE_DIR, "figure_store"))

# --- PDF Parsing Configuration ---
PDF_PARSE_MODE = os.environ.get("PDF_PARSE_MODE", "auto").lower()
PDF_FAST_PARSE_FILE_MB = float(os.environ.get("PDF_FAST_PARSE_FILE_MB", "20"))
PDF_FAST_PARSE_IMAGE_COUNT = int(os.environ.get("PDF_FAST_PARSE_IMAGE_COUNT", "30"))

# --- Collection Configuration ---
DEFAULT_COLLECTION = os.environ.get("RAG_DEFAULT_COLLECTION", "default")
COLLECTION_PREFIX = os.environ.get("RAG_COLLECTION_PREFIX", "document_child_chunks")
COLLECTION_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9_-]+")

# --- Qdrant Configuration ---
SPARSE_VECTOR_NAME = "sparse"

# --- Multimodal / Figure Retrieval Configuration ---
MULTIMODAL_ENABLED = os.environ.get("MULTIMODAL_ENABLED", "true").lower() == "true"
FIGURE_COLLECTION_PREFIX = os.environ.get("FIGURE_COLLECTION_PREFIX", "document_figures")
CLIP_MODEL = os.environ.get("CLIP_MODEL", "clip-ViT-B-32")
CLIP_DEVICE = os.environ.get("CLIP_DEVICE", "")
CLIP_BATCH_SIZE = int(os.environ.get("CLIP_BATCH_SIZE", "8"))
FIGURE_INDEX_PAGE_SCREENSHOTS = os.environ.get("FIGURE_INDEX_PAGE_SCREENSHOTS", "true").lower() == "true"
FIGURE_INDEX_EMBEDDED_IMAGES = os.environ.get("FIGURE_INDEX_EMBEDDED_IMAGES", "true").lower() == "true"
FIGURE_PAGE_RENDER_DPI = int(os.environ.get("FIGURE_PAGE_RENDER_DPI", "120"))
FIGURE_MAX_PAGES_PER_DOC = int(os.environ.get("FIGURE_MAX_PAGES_PER_DOC", "60"))
FIGURE_MIN_WIDTH = int(os.environ.get("FIGURE_MIN_WIDTH", "160"))
FIGURE_MIN_HEIGHT = int(os.environ.get("FIGURE_MIN_HEIGHT", "120"))
FIGURE_MAX_IMAGE_PIXELS = int(os.environ.get("FIGURE_MAX_IMAGE_PIXELS", "12000000"))
FIGURE_CONTEXT_CHARS = int(os.environ.get("FIGURE_CONTEXT_CHARS", "1200"))

# --- Model Configuration ---
DENSE_MODEL = os.environ.get("DENSE_MODEL", "sentence-transformers/all-mpnet-base-v2")
SPARSE_MODEL = os.environ.get("SPARSE_MODEL", "Qdrant/bm25")

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama").lower()
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3:14b")
SMALL_LLM_MODEL = os.environ.get("SMALL_LLM_MODEL", "qwen2.5:1.5b")
LARGE_LLM_MODEL = os.environ.get("LARGE_LLM_MODEL", LLM_MODEL)
MODEL_ROUTER_ENABLED = os.environ.get("MODEL_ROUTER_ENABLED", "false").lower() == "true"
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0"))
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
LOCAL_VLLM_BASE_URL = os.environ.get("LOCAL_VLLM_BASE_URL", "http://localhost:8001/v1")
LOCAL_VLLM_API_KEY = os.environ.get("LOCAL_VLLM_API_KEY", "dummy")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# --- Corrective RAG / Web Search Fallback ---
CRAG_ENABLED = os.environ.get("CRAG_ENABLED", "false").lower() == "true"
CRAG_PROVIDER = os.environ.get("CRAG_PROVIDER", "tavily").lower()
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")
CRAG_MAX_RESULTS = int(os.environ.get("CRAG_MAX_RESULTS", "5"))
CRAG_SEARCH_DEPTH = os.environ.get("CRAG_SEARCH_DEPTH", "basic")
CRAG_TIMEOUT_SECONDS = int(os.environ.get("CRAG_TIMEOUT_SECONDS", "20"))

# --- Retrieval Configuration ---
RETRIEVAL_MODE = os.environ.get("RETRIEVAL_MODE", "baseline_hybrid")
SIMILARITY_SCORE_THRESHOLD = float(os.environ.get("SIMILARITY_SCORE_THRESHOLD", "0.7"))
RERANKER_ENABLED = os.environ.get("RERANKER_ENABLED", "true").lower() == "true"
RERANKER_MODEL = os.environ.get("RERANKER_MODEL", "BAAI/bge-reranker-base")
RERANK_CANDIDATE_MULTIPLIER = int(os.environ.get("RERANK_CANDIDATE_MULTIPLIER", "4"))
RERANK_MAX_CANDIDATES = int(os.environ.get("RERANK_MAX_CANDIDATES", "20"))

# --- Evaluation Configuration ---
EVAL_OUTPUT_DIR = os.environ.get("EVAL_OUTPUT_DIR", os.path.join(_BASE_DIR, "evaluation", "reports"))
EVAL_DEFAULT_DATASET = os.environ.get(
    "EVAL_DEFAULT_DATASET",
    os.path.join(_BASE_DIR, "evaluation", "datasets", "sample_eval.jsonl"),
)

# --- LightRAG Configuration ---
LIGHTRAG_ENABLED = os.environ.get("LIGHTRAG_ENABLED", "true").lower() == "true"
LIGHTRAG_BASE_URL = os.environ.get("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
LIGHTRAG_QUERY_MODE = os.environ.get("LIGHTRAG_QUERY_MODE", "mix")
LIGHTRAG_TIMEOUT_SECONDS = int(os.environ.get("LIGHTRAG_TIMEOUT_SECONDS", "180"))
LIGHTRAG_TOP_K = int(os.environ.get("LIGHTRAG_TOP_K", "10"))
LIGHTRAG_CHUNK_TOP_K = int(os.environ.get("LIGHTRAG_CHUNK_TOP_K", "10"))

# --- Agent Configuration ---
SKILLS_ENABLED = os.environ.get("SKILLS_ENABLED", "true").lower() == "true"
SKILL_RETRIEVAL_MODES = {"baseline_hybrid", "hybrid_rerank", "lightrag", "router"}
WORKER_SPECS_DIR = os.environ.get("AGENT_WORKER_SPECS_DIR", os.path.join(_BASE_DIR, "agents", "specs"))
REFLECTION_ENABLED = os.environ.get("REFLECTION_ENABLED", "true").lower() == "true"
MAX_REFLECTION_ROUNDS = int(os.environ.get("MAX_REFLECTION_ROUNDS", "1"))
MIN_EVIDENCE_SCORE = float(os.environ.get("MIN_EVIDENCE_SCORE", "0.7"))
MULTI_AGENT_PLANNER_ENABLED = os.environ.get("MULTI_AGENT_PLANNER_ENABLED", "true").lower() == "true"
MAX_TOOL_CALLS = 8
MAX_ITERATIONS = 10
GRAPH_RECURSION_LIMIT = 50
BASE_TOKEN_THRESHOLD = 2000
TOKEN_GROWTH_FACTOR = 0.9

# --- Agent Harness Runtime ---
MEMORY_ENABLED = os.environ.get("AGENT_MEMORY_ENABLED", "true").lower() == "true"
MEMORY_DB_PATH = os.environ.get("AGENT_MEMORY_DB_PATH", os.path.join(_BASE_DIR, "agent_memory.db"))
MEMORY_INJECTION_ENABLED = os.environ.get("AGENT_MEMORY_INJECTION_ENABLED", "true").lower() == "true"
MEMORY_INJECTION_LIMIT = int(os.environ.get("AGENT_MEMORY_INJECTION_LIMIT", "4"))
MEMORY_MAX_CONTEXT_CHARS = int(os.environ.get("AGENT_MEMORY_MAX_CONTEXT_CHARS", "2500"))
BADCASE_DATASET_PATH = os.environ.get(
    "AGENT_BADCASE_DATASET_PATH",
    os.path.join(_BASE_DIR, "evaluation", "datasets", "agent_badcases.jsonl"),
)
BADCASE_EVAL_DATASET_PATH = os.environ.get(
    "AGENT_BADCASE_EVAL_DATASET_PATH",
    os.path.join(_BASE_DIR, "evaluation", "datasets", "agent_badcase_eval.jsonl"),
)
TOOL_POLICY_ENABLED = os.environ.get("AGENT_TOOL_POLICY_ENABLED", "true").lower() == "true"
TOOL_POLICY_ENFORCE_WORKER_ALLOWED_TOOLS = os.environ.get("AGENT_TOOL_POLICY_ENFORCE_WORKER_ALLOWED_TOOLS", "true").lower() == "true"
TOOL_APPROVAL_ENABLED = os.environ.get("AGENT_TOOL_APPROVAL_ENABLED", "true").lower() == "true"
TOOL_APPROVAL_REQUIRED_RISKS = {
    risk.strip().lower()
    for risk in os.environ.get("AGENT_TOOL_APPROVAL_REQUIRED_RISKS", "high").split(",")
    if risk.strip()
}
TOOL_POLICY_ALLOW_HIGH_RISK = os.environ.get("AGENT_TOOL_POLICY_ALLOW_HIGH_RISK", "false").lower() == "true"
TOOL_POLICY_MAX_QUERY_CHARS = int(os.environ.get("AGENT_TOOL_POLICY_MAX_QUERY_CHARS", "2000"))
TOOL_POLICY_MAX_PATH_CHARS = int(os.environ.get("AGENT_TOOL_POLICY_MAX_PATH_CHARS", "500"))

# --- Worker Runtime Controls ---
WORKER_MAX_RETRIES = int(os.environ.get("AGENT_WORKER_MAX_RETRIES", "1"))
WORKER_TIMEOUT_SECONDS = float(os.environ.get("AGENT_WORKER_TIMEOUT_SECONDS", "60"))
WORKER_MAX_CONCURRENCY = int(os.environ.get("AGENT_WORKER_MAX_CONCURRENCY", "4"))

# --- Workspace Sandbox ---
WORKSPACE_ROOT = os.environ.get("AGENT_WORKSPACE_ROOT", os.path.dirname(_BASE_DIR))
WORKSPACE_WRITE_ROOT = os.environ.get("AGENT_WORKSPACE_WRITE_ROOT", os.path.join(_BASE_DIR, "workspace"))
MCP_FILESYSTEM_WRITE_ENABLED = os.environ.get("MCP_FILESYSTEM_WRITE_ENABLED", "false").lower() == "true"
WORKSPACE_BLOCKED_PATH_PATTERNS = [
    pattern.strip()
    for pattern in os.environ.get(
        "AGENT_WORKSPACE_BLOCKED_PATH_PATTERNS",
        ".env,.env.*,id_rsa,id_ed25519,*.pem,*.key,*secret*,*token*,*.sqlite,*.db",
    ).split(",")
    if pattern.strip()
]

# --- Text Splitter Configuration ---
CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP = 100
MIN_PARENT_SIZE = 2000
MAX_PARENT_SIZE = 4000
HEADERS_TO_SPLIT_ON = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3"),
]

# --- Langfuse Observability ---
LANGFUSE_ENABLED = os.environ.get("LANGFUSE_ENABLED", "false").lower() == "true"
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGFUSE_BASE_URL = os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000")

# --- Phoenix Tracing ---
PHOENIX_ENABLED = os.environ.get("PHOENIX_ENABLED", "false").lower() == "true"
PHOENIX_COLLECTOR_ENDPOINT = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT", "http://127.0.0.1:6006/v1/traces")
PHOENIX_PROJECT_NAME = os.environ.get("PHOENIX_PROJECT_NAME", "agentic-rag-platform")
PHOENIX_PROTOCOL = os.environ.get("PHOENIX_PROTOCOL", "http/protobuf")
PHOENIX_API_KEY = os.environ.get("PHOENIX_API_KEY", "")

# --- Gradio / API Runtime ---
GRADIO_HOST = os.environ.get("GRADIO_HOST", "127.0.0.1")
GRADIO_PORT = int(os.environ.get("GRADIO_PORT", "7860"))
API_HOST = os.environ.get("API_HOST", "127.0.0.1")
API_PORT = int(os.environ.get("API_PORT", "8000"))

# --- MCP Filesystem Server ---
MCP_FILESYSTEM_SERVER_NAME = os.environ.get("MCP_FILESYSTEM_SERVER_NAME", "agentic-rag-filesystem")
MCP_FILESYSTEM_ENABLED = os.environ.get("MCP_FILESYSTEM_ENABLED", "true").lower() == "true"
MCP_FILESYSTEM_TRANSPORT = os.environ.get("MCP_FILESYSTEM_TRANSPORT", "stdio")
MCP_FILESYSTEM_MAX_READ_CHARS = int(os.environ.get("MCP_FILESYSTEM_MAX_READ_CHARS", "12000"))
MCP_FILESYSTEM_MAX_SEARCH_RESULTS = int(os.environ.get("MCP_FILESYSTEM_MAX_SEARCH_RESULTS", "25"))
MCP_FILESYSTEM_SEARCH_MAX_FILE_SIZE = int(os.environ.get("MCP_FILESYSTEM_SEARCH_MAX_FILE_SIZE", "1048576"))
_DEFAULT_ALLOWED_ROOTS = ",".join([
    os.path.dirname(_BASE_DIR),
    os.path.join(_BASE_DIR, "evaluation"),
    os.path.join(_BASE_DIR, "test_corpus"),
])
MCP_FILESYSTEM_ALLOWED_ROOTS = [
    os.path.abspath(path.strip())
    for path in os.environ.get("MCP_FILESYSTEM_ALLOWED_ROOTS", _DEFAULT_ALLOWED_ROOTS).split(",")
    if path.strip()
]


def normalize_collection_name(name: str | None) -> str:
    normalized = (name or DEFAULT_COLLECTION).strip().lower()
    normalized = COLLECTION_NAME_PATTERN.sub("-", normalized).strip("-")
    return normalized or DEFAULT_COLLECTION


def get_vector_collection_name(name: str | None = None) -> str:
    return f"{COLLECTION_PREFIX}_{normalize_collection_name(name)}"


def get_figure_collection_name(name: str | None = None) -> str:
    return f"{FIGURE_COLLECTION_PREFIX}_{normalize_collection_name(name)}"


def get_markdown_dir(name: str | None = None) -> str:
    return os.path.join(MARKDOWN_ROOT_DIR, normalize_collection_name(name))


def get_figure_dir(name: str | None = None) -> str:
    return os.path.join(FIGURE_ROOT_DIR, normalize_collection_name(name))


def get_parent_store_path(name: str | None = None) -> str:
    return os.path.join(PARENT_STORE_ROOT, normalize_collection_name(name))


MARKDOWN_DIR = get_markdown_dir(DEFAULT_COLLECTION)
PARENT_STORE_PATH = get_parent_store_path(DEFAULT_COLLECTION)
CHILD_COLLECTION = get_vector_collection_name(DEFAULT_COLLECTION)
