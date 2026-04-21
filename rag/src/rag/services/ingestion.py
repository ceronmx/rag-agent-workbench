import os
import shutil
from sqlalchemy.orm import Session
from typing import Optional
from rag.models.database import Chunk, Document
from rag.models.ollama_client import get_embeddings
from rag.rag.extractor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extract_text_general,
    partition_document,
    HAS_UNSTRUCTURED,
)
from rag.rag.chunker import chunk_text, chunk_elements
from rag.utils.logger import logger

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")


class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        # Ensure upload directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)

    async def ingest_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        overlap: int = 200,
        document_name: str = None,
    ):
        doc_name = document_name or os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        # Save to persistent storage
        storage_filename = f"{doc_name}{ext}" if not doc_name.endswith(ext) else doc_name
        persistent_path = os.path.join(UPLOAD_DIR, storage_filename)
        
        # Avoid overwriting with same name if it's already there (optional but safer)
        if os.path.abspath(file_path) != os.path.abspath(persistent_path):
            shutil.copy(file_path, persistent_path)
            
        logger.info(f"Ingesting {file_path} (Type: {ext}) as '{doc_name}'...")
        logger.info(f"Stored original file at {persistent_path}")

        if HAS_UNSTRUCTURED:
            try:
                logger.info(f"Using Unstructured.io for auto-partitioning of {ext}...")
                elements = partition_document(file_path)
                chunks_text = chunk_elements(
                    elements, max_characters=chunk_size, overlap=overlap
                )
                logger.info(f"Created {len(chunks_text)} layout-aware chunks.")
            except Exception as e:
                logger.warning(
                    f"Unstructured partitioning failed for {ext}: {e}. Falling back to standard extraction."
                )
                text = self._fallback_extract(file_path, ext)
                chunks_text = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        else:
            text = self._fallback_extract(file_path, ext)
            chunks_text = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

        if not chunks_text:
            logger.warning("No text extracted from file.")
            return {"status": "success", "chunks_ingested": 0}

        logger.info("Generating embeddings...")
        embeddings = await get_embeddings(chunks_text)

        logger.info("Storing in database...")
        file_type = ext.replace(".", "")

        try:
            # Create Document record
            doc_record = self.db.query(Document).filter(Document.document_name == doc_name).first()
            if not doc_record:
                doc_record = Document(
                    document_name=doc_name,
                    storage_path=persistent_path,
                    file_type=file_type
                )
                self.db.add(doc_record)
            else:
                doc_record.storage_path = persistent_path
                doc_record.file_type = file_type

            for i, (txt, emb) in enumerate(zip(chunks_text, embeddings)):
                chunk = Chunk(
                    text=txt,
                    document_name=doc_name,
                    chunk_index=i,
                    embedding=emb,
                    file_type=file_type,
                    metadata_vars={"source_path": file_path},
                )
                self.db.add(chunk)
            self.db.commit()
            logger.info(f"Successfully ingested {len(chunks_text)} chunks.")
            return {"status": "success", "chunks_ingested": len(chunks_text)}
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            self.db.rollback()
            raise e

    def _fallback_extract(self, file_path: str, ext: str) -> str:
        if ext == ".pdf":
            return extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return extract_text_from_docx(file_path)
        elif ext == ".txt" or ext == ".md":
            return extract_text_from_txt(file_path)
        else:
            return extract_text_general(file_path)

    async def ingest_text(
        self,
        text: str,
        document_name: str,
        chunk_size: int = 1000,
        overlap: int = 200,
        metadata: Optional[dict] = None,
    ):
        logger.info(f"Ingesting raw text as '{document_name}'...")

        chunks_text = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        logger.info(f"Created {len(chunks_text)} chunks from raw text.")

        logger.info("Generating embeddings...")
        embeddings = await get_embeddings(chunks_text)

        logger.info("Storing in database...")
        try:
            for i, (txt, emb) in enumerate(zip(chunks_text, embeddings)):
                chunk = Chunk(
                    text=txt,
                    document_name=document_name,
                    chunk_index=i,
                    embedding=emb,
                    file_type="text",
                    metadata_vars=metadata or {},
                )
                self.db.add(chunk)
            self.db.commit()
            logger.info(f"Successfully ingested {len(chunks_text)} chunks from text.")
            return {"status": "success", "chunks_ingested": len(chunks_text)}
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            self.db.rollback()
            raise e
