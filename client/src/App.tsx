import { useState, useMemo } from "react"
import { Badge } from "@/components/ui/badge"
import { AlertCircle } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Layout } from "./components/layout/Layout"
import { useDocuments } from "./hooks/useDocuments"
import { useRAGQuery } from "./hooks/useRAGQuery"
import { toast } from "sonner"

// Modular Components
import { DocumentList } from "./components/documents/DocumentList"
import { DocumentUpload } from "./components/documents/DocumentUpload"
import { SynthesisResult } from "./components/chat/results/SynthesisResult"
import { ContextualInsights } from "./components/chat/results/ContextualInsights"

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

  const handleUpload = async (file: File) => {
    try {
      const promise = uploadMutation.mutateAsync({ file })
      toast.promise(promise, {
        loading: `Uploading ${file.name}...`,
        success: `${file.name} ingested successfully`,
        error: (err) => `Upload failed: ${err.message || 'Unknown error'}`
      })
      await promise
    } catch (err) {
      // Handled by toast.promise
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
      <SynthesisResult 
        lastResult={lastResult}
        isLoading={isQueryLoading}
        isError={isQueryError}
        error={queryError}
        onClear={clearResult}
        isUploading={uploadMutation.isPending}
      />

      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl lg:text-3xl font-bold tracking-tight uppercase lg:normal-case text-foreground">
              Data Sources
            </h2>
            <Badge className="bg-transparent border-none text-muted-foreground font-bold text-xs p-0">
              {filteredDocuments.length} {filteredDocuments.length === 1 ? 'File' : 'Files'}
            </Badge>
          </div>
          <DocumentUpload 
            onUpload={handleUpload} 
            isUploading={uploadMutation.isPending} 
          />
        </div>

        {isDocsError && (
          <Card className="p-4 bg-destructive/10 border-destructive/20 text-destructive flex items-center gap-3">
            <AlertCircle size={20} />
            <p className="text-sm font-medium">Error loading documents: {(docsError as any)?.message || 'Unknown error'}</p>
          </Card>
        )}

        <DocumentList 
          documents={filteredDocuments}
          isLoading={isDocsLoading}
          onDelete={handleDelete}
          isDeleting={deleteMutation.isPending}
          deletingName={deleteMutation.variables}
          searchQuery={searchQuery}
        />
      </section>

      <ContextualInsights />
    </Layout>
  )
}

export default App
