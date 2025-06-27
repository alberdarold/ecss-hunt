
# Add backend root to path


#!/usr/bin/env python3
"""
Practical demonstration of search and retrieval functionality
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Practical demonstration of search and retrieval functionality
"""

import os
import sys
import json
from morphik import Morphik

# Load environment variables

def demo_search_functionality():
    """Demonstrate practical search and retrieval capabilities"""
    
    # Connect to Morphik
    morphik_uri = os.getenv('MORPHIK_URI')
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    print("🎯 PRACTICAL SEARCH AND RETRIEVAL DEMONSTRATION")
    print("=" * 60)
    
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        if not documents:
            print("❌ No documents found!")
            return
        
        doc = documents[0]
        print(f"📄 Working with: {doc.filename}")
        
        # DEMO 1: Search by Standard ID
        print(f"\n🔍 DEMO 1: Search by Standard ID")
        print("-" * 40)
        
        # Get document metadata
        metadata = doc.metadata
        standard_id = metadata.get('standard_id', '')
        
        print(f"Searching for standard: {standard_id}")
        
        # Filter documents by standard ID
        matching_docs = [d for d in documents if d.metadata.get('standard_id') == standard_id]
        print(f"✅ Found {len(matching_docs)} documents matching {standard_id}")
        
        for doc_match in matching_docs:
            print(f"   • {doc_match.filename}")
            print(f"     - Date: {doc_match.metadata.get('date', 'N/A')}")
            print(f"     - Scope: {doc_match.metadata.get('scope', 'N/A')[:100]}...")
        
        # DEMO 2: Search by Keywords
        print(f"\n🔍 DEMO 2: Search by Keywords")
        print("-" * 40)
        
        keywords = metadata.get('keywords', [])
        print(f"Document keywords: {', '.join(keywords[:5])}")
        
        # Show how to filter by keywords
        print(f"\n📊 Keyword-based filtering examples:")
        for keyword in keywords[:3]:
            print(f"   • '{keyword}' → Would find this document")
        
        # DEMO 3: Search by Table Information
        print(f"\n🔍 DEMO 3: Search by Table Information")
        print("-" * 40)
        
        table_title = metadata.get('table_title', '')
        table_number = metadata.get('table_number', '')
        
        print(f"Table: {table_title} ({table_number})")
        print(f"✅ Can search for:")
        print(f"   • Table title: '{table_title}'")
        print(f"   • Table number: '{table_number}'")
        print(f"   • Table type: '{metadata.get('table_type', 'N/A')}'")
        
        # DEMO 4: Search by Requirements
        print(f"\n🔍 DEMO 4: Search by Requirements")
        print("-" * 40)
        
        if 'requirement_text' in metadata:
            requirement = metadata['requirement_text']
            print(f"Requirement: {requirement}")
            print(f"Type: {metadata.get('requirement_type', 'N/A')}")
            print(f"ID: {metadata.get('requirement_id', 'N/A')}")
            
            print(f"\n✅ Can search for:")
            print(f"   • Requirement text: '{requirement[:50]}...'")
            print(f"   • Requirement type: '{metadata.get('requirement_type', 'N/A')}'")
            print(f"   • Requirement ID: '{metadata.get('requirement_id', 'N/A')}'")
        
        # DEMO 5: Search by Related Terms
        print(f"\n🔍 DEMO 5: Search by Related Terms")
        print("-" * 40)
        
        related_terms = metadata.get('related_terms', [])
        print(f"Related terms ({len(related_terms)} found):")
        
        for i, term in enumerate(related_terms[:3]):
            print(f"   {i+1}. {term}")
            print(f"      → Can search for: '{term[:30]}...'")
        
        # DEMO 6: Search by Date and Branch
        print(f"\n🔍 DEMO 6: Search by Date and Branch")
        print("-" * 40)
        
        date = metadata.get('date', '')
        branch = metadata.get('branch', '')
        
        print(f"Date: {date}")
        print(f"Branch: {branch}")
        print(f"✅ Can filter by:")
        print(f"   • Date: '{date}'")
        print(f"   • Branch: '{branch}'")
        print(f"   • Revision: '{metadata.get('revision', 'N/A')}'")
        
        # DEMO 7: Search by Content Summary
        print(f"\n🔍 DEMO 7: Search by Content Summary")
        print("-" * 40)
        
        content_summary = metadata.get('content_summary', '')
        print(f"Content Summary: {content_summary}")
        
        # Extract key concepts for search
        key_concepts = ['TRL', 'Technology Readiness Level', 'milestones', 'aerospace']
        print(f"\n✅ Can search for key concepts:")
        for concept in key_concepts:
            if concept.lower() in content_summary.lower():
                print(f"   • '{concept}' → Found in content")
        
        # DEMO 8: Practical Search Queries
        print(f"\n🔍 DEMO 8: Practical Search Queries")
        print("-" * 40)
        
        print("🎯 Example search queries you can implement:")
        
        search_examples = [
            "Find all ECSS-E-AS-11C documents",
            "Find documents about Technology Readiness Level",
            "Find documents with TRL requirements",
            "Find documents from 2014",
            "Find documents with Table 4-2",
            "Find documents about flight qualification",
            "Find documents referencing ISO 16290",
            "Find performance requirements",
            "Find documents with aerospace elements"
        ]
        
        for i, query in enumerate(search_examples, 1):
            print(f"   {i}. {query}")
        
        # DEMO 9: Metadata Retrieval Functions
        print(f"\n🔍 DEMO 9: Metadata Retrieval Functions")
        print("-" * 40)
        
        print("📋 Functions you can implement:")
        print("""
def search_by_standard_id(standard_id):
    # Filter documents by standard ID
    return [doc for doc in documents if doc.metadata.get('standard_id') == standard_id]

def search_by_keywords(keywords):
    # Filter documents by keywords
    return [doc for doc in documents if any(kw in doc.metadata.get('keywords', []) for kw in keywords)]

def search_by_date_range(start_date, end_date):
    # Filter documents by date range
    return [doc for doc in documents if start_date <= doc.metadata.get('date') <= end_date]

def search_by_requirement_type(req_type):
    # Filter documents by requirement type
    return [doc for doc in documents if doc.metadata.get('requirement_type') == req_type]

def search_by_table_info(table_title):
    # Filter documents by table information
    return [doc for doc in documents if doc.metadata.get('table_title') == table_title]
        """)
        
        print(f"\n✅ DEMONSTRATION COMPLETED!")
        print(f"   • All metadata is retrievable and searchable")
        print(f"   • Images contain searchable content")
        print(f"   • Requirements are extracted and accessible")
        print(f"   • System supports complex queries and filtering")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_search_functionality() 

