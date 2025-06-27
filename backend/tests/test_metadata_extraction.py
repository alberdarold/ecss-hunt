from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))



print("[DEBUG] Script started")

import os
import sys
from datetime import datetime

print("[DEBUG] Imports completed")

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
        print("[DEBUG] dotenv loaded from root")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))
print("[DEBUG] Backend dir added to sys.path")

from morphik import Morphik
from core.ecss_rules_schema import create_ecss_metadata_rules
print("[DEBUG] Morphik and rules imported")

def test_metadata_extraction():
    print("[DEBUG] test_metadata_extraction() called")
    # ... rest of function unchanged ...

def test_ingestion_with_metadata():
    print("[DEBUG] test_ingestion_with_metadata() called")
    # ... rest of function unchanged ...

def main():
    print("[DEBUG] main() called")
    # Test 1: Check existing documents
    print("[DEBUG] Calling test_metadata_extraction()")
    success1 = test_metadata_extraction()
    print(f"[DEBUG] test_metadata_extraction() returned: {success1}")
    # Test 2: Test new ingestion with metadata
    print("[DEBUG] Calling test_ingestion_with_metadata()")
    success2 = test_ingestion_with_metadata()
    print(f"[DEBUG] test_ingestion_with_metadata() returned: {success2}")
    if success1 and success2:
        print("\n🎉 All tests passed!")
        print("✅ Metadata extraction is working correctly")
    else:
        print("\n❌ Some tests failed!")
        print("⚠️  Check the output above for details")

if __name__ == "__main__":
    print("[DEBUG] __main__ entrypoint")
    main() 