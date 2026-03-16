"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from hu_ai_platform.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


class TestRootEndpoint:
    def test_root_returns_status(self, client) -> None:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "name" in data


class TestHealthEndpoint:
    def test_health_returns_healthy(self, client) -> None:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data


class TestMetricsEndpoint:
    def test_metrics_returns_summary(self, client) -> None:
        response = client.get("/api/v1/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_requests" in data


class TestChatEndpoint:
    def test_chat_returns_valid_response(self, client) -> None:
        """Chat returns a well-formed response with transparency notice."""
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert "language" in data
        assert "pii_redacted" in data
        # EU AI Act transparency notice must always be present
        assert "AI system" in data["response"] or "AI-systeem" in data["response"]

    def test_chat_with_session_id(self, client) -> None:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hi", "session_id": "test-session-123"},
        )
        assert response.status_code == 200
        assert response.json()["session_id"] == "test-session-123"

    def test_chat_pii_redaction(self, client) -> None:
        """PII in user input should be flagged."""
        response = client.post(
            "/api/v1/chat",
            json={"message": "My email is student@hu.nl and my BSN is 111222333"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["pii_redacted"] is True

    def test_chat_dutch_detected(self, client) -> None:
        """Dutch input should be detected."""
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Wat is de opleiding voor AI bij Hogeschool Utrecht?"
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "nl"
