"""
Integration tests for E08 Automated Scanning API.

Tests comprehensive coverage of:
- Scan Profiles (15 tests)
- Schedules (14 tests)
- Scan Jobs (16 tests)
- Findings (14 tests)
- Targets (12 tests)
- Dashboard (6 tests)
- Edge Cases (8 tests)

Total: 85 tests
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4

# Mock imports - adjust based on actual structure
from app.main import app
from app.models.scanning import (
    ScanProfile,
    ScanSchedule,
    ScanJob,
    Finding,
    Target,
    ScanType,
    JobStatus,
    FindingSeverity,
    FindingStatus
)


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def customer_id():
    """Test customer ID."""
    return "CUST-TEST-001"


@pytest.fixture
def mock_qdrant():
    """Mock Qdrant client."""
    with patch('app.services.qdrant.QdrantService') as mock:
        qdrant_instance = Mock()
        qdrant_instance.search.return_value = []
        qdrant_instance.upsert.return_value = True
        qdrant_instance.delete.return_value = True
        mock.return_value = qdrant_instance
        yield qdrant_instance


@pytest.fixture
def auth_headers(customer_id):
    """Authentication headers with customer context."""
    return {
        "Authorization": "Bearer test-token",
        "X-Customer-ID": customer_id
    }


@pytest.fixture
def sample_profile(customer_id):
    """Sample scan profile."""
    return {
        "name": "Standard Security Scan",
        "scan_type": "vulnerability",
        "customer_id": customer_id,
        "configuration": {
            "scan_depth": "comprehensive",
            "port_range": "1-65535",
            "scan_timeout": 3600,
            "max_concurrent_scans": 10
        },
        "enabled": True
    }


@pytest.fixture
def sample_schedule(customer_id):
    """Sample scan schedule."""
    return {
        "name": "Daily Vulnerability Scan",
        "profile_id": str(uuid4()),
        "customer_id": customer_id,
        "frequency": "daily",
        "time": "02:00",
        "enabled": True,
        "notification_recipients": ["security@example.com"]
    }


@pytest.fixture
def sample_job(customer_id):
    """Sample scan job."""
    return {
        "profile_id": str(uuid4()),
        "customer_id": customer_id,
        "targets": ["192.168.1.0/24"],
        "status": "pending",
        "started_at": None,
        "completed_at": None
    }


@pytest.fixture
def sample_finding(customer_id):
    """Sample security finding."""
    return {
        "title": "SQL Injection Vulnerability",
        "severity": "high",
        "status": "open",
        "customer_id": customer_id,
        "job_id": str(uuid4()),
        "affected_asset": "192.168.1.100",
        "cvss_score": 8.5,
        "cve_id": "CVE-2024-1234",
        "description": "SQL injection vulnerability in login form",
        "remediation": "Implement parameterized queries"
    }


@pytest.fixture
def sample_target(customer_id):
    """Sample scan target."""
    return {
        "name": "Production Server",
        "address": "192.168.1.100",
        "customer_id": customer_id,
        "port_range": "1-1024",
        "enabled": True,
        "tags": ["production", "web-server"]
    }


# ============================================================================
# 1. SCAN PROFILES TESTS (15 tests)
# ============================================================================

class TestScanProfiles:
    """Test scan profile management."""

    def test_create_profile_success(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test successful profile creation."""
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_profile["name"]
        assert data["scan_type"] == sample_profile["scan_type"]
        assert "id" in data
        assert "created_at" in data

    def test_create_profile_invalid_type(self, client, auth_headers, sample_profile):
        """Test profile creation with invalid scan type."""
        sample_profile["scan_type"] = "invalid_type"
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 422
        assert "scan_type" in response.json()["detail"][0]["loc"]

    def test_get_profile_success(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test retrieving a profile."""
        # Create profile first
        create_response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]

        # Get profile
        response = client.get(
            f"/api/v1/scanning/profiles/{profile_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
        assert data["name"] == sample_profile["name"]

    def test_get_profile_not_found(self, client, auth_headers):
        """Test retrieving non-existent profile."""
        response = client.get(
            f"/api/v1/scanning/profiles/{uuid4()}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_profile_success(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test profile update."""
        # Create profile
        create_response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]

        # Update profile
        update_data = {"name": "Updated Profile Name"}
        response = client.patch(
            f"/api/v1/scanning/profiles/{profile_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]

    def test_delete_profile_success(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test profile deletion."""
        # Create profile
        create_response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]

        # Delete profile
        response = client.delete(
            f"/api/v1/scanning/profiles/{profile_id}",
            headers=auth_headers
        )
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(
            f"/api/v1/scanning/profiles/{profile_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_list_profiles_empty(self, client, auth_headers, mock_qdrant):
        """Test listing profiles when none exist."""
        mock_qdrant.search.return_value = []
        response = client.get(
            "/api/v1/scanning/profiles",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["items"] == []
        assert response.json()["total"] == 0

    def test_list_profiles_with_results(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test listing profiles with results."""
        # Create multiple profiles
        for i in range(3):
            profile = sample_profile.copy()
            profile["name"] = f"Profile {i}"
            client.post(
                "/api/v1/scanning/profiles",
                json=profile,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/profiles",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    def test_profiles_by_scan_type(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test filtering profiles by scan type."""
        response = client.get(
            "/api/v1/scanning/profiles?scan_type=vulnerability",
            headers=auth_headers
        )
        assert response.status_code == 200
        for profile in response.json()["items"]:
            assert profile["scan_type"] == "vulnerability"

    def test_clone_profile_success(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test cloning a profile."""
        # Create original profile
        create_response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]

        # Clone profile
        response = client.post(
            f"/api/v1/scanning/profiles/{profile_id}/clone",
            json={"name": "Cloned Profile"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Cloned Profile"
        assert data["id"] != profile_id
        assert data["configuration"] == sample_profile["configuration"]

    def test_profile_configuration(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test profile configuration validation."""
        sample_profile["configuration"]["scan_timeout"] = -100
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_profile_target_specification(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test profile with target specifications."""
        sample_profile["default_targets"] = ["192.168.1.0/24", "10.0.0.0/8"]
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["default_targets"] == sample_profile["default_targets"]

    def test_profile_timeout_validation(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test timeout validation."""
        sample_profile["configuration"]["scan_timeout"] = 0
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_profile_customer_isolation(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test customer isolation for profiles."""
        # Create profile for customer 1
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        profile_id = response.json()["id"]

        # Try to access with different customer
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        response = client.get(
            f"/api/v1/scanning/profiles/{profile_id}",
            headers=other_headers
        )
        assert response.status_code == 404

    def test_profile_scanner_type(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test different scanner types."""
        for scan_type in ["vulnerability", "port", "web", "compliance"]:
            profile = sample_profile.copy()
            profile["scan_type"] = scan_type
            profile["name"] = f"{scan_type.title()} Scan"
            response = client.post(
                "/api/v1/scanning/profiles",
                json=profile,
                headers=auth_headers
            )
            assert response.status_code == 201
            assert response.json()["scan_type"] == scan_type


# ============================================================================
# 2. SCHEDULES TESTS (14 tests)
# ============================================================================

class TestSchedules:
    """Test scan schedule management."""

    def test_create_schedule_success(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test successful schedule creation."""
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_schedule["name"]
        assert data["frequency"] == sample_schedule["frequency"]
        assert "id" in data
        assert "next_run" in data

    def test_get_schedule_success(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test retrieving a schedule."""
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/schedules/{schedule_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == schedule_id

    def test_update_schedule_success(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test schedule update."""
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        update_data = {"frequency": "weekly", "time": "03:00"}
        response = client.patch(
            f"/api/v1/scanning/schedules/{schedule_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["frequency"] == "weekly"
        assert response.json()["time"] == "03:00"

    def test_delete_schedule_success(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test schedule deletion."""
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        response = client.delete(
            f"/api/v1/scanning/schedules/{schedule_id}",
            headers=auth_headers
        )
        assert response.status_code == 204

    def test_list_schedules(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test listing schedules."""
        # Create multiple schedules
        for i in range(3):
            schedule = sample_schedule.copy()
            schedule["name"] = f"Schedule {i}"
            client.post(
                "/api/v1/scanning/schedules",
                json=schedule,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/schedules",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    def test_enable_schedule(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test enabling a schedule."""
        sample_schedule["enabled"] = False
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        response = client.post(
            f"/api/v1/scanning/schedules/{schedule_id}/enable",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["enabled"] is True

    def test_disable_schedule(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test disabling a schedule."""
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        response = client.post(
            f"/api/v1/scanning/schedules/{schedule_id}/disable",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["enabled"] is False

    def test_schedule_frequency_validation(self, client, auth_headers, sample_schedule):
        """Test schedule frequency validation."""
        sample_schedule["frequency"] = "invalid_frequency"
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_schedule_next_run_calculation(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test next run time calculation."""
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "next_run" in data
        # Verify next_run is in the future
        next_run = datetime.fromisoformat(data["next_run"].replace('Z', '+00:00'))
        assert next_run > datetime.now()

    def test_schedule_notification_recipients(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test notification recipient validation."""
        sample_schedule["notification_recipients"] = ["invalid-email"]
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_schedule_maintenance_window(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test maintenance window configuration."""
        sample_schedule["maintenance_window"] = {
            "start": "22:00",
            "end": "06:00"
        }
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["maintenance_window"]["start"] == "22:00"

    def test_schedule_max_duration(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test maximum duration setting."""
        sample_schedule["max_duration"] = 7200  # 2 hours
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["max_duration"] == 7200

    def test_schedule_customer_isolation(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test customer isolation for schedules."""
        create_response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        schedule_id = create_response.json()["id"]

        # Try to access with different customer
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        response = client.get(
            f"/api/v1/scanning/schedules/{schedule_id}",
            headers=other_headers
        )
        assert response.status_code == 404

    def test_schedule_profile_link(self, client, auth_headers, sample_schedule, mock_qdrant):
        """Test schedule linked to profile."""
        response = client.post(
            "/api/v1/scanning/schedules",
            json=sample_schedule,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["profile_id"] == sample_schedule["profile_id"]


# ============================================================================
# 3. SCAN JOBS TESTS (16 tests)
# ============================================================================

class TestScanJobs:
    """Test scan job execution and management."""

    def test_start_job_success(self, client, auth_headers, sample_job, mock_qdrant):
        """Test starting a scan job."""
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data

    def test_get_job_status(self, client, auth_headers, sample_job, mock_qdrant):
        """Test retrieving job status."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == job_id
        assert "status" in response.json()

    def test_list_jobs(self, client, auth_headers, sample_job, mock_qdrant):
        """Test listing jobs."""
        # Create multiple jobs
        for i in range(3):
            job = sample_job.copy()
            job["targets"] = [f"192.168.{i}.0/24"]
            client.post(
                "/api/v1/scanning/jobs",
                json=job,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/jobs",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    def test_cancel_job(self, client, auth_headers, sample_job, mock_qdrant):
        """Test canceling a running job."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.post(
            f"/api/v1/scanning/jobs/{job_id}/cancel",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] in ["cancelled", "cancelling"]

    def test_get_job_findings(self, client, auth_headers, sample_job, mock_qdrant):
        """Test retrieving job findings."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}/findings",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "items" in response.json()

    def test_list_running_jobs(self, client, auth_headers, sample_job, mock_qdrant):
        """Test listing only running jobs."""
        response = client.get(
            "/api/v1/scanning/jobs?status=running",
            headers=auth_headers
        )
        assert response.status_code == 200
        for job in response.json()["items"]:
            assert job["status"] == "running"

    def test_job_progress_tracking(self, client, auth_headers, sample_job, mock_qdrant):
        """Test job progress tracking."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "progress_percent" in data
        assert "targets_scanned" in data
        assert "targets_total" in data

    def test_job_completion(self, client, auth_headers, sample_job, mock_qdrant):
        """Test job completion status."""
        sample_job["status"] = "completed"
        sample_job["completed_at"] = datetime.now().isoformat()
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "completed"
        assert "completed_at" in data

    def test_job_failure_handling(self, client, auth_headers, sample_job, mock_qdrant):
        """Test job failure scenarios."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        # Simulate failure
        response = client.patch(
            f"/api/v1/scanning/jobs/{job_id}",
            json={
                "status": "failed",
                "error_message": "Network timeout"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "failed"
        assert "error_message" in response.json()

    def test_job_targets_scanned(self, client, auth_headers, sample_job, mock_qdrant):
        """Test tracking scanned targets."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "targets" in data
        assert isinstance(data["targets"], list)

    def test_job_findings_count(self, client, auth_headers, sample_job, mock_qdrant):
        """Test findings count in job summary."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "findings_count" in data
        assert "findings_by_severity" in data

    def test_job_by_severity(self, client, auth_headers, sample_job, mock_qdrant):
        """Test filtering findings by severity."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}/findings?severity=high",
            headers=auth_headers
        )
        assert response.status_code == 200
        for finding in response.json()["items"]:
            assert finding["severity"] == "high"

    def test_job_scan_log(self, client, auth_headers, sample_job, mock_qdrant):
        """Test retrieving job scan logs."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}/logs",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "logs" in response.json()

    def test_job_error_message(self, client, auth_headers, sample_job, mock_qdrant):
        """Test error message in failed jobs."""
        sample_job["status"] = "failed"
        sample_job["error_message"] = "Connection refused"
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["error_message"] == "Connection refused"

    def test_job_customer_isolation(self, client, auth_headers, sample_job, mock_qdrant):
        """Test customer isolation for jobs."""
        create_response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        # Try to access with different customer
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        response = client.get(
            f"/api/v1/scanning/jobs/{job_id}",
            headers=other_headers
        )
        assert response.status_code == 404

    def test_job_schedule_link(self, client, auth_headers, sample_job, mock_qdrant):
        """Test job linked to schedule."""
        sample_job["schedule_id"] = str(uuid4())
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["schedule_id"] == sample_job["schedule_id"]


# ============================================================================
# 4. FINDINGS TESTS (14 tests)
# ============================================================================

class TestFindings:
    """Test security findings management."""

    def test_list_findings(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test listing findings."""
        # Create multiple findings
        for i in range(3):
            finding = sample_finding.copy()
            finding["title"] = f"Finding {i}"
            client.post(
                "/api/v1/scanning/findings",
                json=finding,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/findings",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    def test_get_finding(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test retrieving a specific finding."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        finding_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/scanning/findings/{finding_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == finding_id

    def test_update_finding_status(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test updating finding status."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        finding_id = create_response.json()["id"]

        response = client.patch(
            f"/api/v1/scanning/findings/{finding_id}",
            json={"status": "resolved"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"

    def test_findings_by_severity(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test filtering findings by severity."""
        # Create findings with different severities
        for severity in ["critical", "high", "medium", "low"]:
            finding = sample_finding.copy()
            finding["severity"] = severity
            finding["title"] = f"{severity.title()} Finding"
            client.post(
                "/api/v1/scanning/findings",
                json=finding,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/findings?severity=critical",
            headers=auth_headers
        )
        assert response.status_code == 200
        for finding in response.json()["items"]:
            assert finding["severity"] == "critical"

    def test_search_findings(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test searching findings."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/scanning/findings?search=SQL injection",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) > 0

    def test_finding_cvss_score(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test CVSS score validation."""
        sample_finding["cvss_score"] = 10.5  # Invalid score
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_finding_cve_link(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test CVE ID linking."""
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["cve_id"] == sample_finding["cve_id"]
        assert "cve_url" in data

    def test_finding_affected_asset(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test affected asset tracking."""
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["affected_asset"] == sample_finding["affected_asset"]

    def test_finding_remediation(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test remediation information."""
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "remediation" in data
        assert data["remediation"] == sample_finding["remediation"]

    def test_finding_false_positive(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test marking finding as false positive."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        finding_id = create_response.json()["id"]

        response = client.post(
            f"/api/v1/scanning/findings/{finding_id}/false-positive",
            json={"reason": "Known safe configuration"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "false_positive"
        assert "false_positive_reason" in data

    def test_finding_first_detected(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test first detected timestamp."""
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert "first_detected" in response.json()

    def test_finding_evidence(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test finding evidence data."""
        sample_finding["evidence"] = {
            "request": "GET /login?user=' OR 1=1--",
            "response": "200 OK",
            "proof": "SQL error message in response"
        }
        response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["evidence"] == sample_finding["evidence"]

    def test_finding_customer_isolation(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test customer isolation for findings."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        finding_id = create_response.json()["id"]

        # Try to access with different customer
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        response = client.get(
            f"/api/v1/scanning/findings/{finding_id}",
            headers=other_headers
        )
        assert response.status_code == 404

    def test_finding_status_transition(self, client, auth_headers, sample_finding, mock_qdrant):
        """Test valid status transitions."""
        create_response = client.post(
            "/api/v1/scanning/findings",
            json=sample_finding,
            headers=auth_headers
        )
        finding_id = create_response.json()["id"]

        # Test valid transitions: open -> in_progress -> resolved
        for status in ["in_progress", "resolved"]:
            response = client.patch(
                f"/api/v1/scanning/findings/{finding_id}",
                json={"status": status},
                headers=auth_headers
            )
            assert response.status_code == 200
            assert response.json()["status"] == status


# ============================================================================
# 5. TARGETS TESTS (12 tests)
# ============================================================================

class TestTargets:
    """Test scan target management."""

    def test_create_target_success(self, client, auth_headers, sample_target, mock_qdrant):
        """Test successful target creation."""
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_target["name"]
        assert data["address"] == sample_target["address"]
        assert "id" in data

    def test_list_targets(self, client, auth_headers, sample_target, mock_qdrant):
        """Test listing targets."""
        # Create multiple targets
        for i in range(3):
            target = sample_target.copy()
            target["name"] = f"Target {i}"
            target["address"] = f"192.168.1.{i}"
            client.post(
                "/api/v1/scanning/targets",
                json=target,
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/scanning/targets",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    def test_update_target(self, client, auth_headers, sample_target, mock_qdrant):
        """Test target update."""
        create_response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        target_id = create_response.json()["id"]

        update_data = {"name": "Updated Target", "port_range": "1-65535"}
        response = client.patch(
            f"/api/v1/scanning/targets/{target_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Target"
        assert response.json()["port_range"] == "1-65535"

    def test_delete_target(self, client, auth_headers, sample_target, mock_qdrant):
        """Test target deletion."""
        create_response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        target_id = create_response.json()["id"]

        response = client.delete(
            f"/api/v1/scanning/targets/{target_id}",
            headers=auth_headers
        )
        assert response.status_code == 204

    def test_target_address_validation(self, client, auth_headers, sample_target):
        """Test target address validation."""
        sample_target["address"] = "invalid-address"
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_target_port_range(self, client, auth_headers, sample_target, mock_qdrant):
        """Test port range specification."""
        sample_target["port_range"] = "80,443,8080-8090"
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["port_range"] == sample_target["port_range"]

    def test_target_credentials(self, client, auth_headers, sample_target, mock_qdrant):
        """Test target credentials storage."""
        sample_target["credentials"] = {
            "username": "admin",
            "auth_type": "basic"
        }
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        # Credentials should not be returned in response
        assert "credentials" not in response.json() or \
               "password" not in response.json().get("credentials", {})

    def test_target_last_scanned(self, client, auth_headers, sample_target, mock_qdrant):
        """Test last scanned timestamp."""
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert "last_scanned" in response.json()

    def test_target_scan_frequency(self, client, auth_headers, sample_target, mock_qdrant):
        """Test scan frequency configuration."""
        sample_target["scan_frequency"] = "weekly"
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["scan_frequency"] == "weekly"

    def test_target_enabled_flag(self, client, auth_headers, sample_target, mock_qdrant):
        """Test enabling/disabling targets."""
        create_response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        target_id = create_response.json()["id"]

        # Disable target
        response = client.patch(
            f"/api/v1/scanning/targets/{target_id}",
            json={"enabled": False},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["enabled"] is False

    def test_target_tags(self, client, auth_headers, sample_target, mock_qdrant):
        """Test target tagging."""
        response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["tags"] == sample_target["tags"]

    def test_target_customer_isolation(self, client, auth_headers, sample_target, mock_qdrant):
        """Test customer isolation for targets."""
        create_response = client.post(
            "/api/v1/scanning/targets",
            json=sample_target,
            headers=auth_headers
        )
        target_id = create_response.json()["id"]

        # Try to access with different customer
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        response = client.get(
            f"/api/v1/scanning/targets/{target_id}",
            headers=other_headers
        )
        assert response.status_code == 404


# ============================================================================
# 6. DASHBOARD TESTS (6 tests)
# ============================================================================

class TestDashboard:
    """Test scanning dashboard endpoints."""

    def test_dashboard_summary(self, client, auth_headers, mock_qdrant):
        """Test dashboard summary statistics."""
        response = client.get(
            "/api/v1/scanning/dashboard/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_jobs" in data
        assert "active_jobs" in data
        assert "total_findings" in data
        assert "critical_findings" in data

    def test_dashboard_jobs_by_status(self, client, auth_headers, mock_qdrant):
        """Test jobs grouped by status."""
        response = client.get(
            "/api/v1/scanning/dashboard/jobs-by-status",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "pending" in data
        assert "running" in data
        assert "completed" in data
        assert "failed" in data

    def test_dashboard_findings_by_severity(self, client, auth_headers, mock_qdrant):
        """Test findings grouped by severity."""
        response = client.get(
            "/api/v1/scanning/dashboard/findings-by-severity",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "critical" in data
        assert "high" in data
        assert "medium" in data
        assert "low" in data

    def test_dashboard_recent_scans(self, client, auth_headers, mock_qdrant):
        """Test recent scans listing."""
        response = client.get(
            "/api/v1/scanning/dashboard/recent-scans?limit=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) <= 10

    def test_dashboard_customer_isolation(self, client, auth_headers, mock_qdrant):
        """Test dashboard respects customer isolation."""
        response = client.get(
            "/api/v1/scanning/dashboard/summary",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Verify another customer gets different data
        other_headers = auth_headers.copy()
        other_headers["X-Customer-ID"] = "CUST-OTHER-001"
        other_response = client.get(
            "/api/v1/scanning/dashboard/summary",
            headers=other_headers
        )
        assert other_response.status_code == 200
        # Data should be different (or both empty)
        assert response.json() != other_response.json() or \
               response.json()["total_jobs"] == 0

    def test_dashboard_empty_state(self, client, auth_headers, mock_qdrant):
        """Test dashboard with no data."""
        mock_qdrant.search.return_value = []
        response = client.get(
            "/api/v1/scanning/dashboard/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_jobs"] == 0
        assert data["active_jobs"] == 0
        assert data["total_findings"] == 0


# ============================================================================
# 7. EDGE CASES TESTS (8 tests)
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_missing_customer_id(self, client):
        """Test request without customer ID."""
        headers = {"Authorization": "Bearer test-token"}
        response = client.get(
            "/api/v1/scanning/profiles",
            headers=headers
        )
        assert response.status_code == 400
        assert "customer" in response.json()["detail"].lower()

    def test_invalid_customer_id(self, client):
        """Test request with invalid customer ID."""
        headers = {
            "Authorization": "Bearer test-token",
            "X-Customer-ID": "INVALID"
        }
        response = client.get(
            "/api/v1/scanning/profiles",
            headers=headers
        )
        assert response.status_code == 400

    def test_concurrent_job_limit(self, client, auth_headers, sample_job, mock_qdrant):
        """Test concurrent job limit enforcement."""
        # Create maximum allowed concurrent jobs
        for i in range(10):
            job = sample_job.copy()
            job["targets"] = [f"192.168.{i}.0/24"]
            client.post(
                "/api/v1/scanning/jobs",
                json=job,
                headers=auth_headers
            )

        # Try to create one more
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        assert response.status_code in [429, 400]
        assert "concurrent" in response.json()["detail"].lower() or \
               "limit" in response.json()["detail"].lower()

    def test_large_target_list(self, client, auth_headers, sample_job, mock_qdrant):
        """Test handling large target lists."""
        sample_job["targets"] = [f"192.168.{i}.0/24" for i in range(100)]
        response = client.post(
            "/api/v1/scanning/jobs",
            json=sample_job,
            headers=auth_headers
        )
        # Should either succeed or return validation error for too many targets
        assert response.status_code in [201, 422]

    def test_special_characters(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test handling special characters in names."""
        sample_profile["name"] = "Test <script>alert('xss')</script> Profile"
        response = client.post(
            "/api/v1/scanning/profiles",
            json=sample_profile,
            headers=auth_headers
        )
        assert response.status_code == 201
        # Verify name is sanitized
        assert "<script>" not in response.json()["name"]

    def test_pagination(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test pagination parameters."""
        # Create multiple profiles
        for i in range(25):
            profile = sample_profile.copy()
            profile["name"] = f"Profile {i}"
            client.post(
                "/api/v1/scanning/profiles",
                json=profile,
                headers=auth_headers
            )

        # Test pagination
        response = client.get(
            "/api/v1/scanning/profiles?page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 25
        assert data["page"] == 1

    def test_sorting(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test sorting functionality."""
        # Create profiles with different names
        for name in ["Zebra", "Alpha", "Beta"]:
            profile = sample_profile.copy()
            profile["name"] = name
            client.post(
                "/api/v1/scanning/profiles",
                json=profile,
                headers=auth_headers
            )

        # Test sorting
        response = client.get(
            "/api/v1/scanning/profiles?sort=name&order=asc",
            headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        names = [item["name"] for item in items]
        assert names == sorted(names)

    def test_filtering(self, client, auth_headers, sample_profile, mock_qdrant):
        """Test multiple filter combinations."""
        # Test with multiple filters
        response = client.get(
            "/api/v1/scanning/profiles?scan_type=vulnerability&enabled=true",
            headers=auth_headers
        )
        assert response.status_code == 200
        for profile in response.json()["items"]:
            assert profile["scan_type"] == "vulnerability"
            assert profile["enabled"] is True


# ============================================================================
# TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
