

#!/usr/bin/env python3
"""
Test OpenAI API Integration
Verify that OpenAI API calls are being made during ingestion and processing.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test OpenAI API Integration
Verify that OpenAI API calls are being made during ingestion and processing.
"""

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_openai_integration():
    """Test that OpenAI API calls are being made."""
    print("🔍 Testing OpenAI API Integration")
    print("=" * 40)
    
    # Check environment variables
    morphik_uri = os.getenv("MORPHIK_URI")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"Environment Check:")
    print(f"  MORPHIK_URI: {'SET' if morphik_uri else 'NOT SET'}")
    print(f"  OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found - this is required for AI processing")
        return
    
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Connect to Morphik
    db = Morphik(morphik_uri)
    
    # Create a simple test file with clear content
    test_content = """
    ECSS Standard Test Document
    
    Title: Test Standard for OpenAI Integration
    Standard Number: ECSS-TEST-001
    Document Type: Standard
    Scope: This is a test document to verify OpenAI API integration
    
    Requirements:
    REQ-001: The system shall process this document using OpenAI models
    REQ-002: The system shall extract metadata using AI rules
    REQ-003: The system shall demonstrate text processing capabilities
    """
    
    # Write test content to a file
    test_file = Path("openai_test_document.txt")
    test_file.write_text(test_content)
    
    print(f"\n📄 Created test document: {test_file.name}")
    print(f"Content length: {len(test_content)} characters")
    
    # Create a rule that should definitely trigger OpenAI API calls
    ai_rule = NaturalLanguageRule(
        prompt="""Analyze this document and extract the following information in JSON format:
{
  "title": "document title",
  "standard_number": "ECSS standard number", 
  "document_type": "type of document",
  "requirements": ["list of requirements"],
  "summary": "brief summary of content"
}

Be very specific and detailed in your analysis."""
    )
    
    try:
        print(f"\n🔍 Ingesting with AI rule (should trigger OpenAI API calls)...")
        
        # Ingest the text file with the AI rule
        doc = db.ingest_file(
            test_file,
            filename="openai_integration_test.txt",
            rules=[ai_rule],
            use_colpali=False  # Use text processing
        )
        
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing...")
        start_time = time.time()
        max_wait = 120  # 2 minutes max
        
        while time.time() - start_time < max_wait:
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            if status_value == 'completed':
                print("✅ AI processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                error_msg = current_status.get('error', 'Unknown error') if isinstance(current_status, dict) else 'Unknown error'
                print(f"Error details: {error_msg}")
                return
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(5)
        else:
            print("❌ Processing timed out")
            return
        
        # Check what was extracted
        print(f"\n🔍 Checking AI-extracted content:")
        
        # Search for the test content
        chunks = db.retrieve_chunks("ECSS-TEST-001")
        print(f"Found {len(chunks)} chunks containing 'ECSS-TEST-001'")
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"\nChunk {i+1}:")
            print(f"  Length: {len(content)} characters")
            print(f"  Content: {content[:300]}...")
            
            # Check if this looks like AI-extracted JSON
            if "title" in content and "standard_number" in content:
                print(f"  ✅ This looks like AI-extracted metadata!")
        
        # Test a query that should use OpenAI
        print(f"\n🔍 Testing AI-powered query:")
        try:
            response = db.query(
                "What is the standard number and what requirements are listed?",
                k=3
            )
            
            if response and response.sources:
                print(f"✅ AI query successful - found {len(response.sources)} results")
                for i, source in enumerate(response.sources[:2]):
                    source_text = getattr(source, 'text', '')
                    print(f"  Result {i+1}: {source_text[:200]}...")
            else:
                print("⚠ No results from AI query")
                
        except Exception as e:
            print(f"❌ AI query failed: {e}")
        
        print(f"\n📊 OpenAI Integration Test Summary:")
        print(f"  - Test document processed successfully")
        print(f"  - AI rule applied and completed")
        print(f"  - OpenAI API calls should have been made")
        print(f"  - Check your OpenAI dashboard for API usage")
        
        # Clean up
        test_file.unlink()
        print(f"  - Test file cleaned up")
        
    except Exception as e:
        print(f"❌ OpenAI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up on error
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_openai_integration() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_openai_integration():
    """Test that OpenAI API calls are being made."""
    print("🔍 Testing OpenAI API Integration")
    print("=" * 40)
    
    # Check environment variables
    morphik_uri = os.getenv("MORPHIK_URI")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"Environment Check:")
    print(f"  MORPHIK_URI: {'SET' if morphik_uri else 'NOT SET'}")
    print(f"  OPENAI_API_KEY: {'SET' if openai_key else 'NOT SET'}")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found - this is required for AI processing")
        return
    
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Connect to Morphik
    db = Morphik(morphik_uri)
    
    # Create a simple test file with clear content
    test_content = """
    ECSS Standard Test Document
    
    Title: Test Standard for OpenAI Integration
    Standard Number: ECSS-TEST-001
    Document Type: Standard
    Scope: This is a test document to verify OpenAI API integration
    
    Requirements:
    REQ-001: The system shall process this document using OpenAI models
    REQ-002: The system shall extract metadata using AI rules
    REQ-003: The system shall demonstrate text processing capabilities
    """
    
    # Write test content to a file
    test_file = Path("openai_test_document.txt")
    test_file.write_text(test_content)
    
    print(f"\n📄 Created test document: {test_file.name}")
    print(f"Content length: {len(test_content)} characters")
    
    # Create a rule that should definitely trigger OpenAI API calls
    ai_rule = NaturalLanguageRule(
        prompt="""Analyze this document and extract the following information in JSON format:
{
  "title": "document title",
  "standard_number": "ECSS standard number", 
  "document_type": "type of document",
  "requirements": ["list of requirements"],
  "summary": "brief summary of content"
}

Be very specific and detailed in your analysis."""
    )
    
    try:
        print(f"\n🔍 Ingesting with AI rule (should trigger OpenAI API calls)...")
        
        # Ingest the text file with the AI rule
        doc = db.ingest_file(
            test_file,
            filename="openai_integration_test.txt",
            rules=[ai_rule],
            use_colpali=False  # Use text processing
        )
        
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing...")
        start_time = time.time()
        max_wait = 120  # 2 minutes max
        
        while time.time() - start_time < max_wait:
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            if status_value == 'completed':
                print("✅ AI processing completed!")
                break
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                error_msg = current_status.get('error', 'Unknown error') if isinstance(current_status, dict) else 'Unknown error'
                print(f"Error details: {error_msg}")
                return
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(5)
        else:
            print("❌ Processing timed out")
            return
        
        # Check what was extracted
        print(f"\n🔍 Checking AI-extracted content:")
        
        # Search for the test content
        chunks = db.retrieve_chunks("ECSS-TEST-001")
        print(f"Found {len(chunks)} chunks containing 'ECSS-TEST-001'")
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"\nChunk {i+1}:")
            print(f"  Length: {len(content)} characters")
            print(f"  Content: {content[:300]}...")
            
            # Check if this looks like AI-extracted JSON
            if "title" in content and "standard_number" in content:
                print(f"  ✅ This looks like AI-extracted metadata!")
        
        # Test a query that should use OpenAI
        print(f"\n🔍 Testing AI-powered query:")
        try:
            response = db.query(
                "What is the standard number and what requirements are listed?",
                k=3
            )
            
            if response and response.sources:
                print(f"✅ AI query successful - found {len(response.sources)} results")
                for i, source in enumerate(response.sources[:2]):
                    source_text = getattr(source, 'text', '')
                    print(f"  Result {i+1}: {source_text[:200]}...")
            else:
                print("⚠ No results from AI query")
                
        except Exception as e:
            print(f"❌ AI query failed: {e}")
        
        print(f"\n📊 OpenAI Integration Test Summary:")
        print(f"  - Test document processed successfully")
        print(f"  - AI rule applied and completed")
        print(f"  - OpenAI API calls should have been made")
        print(f"  - Check your OpenAI dashboard for API usage")
        
        # Clean up
        test_file.unlink()
        print(f"  - Test file cleaned up")
        
    except Exception as e:
        print(f"❌ OpenAI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up on error
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_openai_integration() 