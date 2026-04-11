import pytest
from rag.rag.chunker import chunk_text, chunk_elements


def test_chunk_text():
    text = "Line 1\n\nLine 2\n\nLine 3"
    chunks = chunk_text(text, chunk_size=10, overlap=0)
    # Recursively splits by \n\n, then \n
    assert len(chunks) >= 3


def test_chunk_elements_fallback():
    # Test fallback when passing simple strings instead of elements
    elements = ["This is element 1", "This is element 2"]
    chunks = chunk_elements(elements, max_characters=50, overlap=0)
    assert len(chunks) > 0
    assert "element 1" in chunks[0] or "element 1" in "".join(chunks)


def test_chunk_elements_unstructured():
    try:
        from unstructured.documents.elements import Title, NarrativeText
    except ImportError:
        pytest.skip("Unstructured not installed")

    elements = [
        Title("Document Title"),
        NarrativeText(
            "This is a paragraph under the title. It should be grouped together if possible."
        ),
    ]

    chunks = chunk_elements(elements, max_characters=1000)
    assert len(chunks) > 0
    # chunk_by_title usually groups text under titles
    assert "Document Title" in chunks[0]
