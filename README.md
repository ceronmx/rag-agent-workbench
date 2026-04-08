# v2-one RAG Project

A modern Retrieval-Augmented Generation (RAG) system using Python v3, PostgreSQL with `pgvector`, and Ollama for local LLM inference.

## 🚀 Features

- **Modern Python Structure**: Follows `src/` layout with modular packages.
- **Full RAG Pipeline**: Ingestion, Chunking, Embedding, Restructuration, Search, Rescoring, and Generation.
- **Local RAG Stack**: Uses Ollama for embeddings (`nomic-embed-text-v2-moe`) and LLM (`llama3.2`).
- **Query Optimization**: Automatically restructures user queries for better vector search results.
- **LLM Rescoring**: Reranks vector search results using an LLM for higher precision.
- **Vector Database**: PostgreSQL 17 with the `pgvector` extension running in Docker.
- **Dependency Management**: Powered by `uv` for fast and reliable builds.

## 📋 Prerequisites

- **Python**: 3.10 or higher.
- **uv**: [Install uv](https://github.com/astral-sh/uv) for dependency management.
- **Docker & Docker Compose**: For running the PostgreSQL database.
- **Ollama**: [Install Ollama](https://ollama.ai/) and pull required models:
  ```bash
  ollama pull llama3.2
  ollama pull nomic-embed-text-v2-moe
  ```

## 🛠️ Getting Started

### 1. Set up Environment
```bash
cp .env.example .env
# Edit .env if needed (OLLAMA_BASE_URL, DB credentials, etc.)
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

### 1. Ingest Documents
Process a PDF file, chunk it, and store embeddings in the database:
```bash
uv run v2-one ingest /path/to/document.pdf --document-name "MyDoc"
```
Optional flags: `--chunk-size 1000`, `--overlap 200`.

### 2. Query the System
Ask questions based on the ingested documents:
```bash
uv run v2-one query "What are the key findings in the document?"
```
The system will:
1. **Restructure** your query for search.
2. **Search** the vector database.
3. **Rescore** the top results using the LLM.
4. **Generate** a final answer based on the best context.

**Options:**
- `--no-rescore`: Skip the LLM reranking step for faster (but potentially less precise) results.
- `--top-k`: Number of context chunks to include in the final prompt (default: 3).

### 3. Development / Test Mode
Initialize or wipe the database schema:
```bash
uv run v2-one start --test-mode
```

## 📂 Project Structure

```text
v2_one/
├── src/
│   └── v2_one/
│       ├── main.py           # CLI entry point
│       ├── rag/
│       │   ├── extractor.py  # PDF text extraction (PyMuPDF)
│       │   ├── chunker.py    # Recursive text splitting
│       │   └── engine.py     # Rescoring & Prompt assembly
│       ├── models/
│       │   ├── database.py   # SQLAlchemy & pgvector search
│       │   ├── management.py # DB schema utilities
│       │   └── ollama_client.py # Ollama API integration
│       └── utils/
├── scripts/                  # Test & Utility scripts
├── docker-compose.yml        # PostgreSQL + pgvector
└── pyproject.toml
```

## 🧪 Testing

The project uses `pytest` for comprehensive testing of the RAG pipeline, including extraction, chunking, database search, and LLM logic.

### 1. Run All Tests
```bash
PYTHONPATH=src uv run pytest
```

### 2. Test Suites
- **Chunking**: `tests/test_rag_basics.py` (verified recursive splitting and overlap)
- **Database**: `tests/test_database.py` (verifies schema and `pgvector` similarity search)
- **Ollama Client**: `tests/test_ollama_client.py` (mocked API interaction)
- **RAG Engine**: `tests/test_rag_engine.py` (rescoring and prompt logic)

### 3. Pre-commit Hooks
The project uses `pre-commit` to ensure code quality and that all tests pass before every commit.
- **Install Hooks**: `uv run pre-commit install`
- **Run Manually**: `uv run pre-commit run --all-files`

## 📜 License
[MIT](LICENSE)
