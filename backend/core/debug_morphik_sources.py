#!/usr/bin/env python3
"""
Debug script to understand the actual structure of sources returned by Morphik.
This will help us fix the visual content detection logic.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
from datetime import datetime
from morphik import Morphik

def debug_morphik_sources():
    """Debug the actual structure of sources returned by Morphik."""
    print("Debug: Morphik Source Structure Analysis")
    print("=" * 50)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found in environment variables")
        return
    
    try:
        # Initialize Morphik
        db = Morphik(morphik_uri)
        print("SUCCESS: Connected to Morphik")
        
        # Get documents
        documents = db.list_documents()
        print(f"INFO: Found {len(documents)} documents")
        
        if not documents:
            print("WARNING: No documents found. Please ingest some documents first.")
            return
        
        # Test with a simple query
        print("\nTesting with simple query...")
        response = db.query("ECSS", use_colpali=True, k=3)
        
        print(f"Response type: {type(response)}")
        print(f"Response attributes: {dir(response)}")
        
        if hasattr(response, 'sources') and response.sources:
            print(f"\nFound {len(response.sources)} sources")
            
            for i, source in enumerate(response.sources[:3]):  # Analyze first 3 sources
                print(f"\n--- SOURCE {i+1} ---")
                print(f"Source type: {type(source)}")
                print(f"Source attributes: {dir(source)}")
                
                # Check all possible attributes
                possible_attrs = [
                    'content', 'text', 'data', 'chunk', 'image', 'visual', 
                    'document_id', 'chunk_id', 'score', 'metadata', 'entity_type'
                ]
                
                for attr in possible_attrs:
                    if hasattr(source, attr):
                        value = getattr(source, attr)
                        print(f"  {attr}: {type(value)} - {str(value)[:100]}...")
                        
                        # Special handling for potential image content
                        if value and hasattr(value, '__class__'):
                            class_name = str(type(value))
                            if 'PIL' in class_name or 'Image' in class_name:
                                print(f"    >>> VISUAL CONTENT DETECTED! Type: {class_name}")
                                if hasattr(value, 'size'):
                                    print(f"    >>> Image size: {value.size}")
                                if hasattr(value, 'mode'):
                                    print(f"    >>> Image mode: {value.mode}")
                
                # Check if source has a dict-like structure
                if hasattr(source, '__dict__'):
                    print(f"  __dict__: {source.__dict__}")
                
                # Check if source is iterable
                try:
                    if hasattr(source, '__iter__') and not isinstance(source, str):
                        print(f"  Iterable source detected")
                except:
                    pass
        
        else:
            print("WARNING: No sources found in response")
            if hasattr(response, 'response'):
                print(f"Response text: {response.response}")
        
        # Test with visual-specific query
        print("\n" + "="*50)
        print("Testing with visual-specific query...")
        
        visual_response = db.query("diagrams tables figures", use_colpali=True, k=3)
        
        if hasattr(visual_response, 'sources') and visual_response.sources:
            print(f"Found {len(visual_response.sources)} visual sources")
            
            for i, source in enumerate(visual_response.sources[:2]):
                print(f"\n--- VISUAL SOURCE {i+1} ---")
                print(f"Type: {type(source)}")
                
                # Deep inspection of visual sources
                if hasattr(source, 'content'):
                    content = source.content
                    print(f"Content type: {type(content)}")
                    
                    if content:
                        # Check for PIL Image
                        if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                            print(">>> PIL IMAGE DETECTED!")
                            print(f"    Image type: {type(content)}")
                            print(f"    Image size: {getattr(content, 'size', 'unknown')}")
                            print(f"    Image mode: {getattr(content, 'mode', 'unknown')}")
                        
                        # Check for base64 image
                        elif isinstance(content, str) and len(content) > 1000:
                            if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                                print(">>> BASE64 IMAGE DETECTED!")
                                print(f"    Content length: {len(content)}")
                                print(f"    Content start: {content[:50]}...")
                        
                        # Check for other content types
                        else:
                            print(f"Content (first 200 chars): {str(content)[:200]}...")
                
                # Check other attributes
                for attr in ['text', 'data', 'chunk', 'metadata']:
                    if hasattr(source, attr):
                        value = getattr(source, attr)
                        if value:
                            print(f"{attr}: {type(value)} - {str(value)[:100]}...")
        
        # Test retrieve_chunks method
        print("\n" + "="*50)
        print("Testing retrieve_chunks method...")
        
        try:
            chunks = db.retrieve_chunks("ECSS")
            print(f"Found {len(chunks)} chunks")
            
            if chunks:
                for i, chunk in enumerate(chunks[:2]):
                    print(f"\n--- CHUNK {i+1} ---")
                    print(f"Chunk type: {type(chunk)}")
                    print(f"Chunk attributes: {dir(chunk)}")
                    
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        print(f"Chunk content type: {type(content)}")
                        
                        if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                            print(">>> PIL IMAGE IN CHUNK!")
                            print(f"    Image: {type(content)}")
                            print(f"    Size: {getattr(content, 'size', 'unknown')}")
                        elif isinstance(content, str) and len(content) > 100:
                            print(f"Text content: {content[:200]}...")
                    
                    # Check other chunk attributes
                    for attr in ['text', 'data', 'metadata', 'id', 'score']:
                        if hasattr(chunk, attr):
                            value = getattr(chunk, attr)
                            if value:
                                print(f"  {attr}: {type(value)} - {str(value)[:100]}...")
        
        except Exception as e:
            print(f"ERROR: retrieve_chunks failed: {e}")
        
        print("\n" + "="*50)
        print("DEBUG SUMMARY:")
        print("1. Check the source structure above")
        print("2. Look for PIL Image objects or base64 content")
        print("3. Note which attributes contain visual content")
        print("4. This will help fix the visual content detection logic")
        
    except Exception as e:
        print(f"ERROR: Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_morphik_sources() 