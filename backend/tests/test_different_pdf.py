

#!/usr/bin/env python3
"""
Test ingestion of a different ECSS PDF to see if text extraction works
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test ingestion of a different ECSS PDF to see if text extraction works
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

def test_different_pdf():
    """Test ingestion of a different ECSS PDF."""
    print("🔍 Testing Different ECSS PDF")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Find PDF files
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Get list of already ingested documents
    existing_docs = db.list_documents()
    existing_filenames = [doc.filename for doc in existing_docs]
    
    # Find a PDF that hasn't been ingested yet
    available_pdfs = [f for f in pdf_files if f.name not in existing_filenames]
    
    if not available_pdfs:
        print("❌ All PDFs have already been ingested")
        return
    
    # Select the second smallest PDF (different from the first test)
    test_pdf = sorted(available_pdfs, key=lambda f: f.stat().st_size)[1] if len(available_pdfs) > 1 else available_pdfs[0]
    
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Create a simple rule
    simple_rule = NaturalLanguageRule(
        prompt="Extract the title and main topic of this document. Return as JSON with fields: title, topic, document_type"
    )
    
    try:
        # Ingest with text-based parsing
        print(f"🔍 Ingesting with use_colpali=False...")
        doc = db.ingest_file(
            test_pdf,
            filename=f"test_different_{test_pdf.name}",
            rules=[simple_rule],
            use_colpali=False  # Force text-based parsing
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        start_time = time.time()
        max_wait = 300  # 5 minutes max
        
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
                return
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(10)
        else:
            print("❌ Processing timed out")
            return
        
        # Check what content was extracted
        print(f"\n🔍 Checking extracted content:")
        
        # Try to retrieve chunks
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks for 'ECSS'")
            for i, chunk in enumerate(chunks[:3]):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    print(f"  Chunk {i+1} ({len(content)} chars): {content[:200]}...")
                else:
                    print(f"  Chunk {i+1}: No content")
        else:
            print("❌ No chunks found for 'ECSS'")
        
        # Try with common words
        for term in ["the", "and", "document"]:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"✅ Found {len(chunks)} chunks for '{term}'")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        if len(content) > 100:
                            print(f"  Chunk {i+1}: {content[:100]}...")
                        else:
                            print(f"  Chunk {i+1}: {content}")
                    else:
                        print(f"  Chunk {i+1}: No content")
                break
        
        print(f"\n📊 Test Summary:")
        print(f"Document: {test_pdf.name}")
        print(f"File size: {test_pdf.stat().st_size / 1024:.1f} KB")
        print(f"Processing time: {time.time() - start_time:.1f} seconds")
        print(f"Document ID: {doc.external_id}")
        
    except Exception as e:
        print(f"❌ Error processing {test_pdf.name}: {e}")

if __name__ == "__main__":
    test_different_pdf() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_different_pdf():
    """Test ingestion of a different ECSS PDF."""
    print("🔍 Testing Different ECSS PDF")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Find PDF files
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Get list of already ingested documents
    existing_docs = db.list_documents()
    existing_filenames = [doc.filename for doc in existing_docs]
    
    # Find a PDF that hasn't been ingested yet
    available_pdfs = [f for f in pdf_files if f.name not in existing_filenames]
    
    if not available_pdfs:
        print("❌ All PDFs have already been ingested")
        return
    
    # Select the second smallest PDF (different from the first test)
    test_pdf = sorted(available_pdfs, key=lambda f: f.stat().st_size)[1] if len(available_pdfs) > 1 else available_pdfs[0]
    
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Create a simple rule
    simple_rule = NaturalLanguageRule(
        prompt="Extract the title and main topic of this document. Return as JSON with fields: title, topic, document_type"
    )
    
    try:
        # Ingest with text-based parsing
        print(f"🔍 Ingesting with use_colpali=False...")
        doc = db.ingest_file(
            test_pdf,
            filename=f"test_different_{test_pdf.name}",
            rules=[simple_rule],
            use_colpali=False  # Force text-based parsing
        )
        print(f"✅ Document created: {doc.external_id}")
        
        # Wait for completion
        print("⏳ Waiting for processing...")
        start_time = time.time()
        max_wait = 300  # 5 minutes max
        
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
                return
            elif status_value == 'processing':
                elapsed = time.time() - start_time
                print(f"  Still processing... ({elapsed:.0f}s elapsed)")
            
            time.sleep(10)
        else:
            print("❌ Processing timed out")
            return
        
        # Check what content was extracted
        print(f"\n🔍 Checking extracted content:")
        
        # Try to retrieve chunks
        chunks = db.retrieve_chunks("ECSS")
        if chunks:
            print(f"✅ Found {len(chunks)} chunks for 'ECSS'")
            for i, chunk in enumerate(chunks[:3]):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    print(f"  Chunk {i+1} ({len(content)} chars): {content[:200]}...")
                else:
                    print(f"  Chunk {i+1}: No content")
        else:
            print("❌ No chunks found for 'ECSS'")
        
        # Try with common words
        for term in ["the", "and", "document"]:
            chunks = db.retrieve_chunks(term)
            if chunks:
                print(f"✅ Found {len(chunks)} chunks for '{term}'")
                for i, chunk in enumerate(chunks[:2]):
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        if len(content) > 100:
                            print(f"  Chunk {i+1}: {content[:100]}...")
                        else:
                            print(f"  Chunk {i+1}: {content}")
                    else:
                        print(f"  Chunk {i+1}: No content")
                break
        
        print(f"\n📊 Test Summary:")
        print(f"Document: {test_pdf.name}")
        print(f"File size: {test_pdf.stat().st_size / 1024:.1f} KB")
        print(f"Processing time: {time.time() - start_time:.1f} seconds")
        print(f"Document ID: {doc.external_id}")
        
    except Exception as e:
        print(f"❌ Error processing {test_pdf.name}: {e}")

if __name__ == "__main__":
    test_different_pdf() 