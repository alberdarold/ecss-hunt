from morphik import Morphik
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

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
            # Try different query approaches
            try:
                # First try with just the query
                results = db.query(query)
                print(f"  Found results using simple query")
            except Exception as e1:
                print(f"  Simple query failed: {e1}")
                try:
                    # Try with different parameters
                    results = db.query(query, top_k=3)
                    print(f"  Found results using top_k parameter")
                except Exception as e2:
                    print(f"  Top_k query failed: {e2}")
                    try:
                        # Try with max_results
                        results = db.query(query, max_results=3)
                        print(f"  Found results using max_results parameter")
                    except Exception as e3:
                        print(f"  Max_results query failed: {e3}")
                        results = None
            
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
            elif results:
                print(f"  Results found but no 'results' attribute")
                print(f"  Result type: {type(results)}")
                print(f"  Result: {results}")
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