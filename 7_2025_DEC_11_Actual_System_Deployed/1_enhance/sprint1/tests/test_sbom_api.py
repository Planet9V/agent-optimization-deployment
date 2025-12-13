"""
Unit and integration tests for SBOM APIs
Tests multi-tenant isolation, SBOM parsing, and database operations
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from uuid import uuid4

import sys
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/1_enhance/sprint1/backend')

from main import app
from api.v2.sbom.models import (
    SBOMAnalyzeRequest,
    ComponentSearchRequest
)

client = TestClient(app)

# Test customer IDs
CUSTOMER_A = "customer_test_a"
CUSTOMER_B = "customer_test_b"


class TestSBOMAnalyze:
    """Test POST /api/v2/sbom/analyze"""

    def test_analyze_cyclonedx_sbom_success(self):
        """Test successful CycloneDX SBOM analysis"""

        cyclonedx_sbom = {
            "format": "cyclonedx",
            "project_name": "test-project",
            "project_version": "1.0.0",
            "content": {
                "bomFormat": "CycloneDX",
                "specVersion": "1.4",
                "version": 1,
                "components": [
                    {
                        "type": "library",
                        "name": "express",
                        "version": "4.18.2",
                        "purl": "pkg:npm/express@4.18.2",
                        "licenses": [
                            {"license": {"id": "MIT"}}
                        ]
                    },
                    {
                        "type": "library",
                        "name": "lodash",
                        "version": "4.17.21",
                        "purl": "pkg:npm/lodash@4.17.21"
                    }
                ]
            }
        }

        response = client.post(
            "/api/v2/sbom/analyze",
            json=cyclonedx_sbom,
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 201
        data = response.json()
        assert "sbom_id" in data
        assert data["project_name"] == "test-project"
        assert data["components_count"] == 2
        assert data["customer_id"] == CUSTOMER_A
        assert "created_at" in data

    def test_analyze_spdx_sbom_success(self):
        """Test successful SPDX SBOM analysis"""

        spdx_sbom = {
            "format": "spdx",
            "project_name": "spdx-test-project",
            "project_version": "2.0.0",
            "content": {
                "spdxVersion": "SPDX-2.3",
                "dataLicense": "CC0-1.0",
                "packages": [
                    {
                        "name": "numpy",
                        "versionInfo": "1.24.0",
                        "licenseConcluded": "BSD-3-Clause",
                        "supplier": "Organization: NumPy Developers"
                    },
                    {
                        "name": "pandas",
                        "versionInfo": "2.0.0",
                        "licenseConcluded": "BSD-3-Clause"
                    }
                ]
            }
        }

        response = client.post(
            "/api/v2/sbom/analyze",
            json=spdx_sbom,
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["components_count"] == 2

    def test_analyze_without_customer_id(self):
        """Test that request fails without X-Customer-ID header"""

        sbom = {
            "format": "cyclonedx",
            "project_name": "test",
            "content": {"components": []}
        }

        response = client.post("/api/v2/sbom/analyze", json=sbom)
        assert response.status_code == 401
        assert "X-Customer-ID" in response.json()["detail"]

    def test_analyze_invalid_format(self):
        """Test validation for invalid SBOM format"""

        invalid_sbom = {
            "format": "invalid_format",
            "project_name": "test",
            "content": {}
        }

        response = client.post(
            "/api/v2/sbom/analyze",
            json=invalid_sbom,
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 422  # Validation error


class TestSBOMGet:
    """Test GET /api/v2/sbom/{sbom_id}"""

    @pytest.fixture
    def sample_sbom_id(self):
        """Create a sample SBOM and return its ID"""
        sbom = {
            "format": "cyclonedx",
            "project_name": "get-test-project",
            "content": {
                "components": [
                    {"name": "test-lib", "version": "1.0.0"}
                ]
            }
        }

        response = client.post(
            "/api/v2/sbom/analyze",
            json=sbom,
            headers={"X-Customer-ID": CUSTOMER_A}
        )
        return response.json()["sbom_id"]

    def test_get_sbom_success(self, sample_sbom_id):
        """Test successful SBOM retrieval"""

        response = client.get(
            f"/api/v2/sbom/{sample_sbom_id}",
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sbom_id"] == sample_sbom_id
        assert data["project_name"] == "get-test-project"
        assert data["components_count"] >= 1
        assert "components" in data

    def test_get_sbom_wrong_customer(self, sample_sbom_id):
        """Test multi-tenant isolation - different customer cannot access SBOM"""

        response = client.get(
            f"/api/v2/sbom/{sample_sbom_id}",
            headers={"X-Customer-ID": CUSTOMER_B}
        )

        assert response.status_code == 404

    def test_get_nonexistent_sbom(self):
        """Test retrieving non-existent SBOM"""

        fake_id = str(uuid4())
        response = client.get(
            f"/api/v2/sbom/{fake_id}",
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 404


class TestSBOMSummary:
    """Test GET /api/v2/sbom/summary"""

    def test_get_summary_success(self):
        """Test SBOM summary retrieval"""

        # Create some SBOMs first
        for i in range(3):
            sbom = {
                "format": "cyclonedx",
                "project_name": f"summary-test-{i}",
                "content": {
                    "components": [
                        {"name": f"lib-{i}", "version": "1.0.0"}
                    ]
                }
            }
            client.post(
                "/api/v2/sbom/analyze",
                json=sbom,
                headers={"X-Customer-ID": CUSTOMER_A}
            )

        response = client.get(
            "/api/v2/sbom/summary",
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total_sboms"] >= 3
        assert data["total_components"] >= 3
        assert "total_vulnerabilities" in data
        assert "critical_vulnerabilities" in data
        assert data["customer_id"] == CUSTOMER_A

    def test_summary_multi_tenant_isolation(self):
        """Test that summary only includes customer's data"""

        # Create SBOM for customer A
        client.post(
            "/api/v2/sbom/analyze",
            json={
                "format": "cyclonedx",
                "project_name": "customer-a-project",
                "content": {"components": [{"name": "lib-a", "version": "1.0"}]}
            },
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        # Create SBOM for customer B
        client.post(
            "/api/v2/sbom/analyze",
            json={
                "format": "cyclonedx",
                "project_name": "customer-b-project",
                "content": {"components": [{"name": "lib-b", "version": "1.0"}]}
            },
            headers={"X-Customer-ID": CUSTOMER_B}
        )

        # Get summary for customer A
        response_a = client.get(
            "/api/v2/sbom/summary",
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        # Get summary for customer B
        response_b = client.get(
            "/api/v2/sbom/summary",
            headers={"X-Customer-ID": CUSTOMER_B}
        )

        # Summaries should be different
        assert response_a.json()["total_sboms"] != response_b.json()["total_sboms"]


class TestComponentSearch:
    """Test POST /api/v2/sbom/components/search"""

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Create test SBOMs for search testing"""
        sboms = [
            {
                "format": "cyclonedx",
                "project_name": "search-test-1",
                "content": {
                    "components": [
                        {"name": "express", "version": "4.18.2"},
                        {"name": "react", "version": "18.2.0"}
                    ]
                }
            },
            {
                "format": "cyclonedx",
                "project_name": "search-test-2",
                "content": {
                    "components": [
                        {"name": "django", "version": "4.2.0"},
                        {"name": "flask", "version": "3.0.0"}
                    ]
                }
            }
        ]

        for sbom in sboms:
            client.post(
                "/api/v2/sbom/analyze",
                json=sbom,
                headers={"X-Customer-ID": CUSTOMER_A}
            )

    def test_search_components_success(self):
        """Test successful component search"""

        search_request = {
            "query": "express web framework",
            "limit": 10,
            "similarity_threshold": 0.5
        }

        response = client.post(
            "/api/v2/sbom/components/search",
            json=search_request,
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert data["query"] == "express web framework"
        assert data["customer_id"] == CUSTOMER_A
        assert data["total_results"] >= 0

    def test_search_with_limit(self):
        """Test search respects limit parameter"""

        search_request = {
            "query": "python framework",
            "limit": 2
        }

        response = client.post(
            "/api/v2/sbom/components/search",
            json=search_request,
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) <= 2

    def test_search_multi_tenant_isolation(self):
        """Test search only returns customer's components"""

        # Create component for customer B
        client.post(
            "/api/v2/sbom/analyze",
            json={
                "format": "cyclonedx",
                "project_name": "customer-b-only",
                "content": {
                    "components": [{"name": "customer-b-lib", "version": "1.0"}]
                }
            },
            headers={"X-Customer-ID": CUSTOMER_B}
        )

        # Search as customer A
        response = client.post(
            "/api/v2/sbom/components/search",
            json={"query": "customer-b-lib"},
            headers={"X-Customer-ID": CUSTOMER_A}
        )

        # Should not find customer B's component
        assert response.status_code == 200
        # Results should not contain customer B's data
        for result in response.json()["results"]:
            assert result["name"] != "customer-b-lib"


class TestAPIHealth:
    """Test health and root endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "AEON SBOM API"
        assert "endpoints" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
