

#!/usr/bin/env python3
"""
Test metadata extraction using the query() method with schema
This might be the correct approach instead of rules during ingestion.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Test metadata extraction using the query() method with schema
This might be the correct approach instead of rules during ingestion.
"""

import os
import sys

# Load environment variables

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from pydantic import BaseModel, Field
from typing import List

def test_query_metadata():
    """Test metadata extraction using query() with schema."""
    print("🔍 Testing Metadata Extraction with query() method")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define metadata schema
    class ECSSMetadata(BaseModel):
        title: str = Field(description="Document title")
        standard_id: str = Field(description="ECSS standard identifier")
        revision: str = Field(description="Revision number")
        date: str = Field(description="Publication date")
        branch: str = Field(description="ECSS branch (E, M, P, Q)")
        discipline: str = Field(description="ECSS discipline")
        summary: str = Field(description="Brief summary of the document")
        key_requirements: List[str] = Field(description="Key requirements mentioned")
    
    # Test 1: Query existing documents for metadata
    print("\n🔍 Test 1: Query existing documents for metadata")
    try:
        response = db.query(
            "Extract metadata from this ECSS document including title, standard ID, revision, date, branch, discipline, summary, and key requirements",
            k=10,  # Get more context
            schema=ECSSMetadata
        )
        
        print(f"✅ Query completed")
        print(f"Response type: {type(response.completion)}")
        
        if isinstance(response.completion, dict):
            print(f"✅ Structured output received:")
            for key, value in response.completion.items():
                print(f"  {key}: {value}")
        elif isinstance(response.completion, str):
            print(f"📝 Text response: {response.completion[:500]}...")
        else:
            print(f"❓ Unexpected response type: {response.completion}")
            
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
    
    # Test 2: Query with specific filters
    print("\n🔍 Test 2: Query with specific filters")
    try:
        response = db.query(
            "What is the title, standard ID, and revision of this ECSS document?",
            filters={"filename": "ECSS-E-AS-11C(1October2014).pdf"},
            schema=ECSSMetadata
        )
        
        print(f"✅ Filtered query completed")
        if isinstance(response.completion, dict):
            print(f"✅ Structured output: {response.completion}")
        else:
            print(f"📝 Response: {response.completion}")
            
    except Exception as e:
        print(f"❌ Error in Test 2: {e}")
    
    # Test 3: Simple text query without schema
    print("\n🔍 Test 3: Simple text query without schema")
    try:
        response = db.query(
            "What is the title and standard ID of this ECSS document?",
            k=5
        )
        
        print(f"✅ Text query completed")
        print(f"Response: {response.completion}")
        
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
    
    # Test 4: Check what documents are available
    print("\n🔍 Test 4: Check available documents")
    try:
        docs = db.list_documents()
        print(f"✅ Found {len(docs)} documents")
        
        for i, doc in enumerate(docs[:3]):
            print(f"  Document {i+1}: {doc.filename}")
            print(f"    ID: {doc.external_id}")
            print(f"    Status: {doc.status}")
            
    except Exception as e:
        print(f"❌ Error in Test 4: {e}")

if __name__ == "__main__":
    test_query_metadata() 

import os
import sys

# Load environment variables

# Add the backend directory to the path
sys.path.insert(0, str(backend_dir.parent))

from morphik import Morphik
from pydantic import BaseModel, Field
from typing import List

def test_query_metadata():
    """Test metadata extraction using query() with schema."""
    print("🔍 Testing Metadata Extraction with query() method")
    print("=" * 50)
    
    # Connect to Morphik
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    db = Morphik(morphik_uri)
    
    # Define metadata schema
    class ECSSMetadata(BaseModel):
        title: str = Field(description="Document title")
        standard_id: str = Field(description="ECSS standard identifier")
        revision: str = Field(description="Revision number")
        date: str = Field(description="Publication date")
        branch: str = Field(description="ECSS branch (E, M, P, Q)")
        discipline: str = Field(description="ECSS discipline")
        summary: str = Field(description="Brief summary of the document")
        key_requirements: List[str] = Field(description="Key requirements mentioned")
    
    # Test 1: Query existing documents for metadata
    print("\n🔍 Test 1: Query existing documents for metadata")
    try:
        response = db.query(
            "Extract metadata from this ECSS document including title, standard ID, revision, date, branch, discipline, summary, and key requirements",
            k=10,  # Get more context
            schema=ECSSMetadata
        )
        
        print(f"✅ Query completed")
        print(f"Response type: {type(response.completion)}")
        
        if isinstance(response.completion, dict):
            print(f"✅ Structured output received:")
            for key, value in response.completion.items():
                print(f"  {key}: {value}")
        elif isinstance(response.completion, str):
            print(f"📝 Text response: {response.completion[:500]}...")
        else:
            print(f"❓ Unexpected response type: {response.completion}")
            
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
    
    # Test 2: Query with specific filters
    print("\n🔍 Test 2: Query with specific filters")
    try:
        response = db.query(
            "What is the title, standard ID, and revision of this ECSS document?",
            filters={"filename": "ECSS-E-AS-11C(1October2014).pdf"},
            schema=ECSSMetadata
        )
        
        print(f"✅ Filtered query completed")
        if isinstance(response.completion, dict):
            print(f"✅ Structured output: {response.completion}")
        else:
            print(f"📝 Response: {response.completion}")
            
    except Exception as e:
        print(f"❌ Error in Test 2: {e}")
    
    # Test 3: Simple text query without schema
    print("\n🔍 Test 3: Simple text query without schema")
    try:
        response = db.query(
            "What is the title and standard ID of this ECSS document?",
            k=5
        )
        
        print(f"✅ Text query completed")
        print(f"Response: {response.completion}")
        
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
    
    # Test 4: Check what documents are available
    print("\n🔍 Test 4: Check available documents")
    try:
        docs = db.list_documents()
        print(f"✅ Found {len(docs)} documents")
        
        for i, doc in enumerate(docs[:3]):
            print(f"  Document {i+1}: {doc.filename}")
            print(f"    ID: {doc.external_id}")
            print(f"    Status: {doc.status}")
            
    except Exception as e:
        print(f"❌ Error in Test 4: {e}")

if __name__ == "__main__":
    test_query_metadata() 