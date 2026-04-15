import { Download, FileText, Loader2, Trash2 } from "lucide-react";
import { useMemo } from "react";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useDocuments } from "@/hooks/useDocuments";

interface DocumentListProps {
  searchQuery: string;
}

export function DocumentList({ searchQuery }: DocumentListProps) {
  const { documents, isLoading, deleteMutation } = useDocuments();

  const filteredDocuments = useMemo(() => {
    return documents.filter((doc) =>
      doc.document_name.toLowerCase().includes(searchQuery.toLowerCase()),
    );
  }, [documents, searchQuery]);

  const handleDelete = async (name: string) => {
    if (confirm(`Are you sure you want to delete ${name}?`)) {
      try {
        const promise = deleteMutation.mutateAsync(name);
        toast.promise(promise, {
          loading: `Deleting ${name}...`,
          success: `${name} deleted successfully`,
          error: (err) => `Delete failed: ${err.message || "Unknown error"}`,
        });
        await promise;
      } catch (_err) {
        // Handled by toast.promise
      }
    }
  };

  if (isLoading) {
    return (
      <Card className="border-none bg-surface-lowest overflow-hidden shadow-2xl rounded-2xl min-h-[200px] flex items-center justify-center">
        <Loader2 className="animate-spin text-primary" size={32} />
      </Card>
    );
  }

  if (filteredDocuments.length === 0) {
    return (
      <Card className="border-none bg-surface-lowest overflow-hidden shadow-2xl rounded-2xl min-h-[200px] flex flex-col items-center justify-center text-muted-foreground space-y-2">
        <FileText size={40} className="opacity-20" />
        <p className="font-medium italic">
          {searchQuery ? `No files matching "${searchQuery}"` : "No documents uploaded yet."}
        </p>
      </Card>
    );
  }

  return (
    <>
      {/* Desktop View (Table) */}
      <Card className="hidden lg:block border-none bg-surface-lowest overflow-hidden shadow-2xl rounded-2xl">
        <Table>
          <TableHeader className="bg-surface-low/50">
            <TableRow className="hover:bg-transparent border-border h-16">
              <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] pl-8">
                File Name
              </TableHead>
              <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">
                Chunks
              </TableHead>
              <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em]">
                Status
              </TableHead>
              <TableHead className="text-muted-foreground font-bold uppercase text-[10px] tracking-[0.2em] text-right pr-8">
                Actions
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredDocuments.map((file) => (
              <TableRow
                key={file.document_name}
                className="border-border hover:bg-surface-mid/30 transition-colors h-24"
              >
                <TableCell className="font-semibold py-4 pl-8">
                  <div className="flex items-center gap-4">
                    <div className="w-11 h-11 rounded-lg flex items-center justify-center border border-border/50 shadow-sm bg-surface-highest text-primary">
                      <FileText size={22} />
                    </div>
                    <span className="text-base font-bold">{file.document_name}</span>
                  </div>
                </TableCell>
                <TableCell className="text-muted-foreground font-bold text-sm">
                  {file.chunk_count} units
                </TableCell>
                <TableCell>
                  <Badge
                    variant="secondary"
                    className="bg-surface-highest text-foreground border-none px-4 py-1.5 font-bold text-[10px] tracking-widest rounded-full"
                  >
                    <div className="w-1.5 h-1.5 rounded-full mr-2 bg-primary" />
                    INDEXED
                  </Badge>
                </TableCell>
                <TableCell className="text-right pr-8">
                  <div className="flex items-center justify-end gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="gap-2 text-muted-foreground hover:text-foreground font-bold uppercase text-[10px] tracking-[0.2em] h-10 px-4"
                    >
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
                      {deleteMutation.isPending &&
                      deleteMutation.variables === file.document_name ? (
                        <Loader2 className="animate-spin" size={18} />
                      ) : (
                        <Trash2 size={18} />
                      )}
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Mobile View (List) */}
      <div className="lg:hidden space-y-3">
        {filteredDocuments.map((file) => (
          <Card
            key={file.document_name}
            className="p-4 bg-surface-low border-none flex items-center justify-between rounded-xl"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-surface-lowest flex items-center justify-center text-on-surface border border-border/30">
                <FileText size={24} />
              </div>
              <div className="space-y-1">
                <h3 className="font-bold text-sm tracking-tight truncate max-w-[150px]">
                  {file.document_name}
                </h3>
                <div className="flex items-center gap-2">
                  <span className="text-[9px] font-bold uppercase tracking-widest text-primary">
                    INDEXED
                  </span>
                  <span className="text-[9px] text-muted-foreground font-bold uppercase tracking-widest">
                    • {file.chunk_count} Chunks
                  </span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="bg-surface-highest/50 h-10 w-10 rounded-xl"
                onClick={() => handleDelete(file.document_name)}
                disabled={deleteMutation.isPending}
              >
                {deleteMutation.isPending && deleteMutation.variables === file.document_name ? (
                  <Loader2 className="animate-spin" size={18} />
                ) : (
                  <Trash2 size={18} className="text-muted-foreground" />
                )}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </>
  );
}
