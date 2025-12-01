"""
AEON Web Interface - AI Assistant Page
Natural language interface for document queries and ingestion guidance
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web_utils.ai_assistant import get_assistant

# Page config
st.set_page_config(
    page_title="AI Assistant - AEON",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AEON AI Assistant")
st.markdown("Ask me anything about your documents, entities, or the ingestion process!")
st.markdown("---")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(datetime.now().timestamp())}"

# Get AI assistant instance
try:
    assistant = get_assistant()
    assistant_available = True
except Exception as e:
    assistant_available = False
    st.error(f"❌ AI Assistant not available: {str(e)}")
    st.info("💡 Make sure to set your OPENROUTER_API_KEY in the .env file")

# Sidebar with assistant info and settings
with st.sidebar:
    st.header("🤖 Assistant Settings")

    if assistant_available:
        st.success("✅ AI Assistant Ready")
        st.markdown(f"**Model**: `{assistant.model.split('/')[-1]}`")

        # Show system stats
        try:
            stats = assistant.get_system_stats()
            st.metric("Documents", f"{stats.get('total_documents', 0):,}")
            st.metric("Entities", f"{stats.get('total_entities', 0):,}")
        except Exception:
            pass

    st.markdown("---")
    st.markdown("### 💬 What can I help with?")
    st.markdown("""
    - **Document Search**: "Find all Siemens PLC documents"
    - **Entity Queries**: "What vendors are mentioned?"
    - **Classification Help**: "How do I classify a document?"
    - **System Info**: "How many documents are indexed?"
    - **Ingestion Guidance**: "How do I add new documents?"
    """)

    st.markdown("---")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
if assistant_available:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show metadata if available
            if message["role"] == "assistant" and "metadata" in message:
                with st.expander("ℹ️ Response Details"):
                    metadata = message["metadata"]
                    st.markdown(f"**Context Used**: {metadata.get('context_used', 0)} documents")
                    st.markdown(f"**Model**: {metadata.get('model', 'Unknown')}")

    # Chat input
    if prompt := st.chat_input("Ask me anything about AEON documents and entities..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = assistant.chat(prompt, session_id=st.session_state.session_id)

                    if response["success"]:
                        st.markdown(response["response"])

                        # Store assistant response
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["response"],
                            "metadata": {
                                "context_used": response.get("context_used", 0),
                                "model": response.get("model", "")
                            }
                        })
                    else:
                        error_msg = f"❌ Error: {response.get('error', 'Unknown error')}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
                except Exception as e:
                    error_msg = f"❌ Unexpected error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

    # Quick action buttons
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Show System Stats"):
            prompt = "Show me the current system statistics"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    with col2:
        if st.button("🔍 Search Documents"):
            prompt = "How can I search for specific documents?"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    with col3:
        if st.button("📤 Ingestion Help"):
            prompt = "How do I ingest new documents?"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

else:
    # Assistant not available - show setup instructions
    st.warning("🔧 AI Assistant Setup Required")

    with st.expander("📖 Setup Instructions", expanded=True):
        st.markdown("""
        ### Step 1: Get OpenRouter API Key

        1. Visit [OpenRouter.ai](https://openrouter.ai/)
        2. Sign up for a free account
        3. Navigate to Keys section
        4. Create a new API key

        ### Step 2: Configure Environment

        1. Open the file: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/.env`
        2. Replace `your_openrouter_api_key_here` with your actual API key
        3. Save the file

        ### Step 3: Restart Web Interface

        ```bash
        # Stop current instance (Ctrl+C in terminal)
        # Restart with:
        ./launch.sh
        ```

        ### Environment File Location

        ```
        /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/.env
        ```

        ### Model Information

        **Default Model**: `google/gemini-2.5-flash-lite-preview-09-2025`
        - Fast and efficient
        - Free tier available on OpenRouter
        - Good for conversational queries

        You can change the model in the .env file if needed.
        """)

    st.markdown("---")

    st.info("""
    💡 **Without AI Assistant, you can still use**:
    - Documents page for browsing and search
    - Entities page for entity exploration
    - Analytics page for statistics
    - System page for ingestion control
    """)

# Footer
st.markdown("---")
st.caption("AEON AI Assistant | Powered by OpenRouter + Neo4j + Qdrant")
