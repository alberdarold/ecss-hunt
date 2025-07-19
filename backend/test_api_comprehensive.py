#!/usr/bin/env python3
"""
Comprehensive API Test
=====================

Tests multiple ports and configurations to find the running API server.
"""

import requests
import time

def test_port(port):
    """Test a specific port for API availability."""
    try:
        response = requests.get(f"http://localhost:{port}/api/health", timeout=2)
        return response.status_code, response.json() if response.status_code == 200 else response.text
    except requests.exceptions.ConnectionError:
        return None, "Connection refused"
    except Exception as e:
        return None, str(e)

def comprehensive_api_test():
    """Test API on multiple common ports."""
    print("🔍 COMPREHENSIVE API TESTING")
    print("=" * 50)
    
    # Common ports for Flask applications
    ports_to_test = [8000, 5000, 3000, 8080, 8001]
    
    print("🌐 Testing common ports...")
    working_ports = []
    
    for port in ports_to_test:
        print(f"   Testing port {port}...", end=" ")
        status_code, response = test_port(port)
        if status_code:
            print(f"✅ FOUND! Status: {status_code}")
            working_ports.append(port)
            print(f"      Response: {response}")
        else:
            print(f"❌ {response}")
    
    if working_ports:
        print(f"\n🎉 Found API server(s) on port(s): {working_ports}")
        
        # Test full functionality on first working port
        port = working_ports[0]
        print(f"\n🧪 Testing full functionality on port {port}:")
        test_full_api(port)
    else:
        print(f"\n❌ No API server found on any tested port.")
        print(f"💡 Make sure the API server is running with:")
        print(f"   python production/production_working_api.py")

def test_full_api(port):
    """Test full API functionality on a working port."""
    base_url = f"http://localhost:{port}"
    
    # Test available endpoints
    endpoints = [
        ("/api/health", "GET"),
        ("/api/status", "GET"),
        ("/api/search", "POST"),
    ]
    
    for endpoint, method in endpoints:
        try:
            print(f"🔍 Testing {method} {endpoint}...")
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:  # POST
                test_data = {"query": "verification requirements", "k": 3}
                response = requests.post(f"{base_url}{endpoint}", json=test_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if endpoint == "/api/search" and "results" in result:
                    print(f"   ✅ Success: {len(result['results'])} results found")
                else:
                    print(f"   ✅ Success: {result}")
            else:
                print(f"   ⚠️ Status {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    comprehensive_api_test() 