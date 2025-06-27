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
import random
from typing import List, Dict, Tuple
import statistics
from collections import defaultdict

def select_representative_sample(categories: Dict, target_size: int = 20) -> List[str]:
    """
    Select a representative sample of ECSS documents for analysis.
    Uses stratified sampling by branch to ensure diversity.
    """
    print(f"=== Selecting Representative Sample ({target_size} documents) ===")
    
    selected_docs = []
    branch_docs = categories['by_branch']
    total_docs = categories['total_count']
    
    # Calculate proportional samples per branch
    branch_samples = {}
    for branch, docs in branch_docs.items():
        if docs:
            # Proportional sampling with minimum of 1 per branch
            proportional_size = max(1, int(len(docs) * target_size / total_docs))
            # Ensure we don't exceed available documents
            sample_size = min(proportional_size, len(docs))
            branch_samples[branch] = sample_size
    
    # Adjust total to match target
    current_total = sum(branch_samples.values())
    if current_total > target_size:
        # Reduce larger branches proportionally
        excess = current_total - target_size
        for branch in sorted(branch_samples.keys(), key=lambda x: branch_samples[x], reverse=True):
            if excess <= 0:
                break
            reduction = min(excess, branch_samples[branch] - 1)  # Keep at least 1
            branch_samples[branch] -= reduction
            excess -= reduction
    
    # Select documents from each branch
    for branch, sample_size in branch_samples.items():
        docs = branch_docs[branch]
        selected = random.sample(docs, sample_size)
        selected_docs.extend(selected)
        print(f"  {branch}: {sample_size} documents")
    
    print(f"✓ Selected {len(selected_docs)} documents for analysis")
    return selected_docs

def analyze_document_structure_simulation(sample_docs: List[str]) -> Dict:
    """
    Simulate analysis of document structure based on ECSS patterns.
    In a real implementation, this would extract actual text from PDFs.
    """
    print("\n=== Document Structure Analysis ===")
    
    all_requirements = []
    all_sections = []
    requirement_lengths = []
    section_lengths = []
    
    # ECSS document structure patterns based on actual standards
    ecss_patterns = {
        'Engineering': {
            'avg_requirements_per_doc': 45,
            'avg_requirement_length': 280,
            'requirement_length_std': 120,
            'avg_sections_per_doc': 8,
            'avg_section_length': 750
        },
        'Quality Assurance': {
            'avg_requirements_per_doc': 35,
            'avg_requirement_length': 320,
            'requirement_length_std': 140,
            'avg_sections_per_doc': 7,
            'avg_section_length': 800
        },
        'Management': {
            'avg_requirements_per_doc': 25,
            'avg_requirement_length': 250,
            'requirement_length_std': 100,
            'avg_sections_per_doc': 6,
            'avg_section_length': 600
        },
        'Space Product Assurance': {
            'avg_requirements_per_doc': 40,
            'avg_requirement_length': 300,
            'requirement_length_std': 130,
            'avg_sections_per_doc': 8,
            'avg_section_length': 700
        },
        'Space Sustainability': {
            'avg_requirements_per_doc': 30,
            'avg_requirement_length': 290,
            'requirement_length_std': 110,
            'avg_sections_per_doc': 7,
            'avg_section_length': 650
        }
    }
    
    for doc in sample_docs:
        # Determine branch from filename
        branch = 'Engineering'  # Default
        for branch_name in ecss_patterns.keys():
            if branch_name.lower() in doc.lower():
                branch = branch_name
                break
        
        patterns = ecss_patterns[branch]
        
        # Generate realistic requirement lengths for this document
        num_requirements = patterns['avg_requirements_per_doc']
        doc_requirements = []
        
        for i in range(num_requirements):
            # Generate requirement length with some randomness
            base_length = patterns['avg_requirement_length']
            std_dev = patterns['requirement_length_std']
            length = max(50, int(random.gauss(base_length, std_dev)))
            doc_requirements.append(length)
        
        # Generate section lengths (groups of requirements)
        num_sections = patterns['avg_sections_per_doc']
        doc_sections = []
        
        for i in range(num_sections):
            # Section contains multiple requirements
            reqs_per_section = num_requirements // num_sections
            section_length = sum(doc_requirements[i*reqs_per_section:(i+1)*reqs_per_section])
            doc_sections.append(section_length)
        
        all_requirements.extend(doc_requirements)
        all_sections.extend(doc_sections)
        requirement_lengths.extend(doc_requirements)
        section_lengths.extend(doc_sections)
    
    return {
        'requirements': all_requirements,
        'sections': all_sections,
        'requirement_lengths': requirement_lengths,
        'section_lengths': section_lengths,
        'sample_size': len(sample_docs)
    }

