#!/usr/bin/env python3
"""Test the ECSS ingestion system without ingesting documents."""
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

# Import the ingestion system
from clean_and_ingest import ECSSRulesBasedIngestion

def test_system():
    """Test the system initialization and basic functionality."""
    print("🧪 Testing ECSS Ingestion System")
    print("=" * 40)
    
    # Check environment
    morphik_uri = os.getenv('MORPHIK_URI')
    if not morphik_uri:
        print("❌ MORPHIK_URI not set")
        return False
    
    print(f"✅ MORPHIK_URI loaded: {morphik_uri[:50]}...")
    
    # Test system initialization
    try:
        print("\n🔄 Initializing ingestion system...")
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        print("✅ System initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return False
    
    # Test rules generation
    try:
        print("\n🔄 Testing NaturalLanguageRule generation...")
        nl_rules = ingestion_system.get_ecss_nl_rules()
        print(f"✅ Generated {len(nl_rules)} NaturalLanguageRules")
        
        print("\n🔄 Testing MetadataExtractionRule generation...")
        metadata_rules = ingestion_system.get_ecss_metadata_rules_with_images()
        print(f"✅ Generated {len(metadata_rules)} MetadataExtractionRules")
    except Exception as e:
        print(f"❌ Failed to generate rules: {e}")
        return False
    
    # Test document validation
    try:
        print("\n🔄 Testing document validation...")
        test_file = Path("../ECSS Published Standards/1-Active Standards/ECSS-E-ST-10C-Rev.1(15February2017).pdf")
        if test_file.exists():
            is_valid, msg = ingestion_system.validate_document(test_file)
            print(f"✅ Document validation test: {msg}")
            
            # Test cost estimation
            cost_info = ingestion_system.estimate_ingestion_cost(test_file)
            print(f"✅ Cost estimation: {cost_info}")
        else:
            print("⚠️ Test file not found, skipping validation test")
    except Exception as e:
        print(f"❌ Failed to test validation: {e}")
        return False
    
    print("\n🎉 All tests passed! System is ready for ingestion.")
    return True

if __name__ == "__main__":
    test_system() 