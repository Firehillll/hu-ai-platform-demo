# Data Flow Documentation

## GDPR Data Flow Mapping

This document describes how data flows through the HU AI Platform, in compliance with GDPR documentation requirements.

## Data Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────┐
│  PII Filter          │  ← Scan for BSN, IBAN, email, phone
│  (guardrails)        │  ← Redact detected PII
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Language Detection  │  ← Determine nl/en for response language
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  RAG Retrieval       │  ← Query vector store for relevant context
│  (FAISS / AI Search) │  ← Return top-k document chunks
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  LLM Processing      │  ← Send sanitized query + context to OpenAI
│  (Azure OpenAI)      │  ← Generate response
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Transparency Notice │  ← Append EU AI Act disclosure
└─────────────────────┘
    │
    ▼
Response to User
```

## Data Categories

| Data Type | Source | Processing | Storage | Retention |
|-----------|--------|------------|---------|-----------|
| User query | User input | PII scan → redact → LLM | Session store (SQLite/Cosmos) | Session duration |
| AI response | LLM output | Transparency notice added | Session store | Session duration |
| Knowledge base | Curated documents | Embedded → vector store | FAISS index / AI Search | Until re-seeded |
| Metrics | System telemetry | Aggregated (no PII) | In-memory / Azure Monitor | Configurable |

## Data Protection Measures

1. **PII Redaction**: All user inputs are scanned for Dutch PII patterns before processing
2. **No Training**: User data is not used to train or fine-tune the base model (OpenAI API policy)
3. **Data Minimization**: Only the current query and relevant context are sent to the LLM
4. **Encryption**: Azure services use encryption at rest and in transit
5. **Session Isolation**: Each session is independently stored and retrievable

## Data Processing Basis

- **Legitimate interest**: Providing information services to students and staff
- **Consent**: Users initiate the interaction and are informed via transparency notice
- **Data processor agreement**: Required with OpenAI/Azure for production deployment

## DPIA Considerations

For production deployment, a Data Protection Impact Assessment (DPIA) should address:
- Risk of re-identification from aggregated queries
- Impact of LLM hallucinations on student decisions
- Cross-border data transfer implications (Azure region selection)
