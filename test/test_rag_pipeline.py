"""
Test RAG Pipeline - Build Vector Store and Answer Questions
"""

import os
import json
from dotenv import load_dotenv
from src.rag_pipeline import RAGPipeline
from configs.configurations import (STRATEGIC_PLAN_PATH, ACTION_PLAN_PATH, LLM_SYNCHRONIZATION_RESULTS_PATH)


def main():
    print("=" * 70)
    print("RAG PIPELINE - VECTOR STORE BUILDER")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    pinecone_key = os.getenv('PINECONE_API_KEY')
    
    if not openai_key or not pinecone_key:
        print("\n❌ Missing API keys!")
        print("   Ensure .env has OPENAI_API_KEY and PINECONE_API_KEY")
        return
    
    # Load documents
    print("\n[Step 1] Loading documents...")
    try:
        with open(STRATEGIC_PLAN_PATH, 'r') as f:
            strategic_doc = json.load(f)
        print("  ✓ Strategic plan loaded")
        
        with open(ACTION_PLAN_PATH, 'r') as f:
            action_doc = json.load(f)
        print("  ✓ Action plan loaded")
        
        with open(LLM_SYNCHRONIZATION_RESULTS_PATH, 'r') as f:
            analysis_results = json.load(f)
        print("  ✓ Analysis results loaded")
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Run the complete analysis pipeline first!")
        return
    
    # Initialize RAG pipeline
    print("\n[Step 2] Initializing RAG pipeline...")
    rag = RAGPipeline(
        openai_api_key=openai_key,
        pinecone_api_key=pinecone_key,
        index_name="strategic-rag"
    )
    print("  ✓ RAG pipeline ready")
    
    # Build vector store
    print("\n[Step 3] Building vector store...")
    print("  (This will take 1-2 minutes to chunk and embed all documents)")
    
    rag.build_vector_store(
        strategic_doc=strategic_doc,
        action_doc=action_doc,
        analysis_results=analysis_results
    )
    
    # Test with sample questions
    print("\n" + "="*70)
    print("TESTING RAG Q&A CAPABILITIES")
    print("="*70)
    
    test_questions = [
        "Why is the Digital Transformation objective scoring well?",
        "What are the weaknesses in Risk Management?",
        "What specific KPIs are missing in the action plan?",
        "What recommendations were made for improving alignment?",
        "How does the entity matching score compare to embedding score?"
    ]
    
    print("\nAsking sample questions...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"QUESTION {i}: {question}")
        print('='*70)
        
        result = rag.answer_question(question, top_k=5)
        
        print(f"\nANSWER:\n{result['answer']}")
        
        print(f"\n📚 Sources Referenced ({result['num_contexts_used']}):")
        for j, source in enumerate(result['sources'][:3], 1):
            print(f"  {j}. [{source['source']}] {source['section']} (similarity: {source['similarity']})")
        
        print()
    
    print("\n" + "="*70)
    print("✅ RAG PIPELINE SETUP COMPLETE!")
    print("="*70)
    

if __name__ == "__main__":
    main()
