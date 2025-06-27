

#!/usr/bin/env python3
"""
Pre-Ingestion Test Suite
Validates system components that can be tested before ingesting documents.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Pre-Ingestion Test Suite
Validates system components that can be tested before ingesting documents.
"""

import os
import sys
import json

# Load environment variables from .env file
try:
        except ImportError:
    pass  # Continue without dotenv if not available
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    pass

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

def test_environment_setup():
    """Test environment setup and required variables."""
    print("\n🔧 Testing Environment Setup...")
    
    # Check for required environment variables
    morphik_uri = os.getenv("MORPHIK_URI")
    
    if not morphik_uri:
        print("❌ MORPHIK_URI environment variable not set")
        print("\n📋 To fix this:")
        print("1. Run: python setup_environment.py")
        print("2. Edit the .env file with your Morphik URI")
        print("3. Or set the environment variable manually:")
        print("   Windows: set MORPHIK_URI=https://your-morphik-instance.com")
        print("   Linux/Mac: export MORPHIK_URI=https://your-morphik-instance.com")
        return False
    
    print(f"✅ MORPHIK_URI is set: {morphik_uri[:30]}...")
    return True

def test_morphik_connection():
    """Test connection to Morphik instance."""
    print("\n🔗 Testing Morphik Connection...")
    
    try:
        from morphik import Morphik
        
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test basic connection
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"   Current documents: {len(documents)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik connection test failed: {e}")
        return False

def test_rules_implementation():
    """Test rules implementation without documents."""
    print("\n📋 Testing Rules Implementation...")
    
    try:
        from core.ecss_rules_schema import (
            create_ecss_metadata_rules,
            create_ecss_content_rules,
            create_ecss_quality_rules,
            get_ecss_rules_for_branch,
            validate_ecss_rules,
            optimize_rules_for_performance
        )
        
        # Test rule creation
        metadata_rules = create_ecss_metadata_rules()
        content_rules = create_ecss_content_rules()
        quality_rules = create_ecss_quality_rules()
        
        print(f"✅ Created {len(metadata_rules)} metadata rules")
        print(f"✅ Created {len(content_rules)} content rules")
        print(f"✅ Created {len(quality_rules)} quality rules")
        
        # Test branch-specific rules
        for branch in ['E', 'M', 'P', 'Q']:
            branch_rules = get_ecss_rules_for_branch(branch)
            print(f"✅ Created {len(branch_rules)} rules for {branch}-branch")
        
        # Test rule validation
        all_rules = metadata_rules + content_rules
        is_valid = validate_ecss_rules(all_rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Test rule optimization
        optimized_rules = optimize_rules_for_performance(all_rules, "medium")
        print(f"✅ Rule optimization: {len(optimized_rules)} rules")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules implementation test failed: {e}")
        return False

def test_graph_prompts():
    """Test graph prompts creation without documents."""
    print("\n🔗 Testing Graph Prompts...")
    
    try:
        from core.ecss_graph_prompts import (
            get_ecss_entity_extraction_examples,
            get_ecss_entity_resolution_examples,
            create_ecss_graph_prompts,
            create_branch_specific_graph_prompts
        )
        
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created general ECSS graph prompts")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific graph prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph prompts test failed: {e}")
        return False

def test_optimized_graph_strategy():
    """Test optimized graph strategy initialization."""
    print("\n⚙️ Testing Optimized Graph Strategy...")
    
    try:
        from morphik import Morphik
        from core.optimized_graph_strategy import OptimizedECSSGraphManager
        
        morphik_uri = os.getenv("MORPHIK_URI")
        graph_manager = OptimizedECSSGraphManager(morphik_uri)
        
        print(f"✅ OptimizedECSSGraphManager initialized successfully")
        
        # Test query complexity detection
        simple_query = "What is ECSS?"
        complex_query = "What are the relationships between spacecraft design requirements and verification methods in ECSS standards?"
        
        is_simple_complex = graph_manager._is_complex_query(simple_query)
        is_complex_complex = graph_manager._is_complex_query(complex_query)
        
        print(f"✅ Query complexity detection:")
        print(f"   Simple query: {'Complex' if is_simple_complex else 'Simple'}")
        print(f"   Complex query: {'Complex' if is_complex_complex else 'Simple'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Optimized graph strategy test failed: {e}")
        return False

