#!/usr/bin/env python3
"""
Deploy Foundation System
=======================

This script helps deploy the new ECSS Foundation System to replace the old API server.
It includes validation, testing, and deployment guidance.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

def check_environment():
    """Check if environment is ready for deployment."""
    print("🔍 Checking deployment environment...")
    
    required_vars = [
        "MORPHIK_URI",
        "ECSS_DOCUMENTS_PATH"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_foundation_system():
    """Test the foundation system before deployment."""
    print("\n🧪 Testing Foundation System...")
    
    try:
        # Add core directory to path
        sys.path.insert(0, os.path.join(str(Path(__file__).parent.parent), 'core'))
        
        # Import and test the foundation system
        from production.production_legacy.api_server import ProductionAPIServer, FoundationConfig
        
        config = FoundationConfig(
            morphik_uri=os.getenv("MORPHIK_URI"),
            ecss_documents_path=os.getenv("ECSS_DOCUMENTS_PATH", "../../ECSS Published Standards/1-Active Standards/"),
            use_colpali=True,
            api_port=8001,  # Use different port for testing
            debug_mode=True
        )
        
        server = ProductionAPIServer(config)
        print("✅ Foundation system initialized successfully")
        
        # Test Morphik connection
        foundation = server.foundation
        status = foundation.get_system_status()
        print(f"✅ Morphik connected: {status['morphik_connected']}")
        print(f"✅ ColPali enabled: {status['colpali_enabled']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Foundation system test failed: {e}")
        return False

def create_production_entrypoint():
    """Create the main entry point for production deployment."""
    print("\n📝 Creating production entry point...")
    
    entrypoint_content = '''#!/usr/bin/env python3
"""
Production Entry Point for ECSS Foundation System
===============================================

This is the main entry point for the production deployment.
Render will use this file to start the foundation system.
"""

import os
import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, os.path.join(str(Path(__file__).parent.parent), 'core'))

# Import and run the production API server
from production.production_legacy.api_server import main

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w") as f:
        f.write(entrypoint_content)
    
    print("✅ Created main.py as production entry point")

def display_deployment_instructions():
    """Display instructions for deploying to Render."""
    print("\n🚀 Deployment Instructions")
    print("=" * 50)
    print()
    print("1. **Commit Changes:**")
    print("   git add .")
    print("   git commit -m 'deploy: Switch to foundation system'")
    print("   git push origin main")
    print()
    print("2. **Update Render Configuration:**")
    print("   - Go to your Render dashboard")
    print("   - Select your backend service")
    print("   - Update the 'Start Command' to: python main.py")
    print("   - Or if using the core directory directly: python core/production.production_legacy.api_server.py")
    print()
    print("3. **Environment Variables (ensure these are set in Render):**")
    print("   - MORPHIK_URI=your_morphik_uri")
    print("   - ECSS_DOCUMENTS_PATH=./ECSS Published Standards/1-Active Standards/")
    print("   - API_PORT=8000")
    print("   - DEBUG=false")
    print()
    print("4. **Deploy:**")
    print("   - Render will automatically deploy from your git push")
    print("   - Or manually redeploy from the Render dashboard")
    print()
    print("5. **Verify Deployment:**")
    print("   - Check: https://ecss-hunt.onrender.com/api/health")
    print("   - Test: https://ecss-hunt.onrender.com/api/status")
    print("   - Search: https://ecss-hunt.onrender.com/api/search?q=test")

def main():
    """Main deployment function."""
    print("🎯 ECSS Foundation System Deployment")
    print("=" * 40)
    print("Deploying enhanced foundation system with:")
    print("✅ Visual content extraction (ColPali)")
    print("✅ Enhanced search with contextual responses")
    print("✅ Production API server")
    print("✅ System monitoring and stats")
    print()
    
    # Step 1: Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please set required environment variables.")
        return False
    
    # Step 2: Test foundation system
    if not test_foundation_system():
        print("\n❌ Foundation system test failed. Please check configuration.")
        return False
    
    # Step 3: Create production entry point
    create_production_entrypoint()
    
    # Step 4: Display deployment instructions
    display_deployment_instructions()
    
    print("\n🎉 Foundation system is ready for deployment!")
    print("Follow the deployment instructions above to complete the process.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 