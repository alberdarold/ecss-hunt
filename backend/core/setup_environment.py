"""
Environment Setup Script for ECSS Standards Navigator
Sets up required environment variables and validates configuration.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Environment Setup Script for ECSS Standards Navigator
Sets up required environment variables and validates configuration.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))



import os
import sys

def setup_environment():
    """Set up environment variables for the ECSS Standards Navigator."""
    
    print("🔧 Setting up ECSS Standards Navigator Environment")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    # Load environment variables
        
    # Validate required variables
    validate_environment()
    
    print("\n✅ Environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python test_pre_ingestion.py")
    print("2. If all tests pass, run: python clean_and_ingest.py")
    print("3. Start the API server: python api_server.py")

def create_env_file():
    """Create a .env file with required variables."""
    
    env_content = """# ECSS Standards Navigator Environment Variables
# Replace with your actual Morphik URI
MORPHIK_URI=https://your-morphik-instance.com

# Optional: API Configuration
API_HOST=localhost
API_PORT=5000
DEBUG=True

# Optional: Logging
LOG_LEVEL=INFO
"""

# Add backend root to path



import os
import sys

def setup_environment():
    """Set up environment variables for the ECSS Standards Navigator."""
    
    print("🔧 Setting up ECSS Standards Navigator Environment")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    # Load environment variables
        
    # Validate required variables
    validate_environment()
    
    print("\n✅ Environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python test_pre_ingestion.py")
    print("2. If all tests pass, run: python clean_and_ingest.py")
    print("3. Start the API server: python api_server.py")

def create_env_file():
    """Create a .env file with required variables."""
    
    env_content = """# ECSS Standards Navigator Environment Variables
# Replace with your actual Morphik URI
MORPHIK_URI=https://your-morphik-instance.com

# Optional: API Configuration
API_HOST=localhost
API_PORT=5000
DEBUG=True

# Optional: Logging
LOG_LEVEL=INFO
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("📝 Created .env file. Please edit it with your Morphik URI.")

def :
    """Load environment variables from .env file."""
    try:
                        print("✅ Loaded environment variables from .env")
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        print("   Environment variables must be set manually.")

def validate_environment():
    """Validate that required environment variables are set."""
    
    print("\n🔍 Validating environment variables...")
    
    required_vars = {
        "MORPHIK_URI": "Morphik instance URI (required for document ingestion and queries)"
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "uri" in var.lower() or "url" in var.lower():
                masked_value = value[:20] + "..." if len(value) > 20 else value
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET - {description}")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please edit the .env file and set these variables.")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True

if __name__ == "__main__":
    setup_environment() 
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("📝 Created .env file. Please edit it with your Morphik URI.")

def :
    """Load environment variables from .env file."""
    try:
                        print("✅ Loaded environment variables from .env")
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        print("   Environment variables must be set manually.")

def validate_environment():
    """Validate that required environment variables are set."""
    
    print("\n🔍 Validating environment variables...")
    
    required_vars = {
        "MORPHIK_URI": "Morphik instance URI (required for document ingestion and queries)"
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "uri" in var.lower() or "url" in var.lower():
                masked_value = value[:20] + "..." if len(value) > 20 else value
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET - {description}")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please edit the .env file and set these variables.")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True

if __name__ == "__main__":
    setup_environment() 