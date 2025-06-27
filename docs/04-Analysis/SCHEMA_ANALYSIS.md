# ECSS Knowledge Graph Schema Analysis

## Current Schema vs. Enhanced Schema Comparison

### Current Schema (Basic)
```python
# Entities
- Standard (name, category, version, title)
- Requirement (requirement_id, text, level, parent_section)
- Diagram (figure_id, caption, content_type)

# Relationships
- Specifies (Standard → Requirement)
- Contains (Standard → Diagram)
- References (Requirement → Standard)
- Illustrates (Diagram → Requirement)
```

### Enhanced Schema (Comprehensive)
```python
# Core Entities (Essential)
- Standard (name, category, version, title, publication_date, scope)
- Section (section_id, title, level, content_summary)
- Requirement (requirement_id, text, level, parent_section, compliance_category, verification_method)
- Definition (term, definition, context, source)
- Diagram (figure_id, caption, content_type, purpose)

# Extended Entities (Advanced)
- Procedure (procedure_id, title, description, steps, purpose)
- Table (table_id, title, content, table_type)
- TechnicalConcept (concept_name, description, category, specifications)
- CrossReference (reference_id, source_text, target_type, target_id)

# Core Relationships (Essential)
- HasSection (Standard → Section)
- ContainsRequirement (Section → Requirement)
- Specifies (Standard → Requirement)
- Defines (Standard/Section → Definition)
- ContainsDiagram (Section → Diagram)
- References (Requirement/Section → Standard)
- Illustrates (Diagram → Requirement)

# Extended Relationships (Advanced)
- SubsectionOf (Section → Section)
- Describes (Section → Procedure)
- ContainsTable (Section → Table)
- CrossReferences (CrossReference → Entity)
- Uses (Requirement/Procedure → TechnicalConcept)
- Implements (Procedure → Requirement)
- Verifies (Procedure → Requirement)
- RelatedTo (Entity → Entity)
- DependsOn (Entity → Entity)
- CompliesWith (Entity → Standard/Requirement)
```

## Analysis: What We're Missing

### ❌ **Critical Missing Entities**

1. **Section Entity** - Essential for document structure
   - **Impact**: Without sections, we lose hierarchical organization
   - **Example**: "Chapter 4: System Requirements" → "Section 4.2: Telemetry" → "4.2.1a: Telemetry Link"
   - **Recommendation**: **HIGH PRIORITY** - Add immediately

2. **Definition Entity** - Critical for terminology understanding
   - **Impact**: Users can't understand technical terms
   - **Example**: "telemetry", "qualification", "verification"
   - **Recommendation**: **HIGH PRIORITY** - Add immediately

3. **Table Entity** - Important for structured data
   - **Impact**: Lose valuable tabular information
   - **Example**: Material specifications, test procedures, compliance matrices
   - **Recommendation**: **MEDIUM PRIORITY** - Add in next iteration

### ❌ **Critical Missing Relationships**

1. **HasSection** - Document structure
   - **Impact**: Can't navigate document hierarchy
   - **Recommendation**: **HIGH PRIORITY**

2. **ContainsRequirement** - Section-requirement mapping
   - **Impact**: Can't find requirements within sections
   - **Recommendation**: **HIGH PRIORITY**

3. **Defines** - Term definitions
   - **Impact**: Can't understand technical terminology
   - **Recommendation**: **HIGH PRIORITY**

### ❌ **Advanced Missing Features**

1. **Procedure Entity** - Step-by-step processes
   - **Impact**: Lose procedural information
   - **Example**: Test procedures, qualification processes
   - **Recommendation**: **MEDIUM PRIORITY**

2. **TechnicalConcept Entity** - Domain knowledge
   - **Impact**: Lose technical context
   - **Example**: Materials, components, systems
   - **Recommendation**: **MEDIUM PRIORITY**

3. **CrossReference Entity** - Internal references
   - **Impact**: Lose document navigation
   - **Example**: "See Section 4.2", "Refer to Table 3-1"
   - **Recommendation**: **LOW PRIORITY**

