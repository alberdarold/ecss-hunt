
import sys

# Add backend root to path


#!/usr/bin/env python3
"""
ECSS-Specific Graph Prompts and Utilities for Morphik Knowledge Graphs.
Provides custom entity extraction, resolution, and graph creation logic for ECSS standards.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

ECSS-Specific Graph Prompts and Utilities for Morphik Knowledge Graphs.
Provides custom entity extraction, resolution, and graph creation logic for ECSS standards.
"""
import logging
from typing import Optional, Dict, List

from morphik.models import (
    EntityExtractionExample, 
    EntityResolutionExample,
    EntityExtractionPromptOverride, 
    EntityResolutionPromptOverride,
    GraphPromptOverrides
)
# Import Pydantic models and utility from the central schema definition file
from core.schemas import BaseModel, Field, dict_to_model

logger = logging.getLogger(__name__)

#<editor-fold desc="Entity Extraction and Resolution Examples">
def get_ecss_entity_extraction_examples() -> list[EntityExtractionExample]:
    """Get ECSS-specific entity extraction examples."""
    return [
        EntityExtractionExample(label="ECSS-E-ST-10C", type="STANDARD", properties={"branch": "E", "discipline": "Engineering", "document_type": "ST", "revision": "Rev.1"}),
        EntityExtractionExample(label="ECSS-M-ST-10C", type="STANDARD", properties={"branch": "M", "discipline": "Management", "document_type": "ST", "revision": "Rev.1"}),
        EntityExtractionExample(label="Spacecraft", type="SYSTEM", properties={"category": "space_system", "domain": "space_engineering"}),
        EntityExtractionExample(label="Launch Vehicle", type="SYSTEM", properties={"category": "launch_system", "domain": "space_engineering"}),
        EntityExtractionExample(label="Functional Requirement", type="REQUIREMENT", properties={"requirement_type": "functional", "priority": "mandatory"}),
        EntityExtractionExample(label="Performance Requirement", type="REQUIREMENT", properties={"requirement_type": "performance", "priority": "mandatory"}),
        EntityExtractionExample(label="Thermal Control", type="DISCIPLINE", properties={"domain": "engineering", "specialization": "thermal"}),
        EntityExtractionExample(label="Structural Analysis", type="DISCIPLINE", properties={"domain": "engineering", "specialization": "structural"}),
        EntityExtractionExample(label="Test Verification", type="VERIFICATION_METHOD", properties={"method_type": "test", "category": "verification"}),
        EntityExtractionExample(label="Analysis Verification", type="VERIFICATION_METHOD", properties={"method_type": "analysis", "category": "verification"}),
        EntityExtractionExample(label="Phase A", type="PROJECT_PHASE", properties={"phase_type": "preliminary_design", "order": 1}),
        EntityExtractionExample(label="Phase B", type="PROJECT_PHASE", properties={"phase_type": "detailed_design", "order": 2}),
        EntityExtractionExample(label="Quality Assurance", type="PROCESS", properties={"process_type": "assurance", "domain": "quality"}),
        EntityExtractionExample(label="Configuration Management", type="PROCESS", properties={"process_type": "management", "domain": "configuration"})
    ]

