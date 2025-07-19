'use client';

import { useState, useEffect } from 'react';
// Enhanced icon components for foundation system
const SearchIcon = () => <span className="text-lg">🔍</span>;
const EyeIcon = () => <span className="text-lg">👁️</span>;
const FileTextIcon = () => <span className="text-lg">📄</span>;
const ImageIcon = () => <span className="text-lg">🖼️</span>;
const AlertCircleIcon = () => <span className="text-lg">⚠️</span>;
const CheckCircleIcon = () => <span className="text-lg">✅</span>;
const ClockIcon = () => <span className="text-lg">⏰</span>;
const ZapIcon = () => <span className="text-lg">⚡</span>;
const BarChartIcon = () => <span className="text-lg">📊</span>;
const CogIcon = () => <span className="text-lg">⚙️</span>;
const DatabaseIcon = () => <span className="text-lg">🗄️</span>;
const TrendingUpIcon = () => <span className="text-lg">📈</span>;
const FilterIcon = () => <span className="text-lg">🔽</span>;
const BrainIcon = () => <span className="text-lg">🧠</span>;
const RocketIcon = () => <span className="text-lg">🚀</span>;
import { searchAPI, systemAPI, apiUtils, errorUtils } from '../utils/api';
import { SearchResult, SearchFilters, SystemStatusResponse } from '../types/api';

