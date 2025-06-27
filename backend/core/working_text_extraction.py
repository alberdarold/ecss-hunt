

#!/usr/bin/env python3
"""
Working Text Extraction and Ingestion
Extract text locally using pdfplumber, then ingest the text directly into Morphik.
This bypasses the broken PDF parser and ensures AI rules get real content.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Working Text Extraction and Ingestion
Extract text locally using pdfplumber, then ingest the text directly into Morphik.
This bypasses the broken PDF parser and ensures AI rules get real content.
"""

import os
import sys
import json
import time
import pdfplumber

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    print(f"📄 Extracting text from {pdf_path.name}...")
    
    try:
        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    full_text.append(text)
                else:
                    print(f"  ⚠️  No text found on page {i+1}")
        
        if not full_text:
            print(f"❌ No text extracted from {pdf_path.name}")
            return ""
        
        extracted_text = "\n\n".join(full_text)
        print(f"✅ Extracted {len(extracted_text)} characters from {len(pdf.pages)} pages")
        return extracted_text
        
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

def ingest_text_with_ai_rules(text_content: str, filename: str, db: Morphik) -> bool:
    """Ingest extracted text with AI rules."""
    print(f"🤖 Ingesting text with AI rules...")
    
    # Create AI rules for ECSS document analysis
    rules = [
        NaturalLanguageRule(
            prompt="""Extract the following information from this ECSS document:
{
  "title": "document title",
  "standard_number": "ECSS standard number (e.g., ECSS-E-ST-10-01C)",
  "document_type": "type of document (standard, specification, etc.)",
  "scope": "brief description of what this document covers",
  "requirements": ["list of key requirements found in the document"],
  "key_topics": ["main topics and subjects covered"]
}

Be specific and extract actual content from the document."""
        ),
        NaturalLanguageRule(
            prompt="""Analyze this ECSS document for requirements and extract:
{
  "requirement_count": "number of requirements found",
  "requirement_types": ["functional", "performance", "interface", "etc."],
  "critical_requirements": ["list of the most important requirements"],
  "verification_methods": ["test", "analysis", "demonstration", "inspection"]
}"""
        )
    ]
    
    try:
        # Ingest the text directly
        doc = db.ingest_text(
            text_content,
            filename=filename,
            rules=rules
        )
        
        print(f"✅ Text ingested: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing...")
        start_time = time.time()
        max_wait = 300  # 5 minutes
        
        while time.time() - start_time < max_wait:
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            if status_value == 'completed':
                print("✅ AI processing completed!")
                return True
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return False
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(10)
        else:
            print("❌ Processing timed out")
            return False
            
    except Exception as e:
        print(f"❌ Text ingestion failed: {e}")
        return False

def main():
    """Main function to test working text extraction."""
    print("🚀 Working Text Extraction and AI Processing")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Connect to Morphik
    db = Morphik(morphik_uri)
    
    # Find a test PDF
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Use a small PDF for testing
    test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Extract text locally
    extracted_text = extract_text_from_pdf(test_pdf)
    
    if not extracted_text:
        print("❌ No text extracted - cannot proceed")
        return
    
    # Show a preview of extracted text
    print(f"\n📝 Extracted Text Preview:")
    print(f"  Length: {len(extracted_text)} characters")
    print(f"  Preview: {extracted_text[:500]}...")
    
    # Check if it looks like real content
    if "ECSS" in extracted_text and len(extracted_text) > 1000:
        print("✅ Text extraction looks successful!")
    else:
        print("⚠️  Extracted text seems minimal - may need different extraction method")
    
    # Ingest with AI rules
    success = ingest_text_with_ai_rules(extracted_text, f"text_{test_pdf.name}", db)
    
    if success:
        print(f"\n🎉 SUCCESS! Text extraction and AI processing completed!")
        print(f"  - Text extracted locally using pdfplumber")
        print(f"  - Text ingested directly into Morphik")
        print(f"  - AI rules processed the real document content")
        print(f"  - Check your OpenAI dashboard for API usage")
    else:
        print(f"\n❌ Failed to complete text ingestion and AI processing")

