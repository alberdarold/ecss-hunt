

#!/usr/bin/env python3
"""
Debug Document Object Structure
Understanding how to access document properties in Morphik.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug Document Object Structure
Understanding how to access document properties in Morphik.
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def debug_document_structure():
    """Debug the Document object structure."""
    print("🔍 Debugging Document Object Structure")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Check existing documents
    print("\n📄 Checking existing documents...")
    documents = db.list_documents()
    print(f"Found {len(documents)} documents")
    
    for i, doc in enumerate(documents[:3], 1):
        print(f"\n--- Document {i} ---")
        print(f"Type: {type(doc)}")
        print(f"Dir: {dir(doc)}")
        
        # Try different ways to get document ID
        print(f"\nTrying to get document ID:")
        for attr in ['id', 'external_id', 'document_id', 'doc_id', 'uuid']:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Check other attributes
        print(f"\nOther attributes:")
        for attr in ['filename', 'name', 'title', 'status', 'metadata']:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
    
    # Test 2: Create a new document and examine it
    print("\n🧪 Creating a new test document...")
    try:
        test_text = "This is a test document for debugging."
        new_doc = db.ingest_text(test_text, filename="debug_test.txt")
        
        print(f"New document type: {type(new_doc)}")
        print(f"New document dir: {dir(new_doc)}")
        
        # Check for ID
        print(f"\nNew document ID attributes:")
        for attr in ['id', 'external_id', 'document_id', 'doc_id', 'uuid']:
            if hasattr(new_doc, attr):
                value = getattr(new_doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Check other attributes
        print(f"\nNew document other attributes:")
        for attr in ['filename', 'name', 'title', 'status', 'metadata']:
            if hasattr(new_doc, attr):
                value = getattr(new_doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Try to get document by different methods
        print(f"\n🔍 Trying to retrieve document...")
        
        # Method 1: Try with external_id
        if hasattr(new_doc, 'external_id'):
            try:
                retrieved = db.get_document(new_doc.external_id)
                print(f"✅ Retrieved by external_id: {type(retrieved)}")
            except Exception as e:
                print(f"❌ Failed to retrieve by external_id: {e}")
        
        # Method 2: Try with filename
        try:
            retrieved = db.get_document_by_filename("debug_test.txt")
            print(f"✅ Retrieved by filename: {type(retrieved)}")
        except Exception as e:
            print(f"❌ Failed to retrieve by filename: {e}")
        
        # Method 3: Try to get chunks
        print(f"\n🔍 Trying to retrieve chunks...")
        try:
            # Try different ways to get document ID for chunks
            doc_id = None
            for attr in ['id', 'external_id', 'document_id']:
                if hasattr(new_doc, attr):
                    doc_id = getattr(new_doc, attr)
                    break
            
            if doc_id:
                chunks = db.retrieve_chunks(doc_id, query="test")
                print(f"✅ Retrieved {len(chunks)} chunks using {doc_id}")
            else:
                print("❌ Could not find document ID for chunks")
        except Exception as e:
            print(f"❌ Failed to retrieve chunks: {e}")
        
    except Exception as e:
        print(f"❌ Error creating test document: {e}")
        import traceback
        traceback.print_exc()

def test_document_methods():
    """Test different methods to access document properties."""
    print("\n🧪 Testing Document Methods")
    print("=" * 40)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get a document
    documents = db.list_documents()
    if not documents:
        print("❌ No documents found")
        return
    
    doc = documents[0]
    print(f"Testing with document: {getattr(doc, 'filename', 'Unknown')}")
    
    # Test different ways to access document properties
    print(f"\n📋 Document properties:")
    
    # Try direct attribute access
    for attr in ['id', 'external_id', 'document_id', 'filename', 'status', 'metadata']:
        try:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        except Exception as e:
            print(f"  {attr}: Error - {e}")
    
    # Try dictionary access
    print(f"\n📋 Dictionary access:")
    try:
        doc_dict = dict(doc)
        print(f"  As dict: {doc_dict}")
    except Exception as e:
        print(f"  Dict conversion failed: {e}")
    
    # Try JSON serialization
    print(f"\n📋 JSON serialization:")
    try:
        import json
        doc_json = json.dumps(doc, default=str)
        print(f"  As JSON: {doc_json}")
    except Exception as e:
        print(f"  JSON serialization failed: {e}")

if __name__ == "__main__":
    debug_document_structure()
    test_document_methods() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def debug_document_structure():
    """Debug the Document object structure."""
    print("🔍 Debugging Document Object Structure")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Check existing documents
    print("\n📄 Checking existing documents...")
    documents = db.list_documents()
    print(f"Found {len(documents)} documents")
    
    for i, doc in enumerate(documents[:3], 1):
        print(f"\n--- Document {i} ---")
        print(f"Type: {type(doc)}")
        print(f"Dir: {dir(doc)}")
        
        # Try different ways to get document ID
        print(f"\nTrying to get document ID:")
        for attr in ['id', 'external_id', 'document_id', 'doc_id', 'uuid']:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Check other attributes
        print(f"\nOther attributes:")
        for attr in ['filename', 'name', 'title', 'status', 'metadata']:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
    
    # Test 2: Create a new document and examine it
    print("\n🧪 Creating a new test document...")
    try:
        test_text = "This is a test document for debugging."
        new_doc = db.ingest_text(test_text, filename="debug_test.txt")
        
        print(f"New document type: {type(new_doc)}")
        print(f"New document dir: {dir(new_doc)}")
        
        # Check for ID
        print(f"\nNew document ID attributes:")
        for attr in ['id', 'external_id', 'document_id', 'doc_id', 'uuid']:
            if hasattr(new_doc, attr):
                value = getattr(new_doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Check other attributes
        print(f"\nNew document other attributes:")
        for attr in ['filename', 'name', 'title', 'status', 'metadata']:
            if hasattr(new_doc, attr):
                value = getattr(new_doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        
        # Try to get document by different methods
        print(f"\n🔍 Trying to retrieve document...")
        
        # Method 1: Try with external_id
        if hasattr(new_doc, 'external_id'):
            try:
                retrieved = db.get_document(new_doc.external_id)
                print(f"✅ Retrieved by external_id: {type(retrieved)}")
            except Exception as e:
                print(f"❌ Failed to retrieve by external_id: {e}")
        
        # Method 2: Try with filename
        try:
            retrieved = db.get_document_by_filename("debug_test.txt")
            print(f"✅ Retrieved by filename: {type(retrieved)}")
        except Exception as e:
            print(f"❌ Failed to retrieve by filename: {e}")
        
        # Method 3: Try to get chunks
        print(f"\n🔍 Trying to retrieve chunks...")
        try:
            # Try different ways to get document ID for chunks
            doc_id = None
            for attr in ['id', 'external_id', 'document_id']:
                if hasattr(new_doc, attr):
                    doc_id = getattr(new_doc, attr)
                    break
            
            if doc_id:
                chunks = db.retrieve_chunks(doc_id, query="test")
                print(f"✅ Retrieved {len(chunks)} chunks using {doc_id}")
            else:
                print("❌ Could not find document ID for chunks")
        except Exception as e:
            print(f"❌ Failed to retrieve chunks: {e}")
        
    except Exception as e:
        print(f"❌ Error creating test document: {e}")
        import traceback
        traceback.print_exc()

def test_document_methods():
    """Test different methods to access document properties."""
    print("\n🧪 Testing Document Methods")
    print("=" * 40)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get a document
    documents = db.list_documents()
    if not documents:
        print("❌ No documents found")
        return
    
    doc = documents[0]
    print(f"Testing with document: {getattr(doc, 'filename', 'Unknown')}")
    
    # Test different ways to access document properties
    print(f"\n📋 Document properties:")
    
    # Try direct attribute access
    for attr in ['id', 'external_id', 'document_id', 'filename', 'status', 'metadata']:
        try:
            if hasattr(doc, attr):
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            else:
                print(f"  {attr}: Not found")
        except Exception as e:
            print(f"  {attr}: Error - {e}")
    
    # Try dictionary access
    print(f"\n📋 Dictionary access:")
    try:
        doc_dict = dict(doc)
        print(f"  As dict: {doc_dict}")
    except Exception as e:
        print(f"  Dict conversion failed: {e}")
    
    # Try JSON serialization
    print(f"\n📋 JSON serialization:")
    try:
        import json
        doc_json = json.dumps(doc, default=str)
        print(f"  As JSON: {doc_json}")
    except Exception as e:
        print(f"  JSON serialization failed: {e}")

if __name__ == "__main__":
    debug_document_structure()
    test_document_methods() 