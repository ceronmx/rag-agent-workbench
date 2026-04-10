from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    question: str = Field(..., description="The question to ask the RAG system")
    search_mode: str = Field("vector", description="Search mode: 'vector', 'keyword', or 'hybrid'")
    use_rescoring: bool = Field(True, description="Whether to use LLM rescoring")
    use_stream: bool = Field(False, description="Whether to stream the response (currently handled via separate streaming endpoint or logic)")
    top_k: int = Field(3, description="Number of context chunks to use")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters (e.g., {'file_type': 'pdf'})")

class ContextChunk(BaseModel):
    text: str
    document_name: str
    chunk_index: int
    score: Optional[float] = None
    file_type: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    search_query: str
    search_mode: str
    contexts: List[ContextChunk]
    is_stream: bool = False
