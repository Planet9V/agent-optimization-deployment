"""
Phase 1 Integration Tests
Test suite for verifying all Phase 1 gaps work together
"""

import pytest
import asyncio
import websockets
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import sys
from pathlib import Path
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.temporal_versioning import (
    create_temporal_actor,
    get_point_in_time_snapshot,
    update_temporal_property
)
from src.api.websocket_ews import (
    start_websocket_server,
    trigger_ews_alert
)
from src.api.cascade_tracking import (
    create_cascade_event,
    track_cascade_genealogy,
    calculate_cascade_velocity
)
from src.api.batch_prediction import (
    submit_batch_prediction,
    get_batch_job_status,
    get_batch_results
)


class TestPhase1Integration:
    """Integration tests for all Phase 1 McKenney-Lacan gaps"""

    @pytest.fixture
    def sample_scenario(self) -> Dict[str, Any]:
        """Create comprehensive test scenario"""
        return {
            "actors": [
                {
                    "actor_id": f"ACTOR-{i:03d}",
                    "name": f"Operator {chr(65+i)}",
                    "properties": {
                        "security_clearance": "SECRET",
                        "team": "Blue Team" if i % 2 == 0 else "Red Team",
                        "location": f"Site {chr(65+i%3)}"
                    }
                }
                for i in range(20)
            ],
            "cascade_root": {
                "event_id": "CASCADE-INT-001",
                "event_type": "apt_attack",
                "source_entity": "EXTERNAL-THREAT",
                "severity": "critical"
            }
        }

    @pytest.mark.asyncio
    async def test_temporal_versioning_cascade_integration(self, sample_scenario):
        """
        Integration Test: Temporal versioning + cascade tracking work together

        Scenario: Track actor property changes during cascade event progression
        Expected: Historical actor states correlate with cascade timeline
        """
        # Create temporal actors
        actors = []
        for actor_data in sample_scenario["actors"][:5]:
            actor = create_temporal_actor(
                actor_id=actor_data["actor_id"],
                name=actor_data["name"],
                properties=actor_data["properties"]
            )
            actors.append(actor)

        # Create cascade root
        cascade_root = create_cascade_event(
            event_id=sample_scenario["cascade_root"]["event_id"],
            event_type=sample_scenario["cascade_root"]["event_type"],
            source_entity=sample_scenario["cascade_root"]["source_entity"],
            timestamp=datetime.now(),
            severity=sample_scenario["cascade_root"]["severity"]
        )

        # Simulate cascade progression with actor property changes
        for i, actor in enumerate(actors):
            # Update actor properties
            update_temporal_property(
                actor_id=actor["actor_id"],
                property_name="security_clearance",
                new_value="TOP SECRET"
            )

            # Create cascade child event
            cascade_child = create_cascade_event(
                event_id=f"CASCADE-INT-001-CHILD-{i}",
                event_type="compromise",
                source_entity=actor["actor_id"],
                timestamp=datetime.now() + timedelta(minutes=i),
                severity="high",
                parent_event_id=cascade_root["event_id"]
            )

            time.sleep(0.1)

        # Query historical state during cascade
        middle_time = datetime.now() + timedelta(minutes=2)
        historical_snapshot = get_point_in_time_snapshot(
            actor_id=actors[2]["actor_id"],
            timestamp=middle_time
        )

        # Verify cascade genealogy
        genealogy = track_cascade_genealogy(cascade_root["event_id"])

        # Integration verification
        assert historical_snapshot["success"] is True
        assert genealogy["success"] is True
        assert len(genealogy["descendants"]) == 5

        # Verify temporal-cascade correlation
        assert historical_snapshot["properties"]["security_clearance"] == "TOP SECRET"

    @pytest.mark.asyncio
    async def test_ews_alerts_trigger_correctly(self, sample_scenario):
        """
        Integration Test: EWS alerts trigger correctly with real metrics

        Scenario: Monitor cascade velocity and trigger EWS alerts
        Expected: Alerts fire when cascade acceleration exceeds threshold
        """
        # Start WebSocket server
        server = await start_websocket_server(port=8766)

        try:
            uri = "ws://localhost:8766"

            # Create cascade
            cascade_root = create_cascade_event(
                event_id="CASCADE-EWS-001",
                event_type="malware_spread",
                source_entity="INFECTED-HOST",
                timestamp=datetime.now(),
                severity="high"
            )

            # Connect to WebSocket
            async with websockets.connect(uri) as websocket:
                # Subscribe to cascade velocity alerts
                subscribe_message = {
                    "type": "subscribe",
                    "entity_id": cascade_root["cascade_id"],
                    "thresholds": {
                        "velocity": 5.0  # events per hour
                    }
                }
                await websocket.send(json.dumps(subscribe_message))
                await websocket.recv()  # Confirmation

                # Create rapid cascade (exceeding threshold)
                for i in range(12):
                    create_cascade_event(
                        event_id=f"CASCADE-EWS-001-CHILD-{i}",
                        event_type="lateral_movement",
                        source_entity=f"HOST-{i:02d}",
                        timestamp=datetime.now() + timedelta(minutes=i*5),
                        severity="medium",
                        parent_event_id=cascade_root["event_id"]
                    )

                # Calculate velocity
                velocity = calculate_cascade_velocity(cascade_root["cascade_id"])

                # Trigger EWS alert if threshold exceeded
                if velocity["events_per_hour"] > 5.0:
                    await trigger_ews_alert(
                        entity_id=cascade_root["cascade_id"],
                        metric="velocity",
                        value=velocity["events_per_hour"],
                        threshold=5.0
                    )

                    # Receive alert
                    alert = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    alert_data = json.loads(alert)

                    assert alert_data["type"] == "ews_alert"
                    assert alert_data["metric"] == "velocity"
                    assert alert_data["value"] > 5.0

        finally:
            server.close()
            await server.wait_closed()

    def test_batch_predictions_use_temporal_data(self, sample_scenario):
        """
        Integration Test: Batch predictions use temporal data

        Scenario: Batch predict using historical actor states
        Expected: Predictions incorporate temporal features
        """
        # Create temporal actors with history
        entities_with_history = []
        for actor_data in sample_scenario["actors"][:10]:
            actor = create_temporal_actor(
                actor_id=actor_data["actor_id"],
                name=actor_data["name"],
                properties=actor_data["properties"]
            )

            # Create property history
            for j in range(3):
                update_temporal_property(
                    actor_id=actor["actor_id"],
                    property_name="security_clearance",
                    new_value=f"LEVEL-{j}"
                )
                time.sleep(0.05)

            # Get temporal features for prediction
            snapshot = get_point_in_time_snapshot(
                actor_id=actor["actor_id"],
                timestamp=datetime.now()
            )

            entities_with_history.append({
                "entity_id": actor["actor_id"],
                "type": "actor",
                "features": snapshot["properties"],
                "temporal_metadata": {
                    "version_count": len(snapshot.get("version_history", [])),
                    "last_modified": snapshot["timestamp"]
                }
            })

        # Submit batch prediction using temporal features
        job = submit_batch_prediction(
            entities=entities_with_history,
            model_id="temporal_risk_predictor",
            prediction_type="risk_assessment",
            use_temporal_features=True
        )

        # Wait for completion
        timeout = 30
        elapsed = 0
        while elapsed < timeout:
            status = get_batch_job_status(job["job_id"])
            if status["status"] == "completed":
                break
            time.sleep(1)
            elapsed += 1

        # Get results
        results = get_batch_results(job["job_id"])

        assert results["success"] is True
        assert len(results["predictions"]) == 10

        # Verify predictions incorporate temporal data
        for prediction in results["predictions"]:
            assert "temporal_features_used" in prediction
            assert prediction["temporal_features_used"] is True

    @pytest.mark.asyncio
    async def test_complete_workflow_integration(self, sample_scenario):
        """
        Integration Test: Complete workflow using all 4 gaps

        Scenario: Full incident response workflow
        1. Temporal actors created
        2. Cascade event detected
        3. EWS alert triggered
        4. Batch prediction for risk assessment

        Expected: All components work together seamlessly
        """
        # Phase 1: Create temporal actors
        actors = []
        for actor_data in sample_scenario["actors"]:
            actor = create_temporal_actor(
                actor_id=actor_data["actor_id"],
                name=actor_data["name"],
                properties=actor_data["properties"]
            )
            actors.append(actor)

        # Phase 2: Detect cascade event
        cascade_root = create_cascade_event(
            event_id="CASCADE-WORKFLOW-001",
            event_type="security_incident",
            source_entity="EXTERNAL-THREAT",
            timestamp=datetime.now(),
            severity="critical"
        )

        # Create cascade children
        for i in range(15):
            create_cascade_event(
                event_id=f"CASCADE-WORKFLOW-001-CHILD-{i}",
                event_type="compromise",
                source_entity=actors[i]["actor_id"],
                timestamp=datetime.now() + timedelta(minutes=i*2),
                severity="high",
                parent_event_id=cascade_root["event_id"]
            )

            # Update actor properties
            update_temporal_property(
                actor_id=actors[i]["actor_id"],
                property_name="security_clearance",
                new_value="COMPROMISED"
            )

        # Phase 3: Calculate cascade velocity and trigger EWS
        velocity = calculate_cascade_velocity(cascade_root["cascade_id"])

        server = await start_websocket_server(port=8767)
        try:
            async with websockets.connect("ws://localhost:8767") as websocket:
                subscribe_message = {
                    "type": "subscribe",
                    "entity_id": cascade_root["cascade_id"],
                    "thresholds": {"velocity": 5.0}
                }
                await websocket.send(json.dumps(subscribe_message))
                await websocket.recv()

                if velocity["events_per_hour"] > 5.0:
                    await trigger_ews_alert(
                        entity_id=cascade_root["cascade_id"],
                        metric="velocity",
                        value=velocity["events_per_hour"],
                        threshold=5.0
                    )

                    alert = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    alert_data = json.loads(alert)
                    assert alert_data["type"] == "ews_alert"
        finally:
            server.close()
            await server.wait_closed()

        # Phase 4: Batch prediction for risk assessment
        compromised_actors = [
            {
                "entity_id": actor["actor_id"],
                "type": "actor",
                "features": get_point_in_time_snapshot(
                    actor["actor_id"], datetime.now()
                )["properties"]
            }
            for actor in actors[:15]
        ]

        job = submit_batch_prediction(
            entities=compromised_actors,
            model_id="incident_risk_predictor",
            prediction_type="cascade_risk"
        )

        # Wait for results
        timeout = 60
        elapsed = 0
        while elapsed < timeout:
            status = get_batch_job_status(job["job_id"])
            if status["status"] == "completed":
                break
            time.sleep(1)
            elapsed += 1

        results = get_batch_results(job["job_id"])

        # Verify complete workflow
        assert results["success"] is True
        assert len(results["predictions"]) == 15

        # All components integrated successfully
        workflow_complete = {
            "temporal_actors_created": len(actors) == 20,
            "cascade_detected": True,
            "ews_alert_triggered": velocity["events_per_hour"] > 5.0,
            "batch_prediction_completed": results["success"]
        }

        assert all(workflow_complete.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
