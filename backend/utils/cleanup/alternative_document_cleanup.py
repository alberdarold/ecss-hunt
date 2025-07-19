#!/usr/bin/env python3
"""
ALTERNATIVE DOCUMENT CLEANUP
============================

Try alternative methods to delete documents without using list_documents().
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from morphik import Morphik

def main():
    """Try alternative document deletion methods."""
    print("🔄 ALTERNATIVE DOCUMENT CLEANUP")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    try:
        # Connect to Morphik
        print("🔗 Connecting to Morphik...")
        db = Morphik(morphik_uri)
        
        print("🔍 Available deletion methods:")
        deletion_methods = [attr for attr in dir(db) if 'delete' in attr.lower()]
        for method in deletion_methods:
            print(f"  - {method}")
        
        # Try alternative approaches
        print(f"\n🎯 Trying Alternative Approaches:")
        
        # Method 1: Try delete by filename patterns
        print(f"\n1️⃣ Trying delete by filename...")
        ecss_patterns = [
            "ECSS-E-AS-11C",
            "ECSS-M-70A", 
            "ECSS-E-ST-40C",
            "ECSS-Q-ST-80C"
        ]
        
        for pattern in ecss_patterns:
            try:
                result = db.delete_document_by_filename(f"{pattern}.pdf")
                print(f"✅ Deleted: {pattern}.pdf")
            except Exception as e:
                if "not found" in str(e).lower():
                    print(f"⚪ Not found: {pattern}.pdf")
                else:
                    print(f"❌ Error deleting {pattern}.pdf: {e}")
        
        # Method 2: Try batch operations for cleanup
        print(f"\n2️⃣ Trying batch operations...")
        try:
            # See if batch_get_documents works without list_documents
            docs = db.batch_get_documents()
            if docs:
                print(f"📊 Found {len(docs)} documents via batch method")
                for i, doc in enumerate(docs[:3]):  # Try first 3
                    try:
                        doc_id = getattr(doc, 'id', None)
                        if doc_id:
                            db.delete_document(doc_id)
                            print(f"✅ Deleted document {i+1}")
                        else:
                            print(f"⚠️ Document {i+1} has no ID")
                    except Exception as e:
                        print(f"❌ Error deleting document {i+1}: {e}")
            else:
                print("❌ No documents found via batch method")
        except Exception as e:
            print(f"❌ Batch method failed: {e}")
        
        # Method 3: Try to get documents through search results
        print(f"\n3️⃣ Trying via search results...")
        try:
            # Search for something general to get document references
            chunks = db.retrieve_chunks("ECSS", k=10)
            if chunks:
                print(f"📚 Found {len(chunks)} chunks")
                
                # Extract unique document references
                doc_refs = set()
                for chunk in chunks:
                    if hasattr(chunk, 'document_id'):
                        doc_refs.add(chunk.document_id)
                    elif hasattr(chunk, 'filename'):
                        doc_refs.add(chunk.filename)
                
                print(f"🔍 Found {len(doc_refs)} unique document references")
                
                # Try to delete by reference
                for ref in list(doc_refs)[:3]:  # Try first 3
                    try:
                        if ref.endswith('.pdf'):
                            # Try delete by filename
                            db.delete_document_by_filename(ref)
                            print(f"✅ Deleted by filename: {ref}")
                        else:
                            # Try delete by ID
                            db.delete_document(ref)
                            print(f"✅ Deleted by ID: {ref}")
                    except Exception as e:
                        print(f"❌ Error deleting {ref}: {e}")
            else:
                print("❌ No chunks found")
        except Exception as e:
            print(f"❌ Search method failed: {e}")
        
        # Method 4: Check if there's a bulk delete method
        print(f"\n4️⃣ Looking for bulk delete methods...")
        bulk_methods = [attr for attr in dir(db) if any(term in attr.lower() for term in ['bulk', 'all', 'clear', 'purge'])]
        if bulk_methods:
            print(f"🔍 Found potential bulk methods: {bulk_methods}")
            for method in bulk_methods:
                print(f"  - {method} (not attempting - could be dangerous)")
        else:
            print("❌ No bulk delete methods found")
        
        print(f"\n🏁 Alternative cleanup attempts completed")
        print(f"💡 If documents persist, they may need to be deleted from the Morphik web interface")
        
    except Exception as e:
        print(f"❌ Alternative cleanup failed: {e}")

if __name__ == "__main__":
    main() 