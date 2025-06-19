from morphik import Morphik
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def explore_morphik_api():
    """Explore the available methods in Morphik API."""
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI not set in .env file")
        return
    
    # Initialize Morphik client
    db = Morphik(uri=morphik_uri)
    
    print("=== Exploring Morphik API ===")
    print(f"Morphik object type: {type(db)}")
    print(f"Available methods: {[method for method in dir(db) if not method.startswith('_')]}")
    
    # Try to get documents
    try:
        print("\n=== Trying to get documents ===")
        documents = db.get_documents()
        print(f"Documents: {documents}")
    except Exception as e:
        print(f"Error getting documents: {e}")
    
    # Try to get document by ID
    try:
        print("\n=== Trying to get document by ID ===")
        # Use one of the document IDs from our ingestion
        doc_id = "8b19510b-d35b-4dd6-af9f-86f20cbc72d3"
        document = db.get_document(doc_id)
        print(f"Document: {document}")
    except Exception as e:
        print(f"Error getting document: {e}")

if __name__ == "__main__":
    explore_morphik_api() 