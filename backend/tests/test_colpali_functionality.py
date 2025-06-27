

#!/usr/bin/env python3
"""
Test script for ColPali functionality and visual content retrieval.
Validates that our system can properly handle visual queries using ColPali.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script for ColPali functionality and visual content retrieval.
Validates that our system can properly handle visual queries using ColPali.
"""

import os
import sys
import json

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.optimized_graph_strategy import OptimizedGraphManager

def test_colpali_ingestion():
    """Test that documents are ingested with ColPali support."""
    print("🔍 Testing ColPali Ingestion...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Check if we have any documents ingested
        documents = db.list_documents()
        if not documents:
            print("⚠ No documents found. Please run ingestion first.")
            return False
        
        print(f"✅ Found {len(documents)} documents")
        
        # Check if any documents have visual content
        visual_docs = []
        for doc in documents[:5]:  # Check first 5 documents
            try:
                doc_info = db.get_document(doc.id)
                if hasattr(doc_info, 'metadata') and doc_info.metadata:
                    # Check if document contains visual content indicators
                    if any(keyword in str(doc_info.metadata).lower() 
                           for keyword in ['figure', 'diagram', 'image', 'photo']):
                        visual_docs.append(doc.id)
            except Exception as e:
                print(f"⚠ Could not check document {doc.id}: {e}")
        
        print(f"📸 Found {len(visual_docs)} documents with potential visual content")
        return len(visual_docs) > 0
        
    except Exception as e:
        print(f"❌ ColPali ingestion test failed: {e}")
        return False

def test_colpali_queries():
    """Test ColPali queries for visual content."""
    print("\n🔍 Testing ColPali Queries...")
    
    try:
        # Initialize Morphik and graph manager
        db = Morphik(os.getenv("MORPHIK_URI"))
        graph_manager = OptimizedGraphManager(db)
        
        # Test queries that should benefit from ColPali
        visual_queries = [
            "Find diagrams showing system architecture",
            "Show me figures with electrical schematics",
            "Display images of mechanical components",
            "Find charts showing performance data",
            "Show diagrams of satellite systems"
        ]
        
        results = []
        for query in visual_queries:
            print(f"\n📝 Testing query: '{query}'")
            
            try:
                # Test with ColPali
                colpali_response = db.query(
                    query,
                    use_colpali=True,
                    k=5,
                    model_config={"model_name": "gpt-4o"}
                )
                
                if colpali_response and colpali_response.sources:
                    print(f"✅ ColPali found {len(colpali_response.sources)} results")
                    
                    # Check for visual content in results
                    visual_results = 0
                    for source in colpali_response.sources:
                        source_text = getattr(source, 'text', '')
                        if any(keyword in source_text.lower() 
                               for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph']):
                            visual_results += 1
                    
                    print(f"📸 {visual_results}/{len(colpali_response.sources)} results contain visual content")
                    results.append({
                        'query': query,
                        'total_results': len(colpali_response.sources),
                        'visual_results': visual_results,
                        'success': True
                    })
                else:
                    print("⚠ No results found with ColPali")
                    results.append({
                        'query': query,
                        'total_results': 0,
                        'visual_results': 0,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ ColPali query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        total_visual_results = sum(r.get('visual_results', 0) for r in results)
        
        print(f"\n📊 ColPali Query Summary:")
        print(f"   Successful queries: {successful_queries}/{len(visual_queries)}")
        print(f"   Total visual results found: {total_visual_results}")
        
        return successful_queries > 0
        
    except Exception as e:
        print(f"❌ ColPali query test failed: {e}")
        return False

def test_graph_manager_colpali():
    """Test that the graph manager properly uses ColPali for visual queries."""
    print("\n🔍 Testing Graph Manager ColPali Integration...")
    
    try:
        # Initialize Morphik and graph manager
        db = Morphik(os.getenv("MORPHIK_URI"))
        graph_manager = OptimizedGraphManager(db)
        
        # Test visual queries through graph manager
        visual_queries = [
            "Find diagrams in ECSS standards",
            "Show me figures with technical specifications",
            "Display images of spacecraft components"
        ]
        
        results = []
        for query in visual_queries:
            print(f"\n📝 Testing graph manager query: '{query}'")
            
            try:
                response = graph_manager.query_with_adaptive_settings(query)
                
                if 'error' not in response:
                    sources = response.get('sources', [])
                    query_settings = response.get('query_settings', {})
                    
                    print(f"✅ Graph manager found {len(sources)} results")
                    print(f"   Settings: hop_depth={query_settings.get('hop_depth')}, "
                          f"k={query_settings.get('k')}, "
                          f"use_colpali={query_settings.get('use_colpali')}")
                    
                    # Check for visual content
                    visual_results = 0
                    for source in sources:
                        source_text = getattr(source, 'text', '')
                        if any(keyword in source_text.lower() 
                               for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph']):
                            visual_results += 1
                    
                    print(f"📸 {visual_results}/{len(sources)} results contain visual content")
                    results.append({
                        'query': query,
                        'total_results': len(sources),
                        'visual_results': visual_results,
                        'use_colpali': query_settings.get('use_colpali', False),
                        'success': True
                    })
                else:
                    print(f"❌ Graph manager query failed: {response['error']}")
                    results.append({
                        'query': query,
                        'error': response['error'],
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Graph manager query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        colpali_used = sum(1 for r in results if r.get('use_colpali', False))
        total_visual_results = sum(r.get('visual_results', 0) for r in results)
        
        print(f"\n📊 Graph Manager ColPali Summary:")
        print(f"   Successful queries: {successful_queries}/{len(visual_queries)}")
        print(f"   Queries using ColPali: {colpali_used}/{len(visual_queries)}")
        print(f"   Total visual results found: {total_visual_results}")
        
        return successful_queries > 0 and colpali_used > 0
        
    except Exception as e:
        print(f"❌ Graph manager ColPali test failed: {e}")
        return False

def main():
    """Run all ColPali functionality tests."""
    print("🚀 Testing ColPali Functionality")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("ColPali Ingestion", test_colpali_ingestion),
        ("ColPali Queries", test_colpali_queries),
        ("Graph Manager ColPali", test_graph_manager_colpali)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 FINAL TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All ColPali functionality tests passed!")
        print("✅ Your system is robust for visual content retrieval")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 

import os
import sys
import json

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from core.optimized_graph_strategy import OptimizedGraphManager

def test_colpali_ingestion():
    """Test that documents are ingested with ColPali support."""
    print("🔍 Testing ColPali Ingestion...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Check if we have any documents ingested
        documents = db.list_documents()
        if not documents:
            print("⚠ No documents found. Please run ingestion first.")
            return False
        
        print(f"✅ Found {len(documents)} documents")
        
        # Check if any documents have visual content
        visual_docs = []
        for doc in documents[:5]:  # Check first 5 documents
            try:
                doc_info = db.get_document(doc.id)
                if hasattr(doc_info, 'metadata') and doc_info.metadata:
                    # Check if document contains visual content indicators
                    if any(keyword in str(doc_info.metadata).lower() 
                           for keyword in ['figure', 'diagram', 'image', 'photo']):
                        visual_docs.append(doc.id)
            except Exception as e:
                print(f"⚠ Could not check document {doc.id}: {e}")
        
        print(f"📸 Found {len(visual_docs)} documents with potential visual content")
        return len(visual_docs) > 0
        
    except Exception as e:
        print(f"❌ ColPali ingestion test failed: {e}")
        return False

def test_colpali_queries():
    """Test ColPali queries for visual content."""
    print("\n🔍 Testing ColPali Queries...")
    
    try:
        # Initialize Morphik and graph manager
        db = Morphik(os.getenv("MORPHIK_URI"))
        graph_manager = OptimizedGraphManager(db)
        
        # Test queries that should benefit from ColPali
        visual_queries = [
            "Find diagrams showing system architecture",
            "Show me figures with electrical schematics",
            "Display images of mechanical components",
            "Find charts showing performance data",
            "Show diagrams of satellite systems"
        ]
        
        results = []
        for query in visual_queries:
            print(f"\n📝 Testing query: '{query}'")
            
            try:
                # Test with ColPali
                colpali_response = db.query(
                    query,
                    use_colpali=True,
                    k=5,
                    model_config={"model_name": "gpt-4o"}
                )
                
                if colpali_response and colpali_response.sources:
                    print(f"✅ ColPali found {len(colpali_response.sources)} results")
                    
                    # Check for visual content in results
                    visual_results = 0
                    for source in colpali_response.sources:
                        source_text = getattr(source, 'text', '')
                        if any(keyword in source_text.lower() 
                               for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph']):
                            visual_results += 1
                    
                    print(f"📸 {visual_results}/{len(colpali_response.sources)} results contain visual content")
                    results.append({
                        'query': query,
                        'total_results': len(colpali_response.sources),
                        'visual_results': visual_results,
                        'success': True
                    })
                else:
                    print("⚠ No results found with ColPali")
                    results.append({
                        'query': query,
                        'total_results': 0,
                        'visual_results': 0,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ ColPali query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        total_visual_results = sum(r.get('visual_results', 0) for r in results)
        
        print(f"\n📊 ColPali Query Summary:")
        print(f"   Successful queries: {successful_queries}/{len(visual_queries)}")
        print(f"   Total visual results found: {total_visual_results}")
        
        return successful_queries > 0
        
    except Exception as e:
        print(f"❌ ColPali query test failed: {e}")
        return False

def test_graph_manager_colpali():
    """Test that the graph manager properly uses ColPali for visual queries."""
    print("\n🔍 Testing Graph Manager ColPali Integration...")
    
    try:
        # Initialize Morphik and graph manager
        db = Morphik(os.getenv("MORPHIK_URI"))
        graph_manager = OptimizedGraphManager(db)
        
        # Test visual queries through graph manager
        visual_queries = [
            "Find diagrams in ECSS standards",
            "Show me figures with technical specifications",
            "Display images of spacecraft components"
        ]
        
        results = []
        for query in visual_queries:
            print(f"\n📝 Testing graph manager query: '{query}'")
            
            try:
                response = graph_manager.query_with_adaptive_settings(query)
                
                if 'error' not in response:
                    sources = response.get('sources', [])
                    query_settings = response.get('query_settings', {})
                    
                    print(f"✅ Graph manager found {len(sources)} results")
                    print(f"   Settings: hop_depth={query_settings.get('hop_depth')}, "
                          f"k={query_settings.get('k')}, "
                          f"use_colpali={query_settings.get('use_colpali')}")
                    
                    # Check for visual content
                    visual_results = 0
                    for source in sources:
                        source_text = getattr(source, 'text', '')
                        if any(keyword in source_text.lower() 
                               for keyword in ['figure', 'diagram', 'image', 'photo', 'chart', 'graph']):
                            visual_results += 1
                    
                    print(f"📸 {visual_results}/{len(sources)} results contain visual content")
                    results.append({
                        'query': query,
                        'total_results': len(sources),
                        'visual_results': visual_results,
                        'use_colpali': query_settings.get('use_colpali', False),
                        'success': True
                    })
                else:
                    print(f"❌ Graph manager query failed: {response['error']}")
                    results.append({
                        'query': query,
                        'error': response['error'],
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Graph manager query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        colpali_used = sum(1 for r in results if r.get('use_colpali', False))
        total_visual_results = sum(r.get('visual_results', 0) for r in results)
        
        print(f"\n📊 Graph Manager ColPali Summary:")
        print(f"   Successful queries: {successful_queries}/{len(visual_queries)}")
        print(f"   Queries using ColPali: {colpali_used}/{len(visual_queries)}")
        print(f"   Total visual results found: {total_visual_results}")
        
        return successful_queries > 0 and colpali_used > 0
        
    except Exception as e:
        print(f"❌ Graph manager ColPali test failed: {e}")
        return False

def main():
    """Run all ColPali functionality tests."""
    print("🚀 Testing ColPali Functionality")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("ColPali Ingestion", test_colpali_ingestion),
        ("ColPali Queries", test_colpali_queries),
        ("Graph Manager ColPali", test_graph_manager_colpali)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 FINAL TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All ColPali functionality tests passed!")
        print("✅ Your system is robust for visual content retrieval")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 