#!/usr/bin/env python3
"""
ECSS Hunt - Production Entry Point with Fallback
===============================================

Entry point that tries the full production server first,
then falls back to working API if dependencies fail.
"""
import os
import sys
from pathlib import Path

# Add backend to Python path - handle both local and Render paths
project_root = Path(__file__).parent
backend_dir = project_root / "backend"

# Handle Render's different path structure
if not backend_dir.exists():
    backend_dir = project_root / "src" / "backend"
    if not backend_dir.exists():
        backend_dir = Path("/opt/render/project/src/backend")

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

print(f"🔍 Project root: {project_root}")
print(f"🔍 Backend dir: {backend_dir}")
print(f"🔍 Backend exists: {backend_dir.exists()}")

def main():
    """Main entry point with fallback logic."""
    print("🚀 Starting ECSS Hunt API Server")
    
    # Get port from environment (Render sets PORT automatically)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🌐 Starting server on port {port}")
    print(f"🔐 Morphik URI: {os.getenv('MORPHIK_URI', 'Not set')[:50]}...")
    
    # Try Production API Server first (with document access)
    try:
        print("🎯 Attempting to start Production API Server (with document access)...")
        
        from production.production_api_server import ProductionAPIServer, FoundationConfig
        print("✅ Successfully imported ProductionAPIServer")
        
        # Create configuration for production server
        config = FoundationConfig(
            morphik_uri=os.getenv("MORPHIK_URI"),
            ecss_documents_path=os.getenv("ECSS_DOCUMENTS_PATH", "./ECSS Published Standards/1-Active Standards/"),
            max_documents=int(os.getenv("MAX_DOCUMENTS", "10")),
            use_colpali=True,  # Enable visual content extraction
            api_port=port,
            debug_mode=os.getenv("DEBUG", "false").lower() == "true",
            cost_limit_per_doc=float(os.getenv("COST_LIMIT_PER_DOC", "2.0"))
        )
        
        # Create and run the production API server with document access
        server = ProductionAPIServer(config)
        print("✅ Production API server created successfully")
        print("📚 Document access: ENABLED")
        print("🔍 Visual search: ENABLED")
        server.run()
        
    except ImportError as e:
        print(f"⚠️ ProductionAPIServer import failed: {e}")
        print("🔄 Falling back to Production Working API...")
        
        try:
            from production.production_working_api import ProductionWorkingAPI
            print("✅ Successfully imported ProductionWorkingAPI (fallback)")
            
            # Create and run the working API server
            api = ProductionWorkingAPI(port=port)
            print("✅ Production Working API server created successfully")
            print("📚 Document access: LIMITED (AI responses only)")
            print("🔍 Visual search: ENABLED")
            api.run()
            
        except Exception as e2:
            print(f"❌ Both production servers failed to start")
            print(f"   - ProductionAPIServer error: {e}")
            print(f"   - ProductionWorkingAPI error: {e2}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Production API server failed to start: {e}")
        import traceback
        traceback.print_exc()
        print("🔄 Falling back to Production Working API...")
        
        try:
            from production.production_working_api import ProductionWorkingAPI
            print("✅ Successfully imported ProductionWorkingAPI (fallback)")
            
            api = ProductionWorkingAPI(port=port)
            print("✅ Production Working API server created successfully")
            print("📚 Document access: LIMITED (AI responses only)")
            print("🔍 Visual search: ENABLED")
            api.run()
            
        except Exception as e2:
            print(f"❌ All servers failed to start: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main() 