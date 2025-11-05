/**
 * API utility functions for the ECSS Foundation System
 * Updated to work with the Production Working API on Render
 */

import {
  SearchResponse,
  SearchResult,
  VisualSearchResponse,
  VisualResult,
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

// Configuration - Always use Render backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://ecss-hunt.onrender.com';
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION !== undefined ? process.env.NEXT_PUBLIC_API_VERSION : 'working';

// Lightweight in-memory cache and request controller for client-side perf
const responseCache = new Map<string, { ts: number; data: any }>();
const CACHE_TTL_MS = 60_000; // 60s
let inflightControllers = new Map<string, AbortController>();

function normalizeKey(s: string): string {
  return s.toLowerCase().replace(/\s+/g, ' ').trim();
}

// Helper function for API calls with better error handling
async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const versionPath = API_VERSION ? `${API_VERSION}/` : '';
  const url = `${API_BASE_URL}/api/${versionPath}${endpoint.startsWith('/') ? endpoint.slice(1) : endpoint}`;
  const cacheKey = normalizeKey(url);
  
  // Debug logging (remove in production)
  if (process.env.NODE_ENV === 'development') {
    console.log(`[API] Fetching: ${url}`, { API_BASE_URL, API_VERSION, endpoint });
  }
  
  // Serve from cache if fresh
  const cached = responseCache.get(cacheKey);
  const now = Date.now();
  if (cached && now - cached.ts < CACHE_TTL_MS) {
    return cached.data as T;
  }
  
  // Cancel any duplicate in-flight request
  const existing = inflightControllers.get(cacheKey);
  if (existing) {
    existing.abort();
    inflightControllers.delete(cacheKey);
  }
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  const controller = new AbortController();
  inflightControllers.set(cacheKey, controller);

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    signal: controller.signal,
    credentials: 'include', // Important for session cookies
    // Hint intermediate caches; safe for GET
    cache: 'no-store',
  };

  try {
    const response = await fetch(url, config);
    
    // Handle network errors or non-OK responses
    if (!response.ok) {
      let data;
      try {
        data = await response.json();
      } catch (e) {
        // If JSON parsing fails, create a generic error
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      // Handle specific error cases
      if (response.status === 400 && data.error === 'insufficient_credits') {
        const error: any = new Error(data.message || 'Insufficient credits');
        error.status = 400;
        error.error = 'insufficient_credits';
        error.current_balance = data.current_balance;
        error.required = data.required;
        error.shortfall = data.shortfall;
        throw error;
      } else if (response.status === 401) {
        const error: any = new Error(data.message || 'Unauthorized');
        error.status = 401;
        error.error = 'unauthorized';
        throw error;
      } else {
        throw new Error(data.message || `HTTP ${response.status}: ${response.statusText}`);
      }
    }
    
    // Parse JSON response
    let data;
    try {
      data = await response.json();
    } catch (e) {
      throw new Error(`Invalid JSON response from server`);
    }
    
    // Populate cache on success
    responseCache.set(cacheKey, { ts: Date.now(), data });
    return data;
  } catch (error: any) {
    // If aborted due to new duplicate request, surface a clean error
    if (error?.name === 'AbortError') {
      throw new Error('Request aborted');
    }
    // Re-throw if it's already our custom error
    if (error?.error === 'insufficient_credits' || error?.error === 'unauthorized') {
      throw error;
    }
    
    // Handle network errors (connection refused, CORS, etc.)
    if (error?.message?.includes('fetch') || error?.message?.includes('Failed to fetch') || error?.name === 'TypeError') {
      const errorMessage = `Unable to connect to backend API at ${API_BASE_URL}. Make sure the backend server is running.`;
      console.error(`API call failed for ${endpoint} (${url}):`, errorMessage, error);
      const networkError: any = new Error(errorMessage);
      networkError.isNetworkError = true;
      networkError.originalError = error;
      throw networkError;
    }
    
    console.error(`API call failed for ${endpoint} (${url}):`, error);
    throw error;
  } finally {
    inflightControllers.delete(cacheKey);
  }
}

// Transform function for search results with new backend format
function transformSearchResponse(rawResponse: any): SearchResponse {
  if (!rawResponse.results) {
    return {
      query: rawResponse.query || '',
      results: [],
      total: 0,
      ai_response: '',
      processing_time: rawResponse.processing_time || 0,
      methods_used: rawResponse.methods_used || [],
      credits_remaining: rawResponse.credits_remaining,
      credits_used: rawResponse.credits_used,
    };
  }

  // New backend format has ai_response separate from results
  const aiResponse = rawResponse.ai_response || '';
  
  // Transform individual document results
  const documentResults: SearchResult[] = rawResponse.results.map((result: any, index: number) => {
    let content = result.content || '';
    let isVisual = false;
    let imageUrl = '';

    // Handle visual content if present
    if (result.metadata?.is_visual || content.startsWith('data:image/')) {
      isVisual = true;
      if (content.startsWith('data:image/')) {
        imageUrl = content;
        content = `[Visual Content] Diagram or table from ${result.metadata?.document_name || 'ECSS Document'}`;
      }
    }

    return {
      id: result.id || `result_${index}`,
      title: result.title || `ECSS Document Section ${index + 1}`,
      content: content,
      score: result.score || 0,
      source: result.source || result.metadata?.document_name || 'ECSS Document',
      metadata: {
        method: result.metadata?.method || 'text_extraction',
        processing_time: rawResponse.processing_time || 0,
        is_visual: isVisual,
        image_url: imageUrl,
        document_name: result.metadata?.document_name || result.source,
      }
    };
  });

  return {
    query: rawResponse.query || '',
    results: documentResults,
    total: rawResponse.total || documentResults.length,
    ai_response: cleanAIResponse(aiResponse),
    document_sources: rawResponse.document_sources || [],
    processing_time: rawResponse.processing_time || 0,
    methods_used: rawResponse.methods_used || [],
    credits_remaining: rawResponse.credits_remaining,
    credits_used: rawResponse.credits_used,
  };
}

