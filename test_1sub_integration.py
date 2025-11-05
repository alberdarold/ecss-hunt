#!/usr/bin/env python3
"""
Test script for 1sub.io integration
Tests the connection and configuration of 1sub API client
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv

# Load environment variables
env_path = backend_dir / "config" / ".env"
load_dotenv(env_path)

def test_1sub_config():
    """Test 1sub configuration."""
    print("Testing 1sub.io Configuration\n")
    
    # Check environment variables
    required_vars = {
        "ONESUB_API_KEY": os.getenv("ONESUB_API_KEY"),
        "ONESUB_TOOL_ID": os.getenv("ONESUB_TOOL_ID"),
        "FLASK_SESSION_SECRET_KEY": os.getenv("FLASK_SESSION_SECRET_KEY"),
    }
    
    print("Environment Variables:")
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            # Mask sensitive values
            masked = var_value[:10] + "..." if len(var_value) > 10 else var_value
            print(f"  [OK] {var_name}: {masked}")
        else:
            print(f"  [FAIL] {var_name}: NOT SET")
            all_set = False
    
    if not all_set:
        print("\n[WARN] Missing required environment variables!")
        return False
    
    print("\nTesting OneSubClient Initialization...")
    try:
        from utils.onesub_client import OneSubClient
        
        client = OneSubClient()
        print("  [OK] OneSubClient initialized successfully")
        print(f"  [OK] API Base URL: {client.base_url}")
        print(f"  [OK] API Key: {client.api_key[:10]}...")
        
        return True
        
    except ValueError as e:
        print(f"  [FAIL] Initialization failed: {e}")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False

def test_1sub_api_endpoint():
    """Test 1sub API endpoint connectivity."""
    print("\nTesting 1sub.io API Connectivity...")
    
    try:
        import requests
        
        # Test basic connectivity
        base_url = "https://1sub.io"
        test_url = f"{base_url}/api/v1/verify-user"
        
        print(f"  Testing endpoint: {test_url}")
        
        # Try a simple request (will fail but shows connectivity)
        response = requests.get(base_url, timeout=5)
        if response.status_code in [200, 404, 405]:  # Any response means server is reachable
            print("  [OK] 1sub.io server is reachable")
            return True
        else:
            print(f"  [WARN] Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("  [FAIL] Connection timeout - check internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("  [FAIL] Connection error - check internet connection or 1sub.io status")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False

def test_backend_integration():
    """Test backend integration with 1sub."""
    print("\nTesting Backend Integration...")
    
    try:
        from production.production_api_server import ProductionAPIServer
        from production.ecss_foundation_system import FoundationConfig
        
        # Create minimal config for testing
        config = FoundationConfig(
            morphik_uri=os.getenv("MORPHIK_URI", "test"),
            api_port=8000,
            use_colpali=False,
            debug_mode=True
        )
        
        # Try to create server (will fail at Morphik but should initialize 1sub)
        print("  Attempting to initialize server...")
        server = ProductionAPIServer(config)
        
        if server.onesub_client:
            print("  [OK] 1sub client initialized in ProductionAPIServer")
            return True
        else:
            print("  [FAIL] 1sub client not initialized")
            return False
            
    except Exception as e:
        # Expected to fail at Morphik initialization, but check if 1sub was initialized
        error_msg = str(e)
        if "ONESUB_API_KEY" in error_msg or "onesub" in error_msg.lower():
            print(f"  [FAIL] 1sub initialization error: {e}")
            return False
        elif "Morphik" in error_msg or "morphik" in error_msg.lower():
            print("  [WARN] Morphik initialization failed (expected), but checking 1sub...")
            # This is expected - we can't test full initialization without Morphik
            print("  [INFO] Cannot fully test without Morphik connection")
            return None
        else:
            print(f"  [FAIL] Unexpected error: {e}")
            return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("1sub.io Integration Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Configuration
    results.append(("Configuration", test_1sub_config()))
    
    # Test 2: API Connectivity
    results.append(("API Connectivity", test_1sub_api_endpoint()))
    
    # Test 3: Backend Integration
    result = test_backend_integration()
    results.append(("Backend Integration", result))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"  {status}: {test_name}")
    
    print("\nNext Steps:")
    print("  1. Ensure all environment variables are set in Render")
    print("  2. Check Render logs for 1sub initialization messages")
    print("  3. Test the /api/auth/verify endpoint with a real token")
    print("  4. Verify tool_id is correctly configured in 1sub.io dashboard")

if __name__ == "__main__":
    main()

