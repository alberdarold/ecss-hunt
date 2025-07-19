#!/usr/bin/env python3
"""
PROJECT ORGANIZATION SCRIPT
===========================

Reorganizes the backend project structure while maintaining all imports and functionality.
"""
import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Set

class ProjectOrganizer:
    """Organizes the project structure and fixes imports."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.moves = {}  # old_path -> new_path
        self.import_fixes = {}  # file_path -> list of import replacements
        
    def create_structure(self):
        """Create the new directory structure."""
        directories = [
            "production",
            "experimental", 
            "ingestion/production",
            "ingestion/experimental", 
            "ingestion/legacy",
            "utils/cleanup",
            "utils/testing", 
            "utils/fixes",
            "deployment",
            "logs",
            "legacy"
        ]
        
        print("🗂️ Creating directory structure...")
        for dir_path in directories:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ {dir_path}")
    
    def define_file_moves(self):
        """Define where each file should be moved."""
        
        # Production-ready systems (confirmed working)
        production_files = [
            "working_morphik_system.py",
            "production_working_api.py", 
            "core/production_api_server.py",
            "core/ecss_foundation_system.py",
        ]
        
        # Experimental/advanced features  
        experimental_files = [
            "core/morphik_advanced_system.py",
            "core/morphik_enhanced_api_server.py",
        ]
        
        # Cleanup utilities
        cleanup_files = [
            "alternative_document_cleanup.py",
            "targeted_graph_cleanup.py",
            "cleanup_runaway_graphs.py",
        ]
        
        # Testing utilities
        testing_files = [
            "test_morphik_methods.py", 
            "test_morphik_connection.py",
            "test_enhanced_system.py",
            "core/test_foundation_system.py",
            "core/test_morphik_native_capabilities.py",
            "core/test_enhanced_image_processing.py",
            "core/working_text_extraction.py",  # Text extraction testing
        ]
        
        # Fix utilities
        fix_files = [
            "fix_all_imports.py",
            "fix_remaining_issues.py", 
            "fix_env_paths.py",
        ]
        
        # Deployment scripts
        deployment_files = [
            "deploy_foundation_system.py",
            "deploy_enhanced_morphik.py",
            "enhanced_main.py",
            "main.py",
        ]
        
        # Log files and results
        log_files = [
            "*.log",
            "core/*.log",
            "core/simplified_ingestion_results_*.json",
            "core/image_ingestion_results_*.json",
            "core/morphik_native_visual_fixed_results_*.json",
        ]
        
        # Ingestion systems - PRODUCTION READY
        ingestion_production_files = [
            "core/working_ingestion_with_image_support.py",  # MetadataExtractionRule + ColPali
            "core/working_ingestion_with_nl_rules.py",       # NaturalLanguageRule approach
            "core/ecss_batch_ingestion.py",                  # Production batch ingestion
            "core/clean_and_ingest.py",                      # Smart fallback system
        ]
        
        # Ingestion systems - EXPERIMENTAL/ENHANCED  
        ingestion_experimental_files = [
            "core/enhanced_simplified_ingestion.py",         # Enhanced with OCR
            "core/morphik_native_simplified_ingestion.py",   # Native multimodal
            "core/ecss_simplified_ingestion.py",             # Simplified ColPali
            "core/morphik_native_visual_processor.py",       # Native visual processing
            "core/morphik_visual_content_processor.py",      # Visual content processor
        ]
        
        # Ingestion systems - LEGACY (truly deprecated)
        ingestion_legacy_files = [
            # Add any truly old ingestion methods here
        ]
        
        # Legacy files (non-ingestion deprecated code)
        legacy_files = [
            "core/enhanced_image_processor.py",
            "core/api_server.py",  # Old API server
            "core/enhanced_api_server.py",  # Old enhanced API
        ]
        
        # Map files to new locations
        for file in production_files:
            self.moves[file] = f"production/{Path(file).name}"
            
        for file in experimental_files:
            self.moves[file] = f"experimental/{Path(file).name}"
            
        for file in ingestion_production_files:
            self.moves[file] = f"ingestion/production/{Path(file).name}"
            
        for file in ingestion_experimental_files:
            self.moves[file] = f"ingestion/experimental/{Path(file).name}"
            
        for file in ingestion_legacy_files:
            self.moves[file] = f"ingestion/legacy/{Path(file).name}"
            
        for file in cleanup_files:
            self.moves[file] = f"utils/cleanup/{Path(file).name}"
            
        for file in testing_files:
            self.moves[file] = f"utils/testing/{Path(file).name}"
            
        for file in fix_files:
            self.moves[file] = f"utils/fixes/{Path(file).name}"
            
        for file in deployment_files:
            self.moves[file] = f"deployment/{Path(file).name}"
            
        for file in legacy_files:
            self.moves[file] = f"legacy/{Path(file).name}"
        
        # Handle log files and results separately (they use wildcards)
        # These will be handled in move_log_files method
    
    def analyze_imports(self, file_path: Path) -> List[str]:
        """Analyze imports in a Python file."""
        if not file_path.exists() or file_path.suffix != '.py':
            return []
        
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all import statements
            import_patterns = [
                r'^from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+import',
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)',
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.extend(matches)
                
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            
        return imports
    
    def calculate_import_fixes(self):
        """Calculate what import statements need to be updated."""
        print("🔍 Analyzing imports...")
        
        # Create mapping of module names to new paths
        module_map = {}
        for old_path, new_path in self.moves.items():
            old_name = Path(old_path).stem
            new_location = Path(new_path).parent
            module_map[old_name] = str(new_location).replace('/', '.').replace('\\', '.')
        
        # Check each file that will be moved
        for old_path, new_path in self.moves.items():
            file_path = self.base_path / old_path
            if not file_path.exists():
                continue
                
            imports = self.analyze_imports(file_path)
            fixes = []
            
            for imp in imports:
                # Check if this import refers to a file we're moving
                for module, new_loc in module_map.items():
                    if module in imp:
                        old_import = imp
                        new_import = imp.replace(module, f"{new_loc}.{module}")
                        fixes.append((old_import, new_import))
            
            if fixes:
                self.import_fixes[new_path] = fixes
    
    def preview_changes(self):
        """Preview all changes that will be made."""
        print("\n📋 ORGANIZATION PREVIEW")
        print("=" * 50)
        
        print("\n📦 Files to Move:")
        for old_path, new_path in self.moves.items():
            file_path = self.base_path / old_path
            status = "✅" if file_path.exists() else "❓"
            print(f"  {status} {old_path} → {new_path}")
        
        print("\n🔧 Import Fixes Needed:")
        for file_path, fixes in self.import_fixes.items():
            print(f"  📄 {file_path}:")
            for old_imp, new_imp in fixes:
                print(f"    {old_imp} → {new_imp}")
        
        print(f"\n📊 Summary:")
        print(f"  • Files to move: {len(self.moves)}")
        print(f"  • Files needing import fixes: {len(self.import_fixes)}")
        
    def execute_organization(self, dry_run: bool = True):
        """Execute the reorganization."""
        if dry_run:
            print("\n🧪 DRY RUN - No files will be moved")
            self.preview_changes()
            return
        
        print("\n🚀 Executing organization...")
        
        # Move files
        for old_path, new_path in self.moves.items():
            old_file = self.base_path / old_path
            new_file = self.base_path / new_path
            
            if old_file.exists():
                # Ensure target directory exists
                new_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(old_file), str(new_file))
                print(f"✅ Moved: {old_path} → {new_path}")
            else:
                print(f"⚠️ Not found: {old_path}")
        
        # Fix imports
        for file_path, fixes in self.import_fixes.items():
            full_path = self.base_path / file_path
            if full_path.exists():
                self.fix_imports_in_file(full_path, fixes)
        
        # Move log files and results
        self.move_log_files()
    
    def fix_imports_in_file(self, file_path: Path, fixes: List[tuple]):
        """Fix imports in a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old_import, new_import in fixes:
                content = content.replace(old_import, new_import)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"🔧 Fixed imports in: {file_path}")
            
        except Exception as e:
            print(f"❌ Error fixing imports in {file_path}: {e}")
    
    def move_log_files(self):
        """Move log files and result files to logs directory."""
        log_patterns = [
            "*.log",
            "core/*.log", 
            "core/simplified_ingestion_results_*.json",
            "core/image_ingestion_results_*.json",
            "core/morphik_native_visual_fixed_results_*.json",
        ]
        
        import glob
        
        for pattern in log_patterns:
            files = glob.glob(str(self.base_path / pattern))
            for file_path in files:
                file_obj = Path(file_path)
                if file_obj.exists():
                    target_path = self.base_path / "logs" / file_obj.name
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.move(str(file_obj), str(target_path))
                        print(f"📋 Moved log: {file_obj.name} → logs/")
                    except Exception as e:
                        print(f"⚠️ Could not move {file_obj.name}: {e}")

def main():
    """Main organization function."""
    print("🗂️ BACKEND PROJECT ORGANIZER")
    print("=" * 50)
    
    organizer = ProjectOrganizer(".")
    
    # Step 1: Create directory structure
    organizer.create_structure()
    
    # Step 2: Define file moves
    organizer.define_file_moves()
    
    # Step 3: Analyze imports
    organizer.calculate_import_fixes()
    
    # Step 4: Preview changes
    organizer.preview_changes()
    
    # Step 5: Ask for confirmation
    print("\n❓ Execute this organization? (y/N): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        organizer.execute_organization(dry_run=False)
        print("\n✅ Organization complete!")
        print("💡 Test your systems to ensure everything still works")
    else:
        print("\n❌ Organization cancelled")

if __name__ == "__main__":
    main() 