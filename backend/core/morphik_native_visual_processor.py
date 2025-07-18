#!/usr/bin/env python3
"""
Morphik Native Visual Content Processor
Leverages Morphik's built-in multimodal search and visual understanding capabilities.
No external OCR needed - uses Morphik's native ColPali and visual processing.
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
import logging
import time
from typing import List, Dict, Optional, Any
from datetime import datetime

from morphik import Morphik

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('morphik_native_visual.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MorphikNativeVisualProcessor:
    """Processor that leverages Morphik's native visual understanding capabilities."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the processor with Morphik's native capabilities."""
        self.db = Morphik(morphik_uri)
        
        # Validate connection
        try:
            self.db.list_documents()
            logger.info("✅ Connected to Morphik with native visual processing")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Morphik: {e}")
            raise
    
    def analyze_visual_content_with_morphik(self, query: str = "visual content") -> Dict[str, Any]:
        """Use Morphik's native visual understanding to analyze content."""
        try:
            logger.info(f"🔍 Analyzing visual content with Morphik's native capabilities")
            
            # Use Morphik's native query with ColPali enabled
            response = self.db.query(
                query,
                use_colpali=True,  # Enable visual understanding
                k=20  # Get more results for comprehensive analysis
            )
            
            visual_analysis = {
                'query': query,
                'total_sources': len(response.sources) if response.sources else 0,
                'visual_elements': [],
                'text_content': [],
                'response_text': response.response if hasattr(response, 'response') else '',
                'processing_time': time.time()
            }
            
            if response.sources:
                for i, source in enumerate(response.sources):
                    source_info = {
                        'index': i,
                        'document_id': getattr(source, 'document_id', 'unknown'),
                        'chunk_id': getattr(source, 'chunk_id', 'unknown'),
                        'score': getattr(source, 'score', 0.0),
                        'content_type': 'unknown'
                    }
                    
                    # Check if this is visual content
                    if hasattr(source, 'content') and source.content:
                        content = source.content
                        
                        # Detect visual content (PIL Images from ColPali)
                        if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                            source_info.update({
                                'content_type': 'visual',
                                'image_type': type(content).__name__,
                                'image_size': getattr(content, 'size', 'unknown'),
                                'image_mode': getattr(content, 'mode', 'unknown'),
                                'description': f"Visual element detected by ColPali: {type(content).__name__}"
                            })
                            visual_analysis['visual_elements'].append(source_info)
                        
                        # Handle text content
                        elif isinstance(content, str):
                            source_info.update({
                                'content_type': 'text',
                                'text_length': len(content),
                                'text_preview': content[:200] + "..." if len(content) > 200 else content
                            })
                            visual_analysis['text_content'].append(source_info)
                        
                        # Handle other content types
                        else:
                            source_info.update({
                                'content_type': 'other',
                                'content_str': str(content)[:100]
                            })
                    
                    # Check for text attributes
                    elif hasattr(source, 'text') and source.text:
                        source_info.update({
                            'content_type': 'text',
                            'text_length': len(source.text),
                            'text_preview': source.text[:200] + "..." if len(source.text) > 200 else source.text
                        })
                        visual_analysis['text_content'].append(source_info)
            
            logger.info(f"📊 Visual analysis complete:")
            logger.info(f"   • Total sources: {visual_analysis['total_sources']}")
            logger.info(f"   • Visual elements: {len(visual_analysis['visual_elements'])}")
            logger.info(f"   • Text content: {len(visual_analysis['text_content'])}")
            
            return visual_analysis
            
        except Exception as e:
            logger.error(f"❌ Visual analysis failed: {e}")
            return {
                'query': query,
                'error': str(e),
                'total_sources': 0,
                'visual_elements': [],
                'text_content': []
            }
    
    def search_visual_content(self, query: str, focus_area: str = None) -> List[Dict[str, Any]]:
        """Search for visual content using Morphik's native capabilities."""
        try:
            logger.info(f"🔍 Searching visual content for: '{query}'")
            
            # Build enhanced query for visual content
            if focus_area:
                enhanced_query = f"{query} {focus_area}"
            else:
                enhanced_query = query
            
            # Use Morphik's native multimodal search
            response = self.db.query(
                enhanced_query,
                use_colpali=True,  # Enable visual understanding
                k=10
            )
            
            results = []
            
            if response.sources:
                for i, source in enumerate(response.sources):
                    result = {
                        'index': i,
                        'query': enhanced_query,
                        'relevance_score': getattr(source, 'score', 0.0),
                        'document_id': getattr(source, 'document_id', 'unknown'),
                        'chunk_id': getattr(source, 'chunk_id', 'unknown'),
                        'content_type': 'unknown',
                        'morphik_processed': True  # Flag to indicate native processing
                    }
                    
                    # Process content with Morphik's understanding
                    if hasattr(source, 'content') and source.content:
                        content = source.content
                        
                        # Visual content processed by ColPali
                        if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                            result.update({
                                'content_type': 'visual',
                                'summary': f"Visual element understood by Morphik ColPali: {type(content).__name__}",
                                'text': f"[Visual Content] Image/diagram/table processed by ColPali visual understanding",
                                'visual_info': {
                                    'type': type(content).__name__,
                                    'size': getattr(content, 'size', 'unknown'),
                                    'mode': getattr(content, 'mode', 'unknown'),
                                    'processed_by': 'ColPali'
                                }
                            })
                        
                        # Text content
                        elif isinstance(content, str):
                            result.update({
                                'content_type': 'text',
                                'text': content,
                                'summary': content[:200] + "..." if len(content) > 200 else content
                            })
                        
                        # Other content types
                        else:
                            result.update({
                                'content_type': 'other',
                                'text': str(content),
                                'summary': f"Content type: {type(content).__name__}"
                            })
                    
                    # Handle text attribute
                    elif hasattr(source, 'text') and source.text:
                        result.update({
                            'content_type': 'text',
                            'text': source.text,
                            'summary': source.text[:200] + "..." if len(source.text) > 200 else source.text
                        })
                    
                    results.append(result)
            
            logger.info(f"✅ Found {len(results)} results using Morphik's native capabilities")
            return results
            
        except Exception as e:
            logger.error(f"❌ Visual search failed: {e}")
            return []
    
    def query_with_visual_context(self, question: str) -> Dict[str, Any]:
        """Ask questions about visual content using Morphik's native understanding."""
        try:
            logger.info(f"❓ Querying with visual context: '{question}'")
            
            # Use Morphik's native query with visual understanding
            response = self.db.query(
                question,
                use_colpali=True  # Enable visual understanding
            )
            
            result = {
                'question': question,
                'response': response.response if hasattr(response, 'response') else '',
                'sources_count': len(response.sources) if response.sources else 0,
                'visual_sources': [],
                'text_sources': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Categorize sources
            if response.sources:
                for source in response.sources:
                    source_info = {
                        'document_id': getattr(source, 'document_id', 'unknown'),
                        'score': getattr(source, 'score', 0.0)
                    }
                    
                    # Check for visual content
                    if hasattr(source, 'content') and source.content:
                        if hasattr(source.content, '__class__') and 'PIL' in str(type(source.content).__module__):
                            source_info['type'] = 'visual'
                            source_info['description'] = f"Visual element processed by ColPali"
                            result['visual_sources'].append(source_info)
                        else:
                            source_info['type'] = 'text'
                            source_info['preview'] = str(source.content)[:100]
                            result['text_sources'].append(source_info)
                    elif hasattr(source, 'text'):
                        source_info['type'] = 'text'
                        source_info['preview'] = source.text[:100]
                        result['text_sources'].append(source_info)
            
            logger.info(f"✅ Query completed with {len(result['visual_sources'])} visual and {len(result['text_sources'])} text sources")
            return result
            
        except Exception as e:
            logger.error(f"❌ Query with visual context failed: {e}")
            return {
                'question': question,
                'error': str(e),
                'response': '',
                'sources_count': 0,
                'visual_sources': [],
                'text_sources': []
            }
    
    def get_visual_content_summary(self) -> Dict[str, Any]:
        """Get a summary of visual content using Morphik's native capabilities."""
        try:
            logger.info("📊 Getting visual content summary using Morphik native capabilities")
            
            # Test queries for different types of visual content
            test_queries = [
                "diagrams and figures",
                "tables and charts", 
                "technical drawings",
                "process flows",
                "requirements and specifications"
            ]
            
            summary = {
                'total_queries': len(test_queries),
                'query_results': [],
                'visual_content_detected': 0,
                'text_content_detected': 0,
                'total_sources': 0,
                'morphik_native_processing': True
            }
            
            for query in test_queries:
                logger.info(f"   Testing query: '{query}'")
                
                try:
                    response = self.db.query(query, use_colpali=True, k=5)
                    
                    query_result = {
                        'query': query,
                        'sources_found': len(response.sources) if response.sources else 0,
                        'visual_sources': 0,
                        'text_sources': 0,
                        'response_available': bool(hasattr(response, 'response') and response.response)
                    }
                    
                    if response.sources:
                        for source in response.sources:
                            if hasattr(source, 'content') and source.content:
                                if hasattr(source.content, '__class__') and 'PIL' in str(type(source.content).__module__):
                                    query_result['visual_sources'] += 1
                                    summary['visual_content_detected'] += 1
                                else:
                                    query_result['text_sources'] += 1
                                    summary['text_content_detected'] += 1
                            elif hasattr(source, 'text'):
                                query_result['text_sources'] += 1
                                summary['text_content_detected'] += 1
                    
                    summary['query_results'].append(query_result)
                    summary['total_sources'] += query_result['sources_found']
                    
                except Exception as e:
                    logger.warning(f"Query '{query}' failed: {e}")
                    summary['query_results'].append({
                        'query': query,
                        'error': str(e),
                        'sources_found': 0
                    })
            
            logger.info(f"📊 Summary complete:")
            logger.info(f"   • Total sources found: {summary['total_sources']}")
            logger.info(f"   • Visual content detected: {summary['visual_content_detected']}")
            logger.info(f"   • Text content detected: {summary['text_content_detected']}")
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Visual content summary failed: {e}")
            return {
                'error': str(e),
                'total_queries': 0,
                'query_results': [],
                'visual_content_detected': 0,
                'text_content_detected': 0
            }

def main():
    """Main function to demonstrate Morphik's native visual processing."""
    print("🚀 Morphik Native Visual Content Processor")
    print("=" * 60)
    print("✨ Using Morphik's built-in ColPali and multimodal capabilities")
    print("🔍 No external OCR needed - leveraging native visual understanding")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize processor
    try:
        processor = MorphikNativeVisualProcessor(morphik_uri)
        print("✅ Morphik native visual processor initialized")
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return
    
    # Test 1: Analyze visual content
    print("\n🔍 Test 1: Analyzing visual content with Morphik's native capabilities...")
    visual_analysis = processor.analyze_visual_content_with_morphik("ECSS diagrams tables figures")
    
    print(f"📊 Analysis Results:")
    print(f"   • Total sources: {visual_analysis['total_sources']}")
    print(f"   • Visual elements: {len(visual_analysis['visual_elements'])}")
    print(f"   • Text content: {len(visual_analysis['text_content'])}")
    
    # Test 2: Search visual content
    print("\n🔍 Test 2: Searching visual content...")
    search_queries = [
        "ECSS requirements diagrams",
        "verification procedures tables",
        "space engineering figures"
    ]
    
    for query in search_queries:
        print(f"\n   🔎 Query: '{query}'")
        results = processor.search_visual_content(query)
        
        if results:
            for i, result in enumerate(results[:2], 1):
                print(f"      📄 Result {i}:")
                print(f"         Type: {result['content_type']}")
                print(f"         Score: {result['relevance_score']:.3f}")
                print(f"         Summary: {result['summary'][:80]}...")
                if result['content_type'] == 'visual':
                    print(f"         Processed by: {result['visual_info']['processed_by']}")
        else:
            print("      ❌ No results found")
    
    # Test 3: Query with visual context
    print("\n🔍 Test 3: Querying with visual context...")
    questions = [
        "What are the main requirements shown in the diagrams?",
        "Describe the verification procedures in the tables",
        "What technical specifications are shown in the figures?"
    ]
    
    for question in questions:
        print(f"\n   ❓ Question: '{question}'")
        result = processor.query_with_visual_context(question)
        
        if result['response']:
            print(f"      💬 Response: {result['response'][:100]}...")
            print(f"      📊 Sources: {result['sources_count']} total ({len(result['visual_sources'])} visual, {len(result['text_sources'])} text)")
        else:
            print("      ❌ No response generated")
    
    # Test 4: Get visual content summary
    print("\n🔍 Test 4: Getting visual content summary...")
    summary = processor.get_visual_content_summary()
    
    print(f"📊 Visual Content Summary:")
    print(f"   • Total sources: {summary['total_sources']}")
    print(f"   • Visual content detected: {summary['visual_content_detected']}")
    print(f"   • Text content detected: {summary['text_content_detected']}")
    print(f"   • Native processing: {summary['morphik_native_processing']}")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"morphik_native_visual_results_{timestamp}.json"
    
    results_data = {
        'timestamp': timestamp,
        'visual_analysis': visual_analysis,
        'visual_content_summary': summary,
        'test_queries': search_queries,
        'test_questions': questions
    }
    
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")
    print(f"\n🎉 Native visual processing demonstration complete!")
    print(f"\n📋 Key benefits of using Morphik's native capabilities:")
    print(f"   • No external OCR dependencies")
    print(f"   • Built-in ColPali visual understanding")
    print(f"   • Native multimodal search")
    print(f"   • Integrated visual and text processing")

if __name__ == "__main__":
    main() 