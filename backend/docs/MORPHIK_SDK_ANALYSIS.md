# Morphik SDK Analysis & Issues Report

## Overview
This document analyzes the Morphik Python SDK documentation and identifies issues with our current ECSS ingestion implementation.

## Key SDK Methods & Our Usage

### Document Ingestion
- **Method**: `db.ingest_file(file, rules=[...], use_colpali=True)`
- **Our Usage**: ✅ Correct
- **Returns**: `Document` object

### Document Retrieval
- **Method**: `db.get_document(document_id)` 
- **Our Usage**: ❌ **WRONG** - We're using `db.document(external_id=...)` which doesn't exist
- **Correct Usage**: `db.get_document(document_id)`

### Document Listing
- **Method**: `db.list_documents()`
- **Our Usage**: ✅ Correct

### Document Updates
- **Methods Available**:
  - `update_document_metadata(document_id, metadata)`
  - `update_document_with_file(document_id, file)`
  - `update_document_with_text(document_id, text)`
- **Our Usage**: Not using these methods

## Critical Issues Found

### 1. **Incorrect Document Retrieval Method**
**Problem**: Our code uses `db.document(external_id=...)` which doesn't exist in the SDK.
```python
# WRONG (our current code):
refetched_doc = db.document(external_id=doc.id)

# CORRECT (per SDK docs):
refetched_doc = db.get_document(doc_id)
```

### 2. **Metadata Access Pattern**
**Problem**: We're looking for `structured_data` attribute, but SDK docs show metadata is in `.metadata` property.

**From SDK docs**:
- `retrieve_chunks()` returns `FinalChunkResult` with `.metadata` property
- `retrieve_docs()` returns `DocumentResult` with `.metadata` property  
- `get_document()` returns `Document` with `.metadata` property

### 3. **Missing Document ID Handling**
**Problem**: Our debug script fails because `Document` objects don't have `.id` attribute.

**From SDK docs**: Document objects have different ID attributes depending on context:
- `document_id` (most common)
- `external_id` (if provided during ingestion)
- `id` (may not exist)

### 4. **Rule Creation Issues**
**Problem**: Our rules don't have `.name` attribute, causing debug script failures.

**From SDK docs**: Rules should be:
- `MetadataExtractionRule(schema=BaseModel)`
- `NaturalLanguageRule(prompt="...")`

## SDK Features We're Not Using

### 1. **Document Update Capabilities**
```python
# We could use these to update metadata after ingestion:
db.update_document_metadata(document_id, {"branch": "E", "discipline": "Engineering"})
```

### 2. **Batch Operations**
```python
# For efficient processing of multiple documents:
documents = db.batch_get_documents([doc_id1, doc_id2, doc_id3])
```

### 3. **Advanced Querying**
```python
# For testing if metadata extraction worked:
chunks = db.retrieve_chunks("ECSS requirements", filters={"branch": "E"})
```

### 4. **Workflow Status Checking**
```python
# To check if AI processing is complete:
status = db.check_workflow_status(document_id)
```

## Recommended Fixes

### 1. **Fix Document Retrieval**
```python
# In clean_and_ingest.py, change:
refreshed_doc = db.document(external_id=doc.id)
# To:
refreshed_doc = db.get_document(doc_id)
```

### 2. **Fix Debug Script**
```python
# In debug_ai_extraction.py, change:
print(f"ID: {doc.id}")
# To:
doc_id = getattr(doc, 'document_id', getattr(doc, 'external_id', None))
print(f"ID: {doc_id}")
```

### 3. **Use Correct Metadata Access**
```python
# Instead of looking for structured_data:
if hasattr(doc, 'structured_data'):
    metadata = doc.structured_data

# Use the documented approach:
if hasattr(doc, 'metadata'):
    metadata = doc.metadata
```

### 4. **Add Workflow Status Checking**
```python
# After ingestion, check if AI processing is complete:
status = db.check_workflow_status(doc.document_id)
if status.status == 'completed':
    # Now safe to retrieve metadata
    full_doc = db.get_document(doc.document_id)
```

## Testing Strategy

### 1. **Test Document Retrieval**
```python
# Test the correct method:
doc = db.get_document("test_doc_id")
print(f"Metadata: {doc.metadata}")
```

### 2. **Test Metadata Extraction**
```python
# Use retrieve_chunks to see if metadata is being extracted:
chunks = db.retrieve_chunks("ECSS", k=1)
if chunks:
    print(f"Chunk metadata: {chunks[0].metadata}")
```

### 3. **Test Workflow Status**
```python
# Check if AI processing completed:
status = db.check_workflow_status(doc.document_id)
print(f"Workflow status: {status.status}")
```

## References
- [ingest_file](https://www.morphik.ai/docs/python-sdk/ingest_file)
- [get_document](https://www.morphik.ai/docs/python-sdk/get_document)
- [retrieve_chunks](https://www.morphik.ai/docs/python-sdk/retrieve_chunks)
- [retrieve_docs](https://www.morphik.ai/docs/python-sdk/retrieve_docs)
- [query](https://www.morphik.ai/docs/python-sdk/query)
- [check_workflow_status](https://www.morphik.ai/docs/python-sdk/check_workflow_status)
- [update_document_metadata](https://www.morphik.ai/docs/python-sdk/update_document_metadata)

## Next Steps
1. Fix the document retrieval method in `clean_and_ingest.py`
2. Update debug script to use correct attribute names
3. Test metadata access using `.metadata` property
4. Add workflow status checking
5. Test with a simple document to verify the fixes work 