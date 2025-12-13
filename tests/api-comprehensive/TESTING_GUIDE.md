# Complete API Testing Guide

**Objective**: Test all 232 APIs after middleware fixes are applied

## Pre-Testing Checklist

### ✅ Prerequisites

1. **Container Status**
   ```bash
   docker ps | grep api-container
   # Should show container running
   ```

2. **Middleware Fix Applied**
   ```bash
   # Verify the bodyParser middleware fix is in place
   grep -A 5 "bodyParser" server.js
   ```

3. **API Health Check**
   ```bash
   curl http://localhost:3000/api/health
   # Should return 200 OK
   ```

4. **Dependencies Installed**
   ```bash
   cd tests/api-comprehensive
   npm install
   ```

5. **Qdrant Running (Optional)**
   ```bash
   docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
   curl http://localhost:6333/collections
   ```

## Step-by-Step Testing Process

### Step 1: Verify Environment

```bash
# Navigate to test directory
cd tests/api-comprehensive

# Check API availability
./run-tests.sh --check

# Expected output:
# ✅ API is available
```

### Step 2: Run Comprehensive Tests

```bash
# Test all 232 APIs
./run-tests.sh --all

# Progress output:
📦 Testing NER APIs...
  ✅ [1/5] POST /extract (234ms) - PASS
  ✅ [2/5] GET /entities (123ms) - PASS
  ...

📦 Testing SBOM APIs...
  ✅ [1/32] POST /generate (456ms) - PASS
  ...

# Summary output:
========================================================
📊 TEST SUMMARY
========================================================
Total Tests: 232
✅ Passed: 215 (92.67%)
❌ Failed: 12 (5.17%)
⚠️ Errors: 5 (2.16%)
⏱️ Total Time: 234.56s
========================================================
```

### Step 3: Review Results

```bash
# View comprehensive markdown report
cat results/COMPLETE_API_TEST_RESULTS.md

# View JSON results for analysis
cat results/results-*.json | jq '.[] | select(.status != "PASS")'

# View CSV in spreadsheet
libreoffice results/results-*.csv
```

### Step 4: Store Results in Qdrant

```bash
# Find latest results file
LATEST=$(ls -t results/results-*.json | head -1)

# Store in Qdrant
npx ts-node qdrant-storage.ts store "$LATEST"

# Expected output:
# 📦 Storing 232 test results in Qdrant...
#   Stored batch 1/3
#   Stored batch 2/3
#   Stored batch 3/3
# ✅ All results stored in Qdrant
```

### Step 5: Query and Analyze

```bash
# Get overall statistics
npx ts-node qdrant-storage.ts stats

# Query specific category
npx ts-node qdrant-storage.ts query sbom

# Get all failed tests
npx ts-node qdrant-storage.ts failed
```

## Category-Specific Testing

### Test Individual Categories

```bash
# Test NER APIs only
./run-tests.sh --category ner

# Test SBOM APIs only
./run-tests.sh --category sbom

# Test all categories one by one
for category in ner sbom vendor_equipment threat_intel risk_scoring \
                remediation compliance scanning alerts economic \
                demographics prioritization nextjs openspg; do
  echo "Testing $category..."
  ./run-tests.sh --category "$category"
  sleep 2
done
```

### Priority Testing Order

1. **Core APIs First**
   ```bash
   ./run-tests.sh --category ner
   ./run-tests.sh --category sbom
   ```

2. **Security APIs Next**
   ```bash
   ./run-tests.sh --category threat_intel
   ./run-tests.sh --category scanning
   ./run-tests.sh --category compliance
   ```

3. **Management APIs**
   ```bash
   ./run-tests.sh --category alerts
   ./run-tests.sh --category remediation
   ./run-tests.sh --category prioritization
   ```

4. **Data APIs**
   ```bash
   ./run-tests.sh --category economic
   ./run-tests.sh --category demographics
   ```

5. **Application APIs**
   ```bash
   ./run-tests.sh --category nextjs
   ./run-tests.sh --category openspg
   ```

## Understanding Test Results

### Result Files

1. **COMPLETE_API_TEST_RESULTS.md**
   - Executive summary
   - Category breakdowns
   - Detailed test results
   - Failed test analysis
   - Recommendations

2. **results-TIMESTAMP.json**
   - Machine-readable format
   - Complete test data
   - Response schemas
   - Error details

3. **results-TIMESTAMP.csv**
   - Spreadsheet format
   - Easy filtering
   - Pivot table analysis

### Test Status Indicators

| Status | Symbol | Meaning | Action |
|--------|--------|---------|--------|
| PASS | ✅ | 2xx response | None needed |
| FAIL | ❌ | 4xx response | Fix request |
| ERROR | ⚠️ | 5xx or timeout | Fix server |

### Response Time Guidelines

- **< 100ms**: Excellent
- **100-500ms**: Good
- **500-1000ms**: Acceptable
- **> 1000ms**: Needs optimization

## Troubleshooting Common Issues

### Issue: Connection Refused

```bash
# Check API is running
curl http://localhost:3000/api/health

# Restart if needed
docker restart api-container
```

### Issue: All Tests Failing

```bash
# Verify middleware fix
cat server.js | grep -A 10 "bodyParser"

# Check server logs
docker logs api-container

# Test single endpoint manually
curl -X POST http://localhost:3000/api/ner/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
```

### Issue: High Failure Rate

```bash
# Test one category to isolate
./run-tests.sh --category ner

# Check for pattern in failures
jq '.[] | select(.status != "PASS") | .error' results/results-*.json

# Review specific category
cat results/COMPLETE_API_TEST_RESULTS.md | grep -A 20 "### NER"
```

### Issue: Qdrant Connection Failed

```bash
# Check Qdrant status
docker ps | grep qdrant

# Start Qdrant if not running
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

# Test connection
curl http://localhost:6333/collections
```

## Analysis Examples

### Find Slowest APIs

```bash
jq 'sort_by(.response_time) | reverse | .[0:10]' results/results-*.json
```

### Count Failures by Category

```bash
jq -r '.[] | select(.status != "PASS") | .category' results/results-*.json | sort | uniq -c
```

### Get All 4xx Errors

```bash
jq '.[] | select(.http_status >= 400 and .http_status < 500)' results/results-*.json
```

### Get All 5xx Errors

```bash
jq '.[] | select(.http_status >= 500)' results/results-*.json
```

### Average Response Time by Category

```bash
jq -r '.[] | "\(.category) \(.response_time)"' results/results-*.json | \
  awk '{sum[$1]+=$2; count[$1]++} END {for (cat in sum) print cat, sum[cat]/count[cat]}'
```

## Expected Results After Middleware Fix

### Success Criteria

- ✅ **Pass Rate**: > 95%
- ✅ **Average Response Time**: < 200ms
- ✅ **No 500 Errors**: 0 server errors
- ✅ **4xx Errors**: < 5% (acceptable client validation)

### Category Expectations

| Category | Expected Pass Rate | Notes |
|----------|-------------------|-------|
| NER | 100% | Core functionality |
| SBOM | > 95% | Some optional features |
| Vendor Equipment | > 90% | May have data dependencies |
| Threat Intel | > 95% | External service deps |
| All Others | > 90% | Various implementations |

## Continuous Monitoring

### Setup Automated Testing

```bash
# Create cron job
crontab -e

# Add hourly testing
0 * * * * cd /path/to/tests/api-comprehensive && ./run-tests.sh >> /var/log/api-tests.log 2>&1
```

### Alert on Failures

```bash
#!/bin/bash
# test-and-alert.sh

./run-tests.sh --all

# Check failure rate
FAILED=$(jq '[.[] | select(.status != "PASS")] | length' results/results-latest.json)

if [ "$FAILED" -gt 10 ]; then
  echo "High failure rate: $FAILED tests failed" | mail -s "API Test Alert" admin@example.com
fi
```

## Reporting

### Generate Executive Summary

```bash
# Extract key metrics
cat results/COMPLETE_API_TEST_RESULTS.md | grep -A 10 "Overall Summary"
```

### Create Trend Report

```bash
# Compare multiple test runs
for file in results/results-*.json; do
  timestamp=$(basename "$file" .json | cut -d- -f2-)
  passed=$(jq '[.[] | select(.status == "PASS")] | length' "$file")
  echo "$timestamp: $passed passed"
done
```

### Export for Presentation

```bash
# Convert to PDF
pandoc results/COMPLETE_API_TEST_RESULTS.md -o report.pdf

# Create charts
# (Use results CSV in Excel/Google Sheets for visualization)
```

## Next Steps After Testing

1. **Review Failed Tests**: Analyze and fix issues
2. **Optimize Slow APIs**: Improve response times
3. **Document Findings**: Update API documentation
4. **Plan Remediation**: Create tickets for failures
5. **Schedule Retests**: Verify fixes work

## Support and Resources

- **Test Framework**: `tests/api-comprehensive/`
- **API Inventory**: `api-inventory.json`
- **Test Script**: `test-all-apis.ts`
- **Qdrant Storage**: `qdrant-storage.ts`
- **Results**: `results/`

## Summary Checklist

- [ ] Prerequisites verified
- [ ] All 232 APIs tested
- [ ] Results reviewed and analyzed
- [ ] Results stored in Qdrant
- [ ] Failed tests documented
- [ ] Recommendations generated
- [ ] Next actions planned
