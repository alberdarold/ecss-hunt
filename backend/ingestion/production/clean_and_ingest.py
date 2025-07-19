#!/usr/bin/env python3
"""
Enhanced ECSS Document Ingestion with Morphik Rules-Based Processing
Uses Morphik's NaturalLanguageRule for robust metadata extraction and content transformation.
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
import re
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import pdfplumber

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ECSSRulesBasedIngestion:
    """Enhanced ECSS ingestion using Morphik's NaturalLanguageRule."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the rules-based ingestion system."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        self.rules_cache = {}
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Morphik: {e}")
            raise
    
    def _extract_text_from_pdf_local(self, file_path: Path) -> Optional[str]:
        """Extract all text content from a PDF file using pdfplumber."""
        if not file_path.exists():
            logger.error(f"PDF file not found at {file_path}")
            return None
        
        try:
            logger.info(f"Extracting text from {file_path.name} with pdfplumber...")
            full_text = []
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
                    else:
                        logger.warning(f"No text found on page {i+1} of {file_path.name}")
            
            if not full_text:
                logger.error(f"Failed to extract any text from {file_path.name}")
                return None
            
            logger.info(f"Successfully extracted text from {len(pdf.pages)} pages.")
            return "\\n".join(full_text)
        except Exception as e:
            logger.error(f"An error occurred during PDF text extraction for {file_path.name}: {e}", exc_info=True)
            return None
    
    def get_ecss_nl_rules(self) -> List[NaturalLanguageRule]:
        """Get NaturalLanguageRule-based rules for ECSS document processing, fully aligned with ECSS/ESA structure and golden rules."""
        cache_key = "ecss_nl_rules"
        if cache_key in self.rules_cache:
            return self.rules_cache[cache_key]

        rules = [
            # 1. Standard metadata and structure
            NaturalLanguageRule(
                prompt="""Extract the following ECSS standard metadata as JSON:
- standard_id, branch, discipline, title, revision, date, status, scope, keywords, applicable_domains
- For each main section (scope, normative reference, terms, requirements, annexes, bibliography), provide a summary of its content.
"""
            ),
            # 2. Section information
            NaturalLanguageRule(
                prompt="""For each section, extract:
- section_number, section_title, section_type (normative/informative/annex/note), is_normative, is_informative, content_summary
- Count of requirements, recommendations, permissions, figures, tables.
"""
            ),
            # 3. Requirements, recommendations, permissions
            NaturalLanguageRule(
                prompt="""For every normative statement, extract:
- unique_id, statement, requirement_type (requirement, recommendation, permission), is_normative, section_number, cross_references, verification_method, applicable_phases, notes.
"""
            ),
            # 4. Cross-references
            NaturalLanguageRule(
                prompt="""Extract all cross-references (internal and external) as:
- source_id, target, target_type (internal, external), context.
"""
            ),
            # 5. Annexes
            NaturalLanguageRule(
                prompt="""For each annex, extract:
- annex_id, title, is_normative, content_summary.
"""
            ),
            # 6. Notes
            NaturalLanguageRule(
                prompt="""For each note, extract:
- note_id, related_to (requirement id), content.
"""
            ),
            # 7. Tables
            NaturalLanguageRule(
                prompt="""For each table, extract:
- table_number, table_title, table_type (requirements, parameters, classifications), row_count, column_count, content_summary, key_parameters, section_number.
"""
            ),
            # 8. Figures
            NaturalLanguageRule(
                prompt="""For each figure, extract:
- figure_number, figure_title, diagram_type (flowchart, block diagram, schematic), content_description, components, relationships, section_number.
"""
            ),
        ]
        self.rules_cache[cache_key] = rules
        logger.info(f"Generated {len(rules)} ECSS/ESA-aligned NaturalLanguageRule-based rules for ECSS document processing")
        return rules
    
    def get_ecss_metadata_rules_with_images(self) -> List[MetadataExtractionRule]:
        """Get MetadataExtractionRule-based rules with image support for ECSS document processing, fully aligned with ECSS/ESA structure and golden rules."""
        # Check cache first
        cache_key = "ecss_metadata_rules_with_images"
        if cache_key in self.rules_cache:
            return self.rules_cache[cache_key]

        # --- ECSS-aligned schemas ---
        class ECSSStandardMetadata(BaseModel):
            standard_id: str
            branch: str
            discipline: str
            title: str
            revision: str
            date: str
            status: str
            scope: str
            keywords: List[str]
            applicable_domains: List[str]
            structure: Dict[str, str]  # e.g. {"scope": ..., "normative_reference": ..., ...}

        class ECSSSectionInfo(BaseModel):
            section_number: str
            section_title: str
            section_type: str  # "normative", "informative", "annex", "note"
            is_normative: bool
            is_informative: bool
            content_summary: str
            requirements_count: int
            recommendations_count: int
            permissions_count: int
            figures_count: int
            tables_count: int

        class ECSSRequirement(BaseModel):
            unique_id: str
            statement: str
            requirement_type: str  # "requirement", "recommendation", "permission"
            is_normative: bool
            section_number: str
            cross_references: List[str]
            verification_method: str
            applicable_phases: List[str]
            notes: List[str]

        class ECSSCrossReference(BaseModel):
            source_id: str
            target: str
            target_type: str  # "internal", "external"
            context: str

        class ECSSAnnexInfo(BaseModel):
            annex_id: str
            title: str
            is_normative: bool
            content_summary: str

        class ECSSNoteInfo(BaseModel):
            note_id: str
            related_to: str  # requirement id
            content: str

        class ECSSTableInfo(BaseModel):
            table_number: str
            table_title: str
            table_type: str  # e.g. "requirements", "parameters", "classifications"
            row_count: int
            column_count: int
            content_summary: str
            key_parameters: List[str]
            section_number: str

        class ECSSFigureInfo(BaseModel):
            figure_number: str
            figure_title: str
            diagram_type: str  # e.g. "flowchart", "block diagram", "schematic"
            content_description: str
            components: List[str]
            relationships: List[str]
            section_number: str

        # --- ECSS-aligned extraction rules ---
        rules = [
            # Standard metadata and structure
            MetadataExtractionRule(
                schema=ECSSStandardMetadata,
                stage="post_chunking",
                use_images=True
            ),
            # Section info
            MetadataExtractionRule(
                schema=ECSSSectionInfo,
                stage="post_chunking",
                use_images=True
            ),
            # Requirements, recommendations, permissions
            MetadataExtractionRule(
                schema=ECSSRequirement,
                stage="post_chunking",
                use_images=True
            ),
            # Cross-references
            MetadataExtractionRule(
                schema=ECSSCrossReference,
                stage="post_chunking",
                use_images=True
            ),
            # Annexes
            MetadataExtractionRule(
                schema=ECSSAnnexInfo,
                stage="post_chunking",
                use_images=True
            ),
            # Notes
            MetadataExtractionRule(
                schema=ECSSNoteInfo,
                stage="post_chunking",
                use_images=True
            ),
            # Tables
            MetadataExtractionRule(
                schema=ECSSTableInfo,
                stage="post_chunking",
                use_images=True
            ),
            # Figures
            MetadataExtractionRule(
                schema=ECSSFigureInfo,
                stage="post_chunking",
                use_images=True
            ),
        ]

        # Cache the rules
        self.rules_cache[cache_key] = rules
        logger.info(f"Generated {len(rules)} ECSS/ESA-aligned MetadataExtractionRule-based rules with image support for ECSS document processing")
        return rules
    
    def validate_document(self, file_path: Path) -> Tuple[bool, str]:
        """Validate document before ingestion."""
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"
        
        if file_path.suffix.lower() != '.pdf':
            return False, f"Unsupported file type: {file_path.suffix}"
        
        # Check file size (reasonable limit)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 100:  # 100MB limit
            return False, f"File too large: {file_size_mb:.1f}MB"
        
        # Check if already ingested
        try:
            documents = self.db.list_documents()
            for doc in documents:
                if hasattr(doc, 'filename') and doc.filename == file_path.name:
                    return False, f"Document already ingested: {file_path.name}"
        except Exception as e:
            logger.warning(f"Could not check existing documents: {e}")
        
        return True, "Valid"
    
    def estimate_ingestion_cost(self, file_path: Path) -> Dict:
        """Estimate ingestion cost using Morphik's flat-rate model."""
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        # Estimate pages (rough calculation: 1MB ≈ 2-3 pages)
        estimated_pages = int(file_size_mb * 2.5)
        
        # Morphik Pro plan: $35/month for 1,000 pages
        # Since it's flat-rate, cost is $0 for additional pages within plan
        cost_info = {
            'file_size_mb': round(file_size_mb, 2),
            'estimated_pages': estimated_pages,
            'cost_usd': 0.0,  # Flat-rate plan
            'plan_usage': f"{estimated_pages}/1000 pages",
            'within_plan': estimated_pages <= 1000
        }
        
        return cost_info
    
    def ingest_document_with_rules(self, file_path: Path) -> bool:
        """Ingest a single document using Morphik's native file processing."""
        try:
            # Validate document
            is_valid, validation_msg = self.validate_document(file_path)
            if not is_valid:
                logger.warning(f"Document validation failed: {validation_msg}")
                self.failed_docs.append({'file': str(file_path), 'error': validation_msg})
                return False
            
            # Get NaturalLanguageRule-based rules
            rules = self.get_ecss_nl_rules()
            
            logger.info(f"Ingesting {file_path.name} with {len(rules)} NaturalLanguageRules...")
            logger.info(f"File size: {file_path.stat().st_size / 1024:.1f}KB")
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Log the ingestion call details
            logger.info(f"Calling db.ingest_file with:")
            logger.info(f"  - file_path: {file_path}")
            logger.info(f"  - filename: {external_id}")
            logger.info(f"  - rules count: {len(rules)}")
            logger.info(f"  - use_colpali: False")
            
            doc = self.db.ingest_file(
                file_path, 
                filename=external_id, 
                rules=rules,
                use_colpali=False  # Explicitly disable image-based pipeline
            )
            
            logger.info(f"Document object created:")
            logger.info(f"  - Document ID: {doc.external_id}")
            logger.info(f"  - Initial status: {doc.status}")
            logger.info(f"  - Document type: {type(doc)}")

            # Custom waiting logic for text processing
            logger.info(f"Waiting for NaturalLanguageRules to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Custom waiting logic to bypass SDK timeout
            max_wait_time = 600  # 10 minutes maximum wait for text processing
            check_interval = 10   # Check every 10 seconds
            start_wait = time.time()
            
            while True:
                current_status = doc.status
                
                # Check if completed
                if isinstance(current_status, dict):
                    status_value = current_status.get('status', 'unknown')
                else:
                    status_value = current_status
                
                if status_value == 'completed':
                    logger.info("NaturalLanguageRule processing completed successfully")
                    break
                elif status_value in ['failed', 'error']:
                    logger.error(f"Document processing failed with status: {status_value}")
                    self.failed_docs.append({'file': str(file_path), 'error': f"Processing failed with status: {status_value}"})
                    return False
                
                # Check if we've been waiting too long
                elapsed = time.time() - start_wait
                if elapsed > max_wait_time:
                    logger.error(f"Document processing exceeded {max_wait_time} seconds")
                    self.failed_docs.append({'file': str(file_path), 'error': f"Processing exceeded {max_wait_time} seconds"})
                    return False
                
                logger.info(f"Still processing... (elapsed: {elapsed:.0f}s, status: {status_value})")
                time.sleep(check_interval)
            
            ingestion_time = time.time() - start_time
            
            # Check the final status
            status_value = doc.status.get('status', 'unknown') if isinstance(doc.status, dict) else doc.status

            if status_value == 'completed':
                logger.info("NaturalLanguageRule processing complete.")
                refreshed_doc = self.db.get_document(doc.external_id)
                if not refreshed_doc:
                    raise ValueError(f"Failed to re-fetch document {doc.external_id} after completion.")
                
                extracted_metadata = self.get_extracted_metadata_from_chunks(refreshed_doc.external_id)
                
                self.ingested_docs.append({
                    'filename': file_path.name,
                    'document_id': refreshed_doc.external_id,
                    'extracted_metadata': extracted_metadata,
                    'ingestion_time': round(ingestion_time, 2),
                    'document_object': refreshed_doc,
                    'method_used': 'text-based (NaturalLanguageRule)'
                })
                return True
            else:
                full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                error_message = full_status.get('error', f'Processing failed with status: {status_value}')
                logger.error(f"Ingestion failed for {file_path.name}. Reason: {error_message}")
                self.failed_docs.append({'file': str(file_path), 'error': error_message})
                return False
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path.name}: {e}", exc_info=True)
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False
    
    def get_extracted_metadata_from_chunks(self, doc_id: str) -> Dict:
        """Retrieve extracted metadata from chunks since metadata field may not be populated."""
        try:
            # Search for metadata-related chunks
            search_terms = ["ECSS", "standard", "requirement", "metadata"]
            extracted_data = {}
            
            for term in search_terms:
                try:
                    chunks = self.db.retrieve_chunks(term)
                    if chunks:
                        extracted_data[term] = []
                        for chunk in chunks[:3]:  # Get first 3 chunks
                            if hasattr(chunk, 'content') and chunk.content:
                                content = chunk.content
                                if isinstance(content, str) and len(content) > 20:
                                    extracted_data[term].append(content)
                except Exception as e:
                    logger.warning(f"Could not retrieve chunks for '{term}': {e}")
            
            return extracted_data
            
        except Exception as e:
            logger.warning(f"Could not extract metadata from chunks: {e}")
            return {}
    
    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents with NaturalLanguageRule-based processing."""
        logger.info(f"Starting NaturalLanguageRule-based ingestion from {pdf_dir}")
        
        # Find PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return {'error': 'No PDF files found'}
        
        # Filter files under 300KB and randomly select
        small_files = []
        for pdf_file in pdf_files:
            file_size_kb = pdf_file.stat().st_size / 1024
            if file_size_kb < 300:
                small_files.append((pdf_file, file_size_kb))
        
        if not small_files:
            logger.error(f"No PDF files under 300KB found in {pdf_dir}")
            logger.info(f"Available files range from {min([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB to {max([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB")
            return {'error': 'No PDF files under 300KB found'}
        
        # Randomly select files
        if max_docs:
            selected_files = random.sample(small_files, min(max_docs, len(small_files)))
        else:
            selected_files = random.sample(small_files, min(1, len(small_files)))  # Default to 1 file
        
        # Extract just the file paths
        pdf_files = [file_info[0] for file_info in selected_files]
        
        logger.info(f"Randomly selected {len(pdf_files)} files under 300KB:")
        for file_info in selected_files:
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document_with_rules(pdf_file):
                successful += 1
                logger.info(f"SUCCESS: Ingested {pdf_file.name}")
            
            # Add delay between ingestions to avoid overwhelming the system
            time.sleep(1)
        
        total_time = time.time() - start_time
        
        # Generate summary
        summary = {
            'total_documents': len(pdf_files),
            'successful_ingestions': successful,
            'failed_ingestions': len(self.failed_docs),
            'total_time': round(total_time, 2),
            'average_time_per_doc': round(total_time / len(pdf_files), 2),
            'success_rate': round(successful / len(pdf_files) * 100, 1),
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'selected_files': [f.name for f in pdf_files]
        }
        
        logger.info(f"Ingestion complete: {successful}/{len(pdf_files)} successful")
        logger.info(f"Total time: {total_time:.2f}s, Average: {summary['average_time_per_doc']:.2f}s per doc")
        
        return summary
    
    def create_graphs_with_rules(self) -> bool:
        """Create knowledge graphs using the ingested documents."""
        try:
            logger.info("Creating ECSS knowledge graphs...")
            
            # Get the list of successfully ingested document objects
            successful_docs = [item['document_object'] for item in self.ingested_docs if 'document_object' in item]
            if not successful_docs:
                logger.warning("No successfully ingested documents available to create graphs.")
                return False
            
            # Create a comprehensive knowledge graph
            try:
                graph_prompt = """Create a comprehensive knowledge graph for ECSS standards that includes:
