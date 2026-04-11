from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_query_service
from unittest.mock import AsyncMock

client = TestClient(app)

def test_query_endpoint_success():
    # Mock return value of QueryService.query
    mock_result = {
        "answer": "The key findings involve revenue growth.",
        "search_query": "key findings",
        "search_mode": "vector",
        "contexts": [
            {
                "text": "Revenue grew by 10% in Q4.",
                "document_name": "Report2025.pdf",
                "chunk_index": 0,
                "score": 0.85,
                "file_type": "pdf"
            }
        ],
        "is_stream": False
    }

    # Override the dependency to use a mock service
    mock_service = AsyncMock()
    mock_service.query.return_value = mock_result
    app.dependency_overrides[get_query_service] = lambda: mock_service

    response = client.post("/query/", json={"question": "What are the key findings?"})
    
    # Cleanup dependency overrides
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == mock_result["answer"]
    assert data["search_query"] == mock_result["search_query"]
    assert len(data["contexts"]) == 1
    assert data["contexts"][0]["document_name"] == "Report2025.pdf"

def test_query_endpoint_streaming_forbidden():
    # Mock service returning a stream result
    mock_service = AsyncMock()
    mock_service.query.return_value = {"is_stream": True}
    app.dependency_overrides[get_query_service] = lambda: mock_service

    response = client.post("/query/", json={"question": "Any question", "use_stream": True})
    
    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert "Streaming is not supported via this endpoint" in response.json()["detail"]
