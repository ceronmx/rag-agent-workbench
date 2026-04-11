from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_document_service
from unittest.mock import MagicMock

client = TestClient(app)


def test_list_documents_success():
    mock_service = MagicMock()
    mock_service.list_documents.return_value = [
        {"document_name": "doc1.pdf", "chunk_count": 10, "file_type": "pdf"}
    ]
    app.dependency_overrides[get_document_service] = lambda: mock_service

    response = client.get("/documents/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["document_name"] == "doc1.pdf"


def test_delete_document_success():
    mock_service = MagicMock()
    mock_service.delete_document.return_value = True
    app.dependency_overrides[get_document_service] = lambda: mock_service

    response = client.delete("/documents/doc1.pdf")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_delete_document_not_found():
    mock_service = MagicMock()
    mock_service.delete_document.return_value = False
    app.dependency_overrides[get_document_service] = lambda: mock_service

    response = client.delete("/documents/nonexistent.pdf")

    app.dependency_overrides.clear()

    assert response.status_code == 404
