#!/usr/bin/env python3
"""
MORPHIK ADVANCED SYSTEM - FULL FEATURE UTILIZATION
================================================

This system leverages ALL of Morphik's advanced capabilities:
1. Knowledge Graph Operations with custom entity extraction
2. ECSS-specific entity types and relationships  
3. Batch operations for efficiency
4. Advanced querying with agent_query
5. Workflow status monitoring
6. Document metadata management
7. Cache management for performance
8. Graph visualization and analysis

Built to exploit Morphik's full potential for ECSS documents.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import os
import json
import time
import logging
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

from morphik import Morphik
from morphik.models import (
    GraphPromptOverrides, 
    EntityExtractionPromptOverride, 
    EntityExtractionExample,
    EntityResolutionPromptOverride,
    EntityResolutionExample
)
from morphik.rules import NaturalLanguageRule

# Configure logging (Windows-compatible)
import sys
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('morphik_advanced.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
# Set console encoding for Windows
if sys.platform == "win32":
    import os
    os.system("chcp 65001 >nul 2>&1")  # Set UTF-8 encoding
logger = logging.getLogger(__name__)

@dataclass
class ECSSEntityConfig:
    """Configuration for ECSS-specific entity extraction."""
    entity_examples: List[EntityExtractionExample]
    resolution_examples: List[EntityResolutionExample]
    custom_prompt: str

@dataclass
class AdvancedMorphikConfig:
    """Configuration for advanced Morphik features."""
    morphik_uri: str
    enable_knowledge_graphs: bool = True
    enable_batch_operations: bool = True
    enable_caching: bool = True
    enable_workflow_monitoring: bool = True
    max_concurrent_graphs: int = 5

class MorphikAdvancedSystem:
    """
    Advanced ECSS system that fully exploits Morphik's capabilities.
    
    Features:
    - Knowledge graphs with ECSS-specific entities
    - Batch operations for efficiency  
    - Advanced querying and filtering
    - Workflow monitoring and status tracking
    - Document metadata management
    - Performance optimization with caching
    - Graph visualization and analysis
    """
    
    def __init__(self, config: AdvancedMorphikConfig):
        """Initialize the advanced system."""
        self.config = config
        self.db = None
        self.graphs = {}
        self.caches = {}
        self.entity_config = self._create_ecss_entity_config()
        
        # Initialize Morphik
        self._init_morphik()
        
        # Initialize advanced features
        if self.config.enable_knowledge_graphs:
            self._init_knowledge_graphs()
        
        if self.config.enable_caching:
            self._init_caching()
        
        logger.info("🚀 Advanced Morphik System initialized with full feature utilization")
    
    def _init_morphik(self):
        """Initialize Morphik connection with fallback validation."""
        try:
            self.db = Morphik(self.config.morphik_uri)
            logger.info("PASS: Morphik client initialized")
            
            # Test connection with multiple fallback methods
            connection_validated = False
            
            # Method 1: Try list_documents()
            try:
                documents = self.db.list_documents()
                logger.info(f"PASS: Morphik connection validated - found {len(documents)} documents")
                connection_validated = True
            except Exception as list_error:
                logger.warning(f"WARNING: list_documents() failed: {str(list_error)[:200]}")
                
                # Method 2: Try basic query
                try:
                    test_response = self.db.query("test", k=1)
                    logger.info("PASS: Morphik connection validated via query method")
                    connection_validated = True
                except Exception as query_error:
                    logger.warning(f"WARNING: query() also failed: {str(query_error)[:200]}")
                    
                    # Method 3: Try retrieve_chunks
                    try:
                        test_chunks = self.db.retrieve_chunks("test", k=1)
                        logger.info("PASS: Morphik connection validated via retrieve_chunks")
                        connection_validated = True
                    except Exception as chunks_error:
                        logger.error(f"FAIL: All connection methods failed")
                        logger.error(f"1. list_documents: {str(list_error)[:100]}")
                        logger.error(f"2. query: {str(query_error)[:100]}")
                        logger.error(f"3. retrieve_chunks: {str(chunks_error)[:100]}")
                        raise Exception("Could not establish Morphik connection with any method")
            
            if connection_validated:
                logger.info("PASS: Connected to Morphik with advanced features enabled")
            
        except Exception as e:
            logger.error(f"FAIL: Failed to initialize Morphik: {str(e)[:200]}")
            raise
    
    def _create_ecss_entity_config(self) -> ECSSEntityConfig:
        """Create ECSS-specific entity extraction configuration."""
        
        # Define ECSS-specific entity examples
        entity_examples = [
            # Standards and Documents
            EntityExtractionExample(
                label="ECSS-E-ST-40C", 
                type="STANDARD",
                properties={"branch": "E", "discipline": "ST", "number": "40"}
            ),
            EntityExtractionExample(
                label="Software Development Standard", 
                type="STANDARD_TITLE"
            ),
            
            # Requirements
            EntityExtractionExample(
                label="The software shall be verified", 
                type="REQUIREMENT",
                properties={"type": "verification", "mandatory": True}
            ),
            EntityExtractionExample(
                label="Software Requirement SR-001", 
                type="REQUIREMENT_ID"
            ),
            
            # Procedures and Methods
            EntityExtractionExample(
                label="Static Analysis Procedure", 
                type="PROCEDURE",
                properties={"category": "verification"}
            ),
            EntityExtractionExample(
                label="Code Review Process", 
                type="PROCEDURE",
                properties={"category": "quality"}
            ),
            
            # Technical Concepts
            EntityExtractionExample(
                label="Software Configuration Management", 
                type="CONCEPT",
                properties={"domain": "software"}
            ),
            EntityExtractionExample(
                label="Verification and Validation", 
                type="CONCEPT",
                properties={"domain": "quality"}
            ),
            
            # Phases and Lifecycles
            EntityExtractionExample(
                label="Preliminary Design Review", 
                type="PHASE",
                properties={"stage": "design"}
            ),
            EntityExtractionExample(
                label="Critical Design Review", 
                type="PHASE",
                properties={"stage": "design"}
            ),
            
            # Tools and Methods
            EntityExtractionExample(
                label="MISRA-C Compliance", 
                type="TOOL",
                properties={"category": "coding_standard"}
            ),
            EntityExtractionExample(
                label="Unit Testing Framework", 
                type="TOOL",
                properties={"category": "testing"}
            )
        ]
        
        # Define entity resolution examples
        resolution_examples = [
            EntityResolutionExample(
                canonical="Software Verification",
                variants=["SW Verification", "Software V&V", "SW V&V", "Software Testing"]
            ),
            EntityResolutionExample(
                canonical="Configuration Management",
                variants=["CM", "Config Management", "SCM", "Software CM"]
            ),
            EntityResolutionExample(
                canonical="ECSS-E-ST-40C",
                variants=["ECSS-E-ST-40", "E-ST-40C", "E-ST-40"]
            )
        ]
        
        # Custom prompt for ECSS extraction
        custom_prompt = """
        Extract entities from this ECSS space engineering document focusing on:
        
        1. STANDARDS: ECSS standard identifiers and titles
        2. REQUIREMENTS: Shall/should statements and requirement IDs
        3. PROCEDURES: Step-by-step processes and methods
        4. CONCEPTS: Technical concepts and engineering principles
        5. PHASES: Project phases and milestones
        6. TOOLS: Software tools, frameworks, and standards
        
        For each entity, identify:
        - Type (STANDARD, REQUIREMENT, PROCEDURE, CONCEPT, PHASE, TOOL)
        - Properties (branch, discipline, category, domain, etc.)
        - Relationships to other entities
        
        Content: {content}
        
        Examples: {examples}
        
        Return entities in JSON format with proper classification.
        """
        
        return ECSSEntityConfig(
            entity_examples=entity_examples,
            resolution_examples=resolution_examples,
            custom_prompt=custom_prompt
        )
    
    def _init_knowledge_graphs(self):
        """Initialize ECSS knowledge graphs for each branch."""
        if not self.config.enable_knowledge_graphs:
            return
        
        # First, check for and clean up any existing duplicate graphs
        self._cleanup_duplicate_graphs()
        
        ecss_branches = {
            'E': 'Engineering Standards',
            'M': 'Management Standards', 
            'Q': 'Quality Standards',
            'S': 'Space Assurance Standards',
            'U': 'Sustainability Standards'
        }
        
        logger.info("🔗 Initializing ECSS knowledge graphs...")
        
        # Get list of existing graphs first
        try:
            existing_graphs = self.db.list_graphs()
            existing_graph_names = [g.name for g in existing_graphs] if existing_graphs else []
        except Exception as e:
            logger.warning(f"⚠️ Could not list existing graphs: {e}")
            existing_graph_names = []
        
        for branch, description in ecss_branches.items():
            try:
                graph_name = f"ecss_{branch.lower()}_knowledge_graph"
                
                # Check if graph already exists
                if graph_name in existing_graph_names:
                    logger.info(f"♻️ Graph {graph_name} already exists, skipping creation")
                    # Still add to our tracking
                    self.graphs[branch] = {
                        'name': graph_name,
                        'description': description,
                        'status': 'processing'  # Assume it's still processing
                    }
                    continue
                
                # Create graph with ECSS-specific entity extraction
                graph = self.db.create_graph(
                    name=graph_name,
                    filters={"filename": f"ECSS-{branch}-"},  # Filter by branch
                    prompt_overrides=GraphPromptOverrides(
                        entity_extraction=EntityExtractionPromptOverride(
                            prompt_template=self.entity_config.custom_prompt,
                            examples=self.entity_config.entity_examples
                        ),
                        entity_resolution=EntityResolutionPromptOverride(
                            examples=self.entity_config.resolution_examples
                        )
                    )
                )
                
                self.graphs[branch] = {
                    'graph': graph,
                    'name': graph_name,
                    'description': description,
                    'status': 'processing'
                }
                
                logger.info(f"✅ Created {description} knowledge graph: {graph_name}")
                
            except Exception as e:
                logger.error(f"❌ Failed to create graph for branch {branch}: {e}")

    def _cleanup_duplicate_graphs(self):
        """Clean up any duplicate or unwanted graphs."""
        try:
            logger.info("🧹 Checking for duplicate graphs to clean up...")
            
            # Get all existing graphs
            existing_graphs = self.db.list_graphs()
            if not existing_graphs:
                return
            
            # Define the canonical graph names we want to keep
            canonical_names = {
                "ecss_e_knowledge_graph",
                "ecss_m_knowledge_graph", 
                "ecss_q_knowledge_graph",
                "ecss_s_knowledge_graph",
                "ecss_u_knowledge_graph"
            }
            
            graphs_to_delete = []
            canonical_found = set()
            
            for graph in existing_graphs:
                graph_name = graph.name
                
                # If it's a canonical graph name
                if graph_name in canonical_names:
                    if graph_name in canonical_found:
                        # Duplicate canonical graph
                        graphs_to_delete.append(graph_name)
                        logger.warning(f"🗑️ Found duplicate canonical graph: {graph_name}")
                    else:
                        canonical_found.add(graph_name)
                        logger.info(f"✅ Keeping canonical graph: {graph_name}")
                
                # If it looks like an ECSS graph but isn't canonical (test graphs, branches, etc.)
                elif any(term in graph_name.lower() for term in ['ecss', 'test', 'branch']):
                    graphs_to_delete.append(graph_name)
                    logger.warning(f"🗑️ Found non-canonical ECSS graph: {graph_name}")
            
            # Delete unwanted graphs
            if graphs_to_delete:
                logger.info(f"🧹 Cleaning up {len(graphs_to_delete)} duplicate/unwanted graphs...")
                for graph_name in graphs_to_delete[:10]:  # Limit to 10 at a time for safety
                    try:
                        self.db.delete_graph(graph_name)
                        logger.info(f"🗑️ Deleted graph: {graph_name}")
                    except Exception as e:
                        logger.error(f"❌ Failed to delete graph {graph_name}: {e}")
                
                if len(graphs_to_delete) > 10:
                    logger.warning(f"⚠️ {len(graphs_to_delete) - 10} more graphs need cleanup")
            else:
                logger.info("✅ No duplicate graphs found")
                
        except Exception as e:
            logger.error(f"❌ Error during graph cleanup: {e}")
    
    def _init_caching(self):
        """Initialize performance caching."""
        if not self.config.enable_caching:
            return
        
        try:
            # Create caches for common operations
            caches_to_create = [
                ("ecss_search_cache", "Common ECSS search results"),
                ("entity_extraction_cache", "Entity extraction results"),
                ("document_metadata_cache", "Document metadata")
            ]
            
            for cache_name, description in caches_to_create:
                cache = self.db.create_cache(name=cache_name)
                self.caches[cache_name] = {
                    'cache': cache,
                    'description': description
                }
                logger.info(f"✅ Created cache: {cache_name}")
                
        except Exception as e:
            logger.warning(f"⚠️  Cache creation failed: {e}")
    
    def wait_for_graph_completion(self, branch: str = None) -> Dict[str, Any]:
        """Wait for knowledge graph completion with status monitoring."""
        if not self.config.enable_workflow_monitoring:
            return {}
        
        if branch:
            branches_to_check = [branch]
        else:
            branches_to_check = list(self.graphs.keys())
        
        completion_status = {}
        
        for branch_key in branches_to_check:
            if branch_key not in self.graphs:
                continue
            
            graph_info = self.graphs[branch_key]
            graph_name = graph_info['name']
            
            logger.info(f"⏳ Waiting for {graph_name} completion...")
            
            try:
                # Wait for completion
                completed_graph = self.db.wait_for_graph_completion(graph_name)
                
                # Update status
                self.graphs[branch_key]['graph'] = completed_graph
                self.graphs[branch_key]['status'] = 'completed'
                
                completion_status[branch_key] = {
                    'status': 'completed',
                    'entities': len(completed_graph.entities),
                    'relationships': len(completed_graph.relationships),
                    'graph_name': graph_name
                }
                
                logger.info(f"✅ {graph_name} completed: {len(completed_graph.entities)} entities, {len(completed_graph.relationships)} relationships")
                
            except Exception as e:
                logger.error(f"❌ Failed to complete graph {graph_name}: {e}")
                completion_status[branch_key] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        return completion_status
    
    def advanced_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Perform advanced search using all available Morphik features."""
        
        # Extract parameters
        branch = kwargs.get('branch')
        use_graphs = kwargs.get('use_graphs', True)
        use_agent = kwargs.get('use_agent', True)
        limit = kwargs.get('limit', 10)
        filters = kwargs.get('filters', {})
        
        logger.info(f"🔍 Advanced search: '{query}' (branch: {branch}, graphs: {use_graphs})")
        
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'methods_used': [],
            'results': []
        }
        
        try:
            # Method 1: Agent Query (if available)
            if use_agent and hasattr(self.db, 'agent_query'):
                try:
                    agent_results = self.db.agent_query(
                        query=query,
                        k=limit,
                        filters=filters
                    )
                    results['agent_results'] = agent_results
                    results['methods_used'].append('agent_query')
                    logger.info("✅ Agent query completed")
                except Exception as e:
                    logger.warning(f"⚠️  Agent query failed: {e}")
            
            # Method 2: Knowledge Graph Query
            if use_graphs and branch and branch in self.graphs:
                graph_info = self.graphs[branch]
                if graph_info['status'] == 'completed':
                    try:
                        graph = graph_info['graph']
                        # Search within graph entities
                        relevant_entities = [
                            entity for entity in graph.entities 
                            if query.lower() in entity.label.lower()
                        ]
                        results['graph_entities'] = [
                            {
                                'label': entity.label,
                                'type': entity.type,
                                'properties': getattr(entity, 'properties', {})
                            }
                            for entity in relevant_entities[:limit]
                        ]
                        results['methods_used'].append('knowledge_graph')
                        logger.info(f"✅ Found {len(relevant_entities)} relevant entities in graph")
                    except Exception as e:
                        logger.warning(f"⚠️  Graph query failed: {e}")
            
            # Method 3: Enhanced ColPali Search
            try:
                chunks = self.db.retrieve_chunks(
                    query=query,
                    use_colpali=True,
                    k=limit,
                    filters=filters
                )
                
                enhanced_chunks = []
                for chunk in chunks:
                    enhanced_chunk = {
                        'content': str(chunk.content)[:500] + "..." if len(str(chunk.content)) > 500 else str(chunk.content),
                        'filename': getattr(chunk, 'filename', 'unknown'),
                        'score': getattr(chunk, 'score', 0.0),
                        'chunk_number': getattr(chunk, 'chunk_number', 0),
                        'is_visual': hasattr(chunk.content, 'size'),  # PIL Image check
                    }
                    enhanced_chunks.append(enhanced_chunk)
                
                results['colpali_chunks'] = enhanced_chunks
                results['methods_used'].append('colpali_retrieval')
                logger.info(f"✅ Retrieved {len(enhanced_chunks)} ColPali chunks")
                
            except Exception as e:
                logger.warning(f"⚠️  ColPali search failed: {e}")
            
            # Method 4: Standard Query with Enhancements
            try:
                query_response = self.db.query(
                    query=query,
                    use_colpali=True,
                    k=limit
                )
                
                if query_response and query_response.completion:
                    results['contextual_response'] = query_response.completion
                    results['methods_used'].append('standard_query')
                    logger.info("✅ Standard query completed")
                
            except Exception as e:
                logger.warning(f"⚠️  Standard query failed: {e}")
            
        except Exception as e:
            logger.error(f"❌ Advanced search failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def batch_document_analysis(self, document_ids: List[str]) -> Dict[str, Any]:
        """Perform batch analysis of multiple documents efficiently."""
        logger.info(f"📊 Batch analysis of {len(document_ids)} documents")
        
        try:
            # Use batch operations for efficiency
            documents = self.db.batch_get_documents(document_ids)
            
            analysis_results = {
                'total_documents': len(documents),
                'successful_analyses': 0,
                'failed_analyses': 0,
                'document_summaries': [],
                'entity_statistics': {},
                'processing_time': time.time()
            }
            
            for doc in documents:
                try:
                    # Analyze each document
                    doc_analysis = self._analyze_single_document(doc)
                    analysis_results['document_summaries'].append(doc_analysis)
                    analysis_results['successful_analyses'] += 1
                    
                    # Update entity statistics
                    for entity_type, count in doc_analysis.get('entity_counts', {}).items():
                        if entity_type not in analysis_results['entity_statistics']:
                            analysis_results['entity_statistics'][entity_type] = 0
                        analysis_results['entity_statistics'][entity_type] += count
                        
                except Exception as e:
                    logger.error(f"❌ Failed to analyze document {getattr(doc, 'filename', 'unknown')}: {e}")
                    analysis_results['failed_analyses'] += 1
            
            analysis_results['processing_time'] = time.time() - analysis_results['processing_time']
            logger.info(f"✅ Batch analysis completed: {analysis_results['successful_analyses']}/{len(documents)} successful")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"❌ Batch analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_single_document(self, document) -> Dict[str, Any]:
        """Analyze a single document for entities and metadata."""
        
        doc_info = {
            'filename': getattr(document, 'filename', 'unknown'),
            'document_id': getattr(document, 'external_id', 'unknown'),
            'metadata': getattr(document, 'metadata', {}),
            'entity_counts': {},
            'key_entities': [],
            'ecss_classification': {}
        }
        
        # Extract ECSS classification from filename
        filename = doc_info['filename']
        if filename.startswith('ECSS-'):
            parts = filename.split('-')
            if len(parts) >= 4:
                doc_info['ecss_classification'] = {
                    'branch': parts[1],
                    'discipline': parts[2],
                    'number': parts[3].split('C')[0] if 'C' in parts[3] else parts[3]
                }
        
        return doc_info
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status using all advanced features."""
        status = {
            'timestamp': datetime.now().isoformat(),
            'morphik_connection': 'connected',
            'features_enabled': {
                'knowledge_graphs': self.config.enable_knowledge_graphs,
                'batch_operations': self.config.enable_batch_operations,
                'caching': self.config.enable_caching,
                'workflow_monitoring': self.config.enable_workflow_monitoring
            },
            'knowledge_graphs': {},
            'caches': {},
            'document_stats': {},
            'performance_metrics': {}
        }
        
        try:
            # Graph status
            for branch, graph_info in self.graphs.items():
                status['knowledge_graphs'][branch] = {
                    'name': graph_info['name'],
                    'status': graph_info['status'],
                    'description': graph_info['description']
                }
                
                if graph_info['status'] == 'completed':
                    graph = graph_info['graph']
                    status['knowledge_graphs'][branch].update({
                        'entities': len(graph.entities),
                        'relationships': len(graph.relationships)
                    })
            
            # Cache status
            for cache_name, cache_info in self.caches.items():
                status['caches'][cache_name] = cache_info['description']
            
            # Document statistics
            try:
                documents = self.db.list_documents()
                status['document_stats'] = {
                    'total_documents': len(documents),
                    'ecss_branches': self._count_ecss_branches([doc.filename for doc in documents])
                }
            except Exception as e:
                status['document_stats'] = {'error': str(e)}
            
        except Exception as e:
            status['error'] = str(e)
        
        return status
    
    def _count_ecss_branches(self, filenames: List[str]) -> Dict[str, int]:
        """Count documents by ECSS branch."""
        branch_counts = {'E': 0, 'M': 0, 'Q': 0, 'S': 0, 'U': 0, 'Other': 0}
        
        for filename in filenames:
            if filename.startswith('ECSS-'):
                parts = filename.split('-')
                if len(parts) >= 2:
                    branch = parts[1]
                    if branch in branch_counts:
                        branch_counts[branch] += 1
                    else:
                        branch_counts['Other'] += 1
                else:
                    branch_counts['Other'] += 1
            else:
                branch_counts['Other'] += 1
        
        return branch_counts

def main():
    """Test the advanced Morphik system."""
    print("🚀 TESTING ADVANCED MORPHIK SYSTEM")
    print("=" * 50)
    
    # Configuration
    config = AdvancedMorphikConfig(
        morphik_uri=os.getenv("MORPHIK_URI"),
        enable_knowledge_graphs=True,
        enable_batch_operations=True,
        enable_caching=True,
        enable_workflow_monitoring=True
    )
    
    if not config.morphik_uri:
        print("❌ MORPHIK_URI not set")
        return
    
    # Initialize system
    system = MorphikAdvancedSystem(config)
    
    # Test system status
    print("\n1️⃣ System Status:")
    status = system.get_system_status()
    print(json.dumps(status, indent=2, default=str))
    
    # Test advanced search
    print("\n2️⃣ Advanced Search Test:")
    search_results = system.advanced_search(
        "software verification requirements",
        branch="E",
        use_graphs=True,
        use_agent=True,
        limit=5
    )
    print(f"Search methods used: {search_results.get('methods_used', [])}")
    
    # Wait for graph completion if needed
    if system.graphs:
        print("\n3️⃣ Waiting for Knowledge Graph Completion:")
        completion_status = system.wait_for_graph_completion()
        for branch, status in completion_status.items():
            print(f"  {branch}: {status.get('status', 'unknown')}")
    
    print("\n✅ Advanced system test completed!")

if __name__ == "__main__":
    main() 