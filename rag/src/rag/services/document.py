import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from rag.models.database import Chunk, Document
from typing import List, Dict, Any


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all ingested documents with their chunk counts and file types.
        """
        results = (
            self.db.query(
                Chunk.document_name,
                func.count(Chunk.id).label("chunk_count"),
                func.max(Chunk.file_type).label("file_type"),
            )
            .group_by(Chunk.document_name)
            .all()
        )

        return [
            {
                "document_name": r.document_name,
                "chunk_count": r.chunk_count,
                "file_type": r.file_type,
                "preview_url": f"/documents/{r.document_name}/preview",
            }
            for r in results
        ]

    def delete_document(self, document_name: str) -> bool:
        """
        Delete a document record, all its chunks, and the physical file.
        """
        try:
            # Get document info to find storage path
            doc = self.db.query(Document).filter(Document.document_name == document_name).first()
            if doc and os.path.exists(doc.storage_path):
                try:
                    os.remove(doc.storage_path)
                except Exception as e:
                    print(f"Error removing file {doc.storage_path}: {e}")

            # Delete Chunks
            self.db.query(Chunk).filter(Chunk.document_name == document_name).delete()
            
            # Delete Document record
            num_deleted = 0
            if doc:
                self.db.delete(doc)
                num_deleted = 1
                
            self.db.commit()
            return num_deleted > 0
        except Exception as e:
            self.db.rollback()
            raise e

    def get_document_path(self, document_name: str) -> str:
        """
        Get the storage path for a document.
        """
        doc = (
            self.db.query(Document)
            .filter(Document.document_name == document_name)
            .first()
        )
        if doc:
            return doc.storage_path
        return None
