#!/usr/bin/env python3
"""
Enhanced ECSS API Server with Improved Search and Context
This server provides meaningful, contextual search results for ECSS standards.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from flask import Flask, request, jsonify
from flask_cors import CORS
from morphik import Morphik
import os
import sys
import json
import uuid
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enhanced CORS configuration
allowed_origins = [
    "https://ecss-hunt.onrender.com",
    "http://localhost:3000", 
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.6:3000",
    "https://ecss-hunt-frontend.vercel.app",
    "https://ecss-hunt.vercel.app"
]

# Configure CORS
if os.getenv('FLASK_DEBUG', 'False').lower() == 'true':
    CORS(app, origins="*")
else:
    CORS(app, 
         origins=allowed_origins,
         methods=["GET", "POST", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=False,
         max_age=86400)

logger.info(f"🌐 CORS configured for origins: {allowed_origins if not os.getenv('FLASK_DEBUG', 'False').lower() == 'true' else 'ALL (debug mode)'}")

@dataclass
class SearchResult:
    """Enhanced search result with context."""
    content: str
    summary: str
    relevance_score: float
    document_info: Dict
    source_type: str
    explanation: str

class EnhancedECSSSearch:
    """Enhanced search functionality for ECSS documents."""
    
    def __init__(self, morphik_uri: str):
        self.db = Morphik(uri=morphik_uri)
        
    def search_with_context(self, query: str, limit: int = 5) -> List[SearchResult]:
        """Search with enhanced context and explanations."""
        try:
            logger.info(f"🔍 Enhanced search for: '{query}'")
            
            # Retrieve chunks from Morphik
            chunks = self.db.retrieve_chunks(query, limit=limit * 2)  # Get more to filter
            
            results = []
            for chunk in chunks[:limit]:
                if hasattr(chunk, 'content') and chunk.content:
                    # Create enhanced result
                    result = self._create_enhanced_result(chunk, query)
                    if result:
                        results.append(result)
            
            logger.info(f"📊 Found {len(results)} enhanced results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Enhanced search failed: {e}")
            return []
    
    def _create_enhanced_result(self, chunk, query: str) -> Optional[SearchResult]:
        """Create an enhanced search result with context."""
        try:
            content = chunk.content.strip()
            if len(content) < 50:  # Skip very short content
                return None
            
            # Create summary
            summary = self._create_intelligent_summary(content)
            
            # Extract document info
            doc_info = self._extract_document_info(chunk)
            
            # Create explanation
            explanation = self._create_explanation(content, query)
            
            # Determine source type
            source_type = self._determine_source_type(content)
            
            return SearchResult(
                content=content,
                summary=summary,
                relevance_score=getattr(chunk, 'score', 0.0),
                document_info=doc_info,
                source_type=source_type,
                explanation=explanation
            )
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create enhanced result: {e}")
            return None
    
    def _create_intelligent_summary(self, content: str) -> str:
        """Create an intelligent summary of the content."""
        if len(content) <= 200:
            return content
        
        # Look for key ECSS patterns
        if "shall" in content.lower():
            # This is likely a requirement
            sentences = content.split('. ')
            for sentence in sentences[:3]:
                if "shall" in sentence.lower():
                    return sentence.strip() + "..."
        
        # Look for definitions
        if any(word in content.lower() for word in ["definition", "means", "defined as"]):
            sentences = content.split('. ')
            return '. '.join(sentences[:2]) + "..."
        
        # Default summary
        sentences = content.split('. ')
        summary = '. '.join(sentences[:2])
        return summary + "..." if len(summary) < len(content) else summary
    
    def _extract_document_info(self, chunk) -> Dict:
        """Extract document information from chunk metadata."""
        metadata = getattr(chunk, 'metadata', {})
        
        # Try to extract ECSS standard ID from content or metadata
        content = getattr(chunk, 'content', '')
        standard_id = self._extract_ecss_id(content)
        
        return {
            'filename': metadata.get('filename', 'Unknown'),
            'page': metadata.get('page_label', 'Unknown'),
            'standard_id': standard_id,
            'source': metadata.get('source', 'ECSS Standards'),
            'file_size': metadata.get('file_size', 0),
            'last_modified': metadata.get('last_modified_date', 'Unknown')
        }
    
    def _extract_ecss_id(self, content: str) -> str:
        """Extract ECSS standard ID from content."""
        import re
        
        # Pattern for ECSS IDs like ECSS-E-ST-10C
        pattern = r'ECSS-[A-Z]-[A-Z]{2,3}-\d+[A-Z]?(?:-Rev\.\d+)?'
        match = re.search(pattern, content)
        
        if match:
            return match.group(0)
        
        # Fallback pattern
        pattern = r'ECSS[- ][A-Z][- ][A-Z]{2,3}[- ]\d+'
        match = re.search(pattern, content)
        
        return match.group(0) if match else "Unknown"
    
    def _create_explanation(self, content: str, query: str) -> str:
        """Create an explanation of why this result is relevant."""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Check for different types of content
        if "shall" in content_lower:
            return f"This contains requirements related to your query about '{query}'"
        elif any(word in content_lower for word in ["procedure", "process", "method"]):
            return f"This describes procedures or methods relevant to '{query}'"
        elif any(word in content_lower for word in ["definition", "terminology", "glossary"]):
            return f"This provides definitions or terminology related to '{query}'"
        elif any(word in content_lower for word in ["test", "verification", "validation"]):
            return f"This covers testing or verification aspects of '{query}'"
        elif any(word in content_lower for word in ["table", "figure", "appendix"]):
            return f"This contains reference material (tables/figures) for '{query}'"
        else:
            return f"This provides general information about '{query}'"
    
    def _determine_source_type(self, content: str) -> str:
        """Determine the type of source content."""
        content_lower = content.lower()
        
        if "shall" in content_lower:
            return "requirement"
        elif any(word in content_lower for word in ["procedure", "step", "process"]):
            return "procedure"
        elif any(word in content_lower for word in ["definition", "terminology"]):
            return "definition"
        elif any(word in content_lower for word in ["table", "figure"]):
            return "reference"
        elif any(word in content_lower for word in ["test", "verification"]):
            return "verification"
        else:
            return "general"

# Initialize the enhanced search system
def get_enhanced_search():
    """Get enhanced search client instance."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        logger.error("⚠ MORPHIK_URI not set in .env file")
        return None
    
    try:
        return EnhancedECSSSearch(morphik_uri)
    except Exception as e:
        logger.error(f"✗ Failed to connect to Morphik: {e}")
        return None

