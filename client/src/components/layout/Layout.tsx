import type React from "react";
import { toast } from "sonner";
import { useRAGQuery } from "@/hooks/useRAGQuery";
import { QueryBar } from "../chat/QueryBar";
import { Header } from "./Header";
import { MobileNav } from "./MobileNav";
import { Sidebar } from "./Sidebar";

interface LayoutProps {
  children: React.ReactNode;
  searchQuery?: string;
  onSearchChange?: (value: string) => void;
}

export function Layout({ children, searchQuery, onSearchChange }: LayoutProps) {
  const { queryMutation, isLoading: isQueryLoading } = useRAGQuery();

  const handleQuery = async (question: string) => {
    try {
      await queryMutation.mutateAsync({ question });
      toast.success("Query successful");
    } catch (err) {
      toast.error(`Query failed: ${(err as any).message || "Unknown error"}`);
    }
  };

  return (
    <div className="flex min-h-screen bg-background text-foreground font-sans overflow-hidden">
      {/* Sidebar - Desktop */}
      <Sidebar className="hidden lg:flex w-64 flex-col border-r border-border bg-surface-container-low" />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 relative">
        <Header searchQuery={searchQuery} onSearchChange={onSearchChange} />

        <main className="flex-1 overflow-auto p-4 lg:p-8 pb-32 lg:pb-40">
          <div className="max-w-7xl mx-auto">{children}</div>
        </main>

        {/* Floating Query Bar - Fixed at bottom of main content */}
        <div className="absolute bottom-0 left-0 right-0 p-4 lg:p-8 pointer-events-none z-20">
          <div className="max-w-4xl mx-auto pointer-events-auto">
            <QueryBar onQuery={handleQuery} isLoading={isQueryLoading} />
          </div>
        </div>

        {/* Mobile Nav Spacer */}
        <div className="h-16 lg:hidden shrink-0" />
      </div>

      {/* Mobile Bottom Navigation */}
      <MobileNav className="lg:hidden fixed bottom-0 left-0 right-0 h-16 bg-surface-container-low border-t border-border z-50" />
    </div>
  );
}
