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
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",
    "https://ecss-hunt.vercel.app",
    "https://ecss-hunt-alberdarolds-projects.vercel.app",
    "https://ecss-hunt.onrender.com"
]}}, supports_credentials=True)

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
    """Search ECSS documents using optimized graph strategy with adaptive settings."""
    query = request.args.get('q', '')
    branch = request.args.get('branch', None)  # Optional branch filter
    
    if not query.strip():
        return jsonify({
            'results': [],
            'total': 0,
            'query': query
        })
    
    try:
        # Get Morphik client and graph manager
        db, graph_manager = get_morphik_client()
        if not db or not graph_manager:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # --- Use optimized query with adaptive settings ---
        print(f"Performing optimized graph query for: '{query}' (branch: {branch})")
        
        # Use the optimized graph manager with adaptive settings
        response_data = graph_manager.query_with_adaptive_settings(query, branch)
        
        # Add ColPali support for visual content queries
        # Check if query might benefit from visual understanding
        visual_keywords = ['image', 'diagram', 'figure', 'chart', 'graph', 'table', 'visual', 'picture', 'photo']
        is_visual_query = any(keyword in query.lower() for keyword in visual_keywords)
        
        if is_visual_query:
            print(f"🔍 Detected visual query, using ColPali for enhanced retrieval")
            # For visual queries, we might want to also do a ColPali-based search
            try:
                colpali_response = db.query(
                    query,
                    use_colpali=True,  # Enable ColPali for visual understanding
                    k=5  # Limit results for ColPali
                )
                
                # Merge ColPali results with graph results if available
                if colpali_response and colpali_response.sources:
                    print(f"📸 ColPali found {len(colpali_response.sources)} visual results")
                    # Add ColPali sources to the response
                    if 'sources' not in response_data:
                        response_data['sources'] = []
                    response_data['sources'].extend(colpali_response.sources)
                    
            except Exception as e:
                print(f"⚠ ColPali query failed: {e}")
        
        if 'error' in response_data:
            return jsonify({
                'results': [],
                'total': 0,
                'error': response_data['error'],
                'query': query
            })
        
        # Extract data from response
        summary_content = response_data.get('completion', '')
        sources = response_data.get('sources', [])
        query_settings = response_data.get('query_settings', {})
        
        results = []
        
        # Guard against empty responses
        if not summary_content:
            print("Query returned no completion. Sending empty results.")
            return jsonify({
                'results': [],
                'total': 0,
                'query': query,
                'query_settings': query_settings
            })

        # Process sources if available
        if not sources:
            print("Query returned a completion but no sources. Sending summary as single result.")
            results.append({
                'id': str(uuid.uuid4()),
                'content': summary_content,
                'score': 1.0,
                'metadata': {
                    'document_name': 'Knowledge Graph Summary',
                    'entity_type': 'summary',
                    'source_type': 'graph_completion',
                    'query_settings': query_settings
                }
            })
        else:
            # Process each source with enhanced metadata
            for i, source in enumerate(sources):
                doc_id = getattr(source, 'document_id', str(uuid.uuid4()))
                doc_name = 'Unknown Document'
                doc_metadata = {}
                entity_type = 'unknown'
                source_type = 'text_chunk'

                try:
                    # Fetch the original document to get its filename and other metadata
                    document = db.get_document(doc_id)
                    doc_name = getattr(document, 'filename', 'Unknown')
                    doc_metadata = getattr(document, 'metadata', {})

                    # Check if this source has entity information
                    if hasattr(source, 'entity_type'):
                        entity_type = source.entity_type
                    elif hasattr(source, 'type'):
                        entity_type = source.type

                    # Determine source type based on content and entity type
                    source_text = getattr(source, 'text', '')
                    if entity_type == 'Section':
                        source_type = 'section'
                    elif entity_type == 'Definition':
                        source_type = 'definition'
                    elif entity_type == 'Table':
                        source_type = 'table'
                    elif entity_type == 'Requirement':
                        source_type = 'requirement'
                    elif entity_type == 'Diagram':
                        source_type = 'diagram'
                    elif 'figure' in source_text.lower() or 'diagram' in source_text.lower():
                        source_type = 'diagram'
                    elif any(keyword in source_text.lower() for keyword in ['shall', 'should', 'may', 'can']):
                        source_type = 'requirement'
                    elif 'ECSS-' in source_text:
                        source_type = 'standard'
                except Exception as e:
                    print(f"Warning: Could not fetch document {doc_id} for source. {e}")
            
                # Combine metadata and add the source's text chunk as content
                final_metadata = doc_metadata.copy()
                final_metadata.update({
                    'document_name': doc_name,
                    'entity_type': entity_type,
                    'source_type': source_type,
                    'chunk_id': getattr(source, 'chunk_id', f'chunk_{i}'),
                    'score': getattr(source, 'score', 0),
                    'query_settings': query_settings
                })
                
                # The 'text' of the source is the specific chunk of text that contributed to the answer
                source_content = getattr(source, 'text', 'No content available.')

                # Create enhanced content with better formatting based on entity type
                if source_type == 'section':
                    full_content = f"**Section from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                elif source_type == 'definition':
                    full_content = f"**Definition from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                elif source_type == 'table':
                    full_content = f"**Table from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                elif source_type == 'requirement':
                    full_content = f"**Requirement from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                elif source_type == 'diagram':
                    full_content = f"**Diagram/Image from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                elif source_type == 'standard':
                    full_content = f"**Standard Reference from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"
                else:
                    full_content = f"**Evidence from {doc_name}:**\n{source_content}\n\n**Context:**\n{summary_content}"

                results.append({
                    'id': f"{doc_id}-{getattr(source, 'chunk_id', i)}", # Create a more unique ID for React keys
                    'content': full_content,
                    'score': getattr(source, 'score', 0),
                    'metadata': final_metadata
                })
        
        # Sort results by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'results': results,
            'total': len(results),
            'query': query,
            'summary': summary_content,
            'query_settings': query_settings
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 