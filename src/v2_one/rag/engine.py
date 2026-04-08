from typing import List, Dict, Any
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")


def rescore_results(query: str, results: List[Any]) -> List[Any]:
    """
    Rerank vector search results using an LLM.
    This is a simple implementation that asks the LLM to pick the most relevant chunks.
    """
    if not results:
        return []

    context = "\n".join([f"[{i}] {r.text}" for i, r in enumerate(results)])

    prompt = f"""
    You are an expert at evaluating the relevance of document segments to a search query.
    Given the following query and a list of numbered document segments, identify the indices (e.g., 0, 2) of the most relevant segments that directly help answer the query.
    Return ONLY the indices separated by commas, in order of relevance.
    
    Query: {query}
    
    Segments:
    {context}
    
    Relevant Indices:"""

    try:
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
            indices_str = response.json()["response"].strip()

            # Extract integers from response
            import re

            indices = [int(i) for i in re.findall(r"\d+", indices_str)]

            # Reorder and filter
            rescored = []
            seen = set()
            for idx in indices:
                if 0 <= idx < len(results) and idx not in seen:
                    rescored.append(results[idx])
                    seen.add(idx)

            # Add remaining results that weren't picked (optional, but keeps all data)
            for i, r in enumerate(results):
                if i not in seen:
                    rescored.append(r)

            return rescored
    except Exception as e:
        print(f"Rescoring failed: {e}. Returning original results.")
        return results
