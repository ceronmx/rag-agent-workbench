import os
from typing import List, Any
from rag.utils.logger import logger

# Try to import unstructured
try:
    from unstructured.partition.auto import partition
    from unstructured.staging.base import elements_to_json

    HAS_UNSTRUCTURED = True
except ImportError:
    HAS_UNSTRUCTURED = False
    logger.warning("Unstructured.io not found. Falling back to simple extractors.")

import fitz  # PyMuPDF
import docx


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a given PDF file.
    Uses Unstructured if available, else falls back to PyMuPDF.
    """
    if HAS_UNSTRUCTURED:
        try:
            elements = partition(filename=pdf_path)
            return "\n\n".join([str(el) for el in elements])
        except Exception as e:
            logger.warning(
                f"Unstructured PDF extraction failed: {e}. Falling back to PyMuPDF."
            )

    # Fallback to PyMuPDF
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF with PyMuPDF: {e}")
        raise e


def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts all text from a given Word (.docx) file.
    Uses Unstructured if available, else falls back to python-docx.
    """
    if HAS_UNSTRUCTURED:
        try:
            elements = partition(filename=docx_path)
            return "\n\n".join([str(el) for el in elements])
        except Exception as e:
            logger.warning(
                f"Unstructured DOCX extraction failed: {e}. Falling back to python-docx."
            )

    # Fallback to python-docx
    try:
        doc = docx.Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        logger.error(f"Error extracting Word doc: {e}")
        raise e


def extract_text_from_txt(txt_path: str) -> str:
    """
    Extracts all text from a given text or markdown file.
    """
    if HAS_UNSTRUCTURED:
        try:
            elements = partition(filename=txt_path)
            return "\n\n".join([str(el) for el in elements])
        except Exception as e:
            logger.warning(
                f"Unstructured TXT extraction failed: {e}. Falling back to standard read."
            )

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error extracting text file: {e}")
        raise e


def extract_text_general(file_path: str) -> str:
    """
    General purpose text extraction using Unstructured.
    """
    if HAS_UNSTRUCTURED:
        try:
            elements = partition(filename=file_path)
            return "\n\n".join([str(el) for el in elements])
        except Exception as e:
            logger.error(f"Unstructured extraction failed for {file_path}: {e}")
            raise e
    else:
        # Very basic fallback for unknown formats
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Fallback extraction failed for {file_path}: {e}")
            raise e


def partition_document(file_path: str) -> List[Any]:
    """
    Returns Unstructured elements for layout-aware processing.
    """
    if not HAS_UNSTRUCTURED:
        raise ImportError("Unstructured.io is required for partition_document.")

    return partition(filename=file_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
        ext = os.path.splitext(path)[1].lower()
        print(
            f"Extracting from {path} (Type: {ext}) using {'Unstructured' if HAS_UNSTRUCTURED else 'Standard'}..."
        )

        if ext == ".pdf":
            extracted = extract_text_from_pdf(path)
        elif ext == ".docx":
            extracted = extract_text_from_docx(path)
        else:
            extracted = extract_text_from_txt(path)

        print(f"Extracted {len(extracted)} characters.")
        print("Preview:")
        print(extracted[:500])
