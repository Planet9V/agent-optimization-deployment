"""
ML-011 Batch Prediction Tests
Test suite for batch prediction job processing
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, List
import sys
from pathlib import Path
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.batch_prediction import (
    submit_batch_prediction,
    get_batch_job_status,
    get_batch_results,
    cancel_batch_job,
    get_job_queue_status
)
from src.models.batch_models import BatchJob, PredictionRequest


class TestML011BatchPrediction:
    """Test suite for ML-011 batch prediction functionality"""

    @pytest.fixture
    def sample_entities(self) -> List[Dict[str, Any]]:
        """Create sample entities for batch prediction"""
        return [
            {
                "entity_id": f"NET-{i:03d}",
                "type": "network",
                "features": {
                    "traffic_volume": 1000 + i * 100,
                    "connection_count": 50 + i * 5,
                    "packet_size": 512 + i * 10
                }
            }
            for i in range(100)
        ]

    def test_submit_batch_request(self, sample_entities):
        """
        Test: Submit batch request
        Expected: Job queued with job_id
        """
        result = submit_batch_prediction(
            entities=sample_entities,
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing",
            priority="normal"
        )

        assert result["success"] is True
        assert "job_id" in result
        assert result["status"] == "queued"
        assert result["entity_count"] == len(sample_entities)

    def test_job_queues(self, sample_entities):
        """
        Test: Job queues correctly
        Expected: Job appears in queue with correct status
        """
        # Submit job
        job = submit_batch_prediction(
            entities=sample_entities,
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing"
        )

        # Check queue status
        queue_status = get_job_queue_status()

        assert queue_status["success"] is True
        assert job["job_id"] in queue_status["queued_jobs"]

        job_info = queue_status["queued_jobs"][job["job_id"]]
        assert job_info["status"] in ["queued", "processing"]
        assert job_info["entity_count"] == len(sample_entities)

    def test_job_completion_time(self, sample_entities):
        """
        Test: Job completes in <1 minute for 100 entities
        Expected: Completion time < 60 seconds
        """
        # Submit job
        start_time = time.time()

        job = submit_batch_prediction(
            entities=sample_entities,
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing",
            priority="high"  # High priority for faster processing
        )

        # Poll for completion
        timeout = 60
        poll_interval = 1
        elapsed = 0

        while elapsed < timeout:
            status = get_batch_job_status(job["job_id"])

            if status["status"] == "completed":
                completion_time = time.time() - start_time
                assert completion_time < 60, f"Job took {completion_time}s, expected <60s"
                break

            elif status["status"] == "failed":
                pytest.fail(f"Job failed: {status.get('error')}")

            time.sleep(poll_interval)
            elapsed += poll_interval
        else:
            pytest.fail(f"Job did not complete within {timeout}s")

    def test_retrieve_batch_results(self, sample_entities):
        """
        Test: Results retrievable
        Expected: Complete results for all entities
        """
        # Submit and wait for completion
        job = submit_batch_prediction(
            entities=sample_entities[:10],  # Smaller batch for faster test
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing"
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

        # Retrieve results
        results = get_batch_results(job["job_id"])

        assert results["success"] is True
        assert results["job_id"] == job["job_id"]
        assert "predictions" in results
        assert len(results["predictions"]) == len(sample_entities[:10])

        # Verify each entity has predictions
        for entity in sample_entities[:10]:
            entity_result = next(
                (p for p in results["predictions"] if p["entity_id"] == entity["entity_id"]),
                None
            )
            assert entity_result is not None
            assert "prediction" in entity_result
            assert "confidence" in entity_result

    def test_batch_job_priority(self, sample_entities):
        """
        Test: Priority queue handling
        Expected: High priority jobs processed first
        """
        # Submit low priority job
        low_priority = submit_batch_prediction(
            entities=sample_entities,
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing",
            priority="low"
        )

        # Submit high priority job
        high_priority = submit_batch_prediction(
            entities=sample_entities[:20],
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing",
            priority="high"
        )

        # Wait a bit and check queue
        time.sleep(2)

        queue = get_job_queue_status()

        # High priority should be processing or completed before low priority
        high_status = get_batch_job_status(high_priority["job_id"])
        low_status = get_batch_job_status(low_priority["job_id"])

        # High priority should not still be queued if low priority is processing
        if low_status["status"] == "processing":
            assert high_status["status"] in ["completed", "processing"]

    def test_cancel_batch_job(self, sample_entities):
        """
        Test: Cancel queued or processing job
        Expected: Job status changes to cancelled
        """
        # Submit job
        job = submit_batch_prediction(
            entities=sample_entities,
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing"
        )

        # Cancel job
        cancel_result = cancel_batch_job(job["job_id"])

        assert cancel_result["success"] is True
        assert cancel_result["status"] == "cancelled"

        # Verify status
        status = get_batch_job_status(job["job_id"])
        assert status["status"] == "cancelled"

    def test_batch_job_error_handling(self):
        """
        Test: Invalid batch request handling
        Expected: Appropriate error messages
        """
        # Submit with invalid model
        result = submit_batch_prediction(
            entities=[{"entity_id": "TEST-001"}],
            model_id="nonexistent_model",
            prediction_type="critical_slowing"
        )

        assert result["success"] is False
        assert "error" in result

    def test_concurrent_batch_jobs(self, sample_entities):
        """
        Test: Multiple concurrent batch jobs
        Expected: All jobs process correctly
        """
        # Submit multiple jobs
        jobs = []
        for i in range(3):
            job = submit_batch_prediction(
                entities=sample_entities[i*30:(i+1)*30],
                model_id="ews_predictor_v1",
                prediction_type="critical_slowing",
                priority="normal"
            )
            jobs.append(job)

        # Wait for all to complete
        timeout = 90
        start_time = time.time()

        completed = []
        while len(completed) < len(jobs) and (time.time() - start_time) < timeout:
            for job in jobs:
                if job["job_id"] not in completed:
                    status = get_batch_job_status(job["job_id"])
                    if status["status"] == "completed":
                        completed.append(job["job_id"])
            time.sleep(1)

        assert len(completed) == len(jobs), "Not all jobs completed"

        # Verify all results
        for job in jobs:
            results = get_batch_results(job["job_id"])
            assert results["success"] is True
            assert len(results["predictions"]) == 30

    def test_batch_prediction_accuracy(self, sample_entities):
        """
        Test: Prediction results consistency
        Expected: Predictions include required fields and valid values
        """
        job = submit_batch_prediction(
            entities=sample_entities[:10],
            model_id="ews_predictor_v1",
            prediction_type="critical_slowing"
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

        results = get_batch_results(job["job_id"])

        for prediction in results["predictions"]:
            # Required fields
            assert "entity_id" in prediction
            assert "prediction" in prediction
            assert "confidence" in prediction
            assert "timestamp" in prediction

            # Valid values
            assert 0 <= prediction["confidence"] <= 1
            assert prediction["prediction"] in [
                "stable", "warning", "critical", "transition_imminent"
            ]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
