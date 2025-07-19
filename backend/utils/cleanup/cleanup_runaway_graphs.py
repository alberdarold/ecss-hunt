#!/usr/bin/env python3
"""
MORPHIK GRAPH CLEANUP SCRIPT
===========================

Cleans up the runaway graph creation bug and resets to just 5 canonical graphs.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from morphik import Morphik

def main():
    """Clean up runaway graphs."""
    print("🧹 MORPHIK GRAPH CLEANUP SCRIPT")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    try:
        # Connect to Morphik
        print("🔗 Connecting to Morphik...")
        db = Morphik(morphik_uri)
        
        # Get all graphs
        print("📊 Fetching all graphs...")
        existing_graphs = db.list_graphs()
        
        if not existing_graphs:
            print("✅ No graphs found - system is clean!")
            return
        
        print(f"📈 Found {len(existing_graphs)} total graphs")
        
        # Define canonical graphs we want to keep
        canonical_names = {
            "ecss_e_knowledge_graph": "Engineering Standards",
            "ecss_m_knowledge_graph": "Management Standards", 
            "ecss_q_knowledge_graph": "Quality Standards",
            "ecss_s_knowledge_graph": "Space Assurance Standards",
            "ecss_u_knowledge_graph": "Sustainability Standards"
        }
        
        # Categorize graphs
        canonical_found = {}
        duplicates = []
        unwanted = []
        
        for graph in existing_graphs:
            name = graph.name
            
            if name in canonical_names:
                if name in canonical_found:
                    duplicates.append(name)
                else:
                    canonical_found[name] = graph
            else:
                # Any graph with ECSS, test, branch, etc.
                if any(term in name.lower() for term in ['ecss', 'test', 'branch']):
                    unwanted.append(name)
        
        # Show summary
        print(f"\n📊 GRAPH ANALYSIS:")
        print(f"✅ Canonical graphs found: {len(canonical_found)}")
        print(f"🔄 Duplicate canonical: {len(duplicates)}")
        print(f"🗑️ Unwanted graphs: {len(unwanted)}")
        
        for name, desc in canonical_names.items():
            if name in canonical_found:
                print(f"  ✅ {desc}: {name}")
            else:
                print(f"  ❌ {desc}: {name} (MISSING)")
        
        # Show unwanted graphs
        if unwanted:
            print(f"\n🗑️ UNWANTED GRAPHS TO DELETE:")
            for name in unwanted[:10]:  # Show first 10
                print(f"  - {name}")
            if len(unwanted) > 10:
                print(f"  ... and {len(unwanted) - 10} more")
        
        if duplicates:
            print(f"\n🔄 DUPLICATE CANONICAL GRAPHS:")
            for name in duplicates:
                print(f"  - {name}")
        
        # Ask for confirmation
        total_to_delete = len(unwanted) + len(duplicates)
        if total_to_delete == 0:
            print("\n✅ System is clean! No graphs need deletion.")
            return
        
        print(f"\n⚠️ ABOUT TO DELETE {total_to_delete} GRAPHS")
        response = input("Continue with cleanup? (y/N): ").strip().lower()
        
        if response != 'y':
            print("❌ Cleanup cancelled by user")
            return
        
        # Delete unwanted graphs
        deleted_count = 0
        
        print(f"\n🧹 Deleting {len(unwanted)} unwanted graphs...")
        for name in unwanted:
            try:
                db.delete_graph(name)
                print(f"  🗑️ Deleted: {name}")
                deleted_count += 1
                time.sleep(0.5)  # Be gentle with API
            except Exception as e:
                print(f"  ❌ Failed to delete {name}: {e}")
        
        print(f"\n🔄 Deleting {len(duplicates)} duplicate graphs...")
        for name in duplicates:
            try:
                db.delete_graph(name)
                print(f"  🗑️ Deleted duplicate: {name}")
                deleted_count += 1
                time.sleep(0.5)  # Be gentle with API
            except Exception as e:
                print(f"  ❌ Failed to delete {name}: {e}")
        
        print(f"\n✅ CLEANUP COMPLETE!")
        print(f"🗑️ Deleted {deleted_count} graphs")
        print(f"✅ Kept {len(canonical_found)} canonical graphs")
        
        # Final verification
        print(f"\n🔍 Verifying cleanup...")
        final_graphs = db.list_graphs()
        print(f"📊 Final graph count: {len(final_graphs) if final_graphs else 0}")
        
        if final_graphs:
            print("📈 Remaining graphs:")
            for graph in final_graphs:
                name = graph.name
                if name in canonical_names:
                    print(f"  ✅ {name} ({canonical_names[name]})")
                else:
                    print(f"  ⚠️ {name} (unexpected)")
        
        print(f"\n🚀 System is now clean and ready!")
        print(f"💡 You can safely restart the enhanced API server.")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    main() 