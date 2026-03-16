"""Application configuration driven by environment variables."""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration — all values can be overridden via env vars or .env file."""

    # General
    app_name: str = "HU AI Platform"
    debug: bool = False
    api_version: str = "v1"
    log_level: str = "INFO"

    # OpenAI
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # Azure OpenAI
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"

    # Azure AI Search
    azure_search_endpoint: str | None = None
    azure_search_key: str | None = None
    azure_search_index: str = "hu-knowledge"

    # Vector store
    vector_store_type: Literal["faiss", "azure"] = "faiss"
    faiss_index_path: str = "data/faiss_index"

    # Session store
    session_store_type: Literal["sqlite", "cosmos"] = "sqlite"
    sqlite_path: str = "data/sessions.db"

    # Observability
    otel_enabled: bool = False
    otel_endpoint: str | None = None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }
