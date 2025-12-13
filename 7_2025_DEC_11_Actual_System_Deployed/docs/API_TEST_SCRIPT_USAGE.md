# Comprehensive API Test Script - Usage Guide

**Created:** 2025-12-12 14:55:00
**Script:** `/scripts/test_all_232_apis.sh`
**Storage:** `/scripts/store_test_results_qdrant.py`

---

## Overview

Comprehensive automated testing script for ALL 232 API endpoints across 3 services:

- **ner11-gold-api** (Port 8000): 128 endpoints
- **aeon-saas-dev** (Port 3000): 64 endpoints
- **openspg-server** (Port 8887): 40 endpoints (estimated)

---

## Quick Start

### 1. Run Complete Test Suite

```bash
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed

# Execute all 232 API tests
./scripts/test_all_232_apis.sh
```

### 2. Results Files Generated

After execution, you'll get:

- **Markdown Report:** `/docs/test_results_[timestamp].md`
- **JSON Data:** `/tmp/api_test_[timestamp].json`
- **Detail Log:** `/tmp/api_test_detail_[timestamp].log`

### 3. Automatic Qdrant Storage

Results are automatically stored in Qdrant:
- **Collection:** `api-fixes`
- **Namespace:** `api-fixes/test-script`

---

## Script Features

### Test Execution

✅ **Comprehensive Coverage**
- Tests ALL 232 endpoints
- Organized by service and category
- HTTP status code validation
- Response time measurement

✅ **Detailed Classification**
- ✅ **PASS:** 2xx status codes
- ⚠️ **CLIENT_ERROR:** 4xx status codes
- ❌ **SERVER_ERROR:** 5xx status codes
- ❌ **ERROR:** Timeouts and failures

✅ **Multi-Format Output**
- Color-coded console output
- Structured markdown report
- JSON data for analysis
- Detailed execution logs

### Data Storage

All test results are stored in Qdrant with:

**Summary Points:**
- Overall test statistics
- Pass/fail rates
- Execution metadata

**Individual Test Points:**
- Each API test result
- HTTP codes and response times
- Service and category tags

**Grouped Summaries:**
- By status (PASS, FAIL, ERROR)
- By service (backend, frontend, openspg)
- By category (SBOM, Risk, Threat Intel, etc.)

---

## Service Breakdown

### Service 1: ner11-gold-api (128 endpoints)

**Categories:**
- SBOM Analysis: 34 endpoints
- Vendor & Equipment: 23 endpoints
- Threat Intelligence: 20 endpoints
- Risk Management: 21 endpoints
- Remediation Management: 25 endpoints
- NER & Search: 5 endpoints

**Authentication:**
```bash
-H 'x-customer-id: dev'
-H 'x-namespace: default'
-H 'Content-Type: application/json'
```

### Service 2: aeon-saas-dev (64 endpoints)

**Categories:**
- Pipeline Management: 5 endpoints
- Query Control: 9 endpoints
- Dashboard & Metrics: 3 endpoints
- Search & Chat: 3 endpoints
- Threat Intelligence: 6 endpoints
- Customer Management: 5 endpoints
- Tag Management: 8 endpoints
- Analytics: 6 endpoints
- Observability: 4 endpoints
- Graph & Neo4j: 4 endpoints
- System: 4 endpoints

**Authentication:**
- Clerk-based (Next.js middleware)
- Session cookies

### Service 3: openspg-server (40 endpoints - estimated)

**Categories:**
- Schema Management: ~8 endpoints
- Entity Management: ~10 endpoints
- Knowledge Graph Query: ~6 endpoints
- System: ~3 endpoints

**Note:** OpenSPG requires authentication. Only public endpoints tested.

---

## Reading Test Results

### Markdown Report Structure

```markdown
# COMPREHENSIVE API TEST RESULTS - ALL 232 ENDPOINTS

## EXECUTIVE SUMMARY
- Total Tests: 232
- Passed: XX (XX%)
- Failed: XX
- Errors: XX

## DETAILED TEST RESULTS
| # | API Name | Category | Service | Status | HTTP | Time | Endpoint |
|---|----------|----------|---------|--------|------|------|----------|
| 1 | Create SBOM | SBOM | backend | ✅ PASS | 200 | 0.12s | POST /api/v2/sbom/sboms |
...

## JSON TEST DATA
[Full JSON array of all test results]
```

### JSON Data Format

```json
[
  {
    "test_number": 1,
    "description": "Create new SBOM",
    "category": "SBOM",
    "service": "backend",
    "method": "POST",
    "endpoint": "/api/v2/sbom/sboms",
    "status": "PASS",
    "http_code": "200",
    "response_time": "0.123s",
    "timestamp": "2025-12-12 14:30:15"
  }
]
```

---

## Querying Qdrant Results

### Using Python

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Search for failed tests
results = client.search(
    collection_name="api-fixes",
    query_text="failed server error",
    limit=10,
    query_filter={
        "must": [
            {"key": "namespace", "match": {"value": "api-fixes/test-script"}},
            {"key": "status", "match": {"value": "SERVER_ERROR"}}
        ]
    }
)

for hit in results:
    print(f"{hit.payload['description']}: {hit.payload['http_code']}")
```

### Using REST API

```bash
# Get test summary
curl -X POST "http://localhost:6333/collections/api-fixes/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "type", "match": {"value": "test_summary"}},
        {"key": "namespace", "match": {"value": "api-fixes/test-script"}}
      ]
    },
    "limit": 1
  }'

