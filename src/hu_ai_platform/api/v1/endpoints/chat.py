"""Chat endpoint — conversational AI interface with guardrails."""

import logging
import uuid

from agno.knowledge.protocol import KnowledgeProtocol
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from hu_ai_platform.agents.assistant import create_assistant
from hu_ai_platform.agents.research_team import create_research_team
from hu_ai_platform.api.dependencies import (
    get_knowledge_base,
    get_metrics,
    get_session_store,
    get_settings,
)
from hu_ai_platform.config import Settings
from hu_ai_platform.guardrails.eu_ai_act import add_transparency_notice
from hu_ai_platform.guardrails.language_check import detect_language
from hu_ai_platform.guardrails.pii_filter import redact_pii
from hu_ai_platform.monitoring.metrics import MetricsCollector, RequestMetrics, Timer
from hu_ai_platform.storage.session import SessionStore
from hu_ai_platform.tools.curriculum_tool import list_programs, lookup_program

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    team_mode: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: str
    language: str
    pii_redacted: bool
    sources: list[str] | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    settings: Settings = Depends(get_settings),
    knowledge_base: KnowledgeProtocol | None = Depends(get_knowledge_base),
    session_store: SessionStore = Depends(get_session_store),
    metrics: MetricsCollector = Depends(get_metrics),
) -> ChatResponse:
    """Process a chat message through the guardrail pipeline and return a response."""
    session_id = request.session_id or str(uuid.uuid4())
    req_metrics = RequestMetrics()

    # --- Input guardrails ---
    message, pii_detections = redact_pii(request.message)
    pii_redacted = len(pii_detections) > 0
    if pii_redacted:
        req_metrics.guardrail_triggered = True
        req_metrics.guardrail_type = "pii_filter"
        logger.info(
            "PII redacted from input (session=%s, types=%s)",
            session_id,
            [d.pii_type for d in pii_detections],
        )

    language = detect_language(message)

    # Store the user message
    session_store.add_message(session_id, "user", message)

    if not settings.openai_api_key:
        demo_response = (
            "**Demo mode** — no OpenAI API key configured. "
            "Set `OPENAI_API_KEY` in your `.env` file to enable the AI assistant.\n\n"
            f"Your message was: *{message}*"
        )
        demo_response = add_transparency_notice(demo_response, language)
        session_store.add_message(session_id, "assistant", demo_response)

        return ChatResponse(
            response=demo_response,
            session_id=session_id,
            language=language,
            pii_redacted=pii_redacted,
        )

    try:
        with Timer() as timer:
            if request.team_mode:
                team = create_research_team(settings)
                team_response = team.run(message)
                content = getattr(team_response, "content", "") or ""
            else:
                history = session_store.get_history(session_id, limit=10)
                agent = create_assistant(
                    settings=settings,
                    knowledge_base=knowledge_base,
                    tools=[lookup_program, list_programs],
                )
                agent_response = agent.run(message, messages=history)
                content = getattr(agent_response, "content", "") or ""
        req_metrics.latency_ms = timer.elapsed_ms

        # --- Output guardrails ---
        content = add_transparency_notice(content, language)

        session_store.add_message(session_id, "assistant", content)
        metrics.record(req_metrics)

        return ChatResponse(
            response=content,
            session_id=session_id,
            language=language,
            pii_redacted=pii_redacted,
        )
    except Exception as exc:
        logger.exception("Chat request failed (session=%s)", session_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
