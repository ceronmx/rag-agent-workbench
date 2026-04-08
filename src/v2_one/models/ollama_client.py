import os
import ollama
from typing import List
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

client = ollama.Client(host=OLLAMA_BASE_URL)


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for a list of strings from Ollama using the official SDK.
    """
    if not texts:
        return []

    try:
        # The SDK uses the newer /api/embed endpoint when calling embed()
        response = client.embed(model=EMBEDDING_MODEL, input=texts)
        return response.embeddings
    except Exception as e:
        print(
            f"Warning: Batch embedding failed with {e}. Falling back to sequential requests."
        )

    # Fallback to sequential requests if batching fails
    embeddings = []
    for text in texts:
        if not text:
            continue

        # Simple retry loop for transient errors
        for attempt in range(3):
            try:
                # generate embeddings for a single prompt
                # Note: older Ollama versions might not have /api/embed,
                # but the SDK might try to use it. If it fails, we try a single prompt.
                response = client.embeddings(model=EMBEDDING_MODEL, prompt=text)
                embeddings.append(response.embedding)
                break
            except Exception as ex:
                if attempt < 2:
                    print(
                        f"Retrying embedding request (attempt {attempt + 1}) after error: {ex}"
                    )
                    continue
                print(f"Error for chunk: {text[:100]}...")
                raise ex

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

    response = client.generate(
        model=LLM_MODEL,
        prompt=prompt,
        stream=False,
        options={"temperature": 0.0},
    )
    return response.response.strip()


def generate_answer(prompt: str, stream: bool = False):
    """
    Call Ollama generate for final answer.
    """
    if stream:
        return client.generate(model=LLM_MODEL, prompt=prompt, stream=True)
    else:
        response = client.generate(model=LLM_MODEL, prompt=prompt, stream=False)
        return response.response


if __name__ == "__main__":
    test_q = "What are the main benefits of using pgvector in Postgres for RAG?"
    print(f"Original: {test_q}")
    print(f"Restructured: {restructure_query(test_q)}")
