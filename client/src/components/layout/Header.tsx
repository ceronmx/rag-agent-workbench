import { 
  Search, 
  Bell, 
  History, 
  User 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function Header() {
  return (
    <header className="h-20 lg:h-24 border-b border-border flex items-center justify-between px-6 lg:px-8 bg-background/50 backdrop-blur-md">
      <div className="flex items-center gap-6 flex-1 max-w-2xl">
        <div className="flex items-center gap-3 lg:hidden">
          <div className="w-8 h-8 rounded-lg bg-surface-bright flex items-center justify-center border border-border overflow-hidden">
            <User size={18} />
          </div>
          <h1 className="text-xl font-bold tracking-tight">Cognitive Monolith</h1>
        </div>
        
        <div className="relative w-full max-w-md hidden md:block">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
          <Input 
            placeholder="Search embeddings..." 
            className="pl-12 h-12 bg-surface-container-low border-none ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring text-base rounded-xl"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground hidden sm:flex h-11 w-11">
          <Bell size={22} />
        </Button>
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground hidden sm:flex h-11 w-11">
          <History size={22} />
        </Button>
        <Search className="text-muted-foreground md:hidden" size={24} />
        <div className="w-10 h-10 lg:w-11 lg:h-11 rounded-lg border-2 border-surface-container-highest overflow-hidden p-0.5">
          <img src="https://github.com/shadcn.png" alt="Avatar" className="w-full h-full object-cover rounded-md" />
        </div>
      </div>
    </header>
  )
}
