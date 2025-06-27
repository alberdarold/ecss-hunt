

#!/usr/bin/env python3
"""
Test script to verify the configuration fixes and test text extraction.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script to verify the configuration fixes and test text extraction.
"""

import os
import sys

# Load environment variables

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_configuration_fixes():
    """Test the configuration fixes and text extraction."""
    print("🧪 Testing Configuration Fixes")
    print("=" * 40)
    
    # Test 1: Check if Morphik can connect with new config
    print("\n1. Testing Morphik connection with new configuration...")
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI not set")
            return False
        
        db = Morphik(morphik_uri)
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"✅ Found {len(documents)} existing documents")
        
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return False
    
    # Test 2: Check if we have documents to work with
    if not documents:
        print("⚠️  No documents found. Please run ingestion first.")
        return True
    
    # Test 3: Test text extraction with new configuration
    print("\n2. Testing text extraction with new configuration...")
    try:
        # Test with a simple search term
        test_term = "the"
        print(f"Searching for '{test_term}'...")
        
        chunks = db.retrieve_chunks(test_term)
        print(f"Found {len(chunks)} chunks")
        
        text_chunks = 0
        image_chunks = 0
        json_chunks = 0
        
        for i, chunk in enumerate(chunks[:3]):  # Check first 3 chunks
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                if isinstance(content, str):
                    if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                        image_chunks += 1
                        print(f"  Chunk {i+1}: IMAGE (base64)")
                    elif content.startswith('{') and content.endswith('}'):
                        json_chunks += 1
                        print(f"  Chunk {i+1}: JSON (NaturalLanguageRule output)")
                        print(f"    Preview: {content[:200]}...")
                    else:
                        text_chunks += 1
                        print(f"  Chunk {i+1}: TEXT")
                        print(f"    Preview: {content[:200]}...")
        
        print(f"\n📊 Chunk Analysis:")
        print(f"  Text chunks: {text_chunks}")
        print(f"  Image chunks: {image_chunks}")
        print(f"  JSON chunks: {json_chunks}")
        
        if text_chunks > 0:
            print("✅ Found text content! Configuration may be working.")
        elif json_chunks > 0:
            print("✅ Found NaturalLanguageRule output! Rules are working.")
        else:
            print("❌ Still only finding images. Configuration may need more adjustment.")
        
    except Exception as e:
        print(f"❌ Text extraction test failed: {e}")
        return False
    
    # Test 4: Test knowledge graph creation
    print("\n3. Testing knowledge graph creation...")
    try:
        graph = db.create_graph("Test Configuration Graph")
        if graph:
            print(f"✅ Successfully created test graph: {graph.id}")
        else:
            print("❌ Graph creation returned None")
    except Exception as e:
        print(f"❌ Graph creation failed: {e}")
    
    return True

if __name__ == "__main__":
    success = test_configuration_fixes()
    if success:
        print("\n✅ Configuration test completed successfully!")
        print("You can now try running the ingestion script again.")
    else:
        print("\n❌ Configuration test failed. Please check the issues above.") 

import os
import sys

# Load environment variables

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_configuration_fixes():
    """Test the configuration fixes and text extraction."""
    print("🧪 Testing Configuration Fixes")
    print("=" * 40)
    
    # Test 1: Check if Morphik can connect with new config
    print("\n1. Testing Morphik connection with new configuration...")
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI not set")
            return False
        
        db = Morphik(morphik_uri)
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"✅ Found {len(documents)} existing documents")
        
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return False
    
    # Test 2: Check if we have documents to work with
    if not documents:
        print("⚠️  No documents found. Please run ingestion first.")
        return True
    
    # Test 3: Test text extraction with new configuration
    print("\n2. Testing text extraction with new configuration...")
    try:
        # Test with a simple search term
        test_term = "the"
        print(f"Searching for '{test_term}'...")
        
        chunks = db.retrieve_chunks(test_term)
        print(f"Found {len(chunks)} chunks")
        
        text_chunks = 0
        image_chunks = 0
        json_chunks = 0
        
        for i, chunk in enumerate(chunks[:3]):  # Check first 3 chunks
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                if isinstance(content, str):
                    if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                        image_chunks += 1
                        print(f"  Chunk {i+1}: IMAGE (base64)")
                    elif content.startswith('{') and content.endswith('}'):
                        json_chunks += 1
                        print(f"  Chunk {i+1}: JSON (NaturalLanguageRule output)")
                        print(f"    Preview: {content[:200]}...")
                    else:
                        text_chunks += 1
                        print(f"  Chunk {i+1}: TEXT")
                        print(f"    Preview: {content[:200]}...")
        
        print(f"\n📊 Chunk Analysis:")
        print(f"  Text chunks: {text_chunks}")
        print(f"  Image chunks: {image_chunks}")
        print(f"  JSON chunks: {json_chunks}")
        
        if text_chunks > 0:
            print("✅ Found text content! Configuration may be working.")
        elif json_chunks > 0:
            print("✅ Found NaturalLanguageRule output! Rules are working.")
        else:
            print("❌ Still only finding images. Configuration may need more adjustment.")
        
    except Exception as e:
        print(f"❌ Text extraction test failed: {e}")
        return False
    
    # Test 4: Test knowledge graph creation
    print("\n3. Testing knowledge graph creation...")
    try:
        graph = db.create_graph("Test Configuration Graph")
        if graph:
            print(f"✅ Successfully created test graph: {graph.id}")
        else:
            print("❌ Graph creation returned None")
    except Exception as e:
        print(f"❌ Graph creation failed: {e}")
    
    return True

if __name__ == "__main__":
    success = test_configuration_fixes()
    if success:
        print("\n✅ Configuration test completed successfully!")
        print("You can now try running the ingestion script again.")
    else:
        print("\n❌ Configuration test failed. Please check the issues above.") 