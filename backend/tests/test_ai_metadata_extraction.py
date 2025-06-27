

#!/usr/bin/env python3
"""
Test script for AI-powered metadata extraction
Validates that our ECSS rules can properly extract metadata using AI instead of regex.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script for AI-powered metadata extraction
Validates that our ECSS rules can properly extract metadata using AI instead of regex.
"""

import os
import sys
import json
from typing import List, Dict

# Load environment variables from .env file
try:
        except ImportError:
    pass  # Continue without dotenv if not available
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    pass

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_rules_schema import (
    create_ecss_metadata_rules,
    create_ecss_content_rules,
    create_ecss_quality_rules,
    validate_ecss_rules
)

def test_rules_creation():
    """Test that we can create all the AI-powered rules."""
    print("🧪 Testing AI-Powered Rules Creation...")
    
    try:
        # Test metadata rules (these will extract branch, discipline, etc.)
        metadata_rules = create_ecss_metadata_rules()
        print(f"✅ Created {len(metadata_rules)} metadata extraction rules")
        
        # Test content rules
        content_rules = create_ecss_content_rules()
        print(f"✅ Created {len(content_rules)} content transformation rules")
        
        # Test quality rules
        quality_rules = create_ecss_quality_rules()
        print(f"✅ Created {len(quality_rules)} quality assurance rules")
        
        # Combine all rules
        all_rules = metadata_rules + content_rules + quality_rules
        print(f"✅ Total rules: {len(all_rules)}")
        
        # Validate rules
        is_valid = validate_ecss_rules(all_rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        return all_rules
        
    except Exception as e:
        print(f"❌ Rules creation test failed: {e}")
        return None

def test_morphik_connection():
    """Test connection to Morphik."""
    print("\n🔗 Testing Morphik Connection...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return None
        
        db = Morphik(morphik_uri)
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"✅ Found {len(documents)} existing documents")
        
        return db
        
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return None

def test_single_document_ai_extraction(db, test_file_path: str):
    """Test AI-powered metadata extraction on a single document."""
    print(f"\n📄 Testing AI Metadata Extraction on: {Path(test_file_path).name}")
    
    try:
        # Get comprehensive rules
        all_rules = create_ecss_metadata_rules() + create_ecss_content_rules() + create_ecss_quality_rules()
        
        print(f"✅ Using {len(all_rules)} AI-powered rules")
        
        # Test ingestion with AI rules
        print("🔄 Ingesting document with AI rules...")
        
        doc = db.ingest_file(
            test_file_path,
            metadata={
                'filename': Path(test_file_path).name,
                'source': 'ECSS Standards Navigator Test'
            },
            rules=all_rules,
            use_colpali=True
        )
        
        print(f"✅ Document ingested successfully")
        
        # Get document details to see what metadata was extracted
        doc_id = getattr(doc, 'external_id', None)
        if doc_id:
            print(f"✅ Document ID: {doc_id}")
            
            # Try to get the document to see extracted metadata
            try:
                doc_info = db.get_document(doc_id)
                if hasattr(doc_info, 'metadata') and doc_info.metadata:
                    print("📊 AI-Extracted Metadata:")
                    for key, value in doc_info.metadata.items():
                        print(f"   {key}: {value}")
                else:
                    print("⚠️  No metadata found in document info")
                    
            except Exception as e:
                print(f"⚠️  Could not retrieve document details: {e}")
        
        # Clean up - delete the test document
        try:
            db.delete_document(doc_id)
            print(f"✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up test document: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI metadata extraction test failed: {e}")
        return False

def find_test_document():
    """Find a suitable test document."""
    print("\n📁 Looking for test document...")
    
    # Look for a small ECSS document
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return None
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_dir}")
        return None
    
    # Find the smallest file for quick testing
    smallest_file = min(pdf_files, key=lambda f: f.stat().st_size)
    file_size_mb = smallest_file.stat().st_size / (1024 * 1024)
    
    print(f"✅ Found test document: {smallest_file.name}")
    print(f"✅ File size: {file_size_mb:.2f} MB")
    
    return str(smallest_file)

def main():
    """Main test function."""
    print("🚀 AI-Powered Metadata Extraction Test")
    print("=" * 50)
    
    # Test 1: Rules creation
    rules = test_rules_creation()
    if not rules:
        print("❌ Rules creation failed, stopping test")
        return False
    
    # Test 2: Morphik connection
    db = test_morphik_connection()
    if not db:
        print("❌ Morphik connection failed, stopping test")
        return False
    
    # Test 3: Find test document
    test_file = find_test_document()
    if not test_file:
        print("❌ No test document found, stopping test")
        return False
    
    # Test 4: AI metadata extraction
    success = test_single_document_ai_extraction(db, test_file)
    
    if success:
        print("\n🎉 AI-Powered Metadata Extraction Test PASSED!")
        print("✅ The system is ready for full ingestion with AI-powered metadata extraction")
    else:
        print("\n❌ AI-Powered Metadata Extraction Test FAILED!")
        print("⚠️  Please check the errors above before proceeding with full ingestion")
    
    return success

