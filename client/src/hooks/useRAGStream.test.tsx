import { act, renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../lib/api-client";
import { useRAGStream } from "./useRAGStream";

vi.mock("../lib/api-client", () => ({
  api: {
    queryStream: vi.fn(),
  },
}));

describe("useRAGStream", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should stream content correctly", async () => {
    const mockChunks = [
      'data: {"content": "Hello"}\n\n',
      'data: {"content": " world"}\n\n',
      "data: [DONE]\n\n",
    ];

    const stream = new ReadableStream({
      start(controller) {
        mockChunks.forEach((chunk) => {
          controller.enqueue(new TextEncoder().encode(chunk));
        });
        controller.close();
      },
    });

    (api.queryStream as any).mockResolvedValue({
      ok: true,
      body: stream,
    });

    const { result } = renderHook(() => useRAGStream());

    act(() => {
      result.current.streamQuery({ question: "Hello?" });
    });

    await waitFor(() => expect(result.current.content).toBe("Hello world"));
    expect(result.current.isStreaming).toBe(false);
  });

  it("should handle errors during streaming", async () => {
    (api.queryStream as any).mockResolvedValue({
      ok: false,
      statusText: "Internal Server Error",
    });

    const { result } = renderHook(() => useRAGStream());

    act(() => {
      result.current.streamQuery({ question: "Fail?" });
    });

    await waitFor(() => expect(result.current.error).toBeDefined());
    expect(result.current.isStreaming).toBe(false);
  });
});
