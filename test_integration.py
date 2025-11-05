#!/usr/bin/env python3
"""
Test script for 1sub.io integration
Tests the key endpoints and functionality
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / "backend" / "config" / ".env"
load_dotenv(dotenv_path=env_path)

import os
import requests

# Configuration
API_BASE_URL = os.getenv("NEXT_PUBLIC_API_BASE_URL", "http://localhost:8000")
ONESUB_API_KEY = os.getenv("ONESUB_API_KEY")
ONESUB_TOOL_ID = os.getenv("ONESUB_TOOL_ID")

def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   [OK] Health check passed: {data.get('status')}")
            return True
        else:
            print(f"   [FAIL] Health check failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   [FAIL] Cannot connect to {API_BASE_URL}")
        print(f"   Make sure the backend server is running!")
        return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_tool_id_endpoint():
    """Test tool ID endpoint"""
    print("\n2. Testing Tool ID Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/config/tool-id", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            tool_id = data.get('tool_id')
            print(f"   [OK] Tool ID retrieved: {tool_id}")
            if tool_id == ONESUB_TOOL_ID:
                print(f"   [OK] Tool ID matches environment variable")
            else:
                print(f"   [WARN] Tool ID mismatch (env: {ONESUB_TOOL_ID})")
            return True
        else:
            data = response.json()
            print(f"   [FAIL] Failed: {data.get('message')}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_session_endpoint():
    """Test session endpoint (should return not authenticated)"""
    print("\n3. Testing Session Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/auth/session", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            authenticated = data.get('authenticated', False)
            print(f"   [OK] Session check successful")
            print(f"   Authenticated: {authenticated} (expected: False)")
            return True
        else:
            print(f"   [FAIL] Failed: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_onesub_client():
    """Test 1sub API client initialization"""
    print("\n4. Testing 1sub API Client...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        from utils.onesub_client import OneSubClient
        
        if not ONESUB_API_KEY:
            print("   ❌ ONESUB_API_KEY not set")
            return False
        
        client = OneSubClient()
        print(f"   [OK] 1sub client initialized successfully")
        print(f"   API Key: {ONESUB_API_KEY[:20]}...")
        print(f"   Base URL: {client.base_url}")
        return True
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_environment_variables():
    """Test environment variables"""
    print("\n5. Testing Environment Variables...")
    issues = []
    
    if not ONESUB_API_KEY:
        issues.append("ONESUB_API_KEY not set")
    else:
        print(f"   [OK] ONESUB_API_KEY: {ONESUB_API_KEY[:20]}...")
    
    if not ONESUB_TOOL_ID:
        issues.append("ONESUB_TOOL_ID not set")
    else:
        print(f"   [OK] ONESUB_TOOL_ID: {ONESUB_TOOL_ID}")
    
    session_secret = os.getenv("FLASK_SESSION_SECRET_KEY")
    if not session_secret:
        issues.append("FLASK_SESSION_SECRET_KEY not set")
    else:
        print(f"   [OK] FLASK_SESSION_SECRET_KEY: SET")
    
    if issues:
        print(f"   [FAIL] Issues found: {', '.join(issues)}")
        return False
    else:
        print(f"   [OK] All environment variables are set")
        return True

def main():
    print("=" * 60)
    print("1sub.io Integration Test Suite")
    print("=" * 60)
    
    # Test environment variables first
    env_ok = test_environment_variables()
    
    if not env_ok:
        print("\n[FAIL] Environment variables not properly configured!")
        print("Please check backend/config/.env file")
        return
    
    # Test 1sub client
    client_ok = test_onesub_client()
    
    # Test backend endpoints
    health_ok = test_health_check()
    
    if health_ok:
        tool_id_ok = test_tool_id_endpoint()
        session_ok = test_session_endpoint()
    else:
        print("\n[WARN] Backend server is not running. Please start it first:")
        print("   cd backend")
        print("   python production/production_api_server.py")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Environment Variables: {'[OK]' if env_ok else '[FAIL]'}")
    print(f"1sub API Client: {'[OK]' if client_ok else '[FAIL]'}")
    print(f"Health Check: {'[OK]' if health_ok else '[FAIL]'}")
    if health_ok:
        print(f"Tool ID Endpoint: {'[OK]' if tool_id_ok else '[FAIL]'}")
        print(f"Session Endpoint: {'[OK]' if session_ok else '[FAIL]'}")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("1. Start backend server: python backend/production/production_api_server.py")
    print("2. Start frontend: cd frontend && npm run dev")
    print("3. Test purchase flow in browser at http://localhost:3000/demo")
    print("=" * 60)

if __name__ == "__main__":
    main()