# Get failed tests by service
curl -X POST "http://localhost:6333/collections/api-fixes/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "type", "match": {"value": "test_result"}},
        {"key": "service", "match": {"value": "backend"}},
        {"key": "status", "match": {"value": "SERVER_ERROR"}}
      ]
    },
    "limit": 100
  }'
```

---

## Customization

### Test Specific Services

Edit the script to comment out services you don't want to test:

```bash
# Comment out Service 2 tests
# echo "Testing aeon-saas-dev..."
# test_api "GET" "/api/health" ...
```

### Change Timeouts

Default timeout is 30 seconds per API. To change:

```bash
# Find this line in the script:
CMD="curl ... --max-time 30"

# Change to:
CMD="curl ... --max-time 60"  # 60 second timeout
```

### Modify Test Data

Edit the JSON payloads in the script:

```bash
# Current:
test_api "POST" "/api/v2/sbom/sboms" "Create SBOM" '{"name":"test-sbom"}' "backend" "SBOM"

# Custom:
test_api "POST" "/api/v2/sbom/sboms" "Create SBOM" '{"name":"my-custom-sbom","format":"spdx"}' "backend" "SBOM"
```

---

## Troubleshooting

### Services Not Running

**Error:** `Connection refused`

**Solution:**
```bash
# Check service status
docker ps | grep -E "ner11-gold-api|aeon-saas-dev|openspg-server"

# Start services if needed
docker-compose up -d
```

### Authentication Failures

**Error:** `401 Unauthorized` or `403 Forbidden`

**Solution:**
```bash
# Update customer ID in script
CUSTOMER_ID="your-customer-id"

# Or set environment variable
export CUSTOMER_ID="your-customer-id"
./scripts/test_all_232_apis.sh
```

### Qdrant Storage Fails

**Error:** `Connection refused to localhost:6333`

**Solution:**
```bash
# Check Qdrant status
curl http://localhost:6333/

# Start Qdrant if needed
docker start qdrant
```

### Missing Dependencies

**Error:** `jq: command not found`

**Solution:**
```bash
sudo apt-get update
sudo apt-get install -y jq curl
```

---

## Performance Considerations

### Execution Time

- **Full suite:** ~15-20 minutes (232 tests × 30s timeout)
- **Backend only:** ~6-8 minutes (128 tests)
- **Frontend only:** ~3-4 minutes (64 tests)

### Resource Usage

- **Network:** Moderate (local services)
- **CPU:** Low
- **Memory:** Low (<100MB)
- **Disk:** Minimal (logs ~5MB)

### Optimization Tips

1. **Run in parallel** (advanced):
   ```bash
   # Split by service and run in background
   ./test_backend.sh &
   ./test_frontend.sh &
   wait
   ```

2. **Reduce timeouts** for faster feedback:
   ```bash
   # Change --max-time from 30 to 10
   ```

3. **Test critical paths first**:
   ```bash
   # Reorder tests to put high-priority APIs first
   ```

---

## Integration with CI/CD

### GitHub Actions

```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test-apis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start services
        run: docker-compose up -d
      - name: Wait for services
        run: sleep 30
      - name: Run API tests
        run: ./scripts/test_all_232_apis.sh
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: docs/test_results_*.md
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Test APIs') {
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 30'
                sh './scripts/test_all_232_apis.sh'
            }
        }
        stage('Store Results') {
            steps {
                archiveArtifacts artifacts: 'docs/test_results_*.md'
            }
        }
    }
}
```

---

## Advanced Usage

### Store Results Manually

```bash
# If automatic storage fails, run manually:
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/store_test_results_qdrant.py \
  --results-file /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/test_results_2025-12-12_14-30-00.md \
  --json-file /tmp/api_test_2025-12-12_14-30-00.json \
  --collection api-fixes \
  --query
```

### Query Stored Results

```bash
# Add --query flag to see sample queries
python3 ./scripts/store_test_results_qdrant.py \
  --results-file ./docs/test_results_latest.md \
  --json-file /tmp/api_test_latest.json \
  --query
```

### Export Results to CSV

```bash
# Convert JSON to CSV
cat /tmp/api_test_*.json | jq -r '.[] | [.test_number, .description, .status, .http_code, .response_time] | @csv' > results.csv
```

---

## Maintenance

### Update API Inventory

When new APIs are added:

1. Update `/docs/API_COMPLETE_INVENTORY.md`
2. Add test cases to script:
   ```bash
   test_api "GET" "/api/v2/new/endpoint" "New API" "" "backend" "New Category"
   ```
3. Update this documentation

### Archive Old Results

```bash
# Move old results to archive
mkdir -p /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/archive
mv /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/test_results_*.md /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/archive/
```

---

## Summary

✅ **Created:**
- `test_all_232_apis.sh` - Comprehensive test script (34KB)
- `store_test_results_qdrant.py` - Qdrant storage script
- This usage guide

✅ **Features:**
- Tests ALL 232 endpoints
- Color-coded output
- Multiple output formats
- Automatic Qdrant storage
- Detailed logging

✅ **Next Steps:**
1. Run the test script
2. Review results in generated markdown
3. Query Qdrant for analysis
4. Fix failing APIs systematically

---

**Document Status:** Complete
**Last Updated:** 2025-12-12 14:55:00
**Stored in Qdrant:** api-fixes/test-script
