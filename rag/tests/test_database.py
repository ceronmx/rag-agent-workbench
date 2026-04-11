import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rag.models.database import Base, Chunk, vector_search, SQLALCHEMY_DATABASE_URL

# Create a test engine. We'll use the same URL but ideally it should be a test DB.
# For this project, we'll connect and use transactions to roll back changes.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create the tables once for the module."""
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: Base.metadata.drop_all(bind=engine) if we want to clean up completely,
    # but normally we might just keep them. For now, let's keep it safe.
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a transactional scope around a series of operations."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_schema_creation(db_session):
    """Test that we can insert a Chunk and query it."""
    chunk = Chunk(
        text="Sample test text",
        document_name="test_doc.pdf",
        chunk_index=0,
        embedding=[0.1] * 768,  # Dummy embedding
    )
    db_session.add(chunk)
    db_session.commit()

    # Query it back
    queried_chunk = (
        db_session.query(Chunk).filter(Chunk.document_name == "test_doc.pdf").first()
    )
    assert queried_chunk is not None
    assert queried_chunk.text == "Sample test text"
    assert queried_chunk.chunk_index == 0
    assert len(queried_chunk.embedding) == 768


def test_vector_search(db_session):
    """Test cosine similarity search."""
    # Insert a few chunks with distinct embeddings
    emb1 = [1.0] + [0.0] * 767  # Unit vector on axis 0
    emb2 = [0.0, 1.0] + [0.0] * 766  # Unit vector on axis 1

    chunk1 = Chunk(
        text="Vector 1", document_name="vec_doc.pdf", chunk_index=0, embedding=emb1
    )
    chunk2 = Chunk(
        text="Vector 2", document_name="vec_doc.pdf", chunk_index=1, embedding=emb2
    )

    db_session.add(chunk1)
    db_session.add(chunk2)
    db_session.commit()

    # Search for something close to emb1
    query_emb = [0.9, 0.1] + [0.0] * 766
    results = vector_search(db_session, query_emb, limit=2)

    assert len(results) == 2
    # The first result should be chunk1 because query_emb is closer to emb1 than emb2
    # Result format from vector_search: (id, text, document_name, chunk_index, similarity)
    # The first result (closest) should be "Vector 1"
    assert results[0].text == "Vector 1"
    assert results[1].text == "Vector 2"

    # Similarity score checks
    assert results[0].similarity > results[1].similarity
