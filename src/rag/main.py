from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag.api.query import router as query_router
from rag.api.ingestion import router as ingestion_router
from rag.api.documents import router as documents_router
from rag.api.evaluation import router as evaluation_router
from rag.utils.logger import logger
import time

app = FastAPI(
    title="RAG API",
    description="FastAPI application for RAG Project",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Routes
app.include_router(query_router)
app.include_router(ingestion_router)
app.include_router(documents_router)
app.include_router(evaluation_router)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | Status: {response.status_code} | Time: {process_time:.4f}s"
    )
    return response

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to ensure the API is running."""
    return {"status": "ok", "message": "API is running"}
