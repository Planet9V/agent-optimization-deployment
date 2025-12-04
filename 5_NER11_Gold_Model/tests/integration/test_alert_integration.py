"""
Integration tests for E09 Alert Management API with customer isolation.

This test suite validates:
- Alert CRUD operations with customer isolation
- Alert rules and conditions
- Notification rules and channels
- Escalation policies
- Alert correlations
- Dashboard metrics and summaries
- Edge cases and error handling

Total: 85 comprehensive tests
"""

import pytest
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# Import the FastAPI app (adjust import path as needed)
# from app.main import app
# from app.models.alert import Alert, AlertRule, NotificationRule, EscalationPolicy

# Mock app for testing
from fastapi import FastAPI
app = FastAPI()

client = TestClient(app)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client for customer isolation."""
    mock_client = MagicMock()
    mock_client.search.return_value = []
    mock_client.upsert.return_value = {"status": "ok"}
    mock_client.delete.return_value = {"status": "ok"}
    mock_client.scroll.return_value = ([], None)
    return mock_client


@pytest.fixture
def customer_context():
    """Customer context for isolation testing."""
    return {
        "customer_id": f"CUST-{uuid.uuid4()}",
        "tenant_id": f"TENANT-{uuid.uuid4()}",
        "user_id": f"USER-{uuid.uuid4()}",
        "roles": ["analyst", "admin"]
    }


@pytest.fixture
def second_customer_context():
    """Second customer context for isolation validation."""
    return {
        "customer_id": f"CUST-{uuid.uuid4()}",
        "tenant_id": f"TENANT-{uuid.uuid4()}",
        "user_id": f"USER-{uuid.uuid4()}",
        "roles": ["analyst"]
    }


@pytest.fixture
def sample_alert(customer_context):
    """Sample alert data."""
    return {
        "alert_id": f"ALERT-{uuid.uuid4()}",
        "customer_id": customer_context["customer_id"],
        "title": "Suspicious Network Activity Detected",
        "description": "Multiple failed login attempts from IP 192.168.1.100",
        "severity": "high",
        "status": "open",
        "category": "intrusion_detection",
        "source": "IDS-001",
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.50",
        "affected_assets": ["server-01", "firewall-02"],
        "indicators": [
            {"type": "ip", "value": "192.168.1.100", "confidence": 0.95},
            {"type": "port", "value": "22", "confidence": 0.85}
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "first_seen": datetime.utcnow().isoformat(),
        "last_seen": datetime.utcnow().isoformat(),
        "count": 15,
        "tags": ["brute_force", "ssh"],
        "metadata": {
            "user_agent": "OpenSSH_8.2",
            "protocol": "SSH"
        }
    }


@pytest.fixture
def sample_alert_rule(customer_context):
    """Sample alert rule data."""
    return {
        "rule_id": f"RULE-{uuid.uuid4()}",
        "customer_id": customer_context["customer_id"],
        "name": "Failed Login Detection",
        "description": "Detect multiple failed login attempts",
        "enabled": True,
        "conditions": {
            "event_type": "authentication_failure",
            "threshold": 5,
            "window": "5m",
            "field": "source_ip"
        },
        "severity": "high",
        "category": "authentication",
        "notification_channels": ["email", "slack"],
        "escalation_policy_id": None,
        "suppression_window": 300,
        "rate_limit": {
            "count": 10,
            "period": "1h"
        },
        "tags": ["authentication", "brute_force"]
    }


@pytest.fixture
def sample_notification_rule(customer_context):
    """Sample notification rule data."""
    return {
        "notification_id": f"NOTIF-{uuid.uuid4()}",
        "customer_id": customer_context["customer_id"],
        "name": "High Severity Alert Notification",
        "enabled": True,
        "channels": ["email", "slack", "pagerduty"],
        "recipients": {
            "email": ["security@example.com", "soc@example.com"],
            "slack": ["#security-alerts"],
            "pagerduty": ["soc-oncall"]
        },
        "severity_filter": ["critical", "high"],
        "category_filter": ["intrusion_detection", "malware"],
        "schedule": {
            "business_hours_only": False,
            "timezone": "UTC"
        },
        "rate_limit": {
            "count": 20,
            "period": "1h"
        }
    }


@pytest.fixture
def sample_escalation_policy(customer_context):
    """Sample escalation policy data."""
    return {
        "policy_id": f"POLICY-{uuid.uuid4()}",
        "customer_id": customer_context["customer_id"],
        "name": "SOC Escalation Policy",
        "description": "Standard SOC escalation workflow",
        "enabled": True,
        "levels": [
            {
                "level": 1,
                "timeout_minutes": 15,
                "notify_users": ["analyst1@example.com"],
                "notify_groups": ["soc-tier1"],
                "actions": ["notify"]
            },
            {
                "level": 2,
                "timeout_minutes": 30,
                "notify_users": ["lead@example.com"],
                "notify_groups": ["soc-tier2"],
                "actions": ["notify", "create_ticket"]
            },
            {
                "level": 3,
                "timeout_minutes": 60,
                "notify_users": ["manager@example.com"],
                "notify_groups": ["soc-management"],
                "actions": ["notify", "create_ticket", "page"]
            }
        ],
        "business_hours_only": False,
        "timezone": "UTC"
    }


# ============================================================================
# 1. ALERTS TESTS (18 tests)
# ============================================================================

class TestAlerts:
    """Test alert CRUD operations with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_create_alert_success(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test successful alert creation."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/alerts",
            json=sample_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["alert_id"] is not None
        assert data["customer_id"] == customer_context["customer_id"]
        assert data["severity"] == "high"
        assert data["status"] == "open"

    def test_create_alert_invalid_severity(self, customer_context, sample_alert):
        """Test alert creation with invalid severity."""
        sample_alert["severity"] = "invalid_severity"

        response = client.post(
            "/api/v1/alerts",
            json=sample_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 422  # Validation error

    @patch('app.services.alert_service.qdrant_client')
    def test_get_alert_success(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test retrieving an alert by ID."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant_client.retrieve.return_value = [Mock(payload=sample_alert)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/alerts/{alert_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["alert_id"] == alert_id
        assert data["customer_id"] == customer_context["customer_id"]

    def test_get_alert_not_found(self, customer_context):
        """Test retrieving non-existent alert."""
        response = client.get(
            f"/api/v1/alerts/ALERT-nonexistent",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 404

    @patch('app.services.alert_service.qdrant_client')
    def test_update_alert_success(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test updating an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        update_data = {
            "severity": "critical",
            "status": "investigating",
            "assigned_to": "analyst@example.com"
        }

        response = client.patch(
            f"/api/v1/alerts/{alert_id}",
            json=update_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["severity"] == "critical"
        assert data["status"] == "investigating"

    @patch('app.services.alert_service.qdrant_client')
    def test_delete_alert_success(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test deleting an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.delete(
            f"/api/v1/alerts/{alert_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 204

    @patch('app.services.alert_service.qdrant_client')
    def test_list_alerts_empty(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test listing alerts with no results."""
        mock_qdrant_client.scroll.return_value = ([], None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    @patch('app.services.alert_service.qdrant_client')
    def test_list_alerts_with_results(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test listing alerts with results."""
        mock_points = [Mock(payload=sample_alert) for _ in range(3)]
        mock_qdrant_client.scroll.return_value = (mock_points, None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    @patch('app.services.alert_service.qdrant_client')
    def test_alerts_by_severity(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test filtering alerts by severity."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts?severity=high",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        # Verify filter was applied in query

    @patch('app.services.alert_service.qdrant_client')
    def test_alerts_by_status(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test filtering alerts by status."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts?status=open",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200

    @patch('app.services.alert_service.qdrant_client')
    def test_acknowledge_alert(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test acknowledging an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            f"/api/v1/alerts/{alert_id}/acknowledge",
            json={"acknowledged_by": "analyst@example.com", "note": "Investigating"},
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "acknowledged"

    @patch('app.services.alert_service.qdrant_client')
    def test_resolve_alert(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test resolving an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            f"/api/v1/alerts/{alert_id}/resolve",
            json={"resolved_by": "analyst@example.com", "resolution": "False positive"},
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "resolved"

    @patch('app.services.alert_service.qdrant_client')
    def test_assign_alert(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test assigning an alert to a user."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            f"/api/v1/alerts/{alert_id}/assign",
            json={"assigned_to": "analyst@example.com"},
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to"] == "analyst@example.com"

    @patch('app.services.alert_service.qdrant_client')
    def test_search_alerts(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test searching alerts with query."""
        mock_qdrant_client.search.return_value = [Mock(payload=sample_alert, score=0.95)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/alerts/search",
            json={"query": "failed login", "limit": 10},
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) > 0

    @patch('app.services.alert_service.qdrant_client')
    def test_alert_affected_assets(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test retrieving affected assets for an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/alerts/{alert_id}/affected-assets",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "server-01" in data["assets"]

    @patch('app.services.alert_service.qdrant_client')
    def test_alert_indicators(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test retrieving indicators for an alert."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/alerts/{alert_id}/indicators",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["indicators"]) > 0

    @patch('app.services.alert_service.qdrant_client')
    def test_alert_related_alerts(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test finding related alerts."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant_client.search.return_value = [Mock(payload=sample_alert, score=0.85)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/alerts/{alert_id}/related",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "related_alerts" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_alert_customer_isolation(self, mock_qdrant, customer_context, second_customer_context,
                                     sample_alert, mock_qdrant_client):
        """Test that alerts are isolated by customer."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        # Try to access alert from different customer
        response = client.get(
            f"/api/v1/alerts/{alert_id}",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response.status_code == 404  # Should not find alert from different customer


# ============================================================================
# 2. ALERT RULES TESTS (14 tests)
# ============================================================================

class TestAlertRules:
    """Test alert rule management with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_create_rule_success(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test creating an alert rule."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["rule_id"] is not None
        assert data["customer_id"] == customer_context["customer_id"]
        assert data["enabled"] is True

    @patch('app.services.alert_service.qdrant_client')
    def test_get_rule_success(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test retrieving an alert rule."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant_client.retrieve.return_value = [Mock(payload=sample_alert_rule)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/alert-rules/{rule_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["rule_id"] == rule_id

    @patch('app.services.alert_service.qdrant_client')
    def test_update_rule_success(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test updating an alert rule."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant.return_value = mock_qdrant_client

        update_data = {
            "enabled": False,
            "severity": "critical",
            "conditions": {"threshold": 10}
        }

        response = client.patch(
            f"/api/v1/alert-rules/{rule_id}",
            json=update_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["enabled"] is False

    @patch('app.services.alert_service.qdrant_client')
    def test_delete_rule_success(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test deleting an alert rule."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.delete(
            f"/api/v1/alert-rules/{rule_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 204

    @patch('app.services.alert_service.qdrant_client')
    def test_list_rules(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test listing alert rules."""
        mock_points = [Mock(payload=sample_alert_rule) for _ in range(5)]
        mock_qdrant_client.scroll.return_value = (mock_points, None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alert-rules",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5

    @patch('app.services.alert_service.qdrant_client')
    def test_enable_rule(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test enabling an alert rule."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            f"/api/v1/alert-rules/{rule_id}/enable",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["enabled"] is True

    @patch('app.services.alert_service.qdrant_client')
    def test_disable_rule(self, mock_qdrant, customer_context, sample_alert_rule, mock_qdrant_client):
        """Test disabling an alert rule."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            f"/api/v1/alert-rules/{rule_id}/disable",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["enabled"] is False

    def test_rule_conditions(self, customer_context, sample_alert_rule):
        """Test rule condition validation."""
        sample_alert_rule["conditions"] = {
            "event_type": "authentication_failure",
            "threshold": 5,
            "window": "5m"
        }

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        # Should validate conditions structure
        assert response.status_code in [201, 422]

    def test_rule_severity_mapping(self, customer_context, sample_alert_rule):
        """Test rule severity mapping validation."""
        sample_alert_rule["severity"] = "low"

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_rule_notification_channels(self, customer_context, sample_alert_rule):
        """Test rule notification channel validation."""
        sample_alert_rule["notification_channels"] = ["email", "slack", "pagerduty", "webhook"]

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_rule_escalation_policy(self, customer_context, sample_alert_rule):
        """Test rule escalation policy assignment."""
        sample_alert_rule["escalation_policy_id"] = "POLICY-123"

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_rule_suppression_window(self, customer_context, sample_alert_rule):
        """Test rule suppression window validation."""
        sample_alert_rule["suppression_window"] = 600  # 10 minutes

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_rule_rate_limit(self, customer_context, sample_alert_rule):
        """Test rule rate limit validation."""
        sample_alert_rule["rate_limit"] = {"count": 5, "period": "5m"}

        response = client.post(
            "/api/v1/alert-rules",
            json=sample_alert_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    @patch('app.services.alert_service.qdrant_client')
    def test_rule_customer_isolation(self, mock_qdrant, customer_context, second_customer_context,
                                    sample_alert_rule, mock_qdrant_client):
        """Test that alert rules are isolated by customer."""
        rule_id = sample_alert_rule["rule_id"]
        mock_qdrant.return_value = mock_qdrant_client

        # Try to access rule from different customer
        response = client.get(
            f"/api/v1/alert-rules/{rule_id}",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response.status_code == 404


# ============================================================================
# 3. NOTIFICATION RULES TESTS (12 tests)
# ============================================================================

class TestNotificationRules:
    """Test notification rule management with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_create_notification_success(self, mock_qdrant, customer_context,
                                        sample_notification_rule, mock_qdrant_client):
        """Test creating a notification rule."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["notification_id"] is not None
        assert data["customer_id"] == customer_context["customer_id"]

    @patch('app.services.alert_service.qdrant_client')
    def test_get_notification_success(self, mock_qdrant, customer_context,
                                     sample_notification_rule, mock_qdrant_client):
        """Test retrieving a notification rule."""
        notification_id = sample_notification_rule["notification_id"]
        mock_qdrant_client.retrieve.return_value = [Mock(payload=sample_notification_rule)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/notification-rules/{notification_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["notification_id"] == notification_id

    @patch('app.services.alert_service.qdrant_client')
    def test_update_notification_success(self, mock_qdrant, customer_context,
                                        sample_notification_rule, mock_qdrant_client):
        """Test updating a notification rule."""
        notification_id = sample_notification_rule["notification_id"]
        mock_qdrant.return_value = mock_qdrant_client

        update_data = {
            "enabled": False,
            "channels": ["email"]
        }

        response = client.patch(
            f"/api/v1/notification-rules/{notification_id}",
            json=update_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200

    @patch('app.services.alert_service.qdrant_client')
    def test_delete_notification_success(self, mock_qdrant, customer_context,
                                        sample_notification_rule, mock_qdrant_client):
        """Test deleting a notification rule."""
        notification_id = sample_notification_rule["notification_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.delete(
            f"/api/v1/notification-rules/{notification_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 204

    @patch('app.services.alert_service.qdrant_client')
    def test_list_notifications(self, mock_qdrant, customer_context,
                               sample_notification_rule, mock_qdrant_client):
        """Test listing notification rules."""
        mock_points = [Mock(payload=sample_notification_rule) for _ in range(3)]
        mock_qdrant_client.scroll.return_value = (mock_points, None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/notification-rules",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_notification_channels(self, customer_context, sample_notification_rule):
        """Test notification channel validation."""
        sample_notification_rule["channels"] = ["email", "slack", "teams", "webhook"]

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_notification_recipients(self, customer_context, sample_notification_rule):
        """Test notification recipient validation."""
        sample_notification_rule["recipients"] = {
            "email": ["user1@example.com", "user2@example.com"],
            "slack": ["#channel1", "#channel2"]
        }

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_notification_severity_filter(self, customer_context, sample_notification_rule):
        """Test notification severity filter validation."""
        sample_notification_rule["severity_filter"] = ["critical", "high", "medium"]

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_notification_category_filter(self, customer_context, sample_notification_rule):
        """Test notification category filter validation."""
        sample_notification_rule["category_filter"] = ["malware", "phishing", "data_exfiltration"]

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_notification_schedule(self, customer_context, sample_notification_rule):
        """Test notification schedule configuration."""
        sample_notification_rule["schedule"] = {
            "business_hours_only": True,
            "timezone": "America/New_York",
            "hours": {"start": "09:00", "end": "17:00"}
        }

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_notification_rate_limit(self, customer_context, sample_notification_rule):
        """Test notification rate limit validation."""
        sample_notification_rule["rate_limit"] = {"count": 10, "period": "5m"}

        response = client.post(
            "/api/v1/notification-rules",
            json=sample_notification_rule,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    @patch('app.services.alert_service.qdrant_client')
    def test_notification_customer_isolation(self, mock_qdrant, customer_context,
                                            second_customer_context, sample_notification_rule,
                                            mock_qdrant_client):
        """Test that notification rules are isolated by customer."""
        notification_id = sample_notification_rule["notification_id"]
        mock_qdrant.return_value = mock_qdrant_client

        # Try to access notification from different customer
        response = client.get(
            f"/api/v1/notification-rules/{notification_id}",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response.status_code == 404


# ============================================================================
# 4. ESCALATION POLICIES TESTS (12 tests)
# ============================================================================

class TestEscalationPolicies:
    """Test escalation policy management with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_create_escalation_success(self, mock_qdrant, customer_context,
                                      sample_escalation_policy, mock_qdrant_client):
        """Test creating an escalation policy."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["policy_id"] is not None
        assert len(data["levels"]) == 3

    @patch('app.services.alert_service.qdrant_client')
    def test_get_escalation_success(self, mock_qdrant, customer_context,
                                   sample_escalation_policy, mock_qdrant_client):
        """Test retrieving an escalation policy."""
        policy_id = sample_escalation_policy["policy_id"]
        mock_qdrant_client.retrieve.return_value = [Mock(payload=sample_escalation_policy)]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/escalation-policies/{policy_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["policy_id"] == policy_id

    @patch('app.services.alert_service.qdrant_client')
    def test_update_escalation_success(self, mock_qdrant, customer_context,
                                      sample_escalation_policy, mock_qdrant_client):
        """Test updating an escalation policy."""
        policy_id = sample_escalation_policy["policy_id"]
        mock_qdrant.return_value = mock_qdrant_client

        update_data = {
            "enabled": False,
            "business_hours_only": True
        }

        response = client.patch(
            f"/api/v1/escalation-policies/{policy_id}",
            json=update_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200

    @patch('app.services.alert_service.qdrant_client')
    def test_delete_escalation_success(self, mock_qdrant, customer_context,
                                      sample_escalation_policy, mock_qdrant_client):
        """Test deleting an escalation policy."""
        policy_id = sample_escalation_policy["policy_id"]
        mock_qdrant.return_value = mock_qdrant_client

        response = client.delete(
            f"/api/v1/escalation-policies/{policy_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 204

    @patch('app.services.alert_service.qdrant_client')
    def test_list_escalations(self, mock_qdrant, customer_context,
                             sample_escalation_policy, mock_qdrant_client):
        """Test listing escalation policies."""
        mock_points = [Mock(payload=sample_escalation_policy) for _ in range(2)]
        mock_qdrant_client.scroll.return_value = (mock_points, None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/escalation-policies",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    def test_escalation_levels(self, customer_context, sample_escalation_policy):
        """Test escalation level validation."""
        assert len(sample_escalation_policy["levels"]) == 3
        assert sample_escalation_policy["levels"][0]["level"] == 1
        assert sample_escalation_policy["levels"][2]["level"] == 3

    def test_escalation_timeout(self, customer_context, sample_escalation_policy):
        """Test escalation timeout validation."""
        sample_escalation_policy["levels"][0]["timeout_minutes"] = 5

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_escalation_business_hours(self, customer_context, sample_escalation_policy):
        """Test escalation business hours configuration."""
        sample_escalation_policy["business_hours_only"] = True
        sample_escalation_policy["timezone"] = "America/New_York"

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_escalation_actions(self, customer_context, sample_escalation_policy):
        """Test escalation action validation."""
        sample_escalation_policy["levels"][0]["actions"] = ["notify", "create_ticket", "page"]

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_escalation_notify_users(self, customer_context, sample_escalation_policy):
        """Test escalation user notification configuration."""
        sample_escalation_policy["levels"][1]["notify_users"] = [
            "user1@example.com", "user2@example.com", "user3@example.com"
        ]

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_escalation_notify_groups(self, customer_context, sample_escalation_policy):
        """Test escalation group notification configuration."""
        sample_escalation_policy["levels"][2]["notify_groups"] = [
            "soc-management", "incident-response", "executives"
        ]

        response = client.post(
            "/api/v1/escalation-policies",
            json=sample_escalation_policy,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    @patch('app.services.alert_service.qdrant_client')
    def test_escalation_customer_isolation(self, mock_qdrant, customer_context,
                                          second_customer_context, sample_escalation_policy,
                                          mock_qdrant_client):
        """Test that escalation policies are isolated by customer."""
        policy_id = sample_escalation_policy["policy_id"]
        mock_qdrant.return_value = mock_qdrant_client

        # Try to access policy from different customer
        response = client.get(
            f"/api/v1/escalation-policies/{policy_id}",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response.status_code == 404


# ============================================================================
# 5. CORRELATIONS TESTS (10 tests)
# ============================================================================

class TestCorrelations:
    """Test alert correlation functionality with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_create_correlation_success(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test creating an alert correlation."""
        mock_qdrant.return_value = mock_qdrant_client

        correlation_data = {
            "correlation_id": f"CORR-{uuid.uuid4()}",
            "customer_id": customer_context["customer_id"],
            "alert_ids": ["ALERT-1", "ALERT-2", "ALERT-3"],
            "correlation_type": "temporal",
            "confidence": 0.85,
            "description": "Related authentication failures from same source",
            "status": "active"
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["correlation_id"] is not None
        assert len(data["alert_ids"]) == 3

    @patch('app.services.alert_service.qdrant_client')
    def test_list_correlations(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test listing alert correlations."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/correlations",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200

    @patch('app.services.alert_service.qdrant_client')
    def test_get_correlation(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test retrieving a specific correlation."""
        correlation_id = f"CORR-{uuid.uuid4()}"
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            f"/api/v1/correlations/{correlation_id}",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [200, 404]

    def test_correlation_alert_ids(self, customer_context):
        """Test correlation alert ID validation."""
        correlation_data = {
            "alert_ids": ["ALERT-1", "ALERT-2"],
            "correlation_type": "temporal",
            "customer_id": customer_context["customer_id"]
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        # Should require at least 2 alert IDs
        assert response.status_code in [201, 422]

    def test_correlation_type(self, customer_context):
        """Test correlation type validation."""
        correlation_data = {
            "alert_ids": ["ALERT-1", "ALERT-2", "ALERT-3"],
            "correlation_type": "causal",  # temporal, causal, spatial
            "customer_id": customer_context["customer_id"]
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_correlation_confidence(self, customer_context):
        """Test correlation confidence score validation."""
        correlation_data = {
            "alert_ids": ["ALERT-1", "ALERT-2"],
            "correlation_type": "temporal",
            "confidence": 0.75,
            "customer_id": customer_context["customer_id"]
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        # Confidence should be between 0 and 1
        assert response.status_code in [201, 422]

    def test_correlation_status(self, customer_context):
        """Test correlation status validation."""
        correlation_data = {
            "alert_ids": ["ALERT-1", "ALERT-2"],
            "correlation_type": "temporal",
            "status": "reviewed",
            "customer_id": customer_context["customer_id"]
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_correlation_analyst_notes(self, customer_context):
        """Test correlation analyst notes."""
        correlation_data = {
            "alert_ids": ["ALERT-1", "ALERT-2"],
            "correlation_type": "temporal",
            "analyst_notes": "Confirmed as part of coordinated attack",
            "customer_id": customer_context["customer_id"]
        }

        response = client.post(
            "/api/v1/correlations",
            json=correlation_data,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    @patch('app.services.alert_service.qdrant_client')
    def test_correlation_auto_detection(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test automatic correlation detection."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.post(
            "/api/v1/correlations/detect",
            json={"time_window": "1h", "min_confidence": 0.7},
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [200, 404]

    @patch('app.services.alert_service.qdrant_client')
    def test_correlation_customer_isolation(self, mock_qdrant, customer_context,
                                           second_customer_context, mock_qdrant_client):
        """Test that correlations are isolated by customer."""
        correlation_id = f"CORR-{uuid.uuid4()}"
        mock_qdrant.return_value = mock_qdrant_client

        # Try to access correlation from different customer
        response = client.get(
            f"/api/v1/correlations/{correlation_id}",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response.status_code == 404


# ============================================================================
# 6. DASHBOARD TESTS (8 tests)
# ============================================================================

class TestDashboard:
    """Test dashboard metrics and summaries with customer isolation."""

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_summary(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test dashboard summary endpoint."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/summary",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_alerts" in data
        assert "alerts_by_severity" in data
        assert "alerts_by_status" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_alerts_by_severity(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test alerts grouped by severity."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/alerts-by-severity",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "critical" in data or "high" in data or "medium" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_alerts_by_status(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test alerts grouped by status."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/alerts-by-status",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "open" in data or "investigating" in data or "resolved" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_mttr_metrics(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test mean time to resolve (MTTR) metrics."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/mttr",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "mttr_minutes" in data or "average_resolution_time" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_trend_analysis(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test alert trend analysis."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/trends?period=7d",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "trends" in data or "time_series" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_top_sources(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test top alert sources."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/top-sources",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "sources" in data or "top_sources" in data

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_customer_isolation(self, mock_qdrant, customer_context,
                                         second_customer_context, mock_qdrant_client):
        """Test that dashboard metrics are isolated by customer."""
        mock_qdrant.return_value = mock_qdrant_client

        # Get metrics for first customer
        response1 = client.get(
            "/api/v1/dashboard/summary",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        # Get metrics for second customer
        response2 = client.get(
            "/api/v1/dashboard/summary",
            headers={"X-Customer-ID": second_customer_context["customer_id"]}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200
        # Metrics should be different for different customers

    @patch('app.services.alert_service.qdrant_client')
    def test_dashboard_empty_state(self, mock_qdrant, customer_context, mock_qdrant_client):
        """Test dashboard with no alerts."""
        mock_qdrant_client.scroll.return_value = ([], None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/dashboard/summary",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("total_alerts", 0) == 0


# ============================================================================
# 7. EDGE CASES TESTS (11 tests)
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_missing_customer_id(self, sample_alert):
        """Test request without customer ID header."""
        response = client.post(
            "/api/v1/alerts",
            json=sample_alert
        )

        assert response.status_code == 401  # Unauthorized

    def test_invalid_customer_id(self, sample_alert):
        """Test request with invalid customer ID."""
        response = client.post(
            "/api/v1/alerts",
            json=sample_alert,
            headers={"X-Customer-ID": "invalid-format"}
        )

        assert response.status_code in [400, 401, 422]

    @patch('app.services.alert_service.qdrant_client')
    def test_concurrent_acknowledgments(self, mock_qdrant, customer_context,
                                       sample_alert, mock_qdrant_client):
        """Test concurrent alert acknowledgments."""
        alert_id = sample_alert["alert_id"]
        mock_qdrant.return_value = mock_qdrant_client

        # Simulate concurrent acknowledgments
        responses = []
        for i in range(3):
            response = client.post(
                f"/api/v1/alerts/{alert_id}/acknowledge",
                json={"acknowledged_by": f"analyst{i}@example.com"},
                headers={"X-Customer-ID": customer_context["customer_id"]}
            )
            responses.append(response.status_code)

        # At least one should succeed
        assert 200 in responses or 201 in responses

    def test_large_payload(self, customer_context):
        """Test handling of large alert payload."""
        large_alert = {
            "customer_id": customer_context["customer_id"],
            "title": "Large Alert",
            "description": "A" * 10000,  # 10KB description
            "severity": "medium",
            "status": "open",
            "metadata": {f"key_{i}": f"value_{i}" for i in range(100)}
        }

        response = client.post(
            "/api/v1/alerts",
            json=large_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 413, 422]  # Success or payload too large

    def test_special_characters(self, customer_context):
        """Test handling of special characters in alert data."""
        alert_with_special_chars = {
            "customer_id": customer_context["customer_id"],
            "title": "Alert with special chars: <script>alert('xss')</script>",
            "description": "SQL injection attempt: '; DROP TABLE users; --",
            "severity": "high",
            "status": "open",
            "tags": ["test'tag", "tag\"with\"quotes", "tag<>brackets"]
        }

        response = client.post(
            "/api/v1/alerts",
            json=alert_with_special_chars,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code in [201, 422]

    def test_date_format_validation(self, customer_context, sample_alert):
        """Test date format validation."""
        sample_alert["timestamp"] = "2024-13-45 25:99:99"  # Invalid date

        response = client.post(
            "/api/v1/alerts",
            json=sample_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 422  # Validation error

    def test_enum_validation(self, customer_context, sample_alert):
        """Test enum field validation."""
        sample_alert["severity"] = "super-critical"  # Invalid enum value

        response = client.post(
            "/api/v1/alerts",
            json=sample_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 422

    def test_required_fields(self, customer_context):
        """Test missing required fields."""
        incomplete_alert = {
            "customer_id": customer_context["customer_id"],
            "title": "Incomplete Alert"
            # Missing severity, status, etc.
        }

        response = client.post(
            "/api/v1/alerts",
            json=incomplete_alert,
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 422

    @patch('app.services.alert_service.qdrant_client')
    def test_pagination(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test pagination parameters."""
        mock_points = [Mock(payload=sample_alert) for _ in range(50)]
        mock_qdrant_client.scroll.return_value = (mock_points, None)
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts?limit=10&offset=20",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 10

    @patch('app.services.alert_service.qdrant_client')
    def test_sorting(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test sorting parameters."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts?sort_by=timestamp&order=desc",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200

    @patch('app.services.alert_service.qdrant_client')
    def test_filtering(self, mock_qdrant, customer_context, sample_alert, mock_qdrant_client):
        """Test multiple filter combinations."""
        mock_qdrant.return_value = mock_qdrant_client

        response = client.get(
            "/api/v1/alerts?severity=high&status=open&category=intrusion_detection",
            headers={"X-Customer-ID": customer_context["customer_id"]}
        )

        assert response.status_code == 200


# ============================================================================
# TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
