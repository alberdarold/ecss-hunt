import requests
import json

def test_search_api():
    """Test the Next.js search API with real queries."""
    
    base_url = "http://localhost:3000/api/search"
    
    # Test queries
    test_queries = [
        "software development requirements",
        "materials and processes",
        "communications protocols",
        "project planning"
    ]
    
    print("=== Testing ECSS Standards Navigator Search API ===\n")
    
    for query in test_queries:
        print(f"Searching for: '{query}'")
        
        try:
            # Make API request using GET with query parameters
            params = {"q": query}
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ API Response (Status: {response.status_code})")
                print(f"  Results found: {len(data.get('results', []))}")
                
                # Display results
                for i, result in enumerate(data.get('results', [])[:3]):
                    print(f"    {i+1}. Document: {result.get('title', 'N/A')}")
                    print(f"       Score: {result.get('score', 'N/A')}")
                    print(f"       Branch: {result.get('metadata', {}).get('branch_name', 'N/A')}")
                    content = result.get('content', 'N/A')
                    if content and len(content) > 100:
                        content = content[:100] + "..."
                    print(f"       Content: {content}")
                    print()
            else:
                print(f"✗ API Error (Status: {response.status_code})")
                print(f"  Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Connection Error: Make sure the Next.js server is running on http://localhost:3000")
            break
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_search_api() 