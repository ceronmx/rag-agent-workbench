import asyncio
from typing import List, Dict, Any, Optional, Union, AsyncGenerator
from rag.models.database import SessionLocal, vector_search, keyword_search
from rag.models.ollama_client import get_embeddings, restructure_query, generate_answer
from rag.rag.engine import rescore_results, assemble_rag_prompt, reciprocal_rank_fusion
from rag.utils.logger import logger


async def run_rag_pipeline(
    question: str,
    use_restructuring: bool = True,
    use_rescoring: bool = True,
    search_mode: str = "vector",
    filters: Optional[Dict[str, Any]] = None,
    top_k: int = 3,
    stream: bool = False,
) -> Dict[str, Any]:
    """
    Execute the RAG pipeline with configurable steps.
    Returns a dictionary with the answer (or stream) and intermediate results.
    """
    # 1. Restructure (Optional)
    search_query = question
    if use_restructuring:
        logger.debug(f"Restructuring query: {question}")
        search_query = await restructure_query(question)

    # 2. Search
    logger.debug(
        f"Searching for: {search_query} (Mode: {search_mode}, Filters: {filters})"
    )
    db = SessionLocal()
    try:
        search_results = []

        if search_mode in ["vector", "hybrid"]:
            query_emb_list = await get_embeddings([search_query])
            query_emb = query_emb_list[0]
            vector_results = vector_search(db, query_emb, limit=10, filters=filters)
            if search_mode == "vector":
                search_results = vector_results

        if search_mode in ["keyword", "hybrid"]:
            keyword_results = keyword_search(
                db, search_query, limit=10, filters=filters
            )
            if search_mode == "keyword":
                search_results = keyword_results

        if search_mode == "hybrid":
            search_results = reciprocal_rank_fusion(vector_results, keyword_results)

        if not search_results:
            return {
                "answer": "No relevant context found.",
                "contexts": [],
                "search_query": search_query,
                "search_mode": search_mode,
            }

        # 3. Rescore (Optional)
        final_results = search_results
        if use_rescoring:
            logger.debug("Rescoring results...")
            final_results = await rescore_results(search_query, search_results)

        # 4. Assemble & Generate
        prompt = assemble_rag_prompt(question, final_results, top_k=top_k)

        # answer will be a string OR an AsyncGenerator
        answer = await generate_answer(prompt, stream=stream)

        # Format contexts (list of dicts with metadata)
        contexts = [
            {
                "text": r.text,
                "document_name": r.document_name,
                "chunk_index": r.chunk_index,
                "score": getattr(r, "similarity", None),
                "file_type": getattr(r, "file_type", None),
            }
            for r in final_results[:top_k]
        ]

        return {
            "answer": answer,
            "contexts": contexts,
            "search_query": search_query,
            "used_restructuring": use_restructuring,
            "used_rescoring": use_rescoring,
            "search_mode": search_mode,
            "is_stream": stream,
        }
    finally:
        db.close()
