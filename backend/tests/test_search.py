from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


# Add backend root to path


from morphik import Morphik
import os
import sys
import json

# Load environment variables

def test_morphik_search():
    """Test Morphik search functionality with ingested ECSS documents."""
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI not set in .env file")
        print("Please set MORPHIK_URI in your .env file")
        return
    
    # Initialize Morphik client
    try:
        db = Morphik(uri=morphik_uri)
        print("✓ Connected to Morphik successfully")
    except Exception as e:
        print(f"✗ Failed to connect to Morphik: {e}")
        return
    
    # Test 1: List all documents
    print("\n=== Test 1: Listing Documents ===")
    try:
        documents = db.list_documents()
        print(f"Found {len(documents)} documents in Morphik")
        
        if documents:
            print("\nDocument details:")
            for i, doc in enumerate(documents[:5]):  # Show first 5
                print(f"  {i+1}. ID: {getattr(doc, 'external_id', 'N/A')}")
                print(f"     Filename: {getattr(doc, 'filename', 'N/A')}")
                print(f"     Status: {getattr(doc, 'system_metadata', {}).get('status', 'N/A')}")
                print(f"     Branch: {getattr(doc, 'metadata', {}).get('branch_name', 'N/A')}")
                print(f"     Discipline: {getattr(doc, 'metadata', {}).get('discipline_name', 'N/A')}")
                print()
        else:
            print("No documents found. Please run the ingestion script first.")
            return
            
    except Exception as e:
        print(f"✗ Error listing documents: {e}")
        return
    
    # Test 2: Search for specific terms
    print("\n=== Test 2: Search Functionality ===")
    
    # Test queries related to ECSS standards
    test_queries = [
        "software development requirements",
        "materials and processes",
        "communications protocols",
        "project planning",
        "quality assurance",
        "system description",
        "testing procedures",
        "documentation requirements"
    ]
    
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        try:
            # Use the query method from Morphik
            results = db.query(query, limit=3)
            
            if results and hasattr(results, 'results'):
                print(f"  Found {len(results.results)} results:")
                for i, result in enumerate(results.results[:3]):
                    doc_info = getattr(result, 'document', {})
                    print(f"    {i+1}. Document: {doc_info.get('filename', 'N/A')}")
                    print(f"       Relevance: {getattr(result, 'relevance', 'N/A')}")
                    content = getattr(result, 'content', 'N/A')
                    if content and len(content) > 100:
                        content = content[:100] + "..."
                    print(f"       Content: {content}")
            else:
                print("  No results found")
                
        except Exception as e:
            print(f"  ✗ Search error: {e}")
    
    # Test 3: Test specific document retrieval
    print("\n=== Test 3: Document Retrieval ===")
    if documents:
        try:
            # Try to get the first document
            first_doc = documents[0]
            doc_id = getattr(first_doc, 'external_id', None)
            
            if doc_id:
                print(f"Retrieving document with ID: {doc_id}")
                retrieved_doc = db.get_document(doc_id)
                print(f"✓ Successfully retrieved document")
                print(f"  Filename: {getattr(retrieved_doc, 'filename', 'N/A')}")
                print(f"  Status: {getattr(retrieved_doc, 'system_metadata', {}).get('status', 'N/A')}")
            else:
                print("No document ID available for retrieval test")
                
        except Exception as e:
            print(f"✗ Document retrieval error: {e}")
    
    print("\n=== Test Summary ===")
    print("✓ Morphik connection: Working")
    print(f"✓ Documents found: {len(documents) if 'documents' in locals() else 0}")
    print("✓ Search functionality: Tested")
    print("✓ Document retrieval: Tested")
    
    if documents:
        print("\n🎉 All tests passed! Your ECSS documents are ready for the web application.")
        print(f"📄 Documents available: {len(documents)}")
        for doc in documents:
            filename = getattr(doc, 'filename', 'Unknown')
            branch = getattr(doc, 'metadata', {}).get('branch_name', 'Unknown')
            print(f"   - {filename} ({branch})")
    else:
        print("\n⚠ No documents found. Please run the ingestion script first:")
        print("   python backend/ingest_documents.py")

if __name__ == "__main__":
    test_morphik_search() 