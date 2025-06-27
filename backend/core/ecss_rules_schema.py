
import sys

# Add backend root to path


#!/usr/bin/env python3
"""
ECSS Rules Schema for Morphik Rules-Based Ingestion
Defines structured schemas and rules for robust ECSS document processing.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

ECSS Rules Schema for Morphik Rules-Based Ingestion
Defines structured schemas and rules for robust ECSS document processing.
"""

from typing import List, Dict, Optional, Any
from core.schemas import BaseModel, Field, NaturalLanguageRule

# ============================================================================
# ECSS Document Metadata Schema
# ============================================================================

class ECSSStandard(BaseModel):
    """Schema for extracting ECSS standard metadata."""
    standard_id: str = Field(description="ECSS standard identifier (e.g., ECSS-E-ST-10C)")
    branch: str = Field(description="ECSS branch (E, M, P, Q)")
    discipline: str = Field(description="ECSS discipline (Engineering, Management, Product Assurance, etc.)")
    title: str = Field(description="Full title of the standard")
    revision: str = Field(description="Revision number (e.g., Rev.1, Rev.2)")
    date: str = Field(description="Publication date")
    status: str = Field(description="Status (Active, Superseded, etc.)")
    scope: str = Field(description="Brief description of the standard's scope")
    keywords: List[str] = Field(description="Key technical terms and concepts")
    applicable_domains: List[str] = Field(description="Space engineering domains this applies to")

class ECSSSection(BaseModel):
    """Schema for extracting section information."""
    section_number: str = Field(description="Section number (e.g., 3.1, 4.2.1)")
    section_title: str = Field(description="Title of the section")
    section_type: str = Field(description="Type of section (normative, informative, annex)")
    content_summary: str = Field(description="Brief summary of section content")
    requirements_count: int = Field(description="Number of requirements in this section")
    figures_count: int = Field(description="Number of figures in this section")
    tables_count: int = Field(description="Number of tables in this section")

class ECSSDefinition(BaseModel):
    """Schema for extracting definitions."""
    term: str = Field(description="The term being defined")
    definition: str = Field(description="The definition of the term")
    context: str = Field(description="Context where this definition is used")
    related_terms: List[str] = Field(description="Related terms or synonyms")
    standard_reference: str = Field(description="Which standard this definition comes from")

class ECSSTable(BaseModel):
    """Schema for extracting table information."""
    table_number: str = Field(description="Table number (e.g., Table 1, Table A.1)")
    table_title: str = Field(description="Title or caption of the table")
    table_type: str = Field(description="Type of table (requirements, parameters, classifications)")
    row_count: int = Field(description="Number of rows in the table")
    column_count: int = Field(description="Number of columns in the table")
    content_summary: str = Field(description="Summary of what the table contains")
    key_parameters: List[str] = Field(description="Key parameters or values in the table")

class ECSSDiagram(BaseModel):
    """Schema for extracting diagram information."""
    figure_number: str = Field(description="Figure number (e.g., Figure 1, Figure A.1)")
    figure_title: str = Field(description="Title or caption of the figure")
    diagram_type: str = Field(description="Type of diagram (flowchart, block diagram, schematic)")
    content_description: str = Field(description="Description of what the diagram shows")
    components: List[str] = Field(description="Key components or elements in the diagram")
    relationships: List[str] = Field(description="Relationships or connections shown")

class ECSSRequirement(BaseModel):
    """Schema for extracting requirements."""
    requirement_id: str = Field(description="Requirement identifier (e.g., REQ-001)")
    requirement_text: str = Field(description="The requirement statement")
    requirement_type: str = Field(description="Type of requirement (functional, performance, interface)")
    priority: str = Field(description="Priority level (mandatory, recommended, optional)")
    verification_method: str = Field(description="How this requirement is verified")
    applicable_phases: List[str] = Field(description="Project phases this applies to")

# ============================================================================
# ECSS Rules Configuration
# ============================================================================