def get_ecss_entity_resolution_examples() -> list[EntityResolutionExample]:
    """Get ECSS-specific entity resolution examples."""
    return [
        EntityResolutionExample(canonical="ECSS-E-ST-10C", variants=["ECSS-E-ST-10C Rev.1", "ECSS-E-ST-10C Revision 1", "ECSS-E-ST-10C (15February2017)", "ECSS-E-ST-10C-Rev.1(15February2017)"]),
        EntityResolutionExample(canonical="ECSS-M-ST-10C", variants=["ECSS-M-ST-10C Rev.1", "ECSS-M-ST-10C Revision 1", "Management Standard 10C"]),
        EntityResolutionExample(canonical="Spacecraft", variants=["space vehicle", "satellite", "orbital vehicle", "space system"]),
        EntityResolutionExample(canonical="Launch Vehicle", variants=["launcher", "rocket", "launch system", "propulsion system"]),
        EntityResolutionExample(canonical="Functional Requirement", variants=["functional req", "function requirement", "functional specification", "functional need"]),
        EntityResolutionExample(canonical="Performance Requirement", variants=["performance req", "performance specification", "performance criteria", "performance need"]),
        EntityResolutionExample(canonical="Thermal Control", variants=["thermal management", "thermal engineering", "temperature control", "thermal analysis"]),
        EntityResolutionExample(canonical="Structural Analysis", variants=["structural engineering", "structural design", "mechanical analysis", "structural integrity"]),
        EntityResolutionExample(canonical="Test Verification", variants=["testing", "test method", "experimental verification", "test validation"]),
        EntityResolutionExample(canonical="Analysis Verification", variants=["analysis", "analytical method", "analytical verification", "verification by analysis"]),
        EntityResolutionExample(canonical="Phase A", variants=["Phase-A", "Preliminary Design Phase", "Feasibility Study"]),
        EntityResolutionExample(canonical="Phase B", variants=["Phase-B", "Detailed Design Phase", "Preliminary Definition Phase"]),
        EntityResolutionExample(canonical="Quality Assurance", variants=["QA", "quality control", "product assurance"]),
        EntityResolutionExample(canonical="Configuration Management", variants=["CM", "config management", "change management"])
    ]
#</editor-fold>

#<editor-fold desc="Prompt Override Definitions">
def get_ecss_entity_extraction_prompt() -> str:
    """Get the ECSS-specific entity extraction prompt."""
    return """
    You are an expert in European Cooperation for Space Standardization (ECSS) documents.
    Your task is to extract entities from the provided text based on the ECSS system.
    Focus on identifying:
    - Standard document identifiers (e.g., ECSS-E-ST-10C)
    - Technical terms, systems, and components (e.g., Spacecraft, Solar Panel)
    - Requirements, specifications, and their unique IDs
    - Engineering disciplines (e.g., Thermal Control, Structural Analysis)
    - Verification and validation methods (e.g., Test, Analysis, Inspection)
    - Project management concepts (e.g., Project Phases, Quality Assurance)
    - Materials, processes, and standards mentioned in the text.
    - Acronyms and their definitions (e.g., ESA for European Space Agency).
    
    Assign appropriate types and properties to each entity based on the examples provided.
    Be precise and thorough in your extraction.
"""
import logging
from typing import Optional, Dict, List

from morphik.models import (
    EntityExtractionExample, 
    EntityResolutionExample,
    EntityExtractionPromptOverride, 
    EntityResolutionPromptOverride,
    GraphPromptOverrides
)
# Import Pydantic models and utility from the central schema definition file
from core.schemas import BaseModel, Field, dict_to_model

logger = logging.getLogger(__name__)

#<editor-fold desc="Entity Extraction and Resolution Examples">
def get_ecss_entity_extraction_examples() -> list[EntityExtractionExample]:
    """Get ECSS-specific entity extraction examples."""
    return [
        EntityExtractionExample(label="ECSS-E-ST-10C", type="STANDARD", properties={"branch": "E", "discipline": "Engineering", "document_type": "ST", "revision": "Rev.1"}),
        EntityExtractionExample(label="ECSS-M-ST-10C", type="STANDARD", properties={"branch": "M", "discipline": "Management", "document_type": "ST", "revision": "Rev.1"}),
        EntityExtractionExample(label="Spacecraft", type="SYSTEM", properties={"category": "space_system", "domain": "space_engineering"}),
        EntityExtractionExample(label="Launch Vehicle", type="SYSTEM", properties={"category": "launch_system", "domain": "space_engineering"}),
        EntityExtractionExample(label="Functional Requirement", type="REQUIREMENT", properties={"requirement_type": "functional", "priority": "mandatory"}),
        EntityExtractionExample(label="Performance Requirement", type="REQUIREMENT", properties={"requirement_type": "performance", "priority": "mandatory"}),
        EntityExtractionExample(label="Thermal Control", type="DISCIPLINE", properties={"domain": "engineering", "specialization": "thermal"}),
        EntityExtractionExample(label="Structural Analysis", type="DISCIPLINE", properties={"domain": "engineering", "specialization": "structural"}),
        EntityExtractionExample(label="Test Verification", type="VERIFICATION_METHOD", properties={"method_type": "test", "category": "verification"}),
        EntityExtractionExample(label="Analysis Verification", type="VERIFICATION_METHOD", properties={"method_type": "analysis", "category": "verification"}),
        EntityExtractionExample(label="Phase A", type="PROJECT_PHASE", properties={"phase_type": "preliminary_design", "order": 1}),
        EntityExtractionExample(label="Phase B", type="PROJECT_PHASE", properties={"phase_type": "detailed_design", "order": 2}),
        EntityExtractionExample(label="Quality Assurance", type="PROCESS", properties={"process_type": "assurance", "domain": "quality"}),
        EntityExtractionExample(label="Configuration Management", type="PROCESS", properties={"process_type": "management", "domain": "configuration"})
    ]

