"""OpenTelemetry setup for observability."""

import logging

from hu_ai_platform.config import Settings

logger = logging.getLogger(__name__)


def setup_telemetry(settings: Settings) -> None:
    """Initialize OpenTelemetry tracing and metrics if enabled."""
    if not settings.otel_enabled:
        logger.info("OpenTelemetry is disabled")
        return

    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    resource = Resource.create({"service.name": "hu-ai-platform"})
    provider = TracerProvider(resource=resource)

    if settings.otel_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[import-not-found]
                OTLPSpanExporter,
            )

            exporter = OTLPSpanExporter(endpoint=settings.otel_endpoint)
            provider.add_span_processor(BatchSpanProcessor(exporter))
            logger.info("OTLP exporter configured: %s", settings.otel_endpoint)
        except ImportError:
            logger.warning("OTLP exporter not installed, falling back to console")
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    logger.info("OpenTelemetry tracing initialized")
