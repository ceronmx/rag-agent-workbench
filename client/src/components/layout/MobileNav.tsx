import { LayoutGrid, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface MobileNavProps {
  className?: string;
}

export function MobileNav({ className }: MobileNavProps) {
  return (
    <nav className={cn("flex lg:hidden items-center justify-around", className)}>
      <Button
        variant="ghost"
        className="flex flex-col h-full items-center justify-center gap-1.5 flex-1 rounded-none bg-surface-highest/30 border-b-2 border-primary text-foreground"
      >
        <LayoutGrid size={22} className="text-primary" />
        <span className="text-[10px] font-bold uppercase tracking-wider">Knowledge Base</span>
      </Button>
      <Button
        variant="ghost"
        className="flex flex-col h-full items-center justify-center gap-1.5 flex-1 rounded-none text-muted-foreground hover:text-foreground"
      >
        <Settings size={22} />
        <span className="text-[10px] font-bold uppercase tracking-wider">Settings</span>
      </Button>
    </nav>
  );
}
