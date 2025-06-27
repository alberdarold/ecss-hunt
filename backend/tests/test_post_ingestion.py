

#!/usr/bin/env python3
"""
Comprehensive Post-Ingestion Test Script
Validates the entire ECSS system after document ingestion, including:
1. Document and AI metadata integrity.
2. Correct knowledge graph creation.
3. Search functionality.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Comprehensive Post-Ingestion Test Script
Validates the entire ECSS system after document ingestion, including:
1. Document and AI metadata integrity.
2. Correct knowledge graph creation.
3. Search functionality.
"""

import os
import sys
import time

# Load environment variables
try:
        except ImportError:
    pass

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_graph_prompts import create_ecss_graph_prompts

def get_db_connection():
    """Establishes and returns a Morphik DB connection."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI environment variable not set.")
        return None
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully.")
        return db
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return None

def test_1_document_ingestion_status(db):
    """Test 1: Check if documents were ingested and inspect their AI-extracted data."""
    print("\n" + "="*50)
    print("✅ TEST 1: DOCUMENT INGESTION & AI METADATA STATUS")
    print("="*50)
    
    try:
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents.")
        if not documents:
            print("❌ No documents found. Please run ingestion first.")
            return False, None

        # Inspect the first document
        doc_to_inspect = documents[0]
        doc_id = getattr(doc_to_inspect, 'external_id', 'N/A')
        print(f"\n🔬 Inspecting first document (ID: {doc_id})...")
        
        doc_details = db.get_document(doc_id)
        
        # The AI-extracted structured data is in the `structured_data` attribute
        structured_data = getattr(doc_details, 'structured_data', {})
        if not structured_data:
            print("❌ CRITICAL: No 'structured_data' found. AI extraction rules may have failed.")
            return False, documents

        print("✅ Found 'structured_data' attribute.")
        
        # Check for the main 'ECSSStandard' entity
        standard_entity = structured_data.get('ECSSStandard', [{}])[0]
        if not standard_entity:
            print("❌ CRITICAL: 'ECSSStandard' entity not found in structured data.")
            return False, documents
            
        branch = standard_entity.get('branch')
        discipline = standard_entity.get('discipline')
        
        print("\n📊 AI-Extracted 'ECSSStandard' Info:")
        print(f"   - Branch: {branch}")
        print(f"   - Discipline: {discipline}")
        print(f"   - Title: {standard_entity.get('title')}")

        if branch and discipline:
            print("✅ TEST 1 PASSED: Documents are ingested and AI metadata is present.")
            return True, documents
        else:
            print("❌ TEST 1 FAILED: Branch or Discipline metadata is missing from the AI extraction.")
            return False, documents

    except Exception as e:
        print(f"❌ An error occurred during Test 1: {e}")
        return False, None

def test_2_rebuild_knowledge_graphs(db, documents):
    """Test 2: Delete empty graphs and rebuild them correctly using AI-extracted data."""
    print("\n" + "="*50)
    print("✅ TEST 2: KNOWLEDGE GRAPH REBUILD")
    print("="*50)

    try:
        # Step 1: Delete existing (likely empty) graphs
        print("🧹 Deleting existing graphs...")
        existing_graphs = db.list_graphs()
        for graph in existing_graphs:
            db.delete_graph(graph.name)
            print(f"   - Deleted graph: {graph.name}")
        print(f"✅ Deleted {len(existing_graphs)} graphs.")

        # Step 2: Rebuild graphs for each branch correctly
        branches = ['E', 'M', 'P', 'Q']
        graph_creation_prompts = create_ecss_graph_prompts()
        
        for branch in branches:
            graph_name = f"ecss_{branch.lower()}_branch_enhanced"
            print(f"\n🏗️  Building graph for Branch '{branch}'...")

            # THIS IS THE FIX: Filter documents based on AI-extracted structured_data
            # We look for documents where the 'ECSSStandard' entity has the correct branch.
            filter_query = {
                "structured_data.ECSSStandard.branch": branch
            }
            
            graph = db.create_graph(
                graph_name=graph_name,
                document_ids=None, # Let the filter do the work
                filters=filter_query,
                prompt_override=graph_creation_prompts
            )

            # Give it a moment to build
            time.sleep(5)
            
            # Verify the new graph
            graph_details = db.get_graph(graph_name)
            num_entities = len(getattr(graph_details, 'entities', []))
            num_rels = len(getattr(graph_details, 'relationships', []))

            print(f"   - Graph '{graph_name}' created.")
            print(f"   - Entities: {num_entities}")
            print(f"   - Relationships: {num_rels}")

            if num_entities == 0:
                print(f"⚠️  WARNING: Graph for branch '{branch}' is still empty. Check document filters.")

        print("\n✅ TEST 2 COMPLETED: Graph rebuild process finished.")
        return True

    except Exception as e:
        print(f"❌ An error occurred during Test 2: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3_validate_graphs(db):
    """Test 3: Validate that the rebuilt graphs are not empty."""
    print("\n" + "="*50)
    print("✅ TEST 3: VALIDATE REBUILT GRAPHS")
    print("="*50)

    try:
        graphs = db.list_graphs()
        if not graphs:
            print("❌ No graphs found after rebuild.")
            return False

        total_entities = 0
        for graph in graphs:
            details = db.get_graph(graph.name)
            num_entities = len(getattr(details, 'entities', []))
            total_entities += num_entities
            print(f"   - Graph '{graph.name}': {num_entities} entities")

        if total_entities > 0:
            print("✅ TEST 3 PASSED: Knowledge graphs are populated.")
            return True
        else:
            print("❌ TEST 3 FAILED: All knowledge graphs are still empty.")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred during Test 3: {e}")
        return False

def test_4_final_search_test(db):
    """Test 4: Run a final search query against the new graph."""
    print("\n" + "="*50)
    print("✅ TEST 4: FINAL SEARCH TEST")
    print("="*50)

    try:
        query = "What are the requirements for software development in the E branch?"
        print(f"❓ Query: \"{query}\"")

        # Query the engineering branch graph
        response = db.query(query, graph_name="ecss_e_branch_enhanced")
        
        if response and response.completion:
            print("✅ TEST 4 PASSED: Search query returned a valid response.")
            print("\nResponse Snippet:")
            print(response.completion[:300] + "...")
            return True
        else:
            print("❌ TEST 4 FAILED: Search query did not return a valid response.")
            return False

    except Exception as e:
        print(f"❌ An error occurred during Test 4: {e}")
        return False

def main():
    """Run all post-ingestion tests."""
    db = get_db_connection()
    if not db:
        return

    # Run tests in sequence
    test_1_ok, documents = test_1_document_ingestion_status(db)
    if not test_1_ok:
        print("\n🚫 Aborting due to failure in Test 1.")
        return

    test_2_ok = test_2_rebuild_knowledge_graphs(db, documents)
    if not test_2_ok:
        print("\n🚫 Aborting due to failure in Test 2.")
        return
        
    test_3_ok = test_3_validate_graphs(db)
    if not test_3_ok:
        print("\n🚫 Aborting due to failure in Test 3.")
        return

    test_4_ok = test_4_final_search_test(db)
    if not test_4_ok:
        print("\n🚫 Aborting due to failure in Test 4.")
        return

    print("\n" + "="*50)
    print("🎉 ALL POST-INGESTION TESTS PASSED! 🎉")
    print("✅ System is fully operational.")
    print("="*50)

if __name__ == "__main__":
    main() 

import os
import sys
import time

# Load environment variables
try:
        except ImportError:
    pass

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.ecss_graph_prompts import create_ecss_graph_prompts

def get_db_connection():
    """Establishes and returns a Morphik DB connection."""
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI environment variable not set.")
        return None
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully.")
        return db
    except Exception as e:
        print(f"❌ Morphik connection failed: {e}")
        return None

def test_1_document_ingestion_status(db):
    """Test 1: Check if documents were ingested and inspect their AI-extracted data."""
    print("\n" + "="*50)
    print("✅ TEST 1: DOCUMENT INGESTION & AI METADATA STATUS")
    print("="*50)
    
    try:
        documents = db.list_documents()
        print(f"📄 Found {len(documents)} documents.")
        if not documents:
            print("❌ No documents found. Please run ingestion first.")
            return False, None

        # Inspect the first document
        doc_to_inspect = documents[0]
        doc_id = getattr(doc_to_inspect, 'external_id', 'N/A')
        print(f"\n🔬 Inspecting first document (ID: {doc_id})...")
        
        doc_details = db.get_document(doc_id)
        
        # The AI-extracted structured data is in the `structured_data` attribute
        structured_data = getattr(doc_details, 'structured_data', {})
        if not structured_data:
            print("❌ CRITICAL: No 'structured_data' found. AI extraction rules may have failed.")
            return False, documents

        print("✅ Found 'structured_data' attribute.")
        
        # Check for the main 'ECSSStandard' entity
        standard_entity = structured_data.get('ECSSStandard', [{}])[0]
        if not standard_entity:
            print("❌ CRITICAL: 'ECSSStandard' entity not found in structured data.")
            return False, documents
            
        branch = standard_entity.get('branch')
        discipline = standard_entity.get('discipline')
        
        print("\n📊 AI-Extracted 'ECSSStandard' Info:")
        print(f"   - Branch: {branch}")
        print(f"   - Discipline: {discipline}")
        print(f"   - Title: {standard_entity.get('title')}")

        if branch and discipline:
            print("✅ TEST 1 PASSED: Documents are ingested and AI metadata is present.")
            return True, documents
        else:
            print("❌ TEST 1 FAILED: Branch or Discipline metadata is missing from the AI extraction.")
            return False, documents

    except Exception as e:
        print(f"❌ An error occurred during Test 1: {e}")
        return False, None

def test_2_rebuild_knowledge_graphs(db, documents):
    """Test 2: Delete empty graphs and rebuild them correctly using AI-extracted data."""
    print("\n" + "="*50)
    print("✅ TEST 2: KNOWLEDGE GRAPH REBUILD")
    print("="*50)

    try:
        # Step 1: Delete existing (likely empty) graphs
        print("🧹 Deleting existing graphs...")
        existing_graphs = db.list_graphs()
        for graph in existing_graphs:
            db.delete_graph(graph.name)
            print(f"   - Deleted graph: {graph.name}")
        print(f"✅ Deleted {len(existing_graphs)} graphs.")

        # Step 2: Rebuild graphs for each branch correctly
        branches = ['E', 'M', 'P', 'Q']
        graph_creation_prompts = create_ecss_graph_prompts()
        
        for branch in branches:
            graph_name = f"ecss_{branch.lower()}_branch_enhanced"
            print(f"\n🏗️  Building graph for Branch '{branch}'...")

            # THIS IS THE FIX: Filter documents based on AI-extracted structured_data
            # We look for documents where the 'ECSSStandard' entity has the correct branch.
            filter_query = {
                "structured_data.ECSSStandard.branch": branch
            }
            
            graph = db.create_graph(
                graph_name=graph_name,
                document_ids=None, # Let the filter do the work
                filters=filter_query,
                prompt_override=graph_creation_prompts
            )

            # Give it a moment to build
            time.sleep(5)
            
            # Verify the new graph
            graph_details = db.get_graph(graph_name)
            num_entities = len(getattr(graph_details, 'entities', []))
            num_rels = len(getattr(graph_details, 'relationships', []))

            print(f"   - Graph '{graph_name}' created.")
            print(f"   - Entities: {num_entities}")
            print(f"   - Relationships: {num_rels}")

            if num_entities == 0:
                print(f"⚠️  WARNING: Graph for branch '{branch}' is still empty. Check document filters.")

        print("\n✅ TEST 2 COMPLETED: Graph rebuild process finished.")
        return True

    except Exception as e:
        print(f"❌ An error occurred during Test 2: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3_validate_graphs(db):
    """Test 3: Validate that the rebuilt graphs are not empty."""
    print("\n" + "="*50)
    print("✅ TEST 3: VALIDATE REBUILT GRAPHS")
    print("="*50)

    try:
        graphs = db.list_graphs()
        if not graphs:
            print("❌ No graphs found after rebuild.")
            return False

        total_entities = 0
        for graph in graphs:
            details = db.get_graph(graph.name)
            num_entities = len(getattr(details, 'entities', []))
            total_entities += num_entities
            print(f"   - Graph '{graph.name}': {num_entities} entities")

        if total_entities > 0:
            print("✅ TEST 3 PASSED: Knowledge graphs are populated.")
            return True
        else:
            print("❌ TEST 3 FAILED: All knowledge graphs are still empty.")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred during Test 3: {e}")
        return False

def test_4_final_search_test(db):
    """Test 4: Run a final search query against the new graph."""
    print("\n" + "="*50)
    print("✅ TEST 4: FINAL SEARCH TEST")
    print("="*50)

    try:
        query = "What are the requirements for software development in the E branch?"
        print(f"❓ Query: \"{query}\"")

        # Query the engineering branch graph
        response = db.query(query, graph_name="ecss_e_branch_enhanced")
        
        if response and response.completion:
            print("✅ TEST 4 PASSED: Search query returned a valid response.")
            print("\nResponse Snippet:")
            print(response.completion[:300] + "...")
            return True
        else:
            print("❌ TEST 4 FAILED: Search query did not return a valid response.")
            return False

    except Exception as e:
        print(f"❌ An error occurred during Test 4: {e}")
        return False

def main():
    """Run all post-ingestion tests."""
    db = get_db_connection()
    if not db:
        return

    # Run tests in sequence
    test_1_ok, documents = test_1_document_ingestion_status(db)
    if not test_1_ok:
        print("\n🚫 Aborting due to failure in Test 1.")
        return

    test_2_ok = test_2_rebuild_knowledge_graphs(db, documents)
    if not test_2_ok:
        print("\n🚫 Aborting due to failure in Test 2.")
        return
        
    test_3_ok = test_3_validate_graphs(db)
    if not test_3_ok:
        print("\n🚫 Aborting due to failure in Test 3.")
        return

    test_4_ok = test_4_final_search_test(db)
    if not test_4_ok:
        print("\n🚫 Aborting due to failure in Test 4.")
        return

    print("\n" + "="*50)
    print("🎉 ALL POST-INGESTION TESTS PASSED! 🎉")
    print("✅ System is fully operational.")
    print("="*50)

if __name__ == "__main__":
    main() 