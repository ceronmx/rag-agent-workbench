# MCP Bridge for RAG

This directory contains a **Model Context Protocol (MCP)** server that acts as a bridge between the [local RAG system](../rag/) and any MCP-compatible client (like Cursor, Claude Desktop, or Gemini CLI).

It allows LLMs to query your local knowledge base using a dedicated tool.

## Features

- **rag_query Tool**: Allows the LLM to search and retrieve answers from ingested documents using vector, keyword, or hybrid search modes.
- **Simplified Output**: Returns clean answers with a list of source documents used for citations.
- **Built with MCP SDK**: Uses the official Model Context Protocol TypeScript SDK.

## Setup

### Prerequisites

- [pnpm](https://pnpm.io/) (or npm/yarn)
- Node.js (v18+)
- The [RAG API](../rag/) must be running (default: http://127.0.0.1:8000)

### Installation

```bash
cd mcp_bridge
pnpm install
pnpm build
```

## Configuration

The bridge can be configured using environment variables:

- `RAG_API_BASE_URL`: The base URL of your running RAG API. Default is `http://127.0.0.1:8000`.

## Usage

### As an MCP Tool

Once connected to an MCP client, the LLM will have access to the `rag_query` tool:

- **Arguments**:
  - `question` (string, required): The query to ask the knowledge base.
  - `search_mode` (enum, optional): `vector`, `keyword`, or `hybrid`. Default is `vector`.
  - `top_k` (number, optional): Number of context chunks to retrieve. Default is 3.

### Development

Run the server in development mode:

```bash
pnpm dev
```

Run tests:

```bash
pnpm test
```

## Project Structure

- `src/index.ts`: Main entry point and tool definitions.
- `src/index.test.ts`: Unit tests for the MCP handlers.
- `biome.json`: Linting and formatting configuration.
