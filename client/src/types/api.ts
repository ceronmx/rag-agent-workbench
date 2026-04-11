export interface DocumentInfo {
  document_name: string;
  chunk_count: number;
  file_type: string;
  // UI-specific properties
  size?: string;
  upload_date?: string;
  status?: "INDEXED" | "PENDING" | "ERROR";
}

export interface ContextChunk {
  text: string;
  document_name: string;
  chunk_index: number;
  score?: number;
  file_type?: string;
}

export interface QueryResponse {
  answer: string;
  search_query: string;
  search_mode: string;
  contexts: ContextChunk[];
  is_stream: boolean;
}

export interface QueryRequest {
  question: string;
  search_mode?: "vector" | "keyword" | "hybrid";
  use_rescoring?: boolean;
  use_stream?: boolean;
  top_k?: number;
  filters?: Record<string, any>;
}

export interface TextIngestRequest {
  text: string;
  document_name: string;
  chunk_size?: number;
  overlap?: number;
  metadata?: Record<string, any>;
}

export interface IngestResponse {
  status: string;
  message: string;
  document_name: string;
  chunk_count: number;
}
