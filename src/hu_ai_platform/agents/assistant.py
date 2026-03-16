"""HU AI Assistant — main conversational agent powered by Agno."""

from agno.agent import Agent
from agno.knowledge.protocol import KnowledgeProtocol
from agno.models.openai import OpenAIChat

from hu_ai_platform.config import Settings
from hu_ai_platform.guardrails.eu_ai_act import get_system_disclosure

SYSTEM_PROMPT = """\
You are the Hogeschool Utrecht AI Assistant, a knowledgeable and helpful \
assistant for Hogeschool Utrecht (HU), a University of Applied Sciences in \
Utrecht, the Netherlands.

Your responsibilities:
- Answer questions about HU programs, courses, research, and student services.
- Help students, staff, and prospective students find relevant information.
- When you use information from the knowledge base, cite the source.
- Respond in the same language as the user (Dutch or English).
- If you don't know the answer, say so — never fabricate information.

Always be professional, inclusive, and supportive.\
"""


def create_assistant(
    settings: Settings,
    knowledge_base: KnowledgeProtocol | None = None,
    tools: list | None = None,  # type: ignore[type-arg]
) -> Agent:
    """Create and return the HU assistant agent with EU AI Act disclosure."""
    model = OpenAIChat(
        id=settings.openai_model,
        api_key=settings.openai_api_key,
    )

    agent = Agent(
        model=model,
        description="Hogeschool Utrecht AI Assistant",
        instructions=[SYSTEM_PROMPT, get_system_disclosure()],
        knowledge=knowledge_base,
        tools=tools,
        markdown=True,
    )
    return agent
