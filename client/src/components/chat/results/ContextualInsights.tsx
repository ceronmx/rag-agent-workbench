import { Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";

export function ContextualInsights() {
  return (
    <section className="space-y-4 pt-10 pb-20">
      <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">
        Contextual Insights
      </p>
      <Card className="p-8 bg-surface-container-lowest border-none shadow-inner rounded-3xl text-center">
        <Sparkles className="text-muted-foreground/20 mx-auto mb-4" size={40} />
        <p className="text-muted-foreground text-sm font-medium">
          Ask the Monolith about your data to generate deep insights.
        </p>
      </Card>
    </section>
  );
}
