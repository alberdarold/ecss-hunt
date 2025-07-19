#!/usr/bin/env python3
"""
Morphik Connection Diagnostic Tool
=================================

This script tests the basic Morphik connection to diagnose issues
before testing the enhanced system.

Usage:
    python test_morphik_connection.py
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import os
import traceback
from morphik import Morphik

def test_basic_connection():
    """Test basic Morphik connection with detailed error reporting."""
    print("MORPHIK CONNECTION DIAGNOSTIC")
    print("=" * 40)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("FAIL: MORPHIK_URI not found in environment")
        return False
    
    print(f"INFO: Using Morphik URI: {morphik_uri[:50]}...")
    
    try:
        # Test 1: Initialize client
        print("\nTEST 1: Initializing Morphik client...")
        db = Morphik(morphik_uri)
        print("PASS: Morphik client created successfully")
        
        # Test 2: Try different connection methods
        connection_methods = [
            ("list_documents", lambda: db.list_documents()),
            ("query", lambda: db.query("test", k=1)),
            ("retrieve_chunks", lambda: db.retrieve_chunks("test", k=1))
        ]
        
        for method_name, method_func in connection_methods:
            print(f"\nTEST 2.{method_name}: Testing {method_name}()...")
            try:
                result = method_func()
                print(f"PASS: {method_name}() worked successfully")
                
                if method_name == "list_documents":
                    print(f"INFO: Found {len(result)} documents")
                elif method_name == "query":
                    if hasattr(result, 'completion'):
                        print(f"INFO: Query returned completion: {len(result.completion) if result.completion else 0} chars")
                    if hasattr(result, 'sources'):
                        print(f"INFO: Query returned {len(result.sources)} sources")
                elif method_name == "retrieve_chunks":
                    print(f"INFO: Retrieved {len(result)} chunks")
                
                return True  # If any method works, connection is good
                
            except Exception as e:
                print(f"FAIL: {method_name}() failed")
                print(f"Error: {str(e)[:200]}")
                
                # Print detailed error for debugging
                if "307" in str(e) or "Redirect" in str(e):
                    print("DEBUG: This is a 307 redirect issue")
                    print("CAUSE: Morphik API endpoint format may have changed")
                    print("SOLUTION: Check if API requires trailing slashes or different endpoint format")
                elif "401" in str(e) or "Unauthorized" in str(e):
                    print("DEBUG: Authentication issue")
                    print("CAUSE: Invalid or expired API key")
                    print("SOLUTION: Check MORPHIK_URI credentials")
                elif "404" in str(e) or "Not Found" in str(e):
                    print("DEBUG: Endpoint not found")
                    print("CAUSE: API endpoint may have moved or changed")
                elif "timeout" in str(e).lower() or "connection" in str(e).lower():
                    print("DEBUG: Network connectivity issue")
                    print("CAUSE: Network or firewall blocking connection")
        
        print("\nFAIL: All connection methods failed")
        return False
        
    except Exception as e:
        print(f"\nFAIL: Failed to initialize Morphik client")
        print(f"Error: {str(e)[:300]}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_morphik_sdk_info():
    """Get information about the Morphik SDK."""
    print("\nSDK INFORMATION")
    print("-" * 20)
    
    try:
        import morphik
        print(f"Morphik SDK version: {getattr(morphik, '__version__', 'unknown')}")
        print(f"Morphik module location: {morphik.__file__}")
        
        # Check available methods
        db_methods = [method for method in dir(Morphik) if not method.startswith('_')]
        print(f"Available Morphik methods: {len(db_methods)}")
        
        # Check for specific methods we need
        required_methods = ['list_documents', 'query', 'retrieve_chunks', 'ingest_file']
        for method in required_methods:
            if hasattr(Morphik, method):
                print(f"  PASS: {method}() available")
            else:
                print(f"  FAIL: {method}() missing")
        
    except Exception as e:
        print(f"Error getting SDK info: {e}")

def main():
    """Main diagnostic function."""
    
    # Test SDK information
    test_morphik_sdk_info()
    
    # Test basic connection
    success = test_basic_connection()
    
    print("\n" + "=" * 40)
    if success:
        print("RESULT: Morphik connection WORKING")
        print("NEXT STEP: You can proceed with enhanced system testing")
        print("Command: python deploy_enhanced_morphik.py")
    else:
        print("RESULT: Morphik connection FAILED")
        print("NEXT STEPS:")
        print("1. Check your MORPHIK_URI in .env file")
        print("2. Verify network connectivity")
        print("3. Try updating Morphik SDK: pip install --upgrade morphik")
        print("4. Contact Morphik support if issue persists")
    
    return success

if __name__ == "__main__":
    main() 