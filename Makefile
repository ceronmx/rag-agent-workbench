# .PHONY declares that these are not actual files
.PHONY: help setup start-api start-mcp inspector db-wipe db-upgrade test lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Install Python and Node dependencies"
	@echo "  make start-api   - Run the FastAPI RAG server"
	@echo "  make start-mcp   - Build and run the MCP Bridge"
	@echo "  make inspector   - Launch the MCP Inspector for the bridge"
	@echo "  make db-wipe     - Wipe the database and re-run migrations"
	@echo "  make db-upgrade  - Run standard Alembic migrations"
	@echo "  make test        - Run Python and Node test suites"
	@echo "  make lint        - Run linters (Pre-commit & Biome)"
	@echo "  make format      - Run code formatters (Pre-commit & Biome)"
	@echo "  make clean       - Clear temporary caches and artifacts"

setup:
	cd rag && uv sync
	cd mcp_bridge && npm install

start-api:
	cd rag && uv run uvicorn rag.main:app --reload

start-mcp:
	cd mcp_bridge && npm run build && npm run start

inspector:
	cd mcp_bridge && npm run build && npm run inspector

db-wipe:
	cd rag && uv run rag start --test-mode

db-upgrade:
	cd rag && uv run rag start

test:
	cd rag && uv run pytest
	cd mcp_bridge && npm run test

lint:
	cd rag && uv run pre-commit run --all-files
	cd mcp_bridge && npm run check

format:
	cd rag && uv run pre-commit run --all-files
	cd mcp_bridge && npm run format

clean:
	cd rag && uv run rag clean-cache
