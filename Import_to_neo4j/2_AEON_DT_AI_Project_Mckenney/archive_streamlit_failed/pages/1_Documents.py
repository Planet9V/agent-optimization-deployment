"""
AEON Web Interface - Documents Page
Browse, search, and view documents in the knowledge graph
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web_utils.neo4j_connector import get_connector

# Page config
st.set_page_config(
    page_title="Documents - AEON",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Browser")
st.markdown("Search and explore ingested documents")
st.markdown("---")

try:
    # Get Neo4j connector
    neo4j = get_connector()

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Search & Filter")

        # Search box
        search_query = st.text_input("Search documents", placeholder="Enter search term...")

        st.markdown("### Filters")

        # Get unique sectors for filter
        stats = neo4j.get_statistics()
        sectors = [s['sector'] for s in stats.get('sector_distribution', [])]

        sector_filter = st.selectbox(
            "Sector",
            options=["All"] + sectors,
            index=0
        )

        # Pagination
        st.markdown("### Pagination")
        page_size = st.select_slider(
            "Results per page",
            options=[10, 20, 50, 100],
            value=20
        )

        if st.button("🔄 Refresh"):
            st.rerun()

    # Apply filters
    sector = None if sector_filter == "All" else sector_filter

    # Get total count
    total_count = neo4j.get_document_count(
        search=search_query,
        sector=sector
    )

    # Calculate pagination
    total_pages = max(1, (total_count + page_size - 1) // page_size)

    # Page selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_page = st.number_input(
            f"Page (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

    # Display stats
    st.markdown(f"**Found {total_count} documents** (Page {current_page} of {total_pages})")

    # Get documents
    skip = (current_page - 1) * page_size
    documents = neo4j.get_documents(
        search=search_query,
        sector=sector,
        skip=skip,
        limit=page_size
    )

    if documents:
        # Display as expandable cards
        for doc in documents:
            with st.expander(f"📄 {doc.get('title', 'Untitled Document')}"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**File:** {doc.get('file_path', 'N/A')}")
                    st.markdown(f"**Type:** {doc.get('file_type', 'N/A')}")

                    # Content preview
                    content = doc.get('content', '')
                    if content:
                        preview = content[:500] + "..." if len(content) > 500 else content
                        st.markdown("**Content Preview:**")
                        st.text(preview)

                with col2:
                    st.markdown(f"**Sector:** {doc.get('sector', 'N/A')}")
                    st.markdown(f"**Subsector:** {doc.get('subsector', 'N/A')}")
                    st.markdown(f"**Document Type:** {doc.get('document_type', 'N/A')}")
                    st.markdown(f"**Entities:** {doc.get('entity_count', 0)}")
                    st.markdown(f"**Words:** {doc.get('word_count', 0):,}")

                    processed_date = doc.get('processed_date', 'N/A')
                    if processed_date != 'N/A':
                        st.markdown(f"**Processed:** {processed_date}")

                # View entities button
                if st.button(f"View Entities", key=f"entities_{doc.get('id')}"):
                    st.session_state['selected_doc_id'] = doc.get('id')
                    st.session_state['show_entities'] = True

                # Show entities if selected
                if st.session_state.get('show_entities') and st.session_state.get('selected_doc_id') == doc.get('id'):
                    entities = neo4j.get_document_entities(doc.get('id'))

                    if entities:
                        st.markdown("### 🔍 Extracted Entities")

                        # Group by type
                        entity_df = pd.DataFrame(entities)

                        for entity_type in entity_df['label'].unique():
                            st.markdown(f"**{entity_type}:**")
                            type_entities = entity_df[entity_df['label'] == entity_type]

                            for _, ent in type_entities.iterrows():
                                st.markdown(
                                    f"- {ent['text']} "
                                    f"(confidence: {ent.get('confidence', 0):.2f}, "
                                    f"mentions: {ent.get('mention_count', 1)})"
                                )
                    else:
                        st.info("No entities extracted from this document")

                    if st.button("Hide Entities", key=f"hide_{doc.get('id')}"):
                        st.session_state['show_entities'] = False
                        st.rerun()
    else:
        st.info("No documents found matching your search criteria.")

    # Navigation buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if current_page > 1:
            if st.button("⬅️ Previous Page"):
                st.query_params = {"page": current_page - 1}
                st.rerun()

    with col3:
        if current_page < total_pages:
            if st.button("Next Page ➡️"):
                st.query_params = {"page": current_page + 1}
                st.rerun()

except Exception as e:
    st.error(f"❌ Error loading documents: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.caption("AEON Document Browser | Navigate through your knowledge graph")
