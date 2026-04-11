import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../lib/api-client";
import { useDocuments } from "./useDocuments";

vi.mock("../lib/api-client", () => ({
  api: {
    listDocuments: vi.fn(),
    deleteDocument: vi.fn(),
    ingestFile: vi.fn(),
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

describe("useDocuments", () => {
  beforeEach(() => {
    queryClient.clear();
    vi.clearAllMocks();
  });

  it("fetches documents correctly", async () => {
    const mockDocs = [{ document_name: "test.pdf", chunk_count: 5, file_type: "pdf" }];
    (api.listDocuments as any).mockResolvedValue(mockDocs);

    const { result } = renderHook(() => useDocuments(), { wrapper });

    await waitFor(() => expect(result.current.documents).toEqual(mockDocs));
    expect(api.listDocuments).toHaveBeenCalled();
  });

  it("calls deleteDocument and invalidates cache", async () => {
    (api.deleteDocument as any).mockResolvedValue({ status: "success" });
    const invalidateSpy = vi.spyOn(queryClient, "invalidateQueries");

    const { result } = renderHook(() => useDocuments(), { wrapper });

    await result.current.deleteMutation.mutateAsync("test.pdf");

    expect(api.deleteDocument).toHaveBeenCalled();
    expect(vi.mocked(api.deleteDocument).mock.calls[0][0]).toBe("test.pdf");
    expect(invalidateSpy).toHaveBeenCalled();
  });
});
