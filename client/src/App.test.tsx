import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen } from "@testing-library/react";
import type React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { useDocuments } from "./hooks/useDocuments";
import { useRAGQuery } from "./hooks/useRAGQuery";

vi.mock("./hooks/useDocuments");
vi.mock("./hooks/useRAGQuery");

const queryClient = new QueryClient();
const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe("App Search", () => {
  beforeEach(() => {
    vi.mocked(useDocuments).mockReturnValue({
      documents: [
        { document_name: "apple.pdf", chunk_count: 1, file_type: "pdf" },
        { document_name: "banana.docx", chunk_count: 2, file_type: "doc" },
      ],
      isLoading: false,
      isError: false,
      error: null,
      uploadMutation: { isPending: false } as any,
      deleteMutation: { isPending: false } as any,
      refetch: vi.fn(),
    });

    vi.mocked(useRAGQuery).mockReturnValue({
      queryMutation: { isPending: false } as any,
      lastResult: null,
      isLoading: false,
      isError: false,
      error: null,
      clearResult: vi.fn(),
    });
  });

  it("filters document list based on search input", () => {
    // This test will fail initially because we haven't implemented search yet
    render(<App />, { wrapper });

    // Header search input
    const searchInput = screen.getByPlaceholderText(/Search embeddings/i);

    expect(screen.getAllByText("apple.pdf")[0]).toBeInTheDocument();
    expect(screen.getAllByText("banana.docx")[0]).toBeInTheDocument();

    fireEvent.change(searchInput, { target: { value: "apple" } });

    expect(screen.getAllByText("apple.pdf")[0]).toBeInTheDocument();
    expect(screen.queryByText("banana.docx")).not.toBeInTheDocument();
  });
});
