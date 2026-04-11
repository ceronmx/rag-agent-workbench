import { 
  LayoutGrid, 
  Settings, 
  User 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  return (
    <aside className={cn("hidden lg:flex flex-col", className)}>
      <div className="p-8">
        <h2 className="text-xl font-bold tracking-tight text-on-surface">Cognitive Monolith</h2>
        <p className="text-[10px] text-muted-foreground uppercase tracking-[0.2em] mt-1 font-semibold">RAG Intelligence</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-1.5 mt-4">
        <Button variant="secondary" className="w-full justify-start gap-3 bg-surface-container-highest/50 text-foreground border-none hover:bg-surface-container-highest h-11 px-4">
          <LayoutGrid size={20} className="text-primary" />
          <span className="font-medium">KNOWLEDGE BASE</span>
        </Button>
        <Button variant="ghost" className="w-full justify-start gap-3 text-muted-foreground hover:text-foreground h-11 px-4 hover:bg-surface-container-highest/30">
          <Settings size={20} />
          <span className="font-medium uppercase tracking-wide text-xs">Settings</span>
        </Button>
      </nav>

      <div className="p-6 border-t border-border flex items-center gap-3 mt-auto bg-surface-container-lowest/50">
        <div className="w-10 h-10 rounded-lg bg-surface-bright flex items-center justify-center border border-border">
          <User size={20} />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-semibold">Admin</span>
          <span className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">v2.4.0-retrieval</span>
        </div>
      </div>
    </aside>
  )
}
