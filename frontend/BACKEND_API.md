# ECSS Search API - Backend Implementation

## Overview

The backend API provides search functionality for ECSS standards documents using Morphik's RAG capabilities. The API is implemented as a Next.js API route at `/api/search`.

## API Endpoints

### GET /api/search
Returns API status and information.

**Response:**
```json
{
  "message": "ECSS Search API",
  "status": "operational",
  "endpoints": {
    "search": "POST /api/search"
  },
  "note": "Currently using mock data - replace with actual Morphik integration"
}
```

### POST /api/search
Performs a search query against ECSS documents.

**Request Body:**
```json
{
  "query": "software development requirements",
  "filters": {
    "branch": "E",
    "discipline": "ST",
    "document_number": "20"
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "mock-1",
      "content": "This is a mock result for the query...",
      "document": {
        "filename": "ECSS-E-ST-20-08C_Rev.2(20April2023).pdf",
        "branch": "E",
        "branch_name": "Engineering",
        "discipline": "ST",
        "discipline_name": "Space Systems",
        "document_number": "20",
        "revision": "2"
      },
      "metadata": {
        "page": 15,
        "section": "5.2.2",
        "requirement_id": "5.2.2.1a"
      },
      "score": 0.95
    }
  ],
  "total": 2,
  "query": "software development requirements",
  "processing_time_ms": 523
}
```

## Implementation Details

### Current Status
- ✅ API route structure implemented
- ✅ Request/response validation
- ✅ Error handling
- ✅ Mock data for testing
- ⏳ Morphik integration (pending)

### Next Steps
1. **Replace MockMorphik with actual Morphik SDK**
2. **Add authentication middleware**
3. **Implement rate limiting**
4. **Add caching for common queries**

### Environment Variables
- `MORPHIK_URI`: Your Morphik instance URI
- `NODE_ENV`: Set to 'development' for detailed error messages

## Testing

Run the development server:
```bash
npm run dev
```

Test the API:
```bash
node test-api.js
```

Or use curl:
```bash
# Test GET endpoint
curl http://localhost:3000/api/search

# Test POST endpoint
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "software requirements"}'
```

## Error Handling

The API includes comprehensive error handling:
- **400**: Invalid request (missing query, empty query)
- **500**: Internal server error (Morphik connection issues, etc.)

All errors include processing time and optional details in development mode. 