from morphik import Morphik
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_search():
    """Test if ingested documents are searchable."""
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI not set in .env file")
        return
    
    # Initialize Morphik client
    db = Morphik(uri=morphik_uri)
    
    # First, let's check what documents we have
    print("\n=== Checking Ingested Documents ===")
    try:
        documents = db.list_documents()
        print(f"✓ Found {len(documents)} documents in Morphik")
        for doc in documents:
            print(f"  - {doc.filename} (ID: {doc.external_id})")
    except Exception as e:
        print(f"✗ Error listing documents: {e}")
        return
    
    # Test queries
    test_queries = [
        "software requirements",
        "materials testing",
        "communication protocols",
        "project planning",
        "quality assurance"
    ]
    
    print("\n=== Testing Document Search ===\n")
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        try:
            results = db.query(
                query=query,
                use_colpali=True
            )
            
            if results and hasattr(results, 'results') and len(results.results) > 0:
                print(f"✓ Found {len(results.results)} results")
                # Show first result
                first = results.results[0]
                print(f"\nTop Result:")
                print(f"  Score: {getattr(first, 'score', 'N/A')}")
                print(f"  Content: {first.content[:200]}...")
                if hasattr(first, 'metadata'):
                    print(f"  Document: {first.metadata.get('filename', 'N/A')}")
            else:
                print("✗ No results found")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
if __name__ == "__main__":
    test_search() 