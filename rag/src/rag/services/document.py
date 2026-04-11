from sqlalchemy.orm import Session
from sqlalchemy import func
from rag.models.database import Chunk
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
            }
            for r in results
        ]

    def delete_document(self, document_name: str) -> bool:
        """
        Delete all chunks associated with a document name.
        """
        try:
            num_deleted = (
                self.db.query(Chunk)
                .filter(Chunk.document_name == document_name)
                .delete()
            )
            self.db.commit()
            return num_deleted > 0
        except Exception as e:
            self.db.rollback()
            raise e
