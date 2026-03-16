"""University search tool — allows the agent to query the knowledge base."""

from hu_ai_platform.knowledge.vectorstore import FAISSVectorStore


def search_university_knowledge(query: str, store: FAISSVectorStore, k: int = 5) -> str:
    """Search the HU knowledge base and return formatted results.

    This function is designed to be wrapped as an Agno tool for the assistant agent.
    """
    results = store.search(query, k=k)

    if not results:
        return "No relevant information found in the knowledge base."

    formatted = []
    for i, result in enumerate(results, 1):
        source = result.metadata.get("source", "unknown")
        formatted.append(f"**[{i}]** (source: {source})\n{result.content}")

    return "\n\n---\n\n".join(formatted)
