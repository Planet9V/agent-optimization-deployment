"""
Unit tests for QdrantMemoryManager
Tests both Qdrant mode and in-memory fallback
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from memory.qdrant_memory_manager import QdrantMemoryManager


class TestQdrantMemoryManager:
    """Test suite for QdrantMemoryManager"""

    @pytest.fixture
    def memory_manager(self):
        """Create memory manager instance (will use in-memory fallback if Qdrant unavailable)"""
        return QdrantMemoryManager(use_qdrant=False)  # Force in-memory mode for testing

    def test_initialization(self, memory_manager):
        """Test memory manager initialization"""
        assert memory_manager is not None
        assert memory_manager.logger is not None
        assert isinstance(memory_manager.memory_store, dict)

    def test_track_agent_activity(self, memory_manager):
        """Test tracking agent activities"""
        activity_id = memory_manager.track_agent_activity(
            agent_name="TestAgent",
            activity_type="classification",
            data={"file": "test.pdf", "result": "success"},
            metadata={"version": "1.0"}
        )

        assert activity_id is not None
        assert len(activity_id) > 0

        # Verify activity was stored
        history = memory_manager.get_agent_history("TestAgent")
        assert len(history) == 1
        assert history[0]["agent_name"] == "TestAgent"
        assert history[0]["activity_type"] == "classification"

    def test_store_and_retrieve_checkpoint(self, memory_manager):
        """Test storing and retrieving checkpoints"""
        checkpoint_name = "test_checkpoint_1"
        state_data = {
            "processed_files": 10,
            "current_batch": 2,
            "errors": []
        }

        # Store checkpoint
        checkpoint_id = memory_manager.store_checkpoint(
            checkpoint_name=checkpoint_name,
            state_data=state_data,
            metadata={"phase": "processing"}
        )

        assert checkpoint_id is not None

        # Retrieve checkpoint
        retrieved = memory_manager.retrieve_checkpoint(checkpoint_name)
        assert retrieved is not None
        assert retrieved["checkpoint_name"] == checkpoint_name
        assert retrieved["state_data"] == state_data

    def test_store_classification_decision(self, memory_manager):
        """Test storing classification decisions"""
        decision_id = memory_manager.store_classification_decision(
            file_path="/path/to/document.pdf",
            sector="General Contractor",
            subsector="Commercial Construction",
            confidence=0.85,
            user_feedback="Correct classification",
            metadata={"model_version": "1.0"}
        )

        assert decision_id is not None
        assert len(decision_id) > 0

    def test_get_agent_history_with_limit(self, memory_manager):
        """Test getting agent history with limit"""
        # Add multiple activities
        for i in range(10):
            memory_manager.track_agent_activity(
                agent_name="TestAgent",
                activity_type=f"action_{i}",
                data={"index": i}
            )

        # Get limited history
        history = memory_manager.get_agent_history("TestAgent", limit=5)
        assert len(history) == 5

    def test_get_statistics(self, memory_manager):
        """Test getting memory statistics"""
        # Add some data
        memory_manager.track_agent_activity(
            agent_name="TestAgent",
            activity_type="test",
            data={}
        )
        memory_manager.store_checkpoint("test_cp", {"data": "test"})

        stats = memory_manager.get_statistics()
        assert stats is not None
        assert "mode" in stats
        assert stats["mode"] == "in-memory"
        assert "in_memory_counts" in stats

    def test_multiple_agents_tracking(self, memory_manager):
        """Test tracking activities for multiple agents"""
        agents = ["Agent1", "Agent2", "Agent3"]

        for agent in agents:
            for i in range(3):
                memory_manager.track_agent_activity(
                    agent_name=agent,
                    activity_type="processing",
                    data={"iteration": i}
                )

        # Verify each agent's history
        for agent in agents:
            history = memory_manager.get_agent_history(agent)
            assert len(history) == 3
            assert all(h["agent_name"] == agent for h in history)

    def test_checkpoint_overwrites(self, memory_manager):
        """Test that checkpoints with same name overwrite"""
        checkpoint_name = "recurring_checkpoint"

        # Store first checkpoint
        memory_manager.store_checkpoint(
            checkpoint_name=checkpoint_name,
            state_data={"version": 1}
        )

        # Store second checkpoint with same name
        memory_manager.store_checkpoint(
            checkpoint_name=checkpoint_name,
            state_data={"version": 2}
        )

        # Retrieve should get latest
        retrieved = memory_manager.retrieve_checkpoint(checkpoint_name)
        assert retrieved is not None
        assert retrieved["state_data"]["version"] == 2

    def test_clear_collection(self, memory_manager):
        """Test clearing collections"""
        # Add data
        memory_manager.track_agent_activity(
            agent_name="TestAgent",
            activity_type="test",
            data={}
        )

        # Clear collection
        success = memory_manager.clear_collection("agent_activities")
        assert success

        # Verify cleared
        history = memory_manager.get_agent_history("TestAgent")
        assert len(history) == 0

    def test_invalid_collection_clear(self, memory_manager):
        """Test clearing invalid collection name"""
        success = memory_manager.clear_collection("invalid_collection")
        assert not success

    def test_store_document_embedding_fallback(self, memory_manager):
        """Test storing document embeddings in fallback mode"""
        # Create dummy embedding
        embedding = [0.1] * 384

        success = memory_manager.store_document_embedding(
            document_id="doc_001",
            embedding=embedding,
            metadata={"filename": "test.pdf", "size": 1024}
        )

        # In fallback mode, this returns False but still stores metadata
        assert not success  # Because Qdrant is not available
        assert len(memory_manager.memory_store["document_embeddings"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
