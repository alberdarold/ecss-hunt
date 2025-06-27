
# Add backend root to path


#!/usr/bin/env python3
"""
Utility script to delete ALL documents from a Morphik project.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Utility script to delete ALL documents from a Morphik project.
"""
import os
import sys
from morphik import Morphik

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

        for i, doc in enumerate(documents, 1):
            doc_id = getattr(doc, 'external_id', None) or getattr(doc, 'id', None)
            if doc_id:
                try:
                    print(f"Deleting document {i}/{len(documents)}: {doc_id} ({getattr(doc, 'filename', 'N/A')})...")
                    db.delete_document(doc_id)
                except Exception as e:
                    print(f"Failed to delete document {doc_id}: {e}")
            else:
                print(f"Could not find ID for document {i}, skipping.")

        print(f"Successfully deleted {len(documents)} documents.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Remove confirmation for non-interactive use, assuming user intent is clear
    delete_all_documents() 
import os
import sys
from morphik import Morphik

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

        for i, doc in enumerate(documents, 1):
            doc_id = getattr(doc, 'external_id', None) or getattr(doc, 'id', None)
            if doc_id:
                try:
                    print(f"Deleting document {i}/{len(documents)}: {doc_id} ({getattr(doc, 'filename', 'N/A')})...")
                    db.delete_document(doc_id)
                except Exception as e:
                    print(f"Failed to delete document {doc_id}: {e}")
            else:
                print(f"Could not find ID for document {i}, skipping.")

        print(f"Successfully deleted {len(documents)} documents.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Remove confirmation for non-interactive use, assuming user intent is clear
    delete_all_documents() 