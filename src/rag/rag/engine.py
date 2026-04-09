from typing import List, Dict, Any
import os
import re
from rag.models.ollama_client import client, LLM_MODEL
from rag.utils.logger import logger


async def rescore_results(query: str, results: List[Any]) -> List[Any]:
    """
    Rerank vector search results using an LLM (Async).
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
        response = await client.generate(
            model=LLM_MODEL,
            prompt=prompt,
            stream=False,
            options={"temperature": 0.0},
        )
        indices_str = response.response.strip()

        # Extract integers from response
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
        logger.error(f"Rescoring failed: {e}. Returning original results.")
        return results


def assemble_rag_prompt(query: str, rescored_results: List[Any], top_k: int = 3) -> str:
    """
    Build a final RAG prompt for the LLM.
    """
    # Use top K results only
    top_results = rescored_results[:top_k]

    context = "\n".join(
        [
            f"Source: {r.document_name} (Chunk {r.chunk_index})\n{r.text}"
            for r in top_results
        ]
    )

    prompt = f"""
    You are a helpful and knowledgeable assistant. Use the provided context to answer the user question accurately.
    If the context does not contain enough information to answer, say so.
    
    ---
    CONTEXT:
    {context}
    ---
    
    USER QUESTION: {query}
    
    ANSWER:"""

    return prompt


def reciprocal_rank_fusion(
    vector_results: List[Any], keyword_results: List[Any], k: int = 60
) -> List[Any]:
    """
    Combine two lists of results using Reciprocal Rank Fusion.
    """
    scores = {}

    # Helper to update scores
    def update_scores(results):
        for rank, result in enumerate(results, start=1):
            # We use ID as unique identifier
            doc_id = result.id
            if doc_id not in scores:
                scores[doc_id] = {"score": 0.0, "data": result}
            scores[doc_id]["score"] += 1.0 / (k + rank)

    update_scores(vector_results)
    update_scores(keyword_results)

    # Sort by score descending
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x]["score"], reverse=True)
    return [scores[doc_id]["data"] for doc_id in sorted_ids]
