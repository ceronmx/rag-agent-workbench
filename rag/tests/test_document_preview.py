import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rag.models.database import Base, Document, Chunk, SQLALCHEMY_DATABASE_URL
from rag.services.ingestion import IngestionService
from rag.services.document import DocumentService
import shutil
import tempfile
from unittest.mock import patch, AsyncMock

# Use the real DB for integration testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Provide a transactional scope around a series of operations."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_db

client = TestClient(app)

@pytest.mark.asyncio
async def test_preview_endpoint(db_session):
    # Override get_db to use our test session
    app.dependency_overrides[get_db] = lambda: db_session
    
    with tempfile.TemporaryDirectory() as temp_upload_dir:
        with patch("rag.services.ingestion.UPLOAD_DIR", temp_upload_dir):
            ingestion_service = IngestionService(db_session)
            
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                tmp.write(b"API preview test content.")
                tmp_path = tmp.name
            
            try:
                with patch("rag.services.ingestion.get_embeddings", new_callable=AsyncMock) as mock_emb:
                    mock_emb.return_value = [[0.1] * 768]
                    await ingestion_service.ingest_file(tmp_path, document_name="api_test.txt")
                    
                    # Test preview endpoint
                    response = client.get("/documents/api_test.txt/preview")
                    assert response.status_code == 200
                    assert response.content == b"API preview test content."
                    assert response.headers["content-type"] == "text/plain; charset=utf-8"
                    
                    # Test list documents includes preview_url
                    response = client.get("/documents/")
                    assert response.status_code == 200
                    docs = response.json()
                    test_doc = next((d for d in docs if d["document_name"] == "api_test.txt"), None)
                    assert test_doc is not None
                    assert test_doc["preview_url"] == "/documents/api_test.txt/preview"
                    
                    # Test 404
                    response = client.get("/documents/non_existent.txt/preview")
                    assert response.status_code == 404
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                app.dependency_overrides.clear()
