"""CLI entry-point for running HU AI agents interactively in the terminal.

Usage:
    python -m hu_ai_platform.cli assistant   # single assistant chat
    python -m hu_ai_platform.cli team        # multi-agent research team
"""

from __future__ import annotations

import argparse
import sys

from hu_ai_platform.config import Settings


def run_assistant() -> None:
    """Launch the HU AI Assistant in interactive CLI mode."""
    from hu_ai_platform.agents.assistant import create_assistant
    from hu_ai_platform.knowledge.vectorstore import create_vector_store
    from hu_ai_platform.tools.curriculum_tool import list_programs, lookup_program

    settings = Settings()

    store = create_vector_store(settings)
    knowledge = store if store.document_count > 0 else None

    agent = create_assistant(
        settings,
        knowledge_base=knowledge,
        tools=[lookup_program, list_programs],
    )

    print("\n=== HU AI Assistant ===")
    if knowledge:
        print(f"Knowledge base loaded: {store.document_count} documents")
    else:
        print("No knowledge base found. Run 'make seed' first for RAG support.")
    print("Type your question and press Enter. Press Ctrl+C or type 'exit' to quit.\n")

    agent.cli_app(markdown=True, stream=True, exit_on=["exit", "quit", "bye"])


def run_team() -> None:
    """Launch the HU Research Team in interactive CLI mode."""
    from hu_ai_platform.agents.research_team import create_research_team

    settings = Settings()
    team = create_research_team(settings)

    print("\n=== HU Research Team (multi-agent) ===")
    print("Type your question and press Enter. Press Ctrl+C or type 'exit' to quit.\n")

    team.cli_app(markdown=True, stream=True, exit_on=["exit", "quit", "bye"])


def main() -> None:
    """Parse arguments and dispatch to the chosen mode."""
    parser = argparse.ArgumentParser(
        description="HU AI Platform - Interactive CLI",
    )
    parser.add_argument(
        "mode",
        choices=["assistant", "team"],
        nargs="?",
        default="assistant",
        help="Which agent to run: 'assistant' (default) or 'team'.",
    )
    args = parser.parse_args()

    try:
        if args.mode == "team":
            run_team()
        else:
            run_assistant()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
