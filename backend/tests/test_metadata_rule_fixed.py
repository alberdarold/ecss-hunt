

#!/usr/bin/env python3
"""
Test MetadataExtractionRule with proper API usage
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test MetadataExtractionRule with proper API usage
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

def test_metadata_rule():
    """Test MetadataExtractionRule with proper API usage."""
    print("🔍 Testing MetadataExtractionRule")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple metadata schema
    class SimpleDoc(BaseModel):
        title: str = Field(description="Document title")
        content_type: str = Field(description="Type of content")
        summary: str = Field(description="Brief summary")
    
    # Create rule
    rule = MetadataExtractionRule(schema=SimpleDoc)
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    print("📝 Ingesting text with MetadataExtractionRule...")
    try:
        # Ingest with metadata rule
        doc = db.ingest_text(test_text, filename="metadata_rule_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion (without timeout parameter)
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
        
        # Check metadata
        print(f"\n🔍 Checking metadata...")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
        else:
            print("❌ No metadata found in document object")
            
        # Re-fetch and check
        print(f"\n🔄 Re-fetching document...")
        refetched = db.get_document(doc.external_id)
        if hasattr(refetched, 'metadata') and refetched.metadata:
            print(f"✅ Re-fetched metadata: {refetched.metadata}")
        else:
            print("❌ No metadata in re-fetched document")
            
        # Check all document attributes
        print(f"\n📋 All document attributes:")
        for attr in dir(refetched):
            if not attr.startswith('_') and not callable(getattr(refetched, attr)):
                try:
                    value = getattr(refetched, attr)
                    print(f"  {attr}: {value}")
                except Exception as e:
                    print(f"  {attr}: Error - {e}")
            
    except Exception as e:
        print(f"❌ Error testing metadata extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_metadata_rule() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule
from pydantic import BaseModel, Field

def test_metadata_rule():
    """Test MetadataExtractionRule with proper API usage."""
    print("🔍 Testing MetadataExtractionRule")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define simple metadata schema
    class SimpleDoc(BaseModel):
        title: str = Field(description="Document title")
        content_type: str = Field(description="Type of content")
        summary: str = Field(description="Brief summary")
    
    # Create rule
    rule = MetadataExtractionRule(schema=SimpleDoc)
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    print("📝 Ingesting text with MetadataExtractionRule...")
    try:
        # Ingest with metadata rule
        doc = db.ingest_text(test_text, filename="metadata_rule_test.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion (without timeout parameter)
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
        
        # Check metadata
        print(f"\n🔍 Checking metadata...")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"✅ Metadata extracted: {doc.metadata}")
        else:
            print("❌ No metadata found in document object")
            
        # Re-fetch and check
        print(f"\n🔄 Re-fetching document...")
        refetched = db.get_document(doc.external_id)
        if hasattr(refetched, 'metadata') and refetched.metadata:
            print(f"✅ Re-fetched metadata: {refetched.metadata}")
        else:
            print("❌ No metadata in re-fetched document")
            
        # Check all document attributes
        print(f"\n📋 All document attributes:")
        for attr in dir(refetched):
            if not attr.startswith('_') and not callable(getattr(refetched, attr)):
                try:
                    value = getattr(refetched, attr)
                    print(f"  {attr}: {value}")
                except Exception as e:
                    print(f"  {attr}: Error - {e}")
            
    except Exception as e:
        print(f"❌ Error testing metadata extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_metadata_rule() 