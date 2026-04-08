import httpx
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for a list of strings from Ollama.
    """
    embeddings = []
    with httpx.Client(timeout=60.0) as client:
        for text in texts:
            response = client.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={"model": EMBEDDING_MODEL, "prompt": text},
            )
            response.raise_for_status()
            embeddings.append(response.json()["embedding"])
    return embeddings


if __name__ == "__main__":
    test_texts = ["Hello world", "This is a test of Ollama embeddings"]
    try:
        results = get_embeddings(test_texts)
        print(f"Got {len(results)} embeddings.")
        print(f"Dimension of first embedding: {len(results[0])}")
    except Exception as e:
        print(f"Error calling Ollama: {e}")
