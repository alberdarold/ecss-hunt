from morphik import Morphik
import os
from typing import List, Dict
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_metadata_from_filename(filename: str) -> Dict:
    """Extract metadata from ECSS filename."""
    # Updated pattern to handle more filename variations
    pattern = r'ECSS-([A-Z])-([A-Z]{2})-(\d+[A-Z]?)(?:[_-]Rev\.?(\d+))?'
    match = re.match(pattern, filename)
    
    if not match:
        return {"filename": filename}

    branch, discipline, doc_number, revision = match.groups()
    
    branch_map = {
        'E': 'Engineering',
        'M': 'Management',
        'Q': 'Quality Assurance',
        'S': 'Space Product Assurance',
        'U': 'Space Sustainability'
    }

    discipline_map = {
        'ST': 'Space Systems',
        'HB': 'Handbooks',
        'TM': 'Technical Memoranda'
    }

    return {
        'branch': branch,
        'branch_name': branch_map.get(branch, 'Unknown'),
        'discipline': discipline,
        'discipline_name': discipline_map.get(discipline, 'Unknown'),
        'document_number': doc_number,
        'revision': revision or '1',
        'filename': filename,
        'document_type': 'ECSS_Standard',
        'source': 'ECSS_Published_Standards'
    }

def ingest_ecss_documents(
    morphik_uri: str,
    pdf_directory: str,
    document_paths: List[str]
) -> None:
    """
    Ingest ECSS documents into Morphik with proper metadata.
    
    Args:
        morphik_uri: The Morphik instance URI
        pdf_directory: Base directory containing ECSS PDFs
        document_paths: List of PDF paths to ingest (relative to pdf_directory)
    """
    # Initialize Morphik client
    if morphik_uri:
        db = Morphik(uri=morphik_uri)
        print(f"Connected to Morphik instance: {morphik_uri[:20]}...")
    else:
        db = Morphik()
        print("Using default Morphik instance")
    
    successful_ingestions = 0
    failed_ingestions = 0
    
    for doc_path in document_paths:
        full_path = os.path.join(pdf_directory, doc_path)
        filename = os.path.basename(doc_path)
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"✗ File not found: {full_path}")
            failed_ingestions += 1
            continue
        
        # Extract metadata from filename
        metadata = extract_metadata_from_filename(filename)
        
        print(f"\nIngesting {filename}...")
        print(f"  Path: {full_path}")
        print(f"  Metadata: {metadata}")
        
        try:
            # Use the correct ingest_file method from Morphik SDK
            doc = db.ingest_file(
                file=full_path,
                filename=filename,
                metadata=metadata,
                use_colpali=True  # Better retrieval accuracy
            )
            
            print(f"✓ Successfully ingested {filename}")
            print(f"  Document ID: {getattr(doc, 'external_id', 'N/A')}")
            print(f"  Status: {getattr(doc, 'status', 'N/A')}")
            successful_ingestions += 1
            
        except Exception as e:
            print(f"✗ Error ingesting {filename}: {e}")
            failed_ingestions += 1
    
    # Summary
    print(f"\n=== Ingestion Summary ===")
    print(f"Successful: {successful_ingestions}")
    print(f"Failed: {failed_ingestions}")
    print(f"Total: {len(document_paths)}")
    
    if successful_ingestions > 0:
        print(f"\n✓ Successfully ingested {successful_ingestions} ECSS documents into Morphik!")
        print("You can now use these documents for searching and retrieval.")
    else:
        print(f"\n✗ No documents were successfully ingested. Please check the errors above.")

if __name__ == "__main__":
    # The 5 initial documents with exact filenames
    INITIAL_DOCUMENTS = [
        "ECSS-S-ST-00C Rev.1(15June2020).pdf",           # System Description
        "ECSS-Q-ST-70C-Rev.2(15October2019).pdf",        # Materials and processes
        "ECSS-E-ST-50C-Rev.1(1March2021).pdf",           # Communications
        "ECSS-M-ST-10C_Rev.1(6March2009).pdf",           # Project planning
        "ECSS-E-ST-20-08C_Rev.2(20April2023).pdf"        # Software development
    ]
    
    # Get Morphik URI from environment for security
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI environment variable is not set!")
        print("Will use default Morphik instance.")
        print("To use a specific instance, set MORPHIK_URI in your .env file:")
        print("MORPHIK_URI=your_morphik_uri_here")
    
    # Base directory containing ECSS PDFs (corrected path)
    pdf_directory = "ECSS Published Standards/1-Active Standards"
    
    print(f"Starting ECSS document ingestion...")
    print(f"PDF directory: {pdf_directory}")
    print(f"Documents to ingest: {len(INITIAL_DOCUMENTS)}")
    
    # Ingest documents
    ingest_ecss_documents(morphik_uri, pdf_directory, INITIAL_DOCUMENTS) 