# Handle preflight OPTIONS requests
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    """Handle CORS preflight requests."""
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/search', methods=['GET'])
def enhanced_search():
    """Enhanced search endpoint with contextual results."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 5)), 10)
    
    # Performance optimization: Early validation
    if not query.strip() or len(query.strip()) < 2:
        return jsonify({
            'results': [],
            'total': 0,
            'query': query,
            'message': 'Query too short. Please provide at least 2 characters.',
            'search_type': 'enhanced_ecss_search',
            'processing_time_ms': 0
        })
    
    start_time = time.time()
    
    # Get enhanced search client
    search_client = get_enhanced_search()
    if not search_client:
        return jsonify({
            'error': 'Search service unavailable',
            'message': 'Unable to connect to the ECSS knowledge base',
            'query': query
        }), 503
    
    try:
        logger.info(f"🔍 Processing enhanced search: '{query}'")
        
        # Perform enhanced search
        search_results = search_client.search_with_context(query, limit)
        
        # Convert to API response format
        api_results = []
        for i, result in enumerate(search_results):
            api_result = {
                'id': f'enhanced-{uuid.uuid4().hex[:8]}',
                'title': f"{result.document_info['standard_id']} - {result.source_type.title()}",
                'content': result.content,
                'summary': result.summary,
                'explanation': result.explanation,
                'score': result.relevance_score,
                'relevance': min(result.relevance_score * 100, 100),  # Convert to percentage
                'metadata': {
                    'document': result.document_info,
                    'source_type': result.source_type,
                    'content_length': len(result.content),
                    'rank': i + 1
                }
            }
            api_results.append(api_result)
        
        processing_time = (time.time() - start_time) * 1000
        
        response = {
            'results': api_results,
            'total': len(api_results),
            'query': query,
            'search_type': 'enhanced_ecss_search',
            'processing_time_ms': round(processing_time, 2),
            'message': f'Found {len(api_results)} contextual results for your ECSS query',
            'tips': [
                'Results are ranked by relevance to your query',
                'Each result includes an explanation of why it\'s relevant',
                'Look for the source type to understand the content better'
            ]
        }
        
        # Add branch filter info if provided
        if branch:
            response['filter_applied'] = f'Branch: {branch}'
        
        logger.info(f"✅ Enhanced search completed: {len(api_results)} results in {processing_time:.1f}ms")
        return jsonify(response)
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"❌ Enhanced search failed: {e}")
        
        return jsonify({
            'error': 'Search failed',
            'message': 'An error occurred while searching the ECSS knowledge base',
            'query': query,
            'processing_time_ms': round(processing_time, 2),
            'debug_info': str(e) if os.getenv('FLASK_DEBUG') else None
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """API status endpoint."""
    search_client = get_enhanced_search()
    
    return jsonify({
        'status': 'operational' if search_client else 'degraded',
        'service': 'Enhanced ECSS Search API',
        'version': '2.0',
        'features': [
            'Contextual search results',
            'Intelligent summaries',
            'Source type classification',
            'Relevance explanations',
            'ECSS standard identification'
        ],
        'endpoints': {
            'search': 'GET /api/search?q=<query>&branch=<branch>&limit=<limit>',
            'status': 'GET /api/status'
        },
        'search_client_status': 'connected' if search_client else 'disconnected'
    })

@app.route('/api/search/suggestions', methods=['GET'])
def search_suggestions():
    """Provide search suggestions for ECSS queries."""
    suggestions = [
        "software development requirements",
        "verification and validation procedures",
        "testing methods and protocols",
        "quality assurance standards",
        "project management guidelines",
        "risk management procedures",
        "configuration management",
        "documentation requirements",
        "review and audit processes",
        "training and qualification"
    ]
    
    return jsonify({
        'suggestions': suggestions,
        'categories': {
            'Requirements': [
                "software requirements",
                "hardware requirements", 
                "system requirements"
            ],
            'Procedures': [
                "testing procedures",
                "verification procedures",
                "validation procedures"
            ],
            'Management': [
                "project management",
                "configuration management",
                "risk management"
            ]
        }
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'message': 'Enhanced ECSS Standards API',
        'description': 'Advanced search and retrieval for ECSS standards with contextual results',
        'version': '2.0',
        'documentation': '/api/status',
        'search_endpoint': '/api/search?q=<your_query>',
        'features': [
            'Contextual search results',
            'Intelligent content summaries',
            'Source type classification',
            'Relevance explanations'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Starting Enhanced ECSS API Server")
    logger.info(f"🌐 Port: {port}")
    logger.info(f"🔧 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 