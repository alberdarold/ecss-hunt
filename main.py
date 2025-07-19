#!/usr/bin/env python3
"""
ECSS Hunt - Production Entry Point with Document Access
======================================================

Entry point that uses the full production API server with:
- Document ingestion and search capabilities
- Visual content extraction (ColPali)
- Real ECSS document content search
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

try:
    # Import the production API server with document access
    from production.production_api_server import ProductionAPIServer, FoundationConfig
    print("✅ Successfully imported ProductionAPIServer")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def main():
    """Main entry point for Render deployment."""
    print("🚀 Starting ECSS Hunt Production API with Document Access")
    
    # Get port from environment (Render sets PORT automatically)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🌐 Starting server on port {port}")
    print(f"🔐 Morphik URI: {os.getenv('MORPHIK_URI', 'Not set')[:50]}...")
    
    try:
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
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 