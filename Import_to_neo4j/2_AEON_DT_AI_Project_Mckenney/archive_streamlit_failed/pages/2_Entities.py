"""
AEON Web Interface - Entities Page
Explore extracted entities and their relationships
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web_utils.neo4j_connector import get_connector
from web_utils.visualizations import create_entity_network_graph

# Page config
st.set_page_config(
    page_title="Entities - AEON",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Entity Explorer")
st.markdown("Browse and analyze extracted entities")
st.markdown("---")

try:
    # Get Neo4j connector
    neo4j = get_connector()

    # Sidebar
    with st.sidebar:
        st.header("🔍 Entity Search")

        # Search box
        search_query = st.text_input("Search entities", placeholder="Enter entity name...")

        st.markdown("### Filters")

        # Get entity types
        entity_types = neo4j.get_entity_types()
        type_names = ["All"] + [et['label'] for et in entity_types]

        type_filter = st.selectbox(
            "Entity Type",
            options=type_names,
            index=0
        )

        # Pagination
        st.markdown("### Display")
        page_size = st.select_slider(
            "Results to show",
            options=[25, 50, 100, 200],
            value=50
        )

        if st.button("🔄 Refresh"):
            st.rerun()

    # Entity Type Distribution
    st.header("📊 Entity Type Distribution")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Counts by Type")

        for et in entity_types[:10]:  # Top 10
            st.metric(
                label=et['label'],
                value=f"{et['count']:,}",
                delta=None
            )

    with col2:
        # Network visualization
        st.markdown("### Entity Network (Top Entities)")

        # Get top entities
        top_entities = neo4j.get_entities(limit=30)

        if top_entities:
            fig = create_entity_network_graph(top_entities, max_nodes=30)
            st.plotly_chart(fig, use_container_width=True)

    # Entity Browser
    st.header("🔍 Entity Browser")

    # Apply filters
    entity_label = None if type_filter == "All" else type_filter

    # Get entities
    entities = neo4j.get_entities(
        search=search_query,
        label=entity_label,
        limit=page_size
    )

    if entities:
        st.markdown(f"**Showing {len(entities)} entities**")

        # Create DataFrame for display
        df = pd.DataFrame(entities)

        # Sort by document count
        df = df.sort_values('document_count', ascending=False)

        # Display table with selection
        st.markdown("### Entity List")

        # Interactive table
        for idx, entity in df.iterrows():
            with st.expander(
                f"**{entity['text']}** ({entity['label']}) - "
                f"{entity['document_count']} documents"
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Entity Text:** {entity['text']}")
                    st.markdown(f"**Type:** {entity['label']}")
                    st.markdown(f"**Confidence:** {entity.get('confidence', 'N/A')}")

                with col2:
                    st.metric(
                        label="Found in Documents",
                        value=entity['document_count']
                    )

                # Show documents containing this entity
                if st.button(f"Show Documents", key=f"docs_{idx}"):
                    st.session_state[f'show_docs_{idx}'] = True

                if st.session_state.get(f'show_docs_{idx}', False):
                    docs = neo4j.get_entity_documents(
                        entity['text'],
                        entity['label']
                    )

                    if docs:
                        st.markdown("#### Documents containing this entity:")

                        docs_df = pd.DataFrame(docs)

                        # Format date
                        if 'processed_date' in docs_df.columns:
                            docs_df['processed_date'] = pd.to_datetime(
                                docs_df['processed_date']
                            ).dt.strftime('%Y-%m-%d %H:%M')

                        st.dataframe(
                            docs_df,
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No documents found")

                    if st.button(f"Hide Documents", key=f"hide_{idx}"):
                        st.session_state[f'show_docs_{idx}'] = False
                        st.rerun()
    else:
        st.info("No entities found matching your search criteria.")

    # Search across all
    st.header("🔎 Global Search")

    global_search = st.text_input(
        "Search across documents and entities",
        placeholder="Enter search term..."
    )

    if global_search:
        with st.spinner("Searching..."):
            results = neo4j.search_all(global_search, limit=20)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📄 Documents")
                docs = results.get('documents', [])
                if docs:
                    for doc in docs:
                        st.markdown(f"- **{doc['title']}** ({doc.get('sector', 'N/A')})")
                else:
                    st.info("No documents found")

            with col2:
                st.markdown("### 🔍 Entities")
                ents = results.get('entities', [])
                if ents:
                    for ent in ents:
                        st.markdown(
                            f"- **{ent['text']}** ({ent['label']}) - "
                            f"{ent.get('doc_count', 0)} docs"
                        )
                else:
                    st.info("No entities found")

except Exception as e:
    st.error(f"❌ Error loading entities: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.caption("AEON Entity Explorer | Discover relationships in your knowledge graph")
