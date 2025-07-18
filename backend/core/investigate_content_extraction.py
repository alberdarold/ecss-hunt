#!/usr/bin/env python3
"""
Investigate how to properly extract processed content from visual elements.
The PIL Images are raw data - we need the text/understanding Morphik extracted.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
from morphik import Morphik

def investigate_content_extraction():
    """Investigate how to extract actual content from visual elements."""
    print("Investigating Content Extraction from Visual Elements")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found")
        return
    
    try:
        # Initialize Morphik
        db = Morphik(morphik_uri)
        print("SUCCESS: Connected to Morphik")
        
        # Get all possible ways to access content
        print("\n1. Testing retrieve_chunks() - Deep Analysis")
        chunks = db.retrieve_chunks("ECSS")
        
        if chunks:
            print(f"Found {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks[:3]):  # Analyze first 3 chunks
                print(f"\n--- CHUNK {i+1} DEEP ANALYSIS ---")
                print(f"Type: {type(chunk)}")
                
                # Check ALL attributes
                all_attrs = [attr for attr in dir(chunk) if not attr.startswith('_')]
                print(f"All attributes: {all_attrs}")
                
                # Check each attribute for content
                for attr in all_attrs:
                    try:
                        value = getattr(chunk, attr)
                        if value is not None:
                            print(f"  {attr}: {type(value)}")
                            
                            # If it's a string and looks like content
                            if isinstance(value, str) and len(value) > 10:
                                print(f"    Content preview: {value[:200]}...")
                            
                            # If it's a dict, explore it
                            elif isinstance(value, dict):
                                print(f"    Dict keys: {list(value.keys())}")
                                for k, v in value.items():
                                    if isinstance(v, str) and len(v) > 10:
                                        print(f"      {k}: {v[:100]}...")
                            
                            # If it's a PIL Image
                            elif hasattr(value, '__class__') and 'PIL' in str(type(value).__module__):
                                print(f"    PIL Image: {type(value).__name__} - Size: {getattr(value, 'size', 'unknown')}")
                    except Exception as e:
                        print(f"  {attr}: ERROR - {e}")
        
        # Test different query approaches
        print(f"\n2. Testing query() with response analysis")
        response = db.query("What are the main requirements in the ECSS document?", use_colpali=True)
        
        print(f"Response type: {type(response)}")
        print(f"Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
        
        # Check response content
        if hasattr(response, 'completion') and response.completion:
            print(f"Completion: {response.completion}")
        
        if hasattr(response, 'response') and response.response:
            print(f"Response: {response.response}")
        else:
            print("No response text found")
        
        # Check response metadata
        if hasattr(response, 'metadata') and response.metadata:
            print(f"Response metadata: {response.metadata}")
        
        # Check if there are other response fields
        for attr in ['completion', 'response', 'text', 'content', 'answer']:
            if hasattr(response, attr):
                value = getattr(response, attr)
                if value:
                    print(f"Found {attr}: {value}")
        
        # Test document-level access
        print(f"\n3. Testing document-level access")
        documents = db.list_documents()
        
        if documents:
            doc = documents[0]
            print(f"Document: {doc.filename}")
            print(f"Document type: {type(doc)}")
            print(f"Document attributes: {[attr for attr in dir(doc) if not attr.startswith('_')]}")
            
            # Check if document has processed content
            for attr in ['content', 'text', 'metadata', 'processed_content', 'extracted_text']:
                if hasattr(doc, attr):
                    value = getattr(doc, attr)
                    if value:
                        print(f"Document {attr}: {type(value)} - {str(value)[:200]}...")
        
        # Test direct chunk access by ID
        print(f"\n4. Testing direct chunk access")
        if chunks:
            chunk = chunks[0]
            if hasattr(chunk, 'document_id') and hasattr(chunk, 'chunk_number'):
                doc_id = chunk.document_id
                chunk_num = chunk.chunk_number
                print(f"Trying to access chunk {chunk_num} from document {doc_id}")
                
                # Try to get chunk content directly
                try:
                    # This might not exist, but let's try
                    if hasattr(db, 'get_chunk'):
                        direct_chunk = db.get_chunk(doc_id, chunk_num)
                        print(f"Direct chunk access: {direct_chunk}")
                except Exception as e:
                    print(f"Direct chunk access failed: {e}")
        
        # Test if there are other methods we haven't tried
        print(f"\n5. Testing Morphik API methods")
        db_methods = [method for method in dir(db) if not method.startswith('_') and callable(getattr(db, method))]
        print(f"Available methods: {db_methods}")
        
        # Look for methods that might return processed content
        interesting_methods = [m for m in db_methods if any(keyword in m.lower() for keyword in ['content', 'text', 'extract', 'process', 'search', 'retrieve'])]
        print(f"Interesting methods: {interesting_methods}")
        
        # Test some of these methods
        for method_name in interesting_methods[:3]:  # Test first 3
            try:
                method = getattr(db, method_name)
                print(f"\nTesting {method_name}:")
                print(f"  Method signature: {method.__doc__}")
            except Exception as e:
                print(f"  Error accessing {method_name}: {e}")
        
        print(f"\n6. INVESTIGATION SUMMARY:")
        print(f"   - PIL Images detected: YES")
        print(f"   - Raw image data available: YES")
        print(f"   - Processed text from images: NEED TO FIND")
        print(f"   - Query responses: Empty/None")
        print(f"   - Need to find where ColPali processed content is stored")
        
    except Exception as e:
        print(f"ERROR: Investigation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_content_extraction() 