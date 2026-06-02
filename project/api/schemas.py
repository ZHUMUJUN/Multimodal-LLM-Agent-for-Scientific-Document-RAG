from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    collection: str = Field(default="default")
    message: str
    session_id: str | None = None
    skill_name: str | None = None


class ChatResponse(BaseModel):
    run_id: str | None = None
    collection: str
    session_id: str
    answer: str
    retrieval_mode: str | None = None
    resolved_retrieval_mode: str | None = None
    routing_reasons: list[str] = Field(default_factory=list)
    active_skill: str | None = None
    skill_reasons: list[str] = Field(default_factory=list)
    skill_version: str | None = None
    selected_model: str | None = None
    model_route_reasons: list[str] = Field(default_factory=list)
    model_complexity: str | None = None
    worker_roles: list[str] = Field(default_factory=list)
    worker_count: int = 0
    tool_call_count: int = 0
    reflection_count: int = 0
    reflection_search_count: int = 0


class ResetRequest(BaseModel):
    collection: str = Field(default="default")
    session_id: str | None = None


class FigureSearchRequest(BaseModel):
    collection: str = Field(default="default")
    query: str
    limit: int = Field(default=5, ge=1, le=20)


class CollectionResponse(BaseModel):
    name: str
    vector_collection: str
    document_count: int


class SkillResponse(BaseModel):
    name: str
    description: str
    allowed_tools: list[str] = Field(default_factory=list)
    retrieval_mode: str = "auto"
    triggers: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    version: str | None = None
    path: str


class MemoryWriteRequest(BaseModel):
    scope: str
    key: str
    value: str
    kind: str = "semantic"
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    ttl_seconds: int | None = Field(default=None, ge=1)
    source_run_id: str | None = None


class BadcaseRequest(BaseModel):
    note: str = ""
    expected_answer: str = ""
    tags: list[str] = Field(default_factory=list)


class ToolApprovalResolveRequest(BaseModel):
    resolved_by: str = "user"
    note: str = ""
