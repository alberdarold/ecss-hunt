

#!/usr/bin/env python3
"""
Test the smart ingestion system with automatic fallback.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test the smart ingestion system with automatic fallback.
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from core.clean_and_ingest import ECSSRulesBasedIngestion

def test_smart_ingestion():
    """Test the smart ingestion system."""
    print("🧠 Testing Smart Ingestion System")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Initialize ingestion system
    try:
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        print("✅ Initialized smart ingestion system")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    print(f"📁 PDF directory: {pdf_dir}")
    
    # Test smart ingestion with 1 document
    print("\n🚀 Testing smart ingestion with 1 document...")
    try:
        results = ingestion_system.smart_ingest_documents_batch(pdf_dir, max_docs=1)
        
        if 'error' in results:
            print(f"❌ Smart ingestion failed: {results['error']}")
            return
        
        print(f"\n✅ Smart ingestion completed!")
        print(f"📊 Results:")
        print(f"   - Total documents: {results['total_documents']}")
        print(f"   - Successful: {results['successful_ingestions']}")
        print(f"   - Failed: {results['failed_ingestions']}")
        print(f"   - Success rate: {results['success_rate']}%")
        print(f"   - Total time: {results['total_time']}s")
        print(f"   - Average time per doc: {results['average_time_per_doc']}s")
        
        # Show method breakdown
        print(f"   - Text-based successful: {results.get('text_based_successful', 0)}")
        print(f"   - Image-based successful: {results.get('image_based_successful', 0)}")
        
        # Show which method was used for each document
        if results.get('ingested_docs'):
            print(f"\n📄 Document details:")
            for doc in results['ingested_docs']:
                print(f"   - {doc.get('filename', 'Unknown')}: {doc.get('method_used', 'Unknown method')}")
        
        print(f"\n🎉 Smart ingestion test completed successfully!")
        
    except Exception as e:
        print(f"❌ Smart ingestion test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_smart_ingestion() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from core.clean_and_ingest import ECSSRulesBasedIngestion

def test_smart_ingestion():
    """Test the smart ingestion system."""
    print("🧠 Testing Smart Ingestion System")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    # Initialize ingestion system
    try:
        ingestion_system = ECSSRulesBasedIngestion(morphik_uri)
        print("✅ Initialized smart ingestion system")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return
    
    print(f"📁 PDF directory: {pdf_dir}")
    
    # Test smart ingestion with 1 document
    print("\n🚀 Testing smart ingestion with 1 document...")
    try:
        results = ingestion_system.smart_ingest_documents_batch(pdf_dir, max_docs=1)
        
        if 'error' in results:
            print(f"❌ Smart ingestion failed: {results['error']}")
            return
        
        print(f"\n✅ Smart ingestion completed!")
        print(f"📊 Results:")
        print(f"   - Total documents: {results['total_documents']}")
        print(f"   - Successful: {results['successful_ingestions']}")
        print(f"   - Failed: {results['failed_ingestions']}")
        print(f"   - Success rate: {results['success_rate']}%")
        print(f"   - Total time: {results['total_time']}s")
        print(f"   - Average time per doc: {results['average_time_per_doc']}s")
        
        # Show method breakdown
        print(f"   - Text-based successful: {results.get('text_based_successful', 0)}")
        print(f"   - Image-based successful: {results.get('image_based_successful', 0)}")
        
        # Show which method was used for each document
        if results.get('ingested_docs'):
            print(f"\n📄 Document details:")
            for doc in results['ingested_docs']:
                print(f"   - {doc.get('filename', 'Unknown')}: {doc.get('method_used', 'Unknown method')}")
        
        print(f"\n🎉 Smart ingestion test completed successfully!")
        
    except Exception as e:
        print(f"❌ Smart ingestion test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_smart_ingestion() 