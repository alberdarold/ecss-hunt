/**
 * API utility functions for the ECSS Foundation System
 * Updated to work with the Production Working API on Render
 */

import {
  SearchResponse,
  VisualSearchResponse,
  DocumentsResponse,
  DocumentChunksResponse,
  SystemStatusResponse,
  SystemStatsResponse,
  IngestionResult,
  BatchIngestionResponse,
  ErrorResponse,
  SearchFilters,
  VisualSearchFilters,
  BatchIngestionRequest,
} from '../types/api';

// Get API base URL from environment - points to our Render backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ecss-hunt.onrender.com';

// API configuration for Production Working API
const API_CONFIG = {
  baseUrl: API_BASE_URL,
  timeout: 30000, // 30 seconds for comprehensive searches
  headers: {
    'Content-Type': 'application/json',
  },
};

// Custom fetch wrapper with error handling
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_CONFIG.baseUrl}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...API_CONFIG.headers,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData: ErrorResponse = await response.json().catch(() => ({
      error: 'Network error',
      message: `HTTP ${response.status}: ${response.statusText}`,
      timestamp: new Date().toISOString(),
    }));
    
    throw new Error(errorData.message || errorData.error);
  }

  return response.json();
}

// Search API functions - Updated for Production Working API
export const searchAPI = {
  /**
   * Enhanced search with visual content support
   * Uses the working backend's unified search endpoint
   */
  async search(filters: SearchFilters): Promise<SearchResponse> {
    const params = new URLSearchParams({
      q: filters.query,
      k: filters.limit.toString(),
    });

    // Our working backend includes both text and visual search in one endpoint
    const rawResponse = await apiFetch<any>(`/api/working/search?${params}`);
    
    // Transform the response to match frontend expectations
    return transformSearchResponse(rawResponse);
  },

  /**
   * Visual search - uses the same endpoint as regular search
   * Our working backend combines both text and visual search
   */
  async searchVisual(filters: VisualSearchFilters): Promise<VisualSearchResponse> {
    const params = new URLSearchParams({
      q: filters.query,
      k: filters.limit.toString(),
    });

    // Use the unified search endpoint (includes visual via ColPali)
    const rawResponse = await apiFetch<any>(`/api/working/search?${params}`);
    return transformVisualSearchResponse(rawResponse);
  },
};

// Document management API functions - LIMITED AVAILABILITY in working backend
export const documentsAPI = {
  /**
   * Get list of all ingested documents - NOT AVAILABLE in working backend
   */
  async getDocuments(): Promise<DocumentsResponse> {
    throw new Error("Document listing not available in working backend. Use search functionality instead.");
  },

  /**
   * Get chunks for a specific document - NOT AVAILABLE in working backend
   */
  async getDocumentChunks(documentId: string, limit: number = 20): Promise<DocumentChunksResponse> {
    throw new Error("Document chunks not available in working backend. Use search functionality instead.");
  },
};

// Ingestion API functions - NOT AVAILABLE in working backend
export const ingestionAPI = {
  /**
   * Ingest a single document - NOT AVAILABLE in working backend
   */
  async ingestDocument(filePath: string): Promise<IngestionResult> {
    throw new Error("Document ingestion not available in working backend");
  },

  /**
   * Batch ingest documents - NOT AVAILABLE in working backend
   */
  async batchIngest(request: BatchIngestionRequest): Promise<BatchIngestionResponse> {
    throw new Error("Batch ingestion not available in working backend");
  },
};

// System monitoring API functions - Updated for working backend
export const systemAPI = {
  /**
   * Health check - Uses standard /api/health endpoint
   */
  async getHealth(): Promise<{ status: string; timestamp: string }> {
    return apiFetch<{ status: string; timestamp: string }>('/api/health');
  },

  /**
   * System status - Uses /api/working/status endpoint
   */
  async getStatus(): Promise<SystemStatusResponse> {
    return apiFetch<SystemStatusResponse>('/api/working/status');
  },

  /**
   * System capabilities - Available in working backend
   */
  async getCapabilities(): Promise<any> {
    return apiFetch<any>('/api/working/capabilities');
  },

  /**
   * System stats - NOT AVAILABLE in working backend
   */
  async getStats(): Promise<SystemStatsResponse> {
    throw new Error("Detailed system statistics not available in working backend. Use status endpoint instead.");
  },
};

// Transform backend response to frontend format
function transformSearchResponse(rawResponse: any): SearchResponse {
  // Handle new foundation system response format
  if (rawResponse.results && rawResponse.results.length > 0 && rawResponse.results[0].content && rawResponse.results[0].summary) {
    // New foundation system format - use directly
    return {
      query: rawResponse.query || '',
      results: rawResponse.results || [],
      total_results: rawResponse.total_results || rawResponse.total || 0,
      visual_results: rawResponse.visual_results || 0,
      text_results: rawResponse.text_results || 0,
      contextual_response: rawResponse.contextual_response || undefined,
      processing_time: rawResponse.processing_time || 0,
      timestamp: rawResponse.timestamp || new Date().toISOString(),
    };
  }
  
  // Legacy format transformation for old backend
  const results = rawResponse.results?.map((item: any) => ({
    content: item.content || 'No content available',
    summary: item.metadata?.document_name || 'No summary available',
    relevance_score: item.score || item.metadata?.score || 0,
    document_info: {
      filename: item.metadata?.document_name || 'Unknown document',
      chunk_number: item.metadata?.chunk_id || 0,
      document_id: item.metadata?.external_id || item.id || 'unknown',
    },
    source_type: item.metadata?.source_type || 'Information',
    explanation: item.metadata?.explanation || 'No explanation available',
    visual_elements: item.metadata?.visual_elements || 0,
    is_visual_content: item.metadata?.is_visual_content || false,
  })) || [];

  return {
    query: rawResponse.query || '',
    results,
    total_results: rawResponse.total || 0,
    visual_results: results.filter((r: any) => r.is_visual_content).length,
    text_results: results.filter((r: any) => !r.is_visual_content).length,
    contextual_response: rawResponse.summary || undefined,
    processing_time: rawResponse.processing_time || 0,
    timestamp: rawResponse.timestamp || new Date().toISOString(),
  };
}

