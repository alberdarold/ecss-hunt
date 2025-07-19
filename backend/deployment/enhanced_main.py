#!/usr/bin/env python3
"""
Enhanced Morphik Production Entry Point
=====================================

This starts the enhanced API server with full Morphik feature utilization.
"""
import sys
import os
from pathlib import Path

# Add backend core to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir / "core"))

from experimental.morphik_enhanced_legacy.api_server import main

if __name__ == "__main__":
    main()
