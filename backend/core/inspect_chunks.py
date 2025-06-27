

#!/usr/bin/env python3
"""
Inspect chunks from recently ingested documents
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Inspect chunks from recently ingested documents
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def inspect_chunks():
    """Inspect chunks from recently ingested documents."""
    print("🔍 Inspecting Chunks from Recent Ingestion")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get recent documents
    docs = db.list_documents()
    if not docs:
        print("❌ No documents found")
        return
    
    print(f"📄 Found {len(docs)} documents")
    
    # Focus on the most recent document
    recent_doc = docs[0]
    print(f"\n🔍 Inspecting most recent document: {recent_doc.filename}")
    print(f"   Document ID: {recent_doc.external_id}")
    print(f"   Status: {recent_doc.status}")
    
    # Test different search terms to get chunks
    search_terms = [
        "ECSS", "standard", "requirement", "space", "engineering",
        "the", "and", "or", "in", "of"  # Common words to find any content
    ]
    
    print(f"\n📝 Searching for chunks with different terms:")
    
    for term in search_terms:
        try:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"\n✅ '{term}': Found {len(chunks)} chunks")
                
                # Analyze first few chunks
                for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                    print(f"\n  Chunk {i+1}:")
                    
                    # Check content type and length
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        content_length = len(content)
                        
                        print(f"    Content length: {content_length} characters")
                        
                        # Check if it's an image
                        if isinstance(content, str) and (
                            content.startswith('data:image/') or 
                            content.startswith('iVBORw0KGgo') or
                            content_length > 100000  # Likely image if very long
                        ):
                            print(f"    Type: IMAGE (base64 data)")
                            print(f"    Preview: {content[:100]}...")
                        else:
                            print(f"    Type: TEXT")
                            if content_length > 200:
                                print(f"    Preview: {content[:200]}...")
                            else:
                                print(f"    Content: {content}")
                    else:
                        print(f"    Type: NO CONTENT")
                        print(f"    Object: {chunk}")
                        
                    # Show chunk metadata if available
                    if hasattr(chunk, 'metadata') and chunk.metadata:
                        print(f"    Metadata: {chunk.metadata}")
                    if hasattr(chunk, 'score') and chunk.score:
                        print(f"    Score: {chunk.score}")
                        
            else:
                print(f"\n❌ '{term}': No chunks found")
                
        except Exception as e:
            print(f"\n❌ '{term}': Error - {e}")
    
    # Try to get chunks without any search term (all chunks)
    print(f"\n🔍 Attempting to retrieve all chunks:")
    try:
        all_chunks = db.retrieve_chunks("")  # Empty query might return all chunks
        if all_chunks:
            print(f"✅ Found {len(all_chunks)} total chunks")
            
            # Analyze chunk types
            text_chunks = 0
            image_chunks = 0
            empty_chunks = 0
            
            for chunk in all_chunks:
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    if isinstance(content, str) and (
                        content.startswith('data:image/') or 
                        content.startswith('iVBORw0KGgo') or
                        len(content) > 100000
                    ):
                        image_chunks += 1
                    else:
                        text_chunks += 1
                else:
                    empty_chunks += 1
            
            print(f"   Text chunks: {text_chunks}")
            print(f"   Image chunks: {image_chunks}")
            print(f"   Empty chunks: {empty_chunks}")
            
        else:
            print("❌ No chunks found with empty query")
            
    except Exception as e:
        print(f"❌ Error retrieving all chunks: {e}")
    
    print(f"\n📊 Summary:")
    print(f"Document: {recent_doc.filename}")
    print(f"Status: {recent_doc.status}")
    print(f"External ID: {recent_doc.external_id}")

if __name__ == "__main__":
    inspect_chunks() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def inspect_chunks():
    """Inspect chunks from recently ingested documents."""
    print("🔍 Inspecting Chunks from Recent Ingestion")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Get recent documents
    docs = db.list_documents()
    if not docs:
        print("❌ No documents found")
        return
    
    print(f"📄 Found {len(docs)} documents")
    
    # Focus on the most recent document
    recent_doc = docs[0]
    print(f"\n🔍 Inspecting most recent document: {recent_doc.filename}")
    print(f"   Document ID: {recent_doc.external_id}")
    print(f"   Status: {recent_doc.status}")
    
    # Test different search terms to get chunks
    search_terms = [
        "ECSS", "standard", "requirement", "space", "engineering",
        "the", "and", "or", "in", "of"  # Common words to find any content
    ]
    
    print(f"\n📝 Searching for chunks with different terms:")
    
    for term in search_terms:
        try:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"\n✅ '{term}': Found {len(chunks)} chunks")
                
                # Analyze first few chunks
                for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                    print(f"\n  Chunk {i+1}:")
                    
                    # Check content type and length
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        content_length = len(content)
                        
                        print(f"    Content length: {content_length} characters")
                        
                        # Check if it's an image
                        if isinstance(content, str) and (
                            content.startswith('data:image/') or 
                            content.startswith('iVBORw0KGgo') or
                            content_length > 100000  # Likely image if very long
                        ):
                            print(f"    Type: IMAGE (base64 data)")
                            print(f"    Preview: {content[:100]}...")
                        else:
                            print(f"    Type: TEXT")
                            if content_length > 200:
                                print(f"    Preview: {content[:200]}...")
                            else:
                                print(f"    Content: {content}")
                    else:
                        print(f"    Type: NO CONTENT")
                        print(f"    Object: {chunk}")
                        
                    # Show chunk metadata if available
                    if hasattr(chunk, 'metadata') and chunk.metadata:
                        print(f"    Metadata: {chunk.metadata}")
                    if hasattr(chunk, 'score') and chunk.score:
                        print(f"    Score: {chunk.score}")
                        
            else:
                print(f"\n❌ '{term}': No chunks found")
                
        except Exception as e:
            print(f"\n❌ '{term}': Error - {e}")
    
    # Try to get chunks without any search term (all chunks)
    print(f"\n🔍 Attempting to retrieve all chunks:")
    try:
        all_chunks = db.retrieve_chunks("")  # Empty query might return all chunks
        if all_chunks:
            print(f"✅ Found {len(all_chunks)} total chunks")
            
            # Analyze chunk types
            text_chunks = 0
            image_chunks = 0
            empty_chunks = 0
            
            for chunk in all_chunks:
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    if isinstance(content, str) and (
                        content.startswith('data:image/') or 
                        content.startswith('iVBORw0KGgo') or
                        len(content) > 100000
                    ):
                        image_chunks += 1
                    else:
                        text_chunks += 1
                else:
                    empty_chunks += 1
            
            print(f"   Text chunks: {text_chunks}")
            print(f"   Image chunks: {image_chunks}")
            print(f"   Empty chunks: {empty_chunks}")
            
        else:
            print("❌ No chunks found with empty query")
            
    except Exception as e:
        print(f"❌ Error retrieving all chunks: {e}")
    
    print(f"\n📊 Summary:")
    print(f"Document: {recent_doc.filename}")
    print(f"Status: {recent_doc.status}")
    print(f"External ID: {recent_doc.external_id}")

if __name__ == "__main__":
    inspect_chunks() 