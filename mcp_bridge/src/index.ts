import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import { z } from 'zod';

// Configuration for the local RAG API
const RAG_API_BASE_URL = process.env.RAG_API_BASE_URL || 'http://127.0.0.1:8000';

export const server = new McpServer({
  name: 'rag-bridge',
  version: '1.0.0',
});

/**
 * Handler for the rag_query tool.
 */
export async function ragQueryHandler({
  question,
  search_mode,
  top_k,
}: {
  question: string;
  search_mode?: 'vector' | 'keyword' | 'hybrid';
  top_k?: number;
}) {
  try {
    const response = await axios.post(`${RAG_API_BASE_URL}/query`, {
      question,
      search_mode: search_mode || 'vector',
      top_k: top_k || 3,
      use_stream: false,
    });

    const data = response.data;

    // Format the response for the MCP client
    let resultText = `${data.answer}\n\n`;
    resultText += 'Sources:\n';

    if (Array.isArray(data.contexts)) {
      // Use a Set to keep track of unique document names for cleaner citations
      const uniqueDocs = new Set<string>();
      for (const context of data.contexts) {
        uniqueDocs.add(context.document_name);
      }

      for (const docName of uniqueDocs) {
        resultText += `- ${docName}\n`;
      }
    }

    return {
      content: [{ type: 'text' as const, text: resultText }],
    };
  } catch (error) {
    let errorMessage = 'Unknown error';
    if (axios.isAxiosError(error)) {
      errorMessage = error.response?.data?.detail || error.message;
    } else if (error instanceof Error) {
      errorMessage = error.message;
    }
    return {
      content: [{ type: 'text' as const, text: `Error calling RAG API: ${errorMessage}` }],
      isError: true,
    };
  }
}

/**
 * Register the 'rag_query' tool.
 * This tool allows the LLM to ask questions to the local RAG system.
 */
server.registerTool(
  'rag_query',
  {
    description: 'Query the local RAG system for information based on ingested documents.',
    inputSchema: {
      question: z.string().describe('The question to ask the RAG system'),
      search_mode: z
        .enum(['vector', 'keyword', 'hybrid'])
        .default('vector')
        .describe('The search mode to use'),
      top_k: z.number().default(3).describe('Number of context chunks to retrieve'),
    },
  },
  ragQueryHandler,
);

/**
 * Main entry point to start the server via stdio transport.
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('RAG MCP Bridge server running on stdio');
}

// Only run main if this file is being executed directly
if (import.meta.url.endsWith(process.argv[1]) || process.env.NODE_ENV !== 'test') {
  main().catch((error) => {
    console.error('Fatal error starting MCP server:', error);
    process.exit(1);
  });
}
