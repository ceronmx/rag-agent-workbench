import pytest
import os
from rag.rag.extractor import (
    extract_text_from_txt,
    extract_text_from_docx,
    extract_text_from_pdf,
    partition_document,
    extract_text_general,
)


def test_extract_text_from_txt(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello World")

    text = extract_text_from_txt(str(p))
    assert "Hello World" in text


def test_partition_document_txt(tmp_path):
    # Only if unstructured is installed and working
    try:
        from unstructured.partition.auto import partition
    except ImportError:
        pytest.skip("Unstructured not installed")

    p = tmp_path / "test.txt"
    p.write_text("This is a test document.")

    elements = partition_document(str(p))
    assert len(elements) > 0
    assert "This is a test document" in str(elements[0])


def test_extract_text_general(tmp_path):
    # Test with a simple text file but via the general extractor
    p = tmp_path / "general.md"
    p.write_text("# Markdown Title\nContent")

    text = extract_text_general(str(p))
    assert "Markdown Title" in text
