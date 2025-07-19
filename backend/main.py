#!/usr/bin/env python3
"""
ECSS Hunt - Backend Main Entry Point
===================================

Backup entry point for backend deployment.
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from production.production_working_api import ProductionWorkingAPI

def main():
    """Main entry point."""
    print("🚀 Starting ECSS Hunt Production API (Backend)")
    
    # Get port from environment
    port = int(os.getenv("PORT", 8002))
    
    print(f"🌐 Starting server on port {port}")
    
    # Create and run the production API server
    api = ProductionWorkingAPI(port=port)
    api.run()

if __name__ == "__main__":
    main() 