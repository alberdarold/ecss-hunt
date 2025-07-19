#!/usr/bin/env python3
"""
ECSS Hunt - Production Working API Entry Point
==============================================

Production entry point that uses only confirmed working features.
Handles Morphik 307 redirects gracefully.
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

logger.info("🚀 Starting ECSS Hunt Production Working API")
logger.info(f"📁 Backend directory: {backend_dir}")
logger.info(f"🔐 Morphik URI set: {'Yes' if os.getenv('MORPHIK_URI') else 'No'}")

try:
    from production.production_working_api import ProductionWorkingAPI
    logger.info("✅ Successfully imported ProductionWorkingAPI")
except ImportError as e:
    logger.error(f"❌ Failed to import ProductionWorkingAPI: {e}")
    logger.error("🔍 Make sure the production directory exists and contains production_working_api.py")
    sys.exit(1)

def main():
    """Main entry point."""
    logger.info("🌐 Initializing Production Working API")
    
    # Get port from environment
    port = int(os.getenv("PORT", 8002))
    logger.info(f"🌐 Starting server on port {port}")
    
    try:
        # Create the production API server using only working features
        api = ProductionWorkingAPI(port=port)
        logger.info("✅ API server created successfully")
        
        # Run the server
        logger.info("🚀 Starting Flask server...")
        api.run()
        
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 