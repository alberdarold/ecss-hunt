#!/usr/bin/env python3
"""
Test Script for Enhanced ECSS System
This script demonstrates the improvements and tests the new functionality.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import os
import json
import time
import requests
from core.ecss_simplified_ingestion import SimplifiedECSSIngestion

def test_morphik_connection():
    """Test connection to Morphik."""
    print("🔗 Testing Morphik Connection...")
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return False
    
    try:
        ingestion = SimplifiedECSSIngestion(morphik_uri)
        print("✅ Successfully connected to Morphik")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Morphik: {e}")
        return False

def test_simplified_ingestion():
    """Test the simplified ingestion with a single document."""
    print("\n📄 Testing Simplified Ingestion...")
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return False
    
    # Initialize simplified ingestion
    ingestion = SimplifiedECSSIngestion(morphik_uri)
    
    # Find a test document
    pdf_dir = Path("ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    
    if not pdf_dir.exists():
        print(f"❌ ECSS documents directory not found")
        return False
    
    # Get the first PDF file
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_dir}")
        return False
    
    test_file = pdf_files[0]
    print(f"📄 Testing with: {test_file.name}")
    
    # Test ingestion
    start_time = time.time()
    success = ingestion.ingest_document(test_file)
    processing_time = time.time() - start_time
    
    if success:
        print(f"✅ Successfully ingested {test_file.name} in {processing_time:.1f}s")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        test_queries = [
            "requirements",
            "software development",
            "verification"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Searching for: '{query}'")
            results = ingestion.search_documents(query, limit=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"  📄 Result {i}:")
                    print(f"     Summary: {result['summary'][:100]}...")
                    print(f"     Score: {result['relevance_score']}")
            else:
                print("     No results found")
        
        return True
    else:
        print(f"❌ Failed to ingest {test_file.name}")
        return False

def test_api_server():
    """Test the enhanced API server."""
    print("\n🌐 Testing Enhanced API Server...")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            status_data = response.json()
            print(f"   Service: {status_data.get('service', 'Unknown')}")
            print(f"   Version: {status_data.get('version', 'Unknown')}")
            print(f"   Status: {status_data.get('status', 'Unknown')}")
            
            # Test search endpoint
            print("\n🔍 Testing search endpoint...")
            test_queries = [
                "software requirements",
                "testing procedures",
                "quality assurance"
            ]
            
            for query in test_queries:
                print(f"\n🔎 Query: '{query}'")
                try:
                    search_response = requests.get(
                        f"http://localhost:8000/api/search",
                        params={'q': query, 'limit': 2},
                        timeout=10
                    )
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        results = search_data.get('results', [])
                        
                        print(f"   📊 Found {len(results)} results")
                        for i, result in enumerate(results, 1):
                            print(f"   📄 Result {i}:")
                            print(f"      Title: {result.get('title', 'No title')}")
                            print(f"      Summary: {result.get('summary', 'No summary')[:80]}...")
                            print(f"      Explanation: {result.get('explanation', 'No explanation')}")
                            print(f"      Source Type: {result.get('metadata', {}).get('source_type', 'Unknown')}")
                            print(f"      Relevance: {result.get('relevance', 0)}%")
                    else:
                        print(f"   ❌ Search failed: {search_response.status_code}")
                        
                except requests.RequestException as e:
                    print(f"   ❌ Search request failed: {e}")
            
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure to start the server with: python core/enhanced_api_server.py")
        return False

def test_search_suggestions():
    """Test search suggestions endpoint."""
    print("\n💡 Testing Search Suggestions...")
    
    try:
        response = requests.get("http://localhost:8000/api/search/suggestions", timeout=5)
        if response.status_code == 200:
            suggestions_data = response.json()
            suggestions = suggestions_data.get('suggestions', [])
            categories = suggestions_data.get('categories', {})
            
            print(f"✅ Found {len(suggestions)} search suggestions")
            print("📋 Sample suggestions:")
            for suggestion in suggestions[:5]:
                print(f"   - {suggestion}")
            
            print(f"\n📂 Found {len(categories)} categories")
            for category, items in categories.items():
                print(f"   {category}: {len(items)} items")
            
            return True
        else:
            print(f"❌ Suggestions endpoint failed: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Cannot get suggestions: {e}")
        return False

def run_comparison_demo():
    """Run a demonstration comparing old vs new approach."""
    print("\n🆚 Comparison Demo: Old vs New Approach")
    print("=" * 50)
    
    print("\n❌ OLD APPROACH ISSUES:")
    print("1. Complex schemas that overwhelmed the LLM")
    print("2. Schema definitions returned instead of data")
    print("3. No contextualization or explanations")
    print("4. Technical metadata not useful for engineers")
    print("5. Poor search experience with raw chunks")
    
    print("\n✅ NEW APPROACH IMPROVEMENTS:")
    print("1. 3 simple, focused rules that work reliably")
    print("2. Actual extracted information, not schemas")
    print("3. Every result includes context and explanations")
    print("4. Engineer-focused practical information")
    print("5. Intelligent summaries with relevance explanations")
    
    print("\n📊 EXAMPLE NEW SEARCH RESULT:")
    example_result = {
        "title": "ECSS-E-ST-40C - Requirement",
        "summary": "Software shall be developed according to defined standards and undergo verification...",
        "explanation": "This contains requirements related to your query about 'software development'",
        "source_type": "requirement",
        "relevance": 95,
        "metadata": {
            "document": {
                "standard_id": "ECSS-E-ST-40C",
                "filename": "ECSS-E-ST-40C(6March2009).pdf",
                "page": "45"
            }
        }
    }
    
    print(json.dumps(example_result, indent=2))

def main():
    """Run all tests and demonstrations."""
    print("🚀 Enhanced ECSS System Test Suite")
    print("=" * 50)
    
    # Test 1: Morphik Connection
    connection_ok = test_morphik_connection()
    
    if not connection_ok:
        print("\n❌ Cannot proceed without Morphik connection")
        print("💡 Please check your MORPHIK_URI in the .env file")
        return
    
    # Test 2: Simplified Ingestion (commented out for demo - takes time)
    print("\n⏸️  Skipping ingestion test (takes several minutes)")
    print("💡 To test ingestion, run: python core/ecss_simplified_ingestion.py")
    
    # Test 3: API Server
    api_ok = test_api_server()
    
    # Test 4: Search Suggestions
    if api_ok:
        test_search_suggestions()
    
    # Test 5: Comparison Demo
    run_comparison_demo()
    
    # Summary
    print("\n📈 TEST SUMMARY")
    print("=" * 50)
    print(f"🔗 Morphik Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"🌐 API Server: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if connection_ok and api_ok:
        print("\n🎉 SYSTEM IS READY!")
        print("\n📋 NEXT STEPS:")
        print("1. Run ingestion: python core/ecss_simplified_ingestion.py")
        print("2. Test search: http://localhost:8000/api/search?q=software+requirements")
        print("3. Update frontend to use enhanced API")
    else:
        print("\n🔧 SETUP REQUIRED:")
        if not connection_ok:
            print("- Fix Morphik connection (check MORPHIK_URI)")
        if not api_ok:
            print("- Start API server: python core/enhanced_api_server.py")

if __name__ == "__main__":
    main() 