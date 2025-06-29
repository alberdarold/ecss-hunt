'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from './page.module.css';

// All interfaces and types at the top level (outside Home)
interface SearchResult {
  id: string;
  content: string;
  metadata: {
    document_name: string;
    branch?: string;
    discipline?: string;
    revision?: string;
    section?: string;
    page_number?: number;
    entity_type?: string;
    retrieval_method?: string;
    visual_confidence?: number;
  };
  score: number;
}

interface SearchFilters {
  branch: string;
  discipline: string;
  revision: string;
}

interface ECSSSectionInfo {
  section_number: string;
  section_title: string;
  section_type: string;
  is_normative?: boolean;
  is_informative?: boolean;
  content_summary?: string;
  requirements_count?: number;
  recommendations_count?: number;
  permissions_count?: number;
  figures_count?: number;
  tables_count?: number;
}

interface ECSSRequirement {
  unique_id: string;
  statement: string;
  requirement_type: string;
  is_normative?: boolean;
  section_number?: string;
  cross_references?: string[];
  verification_method?: string;
  applicable_phases?: string[];
  notes?: string[];
}

interface ECSSCrossReference {
  source_id: string;
  target: string;
  target_type: string;
  context?: string;
}

interface ECSSAnnexInfo {
  annex_id: string;
  title: string;
  is_normative?: boolean;
  content_summary?: string;
}

interface ECSSNoteInfo {
  note_id: string;
  related_to: string;
  content: string;
}

interface ECSSTableInfo {
  table_number: string;
  table_title: string;
  table_type: string;
  row_count?: number;
  column_count?: number;
  content_summary?: string;
  key_parameters?: string[];
  section_number?: string;
}

interface ECSSFigureInfo {
  figure_number: string;
  figure_title: string;
  diagram_type: string;
  content_description?: string;
  components?: string[];
  relationships?: string[];
  section_number?: string;
}

interface ExtendedSearchResult extends SearchResult {
  ecss_sections?: ECSSSectionInfo[];
  ecss_requirements?: ECSSRequirement[];
  ecss_cross_references?: ECSSCrossReference[];
  ecss_annexes?: ECSSAnnexInfo[];
  ecss_notes?: ECSSNoteInfo[];
  ecss_tables?: ECSSTableInfo[];
  ecss_figures?: ECSSFigureInfo[];
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<SearchFilters>({
    branch: '',
    discipline: '',
    revision: ''
  });
  const [expandedResult, setExpandedResult] = useState<number | null>(null);
  const [expandedContent, setExpandedContent] = useState<Set<number>>(new Set());

  const handleSearch = async (page: number = 1) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // Build query string for filters
      const params = new URLSearchParams({
        q: query.trim(),
        compact: 'true',  // Use compact mode by default
        page: page.toString(),
        limit: '5'
      });
      if (filters.branch) params.append('branch', filters.branch);
      if (filters.discipline) params.append('discipline', filters.discipline);
      if (filters.revision) params.append('revision', filters.revision);

