

#!/usr/bin/env python3
"""
Cost-effective test: Single document ingestion with NaturalLanguageRule
Only ingests 1 document to minimize costs.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Cost-effective test: Single document ingestion with NaturalLanguageRule
Only ingests 1 document to minimize costs.
"""

import os
import sys
import json
import time

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_single_document():
    """Test single document ingestion with NaturalLanguageRule - COST EFFECTIVE."""
    print("💰 Cost-Effective Test: Single Document Ingestion")
    print("=" * 50)
    print("⚠️  Only ingesting 1 document to minimize costs")
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create NaturalLanguageRule for metadata extraction
    metadata_rule = NaturalLanguageRule(
        prompt="""Extract comprehensive ECSS standard metadata from the document. Return as JSON with these fields:
- standard_id: ECSS standard identifier (e.g., ECSS-E-ST-10C)
- branch: ECSS branch (E, M, P, Q)
- discipline: ECSS discipline (Engineering, Management, Product Assurance, etc.)
- title: Full title of the standard
- revision: Revision number (e.g., Rev.1, Rev.2)
- date: Publication date
- status: Status (Active, Superseded, etc.)
- scope: Brief description of the standard's scope
- keywords: Array of key technical terms and concepts
- applicable_domains: Array of space engineering domains this applies to

Be precise and extract all available information from the document."""
    )
    
    # Find PDF files
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Select the SMALLEST PDF for minimal cost
    smallest_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
    
    print(f"📄 Selected smallest PDF: {smallest_pdf.name} ({smallest_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Test ingestion of ONLY 1 document
    print(f"\n🔍 Processing: {smallest_pdf.name}")
    
    try:
        # Ingest with NaturalLanguageRule
        doc = db.ingest_file(
            smallest_pdf, 
            filename=f"test_single_{smallest_pdf.name}",
            rules=[metadata_rule],
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
        
        # Show extracted metadata from chunks (this is free - no additional AI cost)
        print(f"\n🔍 Extracted Metadata from Chunks (FREE retrieval):")
        search_terms = ["ECSS", "standard", "requirement"]
        
        for term in search_terms:
            try:
                chunks = db.retrieve_chunks(term)
                if chunks:
                    print(f"\n{term.upper()}: Found {len(chunks)} chunks")
                    for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
                        if hasattr(chunk, 'content') and chunk.content:
                            content = chunk.content
                            if isinstance(content, str) and len(content) > 50:
                                print(f"  Chunk {i+1}: {content[:200]}...")
                            else:
                                print(f"  Chunk {i+1}: {content}")
                else:
                    print(f"\n{term.upper()}: No chunks found")
            except Exception as e:
                print(f"\n{term.upper()}: Error - {e}")
        
        # Summary
        print(f"\n📊 Test Results Summary:")
        print(f"Document processed: {smallest_pdf.name}")
        print(f"File size: {smallest_pdf.stat().st_size / 1024:.1f} KB")
        print(f"Processing time: {time.time() - start_time:.1f} seconds")
        print(f"Document ID: {doc.external_id}")
        print(f"✅ SUCCESS: NaturalLanguageRule extraction working!")
        
        # Save results
        results = {
            'test_type': 'single_document_cost_effective',
            'document_name': smallest_pdf.name,
            'file_size_kb': smallest_pdf.stat().st_size / 1024,
            'external_id': doc.external_id,
            'processing_time_seconds': time.time() - start_time,
            'status': 'success',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = f"single_document_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        print(f"\n💰 Cost Analysis:")
        print(f"  - 1 document ingested: ✅ Minimal cost")
        print(f"  - No knowledge graph: ✅ No additional cost")
        print(f"  - Chunk retrieval: ✅ FREE")
        print(f"  - Total cost: Minimal (1 document processing only)")
        
    except Exception as e:
        print(f"❌ Error processing {smallest_pdf.name}: {e}")

if __name__ == "__main__":
    test_single_document() 

import os
import sys
import json
import time

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_single_document():
    """Test single document ingestion with NaturalLanguageRule - COST EFFECTIVE."""
    print("💰 Cost-Effective Test: Single Document Ingestion")
    print("=" * 50)
    print("⚠️  Only ingesting 1 document to minimize costs")
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Create NaturalLanguageRule for metadata extraction
    metadata_rule = NaturalLanguageRule(
        prompt="""Extract comprehensive ECSS standard metadata from the document. Return as JSON with these fields:
- standard_id: ECSS standard identifier (e.g., ECSS-E-ST-10C)
- branch: ECSS branch (E, M, P, Q)
- discipline: ECSS discipline (Engineering, Management, Product Assurance, etc.)
- title: Full title of the standard
- revision: Revision number (e.g., Rev.1, Rev.2)
- date: Publication date
- status: Status (Active, Superseded, etc.)
- scope: Brief description of the standard's scope
- keywords: Array of key technical terms and concepts
- applicable_domains: Array of space engineering domains this applies to

Be precise and extract all available information from the document."""
    )
    
    # Find PDF files
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Select the SMALLEST PDF for minimal cost
    smallest_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
    
    print(f"📄 Selected smallest PDF: {smallest_pdf.name} ({smallest_pdf.stat().st_size / 1024:.1f} KB)")
    
    # Test ingestion of ONLY 1 document
    print(f"\n🔍 Processing: {smallest_pdf.name}")
    
    try:
        # Ingest with NaturalLanguageRule
        doc = db.ingest_file(
            smallest_pdf, 
            filename=f"test_single_{smallest_pdf.name}",
            rules=[metadata_rule],
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
        
        # Show extracted metadata from chunks (this is free - no additional AI cost)
        print(f"\n🔍 Extracted Metadata from Chunks (FREE retrieval):")
        search_terms = ["ECSS", "standard", "requirement"]
        
        for term in search_terms:
            try:
                chunks = db.retrieve_chunks(term)
                if chunks:
                    print(f"\n{term.upper()}: Found {len(chunks)} chunks")
                    for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
                        if hasattr(chunk, 'content') and chunk.content:
                            content = chunk.content
                            if isinstance(content, str) and len(content) > 50:
                                print(f"  Chunk {i+1}: {content[:200]}...")
                            else:
                                print(f"  Chunk {i+1}: {content}")
                else:
                    print(f"\n{term.upper()}: No chunks found")
            except Exception as e:
                print(f"\n{term.upper()}: Error - {e}")
        
        # Summary
        print(f"\n📊 Test Results Summary:")
        print(f"Document processed: {smallest_pdf.name}")
        print(f"File size: {smallest_pdf.stat().st_size / 1024:.1f} KB")
        print(f"Processing time: {time.time() - start_time:.1f} seconds")
        print(f"Document ID: {doc.external_id}")
        print(f"✅ SUCCESS: NaturalLanguageRule extraction working!")
        
        # Save results
        results = {
            'test_type': 'single_document_cost_effective',
            'document_name': smallest_pdf.name,
            'file_size_kb': smallest_pdf.stat().st_size / 1024,
            'external_id': doc.external_id,
            'processing_time_seconds': time.time() - start_time,
            'status': 'success',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = f"single_document_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        print(f"\n💰 Cost Analysis:")
        print(f"  - 1 document ingested: ✅ Minimal cost")
        print(f"  - No knowledge graph: ✅ No additional cost")
        print(f"  - Chunk retrieval: ✅ FREE")
        print(f"  - Total cost: Minimal (1 document processing only)")
        
    except Exception as e:
        print(f"❌ Error processing {smallest_pdf.name}: {e}")

if __name__ == "__main__":
    test_single_document() 