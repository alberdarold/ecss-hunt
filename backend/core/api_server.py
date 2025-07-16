from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


# Add backend root to path


from flask import Flask, request, jsonify
from flask_cors import CORS
from morphik import Morphik
from core.optimized_graph_strategy import OptimizedECSSGraphManager
import os
import sys
import json
import uuid

# Load environment variables from the root directory
dotenv_path = Path(__file__).parent.parent / '.env'

app = Flask(__name__)

# Production-optimized CORS configuration  
# Allow local development IPs and production domains
allowed_origins = [
    "https://ecss-hunt.onrender.com",
    "http://localhost:3000", 
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.6:3000",  # Your local IP
    "https://ecss-hunt-frontend.vercel.app",  # Add Vercel if you deploy there
    "https://ecss-hunt.vercel.app"
]

# For development, be more permissive with local IPs
import os
if os.getenv('FLASK_DEBUG', 'False').lower() == 'true':
    # In development, allow any local IP
    CORS(app, origins="*")
else:
    # In production, use specific origins
    CORS(app, 
         origins=allowed_origins,
         methods=["GET", "POST", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=False,
         max_age=86400)  # Cache CORS preflight for 24 hours

print(f"🌐 CORS configured for origins: {allowed_origins if not os.getenv('FLASK_DEBUG', 'False').lower() == 'true' else 'ALL (debug mode)'}")

# Performance optimizations
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Handle preflight OPTIONS requests
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    """Handle CORS preflight requests."""
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialize Morphik client and optimized graph manager
def get_morphik_client():
    """Get Morphik client instance."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI not set in .env file")
        return None, None
    
    try:
        db = Morphik(uri=morphik_uri)
        graph_manager = OptimizedECSSGraphManager(morphik_uri)
        return db, graph_manager
    except Exception as e:
        print(f"✗ Failed to connect to Morphik: {e}")
        return None, None

@app.route('/api/search', methods=['GET'])
def search():
    """Search ECSS documents using basic Morphik query (enhanced graph disabled due to issues)."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)  # Optional branch filter
    page = int(request.args.get('page', 1))  # Page number (1-based)
    limit = min(int(request.args.get('limit', 5)), 10)  # Cap at 10 results max
    compact = request.args.get('compact', 'true').lower() == 'true'  # Compact results
    
    # Performance optimization: Early validation
    if not query.strip() or len(query.strip()) < 2:
        return jsonify({
            'results': [],
            'total': 0,
            'query': query,
            'page': page,
            'limit': limit,
            'message': 'Query too short' if len(query.strip()) < 2 else 'Empty query'
                 })
    
    try:
        # Get Morphik client
        db, graph_manager = get_morphik_client()
        if not db:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # --- Use basic Morphik query instead of enhanced graph ---
        print(f"Performing engineer-focused ECSS query for: '{query}'")
        
        # Enhance query for better requirement discovery
        enhanced_query = query
        if not any(word in query.lower() for word in ['shall', 'should', 'requirement', 'must', 'may']):
            enhanced_query = f"requirements for {query} shall should must"
        
        # Use basic query with ColPali support
        try:
            response = db.query(
                enhanced_query,
                k=limit * 3,  # Get more results to filter for requirements
                use_colpali=True if any(keyword in query.lower() for keyword in ['image', 'diagram', 'figure', 'chart', 'graph', 'table', 'visual', 'picture', 'photo']) else False
            )
            
            if not response or not response.sources:
                return jsonify({
                    'results': [],
                    'total': 0,
                    'query': query,
                    'message': 'No results found'
                })
            
            # Extract data from response
            summary_content = getattr(response, 'completion', '')
            sources = getattr(response, 'sources', [])
            
            results = []
            
            # Process each source with focus on engineering content
            for i, source in enumerate(sources):
                doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                doc_name = 'Unknown Document'
                doc_metadata = {}
                entity_type = 'text_chunk'
                source_type = 'text_chunk'

                try:
                    # Fetch the original document to get its filename and other metadata
                    document = db.get_document(doc_id)
                    doc_name = getattr(document, 'filename', 'Unknown')
                    doc_metadata = getattr(document, 'metadata', {})

                    # Enhanced source type detection for engineering content
                    metadata_title = doc_metadata.get('title', '').lower()
                    metadata_content = doc_metadata.get('content', '').lower()
                    
                    if any(word in metadata_title for word in ['requirement', 'shall', 'should', 'must']):
                        source_type = 'requirement'
                        entity_type = 'Requirement'
                    elif 'table' in metadata_title:
                        source_type = 'table'
                        entity_type = 'Table'
                    elif any(word in metadata_title for word in ['figure', 'diagram', 'image']):
                        source_type = 'diagram'
                        entity_type = 'Diagram'
                    elif any(word in metadata_title for word in ['section', 'clause']):
                        source_type = 'section'
                        entity_type = 'Section'
                    elif any(word in metadata_title for word in ['definition', 'term']):
                        source_type = 'definition'
                        entity_type = 'Definition'
                    elif any(word in metadata_title for word in ['annex', 'appendix']):
                        source_type = 'annex'
                        entity_type = 'Annex'
                    else:
                        source_type = 'content'
                        entity_type = 'Content'
                        
                except Exception as e:
                    print(f"Warning: Could not fetch document {doc_id} for source. {e}")
            
                # Apply branch filter if specified
                if branch:
                    doc_branch = doc_metadata.get('branch', '').upper()
                    if doc_branch and doc_branch != branch.upper():
                        continue
                
                # Extract ECSS-specific metadata
                ecss_metadata = {
                    'standard_id': doc_metadata.get('standard_id', ''),
                    'section_number': doc_metadata.get('section_number', ''),
                    'section_title': doc_metadata.get('section_title', ''),
                    'requirement_type': doc_metadata.get('requirement_type', ''),
                    'unique_id': doc_metadata.get('unique_id', ''),
                    'cross_references': doc_metadata.get('cross_references', []),
                    'verification_method': doc_metadata.get('verification_method', ''),
                    'applicable_phases': doc_metadata.get('applicable_phases', []),
                    'is_normative': doc_metadata.get('is_normative', False),
                    'requirements_count': doc_metadata.get('requirements_count', 0),
                    'recommendations_count': doc_metadata.get('recommendations_count', 0)
                }
                
                # Combine metadata
                final_metadata = doc_metadata.copy()
                final_metadata.update({
                    'document_name': doc_name,
                    'entity_type': entity_type,
                    'source_type': source_type,
                    'chunk_id': getattr(source, 'chunk_number', i),
                    'score': getattr(source, 'score', 0),
                    'query_method': 'engineer_focused',
                    'ecss_data': ecss_metadata
                })
                
                # Get the actual chunk content - try multiple methods
                source_content = "No content available"
                
                try:
                    # Method 1: Try to get text directly from source
                    if hasattr(source, 'text') and source.text:
                        raw_content = source.text
                        source_content = process_engineering_content(raw_content, doc_metadata)
                    # Method 2: Try to get content from source
                    elif hasattr(source, 'content') and source.content:
                        raw_content = source.content
                        source_content = process_engineering_content(raw_content, doc_metadata)
                    # Method 3: Try to retrieve chunk by ID
                    else:
                        chunk_id = f"{doc_id}-{getattr(source, 'chunk_number', i)}"
                        chunk = db.get_chunk(chunk_id)
                        if chunk and hasattr(chunk, 'content'):
                            raw_content = chunk.content
                            source_content = process_engineering_content(raw_content, doc_metadata)
                        elif chunk and hasattr(chunk, 'text'):
                            raw_content = chunk.text
                            source_content = process_engineering_content(raw_content, doc_metadata)
                    
                    # If still no content, try retrieving chunks for the document
                    if source_content == "No content available":
                        chunks = db.retrieve_chunks(query, filters={'document_id': doc_id}, k=5)
                        if chunks and len(chunks) > getattr(source, 'chunk_number', i):
                            chunk_idx = getattr(source, 'chunk_number', i)
                            if chunk_idx < len(chunks):
                                raw_content = getattr(chunks[chunk_idx], 'content', '') or getattr(chunks[chunk_idx], 'text', '')
                                if raw_content:
                                    source_content = process_engineering_content(raw_content, doc_metadata)
                                    
                except Exception as e:
                    print(f"Error retrieving content for source {i}: {e}")
                    # Fallback: try to get some content from metadata
                    if doc_metadata.get('content'):
                        source_content = doc_metadata['content'][:500] + "..."
                    elif doc_metadata.get('statement'):
                        source_content = f"**Requirement:** {doc_metadata['statement']}"
                    else:
                        source_content = f"Content from {doc_name} - Unable to retrieve full text. Document contains technical specifications and requirements."
                
                # Skip sources with no meaningful content
                if not source_content or source_content.strip() == '':
                    continue

                # Enhanced content formatting for engineers
                if compact:
                    # Compact mode: focus on requirements and key info
                    full_content = source_content
                    if len(full_content) > 600:
                        # Prioritize requirement statements
                        lines = full_content.split('\n')
                        important_lines = []
                        other_lines = []
                        
                        for line in lines:
                            if any(word in line.lower() for word in ['shall', 'should', 'must', 'requirement', 'r-']):
                                important_lines.append(line)
                            else:
                                other_lines.append(line)
                        
                        # Include all important lines + some context
                        preview_lines = important_lines[:3] + other_lines[:2]
                        full_content = '\n'.join(preview_lines)
                        if len('\n'.join(lines)) > len(full_content):
                            full_content += '\n...'
                else:
                    # Full mode: comprehensive engineering content
                    engineering_context = []
                    
                    if ecss_metadata['standard_id']:
                        engineering_context.append(f"**Standard:** {ecss_metadata['standard_id']}")
                    
                    if ecss_metadata['section_number'] and ecss_metadata['section_title']:
                        engineering_context.append(f"**Section:** {ecss_metadata['section_number']} - {ecss_metadata['section_title']}")
                    
                    if ecss_metadata['requirement_type']:
                        engineering_context.append(f"**Type:** {ecss_metadata['requirement_type']}")
                    
                    if ecss_metadata['verification_method']:
                        engineering_context.append(f"**Verification:** {ecss_metadata['verification_method']}")
                    
                    if ecss_metadata['cross_references']:
                        refs = ', '.join(ecss_metadata['cross_references'][:3])
                        engineering_context.append(f"**References:** {refs}")
                    
                    context_str = '\n'.join(engineering_context)
                    
                    full_content = f"**{source_type.title()} from {doc_name}:**\n\n{context_str}\n\n**Content:**\n{source_content}\n\n**AI Analysis:**\n{summary_content}"

                results.append({
                    'id': f"{doc_id}-{getattr(source, 'chunk_number', i)}", 
                    'content': full_content,
                    'score': getattr(source, 'score', 0),
                    'metadata': final_metadata
                })
                
                # Stop if we have enough results
                if len(results) >= limit:
                    break
        
            # Sort results prioritizing requirements and higher scores
            def sort_key(x):
                score = float(x.get('score', 0))
                # Boost requirement-type content
                if x['metadata']['source_type'] in ['requirement', 'section', 'definition']:
                    score += 1.0
                return score
                
            results.sort(key=sort_key, reverse=True)
            
            # Apply pagination
            total_results = len(results)
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_results = results[start_idx:end_idx]
            
            # Calculate pagination info
            total_pages = (total_results + limit - 1) // limit  # Ceiling division
            has_next = page < total_pages
            has_prev = page > 1
            
            return jsonify({
                'results': paginated_results,
                'total': total_results,
                'query': query,
                'summary': summary_content if not compact else None,
                'query_settings': {
                    'method': 'engineer_focused',
                    'enhanced_graph': False,
                    'query_enhancement': enhanced_query != query,
                    'use_colpali': True if any(keyword in query.lower() for keyword in ['image', 'diagram', 'figure', 'chart', 'graph', 'table', 'visual', 'picture', 'photo']) else False,
                    'prioritizes_requirements': True,
                    'highlights_engineering_content': True
                },
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total_pages': total_pages,
                    'has_next': has_next,
                    'has_prev': has_prev
                },
                'compact': compact
            })
            
        except Exception as e:
            print(f"Basic Morphik query failed: {e}")
            return jsonify({
                'results': [],
                'total': 0,
                'error': f'Search failed: {str(e)}',
                'query': query
            })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'results': [],
            'total': 0,
            'error': str(e),
            'query': query
        })

