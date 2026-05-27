from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import config
from api.schemas import ChatRequest, ChatResponse, CollectionResponse, FigureSearchRequest, ResetRequest, SkillResponse
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
