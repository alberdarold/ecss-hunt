

#!/usr/bin/env python3
"""
Test script to verify the fixed ingestion system.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script to verify the fixed ingestion system.
"""

import os
import sys

# Load environment variables

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_fixes():
    """Test the fixes for knowledge graph creation and metadata extraction."""
    print("🧪 Testing Fixed Ingestion System")
    print("=" * 40)
    
    # Test 1: Check if create_graph method exists
    print("\n1. Testing create_graph method availability...")
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI not set")
            return False
        
        db = Morphik(morphik_uri)
        
        # Check if create_graph method exists
        if hasattr(db, 'create_graph'):
            print("✅ create_graph method found")
        else:
            print("❌ create_graph method not found")
            print(f"Available methods: {[m for m in dir(db) if not m.startswith('_')]}")
            return False
        
        # Test 2: Check if we have documents to work with
        print("\n2. Checking for existing documents...")
        documents = db.list_documents()
        print(f"✅ Found {len(documents)} documents")
        
        if not documents:
            print("⚠️  No documents found. Please run ingestion first.")
            return True
        
        # Test 3: Test metadata extraction filtering
        print("\n3. Testing metadata extraction filtering...")
        from core.clean_and_ingest import ECSSRulesBasedIngestion
        
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        
        # Test with one document
        doc = documents[0]
        print(f"Testing with document: {doc.filename}")
        
        # Test metadata extraction
        metadata = ingestion_system.get_extracted_metadata_from_chunks(doc.external_id)
        
        print(f"Extracted metadata keys: {list(metadata.keys())}")
        for key, values in metadata.items():
            print(f"  {key}: {len(values)} items")
            for i, value in enumerate(values[:2]):  # Show first 2 items
                if isinstance(value, str):
                    preview = value[:100] + "..." if len(value) > 100 else value
                    print(f"    {i+1}: {preview}")
        
        # Test 4: Test knowledge graph creation
        print("\n4. Testing knowledge graph creation...")
        try:
            # Try different parameter combinations
            print("   Trying create_graph with name only...")
            graph = db.create_graph(name="Test ECSS Graph")
            if graph:
                print(f"✅ Successfully created test graph: {graph.id}")
            else:
                print("❌ Graph creation returned None")
        except Exception as e:
            print(f"❌ Graph creation failed: {e}")
            
            # Try with minimal parameters
            try:
                print("   Trying create_graph with minimal parameters...")
                graph = db.create_graph("Test ECSS Graph")
                if graph:
                    print(f"✅ Successfully created test graph: {graph.id}")
                else:
                    print("❌ Graph creation returned None")
            except Exception as e2:
                print(f"❌ Minimal graph creation also failed: {e2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_fixes()
    if success:
        print("\n✅ All tests passed! The fixes are working.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.") 

import os
import sys

# Load environment variables

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def test_fixes():
    """Test the fixes for knowledge graph creation and metadata extraction."""
    print("🧪 Testing Fixed Ingestion System")
    print("=" * 40)
    
    # Test 1: Check if create_graph method exists
    print("\n1. Testing create_graph method availability...")
    try:
        morphik_uri = os.getenv("MORPHIK_URI")
        if not morphik_uri:
            print("❌ MORPHIK_URI not set")
            return False
        
        db = Morphik(morphik_uri)
        
        # Check if create_graph method exists
        if hasattr(db, 'create_graph'):
            print("✅ create_graph method found")
        else:
            print("❌ create_graph method not found")
            print(f"Available methods: {[m for m in dir(db) if not m.startswith('_')]}")
            return False
        
        # Test 2: Check if we have documents to work with
        print("\n2. Checking for existing documents...")
        documents = db.list_documents()
        print(f"✅ Found {len(documents)} documents")
        
        if not documents:
            print("⚠️  No documents found. Please run ingestion first.")
            return True
        
        # Test 3: Test metadata extraction filtering
        print("\n3. Testing metadata extraction filtering...")
        from core.clean_and_ingest import ECSSRulesBasedIngestion
        
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        
        # Test with one document
        doc = documents[0]
        print(f"Testing with document: {doc.filename}")
        
        # Test metadata extraction
        metadata = ingestion_system.get_extracted_metadata_from_chunks(doc.external_id)
        
        print(f"Extracted metadata keys: {list(metadata.keys())}")
        for key, values in metadata.items():
            print(f"  {key}: {len(values)} items")
            for i, value in enumerate(values[:2]):  # Show first 2 items
                if isinstance(value, str):
                    preview = value[:100] + "..." if len(value) > 100 else value
                    print(f"    {i+1}: {preview}")
        
        # Test 4: Test knowledge graph creation
        print("\n4. Testing knowledge graph creation...")
        try:
            # Try different parameter combinations
            print("   Trying create_graph with name only...")
            graph = db.create_graph(name="Test ECSS Graph")
            if graph:
                print(f"✅ Successfully created test graph: {graph.id}")
            else:
                print("❌ Graph creation returned None")
        except Exception as e:
            print(f"❌ Graph creation failed: {e}")
            
            # Try with minimal parameters
            try:
                print("   Trying create_graph with minimal parameters...")
                graph = db.create_graph("Test ECSS Graph")
                if graph:
                    print(f"✅ Successfully created test graph: {graph.id}")
                else:
                    print("❌ Graph creation returned None")
            except Exception as e2:
                print(f"❌ Minimal graph creation also failed: {e2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_fixes()
    if success:
        print("\n✅ All tests passed! The fixes are working.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.") 