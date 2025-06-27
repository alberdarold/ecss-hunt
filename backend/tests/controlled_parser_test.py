

#!/usr/bin/env python3
"""
Controlled Test Script to Isolate Morphik's PDF Parsing Root Cause.

This script performs the following steps:
1.  Reads a simple, known-good text file (`simple_test.txt`).
2.  Creates a basic, clean PDF from that text using `fpdf2`.
3.  Ingests the `.txt` file into Morphik with `use_colpali=False`.
4.  Ingests the simple `.pdf` file into Morphik with `use_colpali=False`.
5.  Reports on the success or failure of each ingestion.

This will definitively determine if Morphik's non-ColPali PDF parser is functional.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Controlled Test Script to Isolate Morphik's PDF Parsing Root Cause.

This script performs the following steps:
1.  Reads a simple, known-good text file (`simple_test.txt`).
2.  Creates a basic, clean PDF from that text using `fpdf2`.
3.  Ingests the `.txt` file into Morphik with `use_colpali=False`.
4.  Ingests the simple `.pdf` file into Morphik with `use_colpali=False`.
5.  Reports on the success or failure of each ingestion.

This will definitively determine if Morphik's non-ColPali PDF parser is functional.
"""

import os
import sys
from fpdf import FPDF

# Load environment variables
dotenv_path = Path(__file__).parent.parent / '.env'

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def create_simple_pdf(text_content: str, output_path: Path):
    """Creates a very basic PDF from a string of text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text_content)
    pdf.output(str(output_path))
    print(f"📄 Successfully created simple PDF: {output_path.name}")

def run_controlled_test():
    """Executes the controlled test to diagnose Morphik's PDF parser."""
    print("🔬 Running Controlled Ingestion Test")
    print("=" * 40)

    # --- Setup ---
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not set. Aborting.")
        return

    try:
        db = Morphik(morphik_uri)
        db.ping()
        print("✅ Connected to Morphik successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to Morphik: {e}")
        return
        
    # Delete previous test documents to ensure a clean slate
    print("\n🧹 Clearing old test documents...")
    try:
        for doc_name in ["simple_test.txt", "simple_test.pdf"]:
            doc = db.get_document_by_filename(doc_name)
            if doc:
                db.delete_document(doc.external_id)
                print(f"  - Deleted old version of: {doc_name}")
    except Exception as e:
        print(f"  - Info: Could not delete old documents (they may not exist). Error: {e}")


    # --- Step 1: Prepare Test Files ---
    print("\n1️⃣  Preparing Test Files")
    txt_file = backend_dir / "simple_test.txt"
    pdf_file = backend_dir / "simple_test.pdf"

    if not txt_file.exists():
        print(f"❌ Critical Error: simple_test.txt not found at {txt_file}")
        return

    text_content = txt_file.read_text()
    create_simple_pdf(text_content, pdf_file)

    # --- Step 2: Ingest the .txt file ---
    print("\n2️⃣  Testing .txt File Ingestion")
    try:
        print(f"  - Ingesting {txt_file.name}...")
        doc_txt = db.ingest_file(str(txt_file), use_colpali=False)
        print("  - Waiting for completion...")
        doc_txt.wait_for_completion()
        status = doc_txt.status.get('status') if isinstance(doc_txt.status, dict) else doc_txt.status
        if status == 'completed':
            print(f"  ✅ SUCCESS: .txt file ingested successfully.")
        else:
            error_msg = doc_txt.status.get('error', 'Unknown error')
            print(f"  ❌ FAILED: .txt file ingestion failed. Status: {status}, Error: {error_msg}")
    except Exception as e:
        print(f"  ❌ FAILED: An exception occurred during .txt ingestion: {e}")


    # --- Step 3: Ingest the simple .pdf file ---
    print("\n3️⃣  Testing Simple .pdf File Ingestion")
    try:
        print(f"  - Ingesting {pdf_file.name}...")
        doc_pdf = db.ingest_file(str(pdf_file), use_colpali=False)
        print("  - Waiting for completion...")
        doc_pdf.wait_for_completion()
        status = doc_pdf.status.get('status') if isinstance(doc_pdf.status, dict) else doc_pdf.status
        if status == 'completed':
            print(f"  ✅ SUCCESS: Simple .pdf file ingested successfully.")
        else:
            error_msg = doc_pdf.status.get('error', 'Unknown error')
            print(f"  ❌ FAILED: Simple .pdf file ingestion failed. Status: {status}, Error: {error_msg}")
    except Exception as e:
        print(f"  ❌ FAILED: An exception occurred during .pdf ingestion: {e}")
        
    print("\n" + "="*40)
    print("🔬 Test Complete.")

