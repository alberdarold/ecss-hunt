#!/usr/bin/env python3
"""
Enhanced Image Processing System for ECSS Documents
Handles PIL Image objects from ColPali, adds OCR capabilities, and extracts meaningful information.
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
import base64
import io
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np

from morphik import Morphik

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_image_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedImageProcessor:
    """Enhanced image processing system with OCR and visual content analysis."""
    
    def __init__(self, morphik_uri: str):
        """Initialize the enhanced image processor."""
        self.db = Morphik(morphik_uri)
        self.output_dir = Path("enhanced_extracted_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # Validate Morphik connection
        try:
            self.db.list_documents()
            logger.info("✅ Connected to Morphik successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Morphik: {e}")
            raise
    
    def preprocess_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results."""
        try:
            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array for OpenCV processing
            img_array = np.array(image)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding for better text contrast
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Convert back to PIL Image
            processed_image = Image.fromarray(thresh)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(processed_image)
            processed_image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(processed_image)
            processed_image = enhancer.enhance(2.0)
            
            return processed_image
            
        except Exception as e:
            logger.warning(f"⚠️ Image preprocessing failed: {e}")
            return image
    
    def extract_text_from_image(self, image: Image.Image) -> Dict[str, Any]:
        """Extract text from image using OCR with multiple strategies."""
        try:
            # Preprocess image for better OCR
            processed_image = self.preprocess_image_for_ocr(image)
            
            # Try different OCR configurations
            ocr_configs = [
                '--psm 3',  # Fully automatic page segmentation
                '--psm 6',  # Uniform block of text
                '--psm 8',  # Single word
                '--psm 11', # Sparse text
                '--psm 13'  # Raw line
            ]
            
            best_text = ""
            best_confidence = 0
            text_details = []
            
            for config in ocr_configs:
                try:
                    # Extract text with confidence scores
                    data = pytesseract.image_to_data(
                        processed_image, 
                        config=config, 
                        output_type=pytesseract.Output.DICT
                    )
                    
                    # Extract text with confidence
                    text_parts = []
                    confidences = []
                    
                    for i in range(len(data['text'])):
                        if int(data['conf'][i]) > 30:  # Filter low confidence
                            text = data['text'][i].strip()
                            if text:
                                text_parts.append(text)
                                confidences.append(int(data['conf'][i]))
                    
                    if text_parts:
                        extracted_text = ' '.join(text_parts)
                        avg_confidence = sum(confidences) / len(confidences)
                        
                        if avg_confidence > best_confidence:
                            best_text = extracted_text
                            best_confidence = avg_confidence
                        
                        text_details.append({
                            'config': config,
                            'text': extracted_text,
                            'confidence': avg_confidence,
                            'word_count': len(text_parts)
                        })
                
                except Exception as e:
                    logger.warning(f"OCR config {config} failed: {e}")
                    continue
            
            # Also try simple text extraction as fallback
            if not best_text:
                try:
                    simple_text = pytesseract.image_to_string(processed_image)
                    if simple_text.strip():
                        best_text = simple_text.strip()
                        best_confidence = 50  # Assume moderate confidence
                        text_details.append({
                            'config': 'simple',
                            'text': best_text,
                            'confidence': best_confidence,
                            'word_count': len(best_text.split())
                        })
                except Exception as e:
                    logger.warning(f"Simple OCR failed: {e}")
            
            return {
                'extracted_text': best_text,
                'confidence': best_confidence,
                'text_details': text_details,
                'has_text': len(best_text.strip()) > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Text extraction failed: {e}")
            return {
                'extracted_text': '',
                'confidence': 0,
                'text_details': [],
                'has_text': False
            }
    
    def analyze_visual_content(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze visual content to determine type and characteristics."""
        try:
            width, height = image.size
            aspect_ratio = width / height
            
            # Convert to numpy for analysis
            img_array = np.array(image)
            
            # Analyze color distribution
            if len(img_array.shape) == 3:
                # Color image
                avg_color = np.mean(img_array, axis=(0, 1))
                color_variance = np.var(img_array, axis=(0, 1))
                is_grayscale = np.allclose(avg_color, avg_color[0], atol=10)
            else:
                # Grayscale image
                avg_color = np.mean(img_array)
                color_variance = np.var(img_array)
                is_grayscale = True
            
            # Detect edges to understand structure
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY) if len(img_array.shape) == 3 else img_array
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Detect lines (might indicate tables or diagrams)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
            line_count = len(lines) if lines is not None else 0
            
            # Analyze content type based on characteristics
            content_type = "unknown"
            if edge_density > 0.1 and line_count > 10:
                content_type = "table_or_diagram"
            elif edge_density > 0.05:
                content_type = "diagram_or_figure"
            elif is_grayscale and edge_density < 0.02:
                content_type = "text_heavy"
            else:
                content_type = "mixed_content"
            
            return {
                'dimensions': {'width': width, 'height': height},
                'aspect_ratio': aspect_ratio,
                'content_type': content_type,
                'edge_density': edge_density,
                'line_count': line_count,
                'is_grayscale': is_grayscale,
                'avg_color': avg_color.tolist() if isinstance(avg_color, np.ndarray) else avg_color,
                'color_variance': color_variance.tolist() if isinstance(color_variance, np.ndarray) else color_variance
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Visual content analysis failed: {e}")
            return {
                'dimensions': {'width': 0, 'height': 0},
                'aspect_ratio': 0,
                'content_type': 'unknown',
                'edge_density': 0,
                'line_count': 0,
                'is_grayscale': False
            }
    
    def process_chunk_content(self, chunk, chunk_index: int) -> Dict[str, Any]:
        """Process a chunk's content, handling both text and visual elements."""
        try:
            result = {
                'chunk_index': chunk_index,
                'chunk_id': getattr(chunk, 'id', f'chunk_{chunk_index}'),
                'content_type': 'unknown',
                'text_content': '',
                'visual_content': None,
                'extracted_text': '',
                'processing_success': False
            }
            
            if not hasattr(chunk, 'content') or not chunk.content:
                result['content_type'] = 'empty'
                return result
            
            content = chunk.content
            
            # Handle PIL Image objects (ColPali visual content)
            if hasattr(content, '__class__') and 'PIL' in str(type(content).__module__):
                logger.info(f"📸 Processing PIL Image object in chunk {chunk_index}")
                
                # Save the image
                image_filename = f"chunk_{chunk_index}_visual.png"
                image_path = self.output_dir / image_filename
                content.save(image_path)
                
                # Analyze visual content
                visual_analysis = self.analyze_visual_content(content)
                
                # Extract text from image
                ocr_result = self.extract_text_from_image(content)
                
                result.update({
                    'content_type': 'visual',
                    'visual_content': {
                        'image_path': str(image_path),
                        'image_filename': image_filename,
                        'analysis': visual_analysis
                    },
                    'extracted_text': ocr_result['extracted_text'],
                    'ocr_confidence': ocr_result['confidence'],
                    'ocr_details': ocr_result['text_details'],
                    'processing_success': True
                })
                
                logger.info(f"✅ Visual content processed: {visual_analysis['content_type']}")
                if ocr_result['has_text']:
                    logger.info(f"📝 Extracted text ({ocr_result['confidence']:.1f}% confidence): {ocr_result['extracted_text'][:100]}...")
                
            # Handle base64 image data
            elif isinstance(content, str) and (content.startswith('data:image/') or content.startswith('iVBORw0KGgo')):
                logger.info(f"🖼️ Processing base64 image data in chunk {chunk_index}")
                
                try:
                    # Decode base64 image
                    if content.startswith('data:image/'):
                        base64_data = content.split(',')[1]
                        mime_type = content.split(';')[0].split(':')[1]
                        ext = 'png' if 'png' in mime_type else 'jpg'
                    else:
                        base64_data = content
                        ext = 'png'
                    
                    # Convert to PIL Image
                    image_data = base64.b64decode(base64_data)
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Save the image
                    image_filename = f"chunk_{chunk_index}_base64.{ext}"
                    image_path = self.output_dir / image_filename
                    image.save(image_path)
                    
                    # Process as visual content
                    visual_analysis = self.analyze_visual_content(image)
                    ocr_result = self.extract_text_from_image(image)
                    
                    result.update({
                        'content_type': 'visual_base64',
                        'visual_content': {
                            'image_path': str(image_path),
                            'image_filename': image_filename,
                            'analysis': visual_analysis
                        },
                        'extracted_text': ocr_result['extracted_text'],
                        'ocr_confidence': ocr_result['confidence'],
                        'ocr_details': ocr_result['text_details'],
                        'processing_success': True
                    })
                    
                    logger.info(f"✅ Base64 image processed: {visual_analysis['content_type']}")
                    if ocr_result['has_text']:
                        logger.info(f"📝 Extracted text ({ocr_result['confidence']:.1f}% confidence): {ocr_result['extracted_text'][:100]}...")
                
                except Exception as e:
                    logger.error(f"❌ Failed to process base64 image: {e}")
                    result['content_type'] = 'visual_base64_failed'
            
            # Handle text content
            elif isinstance(content, str):
                result.update({
                    'content_type': 'text',
                    'text_content': content,
                    'extracted_text': content,  # Text content is already extracted
                    'processing_success': True
                })
                
                logger.info(f"📝 Text content in chunk {chunk_index}: {len(content)} characters")
            
            # Handle other content types
            else:
                result.update({
                    'content_type': 'unknown',
                    'text_content': str(content),
                    'extracted_text': str(content),
                    'processing_success': False
                })
                
                logger.warning(f"⚠️ Unknown content type in chunk {chunk_index}: {type(content)}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to process chunk {chunk_index}: {e}")
            return {
                'chunk_index': chunk_index,
                'content_type': 'error',
                'error': str(e),
                'processing_success': False
            }
    
    def process_all_chunks(self, search_terms: List[str] = None) -> Dict[str, Any]:
        """Process all chunks from ingested documents."""
        logger.info("🔍 Starting comprehensive chunk processing with OCR...")
        
        if not search_terms:
            search_terms = ["", "ECSS", "the", "and", "or", "requirement", "standard"]
        
        all_results = []
        processed_chunks = set()  # Avoid duplicates
        
        start_time = time.time()
        
        for term in search_terms:
            try:
                logger.info(f"📋 Searching for chunks with term: '{term}'")
                chunks = self.db.retrieve_chunks(term)
                
                if not chunks:
                    logger.info(f"   No chunks found for '{term}'")
                    continue
                
                logger.info(f"   Found {len(chunks)} chunks for '{term}'")
                
                for i, chunk in enumerate(chunks):
                    chunk_key = f"{getattr(chunk, 'id', i)}_{term}"
                    
                    if chunk_key not in processed_chunks:
                        processed_chunks.add(chunk_key)
                        result = self.process_chunk_content(chunk, len(all_results))
                        all_results.append(result)
                        
                        # Log progress every 10 chunks
                        if len(all_results) % 10 == 0:
                            logger.info(f"   Processed {len(all_results)} chunks...")
                
            except Exception as e:
                logger.error(f"❌ Error processing chunks for '{term}': {e}")
                continue
        
        processing_time = time.time() - start_time
        
        # Generate summary
        summary = self.generate_processing_summary(all_results, processing_time)
        
        return {
            'total_chunks': len(all_results),
            'processing_time': processing_time,
            'summary': summary,
            'results': all_results
        }
    
    def generate_processing_summary(self, results: List[Dict], processing_time: float) -> Dict[str, Any]:
        """Generate a summary of the processing results."""
        total_chunks = len(results)
        
        # Count different content types
        content_types = {}
        successful_processing = 0
        visual_chunks = 0
        text_chunks = 0
        chunks_with_extracted_text = 0
        total_extracted_text_length = 0
        
        for result in results:
            content_type = result.get('content_type', 'unknown')
            content_types[content_type] = content_types.get(content_type, 0) + 1
            
            if result.get('processing_success', False):
                successful_processing += 1
            
            if content_type in ['visual', 'visual_base64']:
                visual_chunks += 1
            elif content_type == 'text':
                text_chunks += 1
            
            extracted_text = result.get('extracted_text', '')
            if extracted_text and extracted_text.strip():
                chunks_with_extracted_text += 1
                total_extracted_text_length += len(extracted_text)
        
        return {
            'total_chunks': total_chunks,
            'successful_processing': successful_processing,
            'success_rate': (successful_processing / total_chunks * 100) if total_chunks > 0 else 0,
            'content_types': content_types,
            'visual_chunks': visual_chunks,
            'text_chunks': text_chunks,
            'chunks_with_extracted_text': chunks_with_extracted_text,
            'total_extracted_text_length': total_extracted_text_length,
            'avg_extracted_text_length': (total_extracted_text_length / chunks_with_extracted_text) if chunks_with_extracted_text > 0 else 0,
            'processing_time': processing_time,
            'chunks_per_second': (total_chunks / processing_time) if processing_time > 0 else 0
        }
    
    def search_with_enhanced_results(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents with enhanced results that include extracted text from images."""
        logger.info(f"🔍 Enhanced search for: '{query}'")
        
        try:
            chunks = self.db.retrieve_chunks(query)
            
            if not chunks:
                logger.warning(f"No results found for query: '{query}'")
                return []
            
            enhanced_results = []
            
            for i, chunk in enumerate(chunks[:limit]):
                # Process the chunk to extract all possible text
                chunk_result = self.process_chunk_content(chunk, i)
                
                # Create enhanced search result
                enhanced_result = {
                    'chunk_index': i,
                    'relevance_score': getattr(chunk, 'score', 0.0),
                    'document_id': getattr(chunk, 'document_id', 'unknown'),
                    'content_type': chunk_result['content_type'],
                    'original_query': query
                }
                
                # Add text content (either direct or extracted from image)
                if chunk_result['content_type'] in ['visual', 'visual_base64']:
                    enhanced_result.update({
                        'text': chunk_result.get('extracted_text', '[No text extracted]'),
                        'summary': f"Visual content ({chunk_result.get('visual_content', {}).get('analysis', {}).get('content_type', 'unknown')}): {chunk_result.get('extracted_text', 'No text extracted')[:200]}",
                        'type': 'visual_with_ocr',
                        'visual_info': chunk_result.get('visual_content', {}),
                        'ocr_confidence': chunk_result.get('ocr_confidence', 0)
                    })
                else:
                    enhanced_result.update({
                        'text': chunk_result.get('text_content', ''),
                        'summary': chunk_result.get('text_content', '')[:200] + "..." if len(chunk_result.get('text_content', '')) > 200 else chunk_result.get('text_content', ''),
                        'type': 'text_content'
                    })
                
                enhanced_results.append(enhanced_result)
            
            logger.info(f"✅ Generated {len(enhanced_results)} enhanced search results")
            return enhanced_results
            
        except Exception as e:
            logger.error(f"❌ Enhanced search failed: {e}")
            return []

def main():
    """Main function to test the enhanced image processor."""
    print("🚀 Enhanced Image Processing System for ECSS Documents")
    print("=" * 60)
    
    # Get Morphik URI
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    # Initialize processor
    try:
        processor = EnhancedImageProcessor(morphik_uri)
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return
    
    print("✅ Enhanced Image Processor initialized successfully")
    
    # Process all chunks
    print("\n🔄 Processing all chunks with OCR and visual analysis...")
    results = processor.process_all_chunks()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"enhanced_image_processing_results_{timestamp}.json"
    
    # Create serializable results
    serializable_results = {
        'timestamp': timestamp,
        'total_chunks': results['total_chunks'],
        'processing_time': results['processing_time'],
        'summary': results['summary'],
        'results': [
            {k: v for k, v in result.items() if k != 'visual_content' or isinstance(v, (str, int, float, bool, list, dict, type(None)))}
            for result in results['results']
        ]
    }
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    # Print summary
    summary = results['summary']
    print(f"\n📊 Processing Summary:")
    print(f"   Total chunks: {summary['total_chunks']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    print(f"   Visual chunks: {summary['visual_chunks']}")
    print(f"   Text chunks: {summary['text_chunks']}")
    print(f"   Chunks with extracted text: {summary['chunks_with_extracted_text']}")
    print(f"   Total extracted text: {summary['total_extracted_text_length']} characters")
    print(f"   Processing time: {summary['processing_time']:.1f}s")
    print(f"   Speed: {summary['chunks_per_second']:.1f} chunks/sec")
    
    print(f"\n💾 Results saved to: {results_file}")
    print(f"🖼️  Images saved to: {processor.output_dir}")
    
    # Test enhanced search
    print(f"\n🔍 Testing enhanced search capabilities...")
    test_queries = [
        "ECSS requirements",
        "verification procedures",
        "space engineering standards"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Query: '{query}'")
        search_results = processor.search_with_enhanced_results(query, limit=3)
        
        if search_results:
            for i, result in enumerate(search_results, 1):
                print(f"   📄 Result {i} ({result['type']}):")
                print(f"      Score: {result['relevance_score']:.3f}")
                print(f"      Summary: {result['summary'][:100]}...")
                if result['type'] == 'visual_with_ocr':
                    print(f"      OCR Confidence: {result.get('ocr_confidence', 0):.1f}%")
        else:
            print("   ❌ No results found")

if __name__ == "__main__":
    main() 