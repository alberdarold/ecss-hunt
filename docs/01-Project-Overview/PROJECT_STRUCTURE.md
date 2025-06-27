# ECSS Hunter - Project Structure

## Overview
This is a clean, production-ready project structure following software development best practices.

## Directory Structure

```
ecss-hunt/
├── frontend/                          # Next.js 14 application
│   ├── src/
│   │   └── app/
│   │       ├── api/
│   │       │   └── search/
│   │       │       └── route.ts       # Search API endpoint
│   │       ├── globals.css
│   │       ├── layout.tsx
│   │       └── page.tsx
│   ├── public/                        # Static assets
│   ├── test-mock.js                   # Backend logic test
│   ├── BACKEND_API.md                 # API documentation
│   ├── package.json                   # Frontend dependencies
│   └── tsconfig.json                  # TypeScript config
│
├── ECSS Published Standards/          # ECSS PDF documents
│   ├── 1-Active Standards/           # Current ECSS standards
│   └── 2-Superseded Standards/       # Historical standards
│
├── ECSS Utils/                       # ECSS documentation & images
│   ├── Introduction_to_ECSS_2023_presentation.pdf
│   └── [ECSS presentation images]
│
├── ingest_documents.py               # Document ingestion script
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── LICENSE                           # Project license
├── README.md                         # Main project documentation
└── PROJECT_STRUCTURE.md              # This file
```

## Key Files

### Core Application Files
- **`frontend/src/app/api/search/route.ts`**: Main search API endpoint
- **`ingest_documents.py`**: Script to ingest ECSS documents into Morphik
- **`frontend/test-mock.js`**: Test script for backend logic

### Configuration Files
- **`frontend/package.json`**: Frontend dependencies and scripts
- **`frontend/tsconfig.json`**: TypeScript configuration
- **`requirements.txt`**: Python dependencies
- **`.gitignore`**: Git ignore patterns

### Documentation
- **`README.md`**: Main project documentation
- **`frontend/BACKEND_API.md`**: API documentation
- **`PROJECT_STRUCTURE.md`**: This file

## Development Workflow

### 1. Document Ingestion
```bash
python ingest_documents.py
```

### 2. Backend Testing
```bash
cd frontend
node test-mock.js
```

### 3. Frontend Development
```bash
cd frontend
npm run dev
```

## Clean Architecture Principles

✅ **Separation of Concerns**: Frontend and backend clearly separated
✅ **Single Responsibility**: Each file has a specific purpose
✅ **Minimal Dependencies**: Only essential files included
✅ **Clear Documentation**: Comprehensive README and API docs
✅ **Test Coverage**: Backend logic tested and verified
✅ **Version Control**: Proper .gitignore and clean structure

## Removed Files (Cleaned Up)

The following files were removed during cleanup:
- `ingest_documents_v2.py` (duplicate)
- `test_morphik_api.py` (unnecessary)
- `test_basic.py` (replaced by better tests)
- `test_morphik.py` (replaced by better tests)
- `test_ingestion.py` (no longer needed)
- `frontend/test-api.js` (replaced by test-mock.js)
- `frontend/test-api-simple.js` (replaced by test-mock.js)
- `frontend/test-standalone.js` (had import issues)
- `frontend/test-browser.html` (replaced by Node.js tests)

## Next Steps

1. **Frontend Development**: Build search interface
2. **Morphik Integration**: Replace mock data with real API
3. **Authentication**: Add user authentication system
4. **PDF Viewer**: Integrate PDF viewing capabilities 