"""
Complete Analysis Pipeline with LLM-Enhanced Insights
Runs all analyses and generates dashboard with smart recommendations
"""

import json
import os
from dotenv import load_dotenv
from src.scoring_engine_llm import LLMScoringEngine
from configs.configurations import (STRATEGIC_PLAN_PATH, ACTION_PLAN_PATH,EMBEDDING_ANALYZER_RESULTS_PATH, 
                                    ENTITY_ANALYSIS_RESULTS_PATH, LLM_SYNCHRONIZATION_RESULTS_PATH)


def main():
    print("=" * 70)
    print("COMPLETE SYNCHRONIZATION ANALYSIS WITH LLM INSIGHTS")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("\n❌ OPENAI_API_KEY not found!")
        print("   Add it to your .env file")
        return
    
    # Step 1: Load analysis results
    print("\n[Step 1] Loading analysis results...")
    
    try:
        with open(EMBEDDING_ANALYZER_RESULTS_PATH, 'r') as f:
            embedding_results = json.load(f)
        print("  ✓ Embedding analysis loaded")
    except FileNotFoundError:
        print("  ❌ embedding_analysis_results.json not found")
        print("     Run test_embedding_analyzer.py first!")
        return
    
    try:
        with open(ENTITY_ANALYSIS_RESULTS_PATH, 'r') as f:
            entity_results = json.load(f)
        print("  ✓ Entity analysis loaded")
    except FileNotFoundError:
        print("  ❌ entity_analysis_results.json not found")
        print("     Run test_entity_extractor.py first!")
        return
    
    try:
        with open(STRATEGIC_PLAN_PATH, 'r') as f:
            strategic_doc = json.load(f)
        print("  ✓ Strategic plan loaded")
        
        with open(ACTION_PLAN_PATH, 'r') as f:
            action_doc = json.load(f)
        print("  ✓ Action plan loaded")
    except FileNotFoundError:
        print("  ❌ Document JSON files not found")
        print("     Run test_processor.py first!")
        return
    
    # Step 2: Initialize LLM-enhanced scoring engine
    print("\n[Step 2] Initializing LLM-enhanced scoring engine...")
    print("  (This will use GPT-4 for intelligent insights)")
    
    engine = LLMScoringEngine(
        openai_api_key=openai_key,
        embedding_weight=0.60,  # 60% weight for semantic similarity
        entity_weight=0.40,     # 40% weight for entity matching
        strong_support_threshold=75.0
    )
    print("  ✓ Scoring engine ready with LLM capabilities")
    
    # Step 3: Combine scores with LLM insights
    print("\n[Step 3] Combining analysis results with LLM insights...")
    print("  This may take 10-30 seconds as GPT-4 analyzes the data...")
    
    final_result = engine.combine_scores(
        embedding_results=embedding_results,
        entity_results=entity_results,
        strategic_doc=strategic_doc,
        action_doc=action_doc
    )
    
    # Step 4: Save final results
    print("\n[Step 4] Saving enhanced results...")
    engine.save_results(final_result, LLM_SYNCHRONIZATION_RESULTS_PATH)
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("✅ LLM-ENHANCED ANALYSIS COMPLETE!")
    print("=" * 70)
    
    print("\n📊 Results Summary:")
    print(f"  Overall Score: {final_result.overall_score:.1f}/100")
    print(f"  Strengths Identified: {len(final_result.strengths)}")
    print(f"  Weaknesses Identified: {len(final_result.weaknesses)}")
    print(f"  Recommendations Generated: {len(final_result.recommendations)}")
    
    print("\n💡 Key Improvements with LLM:")
    print("  ✓ Context-aware strengths (no generic statements)")
    print("  ✓ Evidence-based weaknesses (specific data points)")
    print("  ✓ Actionable recommendations (concrete steps)")
    print("  ✓ No contradictions (intelligent analysis)")
    
    print("\nGenerated files:")
    print("  ✓ final_synchronization_results.json (with LLM insights)")
        
    print("\n" + "=" * 70)
    
    # Show preview of insights
    if final_result.strengths:
        print("\n🌟 Sample Strength:")
        print(f"  {final_result.strengths[0][:150]}{'...' if len(final_result.strengths[0]) > 150 else ''}")
    
    if final_result.recommendations:
        print("\n💡 Sample Recommendation:")
        rec = final_result.recommendations[0]
        print(f"  [{rec['priority'].upper()}] {rec.get('objective', 'General')}")
        if rec.get('actions'):
            print(f"  → {rec['actions'][0][:120]}{'...' if len(rec['actions'][0]) > 120 else ''}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
