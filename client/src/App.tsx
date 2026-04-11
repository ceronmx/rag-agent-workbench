import { useRef, useState, useMemo } from "react"
import { 
  Plus, 
  Download, 
  FileText,
  Sparkles,
  MoreVertical,
  Trash2,
  Loader2,
  AlertCircle
} from "lucide-react"
import { Button } from "@/components/ui/button"
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
import { cn } from "@/lib/utils"
import { useDocuments } from "./hooks/useDocuments"
import { useRAGQuery } from "./hooks/useRAGQuery"
import { toast } from "sonner"

function App() {
  const [searchQuery, setSearchQuery] = useState("")
  
  const { 
    documents, 
    isLoading: isDocsLoading, 
    isError: isDocsError, 
    error: docsError, 
    uploadMutation, 
    deleteMutation 
  } = useDocuments()

  const {
    queryMutation,
    lastResult,
    isLoading: isQueryLoading,
    isError: isQueryError,
    error: queryError,
    clearResult
  } = useRAGQuery()
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  const filteredDocuments = useMemo(() => {
    return documents.filter(doc => 
      doc.document_name.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }, [documents, searchQuery])

  const handleQuery = async (question: string) => {
    try {
      await queryMutation.mutateAsync({ question })
      toast.success("Query successful")
    } catch (err) {
      toast.error(`Query failed: ${(err as any).message || 'Unknown error'}`)
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      try {
        const promise = uploadMutation.mutateAsync({ file })
        toast.promise(promise, {
          loading: `Uploading ${file.name}...`,
          success: `${file.name} ingested successfully`,
          error: (err) => `Upload failed: ${err.message || 'Unknown error'}`
        })
        await promise
        e.target.value = ''
      } catch (err) {
        // Handled by toast.promise
      }
    }
  }

  const handleDelete = async (name: string) => {
    if (confirm(`Are you sure you want to delete ${name}?`)) {
      try {
        const promise = deleteMutation.mutateAsync(name)
        toast.promise(promise, {
          loading: `Deleting ${name}...`,
          success: `${name} deleted successfully`,
          error: (err) => `Delete failed: ${err.message || 'Unknown error'}`
        })
        await promise
      } catch (err) {
        // Handled by toast.promise
      }
    }
  }

  return (
    <Layout 
      onQuery={handleQuery} 
      isQueryLoading={isQueryLoading}
      searchQuery={searchQuery}
      onSearchChange={setSearchQuery}
    >
      {/* Hidden File Input */}
      <input 
        type="file" 
        ref={fileInputRef} 
        className="hidden" 
        onChange={handleFileChange}
        accept=".pdf,.docx,.txt,.csv"
      />

      {/* RAG Response / Latest Synthesis Section */}
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
          isQueryError ? "border-error" : "border-primary/40"
        )}>
          {isQueryLoading ? (
            <div className="flex items-center gap-4 py-4">
              <Loader2 className="animate-spin text-primary" size={24} />
              <p className="text-sm text-on-surface-variant font-medium animate-pulse">
                The Monolith is synthesizing an answer...
              </p>
            </div>
          ) : isQueryError ? (
            <div className="flex items-center gap-3 text-error">
              <AlertCircle size={20} />
              <p className="text-sm font-medium">Query Error: {(queryError as any)?.message || "Failed to get response"}</p>
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
                  onClick={clearResult}
                  className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground hover:text-foreground h-auto p-0"
                >
                  Clear Result
                </Button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-sm text-on-surface-variant leading-relaxed font-medium">
                {uploadMutation.isPending 
                  ? "Ingesting your document into the vector space..." 
                  : "Welcome to Cognitive Monolith. Start by uploading documents or asking a question below."}
              </p>
              <div className="flex items-center gap-2">
                <Badge variant="secondary" className="bg-surface-container-highest text-[10px] font-bold tracking-wider px-3 py-1 uppercase rounded-md border-none">
                  {uploadMutation.isPending ? "UPLOADING" : "SYSTEM READY"}
                </Badge>
                <div className={cn(
                  "w-2 h-2 rounded-full",
                  uploadMutation.isPending ? "bg-tertiary animate-bounce shadow-[0_0_8px_rgba(255,183,131,0.5)]" : "bg-primary animate-pulse shadow-[0_0_8px_rgba(192,193,255,0.5)]"
                )} />
              </div>
            </div>
          )}
        </Card>
      </div>

      {/* Data Sources Section */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
               <h2 className="text-2xl lg:text-3xl font-bold tracking-tight uppercase lg:normal-case">Data Sources</h2>
               <Badge className="lg:hidden bg-transparent border-none text-muted-foreground font-bold text-xs p-0">
                {filteredDocuments.length} {filteredDocuments.length === 1 ? 'File' : 'Files'}
               </Badge>
            </div>
            <p className="text-[10px] text-muted-foreground uppercase tracking-[0.2em] mt-1 font-bold hidden lg:block">Manage knowledge base corpus</p>
          </div>
          <Button 
            onClick={handleUploadClick}
            disabled={uploadMutation.isPending}
            className="bg-primary text-primary-foreground hover:bg-primary/90 gap-2 font-bold h-12 px-6 rounded-xl shadow-lg shadow-primary/20 hidden lg:flex"
          >
            {uploadMutation.isPending ? <Loader2 className="animate-spin" size={20} /> : <Plus size={20} />}
            {uploadMutation.isPending ? "UPLOADING..." : "UPLOAD NEW"}
          </Button>
        </div>

        {isDocsError && (
          <Card className="p-4 bg-destructive/10 border-destructive/20 text-destructive flex items-center gap-3">
            <AlertCircle size={20} />
            <p className="text-sm font-medium">Error loading documents: {(docsError as any)?.message || 'Unknown error'}</p>
          </Card>
        )}

        {/* Desktop View (Table) */}
        <Card className="hidden lg:block border-none bg-surface-container-lowest overflow-hidden shadow-2xl rounded-2xl min-h-[200px]">
          {isDocsLoading ? (
            <div className="flex items-center justify-center h-48">
              <Loader2 className="animate-spin text-primary" size={32} />
            </div>
          ) : filteredDocuments.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-48 text-muted-foreground space-y-2">
              <FileText size={40} className="opacity-20" />
              <p className="font-medium italic">
                {searchQuery ? `No files matching "${searchQuery}"` : "No documents uploaded yet."}
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader className="bg-surface-container-low/50">
                <TableRow className="hover:bg-transparent border-border h-16">
                  <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] pl-8">File Name</TableHead>
                  <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">Chunks</TableHead>
                  <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">Status</TableHead>
                  <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] text-right pr-8">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredDocuments.map((file) => (
                  <TableRow key={file.document_name} className="border-border hover:bg-surface-container/30 transition-colors h-24">
                    <TableCell className="font-semibold py-4 pl-8">
                      <div className="flex items-center gap-4">
                        <div className="w-11 h-11 rounded-lg flex items-center justify-center border border-border/50 shadow-sm bg-surface-container-highest text-primary">
                          <FileText size={22} />
                        </div>
                        <span className="text-base font-bold">{file.document_name}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-muted-foreground font-bold text-sm">{file.chunk_count} units</TableCell>
                    <TableCell>
                      <Badge variant="secondary" className="bg-surface-container-highest text-foreground border-none px-4 py-1.5 font-bold text-[10px] tracking-widest rounded-full">
                        <div className="w-1.5 h-1.5 rounded-full mr-2 bg-primary" />
                        INDEXED
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right pr-8">
                      <div className="flex items-center justify-end gap-2">
                        <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground font-bold uppercase text-[10px] tracking-[0.2em] h-10 px-4">
                          <Download size={18} />
                          Download
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="text-muted-foreground hover:text-destructive h-10 w-10 transition-colors"
                          onClick={() => handleDelete(file.document_name)}
                          disabled={deleteMutation.isPending}
                        >
                          {deleteMutation.isPending && deleteMutation.variables === file.document_name 
                            ? <Loader2 className="animate-spin" size={18} />
                            : <Trash2 size={18} />
                          }
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Card>

        {/* Mobile View (List) */}
        <div className="lg:hidden space-y-3">
           {isDocsLoading ? (
             <div className="flex items-center justify-center py-10">
               <Loader2 className="animate-spin text-primary" size={24} />
             </div>
           ) : filteredDocuments.length === 0 ? (
             <p className="text-center text-muted-foreground italic text-sm py-10">
               {searchQuery ? `No files matching "${searchQuery}"` : "No documents yet."}
             </p>
           ) : filteredDocuments.map((file) => (
            <Card key={file.document_name} className="p-4 bg-surface-container-low border-none flex items-center justify-between rounded-xl">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-surface-container-lowest flex items-center justify-center text-on-surface border border-border/30">
                  <FileText size={24} />
                </div>
                <div className="space-y-1">
                  <h3 className="font-bold text-sm tracking-tight truncate max-w-[150px]">{file.document_name}</h3>
                  <div className="flex items-center gap-2">
                    <span className="text-[9px] font-bold uppercase tracking-widest text-primary">INDEXED</span>
                    <span className="text-[9px] text-muted-foreground font-bold uppercase tracking-widest">• {file.chunk_count} Chunks</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="bg-surface-container-highest/50 h-10 w-10 rounded-xl"
                  onClick={() => handleDelete(file.document_name)}
                >
                  <Trash2 size={18} className="text-muted-foreground" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Placeholder / Secondary Section */}
      <section className="space-y-4 pt-10 pb-20">
        <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">Contextual Insights</p>
        <Card className="p-8 bg-surface-container-lowest border-none shadow-inner rounded-3xl text-center">
          <Sparkles className="text-muted-foreground/20 mx-auto mb-4" size={40} />
          <p className="text-muted-foreground text-sm font-medium">
            Ask the Monolith about your data to generate deep insights.
          </p>
        </Card>
      </section>
    </Layout>
  )
}

export default App
