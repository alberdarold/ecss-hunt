

#!/usr/bin/env python3
"""
Debug script to investigate metadata extraction issues.
This script will help us understand why structured metadata isn't being extracted properly.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to investigate metadata extraction issues.
This script will help us understand why structured metadata isn't being extracted properly.
"""

import os
import sys
import json
import time

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

def debug_metadata_extraction():
    """Debug metadata extraction to understand what's happening."""
    print("🔍 Debugging Metadata Extraction Issues")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define a simple test schema
    class TestMetadata(BaseModel):
        standard_id: str = Field(description="ECSS standard identifier")
        title: str = Field(description="Document title")
        date: str = Field(description="Publication date")
        summary: str = Field(description="Brief summary")
    
    print("📋 Test Schema:")
    print(f"   - Schema name: {TestMetadata.__name__}")
    print(f"   - Fields: {list(TestMetadata.model_fields.keys())}")
    
    # Test 1: Simple text ingestion with MetadataExtractionRule
    print("\n🧪 Test 1: Text ingestion with MetadataExtractionRule")
    print("-" * 40)
    
    test_text = """
    ECSS-E-AS-11C (1 October 2014)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    # Create rule
    rule = MetadataExtractionRule(schema=TestMetadata)
    print(f"✅ Created MetadataExtractionRule with schema")
    
    try:
        # Ingest text
        doc = db.ingest_text(
            test_text,
            filename="debug_test_metadata.txt",
            rules=[rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        print("\n📊 Checking extracted metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
            
            # Analyze metadata structure
            if isinstance(doc.metadata, dict):
                print(f"📋 Metadata analysis:")
                print(f"   - Type: {type(doc.metadata)}")
                print(f"   - Keys: {list(doc.metadata.keys())}")
                
                # Check if it's schema definition or actual data
                if 'type' in doc.metadata and 'properties' in doc.metadata:
                    print(f"   ❌ This is a schema definition, not extracted data!")
                elif 'standard_id' in doc.metadata:
                    print(f"   ✅ This looks like extracted data!")
                    print(f"   - standard_id: {doc.metadata.get('standard_id')}")
                    print(f"   - title: {doc.metadata.get('title', 'N/A')}")
                else:
                    print(f"   ❓ Unknown format")
        else:
            print("❌ No metadata found in document")
        
        # Check chunks
        print("\n🔍 Checking chunks:")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:3]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    print(f"\n   Chunk {i+1}:")
                    print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                    print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
        else:
            print("❌ No chunks found")
        
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Check if MetadataExtractionRule is working with images
    print("\n🧪 Test 2: MetadataExtractionRule with image support")
    print("-" * 40)
    
    # Find a small PDF
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if pdf_files:
        test_file = min(pdf_files, key=lambda f: f.stat().st_size)
        print(f"📄 Testing with: {test_file.name} ({test_file.stat().st_size / 1024:.1f} KB)")
        
        # Create rule with image support
        image_rule = MetadataExtractionRule(
            schema=TestMetadata,
            stage="post_chunking",
            use_images=True
        )
        print(f"✅ Created MetadataExtractionRule with image support")
        
        try:
            # Ingest PDF
            doc = db.ingest_file(
                test_file,
                filename=f"debug_image_test_{test_file.name}",
                rules=[image_rule],
                use_colpali=True
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            doc.wait_for_completion()
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            print("\n📊 Checking extracted metadata:")
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
            else:
                print("❌ No metadata found in document")
            
            # Check chunks
            print("\n🔍 Checking chunks:")
            chunks = db.retrieve_chunks("ECSS")
            if chunks:
                print(f"✅ Found {len(chunks)} chunks")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        print(f"\n   Chunk {i+1}:")
                        print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                        print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
            else:
                print("❌ No chunks found")
            
            # Clean up
            try:
                db.delete_document(doc.external_id)
                print("✅ Cleaned up test document")
            except Exception as e:
                print(f"⚠️ Warning: Could not clean up test document: {e}")
                
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No PDF files found for testing")
    
    # Test 3: Compare with NaturalLanguageRule
    print("\n🧪 Test 3: NaturalLanguageRule comparison")
    print("-" * 40)
    
    nl_rule = NaturalLanguageRule(
        prompt="""Extract the following information from the document and return as JSON:
{
    "standard_id": "ECSS standard identifier",
    "title": "Document title", 
    "date": "Publication date",
    "summary": "Brief summary"
}"""
    )
    
    try:
        # Ingest text with NaturalLanguageRule
        doc = db.ingest_text(
            test_text,
            filename="debug_nl_test.txt",
            rules=[nl_rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        print("\n📊 Checking extracted metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("❌ No metadata found in document")
        
        # Check chunks
        print("\n🔍 Checking chunks:")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:2]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    print(f"\n   Chunk {i+1}:")
                    print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                    print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
        else:
            print("❌ No chunks found")
        
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔍 Debug Summary:")
    print("=" * 30)
    print("This debug script will help us understand:")
    print("1. Whether MetadataExtractionRule is working at all")
    print("2. Whether the issue is with text vs image processing")
    print("3. Whether NaturalLanguageRule works better")
    print("4. What the actual metadata structure looks like")
    print("5. Whether chunks contain the right content")

if __name__ == "__main__":
    debug_metadata_extraction() 

import os
import sys
import json
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

def debug_metadata_extraction():
    """Debug metadata extraction to understand what's happening."""
    print("🔍 Debugging Metadata Extraction Issues")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define a simple test schema
    class TestMetadata(BaseModel):
        standard_id: str = Field(description="ECSS standard identifier")
        title: str = Field(description="Document title")
        date: str = Field(description="Publication date")
        summary: str = Field(description="Brief summary")
    
    print("📋 Test Schema:")
    print(f"   - Schema name: {TestMetadata.__name__}")
    print(f"   - Fields: {list(TestMetadata.model_fields.keys())}")
    
    # Test 1: Simple text ingestion with MetadataExtractionRule
    print("\n🧪 Test 1: Text ingestion with MetadataExtractionRule")
    print("-" * 40)
    
    test_text = """
    ECSS-E-AS-11C (1 October 2014)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    # Create rule
    rule = MetadataExtractionRule(schema=TestMetadata)
    print(f"✅ Created MetadataExtractionRule with schema")
    
    try:
        # Ingest text
        doc = db.ingest_text(
            test_text,
            filename="debug_test_metadata.txt",
            rules=[rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        print("\n📊 Checking extracted metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
            
            # Analyze metadata structure
            if isinstance(doc.metadata, dict):
                print(f"📋 Metadata analysis:")
                print(f"   - Type: {type(doc.metadata)}")
                print(f"   - Keys: {list(doc.metadata.keys())}")
                
                # Check if it's schema definition or actual data
                if 'type' in doc.metadata and 'properties' in doc.metadata:
                    print(f"   ❌ This is a schema definition, not extracted data!")
                elif 'standard_id' in doc.metadata:
                    print(f"   ✅ This looks like extracted data!")
                    print(f"   - standard_id: {doc.metadata.get('standard_id')}")
                    print(f"   - title: {doc.metadata.get('title', 'N/A')}")
                else:
                    print(f"   ❓ Unknown format")
        else:
            print("❌ No metadata found in document")
        
        # Check chunks
        print("\n🔍 Checking chunks:")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:3]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    print(f"\n   Chunk {i+1}:")
                    print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                    print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
        else:
            print("❌ No chunks found")
        
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Check if MetadataExtractionRule is working with images
    print("\n🧪 Test 2: MetadataExtractionRule with image support")
    print("-" * 40)
    
    # Find a small PDF
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if pdf_files:
        test_file = min(pdf_files, key=lambda f: f.stat().st_size)
        print(f"📄 Testing with: {test_file.name} ({test_file.stat().st_size / 1024:.1f} KB)")
        
        # Create rule with image support
        image_rule = MetadataExtractionRule(
            schema=TestMetadata,
            stage="post_chunking",
            use_images=True
        )
        print(f"✅ Created MetadataExtractionRule with image support")
        
        try:
            # Ingest PDF
            doc = db.ingest_file(
                test_file,
                filename=f"debug_image_test_{test_file.name}",
                rules=[image_rule],
                use_colpali=True
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            doc.wait_for_completion()
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            print("\n📊 Checking extracted metadata:")
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
            else:
                print("❌ No metadata found in document")
            
            # Check chunks
            print("\n🔍 Checking chunks:")
            chunks = db.retrieve_chunks("ECSS")
            if chunks:
                print(f"✅ Found {len(chunks)} chunks")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        print(f"\n   Chunk {i+1}:")
                        print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                        print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
            else:
                print("❌ No chunks found")
            
            # Clean up
            try:
                db.delete_document(doc.external_id)
                print("✅ Cleaned up test document")
            except Exception as e:
                print(f"⚠️ Warning: Could not clean up test document: {e}")
                
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No PDF files found for testing")
    
    # Test 3: Compare with NaturalLanguageRule
    print("\n🧪 Test 3: NaturalLanguageRule comparison")
    print("-" * 40)
    
    nl_rule = NaturalLanguageRule(
        prompt="""Extract the following information from the document and return as JSON:
{
    "standard_id": "ECSS standard identifier",
    "title": "Document title", 
    "date": "Publication date",
    "summary": "Brief summary"
}"""
    )
    
    try:
        # Ingest text with NaturalLanguageRule
        doc = db.ingest_text(
            test_text,
            filename="debug_nl_test.txt",
            rules=[nl_rule]
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        doc.wait_for_completion()
        print(f"✅ Processing completed: {doc.status}")
        
        # Check metadata
        print("\n📊 Checking extracted metadata:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("❌ No metadata found in document")
        
        # Check chunks
        print("\n🔍 Checking chunks:")
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:2]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    print(f"\n   Chunk {i+1}:")
                    print(f"   - Length: {len(content) if isinstance(content, str) else 'N/A'}")
                    print(f"   - Preview: {content[:200] if isinstance(content, str) else content}")
        else:
            print("❌ No chunks found")
        
        # Clean up
        try:
            db.delete_document(doc.external_id)
            print("✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up test document: {e}")
            
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔍 Debug Summary:")
    print("=" * 30)
    print("This debug script will help us understand:")
    print("1. Whether MetadataExtractionRule is working at all")
    print("2. Whether the issue is with text vs image processing")
    print("3. Whether NaturalLanguageRule works better")
    print("4. What the actual metadata structure looks like")
    print("5. Whether chunks contain the right content")

if __name__ == "__main__":
    debug_metadata_extraction() 