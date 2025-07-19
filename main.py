#!/usr/bin/env python3
"""
ECSS Hunt - Render Deployment Entry Point
=========================================

Production entry point for Render deployment.
Starts the working production API server on the configured port.
"""
import os
import sys
from pathlib import Path

# Add backend to Python path - handle both local and Render paths
project_root = Path(__file__).parent
backend_dir = project_root / "backend"

# Handle Render's different path structure
if not backend_dir.exists():
    # Try alternative paths that Render might use
    backend_dir = project_root / "src" / "backend"
    if not backend_dir.exists():
        backend_dir = Path("/opt/render/project/src/backend")

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

print(f"🔍 Project root: {project_root}")
print(f"🔍 Backend dir: {backend_dir}")
print(f"🔍 Backend exists: {backend_dir.exists()}")

try:
    # Import the working production API (not the old foundation system)
    from production.production_working_api import ProductionWorkingAPI
    print("✅ Successfully imported ProductionWorkingAPI")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔍 Available paths:", sys.path)
    # Try alternative import
    try:
        sys.path.insert(0, str(backend_dir / "production"))
        from production_working_api import ProductionWorkingAPI
        print("✅ Successfully imported ProductionWorkingAPI (alternative path)")
    except ImportError as e2:
        print(f"❌ Alternative import also failed: {e2}")
        sys.exit(1)

def main():
    """Main entry point for Render deployment."""
    print("🚀 Starting ECSS Hunt Production API for Render")
    
    # Get port from environment (Render sets PORT automatically)
    port = int(os.getenv("PORT", 8002))
    
    print(f"🌐 Starting server on port {port}")
    print(f"🔐 Morphik URI: {os.getenv('MORPHIK_URI', 'Not set')[:50]}...")
    
    try:
        # Create and run the production API server
        api = ProductionWorkingAPI(port=port)
        print("✅ API server created successfully")
        api.run()
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 