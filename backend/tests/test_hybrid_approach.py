

#!/usr/bin/env python3
"""
Test hybrid approach: Use ColPali with text-focused rules
This attempts to leverage both visual and text processing capabilities.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test hybrid approach: Use ColPali with text-focused rules
This attempts to leverage both visual and text processing capabilities.
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

def test_hybrid_approach():
    """Test hybrid approach with ColPali and text-focused rules."""
    print("🔬 Testing Hybrid Approach (ColPali + Text Rules)")
    print("=" * 50)
    
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
    
    # Select a small PDF for testing
    test_pdf = min(available_pdfs, key=lambda f: f.stat().st_size)
    
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Create a text-focused rule that works with both text and visual content
    hybrid_rule = NaturalLanguageRule(
        prompt="""Analyze this document and extract the following information:
1. Document title and standard number
2. Main topics and scope
3. Key requirements or specifications
4. Document type (standard, specification, etc.)

If the document contains images or diagrams, also describe what they show.
Return the information as a structured JSON response."""
    )
    
    try:
        # Ingest with ColPali enabled (hybrid approach)
        print(f"🔍 Ingesting with hybrid approach (ColPali + text rules)...")
        doc = db.ingest_file(
            test_pdf,
            filename=f"hybrid_test_{test_pdf.name}",
            rules=[hybrid_rule],
            use_colpali=True  # Enable ColPali for visual processing
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
        print(f"Found {len(chunks)} chunks containing 'ECSS'")
        
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"\nChunk {i+1}:")
            print(f"  Length: {len(content)} characters")
            
            # Check if this is text or image content
            if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                print(f"  Type: IMAGE (base64 data)")
                print(f"  Preview: {content[:100]}...")
            else:
                print(f"  Type: TEXT")
                print(f"  Preview: {content[:200]}...")
                
                # Check if this looks like extracted metadata
                if "title" in content.lower() or "standard" in content.lower():
                    print(f"  ✅ This looks like extracted metadata!")
        
        # Test a visual query to see if ColPali is working
        print(f"\n🔍 Testing visual query with ColPali:")
        try:
            visual_response = db.query(
                "What diagrams or figures are shown in this document?",
                use_colpali=True,
                k=3
            )
            
            if visual_response and visual_response.sources:
                print(f"✅ ColPali found {len(visual_response.sources)} visual results")
                for i, source in enumerate(visual_response.sources[:2]):
                    source_text = getattr(source, 'text', '')
                    print(f"  Result {i+1}: {source_text[:200]}...")
            else:
                print("⚠ No visual results found")
                
        except Exception as e:
            print(f"❌ Visual query failed: {e}")
        
        print(f"\n📊 Hybrid Approach Summary:")
        print(f"  - Document processed successfully")
        print(f"  - ColPali enabled for visual processing")
        print(f"  - Text-focused rules applied")
        print(f"  - Both text and visual content should be available")
        
    except Exception as e:
        print(f"❌ Hybrid approach failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hybrid_approach() 

import os
import sys
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_hybrid_approach():
    """Test hybrid approach with ColPali and text-focused rules."""
    print("🔬 Testing Hybrid Approach (ColPali + Text Rules)")
    print("=" * 50)
    
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
    
    # Select a small PDF for testing
    test_pdf = min(available_pdfs, key=lambda f: f.stat().st_size)
    
    print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Create a text-focused rule that works with both text and visual content
    hybrid_rule = NaturalLanguageRule(
        prompt="""Analyze this document and extract the following information:
1. Document title and standard number
2. Main topics and scope
3. Key requirements or specifications
4. Document type (standard, specification, etc.)

If the document contains images or diagrams, also describe what they show.
Return the information as a structured JSON response."""
    )
    
    try:
        # Ingest with ColPali enabled (hybrid approach)
        print(f"🔍 Ingesting with hybrid approach (ColPali + text rules)...")
        doc = db.ingest_file(
            test_pdf,
            filename=f"hybrid_test_{test_pdf.name}",
            rules=[hybrid_rule],
            use_colpali=True  # Enable ColPali for visual processing
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
        print(f"Found {len(chunks)} chunks containing 'ECSS'")
        
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(f"\nChunk {i+1}:")
            print(f"  Length: {len(content)} characters")
            
            # Check if this is text or image content
            if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                print(f"  Type: IMAGE (base64 data)")
                print(f"  Preview: {content[:100]}...")
            else:
                print(f"  Type: TEXT")
                print(f"  Preview: {content[:200]}...")
                
                # Check if this looks like extracted metadata
                if "title" in content.lower() or "standard" in content.lower():
                    print(f"  ✅ This looks like extracted metadata!")
        
        # Test a visual query to see if ColPali is working
        print(f"\n🔍 Testing visual query with ColPali:")
        try:
            visual_response = db.query(
                "What diagrams or figures are shown in this document?",
                use_colpali=True,
                k=3
            )
            
            if visual_response and visual_response.sources:
                print(f"✅ ColPali found {len(visual_response.sources)} visual results")
                for i, source in enumerate(visual_response.sources[:2]):
                    source_text = getattr(source, 'text', '')
                    print(f"  Result {i+1}: {source_text[:200]}...")
            else:
                print("⚠ No visual results found")
                
        except Exception as e:
            print(f"❌ Visual query failed: {e}")
        
        print(f"\n📊 Hybrid Approach Summary:")
        print(f"  - Document processed successfully")
        print(f"  - ColPali enabled for visual processing")
        print(f"  - Text-focused rules applied")
        print(f"  - Both text and visual content should be available")
        
    except Exception as e:
        print(f"❌ Hybrid approach failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hybrid_approach() 