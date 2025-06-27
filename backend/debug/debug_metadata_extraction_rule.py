

#!/usr/bin/env python3
"""
Debug MetadataExtractionRule to understand why it returns schema definitions instead of extracted values
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug MetadataExtractionRule to understand why it returns schema definitions instead of extracted values
"""

import os
import sys
import time
import json

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

def debug_metadata_extraction_rule():
    """Debug why MetadataExtractionRule returns schema instead of extracted values."""
    print("🔍 Debugging MetadataExtractionRule")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Simple schema with minimal fields
    print("\n🧪 Test 1: Minimal Schema")
    print("-" * 30)
    
    class MinimalSchema(BaseModel):
        title: str = Field(description="Document title")
        date: str = Field(description="Publication date")
    
    minimal_rule = MetadataExtractionRule(schema=MinimalSchema)
    print(f"✅ Created minimal rule with schema: {MinimalSchema.__name__}")
    print(f"   Schema fields: {list(MinimalSchema.model_fields.keys())}")
    
    # Test 2: Schema with more descriptive fields
    print("\n🧪 Test 2: Descriptive Schema")
    print("-" * 30)
    
    class DescriptiveSchema(BaseModel):
        title: str = Field(description="The full title of the document")
        date: str = Field(description="The publication date of the document")
        summary: str = Field(description="A brief summary of the document content")
    
    descriptive_rule = MetadataExtractionRule(schema=DescriptiveSchema)
    print(f"✅ Created descriptive rule with schema: {DescriptiveSchema.__name__}")
    
    # Test 3: Schema with validation (fixed for Pydantic v2)
    print("\n🧪 Test 3: Schema with Validation")
    print("-" * 30)
    
    class ValidatedSchema(BaseModel):
        title: str = Field(description="Document title", min_length=1)
        date: str = Field(description="Publication date", pattern=r"\d{4}-\d{2}-\d{2}")
        summary: str = Field(description="Document summary", max_length=500)
    
    validated_rule = MetadataExtractionRule(schema=ValidatedSchema)
    print(f"✅ Created validated rule with schema: {ValidatedSchema.__name__}")
    
    # Test 4: Compare with NaturalLanguageRule
    print("\n🧪 Test 4: NaturalLanguageRule Comparison")
    print("-" * 30)
    
    nl_rule = NaturalLanguageRule(
        prompt="""Extract the following information from the document and return as JSON:
        {
            "title": "Document title",
            "date": "Publication date", 
            "summary": "Brief summary"
        }"""
    )
    print(f"✅ Created NaturalLanguageRule with prompt")
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    # Test all rules
    rules_to_test = [
        ("Minimal Schema", minimal_rule),
        ("Descriptive Schema", descriptive_rule), 
        ("Validated Schema", validated_rule),
        ("Natural Language", nl_rule)
    ]
    
    for rule_name, rule in rules_to_test:
        print(f"\n🔍 Testing: {rule_name}")
        print("-" * 20)
        
        try:
            # Ingest with rule
            doc = db.ingest_text(
                test_text, 
                filename=f"debug_{rule_name.lower().replace(' ', '_')}.txt",
                rules=[rule]
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            start_time = time.time()
            max_wait = 120
            
            while time.time() - start_time < max_wait:
                current_status = doc.status
                if isinstance(current_status, dict):
                    status_value = current_status.get('status', 'unknown')
                else:
                    status_value = current_status
                
                if status_value == 'completed':
                    print("✅ Processing completed!")
                    break
                elif status_value in ['failed', 'error']:
                    print(f"❌ Processing failed: {status_value}")
                    break
                
                time.sleep(5)
            else:
                print("❌ Processing timed out")
                continue
            
            # Check metadata
            print(f"🔍 Checking metadata...")
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
                
                # Analyze the metadata structure
                if isinstance(doc.metadata, dict):
                    print(f"📊 Metadata analysis:")
                    print(f"   Type: {type(doc.metadata)}")
                    print(f"   Keys: {list(doc.metadata.keys())}")
                    
                    # Check if it's schema definition or extracted data
                    if 'type' in doc.metadata and 'title' in doc.metadata and 'properties' in doc.metadata:
                        print(f"   ⚠️  This looks like a schema definition!")
                    elif 'title' in doc.metadata and isinstance(doc.metadata['title'], str) and len(doc.metadata['title']) > 10:
                        print(f"   ✅ This looks like extracted data!")
                    else:
                        print(f"   ❓ Unknown format")
            else:
                print("❌ No metadata found")
            
            # Check chunks for content
            print(f"🔍 Checking chunks...")
            chunks = db.retrieve_chunks("title")
            if chunks:
                print(f"✅ Found {len(chunks)} chunks")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        if isinstance(content, str) and len(content) > 50:
                            print(f"   Chunk {i+1}: {content[:100]}...")
                        else:
                            print(f"   Chunk {i+1}: {content}")
            else:
                print("❌ No chunks found")
                
        except Exception as e:
            print(f"❌ Error testing {rule_name}: {e}")
            import traceback
            traceback.print_exc()

def test_morphik_documentation_examples():
    """Test examples from Morphik documentation."""
    print("\n📚 Testing Morphik Documentation Examples")
    print("=" * 50)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Example from Morphik docs
    class DocumentInfo(BaseModel):
        title: str = Field(description="Document title")
        author: str = Field(description="Document author")
        date: str = Field(description="Publication date")
    
    rule = MetadataExtractionRule(schema=DocumentInfo)
    
    test_text = """
    Title: ECSS-E-ST-10C Rev.1
    Author: European Cooperation for Space Standardization
    Date: 15 February 2017
    
    This is a test document for metadata extraction.
    """
    
    try:
        doc = db.ingest_text(test_text, filename="docs_example.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < 120:
            status = doc.status
            if isinstance(status, dict):
                status_value = status.get('status', 'unknown')
            else:
                status_value = status
            
            if status_value == 'completed':
                print("✅ Processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return
            
            time.sleep(5)
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"📊 Documentation example metadata: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("❌ No metadata in documentation example")
            
    except Exception as e:
        print(f"❌ Documentation example failed: {e}")

if __name__ == "__main__":
    debug_metadata_extraction_rule()
    test_morphik_documentation_examples() 

import os
import sys
import time
import json

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

def debug_metadata_extraction_rule():
    """Debug why MetadataExtractionRule returns schema instead of extracted values."""
    print("🔍 Debugging MetadataExtractionRule")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Test 1: Simple schema with minimal fields
    print("\n🧪 Test 1: Minimal Schema")
    print("-" * 30)
    
    class MinimalSchema(BaseModel):
        title: str = Field(description="Document title")
        date: str = Field(description="Publication date")
    
    minimal_rule = MetadataExtractionRule(schema=MinimalSchema)
    print(f"✅ Created minimal rule with schema: {MinimalSchema.__name__}")
    print(f"   Schema fields: {list(MinimalSchema.model_fields.keys())}")
    
    # Test 2: Schema with more descriptive fields
    print("\n🧪 Test 2: Descriptive Schema")
    print("-" * 30)
    
    class DescriptiveSchema(BaseModel):
        title: str = Field(description="The full title of the document")
        date: str = Field(description="The publication date of the document")
        summary: str = Field(description="A brief summary of the document content")
    
    descriptive_rule = MetadataExtractionRule(schema=DescriptiveSchema)
    print(f"✅ Created descriptive rule with schema: {DescriptiveSchema.__name__}")
    
    # Test 3: Schema with validation (fixed for Pydantic v2)
    print("\n🧪 Test 3: Schema with Validation")
    print("-" * 30)
    
    class ValidatedSchema(BaseModel):
        title: str = Field(description="Document title", min_length=1)
        date: str = Field(description="Publication date", pattern=r"\d{4}-\d{2}-\d{2}")
        summary: str = Field(description="Document summary", max_length=500)
    
    validated_rule = MetadataExtractionRule(schema=ValidatedSchema)
    print(f"✅ Created validated rule with schema: {ValidatedSchema.__name__}")
    
    # Test 4: Compare with NaturalLanguageRule
    print("\n🧪 Test 4: NaturalLanguageRule Comparison")
    print("-" * 30)
    
    nl_rule = NaturalLanguageRule(
        prompt="""Extract the following information from the document and return as JSON:
        {
            "title": "Document title",
            "date": "Publication date", 
            "summary": "Brief summary"
        }"""
    )
    print(f"✅ Created NaturalLanguageRule with prompt")
    
    # Test text
    test_text = """
    ECSS-E-ST-10C Rev.1 (15 February 2017)
    European Cooperation for Space Standardization
    Space Engineering - System Engineering General Requirements
    
    This document defines the general requirements for system engineering in space projects.
    It covers requirements management, system design, verification, and validation.
    """
    
    # Test all rules
    rules_to_test = [
        ("Minimal Schema", minimal_rule),
        ("Descriptive Schema", descriptive_rule), 
        ("Validated Schema", validated_rule),
        ("Natural Language", nl_rule)
    ]
    
    for rule_name, rule in rules_to_test:
        print(f"\n🔍 Testing: {rule_name}")
        print("-" * 20)
        
        try:
            # Ingest with rule
            doc = db.ingest_text(
                test_text, 
                filename=f"debug_{rule_name.lower().replace(' ', '_')}.txt",
                rules=[rule]
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            start_time = time.time()
            max_wait = 120
            
            while time.time() - start_time < max_wait:
                current_status = doc.status
                if isinstance(current_status, dict):
                    status_value = current_status.get('status', 'unknown')
                else:
                    status_value = current_status
                
                if status_value == 'completed':
                    print("✅ Processing completed!")
                    break
                elif status_value in ['failed', 'error']:
                    print(f"❌ Processing failed: {status_value}")
                    break
                
                time.sleep(5)
            else:
                print("❌ Processing timed out")
                continue
            
            # Check metadata
            print(f"🔍 Checking metadata...")
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata found: {json.dumps(doc.metadata, indent=2)}")
                
                # Analyze the metadata structure
                if isinstance(doc.metadata, dict):
                    print(f"📊 Metadata analysis:")
                    print(f"   Type: {type(doc.metadata)}")
                    print(f"   Keys: {list(doc.metadata.keys())}")
                    
                    # Check if it's schema definition or extracted data
                    if 'type' in doc.metadata and 'title' in doc.metadata and 'properties' in doc.metadata:
                        print(f"   ⚠️  This looks like a schema definition!")
                    elif 'title' in doc.metadata and isinstance(doc.metadata['title'], str) and len(doc.metadata['title']) > 10:
                        print(f"   ✅ This looks like extracted data!")
                    else:
                        print(f"   ❓ Unknown format")
            else:
                print("❌ No metadata found")
            
            # Check chunks for content
            print(f"🔍 Checking chunks...")
            chunks = db.retrieve_chunks("title")
            if chunks:
                print(f"✅ Found {len(chunks)} chunks")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content'):
                        content = chunk.content
                        if isinstance(content, str) and len(content) > 50:
                            print(f"   Chunk {i+1}: {content[:100]}...")
                        else:
                            print(f"   Chunk {i+1}: {content}")
            else:
                print("❌ No chunks found")
                
        except Exception as e:
            print(f"❌ Error testing {rule_name}: {e}")
            import traceback
            traceback.print_exc()

def test_morphik_documentation_examples():
    """Test examples from Morphik documentation."""
    print("\n📚 Testing Morphik Documentation Examples")
    print("=" * 50)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Example from Morphik docs
    class DocumentInfo(BaseModel):
        title: str = Field(description="Document title")
        author: str = Field(description="Document author")
        date: str = Field(description="Publication date")
    
    rule = MetadataExtractionRule(schema=DocumentInfo)
    
    test_text = """
    Title: ECSS-E-ST-10C Rev.1
    Author: European Cooperation for Space Standardization
    Date: 15 February 2017
    
    This is a test document for metadata extraction.
    """
    
    try:
        doc = db.ingest_text(test_text, filename="docs_example.txt", rules=[rule])
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < 120:
            status = doc.status
            if isinstance(status, dict):
                status_value = status.get('status', 'unknown')
            else:
                status_value = status
            
            if status_value == 'completed':
                print("✅ Processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return
            
            time.sleep(5)
        
        # Check metadata
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"📊 Documentation example metadata: {json.dumps(doc.metadata, indent=2)}")
        else:
            print("❌ No metadata in documentation example")
            
    except Exception as e:
        print(f"❌ Documentation example failed: {e}")

if __name__ == "__main__":
    debug_metadata_extraction_rule()
    test_morphik_documentation_examples() 