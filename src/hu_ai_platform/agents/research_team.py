"""Multi-agent research team — demonstrates Agno team/coordinate mode."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team, TeamMode

from hu_ai_platform.config import Settings


def create_research_team(settings: Settings) -> Team:
    """Create a multi-agent research team for complex queries."""
    model = OpenAIChat(
        id=settings.openai_model,
        api_key=settings.openai_api_key,
    )

    researcher = Agent(
        name="Researcher",
        model=model,
        description="Research specialist who finds and synthesizes information.",
        instructions=[
            "You are a research specialist at Hogeschool Utrecht.",
            "Find relevant information and provide detailed, well-sourced answers.",
            "Focus on accuracy and completeness.",
        ],
        markdown=True,
    )

    advisor = Agent(
        name="Study Advisor",
        model=model,
        description="Academic advisor who helps with study-related questions.",
        instructions=[
            "You are a study advisor at Hogeschool Utrecht.",
            "Help students with course selection, study planning, and academic guidance.",
            "Be empathetic and practical in your recommendations.",
        ],
        markdown=True,
    )

    team = Team(
        name="HU Research Team",
        mode=TeamMode.coordinate,
        members=[researcher, advisor],
        model=model,
        description="A team of specialists that collaborates to answer complex queries about HU.",
        instructions=[
            "Coordinate between team members to provide comprehensive answers.",
            "The Researcher handles factual questions, the Study Advisor handles guidance.",
            "Synthesize responses into a single, coherent answer.",
        ],
        markdown=True,
    )
    return team
