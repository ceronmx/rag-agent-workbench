import { X, FileText, Download, Loader2, Maximize2, Minimize2 } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { DocumentInfo } from "@/types/api";
import { cn } from "@/lib/utils";

// Getting the base URL similarly to api-client
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface DocumentPreviewProps {
  document: DocumentInfo;
  onClose: () => void;
}

export function DocumentPreview({ document, onClose }: DocumentPreviewProps) {
  const [textContent, setTextContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMaximized, setIsMaximized] = useState(false);

  const previewUrl = `${API_BASE_URL}${document.preview_url}`;
  const isText = ["txt", "md", "csv", "text"].includes(document.file_type.toLowerCase());
  const isPdf = document.file_type.toLowerCase() === "pdf";

  useEffect(() => {
    if (isText) {
      fetchTextContent();
    }
  }, [document]);

  const fetchTextContent = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(previewUrl);
      if (!response.ok) throw new Error("Failed to load document content");
      const text = await response.text();
      setTextContent(text);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] bg-background/90 backdrop-blur-md flex items-center justify-center p-4 lg:p-12 animate-in fade-in duration-300">
      <Card 
        className={cn(
          "bg-surface-low border-white/10 shadow-[0_32px_128px_-16px_rgba(0,0,0,0.7)] flex flex-col transition-all duration-500 ease-in-out overflow-hidden",
          isMaximized ? "w-full h-full" : "w-full h-full max-w-6xl max-h-[85vh] rounded-3xl"
        )}
      >
        {/* Header */}
        <div className="p-5 border-b border-white/5 flex items-center justify-between bg-surface-highest/10 backdrop-blur-xl">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center text-primary shadow-[0_0_15px_rgba(192,193,255,0.2)]">
              <FileText size={20} />
            </div>
            <div>
              <h3 className="font-bold text-lg tracking-tight leading-none">{document.document_name}</h3>
              <p className="text-[10px] text-muted-foreground uppercase tracking-widest mt-1 font-bold">
                {document.file_type} • {document.chunk_count} Chunks
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full hover:bg-white/10 w-10 h-10 text-muted-foreground hover:text-foreground p-0"
            >
              <a href={previewUrl} download={document.document_name} className="flex items-center justify-center w-full h-full">
                <Download size={18} />
              </a>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMaximized(!isMaximized)}
              className="rounded-full hover:bg-white/10 w-10 h-10 text-muted-foreground hover:text-foreground hidden sm:flex"
            >
              {isMaximized ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
            </Button>
            <div className="w-px h-6 bg-white/10 mx-1" />
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              aria-label="Close"
              className="rounded-full hover:bg-destructive/20 w-10 h-10 text-muted-foreground hover:text-destructive transition-colors"
            >
              <X size={20} />
            </Button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-hidden bg-surface-lowest/50 relative">
          {isLoading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 z-10 bg-surface-low/50">
              <Loader2 className="animate-spin text-primary" size={40} />
              <p className="text-sm font-bold text-primary animate-pulse tracking-widest uppercase">Loading Document...</p>
            </div>
          )}

          {error && (
            <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center gap-4">
              <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center text-destructive mb-2">
                <X size={32} />
              </div>
              <h4 className="text-xl font-bold">Preview Failed</h4>
              <p className="text-muted-foreground max-w-md">{error}</p>
              <Button onClick={fetchTextContent} variant="outline" className="mt-2">Try Again</Button>
            </div>
          )}

          {!isLoading && !error && (
            <>
              {isPdf ? (
                <iframe
                  src={`${previewUrl}#toolbar=0`}
                  className="w-full h-full border-none"
                  title={document.document_name}
                />
              ) : isText ? (
                <ScrollArea className="h-full w-full">
                  <div className="p-8 lg:p-12 max-w-4xl mx-auto">
                    <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-on-surface-variant bg-surface-mid/30 p-8 rounded-2xl border border-white/5">
                      {textContent}
                    </pre>
                  </div>
                </ScrollArea>
              ) : (
                <div className="h-full flex flex-col items-center justify-center gap-6 p-8 text-center">
                  <div className="w-20 h-20 rounded-3xl bg-surface-highest flex items-center justify-center text-muted-foreground shadow-inner">
                    <FileText size={40} />
                  </div>
                  <div>
                    <h4 className="text-xl font-bold mb-2">No Visual Preview Available</h4>
                    <p className="text-muted-foreground max-w-xs mx-auto">
                      This file type ({document.file_type}) cannot be previewed directly in the browser.
                    </p>
                  </div>
                  <Button variant="secondary" className="gap-2 px-8 py-6 rounded-2xl font-bold p-0 overflow-hidden">
                    <a href={previewUrl} download={document.document_name} className="flex items-center justify-center w-full h-full px-8 py-6">
                      <Download size={20} />
                      Download to View
                    </a>
                  </Button>
                </div>
              )}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-surface-lowest border-t border-white/5 flex items-center justify-center">
           <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse mr-2 shadow-[0_0_8px_rgba(192,193,255,0.5)]" />
           <span className="text-[9px] font-black uppercase tracking-[0.2em] text-muted-foreground/60">
             Secure Cognitive Preview Active
           </span>
        </div>
      </Card>
    </div>
  );
}