def get_ecss_entity_resolution_examples() -> list[EntityResolutionExample]:
    """Get ECSS-specific entity resolution examples."""
    return [
        EntityResolutionExample(canonical="ECSS-E-ST-10C", variants=["ECSS-E-ST-10C Rev.1", "ECSS-E-ST-10C Revision 1", "ECSS-E-ST-10C (15February2017)", "ECSS-E-ST-10C-Rev.1(15February2017)"]),
        EntityResolutionExample(canonical="ECSS-M-ST-10C", variants=["ECSS-M-ST-10C Rev.1", "ECSS-M-ST-10C Revision 1", "Management Standard 10C"]),
        EntityResolutionExample(canonical="Spacecraft", variants=["space vehicle", "satellite", "orbital vehicle", "space system"]),
        EntityResolutionExample(canonical="Launch Vehicle", variants=["launcher", "rocket", "launch system", "propulsion system"]),
        EntityResolutionExample(canonical="Functional Requirement", variants=["functional req", "function requirement", "functional specification", "functional need"]),
        EntityResolutionExample(canonical="Performance Requirement", variants=["performance req", "performance specification", "performance criteria", "performance need"]),
        EntityResolutionExample(canonical="Thermal Control", variants=["thermal management", "thermal engineering", "temperature control", "thermal analysis"]),
        EntityResolutionExample(canonical="Structural Analysis", variants=["structural engineering", "structural design", "mechanical analysis", "structural integrity"]),
        EntityResolutionExample(canonical="Test Verification", variants=["testing", "test method", "experimental verification", "test validation"]),
        EntityResolutionExample(canonical="Analysis Verification", variants=["analysis", "analytical method", "analytical verification", "verification by analysis"]),
        EntityResolutionExample(canonical="Phase A", variants=["Phase-A", "Preliminary Design Phase", "Feasibility Study"]),
        EntityResolutionExample(canonical="Phase B", variants=["Phase-B", "Detailed Design Phase", "Preliminary Definition Phase"]),
        EntityResolutionExample(canonical="Quality Assurance", variants=["QA", "quality control", "product assurance"]),
        EntityResolutionExample(canonical="Configuration Management", variants=["CM", "config management", "change management"])
    ]
#</editor-fold>

#<editor-fold desc="Prompt Override Definitions">
def get_ecss_entity_extraction_prompt() -> str:
    """Get the ECSS-specific entity extraction prompt."""
    return """
    You are an expert in European Cooperation for Space Standardization (ECSS) documents.
    Your task is to extract entities from the provided text based on the ECSS system.
    Focus on identifying:
    - Standard document identifiers (e.g., ECSS-E-ST-10C)
    - Technical terms, systems, and components (e.g., Spacecraft, Solar Panel)
    - Requirements, specifications, and their unique IDs
    - Engineering disciplines (e.g., Thermal Control, Structural Analysis)
    - Verification and validation methods (e.g., Test, Analysis, Inspection)
    - Project management concepts (e.g., Project Phases, Quality Assurance)
    - Materials, processes, and standards mentioned in the text.
    - Acronyms and their definitions (e.g., ESA for European Space Agency).
    
    Assign appropriate types and properties to each entity based on the examples provided.
    Be precise and thorough in your extraction.
"""

