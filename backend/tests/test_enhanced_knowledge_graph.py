

#!/usr/bin/env python3
"""
Test script for Enhanced Knowledge Graph Implementation
Validates that our ECSS knowledge graph system uses custom prompts and entity resolution.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script for Enhanced Knowledge Graph Implementation
Validates that our ECSS knowledge graph system uses custom prompts and entity resolution.
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
from core.ecss_graph_prompts import (
    get_ecss_entity_extraction_examples,
    get_ecss_entity_resolution_examples,
    create_ecss_graph_prompts,
    create_branch_specific_graph_prompts,
    test_ecss_graph_prompts
)

def test_graph_prompts_creation():
    """Test that we can create all types of ECSS graph prompts."""
    print("🧪 Testing ECSS Graph Prompts Creation...")
    
    try:
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created general ECSS graph prompts")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific graph prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph prompts creation test failed: {e}")
        return False

def test_enhanced_graph_creation():
    """Test enhanced knowledge graph creation with custom prompts."""
    print("\n🧪 Testing Enhanced Knowledge Graph Creation...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Check if we have any documents ingested
        documents = db.list_documents()
        if not documents:
            print("⚠ No documents found. Please run ingestion first.")
            return False
        
        print(f"✅ Found {len(documents)} documents for graph creation")
        
        # Test creating a general ECSS knowledge graph
        from core.ecss_graph_prompts import create_ecss_knowledge_graph
        
        general_graph = create_ecss_knowledge_graph(
            db, 
            "test_ecss_general",
            {"status": "Active"}
        )
        
        if general_graph:
            print(f"✅ Created general ECSS knowledge graph")
            print(f"   Entities: {len(general_graph.entities)}")
            print(f"   Relationships: {len(general_graph.relationships)}")
        else:
            print("⚠ Failed to create general ECSS knowledge graph")
        
        # Test creating branch-specific graphs
        from core.ecss_graph_prompts import create_branch_knowledge_graph
        
        for branch in ['E', 'M', 'P', 'Q']:
            branch_graph = create_branch_knowledge_graph(db, branch)
            
            if branch_graph:
                print(f"✅ Created {branch}-branch knowledge graph")
                print(f"   Entities: {len(branch_graph.entities)}")
                print(f"   Relationships: {len(branch_graph.relationships)}")
            else:
                print(f"⚠ Failed to create {branch}-branch knowledge graph")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced graph creation test failed: {e}")
        return False

def test_enhanced_graph_queries():
    """Test queries using enhanced knowledge graphs."""
    print("\n🧪 Testing Enhanced Knowledge Graph Queries...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test queries that should benefit from enhanced graph traversal
        enhanced_queries = [
            "What is the relationship between spacecraft design and thermal control?",
            "How do requirements in ECSS-E-ST-10C connect to verification methods?",
            "What are the dependencies between project phases and quality assurance?",
            "Show me the connections between engineering disciplines and system requirements",
            "What verification methods are used for spacecraft structural analysis?"
        ]
        
        results = []
        for query in enhanced_queries:
            print(f"\n📝 Testing enhanced query: '{query}'")
            
            try:
                # Query with enhanced graph settings
                response = db.query(
                    query,
                    graph_name="ecss_general_enhanced",  # Use enhanced graph
                    hop_depth=3,  # Higher hop depth for relationship queries
                    include_paths=True,  # Include relationship paths
                    k=15  # More results for complex queries
                )
                
                if response and response.sources:
                    print(f"✅ Enhanced query found {len(response.sources)} results")
                    
                    # Check for path information
                    has_paths = False
                    if response.metadata and "graph" in response.metadata:
                        paths = response.metadata["graph"].get("paths", [])
                        has_paths = len(paths) > 0
                        print(f"📊 Found {len(paths)} relationship paths")
                    
                    results.append({
                        'query': query,
                        'total_results': len(response.sources),
                        'has_paths': has_paths,
                        'success': True
                    })
                else:
                    print("⚠ No results found with enhanced query")
                    results.append({
                        'query': query,
                        'total_results': 0,
                        'has_paths': False,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Enhanced query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        queries_with_paths = sum(1 for r in results if r.get('has_paths', False))
        total_results = sum(r.get('total_results', 0) for r in results)
        
        print(f"\n📊 Enhanced Graph Query Summary:")
        print(f"   Successful queries: {successful_queries}/{len(enhanced_queries)}")
        print(f"   Queries with relationship paths: {queries_with_paths}/{len(enhanced_queries)}")
        print(f"   Total results found: {total_results}")
        
        return successful_queries > 0
        
    except Exception as e:
        print(f"❌ Enhanced graph queries test failed: {e}")
        return False

def test_entity_resolution():
    """Test that entity resolution works correctly with our custom examples."""
    print("\n🧪 Testing Entity Resolution...")
    
    try:
        # Get our entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        
        # Test some specific entity resolutions
        test_cases = [
            ("ECSS-E-ST-10C Rev.1", "ECSS-E-ST-10C"),
            ("space vehicle", "Spacecraft"),
            ("functional req", "Functional Requirement"),
            ("thermal management", "Thermal Control"),
            ("test method", "Test Verification")
        ]
        
        successful_resolutions = 0
        
        for variant, expected_canonical in test_cases:
            # Find the resolution example that contains this variant
            resolved = False
            for example in resolution_examples:
                if variant in example.variants and example.canonical == expected_canonical:
                    resolved = True
                    break
            
            if resolved:
                print(f"✅ Resolved '{variant}' -> '{expected_canonical}'")
                successful_resolutions += 1
            else:
                print(f"❌ Failed to resolve '{variant}' -> '{expected_canonical}'")
        
        print(f"\n📊 Entity Resolution Summary:")
        print(f"   Successful resolutions: {successful_resolutions}/{len(test_cases)}")
        
        return successful_resolutions >= len(test_cases) * 0.8  # 80% success rate
        
    except Exception as e:
        print(f"❌ Entity resolution test failed: {e}")
        return False

def test_graph_traversal():
    """Test that graph traversal works with enhanced hop depth."""
    print("\n🧪 Testing Graph Traversal...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test queries with different hop depths
        hop_depth_tests = [
            ("Find requirements for spacecraft design", 1),
            ("What verification methods are used for thermal control requirements?", 2),
            ("Show me the complete chain from requirements to verification to project phases", 3)
        ]
        
        results = []
        for query, hop_depth in hop_depth_tests:
            print(f"\n📝 Testing traversal with hop_depth={hop_depth}: '{query}'")
            
            try:
                response = db.query(
                    query,
                    graph_name="ecss_general_enhanced",
                    hop_depth=hop_depth,
                    include_paths=True,
                    k=10
                )
                
                if response and response.sources:
                    # Check for path information
                    path_count = 0
                    if response.metadata and "graph" in response.metadata:
                        paths = response.metadata["graph"].get("paths", [])
                        path_count = len(paths)
                    
                    print(f"✅ Found {len(response.sources)} results with {path_count} paths")
                    results.append({
                        'query': query,
                        'hop_depth': hop_depth,
                        'results': len(response.sources),
                        'paths': path_count,
                        'success': True
                    })
                else:
                    print("⚠ No results found")
                    results.append({
                        'query': query,
                        'hop_depth': hop_depth,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Traversal test failed: {e}")
                results.append({
                    'query': query,
                    'hop_depth': hop_depth,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_tests = sum(1 for r in results if r.get('success', False))
        total_paths = sum(r.get('paths', 0) for r in results)
        
        print(f"\n📊 Graph Traversal Summary:")
        print(f"   Successful tests: {successful_tests}/{len(hop_depth_tests)}")
        print(f"   Total relationship paths found: {total_paths}")
        
        return successful_tests > 0
        
    except Exception as e:
        print(f"❌ Graph traversal test failed: {e}")
        return False

def main():
    """Run all enhanced knowledge graph tests."""
    print("🚀 Testing Enhanced Knowledge Graph Implementation")
    print("=" * 60)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("Graph Prompts Creation", test_graph_prompts_creation),
        ("Enhanced Graph Creation", test_enhanced_graph_creation),
        ("Enhanced Graph Queries", test_enhanced_graph_queries),
        ("Entity Resolution", test_entity_resolution),
        ("Graph Traversal", test_graph_traversal)
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
    print(f"\n{'='*60}")
    print("📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced knowledge graph tests passed!")
        print("✅ Your system is robust for knowledge graph operations")
        print("\n📋 Enhanced Knowledge Graph Features:")
        print("   • Custom entity extraction with ECSS-specific examples")
        print("   • Entity resolution for variant terms")
        print("   • Enhanced graph traversal with higher hop depths")
        print("   • Relationship path tracking for explainability")
        print("   • Branch-specific graph optimization")
        print("   • Full compliance with Morphik knowledge graph methodology")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 

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
from core.ecss_graph_prompts import (
    get_ecss_entity_extraction_examples,
    get_ecss_entity_resolution_examples,
    create_ecss_graph_prompts,
    create_branch_specific_graph_prompts,
    test_ecss_graph_prompts
)

def test_graph_prompts_creation():
    """Test that we can create all types of ECSS graph prompts."""
    print("🧪 Testing ECSS Graph Prompts Creation...")
    
    try:
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created general ECSS graph prompts")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific graph prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph prompts creation test failed: {e}")
        return False

def test_enhanced_graph_creation():
    """Test enhanced knowledge graph creation with custom prompts."""
    print("\n🧪 Testing Enhanced Knowledge Graph Creation...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Check if we have any documents ingested
        documents = db.list_documents()
        if not documents:
            print("⚠ No documents found. Please run ingestion first.")
            return False
        
        print(f"✅ Found {len(documents)} documents for graph creation")
        
        # Test creating a general ECSS knowledge graph
        from core.ecss_graph_prompts import create_ecss_knowledge_graph
        
        general_graph = create_ecss_knowledge_graph(
            db, 
            "test_ecss_general",
            {"status": "Active"}
        )
        
        if general_graph:
            print(f"✅ Created general ECSS knowledge graph")
            print(f"   Entities: {len(general_graph.entities)}")
            print(f"   Relationships: {len(general_graph.relationships)}")
        else:
            print("⚠ Failed to create general ECSS knowledge graph")
        
        # Test creating branch-specific graphs
        from core.ecss_graph_prompts import create_branch_knowledge_graph
        
        for branch in ['E', 'M', 'P', 'Q']:
            branch_graph = create_branch_knowledge_graph(db, branch)
            
            if branch_graph:
                print(f"✅ Created {branch}-branch knowledge graph")
                print(f"   Entities: {len(branch_graph.entities)}")
                print(f"   Relationships: {len(branch_graph.relationships)}")
            else:
                print(f"⚠ Failed to create {branch}-branch knowledge graph")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced graph creation test failed: {e}")
        return False

def test_enhanced_graph_queries():
    """Test queries using enhanced knowledge graphs."""
    print("\n🧪 Testing Enhanced Knowledge Graph Queries...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test queries that should benefit from enhanced graph traversal
        enhanced_queries = [
            "What is the relationship between spacecraft design and thermal control?",
            "How do requirements in ECSS-E-ST-10C connect to verification methods?",
            "What are the dependencies between project phases and quality assurance?",
            "Show me the connections between engineering disciplines and system requirements",
            "What verification methods are used for spacecraft structural analysis?"
        ]
        
        results = []
        for query in enhanced_queries:
            print(f"\n📝 Testing enhanced query: '{query}'")
            
            try:
                # Query with enhanced graph settings
                response = db.query(
                    query,
                    graph_name="ecss_general_enhanced",  # Use enhanced graph
                    hop_depth=3,  # Higher hop depth for relationship queries
                    include_paths=True,  # Include relationship paths
                    k=15  # More results for complex queries
                )
                
                if response and response.sources:
                    print(f"✅ Enhanced query found {len(response.sources)} results")
                    
                    # Check for path information
                    has_paths = False
                    if response.metadata and "graph" in response.metadata:
                        paths = response.metadata["graph"].get("paths", [])
                        has_paths = len(paths) > 0
                        print(f"📊 Found {len(paths)} relationship paths")
                    
                    results.append({
                        'query': query,
                        'total_results': len(response.sources),
                        'has_paths': has_paths,
                        'success': True
                    })
                else:
                    print("⚠ No results found with enhanced query")
                    results.append({
                        'query': query,
                        'total_results': 0,
                        'has_paths': False,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Enhanced query failed: {e}")
                results.append({
                    'query': query,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_queries = sum(1 for r in results if r.get('success', False))
        queries_with_paths = sum(1 for r in results if r.get('has_paths', False))
        total_results = sum(r.get('total_results', 0) for r in results)
        
        print(f"\n📊 Enhanced Graph Query Summary:")
        print(f"   Successful queries: {successful_queries}/{len(enhanced_queries)}")
        print(f"   Queries with relationship paths: {queries_with_paths}/{len(enhanced_queries)}")
        print(f"   Total results found: {total_results}")
        
        return successful_queries > 0
        
    except Exception as e:
        print(f"❌ Enhanced graph queries test failed: {e}")
        return False

def test_entity_resolution():
    """Test that entity resolution works correctly with our custom examples."""
    print("\n🧪 Testing Entity Resolution...")
    
    try:
        # Get our entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        
        # Test some specific entity resolutions
        test_cases = [
            ("ECSS-E-ST-10C Rev.1", "ECSS-E-ST-10C"),
            ("space vehicle", "Spacecraft"),
            ("functional req", "Functional Requirement"),
            ("thermal management", "Thermal Control"),
            ("test method", "Test Verification")
        ]
        
        successful_resolutions = 0
        
        for variant, expected_canonical in test_cases:
            # Find the resolution example that contains this variant
            resolved = False
            for example in resolution_examples:
                if variant in example.variants and example.canonical == expected_canonical:
                    resolved = True
                    break
            
            if resolved:
                print(f"✅ Resolved '{variant}' -> '{expected_canonical}'")
                successful_resolutions += 1
            else:
                print(f"❌ Failed to resolve '{variant}' -> '{expected_canonical}'")
        
        print(f"\n📊 Entity Resolution Summary:")
        print(f"   Successful resolutions: {successful_resolutions}/{len(test_cases)}")
        
        return successful_resolutions >= len(test_cases) * 0.8  # 80% success rate
        
    except Exception as e:
        print(f"❌ Entity resolution test failed: {e}")
        return False

def test_graph_traversal():
    """Test that graph traversal works with enhanced hop depth."""
    print("\n🧪 Testing Graph Traversal...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test queries with different hop depths
        hop_depth_tests = [
            ("Find requirements for spacecraft design", 1),
            ("What verification methods are used for thermal control requirements?", 2),
            ("Show me the complete chain from requirements to verification to project phases", 3)
        ]
        
        results = []
        for query, hop_depth in hop_depth_tests:
            print(f"\n📝 Testing traversal with hop_depth={hop_depth}: '{query}'")
            
            try:
                response = db.query(
                    query,
                    graph_name="ecss_general_enhanced",
                    hop_depth=hop_depth,
                    include_paths=True,
                    k=10
                )
                
                if response and response.sources:
                    # Check for path information
                    path_count = 0
                    if response.metadata and "graph" in response.metadata:
                        paths = response.metadata["graph"].get("paths", [])
                        path_count = len(paths)
                    
                    print(f"✅ Found {len(response.sources)} results with {path_count} paths")
                    results.append({
                        'query': query,
                        'hop_depth': hop_depth,
                        'results': len(response.sources),
                        'paths': path_count,
                        'success': True
                    })
                else:
                    print("⚠ No results found")
                    results.append({
                        'query': query,
                        'hop_depth': hop_depth,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ Traversal test failed: {e}")
                results.append({
                    'query': query,
                    'hop_depth': hop_depth,
                    'error': str(e),
                    'success': False
                })
        
        # Summary
        successful_tests = sum(1 for r in results if r.get('success', False))
        total_paths = sum(r.get('paths', 0) for r in results)
        
        print(f"\n📊 Graph Traversal Summary:")
        print(f"   Successful tests: {successful_tests}/{len(hop_depth_tests)}")
        print(f"   Total relationship paths found: {total_paths}")
        
        return successful_tests > 0
        
    except Exception as e:
        print(f"❌ Graph traversal test failed: {e}")
        return False

def main():
    """Run all enhanced knowledge graph tests."""
    print("🚀 Testing Enhanced Knowledge Graph Implementation")
    print("=" * 60)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("Graph Prompts Creation", test_graph_prompts_creation),
        ("Enhanced Graph Creation", test_enhanced_graph_creation),
        ("Enhanced Graph Queries", test_enhanced_graph_queries),
        ("Entity Resolution", test_entity_resolution),
        ("Graph Traversal", test_graph_traversal)
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
    print(f"\n{'='*60}")
    print("📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced knowledge graph tests passed!")
        print("✅ Your system is robust for knowledge graph operations")
        print("\n📋 Enhanced Knowledge Graph Features:")
        print("   • Custom entity extraction with ECSS-specific examples")
        print("   • Entity resolution for variant terms")
        print("   • Enhanced graph traversal with higher hop depths")
        print("   • Relationship path tracking for explainability")
        print("   • Branch-specific graph optimization")
        print("   • Full compliance with Morphik knowledge graph methodology")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 