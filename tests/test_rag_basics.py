import pytest
from v2_one.rag.chunker import chunk_text


def test_chunk_text_basic():
    text = "This is a sentence. This is another sentence. This is the third."
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    assert len(chunks) > 0
    assert all(len(c) <= 20 for c in chunks)
    # Check that it captures the text
    full_recon = " ".join(chunks)
    assert "sentence" in full_recon


def test_chunk_text_small():
    text = "Small text"
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) == 1
    assert chunks[0] == "Small text"


def test_chunk_text_empty():
    chunks = chunk_text("", chunk_size=100, overlap=10)
    assert len(chunks) == 0


def test_chunk_text_exact_size():
    text = "A" * 100
    chunks = chunk_text(text, chunk_size=100, overlap=0)
    assert len(chunks) == 1
    assert len(chunks[0]) == 100


def test_chunk_text_separators():
    text = "Paragraph 1\n\nParagraph 2\nParagraph 3. Word"
    chunks = chunk_text(text, chunk_size=15, overlap=0)
    # Should split at \n\n or \n if possible
    assert any("Paragraph 1" in c for c in chunks)
    assert any("Paragraph 2" in c for c in chunks)
