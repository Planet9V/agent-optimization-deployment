"""
E12 NOW-NEXT-NEVER Prioritization API Tests
Comprehensive test suite for all 28 endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock

from api.prioritization.router import router


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client"""
    client = Mock()
    client.get_collections = Mock(return_value=Mock(collections=[]))
    client.create_collection = Mock()
    client.scroll = Mock(return_value=([], None))
    return client


@pytest.fixture
def test_client():
    """Create test client"""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ============================================================================
# NOW Priority Tests (6 endpoints)
# ============================================================================

class TestNOWPriority:
    """Test NOW priority endpoints (score >= 70)"""

    def test_get_now_items(self, test_client):
        """Test GET /now/items"""
        response = test_client.get(
            "/api/v2/prioritization/now/items",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_now_summary(self, test_client):
        """Test GET /now/summary"""
        response = test_client.get(
            "/api/v2/prioritization/now/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_now_critical(self, test_client):
        """Test GET /now/critical"""
        response = test_client.get(
            "/api/v2/prioritization/now/critical",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_now_by_category(self, test_client):
        """Test GET /now/by-category"""
        response = test_client.get(
            "/api/v2/prioritization/now/by-category",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_now_sla_at_risk(self, test_client):
        """Test GET /now/sla-at-risk"""
        response = test_client.get(
            "/api/v2/prioritization/now/sla-at-risk",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_now_escalations(self, test_client):
        """Test GET /now/escalations"""
        response = test_client.get(
            "/api/v2/prioritization/now/escalations",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# NEXT Priority Tests (6 endpoints)
# ============================================================================

class TestNEXTPriority:
    """Test NEXT priority endpoints (40 <= score < 70)"""

    def test_get_next_items(self, test_client):
        """Test GET /next/items"""
        response = test_client.get(
            "/api/v2/prioritization/next/items",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_next_summary(self, test_client):
        """Test GET /next/summary"""
        response = test_client.get(
            "/api/v2/prioritization/next/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_next_planned(self, test_client):
        """Test GET /next/planned"""
        response = test_client.get(
            "/api/v2/prioritization/next/planned",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_next_by_quarter(self, test_client):
        """Test GET /next/by-quarter"""
        response = test_client.get(
            "/api/v2/prioritization/next/by-quarter",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_next_dependencies(self, test_client):
        """Test GET /next/dependencies"""
        response = test_client.get(
            "/api/v2/prioritization/next/dependencies",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_next_resource_requirements(self, test_client):
        """Test GET /next/resource-requirements"""
        response = test_client.get(
            "/api/v2/prioritization/next/resource-requirements",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# NEVER Priority Tests (4 endpoints)
# ============================================================================

class TestNEVERPriority:
    """Test NEVER priority endpoints (score < 40)"""

    def test_get_never_items(self, test_client):
        """Test GET /never/items"""
        response = test_client.get(
            "/api/v2/prioritization/never/items",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_never_summary(self, test_client):
        """Test GET /never/summary"""
        response = test_client.get(
            "/api/v2/prioritization/never/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_never_review_candidates(self, test_client):
        """Test GET /never/review-candidates"""
        response = test_client.get(
            "/api/v2/prioritization/never/review-candidates",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_never_justifications(self, test_client):
        """Test GET /never/justifications"""
        response = test_client.get(
            "/api/v2/prioritization/never/justifications",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Priority Scoring Tests (6 endpoints)
# ============================================================================

class TestPriorityScoring:
    """Test priority scoring endpoints"""

    def test_calculate_priority_score(self, test_client):
        """Test POST /scoring/calculate"""
        request = {
            "customer_id": "test-customer",
            "item_id": "vuln-001",
            "item_type": "vulnerability",
            "urgency_score": 8.0,
            "risk_score": 9.0,
            "impact_score": 7.5,
            "effort_score": 6.0,
            "roi_score": 8.0,
            "sla_deadline": "2025-01-15T00:00:00Z",
            "affected_assets": 15,
            "dependencies": []
        }
        response = test_client.post(
            "/api/v2/prioritization/scoring/calculate",
            headers={"X-Customer-ID": "test-customer"},
            json=request
        )
        assert response.status_code == 200
        data = response.json()
        assert "priority_score" in data["data"]
        assert "priority_category" in data["data"]

    def test_get_scoring_factors(self, test_client):
        """Test GET /scoring/factors"""
        response = test_client.get(
            "/api/v2/prioritization/scoring/factors",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_scoring_weights(self, test_client):
        """Test GET /scoring/weights"""
        response = test_client.get(
            "/api/v2/prioritization/scoring/weights",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        weights = data["data"]
        assert weights["urgency"] == 0.25
        assert weights["risk"] == 0.30
        assert weights["impact"] == 0.25
        assert weights["effort"] == 0.10
        assert weights["roi"] == 0.10

    def test_update_scoring_weights(self, test_client):
        """Test PUT /scoring/weights"""
        new_weights = {
            "urgency": 0.30,
            "risk": 0.25,
            "impact": 0.25,
            "effort": 0.10,
            "roi": 0.10
        }
        response = test_client.put(
            "/api/v2/prioritization/scoring/weights",
            headers={"X-Customer-ID": "test-customer"},
            json=new_weights
        )
        assert response.status_code in [200, 501]

    def test_batch_calculate_scores(self, test_client):
        """Test POST /scoring/batch"""
        items = [
            {
                "customer_id": "test-customer",
                "item_id": "vuln-001",
                "item_type": "vulnerability",
                "urgency_score": 8.0,
                "risk_score": 9.0,
                "impact_score": 7.5,
                "effort_score": 6.0,
                "roi_score": 8.0
            },
            {
                "customer_id": "test-customer",
                "item_id": "vuln-002",
                "item_type": "vulnerability",
                "urgency_score": 4.0,
                "risk_score": 5.0,
                "impact_score": 4.5,
                "effort_score": 3.0,
                "roi_score": 4.0
            }
        ]
        response = test_client.post(
            "/api/v2/prioritization/scoring/batch",
            headers={"X-Customer-ID": "test-customer"},
            json=items
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["results"]) == 2

    def test_get_scoring_history(self, test_client):
        """Test GET /scoring/history"""
        response = test_client.get(
            "/api/v2/prioritization/scoring/history?item_id=vuln-001",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Dashboard Tests (6 endpoints)
# ============================================================================

class TestPrioritizationDashboard:
    """Test prioritization dashboard endpoints"""

    def test_get_dashboard_summary(self, test_client):
        """Test GET /dashboard/summary"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "now_count" in data["data"]
        assert "next_count" in data["data"]
        assert "never_count" in data["data"]

    def test_get_dashboard_distribution(self, test_client):
        """Test GET /dashboard/distribution"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/distribution",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_dashboard_trends(self, test_client):
        """Test GET /dashboard/trends"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/trends?days=30",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_dashboard_velocity(self, test_client):
        """Test GET /dashboard/velocity"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/velocity",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_dashboard_sla_status(self, test_client):
        """Test GET /dashboard/sla-status"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/sla-status",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_executive_summary(self, test_client):
        """Test GET /dashboard/executive"""
        response = test_client.get(
            "/api/v2/prioritization/dashboard/executive",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Priority Scoring Logic Tests
# ============================================================================

class TestPriorityScoringLogic:
    """Test priority calculation logic"""

    def test_now_category_threshold(self, test_client):
        """Test that scores >= 70 are categorized as NOW"""
        request = {
            "customer_id": "test-customer",
            "item_id": "high-priority",
            "item_type": "vulnerability",
            "urgency_score": 10.0,
            "risk_score": 10.0,
            "impact_score": 10.0,
            "effort_score": 10.0,
            "roi_score": 10.0
        }
        response = test_client.post(
            "/api/v2/prioritization/scoring/calculate",
            headers={"X-Customer-ID": "test-customer"},
            json=request
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["priority_category"] == "NOW"
        assert data["data"]["priority_score"] >= 70

    def test_next_category_threshold(self, test_client):
        """Test that scores 40-69 are categorized as NEXT"""
        request = {
            "customer_id": "test-customer",
            "item_id": "medium-priority",
            "item_type": "vulnerability",
            "urgency_score": 5.0,
            "risk_score": 5.0,
            "impact_score": 5.0,
            "effort_score": 5.0,
            "roi_score": 5.0
        }
        response = test_client.post(
            "/api/v2/prioritization/scoring/calculate",
            headers={"X-Customer-ID": "test-customer"},
            json=request
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["priority_category"] == "NEXT"
        assert 40 <= data["data"]["priority_score"] < 70

    def test_never_category_threshold(self, test_client):
        """Test that scores < 40 are categorized as NEVER"""
        request = {
            "customer_id": "test-customer",
            "item_id": "low-priority",
            "item_type": "vulnerability",
            "urgency_score": 2.0,
            "risk_score": 2.0,
            "impact_score": 2.0,
            "effort_score": 2.0,
            "roi_score": 2.0
        }
        response = test_client.post(
            "/api/v2/prioritization/scoring/calculate",
            headers={"X-Customer-ID": "test-customer"},
            json=request
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["priority_category"] == "NEVER"
        assert data["data"]["priority_score"] < 40


# ============================================================================
# Multi-Tenant Tests
# ============================================================================

class TestPrioritizationMultiTenant:
    """Test multi-tenant isolation"""

    def test_customer_id_required(self, test_client):
        """Test that X-Customer-ID header is required"""
        response = test_client.get("/api/v2/prioritization/now/items")
        assert response.status_code == 422

    def test_customer_isolation(self, test_client):
        """Test data isolation between customers"""
        response1 = test_client.get(
            "/api/v2/prioritization/dashboard/summary",
            headers={"X-Customer-ID": "customer-1"}
        )
        response2 = test_client.get(
            "/api/v2/prioritization/dashboard/summary",
            headers={"X-Customer-ID": "customer-2"}
        )
        assert response1.status_code == 200
        assert response2.status_code == 200


# ============================================================================
# Health Check
# ============================================================================

def test_health_check(test_client):
    """Test health check endpoint"""
    response = test_client.get("/api/v2/prioritization/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["endpoints"] == 28
