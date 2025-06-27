

#!/usr/bin/env python3
"""
Check AI-extracted metadata from ingested documents
Shows what metadata was actually extracted by the AI rules.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Check AI-extracted metadata from ingested documents
Shows what metadata was actually extracted by the AI rules.
"""

import os
import sys
import json

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    pass

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def check_ai_metadata():
    """Check what metadata was extracted by AI rules."""
    print("🔍 Checking AI-Extracted Metadata...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return
        
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents")
        
        for i, doc in enumerate(documents, 1):
            print(f"\n--- Document {i} ---")
            print(f"ID: {getattr(doc, 'external_id', 'N/A')}")
            print(f"Filename: {getattr(doc, 'filename', 'N/A')}")
            
            # Check different metadata sources
            print("\n📊 Metadata Sources:")
            
            # 1. Basic metadata
            basic_metadata = getattr(doc, 'metadata', {})
            if basic_metadata:
                print("   Basic Metadata:")
                for key, value in basic_metadata.items():
                    print(f"     {key}: {value}")
            else:
                print("   Basic Metadata: None")
            
            # 2. System metadata
            system_metadata = getattr(doc, 'system_metadata', {})
            if system_metadata:
                print("   System Metadata:")
                for key, value in system_metadata.items():
                    print(f"     {key}: {value}")
            else:
                print("   System Metadata: None")
            
            # 3. Try to get document details
            try:
                doc_id = getattr(doc, 'external_id', None)
                if doc_id:
                    doc_details = db.get_document(doc_id)
                    print("   Document Details:")
                    print(f"     Status: {getattr(doc_details, 'status', 'N/A')}")
                    
                    # Check for extracted entities/structured data
                    if hasattr(doc_details, 'entities') and doc_details.entities:
                        print("     AI-Extracted Entities:")
                        for entity in doc_details.entities[:5]:  # Show first 5
                            print(f"       - {entity}")
                    
                    if hasattr(doc_details, 'metadata') and doc_details.metadata:
                        print("     AI-Extracted Metadata:")
                        for key, value in doc_details.metadata.items():
                            print(f"       {key}: {value}")
                            
            except Exception as e:
                print(f"     Could not get document details: {e}")
            
            # 4. Check for any other attributes
            print("   All Available Attributes:")
            for attr in dir(doc):
                if not attr.startswith('_'):
                    try:
                        value = getattr(doc, attr)
                        if value and not callable(value):
                            print(f"     {attr}: {value}")
                    except:
                        pass
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to check AI metadata: {e}")
        return False

def main():
    """Main function."""
    print("🚀 AI Metadata Check")
    print("=" * 30)
    
    success = check_ai_metadata()
    
    if success:
        print("\n✅ AI metadata check completed")
    else:
        print("\n❌ AI metadata check failed")

if __name__ == "__main__":
    main() 

import os
import sys
import json

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    pass

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def check_ai_metadata():
    """Check what metadata was extracted by AI rules."""
    print("🔍 Checking AI-Extracted Metadata...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return
        
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents")
        
        for i, doc in enumerate(documents, 1):
            print(f"\n--- Document {i} ---")
            print(f"ID: {getattr(doc, 'external_id', 'N/A')}")
            print(f"Filename: {getattr(doc, 'filename', 'N/A')}")
            
            # Check different metadata sources
            print("\n📊 Metadata Sources:")
            
            # 1. Basic metadata
            basic_metadata = getattr(doc, 'metadata', {})
            if basic_metadata:
                print("   Basic Metadata:")
                for key, value in basic_metadata.items():
                    print(f"     {key}: {value}")
            else:
                print("   Basic Metadata: None")
            
            # 2. System metadata
            system_metadata = getattr(doc, 'system_metadata', {})
            if system_metadata:
                print("   System Metadata:")
                for key, value in system_metadata.items():
                    print(f"     {key}: {value}")
            else:
                print("   System Metadata: None")
            
            # 3. Try to get document details
            try:
                doc_id = getattr(doc, 'external_id', None)
                if doc_id:
                    doc_details = db.get_document(doc_id)
                    print("   Document Details:")
                    print(f"     Status: {getattr(doc_details, 'status', 'N/A')}")
                    
                    # Check for extracted entities/structured data
                    if hasattr(doc_details, 'entities') and doc_details.entities:
                        print("     AI-Extracted Entities:")
                        for entity in doc_details.entities[:5]:  # Show first 5
                            print(f"       - {entity}")
                    
                    if hasattr(doc_details, 'metadata') and doc_details.metadata:
                        print("     AI-Extracted Metadata:")
                        for key, value in doc_details.metadata.items():
                            print(f"       {key}: {value}")
                            
            except Exception as e:
                print(f"     Could not get document details: {e}")
            
            # 4. Check for any other attributes
            print("   All Available Attributes:")
            for attr in dir(doc):
                if not attr.startswith('_'):
                    try:
                        value = getattr(doc, attr)
                        if value and not callable(value):
                            print(f"     {attr}: {value}")
                    except:
                        pass
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to check AI metadata: {e}")
        return False

def main():
    """Main function."""
    print("🚀 AI Metadata Check")
    print("=" * 30)
    
    success = check_ai_metadata()
    
    if success:
        print("\n✅ AI metadata check completed")
    else:
        print("\n❌ AI metadata check failed")

if __name__ == "__main__":
    main() 