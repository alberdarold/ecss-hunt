#!/usr/bin/env python3
"""
Enhanced ECSS Document Ingestion with Advanced Image Processing and OCR
Integrates with the enhanced image processor for comprehensive visual content analysis.
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
from legacy.enhanced_image_processor import EnhancedImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_simplified_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedSimplifiedECSSIngestion:
    """Enhanced ECSS ingestion with advanced image processing and OCR."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the enhanced ingestion system."""
        self.db = Morphik(morphik_uri)
        self.image_processor = EnhancedImageProcessor(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("✅ Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Morphik: {e}")
            raise
    
    def get_enhanced_rules(self) -> List[NaturalLanguageRule]:
        """Get enhanced rules that account for visual content processing."""
        return [
            # Rule 1: Document identification with visual content awareness
            NaturalLanguageRule(
                prompt="""You are analyzing an ECSS document with both text and visual content (diagrams, tables, figures).

Extract comprehensive document information:

**Document Identity:**
- ECSS Standard ID (e.g., ECSS-E-ST-40C)
- Title and full name
- Revision and date
- Document type and purpose
- Target audience

**Content Structure:**
- Main sections and their purpose
- Number of requirements, recommendations, and notes
- Key topics covered
- Visual elements (diagrams, tables, figures) and their purpose

**Visual Content Analysis:**
- Types of diagrams, charts, and figures present
- Tables and their content summary
- Technical drawings and schematics
- Any text extracted from visual elements

Focus on creating a comprehensive understanding that includes both textual and visual information."""
            ),
            
            # Rule 2: Requirements with visual context
            NaturalLanguageRule(
                prompt="""Extract requirements, procedures, and implementation guidance from both text and visual elements.

**Requirements Analysis:**
- Text-based requirements (SHALL statements)
- Requirements illustrated in diagrams or figures
- Verification methods and procedures
- Cross-references to other standards

**Visual Requirements:**
- Requirements expressed through diagrams
- Process flows and decision trees
- Technical specifications in tables
- Compliance matrices and checklists

**Implementation Guidance:**
- Step-by-step procedures (text and visual)
- Technical diagrams and schematics
- Example implementations and case studies
- Best practices and recommendations

Combine information from both text and visual sources to provide complete guidance."""
            ),
            
            # Rule 3: Practical application with visual aids
            NaturalLanguageRule(
                prompt="""Extract practical application information from text and visual content.

**Application Context:**
- When to use this standard (from text and flowcharts)
- Project phases and lifecycle stages
- Decision matrices and selection criteria
- Visual workflow representations

**Implementation Support:**
- Technical diagrams and schematics
- Example configurations and setups
- Process flow diagrams
- Troubleshooting guides and decision trees

**Integration Information:**
- System architecture diagrams
- Interface specifications and drawings
- Integration workflows and procedures
- Compatibility matrices and tables

Provide actionable guidance that leverages both textual instructions and visual aids."""
            )
        ]
    
    def validate_document(self, file_path: Path) -> Tuple[bool, str]:
        """Validate document before ingestion."""
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"
        
        if file_path.suffix.lower() != '.pdf':
            return False, f"Unsupported file type: {file_path.suffix}"
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        file_size_kb = file_path.stat().st_size / 1024
        
        if file_size_mb > 100:  # 100MB limit
            return False, f"File too large: {file_size_mb:.1f}MB"
        
        # Prefer smaller files for cost control
        if file_size_kb > 300:
            return False, f"File too large for cost control: {file_size_kb:.1f}KB (max 300KB)"
        
        return True, "Valid"
    
    def ingest_document_with_enhanced_processing(self, file_path: Path) -> bool:
        """Ingest document with enhanced image processing and OCR."""
        try:
            # Validate document
            is_valid, validation_msg = self.validate_document(file_path)
            if not is_valid:
                logger.warning(f"Document validation failed: {validation_msg}")
                self.failed_docs.append({'file': str(file_path), 'error': validation_msg})
                return False
            
            # Get enhanced rules
            rules = self.get_enhanced_rules()
            
            logger.info(f"🔄 Ingesting {file_path.name} with enhanced image processing...")
            logger.info(f"📄 File size: {file_path.stat().st_size / (1024 * 1024):.1f}MB")
            logger.info(f"🎯 Using {len(rules)} enhanced rules + ColPali + OCR")
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Ingest document using ColPali for visual processing
            doc = self.db.ingest_file(
                file_path, 
                filename=external_id, 
                rules=rules,
                use_colpali=True  # Enable ColPali for visual processing
            )
            
            logger.info(f"📋 Document object created: {doc.external_id}")
            
            # Wait for processing with extended timeout
            logger.info("⏳ Waiting for ColPali processing (text + visual elements)...")
            
            try:
                # Wait for document completion
                doc.wait_for_completion(timeout_seconds=900)  # 15 minutes
                
                ingestion_time = time.time() - start_time
                status_value = doc.status['status'] if isinstance(doc.status, dict) else doc.status
                
                if status_value == 'completed':
                    logger.info(f"✅ Processing completed successfully in {ingestion_time:.1f}s")
                    
                    # Now perform enhanced image processing and OCR
                    logger.info("🔍 Starting enhanced image processing and OCR...")
                    ocr_start_time = time.time()
                    
                    # Process all chunks with OCR
                    processing_results = self.image_processor.process_all_chunks()
                    
                    ocr_time = time.time() - ocr_start_time
                    logger.info(f"✅ Enhanced processing completed in {ocr_time:.1f}s")
                    
                    # Get the refreshed document
                    refreshed_doc = self.db.get_document(doc.external_id)
                    
                    # Create comprehensive info with OCR results
                    extracted_info = self.create_enhanced_document_info(
                        refreshed_doc, processing_results
                    )
                    
                    self.ingested_docs.append({
                        'file': str(file_path),
                        'external_id': external_id,
                        'info': extracted_info,
                        'processing_time': ingestion_time,
                        'ocr_processing_time': ocr_time,
                        'total_time': ingestion_time + ocr_time,
                        'method_used': 'enhanced_rules + ColPali + OCR',
                        'ocr_summary': processing_results['summary']
                    })
                    
                    logger.info(f"🎉 Successfully processed {file_path.name} with enhanced capabilities")
                    return True
                    
                else:
                    # Processing failed
                    full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                    error_message = full_status.get('error', f'Processing failed with status: {status_value}')
                    logger.error(f"❌ Ingestion failed for {file_path.name}: {error_message}")
                    self.failed_docs.append({'file': str(file_path), 'error': error_message})
                    return False
                    
            except Exception as timeout_error:
                logger.error(f"⏰ Timeout during ingestion of {file_path.name}: {timeout_error}")
                self.failed_docs.append({'file': str(file_path), 'error': str(timeout_error)})
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False
    
    def create_enhanced_document_info(self, document, processing_results: Dict) -> Dict:
        """Create enhanced document information combining text and visual content."""
        try:
            # Extract text summaries
            text_summaries = []
            visual_summaries = []
            extracted_text_from_images = []
            
            for result in processing_results.get('results', []):
                if result.get('processing_success', False):
                    if result.get('content_type') == 'text':
                        text_content = result.get('text_content', '')
                        if text_content and len(text_content) > 20:
                            text_summaries.append(text_content[:200])
                    
                    elif result.get('content_type') in ['visual', 'visual_base64']:
                        visual_info = result.get('visual_content', {})
                        analysis = visual_info.get('analysis', {})
                        content_type = analysis.get('content_type', 'unknown')
                        
                        visual_summaries.append(f"Visual: {content_type}")
                        
                        # Add extracted text from images
                        extracted_text = result.get('extracted_text', '')
                        if extracted_text and len(extracted_text.strip()) > 5:
                            extracted_text_from_images.append(extracted_text[:200])
            
            # Combine all text content
            all_text = text_summaries + extracted_text_from_images
            content_summary = " ".join(all_text) if all_text else "No text content extracted"
            
            # Create summary statistics
            ocr_summary = processing_results.get('summary', {})
            
            return {
                'source': 'enhanced_processing',
                'text_summary': content_summary,
                'visual_elements': len(visual_summaries),
                'visual_types': visual_summaries,
                'text_from_images': len(extracted_text_from_images),
                'total_chunks': ocr_summary.get('total_chunks', 0),
                'visual_chunks': ocr_summary.get('visual_chunks', 0),
                'text_chunks': ocr_summary.get('text_chunks', 0),
                'ocr_success_rate': ocr_summary.get('success_rate', 0),
                'total_extracted_text_length': ocr_summary.get('total_extracted_text_length', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating enhanced document info: {e}")
            return {
                'source': 'error',
                'error': str(e),
                'text_summary': '',
                'visual_elements': 0
            }
    
    def enhanced_search(self, query: str, limit: int = 5) -> List[Dict]:
        """Enhanced search that includes OCR results from images."""
        try:
            logger.info(f"🔍 Enhanced search for: '{query}'")
            
            # Use the enhanced image processor for search
            results = self.image_processor.search_with_enhanced_results(query, limit)
            
            if not results:
                logger.warning(f"No results found for query: '{query}'")
                return []
            
            # Format results for consistency
            formatted_results = []
            for result in results:
                formatted_result = {
                    'chunk_id': result.get('chunk_index', 'unknown'),
                    'relevance_score': result.get('relevance_score', 0.0),
                    'document_id': result.get('document_id', 'unknown'),
                    'text': result.get('text', ''),
                    'summary': result.get('summary', ''),
                    'type': result.get('type', 'unknown'),
                    'content_type': result.get('content_type', 'unknown')
                }
                
                # Add OCR-specific information if available
                if result.get('type') == 'visual_with_ocr':
                    formatted_result.update({
                        'ocr_confidence': result.get('ocr_confidence', 0),
                        'visual_info': result.get('visual_info', {}),
                        'source': 'image_ocr'
                    })
                else:
                    formatted_result['source'] = 'text_content'
                
                formatted_results.append(formatted_result)
            
            logger.info(f"✅ Found {len(formatted_results)} enhanced results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Enhanced search failed: {e}")
            return []
    
    def get_suitable_files(self, pdf_dir: Path, max_docs: int = None) -> List[Path]:
        """Get suitable files for ingestion."""
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return []
        
        # Filter files under 300KB for cost control
        suitable_files = []
        for pdf_file in pdf_files:
            file_size_kb = pdf_file.stat().st_size / 1024
            if file_size_kb < 300:
                suitable_files.append((pdf_file, file_size_kb))
        
        if not suitable_files:
            logger.error(f"No PDF files under 300KB found in {pdf_dir}")
            return []
        
        # Sort by size (smallest first)
        suitable_files.sort(key=lambda x: x[1])
        
        # Limit selection
        if max_docs:
            suitable_files = suitable_files[:max_docs]
        
        logger.info(f"Found {len(suitable_files)} suitable files:")
        for file_info in suitable_files:
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        
        return [file_info[0] for file_info in suitable_files]
    
    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents with enhanced processing."""
        logger.info(f"🚀 Starting enhanced batch ingestion from {pdf_dir}")
        
        # Get suitable files
        pdf_files = self.get_suitable_files(pdf_dir, max_docs)
        if not pdf_files:
            return {'error': 'No suitable files found'}
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"📄 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document_with_enhanced_processing(pdf_file):
                successful += 1
                logger.info(f"✅ Successfully processed {pdf_file.name}")
            else:
                logger.error(f"❌ Failed to process {pdf_file.name}")
            
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
            'failed_docs': self.failed_docs,
            'selected_files': [f.name for f in pdf_files]
        }

def main():
    """Main function with enhanced processing capabilities."""
    print("🚀 Enhanced ECSS Document Ingestion System")
    print("=" * 60)
    print("🔍 Features:")
    print("   • ColPali visual processing")
    print("   • OCR text extraction from images")
    print("   • Advanced image analysis")
    print("   • Enhanced search capabilities")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize enhanced ingestion system
    try:
        ingestion = EnhancedSimplifiedECSSIngestion(morphik_uri)
        print("✅ Enhanced ingestion system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    # Get user input
    print(f"\n📁 Found PDF directory: {pdf_dir}")
    print("⚠️  Note: Enhanced processing includes OCR and takes longer")
    
    try:
        max_docs_input = input("\nEnter number of documents to process (default 1): ").strip()
        max_docs = int(max_docs_input) if max_docs_input else 1
    except ValueError:
        print("Invalid input, using 1 document")
        max_docs = 1
    
    # Show preview
    preview_files = ingestion.get_suitable_files(pdf_dir, max_docs)
    if not preview_files:
        print("❌ No suitable files found")
        return
    
    print(f"\n📋 Will process {len(preview_files)} documents with enhanced features:")
    for f in preview_files:
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f}KB)")
    
    # Confirm
    confirm = input(f"\n🚀 Proceed with enhanced processing? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Processing cancelled")
        return
    
    print("\n🔄 Starting enhanced ingestion...")
    
    # Start ingestion
    summary = ingestion.ingest_documents_batch(pdf_dir, max_docs)
    
    if 'error' in summary:
        print(f"❌ Ingestion failed: {summary['error']}")
        return
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"enhanced_ingestion_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    # Print summary
    print(f"\n🎉 Enhanced ingestion completed:")
    print(f"   📄 Total documents: {summary['total_documents']}")
    print(f"   ✅ Successful: {summary['successful_ingestions']}")
    print(f"   ❌ Failed: {summary['failed_ingestions']}")
    print(f"   📊 Success rate: {summary['success_rate']:.1f}%")
    print(f"   ⏱️  Total time: {summary['total_time']:.1f}s")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Test enhanced search
    if summary['successful_ingestions'] > 0:
        print(f"\n🔍 Testing enhanced search with OCR...")
        test_queries = [
            "ECSS requirements",
            "verification procedures",
            "space engineering"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            results = ingestion.enhanced_search(query, limit=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"   📄 Result {i} ({result['source']}):")
                    print(f"      Score: {result['relevance_score']:.3f}")
                    print(f"      Type: {result['type']}")
                    print(f"      Summary: {result['summary'][:100]}...")
                    if result['source'] == 'image_ocr':
                        print(f"      OCR Confidence: {result.get('ocr_confidence', 0):.1f}%")
            else:
                print("   ❌ No results found")

if __name__ == "__main__":
    main() 