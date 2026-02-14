"""
Test script for Document Processor
Demonstrates how to use the processor with your Strategic and Action Plans
"""

from src.document_processor import DocumentProcessor
import json
from pathlib import Path

# Get current file location
BASE_DIR = Path(__file__).resolve().parent.parent
action_data_path = BASE_DIR / "data" / "action_plan_commercial_bank.md"
strategic_pdf_path = BASE_DIR / "data" / "strategic_plan_commercial_bank.md"

def main():

    print("=" * 60)
    print("DOCUMENT PROCESSOR - TEST SCRIPT")
    print("=" * 60)
    print()
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Process Strategic Plan
    print("STEP 1: Processing Strategic Plan PDF...")
    print("-" * 60)
    try:
        strategic_doc = processor.process_document(
            strategic_pdf_path,  
            doc_type="strategic_plan"
        )
        
        print("\nStrategic Plan Summary:")
        print(f"  Title: {strategic_doc.title}")
        print(f"  Organization: {strategic_doc.organization}")
        print(f"  Period: {strategic_doc.planning_period}")
        print(f"  Sections: {len(strategic_doc.sections)}")
        print(f"  Total Budget: ${strategic_doc.total_budget:,.0f}" if strategic_doc.total_budget else "  Total Budget: Not found")
        
        # Save to JSON
        processor.to_json(strategic_doc, "strategic_plan.json")
        
    except Exception as e:
        print(f"Error processing Strategic Plan: {e}")
    
    print("\n")
    
    # Process Action Plan
    print("STEP 2: Processing Action Plan PDF...")
    print("-" * 60)
    try:
        action_doc = processor.process_document(
            action_data_path,
            doc_type="action_plan"
        )
        
        print("\nAction Plan Summary:")
        print(f"  Title: {action_doc.title}")
        print(f"  Organization: {action_doc.organization}")
        print(f"  Period: {action_doc.planning_period}")
        print(f"  Sections: {len(action_doc.sections)}")
        print(f"  Total Budget: ${action_doc.total_budget:,.0f}" if action_doc.total_budget else "  Total Budget: Not found")
        
        # Save to JSON
        processor.to_json(action_doc, "action_plan.json")
        
    except Exception as e:
        print(f"Error processing Action Plan: {e}")
    
    print("\n")
    print("=" * 60)
    print("PROCESSING COMPLETE!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - strategic_plan.json")
    print("  - action_plan.json")
    print("\nYou can now use these JSON files for the embedding analysis step.")


if __name__ == "__main__":
    main()
