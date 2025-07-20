# ECSS Standards Navigator

A web-based platform that enables space engineers and professionals to efficiently navigate and search through European Cooperation for Space Standardization (ECSS) documentation using Morphik's advanced multimodal RAG capabilities.

## Project Status

🎉 **WORKING SYSTEM - DEPLOYED & FUNCTIONAL**

✅ **Frontend**: Complete and deployed on Vercel  
✅ **Backend API**: Production-ready Flask server deployed on Render  
✅ **Document Ingestion**: 3 ECSS documents successfully processed and searchable  
✅ **Search Integration**: Working search with AI contextual responses  
✅ **User Interface**: Modern, responsive design with real-time search  

**Live Demo**: https://ecss-hunt.vercel.app  

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
│   ├── 1-Active Standards/  # 138 Active Standards (available for ingestion)
│   └── 2-Superseded Standards/ # 207 Superseded Standards (available for ingestion)
├── ECSS Utils/              # Supporting documentation
└── docs/                    # Project documentation
    ├── 01-Project-Overview/
    ├── 02-Implementation/
    ├── 03-Optimization/
    ├── 04-Analysis/
    └── 05-Architecture/
```

## 🚀 Quick Start

### Live Demo
Visit the working application: **https://ecss-hunt.vercel.app**

### Local Development

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:3000
```

#### Backend API (Flask)
```bash
cd backend
pip install -r config/requirements.txt
python production/production_working_api.py
# API runs at http://localhost:8002
```

### Production Deployment
- **Frontend**: Automatically deployed on Vercel
- **Backend**: Deployed on Render with production API server
- **Documents**: 3 ECSS documents processed and searchable (out of 345 available)

## 🔧 Features & Capabilities

### Search Functionality
- **Real-time Search**: Instant search through processed ECSS documents
- **AI Contextual Responses**: Intelligent summaries for each query
- **Specific Content Retrieval**: Shows exact requirements, not general descriptions
- **Relevance Scoring**: Real scores based on actual relevance
- **Page Number Display**: Shows actual page references from documents
- **Multiple Results**: Displays 3-8 relevant document sections

### User Interface
- **Modern Design**: Clean, responsive interface with Tailwind CSS
- **Search Interface**: Intuitive search bar with instant results
- **Result Display**: Organized document results with scores and content
- **Error Handling**: Graceful error display and loading states
- **Mobile Responsive**: Works perfectly on all devices

### Technical Features
- **Morphik Integration**: Advanced RAG platform for document processing
- **Flask API**: Robust backend with CORS support
- **Next.js Frontend**: Modern React framework with TypeScript
- **Document Processing**: Text extraction, visual content, and metadata
- **Production Ready**: Deployed and working in production

## 📊 Current Document Status

### ✅ Successfully Processed (3 documents)
- Documents are searchable and returning results
- AI contextual responses working
- Real relevance scores implemented

### 📚 Available for Ingestion (345 documents)
- **138 Active Standards** - Current ECSS standards
- **207 Superseded Standards** - Historical ECSS documents
- All documents are ready for processing when needed

### 🔄 Ingestion Process
- Documents are processed one at a time for quality control
- Each document takes 1-2 minutes to process
- Cost-effective approach with Morphik platform

## 🌐 Deployment & CORS

- **Frontend**: Deployed on Vercel with automatic updates
- **Backend**: Deployed on Render with production API server
- **CORS Configuration**: Properly configured for cross-origin requests
- **API Endpoints**: Working search and health check endpoints

## 🔍 Troubleshooting

### Common Issues
- **CORS Error**: Backend is properly configured for production and local development
- **Failed to Fetch**: Check that both frontend and backend are running
- **No Results**: Ensure you're using ECSS-related search terms
- **Slow Search**: 5-15 seconds is normal for complex document searches

### Local Development Issues
- **Backend Port**: API runs on port 8002, not 5000
- **Frontend Port**: Runs on port 3000 by default
- **Environment Variables**: Ensure MORPHIK_URI is set for backend

### Production Issues
- **Frontend**: Automatically deployed on Vercel
- **Backend**: Deployed on Render with production API server
- **Documents**: 3 ECSS documents are processed and searchable

## 🛠️ Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - Modern React with hooks
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework
- **Vercel** - Deployment platform

### Backend
- **Flask** - Python web framework
- **Morphik SDK** - Document processing and RAG capabilities
- **Python 3.9+** - Backend runtime
- **Render** - Deployment platform

### Search Engine
- **Morphik Cloud** - Advanced RAG platform
- **ColPali** - Visual content processing
- **Text Extraction** - Document content processing
- **Relevance Scoring** - Intelligent search ranking

### Infrastructure
- **Vercel** - Frontend hosting with automatic deployments
- **Render** - Backend hosting with production API server
- **Morphik Cloud** - Document processing and search engine

## 📚 Documentation

### Project Documentation
- [📋 Project Status Summary](PROJECT_STATUS_SUMMARY.md) - Complete project status and progress
- [🏗️ Implementation Plan](docs/05-Architecture/ECSS%20Standards%20Navigator%20-%20Implementation%20Plan%20and%20System%20Architecture.md)
- [📁 Project Structure](docs/01-Project-Overview/PROJECT_STRUCTURE.md)
- [🔌 Backend API](frontend/BACKEND_API.md)

### Key Files
- **Frontend**: `frontend/src/app/page.tsx` - Main search interface
- **Backend**: `backend/production/production_working_api.py` - Production API server
- **Configuration**: `backend/config/requirements.txt` - Python dependencies

## 🎯 Current Status

**✅ WORKING SYSTEM - DEPLOYED & FUNCTIONAL**

The ECSS Standards Navigator is a complete, production-ready system that enables space engineers to search through processed ECSS documents with AI-powered contextual responses and specific content retrieval.

**Current State:**
- ✅ System is fully functional and deployed
- ✅ 3 documents successfully processed and searchable
- ✅ 345 additional documents available for future ingestion
- ✅ Real-time search with AI responses working
- ✅ Modern, responsive UI deployed

**Live Demo**: https://ecss-hunt.vercel.app

---

*Last Updated: January 2025* 