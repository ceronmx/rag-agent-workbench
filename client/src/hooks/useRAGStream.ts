import { useState, useCallback } from "react";
import type { QueryRequest } from "../types/api";

export function useRAGStream() {
  const [content, setContent] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const streamQuery = useCallback(async (request: QueryRequest) => {
    setIsStreaming(true);
    setContent("");
    setError(null);

    try {
      const response = await fetch("/api/query/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...request,
          use_stream: true,
        }),
      });

      if (!response.ok) {
        throw new Error(response.statusText || "Failed to fetch");
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No reader available");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") {
              setIsStreaming(false);
              return;
            }

            try {
              const parsed = JSON.parse(data);
              if (parsed.content) {
                setContent((prev) => prev + parsed.content);
              } else if (parsed.error) {
                throw new Error(parsed.error);
              }
            } catch (e) {
              console.error("Error parsing stream chunk", e);
            }
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Unknown error"));
    } finally {
      setIsStreaming(false);
    }
  }, []);

  return {
    streamQuery,
    content,
    isStreaming,
    error,
    reset: () => {
      setContent("");
      setError(null);
      setIsStreaming(false);
    },
  };
}
