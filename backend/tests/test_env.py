
# Add backend root to path


#!/usr/bin/env python3
"""Simple script to test .env file loading."""

import os
import sys

print("Testing .env file loading...")

morphik_uri = os.getenv('MORPHIK_URI')
print(f"MORPHIK_URI: {morphik_uri}")

if morphik_uri:
    print("✅ .env file loaded successfully!")
else:
    print("❌ MORPHIK_URI not found in .env file") 
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


import os
import sys

print("Testing .env file loading...")

morphik_uri = os.getenv('MORPHIK_URI')
print(f"MORPHIK_URI: {morphik_uri}")

if morphik_uri:
    print("✅ .env file loaded successfully!")
else:
    print("❌ MORPHIK_URI not found in .env file") 