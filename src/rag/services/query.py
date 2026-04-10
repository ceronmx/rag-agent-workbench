from rag.rag.pipeline import run_rag_pipeline
from rag.utils.logger import logger
from typing import Dict, Any, Optional


class QueryService:
    async def query(
        self,
        question: str,
        search_mode: str = "vector",
        use_rescoring: bool = True,
        use_stream: bool = True,
        top_k: int = 3,
        filters: Optional[Dict[str, Any]] = None,
    ):
        logger.info(f"--- USER QUESTION ---\n{question}\n")

        try:
            result = await run_rag_pipeline(
                question,
                use_restructuring=True,
                use_rescoring=use_rescoring,
                search_mode=search_mode,
                filters=filters,
                top_k=top_k,
                stream=use_stream,
            )
            return result
        except Exception as e:
            logger.error(f"Error during query: {e}")
            raise e