      // Call Flask backend using environment variable or Render URL
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : 'https://ecss-hunt.onrender.com');
      const response = await fetch(`${apiUrl}/api/search?${params.toString()}`);

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch(1);
    }
  };

  const clearFilters = () => {
    setFilters({
      branch: '',
      discipline: '',
      revision: ''
    });
  };

  const formatScore = (score: number) => {
    // Handle different score formats from the backend
    if (score >= 0 && score <= 1) {
      // Score is a decimal between 0-1, convert to percentage
      return Math.round(score * 100);
    } else if (score > 1 && score <= 100) {
      // Score is already a percentage
      return Math.round(score);
    } else if (score > 100) {
      // Score is inflated, cap at 100%
      return 100;
    } else {
      // Invalid score, return 0
      return 0;
    }
  };

  const toggleContentExpansion = (index: number) => {
    const newExpanded = new Set(expandedContent);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedContent(newExpanded);
  };

  const getContentPreview = (content: string, maxLength: number = 250) => {
    if (content.length <= maxLength) return content;
    
    // Remove excessive markdown formatting for preview
    let cleanContent = content
      .replace(/\*\*([^*]+)\*\*/g, '$1')  // Remove bold markdown
      .replace(/\*([^*]+)\*/g, '$1')      // Remove italic markdown
      .replace(/#+\s/g, '')               // Remove headers
      .replace(/\n\s*\n/g, ' ')           // Replace multiple newlines with space
      .replace(/\s+/g, ' ')               // Normalize whitespace
      .trim();
    
    if (cleanContent.length <= maxLength) return cleanContent;
    
    // Try to cut at a sentence boundary
    const preview = cleanContent.substring(0, maxLength);
    const lastSentence = preview.lastIndexOf('. ');
    const lastQuestion = preview.lastIndexOf('? ');
    const lastExclamation = preview.lastIndexOf('! ');
    
    const lastPunctuation = Math.max(lastSentence, lastQuestion, lastExclamation);
    
    if (lastPunctuation > maxLength * 0.6) {
      return preview.substring(0, lastPunctuation + 1);
    }
    
    // Fallback to word boundary
    const lastSpace = preview.lastIndexOf(' ');
    return lastSpace > maxLength * 0.6 ? preview.substring(0, lastSpace) + '...' : preview + '...';
  };

  const getDisciplineColor = (discipline: string) => {
    const colors: { [key: string]: string } = {
      'E': 'var(--primary-color)',
      'M': 'var(--accent-color)',
      'Q': 'var(--success-color)',
      'S': 'var(--secondary-color)'
    };
    return colors[discipline] || 'var(--text-secondary)';
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.title}>
            <span className={styles.titleIcon}>🚀</span>
            ECSS Standards Navigator
          </h1>
          <p className={styles.subtitle}>
            Search and navigate European Cooperation for Space Standardization documents
          </p>
        </div>
      </header>

      {/* Search Section */}
      <main className={styles.main}>
        <div className={styles.searchSection}>
          {/* Search Input */}
          <div className={styles.searchContainer}>
            <div className={styles.searchInputWrapper}>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Search ECSS standards (e.g., 'software requirements', 'materials testing')"
                className={styles.searchInput}
                disabled={loading}
              />
              <button
                onClick={() => handleSearch(1)}
                disabled={loading || !query.trim()}
                className={styles.searchButton}
              >
                {loading ? (
                  <span className={styles.spinner}>⏳</span>
                ) : (
                  <span>🔍</span>
                )}
                Search
              </button>
            </div>
          </div>

          {/* Filters */}
          <div className={styles.filtersSection}>
            <h3 className={styles.filtersTitle}>Filters</h3>
            <div className={styles.filtersGrid}>
              <div className={styles.filterGroup}>
                <label htmlFor="branch" className={styles.filterLabel}>Branch</label>
                <select
                  id="branch"
                  value={filters.branch}
                  onChange={(e) => setFilters({...filters, branch: e.target.value})}
                  className={styles.filterSelect}
                >
                  <option value="">All Branches</option>
                  <option value="E">E - Engineering</option>
                  <option value="M">M - Management</option>
                  <option value="Q">Q - Quality Assurance</option>
                  <option value="S">S - Space Engineering</option>
                </select>
              </div>

              <div className={styles.filterGroup}>
                <label htmlFor="discipline" className={styles.filterLabel}>Discipline</label>
                <select
                  id="discipline"
                  value={filters.discipline}
                  onChange={(e) => setFilters({...filters, discipline: e.target.value})}
                  className={styles.filterSelect}
                >
                  <option value="">All Disciplines</option>
                  <option value="10">10 - Project Planning</option>
                  <option value="20">20 - Software</option>
                  <option value="30">30 - Electrical</option>
                  <option value="40">40 - Mechanical</option>
                  <option value="50">50 - Communications</option>
                  <option value="60">60 - Quality</option>
                  <option value="70">70 - Materials</option>
                </select>
              </div>

              <div className={styles.filterGroup}>
                <label htmlFor="revision" className={styles.filterLabel}>Revision</label>
                <select
                  id="revision"
                  value={filters.revision}
                  onChange={(e) => setFilters({...filters, revision: e.target.value})}
                  className={styles.filterSelect}
                >
                  <option value="">All Revisions</option>
                  <option value="A">A</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                </select>
              </div>

              <div className={styles.filterGroup}>
                <button
                  onClick={clearFilters}
                  className={styles.clearFiltersButton}
                >
                  Clear Filters
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className={styles.resultsSection}>
          {error && (
            <div className={styles.errorMessage}>
              <span className={styles.errorIcon}>⚠️</span>
              {error}
            </div>
          )}

          {loading && (
            <div className={styles.loadingMessage}>
              <span className={styles.spinner}>🔍</span>
              Searching ECSS standards...
              <div className="mt-2 text-sm text-gray-500">
                Optimized search with compact results for faster loading
              </div>
            </div>
          )}

          {!loading && !error && results.length > 0 && (
            <div className={styles.resultsHeader}>
              <h2 className={styles.resultsTitle}>
                Found {results.length} result{results.length !== 1 ? 's' : ''}
              </h2>
            </div>
          )}

          {!loading && !error && results.length === 0 && query && (
            <div className={styles.noResults}>
              <span className={styles.noResultsIcon}>🔍</span>
              <h3>No results found</h3>
              <p>Try adjusting your search terms or filters</p>
            </div>
          )}

          <div className={styles.resultsList}>
            {results.map((result, index) => {
              const extResult = result as ExtendedSearchResult;
              const uniqueKey = result.id || `result-${index}`;
              return (
                <div key={uniqueKey} className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow p-4 mb-3">
                    {/* Header with document info and score */}
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-800 mb-1 truncate">
                          {result.metadata?.document_name && result.metadata.document_name !== 'Unknown Document' 
                            ? result.metadata.document_name 
                            : 'ECSS Document'}
                        </h3>
                        <div className="flex items-center gap-2 flex-wrap">
                          {result.metadata?.entity_type && result.metadata.entity_type !== 'unknown' && (
                            <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded-full">
                              {result.metadata.entity_type}
                            </span>
                          )}
                          {result.metadata?.retrieval_method && result.metadata.retrieval_method !== 'unknown' && (
                            <span className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">
                              {result.metadata.retrieval_method}
                            </span>
                          )}
                          {result.metadata?.visual_confidence && result.metadata.visual_confidence > 0 && (
                            <span className="px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded-full">
                              Visual: {Math.round(result.metadata.visual_confidence * 100)}%
                            </span>
                          )}
                          {result.metadata?.section && (
                            <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-700 rounded-full">
                              Section: {result.metadata.section}
                            </span>
                          )}
                          {result.metadata?.page_number && (
                            <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                              P. {result.metadata.page_number}
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="flex flex-col items-end ml-4">
                        <div className="text-sm font-medium text-green-600 mb-1">
                          {formatScore(result.score)}% Match
                        </div>
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full" 
                            style={{ width: `${Math.min(formatScore(result.score), 100)}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                    {/* Content Preview */}
                    <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                      <ReactMarkdown>
                        {expandedContent.has(index) ? result.content : getContentPreview(result.content)}
                      </ReactMarkdown>
                    </div>
                    
                    {/* Action buttons */}
                    <div className="flex items-center gap-2 mt-4 pt-3 border-t border-gray-100">
                      {result.content.length > 250 && (
                        <button
                          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md"
                          onClick={() => toggleContentExpansion(index)}
                        >
                          <span className="text-base">{expandedContent.has(index) ? '📖' : '📄'}</span>
                          {expandedContent.has(index) ? 'Show Less' : 'Read Full Content'}
                        </button>
                      )}
                      
                      {/* ECSS metadata expansion */}
                      <button
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md"
                        onClick={() => setExpandedResult(expandedResult === index ? null : index)}
                      >
                        <span className="text-base">🔍</span>
                        {expandedResult === index ? 'Hide Technical Details' : 'Show Technical Details'}
                      </button>
                      
                      {/* Quick info */}
                      <div className="ml-auto text-xs text-gray-500">
                        {result.metadata?.branch && (
                          <span className="mr-2">Branch: {result.metadata.branch}</span>
                        )}
                        {result.metadata?.discipline && (
                          <span>Discipline: {result.metadata.discipline}</span>
                        )}
                      </div>
                    </div>
                    
                    {expandedResult === index && (
                      <div className="mt-4 border-t pt-4 bg-gray-50 rounded-lg p-4">
                        <div className="mb-4">
                          <h3 className="text-lg font-semibold text-gray-800 mb-2">📋 ECSS Technical Details</h3>
                          <p className="text-sm text-gray-600 mb-4">
                            Detailed technical metadata extracted from the ECSS document, including sections, requirements, and cross-references.
                          </p>
                        </div>
                        
                        {/* Basic Metadata */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div className="bg-white p-3 rounded-md border">
                            <h4 className="font-semibold text-gray-700 mb-2">📄 Document Info</h4>
                            <div className="space-y-1 text-sm">
                              {result.metadata?.document_name && (
                                <div><span className="font-medium">Name:</span> {result.metadata.document_name}</div>
                              )}
                              {result.metadata?.branch && (
                                <div><span className="font-medium">Branch:</span> {result.metadata.branch}</div>
                              )}
                              {result.metadata?.discipline && (
                                <div><span className="font-medium">Discipline:</span> {result.metadata.discipline}</div>
                              )}
                              {result.metadata?.section && (
                                <div><span className="font-medium">Section:</span> {result.metadata.section}</div>
                              )}
                              {result.metadata?.page_number && (
                                <div><span className="font-medium">Page:</span> {result.metadata.page_number}</div>
                              )}
                            </div>
                          </div>
                          
                          <div className="bg-white p-3 rounded-md border">
                            <h4 className="font-semibold text-gray-700 mb-2">🎯 Relevance Info</h4>
                            <div className="space-y-1 text-sm">
                              <div><span className="font-medium">Match Score:</span> {formatScore(result.score)}%</div>
                              {result.metadata?.entity_type && result.metadata.entity_type !== 'unknown' && (
                                <div><span className="font-medium">Content Type:</span> {result.metadata.entity_type}</div>
                              )}
                              {result.metadata?.retrieval_method && result.metadata.retrieval_method !== 'unknown' && (
                                <div><span className="font-medium">Method:</span> {result.metadata.retrieval_method}</div>
                              )}
                              {result.metadata?.visual_confidence && result.metadata.visual_confidence > 0 && (
                                <div><span className="font-medium">Visual Confidence:</span> {Math.round(result.metadata.visual_confidence * 100)}%</div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Sections */}
                        {extResult.ecss_sections && extResult.ecss_sections.length > 0 && (
                          <div className="mb-4">
                            <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                              📑 ECSS Sections ({extResult.ecss_sections.length})
                            </h4>
                            <div className="bg-white rounded-md border divide-y">
                              {extResult.ecss_sections.map((sec, i) => (
                                <div key={i} className="p-3">
                                  <div className="font-medium text-gray-800">
                                    {sec.section_number} - {sec.section_title}
                                  </div>
                                  <div className="text-sm text-gray-600 mt-1">
                                    <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs mr-2">
                                      {sec.section_type}
                                    </span>
                                    {sec.is_normative && (
                                      <span className="inline-block bg-green-100 text-green-800 px-2 py-1 rounded text-xs mr-2">
                                        Normative
                                      </span>
                                    )}
                                    {sec.is_informative && (
                                      <span className="inline-block bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs mr-2">
                                        Informative
                                      </span>
                                    )}
                                  </div>
                                  {sec.content_summary && (
                                    <div className="text-sm text-gray-700 mt-2">{sec.content_summary}</div>
                                  )}
                                  <div className="text-xs text-gray-500 mt-2 flex gap-4">
                                    <span>Requirements: {sec.requirements_count || 0}</span>
                                    <span>Recommendations: {sec.recommendations_count || 0}</span>
                                    <span>Figures: {sec.figures_count || 0}</span>
                                    <span>Tables: {sec.tables_count || 0}</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Requirements */}
                        {extResult.ecss_requirements && extResult.ecss_requirements.length > 0 && (
                          <div className="mb-4">
                            <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                              ⚡ Requirements & Recommendations ({extResult.ecss_requirements.length})
                            </h4>
                            <div className="bg-white rounded-md border divide-y max-h-64 overflow-y-auto">
                              {extResult.ecss_requirements.map((req, i) => (
                                <div key={i} className="p-3">
                                  <div className="font-medium text-gray-800 mb-1">
                                    {req.unique_id}
                                    <span className="ml-2 inline-block bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs">
                                      {req.requirement_type}
                                    </span>
                                    {req.is_normative && (
                                      <span className="ml-1 inline-block bg-red-100 text-red-800 px-2 py-1 rounded text-xs">
                                        Normative
                                      </span>
                                    )}
                                  </div>
                                  <div className="text-sm text-gray-700 mb-2">{req.statement}</div>
                                  {(req.cross_references?.length || req.verification_method || req.applicable_phases?.length || req.notes?.length) && (
                                    <div className="text-xs text-gray-500 space-y-1">
                                      {req.cross_references && req.cross_references.length > 0 && (
                                        <div><span className="font-medium">Cross-refs:</span> {req.cross_references.join(', ')}</div>
                                      )}
                                      {req.verification_method && (
                                        <div><span className="font-medium">Verification:</span> {req.verification_method}</div>
                                      )}
                                      {req.applicable_phases && req.applicable_phases.length > 0 && (
                                        <div><span className="font-medium">Phases:</span> {req.applicable_phases.join(', ')}</div>
                                      )}
                                      {req.notes && req.notes.length > 0 && (
                                        <div><span className="font-medium">Notes:</span> {req.notes.join(' | ')}</div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Show message if no technical details available */}
                        {(!extResult.ecss_sections || extResult.ecss_sections.length === 0) &&
                         (!extResult.ecss_requirements || extResult.ecss_requirements.length === 0) &&
                         (!extResult.ecss_cross_references || extResult.ecss_cross_references.length === 0) &&
                         (!extResult.ecss_tables || extResult.ecss_tables.length === 0) &&
                         (!extResult.ecss_figures || extResult.ecss_figures.length === 0) &&
                         (!extResult.ecss_annexes || extResult.ecss_annexes.length === 0) &&
                         (!extResult.ecss_notes || extResult.ecss_notes.length === 0) && (
                          <div className="bg-blue-50 border border-blue-200 rounded-md p-4 text-center">
                            <div className="text-blue-800 font-medium mb-1">ℹ️ Basic Content Result</div>
                            <div className="text-blue-700 text-sm">
                              This result contains the core document content. Advanced ECSS technical metadata 
                              (sections, requirements, cross-references) may not be extracted for this particular content.
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
              );
            })}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <p>ECSS Standards Navigator - Powered by Morphik RAG</p>
          <p>European Cooperation for Space Standardization</p>
        </div>
      </footer>
    </div>
  );
}
