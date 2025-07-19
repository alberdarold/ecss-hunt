#!/usr/bin/env python3
"""
TARGETED GRAPH CLEANUP - DELETE BY NAME
=======================================

Since list_graphs() returns 404 but graphs clearly exist,
try deleting them individually by name.
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from morphik import Morphik

def main():
    """Delete graphs by targeting known names."""
    print("🎯 TARGETED GRAPH CLEANUP")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    try:
        # Connect to Morphik
        print("🔗 Connecting to Morphik...")
        db = Morphik(morphik_uri)
        
        # List of graph name patterns we know exist from the screenshot
        graph_patterns = [
            # Canonical graphs (keep these eventually, but delete duplicates)
            "ecss_e_knowledge_graph",
            "ecss_m_knowledge_graph", 
            "ecss_q_knowledge_graph",
            "ecss_s_knowledge_graph",
            "ecss_u_knowledge_graph",
            
            # Branch patterns we saw in screenshot
            "ecss_q_branch_",
            "ecss_p_branch_", 
            "ecss_m_branch_",
            "ecss_e_branch_",
            "ecss_s_branch_",
            "ecss_u_branch_",
            
            # Other patterns
            "Test ECSS Graph",
            "test_ecss_general",
            "ECSS Standards",
            "ecss_general_",
        ]
        
        # Try different naming variations for each pattern
        graph_names_to_try = []
        
        # Add exact patterns
        graph_names_to_try.extend(graph_patterns)
        
        # Add numbered variations (common in runaway creation)
        for pattern in graph_patterns:
            if not pattern.endswith("_"):
                for i in range(1, 20):  # Try first 20 numbers
                    graph_names_to_try.extend([
                        f"{pattern}_{i}",
                        f"{pattern}_{i:02d}",  # Zero-padded
                        f"{pattern}_{i}_enhanced",
                        f"{pattern}_enhanced_{i}",
                    ])
        
        # Add enhanced/advanced variations
        for pattern in graph_patterns:
            graph_names_to_try.extend([
                f"{pattern}_enhanced",
                f"{pattern}_advanced", 
                f"{pattern}_v2",
                f"{pattern}_new",
            ])
        
        print(f"🎯 Will attempt to delete {len(graph_names_to_try)} potential graph names...")
        
        deleted_count = 0
        not_found_count = 0
        error_count = 0
        
        # Try deleting each potential graph name
        for i, graph_name in enumerate(graph_names_to_try, 1):
            try:
                # Show progress every 50 attempts
                if i % 50 == 0:
                    print(f"⏳ Progress: {i}/{len(graph_names_to_try)} attempted...")
                
                # Try to delete the graph
                db.delete_graph(graph_name)
                print(f"🗑️ DELETED: {graph_name}")
                deleted_count += 1
                
                # Be gentle with the API
                time.sleep(0.2)
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if "not found" in error_msg or "404" in error_msg:
                    # Graph doesn't exist - that's fine
                    not_found_count += 1
                    if i <= 20:  # Only show first 20 not-found messages
                        print(f"  ⚪ Not found: {graph_name}")
                elif "403" in error_msg or "unauthorized" in error_msg:
                    print(f"  🔒 Access denied: {graph_name}")
                    error_count += 1
                else:
                    print(f"  ❌ Error deleting {graph_name}: {e}")
                    error_count += 1
        
        # Summary
        print(f"\n🏁 CLEANUP SUMMARY:")
        print(f"🗑️ Successfully deleted: {deleted_count}")
        print(f"⚪ Not found (good): {not_found_count}")  
        print(f"❌ Errors: {error_count}")
        
        if deleted_count > 0:
            print(f"\n✅ SUCCESS: Deleted {deleted_count} graphs!")
            print(f"💡 Refresh your UI to see the cleanup results")
        elif error_count == 0:
            print(f"\n✅ All targeted graphs were already clean")
        else:
            print(f"\n⚠️ Some errors occurred - check permissions")
        
        # Try to verify cleanup by attempting one canonical graph check
        print(f"\n🔍 Verifying cleanup...")
        try:
            status = db.get_graph_status("ecss_e_knowledge_graph")
            if status:
                print(f"⚠️ At least one canonical graph still exists")
            else:
                print(f"✅ Canonical graph check: clean")
        except Exception as e:
            if "not found" in str(e).lower():
                print(f"✅ Canonical graphs appear to be deleted")
            else:
                print(f"❓ Cannot verify: {e}")
                
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    main() 