def create_ecss_metadata_rules() -> List[NaturalLanguageRule]:
    """Create comprehensive ECSS metadata extraction rules using NaturalLanguageRule."""
    return [
        NaturalLanguageRule(
            prompt="""Extract comprehensive ECSS standard metadata from the document. Return as JSON with these fields:
- standard_id: ECSS standard identifier (e.g., ECSS-E-ST-10C)
- branch: ECSS branch (E, M, P, Q)
- discipline: ECSS discipline (Engineering, Management, Product Assurance, etc.)
- title: Full title of the standard
- revision: Revision number (e.g., Rev.1, Rev.2)
- date: Publication date
- status: Status (Active, Superseded, etc.)
- scope: Brief description of the standard's scope
- keywords: Array of key technical terms and concepts
- applicable_domains: Array of space engineering domains this applies to

Be precise and extract all available information from the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract section information from the ECSS document. Return as JSON with these fields:
- section_number: Section number (e.g., 3.1, 4.2.1)
- section_title: Title of the section
- section_type: Type of section (normative, informative, annex)
- content_summary: Brief summary of section content
- requirements_count: Number of requirements in this section
- figures_count: Number of figures in this section
- tables_count: Number of tables in this section

Extract information for each major section found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract definitions from the ECSS document. Return as JSON with these fields:
- term: The term being defined
- definition: The definition of the term
- context: Context where this definition is used
- related_terms: Array of related terms or synonyms
- standard_reference: Which standard this definition comes from

Extract all definitions found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract table information from the ECSS document. Return as JSON with these fields:
- table_number: Table number (e.g., Table 1, Table A.1)
- table_title: Title or caption of the table
- table_type: Type of table (requirements, parameters, classifications)
- row_count: Number of rows in the table
- column_count: Number of columns in the table
- content_summary: Summary of what the table contains
- key_parameters: Array of key parameters or values in the table

Extract information for each table found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract diagram and figure information from the ECSS document. Return as JSON with these fields:
- figure_number: Figure number (e.g., Figure 1, Figure A.1)
- figure_title: Title or caption of the figure
- diagram_type: Type of diagram (flowchart, block diagram, schematic)
- content_description: Description of what the diagram shows
- components: Array of key components or elements in the diagram
- relationships: Array of relationships or connections shown

Extract information for each figure or diagram found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract requirements from the ECSS document. Return as JSON with these fields:
- requirement_id: Requirement identifier (e.g., REQ-001)
- requirement_text: The requirement statement
- requirement_type: Type of requirement (functional, performance, interface)
- priority: Priority level (mandatory, recommended, optional)
- verification_method: How this requirement is verified
- applicable_phases: Array of project phases this applies to

Extract all requirements found in the document."""
        )
    ]

def create_ecss_content_rules() -> List[NaturalLanguageRule]:
    """Create ECSS content transformation rules."""
    return [
        NaturalLanguageRule(
            prompt="""Standardize ECSS document formatting:
1. Ensure consistent heading hierarchy (1, 1.1, 1.1.1, etc.)
2. Normalize requirement numbering (REQ-001, REQ-002, etc.)
3. Standardize figure and table references (Figure 1, Table 1, etc.)
4. Ensure consistent terminology usage throughout the document
5. Maintain all technical accuracy and precision
6. Preserve all mathematical formulas and technical specifications
7. Keep all normative content intact"""
        ),
        NaturalLanguageRule(
            prompt="""Enhance ECSS content for better searchability:
1. Add cross-references between related sections
2. Clarify ambiguous technical terms with context
3. Ensure all abbreviations are defined
4. Add implicit relationships between requirements
5. Maintain all original technical content and accuracy
6. Preserve all normative requirements exactly as stated"""
        )
    ]

def create_ecss_quality_rules() -> List[NaturalLanguageRule]:
    """Create ECSS quality assurance rules."""
    return [
        NaturalLanguageRule(
            prompt="""Validate ECSS document quality:
1. Check for missing requirement identifiers
2. Verify figure and table numbering consistency
3. Ensure all referenced terms are defined
4. Validate cross-reference accuracy
5. Check for incomplete requirements
6. Verify normative vs informative content labeling
7. Maintain all original content - only add validation notes"""
        )
    ]

# ============================================================================
# Branch-Specific Rules
# ============================================================================

class EBranchSchema(BaseModel):
    """Engineering branch specific schema."""
    engineering_discipline: str = Field(description="Specific engineering discipline")
    technical_requirement: str = Field(description="Technical requirement details")
    verification_method: str = Field(description="Verification method for engineering requirements")

class MBranchSchema(BaseModel):
    """Management branch specific schema."""
    management_process: str = Field(description="Management process details")
    project_phase: str = Field(description="Project phase information")
    stakeholder: str = Field(description="Stakeholder information")

class PBranchSchema(BaseModel):
    """Product Assurance branch specific schema."""
    assurance_process: str = Field(description="Product assurance process details")
    quality_requirement: str = Field(description="Quality requirement details")
    verification_plan: str = Field(description="Verification planning information")