def get_ecss_entity_resolution_prompt() -> str:
    """Get the ECSS-specific entity resolution prompt."""
    return """
    You are an expert in resolving entity variations within ECSS documents.
    Your task is to merge different textual representations of the same underlying entity.
    Common variations include:
    - Document revisions and dates (e.g., "ECSS-E-ST-32-02C" and "ECSS-E-ST-32-02C Rev.1")
    - Acronyms and full names (e.g., "ESA" and "European Space Agency")
    - Technical synonyms (e.g., "spacecraft" and "satellite")
    - Variations in terminology (e.g., "thermal analysis" and "thermal control")
    
    Use the provided examples to guide your resolution. The canonical form should be the most common or official representation.
    """

def create_ecss_graph_prompts() -> GraphPromptOverrides:
    """Create a set of general ECSS prompt overrides."""
    return GraphPromptOverrides(
        entity_extraction=EntityExtractionPromptOverride(
            prompt=get_ecss_entity_extraction_prompt(),
            examples=get_ecss_entity_extraction_examples()
        ),
        entity_resolution=EntityResolutionPromptOverride(
            prompt=get_ecss_entity_resolution_prompt(),
            examples=get_ecss_entity_resolution_examples()
        )
    )

def create_branch_specific_graph_prompts(branch: str) -> GraphPromptOverrides:
    """Create prompt overrides tailored to a specific ECSS branch."""
    # This is a placeholder for more specific branch logic if needed in the future.
    # For now, it uses the general ECSS prompts which are robust enough.
    logger.info(f"Using general ECSS graph prompts for {branch}-branch.")
    return create_ecss_graph_prompts()
#</editor-fold>

#<editor-fold desc="Graph Creation Functions">
def create_branch_knowledge_graph(db, branch: str, documents: list) -> Optional[Dict]:
    """Creates a knowledge graph for a specific ECSS branch using a list of documents and a custom Pydantic schema."""
    graph_name = f"ecss_{branch.lower()}_branch_enhanced"
    
    class Requirement(BaseModel):
        id: str = Field(..., description="Unique identifier for the requirement, e.g., 'ECSS-E-ST-10-04C-5.2.1a'")
        text: str = Field(..., description="The full text of the requirement.")
        parentId: Optional[str] = Field(None, description="The ID of the parent requirement, if any.")

    class Verification(BaseModel):
        id: str = Field(..., description="Unique identifier for the verification method.")
        method: str = Field(..., description="The verification method (e.g., 'Test', 'Analysis', 'Inspection', 'Review-of-Design').")
        requirementId: str = Field(..., description="The ID of the requirement this verification applies to.")

    try:
        logger.info(f"Creating enhanced knowledge graph '{graph_name}' for {branch}-branch...")
        graph = db.create_graph(
            name=graph_name,
            documents=documents,
            model_json_schema=dict_to_model({"Requirement": Requirement, "Verification": Verification}),
            rebuild_if_exists=True,
        )
        return graph
    except Exception as e:
        logger.error(f"Failed to create {branch}-branch knowledge graph: {e}", exc_info=True)
        return None

