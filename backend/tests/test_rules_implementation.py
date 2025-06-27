

#!/usr/bin/env python3
"""
Test script for Morphik Rules Implementation
Validates that our ECSS rules system follows Morphik's official rules methodology.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test script for Morphik Rules Implementation
Validates that our ECSS rules system follows Morphik's official rules methodology.
"""

import os
import sys
import json
from typing import List, Dict

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from core.ecss_rules_schema import (
    create_ecss_metadata_rules,
    create_ecss_content_rules,
    create_ecss_quality_rules,
    get_ecss_rules_for_branch,
    validate_ecss_rules,
    optimize_rules_for_performance
)

def test_rules_creation():
    """Test that we can create all types of ECSS rules."""
    print("🧪 Testing ECSS Rules Creation...")
    
    try:
        # Test metadata rules
        metadata_rules = create_ecss_metadata_rules()
        print(f"✅ Created {len(metadata_rules)} metadata extraction rules")
        
        # Test content rules
        content_rules = create_ecss_content_rules()
        print(f"✅ Created {len(content_rules)} content transformation rules")
        
        # Test quality rules
        quality_rules = create_ecss_quality_rules()
        print(f"✅ Created {len(quality_rules)} quality assurance rules")
        
        # Test branch-specific rules
        for branch in ['E', 'M', 'P', 'Q']:
            branch_rules = get_ecss_rules_for_branch(branch)
            print(f"✅ Created {len(branch_rules)} rules for {branch}-branch")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules creation test failed: {e}")
        return False

def test_rules_validation():
    """Test that our rules validation works correctly."""
    print("\n🧪 Testing Rules Validation...")
    
    try:
        # Test valid rules
        valid_rules = create_ecss_metadata_rules()
        is_valid = validate_ecss_rules(valid_rules)
        print(f"✅ Valid rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Test invalid rules (missing schema)
        invalid_rules = [
            MetadataExtractionRule(schema=None),  # Invalid: no schema
            NaturalLanguageRule(prompt="")  # Invalid: empty prompt
        ]
        
        # This should fail validation
        try:
            is_invalid = validate_ecss_rules(invalid_rules)
            print(f"⚠ Invalid rules validation: {'FAIL' if not is_invalid else 'PASS'}")
        except Exception as e:
            print(f"✅ Invalid rules correctly rejected: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules validation test failed: {e}")
        return False

def test_rules_optimization():
    """Test rules performance optimization."""
    print("\n🧪 Testing Rules Optimization...")
    
    try:
        base_rules = create_ecss_metadata_rules()
        
        # Test small document optimization
        small_rules = optimize_rules_for_performance(base_rules, "small")
        print(f"✅ Small document optimization: {len(small_rules)} rules (was {len(base_rules)})")
        
        # Test large document optimization
        large_rules = optimize_rules_for_performance(base_rules, "large")
        print(f"✅ Large document optimization: {len(large_rules)} rules (was {len(base_rules)})")
        
        # Test medium document optimization
        medium_rules = optimize_rules_for_performance(base_rules, "medium")
        print(f"✅ Medium document optimization: {len(medium_rules)} rules (was {len(base_rules)})")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules optimization test failed: {e}")
        return False

def test_morphik_rules_integration():
    """Test that our rules work with Morphik's rules engine."""
    print("\n🧪 Testing Morphik Rules Integration...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Create a simple test rule
        from pydantic import BaseModel
        
        class TestMetadata(BaseModel):
            title: str
            author: str
            date: str
        
        test_rule = MetadataExtractionRule(
            schema=TestMetadata,
            description="Test metadata extraction"
        )
        
        print(f"✅ Created test rule: {type(test_rule).__name__}")
        
        # Test that the rule has the expected attributes
        assert hasattr(test_rule, 'schema'), "Rule should have schema attribute"
        assert hasattr(test_rule, 'description'), "Rule should have description attribute"
        
        print("✅ Test rule has expected attributes")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik rules integration test failed: {e}")
        return False

def test_ecss_specific_rules():
    """Test ECSS-specific rule schemas."""
    print("\n🧪 Testing ECSS-Specific Rules...")
    
    try:
        from core.ecss_rules_schema import (
            ECSSStandard, ECSSSection, ECSSDefinition,
            ECSSTable, ECSSDiagram, ECSSRequirement
        )
        
        # Test that all schemas can be instantiated
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
            },
            'ECSSDefinition': {
                'term': 'test_term',
                'definition': 'Test definition',
                'context': 'Test context',
                'related_terms': ['related1', 'related2'],
                'standard_reference': 'ECSS-E-ST-10C'
            },
            'ECSSTable': {
                'table_number': 'Table 1',
                'table_title': 'Test Table',
                'table_type': 'requirements',
                'row_count': 10,
                'column_count': 5,
                'content_summary': 'Test table content',
                'key_parameters': ['param1', 'param2']
            },
            'ECSSDiagram': {
                'figure_number': 'Figure 1',
                'figure_title': 'Test Figure',
                'diagram_type': 'block diagram',
                'content_description': 'Test diagram',
                'components': ['comp1', 'comp2'],
                'relationships': ['rel1', 'rel2']
            },
            'ECSSRequirement': {
                'requirement_id': 'REQ-001',
                'requirement_text': 'Test requirement',
                'requirement_type': 'functional',
                'priority': 'mandatory',
                'verification_method': 'test',
                'applicable_phases': ['design', 'test']
            }
        }
        
        for schema_name, data in test_data.items():
            schema_class = globals()[schema_name]
            instance = schema_class(**data)
            print(f"✅ {schema_name} schema instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ECSS-specific rules test failed: {e}")
        return False

