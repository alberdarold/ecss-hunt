#!/usr/bin/env python3
"""
Test API Functionality
======================

Quick test to verify the production API is working.
"""

import requests
import time

def test_api():
    """Test the production API endpoints."""
    print("🧪 TESTING API FUNCTIONALITY")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        print("🔍 Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ API Health: {response.json()}")
        else:
            print(f"❌ API Health failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API not running - connection failed")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    # Test status endpoint  
    try:
        print("🔍 Testing status endpoint...")
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print(f"✅ API Status: {response.json()}")
        else:
            print(f"⚠️ Status endpoint: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Status test: {e}")
    
    # Test search endpoint
    try:
        print("🔍 Testing search endpoint...")
        search_data = {"query": "test query", "k": 3}
        response = requests.post(f"{base_url}/api/search", json=search_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Search worked: Found {len(result.get('results', []))} results")
        else:
            print(f"⚠️ Search endpoint: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Search test: {e}")
    
    print(f"\n🎉 API functionality test complete!")
    return True

if __name__ == "__main__":
    test_api() 