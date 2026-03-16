"""Health and metrics endpoints."""

from fastapi import APIRouter, Depends

from hu_ai_platform.api.dependencies import get_metrics, get_settings
from hu_ai_platform.config import Settings
from hu_ai_platform.monitoring.metrics import MetricsCollector

router = APIRouter()


@router.get("/health")
async def health_check(
    settings: Settings = Depends(get_settings),
) -> dict[str, object]:
    return {
        "status": "healthy",
        "version": settings.api_version,
        "checks": {
            "vectorstore": settings.vector_store_type,
            "llm_configured": settings.openai_api_key is not None,
            "otel_enabled": settings.otel_enabled,
        },
    }


@router.get("/metrics")
async def get_metrics_summary(
    metrics: MetricsCollector = Depends(get_metrics),
) -> dict[str, object]:
    """Return aggregated request metrics."""
    return metrics.summary()
