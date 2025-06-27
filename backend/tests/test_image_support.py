

#!/usr/bin/env python3
"""
Test MetadataExtractionRule with image support for PDF parsing.
This script tests the stage="post_chunking" and use_images=True parameters.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test MetadataExtractionRule with image support for PDF parsing.
This script tests the stage="post_chunking" and use_images=True parameters.
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

def test_image_support():
    """Test MetadataExtractionRule with image support."""
    print("🖼️ Testing MetadataExtractionRule with Image Support")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple schema for testing
    class SimpleDocument(BaseModel):
        title: str = Field(description="Document title")
        standard_id: str = Field(description="ECSS standard identifier")
        revision: str = Field(description="Revision number")
        date: str = Field(description="Publication date")
        summary: str = Field(description="Brief summary")
    
    # Create rule with image support
    rule = MetadataExtractionRule(
        schema=SimpleDocument,
        stage="post_chunking",
        use_images=True
    )
    
    print(f"✅ Created MetadataExtractionRule with:")
    print(f"   - Schema: {SimpleDocument.__name__}")
    print(f"   - Stage: post_chunking")
    print(f"   - Use images: True")
    
    # Find a small PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Use the smallest file for quick testing
    test_file = min(pdf_files, key=lambda f: f.stat().st_size)
    print(f"📄 Testing with: {test_file.name} ({test_file.stat().st_size / 1024:.1f} KB)")
    
    try:
        # Ingest with image support
        print("🔄 Ingesting PDF with image support...")
        doc = db.ingest_file(
            test_file,
            filename=f"test_image_support_{test_file.name}",
            rules=[rule],
            use_colpali=True  # Enable image processing
        )
        
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion(timeout=300)
        
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
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
        print(f"❌ Error testing image support: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_support() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

def test_image_support():
    """Test MetadataExtractionRule with image support."""
    print("🖼️ Testing MetadataExtractionRule with Image Support")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple schema for testing
    class SimpleDocument(BaseModel):
        title: str = Field(description="Document title")
        standard_id: str = Field(description="ECSS standard identifier")
        revision: str = Field(description="Revision number")
        date: str = Field(description="Publication date")
        summary: str = Field(description="Brief summary")
    
    # Create rule with image support
    rule = MetadataExtractionRule(
        schema=SimpleDocument,
        stage="post_chunking",
        use_images=True
    )
    
    print(f"✅ Created MetadataExtractionRule with:")
    print(f"   - Schema: {SimpleDocument.__name__}")
    print(f"   - Stage: post_chunking")
    print(f"   - Use images: True")
    
    # Find a small PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Use the smallest file for quick testing
    test_file = min(pdf_files, key=lambda f: f.stat().st_size)
    print(f"📄 Testing with: {test_file.name} ({test_file.stat().st_size / 1024:.1f} KB)")
    
    try:
        # Ingest with image support
        print("🔄 Ingesting PDF with image support...")
        doc = db.ingest_file(
            test_file,
            filename=f"test_image_support_{test_file.name}",
            rules=[rule],
            use_colpali=True  # Enable image processing
        )
        
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion(timeout=300)
        
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
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
        print(f"❌ Error testing image support: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_support() 