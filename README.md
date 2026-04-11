# RAG & MCP Monorepo

A centralized workspace for the RAG (Retrieval-Augmented Generation) system and its MCP (Model Context Protocol) bridge.

## 📂 Structure

- **`rag/`**: Python-based RAG system using FastAPI, PostgreSQL (pgvector), and Ollama.
- **`mcp_bridge/`**: Node.js/TypeScript MCP server that exposes RAG tools to LLMs.

## 🛠️ Management (Makefile)

This project uses a root-level `Makefile` to simplify common tasks across both sub-projects.

| Command | Description |
| :--- | :--- |
| `make setup` | Install all Python and Node dependencies |
| `make start-api` | Run the FastAPI RAG server |
| `make start-mcp` | Build and run the MCP Bridge |
| `make inspector` | Launch the MCP Inspector for debugging |
| `make db-wipe` | Wipe the database and re-run migrations |
| `make test` | Run all test suites |
| `make lint` | Run all linters |
| `make format` | Run all formatters |
| `make clean` | Clear temporary caches and artifacts |

---

Run `make help` for a full list of commands.
