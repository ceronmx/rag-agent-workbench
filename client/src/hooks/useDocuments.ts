import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api-client";

export function useDocuments() {
  const queryClient = useQueryClient();

  const {
    data: documents = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["documents"],
    queryFn: api.listDocuments,
  });

  const uploadMutation = useMutation({
    mutationFn: (args: { file: File; documentName?: string }) =>
      api.ingestFile(args.file, args.documentName),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: api.deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });

  return {
    documents,
    isLoading,
    isError,
    error,
    refetch,
    uploadMutation,
    deleteMutation,
  };
}
