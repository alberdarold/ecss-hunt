#!/usr/bin/env python3
"""
Working ECSS Document Ingestion - Bypasses 307 Redirect Issues
==============================================================

Modified version of the simplified ingestion that works around 
the Morphik 307 redirect issue during list_documents() calls.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
import logging
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('working_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkingECSSIngestion:
    """ECSS ingestion that works around 307 redirect issues."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the working ingestion system."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Skip validation that causes 307 redirect
        logger.info("✅ Connected to Morphik (skipping list_documents validation)")
        logger.info("⚠️ Note: Document existence checks disabled due to 307 redirect issue")
    
    def get_simplified_rules(self) -> List[NaturalLanguageRule]:
        """Get effective rules for ECSS document processing."""
        return [
            NaturalLanguageRule(
                prompt="""Extract key ECSS document information:

**Document Identity:**
- ECSS Standard ID (e.g., ECSS-E-ST-40C)
- Title and full name
- Revision and date
- Document type and purpose

**Key Content:**
- Main requirements (SHALL statements)
- Important procedures and methods
- Cross-references to other standards
- Practical implementation guidance

Format as clear, structured information for engineers."""
            ),
            
            NaturalLanguageRule(
                prompt="""Extract practical ECSS implementation details:

**Requirements and Procedures:**
- Critical requirements with verification methods
- Step-by-step procedures
- Guidelines and best practices
- Compliance workflows

**Application Context:**
- When to use this standard
- Project phases where applicable
- Integration with other ECSS standards

Focus on actionable, real-world information."""
            )
        ]
    
    def validate_document(self, file_path: Path) -> Tuple[bool, str]:
        """Validate document before ingestion - simplified validation."""
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"
        
        if file_path.suffix.lower() != '.pdf':
            return False, f"Unsupported file type: {file_path.suffix}"
        
        # Check file size (reasonable limit for cost control)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > 50:  # 50MB limit
            return False, f"File too large: {file_size_mb:.1f}MB"
        
        # Skip existing document check due to 307 redirect issue
        logger.info(f"⚠️ Skipping duplicate check for {file_path.name} (307 redirect workaround)")
        
        return True, "Valid"
    
    def ingest_document(self, file_path: Path) -> bool:
        """Ingest a single document with validation and extended timeout."""
        try:
            # Validate document first
            is_valid, validation_msg = self.validate_document(file_path)
            if not is_valid:
                logger.warning(f"Document validation failed: {validation_msg}")
                self.failed_docs.append({'file': str(file_path), 'error': validation_msg})
                return False
            
            # Get simplified rules
            rules = self.get_simplified_rules()
            
            logger.info(f"📄 Ingesting {file_path.name} with ColPali visual processing...")
            logger.info(f"📏 File size: {file_path.stat().st_size / (1024 * 1024):.1f}MB")
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Ingest document using ColPali for better ECSS document processing
            doc = self.db.ingest_file(
                file_path, 
                filename=external_id, 
                rules=rules,
                use_colpali=True  # Enable ColPali for diagrams, tables, and figures
            )
            
            logger.info(f"🔄 Document created, waiting for processing...")
            
            # Wait for processing with extended timeout for ColPali
            try:
                # Wait for document completion with extended timeout
                doc.wait_for_completion(timeout_seconds=600)  # 10 minutes
                
                # Get final status
                ingestion_time = time.time() - start_time
                status_value = doc.status['status'] if isinstance(doc.status, dict) else doc.status
                
                if status_value == 'completed':
                    logger.info(f"✅ Processing completed in {ingestion_time:.1f}s")
                    
                    # Test search to validate quality
                    try:
                        test_chunks = self.db.retrieve_chunks("ECSS", k=1)
                        if test_chunks:
                            logger.info(f"🔍 Quality check passed - found searchable content")
                        else:
                            logger.warning(f"⚠️ Quality check: no searchable content found")
                    except Exception as e:
                        logger.warning(f"⚠️ Quality check failed: {e}")
                        # Don't fail ingestion for search issues
                    
                    self.ingested_docs.append({
                        'file': str(file_path),
                        'external_id': external_id,
                        'processing_time': ingestion_time,
                        'method': 'working_ingestion + ColPali'
                    })
                    return True
                else:
                    # Processing failed
                    full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                    error_message = full_status.get('error', f'Processing failed: {status_value}')
                    logger.error(f"❌ Ingestion failed: {error_message}")
                    self.failed_docs.append({'file': str(file_path), 'error': error_message})
                    return False
                    
            except Exception as timeout_error:
                logger.error(f"⏱️ Timeout during processing: {timeout_error}")
                self.failed_docs.append({'file': str(file_path), 'error': str(timeout_error)})
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False

    def get_suitable_files(self, pdf_dir: Path, max_docs: int = None) -> List[Path]:
        """Get suitable files for ingestion."""
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return []
        
        # Filter files under 50MB for reasonable processing
        suitable_files = []
        for pdf_file in pdf_files:
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            if file_size_mb < 50:
                suitable_files.append((pdf_file, file_size_mb))
        
        if not suitable_files:
            logger.error(f"No PDF files under 50MB found in {pdf_dir}")
            return []
        
        # Sort by size (smallest first for efficiency)
        suitable_files.sort(key=lambda x: x[1])
        
        # Limit selection
        if max_docs:
            suitable_files = suitable_files[:max_docs]
        
        logger.info(f"Found {len(suitable_files)} suitable files:")
        for file_info in suitable_files[:5]:  # Show first 5
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}MB)")
        
        return [file_info[0] for file_info in suitable_files]

    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents."""
        logger.info(f"🚀 Starting batch ingestion from {pdf_dir}")
        
        # Get suitable files
        pdf_files = self.get_suitable_files(pdf_dir, max_docs)
        if not pdf_files:
            return {'error': 'No suitable files found'}
        
        # Show selection
        total_size = sum(f.stat().st_size / (1024 * 1024) for f in pdf_files)
        logger.info(f"📊 Will process {len(pdf_files)} files ({total_size:.1f}MB total)")
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"📝 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document(pdf_file):
                successful += 1
                logger.info(f"✅ SUCCESS: {pdf_file.name}")
            else:
                logger.error(f"❌ FAILED: {pdf_file.name}")
            
            # Add delay between ingestions
            if i < len(pdf_files):
                time.sleep(2)
        
        total_time = time.time() - start_time
        
        return {
            'total_documents': len(pdf_files),
            'successful_ingestions': successful,
            'failed_ingestions': len(self.failed_docs),
            'total_time': round(total_time, 2),
            'success_rate': round(successful / len(pdf_files) * 100, 1),
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs
        }

    def test_search(self, query: str = "ECSS requirements") -> List[Dict]:
        """Test search functionality."""
        try:
            logger.info(f"🔍 Testing search: '{query}'")
            chunks = self.db.retrieve_chunks(query, k=3)
            
            results = []
            for chunk in chunks:
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    if isinstance(content, str):
                        results.append({
                            'text': content[:200] + "..." if len(content) > 200 else content,
                            'type': 'text',
                            'score': getattr(chunk, 'score', 0.0)
                        })
                    else:
                        # Visual content from ColPali
                        results.append({
                            'text': f"[Visual Content] {type(content).__name__}",
                            'type': 'visual',
                            'score': getattr(chunk, 'score', 0.0)
                        })
            
            logger.info(f"📋 Found {len(results)} search results")
            return results
            
        except Exception as e:
            logger.error(f"🔍 Search test failed: {e}")
            return []

def main():
    """Main function with user interaction."""
    print("=" * 60)
    print("Working ECSS Ingestion - Bypasses 307 Redirect Issues")
    print("Enhanced visual processing with ColPali")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize working ingestion system
    try:
        ingestion = WorkingECSSIngestion(morphik_uri)
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../../../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    # Get user input
    print(f"\n📁 Found PDF directory: {pdf_dir}")
    print("🎯 This ingestion bypasses 307 redirect issues")
    print("📊 Visual processing enabled for diagrams and tables")
    
    try:
        max_docs_input = input("\nEnter number of documents to ingest (default 2): ").strip()
        max_docs = int(max_docs_input) if max_docs_input else 2
    except ValueError:
        print("Invalid input, using 2 documents")
        max_docs = 2
    
    # Confirm before proceeding
    confirm = input(f"\nProceed with ingestion of up to {max_docs} documents? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Ingestion cancelled")
        return
    
    print(f"\n🚀 Starting ingestion...")
    
    # Start ingestion
    summary = ingestion.ingest_documents_batch(pdf_dir, max_docs)
    
    if 'error' in summary:
        print(f"❌ Ingestion failed: {summary['error']}")
        return
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"working_ingestion_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    # Print summary
    print(f"\n📊 INGESTION SUMMARY:")
    print(f"   Total: {summary['total_documents']}")
    print(f"   Success: {summary['successful_ingestions']}")
    print(f"   Failed: {summary['failed_ingestions']}")
    print(f"   Rate: {summary['success_rate']:.1f}%")
    print(f"   Time: {summary['total_time']:.1f}s")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Test search if successful
    if summary['successful_ingestions'] > 0:
        print(f"\n🔍 Testing search functionality...")
        results = ingestion.test_search("verification procedures")
        
        if results:
            print(f"✅ Search working! Found {len(results)} results:")
            for i, result in enumerate(results[:2], 1):
                print(f"   {i}. {result['text'][:100]}...")
        else:
            print("⚠️ Search test returned no results")

if __name__ == "__main__":
    main() 