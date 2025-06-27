#!/usr/bin/env python3
"""
Script to ensure all scripts in core/, debug/, analysis/, and tests/ load the .env file from config/ at the top of the file, if not already present.
"""

from pathlib import Path
import re

ENV_BLOCK = (
    'from pathlib import Path\n'
    'from dotenv import load_dotenv\n'
    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")\n'
)

# Directories to process
TARGET_DIRS = ["core", "debug", "analysis", "tests"]

for subdir in TARGET_DIRS:
    dir_path = Path(__file__).parent / subdir
    if not dir_path.exists():
        continue
    for py_file in dir_path.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Check if the env block is already present
        if 'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")' in content:
            continue
        # Remove any old load_dotenv() or load_dotenv(dotenv_path=...) lines
        content = re.sub(r'from dotenv import load_dotenv\n?', '', content)
        content = re.sub(r'load_dotenv\([^)]+\)\n?', '', content)
        content = re.sub(r'load_dotenv\(\)\n?', '', content)
        content = re.sub(r'from pathlib import Path\n?', '', content)
        # Insert the ENV_BLOCK after the first docstring or at the top
        docstring_match = re.match(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', content)
        if docstring_match:
            insert_at = docstring_match.end()
            new_content = content[:insert_at] + '\n' + ENV_BLOCK + content[insert_at:]
        else:
            new_content = ENV_BLOCK + '\n' + content
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(new_content)
print("✅ All scripts now load .env from config/ at the top.") 