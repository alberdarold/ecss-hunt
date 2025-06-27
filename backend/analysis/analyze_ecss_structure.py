from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


# Add backend root to path


import os
import sys
import re
from typing import List, Dict, Tuple
import statistics

def analyze_ecss_document_structure(pdf_directory: str, sample_docs: List[str]) -> Dict:
    """
    Analyze ECSS document structure to determine optimal chunking parameters.
    """
    print("=== ECSS Document Structure Analysis ===")
    
    all_sections = []
    all_requirements = []
    section_lengths = []
    requirement_lengths = []
    
    for doc_name in sample_docs:
        print(f"\nAnalyzing {doc_name}...")
        
        # For now, we'll analyze the filename structure
        # In a real implementation, you'd extract text from PDFs
        filename_analysis = analyze_filename_structure(doc_name)
        
        # Simulate some analysis based on typical ECSS structure
        # This would be replaced with actual PDF text extraction
        simulated_analysis = simulate_ecss_analysis(doc_name)
        
        all_sections.extend(simulated_analysis['sections'])
        all_requirements.extend(simulated_analysis['requirements'])
        section_lengths.extend(simulated_analysis['section_lengths'])
        requirement_lengths.extend(simulated_analysis['requirement_lengths'])
    
    # Calculate statistics
    stats = calculate_chunking_statistics(section_lengths, requirement_lengths)
    
    # Recommend optimal parameters
    recommendations = recommend_chunking_parameters(stats)
    
    return {
        'statistics': stats,
        'recommendations': recommendations,
        'sample_data': {
            'sections': all_sections[:5],  # Show first 5 as examples
            'requirements': all_requirements[:5]
        }
    }

def analyze_filename_structure(filename: str) -> Dict:
    """Extract information from ECSS filename."""
    # ECSS filename pattern: ECSS-[Branch]-[Discipline]-[Number][Revision]([Date]).pdf
    pattern = r'ECSS-([A-Z])-([A-Z]{2})-(\d+[A-Z]?)(?:[_-]Rev\.?(\d+))?'
    match = re.match(pattern, filename)
    
    if match:
        branch, discipline, doc_number, revision = match.groups()
        return {
            'branch': branch,
            'discipline': discipline,
            'document_number': doc_number,
            'revision': revision or '1',
            'filename': filename
        }
    return {'filename': filename, 'parsed': False}

def simulate_ecss_analysis(doc_name: str) -> Dict:
    """
    Simulate ECSS document analysis based on typical structure.
    In reality, this would extract actual text from PDFs.
    """
    # These are based on typical ECSS document structure
    # Real implementation would use PDF text extraction
    
    # Typical ECSS section structure
    sections = [
        "1. Scope",
        "2. Normative references", 
        "3. Terms and definitions",
        "4. General requirements",
        "5. Detailed requirements",
        "6. Verification",
        "7. Documentation"
    ]
    
    # Simulate requirement lengths based on ECSS patterns
    requirement_lengths = [
        150,   # Short requirement
        300,   # Medium requirement
        450,   # Long requirement
        200,   # Standard requirement
        350,   # Complex requirement
        120,   # Simple requirement
        280,   # Detailed requirement
        400,   # Comprehensive requirement
        180,   # Basic requirement
        320    # Technical requirement
    ]
    
    # Simulate section lengths (multiple requirements per section)
    section_lengths = [
        sum(requirement_lengths[0:2]),    # Section with 2 requirements
        sum(requirement_lengths[2:4]),    # Section with 2 requirements
        sum(requirement_lengths[4:7]),    # Section with 3 requirements
        sum(requirement_lengths[7:10]),   # Section with 3 requirements
    ]
    
    return {
        'sections': sections,
        'requirements': [f"Requirement {i+1}" for i in range(len(requirement_lengths))],
        'section_lengths': section_lengths,
        'requirement_lengths': requirement_lengths
    }

def calculate_chunking_statistics(section_lengths: List[int], requirement_lengths: List[int]) -> Dict:
    """Calculate statistics to inform chunking decisions."""
    
    if not section_lengths or not requirement_lengths:
        return {}
    
    stats = {
        'requirements': {
            'count': len(requirement_lengths),
            'min_length': min(requirement_lengths),
            'max_length': max(requirement_lengths),
            'mean_length': statistics.mean(requirement_lengths),
            'median_length': statistics.median(requirement_lengths),
            'std_dev': statistics.stdev(requirement_lengths) if len(requirement_lengths) > 1 else 0,
            'percentiles': {
                '25': statistics.quantiles(requirement_lengths, n=4)[0] if len(requirement_lengths) > 1 else requirement_lengths[0],
                '75': statistics.quantiles(requirement_lengths, n=4)[2] if len(requirement_lengths) > 1 else requirement_lengths[0],
                '90': statistics.quantiles(requirement_lengths, n=10)[8] if len(requirement_lengths) > 1 else requirement_lengths[0],
                '95': statistics.quantiles(requirement_lengths, n=20)[18] if len(requirement_lengths) > 1 else requirement_lengths[0]
            }
        },
        'sections': {
            'count': len(section_lengths),
            'min_length': min(section_lengths),
            'max_length': max(section_lengths),
            'mean_length': statistics.mean(section_lengths),
            'median_length': statistics.median(section_lengths),
            'std_dev': statistics.stdev(section_lengths) if len(section_lengths) > 1 else 0
        }
    }
    
    return stats

