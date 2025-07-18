import { NextRequest, NextResponse } from 'next/server';

// Get the backend API URL from environment
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q');
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter "q" is required' },
        { status: 400 }
      );
    }

    // Get additional parameters
    const limit = searchParams.get('limit') || '5';
    const includeVisual = searchParams.get('include_visual') || 'true';
    const minScore = searchParams.get('min_score');

    // Build parameters for backend API
    const backendParams = new URLSearchParams({
      q: query,
      limit: limit,
      include_visual: includeVisual,
    });

    if (minScore) {
      backendParams.append('min_score', minScore);
    }

    // Call the backend foundation system API
    const backendUrl = `${BACKEND_API_URL}/api/search?${backendParams.toString()}`;
    
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Return the backend response directly (it already has the correct format)
    return NextResponse.json(data);

  } catch (error) {
    console.error('Search API error:', error);
    
    // Return error response
    return NextResponse.json(
      { 
        error: 'Search failed', 
        message: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
} 