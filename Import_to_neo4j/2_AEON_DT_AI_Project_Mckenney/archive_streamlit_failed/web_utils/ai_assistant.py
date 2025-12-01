"""
AI Assistant for AEON Web Interface
Integrates OpenRouter, Qdrant RAG, Neo4j queries, and existing AEON agents
"""

import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime

# Setup paths - prioritize parent project directory
parent_project_dir = Path(__file__).parent.parent.parent
web_interface_dir = parent_project_dir / "web_interface"

# Add parent first (for agents and parent utils), then web_interface (for web utils)
if str(parent_project_dir) not in sys.path:
    sys.path.insert(0, str(parent_project_dir))
if str(web_interface_dir) not in sys.path:
    sys.path.insert(1, str(web_interface_dir))

import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

from web_utils.neo4j_connector import get_connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIAssistant:
    """
    AI Assistant for AEON Document Ingestion System

    Features:
    - Natural language queries about documents and entities
    - Ingestion guidance and classification assistance
    - RAG-based answers using Qdrant vector search
    - Neo4j graph traversal for relationship queries
    - Conversation memory and context tracking
    """

    def __init__(self):
        """Initialize AI Assistant with all integrations"""
        # OpenRouter configuration
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite-preview-09-2025")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        # Neo4j connector
        self.neo4j = get_connector()

        # Qdrant configuration
        self.qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
        self.conv_collection = os.getenv("QDRANT_COLLECTION_CONVERSATIONS", "aeon_conversations")
        self.doc_collection = os.getenv("QDRANT_COLLECTION_DOCUMENTS", "aeon_document_embeddings")

        # Initialize Qdrant client
        try:
            self.qdrant = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
            self.qdrant_available = True
            self._ensure_collections()
        except Exception as e:
            print(f"⚠️ Qdrant not available: {e}")
            self.qdrant_available = False

        # Initialize sentence transformer for embeddings
        try:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dim = 384
        except Exception as e:
            print(f"⚠️ Sentence transformer not available: {e}")
            self.embedder = None

        # Conversation context
        self.max_context_messages = int(os.getenv("AI_MAX_CONTEXT_MESSAGES", 10))

    def _ensure_collections(self):
        """Ensure required Qdrant collections exist"""
        if not self.qdrant_available:
            return

        try:
            # Create conversations collection
            collections = [c.name for c in self.qdrant.get_collections().collections]

            if self.conv_collection not in collections:
                self.qdrant.create_collection(
                    collection_name=self.conv_collection,
                    vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE)
                )

            if self.doc_collection not in collections:
                self.qdrant.create_collection(
                    collection_name=self.doc_collection,
                    vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE)
                )
        except Exception as e:
            print(f"⚠️ Could not create collections: {e}")

    def chat(self, user_message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process user message and generate AI response

        Args:
            user_message: User's question or command
            session_id: Session identifier for conversation tracking

        Returns:
            Dictionary with response and metadata
        """
        # Get relevant context from RAG
        context = self._get_rag_context(user_message)

        # Build system prompt with AEON knowledge
        system_prompt = self._build_system_prompt(context)

        # Get conversation history
        history = self._get_conversation_history(session_id)

        # Prepare messages for OpenRouter
        messages = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": user_message}
        ]

        # Call OpenRouter API
        try:
            response = self._call_openrouter(messages)
            assistant_message = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Store conversation in memory
            self._store_conversation(session_id, user_message, assistant_message)

            return {
                "success": True,
                "response": assistant_message,
                "context_used": len(context.get("documents", [])),
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": f"❌ Error: {str(e)}\n\nI can still help with basic queries using the database directly."
            }

    def _call_openrouter(self, messages: List[Dict]) -> Dict:
        """Call OpenRouter API"""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set in .env file")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        return response.json()

    def _get_rag_context(self, query: str) -> Dict[str, Any]:
        """
        Get relevant context using RAG (Retrieval-Augmented Generation)
        Combines Qdrant vector search with Neo4j graph queries
        """
        context = {
            "documents": [],
            "entities": [],
            "relationships": []
        }

        if not self.embedder or not self.qdrant_available:
            return context

        try:
            # Generate query embedding
            query_vector = self.embedder.encode(query).tolist()

            # Search Qdrant for similar documents (if collection exists and has data)
            try:
                search_results = self.qdrant.search(
                    collection_name=self.doc_collection,
                    query_vector=query_vector,
                    limit=5
                )

                for result in search_results:
                    if result.payload:
                        context["documents"].append({
                            "title": result.payload.get("title", "Unknown"),
                            "content": result.payload.get("content", "")[:500],  # First 500 chars
                            "score": result.score
                        })
            except Exception:
                # Collection might not exist or be empty - that's okay
                pass

        except Exception as e:
            print(f"⚠️ RAG search error: {e}")

        # Get relevant entities from Neo4j
        try:
            # Extract potential entity names from query
            keywords = query.split()
            for keyword in keywords:
                entities = self.neo4j.search_entities(keyword, limit=3)
                context["entities"].extend(entities[:3])
        except Exception:
            pass

        return context

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with AEON knowledge and context"""
        base_prompt = """You are an AI assistant for the AEON (Automated EON) Document Ingestion System.

AEON helps users:
- Ingest and classify industrial documents (SCADA, PLC, ICS)
- Extract entities (vendors, protocols, standards, components)
- Build knowledge graphs in Neo4j
- Search and query document relationships

Current System Status:
- Documents indexed: {doc_count}
- Entities extracted: {entity_count}
- Supported sectors: Water, Energy, Manufacturing, Transportation
- Entity types: VENDOR, PROTOCOL, STANDARD, COMPONENT, MEASUREMENT, SAFETY_CLASS, SYSTEM_LAYER

You can help users with:
1. Document ingestion and classification
2. Finding documents by sector, vendor, or topic
3. Exploring entity relationships
4. Understanding system architecture
5. Troubleshooting ingestion issues

Be concise, helpful, and technical when needed."""

        # Get system statistics
        try:
            stats = self.neo4j.get_statistics()
            doc_count = stats.get("total_documents", 0)
            entity_count = stats.get("total_entities", 0)
        except Exception:
            doc_count = "Unknown"
            entity_count = "Unknown"

        prompt = base_prompt.format(doc_count=doc_count, entity_count=entity_count)

        # Add context if available
        if context.get("documents"):
            prompt += "\n\nRelevant documents found:\n"
            for doc in context["documents"][:3]:
                prompt += f"- {doc['title']}: {doc['content'][:200]}...\n"

        if context.get("entities"):
            prompt += "\n\nRelevant entities found:\n"
            for ent in context["entities"][:5]:
                prompt += f"- {ent.get('text')} ({ent.get('label')})\n"

        return prompt

    def _get_conversation_history(self, session_id: str) -> List[Dict]:
        """Retrieve conversation history from Qdrant"""
        if not self.qdrant_available:
            return []

        try:
            # Get recent conversation from Qdrant
            points = self.qdrant.scroll(
                collection_name=self.conv_collection,
                scroll_filter={
                    "must": [
                        {
                            "key": "session_id",
                            "match": {"value": session_id}
                        }
                    ]
                },
                limit=self.max_context_messages,
                with_payload=True
            )

            messages = []
            for point in points[0]:
                payload = point.payload
                messages.append({"role": "user", "content": payload.get("user_message", "")})
                messages.append({"role": "assistant", "content": payload.get("assistant_message", "")})

            return messages[-self.max_context_messages:]
        except Exception:
            return []

    def _store_conversation(self, session_id: str, user_message: str, assistant_message: str):
        """Store conversation in Qdrant for memory"""
        if not self.qdrant_available or not self.embedder:
            return

        try:
            # Create embedding of conversation
            conversation_text = f"User: {user_message}\nAssistant: {assistant_message}"
            vector = self.embedder.encode(conversation_text).tolist()

            # Store in Qdrant
            point_id = f"{session_id}_{int(datetime.now().timestamp() * 1000)}"

            self.qdrant.upsert(
                collection_name=self.conv_collection,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "session_id": session_id,
                            "user_message": user_message,
                            "assistant_message": assistant_message,
                            "timestamp": datetime.now().isoformat()
                        }
                    )
                ]
            )
        except Exception as e:
            print(f"⚠️ Could not store conversation: {e}")

    def index_document(self, doc_id: str, title: str, content: str):
        """
        Index a document in Qdrant for RAG

        Args:
            doc_id: Document ID from Neo4j
            title: Document title
            content: Document content
        """
        if not self.qdrant_available or not self.embedder:
            return False

        try:
            # Create document embedding
            doc_text = f"{title}\n\n{content}"
            vector = self.embedder.encode(doc_text).tolist()

            # Store in Qdrant
            self.qdrant.upsert(
                collection_name=self.doc_collection,
                points=[
                    PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload={
                            "doc_id": doc_id,
                            "title": title,
                            "content": content[:2000],  # First 2000 chars
                            "indexed_at": datetime.now().isoformat()
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            print(f"⚠️ Could not index document: {e}")
            return False

    def search_entities(self, query: str) -> List[Dict]:
        """Search Neo4j for entities matching query"""
        try:
            return self.neo4j.search_entities(query, limit=10)
        except Exception:
            return []

    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics"""
        try:
            return self.neo4j.get_statistics()
        except Exception:
            return {}


def get_assistant() -> AIAssistant:
    """Get or create singleton AI assistant instance"""
    global _assistant_instance
    if '_assistant_instance' not in globals():
        _assistant_instance = AIAssistant()
    return _assistant_instance
