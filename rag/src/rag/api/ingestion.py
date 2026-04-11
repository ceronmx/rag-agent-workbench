from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from rag.api.dependencies import get_ingestion_service
from rag.api.schemas import TextIngestRequest
from rag.services.ingestion import IngestionService
import shutil
import os
import tempfile
from typing import Optional

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/file")
async def ingest_file(
    file: UploadFile = File(...),
    document_name: Optional[str] = Form(None),
    chunk_size: int = Form(1000),
    overlap: int = Form(200),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    """
    Upload and ingest a document (PDF, DOCX, TXT).
    """
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = await ingestion_service.ingest_file(
            file_path=temp_file_path,
            chunk_size=chunk_size,
            overlap=overlap,
            document_name=document_name or file.filename,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


@router.post("/text")
async def ingest_text(
    request: TextIngestRequest,
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    """
    Ingest raw text into the RAG system.
    """
    try:
        result = await ingestion_service.ingest_text(
            text=request.text,
            document_name=request.document_name,
            chunk_size=request.chunk_size,
            overlap=request.overlap,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