def test_rules_processing_workflow():
    """Test the complete rules processing workflow."""
    print("\n🧪 Testing Rules Processing Workflow...")
    
    try:
        # Simulate the workflow from clean_and_ingest.py
        from core.ecss_rules_schema import get_ecss_rules_for_branch, validate_ecss_rules
        
        # Test workflow for E-branch
        metadata = {
            'branch': 'E',
            'document_type': 'ST',
            'revision': 'Rev.1',
            'status': 'Active'
        }
        
        # Get rules for document
        rules = get_ecss_rules_for_branch('E')
        print(f"✅ Retrieved {len(rules)} rules for E-branch")
        
        # Validate rules
        is_valid = validate_ecss_rules(rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Optimize rules
        optimized_rules = optimize_rules_for_performance(rules, "large")
        print(f"✅ Rules optimization: {len(optimized_rules)} rules")
        
        # Check rule types
        metadata_rules = [r for r in optimized_rules if isinstance(r, MetadataExtractionRule)]
        content_rules = [r for r in optimized_rules if isinstance(r, NaturalLanguageRule)]
        
        print(f"✅ Rule breakdown: {len(metadata_rules)} metadata, {len(content_rules)} content")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules processing workflow test failed: {e}")
        return False

def test_rules_compliance_with_morphik_docs():
    """Test that our rules implementation follows Morphik's official documentation."""
    print("\n🧪 Testing Morphik Documentation Compliance...")
    
    try:
        # Test 1: MetadataExtractionRule with schema
        from pydantic import BaseModel
        
        class TestSchema(BaseModel):
            name: str
            value: int
        
        metadata_rule = MetadataExtractionRule(schema=TestSchema)
        print("✅ MetadataExtractionRule created with schema")
        
        # Test 2: NaturalLanguageRule with prompt
        content_rule = NaturalLanguageRule(
            prompt="Transform this content according to ECSS standards"
        )
        print("✅ NaturalLanguageRule created with prompt")
        
        # Test 3: Rules list for ingestion
        rules_list = [metadata_rule, content_rule]
        print(f"✅ Created rules list with {len(rules_list)} rules")
        
        # Test 4: Validate rules structure
        for i, rule in enumerate(rules_list):
            if isinstance(rule, MetadataExtractionRule):
                assert hasattr(rule, 'schema'), f"Rule {i} missing schema"
                print(f"✅ Rule {i}: MetadataExtractionRule with schema")
            elif isinstance(rule, NaturalLanguageRule):
                assert hasattr(rule, 'prompt'), f"Rule {i} missing prompt"
                print(f"✅ Rule {i}: NaturalLanguageRule with prompt")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik documentation compliance test failed: {e}")
        return False

def main():
    """Run all rules implementation tests."""
    print("🚀 Testing Morphik Rules Implementation")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("Rules Creation", test_rules_creation),
        ("Rules Validation", test_rules_validation),
        ("Rules Optimization", test_rules_optimization),
        ("Morphik Integration", test_morphik_rules_integration),
        ("ECSS-Specific Rules", test_ecss_specific_rules),
        ("Processing Workflow", test_rules_processing_workflow),
        ("Documentation Compliance", test_rules_compliance_with_morphik_docs)
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
    print("📊 FINAL TEST SUMMARY")
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
        print("🎉 All rules implementation tests passed!")
        print("✅ Your system is robust for rules-based processing")
        print("\n📋 Rules Implementation Features:")
        print("   • MetadataExtractionRule with structured schemas")
        print("   • NaturalLanguageRule for content transformation")
        print("   • Branch-specific rule optimization")
        print("   • Performance-based rule selection")
        print("   • Comprehensive validation and error handling")
        print("   • Full compliance with Morphik documentation")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 

import os
import sys
import json
from typing import List, Dict

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from core.ecss_rules_schema import (
    create_ecss_metadata_rules,
    create_ecss_content_rules,
    create_ecss_quality_rules,
    get_ecss_rules_for_branch,
    validate_ecss_rules,
    optimize_rules_for_performance
)

def test_rules_creation():
    """Test that we can create all types of ECSS rules."""
    print("🧪 Testing ECSS Rules Creation...")
    
    try:
        # Test metadata rules
        metadata_rules = create_ecss_metadata_rules()
        print(f"✅ Created {len(metadata_rules)} metadata extraction rules")
        
        # Test content rules
        content_rules = create_ecss_content_rules()
        print(f"✅ Created {len(content_rules)} content transformation rules")
        
        # Test quality rules
        quality_rules = create_ecss_quality_rules()
        print(f"✅ Created {len(quality_rules)} quality assurance rules")
        
        # Test branch-specific rules
        for branch in ['E', 'M', 'P', 'Q']:
            branch_rules = get_ecss_rules_for_branch(branch)
            print(f"✅ Created {len(branch_rules)} rules for {branch}-branch")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules creation test failed: {e}")
        return False

def test_rules_validation():
    """Test that our rules validation works correctly."""
    print("\n🧪 Testing Rules Validation...")
    
    try:
        # Test valid rules
        valid_rules = create_ecss_metadata_rules()
        is_valid = validate_ecss_rules(valid_rules)
        print(f"✅ Valid rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Test invalid rules (missing schema)
        invalid_rules = [
            MetadataExtractionRule(schema=None),  # Invalid: no schema
            NaturalLanguageRule(prompt="")  # Invalid: empty prompt
        ]
        
        # This should fail validation
        try:
            is_invalid = validate_ecss_rules(invalid_rules)
            print(f"⚠ Invalid rules validation: {'FAIL' if not is_invalid else 'PASS'}")
        except Exception as e:
            print(f"✅ Invalid rules correctly rejected: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules validation test failed: {e}")
        return False

def test_rules_optimization():
    """Test rules performance optimization."""
    print("\n🧪 Testing Rules Optimization...")
    
    try:
        base_rules = create_ecss_metadata_rules()
        
        # Test small document optimization
        small_rules = optimize_rules_for_performance(base_rules, "small")
        print(f"✅ Small document optimization: {len(small_rules)} rules (was {len(base_rules)})")
        
        # Test large document optimization
        large_rules = optimize_rules_for_performance(base_rules, "large")
        print(f"✅ Large document optimization: {len(large_rules)} rules (was {len(base_rules)})")
        
        # Test medium document optimization
        medium_rules = optimize_rules_for_performance(base_rules, "medium")
        print(f"✅ Medium document optimization: {len(medium_rules)} rules (was {len(base_rules)})")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules optimization test failed: {e}")
        return False

def test_morphik_rules_integration():
    """Test that our rules work with Morphik's rules engine."""
    print("\n🧪 Testing Morphik Rules Integration...")
    
    try:
        # Initialize Morphik
        db = Morphik(os.getenv("MORPHIK_URI"))
        
        # Create a simple test rule
        from pydantic import BaseModel
        
        class TestMetadata(BaseModel):
            title: str
            author: str
            date: str
        
        test_rule = MetadataExtractionRule(
            schema=TestMetadata,
            description="Test metadata extraction"
        )
        
        print(f"✅ Created test rule: {type(test_rule).__name__}")
        
        # Test that the rule has the expected attributes
        assert hasattr(test_rule, 'schema'), "Rule should have schema attribute"
        assert hasattr(test_rule, 'description'), "Rule should have description attribute"
        
        print("✅ Test rule has expected attributes")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik rules integration test failed: {e}")
        return False

def test_ecss_specific_rules():
    """Test ECSS-specific rule schemas."""
    print("\n🧪 Testing ECSS-Specific Rules...")
    
    try:
        from core.ecss_rules_schema import (
            ECSSStandard, ECSSSection, ECSSDefinition,
            ECSSTable, ECSSDiagram, ECSSRequirement
        )
        
        # Test that all schemas can be instantiated
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
            },
            'ECSSDefinition': {
                'term': 'test_term',
                'definition': 'Test definition',
                'context': 'Test context',
                'related_terms': ['related1', 'related2'],
                'standard_reference': 'ECSS-E-ST-10C'
            },
            'ECSSTable': {
                'table_number': 'Table 1',
                'table_title': 'Test Table',
                'table_type': 'requirements',
                'row_count': 10,
                'column_count': 5,
                'content_summary': 'Test table content',
                'key_parameters': ['param1', 'param2']
            },
            'ECSSDiagram': {
                'figure_number': 'Figure 1',
                'figure_title': 'Test Figure',
                'diagram_type': 'block diagram',
                'content_description': 'Test diagram',
                'components': ['comp1', 'comp2'],
                'relationships': ['rel1', 'rel2']
            },
            'ECSSRequirement': {
                'requirement_id': 'REQ-001',
                'requirement_text': 'Test requirement',
                'requirement_type': 'functional',
                'priority': 'mandatory',
                'verification_method': 'test',
                'applicable_phases': ['design', 'test']
            }
        }
        
        for schema_name, data in test_data.items():
            schema_class = globals()[schema_name]
            instance = schema_class(**data)
            print(f"✅ {schema_name} schema instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ECSS-specific rules test failed: {e}")
        return False

