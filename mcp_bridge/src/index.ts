import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import { z } from 'zod';

// Configuration for the local RAG API
const RAG_API_BASE_URL = process.env.RAG_API_BASE_URL || 'http://127.0.0.1:8000';

const server = new McpServer({
  name: 'rag-bridge',
  version: '1.0.0',
});

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
  async ({ question, search_mode, top_k }) => {
    try {
      const response = await axios.post(`${RAG_API_BASE_URL}/query/`, {
        question,
        search_mode,
        top_k,
        use_stream: false,
      });

      const data = response.data;

      // Format the response for the MCP client
      let resultText = `Answer: ${data.answer}\n\n`;
      resultText += `Search Query used: ${data.search_query}\n`;
      resultText += `Search Mode: ${data.search_mode}\n\n`;
      resultText += 'Contexts used:\n';

      for (const context of data.contexts) {
        resultText += `--- Document: ${context.document_name} (Chunk ${context.chunk_index}) ---\n`;
        resultText += `${context.text}\n\n`;
      }

      return {
        content: [{ type: 'text', text: resultText }],
      };
    } catch (error) {
      let errorMessage = 'Unknown error';
      if (axios.isAxiosError(error)) {
        errorMessage = error.response?.data?.detail || error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      return {
        content: [{ type: 'text', text: `Error calling RAG API: ${errorMessage}` }],
        isError: true,
      };
    }
  },
);

/**
 * Main entry point to start the server via stdio transport.
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('RAG MCP Bridge server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error starting MCP server:', error);
  process.exit(1);
});
