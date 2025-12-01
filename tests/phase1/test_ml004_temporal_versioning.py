"""
ML-004 Temporal Versioning Tests
Test suite for temporal property versioning and point-in-time snapshots
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.temporal_versioning import (
    create_temporal_actor,
    get_point_in_time_snapshot,
    get_version_history,
    update_temporal_property
)
from src.models.temporal_models import TemporalActor, TemporalProperty


class TestML004TemporalVersioning:
    """Test suite for ML-004 temporal versioning functionality"""

    @pytest.fixture
    def sample_actor(self) -> Dict[str, Any]:
        """Create sample actor data"""
        return {
            "actor_id": "ACTOR-TEST-001",
            "name": "Test Operator Alice",
            "properties": {
                "security_clearance": "SECRET",
                "team": "Blue Team",
                "location": "Site A"
            }
        }

    def test_create_temporal_actor(self, sample_actor):
        """
        Test: Create Actor with temporal properties
        Expected: Actor created with versioned properties
        """
        result = create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        assert result["success"] is True
        assert result["actor_id"] == sample_actor["actor_id"]
        assert "version_id" in result
        assert "timestamp" in result

        # Verify all properties are versioned
        for prop_key in sample_actor["properties"].keys():
            assert prop_key in result["versioned_properties"]

    def test_point_in_time_snapshot(self, sample_actor):
        """
        Test: Query point-in-time snapshot
        Expected: Accurate historical state retrieval
        """
        # Create actor
        create_result = create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        initial_time = datetime.now()

        # Update property after delay
        import time
        time.sleep(0.1)

        update_temporal_property(
            actor_id=sample_actor["actor_id"],
            property_name="security_clearance",
            new_value="TOP SECRET"
        )

        # Query snapshot at initial time
        snapshot = get_point_in_time_snapshot(
            actor_id=sample_actor["actor_id"],
            timestamp=initial_time
        )

        assert snapshot["success"] is True
        assert snapshot["properties"]["security_clearance"] == "SECRET"
        assert snapshot["timestamp"] <= initial_time

    def test_version_history_accuracy(self, sample_actor):
        """
        Test: Version history accurate
        Expected: Complete chronological history of changes
        """
        # Create actor
        create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        # Make multiple updates
        updates = [
            ("security_clearance", "TOP SECRET"),
            ("team", "Red Team"),
            ("location", "Site B")
        ]

        for prop_name, new_value in updates:
            update_temporal_property(
                actor_id=sample_actor["actor_id"],
                property_name=prop_name,
                new_value=new_value
            )
            import time
            time.sleep(0.1)

        # Get version history
        history = get_version_history(
            actor_id=sample_actor["actor_id"]
        )

        assert history["success"] is True
        assert len(history["versions"]) >= 4  # Initial + 3 updates

        # Verify chronological order
        timestamps = [v["timestamp"] for v in history["versions"]]
        assert timestamps == sorted(timestamps)

        # Verify all changes are recorded
        for prop_name, new_value in updates:
            assert any(
                v["property"] == prop_name and v["new_value"] == new_value
                for v in history["versions"]
            )

    def test_temporal_property_isolation(self, sample_actor):
        """
        Test: Property updates are isolated
        Expected: Updating one property doesn't affect others
        """
        create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        # Update single property
        update_temporal_property(
            actor_id=sample_actor["actor_id"],
            property_name="security_clearance",
            new_value="TOP SECRET"
        )

        # Get current snapshot
        snapshot = get_point_in_time_snapshot(
            actor_id=sample_actor["actor_id"],
            timestamp=datetime.now()
        )

        # Other properties should remain unchanged
        assert snapshot["properties"]["team"] == sample_actor["properties"]["team"]
        assert snapshot["properties"]["location"] == sample_actor["properties"]["location"]
        assert snapshot["properties"]["security_clearance"] == "TOP SECRET"

    def test_concurrent_updates(self, sample_actor):
        """
        Test: Concurrent property updates
        Expected: All updates recorded with correct timestamps
        """
        create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        # Simulate concurrent updates
        import threading

        def update_property(prop_name, value):
            update_temporal_property(
                actor_id=sample_actor["actor_id"],
                property_name=prop_name,
                new_value=value
            )

        threads = [
            threading.Thread(target=update_property, args=("security_clearance", "TOP SECRET")),
            threading.Thread(target=update_property, args=("team", "Red Team")),
            threading.Thread(target=update_property, args=("location", "Site B"))
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify all updates recorded
        history = get_version_history(actor_id=sample_actor["actor_id"])
        assert len(history["versions"]) >= 4  # Initial + 3 concurrent updates

    def test_temporal_query_performance(self, sample_actor):
        """
        Test: Query performance for temporal snapshots
        Expected: <100ms for point-in-time queries
        """
        import time

        create_temporal_actor(
            actor_id=sample_actor["actor_id"],
            name=sample_actor["name"],
            properties=sample_actor["properties"]
        )

        # Create history
        for i in range(10):
            update_temporal_property(
                actor_id=sample_actor["actor_id"],
                property_name="security_clearance",
                new_value=f"LEVEL-{i}"
            )

        # Measure query time
        start = time.time()
        snapshot = get_point_in_time_snapshot(
            actor_id=sample_actor["actor_id"],
            timestamp=datetime.now() - timedelta(seconds=5)
        )
        elapsed = (time.time() - start) * 1000

        assert snapshot["success"] is True
        assert elapsed < 100, f"Query took {elapsed}ms, expected <100ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