class QBranchSchema(BaseModel):
    """Quality branch specific schema."""
    quality_process: str = Field(description="Quality process details")
    audit_requirement: str = Field(description="Audit requirement details")
    compliance_check: str = Field(description="Compliance checking information")

def create_e_branch_rules() -> List[NaturalLanguageRule]:
    """Create Engineering branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Engineering branch specific information from the ECSS document. Return as JSON with these fields:
- engineering_discipline: Specific engineering discipline (e.g., Electrical, Mechanical, Software)
- technical_requirement: Technical requirement details
- verification_method: Verification method for engineering requirements

Focus on engineering-specific content and requirements."""
        )
    ]

def create_m_branch_rules() -> List[NaturalLanguageRule]:
    """Create Management branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Management branch specific information from the ECSS document. Return as JSON with these fields:
- management_process: Management process details
- project_phase: Project phase information
- stakeholder: Stakeholder information

Focus on management-specific content and processes."""
        )
    ]

def create_p_branch_rules() -> List[NaturalLanguageRule]:
    """Create Product Assurance branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Product Assurance branch specific information from the ECSS document. Return as JSON with these fields:
- assurance_process: Product assurance process details
- quality_requirement: Quality requirement details
- verification_plan: Verification planning information

Focus on product assurance and quality-specific content."""
        )
    ]

def create_q_branch_rules() -> List[NaturalLanguageRule]:
    """Create Quality branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Quality branch specific information from the ECSS document. Return as JSON with these fields:
- quality_process: Quality process details
- audit_requirement: Audit requirement details
- compliance_check: Compliance checking information

Focus on quality-specific content and processes."""
        )
    ]

# ============================================================================
# Rules Factory Functions
# ============================================================================

def get_ecss_rules_for_branch(branch: str) -> List:
    """Get appropriate rules for a specific ECSS branch."""
    base_rules = create_ecss_metadata_rules() + create_ecss_content_rules()
    
    branch_rules = {
        'E': create_e_branch_rules(),
        'M': create_m_branch_rules(),
        'P': create_p_branch_rules(),
        'Q': create_q_branch_rules()
    }
    
    return base_rules + branch_rules.get(branch.upper(), [])

def get_ecss_rules_for_document_type(doc_type: str) -> List:
    """Get rules optimized for specific document types."""
    if doc_type == "standard":
        return create_ecss_metadata_rules() + create_ecss_content_rules()
    elif doc_type == "handbook":
        return create_ecss_metadata_rules() + create_ecss_quality_rules()
    elif doc_type == "annex":
        return create_ecss_metadata_rules()
    else:
        return create_ecss_metadata_rules() + create_ecss_content_rules()

# ============================================================================
# Rules Validation
# ============================================================================

def validate_ecss_rules(rules: List) -> bool:
    """Validate that ECSS rules are properly configured."""
    try:
        for rule in rules:
            if isinstance(rule, NaturalLanguageRule):
                # Validate prompt
                if not hasattr(rule, 'prompt') or not rule.prompt:
                    print(f"⚠ NaturalLanguageRule missing prompt: {rule}")
                    return False
            else:
                print(f"⚠ Unknown rule type: {type(rule)}")
                return False
        
        print(f"Created {len(rules)} ECSS rules")
        return True
        
    except Exception as e:
        print(f"❌ Rules validation failed: {e}")
        return False

# ============================================================================
# Rules Performance Optimization
# ============================================================================

def optimize_rules_for_performance(rules: List, document_size: str = "medium") -> List:
    """Optimize rules based on document size and complexity."""
    if document_size == "small":
        # For small documents, use fewer rules to improve speed
        return [rules[0]] if rules else []  # Just the main metadata rule
    elif document_size == "large":
        # For large documents, add quality rules
        return rules + create_ecss_quality_rules()
    else:
        # Medium documents use standard rules
        return rules

if __name__ == "__main__":
    # Test rules creation
    print("🧪 Testing ECSS Rules Creation...")
    
    # Test basic rules
    basic_rules = create_ecss_metadata_rules()
    print(f"Created {len(basic_rules)} basic metadata rules")
    
    # Test branch-specific rules
    e_rules = get_ecss_rules_for_branch('E')
    print(f"Created {len(e_rules)} E-branch rules")
    
    # Test validation
    is_valid = validate_ecss_rules(basic_rules)
    print(f"Rules validation: {'PASS' if is_valid else 'FAIL'}")
    
    print("ECSS Rules Schema ready for use!") 