## Recommendations

### 🎯 **Phase 1: Essential Additions (Immediate)**
Add these to our current schema for immediate improvement:

```python
# Add to current schema
class Section(Entity):
    section_id: str
    title: str
    level: int
    content_summary: str

class Definition(Entity):
    term: str
    definition: str
    context: str

# Add relationships
class HasSection(Relationship):
    source: Standard
    target: Section

class ContainsRequirement(Relationship):
    source: Section
    target: Requirement

class Defines(Relationship):
    source: Standard | Section
    target: Definition
```

### 🎯 **Phase 2: Enhanced Features (Next Iteration)**
Add these for comprehensive coverage:

```python
# Extended entities
class Table(Entity):
    table_id: str
    title: str
    content: str
    table_type: str

class Procedure(Entity):
    procedure_id: str
    title: str
    description: str
    steps: List[str]
    purpose: str

class TechnicalConcept(Entity):
    concept_name: str
    description: str
    category: str
    specifications: str

# Extended relationships
class ContainsTable(Relationship):
    source: Section
    target: Table

class Describes(Relationship):
    source: Section
    target: Procedure

class Uses(Relationship):
    source: Requirement | Procedure
    target: TechnicalConcept
```

### 🎯 **Phase 3: Advanced Features (Future)**
For maximum coverage:

```python
# Advanced entities
class CrossReference(Entity):
    reference_id: str
    source_text: str
    target_type: str
    target_id: str

# Advanced relationships
class CrossReferences(Relationship):
    source: CrossReference
    target: Requirement | Section | Table | Diagram

class DependsOn(Relationship):
    source: Requirement | Procedure
    target: Requirement | Procedure

class CompliesWith(Relationship):
    source: Requirement | Procedure
    target: Standard | Requirement
```

## Implementation Strategy

### Option 1: Incremental Approach (Recommended)
1. **Start with Phase 1** - Add Section and Definition entities
2. **Test and validate** - Ensure extraction works correctly
3. **Add Phase 2** - Tables, Procedures, Technical Concepts
4. **Evaluate performance** - Monitor extraction quality
5. **Consider Phase 3** - Advanced features if needed

### Option 2: Comprehensive Approach
1. **Implement all entities** - Full schema from the start
2. **Complex extraction** - More sophisticated prompts
3. **Higher cost** - More entities to extract
4. **Better coverage** - Complete document understanding

## Cost-Benefit Analysis

### Current Schema
- **Entities**: 3
- **Relationships**: 4
- **Extraction Complexity**: Low
- **Coverage**: Basic
- **Cost**: Low

### Phase 1 (Recommended)
- **Entities**: 5 (+2)
- **Relationships**: 7 (+3)
- **Extraction Complexity**: Medium
- **Coverage**: Good
- **Cost**: Medium

### Full Enhanced Schema
- **Entities**: 9 (+6)
- **Relationships**: 18 (+14)
- **Extraction Complexity**: High
- **Coverage**: Excellent
- **Cost**: High

## Recommendation: Phase 1 Implementation

**I recommend implementing Phase 1 immediately** because:

1. **High Impact**: Section and Definition entities provide 80% of the value
2. **Manageable Complexity**: Only 2 new entities and 3 new relationships
3. **Immediate Benefits**: Better document navigation and terminology understanding
4. **Low Risk**: Incremental addition to existing schema
5. **Cost Effective**: Reasonable extraction complexity

### Implementation Plan:
1. Update `clean_and_ingest.py` with Phase 1 entities
2. Update extraction prompt to include Section and Definition extraction
3. Test with current 5 documents
4. Validate extraction quality
5. Deploy and monitor performance

This approach gives us the most value for the least complexity while maintaining the option to expand later.

---

**Conclusion**: Our current schema is functional but missing critical entities for comprehensive ECSS document understanding. Phase 1 additions (Section + Definition) will dramatically improve our knowledge graph's utility while keeping implementation manageable. 