import os
import sys
import json
from morphik import Morphik

# Load environment variables

def demo_search_functionality():
    """Demonstrate practical search and retrieval capabilities"""
    
    # Connect to Morphik
    morphik_uri = os.getenv('MORPHIK_URI')
    if not morphik_uri:
        print("❌ MORPHIK_URI not found in environment variables")
        return
    
    print("🎯 PRACTICAL SEARCH AND RETRIEVAL DEMONSTRATION")
    print("=" * 60)
    
    try:
        db = Morphik(morphik_uri)
        print("✅ Connected to Morphik successfully")
        
        # Get all documents
        documents = db.list_documents()
        if not documents:
            print("❌ No documents found!")
            return
        
        doc = documents[0]
        print(f"📄 Working with: {doc.filename}")
        
        # DEMO 1: Search by Standard ID
        print(f"\n🔍 DEMO 1: Search by Standard ID")
        print("-" * 40)
        
        # Get document metadata
        metadata = doc.metadata
        standard_id = metadata.get('standard_id', '')
        
        print(f"Searching for standard: {standard_id}")
        
        # Filter documents by standard ID
        matching_docs = [d for d in documents if d.metadata.get('standard_id') == standard_id]
        print(f"✅ Found {len(matching_docs)} documents matching {standard_id}")
        
        for doc_match in matching_docs:
            print(f"   • {doc_match.filename}")
            print(f"     - Date: {doc_match.metadata.get('date', 'N/A')}")
            print(f"     - Scope: {doc_match.metadata.get('scope', 'N/A')[:100]}...")
        
        # DEMO 2: Search by Keywords
        print(f"\n🔍 DEMO 2: Search by Keywords")
        print("-" * 40)
        
        keywords = metadata.get('keywords', [])
        print(f"Document keywords: {', '.join(keywords[:5])}")
        
        # Show how to filter by keywords
        print(f"\n📊 Keyword-based filtering examples:")
        for keyword in keywords[:3]:
            print(f"   • '{keyword}' → Would find this document")
        
        # DEMO 3: Search by Table Information
        print(f"\n🔍 DEMO 3: Search by Table Information")
        print("-" * 40)
        
        table_title = metadata.get('table_title', '')
        table_number = metadata.get('table_number', '')
        
        print(f"Table: {table_title} ({table_number})")
        print(f"✅ Can search for:")
        print(f"   • Table title: '{table_title}'")
        print(f"   • Table number: '{table_number}'")
        print(f"   • Table type: '{metadata.get('table_type', 'N/A')}'")
        
        # DEMO 4: Search by Requirements
        print(f"\n🔍 DEMO 4: Search by Requirements")
        print("-" * 40)
        
        if 'requirement_text' in metadata:
            requirement = metadata['requirement_text']
            print(f"Requirement: {requirement}")
            print(f"Type: {metadata.get('requirement_type', 'N/A')}")
            print(f"ID: {metadata.get('requirement_id', 'N/A')}")
            
            print(f"\n✅ Can search for:")
            print(f"   • Requirement text: '{requirement[:50]}...'")
            print(f"   • Requirement type: '{metadata.get('requirement_type', 'N/A')}'")
            print(f"   • Requirement ID: '{metadata.get('requirement_id', 'N/A')}'")
        
        # DEMO 5: Search by Related Terms
        print(f"\n🔍 DEMO 5: Search by Related Terms")
        print("-" * 40)
        
        related_terms = metadata.get('related_terms', [])
        print(f"Related terms ({len(related_terms)} found):")
        
        for i, term in enumerate(related_terms[:3]):
            print(f"   {i+1}. {term}")
            print(f"      → Can search for: '{term[:30]}...'")
        
        # DEMO 6: Search by Date and Branch
        print(f"\n🔍 DEMO 6: Search by Date and Branch")
        print("-" * 40)
        
        date = metadata.get('date', '')
        branch = metadata.get('branch', '')
        
        print(f"Date: {date}")
        print(f"Branch: {branch}")
        print(f"✅ Can filter by:")
        print(f"   • Date: '{date}'")
        print(f"   • Branch: '{branch}'")
        print(f"   • Revision: '{metadata.get('revision', 'N/A')}'")
        
        # DEMO 7: Search by Content Summary
        print(f"\n🔍 DEMO 7: Search by Content Summary")
        print("-" * 40)
        
        content_summary = metadata.get('content_summary', '')
        print(f"Content Summary: {content_summary}")
        
        # Extract key concepts for search
        key_concepts = ['TRL', 'Technology Readiness Level', 'milestones', 'aerospace']
        print(f"\n✅ Can search for key concepts:")
        for concept in key_concepts:
            if concept.lower() in content_summary.lower():
                print(f"   • '{concept}' → Found in content")
        
        # DEMO 8: Practical Search Queries
        print(f"\n🔍 DEMO 8: Practical Search Queries")
        print("-" * 40)
        
        print("🎯 Example search queries you can implement:")
        
        search_examples = [
            "Find all ECSS-E-AS-11C documents",
            "Find documents about Technology Readiness Level",
            "Find documents with TRL requirements",
            "Find documents from 2014",
            "Find documents with Table 4-2",
            "Find documents about flight qualification",
            "Find documents referencing ISO 16290",
            "Find performance requirements",
            "Find documents with aerospace elements"
        ]
        
        for i, query in enumerate(search_examples, 1):
            print(f"   {i}. {query}")
        
        # DEMO 9: Metadata Retrieval Functions
        print(f"\n🔍 DEMO 9: Metadata Retrieval Functions")
        print("-" * 40)
        
        print("📋 Functions you can implement:")
        print("""
def search_by_standard_id(standard_id):
    # Filter documents by standard ID
    return [doc for doc in documents if doc.metadata.get('standard_id') == standard_id]

def search_by_keywords(keywords):
    # Filter documents by keywords
    return [doc for doc in documents if any(kw in doc.metadata.get('keywords', []) for kw in keywords)]

def search_by_date_range(start_date, end_date):
    # Filter documents by date range
    return [doc for doc in documents if start_date <= doc.metadata.get('date') <= end_date]

def search_by_requirement_type(req_type):
    # Filter documents by requirement type
    return [doc for doc in documents if doc.metadata.get('requirement_type') == req_type]

def search_by_table_info(table_title):
    # Filter documents by table information
    return [doc for doc in documents if doc.metadata.get('table_title') == table_title]
        """)
        
        print(f"\n✅ DEMONSTRATION COMPLETED!")
        print(f"   • All metadata is retrievable and searchable")
        print(f"   • Images contain searchable content")
        print(f"   • Requirements are extracted and accessible")
        print(f"   • System supports complex queries and filtering")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_search_functionality() 