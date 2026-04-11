import axios from 'axios';
import { type Mock, describe, expect, it, vi } from 'vitest';
import { ragQueryHandler } from './index.js';

// Mock axios
vi.mock('axios');
const mockedAxios = vi.mocked(axios);

describe('MCP Bridge - rag_query tool', () => {
  it('should successfully return formatted results from RAG API', async () => {
    // Mock RAG API response
    const mockApiResponse = {
      data: {
        answer: 'FastAPI is a modern web framework.',
        search_query: 'what is fastapi',
        search_mode: 'vector',
        contexts: [
          {
            document_name: 'docs.pdf',
            chunk_index: 0,
            text: 'FastAPI is fast and easy to use.',
          },
        ],
      },
    };

    (mockedAxios.post as Mock).mockResolvedValue(mockApiResponse);

    const result = await ragQueryHandler({
      question: 'What is FastAPI?',
      search_mode: 'vector',
      top_k: 3,
    });

    expect(mockedAxios.post).toHaveBeenCalledWith(expect.stringContaining('/query'), {
      question: 'What is FastAPI?',
      search_mode: 'vector',
      top_k: 3,
      use_stream: false,
    });

    expect(result.content[0].text).toContain('FastAPI is a modern web framework.');
    expect(result.content[0].text).toContain('Sources:');
    expect(result.content[0].text).toContain('- docs.pdf');
    expect(result.content[0].text).not.toContain('FastAPI is fast and easy to use.');
    expect(result.content[0].text).not.toContain('Search Query used:');
  });

  it('should handle errors from RAG API gracefully', async () => {
    (mockedAxios.post as Mock).mockRejectedValue({
      isAxiosError: true,
      response: {
        data: {
          detail: 'Database connection failed',
        },
      },
    });

    // We need to ensure axios.isAxiosError returns true for this mock
    (mockedAxios.isAxiosError as Mock).mockReturnValue(true);

    const result = await ragQueryHandler({
      question: 'Error test',
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain('Error calling RAG API: Database connection failed');
  });
});
