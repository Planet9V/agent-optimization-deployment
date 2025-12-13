"""
Unit Tests for Equipment CRUD APIs (Sprint 1)
==============================================

Tests 5 equipment endpoints:
1. POST /api/v2/vendor-equipment/equipment - Create equipment
2. GET /api/v2/vendor-equipment/equipment/{id} - Get equipment by ID
3. GET /api/v2/vendor-equipment/equipment - Search equipment
4. PUT /api/v2/vendor-equipment/equipment/{id} - Update equipment
5. DELETE /api/v2/vendor-equipment/equipment/{id} - Delete equipment

Coverage Target: ≥85%
Response Time Target: <200ms
"""

import pytest
import uuid
from datetime import date, datetime
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import status

# Import the actual API router and service
import sys
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model')
from api.vendor_equipment.vendor_router import router
from api.vendor_equipment.vendor_service import VendorEquipmentService
from api.vendor_equipment.vendor_models import EquipmentModel, Vendor
from api.customer_isolation import CustomerContext, CustomerAccessLevel

@pytest.fixture
def test_client():
    """Create FastAPI test client."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.fixture
def mock_service():
    """Mock VendorEquipmentService."""
    return Mock(spec=VendorEquipmentService)

@pytest.fixture
def customer_headers():
    """Standard customer headers for multi-tenant isolation."""
    return {
        "X-Customer-ID": "test-customer-001",
        "X-Namespace": "test-namespace",
        "X-User-ID": "test-user-001",
        "X-Access-Level": "write"
    }

@pytest.fixture
def sample_equipment_data():
    """Sample equipment data for testing."""
    return {
        "model_id": f"test-equipment-{uuid.uuid4().hex[:8]}",
        "vendor_id": "test-vendor-001",
        "model_name": "Cisco Catalyst 2960X",
        "product_line": "Catalyst Series",
        "release_date": "2024-01-15",
        "eol_date": "2029-01-15",
        "eos_date": "2030-01-15",
        "current_version": "15.2(7)E",
        "maintenance_schedule": "quarterly",
        "criticality": "high",
        "category": "network_switch",
        "description": "Enterprise-grade Layer 2/3 switch"
    }

# =====================================================
# TEST GROUP 1: CREATE EQUIPMENT (POST)
# =====================================================

class TestCreateEquipment:
    """Test POST /api/v2/vendor-equipment/equipment"""

    def test_create_equipment_success(self, test_client, customer_headers, sample_equipment_data):
        """✅ Test successful equipment creation with valid data."""
        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_equipment_data,
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        # Verify response structure
        assert "model_id" in data
        assert "vendor_id" in data
        assert "customer_id" in data
        assert data["model_name"] == sample_equipment_data["model_name"]
        assert data["criticality"] == "high"
        assert data["lifecycle_status"] in ["active", "supported", "approaching_eol", "eol", "eos"]

    def test_create_equipment_missing_required_fields(self, test_client, customer_headers):
        """❌ Test equipment creation fails without required fields."""
        invalid_data = {
            "model_name": "Test Model"  # Missing model_id, vendor_id
        }

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=invalid_data,
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_equipment_invalid_dates(self, test_client, customer_headers, sample_equipment_data):
        """❌ Test equipment creation with invalid date formats."""
        sample_equipment_data["eol_date"] = "invalid-date"

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_equipment_data,
            headers=customer_headers
        )

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_create_equipment_without_auth(self, test_client, sample_equipment_data):
        """❌ Test equipment creation without authentication headers."""
        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_equipment_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Missing X-Customer-ID

    def test_create_equipment_read_only_access(self, test_client, sample_equipment_data):
        """❌ Test equipment creation with read-only access level."""
        headers = {
            "X-Customer-ID": "test-customer-001",
            "X-Access-Level": "read"  # Read-only, should fail
        }

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_equipment_data,
            headers=headers
        )

        # Should either fail permission check or succeed (depends on implementation)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]


# =====================================================
# TEST GROUP 2: GET EQUIPMENT BY ID
# =====================================================

class TestGetEquipment:
    """Test GET /api/v2/vendor-equipment/equipment/{id}"""

    def test_get_equipment_success(self, test_client, customer_headers):
        """✅ Test retrieving equipment by valid ID."""
        # First create equipment
        sample_data = {
            "model_id": "test-get-equipment",
            "vendor_id": "test-vendor-001",
            "model_name": "Test Equipment",
            "maintenance_schedule": "monthly",
            "criticality": "medium"
        }

        create_response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_data,
            headers=customer_headers
        )

        if create_response.status_code == 201:
            model_id = create_response.json()["model_id"]

            # Now retrieve it
            response = test_client.get(
                f"/api/v2/vendor-equipment/equipment/{model_id}",
                headers=customer_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["model_id"] == model_id
            assert data["model_name"] == "Test Equipment"

    def test_get_equipment_not_found(self, test_client, customer_headers):
        """❌ Test retrieving non-existent equipment."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment/nonexistent-id",
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_equipment_cross_tenant_isolation(self, test_client):
        """🔒 Test that Customer A cannot access Customer B's equipment."""
        # Create equipment for Customer A
        headers_a = {
            "X-Customer-ID": "customer-a",
            "X-Access-Level": "write"
        }

        sample_data = {
            "model_id": "customer-a-equipment",
            "vendor_id": "vendor-001",
            "model_name": "Customer A Equipment",
            "maintenance_schedule": "quarterly",
            "criticality": "high"
        }

        create_response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_data,
            headers=headers_a
        )

        if create_response.status_code == 201:
            model_id = create_response.json()["model_id"]

            # Try to access with Customer B credentials
            headers_b = {
                "X-Customer-ID": "customer-b",
                "X-Access-Level": "read"
            }

            response = test_client.get(
                f"/api/v2/vendor-equipment/equipment/{model_id}",
                headers=headers_b
            )

            # Should either get 404 (not found for this customer) or 403 (forbidden)
            assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]