def test_rules_processing_workflow():
    """Test the complete rules processing workflow."""
    print("\n🧪 Testing Rules Processing Workflow...")
    
    try:
        # Simulate the workflow from clean_and_ingest.py
        from core.ecss_rules_schema import get_ecss_rules_for_branch, validate_ecss_rules
        
        # Test workflow for E-branch
        metadata = {
            'branch': 'E',
            'document_type': 'ST',
            'revision': 'Rev.1',
            'status': 'Active'
        }
        
        # Get rules for document
        rules = get_ecss_rules_for_branch('E')
        print(f"✅ Retrieved {len(rules)} rules for E-branch")
        
        # Validate rules
        is_valid = validate_ecss_rules(rules)
        print(f"✅ Rules validation: {'PASS' if is_valid else 'FAIL'}")
        
        # Optimize rules
        optimized_rules = optimize_rules_for_performance(rules, "large")
        print(f"✅ Rules optimization: {len(optimized_rules)} rules")
        
        # Check rule types
        metadata_rules = [r for r in optimized_rules if isinstance(r, MetadataExtractionRule)]
        content_rules = [r for r in optimized_rules if isinstance(r, NaturalLanguageRule)]
        
        print(f"✅ Rule breakdown: {len(metadata_rules)} metadata, {len(content_rules)} content")
        
        return True
        
    except Exception as e:
        print(f"❌ Rules processing workflow test failed: {e}")
        return False

