

#!/usr/bin/env python3
"""
Test PDF content retrieval using the working retrieve_chunks method
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test PDF content retrieval using the working retrieve_chunks method
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_pdf_content():
    """Test if PDF content is accessible."""
    print("🔍 Testing PDF Content Retrieval")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test different search terms
    search_terms = ["ECSS", "standard", "requirement", "engineering", "space"]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: '{term}'")
        try:
            chunks = db.retrieve_chunks(term)
            print(f"✅ Found {len(chunks)} chunks")
            
            # Show first 3 chunks
            for i, chunk in enumerate(chunks[:3]):
                content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                print(f"  Chunk {i+1}: {content[:200]}...")
                
                # Check if this looks like PDF content
                if "ECSS" in content or "standard" in content.lower():
                    print(f"    ✅ This looks like ECSS content!")
                
        except Exception as e:
            print(f"❌ Error searching for '{term}': {e}")
    
    # Test metadata extraction on a simple document
    print(f"\n🔍 Testing metadata extraction on simple document...")
    try:
        # Create a simple document with metadata rule
        from morphik.rules import MetadataExtractionRule
        from pydantic import BaseModel, Field
        
        class SimpleDoc(BaseModel):
            title: str = Field(description="Document title")
            content_type: str = Field(description="Type of content")
            summary: str = Field(description="Brief summary")
        
        rule = MetadataExtractionRule(schema=SimpleDoc)
        
        test_text = """
        ECSS-E-ST-10C Rev.1 (15 February 2017)
        European Cooperation for Space Standardization
        Space Engineering - System Engineering General Requirements
        
        This document defines the general requirements for system engineering in space projects.
        """
        
        doc = db.ingest_text(test_text, filename="metadata_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        doc.wait_for_completion(timeout=120)
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
        else:
            print("❌ No metadata found")
            
        # Re-fetch and check
        refetched = db.get_document(doc.external_id)
        if hasattr(refetched, 'metadata') and refetched.metadata:
            print(f"✅ Re-fetched metadata: {refetched.metadata}")
        else:
            print("❌ No metadata in re-fetched document")
            
    except Exception as e:
        print(f"❌ Error testing metadata extraction: {e}")

if __name__ == "__main__":
    test_pdf_content() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_pdf_content():
    """Test if PDF content is accessible."""
    print("🔍 Testing PDF Content Retrieval")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test different search terms
    search_terms = ["ECSS", "standard", "requirement", "engineering", "space"]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: '{term}'")
        try:
            chunks = db.retrieve_chunks(term)
            print(f"✅ Found {len(chunks)} chunks")
            
            # Show first 3 chunks
            for i, chunk in enumerate(chunks[:3]):
                content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                print(f"  Chunk {i+1}: {content[:200]}...")
                
                # Check if this looks like PDF content
                if "ECSS" in content or "standard" in content.lower():
                    print(f"    ✅ This looks like ECSS content!")
                
        except Exception as e:
            print(f"❌ Error searching for '{term}': {e}")
    
    # Test metadata extraction on a simple document
    print(f"\n🔍 Testing metadata extraction on simple document...")
    try:
        # Create a simple document with metadata rule
        from morphik.rules import MetadataExtractionRule
        from pydantic import BaseModel, Field
        
        class SimpleDoc(BaseModel):
            title: str = Field(description="Document title")
            content_type: str = Field(description="Type of content")
            summary: str = Field(description="Brief summary")
        
        rule = MetadataExtractionRule(schema=SimpleDoc)
        
        test_text = """
        ECSS-E-ST-10C Rev.1 (15 February 2017)
        European Cooperation for Space Standardization
        Space Engineering - System Engineering General Requirements
        
        This document defines the general requirements for system engineering in space projects.
        """
        
        doc = db.ingest_text(test_text, filename="metadata_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        doc.wait_for_completion(timeout=120)
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
        else:
            print("❌ No metadata found")
            
        # Re-fetch and check
        refetched = db.get_document(doc.external_id)
        if hasattr(refetched, 'metadata') and refetched.metadata:
            print(f"✅ Re-fetched metadata: {refetched.metadata}")
        else:
            print("❌ No metadata in re-fetched document")
            
    except Exception as e:
        print(f"❌ Error testing metadata extraction: {e}")

if __name__ == "__main__":
    test_pdf_content() 