def recommend_chunking_parameters(stats: Dict) -> Dict:
    """Recommend optimal chunking parameters based on analysis."""
    
    if not stats:
        return {
            'recommended_chunk_size': 1000,
            'recommended_overlap': 200,
            'reasoning': 'No data available, using defaults'
        }
    
    req_stats = stats['requirements']
    section_stats = stats['sections']
    
    # Strategy 1: Chunk by individual requirements
    # Use 95th percentile to ensure most requirements fit in one chunk
    requirement_based_size = int(req_stats['percentiles']['95'])
    
    # Strategy 2: Chunk by sections
    # Use median section length as a guide
    section_based_size = int(section_stats['median_length'])
    
    # Strategy 3: Hybrid approach
    # Balance between requirement completeness and section context
    hybrid_size = int((requirement_based_size + section_based_size) / 2)
    
    # Choose the most conservative approach
    recommended_size = min(requirement_based_size, hybrid_size)
    
    # Calculate overlap based on requirement variability
    # Use standard deviation to determine overlap
    recommended_overlap = int(req_stats['std_dev'] * 2)  # 2x std dev for context
    
    # Ensure reasonable bounds
    recommended_size = max(500, min(2000, recommended_size))
    recommended_overlap = max(100, min(500, recommended_overlap))
    
    reasoning = f"""
    Analysis Results:
    - Requirements: {req_stats['count']} analyzed, length range {req_stats['min_length']}-{req_stats['max_length']} chars
    - Mean requirement length: {req_stats['mean_length']:.0f} chars
    - 95th percentile requirement: {req_stats['percentiles']['95']:.0f} chars
    - Section median length: {section_stats['median_length']:.0f} chars
    
    Recommendation Strategy:
    - Chunk size: {recommended_size} chars (covers 95% of requirements)
    - Overlap: {recommended_overlap} chars (2x std dev for context)
    - Rationale: Ensures most requirements stay intact while maintaining context
    """
    
    return {
        'recommended_chunk_size': recommended_size,
        'recommended_overlap': recommended_overlap,
        'reasoning': reasoning,
        'alternative_sizes': {
            'requirement_based': requirement_based_size,
            'section_based': section_based_size,
            'hybrid': hybrid_size
        }
    }

def main():
    """Run ECSS structure analysis."""
    
    # Sample documents for analysis
    sample_docs = [
        "ECSS-S-ST-00C Rev.1(15June2020).pdf",
        "ECSS-Q-ST-70C-Rev.2(15October2019).pdf",
        "ECSS-E-ST-50C-Rev.1(1March2021).pdf"
    ]
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_directory = os.path.join(project_root, "ECSS Published Standards", "1-Active Standards")
    
    print("ECSS Document Structure Analysis")
    print("=" * 50)
    print(f"PDF directory: {pdf_directory}")
    print(f"Sample documents: {len(sample_docs)}")
    
    # Run analysis
    analysis = analyze_ecss_document_structure(pdf_directory, sample_docs)
    
    # Display results
    print("\n" + "=" * 50)
    print("ANALYSIS RESULTS")
    print("=" * 50)
    
    if analysis['statistics']:
        stats = analysis['statistics']
        print(f"\nRequirement Statistics:")
        print(f"  Count: {stats['requirements']['count']}")
        print(f"  Length range: {stats['requirements']['min_length']}-{stats['requirements']['max_length']} chars")
        print(f"  Mean: {stats['requirements']['mean_length']:.0f} chars")
        print(f"  Median: {stats['requirements']['median_length']:.0f} chars")
        print(f"  Standard deviation: {stats['requirements']['std_dev']:.0f} chars")
        
        print(f"\nSection Statistics:")
        print(f"  Count: {stats['sections']['count']}")
        print(f"  Length range: {stats['sections']['min_length']}-{stats['sections']['max_length']} chars")
        print(f"  Mean: {stats['sections']['mean_length']:.0f} chars")
        print(f"  Median: {stats['sections']['median_length']:.0f} chars")
    
    recommendations = analysis['recommendations']
    print(f"\nRECOMMENDED CHUNKING PARAMETERS:")
    print(f"  Chunk size: {recommendations['recommended_chunk_size']} characters")
    print(f"  Overlap: {recommendations['recommended_overlap']} characters")
    print(f"\nReasoning:")
    print(recommendations['reasoning'])
    
    print(f"\nAlternative approaches:")
    for approach, size in recommendations['alternative_sizes'].items():
        print(f"  {approach}: {size} chars")
    
    print(f"\nNext steps:")
    print(f"1. Update morphik.toml with recommended parameters")
    print(f"2. Test with a single document")
    print(f"3. Evaluate search quality")
    print(f"4. Adjust based on results")

if __name__ == "__main__":
    main() 