# v2-one RAG Project

A modern Retrieval-Augmented Generation (RAG) system using Python v3, PostgreSQL with `pgvector`, and Ollama for local LLM inference.

## 🚀 Features

- **Modern Python Structure**: Follows `src/` layout with modular packages.
- **Local RAG Stack**: Uses Ollama for embeddings (`nomic-embed-text-v2-moe`) and LLM (`llama3.2`).
- **Vector Database**: PostgreSQL 17 with the `pgvector` extension running in Docker.
- **Dependency Management**: Powered by `uv` for fast and reliable builds.
- **Test Mode**: Built-in support to wipe and recreate the database schema for clean testing.

## 📋 Prerequisites

- **Python**: 3.10 or higher.
- **uv**: [Install uv](https://github.com/astral-sh/uv) for dependency management.
- **Docker & Docker Compose**: For running the PostgreSQL database.
- **Ollama**: [Install Ollama](https://ollama.ai/) for local model execution.

## 🛠️ Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd v2_one
```

### 2. Set up environment variables
Copy the example environment file and adjust as needed:
```bash
cp .env.example .env
```

### 3. Start the Database
Run the PostgreSQL container with the `pgvector` extension:
```bash
docker compose up -d
```
The database will automatically initialize the `vector` extension on first start.

### 4. Install Dependencies
Sync the virtual environment using `uv`:
```bash
uv sync
```

## 🏃 Usage

### Running the Application
Execute the main entry point:
```bash
uv run v2-one
```

### Development/Test Mode
To wipe the database and recreate the schema (useful during development):
```bash
uv run v2-one --test-mode
```

### Manual Database Wipe
You can also run the management utility directly:
```bash
PYTHONPATH=src uv run python src/v2_one/models/management.py
```

## 📂 Project Structure

```text
v2_one/
├── src/
│   └── v2_one/
│       ├── main.py        # Entry point & CLI
│       ├── rag/           # RAG logic (indexing, retrieval)
│       ├── models/        # Database models & Ollama integration
│       │   ├── database.py    # SQLAlchemy connection
│       │   └── management.py  # DB utility functions
│       └── utils/         # Helper functions
├── tests/                 # Test suite
├── scripts/               # SQL & Shell utility scripts
├── docker-compose.yml     # Infrastructure (Postgres + pgvector)
├── pyproject.toml         # Package & Dependency config
└── README.md
```

## 🧪 Testing
Verify the database connection:
```bash
PYTHONPATH=src uv run python scripts/test_db_connection.py
```

## 📜 License
[MIT](LICENSE)
