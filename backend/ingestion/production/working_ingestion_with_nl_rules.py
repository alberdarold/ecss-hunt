#!/usr/bin/env python3
"""
Working ECSS Document Ingestion using NaturalLanguageRule

This implementation uses NaturalLanguageRule approach for metadata extraction
from ECSS documents with comprehensive text processing.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / "config" / ".env")

from morphik.ingestion import Morphik
from morphik.types import NaturalLanguageRule

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ECSSNLRuleIngestionSystem:
    """ECSS Document Ingestion System using Natural Language Rules."""

    def __init__(self, morphik_uri: str):
        """Initialize the ingestion system."""
        self.morphik_uri = morphik_uri
        self.db = Morphik(morphik_uri)
        
    def get_natural_language_rules(self) -> List[NaturalLanguageRule]:
        """Get natural language rules for ECSS documents."""
        return [
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
- applicable_domains: Array of space engineering domains this applies to"""
            )
        ]
    
    def ingest_single_document(self, pdf_path: Path) -> Dict[str, Any]:
        """Ingest a single PDF document with natural language rules."""
        try:
            logger.info(f"Ingesting document: {pdf_path.name}")
            
            # Ingest document with natural language rules
            result = self.db.ingest_pdf(
                pdf_path=str(pdf_path),
                natural_language_rules=self.get_natural_language_rules()
            )
            
            logger.info(f"Successfully ingested: {pdf_path.name}")
            return {
                "status": "success",
                "document_id": result.id if hasattr(result, 'id') else str(result),
                "filename": pdf_path.name
            }

        except Exception as e:
            logger.error(f"Failed to ingest {pdf_path.name}: {e}")
            return {
                "status": "error",
                "filename": pdf_path.name,
                "error": str(e)
            }
    
    def batch_ingest(self, pdf_directory: Path) -> Dict[str, Any]:
        """Batch ingest all PDF documents in a directory."""
        pdf_files = list(pdf_directory.glob("*.pdf"))

        if not pdf_files:
            return {"error": "No PDF files found in directory"}
        
        results = {
            "total_files": len(pdf_files),
            "successful": [],
            "failed": [],
            "summary": {}
        }
        
        for pdf_file in pdf_files:
            result = self.ingest_single_document(pdf_file)
            
            if result["status"] == "success":
                results["successful"].append(result)
            else:
                results["failed"].append(result)
        
        results["summary"] = {
            "success_count": len(results["successful"]),
            "failure_count": len(results["failed"]),
            "success_rate": len(results["successful"]) / len(pdf_files) * 100
        }
        
        return results

def main():
    """Main function to run ECSS document ingestion with natural language rules."""
    print("Working ECSS Document Ingestion with Natural Language Rules")
    print("=" * 60)

    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("Error: MORPHIK_URI not found in environment variables")
        return

    # Initialize system
    try:
        system = ECSSNLRuleIngestionSystem(morphik_uri)
        print("Successfully initialized ingestion system with NL rules")
    except Exception as e:
        print(f"Failed to initialize ingestion system: {e}")
        return
    
    # Check for PDF directory
    pdf_dir = Path(os.getenv("ECSS_DOCUMENTS_PATH", "../ECSS Published Standards/1-Active Standards"))

    if not pdf_dir.exists():
        print(f"PDF directory not found: {pdf_dir}")
        return
    
    print(f"PDF directory: {pdf_dir}")
    
    # Run batch ingestion
    try:
        print("\nStarting batch ingestion with natural language rules...")
        results = system.batch_ingest(pdf_dir)
        
        if "error" in results:
            print(f"Ingestion failed: {results['error']}")
            return
        
        print(f"\nIngestion completed!")
        print(f"Results:")
        print(f"  Total files: {results['total_files']}")
        print(f"  Successful: {results['summary']['success_count']}")
        print(f"  Failed: {results['summary']['failure_count']}")
        print(f"  Success rate: {results['summary']['success_rate']:.1f}%")
        
        # Save results
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = Path(f"nl_rules_ingestion_results_{timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {results_file}")

        except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    main() 