#!/usr/bin/env python3
"""
Utility script to delete ALL documents from a Morphik project.
"""
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
import os
from morphik import Morphik

# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

def delete_all_documents():
    """Connects to Morphik and deletes every document in the project."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("MORPHIK_URI environment variable not set.")
        return

    try:
        db = Morphik(morphik_uri)
        print(f"Connected to Morphik project.")
        
        documents = db.list_documents()
        if not documents:
            print("No documents found to delete.")
            return

        print(f"Found {len(documents)} documents to delete. This may take a moment...")

        deleted_count = 0
        for i, doc in enumerate(documents, 1):
            doc_id = getattr(doc, 'external_id', None) or getattr(doc, 'id', None)
            filename = getattr(doc, 'filename', 'N/A')
            
            if doc_id:
                try:
                    print(f"Deleting document {i}/{len(documents)}: {doc_id} ({filename})...")
                    db.delete_document(doc_id)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete document {doc_id}: {e}")
            else:
                print(f"Could not find ID for document {i}, skipping.")

        print(f"Successfully deleted {deleted_count} out of {len(documents)} documents.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("MORPHIK DOCUMENT DELETION UTILITY")
    print("=" * 50)
    print("This will delete ALL documents in your Morphik project.")
    print("This action cannot be undone!")
    print("=" * 50)
    
    success = delete_all_documents()
    
    if success:
        print("✅ Document deletion completed successfully!")
    else:
        print("❌ Document deletion failed. Check the error messages above.") 