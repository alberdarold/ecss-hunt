#!/usr/bin/env python3
"""
Production ECSS API Server with Visual Content Search
====================================================

This is the production-ready API server that integrates:
1. Foundation system with visual content extraction (ColPali)
2. Enhanced search with contextual results
3. Comprehensive endpoints for ECSS encyclopedia
4. Production-grade error handling and monitoring
5. Real-time ingestion capabilities

Built on the proven foundation with 100% visual content extraction success rate.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
import time
import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import traceback
from PIL import Image

from production.ecss_foundation_system import ECSSFoundationSystem, FoundationConfig, SearchResult, IngestionResult
from ingestion.production.ecss_batch_ingestion import ECSSBatchIngestion, BatchIngestionConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProductionAPIServer:
    """
    Production-ready ECSS API Server with visual content search.
    
    Features:
    - Visual content extraction and search (ColPali)
    - Enhanced contextual search results
    - Real-time document ingestion
    - Batch processing capabilities
    - Comprehensive error handling
    - Production monitoring and logging
    """
    
    def __init__(self, config: FoundationConfig):
        """Initialize the production API server."""
        self.config = config
        self.foundation = ECSSFoundationSystem(config)
        self.app = self._create_flask_app()
        self.request_count = 0
        self.error_count = 0
        
        logger.info("🚀 Production ECSS API Server initialized")
    
    def _create_flask_app(self) -> Flask:
        """Create and configure Flask application."""
        app = Flask(__name__)
        
        # Configure CORS
        allowed_origins = [
            "http://localhost:3000",
            "https://localhost:3000",
            "http://127.0.0.1:3000",
            "https://ecss-hunt.onrender.com",
            "https://ecss-hunt.vercel.app",
            "https://ecss-hunt-frontend.vercel.app"
        ]
        
        if self.config.debug_mode:
            CORS(app, origins="*")
        else:
            CORS(app, origins=allowed_origins)
        
        # Register error handlers
        self._register_error_handlers(app)
        
        # Register routes
        self._register_routes(app)
        
        return app
    
    def _clean_raw_response(self, raw_response: str) -> str:
        """Clean raw AI response by converting markdown headers to structured formatting."""
        if not raw_response:
            return raw_response
        
        lines = raw_response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines and separators
            if not stripped or stripped.startswith('---'):
                continue
            
            # Convert markdown headers to structured formatting
            if stripped.startswith('###### '):
                # Level 6 header - make it a small section
                title = stripped[7:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            elif stripped.startswith('##### '):
                # Level 5 header - make it a small section
                title = stripped[6:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            elif stripped.startswith('#### '):
                # Level 4 header - make it a subsection
                title = stripped[5:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            elif stripped.startswith('### '):
                # Level 3 header - make it a main section
                title = stripped[4:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            elif stripped.startswith('## '):
                # Level 2 header - make it a major section
                title = stripped[3:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            elif stripped.startswith('# '):
                # Level 1 header - make it a main topic
                title = stripped[2:].strip()
                cleaned_lines.append(f"<strong>{title}</strong>")
            else:
                # Regular content line
                cleaned_lines.append(stripped)
        
        # Join lines and clean up extra whitespace
        cleaned = '\n'.join(cleaned_lines)
        
        # Remove any remaining standalone # symbols
        cleaned = cleaned.replace('#', '')
        
        return cleaned

    def _structure_contextual_response(self, raw_response: str, query: str, result_count: int, document_sources: List[str] = None) -> str:
        """Structure the contextual response for better engineer-friendly readability with document sources."""
        try:
            # Clean the raw response first
            cleaned_response = self._clean_raw_response(raw_response)
            
            # Break down the response into digestible sections
            sections = []
            
            # Add header with better spacing
            sections.append(f"<strong>Key Information about '{query.title()}'</strong>")
            sections.append("")  # Add spacing
            
            # Split content into logical chunks
            paragraphs = cleaned_response.split('\n\n')
            if not paragraphs:
                paragraphs = [cleaned_response]
            
            # Process each paragraph to make it more readable with better organization
            structured_content = []
            for i, paragraph in enumerate(paragraphs[:3]):  # Limit to 3 paragraphs
                if len(paragraph.strip()) > 50:  # Only include substantial content
                    # Add structured sections with better formatting
                    if i == 0:
                        structured_content.append(f"<strong>Main Information</strong>\n\n{paragraph.strip()}")
                    elif i == 1:
                        structured_content.append(f"<strong>Detailed Context</strong>\n\n{paragraph.strip()}")
                    else:
                        structured_content.append(f"<strong>Additional Details</strong>\n\n{paragraph.strip()}")
            
            # Combine sections with proper spacing
            if structured_content:
                sections.extend(structured_content)
            else:
                # Fallback: use first 500 characters with better formatting
                content = cleaned_response[:500] + "..." if len(cleaned_response) > 500 else cleaned_response
                sections.append(f"<strong>Summary</strong>\n\n{content}")
            
            # Add document sources section
            if document_sources and len(document_sources) > 0:
                sections.append("")  # Add spacing
                sections.append("<strong>Source Documents:</strong>")
                for source in document_sources[:5]:  # Limit to 5 sources
                    sections.append(f"• {source}")
                if len(document_sources) > 5:
                    sections.append(f"• ... and {len(document_sources) - 5} more documents")
            
            # Add footer with result count and spacing
            sections.append("")  # Add spacing before footer
            sections.append(f"<em>Found {result_count} relevant results from ECSS documents</em>")
            
            return '\n\n'.join(sections)
            
        except Exception as e:
            logger.error(f"Error structuring contextual response: {e}")
            # Fallback: return cleaned original
            cleaned_fallback = self._clean_raw_response(raw_response)
            return cleaned_fallback[:800] + "..." if len(cleaned_fallback) > 800 else cleaned_fallback
    
    def _register_error_handlers(self, app: Flask):
        """Register error handlers."""
        
        @app.errorhandler(Exception)
        def handle_exception(e):
            """Handle all exceptions."""
            self.error_count += 1
            
            # Log the error
            logger.error(f"API Error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Return JSON error response
            if isinstance(e, HTTPException):
                return jsonify({
                    'error': e.description,
                    'status_code': e.code,
                    'timestamp': datetime.now().isoformat()
                }), e.code
            else:
                return jsonify({
                    'error': 'Internal server error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
    
    def _register_routes(self, app: Flask):
        """Register API routes."""
        
        @app.before_request
        def before_request():
            """Before request middleware."""
            self.request_count += 1
            logger.info(f"API Request: {request.method} {request.path}")
        
        @app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time(),
                'request_count': self.request_count,
                'error_count': self.error_count
            })
        
        @app.route('/api/status', methods=['GET'])
        def system_status():
            """Comprehensive system status."""
            foundation_status = self.foundation.get_system_status()
            
            return jsonify({
                'status': 'online',
                'timestamp': datetime.now().isoformat(),
                'foundation_system': foundation_status,
                'api_metrics': {
                    'request_count': self.request_count,
                    'error_count': self.error_count,
                    'error_rate': (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
                }
            })
        
        @app.route('/api/search', methods=['GET'])
        def search():
            """Enhanced search with visual content support and ECSS filtering."""
            query = request.args.get('q', '').strip()
            limit = int(request.args.get('limit', 5))
            include_visual = request.args.get('include_visual', 'true').lower() == 'true'
            fast_mode = request.args.get('fast_mode', 'false').lower() == 'true'
            
            # ECSS-specific filtering (restored from original API)
            branch = request.args.get('branch', None)  # E, M, Q, S, U
            doc_type = request.args.get('doc_type', None)  # standard, handbook, etc.
            content_type = request.args.get('content_type', None)  # requirement, definition, etc.
            min_score = float(request.args.get('min_score', 0.0))
            
            if not query:
                return jsonify({'error': 'Query parameter "q" is required'}), 400
            
            if limit > 20:
                return jsonify({'error': 'Maximum limit is 20'}), 400
            
            start_time = time.time()
            
            try:
                # Perform enhanced search with ECSS filtering
                if fast_mode:
                    # Fast mode: skip ColPali for quicker responses
                    results = self.foundation.search_with_visual_content_fast(query, limit)
                else:
                    # Full mode: use ColPali for comprehensive results
                    results = self.foundation.search_with_visual_content(query, limit)
                
                # Apply ECSS-specific filters
                filtered_results = []
                for result in results:
                    # Apply minimum score filter
                    if result.relevance_score < min_score:
                        continue
                    
                    # Apply branch filter (E, M, Q, S, U)
                    if branch:
                        filename = result.document_info.get('filename', '')
                        if not filename.startswith(f'ECSS-{branch.upper()}-'):
                            continue
                    
                    # Apply content type filter
                    if content_type and result.source_type.lower() != content_type.lower():
                        continue
                    
                    # Apply visual content filter
                    if not include_visual and result.is_visual_content:
                        continue
                    
                    filtered_results.append(result)
                
                results = filtered_results[:limit]
                
                # Robust extraction of document sources for frontend display.
                # Tries multiple fields and regex extraction to ensure sources are always shown.
                document_sources = []
                logger.info(f"🔍 Processing {len(results)} search results for document sources")
                
                for i, result in enumerate(results):
                    filename = None
                    logger.info(f"🔍 Result {i}: has document_info={hasattr(result, 'document_info')}")

                    # 1. Try document_info['filename']
                    if hasattr(result, 'document_info') and result.document_info:
                        filename = result.document_info.get('filename', None)
                        logger.info(f"🔍 Result {i}: filename from document_info='{filename}'")

                    # 2. Try document_id
                    if not filename and hasattr(result, 'document_info') and result.document_info:
                        filename = result.document_info.get('document_id', None)
                        logger.info(f"🔍 Result {i}: filename from document_id='{filename}'")

                    # 3. Try result.source
                    if not filename and hasattr(result, 'source'):
                        filename = getattr(result, 'source', None)
                        logger.info(f"🔍 Result {i}: filename from source='{filename}'")

                    # 4. Try to extract from content using regex
                    if not filename and hasattr(result, 'content'):
                        match = re.search(r'ECSS-[A-Z]-[A-Z]{2}-[A-Za-z0-9().-]+\.pdf', str(result.content))
                        if match:
                            filename = match.group(0)
                            logger.info(f"🔍 Result {i}: filename from regex='{filename}'")

                    # 5. Fallback
                    if not filename:
                        filename = f"Unknown Document {i+1}"
                        logger.info(f"🔍 Result {i}: using fallback filename='{filename}'")

                    if filename and filename not in document_sources:
                        document_sources.append(filename)
                        logger.info(f"🔍 Added document source: {filename}")
                
                # Debug logging for document sources
                logger.info(f"📚 Found {len(document_sources)} document sources: {document_sources}")
                
                # Get contextual response from the search results (avoid duplicate query)
                contextual_response = None
                if results and hasattr(results[0], 'detailed_content'):
                    # Use the detailed content already extracted during search
                    detailed_content = results[0].detailed_content
                    if detailed_content:
                        contextual_response = self._structure_contextual_response(
                            detailed_content, query, len(results), document_sources
                        )
                elif self.config.use_colpali:
                    # Fallback: only query if not already done
                    try:
                        response = self.foundation.db.query(query, use_colpali=True)
                        if response and response.completion:
                            contextual_response = self._structure_contextual_response(
                                response.completion, query, len(results), document_sources
                            )
                    except Exception as e:
                        logger.warning(f"Failed to get contextual response: {e}")
                
                processing_time = time.time() - start_time
                
                # Prepare response
                response_data = {
                    'query': query,
                    'results': [asdict(r) for r in results],
                    'total_results': len(results),
                    'visual_results': sum(1 for r in results if r.is_visual_content),
                    'text_results': sum(1 for r in results if not r.is_visual_content),
                    'document_sources': document_sources,
                    'ai_response': contextual_response,  # Frontend expects ai_response
                    'contextual_response': contextual_response,
                    'processing_time': processing_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Debug logging for response data
                logger.info(f"📤 Response includes {len(document_sources)} document sources")
                logger.info(f"📤 Contextual response length: {len(contextual_response) if contextual_response else 0}")
                
                logger.info(f"Search completed: '{query}' -> {len(results)} results ({processing_time:.2f}s)")
                
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"Search failed: {e}")
                return jsonify({
                    'error': 'Search failed',
                    'message': str(e),
                    'query': query,
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/search/visual', methods=['GET'])
        def visual_search():
            """Search specifically for visual content."""
            query = request.args.get('q', '').strip()
            limit = int(request.args.get('limit', 5))
            
            if not query:
                return jsonify({'error': 'Query parameter "q" is required'}), 400
            
            start_time = time.time()
            
            try:
                # Get all results
                all_results = self.foundation.search_with_visual_content(query, limit * 2)
                
                # Filter only visual content
                visual_results = [r for r in all_results if r.is_visual_content][:limit]
                
                processing_time = time.time() - start_time
                
                response_data = {
                    'query': query,
                    'visual_results': [asdict(r) for r in visual_results],
                    'total_visual_results': len(visual_results),
                    'processing_time': processing_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"Visual search completed: '{query}' -> {len(visual_results)} visual results")
                
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"Visual search failed: {e}")
                return jsonify({
                    'error': 'Visual search failed',
                    'message': str(e),
                    'query': query,
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/ingest', methods=['POST'])
        def ingest_document():
            """Ingest a single document."""
            try:
                data = request.get_json()
                
                if not data or 'file_path' not in data:
                    return jsonify({'error': 'file_path is required in request body'}), 400
                
                file_path = data['file_path']
                
                # Validate file exists
                if not Path(file_path).exists():
                    return jsonify({'error': f'File not found: {file_path}'}), 404
                
                # Ingest document
                result = self.foundation.ingest_document(file_path)
                
                logger.info(f"Document ingestion completed: {result.filename} -> {result.status}")
                
                return jsonify(asdict(result))
                
            except Exception as e:
                logger.error(f"Document ingestion failed: {e}")
                return jsonify({
                    'error': 'Document ingestion failed',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/ingest/batch', methods=['POST'])
        def batch_ingest():
            """Start batch ingestion of multiple documents."""
            try:
                data = request.get_json()
                
                # Configuration for batch ingestion
                batch_config = BatchIngestionConfig(
                    morphik_uri=self.config.morphik_uri,
                    documents_path=data.get('documents_path', self.config.ecss_documents_path),
                    max_documents=data.get('max_documents', 10),
                    max_workers=data.get('max_workers', 3),
                    use_colpali=data.get('use_colpali', True),
                    cost_limit_total=data.get('cost_limit_total', 20.0),
                    skip_existing=data.get('skip_existing', True),
                    output_report=data.get('output_report', True)
                )
                
                # Initialize batch ingestion
                batch_ingestion = ECSSBatchIngestion(batch_config)
                
                # Run batch ingestion
                stats = batch_ingestion.run_batch_ingestion()
                
                # Get processing summary
                summary = batch_ingestion.get_processing_summary()
                
                logger.info(f"Batch ingestion completed: {summary['successful']}/{summary['total_documents']} documents")
                
                return jsonify({
                    'status': 'completed',
                    'stats': asdict(stats),
                    'summary': summary,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Batch ingestion failed: {e}")
                return jsonify({
                    'error': 'Batch ingestion failed',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/documents', methods=['GET'])
        def list_documents():
            """List ingested documents."""
            try:
                documents = self.foundation.db.list_documents()
                
                doc_info = []
                for doc in documents:
                    doc_info.append({
                        'id': doc.external_id,
                        'filename': doc.filename,
                        'status': doc.status,
                        'is_processing': doc.is_processing,
                        'is_failed': doc.is_failed,
                        'content_type': doc.content_type,
                        'metadata': doc.metadata
                    })
                
                return jsonify({
                    'documents': doc_info,
                    'total_documents': len(doc_info),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Failed to list documents: {e}")
                return jsonify({
                    'error': 'Failed to list documents',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/documents/<document_id>/chunks', methods=['GET'])
        def get_document_chunks(document_id):
            """Get chunks for a specific document."""
            try:
                limit = int(request.args.get('limit', 20))
                
                chunks = self.foundation.db.retrieve_chunks(
                    "content",
                    filters={"document_id": document_id},
                    use_colpali=self.config.use_colpali,
                    k=limit
                )
                
                chunk_info = []
                for chunk in chunks:
                    is_visual = isinstance(chunk.content, Image.Image)
                    
                    chunk_data = {
                        'chunk_number': chunk.chunk_number,
                        'document_id': chunk.document_id,
                        'filename': chunk.filename,
                        'is_visual': is_visual,
                        'content_type': 'image' if is_visual else 'text',
                        'score': getattr(chunk, 'score', 0.0)
                    }
                    
                    if is_visual:
                        chunk_data['image_size'] = chunk.content.size
                        chunk_data['image_mode'] = chunk.content.mode
                        chunk_data['content_preview'] = f"Visual content ({chunk.content.size[0]}x{chunk.content.size[1]})"
                    else:
                        content_str = str(chunk.content)
                        chunk_data['content_preview'] = content_str[:200] + "..." if len(content_str) > 200 else content_str
                    
                    chunk_info.append(chunk_data)
                
                return jsonify({
                    'document_id': document_id,
                    'chunks': chunk_info,
                    'total_chunks': len(chunk_info),
                    'visual_chunks': sum(1 for c in chunk_info if c['is_visual']),
                    'text_chunks': sum(1 for c in chunk_info if not c['is_visual']),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Failed to get document chunks: {e}")
                return jsonify({
                    'error': 'Failed to get document chunks',
                    'message': str(e),
                    'document_id': document_id,
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get comprehensive system statistics."""
            try:
                # Get foundation stats
                foundation_status = self.foundation.get_system_status()
                
                # Get document stats
                documents = self.foundation.db.list_documents()
                
                # Calculate chunk statistics
                all_chunks = self.foundation.db.retrieve_chunks(
                    "content",
                    use_colpali=self.config.use_colpali,
                    k=1000
                )
                
                visual_chunks = sum(1 for chunk in all_chunks if isinstance(chunk.content, Image.Image))
                text_chunks = len(all_chunks) - visual_chunks
                
                stats = {
                    'system_status': foundation_status,
                    'documents': {
                        'total': len(documents),
                        'processing': sum(1 for doc in documents if doc.is_processing),
                        'failed': sum(1 for doc in documents if doc.is_failed),
                        'completed': sum(1 for doc in documents if not doc.is_processing and not doc.is_failed)
                    },
                    'chunks': {
                        'total': len(all_chunks),
                        'visual': visual_chunks,
                        'text': text_chunks,
                        'visual_percentage': (visual_chunks / len(all_chunks) * 100) if all_chunks else 0
                    },
                    'api_metrics': {
                        'request_count': self.request_count,
                        'error_count': self.error_count,
                        'error_rate': (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify(stats)
                
            except Exception as e:
                logger.error(f"Failed to get stats: {e}")
                return jsonify({
                    'error': 'Failed to get stats',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
    
    def run(self):
        """Run the production API server."""
        logger.info(f"🌐 Starting Production ECSS API Server")
        logger.info(f"📊 Configuration:")
        logger.info(f"   - Port: {self.config.api_port}")
        logger.info(f"   - ColPali enabled: {self.config.use_colpali}")
        logger.info(f"   - Debug mode: {self.config.debug_mode}")
        logger.info(f"   - Max documents: {self.config.max_documents}")
        
        self.app.run(
            host='0.0.0.0',
            port=self.config.api_port,
            debug=self.config.debug_mode,
            threaded=True
        )

def main():
    """Main function to run the production API server."""
    # Load configuration
    config = FoundationConfig(
        morphik_uri=os.getenv("MORPHIK_URI"),
        ecss_documents_path=os.getenv("ECSS_DOCUMENTS_PATH", "../../ECSS Published Standards/1-Active Standards/"),
        max_documents=int(os.getenv("MAX_DOCUMENTS", "50")),
        use_colpali=True,  # Enable visual content extraction
        api_port=int(os.getenv("API_PORT", "8000")),
        debug_mode=os.getenv("DEBUG", "false").lower() == "true",
        cost_limit_per_doc=float(os.getenv("COST_LIMIT_PER_DOC", "2.0"))
    )
    
    if not config.morphik_uri:
        logger.error("❌ MORPHIK_URI environment variable not set")
        return
    
    # Create and run server
    server = ProductionAPIServer(config)
    server.run()

if __name__ == "__main__":
    main() 