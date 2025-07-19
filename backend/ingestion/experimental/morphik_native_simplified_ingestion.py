#!/usr/bin/env python3
"""
Morphik Native ECSS Document Ingestion
Leverages Morphik's built-in multimodal search and visual understanding.
Uses ColPali and native capabilities - no external OCR needed.
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
        logging.FileHandler('morphik_native_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MorphikNativeECSSIngestion:
    """ECSS ingestion using Morphik's native multimodal capabilities."""
    
    def __init__(self, morphik_uri: str):
        """Initialize with Morphik's native capabilities."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("✅ Connected to Morphik with native multimodal capabilities")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Morphik: {e}")
            raise
    
    def get_morphik_native_rules(self) -> List[NaturalLanguageRule]:
        """Get rules optimized for Morphik's native visual understanding."""
        return [
            # Rule 1: Comprehensive document analysis leveraging visual understanding
            NaturalLanguageRule(
                prompt="""You are analyzing an ECSS document using Morphik's advanced visual understanding capabilities.

Extract comprehensive information from both text and visual elements:

**Document Identification:**
- ECSS Standard ID (e.g., ECSS-E-ST-40C)
- Title and full document name
- Revision number and publication date
- Document type and intended purpose
- Target audience and application scope

**Content Analysis (Text + Visual):**
- Main sections and structural organization
- Requirements, recommendations, and notes
- Technical specifications and parameters
- Visual elements: diagrams, tables, figures, charts
- Process flows and decision trees
- Verification and validation procedures

**Visual Content Understanding:**
- Diagrams and their technical meaning
- Tables with data and specifications
- Flowcharts and process diagrams
- Technical drawings and schematics
- Compliance matrices and checklists

Focus on creating a comprehensive understanding that leverages Morphik's native visual processing capabilities."""
            ),
            
            # Rule 2: Requirements and procedures with visual context
            NaturalLanguageRule(
                prompt="""Extract requirements, procedures, and implementation guidance using Morphik's multimodal understanding.

**Requirements Analysis:**
- Textual requirements (SHALL, SHOULD, MAY statements)
- Visual requirements expressed in diagrams and tables
- Verification methods and test procedures
- Acceptance criteria and compliance measures
- Cross-references to other ECSS standards

**Visual Requirements Processing:**
- Process flow diagrams and decision trees
- Technical specifications in tabular format
- Compliance matrices and verification tables
- System architecture and interface diagrams
- Test setup configurations and procedures

**Implementation Guidance:**
- Step-by-step procedures (text and visual)
- Best practices and recommendations
- Common pitfalls and error prevention
- Integration with other standards and processes

Leverage Morphik's native capabilities to understand both textual and visual requirements."""
            ),
            
            # Rule 3: Practical application with integrated visual understanding
            NaturalLanguageRule(
                prompt="""Extract practical application information using Morphik's comprehensive visual understanding.

**Application Context:**
- When and where to apply this standard
- Project phases and lifecycle integration
- Decision criteria and selection guidelines
- Scope boundaries and limitations

**Visual Application Support:**
- Workflow diagrams and process maps
- Decision trees and selection criteria
- System integration diagrams
- Configuration examples and templates
- Troubleshooting guides and error resolution

**Implementation Support:**
- Practical examples and case studies
- Template documents and forms
- Integration with project management processes
- Quality assurance and verification approaches

Combine textual guidance with visual aids to provide complete implementation support."""
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
        
        if file_size_mb > 100:
            return False, f"File too large: {file_size_mb:.1f}MB"
        
        # Cost control
        if file_size_kb > 300:
            return False, f"File too large for cost control: {file_size_kb:.1f}KB (max 300KB)"
        
        return True, "Valid"
    
    def ingest_document_with_native_multimodal(self, file_path: Path) -> bool:
        """Ingest document using Morphik's native multimodal capabilities."""
        try:
            # Validate document
            is_valid, validation_msg = self.validate_document(file_path)
            if not is_valid:
                logger.warning(f"Document validation failed: {validation_msg}")
                self.failed_docs.append({'file': str(file_path), 'error': validation_msg})
                return False
            
            # Get native rules
            rules = self.get_morphik_native_rules()
            
            logger.info(f"🔄 Ingesting {file_path.name} with Morphik's native multimodal capabilities")
            logger.info(f"📄 File size: {file_path.stat().st_size / (1024 * 1024):.1f}MB")
            logger.info(f"🎯 Using {len(rules)} rules + ColPali native visual understanding")
            
            # Use filename as external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Ingest with ColPali enabled for native visual processing
            doc = self.db.ingest_file(
                file_path,
                filename=external_id,
                rules=rules,
                use_colpali=True  # Enable Morphik's native visual understanding
            )
            
            logger.info(f"📋 Document ingested: {doc.external_id}")
            
            # Wait for processing
            logger.info("⏳ Processing with Morphik's native multimodal capabilities...")
            
            try:
                # Wait for completion
                doc.wait_for_completion(timeout_seconds=900)
                
                ingestion_time = time.time() - start_time
                status_value = doc.status['status'] if isinstance(doc.status, dict) else doc.status
                
                if status_value == 'completed':
                    logger.info(f"✅ Native processing completed in {ingestion_time:.1f}s")
                    
                    # Get the processed document
                    refreshed_doc = self.db.get_document(doc.external_id)
                    
                    # Test native multimodal capabilities
                    document_info = self.analyze_with_native_capabilities(refreshed_doc)
                    
                    self.ingested_docs.append({
                        'file': str(file_path),
                        'external_id': external_id,
                        'info': document_info,
                        'processing_time': ingestion_time,
                        'method_used': 'Morphik native multimodal with ColPali',
                        'native_processing': True
                    })
                    
                    logger.info(f"🎉 Successfully processed {file_path.name} with native capabilities")
                    return True
                    
                else:
                    # Processing failed
                    full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                    error_message = full_status.get('error', f'Processing failed: {status_value}')
                    logger.error(f"❌ Native processing failed for {file_path.name}: {error_message}")
                    self.failed_docs.append({'file': str(file_path), 'error': error_message})
                    return False
                    
            except Exception as timeout_error:
                logger.error(f"⏰ Timeout during native processing: {timeout_error}")
                self.failed_docs.append({'file': str(file_path), 'error': str(timeout_error)})
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False
    
    def analyze_with_native_capabilities(self, document) -> Dict:
        """Analyze document using Morphik's native multimodal capabilities."""
        try:
            logger.info("🔍 Analyzing document with Morphik's native multimodal capabilities")
            
            # Test queries to understand what Morphik extracted
            test_queries = [
                "ECSS requirements and specifications",
                "diagrams tables figures visual elements",
                "verification procedures and methods",
                "technical specifications and parameters"
            ]
            
            analysis_results = {
                'source': 'morphik_native_multimodal',
                'document_id': document.external_id,
                'analysis_queries': [],
                'visual_understanding': {},
                'text_content': {},
                'total_sources_found': 0,
                'multimodal_capability': True
            }
            
            for query in test_queries:
                try:
                    logger.info(f"   Testing query: '{query}'")
                    
                    # Use Morphik's native query with visual understanding
                    response = self.db.query(query, use_colpali=True, k=5)
                    
                    query_result = {
                        'query': query,
                        'response': response.response if hasattr(response, 'response') else '',
                        'sources_count': len(response.sources) if response.sources else 0,
                        'visual_sources': 0,
                        'text_sources': 0,
                        'morphik_understanding': True
                    }
                    
                    # Analyze sources
                    if response.sources:
                        for source in response.sources:
                            # Check for visual content processed by ColPali
                            if hasattr(source, 'content') and source.content:
                                if hasattr(source.content, '__class__') and 'PIL' in str(type(source.content).__module__):
                                    query_result['visual_sources'] += 1
                                else:
                                    query_result['text_sources'] += 1
                            elif hasattr(source, 'text'):
                                query_result['text_sources'] += 1
                    
                    analysis_results['analysis_queries'].append(query_result)
                    analysis_results['total_sources_found'] += query_result['sources_count']
                    
                except Exception as e:
                    logger.warning(f"Query '{query}' failed: {e}")
                    analysis_results['analysis_queries'].append({
                        'query': query,
                        'error': str(e),
                        'sources_count': 0
                    })
            
            # Summarize findings
            total_visual = sum(q.get('visual_sources', 0) for q in analysis_results['analysis_queries'])
            total_text = sum(q.get('text_sources', 0) for q in analysis_results['analysis_queries'])
            
            analysis_results['visual_understanding'] = {
                'total_visual_sources': total_visual,
                'visual_processing_active': total_visual > 0,
                'colpali_enabled': True
            }
            
            analysis_results['text_content'] = {
                'total_text_sources': total_text,
                'text_processing_active': total_text > 0
            }
            
            logger.info(f"📊 Native analysis complete:")
            logger.info(f"   • Total sources: {analysis_results['total_sources_found']}")
            logger.info(f"   • Visual sources: {total_visual}")
            logger.info(f"   • Text sources: {total_text}")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"❌ Native analysis failed: {e}")
            return {
                'source': 'morphik_native_multimodal',
                'error': str(e),
                'analysis_queries': [],
                'total_sources_found': 0
            }
    
    def native_multimodal_search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search using Morphik's native multimodal capabilities."""
        try:
            logger.info(f"🔍 Native multimodal search for: '{query}'")
            
            # Use Morphik's native query with visual understanding
            response = self.db.query(query, use_colpali=True, k=limit)
            
            if not response.sources:
                logger.warning(f"No results found for query: '{query}'")
                return []
            
            # Process results
            results = []
            for i, source in enumerate(response.sources):
                result = {
                    'index': i,
                    'relevance_score': getattr(source, 'score', 0.0),
                    'document_id': getattr(source, 'document_id', 'unknown'),
                    'morphik_native': True,
                    'multimodal_search': True
                }
                
                # Process content with native understanding
                if hasattr(source, 'content') and source.content:
                    content = source.content
                    
                    # Visual content processed by ColPali
                    if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                        result.update({
                            'type': 'visual',
                            'text': f"[Visual Content] Processed by Morphik's ColPali: {type(content).__name__}",
                            'summary': f"Visual element understood by Morphik's native capabilities",
                            'content_type': 'visual',
                            'native_visual_processing': True
                        })
                    else:
                        result.update({
                            'type': 'text',
                            'text': str(content),
                            'summary': str(content)[:200] + "..." if len(str(content)) > 200 else str(content),
                            'content_type': 'text'
                        })
                
                elif hasattr(source, 'text'):
                    result.update({
                        'type': 'text',
                        'text': source.text,
                        'summary': source.text[:200] + "..." if len(source.text) > 200 else source.text,
                        'content_type': 'text'
                    })
                
                results.append(result)
            
            logger.info(f"✅ Found {len(results)} results using native multimodal capabilities")
            return results
            
        except Exception as e:
            logger.error(f"❌ Native multimodal search failed: {e}")
            return []
    
    def get_suitable_files(self, pdf_dir: Path, max_docs: int = None) -> List[Path]:
        """Get suitable files for ingestion."""
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return []
        
        # Filter for cost control
        suitable_files = []
        for pdf_file in pdf_files:
            file_size_kb = pdf_file.stat().st_size / 1024
            if file_size_kb < 300:
                suitable_files.append((pdf_file, file_size_kb))
        
        if not suitable_files:
            logger.error("No suitable files found (under 300KB)")
            return []
        
        # Sort by size
        suitable_files.sort(key=lambda x: x[1])
        
        if max_docs:
            suitable_files = suitable_files[:max_docs]
        
        logger.info(f"Found {len(suitable_files)} suitable files:")
        for file_info in suitable_files:
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        
        return [file_info[0] for file_info in suitable_files]
    
    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents with native multimodal capabilities."""
        logger.info(f"🚀 Starting native multimodal batch ingestion from {pdf_dir}")
        
        # Get suitable files
        pdf_files = self.get_suitable_files(pdf_dir, max_docs)
        if not pdf_files:
            return {'error': 'No suitable files found'}
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"📄 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document_with_native_multimodal(pdf_file):
                successful += 1
                logger.info(f"✅ Successfully processed {pdf_file.name}")
            else:
                logger.error(f"❌ Failed to process {pdf_file.name}")
            
            # Delay between ingestions
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
            'selected_files': [f.name for f in pdf_files],
            'native_multimodal': True
        }

def main():
    """Main function demonstrating Morphik's native multimodal capabilities."""
    print("🚀 Morphik Native ECSS Document Ingestion")
    print("=" * 60)
    print("✨ Features:")
    print("   • Morphik's native ColPali visual understanding")
    print("   • Built-in multimodal search capabilities")
    print("   • No external OCR dependencies")
    print("   • Integrated text and visual processing")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize native ingestion system
    try:
        ingestion = MorphikNativeECSSIngestion(morphik_uri)
        print("✅ Native multimodal ingestion system initialized")
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
    print("🔍 Using Morphik's native multimodal capabilities")
    
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
    
    print(f"\n📋 Will process {len(preview_files)} documents:")
    for f in preview_files:
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f}KB)")
    
    # Confirm
    confirm = input(f"\n🚀 Proceed with native multimodal processing? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Processing cancelled")
        return
    
    print("\n🔄 Starting native multimodal ingestion...")
    
    # Start ingestion
    summary = ingestion.ingest_documents_batch(pdf_dir, max_docs)
    
    if 'error' in summary:
        print(f"❌ Ingestion failed: {summary['error']}")
        return
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"morphik_native_ingestion_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    # Print summary
    print(f"\n🎉 Native multimodal ingestion completed:")
    print(f"   📄 Total documents: {summary['total_documents']}")
    print(f"   ✅ Successful: {summary['successful_ingestions']}")
    print(f"   ❌ Failed: {summary['failed_ingestions']}")
    print(f"   📊 Success rate: {summary['success_rate']:.1f}%")
    print(f"   ⏱️  Total time: {summary['total_time']:.1f}s")
    print(f"   🔍 Native multimodal: {summary['native_multimodal']}")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Test native multimodal search
    if summary['successful_ingestions'] > 0:
        print(f"\n🔍 Testing native multimodal search...")
        test_queries = [
            "ECSS requirements and specifications",
            "verification procedures and methods",
            "diagrams tables and figures"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            results = ingestion.native_multimodal_search(query, limit=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"   📄 Result {i} ({result['type']}):")
                    print(f"      Score: {result['relevance_score']:.3f}")
                    print(f"      Summary: {result['summary'][:100]}...")
                    if result['type'] == 'visual':
                        print(f"      Native visual: {result['native_visual_processing']}")
            else:
                print("   ❌ No results found")

if __name__ == "__main__":
    main() 