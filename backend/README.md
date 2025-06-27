# Backend Directory Structure

This directory contains the backend components of the ECSS Standards Navigator project, organized into logical subdirectories for better maintainability.

## Directory Structure

```
backend/
├── __init__.py                 # Makes backend a Python package
├── README.md                   # This file
├── analysis/                   # Analysis and corpus processing scripts
│   ├── __init__.py
│   ├── analyze_50_documents.py
│   ├── analyze_ecss_structure.py
│   ├── analyze_full_ecss_corpus.py
│   ├── analyze_representative_sample.py
│   └── quick_analysis.py
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── .env                    # Environment variables
│   ├── morphik.toml           # Morphik configuration
│   └── requirements.txt       # Python dependencies
├── core/                       # Core functionality and main scripts
│   ├── __init__.py
│   ├── api_server.py          # Main API server
│   ├── clean_and_ingest.py    # Main ingestion script
│   ├── ecss_rules_schema.py   # ECSS rules and schemas
│   ├── schemas.py             # Base schemas and models
│   ├── optimized_graph_strategy.py
│   ├── working_*.py           # Working ingestion scripts
│   ├── enhanced_*.py          # Enhanced schemas and prompts
│   ├── extract_morphik_images.py
│   ├── inspect_chunks.py
│   ├── demo_search_functionality.py
│   ├── delete_document.py
│   ├── check_*.py             # Utility check scripts
│   ├── setup_environment.py
│   └── explore_morphik.py
├── debug/                      # Debug and troubleshooting scripts
│   ├── __init__.py
│   ├── debug_*.py             # All debug scripts
│   └── debug_content.py
├── docs/                       # Documentation and reports
│   ├── __init__.py
│   ├── *.md                   # Markdown documentation
│   └── morphik_bug_report_email.txt
├── results/                    # Output files and logs
│   ├── __init__.py
│   ├── *.json                 # Analysis results
│   └── *.log                  # Log files
├── tests/                      # Test scripts and test data
│   ├── __init__.py
│   ├── test_*.py              # All test scripts
│   ├── comprehensive_*.py     # Comprehensive tests
│   ├── controlled_parser_test.py
│   ├── simple_test.py
│   └── simple_test.txt
└── extracted_images/           # Extracted images from documents
```

## Key Components

### Core (`core/`)
Contains the main functionality:
- **API Server**: `api_server.py` - Main Flask API server
- **Ingestion**: `clean_and_ingest.py` - Main document ingestion script
- **Schemas**: `schemas.py`, `ecss_rules_schema.py` - Data models and rules
- **Working Scripts**: Various working versions of ingestion and processing scripts

### Tests (`tests/`)
All test scripts for validating functionality:
- Unit tests for individual components
- Integration tests for the full pipeline
- Comprehensive test suites

### Debug (`debug/`)
Scripts for troubleshooting and debugging:
- Debug scripts for specific issues
- Content inspection tools
- Metadata extraction debugging

### Analysis (`analysis/`)
Scripts for analyzing the ECSS corpus:
- Document structure analysis
- Corpus processing scripts
- Quick analysis tools

### Configuration (`config/`)
Configuration files:
- Environment variables (`.env`)
- Morphik configuration (`morphik.toml`)
- Python dependencies (`requirements.txt`)

### Results (`results/`)
Output files and logs:
- JSON results from analysis
- Log files from processing

## Import Paths

All scripts have been updated to use the correct import paths. The scripts use:
```python
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
```

This ensures that all scripts can import from the core modules regardless of their location in the directory structure.

## Running Scripts

To run scripts from any subdirectory, use:
```bash
# From the backend directory
python tests/test_script.py
python core/api_server.py
python debug/debug_script.py
```

## Maintenance

When adding new scripts:
1. Place them in the appropriate subdirectory
2. Ensure they use the correct import path pattern
3. Update this README if adding new categories

## Dependencies

All dependencies are listed in `config/requirements.txt`. Install them with:
```bash
pip install -r config/requirements.txt
``` 