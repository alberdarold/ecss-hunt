"""
Test script for the optimized ECSS implementation
Tests focused graphs, adaptive query settings, and incremental updates
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script for the optimized ECSS implementation
Tests focused graphs, adaptive query settings, and incremental updates
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))



import os
import sys
import requests
import json
from core.optimized_graph_strategy import OptimizedECSSGraphManager

# Load environment variables

def test_optimized_graph_manager():
    """Test the OptimizedECSSGraphManager functionality."""
    print("🧪 Testing OptimizedECSSGraphManager...")
    
    # Initialize graph manager
    morphik_uri = os.getenv("MORPHIK_URI")
    graph_manager = OptimizedECSSGraphManager(morphik_uri)
    
    # Test 1: Query complexity detection
    print("\n1. Testing query complexity detection:")
    
    simple_queries = [
        "What is ECSS?",
        "Define quality assurance",
        "List requirements"
    ]
    
    complex_queries = [
        "What is the relationship between quality and engineering standards?",
        "Compare different ECSS branches",
        "How do various standards interact with each other?"
    ]
    
    for query in simple_queries:
        is_complex = graph_manager._is_complex_query(query)
        print(f"  '{query}' -> Complex: {is_complex}")
    
    for query in complex_queries:
        is_complex = graph_manager._is_complex_query(query)
        print(f"  '{query}' -> Complex: {is_complex}")
    
    # Test 2: Graph statistics
    print("\n2. Testing graph statistics:")
    try:
        stats = graph_manager.get_graph_statistics()
        for branch, stat in stats.items():
            if 'error' not in stat:
                print(f"  {branch}: {stat['entities']} entities, {stat['relationships']} relationships")
            else:
                print(f"  {branch}: Error - {stat['error']}")
    except Exception as e:
        print(f"  Error getting stats: {e}")
    
    print("✅ OptimizedECSSGraphManager tests completed")

def test_api_endpoints():
    """Test the updated API endpoints."""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n1. Testing health check:")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data.get('status')}")
            print(f"  Morphik connected: {data.get('morphik_connected')}")
            print(f"  Graph manager available: {data.get('graph_manager_available')}")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 2: Graph statistics
    print("\n2. Testing graph statistics:")
    try:
        response = requests.get(f"{base_url}/api/graph/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total graphs: {data.get('total_graphs')}")
            graphs = data.get('graphs', {})
            for branch, stats in graphs.items():
                if 'error' not in stats:
                    print(f"  {branch}: {stats.get('entities', 0)} entities")
                else:
                    print(f"  {branch}: Error - {stats['error']}")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 3: Adaptive search queries
    print("\n3. Testing adaptive search queries:")
    
    test_queries = [
        ("Simple query", "What is ECSS?"),
        ("Complex query", "What is the relationship between quality and engineering standards?"),
        ("Branch-specific query", "What are quality requirements?", "Q")
    ]
    
    for query_name, query, *args in test_queries:
        branch = args[0] if args else None
        print(f"\n  Testing: {query_name}")
        print(f"  Query: '{query}'")
        if branch:
            print(f"  Branch: {branch}")
        
        try:
            params = {'q': query}
            if branch:
                params['branch'] = branch
            
            response = requests.get(f"{base_url}/api/search", params=params)
            if response.status_code == 200:
                data = response.json()
                results_count = data.get('total', 0)
                query_settings = data.get('query_settings', {})
                
                print(f"    Results: {results_count}")
                print(f"    Hop depth: {query_settings.get('hop_depth', 'N/A')}")
                print(f"    K: {query_settings.get('k', 'N/A')}")
                print(f"    Reranking: {query_settings.get('use_reranking', 'N/A')}")
                print(f"    Graph: {query_settings.get('graph_name', 'N/A')}")
            else:
                print(f"    Error: {response.status_code}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print("✅ API endpoint tests completed")

def test_entity_specific_searches():
    """Test entity-specific search endpoints."""
    print("\n🔍 Testing entity-specific searches...")
    
    base_url = "http://localhost:5000"
    
    test_searches = [
        ("sections", "quality management"),
        ("definitions", "quality assurance"),
        ("tables", "requirements"),
        ("images", "diagrams")
    ]
    
    for endpoint, query in test_searches:
        print(f"\n  Testing {endpoint} search:")
        print(f"  Query: '{query}'")
        
        try:
            response = requests.get(f"{base_url}/api/search/{endpoint}", params={'q': query})
            if response.status_code == 200:
                data = response.json()
                results_count = data.get('total', 0)
                print(f"    Results: {results_count}")
                
                # Show first result if available
                results = data.get('results', [])
                if results:
                    first_result = results[0]
                    content = first_result.get('content', '')
                    # Truncate content for display
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"    First result preview: {preview}")
            else:
                print(f"    Error: {response.status_code}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print("✅ Entity-specific search tests completed")

def test_document_listing():
    """Test document listing functionality."""
    print("\n📚 Testing document listing...")
    
    base_url = "http://localhost:5000"
    
    try:
        response = requests.get(f"{base_url}/api/documents")
        if response.status_code == 200:
            data = response.json()
            documents = data.get('documents', [])
            total = data.get('total', 0)
            
            print(f"  Total documents: {total}")
            
            # Show first few documents
            for i, doc in enumerate(documents[:3]):
                filename = doc.get('filename', 'Unknown')
                metadata = doc.get('metadata', {})
                branch = metadata.get('branch', 'Unknown')
                print(f"    {i+1}. {filename} (Branch: {branch})")
            
            if len(documents) > 3:
                print(f"    ... and {len(documents) - 3} more documents")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("✅ Document listing tests completed")

def main():
    """Run all tests."""
    print("🚀 ECSS Standards Navigator - Optimized Implementation Tests")
    print("=" * 60)
    
    # Test the optimized graph manager
    test_optimized_graph_manager()
    
    # Test API endpoints (only if server is running)
    print("\n" + "=" * 60)
    print("Note: API tests require the server to be running on localhost:5000")
    print("Run 'python api_server.py' in another terminal to test API endpoints")
    
    # Uncomment the following lines to test API endpoints when server is running
    # test_api_endpoints()
    # test_entity_specific_searches()
    # test_document_listing()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Start the API server: python api_server.py")
    print("2. Run ingestion with focused graphs: python ingest_documents.py")
    print("3. Test the frontend with the new optimized backend")

if __name__ == "__main__":
    main() 

# Add backend root to path



import os
import sys
import requests
import json
from core.optimized_graph_strategy import OptimizedECSSGraphManager

# Load environment variables

def test_optimized_graph_manager():
    """Test the OptimizedECSSGraphManager functionality."""
    print("🧪 Testing OptimizedECSSGraphManager...")
    
    # Initialize graph manager
    morphik_uri = os.getenv("MORPHIK_URI")
    graph_manager = OptimizedECSSGraphManager(morphik_uri)
    
    # Test 1: Query complexity detection
    print("\n1. Testing query complexity detection:")
    
    simple_queries = [
        "What is ECSS?",
        "Define quality assurance",
        "List requirements"
    ]
    
    complex_queries = [
        "What is the relationship between quality and engineering standards?",
        "Compare different ECSS branches",
        "How do various standards interact with each other?"
    ]
    
    for query in simple_queries:
        is_complex = graph_manager._is_complex_query(query)
        print(f"  '{query}' -> Complex: {is_complex}")
    
    for query in complex_queries:
        is_complex = graph_manager._is_complex_query(query)
        print(f"  '{query}' -> Complex: {is_complex}")
    
    # Test 2: Graph statistics
    print("\n2. Testing graph statistics:")
    try:
        stats = graph_manager.get_graph_statistics()
        for branch, stat in stats.items():
            if 'error' not in stat:
                print(f"  {branch}: {stat['entities']} entities, {stat['relationships']} relationships")
            else:
                print(f"  {branch}: Error - {stat['error']}")
    except Exception as e:
        print(f"  Error getting stats: {e}")
    
    print("✅ OptimizedECSSGraphManager tests completed")

def test_api_endpoints():
    """Test the updated API endpoints."""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n1. Testing health check:")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data.get('status')}")
            print(f"  Morphik connected: {data.get('morphik_connected')}")
            print(f"  Graph manager available: {data.get('graph_manager_available')}")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 2: Graph statistics
    print("\n2. Testing graph statistics:")
    try:
        response = requests.get(f"{base_url}/api/graph/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total graphs: {data.get('total_graphs')}")
            graphs = data.get('graphs', {})
            for branch, stats in graphs.items():
                if 'error' not in stats:
                    print(f"  {branch}: {stats.get('entities', 0)} entities")
                else:
                    print(f"  {branch}: Error - {stats['error']}")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 3: Adaptive search queries
    print("\n3. Testing adaptive search queries:")
    
    test_queries = [
        ("Simple query", "What is ECSS?"),
        ("Complex query", "What is the relationship between quality and engineering standards?"),
        ("Branch-specific query", "What are quality requirements?", "Q")
    ]
    
    for query_name, query, *args in test_queries:
        branch = args[0] if args else None
        print(f"\n  Testing: {query_name}")
        print(f"  Query: '{query}'")
        if branch:
            print(f"  Branch: {branch}")
        
        try:
            params = {'q': query}
            if branch:
                params['branch'] = branch
            
            response = requests.get(f"{base_url}/api/search", params=params)
            if response.status_code == 200:
                data = response.json()
                results_count = data.get('total', 0)
                query_settings = data.get('query_settings', {})
                
                print(f"    Results: {results_count}")
                print(f"    Hop depth: {query_settings.get('hop_depth', 'N/A')}")
                print(f"    K: {query_settings.get('k', 'N/A')}")
                print(f"    Reranking: {query_settings.get('use_reranking', 'N/A')}")
                print(f"    Graph: {query_settings.get('graph_name', 'N/A')}")
            else:
                print(f"    Error: {response.status_code}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print("✅ API endpoint tests completed")

def test_entity_specific_searches():
    """Test entity-specific search endpoints."""
    print("\n🔍 Testing entity-specific searches...")
    
    base_url = "http://localhost:5000"
    
    test_searches = [
        ("sections", "quality management"),
        ("definitions", "quality assurance"),
        ("tables", "requirements"),
        ("images", "diagrams")
    ]
    
    for endpoint, query in test_searches:
        print(f"\n  Testing {endpoint} search:")
        print(f"  Query: '{query}'")
        
        try:
            response = requests.get(f"{base_url}/api/search/{endpoint}", params={'q': query})
            if response.status_code == 200:
                data = response.json()
                results_count = data.get('total', 0)
                print(f"    Results: {results_count}")
                
                # Show first result if available
                results = data.get('results', [])
                if results:
                    first_result = results[0]
                    content = first_result.get('content', '')
                    # Truncate content for display
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"    First result preview: {preview}")
            else:
                print(f"    Error: {response.status_code}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print("✅ Entity-specific search tests completed")

def test_document_listing():
    """Test document listing functionality."""
    print("\n📚 Testing document listing...")
    
    base_url = "http://localhost:5000"
    
    try:
        response = requests.get(f"{base_url}/api/documents")
        if response.status_code == 200:
            data = response.json()
            documents = data.get('documents', [])
            total = data.get('total', 0)
            
            print(f"  Total documents: {total}")
            
            # Show first few documents
            for i, doc in enumerate(documents[:3]):
                filename = doc.get('filename', 'Unknown')
                metadata = doc.get('metadata', {})
                branch = metadata.get('branch', 'Unknown')
                print(f"    {i+1}. {filename} (Branch: {branch})")
            
            if len(documents) > 3:
                print(f"    ... and {len(documents) - 3} more documents")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("✅ Document listing tests completed")

def main():
    """Run all tests."""
    print("🚀 ECSS Standards Navigator - Optimized Implementation Tests")
    print("=" * 60)
    
    # Test the optimized graph manager
    test_optimized_graph_manager()
    
    # Test API endpoints (only if server is running)
    print("\n" + "=" * 60)
    print("Note: API tests require the server to be running on localhost:5000")
    print("Run 'python api_server.py' in another terminal to test API endpoints")
    
    # Uncomment the following lines to test API endpoints when server is running
    # test_api_endpoints()
    # test_entity_specific_searches()
    # test_document_listing()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Start the API server: python api_server.py")
    print("2. Run ingestion with focused graphs: python ingest_documents.py")
    print("3. Test the frontend with the new optimized backend")

if __name__ == "__main__":
    main() 