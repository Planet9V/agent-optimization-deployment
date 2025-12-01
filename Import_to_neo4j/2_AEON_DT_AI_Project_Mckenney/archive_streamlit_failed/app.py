"""
AEON Document Ingestion System - Web Interface
Main Dashboard Application (Streamlit)

This is the main entry point for the AEON web interface.
Run with: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime

# Setup paths - add parent project for agents and parent utils
parent_project_dir = Path(__file__).parent.parent
if str(parent_project_dir) not in sys.path:
    sys.path.insert(0, str(parent_project_dir))

# Import from web_utils (renamed to avoid conflict with parent utils)
from web_utils.neo4j_connector import get_connector
from web_utils.orchestrator_control import get_controller
from web_utils.visualizations import (
    create_processing_stats_chart,
    create_sector_pie_chart,
    create_entity_type_bar_chart,
    format_number
)

# Page configuration
st.set_page_config(
    page_title="AEON Document Ingestion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tailwind v4 CDN Integration (Nov 2025)
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<style type="text/tailwindcss">
    @theme {
        --color-primary: #1f77b4;
        --color-primary-dark: #1557a0;
        --color-success: #28a745;
        --color-warning: #ffc107;
        --color-danger: #dc3545;
        --color-info: #17a2b8;
    }

    .main-header {
        @apply text-4xl font-bold text-blue-600 mb-4;
    }
    .metric-card {
        @apply bg-gray-100 p-4 rounded-lg border-l-4 border-blue-500 shadow-sm;
    }
    .success-box {
        @apply bg-green-50 border border-green-200 rounded-lg p-3 my-2;
    }
    .warning-box {
        @apply bg-yellow-50 border border-yellow-200 rounded-lg p-3 my-2;
    }
    .error-box {
        @apply bg-red-50 border border-red-200 rounded-lg p-3 my-2;
    }
    .hover-lift {
        @apply transition-all duration-200;
    }
    .hover-lift:hover {
        @apply transform -translate-y-1 shadow-lg;
    }
    .animate-fadeIn {
        animation: fadeIn 0.3s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# Header
st.markdown('<div class="main-header">📚 AEON Document Ingestion System</div>', unsafe_allow_html=True)
st.markdown("**Automated Document Processing with NLP Entity Extraction**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=AEON", use_container_width=True)
    st.title("Navigation")

    st.markdown("### Quick Links")
    st.page_link("app.py", label="🏠 Dashboard", icon="🏠")
    st.page_link("pages/1_Documents.py", label="📄 Documents", icon="📄")
    st.page_link("pages/2_Entities.py", label="🔍 Entities", icon="🔍")
    st.page_link("pages/3_Analytics.py", label="📊 Analytics", icon="📊")
    st.page_link("pages/4_System.py", label="⚙️ System Control", icon="⚙️")
    st.page_link("pages/5_AI_Assistant.py", label="🤖 AI Assistant", icon="🤖")
    st.page_link("pages/6_Diagnostics.py", label="🔬 Diagnostics", icon="🔬")

    st.markdown("---")

    # Auto-refresh toggle
    st.session_state.auto_refresh = st.checkbox(
        "Auto-refresh (10s)",
        value=st.session_state.auto_refresh
    )

    if st.button("🔄 Refresh Now"):
        st.rerun()

    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main content
try:
    # Get Neo4j connector
    neo4j = get_connector()

    # Test connection
    if not neo4j.test_connection():
        st.error("❌ Unable to connect to Neo4j database. Please check your connection settings.")
        st.stop()

    # Get orchestrator controller
    controller = get_controller()

    # System Status Section
    st.header("🎛️ System Status")

    status = controller.get_status()
    is_running = status.get("running", False)

    col1, col2, col3 = st.columns(3)

    with col1:
        if is_running:
            st.markdown('<div class="success-box"><strong>✅ Status:</strong> Running</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box"><strong>⚠️ Status:</strong> Stopped</div>', unsafe_allow_html=True)

    with col2:
        if is_running:
            workers = status.get("workers_active", 0)
            st.markdown(f'<div class="metric-card"><strong>👷 Active Workers:</strong> {workers}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-card"><strong>👷 Active Workers:</strong> 0</div>', unsafe_allow_html=True)

    with col3:
        queue_size = status.get("queue_size", 0)
        if queue_size > 0:
            st.markdown(f'<div class="warning-box"><strong>📋 Queue:</strong> {queue_size} files</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-card"><strong>📋 Queue:</strong> Empty</div>', unsafe_allow_html=True)

    # Processing Statistics
    st.header("📊 Processing Statistics")

    stats = controller.get_statistics()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Discovered",
            value=format_number(stats.get("files_discovered", 0)),
            delta=None
        )

    with col2:
        st.metric(
            label="Converted",
            value=format_number(stats.get("files_converted", 0)),
            delta=None
        )

    with col3:
        st.metric(
            label="Classified",
            value=format_number(stats.get("files_classified", 0)),
            delta=None
        )

    with col4:
        st.metric(
            label="NER Processed",
            value=format_number(stats.get("files_ner_processed", 0)),
            delta=None
        )

    with col5:
        st.metric(
            label="Ingested",
            value=format_number(stats.get("files_ingested", 0)),
            delta=None
        )

    # Processing pipeline chart
    if stats.get("files_discovered", 0) > 0:
        st.plotly_chart(
            create_processing_stats_chart(stats),
            use_container_width=True
        )

    # Database Statistics
    st.header("💾 Database Statistics")

    db_stats = neo4j.get_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Documents",
            value=format_number(db_stats.get("total_documents", 0)),
            delta=None
        )

    with col2:
        st.metric(
            label="Total Entities",
            value=format_number(db_stats.get("total_entities", 0)),
            delta=None
        )

    with col3:
        st.metric(
            label="Total Relationships",
            value=format_number(db_stats.get("total_relationships", 0)),
            delta=None
        )

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Sector distribution
        sector_data = db_stats.get("sector_distribution", [])
        if sector_data:
            st.plotly_chart(
                create_sector_pie_chart(sector_data),
                use_container_width=True
            )

    with col2:
        # Entity type distribution
        entity_data = db_stats.get("entity_type_distribution", [])
        if entity_data:
            st.plotly_chart(
                create_entity_type_bar_chart(entity_data),
                use_container_width=True
            )

    # Recent Documents
    st.header("📄 Recent Documents")

    recent_docs = neo4j.get_recent_documents(limit=10)

    if recent_docs:
        # Create DataFrame
        import pandas as pd
        df = pd.DataFrame(recent_docs)

        # Format datetime
        if 'processed_date' in df.columns:
            df['processed_date'] = pd.to_datetime(df['processed_date']).dt.strftime('%Y-%m-%d %H:%M')

        # Display table
        st.dataframe(
            df[['title', 'sector', 'doc_type', 'entity_count', 'processed_date']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No documents in database yet. Start monitoring to begin ingestion!")

    # Errors Section
    if is_running:
        errors = stats.get("errors", [])
        if errors:
            st.header("⚠️ Recent Errors")
            for error in errors[-5:]:  # Show last 5 errors
                st.error(f"**Error:** {error}")

    # Quick Actions
    st.header("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Start Monitoring", disabled=is_running, use_container_width=True):
            result = controller.start(mode="watch")
            if result["status"] == "started":
                st.success("✅ Monitoring started successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Failed to start: {result.get('message', 'Unknown error')}")

    with col2:
        if st.button("⏸️ Stop Monitoring", disabled=not is_running, use_container_width=True):
            result = controller.stop()
            if result["status"] == "stopped":
                st.success("✅ Monitoring stopped successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Failed to stop: {result.get('message', 'Unknown error')}")

    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")

    # Auto-refresh
    if st.session_state.auto_refresh and is_running:
        time.sleep(10)
        st.rerun()

except Exception as e:
    st.error(f"❌ Application Error: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.caption("AEON Document Ingestion System v1.0 | Powered by Neo4j, spaCy, and Streamlit")
