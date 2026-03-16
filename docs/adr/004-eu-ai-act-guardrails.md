# ADR 004: EU AI Act Guardrails by Default

## Status
Accepted

## Context
The EU AI Act (Regulation 2024/1689) introduces mandatory requirements for AI systems deployed in the EU. As a Dutch university, HU must comply with transparency and data protection obligations.

## Decision
Implement **guardrails as mandatory middleware**, enabled by default in all environments.

## Guardrails Implemented
1. **PII Detection & Redaction**: Scan inputs for Dutch personal data (BSN, IBAN, phone, email) before processing. Detected PII is redacted and logged.
2. **Transparency Notice**: Every AI-generated response includes a disclosure that it was produced by an AI system (Article 52 compliance).
3. **Language Detection**: Detect user language (Dutch/English) to provide transparency notices in the appropriate language.

## Rationale
- **Legal compliance**: EU AI Act Article 52 requires clear disclosure when users interact with AI systems
- **GDPR alignment**: PII filtering prevents personal data from being sent to external AI models
- **Trust**: Transparency builds trust with students, staff, and regulators
- **Defense in depth**: Guardrails at the application layer complement model-level safety

## Consequences
- Small latency overhead for PII scanning (< 5ms per request)
- Transparency notices add text to every response
- PII patterns are specific to Dutch formats — may need extension for international use
