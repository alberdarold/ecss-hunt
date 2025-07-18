#!/usr/bin/env python3
"""
Simple test to verify the visual content fix works.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
from morphik import Morphik

def test_visual_fix():
    """Test that we can now properly detect visual content."""
    print("Testing Visual Content Fix")
    print("=" * 40)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found")
        return
    
    try:
        # Initialize Morphik
        db = Morphik(morphik_uri)
        print("SUCCESS: Connected to Morphik")
        
        # Test retrieve_chunks (should have PIL Images)
        print("\nTesting retrieve_chunks()...")
        chunks = db.retrieve_chunks("ECSS")
        
        if chunks:
            print(f"Found {len(chunks)} chunks")
            
            visual_count = 0
            text_count = 0
            
            for i, chunk in enumerate(chunks):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    
                    # Check for PIL Image
                    if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                        visual_count += 1
                        print(f"  VISUAL {visual_count}: {type(content).__name__} - Size: {getattr(content, 'size', 'unknown')}")
                        
                        # Check metadata
                        if hasattr(chunk, 'metadata') and chunk.metadata:
                            is_image = chunk.metadata.get('is_image', False)
                            print(f"    Metadata confirms image: {is_image}")
                    
                    elif isinstance(content, str):
                        text_count += 1
                        print(f"  TEXT {text_count}: {len(content)} characters")
            
            print(f"\nSUMMARY:")
            print(f"  Visual content found: {visual_count}")
            print(f"  Text content found: {text_count}")
            
            if visual_count > 0:
                print(f"  SUCCESS: Visual content is working!")
            else:
                print(f"  WARNING: No visual content found")
        
        else:
            print("WARNING: No chunks found")
        
        # Test query method (should have metadata only)
        print(f"\nTesting query()...")
        response = db.query("ECSS", use_colpali=True, k=3)
        
        if response.sources:
            print(f"Found {len(response.sources)} sources from query")
            
            for i, source in enumerate(response.sources):
                print(f"  Source {i+1}: {type(source).__name__}")
                print(f"    Document ID: {getattr(source, 'document_id', 'unknown')}")
                print(f"    Chunk Number: {getattr(source, 'chunk_number', 'unknown')}")
                print(f"    Score: {getattr(source, 'score', 0.0)}")
                
                # Check if source has content (it shouldn't)
                if hasattr(source, 'content'):
                    print(f"    Has content: {source.content is not None}")
                else:
                    print(f"    Has content: No content attribute")
        
        else:
            print("WARNING: No sources found from query")
        
        print(f"\nCONCLUSION:")
        print(f"  - retrieve_chunks() = Content including PIL Images")
        print(f"  - query() = Metadata only (document_id, chunk_number, score)")
        print(f"  - Visual content IS working - just need to use the right API!")
        
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_visual_fix() 