if __name__ == "__main__":
    run_controlled_test() 

import os
import sys
from fpdf import FPDF

# Load environment variables
dotenv_path = Path(__file__).parent.parent / '.env'

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def create_simple_pdf(text_content: str, output_path: Path):
    """Creates a very basic PDF from a string of text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text_content)
    pdf.output(str(output_path))
    print(f"📄 Successfully created simple PDF: {output_path.name}")

def run_controlled_test():
    """Executes the controlled test to diagnose Morphik's PDF parser."""
    print("🔬 Running Controlled Ingestion Test")
    print("=" * 40)

    # --- Setup ---
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not set. Aborting.")
        return

    try:
        db = Morphik(morphik_uri)
        db.ping()
        print("✅ Connected to Morphik successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to Morphik: {e}")
        return
        
    # Delete previous test documents to ensure a clean slate
    print("\n🧹 Clearing old test documents...")
    try:
        for doc_name in ["simple_test.txt", "simple_test.pdf"]:
            doc = db.get_document_by_filename(doc_name)
            if doc:
                db.delete_document(doc.external_id)
                print(f"  - Deleted old version of: {doc_name}")
    except Exception as e:
        print(f"  - Info: Could not delete old documents (they may not exist). Error: {e}")


    # --- Step 1: Prepare Test Files ---
    print("\n1️⃣  Preparing Test Files")
    txt_file = backend_dir / "simple_test.txt"
    pdf_file = backend_dir / "simple_test.pdf"

    if not txt_file.exists():
        print(f"❌ Critical Error: simple_test.txt not found at {txt_file}")
        return

    text_content = txt_file.read_text()
    create_simple_pdf(text_content, pdf_file)

    # --- Step 2: Ingest the .txt file ---
    print("\n2️⃣  Testing .txt File Ingestion")
    try:
        print(f"  - Ingesting {txt_file.name}...")
        doc_txt = db.ingest_file(str(txt_file), use_colpali=False)
        print("  - Waiting for completion...")
        doc_txt.wait_for_completion()
        status = doc_txt.status.get('status') if isinstance(doc_txt.status, dict) else doc_txt.status
        if status == 'completed':
            print(f"  ✅ SUCCESS: .txt file ingested successfully.")
        else:
            error_msg = doc_txt.status.get('error', 'Unknown error')
            print(f"  ❌ FAILED: .txt file ingestion failed. Status: {status}, Error: {error_msg}")
    except Exception as e:
        print(f"  ❌ FAILED: An exception occurred during .txt ingestion: {e}")


    # --- Step 3: Ingest the simple .pdf file ---
    print("\n3️⃣  Testing Simple .pdf File Ingestion")
    try:
        print(f"  - Ingesting {pdf_file.name}...")
        doc_pdf = db.ingest_file(str(pdf_file), use_colpali=False)
        print("  - Waiting for completion...")
        doc_pdf.wait_for_completion()
        status = doc_pdf.status.get('status') if isinstance(doc_pdf.status, dict) else doc_pdf.status
        if status == 'completed':
            print(f"  ✅ SUCCESS: Simple .pdf file ingested successfully.")
        else:
            error_msg = doc_pdf.status.get('error', 'Unknown error')
            print(f"  ❌ FAILED: Simple .pdf file ingestion failed. Status: {status}, Error: {error_msg}")
    except Exception as e:
        print(f"  ❌ FAILED: An exception occurred during .pdf ingestion: {e}")
        
    print("\n" + "="*40)
    print("🔬 Test Complete.")

if __name__ == "__main__":
    run_controlled_test() 