// Helper function to extract document name from title
function extractDocumentName(title: string): string {
  if (!title) return 'Unknown Document';
  
  // Extract ECSS document ID from title like "Source: ECSS-E-ST-50-51C(5February2010).pdf"
  const match = title.match(/ECSS-[A-Z]-[A-Z]{2}-[\d-]+[A-Z]?\([^)]+\)\.pdf/);
  if (match) {
    return match[0];
  }
  
  return title;
}

// Helper function to clean and format AI response
function cleanAIResponse(response: string): string {
  if (!response) return '';
  
  // Remove any remaining # symbols (safety check)
  let cleaned = response.replace(/#/g, '');
  
  // Convert markdown formatting to HTML with better spacing
  cleaned = cleaned
    // Convert bold markdown to HTML
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Convert bullet points to HTML lists
    .replace(/^[\s]*[-*]\s+(.+)$/gm, '<li>$1</li>')
    // Convert numbered lists
    .replace(/^[\s]*\d+\.\s+(.+)$/gm, '<li>$1</li>')
    // Convert line breaks with better paragraph spacing
    .replace(/\n\n\n/g, '</p><p>')  // Triple line breaks for section breaks
    .replace(/\n\n/g, '</p><p>')    // Double line breaks for paragraphs
    .replace(/\n/g, '<br>');        // Single line breaks within paragraphs
  
  // Wrap in paragraphs
  if (cleaned && !cleaned.startsWith('<')) {
    cleaned = '<p>' + cleaned + '</p>';
  }
  
  // Wrap list items in ul tags
  cleaned = cleaned.replace(/(<li>.*?<\/li>)/g, '<ul>$1</ul>');
  
  return cleaned;
}

// Transform function for visual search results
function transformVisualSearchResponse(rawResponse: any): VisualSearchResponse {
  const visualResults: VisualResult[] = rawResponse.results?.filter((result: any) => 
    result.source_type === 'visual' || result.method === 'colpali'
  ).map((result: any) => ({
    id: `visual_${Date.now()}_${Math.random()}`,
    image_url: result.content?.startsWith('data:image') ? result.content : '',
    description: result.title || 'Visual Content',
    confidence: result.relevance_score || 0,
    source: result.title || 'Unknown Document',
  })) || [];

  return {
    query: rawResponse.query || '',
    results: visualResults,
    total: visualResults.length,
    processing_time: rawResponse.processing_time || 0,
  };
}

// Search API functions - Updated for Working Backend with Document Access
export const searchAPI = {
  /**
   * Enhanced search with real ECSS document content + AI responses
   */
  async search(filters: SearchFilters): Promise<SearchResponse> {
    const params = new URLSearchParams({
      q: filters.query.trim(),
      limit: filters.limit?.toString() || '8',
    });

    try {
      const response = await apiFetch<any>(`/search?${params}`);
      return transformSearchResponse(response);
    } catch (error: any) {
      // Re-throw with error details preserved
      if (error.error === 'insufficient_credits' || error.status === 401) {
        throw error;
      }
      throw error;
    }
  },

  /**
   * Visual search using ColPali - returns diagrams, tables, figures
   */
  async searchVisual(filters: VisualSearchFilters): Promise<VisualSearchResponse> {
    const params = new URLSearchParams({
      q: filters.query,
      k: filters.limit.toString(),
    });

    // Use the working backend with ColPali visual processing
    const rawResponse = await apiFetch<any>(`/search?${params}`);
    return transformVisualSearchResponse(rawResponse);
  },
};

// System monitoring API functions - Updated for working backend
export const systemAPI = {
  /**
   * System status - Uses working backend status endpoint
   */
  async getStatus(): Promise<SystemStatusResponse> {
    return apiFetch<SystemStatusResponse>('/status');
  },

  /**
   * System capabilities - Available in working backend
   */
  async getCapabilities(): Promise<any> {
    return apiFetch<any>('/capabilities');
  },

  /**
   * Health check
   */
  async getHealth(): Promise<{ status: string; timestamp: string }> {
    // Use the health endpoint without version prefix for basic health
    const url = `${API_BASE_URL}/api/health`;
    const response = await fetch(url);
    return response.json();
  },
};

// Document and ingestion APIs - Not available in working backend, provide fallbacks
export const documentsAPI = {
  async getDocuments(): Promise<DocumentsResponse> {
    throw new Error("Document listing not available in working backend. Use search functionality instead.");
  },

  async getDocumentChunks(documentId: string, limit: number = 20): Promise<DocumentChunksResponse> {
    throw new Error("Document chunks not available in working backend. Use search functionality instead.");
  },
};

export const ingestionAPI = {
  async ingestDocument(filePath: string): Promise<IngestionResult> {
    throw new Error("Document ingestion not available in working backend");
  },

  async batchIngest(request: BatchIngestionRequest): Promise<BatchIngestionResponse> {
    throw new Error("Batch ingestion not available in working backend");
  },
};

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
    return API_BASE_URL;
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