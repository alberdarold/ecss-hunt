'use client';

import { useState, useEffect } from 'react';
import { searchAPI, systemAPI } from '../utils/api';
import { SearchResult, SearchFilters, SystemStatusResponse, SearchResponse } from '../types/api';

export default function ECSSFoundationApp() {
  const [searchState, setSearchState] = useState({
    query: '',
    isLoading: false,
    error: null as string | null,
  });

  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatusResponse | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  
  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const status = await systemAPI.getStatus();
      setSystemStatus(status);
      setIsConnected(status.connection === 'connected');
    } catch (error) {
      console.error('System status check failed:', error);
      setIsConnected(false);
    }
  };

  const handleSearch = async (query: string) => {
    if (!query.trim()) return;

    setSearchState(prev => ({ ...prev, isLoading: true, error: null }));
    setAiResponse(null);
    setProcessingTime(null);

    try {
      const filters: SearchFilters = {
        query: query.trim(),
        limit: 1, // Only need 1 for AI response
        include_visual: false,
      };

      const response = await searchAPI.search(filters);
      
      // Only extract AI response
      if (response.ai_response) {
        setAiResponse(response.ai_response);
        setProcessingTime(response.processing_time || null);
      } else {
        setAiResponse("No AI response available for this query. Please try a different search term.");
      }
      
      setSearchState(prev => ({
        ...prev,
        query,
        isLoading: false,
        error: null,
      }));

    } catch (error: any) {
      setSearchState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Search failed',
      }));
      setAiResponse(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 shadow-lg border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">🚀</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  ECSS Standards Navigator
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  AI-Powered ECSS Document Search • Fast & Simple
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {systemStatus && (
                <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
                  <div>Status: {isConnected ? 'Connected' : 'Offline'}</div>
                  <div>AI Search: Enabled</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Ask about ECSS standards, requirements, or procedures..."
                value={searchState.query}
                onChange={(e) => setSearchState(prev => ({ ...prev, query: e.target.value }))}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch(searchState.query)}
                className="w-full pl-10 pr-4 py-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-lg text-gray-900"
              />
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                <span className="text-lg">🔍</span>
              </div>
            </div>

            <div className="flex items-center justify-between mt-4">
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  💡 Ask about ECSS requirements, procedures, or standards
                </span>
              </div>

              <button
                onClick={() => handleSearch(searchState.query)}
                disabled={searchState.isLoading || !searchState.query.trim()}
                className="flex items-center space-x-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {searchState.isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                    <span>Searching...</span>
                  </>
                ) : (
                  <>
                    <span>🤖</span>
                    <span>Ask AI</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Error Display */}
          {searchState.error && (
            <div className="max-w-4xl mx-auto mb-6">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center">
                  <span className="text-red-500 mr-2">⚠️</span>
                  <p className="text-red-700">{searchState.error}</p>
                </div>
              </div>
            </div>
          )}

          {/* AI Response */}
          {aiResponse && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 shadow-lg">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 dark:text-blue-400 text-lg">🤖</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
                      AI Response
                    </h3>
                    {processingTime && (
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        Generated in {processingTime.toFixed(1)}s
                      </p>
                    )}
                  </div>
                </div>
                
                <div 
                  className="text-gray-700 dark:text-gray-300 leading-relaxed prose prose-sm max-w-none"
                  style={{ lineHeight: '1.6' }}
                  dangerouslySetInnerHTML={{ __html: aiResponse }}
                />
                
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    💡 This response is based on ECSS standards and requirements from the processed documents.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* No Results Message */}
          {!searchState.isLoading && !aiResponse && searchState.query && !searchState.error && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-6 text-center">
                <div className="text-gray-500 dark:text-gray-400">
                  <span className="text-2xl mb-2 block">🔍</span>
                  <p>Enter a search query above to get AI-powered responses about ECSS standards.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
