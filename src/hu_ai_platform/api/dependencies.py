"""FastAPI dependency injection providers."""

from fastapi import Request

from hu_ai_platform.config import Settings
from hu_ai_platform.monitoring.metrics import MetricsCollector
from hu_ai_platform.storage.session import SessionStore


def get_settings(request: Request) -> Settings:
    return request.app.state.settings  # type: ignore[no-any-return]


def get_knowledge_base(request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.knowledge_base


def get_session_store(request: Request) -> SessionStore:
    return request.app.state.session_store  # type: ignore[no-any-return]


def get_metrics(request: Request) -> MetricsCollector:
    return request.app.state.metrics  # type: ignore[no-any-return]