from typing import List, Dict, Optional, Any
from core.schemas import BaseModel, Field, NaturalLanguageRule

# ============================================================================
# ECSS Document Metadata Schema
# ============================================================================

class ECSSStandard(BaseModel):
    """Schema for extracting ECSS standard metadata."""
    standard_id: str = Field(description="ECSS standard identifier (e.g., ECSS-E-ST-10C)")
    branch: str = Field(description="ECSS branch (E, M, P, Q)")
    discipline: str = Field(description="ECSS discipline (Engineering, Management, Product Assurance, etc.)")
    title: str = Field(description="Full title of the standard")
    revision: str = Field(description="Revision number (e.g., Rev.1, Rev.2)")
    date: str = Field(description="Publication date")
    status: str = Field(description="Status (Active, Superseded, etc.)")
    scope: str = Field(description="Brief description of the standard's scope")
    keywords: List[str] = Field(description="Key technical terms and concepts")
    applicable_domains: List[str] = Field(description="Space engineering domains this applies to")

class ECSSSection(BaseModel):
    """Schema for extracting section information."""
    section_number: str = Field(description="Section number (e.g., 3.1, 4.2.1)")
    section_title: str = Field(description="Title of the section")
    section_type: str = Field(description="Type of section (normative, informative, annex)")
    content_summary: str = Field(description="Brief summary of section content")
    requirements_count: int = Field(description="Number of requirements in this section")
    figures_count: int = Field(description="Number of figures in this section")
    tables_count: int = Field(description="Number of tables in this section")

class ECSSDefinition(BaseModel):
    """Schema for extracting definitions."""
    term: str = Field(description="The term being defined")
    definition: str = Field(description="The definition of the term")
    context: str = Field(description="Context where this definition is used")
    related_terms: List[str] = Field(description="Related terms or synonyms")
    standard_reference: str = Field(description="Which standard this definition comes from")

class ECSSTable(BaseModel):
    """Schema for extracting table information."""
    table_number: str = Field(description="Table number (e.g., Table 1, Table A.1)")
    table_title: str = Field(description="Title or caption of the table")
    table_type: str = Field(description="Type of table (requirements, parameters, classifications)")
    row_count: int = Field(description="Number of rows in the table")
    column_count: int = Field(description="Number of columns in the table")
    content_summary: str = Field(description="Summary of what the table contains")
    key_parameters: List[str] = Field(description="Key parameters or values in the table")

class ECSSDiagram(BaseModel):
    """Schema for extracting diagram information."""
    figure_number: str = Field(description="Figure number (e.g., Figure 1, Figure A.1)")
    figure_title: str = Field(description="Title or caption of the figure")
    diagram_type: str = Field(description="Type of diagram (flowchart, block diagram, schematic)")
    content_description: str = Field(description="Description of what the diagram shows")
    components: List[str] = Field(description="Key components or elements in the diagram")
    relationships: List[str] = Field(description="Relationships or connections shown")

class ECSSRequirement(BaseModel):
    """Schema for extracting requirements."""
    requirement_id: str = Field(description="Requirement identifier (e.g., REQ-001)")
    requirement_text: str = Field(description="The requirement statement")
    requirement_type: str = Field(description="Type of requirement (functional, performance, interface)")
    priority: str = Field(description="Priority level (mandatory, recommended, optional)")
    verification_method: str = Field(description="How this requirement is verified")
    applicable_phases: List[str] = Field(description="Project phases this applies to")

# ============================================================================
# ECSS Rules Configuration
# ============================================================================

