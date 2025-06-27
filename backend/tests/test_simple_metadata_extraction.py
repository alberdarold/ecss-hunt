

#!/usr/bin/env python3
"""
Simple test to verify if metadata extraction works at all.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Simple test to verify if metadata extraction works at all.
"""

import os
import sys

# Load environment variables from the root directory
dotenv_path = Path(__file__).parent.parent / '.env'

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

class SimpleDocumentInfo(BaseModel):
    """Simple schema for testing metadata extraction."""
    title: str = Field(description="The title of the document")
    document_type: str = Field(description="The type of document (e.g., 'standard', 'handbook')")
    branch: str = Field(description="The ECSS branch (E, M, P, Q)")

def test_simple_extraction():
    """Test metadata extraction with a simple schema."""
    print("🧪 Testing Simple Metadata Extraction")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create a simple rule
    simple_rule = MetadataExtractionRule(schema=SimpleDocumentInfo)
    print(f"✅ Created simple rule with schema: {SimpleDocumentInfo.__name__}")
    
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
        # Clean up any existing test document
        print("🧹 Cleaning up any existing test document...")
        try:
            existing_docs = db.list_documents()
            for doc in existing_docs:
                if doc.filename == f"test_{test_file.name}":
                    print(f"   Deleting existing test document: {doc.external_id}")
                    # Note: We don't have a delete method in the SDK, but we can check if it exists
        except Exception as e:
            print(f"   Warning: Could not check existing documents: {e}")
        
        # Ingest with simple rule
        print(f"\n🚀 Ingesting with simple metadata extraction rule...")
        doc = db.ingest_file(
            test_file, 
            rules=[simple_rule]
        )
        print(f"✅ File ingested, document ID: {doc.external_id}")
        print(f"📊 Initial status: {doc.status}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing to complete...")
        doc.wait_for_completion()
        print(f"✅ Processing complete, final status: {doc.status}")
        
        # Get the full document
        print(f"\n🔄 Fetching full document...")
        full_doc = db.get_document(doc.external_id)
        
        if full_doc:
            print(f"✅ Document fetched successfully")
            print(f"📋 Document metadata:")
            print(f"   - Filename: {full_doc.filename}")
            print(f"   - Status: {full_doc.status}")
            print(f"   - Is ingested: {full_doc.is_ingested}")
            print(f"   - Is processing: {full_doc.is_processing}")
            print(f"   - Is failed: {full_doc.is_failed}")
            
            # Check metadata
            print(f"\n🔍 Checking extracted metadata...")
            if hasattr(full_doc, 'metadata') and full_doc.metadata:
                print(f"✅ Metadata found: {full_doc.metadata}")
                
                # Check if it's just schema or actual extracted data
                if 'title' in full_doc.metadata and isinstance(full_doc.metadata['title'], str):
                    print(f"✅ SUCCESS: Found extracted title: {full_doc.metadata['title']}")
                elif 'type' in full_doc.metadata and full_doc.metadata['type'] == 'object':
                    print(f"❌ FAILURE: Metadata only contains schema definition, not extracted values")
                else:
                    print(f"⚠️  UNKNOWN: Metadata format unclear: {full_doc.metadata}")
            else:
                print(f"❌ No metadata found")
            
            # Check system_metadata
            print(f"\n🔍 Checking system metadata...")
            if hasattr(full_doc, 'system_metadata') and full_doc.system_metadata:
                print(f"System metadata: {full_doc.system_metadata}")
            else:
                print(f"No system metadata")
                
        else:
            print(f"❌ Failed to fetch document")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_extraction() 

import os
import sys

# Load environment variables from the root directory
dotenv_path = Path(__file__).parent.parent / '.env'

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

class SimpleDocumentInfo(BaseModel):
    """Simple schema for testing metadata extraction."""
    title: str = Field(description="The title of the document")
    document_type: str = Field(description="The type of document (e.g., 'standard', 'handbook')")
    branch: str = Field(description="The ECSS branch (E, M, P, Q)")

def test_simple_extraction():
    """Test metadata extraction with a simple schema."""
    print("🧪 Testing Simple Metadata Extraction")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create a simple rule
    simple_rule = MetadataExtractionRule(schema=SimpleDocumentInfo)
    print(f"✅ Created simple rule with schema: {SimpleDocumentInfo.__name__}")
    
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
        # Clean up any existing test document
        print("🧹 Cleaning up any existing test document...")
        try:
            existing_docs = db.list_documents()
            for doc in existing_docs:
                if doc.filename == f"test_{test_file.name}":
                    print(f"   Deleting existing test document: {doc.external_id}")
                    # Note: We don't have a delete method in the SDK, but we can check if it exists
        except Exception as e:
            print(f"   Warning: Could not check existing documents: {e}")
        
        # Ingest with simple rule
        print(f"\n🚀 Ingesting with simple metadata extraction rule...")
        doc = db.ingest_file(
            test_file, 
            rules=[simple_rule]
        )
        print(f"✅ File ingested, document ID: {doc.external_id}")
        print(f"📊 Initial status: {doc.status}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing to complete...")
        doc.wait_for_completion()
        print(f"✅ Processing complete, final status: {doc.status}")
        
        # Get the full document
        print(f"\n🔄 Fetching full document...")
        full_doc = db.get_document(doc.external_id)
        
        if full_doc:
            print(f"✅ Document fetched successfully")
            print(f"📋 Document metadata:")
            print(f"   - Filename: {full_doc.filename}")
            print(f"   - Status: {full_doc.status}")
            print(f"   - Is ingested: {full_doc.is_ingested}")
            print(f"   - Is processing: {full_doc.is_processing}")
            print(f"   - Is failed: {full_doc.is_failed}")
            
            # Check metadata
            print(f"\n🔍 Checking extracted metadata...")
            if hasattr(full_doc, 'metadata') and full_doc.metadata:
                print(f"✅ Metadata found: {full_doc.metadata}")
                
                # Check if it's just schema or actual extracted data
                if 'title' in full_doc.metadata and isinstance(full_doc.metadata['title'], str):
                    print(f"✅ SUCCESS: Found extracted title: {full_doc.metadata['title']}")
                elif 'type' in full_doc.metadata and full_doc.metadata['type'] == 'object':
                    print(f"❌ FAILURE: Metadata only contains schema definition, not extracted values")
                else:
                    print(f"⚠️  UNKNOWN: Metadata format unclear: {full_doc.metadata}")
            else:
                print(f"❌ No metadata found")
            
            # Check system_metadata
            print(f"\n🔍 Checking system metadata...")
            if hasattr(full_doc, 'system_metadata') and full_doc.system_metadata:
                print(f"System metadata: {full_doc.system_metadata}")
            else:
                print(f"No system metadata")
                
        else:
            print(f"❌ Failed to fetch document")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_extraction() 