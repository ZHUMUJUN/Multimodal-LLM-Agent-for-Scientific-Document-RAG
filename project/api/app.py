from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import config
from api.schemas import (
    BadcaseRequest,
    ChatRequest,
    ChatResponse,
    CollectionResponse,
    FigureSearchRequest,
    MemoryWriteRequest,
    ResetRequest,
    SkillResponse,
    ToolApprovalResolveRequest,
)
from services import PlatformService


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic RAG Platform", version="0.1.0")
    platform_service = PlatformService()
    Path(config.FIGURE_ROOT_DIR).mkdir(parents=True, exist_ok=True)
    app.mount("/figures/files", StaticFiles(directory=config.FIGURE_ROOT_DIR), name="figure-files")

    @app.get("/health")
    def health():
        return platform_service.health()

    @app.get("/collections", response_model=list[CollectionResponse])
    def list_collections():
        return platform_service.list_collections()

    @app.get("/skills", response_model=list[SkillResponse])
    def list_skills():
        return platform_service.list_skills()

    @app.get("/runs")
    def list_runs(limit: int = 20):
        return platform_service.list_runs(limit=limit)

    @app.get("/runs/{run_id}")
    def get_run_trace(run_id: str):
        return platform_service.get_run_trace(run_id)

    @app.get("/runs/{run_id}/trajectory")
    def evaluate_run_trace(run_id: str):
        return platform_service.evaluate_run_trace(run_id)

    @app.post("/runs/{run_id}/resume")
    def resume_run(run_id: str):
        return platform_service.resume_run(run_id)

    @app.get("/tool-approvals")
    def list_tool_approvals(status: str | None = None, run_id: str | None = None, limit: int = 50):
        return platform_service.list_tool_approvals(status=status, run_id=run_id, limit=limit)

    @app.post("/tool-approvals/{approval_id}/approve")
    def approve_tool_approval(approval_id: str, request: ToolApprovalResolveRequest):
        return platform_service.resolve_tool_approval(
            approval_id,
            approved=True,
            resolved_by=request.resolved_by,
            note=request.note,
        )

    @app.post("/tool-approvals/{approval_id}/reject")
    def reject_tool_approval(approval_id: str, request: ToolApprovalResolveRequest):
        return platform_service.resolve_tool_approval(
            approval_id,
            approved=False,
            resolved_by=request.resolved_by,
            note=request.note,
        )

    @app.post("/runs/{run_id}/badcase")
    def record_badcase(run_id: str, request: BadcaseRequest):
        return platform_service.record_badcase(
            run_id,
            note=request.note,
            expected_answer=request.expected_answer,
            tags=request.tags,
        )

    @app.post("/memories")
    def write_memory(request: MemoryWriteRequest):
        return platform_service.write_memory(
            scope=request.scope,
            key=request.key,
            value=request.value,
            kind=request.kind,
            importance=request.importance,
            ttl_seconds=request.ttl_seconds,
            source_run_id=request.source_run_id,
        )

    @app.get("/memories/search")
    def search_memories(query: str, scope: str | None = None, limit: int = 10):
        return platform_service.search_memories(query=query, scope=scope, limit=limit)

    @app.post("/memories/prune")
    def prune_memories(expired_only: bool = True, max_importance: float | None = None):
        return platform_service.prune_memories(expired_only=expired_only, max_importance=max_importance)

    @app.delete("/memories/{memory_id}")
    def delete_memory(memory_id: int):
        return platform_service.delete_memory(memory_id)

    @app.post("/ingest")
    def ingest(collection: str = "default", files: list[UploadFile] = File(...)):
        return platform_service.ingest_uploads(collection=collection, uploads=files)

    @app.post("/chat", response_model=ChatResponse)
    def chat(request: ChatRequest):
        return platform_service.chat(
            collection=request.collection,
            message=request.message,
            session_id=request.session_id,
            skill_name=request.skill_name,
        )

    @app.post("/chat/stream")
    async def chat_stream(request: ChatRequest):
        return StreamingResponse(
            platform_service.chat_stream(
                collection=request.collection,
                message=request.message,
                session_id=request.session_id,
                skill_name=request.skill_name,
            ),
            media_type="text/event-stream",
        )

    @app.post("/figures/search")
    def search_figures(request: FigureSearchRequest):
        return platform_service.search_figures(
            collection=request.collection,
            query=request.query,
            limit=request.limit,
        )

    @app.post("/reset")
    def reset(request: ResetRequest):
        return platform_service.reset(collection=request.collection, session_id=request.session_id)

    return app


app = create_app()
