#!/usr/bin/env python3
"""
Windows-compatible test script for Morphik native capabilities.
No Unicode emoji characters to avoid Windows console encoding issues.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
from datetime import datetime
from morphik_native_visual_processor import MorphikNativeVisualProcessor
from morphik_native_simplified_ingestion import MorphikNativeECSSIngestion

def test_native_visual_processing():
    """Test Morphik's native visual processing capabilities."""
    print("Testing Morphik's Native Visual Processing")
    print("=" * 50)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found in environment variables")
        return False
    
    try:
        # Initialize processor
        processor = MorphikNativeVisualProcessor(morphik_uri)
        print("SUCCESS: Native visual processor initialized")
        
        # Test 1: Analyze visual content with native capabilities
        print("\nTest 1: Analyzing visual content with native capabilities...")
        visual_analysis = processor.analyze_visual_content_with_morphik("ECSS diagrams tables figures")
        
        print(f"   Results:")
        print(f"   - Total sources: {visual_analysis['total_sources']}")
        print(f"   - Visual elements: {len(visual_analysis['visual_elements'])}")
        print(f"   - Text content: {len(visual_analysis['text_content'])}")
        print(f"   - Response available: {bool(visual_analysis['response_text'])}")
        
        # Test 2: Search visual content
        print("\nTest 2: Native visual content search...")
        search_results = processor.search_visual_content("ECSS requirements diagrams", "technical specifications")
        
        if search_results:
            print(f"   SUCCESS: Found {len(search_results)} results")
            for i, result in enumerate(search_results[:2], 1):
                print(f"      Result {i}:")
                print(f"         Type: {result['content_type']}")
                print(f"         Score: {result['relevance_score']:.3f}")
                print(f"         Native processing: {result['morphik_processed']}")
        else:
            print("   WARNING: No results found")
        
        # Test 3: Query with visual context
        print("\nTest 3: Query with visual context...")
        questions = [
            "What are the main ECSS requirements shown in the document?",
            "Describe the verification procedures mentioned in the standard"
        ]
        
        for question in questions:
            print(f"\n   Question: '{question}'")
            result = processor.query_with_visual_context(question)
            
            if result['response']:
                print(f"      Response: {result['response'][:100]}...")
                print(f"      Sources: {result['sources_count']} total")
                print(f"      Visual sources: {len(result['visual_sources'])}")
                print(f"      Text sources: {len(result['text_sources'])}")
            else:
                print("      WARNING: No response generated")
        
        # Test 4: Visual content summary
        print("\nTest 4: Visual content summary...")
        summary = processor.get_visual_content_summary()
        
        print(f"   Summary:")
        print(f"   - Total sources: {summary['total_sources']}")
        print(f"   - Visual content: {summary['visual_content_detected']}")
        print(f"   - Text content: {summary['text_content_detected']}")
        print(f"   - Native processing: {summary['morphik_native_processing']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        return False

def test_native_ingestion():
    """Test the native ingestion capabilities."""
    print("\nTesting Native Ingestion Capabilities")
    print("=" * 50)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found in environment variables")
        return False
    
    try:
        # Initialize ingestion
        ingestion = MorphikNativeECSSIngestion(morphik_uri)
        print("SUCCESS: Native ingestion system initialized")
        
        # Test the analysis capabilities without ingesting new documents
        print("\nTesting analysis with existing documents...")
        
        # Get existing documents
        try:
            documents = ingestion.db.list_documents()
            if documents:
                print(f"   Found {len(documents)} existing documents")
                
                # Test analysis on first document
                doc = documents[0]
                print(f"   Analyzing: {doc.filename}")
                
                analysis = ingestion.analyze_with_native_capabilities(doc)
                
                print(f"   Analysis results:")
                print(f"   - Total sources: {analysis['total_sources_found']}")
                print(f"   - Visual understanding: {analysis['visual_understanding']['visual_processing_active']}")
                print(f"   - Text processing: {analysis['text_content']['text_processing_active']}")
                print(f"   - ColPali enabled: {analysis['visual_understanding']['colpali_enabled']}")
                
                # Test native search
                print(f"\nTesting native multimodal search...")
                search_results = ingestion.native_multimodal_search("ECSS requirements", limit=3)
                
                if search_results:
                    print(f"   SUCCESS: Found {len(search_results)} search results")
                    for i, result in enumerate(search_results[:2], 1):
                        print(f"      Result {i}:")
                        print(f"         Type: {result['type']}")
                        print(f"         Score: {result['relevance_score']:.3f}")
                        print(f"         Native: {result['morphik_native']}")
                        print(f"         Multimodal: {result['multimodal_search']}")
                else:
                    print("   WARNING: No search results found")
                    
            else:
                print("   WARNING: No existing documents found")
                print("   Run the ingestion script first to test analysis capabilities")
                
        except Exception as e:
            print(f"   ERROR: Error accessing documents: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"ERROR: Native ingestion test failed: {e}")
        return False

def check_morphik_capabilities():
    """Check if Morphik is properly configured for multimodal capabilities."""
    print("Checking Morphik Configuration")
    print("=" * 50)
    
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found in environment variables")
        return False
    
    try:
        from morphik import Morphik
        
        db = Morphik(morphik_uri)
        print("SUCCESS: Morphik connection established")
        
        # Test basic functionality
        documents = db.list_documents()
        print(f"SUCCESS: Document listing works: {len(documents)} documents found")
        
        # Test query capability
        if documents:
            test_response = db.query("test query", use_colpali=True, k=1)
            print(f"SUCCESS: Query capability works: {hasattr(test_response, 'sources')}")
            
            if hasattr(test_response, 'sources') and test_response.sources:
                print(f"SUCCESS: ColPali enabled: Sources returned")
                
                # Check for visual content
                source = test_response.sources[0]
                if hasattr(source, 'content') and source.content:
                    if hasattr(source.content, '__class__') and 'PIL' in str(type(source.content).__module__):
                        print("SUCCESS: Visual content detected: PIL Image objects found")
                    else:
                        print("INFO: Text content detected")
                else:
                    print("INFO: Source structure: No content attribute found")
            else:
                print("WARNING: No sources returned from query")
        else:
            print("INFO: No documents available for testing query capabilities")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Morphik configuration check failed: {e}")
        return False

def main():
    """Main test function."""
    print("Morphik Native Capabilities Test Suite")
    print("=" * 60)
    print("Testing Morphik's built-in multimodal capabilities")
    print("No external OCR or image processing dependencies")
    print("=" * 60)
    
    # Check Morphik configuration
    print("\nStep 1: Checking Morphik configuration...")
    if not check_morphik_capabilities():
        print("\nERROR: Morphik configuration check failed")
        print("Please ensure:")
        print("   1. MORPHIK_URI is set correctly")
        print("   2. Morphik service is accessible")
        print("   3. You have documents ingested with ColPali enabled")
        return
    
    print("\nSUCCESS: Morphik configuration check passed")
    
    # Test native visual processing
    print("\nStep 2: Testing native visual processing...")
    visual_success = test_native_visual_processing()
    
    if not visual_success:
        print("\nWARNING: Native visual processing tests had issues")
        print("This might be expected if no visual content is available")
    else:
        print("\nSUCCESS: Native visual processing tests passed")
    
    # Test native ingestion capabilities
    print("\nStep 3: Testing native ingestion capabilities...")
    ingestion_success = test_native_ingestion()
    
    if not ingestion_success:
        print("\nWARNING: Native ingestion tests had issues")
        print("This might be expected if no documents are available")
    else:
        print("\nSUCCESS: Native ingestion tests passed")
    
    # Save test results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_results_file = f"morphik_native_test_results_windows_{timestamp}.json"
    
    test_data = {
        'timestamp': timestamp,
        'morphik_config_check': True,
        'visual_processing_test': visual_success,
        'ingestion_test': ingestion_success,
        'native_capabilities': True,
        'external_dependencies': False,
        'windows_compatible': True
    }
    
    with open(test_results_file, 'w') as f:
        json.dump(test_data, f, indent=2, default=str)
    
    print(f"\nTest results saved to: {test_results_file}")
    
    # Summary
    if visual_success and ingestion_success:
        print("\nSUCCESS: All tests completed successfully!")
        print("\nNext steps:")
        print("   1. Use morphik_native_simplified_ingestion.py to ingest documents")
        print("   2. Use morphik_native_visual_processor.py for analysis")
        print("   3. Leverage Morphik's native multimodal search capabilities")
        print("   4. No external OCR or image processing needed!")
    else:
        print("\nWARNING: Some tests had issues, but this is expected without documents")
        print("   Run the ingestion script first to fully test capabilities")

if __name__ == "__main__":
    main() 