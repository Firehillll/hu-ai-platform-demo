# Architecture Overview

## System Context (C4 Level 1)

```
┌──────────────┐     ┌───────────────────────┐     ┌──────────────────┐
│   Student /  │────▶│   HU AI Platform      │────▶│  Azure OpenAI    │
│   Staff      │◀────│   (FastAPI)            │◀────│  (GPT-4o)        │
└──────────────┘     └───────────────────────┘     └──────────────────┘
                              │  ▲
                              │  │
                     ┌────────▼──┴────────┐    ┌──────────────────┐
                     │  Knowledge Base     │    │  Azure Monitor   │
                     │  (FAISS / AI Search)│    │  (OpenTelemetry) │
                     └────────────────────┘    └──────────────────┘
```

## Container Diagram (C4 Level 2)

### API Layer (`src/hu_ai_platform/api/`)
- **FastAPI** application with versioned endpoints (`/api/v1/`)
- Endpoints: `/chat`, `/health`, `/knowledge/ingest`, `/knowledge/search`
- Dependency injection for settings, agents, and knowledge base

### Agent Layer (`src/hu_ai_platform/agents/`)
- **Agno** framework for agent orchestration
- Single assistant agent for standard queries
- Multi-agent team (coordinate mode) for complex research queries
- Model-agnostic: swap OpenAI for any supported provider

### Knowledge Layer (`src/hu_ai_platform/knowledge/`)
- Document loading and chunking (markdown → chunks with metadata)
- Vector store abstraction (FAISS local / Azure AI Search production)
- OpenAI embeddings (`text-embedding-3-small`)

### Guardrails Layer (`src/hu_ai_platform/guardrails/`)
- **PII filter**: Detects and redacts BSN, IBAN, email, phone numbers
- **EU AI Act**: Transparency notices per Article 52
- **Language detection**: Dutch/English for appropriate responses

### Monitoring Layer (`src/hu_ai_platform/monitoring/`)
- OpenTelemetry integration for distributed tracing
- Custom metrics: token usage, latency, guardrail triggers
- Azure Monitor / Application Insights export

### Storage Layer (`src/hu_ai_platform/storage/`)
- SQLite (local) / Cosmos DB (Azure) for session persistence

## Deployment Architecture

```
GitHub Actions CI/CD
        │
        ▼
Docker Container (ghcr.io)
        │
        ▼
Azure Container Apps
├── Azure OpenAI (GPT-4o)
├── Azure AI Search (vector store)
├── Azure Key Vault (secrets)
└── Azure Monitor (observability)
```

## Key Design Decisions

See [ADR directory](adr/) for detailed decision records.

- **Local-first**: Every Azure service has a local fallback (FAISS, SQLite)
- **Agent-per-request**: Stateless agents created via dependency injection
- **Guardrails-first**: PII filtering and EU AI Act compliance enabled by default
