
# Add backend root to path


#!/usr/bin/env python3
"""
Debug script to understand ingestion issues.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to understand ingestion issues.
"""
import os
import sys
from datetime import datetime

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    print("python-dotenv not installed")
    sys.exit(1)

from morphik import Morphik
from core.schemas import BaseModel, Field, MetadataExtractionRule

class SimpleTest(BaseModel):
    title: str = Field(description="Document title")
    document_type: str = Field(description="Type of document")

def debug_ingestion():
    """Debug the ingestion process step by step."""
    print("=== INGESTION DEBUG ===")
    
    # 1. Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"1. Environment Check:")
    print(f"   MORPHIK_URI: {'SET' if morphik_uri else 'NOT SET'}")
    print(f"   OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
    
    if not morphik_uri:
        print("   ERROR: MORPHIK_URI not set")
        return
    
    # 2. Connect to Morphik
    print(f"\n2. Morphik Connection:")
    try:
        db = Morphik(morphik_uri)
        docs = db.list_documents()
        print(f"   SUCCESS: Connected, found {len(docs)} documents")
    except Exception as e:
        print(f"   ERROR: Connection failed: {e}")
        return
    
    # 3. Find a test file
    print(f"\n3. Test File:")
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"   ERROR: PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"   ERROR: No PDF files found")
        return
    
    test_file = pdf_files[0]
    print(f"   Using: {test_file.name}")
    
    # 4. Create a simple rule
    print(f"\n4. Rule Creation:")
    try:
        rule = MetadataExtractionRule(schema=SimpleTest)
        print(f"   SUCCESS: Created rule with schema: {SimpleTest.__name__}")
    except Exception as e:
        print(f"   ERROR: Rule creation failed: {e}")
        return
    
    # 5. Ingest with detailed logging
    print(f"\n5. Ingestion Process:")
    try:
        print(f"   Starting ingestion...")
        doc = db.ingest_file(test_file, filename=test_file.name, rules=[rule])
        print(f"   SUCCESS: File ingested")
        print(f"   Document ID: {doc.external_id}")
        print(f"   Initial status: {doc.status}")
        print(f"   Status type: {type(doc.status)}")
        
        # 6. Wait for completion with detailed status tracking
        print(f"\n6. Status Tracking:")
        
        # First, try wait_for_completion
        print(f"   Calling wait_for_completion()...")
        try:
            doc.wait_for_completion()
            print(f"   SUCCESS: wait_for_completion() returned")
            print(f"   Final status: {doc.status}")
        except Exception as e:
            print(f"   ERROR: wait_for_completion() failed: {e}")
        
        # Then check status manually
        max_checks = 10
        for i in range(max_checks):
            print(f"   Check {i+1}/{max_checks}: Status = {doc.status}")
            
            # Check if completed
            if isinstance(doc.status, dict):
                status_value = doc.status.get('status', 'unknown')
            else:
                status_value = doc.status
                
            if status_value == 'completed':
                print(f"   SUCCESS: Document completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"   ERROR: Document failed with status: {status_value}")
                break
            else:
                print(f"   Waiting... (status: {status_value})")
                import time
                time.sleep(3)
        else:
            print(f"   TIMEOUT: Document did not complete within {max_checks * 3} seconds")
        
        # 7. Fetch and examine the document
        print(f"\n7. Document Examination:")
        try:
            full_doc = db.get_document(doc.external_id)
            print(f"   SUCCESS: Document fetched")
            print(f"   Document object type: {type(full_doc)}")
            print(f"   Available attributes: {[attr for attr in dir(full_doc) if not attr.startswith('_')]}")
            
            # Check metadata
            if hasattr(full_doc, 'metadata'):
                print(f"   Metadata: {full_doc.metadata}")
                print(f"   Metadata type: {type(full_doc.metadata)}")
            else:
                print(f"   No metadata attribute found")
                
            # Check system_metadata
            if hasattr(full_doc, 'system_metadata'):
                print(f"   System metadata: {full_doc.system_metadata}")
            else:
                print(f"   No system_metadata attribute found")
                
        except Exception as e:
            print(f"   ERROR: Failed to fetch document: {e}")
        
        # 8. Cleanup
        print(f"\n8. Cleanup:")
        try:
            db.delete_document(doc.external_id)
            print(f"   SUCCESS: Test document deleted")
        except Exception as e:
            print(f"   WARNING: Could not delete test document: {e}")
            
    except Exception as e:
        print(f"   ERROR: Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ingestion() 
import os
import sys
from datetime import datetime

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    print("python-dotenv not installed")
    sys.exit(1)

from morphik import Morphik
from core.schemas import BaseModel, Field, MetadataExtractionRule

class SimpleTest(BaseModel):
    title: str = Field(description="Document title")
    document_type: str = Field(description="Type of document")

def debug_ingestion():
    """Debug the ingestion process step by step."""
    print("=== INGESTION DEBUG ===")
    
    # 1. Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"1. Environment Check:")
    print(f"   MORPHIK_URI: {'SET' if morphik_uri else 'NOT SET'}")
    print(f"   OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
    
    if not morphik_uri:
        print("   ERROR: MORPHIK_URI not set")
        return
    
    # 2. Connect to Morphik
    print(f"\n2. Morphik Connection:")
    try:
        db = Morphik(morphik_uri)
        docs = db.list_documents()
        print(f"   SUCCESS: Connected, found {len(docs)} documents")
    except Exception as e:
        print(f"   ERROR: Connection failed: {e}")
        return
    
    # 3. Find a test file
    print(f"\n3. Test File:")
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"   ERROR: PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"   ERROR: No PDF files found")
        return
    
    test_file = pdf_files[0]
    print(f"   Using: {test_file.name}")
    
    # 4. Create a simple rule
    print(f"\n4. Rule Creation:")
    try:
        rule = MetadataExtractionRule(schema=SimpleTest)
        print(f"   SUCCESS: Created rule with schema: {SimpleTest.__name__}")
    except Exception as e:
        print(f"   ERROR: Rule creation failed: {e}")
        return
    
    # 5. Ingest with detailed logging
    print(f"\n5. Ingestion Process:")
    try:
        print(f"   Starting ingestion...")
        doc = db.ingest_file(test_file, filename=test_file.name, rules=[rule])
        print(f"   SUCCESS: File ingested")
        print(f"   Document ID: {doc.external_id}")
        print(f"   Initial status: {doc.status}")
        print(f"   Status type: {type(doc.status)}")
        
        # 6. Wait for completion with detailed status tracking
        print(f"\n6. Status Tracking:")
        
        # First, try wait_for_completion
        print(f"   Calling wait_for_completion()...")
        try:
            doc.wait_for_completion()
            print(f"   SUCCESS: wait_for_completion() returned")
            print(f"   Final status: {doc.status}")
        except Exception as e:
            print(f"   ERROR: wait_for_completion() failed: {e}")
        
        # Then check status manually
        max_checks = 10
        for i in range(max_checks):
            print(f"   Check {i+1}/{max_checks}: Status = {doc.status}")
            
            # Check if completed
            if isinstance(doc.status, dict):
                status_value = doc.status.get('status', 'unknown')
            else:
                status_value = doc.status
                
            if status_value == 'completed':
                print(f"   SUCCESS: Document completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"   ERROR: Document failed with status: {status_value}")
                break
            else:
                print(f"   Waiting... (status: {status_value})")
                import time
                time.sleep(3)
        else:
            print(f"   TIMEOUT: Document did not complete within {max_checks * 3} seconds")
        
        # 7. Fetch and examine the document
        print(f"\n7. Document Examination:")
        try:
            full_doc = db.get_document(doc.external_id)
            print(f"   SUCCESS: Document fetched")
            print(f"   Document object type: {type(full_doc)}")
            print(f"   Available attributes: {[attr for attr in dir(full_doc) if not attr.startswith('_')]}")
            
            # Check metadata
            if hasattr(full_doc, 'metadata'):
                print(f"   Metadata: {full_doc.metadata}")
                print(f"   Metadata type: {type(full_doc.metadata)}")
            else:
                print(f"   No metadata attribute found")
                
            # Check system_metadata
            if hasattr(full_doc, 'system_metadata'):
                print(f"   System metadata: {full_doc.system_metadata}")
            else:
                print(f"   No system_metadata attribute found")
                
        except Exception as e:
            print(f"   ERROR: Failed to fetch document: {e}")
        
        # 8. Cleanup
        print(f"\n8. Cleanup:")
        try:
            db.delete_document(doc.external_id)
            print(f"   SUCCESS: Test document deleted")
        except Exception as e:
            print(f"   WARNING: Could not delete test document: {e}")
            
    except Exception as e:
        print(f"   ERROR: Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ingestion() 