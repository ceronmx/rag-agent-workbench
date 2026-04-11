import { useRef } from "react"
import { Plus, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useDocuments } from "@/hooks/useDocuments"
import { toast } from "sonner"

export function DocumentUpload() {
  const { uploadMutation } = useDocuments()
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleButtonClick = () => {
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

  return (
    <>
      <input 
        type="file" 
        ref={fileInputRef} 
        className="hidden" 
        onChange={handleFileChange}
        accept=".pdf,.docx,.txt,.csv"
      />
      <Button 
        onClick={handleButtonClick}
        disabled={uploadMutation.isPending}
        className="bg-primary text-primary-foreground hover:bg-primary/90 gap-2 font-bold h-12 px-6 rounded-xl shadow-lg shadow-primary/20 hidden lg:flex"
      >
        {uploadMutation.isPending ? <Loader2 className="animate-spin" size={20} /> : <Plus size={20} />}
        {uploadMutation.isPending ? "UPLOADING..." : "UPLOAD NEW"}
      </Button>
    </>
  )
}
