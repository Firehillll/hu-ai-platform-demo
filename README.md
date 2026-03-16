# HU AI Platform Demo

An enterprise-grade AI platform demo for **Hogeschool Utrecht** — featuring a RAG-powered chatbot, multi-agent orchestration, GDPR/EU AI Act guardrails, and Azure-native infrastructure.

```
┌──────────────┐     ┌───────────────────────┐     ┌──────────────────┐
│   User       │────▶│   HU AI Platform      │────▶│  Azure OpenAI    │
│              │◀────│   (FastAPI + Agno)     │◀────│  (GPT-4o)        │
└──────────────┘     └───────────────────────┘     └──────────────────┘
                              │
                     ┌────────▼───────────┐    ┌──────────────────┐
                     │  Knowledge Base     │    │  Monitoring      │
                     │  (FAISS/AI Search)  │    │  (OpenTelemetry) │
                     └────────────────────┘    └──────────────────┘
```

## Quick Start

```bash
git clone https://github.com/hilariopedro/hu-ai-platform-demo.git
cd hu-ai-platform-demo
cp .env.example .env          # Add your OPENAI_API_KEY
make dev                      # Install dependencies
make seed                     # Populate knowledge base
make run                      # Start API on http://localhost:8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API via Swagger UI.

### CLI Chat

```bash
make chat                     # Interactive assistant with RAG + tools
make team                     # Multi-agent research team mode
```

**No API key?** The platform runs in demo mode — all endpoints work, chat returns a fallback response.

## Features

| Feature | Implementation |
|---------|---------------|
| **RAG Chatbot** | Agno agent + FAISS vector store + OpenAI embeddings |
| **Multi-Agent Team** | Coordinate-mode team with Researcher + Study Advisor agents |
| **PII Protection** | BSN, IBAN, email, phone detection and redaction (GDPR) |
| **EU AI Act Compliance** | Article 52 transparency notices on all responses |
| **Knowledge Pipeline** | Markdown ingestion → chunking → embedding → vector search |
| **Observability** | OpenTelemetry tracing + custom metrics (tokens, latency, guardrails) |
| **Azure IaC** | Bicep templates for OpenAI, AI Search, Container Apps, Key Vault |
| **CI/CD** | GitHub Actions for lint, test, type-check, build, deploy |
| **Local-First** | FAISS + SQLite fallbacks — works without any cloud credentials |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Application status |
| `GET` | `/api/v1/health` | Health check with component status |
| `POST` | `/api/v1/chat` | Chat with the AI assistant |
| `POST` | `/api/v1/knowledge/ingest` | Upload markdown to knowledge base |
| `GET` | `/api/v1/knowledge/search` | Search the knowledge base |

## Project Structure

```
src/hu_ai_platform/
├── main.py                 # FastAPI app + lifespan
├── config.py               # Pydantic Settings (env-driven)
├── api/                    # REST API layer
├── agents/                 # Agno agents (assistant + research team)
├── tools/                  # Agent tools (search, curriculum)
├── knowledge/              # RAG pipeline (vectorstore + loader)
├── guardrails/             # PII filter, EU AI Act, language check
├── monitoring/             # OpenTelemetry + metrics
└── storage/                # Session persistence (SQLite/Cosmos)
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.12+** | Modern, typed, async |
| **FastAPI** | Async API framework with auto-docs |
| **Agno** | Lightweight agent framework (model-agnostic) |
| **uv** | Fast Python package manager (Rust-based) |
| **ruff** | All-in-one linter/formatter |
| **FAISS** | Local vector search (Azure AI Search in production) |
| **OpenTelemetry** | Distributed tracing and metrics |
| **Bicep** | Azure Infrastructure as Code |
| **GitHub Actions** | CI/CD pipeline |
| **Docker** | Containerized deployment |

## Development

```bash
make dev        # Install all dependencies (including dev tools)
make lint       # Run ruff linter and formatter check
make format     # Auto-fix formatting and lint issues
make typecheck  # Run mypy strict type checking
make test       # Run pytest suite
make run        # Start development server with hot reload
make chat       # Interactive CLI assistant (with RAG + tools)
make team       # Interactive CLI multi-agent research team
```

## Docker

```bash
make docker-up    # Build and run containerized
make docker-down  # Stop containers
```

## Documentation

- [Architecture Overview](docs/architecture.md) — C4-style system diagrams
- [Data Flow](docs/data-flow.md) — GDPR data flow mapping
- [Model Card](docs/model-card.md) — Responsible AI documentation
- **Architecture Decision Records:**
  - [ADR 001: Agno over LangChain](docs/adr/001-agno-over-langchain.md)
  - [ADR 002: uv Package Manager](docs/adr/002-uv-package-manager.md)
  - [ADR 003: Azure Managed Identity](docs/adr/003-azure-managed-identity.md)
  - [ADR 004: EU AI Act Guardrails](docs/adr/004-eu-ai-act-guardrails.md)

## Deliverable Mapping

| HU Deliverable | Where in this project |
|---|---|
| AI platform setup | `infra/` (Bicep), `config.py`, `compose.yaml` |
| CI/CD for AI | `.github/workflows/`, `Makefile`, `.pre-commit-config.yaml` |
| Data pipelines | `knowledge/`, `POST /api/v1/knowledge/ingest` |
| Sandbox environment | `compose.yaml`, local FAISS fallback |
| Chatbot/agent platform + RAG | `agents/`, `tools/`, `knowledge/` |
| Generative AI infrastructure | `agents/assistant.py`, streaming chat endpoint |
| Monitoring/validation | `monitoring/`, `guardrails/`, health endpoint |
| Technical documentation | `docs/`, ADRs, model card, README |

## License

MIT — see [LICENSE](LICENSE)

## Author

**Hilario Pedro** — AI Engineer
