# .PHONY declares that these are not actual files
.PHONY: help setup start-api start-mcp start-client inspector db-wipe db-upgrade test lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Install Python and Node dependencies"
	@echo "  make start-api   - Run the FastAPI RAG server"
	@echo "  make start-mcp   - Build and run the MCP Bridge"
	@echo "  make start-client - Run the Vite client project"
	@echo "  make inspector   - Launch the MCP Inspector for the bridge"
	@echo "  make db-wipe     - Wipe the database and re-run migrations"
	@echo "  make db-upgrade  - Run standard Alembic migrations"
	@echo "  make test        - Run Python and Node test suites"
	@echo "  make lint        - Run linters (Pre-commit & Biome)"
	@echo "  make format      - Run code formatters (Pre-commit & Biome)"
	@echo "  make clean       - Clear temporary caches and artifacts"

setup:
	cd rag && unset VIRTUAL_ENV && uv sync
	cd mcp_bridge && pnpm install
	cd client && pnpm install

start-api:
	cd rag && unset VIRTUAL_ENV && uv run uvicorn rag.main:app --reload

start-mcp:
	cd mcp_bridge && pnpm run build && pnpm run start

start-client:
	cd client && pnpm run dev

inspector:
	cd mcp_bridge && pnpm run build && pnpm run inspector

db-wipe:
	cd rag && unset VIRTUAL_ENV && uv run rag start --test-mode

db-upgrade:
	cd rag && unset VIRTUAL_ENV && uv run rag start

test:
	cd rag && unset VIRTUAL_ENV && uv run pytest
	cd mcp_bridge && pnpm run test
	cd client && pnpm run test

lint:
	cd rag && unset VIRTUAL_ENV && uv run pre-commit run --all-files
	cd mcp_bridge && pnpm run check
	cd client && pnpm run lint

format:
	cd rag && unset VIRTUAL_ENV && uv run pre-commit run --all-files
	cd mcp_bridge && pnpm run format
	cd client && pnpm run format

clean:
	cd rag && unset VIRTUAL_ENV && uv run rag clean-cache