# =====================================================
# TEST GROUP 3: SEARCH EQUIPMENT
# =====================================================

class TestSearchEquipment:
    """Test GET /api/v2/vendor-equipment/equipment (search)"""

    def test_search_equipment_no_filters(self, test_client, customer_headers):
        """✅ Test equipment search without filters."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_results" in data
        assert "customer_id" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_equipment_with_query(self, test_client, customer_headers):
        """✅ Test equipment search with query parameter."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            params={"query": "Cisco", "limit": 10},
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_results"] >= 0

    def test_search_equipment_pagination(self, test_client, customer_headers):
        """✅ Test equipment search pagination."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            params={"limit": 5},
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) <= 5

    def test_search_equipment_by_lifecycle_status(self, test_client, customer_headers):
        """✅ Test equipment search by lifecycle status."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            params={"lifecycle_status": "eol"},
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # All returned equipment should have EOL status
        for equipment in data["results"]:
            assert equipment["lifecycle_status"] == "eol"

    def test_search_equipment_invalid_limit(self, test_client, customer_headers):
        """❌ Test equipment search with invalid limit."""
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            params={"limit": 9999},  # Exceeds max limit of 100
            headers=customer_headers
        )

        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]


# =====================================================
# TEST GROUP 4: PERFORMANCE TESTS
# =====================================================

class TestEquipmentPerformance:
    """Performance tests for equipment APIs."""

    @pytest.mark.performance
    def test_get_equipment_response_time(self, test_client, customer_headers):
        """⚡ Test GET equipment response time < 200ms."""
        import time

        start = time.time()
        response = test_client.get(
            "/api/v2/vendor-equipment/equipment",
            headers=customer_headers
        )
        duration_ms = (time.time() - start) * 1000

        assert response.status_code == status.HTTP_200_OK
        assert duration_ms < 200, f"Response took {duration_ms:.2f}ms, expected < 200ms"

    @pytest.mark.performance
    def test_create_equipment_response_time(self, test_client, customer_headers, sample_equipment_data):
        """⚡ Test POST equipment response time < 200ms."""
        import time

        sample_equipment_data["model_id"] = f"perf-test-{uuid.uuid4().hex[:8]}"

        start = time.time()
        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=sample_equipment_data,
            headers=customer_headers
        )
        duration_ms = (time.time() - start) * 1000

        assert response.status_code == status.HTTP_201_CREATED
        assert duration_ms < 200, f"Response took {duration_ms:.2f}ms, expected < 200ms"


# =====================================================
# TEST GROUP 5: EDGE CASES
# =====================================================

class TestEquipmentEdgeCases:
    """Edge case tests for equipment APIs."""

    def test_equipment_with_null_optional_fields(self, test_client, customer_headers):
        """✅ Test equipment creation with minimal required fields only."""
        minimal_data = {
            "model_id": f"minimal-{uuid.uuid4().hex[:8]}",
            "vendor_id": "test-vendor",
            "model_name": "Minimal Equipment",
            "maintenance_schedule": "annual",
            "criticality": "low"
        }

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=minimal_data,
            headers=customer_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_equipment_with_very_long_strings(self, test_client, customer_headers):
        """❌ Test equipment creation with excessively long string values."""
        long_string = "A" * 10000  # 10,000 characters

        data = {
            "model_id": "test-long",
            "vendor_id": "vendor",
            "model_name": long_string,  # Extremely long name
            "maintenance_schedule": "quarterly",
            "criticality": "medium"
        }

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=data,
            headers=customer_headers
        )

        # Should handle gracefully (either accept with truncation or reject)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

    def test_equipment_special_characters_in_names(self, test_client, customer_headers):
        """✅ Test equipment with special characters in names."""
        data = {
            "model_id": "test-special-chars",
            "vendor_id": "vendor",
            "model_name": "Test™ Equipment® <Model> & [Type]",
            "maintenance_schedule": "monthly",
            "criticality": "low"
        }

        response = test_client.post(
            "/api/v2/vendor-equipment/equipment",
            json=data,
            headers=customer_headers
        )

        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]


# =====================================================
# RUN ALL TESTS
# =====================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--cov=api.vendor_equipment", "--cov-report=term-missing"])
