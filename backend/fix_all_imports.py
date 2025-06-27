#!/usr/bin/env python3
"""
Comprehensive script to fix all import paths and ensure backend root is in sys.path for all scripts.
"""

import os
import re
from pathlib import Path

def fix_all_imports():
    """Fix all import paths and sys.path for all scripts."""
    
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
            
            # Ensure the environment block is at the very top (after shebang and docstring)
            env_block = (
                'from pathlib import Path\n'
                'from dotenv import load_dotenv\n'
                'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")\n'
            )
            
            # Remove any existing environment loading code
            content = re.sub(r'from pathlib import Path\n?', '', content)
            content = re.sub(r'from dotenv import load_dotenv\n?', '', content)
            content = re.sub(r'load_dotenv\([^)]*\)\n?', '', content)
            
            # Find the shebang and docstring
            lines = content.split('\n')
            insert_at = 0
            
            # Skip shebang if present
            if lines and lines[0].startswith('#!'):
                insert_at = 1
                
            # Skip docstring if present
            if insert_at < len(lines) and (lines[insert_at].startswith('"""') or lines[insert_at].startswith("'''")):
                # Find the end of the docstring
                docstring_start = insert_at
                docstring_end = docstring_start
                for i in range(docstring_start + 1, len(lines)):
                    if lines[i].startswith('"""') or lines[i].startswith("'''"):
                        docstring_end = i
                        break
                insert_at = docstring_end + 1
            
            # Insert the environment block
            lines.insert(insert_at, env_block)
            content = '\n'.join(lines)
            
            # Ensure sys.path includes backend root
            if 'sys.path.insert(0, str(backend_dir.parent))' not in content:
                # Add sys import if not present
                if 'import sys' not in content:
                    content = content.replace('import os', 'import os\nimport sys')
                
                # Add the sys.path line after the environment block
                content = content.replace(
                    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")',
                    'load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")\n\n# Add backend root to path\nbackend_dir = Path(__file__).parent.parent\nsys.path.insert(0, str(backend_dir))'
                )
            
            # Fix local imports to use the correct paths
            # Replace direct imports with proper paths
            import_fixes = [
                ('from schemas import', 'from core.schemas import'),
                ('from ecss_rules_schema import', 'from core.ecss_rules_schema import'),
                ('from optimized_graph_strategy import', 'from core.optimized_graph_strategy import'),
                ('from enhanced_schema import', 'from core.enhanced_schema import'),
                ('from enhanced_extraction_prompt import', 'from core.enhanced_extraction_prompt import'),
                ('from ecss_graph_prompts import', 'from core.ecss_graph_prompts import'),
                ('from clean_and_ingest import', 'from core.clean_and_ingest import'),
                ('from api_server import', 'from core.api_server import'),
                ('from working_', 'from core.working_'),
                ('from check_', 'from core.check_'),
                ('from setup_environment import', 'from core.setup_environment import'),
                ('from explore_morphik import', 'from core.explore_morphik import'),
                ('from extract_morphik_images import', 'from core.extract_morphik_images import'),
                ('from inspect_chunks import', 'from core.inspect_chunks import'),
                ('from delete_document import', 'from core.delete_document import'),
                ('from demo_search_functionality import', 'from core.demo_search_functionality import'),
            ]
            
            for old_import, new_import in import_fixes:
                content = content.replace(old_import, new_import)
            
            # Write the fixed content back
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_all_imports()
    print("All import paths fixed!") 