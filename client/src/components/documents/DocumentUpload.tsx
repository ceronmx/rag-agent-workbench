import { useRef } from "react"
import { Plus, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"

interface DocumentUploadProps {
  onUpload: (file: File) => void
  isUploading: boolean
}

export function DocumentUpload({ onUpload, isUploading }: DocumentUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleButtonClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      onUpload(file)
      // Reset input so the same file can be selected again
      e.target.value = ""
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
        disabled={isUploading}
        className="bg-primary text-primary-foreground hover:bg-primary/90 gap-2 font-bold h-12 px-6 rounded-xl shadow-lg shadow-primary/20 hidden lg:flex"
      >
        {isUploading ? <Loader2 className="animate-spin" size={20} /> : <Plus size={20} />}
        {isUploading ? "UPLOADING..." : "UPLOAD NEW"}
      </Button>
    </>
  )
}
