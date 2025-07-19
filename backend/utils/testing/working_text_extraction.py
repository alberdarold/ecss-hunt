#!/usr/bin/env python3
"""
Working Text Extraction and AI Processing

This module provides simple text extraction from PDFs using pdfplumber
and AI-based processing with Morphik.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / "config" / ".env")

try:
    import pdfplumber
    from morphik.ingestion import Morphik
    from morphik.types import NaturalLanguageRule
except ImportError as e:
    print(f"Missing dependency: {e}")
    sys.exit(1)

def extract_text_from_pdf(pdf_path: Path) -> Optional[str]:
    """Extract text from PDF using pdfplumber."""
    try:
        print(f"Extracting text from: {pdf_path.name}")
        
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(text)
                else:
                    print(f"  No text found on page {page_num}")
        
        if not text_content:
            print(f"No text extracted from {pdf_path.name}")
            return None
            
        extracted_text = "\n".join(text_content)
        print(f"Extracted {len(extracted_text)} characters from {len(text_content)} pages")
        return extracted_text
        
    except Exception as e:
        print(f"Error extracting text from {pdf_path.name}: {e}")
        return None

def ingest_text_with_ai_rules(db: Morphik, text: str, filename: str) -> Dict[str, Any]:
    """Ingest extracted text with AI rules."""
    print(f"Ingesting text with AI rules for: {filename}")
    
    # Define AI processing rules
    rules = [
        NaturalLanguageRule(
            prompt="""Extract the following information from this ECSS document:
- Document ID
- Title
- Publication Date
- Technical Domain
- Key Requirements

Be specific and extract actual content from the document."""
        )
    ]
    
    try:
        # Ingest text directly
        result = db.ingest_text(
            text=text,
            natural_language_rules=rules
        )
        
        print(f"Text ingested successfully: {result}")
        return {
            "status": "success",
            "document_id": str(result),
            "filename": filename
        }
        
    except Exception as e:
        print(f"Text ingestion failed: {e}")
        return {
            "status": "error",
            "filename": filename,
            "error": str(e)
        }

def test_text_extraction_and_ai():
    """Test complete text extraction and AI processing workflow."""
    print("Working Text Extraction and AI Processing")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("Error: MORPHIK_URI not found")
        return False
    
    # Connect to Morphik
    try:
        db = Morphik(morphik_uri)
        print("Successfully connected to Morphik")
    except Exception as e:
        print(f"Failed to connect to Morphik: {e}")
        return False
    
    # Find test PDF
    pdf_dir = Path(os.getenv("ECSS_DOCUMENTS_PATH", "../ECSS Published Standards/1-Active Standards"))
    
    if not pdf_dir.exists():
        print(f"PDF directory not found: {pdf_dir}")
        return False
    
    # Get first PDF file for testing
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found for testing")
        return False
    
    test_pdf = pdf_files[0]
    print(f"Testing with: {test_pdf.name}")
    
    # Extract text
    extracted_text = extract_text_from_pdf(test_pdf)
    if not extracted_text:
        print("Text extraction failed")
        return False
    
    print(f"\nExtracted Text Preview:")
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    
    # Ingest with AI rules
    result = ingest_text_with_ai_rules(db, extracted_text, test_pdf.name)
    
    if result["status"] == "success":
        print(f"\nSUCCESS! Text extraction and AI processing completed")
        print(f"  - PDF: {test_pdf.name}")
        print(f"  - Text extracted locally using pdfplumber")
        print(f"  - Text ingested into Morphik with AI rules")
        return True
    else:
        print(f"\nFailed to complete text ingestion and AI processing")
        return False

def main():
    """Main function to test working text extraction."""
    success = test_text_extraction_and_ai()
    
    if success:
        print(f"\nAll tests completed successfully!")
    else:
        print(f"\nSome tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()