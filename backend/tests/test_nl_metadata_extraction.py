

#!/usr/bin/env python3
"""
Test metadata extraction using NaturalLanguageRule instead of MetadataExtractionRule
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test metadata extraction using NaturalLanguageRule instead of MetadataExtractionRule
"""

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_nl_metadata_extraction():
    """Test metadata extraction using NaturalLanguageRule."""
    print("🔍 Testing NaturalLanguageRule for Metadata Extraction")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create natural language rule for metadata extraction
    metadata_prompt = """
    Extract the following metadata from the document:
    - title: The document title
    - organization: The organization that published the document
    - date: The publication date
    - document_type: The type of document (standard, specification, etc.)
    - main_topics: List of main topics covered
    - summary: Brief summary of the document content
    
    Return the result as a JSON object with these fields.
    """
    
    rule = NaturalLanguageRule(prompt=metadata_prompt)
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    The standard applies to all space projects and provides a framework for engineering processes.
    """
    
    print("📝 Ingesting text with NaturalLanguageRule...")
    try:
        # Ingest with natural language rule
        doc = db.ingest_text(test_text, filename="nl_metadata_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing to complete...")
        start_time = time.time()
        max_wait = 120  # 2 minutes
        
        while time.time() - start_time < max_wait:
            # Check status
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            print(f"  Status: {status_value}")
            
            if status_value == 'completed':
                print("✅ Processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return
            
            time.sleep(5)  # Wait 5 seconds before checking again
        else:
            print("❌ Processing timed out")
            return
        
        # Check chunks for extracted metadata
        print(f"\n🔍 Checking chunks for extracted metadata...")
        chunks = db.retrieve_chunks("metadata extraction")
        
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                print(f"\n  Chunk {i+1}:")
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    if isinstance(content, str) and content.strip():
                        print(f"    Content: {content[:200]}...")
                    else:
                        print(f"    Content: {content}")
                else:
                    print(f"    No content attribute")
        else:
            print("❌ No chunks found")
            
        # Also check with specific terms
        print(f"\n🔍 Searching for extracted metadata...")
        search_terms = ["title", "organization", "date", "ECSS"]
        
        for term in search_terms:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"✅ Found {len(chunks)} chunks for '{term}'")
                for chunk in chunks[:2]:  # Show first 2 chunks
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        if isinstance(content, str) and len(content) > 50:
                            print(f"    {content[:100]}...")
                        else:
                            print(f"    {content}")
            else:
                print(f"❌ No chunks found for '{term}'")
            
    except Exception as e:
        print(f"❌ Error testing NL metadata extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_nl_metadata_extraction() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_nl_metadata_extraction():
    """Test metadata extraction using NaturalLanguageRule."""
    print("🔍 Testing NaturalLanguageRule for Metadata Extraction")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create natural language rule for metadata extraction
    metadata_prompt = """
    Extract the following metadata from the document:
    - title: The document title
    - organization: The organization that published the document
    - date: The publication date
    - document_type: The type of document (standard, specification, etc.)
    - main_topics: List of main topics covered
    - summary: Brief summary of the document content
    
    Return the result as a JSON object with these fields.
    """
    
    rule = NaturalLanguageRule(prompt=metadata_prompt)
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    The standard applies to all space projects and provides a framework for engineering processes.
    """
    
    print("📝 Ingesting text with NaturalLanguageRule...")
    try:
        # Ingest with natural language rule
        doc = db.ingest_text(test_text, filename="nl_metadata_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing to complete...")
        start_time = time.time()
        max_wait = 120  # 2 minutes
        
        while time.time() - start_time < max_wait:
            # Check status
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            print(f"  Status: {status_value}")
            
            if status_value == 'completed':
                print("✅ Processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return
            
            time.sleep(5)  # Wait 5 seconds before checking again
        else:
            print("❌ Processing timed out")
            return
        
        # Check chunks for extracted metadata
        print(f"\n🔍 Checking chunks for extracted metadata...")
        chunks = db.retrieve_chunks("metadata extraction")
        
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                print(f"\n  Chunk {i+1}:")
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    if isinstance(content, str) and content.strip():
                        print(f"    Content: {content[:200]}...")
                    else:
                        print(f"    Content: {content}")
                else:
                    print(f"    No content attribute")
        else:
            print("❌ No chunks found")
            
        # Also check with specific terms
        print(f"\n🔍 Searching for extracted metadata...")
        search_terms = ["title", "organization", "date", "ECSS"]
        
        for term in search_terms:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"✅ Found {len(chunks)} chunks for '{term}'")
                for chunk in chunks[:2]:  # Show first 2 chunks
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        if isinstance(content, str) and len(content) > 50:
                            print(f"    {content[:100]}...")
                        else:
                            print(f"    {content}")
            else:
                print(f"❌ No chunks found for '{term}'")
            
    except Exception as e:
        print(f"❌ Error testing NL metadata extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_nl_metadata_extraction() 