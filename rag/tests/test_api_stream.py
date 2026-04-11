from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_query_service
from unittest.mock import AsyncMock
import json

client = TestClient(app)


async def mock_generator():
    yield {"message": {"content": "Hello"}}
    yield {"message": {"content": " world"}}


def test_query_stream_endpoint_success():
    # Mock result from service
    mock_result = {"is_stream": True, "answer": mock_generator()}

    mock_service = AsyncMock()
    mock_service.query.return_value = mock_result
    app.dependency_overrides[get_query_service] = lambda: mock_service

    with client.stream(
        "POST", "/query/stream", json={"question": "Stream test"}
    ) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        lines = [line for line in response.iter_lines() if line]
        assert 'data: {"content": "Hello"}' in lines
        assert 'data: {"content": " world"}' in lines
        assert "data: [DONE]" in lines

    app.dependency_overrides.clear()
