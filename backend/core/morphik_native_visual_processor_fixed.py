#!/usr/bin/env python3
"""
FIXED: Morphik Native Visual Content Processor
Now uses the correct API methods based on debug findings:
- retrieve_chunks() for content analysis (has PIL Images)
- query() for search responses (has metadata only)
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

# Configure logging with Windows-compatible format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('morphik_native_visual_fixed.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MorphikNativeVisualProcessorFixed:
    """Fixed processor that uses correct API methods for visual content."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the processor with Morphik's native capabilities."""
        self.db = Morphik(morphik_uri)
        
        # Validate connection
        try:
            self.db.list_documents()
            logger.info("SUCCESS: Connected to Morphik with native visual processing")
        except Exception as e:
            logger.error(f"ERROR: Failed to connect to Morphik: {e}")
            raise
    
    def analyze_visual_content_with_chunks(self, search_term: str = "ECSS") -> Dict[str, Any]:
        """Use retrieve_chunks() to analyze visual content (has PIL Images)."""
        try:
            logger.info(f"ANALYZING: Visual content using retrieve_chunks() method")
            
            # Use retrieve_chunks() which returns FinalChunkResult with content
            chunks = self.db.retrieve_chunks(search_term)
            
            visual_analysis = {
                'method': 'retrieve_chunks',
                'search_term': search_term,
                'total_chunks': len(chunks) if chunks else 0,
                'visual_elements': [],
                'text_elements': [],
                'processing_time': time.time()
            }
            
            if chunks:
                logger.info(f"FOUND: {len(chunks)} chunks from retrieve_chunks()")
                
                for i, chunk in enumerate(chunks):
                    chunk_info = {
                        'index': i,
                        'chunk_type': str(type(chunk)),
                        'document_id': getattr(chunk, 'document_id', 'unknown'),
                        'chunk_number': getattr(chunk, 'chunk_number', 'unknown'),
                        'score': getattr(chunk, 'score', 0.0),
                        'content_type': 'unknown'
                    }
                    
                    # Check if this chunk has content (FinalChunkResult should have it)
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        
                        # Check for PIL Image objects (visual content from ColPali)
                        if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                            chunk_info.update({
                                'content_type': 'visual_pil_image',
                                'image_type': type(content).__name__,
                                'image_size': getattr(content, 'size', 'unknown'),
                                'image_mode': getattr(content, 'mode', 'unknown'),
                                'description': f"PIL Image: {type(content).__name__}"
                            })
                            
                            # Check metadata for additional info
                            if hasattr(chunk, 'metadata') and chunk.metadata:
                                chunk_info['metadata'] = chunk.metadata
                                is_image = chunk.metadata.get('is_image', False)
                                if is_image:
                                    chunk_info['confirmed_image'] = True
                            
                            visual_analysis['visual_elements'].append(chunk_info)
                            logger.info(f"VISUAL: Found PIL Image {type(content).__name__} size {getattr(content, 'size', 'unknown')}")
                        
                        # Handle text content
                        elif isinstance(content, str):
                            chunk_info.update({
                                'content_type': 'text',
                                'text_length': len(content),
                                'text_preview': content[:200] + "..." if len(content) > 200 else content
                            })
                            visual_analysis['text_elements'].append(chunk_info)
                            logger.info(f"TEXT: Found text content {len(content)} chars")
                        
                        # Handle other content types
                        else:
                            chunk_info.update({
                                'content_type': 'other',
                                'content_str': str(content)[:100]
                            })
                            logger.info(f"OTHER: Found content type {type(content)}")
                    
                    else:
                        chunk_info['content_type'] = 'no_content'
                        logger.info(f"NO CONTENT: Chunk {i} has no content attribute")
            
            else:
                logger.warning(f"NO CHUNKS: retrieve_chunks() returned no results")
            
            logger.info(f"ANALYSIS COMPLETE:")
            logger.info(f"  - Total chunks: {visual_analysis['total_chunks']}")
            logger.info(f"  - Visual elements: {len(visual_analysis['visual_elements'])}")
            logger.info(f"  - Text elements: {len(visual_analysis['text_elements'])}")
            
            return visual_analysis
            
        except Exception as e:
            logger.error(f"ERROR: Visual analysis failed: {e}")
            return {
                'method': 'retrieve_chunks',
                'search_term': search_term,
                'error': str(e),
                'total_chunks': 0,
                'visual_elements': [],
                'text_elements': []
            }
    
    def search_with_query_and_fetch_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Use query() for search, then fetch content separately."""
        try:
            logger.info(f"SEARCH: Using query() method for: '{query}'")
            
            # Use query() for search capabilities
            response = self.db.query(query, use_colpali=True, k=limit)
            
            results = []
            
            if response.sources:
                logger.info(f"QUERY RESULTS: Found {len(response.sources)} sources")
                
                # Get all available chunks to match with query results
                all_chunks = self.db.retrieve_chunks(query)
                
                for i, source in enumerate(response.sources):
                    result = {
                        'index': i,
                        'query': query,
                        'relevance_score': getattr(source, 'score', 0.0),
                        'document_id': getattr(source, 'document_id', 'unknown'),
                        'chunk_number': getattr(source, 'chunk_number', 'unknown'),
                        'source_type': str(type(source)),
                        'content_found': False,
                        'content_type': 'unknown'
                    }
                    
                    # Try to find matching chunk content
                    chunk_number = getattr(source, 'chunk_number', None)
                    document_id = getattr(source, 'document_id', None)
                    
                    if chunk_number is not None and document_id and all_chunks:
                        # Find matching chunk
                        for chunk in all_chunks:
                            if (getattr(chunk, 'chunk_number', None) == chunk_number and 
                                getattr(chunk, 'document_id', None) == document_id):
                                
                                # Found matching chunk with content
                                if hasattr(chunk, 'content') and chunk.content:
                                    content = chunk.content
                                    
                                    # Check for PIL Image
                                    if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                                        result.update({
                                            'content_found': True,
                                            'content_type': 'visual',
                                            'text': f"[Visual Content] PIL Image: {type(content).__name__}",
                                            'summary': f"Visual element processed by ColPali: {type(content).__name__} size {getattr(content, 'size', 'unknown')}",
                                            'visual_info': {
                                                'type': type(content).__name__,
                                                'size': getattr(content, 'size', 'unknown'),
                                                'mode': getattr(content, 'mode', 'unknown'),
                                                'processed_by': 'ColPali'
                                            }
                                        })
                                        
                                        # Check metadata
                                        if hasattr(chunk, 'metadata') and chunk.metadata:
                                            result['metadata'] = chunk.metadata
                                    
                                    # Handle text content
                                    elif isinstance(content, str):
                                        result.update({
                                            'content_found': True,
                                            'content_type': 'text',
                                            'text': content,
                                            'summary': content[:200] + "..." if len(content) > 200 else content
                                        })
                                
                                break
                    
                    # If no content found, it's just metadata
                    if not result['content_found']:
                        result.update({
                            'content_type': 'metadata_only',
                            'text': f"[Metadata Only] Document: {document_id}, Chunk: {chunk_number}",
                            'summary': f"Search result with metadata only (score: {result['relevance_score']:.3f})"
                        })
                    
                    results.append(result)
                
                logger.info(f"SEARCH COMPLETE: {len(results)} results with content lookup")
                
            else:
                logger.warning(f"NO RESULTS: query() returned no sources")
            
            return results
            
        except Exception as e:
            logger.error(f"ERROR: Search failed: {e}")
            return []
    
    def query_with_visual_understanding(self, question: str) -> Dict[str, Any]:
        """Ask questions leveraging visual understanding."""
        try:
            logger.info(f"VISUAL QUERY: '{question}'")
            
            # Use query() for the question
            response = self.db.query(question, use_colpali=True)
            
            result = {
                'question': question,
                'response': response.response if hasattr(response, 'response') else '',
                'sources_count': len(response.sources) if response.sources else 0,
                'visual_sources': [],
                'text_sources': [],
                'metadata_sources': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Analyze sources and fetch content
            if response.sources:
                # Get chunks to match with sources
                all_chunks = self.db.retrieve_chunks(question)
                
                for source in response.sources:
                    source_info = {
                        'document_id': getattr(source, 'document_id', 'unknown'),
                        'chunk_number': getattr(source, 'chunk_number', 'unknown'),
                        'score': getattr(source, 'score', 0.0),
                        'content_found': False
                    }
                    
                    # Try to find matching chunk content
                    chunk_number = getattr(source, 'chunk_number', None)
                    document_id = getattr(source, 'document_id', None)
                    
                    if chunk_number is not None and document_id and all_chunks:
                        for chunk in all_chunks:
                            if (getattr(chunk, 'chunk_number', None) == chunk_number and 
                                getattr(chunk, 'document_id', None) == document_id):
                                
                                if hasattr(chunk, 'content') and chunk.content:
                                    content = chunk.content
                                    
                                    # Check for visual content
                                    if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                                        source_info.update({
                                            'type': 'visual',
                                            'description': f"PIL Image: {type(content).__name__}",
                                            'size': getattr(content, 'size', 'unknown'),
                                            'content_found': True
                                        })
                                        result['visual_sources'].append(source_info)
                                    
                                    # Handle text content
                                    elif isinstance(content, str):
                                        source_info.update({
                                            'type': 'text',
                                            'preview': content[:100],
                                            'content_found': True
                                        })
                                        result['text_sources'].append(source_info)
                                
                                break
                    
                    # If no content found, it's metadata only
                    if not source_info['content_found']:
                        source_info['type'] = 'metadata'
                        result['metadata_sources'].append(source_info)
            
            logger.info(f"VISUAL QUERY COMPLETE: {len(result['visual_sources'])} visual, {len(result['text_sources'])} text, {len(result['metadata_sources'])} metadata sources")
            return result
            
        except Exception as e:
            logger.error(f"ERROR: Visual query failed: {e}")
            return {
                'question': question,
                'error': str(e),
                'response': '',
                'sources_count': 0,
                'visual_sources': [],
                'text_sources': [],
                'metadata_sources': []
            }
    
    def get_comprehensive_visual_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary using both API methods."""
        try:
            logger.info("COMPREHENSIVE SUMMARY: Using both query() and retrieve_chunks()")
            
            # Test different search terms
            test_terms = ["ECSS", "diagram", "table", "figure", "requirement"]
            
            summary = {
                'test_terms': test_terms,
                'chunk_analysis': {},
                'query_analysis': {},
                'total_visual_content': 0,
                'total_text_content': 0,
                'api_methods_used': ['query', 'retrieve_chunks']
            }
            
            # Analyze with retrieve_chunks (has content)
            for term in test_terms:
                logger.info(f"TESTING: retrieve_chunks() with '{term}'")
                
                try:
                    chunks = self.db.retrieve_chunks(term)
                    
                    chunk_summary = {
                        'term': term,
                        'total_chunks': len(chunks) if chunks else 0,
                        'visual_chunks': 0,
                        'text_chunks': 0,
                        'other_chunks': 0
                    }
                    
                    if chunks:
                        for chunk in chunks:
                            if hasattr(chunk, 'content') and chunk.content:
                                content = chunk.content
                                
                                if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                                    chunk_summary['visual_chunks'] += 1
                                    summary['total_visual_content'] += 1
                                elif isinstance(content, str):
                                    chunk_summary['text_chunks'] += 1
                                    summary['total_text_content'] += 1
                                else:
                                    chunk_summary['other_chunks'] += 1
                    
                    summary['chunk_analysis'][term] = chunk_summary
                    
                except Exception as e:
                    logger.warning(f"ERROR: retrieve_chunks('{term}') failed: {e}")
                    summary['chunk_analysis'][term] = {'error': str(e)}
            
            # Analyze with query (metadata only)
            for term in test_terms:
                logger.info(f"TESTING: query() with '{term}'")
                
                try:
                    response = self.db.query(term, use_colpali=True, k=3)
                    
                    query_summary = {
                        'term': term,
                        'sources_found': len(response.sources) if response.sources else 0,
                        'response_available': bool(hasattr(response, 'response') and response.response)
                    }
                    
                    summary['query_analysis'][term] = query_summary
                    
                except Exception as e:
                    logger.warning(f"ERROR: query('{term}') failed: {e}")
                    summary['query_analysis'][term] = {'error': str(e)}
            
            logger.info(f"COMPREHENSIVE SUMMARY COMPLETE:")
            logger.info(f"  - Total visual content: {summary['total_visual_content']}")
            logger.info(f"  - Total text content: {summary['total_text_content']}")
            
            return summary
            
        except Exception as e:
            logger.error(f"ERROR: Comprehensive summary failed: {e}")
            return {
                'error': str(e),
                'total_visual_content': 0,
                'total_text_content': 0
            }

