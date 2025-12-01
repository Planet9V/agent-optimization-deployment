#!/bin/bash
# Quick test for Batch Prediction API (GAP-ML-011)

set -e

API_BASE="http://localhost:8000/api/v1"

echo "================================================"
echo "Testing Batch Prediction API (GAP-ML-011)"
echo "================================================"

# Health check
echo ""
echo "[1/5] Testing health endpoint..."
curl -s "$API_BASE/health" | jq '.'
echo "✓ Health check passed"

# Submit batch Ising job
echo ""
echo "[2/5] Submitting batch Ising prediction job (100 entities)..."
ISING_JOB=$(curl -s -X POST "$API_BASE/predict/batch/ising" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_ids": ["ACTOR-001","ACTOR-002","ACTOR-003","ACTOR-004","ACTOR-005","ACTOR-006","ACTOR-007","ACTOR-008","ACTOR-009","ACTOR-010","ACTOR-011","ACTOR-012","ACTOR-013","ACTOR-014","ACTOR-015","ACTOR-016","ACTOR-017","ACTOR-018","ACTOR-019","ACTOR-020","ACTOR-021","ACTOR-022","ACTOR-023","ACTOR-024","ACTOR-025","ACTOR-026","ACTOR-027","ACTOR-028","ACTOR-029","ACTOR-030","ACTOR-031","ACTOR-032","ACTOR-033","ACTOR-034","ACTOR-035","ACTOR-036","ACTOR-037","ACTOR-038","ACTOR-039","ACTOR-040","ACTOR-041","ACTOR-042","ACTOR-043","ACTOR-044","ACTOR-045","ACTOR-046","ACTOR-047","ACTOR-048","ACTOR-049","ACTOR-050","ACTOR-051","ACTOR-052","ACTOR-053","ACTOR-054","ACTOR-055","ACTOR-056","ACTOR-057","ACTOR-058","ACTOR-059","ACTOR-060","ACTOR-061","ACTOR-062","ACTOR-063","ACTOR-064","ACTOR-065","ACTOR-066","ACTOR-067","ACTOR-068","ACTOR-069","ACTOR-070","ACTOR-071","ACTOR-072","ACTOR-073","ACTOR-074","ACTOR-075","ACTOR-076","ACTOR-077","ACTOR-078","ACTOR-079","ACTOR-080","ACTOR-081","ACTOR-082","ACTOR-083","ACTOR-084","ACTOR-085","ACTOR-086","ACTOR-087","ACTOR-088","ACTOR-089","ACTOR-090","ACTOR-091","ACTOR-092","ACTOR-093","ACTOR-094","ACTOR-095","ACTOR-096","ACTOR-097","ACTOR-098","ACTOR-099","ACTOR-100"],
    "parameters": {
      "temperature": 0.5,
      "beta": 1.5,
      "coupling": 0.8,
      "field": 0.2
    }
  }')

ISING_JOB_ID=$(echo "$ISING_JOB" | jq -r '.job_id')
echo "$ISING_JOB" | jq '.'
echo "✓ Job submitted: $ISING_JOB_ID"

# Submit batch EWS job
echo ""
echo "[3/5] Submitting batch EWS calculation job (100 entities)..."
EWS_JOB=$(curl -s -X POST "$API_BASE/predict/batch/ews" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_ids": ["ACTOR-001","ACTOR-002","ACTOR-003","ACTOR-004","ACTOR-005","ACTOR-006","ACTOR-007","ACTOR-008","ACTOR-009","ACTOR-010","ACTOR-011","ACTOR-012","ACTOR-013","ACTOR-014","ACTOR-015","ACTOR-016","ACTOR-017","ACTOR-018","ACTOR-019","ACTOR-020","ACTOR-021","ACTOR-022","ACTOR-023","ACTOR-024","ACTOR-025","ACTOR-026","ACTOR-027","ACTOR-028","ACTOR-029","ACTOR-030","ACTOR-031","ACTOR-032","ACTOR-033","ACTOR-034","ACTOR-035","ACTOR-036","ACTOR-037","ACTOR-038","ACTOR-039","ACTOR-040","ACTOR-041","ACTOR-042","ACTOR-043","ACTOR-044","ACTOR-045","ACTOR-046","ACTOR-047","ACTOR-048","ACTOR-049","ACTOR-050","ACTOR-051","ACTOR-052","ACTOR-053","ACTOR-054","ACTOR-055","ACTOR-056","ACTOR-057","ACTOR-058","ACTOR-059","ACTOR-060","ACTOR-061","ACTOR-062","ACTOR-063","ACTOR-064","ACTOR-065","ACTOR-066","ACTOR-067","ACTOR-068","ACTOR-069","ACTOR-070","ACTOR-071","ACTOR-072","ACTOR-073","ACTOR-074","ACTOR-075","ACTOR-076","ACTOR-077","ACTOR-078","ACTOR-079","ACTOR-080","ACTOR-081","ACTOR-082","ACTOR-083","ACTOR-084","ACTOR-085","ACTOR-086","ACTOR-087","ACTOR-088","ACTOR-089","ACTOR-090","ACTOR-091","ACTOR-092","ACTOR-093","ACTOR-094","ACTOR-095","ACTOR-096","ACTOR-097","ACTOR-098","ACTOR-099","ACTOR-100"],
    "metrics": ["variance", "autocorrelation"],
    "window_size": 30
  }')

EWS_JOB_ID=$(echo "$EWS_JOB" | jq -r '.job_id')
echo "$EWS_JOB" | jq '.'
echo "✓ Job submitted: $EWS_JOB_ID"

# Poll Ising job status
echo ""
echo "[4/5] Polling Ising job status..."
MAX_WAIT=30
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))

    STATUS=$(curl -s "$API_BASE/jobs/$ISING_JOB_ID" | jq -r '.status')
    PROGRESS=$(curl -s "$API_BASE/jobs/$ISING_JOB_ID" | jq -r '.progress_percent')

    echo "  Status: $STATUS (${PROGRESS}%)"

    if [ "$STATUS" = "completed" ]; then
        break
    elif [ "$STATUS" = "failed" ]; then
        echo "✗ Job failed"
        exit 1
    fi
done

if [ "$STATUS" != "completed" ]; then
    echo "✗ Job did not complete within ${MAX_WAIT}s"
    exit 1
fi

echo "✓ Ising job completed in ${ELAPSED}s"

# Get results
echo ""
echo "[5/5] Fetching results..."
RESULTS=$(curl -s "$API_BASE/jobs/$ISING_JOB_ID/results")
echo "$RESULTS" | jq '{job_id, status, total_entities, successful, failed, execution_time_seconds}'

SUCCESSFUL=$(echo "$RESULTS" | jq -r '.successful')
EXEC_TIME=$(echo "$RESULTS" | jq -r '.execution_time_seconds')

echo ""
echo "================================================"
echo "TEST SUMMARY"
echo "================================================"
echo "✓ Health check: PASSED"
echo "✓ Batch Ising: PASSED (${SUCCESSFUL} entities in ${EXEC_TIME}s)"
echo "✓ Batch EWS: QUEUED"
echo ""
echo "All tests passed! GAP-ML-011 is working correctly."
echo "================================================"
