import asyncio
from typing import List, Dict, Any, Optional
from rag.models.database import SessionLocal, vector_search
from rag.models.ollama_client import get_embeddings, restructure_query, generate_answer
from rag.rag.engine import rescore_results, assemble_rag_prompt
from rag.utils.logger import logger


async def run_rag_pipeline(
    question: str,
    use_restructuring: bool = True,
    use_rescoring: bool = True,
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    Execute the RAG pipeline with configurable steps.
    Returns a dictionary with the answer and intermediate results (for evaluation).
    """
    # 1. Restructure (Optional)
    search_query = question
    if use_restructuring:
        logger.debug(f"Restructuring query: {question}")
        search_query = await restructure_query(question)

    # 2. Vector Search
    logger.debug(f"Searching for: {search_query}")
    db = SessionLocal()
    try:
        query_emb_list = await get_embeddings([search_query])
        query_emb = query_emb_list[0]

        # Get top 10 for potential rescoring
        search_results = vector_search(db, query_emb, limit=10)

        if not search_results:
            return {
                "answer": "No relevant context found.",
                "contexts": [],
                "search_query": search_query,
            }

        # 3. Rescore (Optional)
        final_results = search_results
        if use_rescoring:
            logger.debug("Rescoring results...")
            final_results = await rescore_results(search_query, search_results)

        # 4. Assemble & Generate
        prompt = assemble_rag_prompt(question, final_results, top_k=top_k)
        answer = await generate_answer(prompt)

        # Format contexts for RAGAS (list of strings)
        contexts = [r.text for r in final_results[:top_k]]

        return {
            "answer": answer,
            "contexts": contexts,
            "search_query": search_query,
            "used_restructuring": use_restructuring,
            "used_rescoring": use_rescoring,
        }
    finally:
        db.close()