if __name__ == "__main__":
    main() 

import os
import sys
import json
import time
import pdfplumber

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    print(f"📄 Extracting text from {pdf_path.name}...")
    
    try:
        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    full_text.append(text)
                else:
                    print(f"  ⚠️  No text found on page {i+1}")
        
        if not full_text:
            print(f"❌ No text extracted from {pdf_path.name}")
            return ""
        
        extracted_text = "\n\n".join(full_text)
        print(f"✅ Extracted {len(extracted_text)} characters from {len(pdf.pages)} pages")
        return extracted_text
        
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

def ingest_text_with_ai_rules(text_content: str, filename: str, db: Morphik) -> bool:
    """Ingest extracted text with AI rules."""
    print(f"🤖 Ingesting text with AI rules...")
    
    # Create AI rules for ECSS document analysis
    rules = [
        NaturalLanguageRule(
            prompt="""Extract the following information from this ECSS document:
{
  "title": "document title",
  "standard_number": "ECSS standard number (e.g., ECSS-E-ST-10-01C)",
  "document_type": "type of document (standard, specification, etc.)",
  "scope": "brief description of what this document covers",
  "requirements": ["list of key requirements found in the document"],
  "key_topics": ["main topics and subjects covered"]
}

Be specific and extract actual content from the document."""
        ),
        NaturalLanguageRule(
            prompt="""Analyze this ECSS document for requirements and extract:
{
  "requirement_count": "number of requirements found",
  "requirement_types": ["functional", "performance", "interface", "etc."],
  "critical_requirements": ["list of the most important requirements"],
  "verification_methods": ["test", "analysis", "demonstration", "inspection"]
}"""
        )
    ]
    
    try:
        # Ingest the text directly
        doc = db.ingest_text(
            text_content,
            filename=filename,
            rules=rules
        )
        
        print(f"✅ Text ingested: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for AI processing...")
        start_time = time.time()
        max_wait = 300  # 5 minutes
        
        while time.time() - start_time < max_wait:
            current_status = doc.status
            if isinstance(current_status, dict):
                status_value = current_status.get('status', 'unknown')
            else:
                status_value = current_status
            
            if status_value == 'completed':
                print("✅ AI processing completed!")
                return True
            elif status_value in ['failed', 'error']:
                print(f"❌ Processing failed: {status_value}")
                return False
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(10)
        else:
            print("❌ Processing timed out")
            return False
            
    except Exception as e:
        print(f"❌ Text ingestion failed: {e}")
        return False

def main():
    """Main function to test working text extraction."""
    print("🚀 Working Text Extraction and AI Processing")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Connect to Morphik
    db = Morphik(morphik_uri)
    
    # Find a test PDF
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Use a small PDF for testing
    test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Extract text locally
    extracted_text = extract_text_from_pdf(test_pdf)
    
    if not extracted_text:
        print("❌ No text extracted - cannot proceed")
        return
    
    # Show a preview of extracted text
    print(f"\n📝 Extracted Text Preview:")
    print(f"  Length: {len(extracted_text)} characters")
    print(f"  Preview: {extracted_text[:500]}...")
    
    # Check if it looks like real content
    if "ECSS" in extracted_text and len(extracted_text) > 1000:
        print("✅ Text extraction looks successful!")
    else:
        print("⚠️  Extracted text seems minimal - may need different extraction method")
    
    # Ingest with AI rules
    success = ingest_text_with_ai_rules(extracted_text, f"text_{test_pdf.name}", db)
    
    if success:
        print(f"\n🎉 SUCCESS! Text extraction and AI processing completed!")
        print(f"  - Text extracted locally using pdfplumber")
        print(f"  - Text ingested directly into Morphik")
        print(f"  - AI rules processed the real document content")
        print(f"  - Check your OpenAI dashboard for API usage")
    else:
        print(f"\n❌ Failed to complete text ingestion and AI processing")

if __name__ == "__main__":
    main() 