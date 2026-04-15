import { renderHook, act, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { useRAGStream } from "./useRAGStream";

describe("useRAGStream", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock global fetch
    global.fetch = vi.fn();
  });

  it("should stream content correctly", async () => {
    const mockChunks = [
      'data: {"content": "Hello"}\n\n',
      'data: {"content": " world"}\n\n',
      'data: [DONE]\n\n',
    ];

    const stream = new ReadableStream({
      start(controller) {
        mockChunks.forEach(chunk => controller.enqueue(new TextEncoder().encode(chunk)));
        controller.close();
      },
    });

    (global.fetch as any).mockResolvedValue({
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
    (global.fetch as any).mockResolvedValue({
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
