"""
AEON Web Interface - Analytics Page
Comprehensive statistics and visualizations
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web_utils.neo4j_connector import get_connector
from web_utils.orchestrator_control import get_controller
from web_utils.visualizations import (
    create_sector_pie_chart,
    create_entity_type_bar_chart,
    create_processing_stats_chart,
    format_number
)

# Page config
st.set_page_config(
    page_title="Analytics - AEON",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AEON Analytics Dashboard")
st.markdown("Comprehensive insights into your document knowledge graph")
st.markdown("---")

try:
    # Get connectors
    neo4j = get_connector()
    controller = get_controller()

    # Overview Metrics
    st.header("📈 System Overview")

    db_stats = neo4j.get_statistics()
    proc_stats = controller.get_statistics()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Documents",
            value=format_number(db_stats.get("total_documents", 0))
        )

    with col2:
        st.metric(
            label="Total Entities",
            value=format_number(db_stats.get("total_entities", 0))
        )

    with col3:
        st.metric(
            label="Relationships",
            value=format_number(db_stats.get("total_relationships", 0))
        )

    with col4:
        avg_entities = 0
        if db_stats.get("total_documents", 0) > 0:
            avg_entities = db_stats["total_entities"] / db_stats["total_documents"]
        st.metric(
            label="Avg Entities/Doc",
            value=f"{avg_entities:.1f}"
        )

    with col5:
        st.metric(
            label="Files in Queue",
            value=proc_stats.get("queue_size", 0)
        )

    # Processing Pipeline
    st.header("⚙️ Processing Pipeline")

    if proc_stats.get("files_discovered", 0) > 0:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.plotly_chart(
                create_processing_stats_chart(proc_stats),
                use_container_width=True
            )

        with col2:
            st.markdown("### Pipeline Metrics")

            discovered = proc_stats.get("files_discovered", 0)
            ingested = proc_stats.get("files_ingested", 0)

            if discovered > 0:
                completion_rate = (ingested / discovered) * 100
                st.metric(
                    label="Completion Rate",
                    value=f"{completion_rate:.1f}%"
                )

            st.metric(
                label="Discovered",
                value=discovered
            )
            st.metric(
                label="Converted",
                value=proc_stats.get("files_converted", 0)
            )
            st.metric(
                label="Classified",
                value=proc_stats.get("files_classified", 0)
            )
            st.metric(
                label="NER Processed",
                value=proc_stats.get("files_ner_processed", 0)
            )
            st.metric(
                label="Ingested",
                value=ingested
            )
    else:
        st.info("No processing activity yet. Start monitoring to see pipeline statistics.")

    # Distribution Charts
    st.header("📊 Data Distribution")

    col1, col2 = st.columns(2)

    with col1:
        # Sector distribution
        sector_data = db_stats.get("sector_distribution", [])
        if sector_data:
            st.plotly_chart(
                create_sector_pie_chart(sector_data),
                use_container_width=True
            )
        else:
            st.info("No sector data available yet")

    with col2:
        # Entity type distribution
        entity_data = db_stats.get("entity_type_distribution", [])
        if entity_data:
            st.plotly_chart(
                create_entity_type_bar_chart(entity_data),
                use_container_width=True
            )
        else:
            st.info("No entity data available yet")

    # Detailed Breakdowns
    st.header("🔍 Detailed Breakdown")

    tab1, tab2, tab3 = st.tabs(["Sectors", "Entity Types", "Document Types"])

    with tab1:
        sector_data = db_stats.get("sector_distribution", [])
        if sector_data:
            df = pd.DataFrame(sector_data)
            df = df.sort_values('count', ascending=False)

            # Add percentage
            total = df['count'].sum()
            df['percentage'] = (df['count'] / total * 100).round(1)

            st.dataframe(
                df.rename(columns={
                    'sector': 'Sector',
                    'count': 'Documents',
                    'percentage': 'Percentage (%)'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No sector data available")

    with tab2:
        entity_data = db_stats.get("entity_type_distribution", [])
        if entity_data:
            df = pd.DataFrame(entity_data)

            # Handle both 'type' and 'label' column names
            label_col = 'type' if 'type' in df.columns else 'label'

            df = df.sort_values('count', ascending=False)

            # Add percentage
            total = df['count'].sum()
            df['percentage'] = (df['count'] / total * 100).round(1)

            st.dataframe(
                df.rename(columns={
                    label_col: 'Entity Type',
                    'count': 'Count',
                    'percentage': 'Percentage (%)'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No entity data available")

    with tab3:
        # Get document type distribution via custom query
        st.info("Document type analytics coming soon")

    # Top Entities
    st.header("🌟 Top Entities")

    top_entities = neo4j.get_entities(limit=20)

    if top_entities:
        df = pd.DataFrame(top_entities)
        df = df.sort_values('document_count', ascending=False)

        # Create bar chart
        fig = px.bar(
            df,
            x='document_count',
            y='text',
            orientation='h',
            title='Top 20 Entities by Document Count',
            labels={'document_count': 'Document Count', 'text': 'Entity'},
            color='document_count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            showlegend=False,
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No entity data available yet")

    # Export Options
    st.header("📤 Export Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Export Sector Data"):
            sector_data = db_stats.get("sector_distribution", [])
            if sector_data:
                df = pd.DataFrame(sector_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="sector_distribution.csv",
                    mime="text/csv"
                )

    with col2:
        if st.button("Export Entity Data"):
            entity_data = db_stats.get("entity_type_distribution", [])
            if entity_data:
                df = pd.DataFrame(entity_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="entity_distribution.csv",
                    mime="text/csv"
                )

    with col3:
        if st.button("Export All Statistics"):
            import json
            stats_json = json.dumps({
                "database": db_stats,
                "processing": proc_stats,
                "timestamp": pd.Timestamp.now().isoformat()
            }, indent=2, default=str)

            st.download_button(
                label="Download JSON",
                data=stats_json,
                file_name="aeon_statistics.json",
                mime="application/json"
            )

except Exception as e:
    st.error(f"❌ Error loading analytics: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.caption("AEON Analytics Dashboard | Comprehensive insights into your knowledge graph")
