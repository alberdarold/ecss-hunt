

#!/usr/bin/env python3
"""
Check and clean Morphik project before ingestion
Lists all documents and graphs, and optionally deletes them for a fresh start.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Check and clean Morphik project before ingestion
Lists all documents and graphs, and optionally deletes them for a fresh start.
"""

import os
import sys
import argparse

# Load environment variables from .env file
try:
        except ImportError:
    pass

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def check_project_status():
    """Check what's currently in the Morphik project."""
    print("🔍 Checking Morphik Project Status...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return None
        
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Check documents
        try:
            documents = db.list_documents()
            print(f"📄 Documents found: {len(documents)}")
            
            if documents:
                print("\nDocument details:")
                for i, doc in enumerate(documents):
                    doc_id = getattr(doc, 'external_id', 'N/A')
                    filename = getattr(doc, 'filename', 'N/A')
                    print(f"  {i+1}. ID: {doc_id}")
                    print(f"     Filename: {filename}")
            else:
                print("   No documents found")
                
        except Exception as e:
            print(f"⚠️  Could not list documents: {e}")
        
        # Check graphs
        try:
            graphs = db.list_graphs()
            print(f"\n🗺️  Graphs found: {len(graphs)}")
            
            if graphs:
                print("\nGraph details:")
                for i, graph in enumerate(graphs):
                    graph_name = getattr(graph, 'name', 'N/A')
                    entities = getattr(graph, 'entities', [])
                    relationships = getattr(graph, 'relationships', [])
                    print(f"  {i+1}. Name: {graph_name}")
                    print(f"     Entities: {len(entities)}")
                    print(f"     Relationships: {len(relationships)}")
            else:
                print("   No graphs found")
                
        except Exception as e:
            print(f"⚠️  Could not list graphs: {e}")
        
        return db
        
    except Exception as e:
        print(f"❌ Failed to connect to Morphik: {e}")
        return None

def clean_project(db):
    """Clean all documents and graphs from the project."""
    print("\n🧹 Cleaning Morphik Project...")
    
    try:
        # Delete all documents
        documents = db.list_documents()
        if documents:
            print(f"🗑️  Deleting {len(documents)} documents...")
            for doc in documents:
                try:
                    doc_id = getattr(doc, 'external_id', None)
                    if doc_id:
                        db.delete_document(doc_id)
                        print(f"   ✅ Deleted document: {getattr(doc, 'filename', 'Unknown')}")
                except Exception as e:
                    print(f"   ❌ Failed to delete document: {e}")
        else:
            print("   No documents to delete")
        
        # Delete all graphs
        graphs = db.list_graphs()
        if graphs:
            print(f"🗑️  Deleting {len(graphs)} graphs...")
            for graph in graphs:
                try:
                    graph_name = getattr(graph, 'name', None)
                    if graph_name:
                        db.delete_graph(graph_name)
                        print(f"   ✅ Deleted graph: {graph_name}")
                except Exception as e:
                    print(f"   ❌ Failed to delete graph: {e}")
        else:
            print("   No graphs to delete")
        
        print("✅ Project cleaning completed")
        return True
        
    except Exception as e:
        print(f"❌ Project cleaning failed: {e}")
        return False

def verify_clean_project(db):
    """Verify that the project is now clean."""
    print("\n✅ Verifying Clean Project...")
    
    try:
        # Check documents
        documents = db.list_documents()
        if len(documents) == 0:
            print("✅ No documents remaining")
        else:
            print(f"❌ {len(documents)} documents still remain")
        
        # Check graphs
        graphs = db.list_graphs()
        if len(graphs) == 0:
            print("✅ No graphs remaining")
        else:
            print(f"❌ {len(graphs)} graphs still remain")
        
        if len(documents) == 0 and len(graphs) == 0:
            print("🎉 Project is completely clean and ready for fresh ingestion!")
            return True
        else:
            print("⚠️  Project is not completely clean")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main function to check and optionally clean the project."""
    parser = argparse.ArgumentParser(description="Check and clean Morphik project.")
    parser.add_argument('--force-clean', action='store_true', help='Clean the project without prompting.')
    args = parser.parse_args()

    print("🚀 Morphik Project Check and Clean")
    print("=" * 40)
    
    # Check current status
    db = check_project_status()
    if not db:
        return False
    
    # Ask user if they want to clean, unless --force-clean is used
    print("\n" + "=" * 40)
    
    should_clean = False
    if args.force_clean:
        print("✅ --force-clean flag detected. Proceeding with cleaning.")
        should_clean = True
    else:
        response = input("Do you want to clean the project (delete all documents and graphs)? (y/N): ").strip().lower()
        if response == 'y':
            should_clean = True
    
    if should_clean:
        # Clean the project
        success = clean_project(db)
        if success:
            # Verify it's clean
            verify_clean_project(db)
        else:
            print("❌ Cleaning failed")
            return False
    else:
        print("✅ Project left unchanged")
    
    return True

if __name__ == "__main__":
    main() 

import os
import sys
import argparse

# Load environment variables from .env file
try:
        except ImportError:
    pass

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def check_project_status():
    """Check what's currently in the Morphik project."""
    print("🔍 Checking Morphik Project Status...")
    
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI environment variable not set")
            return None
        
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Check documents
        try:
            documents = db.list_documents()
            print(f"📄 Documents found: {len(documents)}")
            
            if documents:
                print("\nDocument details:")
                for i, doc in enumerate(documents):
                    doc_id = getattr(doc, 'external_id', 'N/A')
                    filename = getattr(doc, 'filename', 'N/A')
                    print(f"  {i+1}. ID: {doc_id}")
                    print(f"     Filename: {filename}")
            else:
                print("   No documents found")
                
        except Exception as e:
            print(f"⚠️  Could not list documents: {e}")
        
        # Check graphs
        try:
            graphs = db.list_graphs()
            print(f"\n🗺️  Graphs found: {len(graphs)}")
            
            if graphs:
                print("\nGraph details:")
                for i, graph in enumerate(graphs):
                    graph_name = getattr(graph, 'name', 'N/A')
                    entities = getattr(graph, 'entities', [])
                    relationships = getattr(graph, 'relationships', [])
                    print(f"  {i+1}. Name: {graph_name}")
                    print(f"     Entities: {len(entities)}")
                    print(f"     Relationships: {len(relationships)}")
            else:
                print("   No graphs found")
                
        except Exception as e:
            print(f"⚠️  Could not list graphs: {e}")
        
        return db
        
    except Exception as e:
        print(f"❌ Failed to connect to Morphik: {e}")
        return None

def clean_project(db):
    """Clean all documents and graphs from the project."""
    print("\n🧹 Cleaning Morphik Project...")
    
    try:
        # Delete all documents
        documents = db.list_documents()
        if documents:
            print(f"🗑️  Deleting {len(documents)} documents...")
            for doc in documents:
                try:
                    doc_id = getattr(doc, 'external_id', None)
                    if doc_id:
                        db.delete_document(doc_id)
                        print(f"   ✅ Deleted document: {getattr(doc, 'filename', 'Unknown')}")
                except Exception as e:
                    print(f"   ❌ Failed to delete document: {e}")
        else:
            print("   No documents to delete")
        
        # Delete all graphs
        graphs = db.list_graphs()
        if graphs:
            print(f"🗑️  Deleting {len(graphs)} graphs...")
            for graph in graphs:
                try:
                    graph_name = getattr(graph, 'name', None)
                    if graph_name:
                        db.delete_graph(graph_name)
                        print(f"   ✅ Deleted graph: {graph_name}")
                except Exception as e:
                    print(f"   ❌ Failed to delete graph: {e}")
        else:
            print("   No graphs to delete")
        
        print("✅ Project cleaning completed")
        return True
        
    except Exception as e:
        print(f"❌ Project cleaning failed: {e}")
        return False

def verify_clean_project(db):
    """Verify that the project is now clean."""
    print("\n✅ Verifying Clean Project...")
    
    try:
        # Check documents
        documents = db.list_documents()
        if len(documents) == 0:
            print("✅ No documents remaining")
        else:
            print(f"❌ {len(documents)} documents still remain")
        
        # Check graphs
        graphs = db.list_graphs()
        if len(graphs) == 0:
            print("✅ No graphs remaining")
        else:
            print(f"❌ {len(graphs)} graphs still remain")
        
        if len(documents) == 0 and len(graphs) == 0:
            print("🎉 Project is completely clean and ready for fresh ingestion!")
            return True
        else:
            print("⚠️  Project is not completely clean")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main function to check and optionally clean the project."""
    parser = argparse.ArgumentParser(description="Check and clean Morphik project.")
    parser.add_argument('--force-clean', action='store_true', help='Clean the project without prompting.')
    args = parser.parse_args()

    print("🚀 Morphik Project Check and Clean")
    print("=" * 40)
    
    # Check current status
    db = check_project_status()
    if not db:
        return False
    
    # Ask user if they want to clean, unless --force-clean is used
    print("\n" + "=" * 40)
    
    should_clean = False
    if args.force_clean:
        print("✅ --force-clean flag detected. Proceeding with cleaning.")
        should_clean = True
    else:
        response = input("Do you want to clean the project (delete all documents and graphs)? (y/N): ").strip().lower()
        if response == 'y':
            should_clean = True
    
    if should_clean:
        # Clean the project
        success = clean_project(db)
        if success:
            # Verify it's clean
            verify_clean_project(db)
        else:
            print("❌ Cleaning failed")
            return False
    else:
        print("✅ Project left unchanged")
    
    return True

if __name__ == "__main__":
    main() 