def create_ecss_metadata_rules() -> List[NaturalLanguageRule]:
    """Create comprehensive ECSS metadata extraction rules using NaturalLanguageRule."""
    return [
        NaturalLanguageRule(
            prompt="""Extract comprehensive ECSS standard metadata from the document. Return as JSON with these fields:
- standard_id: ECSS standard identifier (e.g., ECSS-E-ST-10C)
- branch: ECSS branch (E, M, P, Q)
- discipline: ECSS discipline (Engineering, Management, Product Assurance, etc.)
- title: Full title of the standard
- revision: Revision number (e.g., Rev.1, Rev.2)
- date: Publication date
- status: Status (Active, Superseded, etc.)
- scope: Brief description of the standard's scope
- keywords: Array of key technical terms and concepts
- applicable_domains: Array of space engineering domains this applies to

Be precise and extract all available information from the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract section information from the ECSS document. Return as JSON with these fields:
- section_number: Section number (e.g., 3.1, 4.2.1)
- section_title: Title of the section
- section_type: Type of section (normative, informative, annex)
- content_summary: Brief summary of section content
- requirements_count: Number of requirements in this section
- figures_count: Number of figures in this section
- tables_count: Number of tables in this section

Extract information for each major section found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract definitions from the ECSS document. Return as JSON with these fields:
- term: The term being defined
- definition: The definition of the term
- context: Context where this definition is used
- related_terms: Array of related terms or synonyms
- standard_reference: Which standard this definition comes from

Extract all definitions found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract table information from the ECSS document. Return as JSON with these fields:
- table_number: Table number (e.g., Table 1, Table A.1)
- table_title: Title or caption of the table
- table_type: Type of table (requirements, parameters, classifications)
- row_count: Number of rows in the table
- column_count: Number of columns in the table
- content_summary: Summary of what the table contains
- key_parameters: Array of key parameters or values in the table

Extract information for each table found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract diagram and figure information from the ECSS document. Return as JSON with these fields:
- figure_number: Figure number (e.g., Figure 1, Figure A.1)
- figure_title: Title or caption of the figure
- diagram_type: Type of diagram (flowchart, block diagram, schematic)
- content_description: Description of what the diagram shows
- components: Array of key components or elements in the diagram
- relationships: Array of relationships or connections shown

Extract information for each figure or diagram found in the document."""
        ),
        NaturalLanguageRule(
            prompt="""Extract requirements from the ECSS document. Return as JSON with these fields:
- requirement_id: Requirement identifier (e.g., REQ-001)
- requirement_text: The requirement statement
- requirement_type: Type of requirement (functional, performance, interface)
- priority: Priority level (mandatory, recommended, optional)
- verification_method: How this requirement is verified
- applicable_phases: Array of project phases this applies to

Extract all requirements found in the document."""
        )
    ]

def create_ecss_content_rules() -> List[NaturalLanguageRule]:
    """Create ECSS content transformation rules."""
    return [
        NaturalLanguageRule(
            prompt="""Standardize ECSS document formatting:
1. Ensure consistent heading hierarchy (1, 1.1, 1.1.1, etc.)
2. Normalize requirement numbering (REQ-001, REQ-002, etc.)
3. Standardize figure and table references (Figure 1, Table 1, etc.)
4. Ensure consistent terminology usage throughout the document
5. Maintain all technical accuracy and precision
6. Preserve all mathematical formulas and technical specifications
7. Keep all normative content intact"""
        ),
        NaturalLanguageRule(
            prompt="""Enhance ECSS content for better searchability:
1. Add cross-references between related sections
2. Clarify ambiguous technical terms with context
3. Ensure all abbreviations are defined
4. Add implicit relationships between requirements
5. Maintain all original technical content and accuracy
6. Preserve all normative requirements exactly as stated"""
        )
    ]

def create_ecss_quality_rules() -> List[NaturalLanguageRule]:
    """Create ECSS quality assurance rules."""
    return [
        NaturalLanguageRule(
            prompt="""Validate ECSS document quality:
1. Check for missing requirement identifiers
2. Verify figure and table numbering consistency
3. Ensure all referenced terms are defined
4. Validate cross-reference accuracy
5. Check for incomplete requirements
6. Verify normative vs informative content labeling
7. Maintain all original content - only add validation notes"""
        )
    ]

# ============================================================================
# Branch-Specific Rules
# ============================================================================

class EBranchSchema(BaseModel):
    """Engineering branch specific schema."""
    engineering_discipline: str = Field(description="Specific engineering discipline")
    technical_requirement: str = Field(description="Technical requirement details")
    verification_method: str = Field(description="Verification method for engineering requirements")

class MBranchSchema(BaseModel):
    """Management branch specific schema."""
    management_process: str = Field(description="Management process details")
    project_phase: str = Field(description="Project phase information")
    stakeholder: str = Field(description="Stakeholder information")

class PBranchSchema(BaseModel):
    """Product Assurance branch specific schema."""
    assurance_process: str = Field(description="Product assurance process details")
    quality_requirement: str = Field(description="Quality requirement details")
    verification_plan: str = Field(description="Verification planning information")

