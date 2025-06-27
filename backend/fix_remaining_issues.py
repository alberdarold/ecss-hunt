#!/usr/bin/env python3
"""
Script to fix all remaining syntax errors and missing imports across all scripts.
"""

import os
import re
from pathlib import Path

def fix_remaining_issues():
    """Fix all remaining syntax errors and missing imports."""
    
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
            
            # Fix 1: Remove stray .parent.parent / "config" / ".env") lines
            content = re.sub(r'\n\.parent\.parent / "config" / "\.env"\)\n?', '\n', content)
            
            # Fix 2: Ensure import sys is present before sys.path.insert
            if 'sys.path.insert' in content and 'import sys' not in content:
                # Add import sys after the environment block
                content = content.replace(
                    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")',
                    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")\n\nimport sys'
                )
            
            # Fix 3: Ensure proper structure - environment block should be after docstring
            lines = content.split('\n')
            new_lines = []
            env_block_added = False
            
            for i, line in enumerate(lines):
                # Skip shebang
                if line.startswith('#!'):
                    new_lines.append(line)
                    continue
                
                # Skip docstring
                if line.startswith('"""') or line.startswith("'''"):
                    new_lines.append(line)
                    # Find end of docstring
                    j = i + 1
                    while j < len(lines) and not (lines[j].startswith('"""') or lines[j].startswith("'''")):
                        new_lines.append(lines[j])
                        j += 1
                    if j < len(lines):
                        new_lines.append(lines[j])
                    
                    # Add environment block after docstring
                    if not env_block_added:
                        new_lines.extend([
                            'from pathlib import Path',
                            'from dotenv import load_dotenv',
                            'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")',
                            '',
                            'import sys',
                            '# Add backend root to path',
                            'backend_dir = Path(__file__).parent.parent',
                            'sys.path.insert(0, str(backend_dir))',
                            ''
                        ])
                        env_block_added = True
                    
                    # Skip the lines we've already processed
                    i = j
                    continue
                
                # Skip lines that are part of the old environment block
                if any(skip in line for skip in [
                    'from pathlib import Path',
                    'from dotenv import load_dotenv', 
                    'load_dotenv(',
                    'backend_dir = Path(__file__).parent.parent',
                    'sys.path.insert(0, str(backend_dir))'
                ]):
                    continue
                
                new_lines.append(line)
            
            # If no docstring found, add environment block at the beginning
            if not env_block_added:
                new_lines = [
                    'from pathlib import Path',
                    'from dotenv import load_dotenv', 
                    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")',
                    '',
                    'import sys',
                    '# Add backend root to path',
                    'backend_dir = Path(__file__).parent.parent',
                    'sys.path.insert(0, str(backend_dir))',
                    ''
                ] + new_lines
            
            content = '\n'.join(new_lines)
            
            # Write the fixed content back
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_remaining_issues()
    print("All remaining issues fixed!") 