def create_ecss_knowledge_graph(db, name: str, documents: list) -> Optional[Dict]:
    """Creates a general ECSS knowledge graph from a list of documents."""
    class Standard(BaseModel):
        id: str = Field(..., description="Unique identifier for the standard, e.g., 'ECSS-E-ST-10C'")
        title: str = Field(..., description="The official title of the standard.")
        branch: str = Field(..., description="The ECSS branch (E, M, Q, P).")
        discipline: str = Field(..., description="The primary discipline of the standard.")

    class Topic(BaseModel):
        id: str = Field(..., description="A unique, lower-case, snake_case identifier for the topic.")
        name: str = Field(..., description="The name of the key topic or concept discussed.")

    prompt = """
    Generate a high-level knowledge graph from the provided ECSS standard documents.
    Your goal is to identify the main topics covered by each standard.
    - For each document, create a single 'Standard' entity with its ID, title, branch, and discipline.
    - Identify the 5-7 most important technical topics or concepts in the document (e.g., 'Structural Analysis', 'Software Development', 'Quality Assurance') and create a 'Topic' entity for each.
    - Link each 'Standard' entity to its relevant 'Topic' entities using a 'COVERS' relationship.
    """

    try:
        logger.info(f"Creating general ECSS knowledge graph '{name}'...")
        graph = db.create_graph(
            name=name,
            documents=documents,
            model_json_schema=dict_to_model({"Standard": Standard, "Topic": Topic}),
            rebuild_if_exists=True,
        )
        return graph
    except Exception as e:
        logger.error(f"Failed to create ECSS knowledge graph '{name}': {e}", exc_info=True)
        return None
#</editor-fold>

# ============================================================================
# Testing Functions
# ============================================================================

def test_ecss_graph_prompts():
    """Test ECSS graph prompt creation."""
    print("🧪 Testing ECSS Graph Prompts...")
    
    try:
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test prompt templates
        extraction_prompt = get_ecss_entity_extraction_prompt()
        resolution_prompt = get_ecss_entity_resolution_prompt()
        
        print(f"✅ Extraction prompt length: {len(extraction_prompt)} characters")
        print(f"✅ Resolution prompt length: {len(resolution_prompt)} characters")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created graph prompt overrides")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ ECSS graph prompts test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ecss_graph_prompts()
    if success:
        print("🎉 ECSS Graph Prompts ready for use!")
    else:
        print("⚠ ECSS Graph Prompts test failed!") 

def get_ecss_entity_resolution_prompt() -> str:
    """Get the ECSS-specific entity resolution prompt."""
    return """
    You are an expert in resolving entity variations within ECSS documents.
    Your task is to merge different textual representations of the same underlying entity.
    Common variations include:
    - Document revisions and dates (e.g., "ECSS-E-ST-32-02C" and "ECSS-E-ST-32-02C Rev.1")
    - Acronyms and full names (e.g., "ESA" and "European Space Agency")
    - Technical synonyms (e.g., "spacecraft" and "satellite")
    - Variations in terminology (e.g., "thermal analysis" and "thermal control")
    
    Use the provided examples to guide your resolution. The canonical form should be the most common or official representation.
    """

def create_ecss_graph_prompts() -> GraphPromptOverrides:
    """Create a set of general ECSS prompt overrides."""
    return GraphPromptOverrides(
        entity_extraction=EntityExtractionPromptOverride(
            prompt=get_ecss_entity_extraction_prompt(),
            examples=get_ecss_entity_extraction_examples()
        ),
        entity_resolution=EntityResolutionPromptOverride(
            prompt=get_ecss_entity_resolution_prompt(),
            examples=get_ecss_entity_resolution_examples()
        )
    )

def create_branch_specific_graph_prompts(branch: str) -> GraphPromptOverrides:
    """Create prompt overrides tailored to a specific ECSS branch."""
    # This is a placeholder for more specific branch logic if needed in the future.
    # For now, it uses the general ECSS prompts which are robust enough.
    logger.info(f"Using general ECSS graph prompts for {branch}-branch.")
    return create_ecss_graph_prompts()
#</editor-fold>

