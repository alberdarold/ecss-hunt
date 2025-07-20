#!/usr/bin/env python3
"""
Batch Ingest All ECSS Documents
Ingests all ECSS documents in manageable batches with cost control.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
import time
from datetime import datetime
from ecss_simplified_ingestion import SimplifiedECSSIngestion

def main():
    """Ingest all ECSS documents in batches."""
    print("=" * 60)
    print("ECSS Batch Ingestion - All Documents")
    print("⚠️  WARNING: This will be expensive and time-consuming!")
    print("📄 Documents under 100MB will be processed")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("[ERROR] MORPHIK_URI not found in environment variables")
        return
    
    # Initialize ingestion system
    try:
        ingestion = SimplifiedECSSIngestion(morphik_uri)
    except Exception as e:
        print(f"[ERROR] Failed to initialize: {e}")
        return
    
    # Set up PDF directory
    pdf_dir = Path("../../../ECSS Published Standards/1-Active Standards")
    if not pdf_dir.exists():
        print(f"[ERROR] PDF directory not found: {pdf_dir}")
        return
    
    # Get all suitable files
    all_files = ingestion.get_suitable_files(pdf_dir, max_docs=None)  # Get all files
    total_files = len(all_files)
    
    print(f"\n[INFO] Found {total_files} documents to ingest")
    print(f"[INFO] Estimated cost: ${total_files * 3:.0f}-${total_files * 5:.0f}")
    print(f"[INFO] Estimated time: {total_files * 2:.0f} minutes ({total_files * 2 / 60:.1f} hours)")
    
    # Ask for batch size
    try:
        batch_size = int(input("\nEnter batch size (recommended: 5-10): ").strip())
    except ValueError:
        batch_size = 5
        print("Using default batch size: 5")
    
    # Ask for confirmation
    confirm = input(f"\nProceed with {total_files} documents in batches of {batch_size}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Ingestion cancelled")
        return
    
    # Process in batches
    total_successful = 0
    total_failed = 0
    batch_results = []
    
    for batch_num in range(0, total_files, batch_size):
        batch_files = all_files[batch_num:batch_num + batch_size]
        current_batch = batch_num // batch_size + 1
        total_batches = (total_files + batch_size - 1) // batch_size
        
        print(f"\n{'='*50}")
        print(f"BATCH {current_batch}/{total_batches}")
        print(f"Processing {len(batch_files)} documents...")
        print(f"Progress: {batch_num + 1}-{min(batch_num + batch_size, total_files)} of {total_files}")
        print(f"{'='*50}")
        
        # Process this batch
        batch_start = time.time()
        
        for i, pdf_file in enumerate(batch_files, 1):
            print(f"\n[{i}/{len(batch_files)}] Processing: {pdf_file.name}")
            
            if ingestion.ingest_document(pdf_file):
                total_successful += 1
                print(f"✅ SUCCESS: {pdf_file.name}")
            else:
                total_failed += 1
                print(f"❌ FAILED: {pdf_file.name}")
            
            # Small delay between documents
            if i < len(batch_files):
                time.sleep(2)
        
        batch_time = time.time() - batch_start
        
        # Save batch results
        batch_result = {
            'batch_number': current_batch,
            'batch_size': len(batch_files),
            'successful': len([d for d in ingestion.ingested_docs if d['file'] in [str(f) for f in batch_files]]),
            'failed': len([d for d in ingestion.failed_docs if d['file'] in [str(f) for f in batch_files]]),
            'time': batch_time,
            'files': [f.name for f in batch_files]
        }
        batch_results.append(batch_result)
        
        print(f"\n📊 BATCH {current_batch} COMPLETE:")
        print(f"   Time: {batch_time:.1f}s")
        print(f"   Success: {batch_result['successful']}")
        print(f"   Failed: {batch_result['failed']}")
        
        # Ask if user wants to continue
        if current_batch < total_batches:
            continue_batch = input(f"\nContinue with next batch? (y/N): ").strip().lower()
            if continue_batch != 'y':
                print("Stopping at user request")
                break
    
    # Final summary
    total_time = sum(batch['time'] for batch in batch_results)
    
    print(f"\n{'='*60}")
    print("🎉 BATCH INGESTION COMPLETE")
    print(f"{'='*60}")
    print(f"📊 FINAL SUMMARY:")
    print(f"   Total documents: {total_files}")
    print(f"   Successful: {total_successful}")
    print(f"   Failed: {total_failed}")
    print(f"   Success rate: {(total_successful/total_files*100):.1f}%")
    print(f"   Total time: {total_time/60:.1f} minutes")
    print(f"   Average per doc: {total_time/total_files:.1f}s")
    
    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"batch_ingestion_all_results_{timestamp}.json"
    
    final_summary = {
        'total_documents': total_files,
        'successful_ingestions': total_successful,
        'failed_ingestions': total_failed,
        'success_rate': round(total_successful/total_files*100, 1),
        'total_time': round(total_time, 2),
        'average_time_per_doc': round(total_time/total_files, 2),
        'batch_results': batch_results,
        'ingested_docs': ingestion.ingested_docs,
        'failed_docs': ingestion.failed_docs
    }
    
    with open(results_file, 'w') as f:
        json.dump(final_summary, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main() 