"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hu_ai_platform.config import Settings
from hu_ai_platform.monitoring.metrics import MetricsCollector
from hu_ai_platform.monitoring.telemetry import setup_telemetry
from hu_ai_platform.storage.session import SessionStore

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize shared resources on startup, clean up on shutdown."""
    settings = Settings()
    app.state.settings = settings
    app.state.knowledge_base = None

    setup_telemetry(settings)

    app.state.metrics = MetricsCollector()
    app.state.session_store = SessionStore(settings)

    logger.info("HU AI Platform started (model=%s)", settings.openai_model)
    yield

    app.state.session_store.close()
    logger.info("HU AI Platform shut down")


app = FastAPI(
    title="HU AI Platform",
    description="AI Platform Demo for Hogeschool Utrecht",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from hu_ai_platform.api.v1.router import router as v1_router  # noqa: E402

app.include_router(v1_router)


@app.get("/")
async def root() -> dict[str, str]:
    settings: Settings = app.state.settings
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "status": "running",
    }