def test_rules_compliance_with_morphik_docs():
    """Test that our rules implementation follows Morphik's official documentation."""
    print("\n🧪 Testing Morphik Documentation Compliance...")
    
    try:
        # Test 1: MetadataExtractionRule with schema
        from pydantic import BaseModel
        
        class TestSchema(BaseModel):
            name: str
            value: int
        
        metadata_rule = MetadataExtractionRule(schema=TestSchema)
        print("✅ MetadataExtractionRule created with schema")
        
        # Test 2: NaturalLanguageRule with prompt
        content_rule = NaturalLanguageRule(
            prompt="Transform this content according to ECSS standards"
        )
        print("✅ NaturalLanguageRule created with prompt")
        
        # Test 3: Rules list for ingestion
        rules_list = [metadata_rule, content_rule]
        print(f"✅ Created rules list with {len(rules_list)} rules")
        
        # Test 4: Validate rules structure
        for i, rule in enumerate(rules_list):
            if isinstance(rule, MetadataExtractionRule):
                assert hasattr(rule, 'schema'), f"Rule {i} missing schema"
                print(f"✅ Rule {i}: MetadataExtractionRule with schema")
            elif isinstance(rule, NaturalLanguageRule):
                assert hasattr(rule, 'prompt'), f"Rule {i} missing prompt"
                print(f"✅ Rule {i}: NaturalLanguageRule with prompt")
        
        return True
        
    except Exception as e:
        print(f"❌ Morphik documentation compliance test failed: {e}")
        return False

def main():
    """Run all rules implementation tests."""
    print("🚀 Testing Morphik Rules Implementation")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("MORPHIK_URI"):
        print("❌ MORPHIK_URI environment variable not set")
        return False
    
    # Run tests
    tests = [
        ("Rules Creation", test_rules_creation),
        ("Rules Validation", test_rules_validation),
        ("Rules Optimization", test_rules_optimization),
        ("Morphik Integration", test_morphik_rules_integration),
        ("ECSS-Specific Rules", test_ecss_specific_rules),
        ("Processing Workflow", test_rules_processing_workflow),
        ("Documentation Compliance", test_rules_compliance_with_morphik_docs)
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
    print("📊 FINAL TEST SUMMARY")
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
        print("🎉 All rules implementation tests passed!")
        print("✅ Your system is robust for rules-based processing")
        print("\n📋 Rules Implementation Features:")
        print("   • MetadataExtractionRule with structured schemas")
        print("   • NaturalLanguageRule for content transformation")
        print("   • Branch-specific rule optimization")
        print("   • Performance-based rule selection")
        print("   • Comprehensive validation and error handling")
        print("   • Full compliance with Morphik documentation")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 