export default function ECSSFoundationApp() {
  // Enhanced state management for foundation system
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
  
  // Enhanced foundation system features
  const [searchFilters, setSearchFilters] = useState({
    minScore: 0,
    includeVisual: true,
    sourceTypes: [] as string[],
    showAdvanced: false,
    // ECSS-specific filters (restored from original frontend)
    branch: '',
    docType: '',
    contentType: '',
  });
  
  const [systemMetrics, setSystemMetrics] = useState({
    requestCount: 0,
    errorCount: 0,
    avgProcessingTime: 0,
    visualContentRatio: 0,
  });
  
  const [activeTab, setActiveTab] = useState<'search' | 'dashboard'>('search');

  // Check API connection on mount
  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      // Get status from working backend
      const status = await systemAPI.getStatus();
      setSystemStatus(status);
      setIsConnected(status.connection === 'connected');
      
      console.log('✅ Working backend connected:', status);
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
        limit: 15, // Increased limit for foundation system
        include_visual: searchFilters.includeVisual,
        min_score: searchFilters.minScore > 0 ? searchFilters.minScore : undefined,
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

      // Update system metrics
      setSystemMetrics(prev => ({
        ...prev,
        avgProcessingTime: (prev.avgProcessingTime + (response.processing_time || 0)) / 2,
        visualContentRatio: response.total_results > 0 ? 
          (response.visual_results / response.total_results) * 100 : 0,
      }));

    } catch (error: any) {
      setSearchState(prev => ({
        ...prev,
        isLoading: false,
        error: errorUtils.getUserFriendlyMessage(error),
      }));
      
      // Update error count
      setSystemMetrics(prev => ({
        ...prev,
        errorCount: prev.errorCount + 1,
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
        // Include ECSS-specific filters
        ...(searchFilters.branch && { branch: searchFilters.branch }),
        ...(searchFilters.docType && { doc_type: searchFilters.docType }),
        ...(searchFilters.contentType && { content_type: searchFilters.contentType }),
        ...(searchFilters.minScore > 0 && { min_score: searchFilters.minScore }),
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
      {/* Enhanced Header with Tabs */}
      <header className="bg-white dark:bg-gray-900 shadow-lg border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <RocketIcon />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                  ECSS Foundation System
          </h1>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  Enhanced Visual Content Search • ColPali Enabled • Production Ready
                </p>
              </div>
            </div>
            
            {/* System Status */}
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-1 px-3 py-1 rounded-full text-sm ${
                isConnected 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
              }`}>
                {isConnected ? (
                  <>
                    <CheckCircleIcon />
                    <span>Foundation System Online</span>
                  </>
                ) : (
                  <>
                    <AlertCircleIcon />
                    <span>System Offline</span>
                  </>
                )}
              </div>
              
              {systemStatus && (
                <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
                  <div>System: {systemStatus.system}</div>
                  <div>ColPali: {systemStatus.features?.colpali_visual ? 'Available' : 'Unavailable'}</div>
                </div>
              )}
            </div>
          </div>
          
          {/* Navigation Tabs */}
          <div className="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1 mb-8">
            <button
              onClick={() => setActiveTab('search')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors duration-200 ${
                activeTab === 'search'
                  ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              <SearchIcon />
              <span>Search</span>
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors duration-200 ${
                activeTab === 'dashboard'
                  ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              <BarChartIcon />
              <span>Dashboard</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Tab */}
        {activeTab === 'search' && (
          <div className="space-y-8">
            {/* Enhanced Search Section */}
            <div className="max-w-6xl mx-auto">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <div className="flex flex-col space-y-4">
          {/* Search Input */}
                  <div className="relative">
                    <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                      <SearchIcon />
                    </div>
              <input
                type="text"
                      placeholder="Search ECSS documents with enhanced visual content understanding..."
                      value={searchState.query}
                      onChange={(e) => setSearchState(prev => ({ ...prev, query: e.target.value }))}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          showVisualOnly ? handleVisualSearch(searchState.query) : handleSearch(searchState.query);
                        }
                      }}
                      className="w-full pl-10 pr-4 py-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-lg text-gray-900 dark:text-gray-100"
                    />
                  </div>

                  {/* Enhanced Search Controls */}
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
                      
                      <button
                        onClick={() => setSearchFilters(prev => ({ ...prev, showAdvanced: !prev.showAdvanced }))}
                        className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                      >
                        <FilterIcon />
                        <span>Advanced</span>
                      </button>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {searchState.totalResults > 0 && (
                          <span>{searchState.totalResults} results • {apiUtils.formatProcessingTime(searchState.processingTime)}</span>
                        )}
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

                  {/* Advanced Search Filters */}
                  {searchFilters.showAdvanced && (
                    <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Minimum Relevance Score
                          </label>
                          <input
                            type="range"
                            min="0"
                            max="10"
                            step="0.5"
                            value={searchFilters.minScore}
                            onChange={(e) => setSearchFilters(prev => ({ ...prev, minScore: parseFloat(e.target.value) }))}
                            className="w-full"
                          />
                          <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                            Score: {searchFilters.minScore}
                          </div>
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Include Visual Content
                          </label>
                          <div className="flex items-center space-x-3">
                            <input
                              type="checkbox"
                              checked={searchFilters.includeVisual}
                              onChange={(e) => setSearchFilters(prev => ({ ...prev, includeVisual: e.target.checked }))}
                              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              Search images, diagrams, and tables
                            </span>
                          </div>
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            ECSS Branch
                          </label>
                <select
                            value={searchFilters.branch}
                            onChange={(e) => setSearchFilters(prev => ({ 
                              ...prev, 
                              branch: e.target.value 
                            }))}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                >
                  <option value="">All Branches</option>
                  <option value="E">E - Engineering</option>
                  <option value="M">M - Management</option>
                  <option value="Q">Q - Quality Assurance</option>
                            <option value="S">S - Space Assurance</option>
                            <option value="U">U - Sustainability</option>
                </select>
              </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Content Type
                          </label>
                <select
                            value={searchFilters.contentType}
                            onChange={(e) => setSearchFilters(prev => ({ 
                              ...prev, 
                              contentType: e.target.value 
                            }))}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                          >
                            <option value="">All Types</option>
                            <option value="requirement">Requirements</option>
                            <option value="definition">Definitions</option>
                            <option value="procedure">Procedures</option>
                            <option value="specification">Specifications</option>
                            <option value="visual content">Visual Content</option>
                </select>
              </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Document Type
                          </label>
                <select
                            value={searchFilters.docType}
                            onChange={(e) => setSearchFilters(prev => ({ 
                              ...prev, 
                              docType: e.target.value 
                            }))}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                          >
                            <option value="">All Documents</option>
                            <option value="standard">Standards</option>
                            <option value="handbook">Handbooks</option>
                            <option value="annex">Annexes</option>
                </select>
              </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

            {/* Search Results */}
            {searchState.error && (
              <div className="max-w-6xl mx-auto">
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                  <div className="flex items-center space-x-2">
                    <AlertCircleIcon />
                    <p className="text-red-700 dark:text-red-300">{searchState.error}</p>
          </div>
        </div>
            </div>
          )}

            {/* AI Response Section */}
            {searchState.contextualResponse && (
              <div className="max-w-6xl mx-auto mb-6">
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6 shadow-lg">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                      <BrainIcon />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3 text-lg">
                        🤖 AI Analysis & Summary
                      </h4>
                      <div className="text-blue-800 dark:text-blue-200 leading-relaxed prose prose-sm">
                        {searchState.contextualResponse
                          .replace(/\*\*/g, '') 
                          .replace(/\*/g, '')
                          .replace(/\n\n/g, '\n')
                          .split('\n')
                          .filter(line => line.trim())
                          .map((line, index) => {
                            if (line.trim().match(/^\d+\./)) {
                              return (
                                <div key={index} className="mb-2 pl-4">
                                  <span className="font-medium">{line.trim()}</span>
                                </div>
                              );
                            }
                            return (
                              <p key={index} className="mb-3">
                                {line.trim()}
                              </p>
                            );
                          })}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Search Results List */}
            {displayResults.length > 0 && (
              <div className="max-w-6xl mx-auto">
                {/* Results Header */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-6">
                      <div className="text-sm text-gray-600 dark:text-gray-300">
                        <span className="font-semibold text-gray-900 dark:text-white text-lg">
                          {searchState.totalResults}
                        </span>{' '}
                        results found
                      </div>
                      
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="flex items-center space-x-1 px-3 py-1 bg-purple-100 dark:bg-purple-900/20 rounded-full">
                          <ImageIcon />
                          <span className="text-purple-700 dark:text-purple-300 font-medium">
                            {searchState.visualCount} visual
                          </span>
                        </div>
                        <div className="flex items-center space-x-1 px-3 py-1 bg-blue-100 dark:bg-blue-900/20 rounded-full">
                          <FileTextIcon />
                          <span className="text-blue-700 dark:text-blue-300 font-medium">
                            {searchState.textCount} text
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm">
                      <div className="flex items-center space-x-1 text-gray-500 dark:text-gray-400">
                        <ClockIcon />
                        <span>{apiUtils.formatProcessingTime(searchState.processingTime)}</span>
                      </div>
                      <div className="text-xs text-gray-400 dark:text-gray-500">
                        Visual Content: {systemMetrics.visualContentRatio.toFixed(1)}%
                      </div>
                      </div>
                    </div>
                  </div>
                  
            {/* Specific Search Results */}
            <div className="space-y-4">
              <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                📋 Specific Matches ({displayResults.length} found)
              </div>
              {displayResults.map((result, index) => (
                <div
                  key={index}
                  className={`bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow ${
                    (result.is_visual_content === true) ? 'border-l-4 border-l-purple-500' : 'border-l-4 border-l-blue-500'
                  }`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {/* Percentage Score Badge */}
                      <div className={`px-3 py-2 rounded-lg text-sm font-bold ${
                        (result.relevance_score || 0) >= 0.8 
                          ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                          : (result.relevance_score || 0) >= 0.6
                          ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200'
                          : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                      }`}>
                        {result.relevance_score ? `${(result.relevance_score * 100).toFixed(0)}%` : 'N/A'}
                      </div>
                      
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
                    </div>
                    
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {result.document_info?.filename || 'Unknown document'}
                    </div>
                  </div>

                  <div className="mb-4">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-lg">
                      {result.summary || 'Matched Content'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                      {result.content ? 
                        result.content.length > 300 
                          ? `${result.content.substring(0, 300)}...` 
                          : result.content
                        : 'No content available'
                      }
                    </p>
                  </div>

                  {result.explanation && (
                    <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                      <div className="flex items-start space-x-2">
                        <span className="text-xs text-gray-500 dark:text-gray-400 font-medium">Match reason:</span>
                        <p className="text-xs text-gray-600 dark:text-gray-400 flex-1">
                          {result.explanation}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
                        </div>
                      </div>
                    )}
                    
        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* System Overview */}
            <div className="max-w-6xl mx-auto">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <BarChartIcon />
                  <span>Foundation System Dashboard</span>
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg">
                    <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                      {systemStatus?.connection === 'connected' ? '✅' : '❌'}
                    </div>
                    <div className="text-sm text-blue-700 dark:text-blue-300 mt-2">Backend Status</div>
                    <div className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                      {systemStatus?.system || 'Unknown'}
                    </div>
                  </div>
                  
                  <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg">
                    <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                      {systemStatus?.features?.colpali_visual ? '✅' : '❌'}
                    </div>
                    <div className="text-sm text-green-700 dark:text-green-300 mt-2">ColPali Visual</div>
                    <div className="text-xs text-green-600 dark:text-green-400 mt-1">
                      Image & diagram search
                    </div>
                  </div>
                    
                  <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg">
                    <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                      {systemStatus?.features?.standard_query ? '✅' : '❌'}
                        </div>
                    <div className="text-sm text-purple-700 dark:text-purple-300 mt-2">Text Search</div>
                    <div className="text-xs text-purple-600 dark:text-purple-400 mt-1">
                      Standard ECSS search
                            </div>
                          </div>
                          
                  <div className="text-center p-6 bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 rounded-lg">
                    <div className="text-3xl font-bold text-orange-600 dark:text-orange-400">
                      {systemMetrics.avgProcessingTime.toFixed(1)}s
                    </div>
                    <div className="text-sm text-orange-700 dark:text-orange-300 mt-2">Avg Response Time</div>
                    <div className="text-xs text-orange-600 dark:text-orange-400 mt-1">
                      From recent searches
                    </div>
                  </div>
                            </div>
                          </div>
                        </div>

            {/* Performance Metrics */}
            <div className="max-w-6xl mx-auto">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
                  <TrendingUpIcon />
                  <span>Performance Metrics</span>
                            </h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <h5 className="font-medium text-gray-900 dark:text-white mb-2">System Status</h5>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-300">Foundation System:</span>
                        <span className={`font-medium ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
                          {isConnected ? 'Online' : 'Offline'}
                        </span>
                                  </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-300">ColPali:</span>
                        <span className="font-medium text-purple-600">
                          {systemStatus?.foundation_system?.colpali_enabled ? 'Enabled' : 'Disabled'}
                                    </span>
                      </div>
                                             <div className="flex justify-between">
                         <span className="text-gray-600 dark:text-gray-300">Morphik:</span>
                         <span className="font-medium text-blue-600">
                           {systemStatus?.foundation_system?.morphik_connected ? 'Connected' : 'Disconnected'}
                                      </span>
                                  </div>
                                  </div>
                                </div>
                  
                  <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <h5 className="font-medium text-gray-900 dark:text-white mb-2">Cost Monitoring</h5>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-300">Total Cost:</span>
                        <span className="font-medium text-green-600">
                          ${systemStatus?.foundation_system?.ingestion_stats?.total_cost?.toFixed(2) || '0.00'}
                        </span>
                            </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-300">Cost Limit:</span>
                        <span className="font-medium text-yellow-600">
                          ${systemStatus?.foundation_system?.config?.cost_limit_per_doc || '2.00'} per doc
                        </span>
                          </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-300">Max Documents:</span>
                        <span className="font-medium text-blue-600">
                          {systemStatus?.foundation_system?.config?.max_documents || '10'}
                                      </span>
                                  </div>
                                    </div>
                                </div>
                            </div>
                          </div>
                            </div>
                          </div>
                        )}
        

      </main>
    </div>
  );
}
