#!/usr/bin/env python3
"""
Script to fix environment file paths in moved files to look in the config/ directory.
"""

import os
import re
from pathlib import Path

def fix_env_paths():
    """Fix environment file paths in all moved files."""
    
    # Get the backend directory (parent of this script)
    backend_dir = Path(__file__).parent
    
    # Define the directories to process
    directories = ['tests', 'debug', 'analysis', 'core']
    
    for subdir in directories:
        subdir_path = backend_dir / subdir
        if not subdir_path.exists():
            continue
            
        print(f"Processing {subdir}...")
        
        # Process all Python files in the subdirectory
        for py_file in subdir_path.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            print(f"  Fixing {py_file.name}")
            
            # Read the file
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix .env file loading
            # Pattern 1: load_dotenv() without path
            if 'load_dotenv()' in content and 'load_dotenv(' not in content:
                # Find the line with load_dotenv()
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'load_dotenv()' in line and 'load_dotenv(' not in line:
                        # Replace with load_dotenv that points to config/.env
                        lines[i] = line.replace(
                            'load_dotenv()',
                            'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")'
                        )
                        print(f"    Fixed load_dotenv() in {py_file.name}")
                content = '\n'.join(lines)
            
            # Pattern 2: load_dotenv with existing path
            old_dotenv_pattern = r'load_dotenv\(dotenv_path\s*=\s*Path\(__file__\)\.parent\.parent\s*/\s*"\.env"\)'
            new_dotenv_pattern = 'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")'
            
            if re.search(old_dotenv_pattern, content):
                content = re.sub(old_dotenv_pattern, new_dotenv_pattern, content)
                print(f"    Fixed load_dotenv path in {py_file.name}")
            
            # Pattern 3: load_dotenv with dotenv_path but wrong path
            old_dotenv_pattern2 = r'load_dotenv\(dotenv_path\s*=\s*Path\(__file__\)\.parent\s*/\s*"\.env"\)'
            new_dotenv_pattern2 = 'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")'
            
            if re.search(old_dotenv_pattern2, content):
                content = re.sub(old_dotenv_pattern2, new_dotenv_pattern2, content)
                print(f"    Fixed load_dotenv path in {py_file.name}")
            
            # Fix morphik.toml references
            # Pattern 1: morphik.toml in current directory
            old_morphik_pattern = r'Path\(__file__\)\.parent\s*/\s*"morphik\.toml"'
            new_morphik_pattern = 'Path(__file__).parent.parent / "config" / "morphik.toml"'
            
            if re.search(old_morphik_pattern, content):
                content = re.sub(old_morphik_pattern, new_morphik_pattern, content)
                print(f"    Fixed morphik.toml path in {py_file.name}")
            
            # Pattern 2: morphik.toml without Path
            old_morphik_pattern2 = r'"morphik\.toml"'
            new_morphik_pattern2 = 'str(Path(__file__).parent.parent / "config" / "morphik.toml")'
            
            # Only replace if it's not already in a Path() call
            if '"morphik.toml"' in content and 'Path(' not in content:
                content = content.replace('"morphik.toml"', new_morphik_pattern2)
                print(f"    Fixed morphik.toml reference in {py_file.name}")
            
            # Write the fixed content back
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_env_paths()
    print("Environment path fixing completed!") 