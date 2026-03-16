# ADR 001: Agno over LangChain

## Status
Accepted

## Context
We need an agent framework to build the HU AI Assistant. The main candidates are LangChain, LlamaIndex, Semantic Kernel, and Agno (formerly Phidata).

## Decision
We chose **Agno** as the agent framework.

## Rationale
- **Lightweight**: Agno has minimal abstractions compared to LangChain's deep chain/callback hierarchy. This makes the codebase easier to understand and maintain.
- **Model-agnostic**: Supports OpenAI, Azure OpenAI, Anthropic, and local models with the same API.
- **Multi-agent support**: Built-in team/coordinate mode for multi-agent orchestration without additional libraries.
- **Fast iteration**: Simple API means less boilerplate. An agent can be defined in ~10 lines.
- **Production-ready**: Supports structured outputs, tool calling, and streaming out of the box.

## Consequences
- Smaller community and ecosystem compared to LangChain
- Fewer pre-built integrations (but we only need OpenAI + FAISS)
- Team members may need to learn a less well-known framework
