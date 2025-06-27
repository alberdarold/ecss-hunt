

#!/usr/bin/env python3
"""
Script to extract and save images that Morphik is finding from PDFs.
This will help us understand what Morphik is actually extracting.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Script to extract and save images that Morphik is finding from PDFs.
This will help us understand what Morphik is actually extracting.
"""

import os
import sys
import base64

# Load environment variables

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def extract_morphik_images():
    """Extract and save images that Morphik is finding from PDFs."""
    print("🖼️  Extracting Morphik Images")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents")
    
    if not documents:
        print("❌ No documents found")
        return
    
    # Create output directory for images
    output_dir = Path("extracted_images")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Images will be saved to: {output_dir.absolute()}")
    
    # Test with the first document
    doc = documents[0]
    print(f"\n🔍 Analyzing document: {doc.filename}")
    print(f"   Document ID: {doc.external_id}")
    
    # Search for a common term to get chunks
    test_term = "the"
    print(f"\n📝 Searching for '{test_term}' to get chunks...")
    
    try:
        chunks = db.retrieve_chunks(test_term)
        print(f"Found {len(chunks)} chunks")
        
        image_count = 0
        text_count = 0
        
        for i, chunk in enumerate(chunks):
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                
                if isinstance(content, str) and len(content) > 20:
                    # Check if this is an image
                    if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                        image_count += 1
                        print(f"\n🖼️  Found image in chunk {i+1}")
                        print(f"   Content length: {len(content)} characters")
                        
                        # Extract image format
                        if content.startswith('data:image/'):
                            # Extract MIME type
                            mime_type = content.split(';')[0].split(':')[1]
                            print(f"   MIME type: {mime_type}")
                            
                            # Determine file extension
                            if 'png' in mime_type:
                                ext = 'png'
                            elif 'jpeg' in mime_type or 'jpg' in mime_type:
                                ext = 'jpg'
                            elif 'gif' in mime_type:
                                ext = 'gif'
                            else:
                                ext = 'bin'
                        else:
                            # PNG signature
                            ext = 'png'
                            mime_type = 'image/png'
                        
                        # Save the image
                        try:
                            # Extract base64 data
                            if content.startswith('data:image/'):
                                # Remove data URL prefix
                                base64_data = content.split(',')[1]
                            else:
                                # Direct base64 data
                                base64_data = content
                            
                            # Decode base64
                            image_data = base64.b64decode(base64_data)
                            
                            # Save to file
                            filename = f"chunk_{i+1}_doc_{doc.external_id[:8]}.{ext}"
                            filepath = output_dir / filename
                            
                            with open(filepath, 'wb') as f:
                                f.write(image_data)
                            
                            print(f"   ✅ Saved as: {filename}")
                            print(f"   📏 File size: {len(image_data)} bytes")
                            
                        except Exception as e:
                            print(f"   ❌ Failed to save image: {e}")
                    
                    else:
                        text_count += 1
                        print(f"\n📄 Found text in chunk {i+1}")
                        print(f"   Content length: {len(content)} characters")
                        print(f"   Preview: {content[:200]}...")
        
        print(f"\n📊 Summary:")
        print(f"   Images found: {image_count}")
        print(f"   Text chunks: {text_count}")
        print(f"   Total chunks: {len(chunks)}")
        
        if image_count > 0:
            print(f"\n🖼️  Images saved to: {output_dir.absolute()}")
            print("   You can now open these images to see what Morphik extracted.")
        else:
            print("\n❌ No images found in chunks")
        
    except Exception as e:
        print(f"❌ Error retrieving chunks: {e}")

def analyze_image_content():
    """Analyze what's in the extracted images."""
    output_dir = Path("extracted_images")
    
    if not output_dir.exists():
        print("❌ No extracted images directory found. Run extract_morphik_images() first.")
        return
    
    image_files = list(output_dir.glob("*"))
    if not image_files:
        print("❌ No image files found in extracted_images directory.")
        return
    
    print(f"\n🔍 Analyzing {len(image_files)} extracted images:")
    
    for i, image_file in enumerate(image_files, 1):
        file_size = image_file.stat().st_size
        print(f"   {i}. {image_file.name}")
        print(f"      Size: {file_size} bytes ({file_size/1024:.1f}KB)")
        print(f"      Type: {image_file.suffix}")

if __name__ == "__main__":
    extract_morphik_images()
    analyze_image_content() 