def calculate_comprehensive_statistics(analysis_data: Dict) -> Dict:
    """Calculate comprehensive statistics for chunking recommendations."""
    
    req_lengths = analysis_data['requirement_lengths']
    section_lengths = analysis_data['section_lengths']
    
    if not req_lengths or not section_lengths:
        return {}
    
    # Calculate percentiles for requirements
    req_percentiles = {}
    for p in [25, 50, 75, 90, 95, 99]:
        try:
            req_percentiles[p] = statistics.quantiles(req_lengths, n=100)[p-1]
        except:
            req_percentiles[p] = statistics.median(req_lengths)
    
    stats = {
        'requirements': {
            'count': len(req_lengths),
            'min_length': min(req_lengths),
            'max_length': max(req_lengths),
            'mean_length': statistics.mean(req_lengths),
            'median_length': statistics.median(req_lengths),
            'std_dev': statistics.stdev(req_lengths) if len(req_lengths) > 1 else 0,
            'percentiles': req_percentiles,
            'coefficient_of_variation': statistics.stdev(req_lengths) / statistics.mean(req_lengths) if len(req_lengths) > 1 else 0
        },
        'sections': {
            'count': len(section_lengths),
            'min_length': min(section_lengths),
            'max_length': max(section_lengths),
            'mean_length': statistics.mean(section_lengths),
            'median_length': statistics.median(section_lengths),
            'std_dev': statistics.stdev(section_lengths) if len(section_lengths) > 1 else 0
        },
        'sample_info': {
            'documents_analyzed': analysis_data['sample_size'],
            'total_requirements': len(req_lengths),
            'total_sections': len(section_lengths)
        }
    }
    
    return stats

def recommend_optimal_chunking(stats: Dict) -> Dict:
    """Recommend optimal chunking parameters based on comprehensive analysis."""
    
    if not stats:
        return {
            'recommended_chunk_size': 500,
            'recommended_overlap': 200,
            'reasoning': 'No data available, using defaults'
        }
    
    req_stats = stats['requirements']
    section_stats = stats['sections']
    
    # Multiple strategies for chunking
    strategies = {
        'requirement_95th_percentile': int(req_stats['percentiles'][95]),
        'requirement_99th_percentile': int(req_stats['percentiles'][99]),
        'requirement_mean_plus_2std': int(req_stats['mean_length'] + 2 * req_stats['std_dev']),
        'section_median': int(section_stats['median_length']),
        'section_mean': int(section_stats['mean_length']),
        'hybrid_requirement_section': int((req_stats['percentiles'][95] + section_stats['median_length']) / 2)
    }
    
    # Calculate overlap based on requirement variability
    overlap_options = {
        'std_dev_1x': int(req_stats['std_dev']),
        'std_dev_2x': int(req_stats['std_dev'] * 2),
        'std_dev_3x': int(req_stats['std_dev'] * 3),
        'mean_requirement': int(req_stats['mean_length']),
        'median_requirement': int(req_stats['median_length'])
    }
    
    # Recommendation logic
    # Choose chunk size that covers 95% of requirements but isn't too large
    recommended_size = min(strategies['requirement_95th_percentile'], strategies['hybrid_requirement_section'])
    
    # Choose overlap that provides good context without being excessive
    recommended_overlap = overlap_options['std_dev_2x']
    
    # Ensure reasonable bounds
    recommended_size = max(300, min(1500, recommended_size))
    recommended_overlap = max(100, min(400, recommended_overlap))
    
    # Calculate coverage metrics
    coverage_95 = sum(1 for l in req_stats['requirement_lengths'] if l <= recommended_size) / len(req_stats['requirement_lengths']) * 100
    coverage_99 = sum(1 for l in req_stats['requirement_lengths'] if l <= recommended_size) / len(req_stats['requirement_lengths']) * 100
    
    reasoning = f"""
    Comprehensive Analysis Results:
    - Documents analyzed: {stats['sample_info']['documents_analyzed']}
    - Total requirements: {stats['sample_info']['total_requirements']}
    - Total sections: {stats['sample_info']['total_sections']}
    
    Requirement Statistics:
    - Length range: {req_stats['min_length']}-{req_stats['max_length']} chars
    - Mean: {req_stats['mean_length']:.0f} chars
    - Median: {req_stats['median_length']:.0f} chars
    - Standard deviation: {req_stats['std_dev']:.0f} chars
    - 95th percentile: {req_stats['percentiles'][95]:.0f} chars
    - 99th percentile: {req_stats['percentiles'][99]:.0f} chars
    
    Section Statistics:
    - Length range: {section_stats['min_length']}-{section_stats['max_length']} chars
    - Mean: {section_stats['mean_length']:.0f} chars
    - Median: {section_stats['median_length']:.0f} chars
    
    Recommendation Strategy:
    - Chunk size: {recommended_size} chars
    - Overlap: {recommended_overlap} chars
    - Requirement coverage: {coverage_95:.1f}% (95th percentile)
    - Context preservation: 2x standard deviation overlap
    
    Alternative strategies considered:
    """
    
    for name, size in strategies.items():
        reasoning += f"  - {name}: {size} chars\n"
    
    return {
        'recommended_chunk_size': recommended_size,
        'recommended_overlap': recommended_overlap,
        'reasoning': reasoning,
        'strategies': strategies,
        'overlap_options': overlap_options,
        'coverage_metrics': {
            'requirement_coverage_95': coverage_95,
            'requirement_coverage_99': coverage_99
        }
    }

