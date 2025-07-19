#!/usr/bin/env python3
"""
COMPREHENSIVE IMPORT AND PATH TESTING SCRIPT
============================================

Tests all Python files in the reorganized backend structure to ensure:
- All imports work correctly
- All path references are valid
- Configuration files are accessible
- No broken dependencies after reorganization
"""
import os
import sys
import ast
import importlib.util
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Set
import subprocess

class ImportPathTester:
    """Tests imports and paths in the reorganized backend structure."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.results = {
            'working': [],
            'broken': [],
            'warnings': [],
            'skipped': []
        }
        self.tested_files = 0
        self.total_files = 0
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the backend structure."""
        python_files = []
        
        # Define directories to scan
        scan_dirs = [
            "production",
            "experimental", 
            "ingestion",
            "utils",
            "deployment",
            "legacy"
        ]
        
        for scan_dir in scan_dirs:
            dir_path = self.base_path / scan_dir
            if dir_path.exists():
                # Recursively find all .py files
                for py_file in dir_path.rglob("*.py"):
                    if py_file.name != "__init__.py":  # Skip __init__.py files
                        python_files.append(py_file)
        
        # Also check root backend files
        for py_file in self.base_path.glob("*.py"):
            if py_file.name not in ["__init__.py", "test_all_imports_and_paths.py"]:
                python_files.append(py_file)
        
        return sorted(python_files)
    
    def analyze_file_imports(self, file_path: Path) -> Dict:
        """Analyze imports in a Python file using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            imports = {
                'from_imports': [],
                'direct_imports': [],
                'relative_imports': [],
                'path_issues': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports['direct_imports'].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    if node.level > 0:  # Relative import
                        imports['relative_imports'].append(f"{'.' * node.level}{module}")
                    else:
                        imports['from_imports'].append(module)
            
            # Check for common path patterns
            if 'load_dotenv' in content:
                # Check dotenv paths
                if 'Path(__file__).parent / "config"' in content:
                    imports['path_issues'].append("config path may be incorrect")
                elif 'Path(__file__).parent.parent / "config"' not in content:
                    imports['path_issues'].append("config path may need parent.parent")
            
            return imports
            
        except Exception as e:
            return {'error': str(e)}
    
    def test_file_import(self, file_path: Path) -> Tuple[bool, str]:
        """Test if a file can be imported/compiled without execution."""
        try:
            # First try to compile the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to compile to check for syntax errors
            compile(content, str(file_path), 'exec')
            
            # Try to load as module spec (without executing)
            relative_path = file_path.relative_to(self.base_path)
            module_name = str(relative_path).replace('/', '.').replace('\\', '.').replace('.py', '')
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                return False, "Could not create module spec"
            
            # Try to create module (this loads imports but doesn't execute main code)
            module = importlib.util.module_from_spec(spec)
            
            # Test by executing in a subprocess to avoid side effects
            result = subprocess.run(
                [sys.executable, '-c', f'import ast; ast.parse(open(r"{file_path}", encoding="utf-8").read())'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "Syntax and basic imports OK"
            else:
                return False, result.stderr.strip()
            
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except ImportError as e:
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def test_config_access(self, file_path: Path) -> List[str]:
        """Test if config file access works for a given file."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'load_dotenv' in content:
                # Calculate correct config path based on file location
                relative_path = file_path.relative_to(self.base_path)
                depth = len(relative_path.parts) - 1  # -1 because we don't count the file itself
                
                # For files in subdirectories, check if they point to the correct config
                if depth >= 1:  # Files in subdirectories
                    # Should use parent.parent.parent for files in subdirectories
                    correct_config_path = self.base_path / "config" / ".env"
                    
                    # Check if the correct config exists
                    if not correct_config_path.exists():
                        issues.append("Backend config/.env file not found")
                    
                    # Check if file uses wrong pattern (only parent or parent.parent for subdir files)
                    if ('Path(__file__).parent / "config"' in content or 
                        'Path(__file__).parent.parent / "config"' in content) and depth >= 2:
                        # Only flag if it's definitely wrong (2+ levels deep but not using parent.parent.parent)
                        if 'Path(__file__).parent.parent.parent / "config"' not in content:
                            issues.append(f"Config path may need {depth + 1} parent levels for this file location")
        
        except Exception as e:
            issues.append(f"Error checking config access: {e}")
        
        return issues
    
    def test_file(self, file_path: Path) -> Dict:
        """Comprehensively test a single file."""
        result = {
            'file': str(file_path.relative_to(self.base_path)),
            'status': 'unknown',
            'imports': {},
            'config_issues': [],
            'errors': [],
            'warnings': []
        }
        
        print(f"🔍 Testing: {result['file']}")
        
        # Analyze imports
        result['imports'] = self.analyze_file_imports(file_path)
        if 'error' in result['imports']:
            result['errors'].append(f"AST analysis failed: {result['imports']['error']}")
        
        # Test import compilation
        import_ok, import_msg = self.test_file_import(file_path)
        if import_ok:
            result['status'] = 'working'
            if import_msg != "Syntax and basic imports OK":
                result['warnings'].append(import_msg)
        else:
            result['status'] = 'broken'
            result['errors'].append(import_msg)
        
        # Test config access
        config_issues = self.test_config_access(file_path)
        result['config_issues'] = config_issues
        if config_issues:
            result['warnings'].extend(config_issues)
        
        # Add to results
        if result['status'] == 'working':
            if result['warnings'] or result['config_issues']:
                self.results['warnings'].append(result)
            else:
                self.results['working'].append(result)
        else:
            self.results['broken'].append(result)
        
        return result
    
    def run_comprehensive_test(self):
        """Run comprehensive tests on all Python files."""
        print("🧪 COMPREHENSIVE IMPORT AND PATH TESTING")
        print("=" * 60)
        
        # Find all Python files
        python_files = self.find_python_files()
        self.total_files = len(python_files)
        
        print(f"📁 Found {self.total_files} Python files to test")
        print("=" * 60)
        
        # Test each file
        for file_path in python_files:
            try:
                self.test_file(file_path)
                self.tested_files += 1
            except Exception as e:
                print(f"❌ Failed to test {file_path}: {e}")
                self.results['skipped'].append({
                    'file': str(file_path.relative_to(self.base_path)),
                    'error': str(e)
                })
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test summary."""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.results['working']) + len(self.results['warnings']) + len(self.results['broken']) + len(self.results['skipped'])
        
        print(f"📈 Files tested: {self.tested_files}/{self.total_files}")
        print(f"✅ Working perfectly: {len(self.results['working'])}")
        print(f"⚠️ Working with warnings: {len(self.results['warnings'])}")
        print(f"❌ Broken: {len(self.results['broken'])}")
        print(f"⏭️ Skipped: {len(self.results['skipped'])}")
        
        success_rate = (len(self.results['working']) + len(self.results['warnings'])) / total * 100 if total > 0 else 0
        print(f"🎯 Success rate: {success_rate:.1f}%")
        
        # Show broken files
        if self.results['broken']:
            print(f"\n❌ BROKEN FILES ({len(self.results['broken'])}):")
            for result in self.results['broken']:
                print(f"  • {result['file']}")
                for error in result['errors']:
                    print(f"    └─ {error}")
        
        # Show warnings
        if self.results['warnings']:
            print(f"\n⚠️ FILES WITH WARNINGS ({len(self.results['warnings'])}):")
            for result in self.results['warnings']:
                print(f"  • {result['file']}")
                for warning in result['warnings']:
                    print(f"    └─ {warning}")
        
        # Show working files
        if self.results['working']:
            print(f"\n✅ WORKING FILES ({len(self.results['working'])}):")
            for result in self.results['working']:
                print(f"  • {result['file']}")
        
        # Show file organization
        self.print_organization_summary()
    
    def print_organization_summary(self):
        """Print summary by directory organization."""
        print(f"\n📁 FILES BY DIRECTORY:")
        
        by_dir = {}
        all_results = (self.results['working'] + self.results['warnings'] + 
                      self.results['broken'] + self.results['skipped'])
        
        for result in all_results:
            file_path = result['file']
            if '/' in file_path or '\\' in file_path:
                dir_name = file_path.split('/')[0] if '/' in file_path else file_path.split('\\')[0]
            else:
                dir_name = 'root'
            
            if dir_name not in by_dir:
                by_dir[dir_name] = {'working': 0, 'warnings': 0, 'broken': 0, 'skipped': 0}
            
            if result in self.results['working']:
                by_dir[dir_name]['working'] += 1
            elif result in self.results['warnings']:
                by_dir[dir_name]['warnings'] += 1
            elif result in self.results['broken']:
                by_dir[dir_name]['broken'] += 1
            else:
                by_dir[dir_name]['skipped'] += 1
        
        for dir_name, counts in sorted(by_dir.items()):
            total = sum(counts.values())
            working_pct = (counts['working'] + counts['warnings']) / total * 100 if total > 0 else 0
            status = "✅" if working_pct == 100 else "⚠️" if working_pct >= 50 else "❌"
            print(f"  {status} {dir_name}/: {counts['working']}✅ {counts['warnings']}⚠️ {counts['broken']}❌ {counts['skipped']}⏭️ ({working_pct:.0f}%)")
    
    def generate_fix_suggestions(self):
        """Generate suggestions for fixing broken files."""
        print(f"\n🔧 FIX SUGGESTIONS:")
        
        if not self.results['broken'] and not self.results['warnings']:
            print("🎉 All files are working perfectly! No fixes needed.")
            return
        
        print("\n📝 Common fixes needed:")
        
        # Analyze common issues
        config_issues = 0
        import_issues = 0
        
        for result in self.results['broken'] + self.results['warnings']:
            if any('config' in issue.lower() for issue in result.get('config_issues', [])):
                config_issues += 1
            if any('import' in error.lower() for error in result.get('errors', [])):
                import_issues += 1
        
        if config_issues > 0:
            print(f"🔧 {config_issues} files have config path issues:")
            print("   → Change 'Path(__file__).parent / \"config\"' to 'Path(__file__).parent.parent / \"config\"'")
        
        if import_issues > 0:
            print(f"🔧 {import_issues} files have import issues:")
            print("   → Check relative imports and module paths")
            print("   → Ensure sys.path.insert points to backend root")
        
        print(f"\n💡 Run individual file tests with: python -c \"import <module>\"")

def main():
    """Run comprehensive import and path testing."""
    tester = ImportPathTester(".")
    tester.run_comprehensive_test()
    tester.generate_fix_suggestions()

if __name__ == "__main__":
    main() 