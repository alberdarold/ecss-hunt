
import sys

# Add backend root to path


# Enhanced ECSS Document Extraction Prompt
# Comprehensive prompt for extracting all entity types and relationships from ECSS standards

ENHANCED_EXTRACTION_PROMPT = """From the provided text from an ECSS standard, extract the following information to build a comprehensive knowledge graph:

## ENTITIES TO EXTRACT:

### 1. Standard
- **name**: Full identifier (e.g., "ECSS-Q-ST-70C")
- **category**: ECSS category (S=System, E=Engineering, Q=Quality, M=Management)
- **version**: Version/revision (e.g., "Rev.1", "C")
- **title**: Full document title
- **publication_date**: Publication date if mentioned
- **scope**: Brief description of the standard's scope

### 2. Section
- **section_id**: Section identifier (e.g., "4.2", "Chapter 5")
- **title**: Section title
- **level**: Hierarchical level (1=chapter, 2=section, 3=subsection)
- **content_summary**: Brief summary of section content

### 3. Requirement
- **requirement_id**: Section number (e.g., "5.2.1a")
- **text**: Full requirement text
- **level**: Requirement level ("shall", "should", "may", "can")
- **parent_section**: Parent section number (e.g., "5.2")
- **compliance_category**: "mandatory", "recommended", or "optional"
- **verification_method**: "test", "analysis", "inspection", or "demonstration"

### 4. Definition
- **term**: The term being defined
- **definition**: The definition text
- **context**: Context where definition applies
- **source**: Source if referenced

### 5. Procedure
- **procedure_id**: Unique identifier
- **title**: Procedure title
- **description**: Procedure description
- **steps**: List of procedure steps
- **purpose**: Purpose of the procedure

### 6. Table
- **table_id**: Table identifier (e.g., "Table 4-1")
- **title**: Table title
- **content**: Table content
- **table_type**: "data", "comparison", "reference", or "summary"

### 7. Diagram
- **figure_id**: Figure identifier (e.g., "Figure 4-1")
- **caption**: Figure caption
- **content_type**: "diagram", "flowchart", "table", "image", or "graph"
- **purpose**: Purpose of the diagram

### 8. TechnicalConcept
- **concept_name**: Name of technical concept
- **description**: Description of concept
- **category**: "material", "component", "system", "process", or "method"
- **specifications**: Technical specifications if applicable

### 9. CrossReference
- **reference_id**: Unique identifier
- **source_text**: Text containing the reference
- **target_type**: "requirement", "section", "table", or "figure"
- **target_id**: ID of target being referenced

## RELATIONSHIPS TO CREATE:

### Hierarchical Relationships:
1. **HasSection**: Standard → Section
2. **ContainsRequirement**: Section → Requirement
3. **SubsectionOf**: Section → Section (hierarchical)
4. **Contains**: Standard → Section/Diagram/Table/Definition

### Content Relationships:
5. **Specifies**: Standard → Requirement
6. **Defines**: Standard/Section → Definition
7. **Describes**: Section → Procedure
8. **ContainsTable**: Section → Table
9. **ContainsDiagram**: Section → Diagram

### Reference Relationships:
10. **References**: Requirement/Section/Procedure → Standard (external)
11. **CrossReferences**: CrossReference → Requirement/Section/Table/Diagram (internal)
12. **Illustrates**: Diagram → Requirement/Procedure/TechnicalConcept

### Functional Relationships:
13. **Uses**: Requirement/Procedure → TechnicalConcept
14. **Implements**: Procedure → Requirement
15. **Verifies**: Procedure → Requirement
16. **RelatedTo**: TechnicalConcept/Requirement → TechnicalConcept/Requirement
17. **DependsOn**: Requirement/Procedure → Requirement/Procedure
18. **CompliesWith**: Requirement/Procedure → Standard/Requirement

## EXTRACTION GUIDELINES:

### For Requirements:
- Identify requirement levels: "shall" (mandatory), "should" (recommended), "may" (optional), "can" (permitted)
- Extract verification methods mentioned in the text
- Note parent sections for hierarchical organization

### For Sections:
- Maintain hierarchical structure (chapters → sections → subsections)
- Extract section titles and summaries
- Identify content types within sections

### For Definitions:
- Look for terms in bold, italics, or quotation marks
- Extract formal definitions and informal explanations
- Note the context where definitions apply

### For Procedures:
- Identify step-by-step processes
- Extract procedure titles and purposes
- Note which requirements they implement or verify

### For Tables:
- Extract table titles and content
- Classify table types based on content
- Note relationships to surrounding text

### For Diagrams:
- Extract figure numbers and captions
- Classify content types (diagram, flowchart, etc.)
- Identify what the diagram illustrates

### For Technical Concepts:
- Identify materials, components, systems, processes, methods
- Extract technical specifications
- Note relationships to requirements and procedures

### For Cross-References:
- Identify internal references (e.g., "see Section 4.2", "refer to Table 3-1")
- Extract source text and target information
- Maintain reference integrity

## SPECIAL CONSIDERATIONS:

1. **Compliance Tracking**: Pay special attention to requirement levels for compliance tracking
2. **Verification Methods**: Extract how requirements are verified (test, analysis, inspection, demonstration)
3. **Dependencies**: Identify requirement and procedure dependencies
4. **Cross-References**: Track both internal and external references
5. **Hierarchical Structure**: Maintain document structure and relationships
6. **Technical Accuracy**: Preserve technical specifications and relationships

## OUTPUT FORMAT:
For each entity found, extract all available properties. For each relationship, identify the source and target entities with their types. Ensure all relationships are properly typed and connected to valid entities.
"""

