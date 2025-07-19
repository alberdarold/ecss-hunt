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

# Add backend to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import and run the production API
from backend.production.production_working_api import ProductionWorkingAPI

def main():
    """Main entry point for Render deployment."""
    print("🚀 Starting ECSS Hunt Production API for Render")
    
    # Get port from environment (Render sets PORT automatically)
    port = int(os.getenv("PORT", 8002))
    
    print(f"🌐 Starting server on port {port}")
    
    # Create and run the production API server
    api = ProductionWorkingAPI(port=port)
    api.run()

if __name__ == "__main__":
    main() 