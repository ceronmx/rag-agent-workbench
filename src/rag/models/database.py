import os
from typing import List, Dict, Any, Optional
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Index,
    func,
    DateTime,
    text as sa_text,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import UserDefinedType
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rag")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Vector(UserDefinedType):
    def __init__(self, dim):
        self.dim = dim

    def get_col_spec(self, **kw):
        return f"vector({self.dim})"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            return f"[{','.join(map(str, value))}]"

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            # PG returns it as a string like "[1,2,3]"
            return [float(x) for x in value.strip("[]").split(",")]

        return process


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    document_name = Column(String, index=True)
    chunk_index = Column(Integer)
    embedding = Column(Vector(768))  # Dimension for nomic-embed-text-v2-moe

    # Metadata fields
    file_type = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata_vars = Column(JSONB, default={})

    __table_args__ = (
        Index(
            "idx_chunks_fts",
            sa_text("to_tsvector('english', text)"),
            postgresql_using="gin",
        ),
    )


def _build_filter_clause(filters: Optional[Dict[str, Any]]) -> (str, Dict[str, Any]):
    """
    Build a dynamic WHERE clause based on metadata filters.
    """
    if not filters:
        return "", {}

    clauses = []
    params = {}

    if "file_type" in filters:
        clauses.append("file_type = :file_type")
        params["file_type"] = filters["file_type"]

    if "document_name" in filters:
        clauses.append("document_name = :document_name")
        params["document_name"] = filters["document_name"]

    if not clauses:
        return "", {}

    return " WHERE " + " AND ".join(clauses), params


def vector_search(
    db, query_embedding, limit=5, filters: Optional[Dict[str, Any]] = None
):
    """
    Perform a cosine similarity search on the chunks table with optional metadata filters.
    """
    emb_str = f"[{','.join(map(str, query_embedding))}]"
    filter_clause, params = _build_filter_clause(filters)
    params["limit"] = limit

    query = sa_text(
        f"""
        SELECT id, text, document_name, chunk_index, file_type, 1 - (embedding <=> '{emb_str}') as similarity
        FROM chunks
        {filter_clause}
        ORDER BY embedding <=> '{emb_str}'
        LIMIT :limit
    """
    )

    result = db.execute(query, params)
    return result.fetchall()


def keyword_search(db, query_text, limit=5, filters: Optional[Dict[str, Any]] = None):
    """
    Perform a full-text search on the chunks table using websearch_to_tsquery with optional metadata filters.
    """
    filter_clause, params = _build_filter_clause(filters)
    params["query"] = query_text
    params["limit"] = limit

    # Update filter clause if it exists to use AND since we already have a WHERE
    # But wait, keyword search currently doesn't have a WHERE if no filters.
    # Let's adjust logic.

    sql = """
        SELECT id, text, document_name, chunk_index, file_type, ts_rank(to_tsvector('english', text), websearch_to_tsquery('english', :query)) as similarity
        FROM chunks
        WHERE to_tsvector('english', text) @@ websearch_to_tsquery('english', :query)
    """

    if filter_clause:
        # Append to existing WHERE
        sql += filter_clause.replace(" WHERE ", " AND ")

    sql += """
        ORDER BY similarity DESC
        LIMIT :limit
    """

    query = sa_text(sql)
    result = db.execute(query, params)
    return result.fetchall()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
