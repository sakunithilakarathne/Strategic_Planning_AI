"""
Complete Analysis Pipeline
Runs all analyses and generates dashboard
"""

import json
from src.scoring_engine import ScoringEngine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
embedding_analysis_results_json = BASE_DIR / "data" / "embedding_analysis_results.json"
entity_analysis_results_json = BASE_DIR / "data" / "entity_analysis_results.json"
strategic_plan_json = BASE_DIR / "data" / "strategic_plan.json"
action_plan_json = BASE_DIR / "data" / "action_plan.json"

def main():
    print("=" * 70)
    print("COMPLETE SYNCHRONIZATION ANALYSIS PIPELINE")
    print("=" * 70)
    
    # Step 1: Load analysis results
    print("\n[Step 1] Loading analysis results...")
    
    try:
        with open(embedding_analysis_results_json, 'r') as f:
            embedding_results = json.load(f)
        print("  ✓ Embedding analysis loaded")
    except FileNotFoundError:
        print("  ❌ embedding_analysis_results.json not found")
        print("     Run test_embedding_analyzer.py first!")
        return
    
    try:
        with open(entity_analysis_results_json, 'r') as f:
            entity_results = json.load(f)
        print("  ✓ Entity analysis loaded")
    except FileNotFoundError:
        print("  ❌ entity_analysis_results.json not found")
        print("     Run test_entity_extractor.py first!")
        return
    
    try:
        with open(strategic_plan_json, 'r') as f:
            strategic_doc = json.load(f)
        print("  ✓ Strategic plan loaded")
        
        with open(action_plan_json, 'r') as f:
            action_doc = json.load(f)
        print("  ✓ Action plan loaded")
    except FileNotFoundError:
        print("  ❌ Document JSON files not found")
        print("     Run test_processor.py first!")
        return
    
    # Step 2: Initialize scoring engine
    print("\n[Step 2] Initializing scoring engine...")
    engine = ScoringEngine(
        embedding_weight=0.60,  # 60% weight for semantic similarity
        entity_weight=0.40,     # 40% weight for entity matching
        strong_support_threshold=75.0  # 75+ = strong support
    )
    print("  ✓ Scoring engine ready")
    
    # Step 3: Combine scores
    print("\n[Step 3] Combining analysis results...")
    final_result = engine.combine_scores(
        embedding_results=embedding_results,
        entity_results=entity_results,
        strategic_doc=strategic_doc,
        action_doc=action_doc
    )
    
    # Step 4: Save final results
    print("\n[Step 4] Saving final results...")
    engine.save_results(final_result, 'final_synchronization_results.json')
    
    # Step 5: Launch dashboard info
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  ✓ final_synchronization_results.json")
    print("\nTo view the interactive dashboard:")
    print("  streamlit run dashboard.py")
    print("\nThe dashboard will open in your browser and show:")
    print("  • Overall synchronization score with gauges")
    print("  • Per-objective alignment analysis")
    print("  • Interactive charts and visualizations")
    print("  • Strengths, weaknesses, and recommendations")
    print("  • Export functionality for reports")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
