import fitz  # PyMuPDF
from typing import List
from v2_one.utils.logger import logger


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


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Extracting from {path}...")
        extracted = extract_text_from_pdf(path)
        print(f"Extracted {len(extracted)} characters.")
        print("Preview:")
        print(extracted[:200])
