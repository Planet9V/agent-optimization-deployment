"""
Qdrant Memory Manager for Classification Decision Tracking
Provides vector-based similarity search for learning from past classifications
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import hashlib
import json

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    logging.warning("Qdrant client not available. Memory features disabled.")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("Sentence transformers not available. Using dummy embeddings.")


class QdrantMemoryManager:
    """Memory manager for tracking and learning from classification decisions"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Qdrant memory manager

        Args:
            config: Configuration dictionary with memory settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.enabled = config.get('qdrant_enabled', False)

        if not self.enabled:
            self.logger.info("Qdrant memory disabled in config")
            self.client = None
            self.encoder = None
            return

        if not QDRANT_AVAILABLE:
            self.logger.warning("Qdrant client not installed. Memory features unavailable.")
            self.client = None
            self.encoder = None
            self.enabled = False
            return

        # Initialize Qdrant client
        try:
            self.client = QdrantClient(
                host=config.get('qdrant_host', 'localhost'),
                port=config.get('qdrant_port', 6333)
            )

            # Initialize sentence encoder
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                self.vector_size = 384
            else:
                self.encoder = None
                self.vector_size = config.get('vector_size', 384)

            self.collection_name = config.get('collection_name', 'document_classifications')
            self.distance_metric = Distance.COSINE

            # Create collection if it doesn't exist
            self._ensure_collection()

            self.logger.info("Qdrant memory manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Qdrant: {e}")
            self.client = None
            self.encoder = None
            self.enabled = False

    def _ensure_collection(self):
        """Ensure the collection exists"""
        if not self.client:
            return

        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=self.distance_metric
                    )
                )
                self.logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Failed to ensure collection: {e}")

    def _encode_text(self, text: str) -> List[float]:
        """
        Encode text to vector embedding

        Args:
            text: Text to encode

        Returns:
            Vector embedding
        """
        if self.encoder:
            return self.encoder.encode(text).tolist()
        else:
            # Dummy embedding if encoder not available
            import numpy as np
            np.random.seed(hash(text) % 2**32)
            return np.random.rand(self.vector_size).tolist()

    def store_classification(
        self,
        text: str,
        classification: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0
    ) -> bool:
        """
        Store a classification decision for future reference

        Args:
            text: Document text that was classified
            classification: Classification result (sector, subsector, doctype)
            metadata: Additional metadata
            confidence: Confidence score for this classification

        Returns:
            True if stored successfully
        """
        if not self.enabled or not self.client:
            return False

        try:
            # Generate unique ID
            doc_id = hashlib.sha256(text.encode()).hexdigest()[:16]

            # Encode text to vector
            vector = self._encode_text(text[:1000])  # Use first 1000 chars

            # Prepare payload
            payload = {
                'text_sample': text[:500],  # Store sample for reference
                'classification': classification,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {}
            }

            # Store in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )

            self.logger.debug(f"Stored classification for doc {doc_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store classification: {e}")
            return False

    def search_similar(
        self,
        text: str,
        limit: int = 5,
        min_confidence: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar previously classified documents

        Args:
            text: Text to find similar documents for
            limit: Maximum number of results
            min_confidence: Minimum confidence threshold for results

        Returns:
            List of similar classifications with scores
        """
        if not self.enabled or not self.client:
            return []

        try:
            # Encode query text
            query_vector = self._encode_text(text[:1000])

            # Search in Qdrant
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=min_confidence
            )

            # Format results
            similar_docs = []
            for result in results:
                similar_docs.append({
                    'classification': result.payload.get('classification'),
                    'confidence': result.payload.get('confidence'),
                    'similarity_score': result.score,
                    'timestamp': result.payload.get('timestamp'),
                    'text_sample': result.payload.get('text_sample', '')[:200]
                })

            self.logger.debug(f"Found {len(similar_docs)} similar documents")
            return similar_docs

        except Exception as e:
            self.logger.error(f"Failed to search similar documents: {e}")
            return []

    def update_classification(
        self,
        text: str,
        corrected_classification: Dict[str, Any],
        confidence: float = 1.0
    ) -> bool:
        """
        Update/correct a previous classification (learning from user corrections)

        Args:
            text: Original document text
            corrected_classification: Corrected classification
            confidence: New confidence score

        Returns:
            True if updated successfully
        """
        if not self.enabled or not self.client:
            return False

        try:
            # Generate ID (same as original)
            doc_id = hashlib.sha256(text.encode()).hexdigest()[:16]

            # Re-encode and update
            vector = self._encode_text(text[:1000])

            payload = {
                'text_sample': text[:500],
                'classification': corrected_classification,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'corrected': True
            }

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )

            self.logger.info(f"Updated classification for doc {doc_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update classification: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics

        Returns:
            Dictionary with memory stats
        """
        if not self.enabled or not self.client:
            return {'enabled': False, 'count': 0}

        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                'enabled': True,
                'collection': self.collection_name,
                'total_classifications': collection_info.points_count,
                'vector_size': self.vector_size
            }
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {'enabled': False, 'error': str(e)}
