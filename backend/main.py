#!/usr/bin/env python3
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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

# Import and run the production API server
from production_api_server import main

if __name__ == "__main__":
    main()
