

#!/usr/bin/env python3
"""
Debug script to find actual text content in chunks.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to find actual text content in chunks.
"""

import os
import sys

# Load environment variables

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def debug_text_content():
    """Debug to find actual text content in chunks."""
    print("🔍 Debugging Text Content")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents")
    
    if not documents:
        print("❌ No documents found")
        return
    
    # Test with the first document
    doc = documents[0]
    print(f"\n🔍 Testing with document: {doc.filename}")
    print(f"   Document ID: {doc.external_id}")
    
    # Search for common words and check all chunks
    search_terms = ["the", "and", "or", "in", "of", "to", "a", "is", "that", "it"]
    
    text_chunks_found = 0
    image_chunks_found = 0
    
    for term in search_terms:
        try:
            chunks = db.retrieve_chunks(term)
            print(f"\n📝 Searching for '{term}': {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    
                    if isinstance(content, str):
                        if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                            image_chunks_found += 1
                            if image_chunks_found <= 3:  # Show first 3 image chunks
                                print(f"   Chunk {i+1}: IMAGE (base64 data, length: {len(content)})")
                        else:
                            text_chunks_found += 1
                            if text_chunks_found <= 5:  # Show first 5 text chunks
                                preview = content[:300] + "..." if len(content) > 300 else content
                                print(f"   Chunk {i+1}: TEXT (length: {len(content)})")
                                print(f"      Preview: {preview}")
                                print()
            
            # Only check first term to avoid too much output
            if term == "the":
                break
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Text chunks found: {text_chunks_found}")
    print(f"   Image chunks found: {image_chunks_found}")
    
    if text_chunks_found == 0:
        print("\n❌ PROBLEM: No text content found! All chunks are images.")
        print("   This indicates a PDF processing issue where Morphik is only extracting images.")
        print("   The PDF may be image-based or Morphik's text extraction is not working properly.")
    else:
        print(f"\n✅ Found {text_chunks_found} text chunks with actual content.")

if __name__ == "__main__":
    debug_text_content() 

import os
import sys

# Load environment variables

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def debug_text_content():
    """Debug to find actual text content in chunks."""
    print("🔍 Debugging Text Content")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents")
    
    if not documents:
        print("❌ No documents found")
        return
    
    # Test with the first document
    doc = documents[0]
    print(f"\n🔍 Testing with document: {doc.filename}")
    print(f"   Document ID: {doc.external_id}")
    
    # Search for common words and check all chunks
    search_terms = ["the", "and", "or", "in", "of", "to", "a", "is", "that", "it"]
    
    text_chunks_found = 0
    image_chunks_found = 0
    
    for term in search_terms:
        try:
            chunks = db.retrieve_chunks(term)
            print(f"\n📝 Searching for '{term}': {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    
                    if isinstance(content, str):
                        if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                            image_chunks_found += 1
                            if image_chunks_found <= 3:  # Show first 3 image chunks
                                print(f"   Chunk {i+1}: IMAGE (base64 data, length: {len(content)})")
                        else:
                            text_chunks_found += 1
                            if text_chunks_found <= 5:  # Show first 5 text chunks
                                preview = content[:300] + "..." if len(content) > 300 else content
                                print(f"   Chunk {i+1}: TEXT (length: {len(content)})")
                                print(f"      Preview: {preview}")
                                print()
            
            # Only check first term to avoid too much output
            if term == "the":
                break
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Text chunks found: {text_chunks_found}")
    print(f"   Image chunks found: {image_chunks_found}")
    
    if text_chunks_found == 0:
        print("\n❌ PROBLEM: No text content found! All chunks are images.")
        print("   This indicates a PDF processing issue where Morphik is only extracting images.")
        print("   The PDF may be image-based or Morphik's text extraction is not working properly.")
    else:
        print(f"\n✅ Found {text_chunks_found} text chunks with actual content.")

if __name__ == "__main__":
    debug_text_content() 