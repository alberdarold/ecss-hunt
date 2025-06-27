

#!/usr/bin/env python3
"""
Debug script to test PDF text extraction.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Debug script to test PDF text extraction.
"""

import os
import sys

# Load environment variables

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

def test_pdf_text_extraction():
    """Test PDF text extraction using different methods."""
    print("🔍 Testing PDF Text Extraction")
    print("=" * 40)
    
    # Test with a small PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Find a small PDF file
    small_pdfs = []
    for pdf_file in pdf_files:
        file_size_kb = pdf_file.stat().st_size / 1024
        if file_size_kb < 300:
            small_pdfs.append((pdf_file, file_size_kb))
    
    if not small_pdfs:
        print("❌ No small PDF files found")
        return
    
    test_pdf, size_kb = small_pdfs[0]
    print(f"📄 Testing with: {test_pdf.name} ({size_kb:.1f}KB)")
    
    # Method 1: Try PyPDF2
    try:
        import PyPDF2
        print("\n1. Testing PyPDF2 extraction:")
        
        with open(test_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num, page in enumerate(reader.pages[:3]):  # First 3 pages
                page_text = page.extract_text()
                if page_text.strip():
                    text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            if text_content.strip():
                print(f"✅ PyPDF2 extracted {len(text_content)} characters")
                preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
                print(f"   Preview: {preview}")
            else:
                print("❌ PyPDF2 extracted no text content")
                
    except ImportError:
        print("❌ PyPDF2 not installed")
    except Exception as e:
        print(f"❌ PyPDF2 error: {e}")
    
    # Method 2: Try pdfplumber
    try:
        import pdfplumber
        print("\n2. Testing pdfplumber extraction:")
        
        with pdfplumber.open(test_pdf) as pdf:
            text_content = ""
            
            for page_num, page in enumerate(pdf.pages[:3]):  # First 3 pages
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            if text_content.strip():
                print(f"✅ pdfplumber extracted {len(text_content)} characters")
                preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
                print(f"   Preview: {preview}")
            else:
                print("❌ pdfplumber extracted no text content")
                
    except ImportError:
        print("❌ pdfplumber not installed")
    except Exception as e:
        print(f"❌ pdfplumber error: {e}")
    
    # Method 3: Try pymupdf (fitz)
    try:
        import fitz  # PyMuPDF
        print("\n3. Testing PyMuPDF extraction:")
        
        doc = fitz.open(test_pdf)
        text_content = ""
        
        for page_num in range(min(3, len(doc))):  # First 3 pages
            page = doc[page_num]
            page_text = page.get_text()
            if page_text and page_text.strip():
                text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        doc.close()
        
        if text_content.strip():
            print(f"✅ PyMuPDF extracted {len(text_content)} characters")
            preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
            print(f"   Preview: {preview}")
        else:
            print("❌ PyMuPDF extracted no text content")
            
    except ImportError:
        print("❌ PyMuPDF not installed")
    except Exception as e:
        print(f"❌ PyMuPDF error: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   PDF file: {test_pdf.name}")
    print(f"   File size: {size_kb:.1f}KB")
    print(f"   This will help determine if the PDF contains extractable text")

if __name__ == "__main__":
    test_pdf_text_extraction() 

import os
import sys

# Load environment variables

# Add backend directory to path
sys.path.insert(0, str(backend_dir.parent))

def test_pdf_text_extraction():
    """Test PDF text extraction using different methods."""
    print("🔍 Testing PDF Text Extraction")
    print("=" * 40)
    
    # Test with a small PDF file
    pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Find a small PDF file
    small_pdfs = []
    for pdf_file in pdf_files:
        file_size_kb = pdf_file.stat().st_size / 1024
        if file_size_kb < 300:
            small_pdfs.append((pdf_file, file_size_kb))
    
    if not small_pdfs:
        print("❌ No small PDF files found")
        return
    
    test_pdf, size_kb = small_pdfs[0]
    print(f"📄 Testing with: {test_pdf.name} ({size_kb:.1f}KB)")
    
    # Method 1: Try PyPDF2
    try:
        import PyPDF2
        print("\n1. Testing PyPDF2 extraction:")
        
        with open(test_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num, page in enumerate(reader.pages[:3]):  # First 3 pages
                page_text = page.extract_text()
                if page_text.strip():
                    text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            if text_content.strip():
                print(f"✅ PyPDF2 extracted {len(text_content)} characters")
                preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
                print(f"   Preview: {preview}")
            else:
                print("❌ PyPDF2 extracted no text content")
                
    except ImportError:
        print("❌ PyPDF2 not installed")
    except Exception as e:
        print(f"❌ PyPDF2 error: {e}")
    
    # Method 2: Try pdfplumber
    try:
        import pdfplumber
        print("\n2. Testing pdfplumber extraction:")
        
        with pdfplumber.open(test_pdf) as pdf:
            text_content = ""
            
            for page_num, page in enumerate(pdf.pages[:3]):  # First 3 pages
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            if text_content.strip():
                print(f"✅ pdfplumber extracted {len(text_content)} characters")
                preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
                print(f"   Preview: {preview}")
            else:
                print("❌ pdfplumber extracted no text content")
                
    except ImportError:
        print("❌ pdfplumber not installed")
    except Exception as e:
        print(f"❌ pdfplumber error: {e}")
    
    # Method 3: Try pymupdf (fitz)
    try:
        import fitz  # PyMuPDF
        print("\n3. Testing PyMuPDF extraction:")
        
        doc = fitz.open(test_pdf)
        text_content = ""
        
        for page_num in range(min(3, len(doc))):  # First 3 pages
            page = doc[page_num]
            page_text = page.get_text()
            if page_text and page_text.strip():
                text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        doc.close()
        
        if text_content.strip():
            print(f"✅ PyMuPDF extracted {len(text_content)} characters")
            preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
            print(f"   Preview: {preview}")
        else:
            print("❌ PyMuPDF extracted no text content")
            
    except ImportError:
        print("❌ PyMuPDF not installed")
    except Exception as e:
        print(f"❌ PyMuPDF error: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   PDF file: {test_pdf.name}")
    print(f"   File size: {size_kb:.1f}KB")
    print(f"   This will help determine if the PDF contains extractable text")

if __name__ == "__main__":
    test_pdf_text_extraction() 