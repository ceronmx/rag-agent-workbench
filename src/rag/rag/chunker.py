from typing import List


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


if __name__ == "__main__":
    test_text = "This is a test. " * 100
    res = chunk_text(test_text, chunk_size=50, overlap=10)
    for i, c in enumerate(res):
        print(f"Chunk {i}: {c}")
