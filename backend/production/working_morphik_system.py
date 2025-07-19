#!/usr/bin/env python3
"""
WORKING MORPHIK SYSTEM - CONFIRMED FEATURES ONLY
================================================

Uses only the features we've confirmed work:
- ColPali visual search
- Agent queries  
- Batch operations
- Standard query/retrieval
- Document management

No knowledge graphs (404 endpoint).
"""
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Load environment
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")
sys.path.insert(0, str(Path(__file__).parent.parent))

from morphik import Morphik

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WorkingMorphikConfig:
    """Configuration for working Morphik features only."""
    morphik_uri: str
    use_colpali: bool = True
    use_agent_query: bool = True
    use_batch_operations: bool = True

class WorkingMorphikSystem:
    """
    Morphik system using only confirmed working features.
    
    Features:
    - Multi-method search (standard + colpali + agent)
    - Batch document operations
    - Visual content extraction
    - Contextual responses
    """
    
    def __init__(self, config: WorkingMorphikConfig):
        """Initialize the working system."""
        self.config = config
        self.db = None
        
        # Initialize Morphik
        self._init_morphik()
        
        logger.info("🚀 Working Morphik System initialized")
    
    def _init_morphik(self):
        """Initialize Morphik connection."""
        try:
            self.db = Morphik(self.config.morphik_uri)
            logger.info("✅ Morphik connected")
            
            # Test connection with working methods
            try:
                # Test basic query (without limit parameter)
                test_result = self.db.query("test")
                logger.info("✅ Basic query validated")
            except Exception as e:
                logger.warning(f"⚠️ Query test: {e}")
            
            try:
                # Test document listing with fallback for 307 redirects
                docs = self.db.list_documents(limit=1)
                logger.info(f"✅ Document access: {len(docs) if docs else 0} found")
            except Exception as e:
                logger.warning(f"⚠️ Document listing (expected with 307): {e}")
            
        except Exception as e:
            logger.error(f"❌ Morphik initialization failed: {e}")
            raise
    
    def multi_method_search(self, query: str, methods: List[str] = None) -> Dict[str, Any]:
        """
        Perform search using multiple confirmed working methods.
        
        Args:
            query: Search query
            methods: List of methods to use ['standard', 'colpali', 'agent']
        
        Returns:
            Combined results from all methods
        """
        if methods is None:
            methods = ['standard', 'colpali', 'agent']
        
        results = {
            'query': query,
            'methods_used': [],
            'results': {},
            'processing_time': 0,
            'timestamp': time.time()
        }
        
        start_time = time.time()
        
        # Method 1: Standard Query
        if 'standard' in methods:
            try:
                response = self.db.query(query)
                if response:
                    results['results']['standard'] = {
                        'response': response.completion if hasattr(response, 'completion') else str(response),
                        'metadata': response.metadata if hasattr(response, 'metadata') else None
                    }
                    results['methods_used'].append('standard')
                    logger.info("✅ Standard query completed")
            except Exception as e:
                logger.error(f"❌ Standard query failed: {e}")
        
        # Method 2: ColPali Visual Search
        if 'colpali' in methods and self.config.use_colpali:
            try:
                response = self.db.query(query, use_colpali=True)
                if response:
                    results['results']['colpali'] = {
                        'response': response.completion if hasattr(response, 'completion') else str(response),
                        'visual_content': True,
                        'metadata': response.metadata if hasattr(response, 'metadata') else None
                    }
                    results['methods_used'].append('colpali')
                    logger.info("✅ ColPali visual search completed")
            except Exception as e:
                logger.error(f"❌ ColPali search failed: {e}")
        
        # Method 3: Agent Query (with timeout handling)
        if 'agent' in methods and self.config.use_agent_query:
            try:
                # Try agent query with shorter timeout expectation
                logger.info("🤖 Starting agent query (may take 30+ seconds)...")
                response = self.db.agent_query(query)
                if response:
                    results['results']['agent'] = {
                        'response': response.completion if hasattr(response, 'completion') else str(response),
                        'conversational': True,
                        'metadata': response.metadata if hasattr(response, 'metadata') else None
                    }
                    results['methods_used'].append('agent')
                    logger.info("✅ Agent query completed")
            except Exception as e:
                logger.warning(f"⚠️ Agent query failed (timeout/error): {e}")
                # Continue without agent results - other methods still work
        
        # Add chunk retrieval for context
        try:
            chunks = self.db.retrieve_chunks(query, k=5)
            if chunks:
                results['context_chunks'] = [
                    {
                        'content': chunk.content[:200] + '...' if len(chunk.content) > 200 else chunk.content,
                        'filename': getattr(chunk, 'filename', 'Unknown'),
                        'score': getattr(chunk, 'score', 0)
                    }
                    for chunk in chunks[:3]
                ]
                logger.info(f"✅ Retrieved {len(chunks)} context chunks")
        except Exception as e:
            logger.error(f"❌ Chunk retrieval failed: {e}")
        
        results['processing_time'] = time.time() - start_time
        
        return results
    
    def batch_document_analysis(self, limit: int = 5) -> Dict[str, Any]:
        """Analyze documents using batch operations."""
        if not self.config.use_batch_operations:
            return {'error': 'Batch operations disabled'}
        
        try:
            # Use batch methods - try without parameters first
            docs = self.db.batch_get_documents()
            
            # Limit results if we got more than requested
            if docs and len(docs) > limit:
                docs = docs[:limit]
            
            analysis = {
                'total_documents': len(docs) if docs else 0,
                'documents': [],
                'timestamp': time.time()
            }
            
            if docs:
                for doc in docs[:5]:  # Limit display
                    analysis['documents'].append({
                        'filename': getattr(doc, 'filename', 'Unknown'),
                        'id': getattr(doc, 'id', 'Unknown'),
                        'status': getattr(doc, 'status', 'Unknown')
                    })
            
            logger.info(f"✅ Batch analysis: {analysis['total_documents']} documents")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Batch analysis failed: {e}")
            return {'error': str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            'system': 'Working Morphik System',
            'features': {
                'colpali_visual': self.config.use_colpali,
                'agent_query': self.config.use_agent_query,
                'batch_operations': self.config.use_batch_operations,
                'knowledge_graphs': False  # Confirmed not available
            },
            'connection': 'connected' if self.db else 'disconnected',
            'timestamp': time.time()
        }
        
        # Test each feature
        if self.db:
            # Test standard query
            try:
                self.db.query("test")
                status['features']['standard_query'] = True
            except:
                status['features']['standard_query'] = False
            
            # Test document access
            try:
                self.db.list_documents(limit=1)
                status['features']['document_access'] = True
            except:
                status['features']['document_access'] = False
        
        return status

