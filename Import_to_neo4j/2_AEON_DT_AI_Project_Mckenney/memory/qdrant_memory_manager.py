"""
Qdrant Memory Manager
Integrates with Qdrant for tracking agent activities, checkpoints, and state preservation
"""

import logging
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import warnings

# Optional imports with graceful fallback
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance,
        VectorParams,
        PointStruct,
        Filter,
        FieldCondition,
        MatchValue,
        SearchRequest
    )
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    warnings.warn("Qdrant client not available. Using in-memory fallback mode.")

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    warnings.warn("sentence-transformers not available. Embedding features disabled.")


@dataclass
class AgentActivity:
    """Represents a single agent activity"""
    activity_id: str
    agent_name: str
    activity_type: str
    timestamp: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class Checkpoint:
    """Represents a state checkpoint"""
    checkpoint_id: str
    checkpoint_name: str
    timestamp: str
    state_data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class ClassificationDecision:
    """Represents a classification decision with user feedback"""
    decision_id: str
    file_path: str
    sector: str
    subsector: str
    confidence: float
    user_feedback: Optional[str]
    timestamp: str
    metadata: Dict[str, Any]


class QdrantMemoryManager:
    """
    Memory manager integrating with Qdrant for agent tracking and state preservation.
    Falls back to in-memory storage if Qdrant is unavailable.
    """

    # Collection configurations
    COLLECTIONS = {
        "agent_activities": {
            "vector_size": 384,  # all-MiniLM-L6-v2 embedding size
            "distance": Distance.COSINE
        },
        "checkpoints": {
            "vector_size": 384,
            "distance": Distance.COSINE
        },
        "classification_memory": {
            "vector_size": 384,
            "distance": Distance.COSINE
        },
        "document_embeddings": {
            "vector_size": 384,
            "distance": Distance.COSINE
        }
    }

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        use_qdrant: bool = True,
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize Qdrant Memory Manager

        Args:
            host: Qdrant server host
            port: Qdrant server port
            use_qdrant: Whether to attempt Qdrant connection
            embedding_model: Sentence transformer model name
        """
        self.logger = self._setup_logger()
        self.use_qdrant = use_qdrant and QDRANT_AVAILABLE
        self.client: Optional[QdrantClient] = None
        self.embedding_model = None

        # In-memory fallback storage
        self.memory_store = {
            "agent_activities": [],
            "checkpoints": {},
            "classification_memory": [],
            "document_embeddings": []
        }

        # Initialize Qdrant client
        if self.use_qdrant:
            try:
                self.client = QdrantClient(host=host, port=port)
                self._initialize_collections()
                self.logger.info(f"Connected to Qdrant at {host}:{port}")
            except Exception as e:
                self.logger.warning(f"Failed to connect to Qdrant: {e}. Using in-memory fallback.")
                self.use_qdrant = False
                self.client = None

        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer(embedding_model)
                self.logger.info(f"Loaded embedding model: {embedding_model}")
            except Exception as e:
                self.logger.warning(f"Failed to load embedding model: {e}")
                self.embedding_model = None
        else:
            self.logger.warning("Embeddings disabled - sentence-transformers not available")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for memory manager"""
        logger = logging.getLogger("QdrantMemoryManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _initialize_collections(self):
        """Initialize Qdrant collections if they don't exist"""
        if not self.client:
            return

        for collection_name, config in self.COLLECTIONS.items():
            try:
                # Check if collection exists
                collections = self.client.get_collections().collections
                exists = any(c.name == collection_name for c in collections)

                if not exists:
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=config["vector_size"],
                            distance=config["distance"]
                        )
                    )
                    self.logger.info(f"Created collection: {collection_name}")
            except Exception as e:
                self.logger.error(f"Error initializing collection {collection_name}: {e}")

    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text"""
        if not self.embedding_model:
            return None

        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return None

    def track_agent_activity(
        self,
        agent_name: str,
        activity_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Track agent activity

        Args:
            agent_name: Name of the agent
            activity_type: Type of activity (e.g., "classification", "processing", "error")
            data: Activity data
            metadata: Optional additional metadata

        Returns:
            Activity ID
        """
        activity_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        activity = AgentActivity(
            activity_id=activity_id,
            agent_name=agent_name,
            activity_type=activity_type,
            timestamp=timestamp,
            data=data,
            metadata=metadata or {}
        )

        # Generate embedding from activity description
        activity_text = f"{agent_name} {activity_type} {json.dumps(data)}"
        embedding = self._generate_embedding(activity_text)

        if self.use_qdrant and self.client and embedding:
            try:
                point = PointStruct(
                    id=activity_id,
                    vector=embedding,
                    payload=asdict(activity)
                )
                self.client.upsert(
                    collection_name="agent_activities",
                    points=[point]
                )
                self.logger.debug(f"Tracked activity {activity_id} for {agent_name}")
            except Exception as e:
                self.logger.error(f"Error tracking activity in Qdrant: {e}")
                self.memory_store["agent_activities"].append(asdict(activity))
        else:
            # Fallback to in-memory storage
            self.memory_store["agent_activities"].append(asdict(activity))

        return activity_id

    def store_checkpoint(
        self,
        checkpoint_name: str,
        state_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store state checkpoint

        Args:
            checkpoint_name: Unique checkpoint name
            state_data: State data to preserve
            metadata: Optional metadata

        Returns:
            Checkpoint ID
        """
        checkpoint_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            checkpoint_name=checkpoint_name,
            timestamp=timestamp,
            state_data=state_data,
            metadata=metadata or {}
        )

        # Generate embedding from checkpoint description
        checkpoint_text = f"{checkpoint_name} {json.dumps(state_data)}"
        embedding = self._generate_embedding(checkpoint_text)

        if self.use_qdrant and self.client and embedding:
            try:
                point = PointStruct(
                    id=checkpoint_id,
                    vector=embedding,
                    payload=asdict(checkpoint)
                )
                self.client.upsert(
                    collection_name="checkpoints",
                    points=[point]
                )
                self.logger.info(f"Stored checkpoint: {checkpoint_name}")
            except Exception as e:
                self.logger.error(f"Error storing checkpoint in Qdrant: {e}")
                self.memory_store["checkpoints"][checkpoint_name] = asdict(checkpoint)
        else:
            # Fallback to in-memory storage
            self.memory_store["checkpoints"][checkpoint_name] = asdict(checkpoint)

        return checkpoint_id

    def retrieve_checkpoint(self, checkpoint_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve state checkpoint by name

        Args:
            checkpoint_name: Checkpoint name to retrieve

        Returns:
            Checkpoint data or None if not found
        """
        if self.use_qdrant and self.client:
            try:
                # Search for checkpoint by name
                results = self.client.scroll(
                    collection_name="checkpoints",
                    scroll_filter=Filter(
                        must=[
                            FieldCondition(
                                key="checkpoint_name",
                                match=MatchValue(value=checkpoint_name)
                            )
                        ]
                    ),
                    limit=1
                )

                if results[0]:  # results is tuple (points, next_page_offset)
                    return results[0][0].payload

            except Exception as e:
                self.logger.error(f"Error retrieving checkpoint from Qdrant: {e}")

        # Fallback to in-memory storage
        return self.memory_store["checkpoints"].get(checkpoint_name)

    def store_classification_decision(
        self,
        file_path: str,
        sector: str,
        subsector: str,
        confidence: float,
        user_feedback: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store classification decision with user feedback

        Args:
            file_path: Path to classified file
            sector: Classified sector
            subsector: Classified subsector
            confidence: Classification confidence score
            user_feedback: Optional user feedback
            metadata: Optional metadata

        Returns:
            Decision ID
        """
        decision_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        decision = ClassificationDecision(
            decision_id=decision_id,
            file_path=file_path,
            sector=sector,
            subsector=subsector,
            confidence=confidence,
            user_feedback=user_feedback,
            timestamp=timestamp,
            metadata=metadata or {}
        )

        # Generate embedding from classification context
        decision_text = f"{file_path} {sector} {subsector} {user_feedback or ''}"
        embedding = self._generate_embedding(decision_text)

        if self.use_qdrant and self.client and embedding:
            try:
                point = PointStruct(
                    id=decision_id,
                    vector=embedding,
                    payload=asdict(decision)
                )
                self.client.upsert(
                    collection_name="classification_memory",
                    points=[point]
                )
                self.logger.debug(f"Stored classification decision {decision_id}")
            except Exception as e:
                self.logger.error(f"Error storing classification in Qdrant: {e}")
                self.memory_store["classification_memory"].append(asdict(decision))
        else:
            # Fallback to in-memory storage
            self.memory_store["classification_memory"].append(asdict(decision))

        return decision_id

    def search_similar_documents(
        self,
        document_embedding: List[float],
        top_k: int = 5
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for similar documents using vector similarity

        Args:
            document_embedding: Document embedding vector
            top_k: Number of results to return

        Returns:
            List of (document_id, score, metadata) tuples
        """
        if not self.use_qdrant or not self.client:
            self.logger.warning("Qdrant not available, cannot search similar documents")
            return []

        try:
            search_result = self.client.search(
                collection_name="document_embeddings",
                query_vector=document_embedding,
                limit=top_k
            )

            results = [
                (point.id, point.score, point.payload)
                for point in search_result
            ]

            return results

        except Exception as e:
            self.logger.error(f"Error searching similar documents: {e}")
            return []

    def get_agent_history(
        self,
        agent_name: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get activity history for specific agent

        Args:
            agent_name: Agent name
            limit: Maximum number of activities to return

        Returns:
            List of agent activities
        """
        if self.use_qdrant and self.client:
            try:
                results = self.client.scroll(
                    collection_name="agent_activities",
                    scroll_filter=Filter(
                        must=[
                            FieldCondition(
                                key="agent_name",
                                match=MatchValue(value=agent_name)
                            )
                        ]
                    ),
                    limit=limit
                )

                if results[0]:
                    return [point.payload for point in results[0]]

            except Exception as e:
                self.logger.error(f"Error retrieving agent history from Qdrant: {e}")

        # Fallback to in-memory storage
        activities = [
            activity for activity in self.memory_store["agent_activities"]
            if activity["agent_name"] == agent_name
        ]
        return activities[-limit:] if len(activities) > limit else activities

    def store_document_embedding(
        self,
        document_id: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Store document embedding for similarity search

        Args:
            document_id: Unique document identifier
            embedding: Document embedding vector
            metadata: Document metadata

        Returns:
            Success status
        """
        if not self.use_qdrant or not self.client:
            self.logger.warning("Qdrant not available, cannot store document embedding")
            self.memory_store["document_embeddings"].append({
                "document_id": document_id,
                "metadata": metadata
            })
            return False

        try:
            point = PointStruct(
                id=document_id,
                vector=embedding,
                payload=metadata
            )
            self.client.upsert(
                collection_name="document_embeddings",
                points=[point]
            )
            self.logger.debug(f"Stored embedding for document {document_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error storing document embedding: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory manager statistics

        Returns:
            Statistics dictionary
        """
        stats = {
            "qdrant_available": self.use_qdrant,
            "embeddings_available": self.embedding_model is not None,
            "mode": "qdrant" if self.use_qdrant else "in-memory"
        }

        if self.use_qdrant and self.client:
            try:
                collections = self.client.get_collections().collections
                stats["collections"] = {}
                for collection in collections:
                    if collection.name in self.COLLECTIONS:
                        collection_info = self.client.get_collection(collection.name)
                        stats["collections"][collection.name] = {
                            "points_count": collection_info.points_count,
                            "vectors_count": collection_info.vectors_count
                        }
            except Exception as e:
                self.logger.error(f"Error getting statistics: {e}")
        else:
            stats["in_memory_counts"] = {
                "agent_activities": len(self.memory_store["agent_activities"]),
                "checkpoints": len(self.memory_store["checkpoints"]),
                "classification_memory": len(self.memory_store["classification_memory"]),
                "document_embeddings": len(self.memory_store["document_embeddings"])
            }

        return stats

    def clear_collection(self, collection_name: str) -> bool:
        """
        Clear all data from a collection (use with caution)

        Args:
            collection_name: Collection to clear

        Returns:
            Success status
        """
        if collection_name not in self.COLLECTIONS:
            self.logger.error(f"Unknown collection: {collection_name}")
            return False

        if self.use_qdrant and self.client:
            try:
                self.client.delete_collection(collection_name)
                self._initialize_collections()
                self.logger.warning(f"Cleared collection: {collection_name}")
                return True
            except Exception as e:
                self.logger.error(f"Error clearing collection: {e}")
                return False
        else:
            # Clear in-memory storage
            if collection_name == "checkpoints":
                self.memory_store[collection_name] = {}
            else:
                self.memory_store[collection_name] = []
            return True
