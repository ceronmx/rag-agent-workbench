from typing import List, Any
from rag.utils.logger import logger

# Try to import unstructured chunking
try:
    from unstructured.chunking.title import chunk_by_title

    HAS_UNSTRUCTURED_CHUNKING = True
except ImportError:
    HAS_UNSTRUCTURED_CHUNKING = False


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks of a given size.
    Uses a recursive strategy on separators: \n\n, \n, . , ' '
    """
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Try to find a good separator back from the end
        chunk = text[start:end]
        last_sep = -1
        for sep in ["\n\n", "\n", ". ", " "]:
            last_sep = chunk.rfind(sep)
            if last_sep != -1:
                break

        if last_sep == -1 or last_sep <= overlap:
            last_sep = len(chunk)

        chunks.append(text[start : start + last_sep].strip())
        start += last_sep - overlap

    return [c for c in chunks if c]


def chunk_elements(
    elements: List[Any],
    max_characters: int = 1000,
    new_after_n_chars: int = 1500,
    overlap: int = 200,
) -> List[str]:
    """
    Groups Unstructured elements into logical chunks (e.g. by title).
    Falls back to simple text chunking if unstructured is unavailable.
    """
    if not HAS_UNSTRUCTURED_CHUNKING:
        logger.warning(
            "Unstructured chunking not available. Joining elements and using character-based chunking."
        )
        text = "\n\n".join([str(el) for el in elements])
        return chunk_text(text, chunk_size=max_characters, overlap=overlap)

    try:
        # chunk_by_title is smart about keeping tables and lists together
        chunks = chunk_by_title(
            elements,
            max_characters=max_characters,
            new_after_n_chars=new_after_n_chars,
            overlap=overlap,
        )
        # Convert element objects to strings
        return [str(chunk) for chunk in chunks]
    except Exception as e:
        logger.error(
            f"Unstructured chunking failed: {e}. Falling back to simple chunking."
        )
        text = "\n\n".join([str(el) for el in elements])
        return chunk_text(text, chunk_size=max_characters, overlap=overlap)


if __name__ == "__main__":
    test_text = "This is a test. " * 100
    res = chunk_text(test_text, chunk_size=50, overlap=10)
    for i, c in enumerate(res):
        print(f"Chunk {i}: {c}")
