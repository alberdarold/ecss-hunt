from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


import sys

# Add backend root to path


from morphik.models import Entity, Relationship
from pydantic import BaseModel, Field
from typing import List, Optional

# Enhanced ECSS Knowledge Graph Schema
# Captures the full richness of ECSS document structure

class Standard(Entity):
    """A single ECSS standard document."""
    name: str = Field(description="The full identifier of the standard, e.g., 'ECSS-S-ST-00C'.")
    category: str = Field(description="The ECSS category: S (System), E (Engineering), Q (Quality), M (Management)")
    version: str = Field(description="The version/revision of the standard, e.g., 'Rev.1', 'C'")
    title: str = Field(description="The full title of the standard document")
    publication_date: str = Field(description="Publication date of the standard")
    scope: str = Field(description="Brief description of the standard's scope")

class Section(Entity):
    """A section or chapter within an ECSS standard."""
    section_id: str = Field(description="The section identifier, e.g., '4.2', 'Chapter 5'")
    title: str = Field(description="The title of the section")
    level: int = Field(description="Hierarchical level: 1=chapter, 2=section, 3=subsection, etc.")
    content_summary: str = Field(description="Brief summary of the section content")

class Requirement(Entity):
    """A specific, numbered requirement within an ECSS standard."""
    requirement_id: str = Field(description="The identifier for the requirement, e.g., '4.2.1a'.")
    text: str = Field(description="The full text of the requirement.")
    level: str = Field(description="The requirement level: 'shall', 'should', 'may', 'can'")
    parent_section: str = Field(description="The parent section number, e.g., '4.2'")
    compliance_category: str = Field(description="Compliance category: 'mandatory', 'recommended', 'optional'")
    verification_method: str = Field(description="How this requirement is verified: 'test', 'analysis', 'inspection', 'demonstration'")

class Definition(Entity):
    """A definition or term within an ECSS standard."""
    term: str = Field(description="The term being defined")
    definition: str = Field(description="The definition of the term")
    context: str = Field(description="Context where this definition applies")
    source: str = Field(description="Source of the definition if referenced")

class Procedure(Entity):
    """A procedure, process, or method described in the standard."""
    procedure_id: str = Field(description="Unique identifier for the procedure")
    title: str = Field(description="Title of the procedure")
    description: str = Field(description="Description of the procedure")
    steps: List[str] = Field(description="List of procedure steps")
    purpose: str = Field(description="Purpose of the procedure")

class Table(Entity):
    """A table within an ECSS standard."""
    table_id: str = Field(description="Table identifier, e.g., 'Table 4-1'")
    title: str = Field(description="Title of the table")
    content: str = Field(description="Content of the table")
    table_type: str = Field(description="Type of table: 'data', 'comparison', 'reference', 'summary'")

class Diagram(Entity):
    """A diagram, figure, or image within an ECSS standard."""
    figure_id: str = Field(description="The figure identifier, e.g., 'Figure 4-1'")
    caption: str = Field(description="The caption or description of the diagram")
    content_type: str = Field(description="Type of content: 'diagram', 'flowchart', 'table', 'image', 'graph'")
    purpose: str = Field(description="Purpose of the diagram")

class TechnicalConcept(Entity):
    """A technical concept, material, or component mentioned in the standard."""
    concept_name: str = Field(description="Name of the technical concept")
    description: str = Field(description="Description of the concept")
    category: str = Field(description="Category: 'material', 'component', 'system', 'process', 'method'")
    specifications: str = Field(description="Technical specifications if applicable")

class CrossReference(Entity):
    """An internal cross-reference within a document."""
    reference_id: str = Field(description="Unique identifier for the reference")
    source_text: str = Field(description="Text that contains the reference")
    target_type: str = Field(description="Type of target: 'requirement', 'section', 'table', 'figure'")
    target_id: str = Field(description="ID of the target being referenced")

# Enhanced Relationships

class Specifies(Relationship):
    """Indicates that a standard specifies a particular requirement."""
    source: Standard
    target: Requirement

