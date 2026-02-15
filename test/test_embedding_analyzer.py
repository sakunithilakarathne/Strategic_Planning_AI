"""
Test script for Embedding Analyzer
Run this after document_processor has created the JSON files
"""

import os
import json
from dotenv import load_dotenv
from src.embedding_analyzer import EmbeddingAnalyzer
from configs.configurations import STRATEGIC_PLAN_PATH, ACTION_PLAN_PATH,EMBEDDING_ANALYZER_RESULTS_PATH

# # Get current file location
# BASE_DIR = Path(__file__).resolve().parent.parent
# action_plan_json = BASE_DIR / "data" / "action_plan.json"
# strategic_plan_json = BASE_DIR / "data" / "strategic_plan.json"

def main():
    print("=" * 70)
    print("EMBEDDING ANALYSIS TEST")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Check for API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    pinecone_key = os.getenv('PINECONE_API_KEY')
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    if not pinecone_key:
        print("❌ PINECONE_API_KEY not found in environment variables")
        print("   Create a .env file with: PINECONE_API_KEY=your_key_here")
        return
    
    print("✓ API keys loaded")
    
    # Load processed JSON documents
    print("\nLoading processed documents...")
    try:
        with open(STRATEGIC_PLAN_PATH, 'r', encoding='utf-8') as f:
            strategic_doc = json.load(f)
        print(f"  ✓ Strategic Plan: {len(strategic_doc.get('sections', []))} sections")
        
        with open(ACTION_PLAN_PATH, 'r', encoding='utf-8') as f:
            action_doc = json.load(f)
        print(f"  ✓ Action Plan: {len(action_doc.get('sections', []))} sections")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Run test_processor.py first to generate JSON files")
        return
    
    # Initialize analyzer
    print("\nInitializing Embedding Analyzer...")
    analyzer = EmbeddingAnalyzer(
        openai_api_key=openai_key,
        pinecone_api_key=pinecone_key,
        index_name="strategic-alignment",
        similarity_threshold=0.70  # 70% similarity threshold
    )
    
    # Perform analysis
    print("\nStarting synchronization analysis...")
    print("(This may take a few minutes depending on document size)\n")
    
    result = analyzer.analyze_synchronization(
        strategic_doc=strategic_doc,
        action_doc=action_doc,
        top_k=5  # Find top 5 matching actions per objective
    )
    
    # Save detailed results
    analyzer.save_results(result, EMBEDDING_ANALYZER_RESULTS_PATH)
    
    # Print additional insights
    print("\n" + "=" * 70)
    print("DETAILED INSIGHTS")
    print("=" * 70)
    
    # Show weakest alignments
    weak_alignments = [
        a for a in result.objective_alignments 
        if a.best_match_score < 0.80
    ]
    
    if weak_alignments:
        print(f"\n⚠ {len(weak_alignments)} Objectives with weak alignment (<0.80):")
        for alignment in sorted(weak_alignments, key=lambda x: x.best_match_score):
            print(f"\n  Objective: {alignment.objective_title}")
            print(f"  Best Match Score: {alignment.best_match_score:.3f}")
            if alignment.top_matches:
                print(f"  Best Matching Action: {alignment.top_matches[0].action_title[:70]}...")
    
    # Show strongest alignments
    strong_alignments = sorted(
        result.objective_alignments, 
        key=lambda x: x.best_match_score, 
        reverse=True
    )[:3]
    
    print(f"\n✓ Top 3 Strongest Alignments:")
    for i, alignment in enumerate(strong_alignments, 1):
        print(f"\n  {i}. Objective: {alignment.objective_title}")
        print(f"     Score: {alignment.best_match_score:.3f}")
        if alignment.top_matches:
            print(f"     Best Action: {alignment.top_matches[0].action_title[:70]}...")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - embedding_analysis_results.json (detailed results)")


if __name__ == "__main__":
    main()
