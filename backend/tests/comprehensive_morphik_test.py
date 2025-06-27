

#!/usr/bin/env python3
"""
Comprehensive Morphik Testing Script
Based on deep analysis of Morphik documentation and current issues.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Comprehensive Morphik Testing Script
Based on deep analysis of Morphik documentation and current issues.
"""

import os
import sys
import json
import time
from typing import Dict, List, Any

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule

class ComprehensiveMorphikTest:
    """Comprehensive testing of Morphik functionality."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.morphik_uri = os.getenv("MORPHIK_URI")
        if not self.morphik_uri:
            raise ValueError("MORPHIK_URI not found in environment")
        
        self.db = Morphik(self.morphik_uri)
        self.test_results = {}
        
    def test_1_basic_connection(self):
        """Test 1: Basic Morphik connection and ping."""
        print("🔌 Test 1: Basic Connection")
        print("=" * 40)
        
        try:
            # Test ping
            ping_result = self.db.ping()
            print(f"✅ Ping successful: {ping_result}")
            
            # Test list documents
            docs = self.db.list_documents()
            print(f"✅ List documents successful: {len(docs)} documents found")
            
            self.test_results['basic_connection'] = True
            return True
            
        except Exception as e:
            print(f"❌ Basic connection failed: {e}")
            self.test_results['basic_connection'] = False
            return False
    
    def test_2_simple_text_ingestion(self):
        """Test 2: Simple text ingestion without rules."""
        print("\n📝 Test 2: Simple Text Ingestion")
        print("=" * 40)
        
        try:
            # Create simple test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            
            Key Requirements:
            1. All requirements shall be traceable
            2. System design shall be documented
            3. Verification shall be planned and executed
            """
            
            # Ingest without rules
            doc = self.db.ingest_text(test_text, filename="test_simple_text.txt")
            print(f"✅ Text ingested successfully: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=60)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check if we can retrieve content
            chunks = self.db.retrieve_chunks(doc.id, query="requirements")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                print(f"  Chunk {i+1}: {chunk.content[:100]}...")
            
            self.test_results['simple_text_ingestion'] = True
            return True
            
        except Exception as e:
            print(f"❌ Simple text ingestion failed: {e}")
            self.test_results['simple_text_ingestion'] = False
            return False
    
    def test_3_simple_metadata_extraction(self):
        """Test 3: Simple metadata extraction with basic schema."""
        print("\n🏷️ Test 3: Simple Metadata Extraction")
        print("=" * 40)
        
        try:
            # Create a simple schema
            from pydantic import BaseModel, Field
            
            class SimpleDocument(BaseModel):
                title: str = Field(description="Document title")
                author: str = Field(description="Document author or organization")
                date: str = Field(description="Publication date")
                summary: str = Field(description="Brief summary of the document")
            
            # Create simple rule
            rule = MetadataExtractionRule(schema=SimpleDocument)
            
            # Create test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            """
            
            # Ingest with rule
            doc = self.db.ingest_text(
                test_text, 
                filename="test_metadata.txt",
                rules=[rule]
            )
            print(f"✅ Text ingested with metadata rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=120)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata extracted: {doc.metadata}")
            else:
                print("❌ No metadata found")
                
            # Re-fetch document
            refetched = self.db.get_document(doc.id)
            if hasattr(refetched, 'metadata') and refetched.metadata:
                print(f"✅ Re-fetched metadata: {refetched.metadata}")
            else:
                print("❌ No metadata in re-fetched document")
            
            self.test_results['simple_metadata_extraction'] = True
            return True
            
        except Exception as e:
            print(f"❌ Simple metadata extraction failed: {e}")
            self.test_results['simple_metadata_extraction'] = False
            return False
    
    def test_4_natural_language_rule(self):
        """Test 4: Natural language rule for content transformation."""
        print("\n💬 Test 4: Natural Language Rule")
        print("=" * 40)
        
        try:
            # Create natural language rule
            rule = NaturalLanguageRule(
                prompt="""Extract the following information from this document and format as JSON:
                {
                    "title": "Document title",
                    "organization": "Publishing organization", 
                    "date": "Publication date",
                    "main_topics": ["topic1", "topic2"],
                    "key_requirements": ["requirement1", "requirement2"]
                }"""
            )
            
            # Create test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            
            Key Requirements:
            1. All requirements shall be traceable
            2. System design shall be documented
            3. Verification shall be planned and executed
            """
            
            # Ingest with natural language rule
            doc = self.db.ingest_text(
                test_text,
                filename="test_nl_rule.txt",
                rules=[rule]
            )
            print(f"✅ Text ingested with NL rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=120)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check for transformed content
            chunks = self.db.retrieve_chunks(doc.id, query="requirements")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                print(f"  Chunk {i+1}: {chunk.content[:200]}...")
            
            self.test_results['natural_language_rule'] = True
            return True
            
        except Exception as e:
            print(f"❌ Natural language rule failed: {e}")
            self.test_results['natural_language_rule'] = False
            return False
    
    def test_5_pdf_processing(self):
        """Test 5: PDF processing without rules."""
        print("\n📄 Test 5: PDF Processing")
        print("=" * 40)
        
        try:
            # Find a small PDF file
            pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
            pdf_files = list(pdf_dir.glob("*.pdf"))
            
            if not pdf_files:
                print("❌ No PDF files found")
                self.test_results['pdf_processing'] = False
                return False
            
            # Use the smallest PDF
            test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
            print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f}KB)")
            
            # Ingest without rules
            doc = self.db.ingest_file(test_pdf, filename=f"test_pdf_{test_pdf.name}")
            print(f"✅ PDF ingested: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=300)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check if content was extracted
            chunks = self.db.retrieve_chunks(doc.id, query="ECSS")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            if chunks:
                for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                    content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                    print(f"  Chunk {i+1}: {content[:200]}...")
            else:
                print("❌ No chunks found - PDF may not have been processed correctly")
            
            self.test_results['pdf_processing'] = True
            return True
            
        except Exception as e:
            print(f"❌ PDF processing failed: {e}")
            self.test_results['pdf_processing'] = False
            return False
    
    def test_6_pdf_with_metadata_rules(self):
        """Test 6: PDF processing with metadata rules."""
        print("\n📄🏷️ Test 6: PDF with Metadata Rules")
        print("=" * 40)
        
        try:
            # Create simple schema for PDF
            from pydantic import BaseModel, Field
            
            class PDFDocument(BaseModel):
                title: str = Field(description="Document title")
                standard_id: str = Field(description="ECSS standard identifier")
                revision: str = Field(description="Revision number")
                date: str = Field(description="Publication date")
                summary: str = Field(description="Brief summary")
            
            # Create rule
            rule = MetadataExtractionRule(schema=PDFDocument)
            
            # Find a small PDF
            pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
            pdf_files = list(pdf_dir.glob("*.pdf"))
            
            if not pdf_files:
                print("❌ No PDF files found")
                self.test_results['pdf_with_metadata_rules'] = False
                return False
            
            test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
            print(f"📄 Testing with: {test_pdf.name}")
            
            # Ingest with rule
            doc = self.db.ingest_file(
                test_pdf,
                filename=f"test_pdf_metadata_{test_pdf.name}",
                rules=[rule]
            )
            print(f"✅ PDF ingested with metadata rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=300)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata extracted: {doc.metadata}")
            else:
                print("❌ No metadata found")
                
            # Re-fetch and check
            refetched = self.db.get_document(doc.id)
            if hasattr(refetched, 'metadata') and refetched.metadata:
                print(f"✅ Re-fetched metadata: {refetched.metadata}")
            else:
                print("❌ No metadata in re-fetched document")
            
            self.test_results['pdf_with_metadata_rules'] = True
            return True
            
        except Exception as e:
            print(f"❌ PDF with metadata rules failed: {e}")
            self.test_results['pdf_with_metadata_rules'] = False
            return False
    
    def test_7_workflow_status(self):
        """Test 7: Check workflow status functionality."""
        print("\n⚙️ Test 7: Workflow Status")
        print("=" * 40)
        
        try:
            # Get all documents
            docs = self.db.list_documents()
            print(f"📄 Found {len(docs)} documents")
            
            for i, doc in enumerate(docs[:3]):  # Check first 3 documents
                print(f"\nDocument {i+1}: {getattr(doc, 'filename', 'Unknown')}")
                
                # Get document ID
                doc_id = getattr(doc, 'id', None)
                if not doc_id:
                    print("  ❌ No document ID found")
                    continue
                
                # Check workflow status
                try:
                    status = self.db.check_workflow_status(doc_id)
                    print(f"  ✅ Workflow status: {status}")
                except Exception as e:
                    print(f"  ❌ Error checking workflow status: {e}")
                
                # Check document status
                try:
                    doc_status = self.db.get_document_status(doc_id)
                    print(f"  ✅ Document status: {doc_status}")
                except Exception as e:
                    print(f"  ❌ Error checking document status: {e}")
            
            self.test_results['workflow_status'] = True
            return True
            
        except Exception as e:
            print(f"❌ Workflow status test failed: {e}")
            self.test_results['workflow_status'] = False
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("🚀 Starting Comprehensive Morphik Testing")
        print("=" * 60)
        
        tests = [
            self.test_1_basic_connection,
            self.test_2_simple_text_ingestion,
            self.test_3_simple_metadata_extraction,
            self.test_4_natural_language_rule,
            self.test_5_pdf_processing,
            self.test_6_pdf_with_metadata_rules,
            self.test_7_workflow_status
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(2)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n📊 Test Report")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"comprehensive_test_results_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100
                },
                'detailed_results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")

def main():
    """Main test execution."""
    try:
        tester = ComprehensiveMorphikTest()
        tester.run_all_tests()
    except Exception as e:
        print(f"❌ Test suite failed to initialize: {e}")

if __name__ == "__main__":
    main()


import os
import sys
import json
import time
from typing import Dict, List, Any

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule

class ComprehensiveMorphikTest:
    """Comprehensive testing of Morphik functionality."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.morphik_uri = os.getenv("MORPHIK_URI")
        if not self.morphik_uri:
            raise ValueError("MORPHIK_URI not found in environment")
        
        self.db = Morphik(self.morphik_uri)
        self.test_results = {}
        
    def test_1_basic_connection(self):
        """Test 1: Basic Morphik connection and ping."""
        print("🔌 Test 1: Basic Connection")
        print("=" * 40)
        
        try:
            # Test ping
            ping_result = self.db.ping()
            print(f"✅ Ping successful: {ping_result}")
            
            # Test list documents
            docs = self.db.list_documents()
            print(f"✅ List documents successful: {len(docs)} documents found")
            
            self.test_results['basic_connection'] = True
            return True
            
        except Exception as e:
            print(f"❌ Basic connection failed: {e}")
            self.test_results['basic_connection'] = False
            return False
    
    def test_2_simple_text_ingestion(self):
        """Test 2: Simple text ingestion without rules."""
        print("\n📝 Test 2: Simple Text Ingestion")
        print("=" * 40)
        
        try:
            # Create simple test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            
            Key Requirements:
            1. All requirements shall be traceable
            2. System design shall be documented
            3. Verification shall be planned and executed
            """
            
            # Ingest without rules
            doc = self.db.ingest_text(test_text, filename="test_simple_text.txt")
            print(f"✅ Text ingested successfully: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=60)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check if we can retrieve content
            chunks = self.db.retrieve_chunks(doc.id, query="requirements")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                print(f"  Chunk {i+1}: {chunk.content[:100]}...")
            
            self.test_results['simple_text_ingestion'] = True
            return True
            
        except Exception as e:
            print(f"❌ Simple text ingestion failed: {e}")
            self.test_results['simple_text_ingestion'] = False
            return False
    
    def test_3_simple_metadata_extraction(self):
        """Test 3: Simple metadata extraction with basic schema."""
        print("\n🏷️ Test 3: Simple Metadata Extraction")
        print("=" * 40)
        
        try:
            # Create a simple schema
            from pydantic import BaseModel, Field
            
            class SimpleDocument(BaseModel):
                title: str = Field(description="Document title")
                author: str = Field(description="Document author or organization")
                date: str = Field(description="Publication date")
                summary: str = Field(description="Brief summary of the document")
            
            # Create simple rule
            rule = MetadataExtractionRule(schema=SimpleDocument)
            
            # Create test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            """
            
            # Ingest with rule
            doc = self.db.ingest_text(
                test_text, 
                filename="test_metadata.txt",
                rules=[rule]
            )
            print(f"✅ Text ingested with metadata rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=120)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata extracted: {doc.metadata}")
            else:
                print("❌ No metadata found")
                
            # Re-fetch document
            refetched = self.db.get_document(doc.id)
            if hasattr(refetched, 'metadata') and refetched.metadata:
                print(f"✅ Re-fetched metadata: {refetched.metadata}")
            else:
                print("❌ No metadata in re-fetched document")
            
            self.test_results['simple_metadata_extraction'] = True
            return True
            
        except Exception as e:
            print(f"❌ Simple metadata extraction failed: {e}")
            self.test_results['simple_metadata_extraction'] = False
            return False
    
    def test_4_natural_language_rule(self):
        """Test 4: Natural language rule for content transformation."""
        print("\n💬 Test 4: Natural Language Rule")
        print("=" * 40)
        
        try:
            # Create natural language rule
            rule = NaturalLanguageRule(
                prompt="""Extract the following information from this document and format as JSON:
                {
                    "title": "Document title",
                    "organization": "Publishing organization", 
                    "date": "Publication date",
                    "main_topics": ["topic1", "topic2"],
                    "key_requirements": ["requirement1", "requirement2"]
                }"""
            )
            
            # Create test text
            test_text = """
            ECSS-E-ST-10C Rev.1 (15 February 2017)
            European Cooperation for Space Standardization
            Space Engineering - System Engineering General Requirements
            
            This document defines the general requirements for system engineering in space projects.
            It covers requirements management, system design, verification, and validation.
            
            Key Requirements:
            1. All requirements shall be traceable
            2. System design shall be documented
            3. Verification shall be planned and executed
            """
            
            # Ingest with natural language rule
            doc = self.db.ingest_text(
                test_text,
                filename="test_nl_rule.txt",
                rules=[rule]
            )
            print(f"✅ Text ingested with NL rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=120)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check for transformed content
            chunks = self.db.retrieve_chunks(doc.id, query="requirements")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                print(f"  Chunk {i+1}: {chunk.content[:200]}...")
            
            self.test_results['natural_language_rule'] = True
            return True
            
        except Exception as e:
            print(f"❌ Natural language rule failed: {e}")
            self.test_results['natural_language_rule'] = False
            return False
    
    def test_5_pdf_processing(self):
        """Test 5: PDF processing without rules."""
        print("\n📄 Test 5: PDF Processing")
        print("=" * 40)
        
        try:
            # Find a small PDF file
            pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
            pdf_files = list(pdf_dir.glob("*.pdf"))
            
            if not pdf_files:
                print("❌ No PDF files found")
                self.test_results['pdf_processing'] = False
                return False
            
            # Use the smallest PDF
            test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
            print(f"📄 Testing with: {test_pdf.name} ({test_pdf.stat().st_size / 1024:.1f}KB)")
            
            # Ingest without rules
            doc = self.db.ingest_file(test_pdf, filename=f"test_pdf_{test_pdf.name}")
            print(f"✅ PDF ingested: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=300)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check if content was extracted
            chunks = self.db.retrieve_chunks(doc.id, query="ECSS")
            print(f"✅ Retrieved {len(chunks)} chunks")
            
            if chunks:
                for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                    content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                    print(f"  Chunk {i+1}: {content[:200]}...")
            else:
                print("❌ No chunks found - PDF may not have been processed correctly")
            
            self.test_results['pdf_processing'] = True
            return True
            
        except Exception as e:
            print(f"❌ PDF processing failed: {e}")
            self.test_results['pdf_processing'] = False
            return False
    
    def test_6_pdf_with_metadata_rules(self):
        """Test 6: PDF processing with metadata rules."""
        print("\n📄🏷️ Test 6: PDF with Metadata Rules")
        print("=" * 40)
        
        try:
            # Create simple schema for PDF
            from pydantic import BaseModel, Field
            
            class PDFDocument(BaseModel):
                title: str = Field(description="Document title")
                standard_id: str = Field(description="ECSS standard identifier")
                revision: str = Field(description="Revision number")
                date: str = Field(description="Publication date")
                summary: str = Field(description="Brief summary")
            
            # Create rule
            rule = MetadataExtractionRule(schema=PDFDocument)
            
            # Find a small PDF
            pdf_dir = Path("../ECSS Published Standards/1-Active Standards")
            pdf_files = list(pdf_dir.glob("*.pdf"))
            
            if not pdf_files:
                print("❌ No PDF files found")
                self.test_results['pdf_with_metadata_rules'] = False
                return False
            
            test_pdf = min(pdf_files, key=lambda f: f.stat().st_size)
            print(f"📄 Testing with: {test_pdf.name}")
            
            # Ingest with rule
            doc = self.db.ingest_file(
                test_pdf,
                filename=f"test_pdf_metadata_{test_pdf.name}",
                rules=[rule]
            )
            print(f"✅ PDF ingested with metadata rule: {doc.id}")
            
            # Wait for completion
            doc.wait_for_completion(timeout=300)
            print(f"✅ Processing completed: {doc.status}")
            
            # Check metadata
            if hasattr(doc, 'metadata') and doc.metadata:
                print(f"✅ Metadata extracted: {doc.metadata}")
            else:
                print("❌ No metadata found")
                
            # Re-fetch and check
            refetched = self.db.get_document(doc.id)
            if hasattr(refetched, 'metadata') and refetched.metadata:
                print(f"✅ Re-fetched metadata: {refetched.metadata}")
            else:
                print("❌ No metadata in re-fetched document")
            
            self.test_results['pdf_with_metadata_rules'] = True
            return True
            
        except Exception as e:
            print(f"❌ PDF with metadata rules failed: {e}")
            self.test_results['pdf_with_metadata_rules'] = False
            return False
    
    def test_7_workflow_status(self):
        """Test 7: Check workflow status functionality."""
        print("\n⚙️ Test 7: Workflow Status")
        print("=" * 40)
        
        try:
            # Get all documents
            docs = self.db.list_documents()
            print(f"📄 Found {len(docs)} documents")
            
            for i, doc in enumerate(docs[:3]):  # Check first 3 documents
                print(f"\nDocument {i+1}: {getattr(doc, 'filename', 'Unknown')}")
                
                # Get document ID
                doc_id = getattr(doc, 'id', None)
                if not doc_id:
                    print("  ❌ No document ID found")
                    continue
                
                # Check workflow status
                try:
                    status = self.db.check_workflow_status(doc_id)
                    print(f"  ✅ Workflow status: {status}")
                except Exception as e:
                    print(f"  ❌ Error checking workflow status: {e}")
                
                # Check document status
                try:
                    doc_status = self.db.get_document_status(doc_id)
                    print(f"  ✅ Document status: {doc_status}")
                except Exception as e:
                    print(f"  ❌ Error checking document status: {e}")
            
            self.test_results['workflow_status'] = True
            return True
            
        except Exception as e:
            print(f"❌ Workflow status test failed: {e}")
            self.test_results['workflow_status'] = False
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("🚀 Starting Comprehensive Morphik Testing")
        print("=" * 60)
        
        tests = [
            self.test_1_basic_connection,
            self.test_2_simple_text_ingestion,
            self.test_3_simple_metadata_extraction,
            self.test_4_natural_language_rule,
            self.test_5_pdf_processing,
            self.test_6_pdf_with_metadata_rules,
            self.test_7_workflow_status
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(2)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n📊 Test Report")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"comprehensive_test_results_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100
                },
                'detailed_results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")

def main():
    """Main test execution."""
    try:
        tester = ComprehensiveMorphikTest()
        tester.run_all_tests()
    except Exception as e:
        print(f"❌ Test suite failed to initialize: {e}")

if __name__ == "__main__":
    main()
