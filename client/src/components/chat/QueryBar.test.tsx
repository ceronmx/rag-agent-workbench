import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { QueryBar } from "./QueryBar";
import "@testing-library/jest-dom";

describe("QueryBar", () => {
  it("renders the query input and button", () => {
    render(<QueryBar onQuery={() => {}} />);
    expect(screen.getByPlaceholderText(/Ask RAG/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /ASK RAG/i })).toBeInTheDocument();
  });

  it("calls onQuery with input value when button is clicked", () => {
    const onQuery = vi.fn();
    render(<QueryBar onQuery={onQuery} />);

    const input = screen.getByPlaceholderText(/Ask RAG/i);
    const button = screen.getByRole("button", { name: /ASK RAG/i });

    fireEvent.change(input, { target: { value: "How does pgvector work?" } });
    fireEvent.click(button);

    expect(onQuery).toHaveBeenCalledWith("How does pgvector work?");
  });

  it("calls onQuery on Enter key press", () => {
    const onQuery = vi.fn();
    render(<QueryBar onQuery={onQuery} />);

    const input = screen.getByPlaceholderText(/Ask RAG/i);

    fireEvent.change(input, { target: { value: "What is RAG?" } });
    fireEvent.keyDown(input, { key: "Enter", code: "Enter" });

    expect(onQuery).toHaveBeenCalledWith("What is RAG?");
  });
});
