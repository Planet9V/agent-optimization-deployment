#!/usr/bin/env python3
"""
Agent Query Interface - Semantic Search for Schema Knowledge
Provides fast semantic search across schema documentation for agents

File: agent_query_interface.py
Created: 2025-10-31
Purpose: Enable agents to query schema knowledge with semantic search
Status: ACTIVE
"""

import sys
from typing import List, Dict, Any, Optional
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Configuration
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = "deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
OPENAI_API_KEY = "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"
EMBEDDING_MODEL = "text-embedding-3-large"


class AgentQueryInterface:
    """
    Semantic search interface for agents to query schema knowledge

    Features:
    - Natural language queries
    - Semantic similarity search
    - File and wave filtering
    - Confidence scoring
    - Context-aware results
    """

    def __init__(self):
        """Initialize query interface"""
        # Connect to Qdrant
        self.qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        print(f"✓ Connected to Qdrant at {QDRANT_URL}")

        # Connect to OpenAI
        self.openai = OpenAI(api_key=OPENAI_API_KEY)
        print(f"✓ Connected to OpenAI for embeddings")

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for search query"""
        try:
            response = self.openai.embeddings.create(
                model=EMBEDDING_MODEL,
                input=query
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"✗ Error generating embedding: {e}")
            sys.exit(1)

    def search_schema_knowledge(
        self,
        query: str,
        top_k: int = 5,
        file_filter: Optional[str] = None,
        wave_filter: Optional[str] = None,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search schema knowledge with semantic similarity

        Args:
            query: Natural language search query
            top_k: Number of results to return
            file_filter: Filter by filename (e.g., "WAVE_1")
            wave_filter: Filter by wave number (e.g., "WAVE_1")
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of matching results with text, metadata, and scores
        """
        print(f"\n🔍 Searching: '{query}'")

        # Generate query embedding
        query_vector = self.generate_query_embedding(query)

        # Build filter conditions
        filter_conditions = []
        if file_filter:
            filter_conditions.append(
                FieldCondition(
                    key="file_name",
                    match=MatchValue(value=file_filter)
                )
            )

        # Execute search
        try:
            results = self.qdrant.search(
                collection_name="schema_knowledge",
                query_vector=query_vector,
                limit=top_k,
                query_filter=Filter(must=filter_conditions) if filter_conditions else None,
                score_threshold=score_threshold
            )

            # Format results
            formatted_results = []
            for idx, result in enumerate(results, 1):
                formatted_results.append({
                    "rank": idx,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "file_name": result.payload.get("file_name", ""),
                    "chunk_id": result.payload.get("chunk_id", 0),
                    "file_path": result.payload.get("file_path", ""),
                    "start_char": result.payload.get("start_char", 0),
                    "end_char": result.payload.get("end_char", 0)
                })

            print(f"✓ Found {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            print(f"✗ Search error: {e}")
            return []

    def search_by_wave(self, query: str, wave_number: int, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search within specific implementation wave

        Args:
            query: Search query
            wave_number: Wave number (1-12)
            top_k: Number of results

        Returns:
            List of matching results from that wave
        """
        # Map wave numbers to file patterns
        wave_file_pattern = f"WAVE_{wave_number}_"

        print(f"\n🌊 Searching Wave {wave_number}: '{query}'")

        # Search with wave filter
        results = self.search_schema_knowledge(
            query=query,
            top_k=top_k,
            file_filter=None  # Will filter manually
        )

        # Filter for wave-specific files
        wave_results = [
            r for r in results
            if f"WAVE_{wave_number}_" in r["file_name"] or
               f"0{wave_number}_WAVE" in r["file_name"]
        ]

        print(f"✓ Found {len(wave_results)} results in Wave {wave_number}")
        return wave_results

    def get_context_around_chunk(
        self,
        file_name: str,
        chunk_id: int,
        context_chunks: int = 2
    ) -> str:
        """
        Get surrounding context for a specific chunk

        Args:
            file_name: Name of the file
            chunk_id: ID of the target chunk
            context_chunks: Number of chunks before/after to include

        Returns:
            Combined text with context
        """
        # Search for neighboring chunks
        chunks = []
        for offset in range(-context_chunks, context_chunks + 1):
            target_id = chunk_id + offset

            results = self.qdrant.scroll(
                collection_name="schema_knowledge",
                scroll_filter=Filter(
                    must=[
                        FieldCondition(key="file_name", match=MatchValue(value=file_name)),
                        FieldCondition(key="chunk_id", match=MatchValue(value=target_id))
                    ]
                ),
                limit=1
            )

            if results[0]:
                chunk = results[0][0]
                chunks.append((target_id, chunk.payload.get("text", "")))

        # Sort by chunk_id and combine
        chunks.sort(key=lambda x: x[0])
        context_text = "\n\n".join([text for _, text in chunks])

        return context_text

    def interactive_search(self):
        """Interactive search mode for testing"""
        print(f"\n{'='*70}")
        print(f"AGENT QUERY INTERFACE - Interactive Mode")
        print(f"{'='*70}\n")
        print(f"Commands:")
        print(f"  search <query>              - Semantic search")
        print(f"  wave <number> <query>       - Search within wave")
        print(f"  context <file> <chunk_id>   - Get chunk context")
        print(f"  quit                        - Exit")
        print(f"\n{'='*70}\n")

        while True:
            try:
                command = input("\n> ").strip()

                if not command:
                    continue

                if command.lower() in ["quit", "exit", "q"]:
                    print(f"\n✓ Goodbye!")
                    break

                parts = command.split(maxsplit=1)
                cmd = parts[0].lower()

                if cmd == "search" and len(parts) > 1:
                    query = parts[1]
                    results = self.search_schema_knowledge(query, top_k=5)
                    self._print_results(results)

                elif cmd == "wave" and len(parts) > 1:
                    wave_parts = parts[1].split(maxsplit=1)
                    if len(wave_parts) == 2:
                        wave_number = int(wave_parts[0])
                        query = wave_parts[1]
                        results = self.search_by_wave(query, wave_number, top_k=3)
                        self._print_results(results)

                elif cmd == "context" and len(parts) > 1:
                    context_parts = parts[1].split()
                    if len(context_parts) >= 2:
                        file_name = context_parts[0]
                        chunk_id = int(context_parts[1])
                        context = self.get_context_around_chunk(file_name, chunk_id)
                        print(f"\n{'='*70}")
                        print(f"CONTEXT FOR {file_name} chunk {chunk_id}")
                        print(f"{'='*70}\n")
                        print(context)

                else:
                    print(f"⚠ Unknown command: {command}")

            except KeyboardInterrupt:
                print(f"\n\n✓ Interrupted")
                break
            except Exception as e:
                print(f"✗ Error: {e}")

    def _print_results(self, results: List[Dict[str, Any]]):
        """Print formatted search results"""
        if not results:
            print(f"\n⚠ No results found")
            return

        print(f"\n{'='*70}")
        print(f"SEARCH RESULTS ({len(results)} found)")
        print(f"{'='*70}\n")

        for result in results:
            print(f"[{result['rank']}] Score: {result['score']:.3f}")
            print(f"    File: {result['file_name']} (chunk {result['chunk_id']})")
            print(f"    Text: {result['text'][:200]}...")
            print()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command-line query
        query = " ".join(sys.argv[1:])

        interface = AgentQueryInterface()
        results = interface.search_schema_knowledge(query, top_k=5)

        print(f"\n{'='*70}")
        print(f"RESULTS FOR: '{query}'")
        print(f"{'='*70}\n")

        for result in results:
            print(f"[{result['rank']}] Score: {result['score']:.3f}")
            print(f"    File: {result['file_name']}")
            print(f"    {result['text'][:300]}...")
            print()

    else:
        # Interactive mode
        interface = AgentQueryInterface()
        interface.interactive_search()


if __name__ == "__main__":
    main()
