"""
Optimized Graph Strategy following Morphik Documentation Best Practices
Based on: https://www.morphik.ai/docs/concepts/knowledge-graphs#performance-considerations
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from morphik import Morphik
from morphik.models import GraphPromptOverrides, EntityExtractionExample, EntityResolutionExample
from morphik.rules import NaturalLanguageRule
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedECSSGraphManager:
    """
    Manages ECSS knowledge graphs following Morphik's performance recommendations.
    Creates focused graphs by branch and supports incremental updates.
    """
    
    def __init__(self, morphik_uri: Optional[str] = None):
        self.db = Morphik(uri=morphik_uri) if morphik_uri else Morphik()
        self.branch_graphs = {
            'E': 'ecss_engineering_graph',
            'M': 'ecss_management_graph', 
            'Q': 'ecss_quality_graph',
            'S': 'ecss_space_assurance_graph',
            'U': 'ecss_sustainability_graph'
        }
    
    def create_focused_graphs(self, doc_ids: List[str]) -> Dict[str, str]:
        """
        Create focused graphs by ECSS branch following Morphik's recommendation
        to use metadata filters for focused graphs rather than one large graph.
        """
        logger.info("Creating focused ECSS graphs by branch...")
        
        created_graphs = {}
        
        for branch, graph_name in self.branch_graphs.items():
            try:
                logger.info(f"Creating {graph_name} for branch {branch}...")
                
                # Create focused graph with branch filter
                graph = self.db.create_graph(
                    name=graph_name,
                    filters={"branch": branch},
                    prompt_overrides=self._get_ecss_prompt_overrides()
                )
                
                created_graphs[branch] = graph_name
                logger.info(f"✓ Created {graph_name} with {len(graph.entities)} entities")
                
            except Exception as e:
                logger.error(f"✗ Failed to create {graph_name}: {e}")
        
        return created_graphs
    
    def update_graph_incrementally(self, graph_name: str, new_doc_ids: List[str]) -> bool:
        """
        Update existing graph with new documents following Morphik's
        recommendation for incremental updates.
        """
        try:
            logger.info(f"Updating {graph_name} with {len(new_doc_ids)} new documents...")
            
            updated_graph = self.db.update_graph(
                name=graph_name,
                additional_documents=new_doc_ids
            )
            
            logger.info(f"✓ Updated {graph_name} successfully")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to update {graph_name}: {e}")
            return False
    
    def query_with_adaptive_settings(self, query: str, branch: Optional[str] = None) -> Dict:
        """
        Query with adaptive settings based on query complexity,
        following Morphik's performance recommendations.
        """
        # Determine query complexity
        is_complex = self._is_complex_query(query)
        
        # Check if this is a visual query that would benefit from ColPali
        visual_keywords = ['image', 'diagram', 'figure', 'chart', 'graph', 'table', 'visual', 'picture', 'photo']
        is_visual_query = any(keyword in query.lower() for keyword in visual_keywords)
        
        # Check if this is a relationship query that would benefit from enhanced graph traversal
        relationship_keywords = ['relationship', 'connection', 'between', 'related to', 'depends on', 'requires', 'implements']
        is_relationship_query = any(keyword in query.lower() for keyword in relationship_keywords)
        
        # Adaptive settings based on complexity and query type
        if is_complex or is_relationship_query:
            hop_depth = 3  # Higher hop depth for complex/relationship queries
            k = 15
            use_reranking = True
        else:
            hop_depth = 2
            k = 10
            use_reranking = False
        
        # Select appropriate graph
        if branch and branch in self.branch_graphs:
            # Use enhanced branch-specific graph
            graph_name = f"ecss_{branch.lower()}_branch_enhanced"
        else:
            # Use general enhanced graph for cross-branch queries
            graph_name = "ecss_general_enhanced"
        
        logger.info(f"Querying with hop_depth={hop_depth}, k={k}, graph={graph_name}, visual={is_visual_query}, relationship={is_relationship_query}")
        
        try:
            # For visual queries, use ColPali for enhanced retrieval
            if is_visual_query:
                logger.info("🔍 Using ColPali for visual query")
                response = self.db.query(
                    query,
                    graph_name=graph_name,
                    hop_depth=hop_depth,
                    include_paths=True,
                    k=k,
                    use_colpali=True  # Enable ColPali for visual understanding
                )
            else:
                # Standard graph query with enhanced traversal
                response = self.db.query(
                    query,
                    graph_name=graph_name,
                    hop_depth=hop_depth,
                    include_paths=True,
                    k=k
                )
            
            return {
                'completion': response.completion,
                'sources': response.sources,
                'metadata': response.metadata,
                'query_settings': {
                    'hop_depth': hop_depth,
                    'k': k,
                    'use_reranking': use_reranking,
                    'graph_name': graph_name,
                    'use_colpali': is_visual_query,
                    'enhanced_graph': True
                }
            }
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {'error': str(e)}
    
    def _is_complex_query(self, query: str) -> bool:
        """
        Determine if a query is complex based on keywords and structure.
        """
        complex_keywords = [
            'relationship', 'compare', 'difference', 'connection',
            'how does', 'what is the relationship', 'interdependencies',
            'cross-reference', 'multiple', 'various', 'different'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in complex_keywords)
    
    def _get_ecss_prompt_overrides(self) -> GraphPromptOverrides:
        """
        Get optimized prompt overrides for ECSS domain.
        """
        extraction_examples = [
            EntityExtractionExample(label="ECSS-Q-ST-70C", type="Standard"),
            EntityExtractionExample(label="5.2.1a", type="Requirement"),
            EntityExtractionExample(label="Space Product Assurance", type="Discipline"),
            EntityExtractionExample(label="Quality Management System", type="Process")
        ]
        
        resolution_examples = [
            EntityResolutionExample(
                canonical="ECSS-Q-ST-70C",
                variants=["Q-ST-70C", "ECSS Q-ST-70C", "Quality Standard 70C"]
            ),
            EntityResolutionExample(
                canonical="Space Product Assurance",
                variants=["SPA", "Space Assurance", "Product Assurance"]
            )
        ]
        
        return GraphPromptOverrides(
            entity_extraction_examples=extraction_examples,
            entity_resolution_examples=resolution_examples
        )
    
    def get_graph_statistics(self) -> Dict[str, Dict]:
        """
        Get statistics for all graphs to monitor performance.
        """
        stats = {}
        
        for branch, graph_name in self.branch_graphs.items():
            try:
                graph = self.db.get_graph(graph_name)
                stats[branch] = {
                    'name': graph_name,
                    'entities': len(graph.entities),
                    'relationships': len(graph.relationships),
                    'documents': len(set([e.document_ids for e in graph.entities]))
                }
            except Exception as e:
                stats[branch] = {'error': str(e)}
        
        return stats

# Usage example
if __name__ == "__main__":
    # Initialize optimized graph manager
    graph_manager = OptimizedECSSGraphManager()
    
    # Example: Create focused graphs
    # doc_ids = ["doc1", "doc2", "doc3"]  # Your document IDs
    # created_graphs = graph_manager.create_focused_graphs(doc_ids)
    
    # Example: Query with adaptive settings
    # result = graph_manager.query_with_adaptive_settings(
    #     "What are the quality requirements for space systems?",
    #     branch="Q"
    # )
    
    # Example: Get statistics
    # stats = graph_manager.get_graph_statistics()
    # print(stats) 