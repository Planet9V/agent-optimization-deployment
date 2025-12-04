"""
Embedding Service for Vendor Equipment
=======================================

Provides semantic embedding generation for vendor equipment entities
using sentence-transformers for high-quality vector representations.

Version: 1.0.0
Created: 2025-12-04
"""

import logging
from typing import List, Optional, Dict, Any
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Embedding service for vendor equipment semantic search.

    Uses sentence-transformers/all-MiniLM-L6-v2 by default which produces
    384-dimensional embeddings optimized for semantic similarity.
    """

    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_SIZE = 384

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        cache_size: int = 1000,
        lazy_load: bool = True,
    ):
        """
        Initialize embedding service.

        Args:
            model_name: Sentence transformer model to use
            cache_size: Number of embeddings to cache
            lazy_load: If True, model is loaded on first use
        """
        self.model_name = model_name
        self.cache_size = cache_size
        self._model = None
        self._cache: Dict[str, List[float]] = {}

        if not lazy_load:
            self._load_model()

    def _load_model(self) -> None:
        """Load the sentence transformer model."""
        if self._model is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded successfully")
        except ImportError:
            logger.warning("sentence-transformers not installed, using fallback")
            self._model = None
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self._model = None

    @property
    def model(self):
        """Get model, loading if necessary."""
        if self._model is None:
            self._load_model()
        return self._model

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.md5(text.encode()).hexdigest()

    def encode(self, text: str, use_cache: bool = True) -> List[float]:
        """
        Encode text to embedding vector.

        Args:
            text: Text to encode
            use_cache: Whether to use embedding cache

        Returns:
            List of floats representing the embedding vector
        """
        if not text or not text.strip():
            return [0.0] * self.VECTOR_SIZE

        text = text.strip()
        cache_key = self._get_cache_key(text)

        # Check cache
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        # Generate embedding
        if self.model is not None:
            try:
                embedding = self.model.encode(text).tolist()
            except Exception as e:
                logger.error(f"Embedding generation failed: {e}")
                embedding = [0.0] * self.VECTOR_SIZE
        else:
            # Fallback: zero vector
            embedding = [0.0] * self.VECTOR_SIZE

        # Cache result
        if use_cache:
            if len(self._cache) >= self.cache_size:
                # Evict oldest entry
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            self._cache[cache_key] = embedding

        return embedding

    def encode_batch(self, texts: List[str], use_cache: bool = True) -> List[List[float]]:
        """
        Encode multiple texts to embedding vectors.

        Args:
            texts: List of texts to encode
            use_cache: Whether to use embedding cache

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        # Split into cached and uncached
        results = [None] * len(texts)
        uncached_indices = []
        uncached_texts = []

        for i, text in enumerate(texts):
            if not text or not text.strip():
                results[i] = [0.0] * self.VECTOR_SIZE
            elif use_cache:
                cache_key = self._get_cache_key(text.strip())
                if cache_key in self._cache:
                    results[i] = self._cache[cache_key]
                else:
                    uncached_indices.append(i)
                    uncached_texts.append(text.strip())
            else:
                uncached_indices.append(i)
                uncached_texts.append(text.strip())

        # Batch encode uncached texts
        if uncached_texts and self.model is not None:
            try:
                embeddings = self.model.encode(uncached_texts).tolist()
                for idx, embedding in zip(uncached_indices, embeddings):
                    results[idx] = embedding
                    if use_cache:
                        cache_key = self._get_cache_key(uncached_texts[uncached_indices.index(idx)])
                        if len(self._cache) >= self.cache_size:
                            oldest_key = next(iter(self._cache))
                            del self._cache[oldest_key]
                        self._cache[cache_key] = embedding
            except Exception as e:
                logger.error(f"Batch embedding generation failed: {e}")
                for idx in uncached_indices:
                    results[idx] = [0.0] * self.VECTOR_SIZE
        else:
            for idx in uncached_indices:
                results[idx] = [0.0] * self.VECTOR_SIZE

        return results

    def encode_vendor(self, vendor_data: Dict[str, Any]) -> List[float]:
        """
        Generate embedding for vendor entity.

        Creates a rich text representation combining vendor name,
        industry focus, and other relevant metadata.

        Args:
            vendor_data: Vendor dictionary with name, industry_focus, etc.

        Returns:
            Embedding vector for the vendor
        """
        parts = []

        if vendor_data.get("name"):
            parts.append(vendor_data["name"])

        if vendor_data.get("industry_focus"):
            if isinstance(vendor_data["industry_focus"], list):
                parts.extend(vendor_data["industry_focus"])
            else:
                parts.append(vendor_data["industry_focus"])

        if vendor_data.get("country"):
            parts.append(vendor_data["country"])

        if vendor_data.get("description"):
            parts.append(vendor_data["description"])

        text = " ".join(filter(None, parts))
        return self.encode(text)

    def encode_equipment(self, equipment_data: Dict[str, Any]) -> List[float]:
        """
        Generate embedding for equipment entity.

        Creates a rich text representation combining model name,
        product line, category, and other relevant metadata.

        Args:
            equipment_data: Equipment dictionary with model_name, category, etc.

        Returns:
            Embedding vector for the equipment
        """
        parts = []

        if equipment_data.get("model_name"):
            parts.append(equipment_data["model_name"])

        if equipment_data.get("product_line"):
            parts.append(equipment_data["product_line"])

        if equipment_data.get("category"):
            parts.append(equipment_data["category"])

        if equipment_data.get("vendor_name"):
            parts.append(f"manufactured by {equipment_data['vendor_name']}")

        if equipment_data.get("description"):
            parts.append(equipment_data["description"])

        text = " ".join(filter(None, parts))
        return self.encode(text)

    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score between 0 and 1
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have same dimension")

        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a * a for a in embedding1) ** 0.5
        norm2 = sum(b * b for b in embedding2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def clear_cache(self) -> None:
        """Clear the embedding cache."""
        self._cache.clear()

    @property
    def cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "capacity": self.cache_size,
        }


# Global singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service(
    model_name: str = EmbeddingService.DEFAULT_MODEL,
    cache_size: int = 1000,
) -> EmbeddingService:
    """
    Get or create the global embedding service instance.

    Args:
        model_name: Model to use (only used on first call)
        cache_size: Cache size (only used on first call)

    Returns:
        EmbeddingService singleton instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService(
            model_name=model_name,
            cache_size=cache_size,
        )
    return _embedding_service
