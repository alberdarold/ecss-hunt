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

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // Build query string for filters
      const params = new URLSearchParams({
        q: query.trim(),
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
      handleSearch();
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
                onClick={handleSearch}
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
              <span className={styles.spinner}>⏳</span>
              Searching ECSS standards...
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
              return (
                <>
                  <div key={result.id || index} className="bg-white rounded-lg shadow-md p-6 mb-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-sm font-medium text-gray-600">
                            {result.metadata?.document_name || 'Unknown Document'}
                          </span>
                          {result.metadata?.entity_type && (
                            <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                              {result.metadata.entity_type}
                            </span>
                          )}
                          {result.metadata?.retrieval_method && (
                            <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                              {result.metadata.retrieval_method}
                            </span>
                          )}
                          {result.metadata?.visual_confidence && (
                            <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full">
                              Visual: {Math.round(result.metadata.visual_confidence * 100)}%
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-500 mb-2">
                          Relevance: {typeof result.score === 'number' ? Math.round(result.score * 100) : 'N/A'}%
                        </div>
                      </div>
                    </div>
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>{result.content}</ReactMarkdown>
                    </div>
                    {/* Expand/collapse for rich ECSS metadata */}
                    <button
                      className="mt-2 text-blue-600 underline text-xs"
                      onClick={() => setExpandedResult(expandedResult === index ? null : index)}
                    >
                      {expandedResult === index ? 'Hide details' : 'Show ECSS details'}
                    </button>
                    {expandedResult === index && (
                      <div className="mt-4 border-t pt-4 text-xs text-gray-700">
                        {/* Sections */}
                        {extResult.ecss_sections && extResult.ecss_sections.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Sections</h4>
                            <ul className="mb-2">
                              {extResult.ecss_sections.map((sec, i) => (
                                <li key={i}>
                                  <b>{sec.section_number} {sec.section_title}</b> [{sec.section_type}] {sec.is_normative ? 'Normative' : sec.is_informative ? 'Informative' : ''}<br/>
                                  {sec.content_summary && <span>Summary: {sec.content_summary}<br/></span>}
                                  <span>Req: {sec.requirements_count} | Rec: {sec.recommendations_count} | Perm: {sec.permissions_count} | Figs: {sec.figures_count} | Tables: {sec.tables_count}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Requirements */}
                        {extResult.ecss_requirements && extResult.ecss_requirements.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Requirements / Recommendations / Permissions</h4>
                            <ul className="mb-2">
                              {extResult.ecss_requirements.map((req, i) => (
                                <li key={i}>
                                  <b>{req.unique_id}</b> [{req.requirement_type}] {req.is_normative ? 'Normative' : ''}<br/>
                                  {req.statement}<br/>
                                  {req.cross_references && req.cross_references.length > 0 && (
                                    <span>Cross-refs: {req.cross_references.join(', ')}<br/></span>
                                  )}
                                  {req.verification_method && <span>Verification: {req.verification_method}<br/></span>}
                                  {req.applicable_phases && req.applicable_phases.length > 0 && (
                                    <span>Phases: {req.applicable_phases.join(', ')}<br/></span>
                                  )}
                                  {req.notes && req.notes.length > 0 && (
                                    <span>Notes: {req.notes.join(' | ')}<br/></span>
                                  )}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Cross-references */}
                        {extResult.ecss_cross_references && extResult.ecss_cross_references.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Cross-References</h4>
                            <ul className="mb-2">
                              {extResult.ecss_cross_references.map((xref, i) => (
                                <li key={i}>
                                  <b>{xref.source_id}</b> → {xref.target} [{xref.target_type}] {xref.context && <span>({xref.context})</span>}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Annexes */}
                        {extResult.ecss_annexes && extResult.ecss_annexes.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Annexes</h4>
                            <ul className="mb-2">
                              {extResult.ecss_annexes.map((annex, i) => (
                                <li key={i}>
                                  <b>{annex.annex_id}</b>: {annex.title} {annex.is_normative ? '(Normative)' : ''}<br/>
                                  {annex.content_summary}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Notes */}
                        {extResult.ecss_notes && extResult.ecss_notes.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Notes</h4>
                            <ul className="mb-2">
                              {extResult.ecss_notes.map((note, i) => (
                                <li key={i}>
                                  <b>{note.note_id}</b> (to {note.related_to}): {note.content}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Tables */}
                        {extResult.ecss_tables && extResult.ecss_tables.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Tables</h4>
                            <ul className="mb-2">
                              {extResult.ecss_tables.map((table, i) => (
                                <li key={i}>
                                  <b>{table.table_number}</b>: {table.table_title} [{table.table_type}]<br/>
                                  Rows: {table.row_count}, Cols: {table.column_count}<br/>
                                  {table.content_summary && <span>Summary: {table.content_summary}<br/></span>}
                                  {table.key_parameters && table.key_parameters.length > 0 && (
                                    <span>Key Params: {table.key_parameters.join(', ')}<br/></span>
                                  )}
                                  {table.section_number && <span>Section: {table.section_number}</span>}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* Figures */}
                        {extResult.ecss_figures && extResult.ecss_figures.length > 0 && (
                          <div>
                            <h4 className="font-bold mb-1">Figures</h4>
                            <ul className="mb-2">
                              {extResult.ecss_figures.map((fig, i) => (
                                <li key={i}>
                                  <b>{fig.figure_number}</b>: {fig.figure_title} [{fig.diagram_type}]<br/>
                                  {fig.content_description && <span>{fig.content_description}<br/></span>}
                                  {fig.components && fig.components.length > 0 && (
                                    <span>Components: {fig.components.join(', ')}<br/></span>
                                  )}
                                  {fig.relationships && fig.relationships.length > 0 && (
                                    <span>Relationships: {fig.relationships.join(', ')}<br/></span>
                                  )}
                                  {fig.section_number && <span>Section: {fig.section_number}</span>}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </>
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
