import { Settings, Sparkles, User } from "lucide-react";
import type React from "react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

interface QueryBarProps {
  onQuery: (question: string) => void;
  isLoading?: boolean;
}

export function QueryBar({ onQuery, isLoading }: QueryBarProps) {
  const [value, setValue] = useState("");

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (value.trim() && !isLoading) {
      onQuery(value);
      setValue("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <Card className="max-w-4xl mx-auto p-2 bg-surface-container-low/95 backdrop-blur-2xl border border-white/5 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.5)] rounded-2xl">
      <div className="relative flex items-center">
        <div className="absolute left-5 top-1/2 -translate-y-1/2 text-muted-foreground">
          <User size={20} />
        </div>
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          placeholder="Ask RAG..."
          className="pl-16 pr-40 h-16 bg-surface-container-highest/20 border-none ring-offset-background placeholder:text-muted-foreground/40 focus-visible:ring-ring text-lg rounded-xl font-medium shadow-inner"
        />
        <Button
          onClick={handleSubmit}
          disabled={isLoading || !value.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-primary text-primary-foreground hover:bg-primary/90 gap-3 font-bold px-8 h-14 rounded-xl shadow-xl shadow-primary/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
        >
          <Sparkles size={20} />
          ASK RAG
        </Button>
      </div>
      <div className="flex flex-wrap items-center justify-center gap-y-2 gap-x-10 mt-4 pb-2 text-[10px] text-muted-foreground/60 uppercase font-black tracking-[0.2em]">
        <span className="flex items-center gap-2">
          <Settings size={14} className="text-primary/40" />
          TEMPERATURE: 0.7
        </span>
        <span className="flex items-center gap-2">
          <Settings size={14} className="text-primary/40" />
          MAX TOKENS: 2048
        </span>
        <span className="flex items-center gap-2">
          <Settings size={14} className="text-primary/40" />
          MODEL: GPT-4-TURBO
        </span>
      </div>
    </Card>
  );
}
