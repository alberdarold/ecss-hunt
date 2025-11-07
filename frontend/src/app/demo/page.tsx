'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { searchAPI, systemAPI } from '../../utils/api';
import { SearchResult, SearchFilters, SystemStatusResponse, SearchResponse } from '../../types/api';
import { verifyToken, getSession, logout, extractTokenFromURL, clearTokenFromURL, getLocalAuthInfo, createCheckout, getToolId, check1SubAuth } from '../../utils/auth';

export default function DemoPage() {
  const [searchState, setSearchState] = useState({
    query: '',
    isLoading: false,
    error: null as string | null,
  });

  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);
  const [documentSources, setDocumentSources] = useState<string[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatusResponse | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [debounceTimer, setDebounceTimer] = useState<NodeJS.Timeout | null>(null);
  
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isVerifying, setIsVerifying] = useState(true);
  const [creditsRemaining, setCreditsRemaining] = useState<number | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);
  
  useEffect(() => {
    // Check for token in URL first
    const token = extractTokenFromURL();
    if (token) {
      handleTokenVerification(token);
    } else {
      // Check existing session with timeout fallback
      checkExistingSession();
      
      // Fallback: If session check takes too long, show purchase button
      const fallbackTimer = setTimeout(() => {
        console.log('Session check timeout - showing purchase option');
        setIsVerifying(false);
        setIsAuthenticated(false);
      }, 3000); // 3 seconds fallback - faster UX
      
      return () => clearTimeout(fallbackTimer);
    }
    checkSystemStatus();
  }, []);

  // Debounce Enter-less typing to auto-search after pause (optional UX speed)
  useEffect(() => {
    // Only auto-search when query is sufficiently long
    const q = searchState.query.trim();
    if (!q || q.length < 3) return;
    if (searchState.isLoading) return;
    if (debounceTimer) clearTimeout(debounceTimer);
    const t = setTimeout(() => {
      handleSearch(q);
    }, 500);
    setDebounceTimer(t);
    return () => clearTimeout(t);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchState.query]);

  const handleTokenVerification = async (token: string) => {
    setIsVerifying(true);
    setAuthError(null);
    
    try {
      const result = await verifyToken(token);
      
      if (result.success) {
        setIsAuthenticated(true);
        // Clear token from URL
        clearTokenFromURL();
        // Refresh session to get latest info
        await checkExistingSession();
      } else {
        setIsAuthenticated(false);
        setAuthError(result.message || 'Token verification failed');
      }
    } catch (error) {
      console.error('Token verification error:', error);
      setIsAuthenticated(false);
      setAuthError('Failed to verify token. Please try again.');
    } finally {
      setIsVerifying(false);
    }
  };

  const checkExistingSession = async () => {
    setIsVerifying(true);
    
    try {
      // Add timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Session check timeout')), 5000)
      );
      
      const session = await Promise.race([
        getSession(),
        timeoutPromise
      ]) as any;
      
      setIsAuthenticated(session.authenticated || false);
      if (!session.authenticated) {
        setAuthError(null);
      }
    } catch (error) {
      console.error('Session check error:', error);
      setIsAuthenticated(false);
      setAuthError(null); // Clear any previous errors
    } finally {
      setIsVerifying(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    setIsAuthenticated(false);
    setCreditsRemaining(null);
    setAuthError(null);
    setAiResponse(null);
    setDocumentSources([]);
  };

  const handlePurchase = async () => {
    try {
      setIsVerifying(true);
      setAuthError(null);
      
      // Get tool_id from backend config
      const toolId = await getToolId();
      
      // Check if user is authenticated with 1sub.io
      const isAuthenticated = await check1SubAuth();
      
      if (isAuthenticated) {
        // User is authenticated - create checkout directly
        try {
          const checkout = await createCheckout(toolId);
          // Redirect to checkout page
          window.location.href = checkout.checkout_url;
        } catch (checkoutError: any) {
          // Handle 401 from checkout creation
          if (checkoutError.status === 401 || checkoutError.needsLogin) {
            // Not authenticated - redirect to login
            window.location.href = 'https://1sub.io/login?redirect=/backoffice';
          } else {
            throw checkoutError;
          }
        }
      } else {
        // User is not authenticated - redirect to login
        window.location.href = 'https://1sub.io/login?redirect=/backoffice';
      }
    } catch (error: any) {
      console.error('Purchase error:', error);
      // If error getting tool_id or other issues, still try to redirect to login
      if (error.message?.includes('tool ID')) {
        setAuthError('Configuration error. Please contact support.');
        setIsVerifying(false);
      } else {
        // Fallback: redirect to login
        window.location.href = 'https://1sub.io/login?redirect=/backoffice';
      }
    }
  };

  const checkSystemStatus = async () => {
    try {
      const status = await systemAPI.getStatus();
      setSystemStatus(status);
      setIsConnected(status.connection === 'connected');
    } catch (error: any) {
      console.error('System status check failed:', error);
      setIsConnected(false);
      // Set a helpful status message if it's a network error
      if (error?.isNetworkError) {
        setSystemStatus({
          connection: 'disconnected',
          features: {
            agent_query: false,
            batch_operations: false,
            colpali_visual: false,
            document_access: false,
            knowledge_graphs: false,
            standard_query: false,
          },
          system: 'Error',
          timestamp: Date.now(),
        });
      }
    }
  };

  const handleSearch = async (query: string) => {
    if (!query.trim()) return;
    if (searchState.isLoading) return; // avoid overlapping queries
    
    // Check authentication
    if (!isAuthenticated) {
      setAuthError('Please purchase access to use the search feature.');
      return;
    }

    setSearchState(prev => ({ ...prev, isLoading: true, error: null }));
    setAuthError(null);
    setAiResponse(null);
    setProcessingTime(null);
    setDocumentSources([]);

    try {
      const filters: SearchFilters = {
        query: query.trim(),
        limit: 1, // Only need 1 for AI response
        include_visual: false,
      };

      const response = await searchAPI.search(filters);
      
      // Update credits remaining if provided
      if (response.credits_remaining !== undefined) {
        setCreditsRemaining(response.credits_remaining);
      }
      
      // Extract AI response and document sources
      if (response.ai_response) {
        setAiResponse(response.ai_response);
        setProcessingTime(response.processing_time || null);
        setDocumentSources(response.document_sources || []);
      } else {
        setAiResponse("No AI response available for this query. Please try a different search term.");
        setDocumentSources([]);
      }
      
      setSearchState(prev => ({
        ...prev,
        query,
        isLoading: false,
        error: null,
      }));

    } catch (error: any) {
      // Check for insufficient credits error
      if (error.error === 'insufficient_credits' || error.message?.includes('insufficient')) {
        setAuthError('Insufficient credits. Please purchase more credits to continue.');
        setCreditsRemaining(error.current_balance || 0);
        // Redirect to purchase page after showing error
        setTimeout(async () => {
          try {
            const toolId = await getToolId();
            const isAuthenticated = await check1SubAuth();
            
            if (isAuthenticated) {
              try {
                const checkout = await createCheckout(toolId);
                window.location.href = checkout.checkout_url;
              } catch (checkoutError: any) {
                if (checkoutError.status === 401 || checkoutError.needsLogin) {
                  window.location.href = 'https://1sub.io/login?redirect=/backoffice';
                } else {
                  throw checkoutError;
                }
              }
            } else {
              window.location.href = 'https://1sub.io/login?redirect=/backoffice';
            }
          } catch (checkoutError) {
            console.error('Failed to create checkout:', checkoutError);
            // Fallback: redirect to login
            window.location.href = 'https://1sub.io/login?redirect=/backoffice';
          }
        }, 3000);
      } else if (error.status === 401) {
        // Session expired
        setIsAuthenticated(false);
        setAuthError('Your session has expired. Please authenticate again.');
        await checkExistingSession();
      } else {
        setSearchState(prev => ({
          ...prev,
          isLoading: false,
          error: error.message || 'Search failed',
        }));
      }
      setAiResponse(null);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="bg-card/80 backdrop-blur-md border-b border-border">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-background" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  ECSS Navigator
                </h1>
                <p className="text-sm text-muted-foreground">
                  AI-Powered ECSS Document Search • Live Demo
                </p>
              </div>
            </Link>
            
            <div className="flex items-center gap-4">
              <Link 
                href="/"
                className="text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Home
              </Link>
              
              {/* Authentication Status */}
              {isVerifying ? (
                <div className="text-xs text-muted-foreground flex items-center gap-2">
                  <div className="animate-spin rounded-full h-3 w-3 border-2 border-muted-foreground border-t-transparent"></div>
                  <span>Verifying...</span>
                </div>
              ) : isAuthenticated ? (
                <div className="flex items-center gap-4">
                  {creditsRemaining !== null && (
                    <div className="text-xs text-muted-foreground">
                      <div className="font-medium text-foreground">Credits: {creditsRemaining.toFixed(2)}</div>
                      <div className="text-xs">0.01 per search</div>
                    </div>
                  )}
                  <button
                    onClick={handleLogout}
                    className="text-xs text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <button
                  onClick={handlePurchase}
                  disabled={isVerifying}
                  className="px-4 py-2 bg-gradient-primary text-background rounded-lg hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium text-sm"
                >
                  {isVerifying ? 'Loading...' : 'Purchase Access'}
                </button>
              )}
              
              {systemStatus && (
                <div className="text-xs text-muted-foreground text-right">
                  <div className="flex items-center gap-1">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-accent' : 'bg-destructive'}`}></div>
                    <span>{isConnected ? 'Connected' : 'Offline'}</span>
                  </div>
                  <div>AI Search: {isAuthenticated ? 'Enabled' : 'Requires Auth'}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Search Section */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-card/50 backdrop-blur-sm rounded-lg p-8 mb-8 border border-border shadow-card">
            <div className="relative">
              <input
                type="text"
                placeholder="Ask about ECSS standards, requirements, or procedures..."
                value={searchState.query}
                onChange={(e) => setSearchState(prev => ({ ...prev, query: e.target.value }))}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleSearch(searchState.query);
                  }
                }}
                className="w-full pl-12 pr-4 py-4 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-card text-foreground text-lg placeholder:text-muted-foreground"
              />
              <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
                <svg className="w-5 h-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <div className="flex items-center justify-between mt-4">
              <div className="flex items-center gap-4">
                <span className="text-sm text-muted-foreground flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Ask about ECSS requirements, procedures, or standards
                </span>
              </div>

              <button
                onClick={() => handleSearch(searchState.query)}
                disabled={searchState.isLoading || !searchState.query.trim() || !isAuthenticated || isVerifying}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-primary text-background rounded-lg hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium"
              >
                {searchState.isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-background border-t-transparent"></div>
                    <span>Searching...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <span>Ask AI</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Authentication Error Display */}
          {authError && (
            <div className="max-w-4xl mx-auto mb-6">
              <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                    <p className="text-destructive">{authError}</p>
                  </div>
                  {!isAuthenticated && (
                    <button
                      onClick={handlePurchase}
                      disabled={isVerifying}
                      className="px-4 py-2 bg-gradient-primary text-background rounded-lg hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium text-sm"
                    >
                      {isVerifying ? 'Loading...' : 'Purchase Access'}
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {searchState.error && (
            <div className="max-w-4xl mx-auto mb-6">
              <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <p className="text-destructive">{searchState.error}</p>
                </div>
              </div>
            </div>
          )}

          {/* AI Response */}
          {aiResponse && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-card/50 backdrop-blur-sm border border-border rounded-lg p-6 shadow-card">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center">
                    <svg className="w-5 h-5 text-background" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">
                      AI Response
                    </h3>
                    {processingTime && (
                      <p className="text-sm text-muted-foreground">
                        Generated in {processingTime.toFixed(1)}s
                      </p>
                    )}
                  </div>
                </div>
                
                <div 
                  className="text-foreground leading-relaxed prose prose-sm max-w-none prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-code:text-foreground"
                  style={{ lineHeight: '1.6' }}
                  dangerouslySetInnerHTML={{ __html: aiResponse }}
                />
                
                {/* Document Sources */}
                {documentSources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-border">
                    <div className="flex items-center gap-2 mb-2">
                      <svg className="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span className="text-sm font-medium text-foreground">Source Documents:</span>
                    </div>
                    <div className="space-y-1">
                      {documentSources.slice(0, 5).map((source, index) => (
                        <div key={index} className="text-xs text-muted-foreground flex items-center gap-2">
                          <span className="w-1 h-1 bg-accent rounded-full"></span>
                          {source}
                        </div>
                      ))}
                      {documentSources.length > 5 && (
                        <div className="text-xs text-muted-foreground flex items-center gap-2">
                          <span className="w-1 h-1 bg-accent rounded-full"></span>
                          ... and {documentSources.length - 5} more documents
                        </div>
                      )}
                    </div>
                  </div>
                )}
                
                <div className="mt-4 pt-4 border-t border-border">
                  <p className="text-xs text-muted-foreground flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    This response is based on ECSS standards and requirements from the processed documents.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* No Results Message */}
          {!searchState.isLoading && !aiResponse && searchState.query && !searchState.error && !authError && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-card/50 backdrop-blur-sm border border-border rounded-lg p-6 text-center">
                <div className="text-muted-foreground">
                  <svg className="w-12 h-12 mx-auto mb-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <p>Enter a search query above to get AI-powered responses about ECSS standards.</p>
                </div>
              </div>
            </div>
          )}

          {/* Not Authenticated Message */}
          {!isVerifying && !isAuthenticated && !searchState.query && !authError && (
            <div className="max-w-4xl mx-auto mt-8">
              <div className="bg-card/50 backdrop-blur-sm border border-border rounded-lg p-6 text-center">
                <div className="text-muted-foreground">
                  <svg className="w-12 h-12 mx-auto mb-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  <h3 className="text-lg font-semibold text-foreground mb-2">Authentication Required</h3>
                  <p className="mb-4">Please purchase access to use the ECSS Navigator search feature.</p>
                  <button
                    onClick={handlePurchase}
                    disabled={isVerifying}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-primary text-background rounded-lg hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium"
                  >
                    {isVerifying ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-background border-t-transparent"></div>
                        Creating checkout...
                      </>
                    ) : (
                      'Purchase Access'
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Example Queries */}
          {!searchState.isLoading && !aiResponse && !searchState.query && (
            <div className="max-w-4xl mx-auto mt-8">
              <div className="bg-card/50 backdrop-blur-sm rounded-lg p-6 border border-border shadow-card">
                <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Try these example queries:
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {[
                    "What are the main objectives of ECSS-E-ST-10-02C?",
                    "What are the requirements for thermal analysis in ECSS-E-ST-31C?",
                    "What are the configuration management requirements in ECSS-E standards?",
                    "List the quality assurance activities required by ECSS-E-ST-10-02C.",
                    "How does ECSS define redundancy in spacecraft design?",
                    "Explain the process for functional testing of spacecraft systems in ECSS."
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSearchState(prev => ({ ...prev, query: example }));
                        handleSearch(example);
                      }}
                      className="text-left p-3 bg-card rounded-lg hover:bg-card/80 transition-colors text-sm text-foreground border border-border hover:border-primary/50"
                    >
                      "{example}"
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 