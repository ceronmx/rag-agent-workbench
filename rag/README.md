# rag RAG Project

A modern, high-performance Retrieval-Augmented Generation (RAG) system using Python, PostgreSQL with `pgvector`, and Ollama for local LLM inference.

## 🚀 Key Features

-   **FastAPI Web Interface**: Modern, asynchronous REST API for document ingestion, querying, and system health monitoring.
-   **Service Layer Architecture**: Clean separation between API/CLI controllers and business logic for better maintainability.
-   **Asynchronous Core**: Fully non-blocking I/O using `FastAPI`, `AsyncOllamaClient`, and `asyncio` for improved concurrency and responsiveness.
-   **Local RAG Stack**: Uses Ollama for embeddings (`nomic-embed-text-v2-moe`) and LLM (`llama3.2`) locally.
-   **Performance Evaluation**: Integrated **RAGAS** framework to quantitatively measure system performance (Faithfulness, Relevancy, Precision).
-   **Hybrid Search**: Combines semantic **Vector Search** with traditional **Keyword Search (FTS)** using Reciprocal Rank Fusion (RRF) for better precision.
-   **Metadata Filtering**: Filter search results by file type or document name to reduce noise and improve accuracy.
-   **Robust JSON Interceptor**: Custom monkey-patched LLM client that automatically cleans raw responses, stripping markdown noise to ensure reliable evaluation parsing.
-   **Database Migrations**: Integrated **Alembic** for robust database schema management and automated migrations on startup.
-   **Structured Logging**: Centralized, configurable logging system replacing informal prints for better observability.
-   **Smart Retrieval**:
    -   **Query Optimization**: Automatically restructures user queries for semantic vector search.
    -   **LLM Rescoring**: Reranks vector search results using an LLM for higher precision answer context.
-   **Robustness**: Built-in retry logic for LLM requests and modern batching support for embeddings.

## 📋 Prerequisites

-   **Python**: 3.10 or higher.
-   **uv**: [Install uv](https://github.com/astral-sh/uv) for dependency management.
-   **Docker & Docker Compose**: For running the PostgreSQL database.
-   **Ollama**: [Install Ollama](https://ollama.ai/) and pull required models:
    ```bash
    ollama pull llama3.2
    ollama pull nomic-embed-text-v2-moe
    # Recommended for evaluation phase:
    ollama pull llama3.1:8b
    ```

## 🛠️ Getting Started

### 1. Set up Environment
```bash
cp .env.example .env
# Edit .env if needed (LOG_LEVEL, OLLAMA_BASE_URL, DB credentials, etc.)
```

### 2. Start the Database
```bash
docker compose up -d
```

### 3. Install Dependencies
```bash
uv sync
```

## 🏃 Usage

### 1. Start the API Server
Run the FastAPI application locally:
```bash
uv run uvicorn rag.main:app --reload
```
The API is now available at `http://127.0.0.1:8000`. 

**Key Endpoints:**
- `GET /health`: System health check.
- `POST /query/`: Synchronous RAG query.
- `POST /query/stream`: Real-time streaming RAG query (SSE).
- `POST /ingest/file`: Upload and index documents (Multipart).
- `POST /ingest/text`: Index raw text strings (JSON).
- `GET /documents/`: List all ingested documents.
- `DELETE /documents/{name}`: Remove a document and its embeddings.
- `POST /evaluate/`: Run RAGAS benchmark evaluation.

You can explore the interactive **Swagger docs** with full schema details and examples at `http://127.0.0.1:8000/docs`.

### 2. Start / Verify CLI System
Initialize the database and verify connectivity via CLI:
```bash
uv run rag start
```

### 3. Ingest Documents
Via CLI:
```bash
uv run rag ingest /path/to/document.pdf --document-name "MyDoc"
```

### 4. Query the System
Via CLI:
```bash
uv run rag query "What are the key findings in the document?"
```

**New:** Support for Hybrid search:
```bash
uv run rag query "What is pgvector?" --search-mode hybrid
```
Available modes: `vector` (default), `keyword`, `hybrid`.

**New:** Support for Metadata filters:
```bash
# Search only in PDF files
uv run rag query "What is pgvector?" --filter-type pdf

# Search within a specific document
uv run rag query "Annual results" --filter-doc "Q4_Report"
```

### 4. Evaluate Performance (RAGAS)
Measure how well your RAG pipeline is performing across different configurations:
```bash
# 1. (Optional) Edit your golden set benchmark
# File: data/eval/golden_set.json

# 2. Run comparative evaluation
uv run rag evaluate
```
This generates **Markdown** and **CSV** reports in `data/eval/reports/` comparing configurations: Baseline, Restructure Only, Rerank Only, Full Vector, Hybrid Baseline, and Hybrid Full.

**Pro Tip:** For higher evaluation accuracy, set `EVAL_MODEL=llama3.1:8b` (or larger) in your `.env`. The system uses a "Teacher-Judge" pattern where a larger model grades the smaller application model.

### 5. Utility: Clean Cache
Clear `__pycache__` and `.pytest_cache` directories:
```bash
uv run rag clean-cache
```

## 📂 Project Structure

```text
src/rag/
├── main.py           # FastAPI Application entry point
├── cli.py            # CLI entry point (rag command)
├── api/              # API Route controllers
├── services/         # Business logic & Service layer
├── rag/              # Core RAG pipeline logic
│   ├── pipeline.py   # Integrated workflow
│   ├── extractor.py  # PDF/Docx text extraction
│   ├── chunker.py    # Recursive text splitting
│   └── engine.py     # Rescoring & Prompt assembly
├── models/
│   ├── database.py   # SQLAlchemy, pgvector & FTS models
│   ├── management.py # DB schema management
│   └── ollama_client.py # Async Ollama integration
└── utils/
    ├── evaluation.py # RAGAS metric logic
    ├── reporting.py  # Markdown/CSV report generators
    ├── datasets.py   # Golden set management
    ├── llm_robustness.py # JSON cleanup
    ├── logger.py     # Logging setup
    └── migrations.py # Alembic runner
```

## 🧪 Testing

The project uses `pytest` and `pytest-asyncio` for comprehensive testing.

### 1. Run All Tests
```bash
uv run pytest
```

### 2. Pre-commit Hooks
The project uses `pre-commit` to ensure code quality (Black, Pytest) before every commit.
```bash
uv run pre-commit install
```

## 📜 License
[MIT](LICENSE)
