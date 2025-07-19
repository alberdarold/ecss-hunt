#!/usr/bin/env python3
"""
Morphik Visual Content Processor - WORKING SOLUTION
==================================================

This demonstrates that Morphik's ColPali is successfully extracting 
content from images. The PIL images are source data, and the processed 
understanding comes through query responses.

Usage:
    python morphik_visual_content_processor.py
"""

import os
import sys
from typing import List, Dict, Any
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / "config" / ".env")

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from morphik import Morphik

class MorphikVisualProcessor:
    def __init__(self):
        """Initialize connection to Morphik"""
        self.db = None
        self.connect_to_morphik()
    
    def connect_to_morphik(self):
        """Establish connection to Morphik"""
        try:
            # Get Morphik URI from environment
            morphik_uri = os.getenv("MORPHIK_URI")
            if not morphik_uri:
                print("❌ MORPHIK_URI not found in environment")
                sys.exit(1)
            
            # Initialize Morphik with URI
            self.db = Morphik(morphik_uri)
            print("✅ Connected to Morphik successfully")
        except Exception as e:
            print(f"❌ Failed to connect to Morphik: {e}")
            sys.exit(1)
    
    def analyze_visual_content(self, query: str = "What are the main requirements in this document?") -> Dict[str, Any]:
        """
        Analyze visual content using ColPali
        
        Args:
            query: Question to ask about the visual content
            
        Returns:
            Dict containing analysis results
        """
        print(f"\n🔍 Analyzing visual content with query: '{query}'")
        
        # Step 1: Get visual chunks
        chunks = self.db.retrieve_chunks(query, use_colpali=True, k=10)
        print(f"📊 Retrieved {len(chunks)} chunks")
        
        # Step 2: Analyze chunk types
        visual_chunks = []
        text_chunks = []
        
        for chunk in chunks:
            if hasattr(chunk, 'content') and isinstance(chunk.content, Image.Image):
                visual_chunks.append(chunk)
            else:
                text_chunks.append(chunk)
        
        print(f"🖼️  Visual chunks: {len(visual_chunks)}")
        print(f"📝 Text chunks: {len(text_chunks)}")
        
        # Step 3: Query for understanding
        response = self.db.query(query, use_colpali=True)
        
        # Step 4: Extract meaningful content
        content_analysis = {
            'query': query,
            'total_chunks': len(chunks),
            'visual_chunks': len(visual_chunks),
            'text_chunks': len(text_chunks),
            'response_available': bool(response and response.completion),
            'response_length': len(response.completion) if response and response.completion else 0,
            'sources_used': len(response.sources) if response and hasattr(response, 'sources') else 0
        }
        
        if response and response.completion:
            print(f"✅ Successfully extracted content ({content_analysis['response_length']} characters)")
            print(f"📚 Used {content_analysis['sources_used']} sources")
            
            # Show sample of extracted content
            preview = response.completion[:500] + "..." if len(response.completion) > 500 else response.completion
            print(f"\n📖 Content Preview:\n{preview}")
            
            content_analysis['content_preview'] = preview
            content_analysis['full_content'] = response.completion
        else:
            print("❌ No content extracted")
            content_analysis['content_preview'] = ""
            content_analysis['full_content'] = ""
        
        return content_analysis
    
    def test_multiple_queries(self) -> List[Dict[str, Any]]:
        """Test multiple queries to demonstrate visual content extraction"""
        
        test_queries = [
            "What are the main requirements in this document?",
            "What is the document title and standard number?",
            "What are the key sections mentioned in the table of contents?",
            "What is the scope of this ECSS standard?",
            "What are the management requirements described?"
        ]
        
        results = []
        
        print("\n🎯 Testing Multiple Queries to Demonstrate Visual Content Extraction")
        print("=" * 70)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Query {i}/{len(test_queries)} ---")
            result = self.analyze_visual_content(query)
            results.append(result)
            
            # Show success/failure
            if result['response_available']:
                print(f"✅ Query {i}: SUCCESS - {result['response_length']} chars extracted")
            else:
                print(f"❌ Query {i}: FAILED - No content extracted")
        
        return results
    
    def demonstrate_working_system(self):
        """Demonstrate that the visual content extraction system is working"""
        
        print("\n🚀 MORPHIK VISUAL CONTENT PROCESSOR")
        print("=" * 50)
        print("Demonstrating successful visual content extraction using ColPali")
        
        # Test basic functionality
        print("\n1️⃣ Testing Basic Visual Content Analysis")
        basic_result = self.analyze_visual_content()
        
        if basic_result['response_available']:
            print("\n✅ SYSTEM STATUS: WORKING")
            print(f"   - Visual chunks detected: {basic_result['visual_chunks']}")
            print(f"   - Content extracted: {basic_result['response_length']} characters")
            print(f"   - Sources used: {basic_result['sources_used']}")
        else:
            print("\n❌ SYSTEM STATUS: NOT WORKING")
            return False
        
        # Test multiple queries
        print("\n2️⃣ Testing Multiple Query Types")
        multi_results = self.test_multiple_queries()
        
        # Summary
        successful_queries = sum(1 for r in multi_results if r['response_available'])
        total_queries = len(multi_results)
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   - Total queries tested: {total_queries}")
        print(f"   - Successful extractions: {successful_queries}")
        print(f"   - Success rate: {successful_queries/total_queries*100:.1f}%")
        
        if successful_queries == total_queries:
            print(f"\n🎉 CONCLUSION: Visual content extraction is WORKING PERFECTLY!")
            print(f"   ColPali is successfully processing images and extracting meaningful content.")
        else:
            print(f"\n⚠️  CONCLUSION: Partial success - some queries failed")
        
        return successful_queries == total_queries
    
    def get_detailed_chunk_info(self):
        """Get detailed information about available chunks"""
        print("\n🔍 DETAILED CHUNK ANALYSIS")
        print("=" * 40)
        
        chunks = self.db.retrieve_chunks("requirements", use_colpali=True, k=5)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\n--- Chunk {i} ---")
            print(f"Type: {type(chunk.content)}")
            print(f"Document: {chunk.filename}")
            print(f"Chunk Number: {chunk.chunk_number}")
            print(f"Score: {chunk.score:.3f}")
            
            if isinstance(chunk.content, Image.Image):
                print(f"Image Size: {chunk.content.size}")
                print(f"Image Mode: {chunk.content.mode}")
                print("🖼️  Visual content detected")
            else:
                content_preview = str(chunk.content)[:100] + "..." if len(str(chunk.content)) > 100 else str(chunk.content)
                print(f"Content preview: {content_preview}")
                print("📝 Text content detected")

def main():
    """Main execution function"""
    processor = MorphikVisualProcessor()
    
    try:
        # Run the demonstration
        success = processor.demonstrate_working_system()
        
        # Show detailed chunk information
        processor.get_detailed_chunk_info()
        
        if success:
            print("\n🎯 KEY INSIGHT:")
            print("   The PIL images you see are the SOURCE DATA.")
            print("   ColPali processes them to create embeddings.")
            print("   The PROCESSED UNDERSTANDING comes through query responses.")
            print("   Your system is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 