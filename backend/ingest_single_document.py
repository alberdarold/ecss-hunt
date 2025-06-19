from morphik import Morphik
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_metadata_from_filename(filename: str):
    """Extract metadata from ECSS filename."""
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

def ingest_single_document():
    """Ingest a single ECSS document for testing."""
    
    # Get Morphik URI from environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("⚠ MORPHIK_URI environment variable is not set!")
        return
    
    # Initialize Morphik client
    db = Morphik(uri=morphik_uri)
    print(f"Connected to Morphik instance: {morphik_uri[:20]}...")
    
    # Choose one document to ingest
    filename = "ECSS-S-ST-00C Rev.1(15June2020).pdf"  # System Description
    pdf_directory = "ECSS Published Standards/1-Active Standards"
    full_path = os.path.join(pdf_directory, filename)
    
    # Check if file exists
    if not os.path.exists(full_path):
        print(f"✗ File not found: {full_path}")
        return
    
    # Extract metadata from filename
    metadata = extract_metadata_from_filename(filename)
    
    print(f"\n=== Ingesting single document ===")
    print(f"Document: {filename}")
    print(f"Path: {full_path}")
    print(f"Metadata: {metadata}")
    
    try:
        # Ingest the document
        doc = db.ingest_file(
            file=full_path,
            filename=filename,
            metadata=metadata
        )
        
        print(f"\n✓ Successfully ingested {filename}")
        print(f"Document ID: {getattr(doc, 'external_id', 'N/A')}")
        print(f"Status: {getattr(doc, 'status', 'N/A')}")
        
        # Wait a moment and test search
        print(f"\n=== Testing search after ingestion ===")
        import time
        time.sleep(10)  # Wait 10 seconds for processing
        
        try:
            results = db.query("ECSS standards")
            if results and hasattr(results, 'results') and len(results.results) > 0:
                print(f"✓ Search working! Found {len(results.results)} results")
                for i, result in enumerate(results.results[:2]):
                    print(f"  {i+1}. {result.content[:150]}...")
            else:
                print("✗ No search results yet (document may still be processing)")
        except Exception as e:
            print(f"✗ Search error: {e}")
        
    except Exception as e:
        print(f"✗ Error ingesting {filename}: {e}")

if __name__ == "__main__":
    ingest_single_document() 