class QBranchSchema(BaseModel):
    """Quality branch specific schema."""
    quality_process: str = Field(description="Quality process details")
    audit_requirement: str = Field(description="Audit requirement details")
    compliance_check: str = Field(description="Compliance checking information")

def create_e_branch_rules() -> List[NaturalLanguageRule]:
    """Create Engineering branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Engineering branch specific information from the ECSS document. Return as JSON with these fields:
- engineering_discipline: Specific engineering discipline (e.g., Electrical, Mechanical, Software)
- technical_requirement: Technical requirement details
- verification_method: Verification method for engineering requirements

Focus on engineering-specific content and requirements."""
        )
    ]

def create_m_branch_rules() -> List[NaturalLanguageRule]:
    """Create Management branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Management branch specific information from the ECSS document. Return as JSON with these fields:
- management_process: Management process details
- project_phase: Project phase information
- stakeholder: Stakeholder information

Focus on management-specific content and processes."""
        )
    ]

def create_p_branch_rules() -> List[NaturalLanguageRule]:
    """Create Product Assurance branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Product Assurance branch specific information from the ECSS document. Return as JSON with these fields:
- assurance_process: Product assurance process details
- quality_requirement: Quality requirement details
- verification_plan: Verification planning information

Focus on product assurance and quality-specific content."""
        )
    ]

def create_q_branch_rules() -> List[NaturalLanguageRule]:
    """Create Quality branch specific rules."""
    return [
        NaturalLanguageRule(
            prompt="""Extract Quality branch specific information from the ECSS document. Return as JSON with these fields:
- quality_process: Quality process details
- audit_requirement: Audit requirement details
- compliance_check: Compliance checking information

Focus on quality-specific content and processes."""
        )
    ]

# ============================================================================
# Rules Factory Functions
# ============================================================================

def get_ecss_rules_for_branch(branch: str) -> List:
    """Get appropriate rules for a specific ECSS branch."""
    base_rules = create_ecss_metadata_rules() + create_ecss_content_rules()
    
    branch_rules = {
        'E': create_e_branch_rules(),
        'M': create_m_branch_rules(),
        'P': create_p_branch_rules(),
        'Q': create_q_branch_rules()
    }
    
    return base_rules + branch_rules.get(branch.upper(), [])

def get_ecss_rules_for_document_type(doc_type: str) -> List:
    """Get rules optimized for specific document types."""
    if doc_type == "standard":
        return create_ecss_metadata_rules() + create_ecss_content_rules()
    elif doc_type == "handbook":
        return create_ecss_metadata_rules() + create_ecss_quality_rules()
    elif doc_type == "annex":
        return create_ecss_metadata_rules()
    else:
        return create_ecss_metadata_rules() + create_ecss_content_rules()

# ============================================================================
# Rules Validation
# ============================================================================

def validate_ecss_rules(rules: List) -> bool:
    """Validate that ECSS rules are properly configured."""
    try:
        for rule in rules:
            if isinstance(rule, NaturalLanguageRule):
                # Validate prompt
                if not hasattr(rule, 'prompt') or not rule.prompt:
                    print(f"⚠ NaturalLanguageRule missing prompt: {rule}")
                    return False
            else:
                print(f"⚠ Unknown rule type: {type(rule)}")
                return False
        
        print(f"Created {len(rules)} ECSS rules")
        return True
        
    except Exception as e:
        print(f"❌ Rules validation failed: {e}")
        return False

# ============================================================================
# Rules Performance Optimization
# ============================================================================

def optimize_rules_for_performance(rules: List, document_size: str = "medium") -> List:
    """Optimize rules based on document size and complexity."""
    if document_size == "small":
        # For small documents, use fewer rules to improve speed
        return [rules[0]] if rules else []  # Just the main metadata rule
    elif document_size == "large":
        # For large documents, add quality rules
        return rules + create_ecss_quality_rules()
    else:
        # Medium documents use standard rules
        return rules

if __name__ == "__main__":
    # Test rules creation
    print("🧪 Testing ECSS Rules Creation...")
    
    # Test basic rules
    basic_rules = create_ecss_metadata_rules()
    print(f"Created {len(basic_rules)} basic metadata rules")
    
    # Test branch-specific rules
    e_rules = get_ecss_rules_for_branch('E')
    print(f"Created {len(e_rules)} E-branch rules")
    
    # Test validation
    is_valid = validate_ecss_rules(basic_rules)
    print(f"Rules validation: {'PASS' if is_valid else 'FAIL'}")
    
    print("ECSS Rules Schema ready for use!") 