@app.route('/api/search/sections', methods=['GET'])
def search_sections():
    """Search for sections within ECSS documents using optimized graph strategy."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)
    
    if not query.strip():
        return jsonify({'results': [], 'total': 0, 'query': query})
    
    try:
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # Add section-specific context to query
        enhanced_query = f"Find sections related to: {query}"
        
        response_data = graph_manager.query_with_adaptive_settings(enhanced_query, branch)
        
        if 'error' in response_data:
            return jsonify({
                'results': [],
                'total': 0,
                'error': response_data['error'],
                'query': query
            })
        
        # Process results similar to main search
        results = []
        sources = response_data.get('sources', [])
        
        for i, source in enumerate(sources):
            if hasattr(source, 'entity_type') and source.entity_type == 'Section':
                doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                source_content = getattr(source, 'text', 'No content available.')
                
                try:
                    document = db.get_document(doc_id)
                    doc_name = getattr(document, 'filename', 'Unknown')
                except:
                    doc_name = 'Unknown Document'
                
                results.append({
                    'id': f"{doc_id}-section-{i}",
                    'content': f"**Section from {doc_name}:**\n{source_content}",
                    'score': getattr(source, 'score', 0),
                    'metadata': {
                        'document_name': doc_name,
                        'entity_type': 'Section',
                        'source_type': 'section'
                    }
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'results': results,
            'total': len(results),
            'query': query
        })
        
    except Exception as e:
        print(f"Section search error: {e}")
        return jsonify({
            'results': [],
            'total': 0,
            'error': str(e),
            'query': query
        })

@app.route('/api/search/definitions', methods=['GET'])
def search_definitions():
    """Search for definitions within ECSS documents using optimized graph strategy."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)
    
    if not query.strip():
        return jsonify({'results': [], 'total': 0, 'query': query})
    
    try:
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # Add definition-specific context to query
        enhanced_query = f"Find definitions related to: {query}"
        
        response_data = graph_manager.query_with_adaptive_settings(enhanced_query, branch)
        
        if 'error' in response_data:
            return jsonify({
                'results': [],
                'total': 0,
                'error': response_data['error'],
                'query': query
            })
        
        # Process results similar to main search
        results = []
        sources = response_data.get('sources', [])
        
        for i, source in enumerate(sources):
            if hasattr(source, 'entity_type') and source.entity_type == 'Definition':
                doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                source_content = getattr(source, 'text', 'No content available.')
                
                try:
                    document = db.get_document(doc_id)
                    doc_name = getattr(document, 'filename', 'Unknown')
                except:
                    doc_name = 'Unknown Document'
                
                results.append({
                    'id': f"{doc_id}-definition-{i}",
                    'content': f"**Definition from {doc_name}:**\n{source_content}",
                    'score': getattr(source, 'score', 0),
                    'metadata': {
                        'document_name': doc_name,
                        'entity_type': 'Definition',
                        'source_type': 'definition'
                    }
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'results': results,
            'total': len(results),
            'query': query
        })
        
    except Exception as e:
        print(f"Definition search error: {e}")
        return jsonify({
            'results': [],
            'total': 0,
            'error': str(e),
            'query': query
        })

