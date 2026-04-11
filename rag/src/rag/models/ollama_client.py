import os
import ollama
from typing import List, Union, AsyncGenerator
from dotenv import load_dotenv
from rag.utils.logger import logger

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

client = ollama.AsyncClient(host=OLLAMA_BASE_URL)


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for a list of strings from Ollama using the official SDK (Async).
    """
    if not texts:
        return []

    try:
        # The SDK uses the newer /api/embed endpoint when calling embed()
        response = await client.embed(model=EMBEDDING_MODEL, input=texts)
        return response.embeddings
    except Exception as e:
        logger.warning(
            f"Batch embedding failed with {e}. Falling back to sequential requests."
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
                response = await client.embeddings(model=EMBEDDING_MODEL, prompt=text)
                embeddings.append(response.embedding)
                break
            except Exception as ex:
                if attempt < 2:
                    logger.info(
                        f"Retrying embedding request (attempt {attempt + 1}) after error: {ex}"
                    )
                    continue
                logger.error(f"Error for chunk: {text[:100]}...")
                raise ex

    return embeddings


async def restructure_query(user_query: str) -> str:
    """
    Use LLM to restructure the user query for better vector search (Async).
    """
    system_prompt = (
        "You are an expert at optimizing search queries for a vector database. "
        "Your task is to transform user questions into a concise, descriptive search query. "
        "IMPORTANT: You MUST return ONLY the optimized search query string. "
        "Do NOT include any explanations, reasoning, prefix, or suffix. "
        "Example 1:\nUser: What is the capital of France?\nQuery: capital of France\n"
        "Example 2:\nUser: How does pgvector handle indexing?\nQuery: pgvector indexing mechanisms\n"
        "Example 3:\nUser: Tell me about FastAPI performance compared to Flask\nQuery: FastAPI vs Flask performance"
    )

    try:
        response = await client.chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User: {user_query}"},
            ],
            options={"temperature": 0.0},
        )
        content = response["message"]["content"].strip()
        # Clean up any common prefixes the LLM might still add
        if "Query:" in content:
            content = content.split("Query:")[-1].strip()

        # Take only the first line and strip common artifacts
        content = content.split("\n")[0].strip("\"' ")

        # If the LLM still prefix with something like "Optimized query:"
        for prefix in ["optimized search query:", "optimized query:", "search query:"]:
            if content.lower().startswith(prefix):
                content = content[len(prefix) :].strip()

        return content
    except Exception as e:
        logger.error(f"Error restructuring query: {e}. Returning original.")
        return user_query


async def generate_answer(
    prompt: str, stream: bool = False
) -> Union[str, AsyncGenerator]:
    """
    Call Ollama generate for final answer (Async).
    Returns a string if stream=False, or an AsyncGenerator if stream=True.
    """
    if stream:
        return await client.generate(model=LLM_MODEL, prompt=prompt, stream=True)
    else:
        response = await client.generate(model=LLM_MODEL, prompt=prompt, stream=False)
        return response.response


if __name__ == "__main__":
    import asyncio

    async def main():
        test_q = "What are the main benefits of using pgvector in Postgres for RAG?"
        print(f"Original: {test_q}")
        res = await restructure_query(test_q)
        print(f"Restructured: {res}")

    asyncio.run(main())
