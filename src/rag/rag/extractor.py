import fitz  # PyMuPDF
import docx
from typing import List
from rag.utils.logger import logger


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a given PDF file.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}")
        raise e


def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts all text from a given Word (.docx) file.
    """
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
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error extracting text file: {e}")
        raise e


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) > 1:
        path = sys.argv[1]
        ext = os.path.splitext(path)[1].lower()
        print(f"Extracting from {path} (Type: {ext})...")

        if ext == ".pdf":
            extracted = extract_text_from_pdf(path)
        elif ext == ".docx":
            extracted = extract_text_from_docx(path)
        else:
            extracted = extract_text_from_txt(path)

        print(f"Extracted {len(extracted)} characters.")
        print("Preview:")
        print(extracted[:200])
