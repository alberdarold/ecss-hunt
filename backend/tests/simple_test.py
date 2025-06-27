

#!/usr/bin/env python3
"""
Simple Test Script to Understand Document Object Structure
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Simple Test Script to Understand Document Object Structure
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_document_structure():
    """Test document structure and ID access."""
    print("🔍 Testing Document Structure")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Create a simple document
    print("\n📝 Creating test document...")
    test_text = "This is a test document for debugging."
    doc = db.ingest_text(test_text, filename="simple_test.txt")
    
    print(f"Document type: {type(doc)}")
    print(f"Document attributes:")
    
    # List all attributes
    for attr in dir(doc):
        if not attr.startswith('_') and not callable(getattr(doc, attr)):
            try:
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            except Exception as e:
                print(f"  {attr}: Error - {e}")
    
    # Test 2: Try to get document ID
    print(f"\n🔍 Trying to get document ID...")
    doc_id = None
    
    for attr in ['id', 'external_id', 'document_id', 'doc_id']:
        if hasattr(doc, attr):
            value = getattr(doc, attr)
            if value:
                doc_id = value
                print(f"✅ Found ID in {attr}: {doc_id}")
                break
    
    if not doc_id:
        print("❌ No document ID found")
        return
    
    # Test 3: Try to retrieve chunks
    print(f"\n🔍 Testing chunk retrieval...")
    try:
        chunks = db.retrieve_chunks(doc_id, query="test")
        print(f"✅ Retrieved {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Error retrieving chunks: {e}")
    
    # Test 4: Try to get document by ID
    print(f"\n🔍 Testing document retrieval...")
    try:
        retrieved = db.get_document(doc_id)
        print(f"✅ Retrieved document: {type(retrieved)}")
        
        if hasattr(retrieved, 'metadata'):
            print(f"Metadata: {retrieved.metadata}")
        else:
            print("No metadata attribute")
    except Exception as e:
        print(f"❌ Error retrieving document: {e}")

if __name__ == "__main__":
    test_document_structure() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_document_structure():
    """Test document structure and ID access."""
    print("🔍 Testing Document Structure")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Create a simple document
    print("\n📝 Creating test document...")
    test_text = "This is a test document for debugging."
    doc = db.ingest_text(test_text, filename="simple_test.txt")
    
    print(f"Document type: {type(doc)}")
    print(f"Document attributes:")
    
    # List all attributes
    for attr in dir(doc):
        if not attr.startswith('_') and not callable(getattr(doc, attr)):
            try:
                value = getattr(doc, attr)
                print(f"  {attr}: {value}")
            except Exception as e:
                print(f"  {attr}: Error - {e}")
    
    # Test 2: Try to get document ID
    print(f"\n🔍 Trying to get document ID...")
    doc_id = None
    
    for attr in ['id', 'external_id', 'document_id', 'doc_id']:
        if hasattr(doc, attr):
            value = getattr(doc, attr)
            if value:
                doc_id = value
                print(f"✅ Found ID in {attr}: {doc_id}")
                break
    
    if not doc_id:
        print("❌ No document ID found")
        return
    
    # Test 3: Try to retrieve chunks
    print(f"\n🔍 Testing chunk retrieval...")
    try:
        chunks = db.retrieve_chunks(doc_id, query="test")
        print(f"✅ Retrieved {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Error retrieving chunks: {e}")
    
    # Test 4: Try to get document by ID
    print(f"\n🔍 Testing document retrieval...")
    try:
        retrieved = db.get_document(doc_id)
        print(f"✅ Retrieved document: {type(retrieved)}")
        
        if hasattr(retrieved, 'metadata'):
            print(f"Metadata: {retrieved.metadata}")
        else:
            print("No metadata attribute")
    except Exception as e:
        print(f"❌ Error retrieving document: {e}")

if __name__ == "__main__":
    test_document_structure() 