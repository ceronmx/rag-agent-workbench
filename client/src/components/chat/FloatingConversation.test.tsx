import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FloatingConversation } from "./FloatingConversation";

describe("FloatingConversation", () => {
  it("renders when isOpen is true", () => {
    render(
      <FloatingConversation 
        isOpen={true} 
        content="Hello world" 
        isStreaming={true} 
        onClose={() => {}} 
      />
    );
    expect(screen.getByText("Hello world")).toBeInTheDocument();
    expect(screen.getByText(/AI is typing/i)).toBeInTheDocument();
  });

  it("does not render content when isOpen is false", () => {
    const { container } = render(
      <FloatingConversation 
        isOpen={false} 
        content="Hello world" 
        isStreaming={false} 
        onClose={() => {}} 
      />
    );
    // It might still be in DOM but hidden with opacity-0
    const box = container.querySelector(".opacity-0");
    expect(box).toBeInTheDocument();
  });
});