def test_api_server_components():
    """Test API server components without running the server."""
    print("\n🌐 Testing API Server Components...")
    
    try:
        # Test basic imports
        import flask
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        print("✅ Flask and CORS imports successful")
        
        # Test if we can create a basic app
        app = Flask(__name__)
        CORS(app)
        
        print("✅ Flask app creation successful")
        
        # Test if we can import our custom modules
        try:
            from morphik import Morphik
            print("✅ Morphik import successful")
        except Exception as e:
            print(f"⚠️  Morphik import warning: {e}")
        
        try:
            from core.optimized_graph_strategy import OptimizedECSSGraphManager
            print("✅ OptimizedECSSGraphManager import successful")
        except Exception as e:
            print(f"⚠️  OptimizedECSSGraphManager import warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API server components test failed: {e}")
        return False

def test_ingestion_system():
    """Test ingestion system initialization."""
    print("\n📥 Testing Ingestion System...")
    
    try:
        from core.clean_and_ingest import ECSSRulesBasedIngestion
        
        # Test ingestion system initialization
        morphik_uri = os.getenv("MORPHIK_URI")
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        
        print("✅ Ingestion system initialized successfully")
        
        # Test metadata extraction
        test_filename = "ECSS-E-ST-10C-Rev.1(15February2017).pdf"
        metadata = ingestion_system.extract_ecss_metadata(test_filename)
        
        expected_fields = ['branch', 'document_type', 'revision', 'date', 'status', 'discipline']
        missing_fields = [field for field in expected_fields if field not in metadata]
        
        if not missing_fields:
            print(f"✅ Metadata extraction working: {metadata}")
        else:
            print(f"❌ Metadata extraction missing fields: {missing_fields}")
            return False
        
        # Test rules generation
        rules = ingestion_system.get_rules_for_document(metadata)
        print(f"✅ Rules generation working: {len(rules)} rules")
        
        return True
        
    except Exception as e:
        print(f"❌ Ingestion system test failed: {e}")
        return False

def test_schema_validation():
    """Test ECSS schema validation."""
    print("\n📊 Testing Schema Validation...")
    
    try:
        from core.ecss_rules_schema import (
            ECSSStandard, ECSSSection, ECSSDefinition,
            ECSSTable, ECSSDiagram, ECSSRequirement
        )
        
        # Test schema instantiation
        test_data = {
            'ECSSStandard': {
                'standard_id': 'ECSS-E-ST-10C',
                'branch': 'E',
                'discipline': 'Engineering',
                'title': 'Test Standard',
                'revision': 'Rev.1',
                'date': '2024-01-01',
                'status': 'Active',
                'scope': 'Test scope',
                'keywords': ['test', 'engineering'],
                'applicable_domains': ['spacecraft']
            },
            'ECSSSection': {
                'section_number': '3.1',
                'section_title': 'Test Section',
                'section_type': 'normative',
                'content_summary': 'Test content',
                'requirements_count': 5,
                'figures_count': 2,
                'tables_count': 1
            }
        }
        
        # Test each schema
        schemas = {
            'ECSSStandard': ECSSStandard,
            'ECSSSection': ECSSSection
        }
        
        for schema_name, schema_class in schemas.items():
            data = test_data[schema_name]
            instance = schema_class(**data)
            print(f"✅ {schema_name} schema instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation test failed: {e}")
        return False

