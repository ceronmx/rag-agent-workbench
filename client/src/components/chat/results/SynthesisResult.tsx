import { 
  Sparkles, 
  Loader2, 
  AlertCircle 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { QueryResponse } from "@/types/api"
import { cn } from "@/lib/utils"

interface SynthesisResultProps {
  lastResult: QueryResponse | null
  isLoading: boolean
  isError: boolean
  error: any
  onClear: () => void
  isUploading: boolean
}

export function SynthesisResult({ 
  lastResult, 
  isLoading, 
  isError, 
  error, 
  onClear, 
  isUploading 
}: SynthesisResultProps) {
  return (
    <div className="space-y-6 mb-10">
      <div className="space-y-2">
        <p className="text-[10px] font-bold text-tertiary uppercase tracking-[0.2em]">
          {lastResult ? "Query Result" : "System Status"}
        </p>
        <h2 className="text-2xl font-bold tracking-tight">
          {lastResult ? "Latest Synthesis" : "System Ready"}
        </h2>
      </div>
      
      <Card className={cn(
        "p-6 bg-surface-container-low border-l-4 rounded-r-xl space-y-4 border-y-0 border-r-0 transition-all shadow-lg",
        isError ? "border-error" : "border-primary/40"
      )}>
        {isLoading ? (
          <div className="flex items-center gap-4 py-4">
            <Loader2 className="animate-spin text-primary" size={24} />
            <p className="text-sm text-on-surface-variant font-medium animate-pulse">
              The Monolith is synthesizing an answer...
            </p>
          </div>
        ) : isError ? (
          <div className="flex items-center gap-3 text-error">
            <AlertCircle size={20} />
            <p className="text-sm font-medium">Query Error: {error?.message || "Failed to get response"}</p>
          </div>
        ) : lastResult ? (
          <div className="space-y-4">
            <p className="text-sm lg:text-base text-on-surface-variant leading-relaxed font-medium">
              {lastResult.answer}
            </p>
            <div className="flex flex-wrap items-center gap-2">
              {lastResult.contexts.slice(0, 3).map((ctx, idx) => (
                <Badge key={idx} variant="secondary" className="bg-surface-container-highest text-[10px] font-bold tracking-wider px-3 py-1 uppercase rounded-md border-none">
                  Source: {ctx.document_name}
                </Badge>
              ))}
              <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(192,193,255,0.5)]" />
            </div>
            <div className="pt-2">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={onClear}
                className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground hover:text-foreground h-auto p-0"
              >
                Clear Result
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-sm text-on-surface-variant leading-relaxed font-medium">
              {isUploading 
                ? "Ingesting your document into the vector space..." 
                : "Welcome to Cognitive Monolith. Start by uploading documents or asking a question below."}
            </p>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-surface-container-highest text-[10px] font-bold tracking-wider px-3 py-1 uppercase rounded-md border-none">
                {isUploading ? "UPLOADING" : "SYSTEM READY"}
              </Badge>
              <div className={cn(
                "w-2 h-2 rounded-full",
                isUploading ? "bg-tertiary animate-bounce shadow-[0_0_8px_rgba(255,183,131,0.5)]" : "bg-primary animate-pulse shadow-[0_0_8px_rgba(192,193,255,0.5)]"
              )} />
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}
