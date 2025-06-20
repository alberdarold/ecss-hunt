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
    
    # Get all available methods
    methods = [method for method in dir(db) if not method.startswith('_')]
    print(f"Available methods: {methods}")
    
    # Try different possible method names for getting documents
    possible_doc_methods = ['get_documents', 'list_documents', 'documents', 'list', 'get_all']
    
    for method_name in possible_doc_methods:
        if hasattr(db, method_name):
            print(f"\nFound method: {method_name}")
            try:
                result = getattr(db, method_name)()
                print(f"Result: {result}")
                print(f"Type: {type(result)}")
                if hasattr(result, '__len__'):
                    print(f"Length: {len(result)}")
            except Exception as e:
                print(f"Error calling {method_name}: {e}")
    
    # Try search method
    if hasattr(db, 'search'):
        print(f"\nSearch method available")
        try:
            # Try a simple search
            result = db.search("test", limit=1)
            print(f"Search result type: {type(result)}")
            print(f"Search result: {result}")
        except Exception as e:
            print(f"Search error: {e}")
    
    # Try to get document by ID if we have any
    if hasattr(db, 'get_document'):
        print(f"\nGet document method available")
        # We'll need a document ID to test this

if __name__ == "__main__":
    explore_morphik_api() 