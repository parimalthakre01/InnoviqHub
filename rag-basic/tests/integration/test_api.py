"""Integration tests — require a running server or use FastAPI TestClient."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.services.rag_pipeline.nugen_client.embed", new_callable=AsyncMock)
@patch("app.services.vector_store.vector_store.upsert")
def test_ingest(mock_upsert, mock_embed):
    mock_embed.return_value = [0.1] * 768
    response = client.post(
        "/api/v1/ingest/",
        json={"text": "Hello world test document", "metadata": {}},
    )
    assert response.status_code == 200
    assert response.json()["chunks_stored"] >= 1