def main():
    """Test the working system."""
    print("🚀 WORKING MORPHIK SYSTEM TEST")
    print("=" * 50)
    
    # Check environment
    morphik_uri = os.getenv("MORPHIK_URI")
    if not morphik_uri:
        print("❌ MORPHIK_URI not found")
        return
    
    try:
        # Initialize system
        config = WorkingMorphikConfig(morphik_uri=morphik_uri)
        system = WorkingMorphikSystem(config)
        
        # Test system status
        print("\n📊 System Status:")
        status = system.get_system_status()
        for feature, enabled in status['features'].items():
            print(f"  {'✅' if enabled else '❌'} {feature.replace('_', ' ').title()}")
        
        # Test multi-method search
        print(f"\n🔍 Testing Multi-Method Search:")
        query = "verification requirements"
        results = system.multi_method_search(query)
        
        print(f"📝 Query: {results['query']}")
        print(f"⏱️ Processing Time: {results['processing_time']:.2f}s")
        print(f"🔧 Methods Used: {', '.join(results['methods_used'])}")
        
        for method, result in results['results'].items():
            response = result['response']
            preview = response[:100] + '...' if len(response) > 100 else response
            print(f"  {method.title()}: {preview}")
        
        if 'context_chunks' in results:
            print(f"\n📚 Context Chunks: {len(results['context_chunks'])}")
            for i, chunk in enumerate(results['context_chunks'], 1):
                print(f"  {i}. {chunk['filename']}: {chunk['content'][:50]}...")
        
        # Test batch operations
        print(f"\n📊 Testing Batch Operations:")
        batch_results = system.batch_document_analysis(limit=3)
        if 'error' not in batch_results:
            print(f"📈 Documents Found: {batch_results['total_documents']}")
            for doc in batch_results['documents']:
                print(f"  - {doc['filename']}")
        else:
            print(f"❌ Batch Error: {batch_results['error']}")
        
        print(f"\n🎉 Working System Test Complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main() 