'use client';

import { useState } from 'react';
import styles from './page.module.css';

interface SearchResult {
  id: string;
  content: string;
  metadata: {
    document_name: string;
    branch: string;
    discipline: string;
    revision: string;
    section: string;
    requirement_id?: string;
    page_number: number;
  };
  score: number;
}

interface SearchFilters {
  branch: string;
  discipline: string;
  revision: string;
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

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          filters
        }),
      });

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
    return Math.round(score * 100);
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
            {results.map((result, index) => (
              <div key={result.id} className={styles.resultCard}>
                <div className={styles.resultHeader}>
                  <div className={styles.resultMeta}>
                    <span 
                      className={styles.disciplineBadge}
                      style={{ backgroundColor: getDisciplineColor(result.metadata.discipline) }}
                    >
                      {result.metadata.discipline}
                    </span>
                    <span className={styles.documentName}>
                      {result.metadata.document_name}
                    </span>
                    <span className={styles.section}>
                      Section {result.metadata.section}
                    </span>
                    {result.metadata.requirement_id && (
                      <span className={styles.requirementId}>
                        {result.metadata.requirement_id}
                      </span>
                    )}
                  </div>
                  <div className={styles.resultScore}>
                    <span className={styles.scoreLabel}>Relevance</span>
                    <span className={styles.scoreValue}>{formatScore(result.score)}%</span>
                  </div>
                </div>
                
                <div className={styles.resultContent}>
                  <p>{result.content}</p>
                </div>

                <div className={styles.resultFooter}>
                  <span className={styles.pageInfo}>
                    Page {result.metadata.page_number}
                  </span>
                  <span className={styles.branchInfo}>
                    Branch {result.metadata.branch} • Rev {result.metadata.revision}
                  </span>
                </div>
              </div>
            ))}
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