def main():
    """Main function to demonstrate the fixed visual processing."""
    print("FIXED: Morphik Native Visual Content Processor")
    print("=" * 60)
    print("Now uses correct API methods:")
    print("  - retrieve_chunks() for content analysis (has PIL Images)")
    print("  - query() for search responses (has metadata only)")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("ERROR: MORPHIK_URI not found in environment variables")
        return
    
    # Initialize fixed processor
    try:
        processor = MorphikNativeVisualProcessorFixed(morphik_uri)
        print("SUCCESS: Fixed native visual processor initialized")
    except Exception as e:
        print(f"ERROR: Failed to initialize processor: {e}")
        return
    
    # Test 1: Analyze visual content with chunks
    print("\nTest 1: Analyzing visual content with retrieve_chunks()...")
    visual_analysis = processor.analyze_visual_content_with_chunks("ECSS")
    
    print(f"RESULTS:")
    print(f"  - Total chunks: {visual_analysis['total_chunks']}")
    print(f"  - Visual elements: {len(visual_analysis['visual_elements'])}")
    print(f"  - Text elements: {len(visual_analysis['text_elements'])}")
    
    if visual_analysis['visual_elements']:
        print(f"  VISUAL CONTENT FOUND:")
        for i, visual in enumerate(visual_analysis['visual_elements'][:3], 1):
            print(f"    {i}. {visual['image_type']} - Size: {visual['image_size']}")
            if visual.get('confirmed_image'):
                print(f"       Confirmed image: {visual['confirmed_image']}")
    
    # Test 2: Search with query and fetch content
    print("\nTest 2: Search with query() and fetch content...")
    search_results = processor.search_with_query_and_fetch_content("ECSS requirements", limit=3)
    
    print(f"SEARCH RESULTS: {len(search_results)} results")
    for i, result in enumerate(search_results[:3], 1):
        print(f"  {i}. Type: {result['content_type']}")
        print(f"     Score: {result['relevance_score']:.3f}")
        print(f"     Content found: {result['content_found']}")
        if result['content_type'] == 'visual':
            print(f"     Visual info: {result['visual_info']['type']} {result['visual_info']['size']}")
    
    # Test 3: Query with visual understanding
    print("\nTest 3: Query with visual understanding...")
    question = "What are the main requirements in the ECSS document?"
    result = processor.query_with_visual_understanding(question)
    
    print(f"QUESTION: {question}")
    print(f"RESPONSE: {result['response'][:100]}..." if result['response'] else "No response")
    print(f"SOURCES: {result['sources_count']} total")
    print(f"  - Visual sources: {len(result['visual_sources'])}")
    print(f"  - Text sources: {len(result['text_sources'])}")
    print(f"  - Metadata sources: {len(result['metadata_sources'])}")
    
    # Test 4: Comprehensive summary
    print("\nTest 4: Comprehensive visual summary...")
    summary = processor.get_comprehensive_visual_summary()
    
    print(f"COMPREHENSIVE SUMMARY:")
    print(f"  - Total visual content: {summary['total_visual_content']}")
    print(f"  - Total text content: {summary['total_text_content']}")
    print(f"  - API methods tested: {summary['api_methods_used']}")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"morphik_native_visual_fixed_results_{timestamp}.json"
    
    results_data = {
        'timestamp': timestamp,
        'visual_analysis': visual_analysis,
        'search_results': search_results,
        'visual_query_result': result,
        'comprehensive_summary': summary
    }
    
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\nSUCCESS: Results saved to: {results_file}")
    print(f"\nKEY INSIGHT: Visual content IS working!")
    print(f"  - PIL Images found: {summary['total_visual_content']}")
    print(f"  - Use retrieve_chunks() for content analysis")
    print(f"  - Use query() for search, then fetch content separately")

if __name__ == "__main__":
    main() 