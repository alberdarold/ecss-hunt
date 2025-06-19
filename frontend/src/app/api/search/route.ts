import { NextRequest, NextResponse } from 'next/server';

// Types for our search results
interface SearchResult {
  id: string;
  title: string;
  content: string;
  score: number;
  metadata: {
    branch?: string;
    branch_name?: string;
    discipline?: string;
    discipline_name?: string;
    document_number?: string;
    revision?: string;
    filename?: string;
    document_type?: string;
    source?: string;
  };
}

// Mock data for demonstration when Morphik is not available
const mockResults: SearchResult[] = [
  {
    id: '1',
    title: 'ECSS-S-ST-00C Rev.1(15June2020)',
    content: 'This document provides a comprehensive overview of ECSS standards and their application in space systems. It covers the fundamental principles, requirements, and guidelines for implementing ECSS standards across various space projects.',
    score: 0.95,
    metadata: {
      branch: 'S',
      branch_name: 'Space Product Assurance',
      discipline: 'ST',
      discipline_name: 'Space Systems',
      document_number: '00C',
      revision: '1',
      filename: 'ECSS-S-ST-00C Rev.1(15June2020).pdf',
      document_type: 'ECSS_Standard',
      source: 'ECSS_Published_Standards'
    }
  },
  {
    id: '2',
    title: 'ECSS-Q-ST-70C-Rev.2(15October2019)',
    content: 'Materials and processes standards for space applications. This document specifies requirements for materials selection, testing procedures, and quality assurance processes used in space systems.',
    score: 0.87,
    metadata: {
      branch: 'Q',
      branch_name: 'Quality Assurance',
      discipline: 'ST',
      discipline_name: 'Space Systems',
      document_number: '70C',
      revision: '2',
      filename: 'ECSS-Q-ST-70C-Rev.2(15October2019).pdf',
      document_type: 'ECSS_Standard',
      source: 'ECSS_Published_Standards'
    }
  },
  {
    id: '3',
    title: 'ECSS-E-ST-50C-Rev.1(1March2021)',
    content: 'Communication protocols and standards for space systems. This document defines the requirements for communication systems, data transmission protocols, and interface specifications.',
    score: 0.82,
    metadata: {
      branch: 'E',
      branch_name: 'Engineering',
      discipline: 'ST',
      discipline_name: 'Space Systems',
      document_number: '50C',
      revision: '1',
      filename: 'ECSS-E-ST-50C-Rev.1(1March2021).pdf',
      document_type: 'ECSS_Standard',
      source: 'ECSS_Published_Standards'
    }
  }
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('q') || '';
  const branch = searchParams.get('branch') || '';
  const discipline = searchParams.get('discipline') || '';
  const revision = searchParams.get('revision') || '';

  if (!query.trim()) {
    return NextResponse.json({ results: [], total: 0 });
  }

  try {
    // For now, use mock data since Morphik is not available in frontend
    // In a production environment, you would make HTTP requests to your backend API
    console.log('Using mock data for demonstration');
    
    // Filter mock results based on query
    const filteredMockResults = mockResults.filter(result => 
      result.title.toLowerCase().includes(query.toLowerCase()) ||
      result.content.toLowerCase().includes(query.toLowerCase())
    );
    
    // Apply additional filters
    let finalResults = filteredMockResults;
    
    if (branch) {
      finalResults = finalResults.filter((r: SearchResult) => r.metadata.branch === branch);
    }
    
    if (discipline) {
      finalResults = finalResults.filter((r: SearchResult) => r.metadata.discipline === discipline);
    }
    
    if (revision) {
      finalResults = finalResults.filter((r: SearchResult) => r.metadata.revision === revision);
    }
    
    return NextResponse.json({
      results: finalResults,
      total: finalResults.length
    });
    
  } catch (error) {
    console.error('Search error:', error);
    
    // Return mock data on error
    return NextResponse.json({
      results: mockResults.slice(0, 2),
      total: 2,
      error: 'Using mock data due to API error'
    });
  }
} 