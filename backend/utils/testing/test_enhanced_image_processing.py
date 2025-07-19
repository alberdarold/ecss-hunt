#!/usr/bin/env python3
"""
Test script to demonstrate enhanced image processing capabilities.
This script shows how to use the new OCR and visual content analysis features.
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
from datetime import datetime
from legacy.enhanced_image_processor import EnhancedImageProcessor

def test_enhanced_image_processing():
    """Test the enhanced image processing capabilities."""
    print("🧪 Testing Enhanced Image Processing System")
    print("=" * 50)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return False
    
    try:
        # Initialize processor
        processor = EnhancedImageProcessor(morphik_uri)
        print("✅ Enhanced Image Processor initialized")
        
        # Test 1: Process all chunks
        print("\n🔍 Test 1: Processing all chunks with OCR...")
        results = processor.process_all_chunks(search_terms=["ECSS", "the"])
        
        summary = results['summary']
        print(f"   📊 Results:")
        print(f"   • Total chunks: {summary['total_chunks']}")
        print(f"   • Visual chunks: {summary['visual_chunks']}")
        print(f"   • Text chunks: {summary['text_chunks']}")
        print(f"   • Chunks with extracted text: {summary['chunks_with_extracted_text']}")
        print(f"   • Processing time: {summary['processing_time']:.1f}s")
        print(f"   • Success rate: {summary['success_rate']:.1f}%")
        
        # Test 2: Enhanced search
        print("\n🔍 Test 2: Enhanced search with OCR results...")
        search_queries = [
            "ECSS requirements",
            "verification procedures", 
            "space engineering"
        ]
        
        for query in search_queries:
            print(f"\n   🔎 Query: '{query}'")
            search_results = processor.search_with_enhanced_results(query, limit=2)
            
            if search_results:
                for i, result in enumerate(search_results, 1):
                    print(f"      📄 Result {i}:")
                    print(f"         Type: {result['type']}")
                    print(f"         Score: {result['relevance_score']:.3f}")
                    print(f"         Summary: {result['summary'][:80]}...")
                    if result['type'] == 'visual_with_ocr':
                        print(f"         OCR Confidence: {result.get('ocr_confidence', 0):.1f}%")
            else:
                print("      ❌ No results found")
        
        # Save test results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_results_file = f"enhanced_processing_test_{timestamp}.json"
        
        test_data = {
            'timestamp': timestamp,
            'test_summary': {
                'total_chunks': summary['total_chunks'],
                'visual_chunks': summary['visual_chunks'],
                'text_chunks': summary['text_chunks'],
                'success_rate': summary['success_rate'],
                'processing_time': summary['processing_time']
            },
            'search_tests': search_queries
        }
        
        with open(test_results_file, 'w') as f:
            json.dump(test_data, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {test_results_file}")
        print(f"🖼️  Processed images saved to: {processor.output_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def check_system_requirements():
    """Check if required dependencies are installed."""
    print("🔧 Checking system requirements...")
    
    requirements = [
        ('PIL', 'Pillow'),
        ('pytesseract', 'pytesseract'),
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy')
    ]
    
    missing = []
    for module, package in requirements:
        try:
            __import__(module)
            print(f"   ✅ {package} - OK")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install " + " ".join(missing))
        return False
    
    # Check Tesseract OCR
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract OCR {version} - OK")
    except Exception as e:
        print(f"   ❌ Tesseract OCR - ERROR: {e}")
        print("   Install Tesseract OCR:")
        print("   • Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   • macOS: brew install tesseract")
        print("   • Linux: sudo apt-get install tesseract-ocr")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Enhanced Image Processing Test Suite")
    print("=" * 50)
    
    # Check requirements
    if not check_system_requirements():
        print("\n❌ System requirements check failed")
        print("Please install missing dependencies before running tests")
        return
    
    print("\n✅ All system requirements satisfied")
    
    # Run tests
    print("\n🧪 Running enhanced image processing tests...")
    success = test_enhanced_image_processing()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Check the processed images in 'enhanced_extracted_images/' folder")
        print("   2. Review the test results JSON file")
        print("   3. Try the enhanced_simplified_ingestion.py script")
        print("   4. Use the enhanced search capabilities in your application")
    else:
        print("\n❌ Tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 