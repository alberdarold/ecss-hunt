#!/usr/bin/env python3
"""
Test what Morphik methods are actually available
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from morphik import Morphik

def main():
    print("🔍 MORPHIK METHOD DISCOVERY")
    print("=" * 40)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    try:
        # Connect to Morphik
        print("🔗 Connecting to Morphik...")
        db = Morphik(morphik_uri)
        print("✅ Morphik connected")
        
        # Test basic operations
        print("\n📊 Testing Basic Operations:")
        
        try:
            docs = db.list_documents(limit=1)
            print(f"✅ list_documents: {len(docs) if docs else 0} found")
        except Exception as e:
            print(f"❌ list_documents failed: {e}")
        
        try:
            result = db.query('test', limit=1)
            print(f"✅ query works: {bool(result)}")
        except Exception as e:
            print(f"❌ query failed: {e}")
        
        # Check available methods
        print(f"\n🔍 Analyzing Available Methods:")
        methods = [attr for attr in dir(db) if not attr.startswith('_')]
        print(f"📊 Total methods: {len(methods)}")
        
        # Look for graph methods
        graph_methods = [m for m in methods if 'graph' in m.lower()]
        if graph_methods:
            print(f"🔗 Graph methods found: {graph_methods}")
        else:
            print("❌ No graph methods found!")
        
        # Look for other interesting methods
        interesting = ['agent', 'batch', 'cache', 'create', 'delete']
        for term in interesting:
            found = [m for m in methods if term in m.lower()]
            if found:
                print(f"🔍 {term.title()} methods: {found}")
        
        # Show all methods for complete picture
        print(f"\n📋 ALL AVAILABLE METHODS:")
        for i, method in enumerate(sorted(methods), 1):
            print(f"  {i:2d}. {method}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    main() 