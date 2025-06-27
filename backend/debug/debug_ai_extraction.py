

#!/usr/bin/env python3
"""
Debug script to investigate AI metadata extraction issues.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to investigate AI metadata extraction issues.
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_rules_schema import create_ecss_metadata_rules, create_ecss_content_rules, create_ecss_quality_rules

def debug_ai_extraction():
    """Debug the AI metadata extraction process."""
    print("🔍 Debugging AI Metadata Extraction")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents in project")
    
    for i, doc in enumerate(documents, 1):
        print(f"\n--- Document {i}: {getattr(doc, 'filename', 'Unknown')} ---")
        
        # Get document ID - try different possible attributes
        doc_id = None
        for attr in ['id', 'external_id', 'document_id']:
            if hasattr(doc, attr):
                doc_id = getattr(doc, attr)
                print(f"ID ({attr}): {doc_id}")
                break
        
        if not doc_id:
            print("❌ Could not find document ID")
            continue
        
        print(f"Status: {getattr(doc, 'status', 'Unknown')}")
        
        # Fetch the full document using get_document
        print(f"\n🔄 Fetching full document using get_document...")
        try:
            full_doc = db.get_document(doc_id)
            print(f"✅ Successfully fetched document with get_document")
            print(f"All attributes:")
            for attr in dir(full_doc):
                if not attr.startswith('_'):
                    try:
                        value = getattr(full_doc, attr)
                        if callable(value):
                            continue
                        print(f"  {attr}: {str(value)[:100]}")
                    except Exception as e:
                        print(f"  {attr}: <error: {e}>")
            # Print metadata
            print(f"\n.metadata: {getattr(full_doc, 'metadata', None)}")
            print(f".system_metadata: {getattr(full_doc, 'system_metadata', None)}")
            
            # Check workflow status
            print(f"\n🔍 Checking workflow status...")
            try:
                status = db.check_workflow_status(doc_id)
                print(f"Workflow status: {status}")
            except Exception as e:
                print(f"❌ Error checking workflow status: {e}")
                
        except Exception as e:
            print(f"❌ Error fetching document with get_document: {e}")

def test_rule_creation():
    """Test that the rules are being created correctly."""
    print("\n🧪 Testing Rule Creation")
    print("=" * 30)
    
    try:
        # Create rules
        metadata_rules = create_ecss_metadata_rules()
        content_rules = create_ecss_content_rules()
        quality_rules = create_ecss_quality_rules()
        
        all_rules = metadata_rules + content_rules + quality_rules
        
        print(f"✅ Created {len(all_rules)} rules total")
        print(f"  - Metadata rules: {len(metadata_rules)}")
        print(f"  - Content rules: {len(content_rules)}")
        print(f"  - Quality rules: {len(quality_rules)}")
        
        # Show first rule as example
        if all_rules:
            first_rule = all_rules[0]
            print(f"\n📋 Example rule:")
            print(f"  Name: {first_rule.name}")
            print(f"  Description: {first_rule.description}")
            print(f"  Prompt: {first_rule.prompt[:100]}...")
        
        return all_rules
        
    except Exception as e:
        print(f"❌ Error creating rules: {e}")
        return []

def test_single_document_ingestion():
    """Test ingesting a single document with detailed logging."""
    print("\n🧪 Testing Single Document Ingestion")
    print("=" * 40)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Find a PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    test_file = pdf_files[0]
    print(f"📄 Testing with: {test_file.name}")
    
    # Create rules
    rules = test_rule_creation()
    if not rules:
        print("❌ No rules created, aborting test")
        return
    
    try:
        print(f"\n🚀 Starting ingestion with {len(rules)} rules...")
        
        # Ingest the file
        doc = db.ingest_file(test_file, rules=rules, external_id=f"test_{test_file.name}")
        print(f"✅ File ingested, document ID: {doc.id}")
        print(f"📊 Initial status: {doc.status}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing to complete...")
        doc.wait_for_completion(timeout=300)  # 5 minutes
        print(f"✅ Processing complete, final status: {doc.status}")
        
        # Check structured_data immediately
        print(f"\n🔍 Checking structured_data immediately after completion...")
        if hasattr(doc, 'structured_data'):
            if doc.structured_data:
                print(f"✅ structured_data found: {list(doc.structured_data.keys())}")
                print(f"Content: {doc.structured_data}")
            else:
                print("❌ structured_data is empty")
        else:
            print("❌ No structured_data attribute")
        
        # Re-fetch and check again
        print(f"\n🔄 Re-fetching document...")
        refetched_doc = db.get_document(doc.external_id)
        if refetched_doc:
            print(f"✅ Document re-fetched")
            if hasattr(refetched_doc, 'metadata') and refetched_doc.metadata:
                print(f"✅ Re-fetched document has metadata: {list(refetched_doc.metadata.keys())}")
                print(f"Content: {refetched_doc.metadata}")
            else:
                print("❌ Re-fetched document has no metadata")
        else:
            print("❌ Failed to re-fetch document")
            
        # Check workflow status
        print(f"\n🔍 Checking workflow status...")
        try:
            status = db.check_workflow_status(doc.external_id)
            print(f"Workflow status: {status}")
        except Exception as e:
            print(f"❌ Error checking workflow status: {e}")
            
    except Exception as e:
        print(f"❌ Error during test ingestion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting AI Extraction Debug")
    
    # Test 1: Check existing documents
    debug_ai_extraction()
    
    # Test 2: Test rule creation
    test_rule_creation()
    
    # Test 3: Test single document ingestion
    test_single_document_ingestion()
    
    print("\n�� Debug complete") 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_rules_schema import create_ecss_metadata_rules, create_ecss_content_rules, create_ecss_quality_rules

def debug_ai_extraction():
    """Debug the AI metadata extraction process."""
    print("🔍 Debugging AI Metadata Extraction")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents in project")
    
    for i, doc in enumerate(documents, 1):
        print(f"\n--- Document {i}: {getattr(doc, 'filename', 'Unknown')} ---")
        
        # Get document ID - try different possible attributes
        doc_id = None
        for attr in ['id', 'external_id', 'document_id']:
            if hasattr(doc, attr):
                doc_id = getattr(doc, attr)
                print(f"ID ({attr}): {doc_id}")
                break
        
        if not doc_id:
            print("❌ Could not find document ID")
            continue
        
        print(f"Status: {getattr(doc, 'status', 'Unknown')}")
        
        # Fetch the full document using get_document
        print(f"\n🔄 Fetching full document using get_document...")
        try:
            full_doc = db.get_document(doc_id)
            print(f"✅ Successfully fetched document with get_document")
            print(f"All attributes:")
            for attr in dir(full_doc):
                if not attr.startswith('_'):
                    try:
                        value = getattr(full_doc, attr)
                        if callable(value):
                            continue
                        print(f"  {attr}: {str(value)[:100]}")
                    except Exception as e:
                        print(f"  {attr}: <error: {e}>")
            # Print metadata
            print(f"\n.metadata: {getattr(full_doc, 'metadata', None)}")
            print(f".system_metadata: {getattr(full_doc, 'system_metadata', None)}")
            
            # Check workflow status
            print(f"\n🔍 Checking workflow status...")
            try:
                status = db.check_workflow_status(doc_id)
                print(f"Workflow status: {status}")
            except Exception as e:
                print(f"❌ Error checking workflow status: {e}")
                
        except Exception as e:
            print(f"❌ Error fetching document with get_document: {e}")

def test_rule_creation():
    """Test that the rules are being created correctly."""
    print("\n🧪 Testing Rule Creation")
    print("=" * 30)
    
    try:
        # Create rules
        metadata_rules = create_ecss_metadata_rules()
        content_rules = create_ecss_content_rules()
        quality_rules = create_ecss_quality_rules()
        
        all_rules = metadata_rules + content_rules + quality_rules
        
        print(f"✅ Created {len(all_rules)} rules total")
        print(f"  - Metadata rules: {len(metadata_rules)}")
        print(f"  - Content rules: {len(content_rules)}")
        print(f"  - Quality rules: {len(quality_rules)}")
        
        # Show first rule as example
        if all_rules:
            first_rule = all_rules[0]
            print(f"\n📋 Example rule:")
            print(f"  Name: {first_rule.name}")
            print(f"  Description: {first_rule.description}")
            print(f"  Prompt: {first_rule.prompt[:100]}...")
        
        return all_rules
        
    except Exception as e:
        print(f"❌ Error creating rules: {e}")
        return []

def test_single_document_ingestion():
    """Test ingesting a single document with detailed logging."""
    print("\n🧪 Testing Single Document Ingestion")
    print("=" * 40)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Find a PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    test_file = pdf_files[0]
    print(f"📄 Testing with: {test_file.name}")
    
    # Create rules
    rules = test_rule_creation()
    if not rules:
        print("❌ No rules created, aborting test")
        return
    
    try:
        print(f"\n🚀 Starting ingestion with {len(rules)} rules...")
        
        # Ingest the file
        doc = db.ingest_file(test_file, rules=rules, external_id=f"test_{test_file.name}")
        print(f"✅ File ingested, document ID: {doc.id}")
        print(f"📊 Initial status: {doc.status}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing to complete...")
        doc.wait_for_completion(timeout=300)  # 5 minutes
        print(f"✅ Processing complete, final status: {doc.status}")
        
        # Check structured_data immediately
        print(f"\n🔍 Checking structured_data immediately after completion...")
        if hasattr(doc, 'structured_data'):
            if doc.structured_data:
                print(f"✅ structured_data found: {list(doc.structured_data.keys())}")
                print(f"Content: {doc.structured_data}")
            else:
                print("❌ structured_data is empty")
        else:
            print("❌ No structured_data attribute")
        
        # Re-fetch and check again
        print(f"\n🔄 Re-fetching document...")
        refetched_doc = db.get_document(doc.external_id)
        if refetched_doc:
            print(f"✅ Document re-fetched")
            if hasattr(refetched_doc, 'metadata') and refetched_doc.metadata:
                print(f"✅ Re-fetched document has metadata: {list(refetched_doc.metadata.keys())}")
                print(f"Content: {refetched_doc.metadata}")
            else:
                print("❌ Re-fetched document has no metadata")
        else:
            print("❌ Failed to re-fetch document")
            
        # Check workflow status
        print(f"\n🔍 Checking workflow status...")
        try:
            status = db.check_workflow_status(doc.external_id)
            print(f"Workflow status: {status}")
        except Exception as e:
            print(f"❌ Error checking workflow status: {e}")
            
    except Exception as e:
        print(f"❌ Error during test ingestion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting AI Extraction Debug")
    
    # Test 1: Check existing documents
    debug_ai_extraction()
    
    # Test 2: Test rule creation
    test_rule_creation()
    
    # Test 3: Test single document ingestion
    test_single_document_ingestion()
    
    print("\n�� Debug complete") 