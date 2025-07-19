#!/usr/bin/env python3
"""
Test Running API on Port 8002
=============================

Tests the API server that's currently running on port 8002.
"""

import requests
import json
import time

def test_api_8002():
    """Test the API running on port 8002."""
    print("🧪 TESTING RUNNING API ON PORT 8002")
    print("=" * 50)
    
    base_url = "http://localhost:8002"
    
    # Test 1: Health endpoint
    print("🔍 1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health OK: {health_data}")
        else:
            print(f"   ❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health error: {e}")
    
    # Test 2: Status endpoint
    print("\n🔍 2. Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Status OK:")
            for key, value in status_data.items():
                print(f"      {key}: {value}")
        else:
            print(f"   ⚠️ Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Status error: {e}")
    
    # Test 3: Search endpoint
    print("\n🔍 3. Testing search endpoint...")
    try:
        search_data = {
            "query": "verification requirements",
            "k": 5
        }
        print(f"   📝 Query: '{search_data['query']}'")
        
        start_time = time.time()
        response = requests.post(f"{base_url}/api/search", json=search_data, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Search successful!")
            print(f"   ⏱️ Response time: {end_time - start_time:.2f}s")
            print(f"   📊 Results found: {len(result.get('results', []))}")
            print(f"   🔧 Methods used: {result.get('methods_used', 'unknown')}")
            
            # Show first result preview
            if result.get('results'):
                first_result = result['results'][0]
                print(f"   📄 First result preview: {first_result.get('content', 'No content')[:100]}...")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Search error: {e}")
    
    # Test 4: Visual search endpoint (if available)
    print("\n🔍 4. Testing visual search endpoint...")
    try:
        visual_search_data = {
            "query": "ECSS standard requirements",
            "k": 3
        }
        response = requests.post(f"{base_url}/api/search/visual", json=visual_search_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Visual search successful!")
            print(f"   📊 Results found: {len(result.get('results', []))}")
        else:
            print(f"   ⚠️ Visual search: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Visual search: {e}")
    
    print(f"\n🎉 API FUNCTIONALITY TEST COMPLETE!")
    print(f"🌐 API is running at: {base_url}")

if __name__ == "__main__":
    test_api_8002() 