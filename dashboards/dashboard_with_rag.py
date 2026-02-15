"""
Enhanced Dashboard with RAG Q&A Integration
Interactive Q&A about strategic alignment using RAG pipeline
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
final_results_json = BASE_DIR / "data" / "final_synchronization_results.json"

# Import RAG pipeline
try:
    from src.rag_pipeline import RAGPipeline
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False


# Page configuration
st.set_page_config(
    page_title="Strategic Plan Synchronization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
st.markdown("""
    <style>
    .big-score {
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .good-score { color: #28a745; }
    .medium-score { color: #ffc107; }
    .poor-score { color: #dc3545; }
    .qa-question {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
        color: #1565c0;
    }
    .qa-answer {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #212121;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_results():
    """Load analysis results from JSON files"""
    try:
        with open(final_results_json, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Results file not found. Please run the analysis first.")
        return None


@st.cache_resource
def initialize_rag():
    """Initialize RAG pipeline (cached)"""
    if not RAG_AVAILABLE:
        return None
    
    load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    pinecone_key = os.getenv('PINECONE_API_KEY')
    
    if not openai_key or not pinecone_key:
        return None
    
    try:
        rag = RAGPipeline(
            openai_api_key=openai_key,
            pinecone_api_key=pinecone_key,
            index_name="strategic-rag"
        )
        return rag
    except Exception as e:
        st.error(f"Failed to initialize RAG: {e}")
        return None


def get_score_color(score):
    """Get color based on score"""
    if score >= 75:
        return "good-score"
    elif score >= 60:
        return "medium-score"
    else:
        return "poor-score"


def render_rag_qa_page():
    """Render RAG Q&A page"""
    st.header("🔍 Ask Questions (RAG-Powered)")
    
    if not RAG_AVAILABLE:
        st.error("RAG Pipeline not available. Install dependencies: pip install langchain")
        return
    
    # Initialize RAG
    rag = initialize_rag()
    
    if rag is None:
        st.warning("""
        ⚠️ RAG Pipeline not initialized. 
        
        To use Q&A feature:
        1. Ensure .env has OPENAI_API_KEY and PINECONE_API_KEY
        2. Run: `python test_rag_pipeline.py` to build vector store
        3. Refresh this dashboard
        """)
        return
    
    # st.info("""
    # 💡 **Ask questions about your strategic alignment analysis!**
    
    # Examples:
    # - "Why is the Digital Transformation objective scoring high/low?"
    # - "What specific actions support Risk Management?"
    # - "What KPIs are missing in the action plan?"
    # - "How can we improve alignment for objective X?"
    # """)
    
    # Initialize session state for conversation history
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    
    # Question input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            label="Ask a question",
            placeholder="e.g., Why is Risk Management objective weak?",
            key="question_input",
            label_visibility="collapsed"
        )
    
    with col2:
        ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
    
    # Suggested questions
    st.subheader("💭 Suggested Questions")
    suggestions = [
        "What are the main strengths of this strategic alignment?",
        "Which objectives need the most improvement?",
        "What specific KPIs are missing from the action plan?",
        "How does the embedding score compare to entity matching?",
        "What are the top recommendations for improving alignment?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        col_idx = i % 2
        if cols[col_idx].button(f"💡 {suggestion}", key=f"suggestion_{i}", use_container_width=True):
            question = suggestion
            ask_button = True
    
    # Process question
    if ask_button and question:
        with st.spinner("🤔 Thinking..."):
            result = rag.answer_question(question, top_k=5, include_sources=True)
            
            # Add to history
            st.session_state.qa_history.insert(0, {
                'question': question,
                'answer': result['answer'],
                'sources': result['sources']
            })
    
    # Display conversation history
    if st.session_state.qa_history:
        st.markdown("---")
        st.subheader("💬 Conversation History")
        
        for i, qa in enumerate(st.session_state.qa_history):
            with st.container():
                # Question
                st.markdown(f'<div class="qa-question"><strong>Q{len(st.session_state.qa_history) - i}:</strong> {qa["question"]}</div>', unsafe_allow_html=True)
                
                # Answer
                st.markdown(f'<div class="qa-answer"><strong>Answer:</strong><br>{qa["answer"]}</div>', unsafe_allow_html=True)
                
                # Sources
                if qa.get('sources'):
                    with st.expander("📚 View Sources"):
                        for j, source in enumerate(qa['sources'], 1):
                            st.write(f"{j}. **{source['source']}** - {source['section']} (similarity: {source['similarity']})")
                
                st.markdown("---")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.qa_history = []
            st.rerun()


# [Previous render functions remain the same - keeping them for reference]
def render_overview(results):
    """Render overview section"""
    st.header("📊 Overall Synchronization Assessment")
    
    score = results['overall_score']
    score_class = get_score_color(score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<div class="big-score {score_class}">{score:.1f}/100</div>', 
                   unsafe_allow_html=True)
        
        if score >= 90:
            st.success("**Excellent** - Strong alignment across all objectives")
        elif score >= 75:
            st.info("**Good** - Minor gaps that should be addressed")
        elif score >= 60:
            st.warning("**Moderate** - Significant improvements needed")
        else:
            st.error("**Poor** - Major misalignment requiring urgent attention")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Embedding Score",
            f"{results['embedding_score']:.1f}/100",
            help="Semantic similarity between objectives and actions"
        )
    
    with col2:
        st.metric(
            "Entity Match Score",
            f"{results['entity_score']:.1f}/100",
            help="Explicit matching of KPIs, budgets, and timelines"
        )
    
    with col3:
        strong = results['summary']['objectives_with_strong_support']
        total = results['summary']['total_objectives']
        st.metric(
            "Objectives Supported",
            f"{strong}/{total}",
            help="Strategic objectives with strong action support"
        )
    
    with col4:
        matched = results['summary']['matched_entities']
        total_ent = results['summary']['total_strategic_entities']
        match_pct = (matched / total_ent * 100) if total_ent > 0 else 0
        st.metric(
            "Entity Match Rate",
            f"{match_pct:.0f}%",
            help="Percentage of strategic entities found in action plan"
        )


def render_strengths_weaknesses(results):
    """Render strengths and weaknesses"""
    st.header("💪 Strengths & Weaknesses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Strengths")
        if results['strengths']:
            for strength in results['strengths']:
                st.success(f"• {strength}")
        else:
            st.info("No specific strengths identified")
    
    with col2:
        st.subheader("⚠️ Weaknesses")
        if results['weaknesses']:
            for weakness in results['weaknesses']:
                st.warning(f"• {weakness}")
        else:
            st.success("No significant weaknesses identified")


def render_recommendations(results):
    """Render actionable recommendations"""
    st.header("💡 Recommendations")
    
    if not results['recommendations']:
        st.success("✅ No specific recommendations - alignment is strong!")
        return
    
    for i, rec in enumerate(results['recommendations'], 1):
        priority = rec['priority']
        
        if priority == 'high':
            icon = "🔴"
        elif priority == 'medium':
            icon = "🟡"
        else:
            icon = "🟢"
        
        with st.expander(f"{icon} [{priority.upper()}] {rec.get('objective', 'General Recommendation')}"):
            if 'current_score' in rec:
                st.metric("Current Score", f"{rec['current_score']:.1f}/100")
            
            st.write("**Recommended Actions:**")
            for action in rec.get('actions', []):
                st.write(f"• {action}")
            
            if rec.get('expected_impact'):
                st.info(f"**Expected Impact:** {rec['expected_impact']}")


def main():
    """Main dashboard function"""
    
    # Header
    st.title("🎯 Strategic Plan Synchronization Dashboard")
    st.markdown("**Strategic Planning AI Assessment**")
    
    # Load results
    results = load_results()
    
    if results is None:
        st.stop()
    
    # Sidebar
    st.sidebar.header("Assessment Details")
    st.sidebar.write(f"**Date:** {results.get('assessment_date', 'N/A')}")
    st.sidebar.write(f"**Strategic Plan:** {results.get('strategic_plan', 'N/A')}")
    st.sidebar.write(f"**Action Plan:** {results.get('action_plan', 'N/A')}")
    
    # Navigation with RAG Q&A
    st.sidebar.header("Navigation")
    pages = [
        "📊 Overview",
        "💪 Strengths & Weaknesses",
        "💡 Recommendations",
        "🔍 Ask Questions (RAG)"  # New page
    ]
    
    page = st.sidebar.radio("Select View", pages)
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "This dashboard provides comprehensive analysis with AI-powered Q&A capabilities."
    )
    
    # Render selected page
    if page == "📊 Overview":
        render_overview(results)
    elif page == "💪 Strengths & Weaknesses":
        render_strengths_weaknesses(results)
    elif page == "💡 Recommendations":
        render_recommendations(results)
    elif page == "🔍 Ask Questions (RAG)":
        render_rag_qa_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Strategic Planning AI System | Powered by OpenAI, Pinecone & Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
