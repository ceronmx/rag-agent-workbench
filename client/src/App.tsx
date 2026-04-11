import { 
  Plus, 
  Download, 
  FileText,
  Send,
  Sparkles,
  User,
  Settings,
  MoreVertical,
  ArrowUp,
  FileCode,
  FileJson
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Layout } from "./components/layout/Layout"

function App() {
  return (
    <Layout>
      {/* Mobile-only Stats or Latest Synthesis (based on mobile screenshot) */}
      <div className="lg:hidden space-y-6 mb-8">
        <div className="space-y-2">
          <p className="text-[10px] font-bold text-tertiary uppercase tracking-[0.2em]">System Thought</p>
          <h2 className="text-2xl font-bold tracking-tight">Latest Synthesis</h2>
        </div>
        
        <Card className="p-6 bg-surface-container-low border-l-4 border-primary/40 rounded-r-xl space-y-4">
          <p className="text-sm text-on-surface-variant leading-relaxed">
            Analysis of the <span className="text-primary font-medium">Technical_Specs_Monolith.docx</span> indicates a 15% efficiency gain in the retrieval pipeline since the last index.
          </p>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="bg-surface-container-highest text-[10px] font-bold tracking-wider px-3 py-1 uppercase rounded-md border-none">
              Citation: ARCH-04
            </Badge>
            <div className="w-2 h-2 rounded-full bg-tertiary shadow-[0_0_8px_rgba(255,183,131,0.5)]" />
          </div>
        </Card>

        <div className="grid grid-cols-2 gap-4">
          <Card className="p-5 bg-surface-container-low border-none space-y-2">
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Latency</p>
            <p className="text-2xl font-bold tracking-tight">240ms</p>
          </Card>
          <Card className="p-5 bg-surface-container-low border-none space-y-2">
            <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Accuracy</p>
            <p className="text-2xl font-bold tracking-tight">99.2%</p>
          </Card>
        </div>
      </div>

      {/* Data Sources Section */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
               <h2 className="text-2xl lg:text-3xl font-bold tracking-tight uppercase lg:normal-case">Data Sources</h2>
               <Badge className="lg:hidden bg-transparent border-none text-muted-foreground font-bold text-xs p-0">8 Files Total</Badge>
            </div>
            <p className="text-[10px] text-muted-foreground uppercase tracking-[0.2em] mt-1 font-bold hidden lg:block">Manage knowledge base corpus</p>
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90 gap-2 font-bold h-12 px-6 rounded-xl shadow-lg shadow-primary/20 hidden lg:flex">
            <Plus size={20} />
            UPLOAD NEW
          </Button>
        </div>

        {/* Desktop View (Table) */}
        <Card className="hidden lg:block border-none bg-surface-container-lowest overflow-hidden shadow-2xl rounded-2xl">
          <Table>
            <TableHeader className="bg-surface-container-low/50">
              <TableRow className="hover:bg-transparent border-border h-16">
                <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] pl-8">File Name</TableHead>
                <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">Size</TableHead>
                <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">Upload Date</TableHead>
                <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">Status</TableHead>
                <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] text-right pr-8">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {[
                { name: "Q4_Financial_Report.pdf", size: "12.4 MB", date: "Oct 24, 2023", status: "INDEXED", type: 'pdf' },
                { name: "Technical_Specs_Monolith.docx", size: "4.1 MB", date: "Oct 25, 2023", status: "PENDING", type: 'doc' },
                { name: "Customer_Feedback_Log.csv", size: "856 KB", date: "Oct 26, 2023", status: "INDEXED", type: 'csv' },
              ].map((file) => (
                <TableRow key={file.name} className="border-border hover:bg-surface-container/30 transition-colors h-24">
                  <TableCell className="font-semibold py-4 pl-8">
                    <div className="flex items-center gap-4">
                      <div className={cn(
                        "w-11 h-11 rounded-lg flex items-center justify-center border border-border/50 shadow-sm",
                        file.type === 'pdf' ? "bg-surface-container-highest text-primary" : 
                        file.type === 'doc' ? "bg-surface-container-highest text-muted-foreground" :
                        "bg-surface-container-highest text-tertiary"
                      )}>
                        {file.type === 'pdf' && <FileText size={22} />}
                        {file.type === 'doc' && <FileText size={22} />}
                        {file.type === 'csv' && <FileCode size={22} />}
                      </div>
                      <span className="text-base font-bold">{file.name}</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-muted-foreground font-bold text-sm">{file.size}</TableCell>
                  <TableCell className="text-muted-foreground font-bold text-sm">{file.date}</TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={
                      file.status === "INDEXED" 
                      ? "bg-surface-container-highest text-foreground border-none px-4 py-1.5 font-bold text-[10px] tracking-widest rounded-full" 
                      : "bg-surface-container-high/50 text-tertiary border border-tertiary/30 px-4 py-1.5 font-bold text-[10px] tracking-widest rounded-full"
                    }>
                      <div className={`w-1.5 h-1.5 rounded-full mr-2 ${file.status === "INDEXED" ? "bg-primary" : "bg-tertiary"}`} />
                      {file.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right pr-8">
                    <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground font-bold uppercase text-[10px] tracking-[0.2em] h-10 px-4">
                      <Download size={18} />
                      Download
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Mobile View (List) */}
        <div className="lg:hidden space-y-3">
           {[
            { name: "Q4_Financial_Report.pdf", size: "2.4 MB", status: "INDEXED", type: 'pdf' },
            { name: "Technical_Specs_Monolith.docx", size: "1.1 MB", status: "INDEXED", type: 'doc' },
            { name: "Legacy_Systems_V2.pdf", size: "15.8 MB", status: "PENDING", type: 'pdf' },
          ].map((file) => (
            <Card key={file.name} className="p-4 bg-surface-container-low border-none flex items-center justify-between rounded-xl">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-surface-container-lowest flex items-center justify-center text-on-surface border border-border/30">
                  <FileText size={24} />
                </div>
                <div className="space-y-1">
                  <h3 className="font-bold text-sm tracking-tight">{file.name}</h3>
                  <div className="flex items-center gap-2">
                    <span className={cn(
                      "text-[9px] font-bold uppercase tracking-widest",
                      file.status === 'INDEXED' ? "text-primary" : "text-tertiary"
                    )}>{file.status}</span>
                    <span className="text-[9px] text-muted-foreground font-bold uppercase tracking-widest">• {file.size}</span>
                  </div>
                </div>
              </div>
              <Button variant="ghost" size="icon" className="bg-surface-container-highest/50 h-10 w-10 rounded-xl">
                {file.status === 'INDEXED' ? <Download size={18} /> : <MoreVertical size={18} />}
              </Button>
            </Card>
          ))}
        </div>
      </section>

      {/* Intelligence Output Section (Desktop Only in this view) */}
      <section className="space-y-4 pt-4 hidden lg:block">
        <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">Intelligence Output</p>
        <Card className="flex flex-col items-center justify-center py-28 text-center space-y-6 bg-surface-container-lowest border-none shadow-inner rounded-3xl relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent pointer-events-none" />
          <div className="relative">
             <div className="absolute inset-0 blur-3xl bg-primary/20 rounded-full" />
             <Sparkles className="text-muted-foreground/30 relative" size={64} />
          </div>
          <div className="space-y-2 relative">
            <p className="text-muted-foreground italic text-lg max-w-md font-medium leading-relaxed">
              Ready for query context...
            </p>
            <p className="text-muted-foreground/50 text-sm font-medium">Ask the Monolith anything about your data sources.</p>
          </div>
          
          <div className="pt-4">
             <Badge variant="outline" className="border-border bg-surface-container-low/50 text-muted-foreground font-bold px-4 py-2 rounded-lg gap-2 cursor-pointer hover:bg-surface-container-high transition-colors">
               <FileText size={14} className="text-primary/50" />
               SOURCE_ID: FIN_Q4
             </Badge>
          </div>
        </Card>
      </section>

      {/* Mobile Ask RAG... Input */}
      <div className="lg:hidden mt-8 space-y-4">
        <div className="relative">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground">
            <Sparkles size={18} />
          </div>
          <Input 
            placeholder="Ask RAG..." 
            className="pl-12 pr-16 h-14 bg-surface-container-low border-none ring-offset-background placeholder:text-muted-foreground/50 focus-visible:ring-ring text-base rounded-2xl font-bold"
          />
          <Button className="absolute right-1.5 top-1/2 -translate-y-1/2 bg-primary/80 text-primary-foreground hover:bg-primary h-11 w-11 p-0 rounded-xl">
            <ArrowUp size={22} strokeWidth={3} />
          </Button>
        </div>
      </div>

      {/* Desktop Footer (Input) */}
      <div className="hidden lg:block sticky bottom-6 z-10 pt-4">
        <Card className="max-w-4xl mx-auto p-2 bg-surface-container-low/95 backdrop-blur-2xl border border-white/5 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.5)] rounded-2xl">
          <div className="relative flex items-center">
            <div className="absolute left-5 top-1/2 -translate-y-1/2 text-muted-foreground">
              <Sparkles size={20} />
            </div>
            <Input 
              placeholder="Synthesize current financial trajectories based on retrieved reports..." 
              className="pl-16 pr-40 h-20 bg-surface-container-highest/20 border-none ring-offset-background placeholder:text-muted-foreground/40 focus-visible:ring-ring text-lg rounded-xl font-medium shadow-inner"
            />
            <Button className="absolute right-2 top-1/2 -translate-y-1/2 bg-primary text-primary-foreground hover:bg-primary/90 gap-3 font-bold px-8 h-16 rounded-xl shadow-xl shadow-primary/20 transition-all hover:scale-[1.02] active:scale-[0.98]">
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
      </div>
    </Layout>
  )
}

// Utility for cleaner class merging (using the one from lib/utils)
import { cn } from "@/lib/utils"

export default App
