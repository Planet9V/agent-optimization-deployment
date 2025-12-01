"""
ML-005 WebSocket EWS Tests
Test suite for WebSocket early warning system and real-time alerts
"""

import pytest
import asyncio
import websockets
import json
from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.websocket_ews import (
    start_websocket_server,
    subscribe_to_ews,
    trigger_ews_alert,
    calculate_ews_metrics
)


class TestML005WebSocketEWS:
    """Test suite for ML-005 WebSocket EWS functionality"""

    @pytest.fixture
    async def websocket_server(self):
        """Start WebSocket server for testing"""
        server = await start_websocket_server(port=8765)
        yield server
        server.close()
        await server.wait_closed()

    @pytest.fixture
    def sample_entity(self) -> Dict[str, Any]:
        """Create sample entity for EWS monitoring"""
        return {
            "entity_id": "NET-001",
            "type": "network",
            "metrics": {
                "autocorrelation": 0.85,
                "variance": 0.45,
                "recovery_time": 120
            }
        }

    @pytest.mark.asyncio
    async def test_websocket_connection(self, websocket_server):
        """
        Test: Connect to WebSocket
        Expected: Successful connection established
        """
        uri = "ws://localhost:8765"

        async with websockets.connect(uri) as websocket:
            # Send ping
            await websocket.send(json.dumps({"type": "ping"}))

            # Receive pong
            response = await websocket.recv()
            data = json.loads(response)

            assert data["type"] == "pong"
            assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_subscribe_to_ews(self, websocket_server, sample_entity):
        """
        Test: Subscribe to EWS alerts
        Expected: Subscription confirmed
        """
        uri = "ws://localhost:8765"

        async with websockets.connect(uri) as websocket:
            # Subscribe to entity
            subscribe_message = {
                "type": "subscribe",
                "entity_id": sample_entity["entity_id"],
                "thresholds": {
                    "autocorrelation": 0.9,
                    "variance": 0.5,
                    "recovery_time": 150
                }
            }

            await websocket.send(json.dumps(subscribe_message))

            # Receive confirmation
            response = await websocket.recv()
            data = json.loads(response)

            assert data["type"] == "subscription_confirmed"
            assert data["entity_id"] == sample_entity["entity_id"]

    @pytest.mark.asyncio
    async def test_ews_alert_trigger(self, websocket_server, sample_entity):
        """
        Test: Receive alert when threshold breached
        Expected: Alert received with breach details
        """
        uri = "ws://localhost:8765"

        async with websockets.connect(uri) as websocket:
            # Subscribe
            subscribe_message = {
                "type": "subscribe",
                "entity_id": sample_entity["entity_id"],
                "thresholds": {
                    "autocorrelation": 0.8  # Set threshold below current value
                }
            }
            await websocket.send(json.dumps(subscribe_message))
            await websocket.recv()  # Confirmation

            # Trigger alert by updating metrics
            await trigger_ews_alert(
                entity_id=sample_entity["entity_id"],
                metric="autocorrelation",
                value=0.95,  # Above threshold
                threshold=0.8
            )

            # Receive alert
            alert = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            alert_data = json.loads(alert)

            assert alert_data["type"] == "ews_alert"
            assert alert_data["entity_id"] == sample_entity["entity_id"]
            assert alert_data["metric"] == "autocorrelation"
            assert alert_data["value"] == 0.95
            assert alert_data["threshold"] == 0.8
            assert "severity" in alert_data

    @pytest.mark.asyncio
    async def test_alert_latency(self, websocket_server, sample_entity):
        """
        Test: <1 second latency for alerts
        Expected: Alert received within 1000ms of threshold breach
        """
        uri = "ws://localhost:8765"

        async with websockets.connect(uri) as websocket:
            # Subscribe
            subscribe_message = {
                "type": "subscribe",
                "entity_id": sample_entity["entity_id"],
                "thresholds": {"autocorrelation": 0.8}
            }
            await websocket.send(json.dumps(subscribe_message))
            await websocket.recv()

            # Trigger alert and measure latency
            import time
            start_time = time.time()

            await trigger_ews_alert(
                entity_id=sample_entity["entity_id"],
                metric="autocorrelation",
                value=0.95,
                threshold=0.8
            )

            alert = await websocket.recv()
            latency_ms = (time.time() - start_time) * 1000

            assert latency_ms < 1000, f"Latency {latency_ms}ms exceeds 1000ms threshold"

    @pytest.mark.asyncio
    async def test_multiple_subscriptions(self, websocket_server):
        """
        Test: Multiple entity subscriptions
        Expected: Alerts for all subscribed entities
        """
        uri = "ws://localhost:8765"

        entities = [f"NET-{i:03d}" for i in range(5)]

        async with websockets.connect(uri) as websocket:
            # Subscribe to multiple entities
            for entity_id in entities:
                subscribe_message = {
                    "type": "subscribe",
                    "entity_id": entity_id,
                    "thresholds": {"autocorrelation": 0.8}
                }
                await websocket.send(json.dumps(subscribe_message))
                await websocket.recv()

            # Trigger alerts for all entities
            alert_tasks = [
                trigger_ews_alert(entity_id, "autocorrelation", 0.95, 0.8)
                for entity_id in entities
            ]
            await asyncio.gather(*alert_tasks)

            # Receive all alerts
            received_alerts = []
            for _ in range(len(entities)):
                alert = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                received_alerts.append(json.loads(alert))

            received_entity_ids = {alert["entity_id"] for alert in received_alerts}
            assert received_entity_ids == set(entities)

    @pytest.mark.asyncio
    async def test_ews_metrics_calculation(self, sample_entity):
        """
        Test: EWS metrics calculation accuracy
        Expected: Correct autocorrelation, variance, recovery time
        """
        time_series = [0.1, 0.3, 0.5, 0.7, 0.9, 0.85, 0.82, 0.78, 0.75]

        metrics = calculate_ews_metrics(time_series)

        assert "autocorrelation" in metrics
        assert "variance" in metrics
        assert "recovery_time" in metrics

        assert 0 <= metrics["autocorrelation"] <= 1
        assert metrics["variance"] > 0
        assert metrics["recovery_time"] >= 0

    @pytest.mark.asyncio
    async def test_reconnection_handling(self, websocket_server, sample_entity):
        """
        Test: WebSocket reconnection
        Expected: Subscriptions persist after reconnection
        """
        uri = "ws://localhost:8765"

        # Initial connection
        websocket1 = await websockets.connect(uri)
        subscribe_message = {
            "type": "subscribe",
            "entity_id": sample_entity["entity_id"],
            "thresholds": {"autocorrelation": 0.8}
        }
        await websocket1.send(json.dumps(subscribe_message))
        await websocket1.recv()
        await websocket1.close()

        # Reconnect
        websocket2 = await websockets.connect(uri)

        # Trigger alert
        await trigger_ews_alert(
            sample_entity["entity_id"], "autocorrelation", 0.95, 0.8
        )

        # Should receive alert on new connection
        try:
            alert = await asyncio.wait_for(websocket2.recv(), timeout=2.0)
            alert_data = json.loads(alert)
            assert alert_data["entity_id"] == sample_entity["entity_id"]
        finally:
            await websocket2.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
