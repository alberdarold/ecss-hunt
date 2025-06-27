

#!/usr/bin/env python3
"""
Test SimpleDoc(BaseModel) with morphik version 0.2.3 to verify the SDK bug fix.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test SimpleDoc(BaseModel) with morphik version 0.2.3 to verify the SDK bug fix.
"""

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

def test_simple_doc_fixed():
    """Test SimpleDoc(BaseModel) with the fixed morphik version."""
    print("🔧 Testing SimpleDoc(BaseModel) with morphik 0.2.3")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple schema for testing
    class SimpleDoc(BaseModel):
        title: str = Field(description="Document title")
        content_type: str = Field(description="Type of content")
        summary: str = Field(description="Brief summary")
    
    # Create rule
    rule = MetadataExtractionRule(schema=SimpleDoc)
    
    print(f"✅ Created MetadataExtractionRule with schema: {SimpleDoc.__name__}")
    print(f"   Schema fields: {list(SimpleDoc.model_fields.keys())}")
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    print("📝 Ingesting text with SimpleDoc schema...")
    
    try:
        # Ingest with rule
        doc = db.ingest_text(
            test_text, 
            filename="test_simple_doc_fixed.txt",
            rules=[rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
            
            # Analyze the metadata structure
            if isinstance(doc.metadata, dict):
                print(f"📊 Metadata analysis:")
                print(f"   Type: {type(doc.metadata)}")
                print(f"   Keys: {list(doc.metadata.keys())}")
                
                # Check if it's schema definition or extracted data
                if 'type' in doc.metadata and 'title' in doc.metadata and 'properties' in doc.metadata:
                    print(f"   ⚠️  This looks like a schema definition!")
                elif 'title' in doc.metadata and isinstance(doc.metadata['title'], str) and len(doc.metadata['title']) > 10:
                    print(f"   ✅ This looks like extracted data!")
                else:
                    print(f"   ❓ Unknown format")
        else:
            print("❌ No metadata found")
            
        # Check chunks for content
        print("🔍 Checking chunks...")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:2]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    if isinstance(content, str) and len(content) > 50:
                        print(f"   Chunk {i+1}: {content[:100]}...")
                    else:
                        print(f"   Chunk {i+1}: {content}")
        else:
            print("❌ No chunks found")
            
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error testing SimpleDoc: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_doc_fixed() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

def test_simple_doc_fixed():
    """Test SimpleDoc(BaseModel) with the fixed morphik version."""
    print("🔧 Testing SimpleDoc(BaseModel) with morphik 0.2.3")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple schema for testing
    class SimpleDoc(BaseModel):
        title: str = Field(description="Document title")
        content_type: str = Field(description="Type of content")
        summary: str = Field(description="Brief summary")
    
    # Create rule
    rule = MetadataExtractionRule(schema=SimpleDoc)
    
    print(f"✅ Created MetadataExtractionRule with schema: {SimpleDoc.__name__}")
    print(f"   Schema fields: {list(SimpleDoc.model_fields.keys())}")
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    print("📝 Ingesting text with SimpleDoc schema...")
    
    try:
        # Ingest with rule
        doc = db.ingest_text(
            test_text, 
            filename="test_simple_doc_fixed.txt",
            rules=[rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
            
            # Analyze the metadata structure
            if isinstance(doc.metadata, dict):
                print(f"📊 Metadata analysis:")
                print(f"   Type: {type(doc.metadata)}")
                print(f"   Keys: {list(doc.metadata.keys())}")
                
                # Check if it's schema definition or extracted data
                if 'type' in doc.metadata and 'title' in doc.metadata and 'properties' in doc.metadata:
                    print(f"   ⚠️  This looks like a schema definition!")
                elif 'title' in doc.metadata and isinstance(doc.metadata['title'], str) and len(doc.metadata['title']) > 10:
                    print(f"   ✅ This looks like extracted data!")
                else:
                    print(f"   ❓ Unknown format")
        else:
            print("❌ No metadata found")
            
        # Check chunks for content
        print("🔍 Checking chunks...")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:2]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    if isinstance(content, str) and len(content) > 50:
                        print(f"   Chunk {i+1}: {content[:100]}...")
                    else:
                        print(f"   Chunk {i+1}: {content}")
        else:
            print("❌ No chunks found")
            
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error testing SimpleDoc: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_doc_fixed() 