// Transform backend response to visual search format
function transformVisualSearchResponse(rawResponse: any): VisualSearchResponse {
  const results = rawResponse.results?.map((item: any) => ({
    content: item.content || 'No content available',
    summary: item.metadata?.document_name || 'No summary available',
    relevance_score: item.score || item.metadata?.score || 0,
    document_info: {
      filename: item.metadata?.document_name || 'Unknown document',
      chunk_number: item.metadata?.chunk_id || 0,
      document_id: item.metadata?.external_id || item.id || 'unknown',
    },
    source_type: item.metadata?.source_type || 'Information',
    explanation: item.metadata?.explanation || 'No explanation available',
    visual_elements: item.metadata?.visual_elements || 0,
    is_visual_content: item.metadata?.is_visual_content || false,
  })) || [];

  return {
    query: rawResponse.query || '',
    visual_results: results,
    total_visual_results: rawResponse.total || 0,
    processing_time: rawResponse.processing_time || 0,
    timestamp: rawResponse.timestamp || new Date().toISOString(),
  };
}

// Utility functions
export const apiUtils = {
  /**
   * Check if API is available
   */
  async isApiAvailable(): Promise<boolean> {
    try {
      await systemAPI.getHealth();
      return true;
    } catch (error) {
      console.warn('API not available:', error);
      return false;
    }
  },

  /**
   * Get API base URL
   */
  getBaseUrl(): string {
    return API_CONFIG.baseUrl;
  },

  /**
   * Format processing time for display
   */
  formatProcessingTime(seconds: number | undefined): string {
    if (seconds === undefined || seconds === null) {
      return 'N/A';
    }
    if (seconds < 1) {
      return `${(seconds * 1000).toFixed(0)}ms`;
    }
    return `${seconds.toFixed(2)}s`;
  },

  /**
   * Format file size for display
   */
  formatFileSize(bytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }

    return `${size.toFixed(1)} ${units[unitIndex]}`;
  },

  /**
   * Format timestamp for display
   */
  formatTimestamp(timestamp: string): string {
    return new Date(timestamp).toLocaleString();
  },

  /**
   * Get source type color for UI
   */
  getSourceTypeColor(sourceType: string): string {
    const colors: Record<string, string> = {
      'Requirement': 'bg-red-100 text-red-800',
      'Definition': 'bg-blue-100 text-blue-800',
      'Procedure': 'bg-green-100 text-green-800',
      'Reference': 'bg-yellow-100 text-yellow-800',
      'Information': 'bg-gray-100 text-gray-800',
      'Visual Content': 'bg-purple-100 text-purple-800',
    };

    return colors[sourceType] || 'bg-gray-100 text-gray-800';
  },

  /**
   * Get relevance score color for UI
   */
  getRelevanceScoreColor(score: number | undefined): string {
    if (score === undefined || score === null) return 'text-gray-500';
    if (score >= 9) return 'text-green-600';
    if (score >= 7) return 'text-yellow-600';
    if (score >= 5) return 'text-orange-600';
    return 'text-red-600';
  },

  /**
   * Truncate text with ellipsis
   */
  truncateText(text: string, maxLength: number): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  },

  /**
   * Highlight search terms in text
   */
  highlightSearchTerms(text: string, searchTerms: string[]): string {
    let highlightedText = text;
    
    searchTerms.forEach(term => {
      if (term.length > 2) {
        const regex = new RegExp(`(${term})`, 'gi');
        highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
      }
    });

    return highlightedText;
  },

  /**
   * Extract document name from filename
   */
  extractDocumentName(filename: string): string {
    return filename.replace(/\.[^/.]+$/, ''); // Remove file extension
  },

  /**
   * Calculate visual content percentage
   */
  calculateVisualPercentage(visualResults: number, totalResults: number): number {
    if (totalResults === 0) return 0;
    return Math.round((visualResults / totalResults) * 100);
  },
};

// Error handling utilities
export const errorUtils = {
  /**
   * Check if error is network-related
   */
  isNetworkError(error: any): boolean {
    return error.message?.includes('fetch') || 
           error.message?.includes('network') ||
           error.message?.includes('connection');
  },

  /**
   * Get user-friendly error message
   */
  getUserFriendlyMessage(error: any): string {
    if (this.isNetworkError(error)) {
      return 'Unable to connect to the server. Please check your internet connection and try again.';
    }

    if (error.message?.includes('timeout')) {
      return 'The request timed out. Please try again.';
    }

    if (error.message?.includes('404')) {
      return 'The requested resource was not found.';
    }

    if (error.message?.includes('500')) {
      return 'A server error occurred. Please try again later.';
    }

    return error.message || 'An unexpected error occurred. Please try again.';
  },
};

// All API functions are already exported above 