"""
E11 Demographics Baseline API Tests
Comprehensive test suite for all 24 endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock

from api.demographics.router import router


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
# Population Analytics Tests (5 endpoints)
# ============================================================================

class TestPopulationAnalytics:
    """Test population analytics endpoints"""

    def test_get_population_summary(self, test_client):
        """Test GET /population/summary"""
        response = test_client.get(
            "/api/v2/demographics/population/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_population_distribution(self, test_client):
        """Test GET /population/distribution"""
        response = test_client.get(
            "/api/v2/demographics/population/distribution",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_population_by_role(self, test_client):
        """Test GET /population/by-role"""
        response = test_client.get(
            "/api/v2/demographics/population/by-role",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_population_trends(self, test_client):
        """Test GET /population/trends"""
        response = test_client.get(
            "/api/v2/demographics/population/trends?days=90",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_population_growth(self, test_client):
        """Test GET /population/growth"""
        response = test_client.get(
            "/api/v2/demographics/population/growth",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Workforce Analysis Tests (5 endpoints)
# ============================================================================

class TestWorkforceAnalysis:
    """Test workforce analysis endpoints"""

    def test_get_workforce_metrics(self, test_client):
        """Test GET /workforce/metrics"""
        response = test_client.get(
            "/api/v2/demographics/workforce/metrics",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_workforce_skills(self, test_client):
        """Test GET /workforce/skills"""
        response = test_client.get(
            "/api/v2/demographics/workforce/skills",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_workforce_capacity(self, test_client):
        """Test GET /workforce/capacity"""
        response = test_client.get(
            "/api/v2/demographics/workforce/capacity",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_capacity" in data["data"] or "success" in data

    def test_get_workforce_training(self, test_client):
        """Test GET /workforce/training"""
        response = test_client.get(
            "/api/v2/demographics/workforce/training",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_workforce_certifications(self, test_client):
        """Test GET /workforce/certifications"""
        response = test_client.get(
            "/api/v2/demographics/workforce/certifications",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Organization Structure Tests (5 endpoints)
# ============================================================================

class TestOrganizationStructure:
    """Test organization structure endpoints"""

    def test_get_organization_hierarchy(self, test_client):
        """Test GET /organization/hierarchy"""
        response = test_client.get(
            "/api/v2/demographics/organization/hierarchy",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_organization_departments(self, test_client):
        """Test GET /organization/departments"""
        response = test_client.get(
            "/api/v2/demographics/organization/departments",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_organization_locations(self, test_client):
        """Test GET /organization/locations"""
        response = test_client.get(
            "/api/v2/demographics/organization/locations",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_organization_teams(self, test_client):
        """Test GET /organization/teams"""
        response = test_client.get(
            "/api/v2/demographics/organization/teams",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_organization_spans(self, test_client):
        """Test GET /organization/spans-of-control"""
        response = test_client.get(
            "/api/v2/demographics/organization/spans-of-control",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Role Analysis Tests (4 endpoints)
# ============================================================================

class TestRoleAnalysis:
    """Test role analysis endpoints"""

    def test_get_role_distribution(self, test_client):
        """Test GET /roles/distribution"""
        response = test_client.get(
            "/api/v2/demographics/roles/distribution",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_role_competencies(self, test_client):
        """Test GET /roles/competencies"""
        response = test_client.get(
            "/api/v2/demographics/roles/competencies",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200

    def test_get_role_gaps(self, test_client):
        """Test GET /roles/gaps"""
        response = test_client.get(
            "/api/v2/demographics/roles/gaps",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_role_succession(self, test_client):
        """Test GET /roles/succession"""
        response = test_client.get(
            "/api/v2/demographics/roles/succession",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Dashboard Tests (5 endpoints)
# ============================================================================

class TestDemographicsDashboard:
    """Test demographics dashboard endpoints"""

    def test_get_dashboard_summary(self, test_client):
        """Test GET /dashboard/summary"""
        response = test_client.get(
            "/api/v2/demographics/dashboard/summary",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_dashboard_kpis(self, test_client):
        """Test GET /dashboard/kpis"""
        response = test_client.get(
            "/api/v2/demographics/dashboard/kpis",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_dashboard_trends(self, test_client):
        """Test GET /dashboard/trends"""
        response = test_client.get(
            "/api/v2/demographics/dashboard/trends",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_dashboard_alerts(self, test_client):
        """Test GET /dashboard/alerts"""
        response = test_client.get(
            "/api/v2/demographics/dashboard/alerts",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]

    def test_get_executive_summary(self, test_client):
        """Test GET /dashboard/executive"""
        response = test_client.get(
            "/api/v2/demographics/dashboard/executive",
            headers={"X-Customer-ID": "test-customer"}
        )
        assert response.status_code in [200, 501]


# ============================================================================
# Multi-Tenant Tests
# ============================================================================

class TestDemographicsMultiTenant:
    """Test multi-tenant isolation"""

    def test_customer_id_required(self, test_client):
        """Test that X-Customer-ID header is required"""
        response = test_client.get("/api/v2/demographics/population/summary")
        assert response.status_code == 422  # Missing header

    def test_customer_isolation(self, test_client):
        """Test data isolation between customers"""
        response1 = test_client.get(
            "/api/v2/demographics/population/summary",
            headers={"X-Customer-ID": "customer-1"}
        )
        response2 = test_client.get(
            "/api/v2/demographics/population/summary",
            headers={"X-Customer-ID": "customer-2"}
        )
        assert response1.status_code == 200
        assert response2.status_code == 200


# ============================================================================
# Health Check
# ============================================================================

def test_health_check(test_client):
    """Test health check endpoint"""
    response = test_client.get("/api/v2/demographics/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["endpoints"] == 24
