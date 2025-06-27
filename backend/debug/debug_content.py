#!/usr/bin/env python3
"""
Debug script to check document content and metadata extraction.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to check document content and metadata extraction.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import os
import sys

# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from morphik import Morphik
from core.schemas import BaseModel, Field, MetadataExtractionRule

class SimpleTest(BaseModel):
    title: str = Field(description="Document title")
    document_type: str = Field(description="Type of document")

def debug_content():
    """Debug the document content and metadata extraction."""
    print("=== CONTENT DEBUG ===")
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("MORPHIK_URI not set")
        return
    
    db = Morphik(morphik_uri)
    
    # Get the last ingested document
    documents = db.list_documents()
    if not documents:
        print("No documents found")
        return
    
    doc = documents[0]  # Get the most recent document
    print(f"Analyzing document: {doc.filename}")
    print(f"Document ID: {doc.external_id}")
    
    # Check all available attributes
    print(f"\nDocument attributes:")
    for attr in dir(doc):
        if not attr.startswith('_'):
            try:
                value = getattr(doc, attr)
                if callable(value):
                    print(f"  {attr}: <method>")
                else:
                    print(f"  {attr}: {value}")
            except Exception as e:
                print(f"  {attr}: <error: {e}>")
    
    # Check if there's a way to get the actual content
    print(f"\nChecking for content extraction methods...")
    
    # Try to get chunks using the correct API
    try:
        print("\nRetrieving chunks with query...")
        chunks = db.retrieve_chunks(
            "What are the key findings?",
            filters={"document_id": doc.external_id},
            k=5
        )
        print(f"Found {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1} (score: {getattr(chunk, 'score', 'N/A')}): {getattr(chunk, 'content', '')[:200]}...")
    except Exception as e:
        print(f"Could not retrieve chunks: {e}")
        
        # Try alternative method
        try:
            print("Trying alternative chunk retrieval...")
            # Try to get chunks by document ID
            chunks = db.retrieve_chunks(doc.external_id, skip=0, limit=5)
            print(f"Found {len(chunks)} chunks with alternative method:")
            for i, chunk in enumerate(chunks[:3]):
                print(f"  Chunk {i+1}: {chunk.text[:200]}...")
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")
    
    # Check system metadata for content
    if hasattr(doc, 'system_metadata'):
        print(f"\nSystem metadata:")
        for key, value in doc.system_metadata.items():
            print(f"  {key}: {value}")
    
    # Check if there are any other content-related fields
    print(f"\nChecking for content in various fields...")
    
    # Try different ways to access content
    content_fields = ['content', 'text', 'body', 'data', 'extracted_text']
    for field in content_fields:
        if hasattr(doc, field):
            value = getattr(doc, field)
            if value:
                print(f"  {field}: {str(value)[:200]}...")
            else:
                print(f"  {field}: <empty>")
        else:
            print(f"  {field}: <not found>")

if __name__ == "__main__":
    debug_content() 

import os
import sys

# Add backend root to path

from morphik import Morphik
from core.schemas import BaseModel, Field, MetadataExtractionRule

class SimpleTest(BaseModel):
    title: str = Field(description="Document title")
    document_type: str = Field(description="Type of document")

def debug_content():
    """Debug the document content and metadata extraction."""
    print("=== CONTENT DEBUG ===")
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("MORPHIK_URI not set")
        return
    
    db = Morphik(morphik_uri)
    
    # Get the last ingested document
    documents = db.list_documents()
    if not documents:
        print("No documents found")
        return
    
    doc = documents[0]  # Get the most recent document
    print(f"Analyzing document: {doc.filename}")
    print(f"Document ID: {doc.external_id}")
    
    # Check all available attributes
    print(f"\nDocument attributes:")
    for attr in dir(doc):
        if not attr.startswith('_'):
            try:
                value = getattr(doc, attr)
                if callable(value):
                    print(f"  {attr}: <method>")
                else:
                    print(f"  {attr}: {value}")
            except Exception as e:
                print(f"  {attr}: <error: {e}>")
    
    # Check if there's a way to get the actual content
    print(f"\nChecking for content extraction methods...")
    
    # Try to get chunks using the correct API
    try:
        print("\nRetrieving chunks with query...")
        chunks = db.retrieve_chunks(
            "What are the key findings?",
            filters={"document_id": doc.external_id},
            k=5
        )
        print(f"Found {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1} (score: {getattr(chunk, 'score', 'N/A')}): {getattr(chunk, 'content', '')[:200]}...")
    except Exception as e:
        print(f"Could not retrieve chunks: {e}")
        
        # Try alternative method
        try:
            print("Trying alternative chunk retrieval...")
            # Try to get chunks by document ID
            chunks = db.retrieve_chunks(doc.external_id, skip=0, limit=5)
            print(f"Found {len(chunks)} chunks with alternative method:")
            for i, chunk in enumerate(chunks[:3]):
                print(f"  Chunk {i+1}: {chunk.text[:200]}...")
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")
    
    # Check system metadata for content
    if hasattr(doc, 'system_metadata'):
        print(f"\nSystem metadata:")
        for key, value in doc.system_metadata.items():
            print(f"  {key}: {value}")
    
    # Check if there are any other content-related fields
    print(f"\nChecking for content in various fields...")
    
    # Try different ways to access content
    content_fields = ['content', 'text', 'body', 'data', 'extracted_text']
    for field in content_fields:
        if hasattr(doc, field):
            value = getattr(doc, field)
            if value:
                print(f"  {field}: {str(value)[:200]}...")
            else:
                print(f"  {field}: <empty>")
        else:
            print(f"  {field}: <not found>")

if __name__ == "__main__":
    debug_content() 