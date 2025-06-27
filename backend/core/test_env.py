#!/usr/bin/env python3
"""Test environment loading."""
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

# Check environment variables
morphik_uri = os.getenv('MORPHIK_URI')
print(f"MORPHIK_URI: {morphik_uri[:50] + '...' if morphik_uri else 'Not set'}")

# Check if .env file exists
env_file = Path(__file__).parent.parent / "config" / ".env"
print(f"Env file exists: {env_file.exists()}")
if env_file.exists():
    print(f"Env file size: {env_file.stat().st_size} bytes") 