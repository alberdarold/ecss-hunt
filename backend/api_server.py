from flask import Flask, request, jsonify
from flask_cors import CORS
from morphik import Morphik
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://ecss-hunt.vercel.app"])  # Enable CORS for Vercel frontend

# Initialize Morphik client
def get_morphik_client():
    """Get Morphik client instance."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI not set in .env file")
        return None
    
    try:
        return Morphik(uri=morphik_uri)
    except Exception as e:
        print(f"✗ Failed to connect to Morphik: {e}")
        return None

@app.route('/api/search', methods=['GET'])
def search():
    """Search ECSS documents using Morphik."""
    query = request.args.get('q', '')
    
    if not query.strip():
        return jsonify({
            'results': [],
            'total': 0,
            'query': query
        })
    
    try:
        # Get Morphik client
        db = get_morphik_client()
        if not db:
            return jsonify({
                'results': [],
                'total': 0,
                'error': 'Morphik connection failed',
                'query': query
            })
        
        # Search using Morphik
        print(f"Searching Morphik for: '{query}'")
        morphik_response = db.query(query)
        
        # Convert Morphik response to our format
        results = []
        
        if morphik_response and hasattr(morphik_response, 'completion'):
            # Get document info from sources
            document_info = None
            if hasattr(morphik_response, 'sources') and morphik_response.sources:
                # Get the first source document
                first_source = morphik_response.sources[0]
                doc_id = getattr(first_source, 'document_id', None)
                
                if doc_id:
                    try:
                        document = db.get_document(doc_id)
                        document_info = {
                            'filename': getattr(document, 'filename', 'Unknown'),
                            'metadata': getattr(document, 'metadata', {})
                        }
                    except Exception as e:
                        print(f"Error getting document {doc_id}: {e}")
            
            # Create result
            result = {
                'id': getattr(morphik_response.sources[0], 'document_id', '1') if morphik_response.sources else '1',
                'title': document_info['filename'] if document_info else 'ECSS Document',
                'content': morphik_response.completion,
                'score': 0.95,  # Default score
                'relevance': getattr(morphik_response.sources[0], 'score', 0) if morphik_response.sources else 0,
                'metadata': document_info['metadata'] if document_info else {
                    'branch': 'S',
                    'branch_name': 'Space Product Assurance',
                    'discipline': 'ST',
                    'discipline_name': 'Space Systems',
                    'document_number': '00C',
                    'revision': '1',
                    'filename': document_info['filename'] if document_info else 'Unknown',
                    'document_type': 'ECSS_Standard',
                    'source': 'ECSS_Published_Standards'
                }
            }
            results.append(result)
        
        return jsonify({
            'results': results,
            'total': len(results),
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

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents in Morphik."""
    try:
        db = get_morphik_client()
        if not db:
            return jsonify({
                'documents': [],
                'total': 0,
                'error': 'Morphik connection failed'
            })
        
        documents = db.list_documents()
        
        doc_list = []
        for doc in documents:
            doc_info = {
                'id': getattr(doc, 'external_id', 'Unknown'),
                'filename': getattr(doc, 'filename', 'Unknown'),
                'status': getattr(doc, 'system_metadata', {}).get('status', 'Unknown'),
                'metadata': getattr(doc, 'metadata', {})
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
            'total': 0,
            'error': str(e)
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        db = get_morphik_client()
        if db:
            return jsonify({
                'status': 'healthy',
                'morphik_connected': True
            })
        else:
            return jsonify({
                'status': 'degraded',
                'morphik_connected': False
            })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'morphik_connected': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("Starting ECSS Standards Navigator API Server...")
    print("Available endpoints:")
    print("  GET /api/search?q=<query> - Search ECSS documents")
    print("  GET /api/documents - List all documents")
    print("  GET /api/health - Health check")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 