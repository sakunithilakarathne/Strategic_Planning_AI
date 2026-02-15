"""
Interactive Dashboard for Strategic Plan Synchronization
Displays analysis results with visualizations and insights
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
final_results_json = BASE_DIR / "data" / "final_synchronization_results.json"

# Page configuration
st.set_page_config(
    page_title="Strategic Plan Synchronization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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


def get_score_color(score):
    """Get color based on score"""
    if score >= 75:
        return "good-score"
    elif score >= 60:
        return "medium-score"
    else:
        return "poor-score"


def render_overview(results):
    """Render overview section"""
    st.header("📊 Overall Synchronization Assessment")
    
    # Overall score
    score = results['overall_score']
    score_class = get_score_color(score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<div class="big-score {score_class}">{score:.1f}/100</div>', 
                   unsafe_allow_html=True)
        
        # Interpretation
        if score >= 90:
            st.success("**Excellent** - Strong alignment across all objectives")
        elif score >= 75:
            st.info("**Good** - Minor gaps that should be addressed")
        elif score >= 60:
            st.warning("**Moderate** - Significant improvements needed")
        else:
            st.error("**Poor** - Major misalignment requiring urgent attention")
    
    st.markdown("---")
    
    # Component scores
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Embedding Score",
            f"{results['embedding_score']:.1f}/100",
            help="Semantic similarity between strategic objectives and actions"
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


def render_component_scores(results):
    """Render component scores breakdown"""
    st.header("📈 Score Breakdown")
    
    # Create gauge charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_embedding = go.Figure(go.Indicator(
            mode="gauge+number",
            value=results['embedding_score'],
            title={'text': "Embedding Analysis"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_embedding.update_layout(height=300)
        st.plotly_chart(fig_embedding, use_container_width=True)
    
    with col2:
        fig_entity = go.Figure(go.Indicator(
            mode="gauge+number",
            value=results['entity_score'],
            title={'text': "Entity Matching"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_entity.update_layout(height=300)
        st.plotly_chart(fig_entity, use_container_width=True)


def render_objective_analysis(results):
    """Render per-objective analysis"""
    st.header("🎯 Strategic Objective Analysis")
    
    objectives = results['objective_synchronizations']
    
    # Create DataFrame
    df = pd.DataFrame([
        {
            'Objective': obj['objective_title'][:50] + '...' if len(obj['objective_title']) > 50 else obj['objective_title'],
            'Combined Score': obj['combined_score'],
            'Embedding': obj['embedding_score'],
            'Entity Matches': obj['entity_matches'],
            'Status': '✅ Strong' if obj['has_strong_support'] else '⚠️ Weak'
        }
        for obj in objectives
    ])
    
    # Sort by combined score
    df = df.sort_values('Combined Score', ascending=False)
    
    # Bar chart
    fig = px.bar(
        df,
        x='Combined Score',
        y='Objective',
        orientation='h',
        color='Combined Score',
        color_continuous_scale=['red', 'yellow', 'green'],
        range_color=[0, 100],
        title='Objective Synchronization Scores'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Detailed Breakdown")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Expandable details for each objective
    st.subheader("Objective Details")
    for obj in objectives:
        with st.expander(f"{obj['objective_title']} - Score: {obj['combined_score']:.1f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Embedding Score", f"{obj['embedding_score']:.1f}/100")
                st.metric("Entity Matches", obj['entity_matches'])
            
            with col2:
                st.metric("Combined Score", f"{obj['combined_score']:.1f}/100")
                status = "✅ Strong Support" if obj['has_strong_support'] else "⚠️ Weak Support"
                st.write(f"**Status:** {status}")
            
            # Top matching actions
            if obj['top_matching_actions']:
                st.write("**Top Matching Actions:**")
                for action in obj['top_matching_actions']:
                    st.write(f"{action['rank']}. {action['action_title']} ({action['similarity_score']:.2f})")
            
            # Gaps
            if obj['gaps']:
                st.write("**Identified Gaps:**")
                for gap in obj['gaps']:
                    st.warning(gap)


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
        st.success("No specific recommendations - alignment is strong!")
        return
    
    for i, rec in enumerate(results['recommendations'], 1):
        priority = rec['priority']
        
        if priority == 'high':
            icon = "🔴"
            color = "error"
        elif priority == 'medium':
            icon = "🟡"
            color = "warning"
        else:
            icon = "🟢"
            color = "info"
        
        with st.expander(f"{icon} [{priority.upper()}] {rec.get('objective', 'General Recommendation')}"):
            if 'current_score' in rec:
                st.metric("Current Score", f"{rec['current_score']:.1f}/100")
            
            st.write("**Recommended Actions:**")
            for action in rec.get('actions', []):
                st.write(f"• {action}")


def render_entity_heatmap(results):
    """Render entity matching heatmap"""
    st.header("🏷️ Entity Matching Analysis")
    
    # Create summary data
    summary = results['summary']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for entity matching
        fig = go.Figure(data=[go.Pie(
            labels=['Matched', 'Unmatched'],
            values=[summary['matched_entities'], summary['unmatched_entities']],
            hole=.4,
            marker_colors=['#28a745', '#dc3545']
        )])
        fig.update_layout(
            title="Entity Match Coverage",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Support status pie chart
        fig2 = go.Figure(data=[go.Pie(
            labels=['Strong Support', 'Weak Support'],
            values=[
                summary['objectives_with_strong_support'],
                summary['objectives_with_weak_support']
            ],
            hole=.4,
            marker_colors=['#28a745', '#ffc107']
        )])
        fig2.update_layout(
            title="Objective Support Status",
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)


def render_export_section(results):
    """Render data export section"""
    st.header("📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as JSON
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="Download Full Results (JSON)",
            data=json_str,
            file_name="synchronization_results.json",
            mime="application/json"
        )
    
    with col2:
        # Export summary as CSV
        objectives = results['objective_synchronizations']
        df = pd.DataFrame([
            {
                'Objective': obj['objective_title'],
                'Combined Score': obj['combined_score'],
                'Embedding Score': obj['embedding_score'],
                'Entity Matches': obj['entity_matches'],
                'Strong Support': obj['has_strong_support']
            }
            for obj in objectives
        ])
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Objective Summary (CSV)",
            data=csv,
            file_name="objective_summary.csv",
            mime="text/csv"
        )


def main():
    """Main dashboard function"""
    
    # Header
    st.title("🎯 Strategic Plan Synchronization Dashboard")
    st.markdown(f"**Strategic Planning AI Assessment**")
    
    # Load results
    results = load_results()
    
    if results is None:
        st.stop()
    
    # Display metadata
    st.sidebar.header("Assessment Details")
    st.sidebar.write(f"**Date:** {results.get('assessment_date', 'N/A')}")
    st.sidebar.write(f"**Strategic Plan:** {results.get('strategic_plan', 'N/A')}")
    st.sidebar.write(f"**Action Plan:** {results.get('action_plan', 'N/A')}")
    
    # Navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select View",
        [
            "📊 Overview",
            "📈 Score Breakdown",
            "🎯 Objective Analysis",
            "💪 Strengths & Weaknesses",
            "💡 Recommendations",
            "🏷️ Entity Analysis",
            "📥 Export"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "This dashboard provides comprehensive analysis of strategic plan "
        "and action plan synchronization using AI-powered semantic analysis "
        "and entity matching."
    )
    
    # Render selected page
    if page == "📊 Overview":
        render_overview(results)
    elif page == "📈 Score Breakdown":
        render_component_scores(results)
    elif page == "🎯 Objective Analysis":
        render_objective_analysis(results)
    elif page == "💪 Strengths & Weaknesses":
        render_strengths_weaknesses(results)
    elif page == "💡 Recommendations":
        render_recommendations(results)
    elif page == "🏷️ Entity Analysis":
        render_entity_heatmap(results)
    elif page == "📥 Export":
        render_export_section(results)
    
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
