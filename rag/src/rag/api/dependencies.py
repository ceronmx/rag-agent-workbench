from fastapi import Depends
from sqlalchemy.orm import Session
from rag.models.database import SessionLocal
from rag.services.ingestion import IngestionService
from rag.services.query import QueryService
from rag.services.evaluation import EvaluationService
from rag.services.document import DocumentService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_ingestion_service(db: Session = Depends(get_db)) -> IngestionService:
    return IngestionService(db)

def get_query_service() -> QueryService:
    return QueryService()

def get_evaluation_service() -> EvaluationService:
    return EvaluationService()

def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)