@app.route('/api/search/tables', methods=['GET'])
def search_tables():
    """Search for tables within ECSS documents using optimized graph strategy."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)
    
    if not query.strip():
        return jsonify({'results': [], 'total': 0, 'query': query})
    
    try:
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # Add table-specific context to query
        enhanced_query = f"Find tables related to: {query}"
        
        response_data = graph_manager.query_with_adaptive_settings(enhanced_query, branch)
        
        if 'error' in response_data:
            return jsonify({
                'results': [],
                'total': 0,
                'error': response_data['error'],
                'query': query
            })
        
        # Process results similar to main search
        results = []
        sources = response_data.get('sources', [])
        
        for i, source in enumerate(sources):
            if hasattr(source, 'entity_type') and source.entity_type == 'Table':
                doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                source_content = getattr(source, 'text', 'No content available.')
                
                try:
                    document = db.get_document(doc_id)
                    doc_name = getattr(document, 'filename', 'Unknown')
                except:
                    doc_name = 'Unknown Document'
                
                results.append({
                    'id': f"{doc_id}-table-{i}",
                    'content': f"**Table from {doc_name}:**\n{source_content}",
                    'score': getattr(source, 'score', 0),
                    'metadata': {
                        'document_name': doc_name,
                        'entity_type': 'Table',
                        'source_type': 'table'
                    }
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'results': results,
            'total': len(results),
            'query': query
        })
        
    except Exception as e:
        print(f"Table search error: {e}")
        return jsonify({
            'results': [],
            'total': 0,
            'error': str(e),
            'query': query
        })

@app.route('/api/search/images', methods=['GET'])
def search_images():
    """Search for images and diagrams within ECSS documents using ColPali for enhanced visual retrieval."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)
    
    if not query.strip():
        return jsonify({'results': [], 'total': 0, 'query': query})
    
    try:
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        print(f"🔍 Searching for images with ColPali: '{query}'")
        
        # Use ColPali for enhanced visual retrieval
        try:
            # Direct ColPali query for visual content
            colpali_response = db.query(
                query,
                use_colpali=True,  # Enable ColPali for visual understanding
                k=10,  # Get more results for visual content
            )
            
            results = []
            sources = colpali_response.sources if colpali_response else []
            
            for i, source in enumerate(sources):
                source_text = getattr(source, 'text', '')
                source_content = getattr(source, 'content', '')
                
                # Check if this source contains visual content
                is_visual = (
                    hasattr(source, 'entity_type') and source.entity_type == 'Diagram' or
                    any(keyword in source_text.lower() for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph']) or
                    any(keyword in source_content.lower() for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph'])
                )
                
                if is_visual:
                    doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                    
                    try:
                        document = db.get_document(doc_id)
                        doc_name = getattr(document, 'filename', 'Unknown')
                    except:
                        doc_name = 'Unknown Document'
                    
                    # Enhanced content with visual context
                    visual_content = f"**Visual Content from {doc_name}:**\n{source_text}\n\n**Visual Context:**\n{source_content}"
                    
                    results.append({
                        'id': f"{doc_id}-image-{i}",
                        'content': visual_content,
                        'score': getattr(source, 'score', 0),
                        'metadata': {
                            'document_name': doc_name,
                            'entity_type': 'Diagram',
                            'source_type': 'diagram',
                            'retrieval_method': 'ColPali',
                            'visual_confidence': getattr(source, 'score', 0)
                        }
                    })
            
            # Also try graph-based search for additional context
            if branch:
                graph_response = graph_manager.query_with_adaptive_settings(
                    f"Find images, diagrams, or figures related to: {query}", 
                    branch
                )
                
                if 'sources' in graph_response:
                    for source in graph_response['sources']:
                        source_text = getattr(source, 'text', '')
                        if any(keyword in source_text.lower() for keyword in ['figure', 'diagram', 'image', 'photo']):
                            doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                            
                            try:
                                document = db.get_document(doc_id)
                                doc_name = getattr(document, 'filename', 'Unknown')
                            except:
                                doc_name = 'Unknown Document'
                            
                            results.append({
                                'id': f"{doc_id}-graph-image-{len(results)}",
                                'content': f"**Graph-Enhanced Visual Content from {doc_name}:**\n{source_text}",
                                'score': getattr(source, 'score', 0),
                                'metadata': {
                                    'document_name': doc_name,
                                    'entity_type': 'Diagram',
                                    'source_type': 'diagram',
                                    'retrieval_method': 'Graph+ColPali',
                                    'visual_confidence': getattr(source, 'score', 0)
                                }
                            })
            
            results.sort(key=lambda x: x['score'], reverse=True)
            
            return jsonify({
                'results': results,
                'total': len(results),
                'query': query,
                'retrieval_method': 'ColPali + Graph',
                'visual_enhanced': True
            })
            
        except Exception as e:
            print(f"⚠ ColPali search failed, falling back to basic search: {e}")
            # Fallback to basic search
            enhanced_query = f"Find images, diagrams, or figures related to: {query}"
            response_data = graph_manager.query_with_adaptive_settings(enhanced_query, branch)
            
            if 'error' in response_data:
                return jsonify({
                    'results': [],
                    'total': 0,
                    'error': response_data['error'],
                    'query': query
                })
            
            # Process results similar to main search
            results = []
            sources = response_data.get('sources', [])
            
            for i, source in enumerate(sources):
                source_text = getattr(source, 'text', '')
                if (hasattr(source, 'entity_type') and source.entity_type == 'Diagram') or \
                   any(keyword in source_text.lower() for keyword in ['figure', 'diagram', 'image', 'photo']):
                    
                    doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                    
                    try:
                        document = db.get_document(doc_id)
                        doc_name = getattr(document, 'filename', 'Unknown')
                    except:
                        doc_name = 'Unknown Document'
                    
                    results.append({
                        'id': f"{doc_id}-image-{i}",
                        'content': f"**Image/Diagram from {doc_name}:**\n{source_text}",
                        'score': getattr(source, 'score', 0),
                        'metadata': {
                            'document_name': doc_name,
                            'entity_type': 'Diagram',
                            'source_type': 'diagram',
                            'retrieval_method': 'Graph Only'
                        }
                    })
            
            results.sort(key=lambda x: x['score'], reverse=True)
            
            return jsonify({
                'results': results,
                'total': len(results),
                'query': query,
                'retrieval_method': 'Graph Only (ColPali failed)',
                'visual_enhanced': False
            })
        
    except Exception as e:
        print(f"Image search error: {e}")
        return jsonify({
            'results': [],
            'total': 0,
            'error': str(e),
            'query': query
        })

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all ingested documents with their metadata."""
    try:
        db, graph_manager = get_morphik_client()
        if not db:
            return jsonify({'documents': [], 'error': 'Morphik connection failed'})
        
        # Get all documents
        documents = db.list_documents()
        
        doc_list = []
        for doc in documents:
            doc_info = {
                'id': getattr(doc, 'external_id', 'unknown'),
                'filename': getattr(doc, 'filename', 'unknown'),
                'metadata': getattr(doc, 'metadata', {}),
                'created_at': getattr(doc, 'created_at', None)
            }
            doc_list.append(doc_info)
        
        return jsonify({
            'documents': doc_list,
            'total': len(doc_list)
        })
        
    except Exception as e:
        print(f"Error listing documents: {e}")
        return jsonify({
            'documents': [],
            'error': str(e)
        })

@app.route('/api/graph/stats', methods=['GET'])
def graph_stats():
    """Get statistics for all focused knowledge graphs."""
    try:
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({'graphs': {}, 'error': 'Morphik connection failed'})
        
        # Get statistics for all graphs
        stats = graph_manager.get_graph_statistics()
        
        return jsonify({
            'graphs': stats,
            'total_graphs': len(stats)
        })
        
    except Exception as e:
        print(f"Error getting graph stats: {e}")
        return jsonify({
            'graphs': {},
            'error': str(e)
        })

@app.route('/api/graph/update', methods=['POST'])
def update_graph():
    """Update a specific graph with new documents."""
    try:
        data = request.get_json()
        graph_name = data.get('graph_name')
        new_doc_ids = data.get('document_ids', [])
        
        if not graph_name or not new_doc_ids:
            return jsonify({
                'success': False,
                'error': 'Missing graph_name or document_ids'
            })
        
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'success': False,
                'error': 'Morphik connection failed'
            })
        
        # Update the graph incrementally
        success = graph_manager.update_graph_incrementally(graph_name, new_doc_ids)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Successfully updated {graph_name} with {len(new_doc_ids)} documents'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to update {graph_name}'
            })
            
    except Exception as e:
        print(f"Error updating graph: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        db, graph_manager = get_morphik_client()
        if not db:
            return jsonify({
                'status': 'unhealthy',
                'error': 'Morphik connection failed'
            })
        
        return jsonify({
            'status': 'healthy',
            'morphik_connected': True,
            'graph_manager_available': graph_manager is not None
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        })

# Production optimizations
from flask import g
import time

def process_engineering_content(content, metadata):
    """
    Process content to highlight engineering requirements and important information.
    """
    if not content:
        return content
    
    # Clean up the content first
    content = content.strip()
    if len(content) < 10:  # Too short to be meaningful
        return content
    
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        if not line.strip():  # Skip empty lines
            processed_lines.append(line)
            continue
            
        line_lower = line.lower().strip()
        original_line = line.strip()
        
        # Skip very short lines
        if len(line_lower) < 5:
            processed_lines.append(line)
            continue
        
        # Identify and highlight different types of content
        formatted_line = original_line
        
        # 1. REQUIREMENTS (shall, should, must statements)
        if any(pattern in line_lower for pattern in [
            'shall', 'should', 'must', 'may not', 'cannot', 'will not',
            'it is required', 'requirement', 'mandatory'
        ]):
            if not formatted_line.startswith('**'):
                formatted_line = f"🔹 **REQUIREMENT:** {formatted_line}"
        
        # 2. ECSS REFERENCES and STANDARDS
        elif any(pattern in line_lower for pattern in ['ecss-', 'iso ', 'iec ', 'ieee ']):
            if not formatted_line.startswith('**'):
                formatted_line = f"📋 **REFERENCE:** {formatted_line}"
        
        # 3. DEFINITIONS and TERMS
        elif any(pattern in line_lower for pattern in [
            'definition:', 'term:', 'means:', 'refers to:', 'is defined as'
        ]):
            if not formatted_line.startswith('**'):
                formatted_line = f"📖 **DEFINITION:** {formatted_line}"
        
        # 4. NOTES and CLARIFICATIONS  
        elif any(pattern in line_lower for pattern in ['note:', 'note ', 'example:', 'remark:']):
            if not formatted_line.startswith('**'):
                formatted_line = f"💡 **NOTE:** {formatted_line}"
        
        # 5. SECTION HEADERS and STRUCTURE
        elif any(pattern in line_lower for pattern in [
            'section', 'clause', 'annex', 'appendix', 'table', 'figure'
        ]) and len(line_lower) < 100:  # Short lines likely to be headers
            if not formatted_line.startswith('**'):
                formatted_line = f"📂 **SECTION:** {formatted_line}"
        
        # 6. VERIFICATION and TESTING
        elif any(pattern in line_lower for pattern in [
            'verification', 'test', 'validation', 'compliance', 'audit'
        ]):
            if not formatted_line.startswith('**'):
                formatted_line = f"✅ **VERIFICATION:** {formatted_line}"
        
        # 7. TECHNICAL SPECIFICATIONS
        elif any(pattern in line_lower for pattern in [
            'specification', 'parameter', 'criteria', 'threshold', 'limit'
        ]):
            if not formatted_line.startswith('**'):
                formatted_line = f"⚙️ **SPECIFICATION:** {formatted_line}"
        
        processed_lines.append(formatted_line)
    
    # Join and clean up
    result = '\n'.join(processed_lines)
    
    # Add summary if content is very long
    if len(result) > 1000:
        lines = result.split('\n')
        important_lines = [line for line in lines if any(marker in line for marker in ['🔹', '📋', '📖', '✅', '⚙️'])]
        if len(important_lines) > 3:
            result = '\n'.join(important_lines[:5]) + '\n\n... (additional technical content available)'
    
    return result

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request  
def after_request(response):
    # Add performance headers
    if hasattr(g, 'start_time'):
        response.headers['X-Response-Time'] = f"{(time.time() - g.start_time) * 1000:.2f}ms"
    
    # Add caching headers for static content
    if request.endpoint in ['search', 'search_sections', 'search_definitions']:
        response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes cache
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    
    return response

if __name__ == '__main__':
    # Production-ready configuration
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0', 
        port=port,
        threaded=True,  # Enable threading for better concurrency
        use_reloader=debug_mode  # Only use reloader in debug mode
    ) 