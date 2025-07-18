'use client';

import { useState, useEffect } from 'react';
// Simple icon components to replace lucide-react
const SearchIcon = () => <span className="text-lg">🔍</span>;
const EyeIcon = () => <span className="text-lg">👁️</span>;
const FileTextIcon = () => <span className="text-lg">📄</span>;
const ImageIcon = () => <span className="text-lg">🖼️</span>;
const AlertCircleIcon = () => <span className="text-lg">⚠️</span>;
const CheckCircleIcon = () => <span className="text-lg">✅</span>;
const ClockIcon = () => <span className="text-lg">⏰</span>;
const ZapIcon = () => <span className="text-lg">⚡</span>;
import { searchAPI, systemAPI, apiUtils, errorUtils } from '../utils/api';
import { SearchResult, SearchFilters, SystemStatusResponse } from '../types/api';

export default function ECSSFoundationApp() {
  // State management
  const [searchState, setSearchState] = useState({
    query: '',
    results: [] as SearchResult[],
    visualResults: [] as SearchResult[],
    isLoading: false,
    error: null as string | null,
    contextualResponse: null as string | null,
    processingTime: 0,
    totalResults: 0,
    visualCount: 0,
    textCount: 0,
  });

  const [systemStatus, setSystemStatus] = useState<SystemStatusResponse | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [showVisualOnly, setShowVisualOnly] = useState(false);

  // Check API connection on mount
  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const health = await systemAPI.getHealth();
      // For now, we'll just check if we can connect to the API
      setIsConnected(true);
      // Don't set complex system status since the deployed backend doesn't have /api/status
      console.log('✅ Backend connection successful:', health);
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
        include_visual: true,
      };

      const response = await searchAPI.search(filters);

      // Separate visual and text results
      const visualResults = response.results.filter(r => r.is_visual_content);
      const textResults = response.results.filter(r => !r.is_visual_content);

      setSearchState(prev => ({
        ...prev,
        query,
        results: response.results,
        visualResults,
        contextualResponse: response.contextual_response || null,
        processingTime: response.processing_time || 0,
        totalResults: response.total_results,
        visualCount: response.visual_results,
        textCount: response.text_results,
        isLoading: false,
        error: null,
      }));
    } catch (error: any) {
      setSearchState(prev => ({
        ...prev,
        isLoading: false,
        error: errorUtils.getUserFriendlyMessage(error),
      }));
    }
  };

  const handleVisualSearch = async (query: string) => {
    if (!query.trim()) return;

    setSearchState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const filters = {
        query: query.trim(),
        limit: 10,
      };

      const response = await searchAPI.searchVisual(filters);

      setSearchState(prev => ({
        ...prev,
        query,
        results: response.visual_results,
        visualResults: response.visual_results,
        contextualResponse: null,
        processingTime: response.processing_time || 0,
        totalResults: response.total_visual_results,
        visualCount: response.total_visual_results,
        textCount: 0,
        isLoading: false,
        error: null,
      }));
    } catch (error: any) {
      setSearchState(prev => ({
        ...prev,
        isLoading: false,
        error: errorUtils.getUserFriendlyMessage(error),
      }));
    }
  };

  const displayResults = showVisualOnly ? searchState.visualResults : searchState.results;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 shadow-lg border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <ZapIcon />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  ECSS Foundation System
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  Enhanced Visual Content Search
                </p>
              </div>
            </div>
            
            {/* System Status */}
            <div className="flex items-center space-x-2">
              <div className={`flex items-center space-x-1 px-3 py-1 rounded-full text-sm ${
                isConnected 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
              }`}>
                              {isConnected ? (
                <>
                  <CheckCircleIcon />
                  <span>Online</span>
                </>
              ) : (
                <>
                  <AlertCircleIcon />
                  <span>Offline</span>
                </>
              )}
              </div>
              
              {systemStatus && (
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  ColPali: {systemStatus.foundation_system.colpali_enabled ? 'Enabled' : 'Disabled'}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="flex flex-col space-y-4">
              {/* Search Input */}
              <div className="relative">
                <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                  <SearchIcon />
                </div>
                <input
                  type="text"
                  placeholder="Search ECSS documents with visual content support..."
                  value={searchState.query}
                  onChange={(e) => setSearchState(prev => ({ ...prev, query: e.target.value }))}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      showVisualOnly ? handleVisualSearch(searchState.query) : handleSearch(searchState.query);
                    }
                  }}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white search-input"
                />
              </div>

              {/* Search Controls */}
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => setShowVisualOnly(false)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      !showVisualOnly
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <FileTextIcon />
                    <span>All Content</span>
                  </button>
                  
                  <button
                    onClick={() => setShowVisualOnly(true)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      showVisualOnly
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <EyeIcon />
                    <span>Visual Only</span>
                  </button>
                </div>

                <button
                  onClick={() => {
                    showVisualOnly ? handleVisualSearch(searchState.query) : handleSearch(searchState.query);
                  }}
                  disabled={searchState.isLoading || !searchState.query.trim()}
                  className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {searchState.isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                      <span>Searching...</span>
                    </>
                  ) : (
                    <>
                      <SearchIcon />
                      <span>Search</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results Section */}
                 {searchState.error && (
           <div className="max-w-4xl mx-auto mb-8">
             <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
               <div className="flex items-center space-x-2">
                 <AlertCircleIcon />
                 <p className="text-red-700 dark:text-red-300">{searchState.error}</p>
               </div>
             </div>
           </div>
         )}

        {/* Search Results */}
        {displayResults.length > 0 && (
          <div className="max-w-4xl mx-auto">
            {/* Results Header */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-6">
                  <div className="text-sm text-gray-600 dark:text-gray-300">
                    <span className="font-semibold text-gray-900 dark:text-white">
                      {searchState.totalResults}
                    </span>{' '}
                    results found
                  </div>
                  
                                     <div className="flex items-center space-x-4 text-sm">
                     <div className="flex items-center space-x-1">
                       <ImageIcon />
                       <span className="text-gray-600 dark:text-gray-300">
                         {searchState.visualCount} visual
                       </span>
                     </div>
                     <div className="flex items-center space-x-1">
                       <FileTextIcon />
                       <span className="text-gray-600 dark:text-gray-300">
                         {searchState.textCount} text
                       </span>
                     </div>
                   </div>
                 </div>
                 
                 <div className="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400">
                   <ClockIcon />
                   <span>{apiUtils.formatProcessingTime(searchState.processingTime)}</span>
                 </div>
              </div>

              {/* Contextual Response */}
              {searchState.contextualResponse && (
                <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                    AI Summary
                  </h4>
                  <p className="text-blue-800 dark:text-blue-200 text-sm leading-relaxed">
                    {searchState.contextualResponse}
                  </p>
                </div>
              )}
            </div>

            {/* Results List */}
            <div className="space-y-4">
              {displayResults.map((result, index) => (
                <div
                  key={index}
                  className={`bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 card-hover ${
                    (result.is_visual_content === true) ? 'visual-indicator' : ''
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                        apiUtils.getSourceTypeColor(result.source_type || 'Information')
                      }`}>
                        {result.source_type || 'Information'}
                      </div>
                      
                                                                   {(result.is_visual_content === true) && (
                        <div className="flex items-center space-x-1 px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full text-xs">
                          <EyeIcon />
                          <span>Visual</span>
                        </div>
                      )}
                      
                      <div className={`text-sm font-medium ${
                        apiUtils.getRelevanceScoreColor(result.relevance_score || 0)
                      }`}>
                        {result.relevance_score ? result.relevance_score.toFixed(1) : 'N/A'}
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {result.document_info?.filename || 'Unknown document'}
                    </div>
                  </div>

                  <div className="mb-3">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      {result.summary || 'No summary available'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                      {result.content || 'No content available'}
                    </p>
                  </div>

                  <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                    <div className="flex items-center justify-between">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {result.explanation || 'No explanation available'}
                      </p>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        Chunk #{result.document_info?.chunk_number || 'N/A'}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* System Information */}
        {systemStatus && (
          <div className="max-w-4xl mx-auto mt-8">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                System Information
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {systemStatus.foundation_system.ingestion_stats.total_processed}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Documents Processed</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {systemStatus.foundation_system.ingestion_stats.visual_chunks_created}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Visual Chunks</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {systemStatus.api_metrics.request_count}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">API Requests</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
