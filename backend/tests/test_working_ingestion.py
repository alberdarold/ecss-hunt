

#!/usr/bin/env python3
"""
Test working ECSS ingestion using NaturalLanguageRule
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test working ECSS ingestion using NaturalLanguageRule
"""

import os
import sys
import json
import time
import random

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_working_ingestion():
    """Test working ingestion with NaturalLanguageRule."""
    print("🚀 Testing Working ECSS Ingestion with NaturalLanguageRule")
    print("=" * 60)
    
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
    
    # Select small PDFs for testing
    small_pdfs = [f for f in pdf_files if f.stat().st_size < 300 * 1024]
    if not small_pdfs:
        print("❌ No small PDF files found")
        return
    
    # Select 3 random files
    selected_pdfs = random.sample(small_pdfs, min(3, len(small_pdfs)))
    
    print(f"📄 Selected {len(selected_pdfs)} PDF files for testing:")
    for pdf in selected_pdfs:
        print(f"  - {pdf.name} ({pdf.stat().st_size / 1024:.1f} KB)")
    
    # Test ingestion
    successful_ingestions = 0
    ingested_docs = []
    
    for pdf_file in selected_pdfs:
        print(f"\n🔍 Processing: {pdf_file.name}")
        
        try:
            # Ingest with NaturalLanguageRule
            doc = db.ingest_file(
                pdf_file, 
                filename=f"test_{pdf_file.name}",
                rules=[metadata_rule]
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            start_time = time.time()
            max_wait = 300  # 5 minutes
            
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
                
                time.sleep(10)
            else:
                print("❌ Processing timed out")
                continue
            
            # Record successful ingestion
            successful_ingestions += 1
            ingested_docs.append({
                'file': pdf_file.name,
                'external_id': doc.external_id,
                'file_size_kb': pdf_file.stat().st_size / 1024
            })
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    
    # Create knowledge graph
    print(f"\n🧠 Creating knowledge graph...")
    try:
        graph_prompt = """Create a comprehensive knowledge graph for ECSS standards that includes:
1. Document relationships (references, dependencies)
2. Requirement hierarchies and dependencies
3. Technical concept relationships
4. Cross-standard connections
5. Verification and validation relationships
6. Process and workflow connections

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
        
        graph = db.create_knowledge_graph(
            prompt=graph_prompt,
            name="ECSS Standards Knowledge Graph"
        )
        print(f"✅ Knowledge graph created: {graph.id}")
        graph_success = True
    except Exception as e:
        print(f"❌ Failed to create knowledge graph: {e}")
        graph_success = False
    
    # Show extracted metadata from chunks
    print(f"\n🔍 Extracted Metadata from Chunks:")
    search_terms = ["ECSS", "standard", "requirement", "engineering"]
    
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
    print(f"Total files: {len(selected_pdfs)}")
    print(f"Successful ingestions: {successful_ingestions}")
    print(f"Success rate: {(successful_ingestions / len(selected_pdfs)) * 100:.1f}%")
    print(f"Knowledge graph: {'✅ Success' if graph_success else '❌ Failed'}")
    
    # Save results
    results = {
        'test_type': 'working_ingestion_with_nl_rules',
        'total_files': len(selected_pdfs),
        'successful_ingestions': successful_ingestions,
        'success_rate': f"{(successful_ingestions / len(selected_pdfs)) * 100:.1f}%",
        'ingested_docs': ingested_docs,
        'graph_creation': 'success' if graph_success else 'failed',
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"working_ingestion_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    test_working_ingestion() 

import os
import sys
import json
import time
import random

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

def test_working_ingestion():
    """Test working ingestion with NaturalLanguageRule."""
    print("🚀 Testing Working ECSS Ingestion with NaturalLanguageRule")
    print("=" * 60)
    
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
    
    # Select small PDFs for testing
    small_pdfs = [f for f in pdf_files if f.stat().st_size < 300 * 1024]
    if not small_pdfs:
        print("❌ No small PDF files found")
        return
    
    # Select 3 random files
    selected_pdfs = random.sample(small_pdfs, min(3, len(small_pdfs)))
    
    print(f"📄 Selected {len(selected_pdfs)} PDF files for testing:")
    for pdf in selected_pdfs:
        print(f"  - {pdf.name} ({pdf.stat().st_size / 1024:.1f} KB)")
    
    # Test ingestion
    successful_ingestions = 0
    ingested_docs = []
    
    for pdf_file in selected_pdfs:
        print(f"\n🔍 Processing: {pdf_file.name}")
        
        try:
            # Ingest with NaturalLanguageRule
            doc = db.ingest_file(
                pdf_file, 
                filename=f"test_{pdf_file.name}",
                rules=[metadata_rule]
            )
            print(f"✅ Document created: {doc.external_id}")
            
            # Wait for completion
            print("⏳ Waiting for processing...")
            start_time = time.time()
            max_wait = 300  # 5 minutes
            
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
                
                time.sleep(10)
            else:
                print("❌ Processing timed out")
                continue
            
            # Record successful ingestion
            successful_ingestions += 1
            ingested_docs.append({
                'file': pdf_file.name,
                'external_id': doc.external_id,
                'file_size_kb': pdf_file.stat().st_size / 1024
            })
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    
    # Create knowledge graph
    print(f"\n🧠 Creating knowledge graph...")
    try:
        graph_prompt = """Create a comprehensive knowledge graph for ECSS standards that includes:
1. Document relationships (references, dependencies)
2. Requirement hierarchies and dependencies
3. Technical concept relationships
4. Cross-standard connections
5. Verification and validation relationships
6. Process and workflow connections

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
        
        graph = db.create_knowledge_graph(
            prompt=graph_prompt,
            name="ECSS Standards Knowledge Graph"
        )
        print(f"✅ Knowledge graph created: {graph.id}")
        graph_success = True
    except Exception as e:
        print(f"❌ Failed to create knowledge graph: {e}")
        graph_success = False
    
    # Show extracted metadata from chunks
    print(f"\n🔍 Extracted Metadata from Chunks:")
    search_terms = ["ECSS", "standard", "requirement", "engineering"]
    
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
    print(f"Total files: {len(selected_pdfs)}")
    print(f"Successful ingestions: {successful_ingestions}")
    print(f"Success rate: {(successful_ingestions / len(selected_pdfs)) * 100:.1f}%")
    print(f"Knowledge graph: {'✅ Success' if graph_success else '❌ Failed'}")
    
    # Save results
    results = {
        'test_type': 'working_ingestion_with_nl_rules',
        'total_files': len(selected_pdfs),
        'successful_ingestions': successful_ingestions,
        'success_rate': f"{(successful_ingestions / len(selected_pdfs)) * 100:.1f}%",
        'ingested_docs': ingested_docs,
        'graph_creation': 'success' if graph_success else 'failed',
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"working_ingestion_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    test_working_ingestion() 