if __name__ == "__main__":
    main() 

import os
import sys
import json
from typing import List, Dict

# Load environment variables from .env file
try:
        except ImportError:
    pass  # Continue without dotenv if not available
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    pass

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_rules_schema import (
    create_ecss_metadata_rules,
    create_ecss_content_rules,
    create_ecss_quality_rules,
    validate_ecss_rules
)

def test_rules_creation():
    """Test that we can create all the AI-powered rules."""
    print("🧪 Testing AI-Powered Rules Creation...")
    
    try:
        # Test metadata rules (these will extract branch, discipline, etc.)
        metadata_rules = create_ecss_metadata_rules()
        print(f"✅ Created {len(metadata_rules)} metadata extraction rules")
        
        # Test content rules
        content_rules = create_ecss_content_rules()
        print(f"✅ Created {len(content_rules)} content transformation rules")
        
        # Test quality rules
        quality_rules = create_ecss_quality_rules()
        print(f"✅ Created {len(quality_rules)} quality assurance rules")
        
        # Combine all rules
        all_rules = metadata_rules + content_rules + quality_rules
        print(f"✅ Total rules: {len(all_rules)}")
        
        # Validate rules
        is_valid = validate_ecss_rules(all_rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        return all_rules
        
    except Exception as e:
        print(f"❌ Rules creation test failed: {e}")
        return None

def test_morphik_connection():
    """Test connection to Morphik."""
    print("\n🔗 Testing Morphik Connection...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return None
        
        db = Morphik(morphik_uri)
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"✅ Found {len(documents)} existing documents")
        
        return db
        
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return None

def test_single_document_ai_extraction(db, test_file_path: str):
    """Test AI-powered metadata extraction on a single document."""
    print(f"\n📄 Testing AI Metadata Extraction on: {Path(test_file_path).name}")
    
    try:
        # Get comprehensive rules
        all_rules = create_ecss_metadata_rules() + create_ecss_content_rules() + create_ecss_quality_rules()
        
        print(f"✅ Using {len(all_rules)} AI-powered rules")
        
        # Test ingestion with AI rules
        print("🔄 Ingesting document with AI rules...")
        
        doc = db.ingest_file(
            test_file_path,
            metadata={
                'filename': Path(test_file_path).name,
                'source': 'ECSS Standards Navigator Test'
            },
            rules=all_rules,
            use_colpali=True
        )
        
        print(f"✅ Document ingested successfully")
        
        # Get document details to see what metadata was extracted
        doc_id = getattr(doc, 'external_id', None)
        if doc_id:
            print(f"✅ Document ID: {doc_id}")
            
            # Try to get the document to see extracted metadata
            try:
                doc_info = db.get_document(doc_id)
                if hasattr(doc_info, 'metadata') and doc_info.metadata:
                    print("📊 AI-Extracted Metadata:")
                    for key, value in doc_info.metadata.items():
                        print(f"   {key}: {value}")
                else:
                    print("⚠️  No metadata found in document info")
                    
            except Exception as e:
                print(f"⚠️  Could not retrieve document details: {e}")
        
        # Clean up - delete the test document
        try:
            db.delete_document(doc_id)
            print(f"✅ Cleaned up test document")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up test document: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI metadata extraction test failed: {e}")
        return False

def find_test_document():
    """Find a suitable test document."""
    print("\n📁 Looking for test document...")
    
    # Look for a small ECSS document
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return None
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_dir}")
        return None
    
    # Find the smallest file for quick testing
    smallest_file = min(pdf_files, key=lambda f: f.stat().st_size)
    file_size_mb = smallest_file.stat().st_size / (1024 * 1024)
    
    print(f"✅ Found test document: {smallest_file.name}")
    print(f"✅ File size: {file_size_mb:.2f} MB")
    
    return str(smallest_file)

def main():
    """Main test function."""
    print("🚀 AI-Powered Metadata Extraction Test")
    print("=" * 50)
    
    # Test 1: Rules creation
    rules = test_rules_creation()
    if not rules:
        print("❌ Rules creation failed, stopping test")
        return False
    
    # Test 2: Morphik connection
    db = test_morphik_connection()
    if not db:
        print("❌ Morphik connection failed, stopping test")
        return False
    
    # Test 3: Find test document
    test_file = find_test_document()
    if not test_file:
        print("❌ No test document found, stopping test")
        return False
    
    # Test 4: AI metadata extraction
    success = test_single_document_ai_extraction(db, test_file)
    
    if success:
        print("\n🎉 AI-Powered Metadata Extraction Test PASSED!")
        print("✅ The system is ready for full ingestion with AI-powered metadata extraction")
    else:
        print("\n❌ AI-Powered Metadata Extraction Test FAILED!")
        print("⚠️  Please check the errors above before proceeding with full ingestion")
    
    return success

if __name__ == "__main__":
    main() 