class Contains(Relationship):
    """Indicates that a standard contains a section, diagram, table, etc."""
    source: Standard
    target: Section | Diagram | Table | Definition

class HasSection(Relationship):
    """Indicates that a standard has a specific section."""
    source: Standard
    target: Section

class ContainsRequirement(Relationship):
    """Indicates that a section contains a requirement."""
    source: Section
    target: Requirement

class SubsectionOf(Relationship):
    """Indicates hierarchical structure between sections."""
    source: Section
    target: Section

class Defines(Relationship):
    """Indicates that a standard or section defines a term."""
    source: Standard | Section
    target: Definition

class Describes(Relationship):
    """Indicates that a section describes a procedure."""
    source: Section
    target: Procedure

class ContainsTable(Relationship):
    """Indicates that a section contains a table."""
    source: Section
    target: Table

class ContainsDiagram(Relationship):
    """Indicates that a section contains a diagram."""
    source: Section
    target: Diagram

class References(Relationship):
    """Indicates that one entity references another standard."""
    source: Requirement | Section | Procedure
    target: Standard

class CrossReferences(Relationship):
    """Indicates internal cross-references within a document."""
    source: CrossReference
    target: Requirement | Section | Table | Diagram

class Illustrates(Relationship):
    """Indicates that a diagram illustrates a requirement, procedure, or concept."""
    source: Diagram
    target: Requirement | Procedure | TechnicalConcept

class Uses(Relationship):
    """Indicates that a requirement or procedure uses a technical concept."""
    source: Requirement | Procedure
    target: TechnicalConcept

class Implements(Relationship):
    """Indicates that a procedure implements a requirement."""
    source: Procedure
    target: Requirement

class Verifies(Relationship):
    """Indicates that a procedure verifies a requirement."""
    source: Procedure
    target: Requirement

class RelatedTo(Relationship):
    """Indicates related concepts or requirements."""
    source: TechnicalConcept | Requirement
    target: TechnicalConcept | Requirement

class DependsOn(Relationship):
    """Indicates dependency between requirements or procedures."""
    source: Requirement | Procedure
    target: Requirement | Procedure

class CompliesWith(Relationship):
    """Indicates compliance with another standard or requirement."""
    source: Requirement | Procedure
    target: Standard | Requirement

# Schema for different types of ECSS documents
ECSS_SCHEMA = {
    "System Standards": [Standard, Section, Requirement, Definition, Procedure, Table, Diagram, TechnicalConcept, CrossReference],
    "Engineering Standards": [Standard, Section, Requirement, Definition, Procedure, Table, Diagram, TechnicalConcept, CrossReference],
    "Quality Standards": [Standard, Section, Requirement, Definition, Procedure, Table, Diagram, TechnicalConcept, CrossReference],
    "Management Standards": [Standard, Section, Requirement, Definition, Procedure, Table, Diagram, TechnicalConcept, CrossReference]
}

# All relationships for comprehensive graph
ALL_RELATIONSHIPS = [
    Specifies, Contains, HasSection, ContainsRequirement, SubsectionOf,
    Defines, Describes, ContainsTable, ContainsDiagram, References,
    CrossReferences, Illustrates, Uses, Implements, Verifies,
    RelatedTo, DependsOn, CompliesWith
]

# Core entities for basic functionality
CORE_ENTITIES = [Standard, Requirement, Diagram, Section, Definition]

# Extended entities for comprehensive coverage
EXTENDED_ENTITIES = [Procedure, Table, TechnicalConcept, CrossReference]

# Core relationships for basic functionality
CORE_RELATIONSHIPS = [Specifies, Contains, References, Illustrates, HasSection, ContainsRequirement]

# Extended relationships for comprehensive coverage
EXTENDED_RELATIONSHIPS = [
    SubsectionOf, Defines, Describes, ContainsTable, ContainsDiagram,
    CrossReferences, Uses, Implements, Verifies, RelatedTo, DependsOn, CompliesWith
] 