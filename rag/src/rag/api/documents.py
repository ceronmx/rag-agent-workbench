from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from rag.api.dependencies import get_document_service
from rag.api.schemas import DocumentInfo
from rag.services.document import DocumentService
from typing import List
import os

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", response_model=List[DocumentInfo])
async def list_documents(
    document_service: DocumentService = Depends(get_document_service),
):
    """
    List all ingested documents.
    """
    try:
        return document_service.list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_name}")
async def delete_document(
    document_name: str,
    document_service: DocumentService = Depends(get_document_service),
):
    """
    Delete a document and all its chunks.
    """
    try:
        success = document_service.delete_document(document_name)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"Document '{document_name}' not found"
            )
        return {"status": "success", "message": f"Document '{document_name}' deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_name}/preview")
async def preview_document(
    document_name: str,
    document_service: DocumentService = Depends(get_document_service),
):
    """
    Get the original file for preview.
    """
    try:
        storage_path = document_service.get_document_path(document_name)
        if not storage_path or not os.path.exists(storage_path):
            raise HTTPException(
                status_code=404, detail=f"File for document '{document_name}' not found"
            )
        
        # Determine media type based on extension
        ext = os.path.splitext(storage_path)[1].lower()
        media_type = "application/octet-stream"
        if ext == ".pdf":
            media_type = "application/pdf"
        elif ext == ".txt" or ext == ".md":
            media_type = "text/plain"
        elif ext == ".docx":
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        return FileResponse(storage_path, media_type=media_type, filename=document_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        from rag.utils.logger import logger
        logger.error(f"Error in preview_document: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