# Simplified prompt for initial testing
CORE_EXTRACTION_PROMPT = """From the provided text from an ECSS standard, extract the following information to build a knowledge graph:

## CORE ENTITIES:

### 1. Standard
- **name**: Full identifier (e.g., "ECSS-Q-ST-70C")
- **category**: ECSS category (S=System, E=Engineering, Q=Quality, M=Management)
- **version**: Version/revision (e.g., "Rev.1", "C")
- **title**: Full document title

### 2. Section
- **section_id**: Section identifier (e.g., "4.2", "Chapter 5")
- **title**: Section title
- **level**: Hierarchical level (1=chapter, 2=section, 3=subsection)

### 3. Requirement
- **requirement_id**: Section number (e.g., "5.2.1a")
- **text**: Full requirement text
- **level**: Requirement level ("shall", "should", "may", "can")
- **parent_section**: Parent section number (e.g., "5.2")

### 4. Definition
- **term**: The term being defined
- **definition**: The definition text

### 5. Diagram
- **figure_id**: Figure identifier (e.g., "Figure 4-1")
- **caption**: Figure caption
- **content_type**: "diagram", "flowchart", "table", "image", or "graph"

## CORE RELATIONSHIPS:

1. **HasSection**: Standard → Section
2. **ContainsRequirement**: Section → Requirement
3. **Specifies**: Standard → Requirement
4. **Defines**: Standard/Section → Definition
5. **ContainsDiagram**: Section → Diagram
6. **References**: Requirement/Section → Standard
7. **Illustrates**: Diagram → Requirement

## EXTRACTION FOCUS:
- Identify requirement levels (shall/should/may/can)
- Extract section hierarchy
- Find definitions and technical terms
- Identify diagrams and their purposes
- Note cross-references between standards
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


# Simplified prompt for initial testing
CORE_EXTRACTION_PROMPT = """From the provided text from an ECSS standard, extract the following information to build a knowledge graph:

## CORE ENTITIES:

### 1. Standard
- **name**: Full identifier (e.g., "ECSS-Q-ST-70C")
- **category**: ECSS category (S=System, E=Engineering, Q=Quality, M=Management)
- **version**: Version/revision (e.g., "Rev.1", "C")
- **title**: Full document title

### 2. Section
- **section_id**: Section identifier (e.g., "4.2", "Chapter 5")
- **title**: Section title
- **level**: Hierarchical level (1=chapter, 2=section, 3=subsection)

### 3. Requirement
- **requirement_id**: Section number (e.g., "5.2.1a")
- **text**: Full requirement text
- **level**: Requirement level ("shall", "should", "may", "can")
- **parent_section**: Parent section number (e.g., "5.2")

### 4. Definition
- **term**: The term being defined
- **definition**: The definition text

### 5. Diagram
- **figure_id**: Figure identifier (e.g., "Figure 4-1")
- **caption**: Figure caption
- **content_type**: "diagram", "flowchart", "table", "image", or "graph"

## CORE RELATIONSHIPS:

1. **HasSection**: Standard → Section
2. **ContainsRequirement**: Section → Requirement
3. **Specifies**: Standard → Requirement
4. **Defines**: Standard/Section → Definition
5. **ContainsDiagram**: Section → Diagram
6. **References**: Requirement/Section → Standard
7. **Illustrates**: Diagram → Requirement

## EXTRACTION FOCUS:
- Identify requirement levels (shall/should/may/can)
- Extract section hierarchy
- Find definitions and technical terms
- Identify diagrams and their purposes
- Note cross-references between standards
"""

# Entity extraction examples for better recognition
ENHANCED_EXTRACTION_EXAMPLES = [
    {
        "label": "ECSS-Q-ST-70C",
        "type": "Standard",
        "properties": {
            "category": "Q",
            "version": "C",
            "title": "Materials, mechanical parts and processes"
        }
    },
    {
        "label": "4.2.1a",
        "type": "Requirement",
        "properties": {
            "text": "The system shall provide a telemetry link.",
            "level": "shall",
            "parent_section": "4.2"
        }
    },
    {
        "label": "Figure 4-1",
        "type": "Diagram",
        "properties": {
            "caption": "System architecture diagram",
            "content_type": "diagram"
        }
    },
    {
        "label": "telemetry",
        "type": "Definition",
        "properties": {
            "definition": "The process of recording and transmitting data from remote sources"
        }
    },
    {
        "label": "4.2",
        "type": "Section",
        "properties": {
            "title": "Telemetry Requirements",
            "level": 2
        }
    }
] 

# Entity extraction examples for better recognition
ENHANCED_EXTRACTION_EXAMPLES = [
    {
        "label": "ECSS-Q-ST-70C",
        "type": "Standard",
        "properties": {
            "category": "Q",
            "version": "C",
            "title": "Materials, mechanical parts and processes"
        }
    },
    {
        "label": "4.2.1a",
        "type": "Requirement",
        "properties": {
            "text": "The system shall provide a telemetry link.",
            "level": "shall",
            "parent_section": "4.2"
        }
    },
    {
        "label": "Figure 4-1",
        "type": "Diagram",
        "properties": {
            "caption": "System architecture diagram",
            "content_type": "diagram"
        }
    },
    {
        "label": "telemetry",
        "type": "Definition",
        "properties": {
            "definition": "The process of recording and transmitting data from remote sources"
        }
    },
    {
        "label": "4.2",
        "type": "Section",
        "properties": {
            "title": "Telemetry Requirements",
            "level": 2
        }
    }
] 