import httpx
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")


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


def restructure_query(user_query: str) -> str:
    """
    Use LLM to restructure the user query for better vector search.
    """
    prompt = f"""
    You are an expert at optimizing search queries for a vector database.
    Transform the following user question into a concise, descriptive search query that captures the core semantic meaning.
    Focus on key terms and concepts.
    
    User question: {user_query}
    
    Optimized search query:"""

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.0},
            },
        )
        response.raise_for_status()
        return response.json()["response"].strip()


def generate_answer(prompt: str, stream: bool = False):
    """
    Call Ollama generate for final answer.
    """
    with httpx.Client(timeout=120.0) as client:
        if stream:
            return client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": prompt},
            )
        else:
            response = client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json()["response"]


if __name__ == "__main__":
    test_q = "What are the main benefits of using pgvector in Postgres for RAG?"
    print(f"Original: {test_q}")
    print(f"Restructured: {restructure_query(test_q)}")
