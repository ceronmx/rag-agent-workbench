from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "What is pgvector?",
                "search_mode": "hybrid",
                "use_rescoring": True,
                "use_stream": False,
                "top_k": 3,
                "filters": {"file_type": "pdf"},
            }
        }
    )
    question: str = Field(..., description="The question to ask the RAG system")
    search_mode: str = Field(
        "vector", description="Search mode: 'vector', 'keyword', or 'hybrid'"
    )
    use_rescoring: bool = Field(True, description="Whether to use LLM rescoring")
    use_stream: bool = Field(False, description="Whether to stream the response")
    top_k: int = Field(3, description="Number of context chunks to use")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Metadata filters (e.g., {'file_type': 'pdf'})"
    )


class ContextChunk(BaseModel):
    text: str = Field(...)
    document_name: str = Field(...)
    chunk_index: int = Field(...)
    score: Optional[float] = Field(None)
    file_type: Optional[str] = Field(None)


class QueryResponse(BaseModel):
    answer: str = Field(...)
    search_query: str = Field(...)
    search_mode: str = Field(...)
    contexts: List[ContextChunk]
    is_stream: bool = False


class TextIngestRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "This is some sample text to be indexed.",
                "document_name": "Manual_Entry_1",
                "chunk_size": 1000,
                "overlap": 200,
                "metadata": {"author": "admin"},
            }
        }
    )
    text: str = Field(..., description="Raw text to ingest")
    document_name: str = Field(..., description="Name for the ingested document")
    chunk_size: int = Field(1000, description="Size of each chunk")
    overlap: int = Field(200, description="Overlap between chunks")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DocumentInfo(BaseModel):
    document_name: str = Field(...)
    chunk_count: int = Field(...)
    file_type: str = Field(...)
    preview_url: Optional[str] = Field(None)


class EvaluationRequest(BaseModel):
    dataset_path: str = Field(
        "data/eval/golden_set.json", description="Path to the evaluation dataset"
    )


class EvaluationResponse(BaseModel):
    status: str = Field(...)
    md_report: str = Field(...)
    csv_report: str = Field(...)
    metrics: Dict[str, Any] = Field(...)
