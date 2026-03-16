"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from hu_ai_platform.config import Settings
from hu_ai_platform.main import app


@pytest.fixture
def settings() -> Settings:
    """Test settings with no external dependencies."""
    return Settings(
        openai_api_key=None,
        vector_store_type="faiss",
        session_store_type="sqlite",
        sqlite_path=":memory:",
        debug=True,
    )


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
