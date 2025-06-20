import requests
import json

def test_flask_api():
    """Test the Flask API server that interfaces with Morphik."""
    
    base_url = "http://localhost:5000/api"
    
    # Test queries
    test_queries = [
        "software development requirements",
        "materials and processes",
        "communications protocols",
        "project planning"
    ]
    
    print("=== Testing Flask API Server with Morphik Integration ===\n")
    
    # First, test health check
    print("1. Testing Health Check:")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ Health Check (Status: {response.status_code})")
            print(f"  Status: {health_data.get('status', 'Unknown')}")
            print(f"  Morphik Connected: {health_data.get('morphik_connected', False)}")
        else:
            print(f"✗ Health Check Error (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Health Check Error: {e}")
    
    print("\n2. Testing Document List:")
    try:
        response = requests.get(f"{base_url}/documents")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Documents API (Status: {response.status_code})")
            print(f"  Documents found: {data.get('total', 0)}")
            for doc in data.get('documents', [])[:3]:
                print(f"    - {doc.get('filename', 'Unknown')} ({doc.get('status', 'Unknown')})")
        else:
            print(f"✗ Documents API Error (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Documents API Error: {e}")
    
    print("\n3. Testing Search API:")
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        
        try:
            # Make API request using GET with query parameters
            params = {"q": query}
            response = requests.get(f"{base_url}/search", params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Search API (Status: {response.status_code})")
                print(f"  Results found: {len(data.get('results', []))}")
                
                # Display results
                for i, result in enumerate(data.get('results', [])[:3]):
                    print(f"    {i+1}. Document: {result.get('title', 'N/A')}")
                    print(f"       Score: {result.get('score', 'N/A')}")
                    print(f"       Relevance: {result.get('relevance', 'N/A')}")
                    print(f"       Branch: {result.get('metadata', {}).get('branch_name', 'N/A')}")
                    content = result.get('content', 'N/A')
                    if content and len(content) > 150:
                        content = content[:150] + "..."
                    print(f"       Content: {content}")
                    print()
            else:
                print(f"✗ Search API Error (Status: {response.status_code})")
                print(f"  Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Connection Error: Make sure the Flask API server is running on http://localhost:5000")
            break
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_flask_api() 