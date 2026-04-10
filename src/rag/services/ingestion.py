import os
from sqlalchemy.orm import Session
from rag.models.database import Chunk
from rag.models.ollama_client import get_embeddings
from rag.rag.extractor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
)
from rag.rag.chunker import chunk_text
from rag.utils.logger import logger


class IngestionService:
    def __init__(self, db: Session):
        self.db = db

    async def ingest_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        overlap: int = 200,
        document_name: str = None,
    ):
        doc_name = document_name or os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        logger.info(f"Ingesting {file_path} (Type: {ext}) as '{doc_name}'...")

        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".docx":
            text = extract_text_from_docx(file_path)
        else:
            text = extract_text_from_txt(file_path)

        chunks_text = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        logger.info(
            f"Extracted {len(text)} characters. Created {len(chunks_text)} chunks."
        )

        logger.info("Generating embeddings...")
        embeddings = await get_embeddings(chunks_text)

        logger.info("Storing in database...")
        file_type = ext.replace(".", "")

        try:
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