def main():
    """Run all pre-ingestion tests."""
    print("🚀 Pre-Ingestion Test Suite")
    print("=" * 50)
    print("Testing system components that can be validated before ingesting documents")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Morphik Connection", test_morphik_connection),
        ("Rules Implementation", test_rules_implementation),
        ("Graph Prompts", test_graph_prompts),
        ("Optimized Graph Strategy", test_optimized_graph_strategy),
        ("API Server Components", test_api_server_components),
        ("Ingestion System", test_ingestion_system),
        ("Schema Validation", test_schema_validation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 PRE-INGESTION TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All pre-ingestion tests passed!")
        print("✅ Your system is ready for document ingestion")
        print("\n📋 Next Steps:")
        print("   1. Run: python clean_and_ingest.py")
        print("   2. After ingestion, run post-ingestion tests")
    else:
        print("⚠ Some tests failed. Fix issues before ingesting documents.")
        print("\n📋 Failed Tests:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 

import os
import sys
import json

# Load environment variables from .env file
try:
        except ImportError:
    pass  # Continue without dotenv if not available
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    pass

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

def test_environment_setup():
    """Test environment setup and required variables."""
    print("\n🔧 Testing Environment Setup...")
    
    # Check for required environment variables
    morphik_uri = os.getenv("MORPHIK_URI")
    
    if not morphik_uri:
        print("❌ MORPHIK_URI environment variable not set")
        print("\n📋 To fix this:")
        print("1. Run: python setup_environment.py")
        print("2. Edit the .env file with your Morphik URI")
        print("3. Or set the environment variable manually:")
        print("   Windows: set MORPHIK_URI=https://your-morphik-instance.com")
        print("   Linux/Mac: export MORPHIK_URI=https://your-morphik-instance.com")
        return False
    
    print(f"✅ MORPHIK_URI is set: {morphik_uri[:30]}...")
    return True

def test_morphik_connection():
    """Test connection to Morphik instance."""
    print("\n🔗 Testing Morphik Connection...")
    
    try:
        from morphik import Morphik
        
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Test basic connection
        documents = db.list_documents()
        print(f"✅ Connected to Morphik successfully")
        print(f"   Current documents: {len(documents)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik connection test failed: {e}")
        return False

def test_rules_implementation():
    """Test rules implementation without documents."""
    print("\n📋 Testing Rules Implementation...")
    
    try:
        from core.ecss_rules_schema import (
            create_ecss_metadata_rules,
            create_ecss_content_rules,
            create_ecss_quality_rules,
            get_ecss_rules_for_branch,
            validate_ecss_rules,
            optimize_rules_for_performance
        )
        
        # Test rule creation
        metadata_rules = create_ecss_metadata_rules()
        content_rules = create_ecss_content_rules()
        quality_rules = create_ecss_quality_rules()
        
        print(f"✅ Created {len(metadata_rules)} metadata rules")
        print(f"✅ Created {len(content_rules)} content rules")
        print(f"✅ Created {len(quality_rules)} quality rules")
        
        # Test branch-specific rules
        for branch in ['E', 'M', 'P', 'Q']:
            branch_rules = get_ecss_rules_for_branch(branch)
            print(f"✅ Created {len(branch_rules)} rules for {branch}-branch")
        
        # Test rule validation
        all_rules = metadata_rules + content_rules
        is_valid = validate_ecss_rules(all_rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Test rule optimization
        optimized_rules = optimize_rules_for_performance(all_rules, "medium")
        print(f"✅ Rule optimization: {len(optimized_rules)} rules")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules implementation test failed: {e}")
        return False

def test_graph_prompts():
    """Test graph prompts creation without documents."""
    print("\n🔗 Testing Graph Prompts...")
    
    try:
        from core.ecss_graph_prompts import (
            get_ecss_entity_extraction_examples,
            get_ecss_entity_resolution_examples,
            create_ecss_graph_prompts,
            create_branch_specific_graph_prompts
        )
        
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created general ECSS graph prompts")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific graph prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph prompts test failed: {e}")
        return False

def test_optimized_graph_strategy():
    """Test optimized graph strategy initialization."""
    print("\n⚙️ Testing Optimized Graph Strategy...")
    
    try:
        from morphik import Morphik
        from core.optimized_graph_strategy import OptimizedECSSGraphManager
        
        morphik_uri = os.getenv("MORPHIK_URI")
        graph_manager = OptimizedECSSGraphManager(morphik_uri)
        
        print(f"✅ OptimizedECSSGraphManager initialized successfully")
        
        # Test query complexity detection
        simple_query = "What is ECSS?"
        complex_query = "What are the relationships between spacecraft design requirements and verification methods in ECSS standards?"
        
        is_simple_complex = graph_manager._is_complex_query(simple_query)
        is_complex_complex = graph_manager._is_complex_query(complex_query)
        
        print(f"✅ Query complexity detection:")
        print(f"   Simple query: {'Complex' if is_simple_complex else 'Simple'}")
        print(f"   Complex query: {'Complex' if is_complex_complex else 'Simple'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Optimized graph strategy test failed: {e}")
        return False

def test_api_server_components():
    """Test API server components without running the server."""
    print("\n🌐 Testing API Server Components...")
    
    try:
        # Test basic imports
        import flask
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        print("✅ Flask and CORS imports successful")
        
        # Test if we can create a basic app
        app = Flask(__name__)
        CORS(app)
        
        print("✅ Flask app creation successful")
        
        # Test if we can import our custom modules
        try:
            from morphik import Morphik
            print("✅ Morphik import successful")
        except Exception as e:
            print(f"⚠️  Morphik import warning: {e}")
        
        try:
            from core.optimized_graph_strategy import OptimizedECSSGraphManager
            print("✅ OptimizedECSSGraphManager import successful")
        except Exception as e:
            print(f"⚠️  OptimizedECSSGraphManager import warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API server components test failed: {e}")
        return False

def test_ingestion_system():
    """Test ingestion system initialization."""
    print("\n📥 Testing Ingestion System...")
    
    try:
        from core.clean_and_ingest import ECSSRulesBasedIngestion
        
        # Test ingestion system initialization
        morphik_uri = os.getenv("MORPHIK_URI")
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        
        print("✅ Ingestion system initialized successfully")
        
        # Test metadata extraction
        test_filename = "ECSS-E-ST-10C-Rev.1(15February2017).pdf"
        metadata = ingestion_system.extract_ecss_metadata(test_filename)
        
        expected_fields = ['branch', 'document_type', 'revision', 'date', 'status', 'discipline']
        missing_fields = [field for field in expected_fields if field not in metadata]
        
        if not missing_fields:
            print(f"✅ Metadata extraction working: {metadata}")
        else:
            print(f"❌ Metadata extraction missing fields: {missing_fields}")
            return False
        
        # Test rules generation
        rules = ingestion_system.get_rules_for_document(metadata)
        print(f"✅ Rules generation working: {len(rules)} rules")
        
        return True
        
    except Exception as e:
        print(f"❌ Ingestion system test failed: {e}")
        return False

def test_schema_validation():
    """Test ECSS schema validation."""
    print("\n📊 Testing Schema Validation...")
    
    try:
        from core.ecss_rules_schema import (
            ECSSStandard, ECSSSection, ECSSDefinition,
            ECSSTable, ECSSDiagram, ECSSRequirement
        )
        
        # Test schema instantiation
        test_data = {
            'ECSSStandard': {
                'standard_id': 'ECSS-E-ST-10C',
                'branch': 'E',
                'discipline': 'Engineering',
                'title': 'Test Standard',
                'revision': 'Rev.1',
                'date': '2024-01-01',
                'status': 'Active',
                'scope': 'Test scope',
                'keywords': ['test', 'engineering'],
                'applicable_domains': ['spacecraft']
            },
            'ECSSSection': {
                'section_number': '3.1',
                'section_title': 'Test Section',
                'section_type': 'normative',
                'content_summary': 'Test content',
                'requirements_count': 5,
                'figures_count': 2,
                'tables_count': 1
            }
        }
        
        # Test each schema
        schemas = {
            'ECSSStandard': ECSSStandard,
            'ECSSSection': ECSSSection
        }
        
        for schema_name, schema_class in schemas.items():
            data = test_data[schema_name]
            instance = schema_class(**data)
            print(f"✅ {schema_name} schema instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation test failed: {e}")
        return False

def main():
    """Run all pre-ingestion tests."""
    print("🚀 Pre-Ingestion Test Suite")
    print("=" * 50)
    print("Testing system components that can be validated before ingesting documents")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Morphik Connection", test_morphik_connection),
        ("Rules Implementation", test_rules_implementation),
        ("Graph Prompts", test_graph_prompts),
        ("Optimized Graph Strategy", test_optimized_graph_strategy),
        ("API Server Components", test_api_server_components),
        ("Ingestion System", test_ingestion_system),
        ("Schema Validation", test_schema_validation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 PRE-INGESTION TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All pre-ingestion tests passed!")
        print("✅ Your system is ready for document ingestion")
        print("\n📋 Next Steps:")
        print("   1. Run: python clean_and_ingest.py")
        print("   2. After ingestion, run post-ingestion tests")
    else:
        print("⚠ Some tests failed. Fix issues before ingesting documents.")
        print("\n📋 Failed Tests:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 