#<editor-fold desc="Graph Creation Functions">
def create_branch_knowledge_graph(db, branch: str, documents: list) -> Optional[Dict]:
    """Creates a knowledge graph for a specific ECSS branch using a list of documents and a custom Pydantic schema."""
    graph_name = f"ecss_{branch.lower()}_branch_enhanced"
    
    class Requirement(BaseModel):
        id: str = Field(..., description="Unique identifier for the requirement, e.g., 'ECSS-E-ST-10-04C-5.2.1a'")
        text: str = Field(..., description="The full text of the requirement.")
        parentId: Optional[str] = Field(None, description="The ID of the parent requirement, if any.")

    class Verification(BaseModel):
        id: str = Field(..., description="Unique identifier for the verification method.")
        method: str = Field(..., description="The verification method (e.g., 'Test', 'Analysis', 'Inspection', 'Review-of-Design').")
        requirementId: str = Field(..., description="The ID of the requirement this verification applies to.")

    try:
        logger.info(f"Creating enhanced knowledge graph '{graph_name}' for {branch}-branch...")
        graph = db.create_graph(
            name=graph_name,
            documents=documents,
            model_json_schema=dict_to_model({"Requirement": Requirement, "Verification": Verification}),
            rebuild_if_exists=True,
        )
        return graph
    except Exception as e:
        logger.error(f"Failed to create {branch}-branch knowledge graph: {e}", exc_info=True)
        return None

def create_ecss_knowledge_graph(db, name: str, documents: list) -> Optional[Dict]:
    """Creates a general ECSS knowledge graph from a list of documents."""
    class Standard(BaseModel):
        id: str = Field(..., description="Unique identifier for the standard, e.g., 'ECSS-E-ST-10C'")
        title: str = Field(..., description="The official title of the standard.")
        branch: str = Field(..., description="The ECSS branch (E, M, Q, P).")
        discipline: str = Field(..., description="The primary discipline of the standard.")

    class Topic(BaseModel):
        id: str = Field(..., description="A unique, lower-case, snake_case identifier for the topic.")
        name: str = Field(..., description="The name of the key topic or concept discussed.")

    prompt = """
    Generate a high-level knowledge graph from the provided ECSS standard documents.
    Your goal is to identify the main topics covered by each standard.
    - For each document, create a single 'Standard' entity with its ID, title, branch, and discipline.
    - Identify the 5-7 most important technical topics or concepts in the document (e.g., 'Structural Analysis', 'Software Development', 'Quality Assurance') and create a 'Topic' entity for each.
    - Link each 'Standard' entity to its relevant 'Topic' entities using a 'COVERS' relationship.
    """

    try:
        logger.info(f"Creating general ECSS knowledge graph '{name}'...")
        graph = db.create_graph(
            name=name,
            documents=documents,
            model_json_schema=dict_to_model({"Standard": Standard, "Topic": Topic}),
            rebuild_if_exists=True,
        )
        return graph
    except Exception as e:
        logger.error(f"Failed to create ECSS knowledge graph '{name}': {e}", exc_info=True)
        return None
#</editor-fold>

# ============================================================================
# Testing Functions
# ============================================================================

def test_ecss_graph_prompts():
    """Test ECSS graph prompt creation."""
    print("🧪 Testing ECSS Graph Prompts...")
    
    try:
        # Test entity extraction examples
        extraction_examples = get_ecss_entity_extraction_examples()
        print(f"✅ Created {len(extraction_examples)} entity extraction examples")
        
        # Test entity resolution examples
        resolution_examples = get_ecss_entity_resolution_examples()
        print(f"✅ Created {len(resolution_examples)} entity resolution examples")
        
        # Test prompt templates
        extraction_prompt = get_ecss_entity_extraction_prompt()
        resolution_prompt = get_ecss_entity_resolution_prompt()
        
        print(f"✅ Extraction prompt length: {len(extraction_prompt)} characters")
        print(f"✅ Resolution prompt length: {len(resolution_prompt)} characters")
        
        # Test graph prompt overrides
        graph_prompts = create_ecss_graph_prompts()
        print(f"✅ Created graph prompt overrides")
        
        # Test branch-specific prompts
        for branch in ['E', 'M', 'P', 'Q']:
            branch_prompts = create_branch_specific_graph_prompts(branch)
            print(f"✅ Created {branch}-branch specific prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ ECSS graph prompts test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ecss_graph_prompts()
    if success:
        print("🎉 ECSS Graph Prompts ready for use!")
    else:
        print("⚠ ECSS Graph Prompts test failed!") 