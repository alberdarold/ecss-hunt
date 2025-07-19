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

  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
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

    try {
      const filters: SearchFilters = {
        query: query.trim(),
        limit: 10,
        include_visual: false,  // Prioritize text content over visual content
      };

      const response = await searchAPI.search(filters);
      setSearchResults(response);
      
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
                  ECSS Foundation System
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Enhanced Visual Content Search • ColPali Enabled • Production Ready
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {systemStatus && (
                <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
                  <div>Status: {isConnected ? 'Connected' : 'Offline'}</div>
                  <div>ColPali: {systemStatus.features?.colpali_visual ? 'Enabled' : 'Disabled'}</div>
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
                placeholder="Search ECSS documents with enhanced visual content understanding..."
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
                <button
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-blue-600 text-white"
                >
                  <span className="text-lg">📄</span>
                  <span>All Content</span>
                </button>
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
                    <span>🔍</span>
                    <span>Search</span>
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

          {/* Search Results */}
          {searchResults && searchResults.results && searchResults.results.length > 0 && (
            <div className="max-w-6xl mx-auto space-y-6">
              
              {/* AI Contextual Response Box - Compact Lines */}
              {searchResults.ai_response && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-2 h-2 bg-gray-500 rounded-full"></div>
                    <h3 className="text-sm font-semibold text-gray-800">
                      🤖 AI Contextual Response
                    </h3>
                    <span className="text-xs text-gray-500">
                      {searchResults.processing_time?.toFixed(1)}s
                    </span>
                  </div>
                  <div 
                    className="text-sm text-gray-700 leading-snug"
                    style={{ lineHeight: '1.3' }}
                    dangerouslySetInnerHTML={{ __html: searchResults.ai_response }}
                  />
                </div>
              )}

              {/* Document Search Results */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
                    📄 Specific Document Matches ({searchResults.total} found)
                  </h3>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Methods: {searchResults.methods_used?.join(', ')}
                  </div>
                </div>
                
                {searchResults.results.map((result, index) => (
                  <div key={result.id} className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                    
                    {/* Result Header */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result.metadata?.is_visual 
                            ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                            : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        }`}>
                          {result.metadata?.is_visual ? '🎨 Visual' : '📝 Text'}
                        </span>
                        
                        {/* Score Badge */}
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result.score >= 8 ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                          result.score >= 5 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                          'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                        }`}>
                          {result.score.toFixed(1)}% match
                        </span>
                      </div>
                      
                      {/* Document Reference */}
                      {result.metadata?.document_name && (
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          📑 {result.metadata.document_name}
                        </div>
                      )}
                    </div>

                    {/* Text Content - Primary Display */}
                    <div className="space-y-3">
                      <h4 className="text-base font-medium text-gray-800 dark:text-gray-200">
                        {result.title || 'ECSS Document Section'}
                      </h4>
                      
                      {/* Real ECSS Text Content */}
                      <div className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        <div className="whitespace-pre-line text-sm leading-normal bg-white p-4 rounded border border-gray-200 shadow-sm">
                          {result.content}
                        </div>
                      </div>
                      

                      
                      {/* Visual content as supplementary (only if no text) */}
                      {(!result.content || result.content.length < 50) && result.metadata?.is_visual && result.metadata?.image_url && (
                        <div className="mt-4">
                          <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">Visual content reference:</p>
                          <img 
                            src={result.metadata.image_url} 
                            alt="Document visual reference"
                            className="max-w-full h-auto border rounded-lg shadow-sm"
                            style={{ maxHeight: '200px' }}
                          />
                        </div>
                      )}
                    </div>

                    {/* Metadata Footer */}
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600 text-xs text-gray-500 dark:text-gray-400 text-right">
                      <div>
                        {(result.metadata as any)?.page_display || 'Page: N/A'}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
