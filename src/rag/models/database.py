import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import UserDefinedType
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


from sqlalchemy import text


def vector_search(db, query_embedding, limit=5):
    """
    Perform a cosine similarity search on the chunks table.
    """
    # Using <=> for cosine distance in pgvector
    # Order by distance ASC (most similar first)
    emb_str = f"[{','.join(map(str, query_embedding))}]"

    query = text(
        f"""
        SELECT id, text, document_name, chunk_index, 1 - (embedding <=> '{emb_str}') as similarity
        FROM chunks
        ORDER BY embedding <=> '{emb_str}'
        LIMIT :limit
    """
    )

    result = db.execute(query, {"limit": limit})
    return result.fetchall()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
