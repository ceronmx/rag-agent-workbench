from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_ingestion_service
from unittest.mock import AsyncMock
import io

client = TestClient(app)

def test_ingest_text_success():
    mock_service = AsyncMock()
    mock_service.ingest_text.return_value = {"status": "success", "chunks_ingested": 2}
    app.dependency_overrides[get_ingestion_service] = lambda: mock_service

    payload = {
        "text": "This is some raw text to ingest.",
        "document_name": "test_doc",
        "chunk_size": 100,
        "overlap": 20
    }
    response = client.post("/ingest/text", json=payload)
    
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["chunks_ingested"] == 2

def test_ingest_file_success():
    mock_service = AsyncMock()
    mock_service.ingest_file.return_value = {"status": "success", "chunks_ingested": 5}
    app.dependency_overrides[get_ingestion_service] = lambda: mock_service

    # Create a dummy file
    file_content = b"Dummy PDF content"
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/ingest/file",
        files={"file": ("test.pdf", file, "application/pdf")},
        data={"document_name": "test_file_doc"}
    )
    
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["chunks_ingested"] == 5