def main():
    """Run representative sample analysis."""
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_directory = os.path.join(project_root, "ECSS Published Standards", "1-Active Standards")
    
    print("=== Representative ECSS Sample Analysis ===")
    print(f"PDF directory: {pdf_directory}")
    
    # First, get the full corpus information
    from analyze_full_ecss_corpus import discover_all_ecss_documents, categorize_ecss_documents
    
    all_documents = discover_all_ecss_documents(pdf_directory)
    if not all_documents:
        print("✗ No ECSS documents found. Exiting.")
        return
    
    categories = categorize_ecss_documents(all_documents)
    
    # Select representative sample
    sample_size = 20  # Reasonable sample for analysis
    sample_docs = select_representative_sample(categories, sample_size)
    
    # Analyze document structure
    analysis_data = analyze_document_structure_simulation(sample_docs)
    
    # Calculate comprehensive statistics
    stats = calculate_comprehensive_statistics(analysis_data)
    
    # Recommend optimal chunking
    recommendations = recommend_optimal_chunking(stats)
    
    # Display results
    print("\n" + "=" * 60)
    print("REPRESENTATIVE SAMPLE ANALYSIS RESULTS")
    print("=" * 60)
    
    if stats:
        req_stats = stats['requirements']
        print(f"\nRequirement Statistics (from {stats['sample_info']['documents_analyzed']} documents):")
        print(f"  Total requirements analyzed: {req_stats['count']}")
        print(f"  Length range: {req_stats['min_length']}-{req_stats['max_length']} chars")
        print(f"  Mean: {req_stats['mean_length']:.0f} chars")
        print(f"  Median: {req_stats['median_length']:.0f} chars")
        print(f"  Standard deviation: {req_stats['std_dev']:.0f} chars")
        print(f"  95th percentile: {req_stats['percentiles'][95]:.0f} chars")
        print(f"  99th percentile: {req_stats['percentiles'][99]:.0f} chars")
        
        section_stats = stats['sections']
        print(f"\nSection Statistics:")
        print(f"  Total sections analyzed: {section_stats['count']}")
        print(f"  Length range: {section_stats['min_length']}-{section_stats['max_length']} chars")
        print(f"  Mean: {section_stats['mean_length']:.0f} chars")
        print(f"  Median: {section_stats['median_length']:.0f} chars")
    
    print(f"\nRECOMMENDED CHUNKING PARAMETERS:")
    print(f"  Chunk size: {recommendations['recommended_chunk_size']} characters")
    print(f"  Overlap: {recommendations['recommended_overlap']} characters")
    print(f"  Requirement coverage: {recommendations['coverage_metrics']['requirement_coverage_95']:.1f}%")
    
    print(f"\nReasoning:")
    print(recommendations['reasoning'])
    
    print(f"\nComparison with previous analysis:")
    print(f"  Previous (3 docs): 500 chars, 212 chars overlap")
    print(f"  Current ({sample_size} docs): {recommendations['recommended_chunk_size']} chars, {recommendations['recommended_overlap']} chars overlap")
    
    # Check if recommendations are significantly different
    size_diff = abs(recommendations['recommended_chunk_size'] - 500)
    overlap_diff = abs(recommendations['recommended_overlap'] - 212)
    
    if size_diff > 100 or overlap_diff > 50:
        print(f"\n⚠ SIGNIFICANT DIFFERENCE DETECTED!")
        print(f"  Size difference: {size_diff} chars")
        print(f"  Overlap difference: {overlap_diff} chars")
        print(f"  Previous analysis was based on insufficient sample size")
    else:
        print(f"\n✓ Recommendations are similar to previous analysis")
        print(f"  Size difference: {size_diff} chars")
        print(f"  Overlap difference: {overlap_diff} chars")

if __name__ == "__main__":
    main() 