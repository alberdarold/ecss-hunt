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

# Load environment variables

def test_environment():
    """Test environment setup."""
    print("=== Environment Test ===")
    
    # Check MORPHIK_URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("✗ MORPHIK_URI not set in environment")
        return False
    
    print(f"✓ MORPHIK_URI is set: {morphik_uri[:20]}...")
    return True

def test_morphik_connection():
    """Test Morphik connection and basic functionality."""
    print("\n=== Morphik Connection Test ===")
    
    morphik_uri = os.getenv("MORPHIK_URI")
    
    try:
        db = Morphik(uri=morphik_uri)
        print("✓ Successfully connected to Morphik")
        
        # Test basic API calls
        try:
            docs = db.list_documents()
            print(f"✓ Can list documents: {len(docs)} found")
        except Exception as e:
            print(f"⚠ Warning: Could not list documents: {e}")
        
        return True, db
        
    except Exception as e:
        print(f"✗ Failed to connect to Morphik: {e}")
        return False, None

def test_document_access():
    """Test access to ECSS documents."""
    print("\n=== Document Access Test ===")
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_directory = os.path.join(project_root, "ECSS Published Standards", "1-Active Standards")
    
    if not os.path.exists(pdf_directory):
        print(f"✗ PDF directory not found: {pdf_directory}")
        return False
    
    print(f"✓ PDF directory exists: {pdf_directory}")
    
    # Test access to a few key documents
    test_docs = [
        "ECSS-S-ST-00C Rev.1(15June2020).pdf",
        "ECSS-Q-ST-70C-Rev.2(15October2019).pdf"
    ]
    
    accessible_docs = []
    for doc in test_docs:
        full_path = os.path.join(pdf_directory, doc)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"✓ {doc} ({size / 1024 / 1024:.1f} MB)")
            accessible_docs.append(doc)
        else:
            print(f"✗ {doc} not found")
    
    return len(accessible_docs) > 0

def test_single_document_ingestion(db):
    """Test ingesting a single small document."""
    print("\n=== Single Document Ingestion Test ===")
    
    if not db:
        print("✗ No Morphik connection available")
        return False
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_directory = os.path.join(project_root, "ECSS Published Standards", "1-Active Standards")
    
    # Try to ingest the smallest document first
    test_doc = "ECSS-M-ST-10C_Rev.1(6March2009).pdf"
    full_path = os.path.join(pdf_directory, test_doc)
    
    if not os.path.exists(full_path):
        print(f"✗ Test document not found: {test_doc}")
        return False
    
    try:
        print(f"Testing ingestion of {test_doc}...")
        doc = db.ingest_file(
            file=full_path,
            filename=test_doc,
            use_colpali=True
        )
        
        doc_id = getattr(doc, 'external_id', 'N/A')
        print(f"✓ Successfully ingested test document")
        print(f"  Document ID: {doc_id}")
        
        # Clean up - delete the test document
        try:
            db.delete_document(doc_id)
            print(f"✓ Cleaned up test document")
        except Exception as e:
            print(f"⚠ Warning: Could not clean up test document: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to ingest test document: {e}")
        return False

def main():
    """Run all system tests."""
    print("=== ECSS System Pre-Ingestion Test ===")
    
    # Test 1: Environment
    if not test_environment():
        print("\n✗ Environment test failed. Please check your .env file.")
        sys.exit(1)
    
    # Test 2: Morphik connection
    connection_ok, db = test_morphik_connection()
    if not connection_ok:
        print("\n✗ Morphik connection test failed. Please check your MORPHIK_URI.")
        sys.exit(1)
    
    # Test 3: Document access
    if not test_document_access():
        print("\n✗ Document access test failed. Please check your PDF directory.")
        sys.exit(1)
    
    # Test 4: Single document ingestion
    if not test_single_document_ingestion(db):
        print("\n✗ Single document ingestion test failed.")
        print("This might indicate issues with the Morphik setup or document format.")
        sys.exit(1)
    
    print("\n=== All Tests Passed! ===")
    print("✓ Environment is properly configured")
    print("✓ Morphik connection is working")
    print("✓ Documents are accessible")
    print("✓ Document ingestion is working")
    print("\n🎉 You're ready to run the full ingestion process!")
    print("Run: python ingest_documents_safe.py")

if __name__ == "__main__":
    main() 