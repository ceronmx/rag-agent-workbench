# rag RAG Project

A modern, high-performance Retrieval-Augmented Generation (RAG) system using Python, PostgreSQL with `pgvector`, and Ollama for local LLM inference.

## 🚀 Key Features

-   **Asynchronous Core**: Fully non-blocking I/O using `AsyncOllamaClient` and `asyncio` for improved concurrency and responsiveness.
-   **Local RAG Stack**: Uses Ollama for embeddings (`nomic-embed-text-v2-moe`) and LLM (`llama3.2`) locally.
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

### 1. Start / Verify System
Initialize the database and verify connectivity:
```bash
uv run rag start
```

### 2. Ingest Documents
Process a PDF file, chunk it, and store embeddings in the database:
```bash
uv run rag ingest /path/to/document.pdf --document-name "MyDoc"
```
Optional flags: `--chunk-size 1000`, `--overlap 200`.

### 3. Query the System
Ask questions based on the ingested documents:
```bash
uv run rag query "What are the key findings in the document?"
```

### 4. Utility: Clean Cache
Clear `__pycache__` and `.pytest_cache` directories:
```bash
uv run rag clean-cache
```

## 📂 Project Structure

```text
src/rag/
├── main.py           # CLI entry point (Async)
├── rag/
│   ├── extractor.py  # PDF text extraction
│   ├── chunker.py    # Recursive text splitting
│   └── engine.py     # Rescoring & Prompt assembly
├── models/
│   ├── database.py   # SQLAlchemy & pgvector
│   ├── management.py # DB schema utilities
│   └── ollama_client.py # Async Ollama SDK integration
└── utils/
    ├── logger.py     # Centralized logging configuration
    └── migrations.py # Alembic programmatic runner
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
