from __future__ import annotations

from fastapi.testclient import TestClient

from ..main import app


client = TestClient(app)


def test_chat_endpoint_returns_reply(monkeypatch):
    response = client.post(
        "/api/chat",
        json={"agent": "support", "channel_id": "web", "user_id": "user", "text": "Hello there"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["tool_runs"] == []
