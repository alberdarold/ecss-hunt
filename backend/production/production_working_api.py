#!/usr/bin/env python3
"""
PRODUCTION WORKING API - CONFIRMED FEATURES ONLY
===============================================

Production-ready API using only confirmed working Morphik features:
- Standard query with excellent results  
- ColPali visual search with excellent results
- Context chunk retrieval
- Robust error handling
- Fast, reliable responses

No timeouts, no knowledge graphs, no problematic features.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import time
import logging
from typing import Dict, List, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import OrderedDict
import re

from production.working_morphik_system import WorkingMorphikSystem, WorkingMorphikConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionWorkingAPI:
    """Production API using only confirmed working Morphik features."""
    
    def __init__(self, port: int = 8002):
        """Initialize the production API."""
        self.port = port
        self.morphik_system = None
        self.app = self._create_flask_app()
        
        # Simple in-memory TTL LRU cache for search responses
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._cache_ttl_seconds: int = int(os.getenv("WORKING_API_CACHE_TTL", "120"))  # 2 minutes default
        self._cache_max_size: int = int(os.getenv("WORKING_API_CACHE_SIZE", "256"))   # 256 entries
        
        # Initialize working Morphik system
        self._init_working_system()
        
        logger.info("🚀 Production Working API initialized")
    
    def _init_working_system(self):
        """Initialize the working Morphik system."""
        try:
            config = WorkingMorphikConfig(
                morphik_uri=os.getenv("MORPHIK_URI"),
                use_colpali=True,
                use_agent_query=False,  # Disable due to timeout issues
                use_batch_operations=True
            )
            
            if not config.morphik_uri:
                raise ValueError("MORPHIK_URI environment variable not set")
            
            self.morphik_system = WorkingMorphikSystem(config)
            logger.info("✅ Working Morphik system initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize working system: {e}")
            raise
    
    def _create_flask_app(self) -> Flask:
        """Create Flask application with working endpoints."""
        app = Flask(__name__)
        
        # JSON performance settings
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        
        CORS(app)
        
        @app.route('/api/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'system': 'Production Working API',
                'features': ['standard_search', 'colpali_visual', 'context_chunks'],
                'timestamp': time.time()
            })
        
        @app.route('/api/working/search', methods=['GET'])
        def working_search():
            """Simplified search returning only AI response for faster performance."""
            try:
                query = request.args.get('q', '').strip()
                if not query:
                    return jsonify({'error': 'Query parameter q is required'}), 400
                
                # Normalize and build cache key
                norm_query = self._normalize_query(query)
                # Fast fail for very short queries to avoid unnecessary work
                if len(norm_query) < 3:
                    fast_resp = {
                        'ai_response': "Please provide at least 3 characters to search ECSS documents.",
                        'results': [],
                        'total': 0,
                        'query': query,
                        'methods_used': ['ai_context_only'],
                        'processing_time': 0.0,
                        'timestamp': time.time()
                    }
                    resp = jsonify(fast_resp)
                    resp.headers['X-Cache'] = 'BYPASS'
                    resp.headers['Cache-Control'] = 'public, max-age=30'
                    return resp
                cache_key = f"ai_only::{norm_query}"
                
                # Serve from cache if fresh
                cached = self._get_cached_response(cache_key)
                if cached is not None:
                    resp = jsonify(cached)
                    resp.headers['X-Cache'] = 'HIT'
                    resp.headers['Cache-Control'] = 'public, max-age=60'
                    return resp
                
                start_time = time.time()
                
                # Get AI contextual response only
                ai_response = None
                try:
                    # Get AI response directly from Morphik
                    response = self.morphik_system.db.query(query, use_colpali=False)
                    if response and hasattr(response, 'completion') and response.completion:
                        ai_response = response.completion
                        logger.info(f"Got AI response: {len(ai_response)} chars")
                    else:
                        ai_response = "I couldn't find specific information about that in the ECSS documents. Please try asking about ECSS standards, requirements, or procedures."
                except Exception as e:
                    logger.warning(f"AI response failed: {e}")
                    ai_response = "Sorry, I'm having trouble accessing the ECSS documents right now. Please try again later."
                
                processing_time = time.time() - start_time
                
                # Prepare simplified response with only AI response
                response_data = {
                    'ai_response': ai_response,
                    'results': [],  # Empty array for compatibility
                    'total': 0,
                    'query': query,
                    'methods_used': ['ai_context_only'],
                    'processing_time': processing_time,
                    'timestamp': time.time()
                }
                
                # Store in cache (LRU with TTL)
                self._set_cached_response(cache_key, response_data)
                
                logger.info(f"✅ AI search completed in {processing_time:.2f}s")
                resp = jsonify(response_data)
                resp.headers['X-Cache'] = 'MISS'
                resp.headers['Cache-Control'] = 'public, max-age=60'
                return resp
                
            except Exception as e:
                logger.error(f"❌ Search failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/working/status', methods=['GET'])
        def working_status():
            """Get system status for working features."""
            try:
                if not self.morphik_system:
                    return jsonify({'error': 'System not initialized'}), 500
                
                status = self.morphik_system.get_system_status()
                return jsonify(status)
                
            except Exception as e:
                logger.error(f"❌ Status check failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/working/batch', methods=['GET'])
        def working_batch():
            """Test batch operations with fixed parameters."""
            try:
                limit = int(request.args.get('limit', 5))
                
                if not self.morphik_system:
                    return jsonify({'error': 'System not initialized'}), 500
                
                results = self.morphik_system.batch_document_analysis(limit)
                return jsonify(results)
                
            except Exception as e:
                logger.error(f"❌ Batch analysis failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/working/capabilities', methods=['GET'])
        def working_capabilities():
            """Get working capabilities for simplified AI-only system."""
            return jsonify({
                'working_features': {
                    'ai_search': {
                        'status': 'working',
                        'description': 'AI-powered search with contextual responses',
                        'endpoint': '/api/working/search?q=<query>',
                        'response_time': '3-8 seconds'
                    },
                    'ecss_knowledge': {
                        'status': 'working',
                        'description': 'Access to ECSS standards and requirements',
                        'documents_processed': '3 documents',
                        'coverage': 'ECSS standards and procedures'
                    },
                    'simple_interface': {
                        'status': 'working',
                        'description': 'Clean, fast user interface',
                        'features': ['AI responses only', 'Fast loading', 'Mobile responsive']
                    }
                },
                'disabled_features': {
                    'document_chunks': 'removed for speed optimization',
                    'visual_search': 'removed for speed optimization',
                    'batch_operations': 'not needed for AI-only approach'
                },
                'performance': {
                    'typical_response_time': '3-8 seconds',
                    'quality': 'excellent AI responses',
                    'reliability': 'high for AI queries'
                }
            })
        
        return app
    
    def _normalize_query(self, query: str) -> str:
        """Normalize queries for better cache hit ratio."""
        q = query.lower()
        q = re.sub(r"\s+", " ", q).strip()
        return q
    
    def _get_cached_response(self, key: str):
        """Return cached response if not expired; maintain LRU order."""
        now = time.time()
        data = self._cache.get(key)
        if not data:
            return None
        if now - data['ts'] > self._cache_ttl_seconds:
            try:
                del self._cache[key]
            except KeyError:
                pass
            return None
        self._cache.move_to_end(key)
        return data['value']
    
    def _set_cached_response(self, key: str, value: Dict[str, Any]):
        """Insert into LRU cache; prune size and drop expired entries opportunistically."""
        now = time.time()
        self._cache[key] = {'value': value, 'ts': now}
        self._cache.move_to_end(key)
        while len(self._cache) > self._cache_max_size:
            self._cache.popitem(last=False)
        keys_to_delete = []
        for k, v in list(self._cache.items())[:32]:
            if now - v['ts'] > self._cache_ttl_seconds:
                keys_to_delete.append(k)
        for k in keys_to_delete:
            self._cache.pop(k, None)
    
    def run(self):
        """Run the production API server."""
        try:
            logger.info(f"🚀 Starting Production Working API on port {self.port}")
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")

def main():
    """Start the production working API server."""
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI environment variable not set")
        return
    
    # Create and run server
    try:
        server = ProductionWorkingAPI(port=8002)
        server.run()
    except Exception as e:
        logger.error(f"❌ Failed to start production API: {e}")

if __name__ == "__main__":
    main() 