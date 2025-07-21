/**
 * TypeScript types for the ECSS Foundation System API
 * These types match the backend foundation system responses
 */

// Search result from working backend with both AI and document content
export interface SearchResult {
  id: string;
  title: string;
  content: string;
  score: number;
  source: string;
  metadata?: {
    method?: string;
    processing_time?: number;
    is_visual?: boolean;
    image_url?: string;
    document_name?: string;
  };
}

// Enhanced search response with AI and document results separated
export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total: number;
  ai_response?: string; // AI contextual response
  document_sources?: string[]; // Source documents for the AI response
  processing_time: number;
  methods_used: string[];
}

// Visual search result from ColPali processing
export interface VisualResult {
  id: string;
  image_url: string;
  description: string;
  confidence: number;
  source: string;
}

// Visual search response
export interface VisualSearchResponse {
  query: string;
  results: VisualResult[];
  total: number;
  processing_time: number;
}

// Document information
export interface DocumentInfo {
  id: string;
  filename: string;
  status: string;
  is_processing: boolean;
  is_failed: boolean;
  content_type: string;
  metadata: Record<string, any>;
}

// Document chunk information
export interface ChunkInfo {
  chunk_number: number;
  document_id: string;
  filename: string;
  is_visual: boolean;
  content_type: 'image' | 'text';
  score: number;
  image_size?: [number, number];
  image_mode?: string;
  content_preview: string;
}

// Documents list response
export interface DocumentsResponse {
  documents: DocumentInfo[];
  total_documents: number;
  timestamp: string;
}

// Document chunks response
export interface DocumentChunksResponse {
  document_id: string;
  chunks: ChunkInfo[];
  total_chunks: number;
  visual_chunks: number;
  text_chunks: number;
  timestamp: string;
}

// System status response - Updated for working backend
export interface SystemStatusResponse {
  connection: string;
  features: {
    agent_query: boolean;
    batch_operations: boolean;
    colpali_visual: boolean;
    document_access: boolean;
    knowledge_graphs: boolean;
    standard_query: boolean;
  };
  system: string;
  timestamp: number;
}

// System statistics response
export interface SystemStatsResponse {
  system_status: any;
  documents: {
    total: number;
    processing: number;
    failed: number;
    completed: number;
  };
  chunks: {
    total: number;
    visual: number;
    text: number;
    visual_percentage: number;
  };
  api_metrics: {
    request_count: number;
    error_count: number;
    error_rate: number;
  };
  timestamp: string;
}

// Ingestion result
export interface IngestionResult {
  document_id: string;
  filename: string;
  status: string;
  processing_time: number;
  visual_chunks: number;
  text_chunks: number;
  cost_estimate: number;
  error_message?: string;
}

// Batch ingestion request
export interface BatchIngestionRequest {
  documents_path?: string;
  max_documents?: number;
  max_workers?: number;
  use_colpali?: boolean;
  cost_limit_total?: number;
  skip_existing?: boolean;
  output_report?: boolean;
}

// Batch ingestion response
export interface BatchIngestionResponse {
  status: string;
  stats: {
    total_documents: number;
    processed_documents: number;
    successful_ingestions: number;
    failed_ingestions: number;
    skipped_documents: number;
    total_visual_chunks: number;
    total_text_chunks: number;
    total_processing_time: number;
    estimated_cost: number;
    start_time: string;
    end_time: string;
  };
  summary: {
    total_documents: number;
    processed: number;
    successful: number;
    failed: number;
    visual_chunks: number;
    text_chunks: number;
    processing_time: number;
    estimated_cost: number;
    success_rate: number;
  };
  timestamp: string;
}

// Error response
export interface ErrorResponse {
  error: string;
  message?: string;
  timestamp: string;
}

// API configuration
export interface ApiConfig {
  baseUrl: string;
  timeout: number;
  headers: Record<string, string>;
}

// Search filters
export interface SearchFilters {
  query: string;
  limit: number;
  include_visual: boolean;
  min_score?: number;
}

// Visual search filters
export interface VisualSearchFilters {
  query: string;
  limit: number;
}

// UI state types
export interface SearchState {
  isLoading: boolean;
  query: string;
  results: SearchResult[];
  visualResults: SearchResult[];
  contextualResponse?: string;
  error?: string;
  totalResults: number;
  processingTime: number;
}

export interface SystemState {
  isLoading: boolean;
  status?: SystemStatusResponse;
  stats?: SystemStatsResponse;
  error?: string;
}

// Component prop types
export interface SearchFormProps {
  onSearch: (query: string, filters: SearchFilters) => void;
  isLoading: boolean;
  initialQuery?: string;
}

export interface SearchResultsProps {
  results: SearchResult[];
  isLoading: boolean;
  error?: string;
  totalResults: number;
  processingTime: number;
  contextualResponse?: string;
}

export interface VisualContentProps {
  visualResults: SearchResult[];
  isLoading: boolean;
  error?: string;
}

export interface SystemInfoProps {
  status?: SystemStatusResponse;
  stats?: SystemStatsResponse;
  isLoading: boolean;
  error?: string;
} 