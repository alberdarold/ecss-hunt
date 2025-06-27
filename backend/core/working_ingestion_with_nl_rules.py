

#!/usr/bin/env python3
"""
Working ECSS Document Ingestion using NaturalLanguageRule
Since MetadataExtractionRule is broken, we use NaturalLanguageRule for metadata extraction.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Working ECSS Document Ingestion using NaturalLanguageRule
Since MetadataExtractionRule is broken, we use NaturalLanguageRule for metadata extraction.
"""

import os
import sys
import json
import logging
import time
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    print("  python-dotenv not installed. Install with: pip install python-dotenv")

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

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

class WorkingECSSIngestion:
    """Working ECSS ingestion using NaturalLanguageRule for metadata extraction."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the working ingestion system."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Morphik: {e}")
            raise
    
    def get_ecss_nl_rules(self) -> List[NaturalLanguageRule]:
        """Get NaturalLanguageRule-based rules for ECSS document processing."""
        return [
            # Primary metadata extraction rule
            NaturalLanguageRule(
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
            ),
            
            # Section information extraction
            NaturalLanguageRule(
                prompt="""Extract section information from the ECSS document. Return as JSON with these fields:
- section_number: Section number (e.g., 3.1, 4.2.1)
- section_title: Title of the section
- section_type: Type of section (normative, informative, annex)
- content_summary: Brief summary of section content
- requirements_count: Number of requirements in this section
- figures_count: Number of figures in this section
- tables_count: Number of tables in this section

Extract information for each major section found in the document."""
            ),
            
            # Requirements extraction
            NaturalLanguageRule(
                prompt="""Extract requirements from the ECSS document. Return as JSON with these fields:
- requirement_id: Requirement identifier (e.g., REQ-001)
- requirement_text: The requirement statement
- requirement_type: Type of requirement (functional, performance, interface)
- priority: Priority level (mandatory, recommended, optional)
- verification_method: How this requirement is verified
- applicable_phases: Array of project phases this applies to

Extract all requirements found in the document."""
            ),
            
            # Content enhancement rule
            NaturalLanguageRule(
                prompt="""Enhance ECSS content for better searchability:
