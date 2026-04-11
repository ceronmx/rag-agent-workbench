import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../lib/api-client";
import { useRAGQuery } from "./useRAGQuery";

vi.mock("../lib/api-client", () => ({
  api: {
    query: vi.fn(),
  },
}));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe("useRAGQuery", () => {
  beforeEach(() => {
    queryClient.clear();
    vi.clearAllMocks();
  });

  it("executes query and stores result", async () => {
    const mockResponse = {
      answer: "The answer is 42",
      contexts: [],
      search_query: "",
      search_mode: "vector",
      is_stream: false,
    };
    (api.query as any).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useRAGQuery(), { wrapper });

    await result.current.queryMutation.mutateAsync({ question: "What is the answer?" });

    expect(api.query).toHaveBeenCalledWith(
      expect.objectContaining({ question: "What is the answer?" }),
    );
    await waitFor(() => expect(result.current.lastResult).toEqual(mockResponse));
  });
});
