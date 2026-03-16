"""API v1 router — aggregates all endpoint routers."""

from fastapi import APIRouter

from hu_ai_platform.api.v1.endpoints import chat, health, knowledge

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(health.router, tags=["health"])
router.include_router(chat.router, tags=["chat"])
router.include_router(knowledge.router, tags=["knowledge"])
