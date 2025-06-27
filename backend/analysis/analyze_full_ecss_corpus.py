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
from collections import defaultdict

def discover_all_ecss_documents(pdf_directory: str) -> List[str]:
    """Discover all ECSS PDF documents in the directory."""
    print("=== Discovering ECSS Documents ===")
    
    if not os.path.exists(pdf_directory):
        print(f"✗ PDF directory not found: {pdf_directory}")
        return []
    
    # Find all PDF files
    pdf_files = []
    for root, dirs, files in os.walk(pdf_directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                # Get relative path from the PDF directory
                rel_path = os.path.relpath(os.path.join(root, file), pdf_directory)
                pdf_files.append(rel_path)
    
    print(f"✓ Found {len(pdf_files)} PDF files")
    
    # Filter for ECSS documents (should start with ECSS-)
    ecss_files = [f for f in pdf_files if f.startswith('ECSS-')]
    non_ecss_files = [f for f in pdf_files if not f.startswith('ECSS-')]
    
    print(f"  ECSS documents: {len(ecss_files)}")
    print(f"  Non-ECSS documents: {len(non_ecss_files)}")
    
    if non_ecss_files:
        print(f"  Non-ECSS files found: {non_ecss_files[:5]}...")
    
    return ecss_files

def categorize_ecss_documents(documents: List[str]) -> Dict:
    """Categorize ECSS documents by branch, discipline, and type."""
    print("\n=== Categorizing ECSS Documents ===")
    
    categories = {
        'by_branch': defaultdict(list),
        'by_discipline': defaultdict(list),
        'by_type': defaultdict(list),
        'by_revision': defaultdict(list),
        'total_count': len(documents)
    }
    
    for doc in documents:
        # Parse ECSS filename: ECSS-[Branch]-[Discipline]-[Number][Revision]([Date]).pdf
        pattern = r'ECSS-([A-Z])-([A-Z]{2})-(\d+[A-Z]?)(?:[_-]Rev\.?(\d+))?'
        match = re.match(pattern, doc)
        
        if match:
            branch, discipline, doc_number, revision = match.groups()
            
            # Categorize by branch
            branch_name = {
                'E': 'Engineering',
                'M': 'Management', 
                'Q': 'Quality Assurance',
                'S': 'Space Product Assurance',
                'U': 'Space Sustainability'
            }.get(branch, 'Unknown')
            
            categories['by_branch'][branch_name].append(doc)
            
            # Categorize by discipline
            discipline_name = {
                'ST': 'Space Systems',
                'HB': 'Handbooks',
                'TM': 'Technical Memoranda',
                'AS': 'Application Standards'
            }.get(discipline, discipline)
            
            categories['by_discipline'][discipline_name].append(doc)
            
            # Categorize by revision
            rev = revision or '1'
            categories['by_revision'][rev].append(doc)
            
            # Categorize by type (Active vs Superseded)
            if 'Superseded' in doc or '2-Superseded' in doc:
                categories['by_type']['Superseded'].append(doc)
            else:
                categories['by_type']['Active'].append(doc)
    
    # Print summary
    print(f"Total ECSS documents: {categories['total_count']}")
    
    print(f"\nBy Branch:")
    for branch, docs in categories['by_branch'].items():
        print(f"  {branch}: {len(docs)} documents")
    
    print(f"\nBy Discipline:")
    for discipline, docs in categories['by_discipline'].items():
        print(f"  {discipline}: {len(docs)} documents")
    
    print(f"\nBy Type:")
    for doc_type, docs in categories['by_type'].items():
        print(f"  {doc_type}: {len(docs)} documents")
    
    print(f"\nBy Revision:")
    for rev, docs in categories['by_revision'].items():
        print(f"  Rev {rev}: {len(docs)} documents")
    
    return categories

def estimate_document_sizes(pdf_directory: str, documents: List[str]) -> Dict:
    """Estimate document sizes to understand processing requirements."""
    print("\n=== Estimating Document Sizes ===")
    
    size_data = {
        'total_size_mb': 0,
        'size_distribution': [],
        'size_categories': {
            'small': [],    # < 1 MB
            'medium': [],   # 1-5 MB
            'large': [],    # 5-10 MB
            'very_large': [] # > 10 MB
        }
    }
    
    for doc in documents:
        full_path = os.path.join(pdf_directory, doc)
        try:
            size_bytes = os.path.getsize(full_path)
            size_mb = size_bytes / (1024 * 1024)
            size_data['total_size_mb'] += size_mb
            size_data['size_distribution'].append(size_mb)
            
            # Categorize by size
            if size_mb < 1:
                size_data['size_categories']['small'].append(doc)
            elif size_mb < 5:
                size_data['size_categories']['medium'].append(doc)
            elif size_mb < 10:
                size_data['size_categories']['large'].append(doc)
            else:
                size_data['size_categories']['very_large'].append(doc)
                
        except Exception as e:
            print(f"⚠ Could not get size for {doc}: {e}")
    
    # Calculate statistics
    if size_data['size_distribution']:
        size_data['statistics'] = {
            'count': len(size_data['size_distribution']),
            'min_mb': min(size_data['size_distribution']),
            'max_mb': max(size_data['size_distribution']),
            'mean_mb': statistics.mean(size_data['size_distribution']),
            'median_mb': statistics.median(size_data['size_distribution']),
            'std_dev_mb': statistics.stdev(size_data['size_distribution']) if len(size_data['size_distribution']) > 1 else 0
        }
    
    # Print summary
    print(f"Total corpus size: {size_data['total_size_mb']:.1f} MB")
    
    if 'statistics' in size_data:
        stats = size_data['statistics']
        print(f"Document size statistics:")
        print(f"  Count: {stats['count']}")
        print(f"  Range: {stats['min_mb']:.1f} - {stats['max_mb']:.1f} MB")
        print(f"  Mean: {stats['mean_mb']:.1f} MB")
        print(f"  Median: {stats['median_mb']:.1f} MB")
    
    print(f"\nSize distribution:")
    for category, docs in size_data['size_categories'].items():
        print(f"  {category}: {len(docs)} documents")
    
    return size_data

def recommend_sampling_strategy(categories: Dict, size_data: Dict) -> Dict:
    """Recommend a sampling strategy for comprehensive analysis."""
    print("\n=== Sampling Strategy Recommendation ===")
    
    total_docs = categories['total_count']
    
    # If we have a manageable number, analyze all
    if total_docs <= 50:
        strategy = {
            'approach': 'full_analysis',
            'sample_size': total_docs,
            'reasoning': f'Only {total_docs} documents - analyze all'
        }
    else:
        # For larger datasets, use stratified sampling
        sample_size = min(50, total_docs)  # Cap at 50 for cost reasons
        
        # Stratified sampling by branch
        branch_samples = {}
        for branch, docs in categories['by_branch'].items():
            if docs:
                # Proportional sampling
                branch_sample_size = max(1, int(len(docs) * sample_size / total_docs))
                branch_samples[branch] = min(branch_sample_size, len(docs))
        
        strategy = {
            'approach': 'stratified_sampling',
            'sample_size': sample_size,
            'branch_samples': branch_samples,
            'reasoning': f'Large dataset ({total_docs} docs) - use stratified sampling'
        }
    
    print(f"Recommended approach: {strategy['approach']}")
    print(f"Sample size: {strategy['sample_size']}")
    print(f"Reasoning: {strategy['reasoning']}")
    
    if 'branch_samples' in strategy:
        print(f"Branch sampling:")
        for branch, size in strategy['branch_samples'].items():
            print(f"  {branch}: {size} documents")
    
    return strategy

def estimate_processing_costs(size_data: Dict, sample_size: int) -> Dict:
    """Estimate processing costs for the analysis."""
    print("\n=== Cost Estimation ===")
    
    # Rough estimates based on typical Morphik pricing
    avg_size_mb = size_data['statistics']['mean_mb'] if 'statistics' in size_data else 2.0
    
    # Ingestion cost: ~$0.01 per MB
    ingestion_cost_per_doc = avg_size_mb * 0.01
    
    # Graph creation cost: ~$0.10 per document for GPT-4o
    graph_cost_per_doc = 0.10
    
    total_cost_per_doc = ingestion_cost_per_doc + graph_cost_per_doc
    total_cost = total_cost_per_doc * sample_size
    
    cost_estimate = {
        'ingestion_cost_per_doc': ingestion_cost_per_doc,
        'graph_cost_per_doc': graph_cost_per_doc,
        'total_cost_per_doc': total_cost_per_doc,
        'sample_size': sample_size,
        'total_estimated_cost': total_cost,
        'avg_doc_size_mb': avg_size_mb
    }
    
    print(f"Cost estimates for {sample_size} documents:")
    print(f"  Average document size: {avg_size_mb:.1f} MB")
    print(f"  Ingestion cost per doc: ${ingestion_cost_per_doc:.3f}")
    print(f"  Graph creation cost per doc: ${graph_cost_per_doc:.2f}")
    print(f"  Total cost per doc: ${total_cost_per_doc:.2f}")
    print(f"  Total estimated cost: ${total_cost:.2f}")
    
    return cost_estimate

def main():
    """Run comprehensive ECSS corpus analysis."""
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    pdf_directory = os.path.join(project_root, "ECSS Published Standards", "1-Active Standards")
    
    print("=== Comprehensive ECSS Corpus Analysis ===")
    print(f"PDF directory: {pdf_directory}")
    
    # Step 1: Discover all documents
    all_documents = discover_all_ecss_documents(pdf_directory)
    
    if not all_documents:
        print("✗ No ECSS documents found. Exiting.")
        return
    
    # Step 2: Categorize documents
    categories = categorize_ecss_documents(all_documents)
    
    # Step 3: Estimate document sizes
    size_data = estimate_document_sizes(pdf_directory, all_documents)
    
    # Step 4: Recommend sampling strategy
    sampling_strategy = recommend_sampling_strategy(categories, size_data)
    
    # Step 5: Estimate costs
    cost_estimate = estimate_processing_costs(size_data, sampling_strategy['sample_size'])
    
    # Final summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 60)
    
    print(f"Total ECSS documents discovered: {categories['total_count']}")
    print(f"Total corpus size: {size_data['total_size_mb']:.1f} MB")
    print(f"Recommended sample size: {sampling_strategy['sample_size']}")
    print(f"Estimated cost: ${cost_estimate['total_estimated_cost']:.2f}")
    
    print(f"\nKey findings:")
    print(f"1. Document diversity: {len(categories['by_branch'])} branches, {len(categories['by_discipline'])} disciplines")
    print(f"2. Size variation: {size_data['statistics']['min_mb']:.1f} - {size_data['statistics']['max_mb']:.1f} MB per document")
    print(f"3. Processing approach: {sampling_strategy['approach']}")
    
    print(f"\nNext steps:")
    print(f"1. Review the sampling strategy")
    print(f"2. Consider cost vs. coverage trade-offs")
    print(f"3. Run analysis on recommended sample")
    print(f"4. Validate results with full corpus if needed")
    
    # Save results for reference
    results = {
        'categories': categories,
        'size_data': size_data,
        'sampling_strategy': sampling_strategy,
        'cost_estimate': cost_estimate
    }
    
    return results

if __name__ == "__main__":
    main() 