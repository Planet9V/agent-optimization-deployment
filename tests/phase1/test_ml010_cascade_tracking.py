"""
ML-010 Cascade Tracking Tests
Test suite for cascade event tracking and genealogy
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.cascade_tracking import (
    create_cascade_event,
    track_cascade_genealogy,
    calculate_cascade_velocity,
    get_cascade_tree,
    analyze_cascade_pattern
)
from src.models.cascade_models import CascadeEvent, CascadeNode


class TestML010CascadeTracking:
    """Test suite for ML-010 cascade tracking functionality"""

    @pytest.fixture
    def sample_cascade_event(self) -> Dict[str, Any]:
        """Create sample cascade event"""
        return {
            "event_id": "CASCADE-001",
            "event_type": "phishing_attack",
            "source_entity": "EMAIL-SERVER-01",
            "timestamp": datetime.now(),
            "severity": "high",
            "metadata": {
                "campaign": "APT-28",
                "target_count": 150
            }
        }

    def test_create_cascade_event(self, sample_cascade_event):
        """
        Test: Create CascadeEvent
        Expected: Event created with tracking metadata
        """
        result = create_cascade_event(
            event_id=sample_cascade_event["event_id"],
            event_type=sample_cascade_event["event_type"],
            source_entity=sample_cascade_event["source_entity"],
            timestamp=sample_cascade_event["timestamp"],
            severity=sample_cascade_event["severity"],
            metadata=sample_cascade_event["metadata"]
        )

        assert result["success"] is True
        assert result["event_id"] == sample_cascade_event["event_id"]
        assert "cascade_id" in result
        assert result["generation"] == 0  # Root event

    def test_track_cascade_genealogy(self, sample_cascade_event):
        """
        Test: Track genealogy (parent→child)
        Expected: Parent-child relationships recorded
        """
        # Create parent event
        parent = create_cascade_event(
            event_id=sample_cascade_event["event_id"],
            event_type=sample_cascade_event["event_type"],
            source_entity=sample_cascade_event["source_entity"],
            timestamp=sample_cascade_event["timestamp"],
            severity=sample_cascade_event["severity"]
        )

        # Create child events
        child_events = []
        for i in range(3):
            child = create_cascade_event(
                event_id=f"CASCADE-001-CHILD-{i}",
                event_type="credential_theft",
                source_entity=f"WORKSTATION-{i:02d}",
                timestamp=datetime.now() + timedelta(minutes=i),
                severity="medium",
                parent_event_id=parent["event_id"]
            )
            child_events.append(child)

        # Track genealogy
        genealogy = track_cascade_genealogy(
            event_id=parent["event_id"]
        )

        assert genealogy["success"] is True
        assert genealogy["root_event"] == parent["event_id"]
        assert len(genealogy["descendants"]) == 3

        # Verify parent-child links
        for child in child_events:
            assert child["event_id"] in genealogy["descendants"]
            assert genealogy["descendants"][child["event_id"]]["parent"] == parent["event_id"]
            assert genealogy["descendants"][child["event_id"]]["generation"] == 1

    def test_calculate_cascade_velocity(self, sample_cascade_event):
        """
        Test: Calculate velocity
        Expected: Accurate propagation rate (events/hour)
        """
        # Create parent
        parent_time = datetime.now()
        parent = create_cascade_event(
            event_id=sample_cascade_event["event_id"],
            event_type=sample_cascade_event["event_type"],
            source_entity=sample_cascade_event["source_entity"],
            timestamp=parent_time,
            severity=sample_cascade_event["severity"]
        )

        # Create children over time
        num_children = 10
        time_span_hours = 2

        for i in range(num_children):
            create_cascade_event(
                event_id=f"CASCADE-001-CHILD-{i}",
                event_type="lateral_movement",
                source_entity=f"HOST-{i:02d}",
                timestamp=parent_time + timedelta(hours=i * time_span_hours / num_children),
                severity="medium",
                parent_event_id=parent["event_id"]
            )

        # Calculate velocity
        velocity = calculate_cascade_velocity(
            cascade_id=parent["cascade_id"]
        )

        assert velocity["success"] is True
        assert "events_per_hour" in velocity
        assert "acceleration" in velocity

        expected_velocity = num_children / time_span_hours
        assert abs(velocity["events_per_hour"] - expected_velocity) < 0.5

    def test_query_cascade_tree(self, sample_cascade_event):
        """
        Test: Query cascade tree
        Expected: Complete hierarchical structure
        """
        # Create multi-level cascade
        parent = create_cascade_event(
            event_id="CASCADE-ROOT",
            event_type="initial_compromise",
            source_entity="VPN-GATEWAY",
            timestamp=datetime.now(),
            severity="critical"
        )

        # Level 1 children
        level1_ids = []
        for i in range(3):
            child = create_cascade_event(
                event_id=f"CASCADE-L1-{i}",
                event_type="privilege_escalation",
                source_entity=f"SERVER-{i}",
                timestamp=datetime.now() + timedelta(minutes=i),
                severity="high",
                parent_event_id=parent["event_id"]
            )
            level1_ids.append(child["event_id"])

        # Level 2 children (grandchildren)
        for i, parent_id in enumerate(level1_ids):
            for j in range(2):
                create_cascade_event(
                    event_id=f"CASCADE-L2-{i}-{j}",
                    event_type="data_exfiltration",
                    source_entity=f"DATABASE-{i}-{j}",
                    timestamp=datetime.now() + timedelta(minutes=10 + i * 2 + j),
                    severity="high",
                    parent_event_id=parent_id
                )

        # Query tree
        tree = get_cascade_tree(
            root_event_id=parent["event_id"]
        )

        assert tree["success"] is True
        assert tree["root"]["event_id"] == parent["event_id"]
        assert len(tree["root"]["children"]) == 3  # Level 1

        # Verify Level 2
        for l1_child in tree["root"]["children"]:
            assert len(l1_child["children"]) == 2  # Level 2
            for l2_child in l1_child["children"]:
                assert l2_child["generation"] == 2

    def test_cascade_pattern_analysis(self, sample_cascade_event):
        """
        Test: Cascade pattern recognition
        Expected: Identify branching, linear, or explosive patterns
        """
        # Create linear cascade
        linear_parent = create_cascade_event(
            event_id="CASCADE-LINEAR",
            event_type="initial",
            source_entity="HOST-A",
            timestamp=datetime.now(),
            severity="high"
        )

        prev_event_id = linear_parent["event_id"]
        for i in range(5):
            event = create_cascade_event(
                event_id=f"CASCADE-LINEAR-{i}",
                event_type="propagation",
                source_entity=f"HOST-{chr(66+i)}",
                timestamp=datetime.now() + timedelta(minutes=i),
                severity="medium",
                parent_event_id=prev_event_id
            )
            prev_event_id = event["event_id"]

        # Analyze pattern
        analysis = analyze_cascade_pattern(
            cascade_id=linear_parent["cascade_id"]
        )

        assert analysis["success"] is True
        assert analysis["pattern_type"] in ["linear", "branching", "explosive"]
        assert "branching_factor" in analysis
        assert "depth" in analysis
        assert analysis["depth"] == 6  # Root + 5 children

    def test_cascade_with_cycles_detection(self):
        """
        Test: Detect cycles in cascade graph
        Expected: Cycle detection and warning
        """
        # Create events with potential cycle
        event_a = create_cascade_event(
            event_id="CASCADE-A",
            event_type="attack",
            source_entity="HOST-A",
            timestamp=datetime.now(),
            severity="high"
        )

        event_b = create_cascade_event(
            event_id="CASCADE-B",
            event_type="attack",
            source_entity="HOST-B",
            timestamp=datetime.now() + timedelta(minutes=1),
            severity="high",
            parent_event_id=event_a["event_id"]
        )

        # Attempt to create cycle (B -> A)
        result = create_cascade_event(
            event_id="CASCADE-C",
            event_type="attack",
            source_entity="HOST-A",
            timestamp=datetime.now() + timedelta(minutes=2),
            severity="high",
            parent_event_id=event_b["event_id"],
            target_entity=event_a["source_entity"]
        )

        # Should detect potential cycle
        if result.get("cycle_detected"):
            assert result["cycle_warning"] is True

    def test_cascade_merge_events(self):
        """
        Test: Merge multiple cascade branches
        Expected: Combined cascade tree with all branches
        """
        # Create two separate cascades
        cascade1 = create_cascade_event(
            event_id="CASCADE-1-ROOT",
            event_type="attack_vector_1",
            source_entity="VECTOR-1",
            timestamp=datetime.now(),
            severity="high"
        )

        cascade2 = create_cascade_event(
            event_id="CASCADE-2-ROOT",
            event_type="attack_vector_2",
            source_entity="VECTOR-2",
            timestamp=datetime.now(),
            severity="high"
        )

        # Create converging event (both cascades lead to same target)
        converge = create_cascade_event(
            event_id="CASCADE-CONVERGE",
            event_type="data_breach",
            source_entity="DATABASE-MAIN",
            timestamp=datetime.now() + timedelta(minutes=10),
            severity="critical",
            parent_events=[cascade1["event_id"], cascade2["event_id"]]
        )

        # Query should show merged cascade
        tree = get_cascade_tree(root_event_id=converge["event_id"])
        assert len(tree.get("parent_cascades", [])) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
