"""
Test suite for GAP-ML-011 Batch Prediction API
Tests batch Ising and EWS endpoints with 100 entities
"""
import asyncio
import time
from typing import List
import httpx
import pytest

API_BASE_URL = "http://localhost:8000/api/v1"


@pytest.fixture
async def test_entity_ids() -> List[str]:
    """
    Generate 100 test entity IDs
    In production, these would be real Neo4j entity IDs
    """
    return [f"ACTOR-{str(i).zfill(3)}" for i in range(1, 101)]


@pytest.mark.asyncio
async def test_health_check():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_batch_ising_prediction(test_entity_ids):
    """
    Test batch Ising prediction with 100 entities
    Validates:
    - Job submission
    - Job status tracking
    - Results retrieval
    - Performance (< 30 seconds)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Submit batch job
        payload = {
            "entity_ids": test_entity_ids,
            "parameters": {
                "temperature": 0.5,
                "beta": 1.5,
                "coupling": 0.8,
                "field": 0.2
            }
        }

        print(f"\n[TEST] Submitting batch Ising job for {len(test_entity_ids)} entities...")
        start_time = time.time()

        response = await client.post(
            f"{API_BASE_URL}/predict/batch/ising",
            json=payload
        )

        assert response.status_code == 202
        job_data = response.json()
        job_id = job_data["job_id"]

        print(f"[TEST] Job {job_id} submitted (status: {job_data['status']})")

        # Poll job status
        max_wait = 30  # 30 seconds max
        poll_interval = 1
        elapsed = 0

        while elapsed < max_wait:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            status_response = await client.get(f"{API_BASE_URL}/jobs/{job_id}")
            assert status_response.status_code == 200

            status_data = status_response.json()
            current_status = status_data["status"]
            progress = status_data["progress_percent"]

            print(f"[TEST] Job status: {current_status} ({progress:.1f}% complete)")

            if current_status == "completed":
                break
            elif current_status == "failed":
                pytest.fail(f"Job failed: {status_data.get('error_message')}")

        total_time = time.time() - start_time

        assert current_status == "completed", f"Job did not complete within {max_wait}s"
        assert total_time < 30, f"Job took {total_time:.2f}s (expected < 30s)"

        # Get results
        results_response = await client.get(f"{API_BASE_URL}/jobs/{job_id}/results")
        assert results_response.status_code == 200

        results_data = results_response.json()
        assert results_data["status"] == "completed"
        assert results_data["total_entities"] == 100
        assert results_data["successful"] == 100
        assert len(results_data["results"]) == 100

        # Validate result structure
        first_result = results_data["results"][0]
        assert "entity_id" in first_result
        assert "spin_flip_probability" in first_result
        assert "predicted_state" in first_result
        assert "degree" in first_result

        print(f"\n[TEST PASSED] Batch Ising prediction completed in {total_time:.2f}s")
        print(f"[TEST PASSED] Processed {results_data['successful']} entities successfully")


@pytest.mark.asyncio
async def test_batch_ews_prediction(test_entity_ids):
    """
    Test batch EWS calculation with 100 entities
    Validates:
    - Job submission
    - Job status tracking
    - Results retrieval
    - Performance (< 30 seconds)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Submit batch job
        payload = {
            "entity_ids": test_entity_ids,
            "metrics": ["variance", "autocorrelation"],
            "window_size": 30
        }

        print(f"\n[TEST] Submitting batch EWS job for {len(test_entity_ids)} entities...")
        start_time = time.time()

        response = await client.post(
            f"{API_BASE_URL}/predict/batch/ews",
            json=payload
        )

        assert response.status_code == 202
        job_data = response.json()
        job_id = job_data["job_id"]

        print(f"[TEST] Job {job_id} submitted (status: {job_data['status']})")

        # Poll job status
        max_wait = 30
        poll_interval = 1
        elapsed = 0

        while elapsed < max_wait:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            status_response = await client.get(f"{API_BASE_URL}/jobs/{job_id}")
            assert status_response.status_code == 200

            status_data = status_response.json()
            current_status = status_data["status"]
            progress = status_data["progress_percent"]

            print(f"[TEST] Job status: {current_status} ({progress:.1f}% complete)")

            if current_status == "completed":
                break
            elif current_status == "failed":
                pytest.fail(f"Job failed: {status_data.get('error_message')}")

        total_time = time.time() - start_time

        assert current_status == "completed", f"Job did not complete within {max_wait}s"
        assert total_time < 30, f"Job took {total_time:.2f}s (expected < 30s)"

        # Get results
        results_response = await client.get(f"{API_BASE_URL}/jobs/{job_id}/results")
        assert results_response.status_code == 200

        results_data = results_response.json()
        assert results_data["status"] == "completed"
        assert results_data["total_entities"] == 100
        assert results_data["successful"] == 100
        assert len(results_data["results"]) == 100

        # Validate result structure
        first_result = results_data["results"][0]
        assert "entity_id" in first_result
        assert "variance" in first_result
        assert "autocorrelation" in first_result
        assert "critical_slowing" in first_result
        assert "risk_level" in first_result

        print(f"\n[TEST PASSED] Batch EWS calculation completed in {total_time:.2f}s")
        print(f"[TEST PASSED] Processed {results_data['successful']} entities successfully")


@pytest.mark.asyncio
async def test_job_not_found():
    """Test 404 for non-existent job"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/jobs/nonexistent-job-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_parameters():
    """Test validation of invalid parameters"""
    async with httpx.AsyncClient() as client:
        # Invalid temperature
        payload = {
            "entity_ids": ["ACTOR-001"],
            "parameters": {
                "temperature": 5.0  # Invalid: > 2
            }
        }

        response = await client.post(
            f"{API_BASE_URL}/predict/batch/ising",
            json=payload
        )
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    print("Running GAP-ML-011 batch prediction tests...")
    print("Ensure Neo4j and Redis are running:")
    print("  Neo4j: bolt://localhost:7687")
    print("  Redis: redis://localhost:6379")
    print("\nStart server first: python src/api/batch_prediction_server.py")
    print("\nRun tests: pytest tests/test_batch_prediction_api.py -v")
