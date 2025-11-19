"""
AEON Web Interface - System Control Page
Manage orchestrator, configuration, and system settings
"""

import streamlit as st
import sys
from pathlib import Path
import yaml
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web_utils.neo4j_connector import get_connector, test_connection
from web_utils.orchestrator_control import get_controller

# Page config
st.set_page_config(
    page_title="System Control - AEON",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ System Control & Configuration")
st.markdown("Manage AEON document ingestion system")
st.markdown("---")

try:
    # Get controllers
    neo4j = get_connector()
    controller = get_controller()

    # Orchestrator Control
    st.header("🎛️ Orchestrator Control")

    status = controller.get_status()
    is_running = status.get("running", False)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Current Status")

        if is_running:
            st.success("✅ **Status:** Running")
            st.metric("Workers Active", status.get("workers_active", 0))
            st.metric("Queue Size", status.get("queue_size", 0))

            if status.get("started_at"):
                st.markdown(f"**Started:** {status['started_at']}")
        else:
            st.warning("⚠️ **Status:** Stopped")
            st.info("Click 'Start Monitoring' to begin document ingestion")

    with col2:
        st.markdown("### Control Actions")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button(
                "🚀 Start Monitoring",
                disabled=is_running,
                use_container_width=True,
                type="primary"
            ):
                with st.spinner("Starting orchestrator..."):
                    result = controller.start(mode="watch")

                    if result["status"] == "started":
                        st.success("✅ Orchestrator started successfully!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to start: {result.get('message')}")

        with col_b:
            if st.button(
                "⏸️ Stop Monitoring",
                disabled=not is_running,
                use_container_width=True,
                type="secondary"
            ):
                with st.spinner("Stopping orchestrator..."):
                    result = controller.stop()

                    if result["status"] == "stopped":
                        st.success("✅ Orchestrator stopped successfully!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to stop: {result.get('message')}")

        # Processing statistics
        if is_running:
            st.markdown("### Processing Statistics")
            stats = controller.get_statistics()

            col_x, col_y, col_z = st.columns(3)

            with col_x:
                st.metric("Discovered", stats.get("files_discovered", 0))
                st.metric("Converted", stats.get("files_converted", 0))

            with col_y:
                st.metric("Classified", stats.get("files_classified", 0))
                st.metric("NER Processed", stats.get("files_ner_processed", 0))

            with col_z:
                st.metric("Ingested", stats.get("files_ingested", 0))

                # Calculate success rate
                if stats.get("files_discovered", 0) > 0:
                    success_rate = (stats.get("files_ingested", 0) / stats["files_discovered"]) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")

    # Configuration
    st.header("⚙️ System Configuration")

    config_summary = controller.get_config_summary()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Monitoring",
        "Neo4j",
        "NLP/NER",
        "Classification"
    ])

    with tab1:
        st.markdown("### Watch Directories")

        watch_dirs = config_summary.get("watch_directories", [])

        if watch_dirs:
            for directory in watch_dirs:
                st.markdown(f"📁 `{directory}`")
        else:
            st.info("No watch directories configured")

        st.markdown("### Processing Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Batch Size", config_summary.get("batch_size", 5))

        with col2:
            st.metric("Parallel Workers", config_summary.get("parallel_workers", 3))

    with tab2:
        st.markdown("### Neo4j Connection")

        st.markdown(f"**URI:** `{config_summary.get('neo4j_uri', 'N/A')}`")
        st.markdown(f"**Batch Size:** {config_summary.get('neo4j_batch_size', 100)}")

        if st.button("🔌 Test Connection"):
            with st.spinner("Testing Neo4j connection..."):
                if neo4j.test_connection():
                    st.success("✅ Neo4j connection successful!")
                else:
                    st.error("❌ Neo4j connection failed!")

    with tab3:
        st.markdown("### NLP Configuration")

        st.markdown(f"**spaCy Model:** `{config_summary.get('spacy_model', 'N/A')}`")

        st.markdown("### Entity Types")
        st.info("Supported entity types: VENDOR, PROTOCOL, STANDARD, COMPONENT, MEASUREMENT, ORGANIZATION, SAFETY_CLASS, SYSTEM_LAYER")

    with tab4:
        st.markdown("### Classification Settings")

        threshold = config_summary.get("classification_threshold", 0.75)
        st.markdown(f"**Confidence Threshold:** {threshold}")
        st.progress(threshold)

        st.markdown("### Classifiers")
        st.markdown("- **Sector Classifier:** Random Forest + TF-IDF")
        st.markdown("- **Subsector Classifier:** Random Forest + TF-IDF")
        st.markdown("- **Document Type Classifier:** Random Forest + TF-IDF")

    # Database Status
    st.header("💾 Database Status")

    db_stats = neo4j.get_statistics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Documents",
            f"{db_stats.get('total_documents', 0):,}"
        )

    with col2:
        st.metric(
            "Total Entities",
            f"{db_stats.get('total_entities', 0):,}"
        )

    with col3:
        st.metric(
            "Relationships",
            f"{db_stats.get('total_relationships', 0):,}"
        )

    with col4:
        # Calculate graph density
        docs = db_stats.get('total_documents', 0)
        ents = db_stats.get('total_entities', 0)
        rels = db_stats.get('total_relationships', 0)

        if docs > 0 and ents > 0:
            density = rels / (docs * ents) * 100
            st.metric("Graph Density", f"{density:.2f}%")
        else:
            st.metric("Graph Density", "N/A")

    # System Health
    st.header("🏥 System Health")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Connection Tests")

        # Neo4j test
        if neo4j.test_connection():
            st.success("✅ Neo4j: Connected")
        else:
            st.error("❌ Neo4j: Disconnected")

        # Orchestrator test
        if controller.is_running():
            st.success("✅ Orchestrator: Running")
        else:
            st.info("ℹ️ Orchestrator: Stopped (Normal)")

    with col2:
        st.markdown("### Error Log")

        if is_running:
            errors = controller.get_statistics().get("errors", [])

            if errors:
                st.error(f"Found {len(errors)} errors")

                with st.expander("View Errors"):
                    for idx, error in enumerate(errors[-10:], 1):  # Last 10 errors
                        st.text(f"{idx}. {error}")
            else:
                st.success("No errors recorded")
        else:
            st.info("Start orchestrator to monitor errors")

    # Advanced Actions
    st.header("🔧 Advanced Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/3_Analytics.py")

    with col3:
        if st.button("📄 View Documents", use_container_width=True):
            st.switch_page("pages/1_Documents.py")

    # Documentation
    st.header("📚 Documentation")

    with st.expander("Quick Start Guide"):
        st.markdown("""
        ### Getting Started with AEON

        1. **Start Monitoring**: Click 'Start Monitoring' to begin watching configured directories
        2. **Upload Documents**: Place PDF, DOCX, HTML, MD, or TXT files in watch directories
        3. **View Progress**: Monitor real-time processing on the Dashboard
        4. **Browse Results**: Navigate to Documents or Entities to explore ingested data
        5. **Analyze Insights**: Use Analytics page for comprehensive statistics

        ### Processing Pipeline

        1. **Discovery**: Files detected in watch directories
        2. **Conversion**: Multi-format files converted to markdown
        3. **Classification**: ML-based sector/subsector/type classification
        4. **NER**: Entity extraction using hybrid pattern+neural approach
        5. **Ingestion**: Storage in Neo4j knowledge graph

        ### Tips

        - Use the search features to quickly find specific documents or entities
        - Monitor queue size to track processing backlog
        - Check error logs regularly for any issues
        - Export analytics data for reporting
        """)

except Exception as e:
    st.error(f"❌ Error loading system control: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.caption("AEON System Control | Manage your document ingestion pipeline")