import os
import sys
import base64

# Load environment variables

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik

def extract_morphik_images():
    """Extract and save images that Morphik is finding from PDFs."""
    print("🖼️  Extracting Morphik Images")
    print("=" * 40)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment")
        return
    
    db = Morphik(morphik_uri)
    
    # Get all documents
    documents = db.list_documents()
    print(f"📄 Found {len(documents)} documents")
    
    if not documents:
        print("❌ No documents found")
        return
    
    # Create output directory for images
    output_dir = Path("extracted_images")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Images will be saved to: {output_dir.absolute()}")
    
    # Test with the first document
    doc = documents[0]
    print(f"\n🔍 Analyzing document: {doc.filename}")
    print(f"   Document ID: {doc.external_id}")
    
    # Search for a common term to get chunks
    test_term = "the"
    print(f"\n📝 Searching for '{test_term}' to get chunks...")
    
    try:
        chunks = db.retrieve_chunks(test_term)
        print(f"Found {len(chunks)} chunks")
        
        image_count = 0
        text_count = 0
        
        for i, chunk in enumerate(chunks):
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                
                if isinstance(content, str) and len(content) > 20:
                    # Check if this is an image
                    if content.startswith('data:image/') or content.startswith('iVBORw0KGgo'):
                        image_count += 1
                        print(f"\n🖼️  Found image in chunk {i+1}")
                        print(f"   Content length: {len(content)} characters")
                        
                        # Extract image format
                        if content.startswith('data:image/'):
                            # Extract MIME type
                            mime_type = content.split(';')[0].split(':')[1]
                            print(f"   MIME type: {mime_type}")
                            
                            # Determine file extension
                            if 'png' in mime_type:
                                ext = 'png'
                            elif 'jpeg' in mime_type or 'jpg' in mime_type:
                                ext = 'jpg'
                            elif 'gif' in mime_type:
                                ext = 'gif'
                            else:
                                ext = 'bin'
                        else:
                            # PNG signature
                            ext = 'png'
                            mime_type = 'image/png'
                        
                        # Save the image
                        try:
                            # Extract base64 data
                            if content.startswith('data:image/'):
                                # Remove data URL prefix
                                base64_data = content.split(',')[1]
                            else:
                                # Direct base64 data
                                base64_data = content
                            
                            # Decode base64
                            image_data = base64.b64decode(base64_data)
                            
                            # Save to file
                            filename = f"chunk_{i+1}_doc_{doc.external_id[:8]}.{ext}"
                            filepath = output_dir / filename
                            
                            with open(filepath, 'wb') as f:
                                f.write(image_data)
                            
                            print(f"   ✅ Saved as: {filename}")
                            print(f"   📏 File size: {len(image_data)} bytes")
                            
                        except Exception as e:
                            print(f"   ❌ Failed to save image: {e}")
                    
                    else:
                        text_count += 1
                        print(f"\n📄 Found text in chunk {i+1}")
                        print(f"   Content length: {len(content)} characters")
                        print(f"   Preview: {content[:200]}...")
        
        print(f"\n📊 Summary:")
        print(f"   Images found: {image_count}")
        print(f"   Text chunks: {text_count}")
        print(f"   Total chunks: {len(chunks)}")
        
        if image_count > 0:
            print(f"\n🖼️  Images saved to: {output_dir.absolute()}")
            print("   You can now open these images to see what Morphik extracted.")
        else:
            print("\n❌ No images found in chunks")
        
    except Exception as e:
        print(f"❌ Error retrieving chunks: {e}")

def analyze_image_content():
    """Analyze what's in the extracted images."""
    output_dir = Path("extracted_images")
    
    if not output_dir.exists():
        print("❌ No extracted images directory found. Run extract_morphik_images() first.")
        return
    
    image_files = list(output_dir.glob("*"))
    if not image_files:
        print("❌ No image files found in extracted_images directory.")
        return
    
    print(f"\n🔍 Analyzing {len(image_files)} extracted images:")
    
    for i, image_file in enumerate(image_files, 1):
        file_size = image_file.stat().st_size
        print(f"   {i}. {image_file.name}")
        print(f"      Size: {file_size} bytes ({file_size/1024:.1f}KB)")
        print(f"      Type: {image_file.suffix}")

if __name__ == "__main__":
    extract_morphik_images()
    analyze_image_content() 