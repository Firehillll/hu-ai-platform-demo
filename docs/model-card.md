# Model Card — HU AI Assistant

## Model Details

| Field | Value |
|-------|-------|
| **Model Name** | HU AI Assistant |
| **Version** | 0.1.0 |
| **Type** | RAG-augmented conversational agent |
| **Base Model** | OpenAI GPT-4o (via API) |
| **Framework** | Agno |
| **Developer** | Hogeschool Utrecht — AI Engineering Team |

## Intended Use

### Primary Use Cases
- Answering questions about HU programs, courses, and research
- Providing information to prospective and current students
- Assisting staff with knowledge retrieval

### Out of Scope
- Medical, legal, or financial advice
- Automated decision-making affecting student outcomes
- Processing or storing personal data beyond the session

## Training Data
The base model (GPT-4o) is trained by OpenAI. The RAG knowledge base contains:
- General information about Hogeschool Utrecht
- AI Minor curriculum details
- Research project descriptions

All knowledge base content is curated and reviewed by HU staff.

## Evaluation

### Metrics
- **Response relevance**: Evaluated via RAG retrieval accuracy
- **Language accuracy**: Dutch and English response quality
- **PII compliance**: Zero PII leakage in outputs
- **Bias evaluation**: Tested for equitable handling of Dutch and English inputs

### Known Limitations
- Responses are limited to information in the knowledge base
- May not reflect the most current program changes
- Language detection may be inaccurate for very short inputs

## Ethical Considerations

### Bias & Fairness
- The system treats Dutch and English inputs equitably
- No demographic data is collected or used for personalization
- Bias evaluation tests are included in the test suite

### Privacy
- PII detection and redaction is enabled by default
- No conversation data is sent to external systems beyond the LLM API call
- Session data is stored locally (SQLite) or in Azure Cosmos DB with encryption

### Transparency
- Every response includes an EU AI Act Article 52 transparency notice
- The system identifies itself as AI when asked
- Source citations are provided when using RAG-retrieved information

## Maintenance
- Knowledge base updates require re-running the seed pipeline
- Model version changes are configured via environment variables
- Guardrail patterns should be reviewed quarterly
