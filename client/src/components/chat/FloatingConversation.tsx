import { X, Sparkles, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { useEffect, useRef } from "react";

interface FloatingConversationProps {
  isOpen: boolean;
  content: string;
  isStreaming: boolean;
  onClose: () => void;
}

export function FloatingConversation({
  isOpen,
  content,
  isStreaming,
  onClose,
}: FloatingConversationProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom as content streams in
  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [content]);

  return (
    <div
      className={cn(
        "fixed bottom-24 lg:bottom-32 right-4 left-4 lg:left-auto lg:right-8 lg:w-[450px] z-50 transition-all duration-500 ease-out transform",
        isOpen 
          ? "opacity-100 translate-y-0 scale-100" 
          : "opacity-0 translate-y-10 scale-95 pointer-events-none"
      )}
    >
      <Card className="bg-surface-low/95 backdrop-blur-3xl border border-white/10 shadow-[0_32px_128px_-16px_rgba(0,0,0,0.7)] rounded-3xl overflow-hidden flex flex-col max-h-[70vh]">
        <div className="p-5 border-b border-white/5 flex items-center justify-between bg-surface-highest/10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shadow-[0_0_15px_rgba(192,193,255,0.3)]">
              <Sparkles size={16} />
            </div>
            <span className="font-bold text-sm tracking-tight">COGNITIVE STREAM</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="rounded-full hover:bg-white/10 w-8 h-8"
          >
            <X size={16} />
          </Button>
        </div>

        <ScrollArea ref={scrollRef} className="flex-1 p-6 min-h-[100px]">
          <div className="space-y-4">
            <div className="prose prose-invert max-w-none text-sm leading-relaxed font-medium text-on-surface-variant">
              {content || (isStreaming ? "" : "Ask anything to start...")}
            </div>
            
            {isStreaming && (
              <div className="flex items-center gap-2 text-[10px] font-bold text-primary animate-pulse">
                <Loader2 size={12} className="animate-spin" />
                AI IS TYPING...
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="p-4 bg-surface-lowest/50 border-t border-white/5 flex items-center justify-center">
           <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse mr-2 shadow-[0_0_8px_rgba(192,193,255,0.5)]" />
           <span className="text-[9px] font-black uppercase tracking-[0.2em] text-muted-foreground/60">
             Real-time Synthesis Active
           </span>
        </div>
      </Card>
    </div>
  );
}
