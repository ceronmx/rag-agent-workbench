from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from rag.api.schemas import QueryRequest, QueryResponse, ContextChunk
from rag.api.dependencies import get_query_service
from rag.services.query import QueryService
from typing import List, AsyncGenerator
import json

router = APIRouter(prefix="/query", tags=["Query"])

async def stream_answer(result_generator: AsyncGenerator) -> AsyncGenerator[str, None]:
    """Wraps the generator from QueryService to provide SSE-compatible output."""
    try:
        async for chunk in result_generator:
            content = ""
            if "message" in chunk:
                content = chunk["message"]["content"]
            elif "response" in chunk:
                content = chunk["response"]
            
            if content:
                # SSE format: data: <message>\n\n
                yield f"data: {json.dumps({'content': content})}\n\n"
        
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@router.post("/", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    query_service: QueryService = Depends(get_query_service)
):
    """
    Execute a RAG query using the specified search mode and parameters.
    Returns a unified answer along with the search query and context chunks.
    """
    try:
        # Note: current QueryService returns a dict from pipeline, we map it to response schema
        result = await query_service.query(
            question=request.question,
            search_mode=request.search_mode,
            use_rescoring=request.use_rescoring,
            use_stream=request.use_stream,
            top_k=request.top_k,
            filters=request.filters
        )
        
        # Handle non-streaming response
        if result.get("is_stream"):
             raise HTTPException(status_code=400, detail="Streaming is not supported via this endpoint. Use the streaming query endpoint.")

        # Map contexts from internal pipeline format to schema
        contexts = [
            ContextChunk(
                text=c["text"],
                document_name=c["document_name"],
                chunk_index=c["chunk_index"],
                score=c.get("score"),
                file_type=c.get("file_type")
            ) for c in result.get("contexts", [])
        ]

        return QueryResponse(
            answer=result["answer"],
            search_query=result["search_query"],
            search_mode=result["search_mode"],
            contexts=contexts,
            is_stream=False
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def run_query_stream(
    request: QueryRequest,
    query_service: QueryService = Depends(get_query_service)
):
    """
    Execute a RAG query and stream the answer in real-time using SSE.
    """
    try:
        result = await query_service.query(
            question=request.question,
            search_mode=request.search_mode,
            use_rescoring=request.use_rescoring,
            use_stream=True,  # Force streaming
            top_k=request.top_k,
            filters=request.filters
        )

        if not result.get("is_stream"):
             # If for some reason it didn't return a stream
             return QueryResponse(
                answer=result["answer"],
                search_query=result["search_query"],
                search_mode=result["search_mode"],
                contexts=[], 
                is_stream=False
             )

        return StreamingResponse(
            stream_answer(result["answer"]),
            media_type="text/event-stream"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
