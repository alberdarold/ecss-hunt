

#!/usr/bin/env python3
"""
Working ECSS Document Ingestion using MetadataExtractionRule with Image Support
This implementation uses MetadataExtractionRule with stage="post_chunking" and use_images=True
to enable image-based parsing for PDFs when text extraction fails.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Working ECSS Document Ingestion using MetadataExtractionRule with Image Support
This implementation uses MetadataExtractionRule with stage="post_chunking" and use_images=True
to enable image-based parsing for PDFs when text extraction fails.
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
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ingestion_with_images.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define comprehensive ECSS metadata schemas
class ECSSStandardMetadata(BaseModel):
    """Schema for extracting ECSS standard metadata."""
    standard_id: str = Field(description="ECSS standard identifier (e.g., ECSS-E-ST-10C)")
    branch: str = Field(description="ECSS branch (E, M, P, Q)")
    discipline: str = Field(description="ECSS discipline (Engineering, Management, Product Assurance, etc.)")
    title: str = Field(description="Full title of the standard")
    revision: str = Field(description="Revision number (e.g., Rev.1, Rev.2)")
    date: str = Field(description="Publication date")
    status: str = Field(description="Status (Active, Superseded, etc.)")
    scope: str = Field(description="Brief description of the standard's scope")
    keywords: List[str] = Field(description="Array of key technical terms and concepts")
    applicable_domains: List[str] = Field(description="Array of space engineering domains this applies to")

class ECSSSectionInfo(BaseModel):
    """Schema for extracting section information."""
    section_number: str = Field(description="Section number (e.g., 3.1, 4.2.1)")
    section_title: str = Field(description="Title of the section")
    section_type: str = Field(description="Type of section (normative, informative, annex)")
    content_summary: str = Field(description="Brief summary of section content")
    requirements_count: int = Field(description="Number of requirements in this section")
    figures_count: int = Field(description="Number of figures in this section")
    tables_count: int = Field(description="Number of tables in this section")

class ECSSRequirement(BaseModel):
    """Schema for extracting requirements."""
    requirement_id: str = Field(description="Requirement identifier (e.g., REQ-001)")
    requirement_text: str = Field(description="The requirement statement")
    requirement_type: str = Field(description="Type of requirement (functional, performance, interface)")
    priority: str = Field(description="Priority level (mandatory, recommended, optional)")
    verification_method: str = Field(description="How this requirement is verified")
    applicable_phases: List[str] = Field(description="Array of project phases this applies to")

class ECSSDefinition(BaseModel):
    """Schema for extracting definitions."""
    term: str = Field(description="The term being defined")
    definition: str = Field(description="The definition of the term")
    context: str = Field(description="Context where this definition is used")
    related_terms: List[str] = Field(description="Array of related terms or synonyms")
    standard_reference: str = Field(description="Which standard this definition comes from")

class ECSSTableInfo(BaseModel):
    """Schema for extracting table information."""
    table_number: str = Field(description="Table number (e.g., Table 1, Table A.1)")
    table_title: str = Field(description="Title or caption of the table")
    table_type: str = Field(description="Type of table (requirements, parameters, classifications)")
    row_count: int = Field(description="Number of rows in the table")
    column_count: int = Field(description="Number of columns in the table")
    content_summary: str = Field(description="Summary of what the table contains")
    key_parameters: List[str] = Field(description="Array of key parameters or values in the table")

class ECSSFigureInfo(BaseModel):
    """Schema for extracting figure information."""
    figure_number: str = Field(description="Figure number (e.g., Figure 1, Figure A.1)")
    figure_title: str = Field(description="Title or caption of the figure")
    diagram_type: str = Field(description="Type of diagram (flowchart, block diagram, schematic)")
    content_description: str = Field(description="Description of what the diagram shows")
    components: List[str] = Field(description="Array of key components or elements in the diagram")
    relationships: List[str] = Field(description="Array of relationships or connections shown")

class WorkingECSSIngestionWithImages:
    """Working ECSS ingestion using MetadataExtractionRule with image support."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the working ingestion system with image support."""
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
    
    def get_ecss_metadata_rules(self) -> List[MetadataExtractionRule]:
        """Get MetadataExtractionRule-based rules with image support for ECSS document processing."""
        return [
            # Primary metadata extraction rule with image support
            MetadataExtractionRule(
                schema=ECSSStandardMetadata,
                stage="post_chunking",
                use_images=True
            ),
            
            # Section information extraction with image support
            MetadataExtractionRule(
                schema=ECSSSectionInfo,
                stage="post_chunking", 
                use_images=True
            ),
            
            # Requirements extraction with image support
            MetadataExtractionRule(
                schema=ECSSRequirement,
                stage="post_chunking",
                use_images=True
            ),
            
            # Definitions extraction with image support
            MetadataExtractionRule(
                schema=ECSSDefinition,
                stage="post_chunking",
                use_images=True
            ),
            
            # Table information extraction with image support
            MetadataExtractionRule(
                schema=ECSSTableInfo,
                stage="post_chunking",
                use_images=True
            ),
            
            # Figure information extraction with image support
            MetadataExtractionRule(
                schema=ECSSFigureInfo,
                stage="post_chunking",
                use_images=True
            )
        ]
    
    def get_ecss_nl_rules(self) -> List[NaturalLanguageRule]:
        """Get NaturalLanguageRule-based rules as fallback."""
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
            metadata_rules = self.get_ecss_metadata_rules()
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
                use_colpali=True  # Enable image-based processing
            )
            
            logger.info(f"Document object created:")
            logger.info(f"  - Document ID: {doc.external_id}")
            logger.info(f"  - Initial status: {doc.status}")
            logger.info(f"  - Document type: {type(doc)}")

            logger.info(f"Waiting for MetadataExtractionRules with image support to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Use the built-in wait_for_completion method
            doc.wait_for_completion()
            
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
                    'document_object': refreshed_doc
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
    
    def create_graphs_with_image_support(self) -> bool:
        """Create knowledge graphs using the ingested documents."""
        try:
            logger.info("Creating ECSS knowledge graphs with image support...")
            
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
7. Visual content relationships (tables, figures, diagrams)

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
                
                graph = self.db.create_knowledge_graph(
                    prompt=graph_prompt,
                    documents=successful_docs
                )
                
                logger.info(f"✅ Knowledge graph created successfully: {graph.id}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to create knowledge graph: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to create graphs: {e}")
            return False

def main():
    """Main function to run the ingestion with image support."""
    print("🚀 ECSS Document Ingestion with Image Support")
    print("=" * 50)
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        print("Please set MORPHIK_URI in your .env file")
        return
    
    # Initialize ingestion system
    try:
        ingestion = WorkingECSSIngestionWithImages(morphik_uri)
        print("✅ Initialized ingestion system with image support")
    except Exception as e:
        print(f"❌ Failed to initialize ingestion system: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    print(f"📁 PDF directory: {pdf_dir}")
    
    # Run ingestion
    try:
        print("\n🔄 Starting batch ingestion with image support...")
        results = ingestion.ingest_documents_batch(pdf_dir, max_docs=1)
        
        if 'error' in results:
            print(f"❌ Ingestion failed: {results['error']}")
            return
        
        print(f"\n✅ Ingestion completed!")
        print(f"📊 Results:")
        print(f"   - Total documents: {results['total_documents']}")
        print(f"   - Successful: {results['successful_ingestions']}")
        print(f"   - Failed: {results['failed_ingestions']}")
        print(f"   - Success rate: {results['success_rate']}%")
        print(f"   - Total time: {results['total_time']}s")
        print(f"   - Average time per doc: {results['average_time_per_doc']}s")
        
        # Create knowledge graphs
        print("\n🔄 Creating knowledge graphs...")
        if ingestion.create_graphs_with_image_support():
            print("✅ Knowledge graphs created successfully")
        else:
            print("❌ Failed to create knowledge graphs")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"ingestion_results_with_images_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

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
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ingestion_with_images.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define comprehensive ECSS metadata schemas
class ECSSStandardMetadata(BaseModel):
    """Schema for extracting ECSS standard metadata."""
    standard_id: str = Field(description="ECSS standard identifier (e.g., ECSS-E-ST-10C)")
    branch: str = Field(description="ECSS branch (E, M, P, Q)")
    discipline: str = Field(description="ECSS discipline (Engineering, Management, Product Assurance, etc.)")
    title: str = Field(description="Full title of the standard")
    revision: str = Field(description="Revision number (e.g., Rev.1, Rev.2)")
    date: str = Field(description="Publication date")
    status: str = Field(description="Status (Active, Superseded, etc.)")
    scope: str = Field(description="Brief description of the standard's scope")
    keywords: List[str] = Field(description="Array of key technical terms and concepts")
    applicable_domains: List[str] = Field(description="Array of space engineering domains this applies to")

class ECSSSectionInfo(BaseModel):
    """Schema for extracting section information."""
    section_number: str = Field(description="Section number (e.g., 3.1, 4.2.1)")
    section_title: str = Field(description="Title of the section")
    section_type: str = Field(description="Type of section (normative, informative, annex)")
    content_summary: str = Field(description="Brief summary of section content")
    requirements_count: int = Field(description="Number of requirements in this section")
    figures_count: int = Field(description="Number of figures in this section")
    tables_count: int = Field(description="Number of tables in this section")

class ECSSRequirement(BaseModel):
    """Schema for extracting requirements."""
    requirement_id: str = Field(description="Requirement identifier (e.g., REQ-001)")
    requirement_text: str = Field(description="The requirement statement")
    requirement_type: str = Field(description="Type of requirement (functional, performance, interface)")
    priority: str = Field(description="Priority level (mandatory, recommended, optional)")
    verification_method: str = Field(description="How this requirement is verified")
    applicable_phases: List[str] = Field(description="Array of project phases this applies to")

class ECSSDefinition(BaseModel):
    """Schema for extracting definitions."""
    term: str = Field(description="The term being defined")
    definition: str = Field(description="The definition of the term")
    context: str = Field(description="Context where this definition is used")
    related_terms: List[str] = Field(description="Array of related terms or synonyms")
    standard_reference: str = Field(description="Which standard this definition comes from")

class ECSSTableInfo(BaseModel):
    """Schema for extracting table information."""
    table_number: str = Field(description="Table number (e.g., Table 1, Table A.1)")
    table_title: str = Field(description="Title or caption of the table")
    table_type: str = Field(description="Type of table (requirements, parameters, classifications)")
    row_count: int = Field(description="Number of rows in the table")
    column_count: int = Field(description="Number of columns in the table")
    content_summary: str = Field(description="Summary of what the table contains")
    key_parameters: List[str] = Field(description="Array of key parameters or values in the table")

class ECSSFigureInfo(BaseModel):
    """Schema for extracting figure information."""
    figure_number: str = Field(description="Figure number (e.g., Figure 1, Figure A.1)")
    figure_title: str = Field(description="Title or caption of the figure")
    diagram_type: str = Field(description="Type of diagram (flowchart, block diagram, schematic)")
    content_description: str = Field(description="Description of what the diagram shows")
    components: List[str] = Field(description="Array of key components or elements in the diagram")
    relationships: List[str] = Field(description="Array of relationships or connections shown")

class WorkingECSSIngestionWithImages:
    """Working ECSS ingestion using MetadataExtractionRule with image support."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the working ingestion system with image support."""
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
    
    def get_ecss_metadata_rules(self) -> List[MetadataExtractionRule]:
        """Get MetadataExtractionRule-based rules with image support for ECSS document processing."""
        return [
            # Primary metadata extraction rule with image support
            MetadataExtractionRule(
                schema=ECSSStandardMetadata,
                stage="post_chunking",
                use_images=True
            ),
            
            # Section information extraction with image support
            MetadataExtractionRule(
                schema=ECSSSectionInfo,
                stage="post_chunking", 
                use_images=True
            ),
            
            # Requirements extraction with image support
            MetadataExtractionRule(
                schema=ECSSRequirement,
                stage="post_chunking",
                use_images=True
            ),
            
            # Definitions extraction with image support
            MetadataExtractionRule(
                schema=ECSSDefinition,
                stage="post_chunking",
                use_images=True
            ),
            
            # Table information extraction with image support
            MetadataExtractionRule(
                schema=ECSSTableInfo,
                stage="post_chunking",
                use_images=True
            ),
            
            # Figure information extraction with image support
            MetadataExtractionRule(
                schema=ECSSFigureInfo,
                stage="post_chunking",
                use_images=True
            )
        ]
    
    def get_ecss_nl_rules(self) -> List[NaturalLanguageRule]:
        """Get NaturalLanguageRule-based rules as fallback."""
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
            metadata_rules = self.get_ecss_metadata_rules()
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
                use_colpali=True  # Enable image-based processing
            )
            
            logger.info(f"Document object created:")
            logger.info(f"  - Document ID: {doc.external_id}")
            logger.info(f"  - Initial status: {doc.status}")
            logger.info(f"  - Document type: {type(doc)}")

            logger.info(f"Waiting for MetadataExtractionRules with image support to complete for {file_path.name}...")
            logger.info("This may take several minutes - please be patient...")
            
            # Use the built-in wait_for_completion method
            doc.wait_for_completion()
            
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
                    'document_object': refreshed_doc
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
    
    def create_graphs_with_image_support(self) -> bool:
        """Create knowledge graphs using the ingested documents."""
        try:
            logger.info("Creating ECSS knowledge graphs with image support...")
            
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
7. Visual content relationships (tables, figures, diagrams)

Focus on creating meaningful relationships that help users navigate and understand ECSS standards."""
                
                graph = self.db.create_knowledge_graph(
                    prompt=graph_prompt,
                    documents=successful_docs
                )
                
                logger.info(f"✅ Knowledge graph created successfully: {graph.id}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to create knowledge graph: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to create graphs: {e}")
            return False

def main():
    """Main function to run the ingestion with image support."""
    print("🚀 ECSS Document Ingestion with Image Support")
    print("=" * 50)
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        print("Please set MORPHIK_URI in your .env file")
        return
    
    # Initialize ingestion system
    try:
        ingestion = WorkingECSSIngestionWithImages(morphik_uri)
        print("✅ Initialized ingestion system with image support")
    except Exception as e:
        print(f"❌ Failed to initialize ingestion system: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    print(f"📁 PDF directory: {pdf_dir}")
    
    # Run ingestion
    try:
        print("\n🔄 Starting batch ingestion with image support...")
        results = ingestion.ingest_documents_batch(pdf_dir, max_docs=1)
        
        if 'error' in results:
            print(f"❌ Ingestion failed: {results['error']}")
            return
        
        print(f"\n✅ Ingestion completed!")
        print(f"📊 Results:")
        print(f"   - Total documents: {results['total_documents']}")
        print(f"   - Successful: {results['successful_ingestions']}")
        print(f"   - Failed: {results['failed_ingestions']}")
        print(f"   - Success rate: {results['success_rate']}%")
        print(f"   - Total time: {results['total_time']}s")
        print(f"   - Average time per doc: {results['average_time_per_doc']}s")
        
        # Create knowledge graphs
        print("\n🔄 Creating knowledge graphs...")
        if ingestion.create_graphs_with_image_support():
            print("✅ Knowledge graphs created successfully")
        else:
            print("❌ Failed to create knowledge graphs")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"ingestion_results_with_images_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 