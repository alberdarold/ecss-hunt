

#!/usr/bin/env python3
"""
Test retrieve_chunks API usage
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test retrieve_chunks API usage
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_chunks_api():
    """Test different ways to call retrieve_chunks."""
    print("🔍 Testing retrieve_chunks API")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get the most recent document
    docs = db.list_documents()
    if not docs:
        print("❌ No documents found")
        return
    
    doc = docs[0]
    doc_id = doc.external_id
    print(f"Testing with document: {doc.filename} (ID: {doc_id})")
    
    # Test different API calls
    print(f"\n🔍 Testing different retrieve_chunks calls:")
    
    # Method 1: Try with document_id parameter
    try:
        print("Method 1: retrieve_chunks(query='test', document_id=doc_id)")
        chunks = db.retrieve_chunks(query="test", document_id=doc_id)
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Method 2: Try with just query
    try:
        print("\nMethod 2: retrieve_chunks('test')")
        chunks = db.retrieve_chunks("test")
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Method 3: Try with doc_id parameter
    try:
        print("\nMethod 3: retrieve_chunks(query='test', doc_id=doc_id)")
        chunks = db.retrieve_chunks(query="test", doc_id=doc_id)
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_chunks_api() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_chunks_api():
    """Test different ways to call retrieve_chunks."""
    print("🔍 Testing retrieve_chunks API")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get the most recent document
    docs = db.list_documents()
    if not docs:
        print("❌ No documents found")
        return
    
    doc = docs[0]
    doc_id = doc.external_id
    print(f"Testing with document: {doc.filename} (ID: {doc_id})")
    
    # Test different API calls
    print(f"\n🔍 Testing different retrieve_chunks calls:")
    
    # Method 1: Try with document_id parameter
    try:
        print("Method 1: retrieve_chunks(query='test', document_id=doc_id)")
        chunks = db.retrieve_chunks(query="test", document_id=doc_id)
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Method 2: Try with just query
    try:
        print("\nMethod 2: retrieve_chunks('test')")
        chunks = db.retrieve_chunks("test")
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Method 3: Try with doc_id parameter
    try:
        print("\nMethod 3: retrieve_chunks(query='test', doc_id=doc_id)")
        chunks = db.retrieve_chunks(query="test", doc_id=doc_id)
        print(f"✅ Success: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2]):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"  Chunk {i+1}: {content[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_chunks_api() 