1. Add cross-references between related sections
2. Clarify ambiguous technical terms with context
3. Ensure all abbreviations are defined
4. Add implicit relationships between requirements
5. Maintain all original technical content and accuracy
6. Preserve all normative requirements exactly as stated"""
            )
        ]
    
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
        
        return True, "Valid"
    
    def ingest_document_with_nl_rules(self, file_path: Path) -> bool:
        """Ingest a single document using NaturalLanguageRule."""
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
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            doc = self.db.ingest_file(file_path, filename=external_id, rules=rules)

            logger.info(f"Waiting for NaturalLanguageRules to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Custom waiting logic to bypass SDK timeout
            max_wait_time = 3600  # 1 hour maximum wait
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
            
            # Record successful ingestion
            self.ingested_docs.append({
                'file': str(file_path),
                'external_id': doc.external_id,
                'ingestion_time': ingestion_time,
                'file_size_mb': file_path.stat().st_size / (1024 * 1024)
            })
            
            logger.info(f"✅ Successfully ingested {file_path.name} in {ingestion_time:.1f}s")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False
    
    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents in batch."""
        logger.info(f"Starting batch ingestion from {pdf_dir}")
        
        # Find PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return {'success': False, 'error': 'No PDF files found'}
        
        # Filter by size (under 300KB for testing)
        small_pdfs = [f for f in pdf_files if f.stat().st_size < 300 * 1024]
        if not small_pdfs:
            logger.warning("No PDF files under 300KB found")
            return {'success': False, 'error': 'No small PDF files found'}
        
        # Randomly select files if max_docs specified
        if max_docs and len(small_pdfs) > max_docs:
            selected_pdfs = random.sample(small_pdfs, max_docs)
        else:
            selected_pdfs = small_pdfs
        
        logger.info(f"Selected {len(selected_pdfs)} PDF files for ingestion")
        
        # Ingest each document
        successful_ingestions = 0
        for pdf_file in selected_pdfs:
            logger.info(f"Processing {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
            
            if self.ingest_document_with_nl_rules(pdf_file):
                successful_ingestions += 1
            else:
                logger.error(f"Failed to ingest {pdf_file.name}")
        
        # Create knowledge graphs
        logger.info("Creating knowledge graphs...")
        graph_success = self.create_graphs_with_nl_rules()
        
        # Summary
        total_files = len(selected_pdfs)
        success_rate = (successful_ingestions / total_files) * 100 if total_files > 0 else 0
        
        summary = {
            'success': True,
            'total_files': total_files,
            'successful_ingestions': successful_ingestions,
            'failed_ingestions': total_files - successful_ingestions,
            'success_rate': f"{success_rate:.1f}%",
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'graph_creation': 'success' if graph_success else 'failed'
        }
        
        logger.info(f"Ingestion complete: {successful_ingestions}/{total_files} successful ({success_rate:.1f}%)")
        return summary
    
    def create_graphs_with_nl_rules(self) -> bool:
        """Create knowledge graphs using NaturalLanguageRule."""
        try:
            logger.info("Creating ECSS knowledge graph...")
            
            # Create a comprehensive knowledge graph prompt
            graph_prompt = """Create a comprehensive knowledge graph for ECSS standards that includes:
1. Document relationships (references, dependencies)
2. Requirement hierarchies and dependencies
3. Technical concept relationships
4. Cross-standard connections
5. Verification and validation relationships
6. Process and workflow connections

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
            
            # Create the knowledge graph
            graph = self.db.create_knowledge_graph(
                prompt=graph_prompt,
                name="ECSS Standards Knowledge Graph"
            )
            
            logger.info(f"✅ Knowledge graph created successfully: {graph.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create knowledge graph: {e}")
            return False
    
    def get_extracted_metadata_from_chunks(self, search_terms: List[str] = None) -> Dict:
        """Retrieve extracted metadata from chunks since metadata field is not populated."""
        if not search_terms:
            search_terms = ["ECSS", "standard", "requirement", "engineering"]
        
        extracted_data = {}
        
        for term in search_terms:
            try:
                chunks = self.db.retrieve_chunks(term)
                if chunks:
                    extracted_data[term] = []
                    for chunk in chunks[:5]:  # Get first 5 chunks
                        if hasattr(chunk, 'content') and chunk.content:
                            extracted_data[term].append(chunk.content)
            except Exception as e:
                logger.warning(f"Could not retrieve chunks for '{term}': {e}")
        
        return extracted_data

def main():
    """Main function to run the working ingestion."""
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize ingestion system
    ingestion = WorkingECSSIngestion(morphik_uri)
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    # Run batch ingestion (limit to 5 documents for testing)
    print("🚀 Starting working ECSS ingestion with NaturalLanguageRules...")
    result = ingestion.ingest_documents_batch(pdf_dir, max_docs=5)
    
    # Print results
    print("\n📊 Ingestion Results:")
    print(f"Total files: {result['total_files']}")
    print(f"Successful: {result['successful_ingestions']}")
    print(f"Failed: {result['failed_ingestions']}")
    print(f"Success rate: {result['success_rate']}")
    print(f"Graph creation: {result['graph_creation']}")
    
    # Show extracted metadata from chunks
    print("\n🔍 Extracted Metadata from Chunks:")
    metadata = ingestion.get_extracted_metadata_from_chunks()
    for term, chunks in metadata.items():
        print(f"\n{term.upper()}:")
        for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
            if isinstance(chunk, str) and len(chunk) > 50:
                print(f"  Chunk {i+1}: {chunk[:200]}...")
            else:
                print(f"  Chunk {i+1}: {chunk}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"working_ingestion_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main() 

import os
import sys
import json
import logging
import time
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Load environment variables from the root directory
try:
        dotenv_path = Path(__file__).parent.parent / '.env'
    except ImportError:
    print("  python-dotenv not installed. Install with: pip install python-dotenv")

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import NaturalLanguageRule

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

class WorkingECSSIngestion:
    """Working ECSS ingestion using NaturalLanguageRule for metadata extraction."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the working ingestion system."""
        self.db = Morphik(morphik_uri)
        self.ingested_docs = []
        self.failed_docs = []
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Morphik: {e}")
            raise
    
    def get_ecss_nl_rules(self) -> List[NaturalLanguageRule]:
        """Get NaturalLanguageRule-based rules for ECSS document processing."""
        return [
            # Primary metadata extraction rule
            NaturalLanguageRule(
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
            ),
            
            # Section information extraction
            NaturalLanguageRule(
                prompt="""Extract section information from the ECSS document. Return as JSON with these fields:
- section_number: Section number (e.g., 3.1, 4.2.1)
- section_title: Title of the section
- section_type: Type of section (normative, informative, annex)
- content_summary: Brief summary of section content
- requirements_count: Number of requirements in this section
- figures_count: Number of figures in this section
- tables_count: Number of tables in this section

Extract information for each major section found in the document."""
            ),
            
            # Requirements extraction
            NaturalLanguageRule(
                prompt="""Extract requirements from the ECSS document. Return as JSON with these fields:
- requirement_id: Requirement identifier (e.g., REQ-001)
- requirement_text: The requirement statement
- requirement_type: Type of requirement (functional, performance, interface)
- priority: Priority level (mandatory, recommended, optional)
- verification_method: How this requirement is verified
- applicable_phases: Array of project phases this applies to

Extract all requirements found in the document."""
            ),
            
            # Content enhancement rule
            NaturalLanguageRule(
                prompt="""Enhance ECSS content for better searchability:
1. Add cross-references between related sections
2. Clarify ambiguous technical terms with context
3. Ensure all abbreviations are defined
4. Add implicit relationships between requirements
5. Maintain all original technical content and accuracy
6. Preserve all normative requirements exactly as stated"""
            )
        ]
    
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
        
        return True, "Valid"
    
    def ingest_document_with_nl_rules(self, file_path: Path) -> bool:
        """Ingest a single document using NaturalLanguageRule."""
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
            
            # Use the filename as the external_id for idempotency
            external_id = file_path.name
            start_time = time.time()
            doc = self.db.ingest_file(file_path, filename=external_id, rules=rules)

            logger.info(f"Waiting for NaturalLanguageRules to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Custom waiting logic to bypass SDK timeout
            max_wait_time = 3600  # 1 hour maximum wait
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
            
            # Record successful ingestion
            self.ingested_docs.append({
                'file': str(file_path),
                'external_id': doc.external_id,
                'ingestion_time': ingestion_time,
                'file_size_mb': file_path.stat().st_size / (1024 * 1024)
            })
            
            logger.info(f"✅ Successfully ingested {file_path.name} in {ingestion_time:.1f}s")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path.name}: {e}")
            self.failed_docs.append({'file': str(file_path), 'error': str(e)})
            return False
    
    def ingest_documents_batch(self, pdf_dir: Path, max_docs: int = None) -> Dict:
        """Ingest multiple documents in batch."""
        logger.info(f"Starting batch ingestion from {pdf_dir}")
        
        # Find PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return {'success': False, 'error': 'No PDF files found'}
        
        # Filter by size (under 300KB for testing)
        small_pdfs = [f for f in pdf_files if f.stat().st_size < 300 * 1024]
        if not small_pdfs:
            logger.warning("No PDF files under 300KB found")
            return {'success': False, 'error': 'No small PDF files found'}
        
        # Randomly select files if max_docs specified
        if max_docs and len(small_pdfs) > max_docs:
            selected_pdfs = random.sample(small_pdfs, max_docs)
        else:
            selected_pdfs = small_pdfs
        
        logger.info(f"Selected {len(selected_pdfs)} PDF files for ingestion")
        
        # Ingest each document
        successful_ingestions = 0
        for pdf_file in selected_pdfs:
            logger.info(f"Processing {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
            
            if self.ingest_document_with_nl_rules(pdf_file):
                successful_ingestions += 1
            else:
                logger.error(f"Failed to ingest {pdf_file.name}")
        
        # Create knowledge graphs
        logger.info("Creating knowledge graphs...")
        graph_success = self.create_graphs_with_nl_rules()
        
        # Summary
        total_files = len(selected_pdfs)
        success_rate = (successful_ingestions / total_files) * 100 if total_files > 0 else 0
        
        summary = {
            'success': True,
            'total_files': total_files,
            'successful_ingestions': successful_ingestions,
            'failed_ingestions': total_files - successful_ingestions,
            'success_rate': f"{success_rate:.1f}%",
            'ingested_docs': self.ingested_docs,
            'failed_docs': self.failed_docs,
            'graph_creation': 'success' if graph_success else 'failed'
        }
        
        logger.info(f"Ingestion complete: {successful_ingestions}/{total_files} successful ({success_rate:.1f}%)")
        return summary
    
    def create_graphs_with_nl_rules(self) -> bool:
        """Create knowledge graphs using NaturalLanguageRule."""
        try:
            logger.info("Creating ECSS knowledge graph...")
            
            # Create a comprehensive knowledge graph prompt
            graph_prompt = """Create a comprehensive knowledge graph for ECSS standards that includes:
1. Document relationships (references, dependencies)
2. Requirement hierarchies and dependencies
3. Technical concept relationships
4. Cross-standard connections
5. Verification and validation relationships
6. Process and workflow connections

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
            
            # Create the knowledge graph
            graph = self.db.create_knowledge_graph(
                prompt=graph_prompt,
                name="ECSS Standards Knowledge Graph"
            )
            
            logger.info(f"✅ Knowledge graph created successfully: {graph.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create knowledge graph: {e}")
            return False
    
    def get_extracted_metadata_from_chunks(self, search_terms: List[str] = None) -> Dict:
        """Retrieve extracted metadata from chunks since metadata field is not populated."""
        if not search_terms:
            search_terms = ["ECSS", "standard", "requirement", "engineering"]
        
        extracted_data = {}
        
        for term in search_terms:
            try:
                chunks = self.db.retrieve_chunks(term)
                if chunks:
                    extracted_data[term] = []
                    for chunk in chunks[:5]:  # Get first 5 chunks
                        if hasattr(chunk, 'content') and chunk.content:
                            extracted_data[term].append(chunk.content)
            except Exception as e:
                logger.warning(f"Could not retrieve chunks for '{term}': {e}")
        
        return extracted_data

def main():
    """Main function to run the working ingestion."""
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize ingestion system
    ingestion = WorkingECSSIngestion(morphik_uri)
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    # Run batch ingestion (limit to 5 documents for testing)
    print("🚀 Starting working ECSS ingestion with NaturalLanguageRules...")
    result = ingestion.ingest_documents_batch(pdf_dir, max_docs=5)
    
    # Print results
    print("\n📊 Ingestion Results:")
    print(f"Total files: {result['total_files']}")
    print(f"Successful: {result['successful_ingestions']}")
    print(f"Failed: {result['failed_ingestions']}")
    print(f"Success rate: {result['success_rate']}")
    print(f"Graph creation: {result['graph_creation']}")
    
    # Show extracted metadata from chunks
    print("\n🔍 Extracted Metadata from Chunks:")
    metadata = ingestion.get_extracted_metadata_from_chunks()
    for term, chunks in metadata.items():
        print(f"\n{term.upper()}:")
        for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
            if isinstance(chunk, str) and len(chunk) > 50:
                print(f"  Chunk {i+1}: {chunk[:200]}...")
            else:
                print(f"  Chunk {i+1}: {chunk}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"working_ingestion_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main() 