"""
Test script for Entity Extractor
Extracts and matches explicit entities between Strategic and Action Plans
"""

import json
from src.entity_extractor import EntityExtractor
from configs.configurations import STRATEGIC_PLAN_PATH, ACTION_PLAN_PATH, ENTITY_ANALYSIS_RESULTS_PATH

def main():
    print("=" * 70)
    print("ENTITY MATCHING ANALYSIS TEST")
    print("=" * 70)
    
    # Load processed JSON documents
    print("\nLoading documents...")
    try:
        with open(STRATEGIC_PLAN_PATH, 'r', encoding='utf-8') as f:
            strategic_doc = json.load(f)
        print(f"  ✓ Strategic Plan loaded")
        
        with open(ACTION_PLAN_PATH, 'r', encoding='utf-8') as f:
            action_doc = json.load(f)
        print(f"  ✓ Action Plan loaded")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Run test_processor.py first to generate JSON files")
        return
    
    # Initialize entity extractor
    print("\nInitializing Entity Extractor...")
    print("  (This will download spaCy model if not already installed)")
    
    extractor = EntityExtractor(fuzzy_threshold=85)
    print("  ✓ Entity extractor ready")
    
    # Perform entity analysis
    print("\nStarting entity matching analysis...")
    print("(Extracting KPIs, budgets, timelines, goals, initiatives...)\n")
    
    result = extractor.analyze_documents(
        strategic_doc=strategic_doc,
        action_doc=action_doc
    )
    
    # Save results
    extractor.save_results(result, ENTITY_ANALYSIS_RESULTS_PATH)
    
    # Print detailed insights
    print("\n" + "=" * 70)
    print("DETAILED ENTITY ANALYSIS")
    print("=" * 70)
    
    # Show some example matches
    if result.entity_matches:
        print("\n✓ Example Successful Matches:")
        for i, match in enumerate(result.entity_matches[:5], 1):
            print(f"\n  {i}. [{match.strategic_entity.type}] ({match.match_score:.0f}% match)")
            print(f"     Strategic: {match.strategic_entity.text[:60]}...")
            print(f"     Action:    {match.action_entity.text[:60]}...")
    
    # Show unmatched entities by type
    print("\n⚠ Unmatched Strategic Entities by Type:")
    unmatched_by_type = {}
    for entity in result.unmatched_strategic_entities:
        if entity.type not in unmatched_by_type:
            unmatched_by_type[entity.type] = []
        unmatched_by_type[entity.type].append(entity)
    
    for entity_type, entities in unmatched_by_type.items():
        print(f"\n  {entity_type} ({len(entities)} unmatched):")
        for entity in entities[:3]:
            print(f"    - {entity.text[:60]}...")
    
    # Show match quality distribution
    print("\n📊 Match Quality Distribution:")
    exact_matches = sum(1 for m in result.entity_matches if m.match_type == "exact")
    fuzzy_matches = sum(1 for m in result.entity_matches if m.match_type == "fuzzy")
    partial_matches = sum(1 for m in result.entity_matches if m.match_type == "partial")
    
    total_matches = len(result.entity_matches)
    if total_matches > 0:
        print(f"  Exact matches: {exact_matches} ({exact_matches/total_matches*100:.1f}%)")
        print(f"  Fuzzy matches: {fuzzy_matches} ({fuzzy_matches/total_matches*100:.1f}%)")
        print(f"  Partial matches: {partial_matches} ({partial_matches/total_matches*100:.1f}%)")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - entity_analysis_results.json")
    print("\nKey Insights:")
    print(f"  - Overall Entity Match Score: {result.overall_score:.1f}/100")
    print(f"  - {result.matched_entities}/{result.total_strategic_entities} entities matched")
    print(f"  - Match Rate: {result.match_rate:.1f}%")


if __name__ == "__main__":
    main()
