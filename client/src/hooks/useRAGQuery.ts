import { useMutation } from '@tanstack/react-query';
import { api } from '../lib/api-client';
import { QueryRequest, QueryResponse } from '../types/api';
import { useState } from 'react';

export function useRAGQuery() {
  const [lastResult, setLastResult] = useState<QueryResponse | null>(null);

  const queryMutation = useMutation({
    mutationFn: (request: QueryRequest) => api.query(request),
    onSuccess: (data) => {
      setLastResult(data);
    },
  });

  const clearResult = () => setLastResult(null);

  return {
    queryMutation,
    lastResult,
    clearResult,
    isLoading: queryMutation.isPending,
    isError: queryMutation.isError,
    error: queryMutation.error,
  };
}