1. Document relationships (references, dependencies)
2. Requirement hierarchies and dependencies
3. Technical concept relationships
4. Cross-standard connections
5. Verification and validation relationships
6. Process and workflow connections

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
                
                graph = self.db.create_knowledge_graph(
                    prompt=graph_prompt,
                    name="ECSS Standards Knowledge Graph"
                )
                
                if graph:
                    logger.info("Created ECSS knowledge graph successfully")
                    logger.info(f"   Graph ID: {graph.id}")
                else:
                    logger.error("Failed to create ECSS knowledge graph")
                    
            except Exception as e:
                logger.error(f"Failed to create ECSS knowledge graph: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create knowledge graphs: {e}")
            return False

    def ingest_document_with_image_support(self, file_path: Path) -> bool:
        """Ingest a single document using MetadataExtractionRule with image support."""
        try:
            # Validate document
            is_valid, validation_msg = self.validate_document(file_path)
            if not is_valid:
                logger.warning(f"Document validation failed: {validation_msg}")
                self.failed_docs.append({'file': str(file_path), 'error': validation_msg})
                return False
            
            # Get MetadataExtractionRule-based rules with image support
            metadata_rules = self.get_ecss_metadata_rules_with_images()
            nl_rules = self.get_ecss_nl_rules()
            all_rules = metadata_rules + nl_rules
            
            logger.info(f"Ingesting {file_path.name} with {len(metadata_rules)} MetadataExtractionRules (with image support) and {len(nl_rules)} NaturalLanguageRules...")
            logger.info(f"File size: {file_path.stat().st_size / 1024:.1f}KB")
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            
            # Log the ingestion call details
            logger.info(f"Calling db.ingest_file with:")
            logger.info(f"  - file_path: {file_path}")
            logger.info(f"  - filename: {external_id}")
            logger.info(f"  - metadata rules count: {len(metadata_rules)}")
            logger.info(f"  - nl rules count: {len(nl_rules)}")
            logger.info(f"  - use_colpali: True (for image processing)")
            
            doc = self.db.ingest_file(
                file_path, 
                filename=external_id, 
                rules=all_rules,
                use_colpali=True   # Enable image-based processing
            )
            
            logger.info(f"Document object created:")
            logger.info(f"  - Document ID: {doc.external_id}")
            logger.info(f"  - Initial status: {doc.status}")
            logger.info(f"  - Document type: {type(doc)}")

            # Custom waiting logic with longer timeout for image processing
            logger.info(f"Waiting for MetadataExtractionRules with image support to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Custom waiting logic to bypass SDK timeout
            max_wait_time = 1800  # 30 minutes maximum wait for image processing
            check_interval = 10   # Check every 10 seconds
            start_wait = time.time()
            
            while True:
                current_status = doc.status
                
                # Check if completed
                if isinstance(current_status, dict):
                    status_value = current_status.get('status', 'unknown')
                else:
                    status_value = current_status
                
                if status_value == 'completed':
                    logger.info("MetadataExtractionRule with image support processing completed successfully")
                    break
                elif status_value in ['failed', 'error']:
                    logger.error(f"Document processing failed with status: {status_value}")
                    self.failed_docs.append({'file': str(file_path), 'error': f"Processing failed with status: {status_value}"})
                    return False
                
                # Check if we've been waiting too long
                elapsed = time.time() - start_wait
                if elapsed > max_wait_time:
                    logger.error(f"Document processing exceeded {max_wait_time} seconds")
                    self.failed_docs.append({'file': str(file_path), 'error': f"Processing exceeded {max_wait_time} seconds"})
                    return False
                
                logger.info(f"Still processing... (elapsed: {elapsed:.0f}s, status: {status_value})")
                time.sleep(check_interval)
            
            ingestion_time = time.time() - start_time
            
            # Check the final status
            status_value = doc.status.get('status', 'unknown') if isinstance(doc.status, dict) else doc.status

            if status_value == 'completed':
                logger.info("MetadataExtractionRule with image support processing complete.")
                refreshed_doc = self.db.get_document(doc.external_id)
                if not refreshed_doc:
                    raise ValueError(f"Failed to re-fetch document {doc.external_id} after completion.")
                
                extracted_metadata = self.get_extracted_metadata_from_chunks(refreshed_doc.external_id)
                
                self.ingested_docs.append({
                    'filename': file_path.name,
                    'document_id': refreshed_doc.external_id,
                    'extracted_metadata': extracted_metadata,
                    'ingestion_time': round(ingestion_time, 2),
                    'document_object': refreshed_doc,
                    'method_used': 'image-based (MetadataExtractionRule with images)'
                })
                return True
            else:
                full_status = doc.status if isinstance(doc.status, dict) else {'status': doc.status}
                error_message = full_status.get('error', f'Processing failed with status: {status_value}')
                logger.error(f"Ingestion failed for {file_path.name}. Reason: {error_message}")
                self.failed_docs.append({'file': str(file_path), 'error': error_message})
                return False
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path.name}: {e}", exc_info=True)
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False

    def ingest_documents_batch_with_images(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents with MetadataExtractionRule and image support."""
        logger.info(f"Starting MetadataExtractionRule with image support ingestion from {pdf_dir}")
        
        # Find PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return {'error': 'No PDF files found'}
        
        # Filter files under 300KB and randomly select
        small_files = []
        for pdf_file in pdf_files:
            file_size_kb = pdf_file.stat().st_size / 1024
            if file_size_kb < 300:
                small_files.append((pdf_file, file_size_kb))
        
        if not small_files:
            logger.error(f"No PDF files under 300KB found in {pdf_dir}")
            logger.info(f"Available files range from {min([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB to {max([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB")
            return {'error': 'No PDF files under 300KB found'}
        
        # Randomly select files
        if max_docs:
            selected_files = random.sample(small_files, min(max_docs, len(small_files)))
        else:
            selected_files = random.sample(small_files, min(1, len(small_files)))  # Default to 1 file
        
        # Extract just the file paths
        pdf_files = [file_info[0] for file_info in selected_files]
        
        logger.info(f"Randomly selected {len(pdf_files)} files under 300KB:")
        for file_info in selected_files:
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        
        # Process documents
        start_time = time.time()
        successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.ingest_document_with_image_support(pdf_file):
                successful += 1
                logger.info(f"SUCCESS: Ingested {pdf_file.name} with image support")
            
            # Add delay between ingestions to avoid overwhelming the system
            time.sleep(1)
        
        total_time = time.time() - start_time
        
        # Generate summary
        summary = {
            'total_documents': len(pdf_files),
            'successful_ingestions': successful,
            'failed_ingestions': len(self.failed_docs),
            'total_time': round(total_time, 2),
            'average_time_per_doc': round(total_time / len(pdf_files), 2),
            'success_rate': round(successful / len(pdf_files) * 100, 1),
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'selected_files': [f.name for f in pdf_files]
        }
        
        logger.info(f"Ingestion complete: {successful}/{len(pdf_files)} successful")
        logger.info(f"Total time: {total_time:.2f}s, Average: {summary['average_time_per_doc']:.2f}s per doc")
        
        return summary

    def is_metadata_valid(self, doc_id: str) -> bool:
        """Check if the extracted metadata is valid and of good quality."""
        try:
            # Get the document
            doc = self.db.get_document(doc_id)
            if not doc:
                return False
            
            # Check if metadata exists and has meaningful content
            if hasattr(doc, 'metadata') and doc.metadata:
                metadata = doc.metadata
                
                # Check if it's a schema definition (bad) vs actual data (good)
                if isinstance(metadata, dict):
                    # If it looks like a schema definition, it's invalid
                    if 'type' in metadata and 'properties' in metadata:
                        logger.warning(f"Metadata appears to be schema definition, not extracted data")
                        return False
                    
                    # Check if we have meaningful extracted data
                    if 'title' in metadata and isinstance(metadata['title'], str):
                        title = metadata['title'].strip()
                        if len(title) > 10:  # Title should be substantial
                            logger.info(f"Valid metadata found with title: {title[:50]}...")
                            return True
                        else:
                            logger.warning(f"Title too short: '{title}'")
                            return False
            
            # Check chunks for meaningful content
            chunks = self.db.retrieve_chunks("ECSS")
            if chunks and len(chunks) > 0:
                # Check if chunks contain meaningful text
                meaningful_chunks = 0
                for chunk in chunks[:3]:  # Check first 3 chunks
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        if isinstance(content, str) and len(content) > 50:
                            meaningful_chunks += 1
                
                if meaningful_chunks >= 1:  # At least 1 meaningful chunk
                    logger.info(f"Found {meaningful_chunks} meaningful chunks")
                    return True
                else:
                    logger.warning(f"Only {meaningful_chunks} meaningful chunks found")
                    return False
            
            logger.warning("No meaningful metadata or chunks found")
            return False
            
        except Exception as e:
            logger.warning(f"Error checking metadata validity: {e}")
            return False

    def smart_ingest_document(self, file_path: Path) -> bool:
        """Smart ingestion that tries text-based extraction first, then falls back to image-based."""
        logger.info(f"🔄 Starting smart ingestion for {file_path.name}")
        
        # Step 1: Try text-based extraction first
        logger.info("📝 Step 1: Attempting text-based extraction...")
        try:
            success = self.ingest_document_with_rules(file_path)
            if success:
                # Check if the result is valid
                if self.ingested_docs:
                    latest_doc = self.ingested_docs[-1]
                    doc_id = latest_doc.get('document_id')
                    if doc_id and self.is_metadata_valid(doc_id):
                        logger.info("✅ Text-based extraction successful with valid metadata")
                        return True
                    else:
                        logger.warning("⚠️ Text-based extraction completed but metadata quality is poor")
                        # Remove the poor result from ingested_docs
                        if self.ingested_docs:
                            self.ingested_docs.pop()
                        # Clean up the document
                        try:
                            if doc_id:
                                self.db.delete_document(doc_id)
                        except Exception as e:
                            logger.warning(f"Could not clean up poor document: {e}")
                else:
                    logger.warning("⚠️ Text-based extraction completed but no document recorded")
            else:
                logger.warning("⚠️ Text-based extraction failed")
        except Exception as e:
            logger.warning(f"⚠️ Text-based extraction failed with error: {e}")
        
        # Step 2: Fall back to image-based extraction
        logger.info("🖼️ Step 2: Falling back to image-based extraction...")
        try:
            success = self.ingest_document_with_image_support(file_path)
            if success:
                logger.info("✅ Image-based extraction successful")
                return True
            else:
                logger.error("❌ Image-based extraction also failed")
                return False
        except Exception as e:
            logger.error(f"❌ Image-based extraction failed with error: {e}")
            return False

    def smart_ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents using smart fallback logic."""
        logger.info(f"🚀 Starting smart ingestion with automatic fallback from {pdf_dir}")
        
        # Find PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"No PDF files found in {pdf_dir}")
            return {'error': 'No PDF files found'}
        
        # Filter files under 300KB and randomly select
        small_files = []
        for pdf_file in pdf_files:
            file_size_kb = pdf_file.stat().st_size / 1024
            if file_size_kb < 300:
                small_files.append((pdf_file, file_size_kb))
        
        if not small_files:
            logger.error(f"No PDF files under 300KB found in {pdf_dir}")
            logger.info(f"Available files range from {min([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB to {max([f.stat().st_size / 1024 for f in pdf_files]):.1f}KB")
            return {'error': 'No PDF files under 300KB found'}
        
        # Randomly select files
        if max_docs:
            selected_files = random.sample(small_files, min(max_docs, len(small_files)))
        else:
            selected_files = random.sample(small_files, min(1, len(small_files)))  # Default to 1 file
        
        # Extract just the file paths
        pdf_files = [file_info[0] for file_info in selected_files]
        
        logger.info(f"Randomly selected {len(pdf_files)} files under 300KB:")
        for file_info in selected_files:
            logger.info(f"  - {file_info[0].name} ({file_info[1]:.1f}KB)")
        
        # Process documents with smart ingestion
        start_time = time.time()
        successful = 0
        text_successful = 0
        image_successful = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
            
            if self.smart_ingest_document(pdf_file):
                successful += 1
                logger.info(f"SUCCESS: Smart ingestion completed for {pdf_file.name}")
                
                # Count which method was used (this is tracked in the ingestion process)
                if self.ingested_docs:
                    latest_doc = self.ingested_docs[-1]
                    if 'method_used' in latest_doc:
                        if 'text' in latest_doc['method_used'].lower():
                            text_successful += 1
                        elif 'image' in latest_doc['method_used'].lower():
                            image_successful += 1
            
            # Add delay between ingestions to avoid overwhelming the system
            time.sleep(1)
        
        total_time = time.time() - start_time
        
        # Generate summary
        summary = {
            'total_documents': len(pdf_files),
            'successful_ingestions': successful,
            'failed_ingestions': len(self.failed_docs),
            'text_based_successful': text_successful,
            'image_based_successful': image_successful,
            'total_time': round(total_time, 2),
            'average_time_per_doc': round(total_time / len(pdf_files), 2),
            'success_rate': round(successful / len(pdf_files) * 100, 1),
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'selected_files': [f.name for f in pdf_files],
            'method_used': 'Smart ingestion with automatic fallback'
        }
        
        logger.info(f"Smart ingestion complete: {successful}/{len(pdf_files)} successful")
        logger.info(f"  - Text-based: {text_successful}")
        logger.info(f"  - Image-based: {image_successful}")
        logger.info(f"Total time: {total_time:.2f}s, Average: {summary['average_time_per_doc']:.2f}s per doc")
        
        return summary

def main():
    """Main ingestion function with smart automatic fallback."""
    print("🚀 ECSS Smart Ingestion System with Automatic Fallback")
    print("=" * 60)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    print(f"Debug: MORPHIK_URI = {morphik_uri[:50] if morphik_uri else 'None'}...")
    
    if not morphik_uri:
        print("MORPHIK_URI environment variable not set")
        print("Make sure you have a .env file with MORPHIK_URI set")
        return False
    
    # Initialize ingestion system
    try:
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
    except Exception as e:
        print(f"Failed to initialize ingestion system: {e}")
        return False
    
    # Set up paths
    pdf_dir = Path("../../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"PDF directory not found: {pdf_dir}")
        return False
    
    # Get user input for ingestion type
    print(f"\nFound {len(list(pdf_dir.glob('*.pdf')))} PDF files in {pdf_dir}")
    print("\nChoose ingestion method:")
    print("1. Smart ingestion with automatic fallback (RECOMMENDED)")
    print("2. Text-based only (NaturalLanguageRule)")
    print("3. Image-based only (MetadataExtractionRule with images)")
    
    try:
        method_choice = input("Enter choice (1, 2, or 3, default 1): ").strip()
        method_choice = int(method_choice) if method_choice else 1
    except ValueError:
        print("Invalid input, using smart ingestion with automatic fallback")
        method_choice = 1
    
    try:
        max_docs = input("Enter number of documents to ingest (or press Enter for 1): ").strip()
        max_docs = int(max_docs) if max_docs else 1  # Default to 1 for cost control
    except ValueError:
        print("Invalid input, using 1 document")
        max_docs = 1
    
    # Confirm before proceeding
    method_names = {
        1: "Smart ingestion with automatic fallback",
        2: "Text-based only (NaturalLanguageRule)",
        3: "Image-based only (MetadataExtractionRule with images)"
    }
    method_name = method_names.get(method_choice, "Smart ingestion with automatic fallback")
    print(f"Will ingest {max_docs} document(s) using {method_name}")
    
    confirm = input("Proceed with ingestion? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Ingestion cancelled")
        return False
    
    # Start ingestion based on choice
    if method_choice == 1:
        print("\n🚀 Starting smart ingestion with automatic fallback...")
        ingestion_summary = ingestion_system.smart_ingest_documents_batch(pdf_dir, max_docs=max_docs)
        results_file = f"smart_ingestion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    elif method_choice == 2:
        print("\n📝 Starting text-based ingestion only...")
        ingestion_summary = ingestion_system.ingest_documents_batch(pdf_dir, max_docs=max_docs)
        results_file = f"text_ingestion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    else:
        print("\n🖼️ Starting image-based ingestion only...")
        ingestion_summary = ingestion_system.ingest_documents_batch_with_images(pdf_dir, max_docs=max_docs)
        results_file = f"image_ingestion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Create knowledge graphs
    print("\n🔄 Creating knowledge graphs...")
    graphs_created = ingestion_system.create_graphs_with_rules()
    
    if graphs_created:
        print("✅ Knowledge graphs created successfully")
    else:
        print("❌ Knowledge graph creation failed")
        
    # Save results
    # Create a serializable version of the summary
    serializable_summary = {
        'total_documents': ingestion_summary.get('total_documents', 0),
        'successful_ingestions': ingestion_summary.get('successful_ingestions', 0),
        'failed_ingestions': ingestion_summary.get('failed_ingestions', 0),
        'total_time': ingestion_summary.get('total_time', 0),
        'average_time_per_doc': ingestion_summary.get('average_time_per_doc', 0),
        'success_rate': ingestion_summary.get('success_rate', 0),
        'ingested_docs': [
            {k: v for k, v in doc.items() if k != 'document_object'}
            for doc in ingestion_summary.get('ingested_docs', [])
        ],
        'failed_docs': ingestion_summary.get('failed_docs', []),
        'selected_files': ingestion_summary.get('selected_files', []),
        'method_used': method_name
    }
    
    # Add smart ingestion specific stats
    if method_choice == 1:
        serializable_summary['text_based_successful'] = ingestion_summary.get('text_based_successful', 0)
        serializable_summary['image_based_successful'] = ingestion_summary.get('image_based_successful', 0)

    with open(results_file, 'w') as f:
        json.dump(serializable_summary, f, indent=2, default=str)
    
    print(f"\n📊 INGESTION SUMMARY")
    print("="*40)
    print(f"Method used: {method_name}")
    print(f"Total documents: {serializable_summary['total_documents']}")
    print(f"Successful: {serializable_summary['successful_ingestions']}")
    print(f"Failed: {serializable_summary['failed_ingestions']}")
    print(f"Success rate: {serializable_summary['success_rate']}%")
    print(f"Total time: {serializable_summary['total_time']}s")
    print(f"Average time per doc: {serializable_summary['average_time_per_doc']}s")
    
    # Show smart ingestion breakdown if applicable
    if method_choice == 1:
        print(f"  - Text-based successful: {serializable_summary.get('text_based_successful', 0)}")
        print(f"  - Image-based successful: {serializable_summary.get('image_based_successful', 0)}")
    
    if 'selected_files' in serializable_summary and serializable_summary['selected_files']:
        print(f"\nSelected files:")
        for filename in serializable_summary['selected_files']:
            print(f"  - {filename}")
    
    print(f"\nDetailed results saved to: {results_file}")
        
    return True

if __name__ == "__main__":
    main()
 