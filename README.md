# ECSS Standards Navigator

A web-based platform that enables space engineers and professionals to efficiently navigate and search through European Cooperation for Space Standardization (ECSS) documentation using Morphik's advanced multimodal RAG capabilities.

## Project Status

✅ **Frontend**: Complete and functional with modern UI  
✅ **Backend API**: Implemented with Flask (Python) and Morphik integration  
⚠️ **Document Ingestion**: Working but documents stuck in processing (Morphik issue)  
⚠️ **Search Integration**: Ready but waiting for Morphik processing completion  

## Project Structure

```
ecss-hunt/
├── frontend/                 # Next.js frontend application
│   ├── src/app/             # Next.js App Router
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                  # Python backend and ingestion
│   ├── core/                # Main backend API (Flask server, logic, schemas, etc.)
│   ├── config/              # Environment and config files
│   ├── analysis/            # Analysis scripts
│   ├── debug/               # Debugging tools
│   ├── docs/                # Backend documentation
│   ├── extracted_images/    # Extracted images from ECSS docs
│   ├── results/             # Ingestion and analysis results
│   ├── tests/               # Backend tests
│   └── README.md            # Backend-specific README
├── ECSS Published Standards/ # ECSS PDF documents
│   ├── 1-Active Standards/
│   └── 2-Superseded Standards/
├── ECSS Utils/              # Supporting documentation
└── docs/                    # Project documentation
    ├── 01-Project-Overview/
    ├── 02-Implementation/
    ├── 03-Optimization/
    ├── 04-Analysis/
    └── 05-Architecture/
```

## Quick Start

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend API (Flask)
```bash
cd backend/core
pip install -r ../config/requirements.txt
python api_server.py
```

### Backend Ingestion (Python)
```bash
cd backend/core
python clean_and_ingest.py
```

## CORS & Deployment Notes

- The backend now includes a CORS fix to allow requests from:
  - `http://localhost:3000` (local frontend)
  - `https://ecss-hunt.vercel.app` (production frontend)
  - `https://ecss-hunt.onrender.com` (backend itself)
- **If you deploy the backend (e.g., to Render), make sure to redeploy after any CORS or API changes.**
- If you see `CORS` errors in the browser, ensure the deployed backend is running the latest code.

## Troubleshooting

- **CORS Error:**
  - Make sure the backend is redeployed with the latest CORS configuration.
  - For local development, use `http://localhost:5000` for backend and `http://localhost:3000` for frontend.
- **Failed to Fetch:**
  - Check backend logs for errors.
  - Ensure both frontend and backend are running and accessible.
- **Morphik Processing:**
  - Documents may be stuck in processing due to Morphik platform issues. Contact Morphik support if needed.

## Technology Stack

- **Frontend:** Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend:** Flask (Python), Morphik integration, modular structure
- **Search:** Morphik Cloud RAG platform
- **Deployment:** Vercel (frontend), Render or similar (backend)
- **Authentication:** NextAuth.js (planned)

## Documentation

- [Implementation Plan](docs/05-Architecture/ECSS%20Standards%20Navigator%20-%20Implementation%20Plan%20and%20System%20Architecture.md)
- [Project Structure](docs/01-Project-Overview/PROJECT_STRUCTURE.md)
- [Backend API](frontend/BACKEND_API.md) 