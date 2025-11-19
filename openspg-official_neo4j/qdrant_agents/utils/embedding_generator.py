#!/usr/bin/env python3
"""
Embedding Generator - OpenAI Wrapper for Qdrant Agents
Provides caching and batch processing for embedding generation
"""

import os
import hashlib
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from openai import OpenAI
import structlog

logger = structlog.get_logger()

class EmbeddingGenerator:
    """
    OpenAI embedding generator with caching and batch processing
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-large",
        dimensions: int = 3072,
        cache_dir: Optional[Path] = None
    ):
        """Initialize embedding generator"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.dimensions = dimensions
        self.client = OpenAI(api_key=self.api_key)

        # Set up cache
        self.cache_dir = cache_dir or Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/qdrant_backup/embeddings_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_enabled = True

        logger.info("embedding_generator_initialized", model=self.model, dimensions=self.dimensions)

    def _cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.sha256(f"{self.model}:{text}".encode()).hexdigest()

    def _get_cached(self, text: str) -> Optional[List[float]]:
        """Retrieve cached embedding"""
        if not self.cache_enabled:
            return None

        cache_key = self._cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                logger.debug("embedding_cache_hit", text_length=len(text))
                return data["embedding"]
            except Exception as e:
                logger.warning("embedding_cache_read_failed", error=str(e))

        return None

    def _set_cached(self, text: str, embedding: List[float]):
        """Store embedding in cache"""
        if not self.cache_enabled:
            return

        cache_key = self._cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    "text": text[:200],  # First 200 chars for reference
                    "model": self.model,
                    "dimensions": self.dimensions,
                    "embedding": embedding
                }, f)
            logger.debug("embedding_cached", text_length=len(text))
        except Exception as e:
            logger.warning("embedding_cache_write_failed", error=str(e))

    def create(self, text: str, use_cache: bool = True) -> List[float]:
        """
        Generate embedding for text

        Args:
            text: Input text
            use_cache: Whether to use cache

        Returns:
            Embedding vector
        """
        # Check cache
        if use_cache:
            cached = self._get_cached(text)
            if cached is not None:
                return cached

        # Generate embedding
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                dimensions=self.dimensions
            )

            embedding = response.data[0].embedding

            # Cache result
            if use_cache:
                self._set_cached(text, embedding)

            logger.info("embedding_generated", text_length=len(text), model=self.model)
            return embedding

        except Exception as e:
            logger.error("embedding_generation_failed", error=str(e), text_length=len(text))
            raise

    def create_batch(
        self,
        texts: List[str],
        batch_size: int = 100,
        use_cache: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for batch of texts

        Args:
            texts: List of input texts
            batch_size: Maximum texts per API call
            use_cache: Whether to use cache

        Returns:
            List of embedding vectors
        """
        embeddings = []
        uncached_texts = []
        uncached_indices = []

        # Check cache for all texts
        if use_cache:
            for idx, text in enumerate(texts):
                cached = self._get_cached(text)
                if cached is not None:
                    embeddings.append((idx, cached))
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(idx)
        else:
            uncached_texts = texts
            uncached_indices = list(range(len(texts)))

        # Generate embeddings for uncached texts
        for i in range(0, len(uncached_texts), batch_size):
            batch = uncached_texts[i:i + batch_size]
            batch_indices = uncached_indices[i:i + batch_size]

            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    dimensions=self.dimensions
                )

                for idx, data in zip(batch_indices, response.data):
                    embedding = data.embedding
                    embeddings.append((idx, embedding))

                    # Cache individual embedding
                    if use_cache:
                        self._set_cached(uncached_texts[idx - uncached_indices[0]], embedding)

                logger.info("batch_embeddings_generated", batch_size=len(batch), model=self.model)

            except Exception as e:
                logger.error("batch_embedding_failed", error=str(e), batch_size=len(batch))
                raise

        # Sort by original index and return
        embeddings.sort(key=lambda x: x[0])
        return [emb for _, emb in embeddings]

    def clear_cache(self):
        """Clear embedding cache"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info("embedding_cache_cleared")
