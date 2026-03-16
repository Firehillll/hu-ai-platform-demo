# ADR 003: Azure Managed Identity for Authentication

## Status
Accepted

## Context
The platform needs to authenticate with Azure services (OpenAI, AI Search, Key Vault). Options include API keys, service principals, and managed identities.

## Decision
Use **Azure Managed Identity** for all Azure service authentication in production, with API key fallback for local development.

## Rationale
- **No secrets in code**: Managed Identity eliminates the need to store and rotate API keys
- **Zero-trust alignment**: Follows Azure's recommended security practices
- **RBAC integration**: Permissions managed via Azure Role-Based Access Control
- **Automatic rotation**: Azure handles credential lifecycle management
- **Local dev parity**: DefaultAzureCredential tries Managed Identity first, then falls back to CLI auth or environment variables

## Consequences
- Local development requires either Azure CLI login or environment variables with API keys
- Infrastructure must be provisioned with identity assignments (handled in Bicep)
- Adds dependency on `azure-identity` package in production (not needed for local-only mode)
