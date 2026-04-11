from fastapi import APIRouter, Depends, HTTPException
from rag.api.dependencies import get_document_service
from rag.api.schemas import DocumentInfo
from rag.services.document import DocumentService
from typing import List

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
