# ECSS Ingestion Optimization Guide

## Overview
This guide documents the optimizations and cost-saving measures implemented for the ECSS document ingestion process using Morphik. The goal is to prevent wasted money on failed operations and ensure efficient processing.

## Key Improvements Made

### 1. Configuration Optimization (`backend/morphik.toml`)
- **Chunk Size**: 1000 characters with 200 character overlap (optimized for ECSS requirements)
- **Embedding Model**: `text-embedding-3-large` for technical documentation
- **Query Settings**: k=5, reranking enabled for better accuracy
- **Graph Settings**: GPT-4o with 4000 token limit

### 2. Safe Ingestion Process (`backend/ingest_documents_safe.py`)
- **Pre-validation**: Checks all documents exist before any expensive operations
- **Cost estimation**: Provides cost estimates before proceeding
- **Connection testing**: Validates Morphik connection before ingestion
- **Comprehensive error handling**: Prevents partial failures from wasting money
- **Progress tracking**: Clear logging of each step

### 3. System Testing (`backend/test_system_before_ingestion.py`)
- **Environment validation**: Checks .env configuration
- **Connection testing**: Validates Morphik API access
- **Document access**: Verifies PDF files are accessible
- **Single document test**: Tests ingestion with cleanup

### 4. API Server Optimization (`backend/api_server.py`)
- **Reranking enabled**: Better result quality
- **Result limiting**: k=5 for performance
- **Graph-aware queries**: hop_depth=2 for deeper connections
- **Multiple source handling**: Shows evidence from different documents

## Cost-Saving Features

### Pre-Ingestion Validation
```bash
# Run this first to validate everything
python test_system_before_ingestion.py
```

### Cost Estimation
The safe ingestion script provides cost estimates:
- Document ingestion: ~$0.01 per MB
- Graph creation: ~$0.10 per document (GPT-4o)
- Total for 5 documents: ~$0.50-1.00

### Error Prevention
- Validates all files exist before processing
- Tests Morphik connection before expensive operations
- Provides detailed error messages for troubleshooting
- Stops on first failure to prevent wasted processing

## Recommended Workflow

### 1. Initial Setup
```bash
cd backend
python test_system_before_ingestion.py
```

### 2. Safe Ingestion
```bash
python ingest_documents_safe.py
```

### 3. Verify Results
```bash
python test_search_fixed.py
```

## Configuration Details

### Morphik Settings (`morphik.toml`)
```toml
[parser]
chunk_size = 1000        # Optimal for ECSS requirements
chunk_overlap = 200      # Maintains context between chunks

[embedding]
model = "text-embedding-3-large"  # Best for technical docs

[query]
k = 5                   # Limit results for performance
use_reranking = true    # Better accuracy

[graph]
model_name = "gpt-4o"   # High-quality model for graph creation
max_tokens = 4000       # Reasonable limit for cost control
```

### Document Processing
- Uses Colpali for better PDF parsing
- Extracts metadata from filenames
- Creates structured knowledge graph with entities and relationships
- Handles ECSS-specific document structure

## Troubleshooting

### Common Issues

1. **MORPHIK_URI not set**
   - Check your `.env` file
   - Ensure the URI is correct and accessible

2. **Documents not found**
   - Verify PDF directory path
   - Check file permissions
   - Ensure filenames match exactly

3. **Ingestion failures**
   - Check Morphik service status
   - Verify document format (PDF)
   - Check network connectivity

4. **Graph creation failures**
   - Most expensive operation - check Morphik logs
   - Verify GPT-4o model availability
   - Check token limits and costs

### Debugging Steps

1. Run system test first
2. Check Morphik connection
3. Validate document access
4. Test single document ingestion
5. Monitor costs during graph creation

## Cost Optimization Tips

1. **Start small**: Test with 1-2 documents first
2. **Monitor usage**: Check Morphik dashboard for actual costs
3. **Use appropriate models**: GPT-4o for quality, cheaper models for testing
4. **Optimize chunking**: Balance context vs. cost
5. **Clean up**: Remove test documents to avoid storage costs

## Performance Monitoring

### Key Metrics to Watch
- Document ingestion success rate
- Graph creation time and cost
- Query response quality
- API response times

### Expected Performance
- Ingestion: ~30-60 seconds per document
- Graph creation: ~2-5 minutes for 5 documents
- Query response: ~1-3 seconds
- Total cost: ~$0.50-1.00 for initial setup

## Next Steps

1. Run the system test to validate setup
2. Execute safe ingestion with cost monitoring
3. Test search functionality
4. Monitor performance and costs
5. Scale up gradually based on results

## References

- [Morphik Documentation](https://www.morphik.ai/docs/)
- [How to perform search over documents](https://www.morphik.ai/docs/knowledge-base/how-to-perform-search-over-documents)
- [How to improve retrieval accuracy](https://www.morphik.ai/docs/knowledge-base/how-to-improve-retrieval-accuracy)
- [How to manage document chunking](https://www.morphik.ai/docs/knowledge-base/how-to-manage-document-chunking) 