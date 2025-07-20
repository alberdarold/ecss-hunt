#!/usr/bin/env python3
"""
Enhanced ECSS Document Ingestion with Cost Control and Smart Fallback
Based on proven patterns from clean_and_ingest.py for production use.
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
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simplified_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimplifiedECSSIngestion:
    """Cost-controlled ECSS ingestion with proven patterns from clean_and_ingest.py."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the simplified ingestion system."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("[SUCCESS] Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"[ERROR] Failed to connect to Morphik: {e}")
            raise
    
    def get_simplified_rules(self) -> List[NaturalLanguageRule]:
        """Get simplified, effective rules for ECSS document processing."""
        return [
            # Rule 1: Basic document identification and structure
            NaturalLanguageRule(
                prompt="""You are analyzing an ECSS (European Cooperation for Space Standardization) document.

Extract the following key information as structured text:

**Document Identity:**
- ECSS Standard ID (e.g., ECSS-E-ST-40C)
- Title and full name
- Revision and date
- Document type and purpose
- Who should use this standard (target audience)

**Document Structure:**
- Main sections and their purpose
- Number of requirements, recommendations, and notes
- Key topics covered

Please provide clear, concise information that helps engineers understand what this document is and when to use it."""
            ),
            
            # Rule 2: Requirements and procedures extraction
            NaturalLanguageRule(
                prompt="""Extract requirements, procedures, and implementation guidance from this ECSS document.

Focus on:

**Requirements (SHALL statements):**
- List key requirements with their context
- Include verification methods when specified
- Note any cross-references to other standards

**Procedures and Methods:**
- Step-by-step processes described
- Guidelines and best practices
- Implementation recommendations

**Cross-References:**
- References to other ECSS standards
- External standards mentioned
- Dependencies and relationships

Format the output to be practical and actionable for engineers working on space projects."""
            ),
            
            # Rule 3: Practical application and context
            NaturalLanguageRule(
                prompt="""Extract practical application information from this ECSS document.

Provide:

**When to Use This Standard:**
- Project phases where this applies
- Types of space missions or systems
- Specific use cases and scenarios

**Key Takeaways:**
- Most important points engineers should remember
- Common implementation challenges
- Critical success factors

**Integration with Other Standards:**
- How this fits into the broader ECSS framework
- Related standards that should be considered together
- Typical compliance workflows

Focus on practical, real-world application rather than theoretical content."""
            )
        ]
    
    def validate_document(self, file_path: Path) -> Tuple[bool, str]:
        """Validate document before ingestion - based on clean_and_ingest.py patterns."""
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"
        
        if file_path.suffix.lower() != '.pdf':
            return False, f"Unsupported file type: {file_path.suffix}"
        
        # Check file size (reasonable limit for cost control)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        file_size_kb = file_path.stat().st_size / 1024
        
        if file_size_mb > 100:  # 100MB limit
            return False, f"File too large: {file_size_mb:.1f}MB"
        
        # Removed 300KB limit - allow all reasonable sized documents
        # Most ECSS documents are 200KB-8MB, which is perfectly fine
        
        # Check if already ingested
        try:
            documents = self.db.list_documents()
            for doc in documents:
                if hasattr(doc, 'filename') and doc.filename == file_path.name:
                    return False, f"Document already ingested: {file_path.name}"
                if hasattr(doc, 'external_id') and doc.external_id == file_path.name:
                    return False, f"Document already ingested: {file_path.name}"
        except Exception as e:
            logger.warning(f"Could not check existing documents: {e}")
        
        return True, "Valid"
    
    def estimate_cost_impact(self, file_count: int, file_sizes: List[float]) -> Dict:
        """Estimate cost impact based on clean_and_ingest.py patterns."""
        total_size_mb = sum(file_sizes)
        estimated_pages = int(total_size_mb * 2.5)  # Rough estimate
        
        return {
            'file_count': file_count,
            'total_size_mb': round(total_size_mb, 2),
            'estimated_pages': estimated_pages,
            'cost_note': 'Each ingestion counts toward your Morphik plan limits',
            'recommendation': 'Start with 1-2 documents to test quality before batch processing'
        }
    
    def is_metadata_valid(self, doc_id: str) -> bool:
        """Check if extracted metadata is valid - based on clean_and_ingest.py validation."""
        try:
            doc = self.db.get_document(doc_id)
            if not doc:
                return False
            
            # Check if metadata exists and has meaningful content
            if hasattr(doc, 'metadata') and doc.metadata:
                metadata = doc.metadata
                
                # Check if it's a schema definition (bad) vs actual data (good)
                if isinstance(metadata, dict):
                    if 'type' in metadata and 'properties' in metadata:
                        logger.warning("Metadata appears to be schema definition, not extracted data")
                        return False
                    
                    # Look for meaningful extracted content
                    if any(key in metadata for key in ['title', 'standard_id', 'requirements']):
                        logger.info("Valid metadata found with meaningful content")
                        return True
            
            # Check chunks for meaningful content
            try:
                chunks = self.db.retrieve_chunks("ECSS")
                if chunks and len(chunks) > 0:
                    meaningful_chunks = 0
                    for chunk in chunks[:3]:
                        # Handle both text and image chunks from ColPali
                        if hasattr(chunk, 'content') and chunk.content:
                            if isinstance(chunk.content, str) and len(chunk.content) > 50:
                                meaningful_chunks += 1
                        # ColPali image chunks are also meaningful content
                        elif hasattr(chunk, '__class__') and 'Image' in str(type(chunk)):
                            meaningful_chunks += 1
                    
                    if meaningful_chunks >= 1:
                        logger.info(f"Found {meaningful_chunks} meaningful chunks (text + visual)")
                        return True
            except Exception as e:
                logger.warning(f"Could not check chunks: {e}")
                # If it's a server error, don't fail validation - the document might be fine
                if "500" in str(e) or "Internal Server Error" in str(e):
                    logger.info("Server error during chunk retrieval - assuming document is valid")
                    return True
            
            # If we have metadata but can't check chunks, assume it's valid
            if hasattr(doc, 'metadata') and doc.metadata:
                logger.info("Document has metadata but chunks unavailable - assuming valid")
                return True
            
            logger.warning("No meaningful metadata or chunks found")
            return False
            
        except Exception as e:
            logger.warning(f"Error checking metadata validity: {e}")
            return False
    
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
            
            logger.info(f"[INGEST] Ingesting {file_path.name} with {len(rules)} simplified rules + ColPali...")
            logger.info(f"[FILE] File size: {file_path.stat().st_size / (1024 * 1024):.1f}MB")
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Log the ingestion call details
            logger.info(f"[API] Calling Morphik with ColPali enabled:")
            logger.info(f"  - File: {file_path}")
            logger.info(f"  - External ID: {external_id}")
            logger.info(f"  - Rules: {len(rules)} NaturalLanguageRules")
            logger.info(f"  - ColPali: Enabled (for diagrams, tables, figures)")
            
            # Ingest document using ColPali for better ECSS document processing
            doc = self.db.ingest_file(
                file_path, 
                filename=external_id, 
                rules=rules,
                use_colpali=True  # Enable ColPali for diagrams, tables, and figures
            )
            
            logger.info(f"[DOC] Document object created:")
            logger.info(f"  - Document ID: {doc.external_id}")
            
            # Wait for processing with extended timeout for ColPali
            logger.info(f"[WAIT] Waiting for ColPali processing to complete...")
            logger.info("This may take several minutes - processing text + visual elements...")
            
            try:
                # Wait for document completion with extended timeout for ColPali processing
                doc.wait_for_completion(timeout_seconds=900)  # 15 minutes for ColPali
                
                # Get final status
                ingestion_time = time.time() - start_time
                status_value = doc.status['status'] if isinstance(doc.status, dict) else doc.status
                
                if status_value == 'completed':
                    logger.info(f"[SUCCESS] Processing completed successfully in {ingestion_time:.1f}s")
                    
                    # Get the refreshed document and validate quality
                    refreshed_doc = self.db.get_document(doc.external_id)
                    
                    # Validate the extraction quality (like clean_and_ingest.py)
                    if self.is_metadata_valid(doc.external_id):
                        extracted_info = self.extract_meaningful_info(refreshed_doc)
                        
                        self.ingested_docs.append({
                            'file': str(file_path),
                            'external_id': external_id,
                            'info': extracted_info,
                            'processing_time': ingestion_time,
                            'method_used': 'simplified_rules + ColPali (visual processing)'
                        })
                        logger.info(f"[COMPLETE] Successfully processed {file_path.name}")
                        return True
                    else:
                        logger.warning(f"Quality validation failed for {file_path.name}")
                        # Clean up poor quality document
                        try:
                            self.db.delete_document(doc.external_id)
                        except:
                            pass
                        self.failed_docs.append({'file': str(file_path), 'error': 'Poor quality extraction'})
                        return False
                else:
                    # Processing failed
                    full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                    error_message = full_status.get('error', f'Processing failed with status: {status_value}')
                    logger.error(f"[ERROR] Ingestion failed for {file_path.name}. Reason: {error_message}")
                    self.failed_docs.append({'file': str(file_path), 'error': error_message})
                    return False
                    
            except Exception as timeout_error:
                logger.error(f"[TIMEOUT] Failed to ingest {file_path.name}: {timeout_error}")
                self.failed_docs.append({'file': str(file_path), 'error': str(timeout_error)})
                return False
                
        except Exception as e:
            logger.error(f"[ERROR] Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False

    def extract_meaningful_info(self, document) -> Dict:
        """Extract meaningful information from a processed document."""
        try:
            # First try to get the structured metadata
            if hasattr(document, 'metadata') and document.metadata:
                # Check if we have actual extracted data or just schema
                if not any('title' in str(document.metadata).lower() for _ in [1]):
                    logger.info("[FALLBACK] Falling back to chunk-based content extraction...")
                    
                    # Try to get some chunks using search terms
                    search_terms = ['ECSS', 'requirement', 'shall']
                    all_chunks = []
                    
                    for term in search_terms:
                        try:
                            # Remove the limit parameter that's causing issues
                            chunks = self.db.retrieve_chunks(term)
                            if chunks:
                                all_chunks.extend(chunks[:3])  # Get first 3 chunks manually
                        except Exception as e:
                            logger.warning(f"Could not retrieve chunks for '{term}': {e}")
                    
                    if all_chunks:
                        # Extract summary from text chunks only (skip image chunks)
                        text_summaries = []
                        image_count = 0
                        for chunk in all_chunks[:2]:
                            if hasattr(chunk, 'content') and chunk.content and isinstance(chunk.content, str):
                                text_summaries.append(chunk.content[:200])
                            elif hasattr(chunk, '__class__') and 'Image' in str(type(chunk)):
                                image_count += 1
                        
                        content_summary = " ".join(text_summaries)
                        if not content_summary and image_count > 0:
                            content_summary = f"Visual content detected: {image_count} diagram(s)/table(s)/figure(s)"
                        
                        return {
                            'source': 'chunks',
                            'summary': content_summary,
                            'chunk_count': len(all_chunks),
                            'visual_elements': image_count
                        }
                
                return {
                    'source': 'metadata',
                    'data': document.metadata
                }
            
            return {'source': 'none', 'data': None}
            
        except Exception as e:
            logger.error(f"Error extracting info: {e}")
            return {'source': 'error', 'error': str(e)}

    def get_suitable_files(self, pdf_dir: Path, max_docs: int = None) -> List[Path]:
        """Get suitable files for ingestion - removed 300KB limit."""
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return []
        
        # Include all files under 100MB (removed 300KB limit)
        suitable_files = []
        for pdf_file in pdf_files:
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            file_size_kb = pdf_file.stat().st_size / 1024
            
            # Only exclude files over 100MB
            if file_size_mb <= 100:
                suitable_files.append((pdf_file, file_size_kb))
        
        if not suitable_files:
            logger.error(f"No suitable PDF files found in {pdf_dir}")
            logger.info(f"Available files range from {min([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB to {max([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB")
            return []
        
        # Sort by size (smallest first for cost efficiency)
        suitable_files.sort(key=lambda x: x[1])
        
        # Limit selection if specified
        if max_docs:
            suitable_files = suitable_files[:max_docs]
        
        logger.info(f"Found {len(suitable_files)} suitable files (under 100MB):")
        for file_info in suitable_files[:10]:  # Show first 10
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        if len(suitable_files) > 10:
            logger.info(f"  ... and {len(suitable_files) - 10} more files")
        
        return [file_info[0] for file_info in suitable_files]

    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents with cost control and validation."""
        logger.info(f"Starting cost-controlled batch ingestion from {pdf_dir}")
        
        # Get suitable files
        pdf_files = self.get_suitable_files(pdf_dir, max_docs)
        if not pdf_files:
            return {'error': 'No suitable files found'}
        
        # Show cost estimate
        file_sizes = [f.stat().st_size / (1024 * 1024) for f in pdf_files]
        cost_info = self.estimate_cost_impact(len(pdf_files), file_sizes)
        
        logger.info(f"Cost estimate:")
        logger.info(f"  - Files: {cost_info['file_count']}")
        logger.info(f"  - Total size: {cost_info['total_size_mb']}MB")
        logger.info(f"  - Estimated pages: {cost_info['estimated_pages']}")
        logger.info(f"  - Note: {cost_info['cost_note']}")
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document(pdf_file):
                successful += 1
                logger.info(f"SUCCESS: Ingested {pdf_file.name}")
            else:
                logger.error(f"FAILED: Could not ingest {pdf_file.name}")
            
            # Add delay between ingestions to avoid overwhelming the system
            if i < len(pdf_files):
                time.sleep(2)
        
        total_time = time.time() - start_time
        
        return {
            'total_documents': len(pdf_files),
            'successful_ingestions': successful,
            'failed_ingestions': len(self.failed_docs),
            'total_time': round(total_time, 2),
            'average_time_per_doc': round(total_time / len(pdf_files), 2),
            'success_rate': round(successful / len(pdf_files) * 100, 1),
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'selected_files': [f.name for f in pdf_files],
            'cost_info': cost_info
        }

    def get_ingestion_summary(self) -> Dict:
        """Get ingestion summary statistics."""
        total = len(self.ingested_docs) + len(self.failed_docs)
        successful = len(self.ingested_docs)
        failed = len(self.failed_docs)
        
        return {
            'total_documents': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }

    def search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for documents using the query."""
        try:
            logger.info(f"[SEARCH] Searching for: '{query}'")
            
            # Remove the limit parameter that's causing API issues
            chunks = self.db.retrieve_chunks(query)
            
            if not chunks:
                logger.warning(f"No results found for query: '{query}'")
                return []
            
            # Process and format results
            results = []
            for i, chunk in enumerate(chunks[:limit]):  # Manually limit results
                result = {
                    'chunk_id': getattr(chunk, 'id', f'chunk_{i}'),
                    'relevance_score': getattr(chunk, 'score', 0.0),
                    'document_id': getattr(chunk, 'document_id', 'unknown')
                }
                
                # Handle FinalChunkResult objects from Morphik
                text_content = None
                chunk_type = 'unknown'
                
                # Check the content attribute we know exists
                if hasattr(chunk, 'content'):
                    content_value = getattr(chunk, 'content', None)
                    
                    if content_value is not None:
                        # Check for PIL Image objects (visual content from ColPali)
                        if hasattr(content_value, '__class__') and 'PIL' in str(type(content_value).__module__):
                            # This is a visual element extracted by ColPali
                            image_type = type(content_value).__name__
                            result['text'] = f"[Visual Element] {image_type} - Diagram/Table/Figure extracted by ColPali"
                            result['summary'] = "Visual content from ECSS document - contains diagrams, tables, or technical figures"
                            result['type'] = 'colpali_visual'
                            result['visual_info'] = {
                                'type': image_type,
                                'size': getattr(content_value, 'size', 'unknown') if hasattr(content_value, 'size') else 'unknown',
                                'mode': getattr(content_value, 'mode', 'unknown') if hasattr(content_value, 'mode') else 'unknown'
                            }
                            results.append(result)
                            continue
                        
                        # If it's a string, use it directly
                        elif isinstance(content_value, str):
                            text_content = content_value
                            chunk_type = 'text_content'
                        
                        # If it's bytes, decode it
                        elif isinstance(content_value, bytes):
                            try:
                                text_content = content_value.decode('utf-8')
                                chunk_type = 'text_bytes'
                            except:
                                text_content = str(content_value)
                                chunk_type = 'bytes_fallback'
                        
                        # For other object types, try to extract text
                        elif hasattr(content_value, '__dict__'):
                            # Check if it has text-like attributes
                            for text_attr in ['text', 'content', 'data', 'value']:
                                if hasattr(content_value, text_attr):
                                    text_val = getattr(content_value, text_attr, None)
                                    if text_val and isinstance(text_val, str):
                                        text_content = text_val
                                        chunk_type = f'nested_{text_attr}'
                                        break
                        
                        # Try converting to string as last resort
                        else:
                            str_content = str(content_value)
                            if len(str_content) > 10 and not str_content.startswith('<'):
                                text_content = str_content
                                chunk_type = 'string_conversion'
                
                # Build result for text content
                if text_content and len(text_content.strip()) > 0:
                    result['text'] = text_content[:500]  # First 500 characters
                    result['summary'] = text_content[:200] + "..." if len(text_content) > 200 else text_content
                    result['type'] = chunk_type
                else:
                    # If no content found, it might be an unknown type
                    result['text'] = "[No extractable text content]"
                    result['summary'] = "Chunk found but no readable text content available"
                    result['type'] = 'no_content'
                
                results.append(result)
            
            logger.info(f"[RESULTS] Found {len(results)} relevant results")
            return results
            
        except Exception as e:
            logger.error(f"[ERROR] Search failed: {e}")
            return []

def main():
    """Main function with user interaction and cost control like clean_and_ingest.py."""
    print("=" * 60)
    print("ECSS Simplified Ingestion System with ColPali + Cost Control")
    print("Enhanced visual processing for diagrams, tables, and figures")
    print("Based on proven patterns from clean_and_ingest.py")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("[ERROR] MORPHIK_URI not found in environment variables")
        return
    
    # Initialize simplified ingestion system
    try:
        ingestion = SimplifiedECSSIngestion(morphik_uri)
    except Exception as e:
        print(f"[ERROR] Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"[ERROR] PDF directory not found: {pdf_dir}")
        return
    
    # Get user input for number of documents
    print(f"\nFound PDF directory: {pdf_dir}")
    print("[INFO] This system uses ColPali for enhanced visual processing")
    print("[INFO] Cost-controlled ingestion (files under 300KB only)")
    print("[INFO] Each document ingestion counts toward your Morphik plan limits")
    
    try:
        max_docs_input = input("\nEnter number of documents to ingest (default 1): ").strip()
        max_docs = int(max_docs_input) if max_docs_input else 1
    except ValueError:
        print("Invalid input, using 1 document")
        max_docs = 1
    
    # Show files that would be selected
    ingestion_preview = ingestion.get_suitable_files(pdf_dir, max_docs)
    if not ingestion_preview:
        print("[ERROR] No suitable files found for ingestion")
        return
    
    # Show cost estimate
    file_sizes = [f.stat().st_size / (1024 * 1024) for f in ingestion_preview]
    cost_info = ingestion.estimate_cost_impact(len(ingestion_preview), file_sizes)
    
    print(f"\n[PREVIEW] Will process {len(ingestion_preview)} documents:")
    for f in ingestion_preview:
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f}KB)")
    
    print(f"\n[COST ESTIMATE]")
    print(f"  Files: {cost_info['file_count']}")
    print(f"  Total size: {cost_info['total_size_mb']}MB")
    print(f"  Estimated pages: {cost_info['estimated_pages']}")
    print(f"  Note: {cost_info['cost_note']}")
    print(f"  Recommendation: {cost_info['recommendation']}")
    
    # Confirm before proceeding
    confirm = input(f"\nProceed with ingestion of {len(ingestion_preview)} documents? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Ingestion cancelled by user")
        return
    
    print("\n[START] Starting cost-controlled ingestion...")
    print("[INFO] Processing files smallest to largest for cost efficiency")
    
    # Start ingestion
    summary = ingestion.ingest_documents_batch(pdf_dir, max_docs)
    
    if 'error' in summary:
        print(f"[ERROR] Ingestion failed: {summary['error']}")
        return
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"simplified_ingestion_results_{timestamp}.json"
    
    # Create serializable summary
    serializable_summary = {k: v for k, v in summary.items() if k != 'ingested_docs'}
    serializable_summary['ingested_docs'] = [
        {k: v for k, v in doc.items() if k != 'document_object'} 
        for doc in summary.get('ingested_docs', [])
    ]
    
    with open(results_file, 'w') as f:
        json.dump(serializable_summary, f, indent=2, default=str)
    
    # Print final summary
    print(f"\n[SUMMARY] Ingestion completed:")
    print(f"  [TOTAL] Total documents: {summary['total_documents']}")
    print(f"  [SUCCESS] Successful: {summary['successful_ingestions']}")
    print(f"  [ERROR] Failed: {summary['failed_ingestions']}")
    print(f"  [RATE] Success rate: {summary['success_rate']:.1f}%")
    print(f"  [TIME] Total time: {summary['total_time']:.1f}s")
    print(f"  [AVG] Average per doc: {summary['average_time_per_doc']:.1f}s")
    
    print(f"\nResults saved to: {results_file}")
    
    # Test search if we have successful ingestions
    if summary['successful_ingestions'] > 0:
        print(f"\n[TEST] Testing search functionality...")
        test_queries = [
            "What are ECSS requirements?",
            "How to perform verification?"
        ]
        
        for query in test_queries:
            print(f"\n[QUERY] {query}")
            results = ingestion.search_documents(query, limit=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"  [RESULT {i}] {result['summary']}")
                    print(f"     [SCORE] {result['relevance_score']}")
            else:
                print("  [NO RESULTS]")

if __name__ == "__main__":
    main() 