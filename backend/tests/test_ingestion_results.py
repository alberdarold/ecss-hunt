
# Add backend root to path


#!/usr/bin/env python3
"""
Test script to check what we're actually getting from ingested documents
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script to check what we're actually getting from ingested documents
"""

import os
import sys
import json
from morphik import Morphik

# Load environment variables

def test_ingestion_results():
    """Test what we're actually getting from ingested documents"""
    
    # Connect to Morphik
    morphik_uri = os.getenv('MORPHIK_URI')
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    print("🔍 Testing ingestion results...")
    print(f"Connecting to: {morphik_uri[:50]}...")
    
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents")
        
        if not documents:
            print("❌ No documents found!")
            return
        
        # Test the first document
        doc = documents[0]
        print(f"\n🔍 Testing document: {doc.filename}")
        print(f"   ID: {doc.external_id}")
        print(f"   Status: {doc.status}")
        
        # Get document metadata
        print(f"\n📋 Document Metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"   Metadata: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("   ❌ No metadata found!")
        
        # Get chunks
        print(f"\n📝 Document Chunks:")
        chunks = db.retrieve_chunks(doc.external_id)
        print(f"   Found {len(chunks)} chunks (showing first 5)")
        
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n   Chunk {i+1}:")
            print(f"     Content: {chunk.content[:200]}...")
            if hasattr(chunk, 'metadata') and chunk.metadata:
                print(f"     Metadata: {json.dumps(chunk.metadata, indent=4)}")
            else:
                print("     ❌ No chunk metadata!")
        
        # Test search
        print(f"\n🔍 Testing search functionality:")
        search_results = db.search("ECSS standard", limit=3)
        print(f"   Search results: {len(search_results)} found")
        
        for i, result in enumerate(search_results[:3]):
            print(f"   Result {i+1}: {result.content[:100]}...")
        
        print(f"\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ingestion_results() 

import os
import sys
import json
from morphik import Morphik

# Load environment variables

def test_ingestion_results():
    """Test what we're actually getting from ingested documents"""
    
    # Connect to Morphik
    morphik_uri = os.getenv('MORPHIK_URI')
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    print("🔍 Testing ingestion results...")
    print(f"Connecting to: {morphik_uri[:50]}...")
    
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents")
        
        if not documents:
            print("❌ No documents found!")
            return
        
        # Test the first document
        doc = documents[0]
        print(f"\n🔍 Testing document: {doc.filename}")
        print(f"   ID: {doc.external_id}")
        print(f"   Status: {doc.status}")
        
        # Get document metadata
        print(f"\n📋 Document Metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"   Metadata: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("   ❌ No metadata found!")
        
        # Get chunks
        print(f"\n📝 Document Chunks:")
        chunks = db.retrieve_chunks(doc.external_id)
        print(f"   Found {len(chunks)} chunks (showing first 5)")
        
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n   Chunk {i+1}:")
            print(f"     Content: {chunk.content[:200]}...")
            if hasattr(chunk, 'metadata') and chunk.metadata:
                print(f"     Metadata: {json.dumps(chunk.metadata, indent=4)}")
            else:
                print("     ❌ No chunk metadata!")
        
        # Test search
        print(f"\n🔍 Testing search functionality:")
        search_results = db.search("ECSS standard", limit=3)
        print(f"   Search results: {len(search_results)} found")
        
        for i, result in enumerate(search_results[:3]):
            print(f"   Result {i+1}: {result.content[:100]}...")
        
        print(f"\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ingestion_results() 