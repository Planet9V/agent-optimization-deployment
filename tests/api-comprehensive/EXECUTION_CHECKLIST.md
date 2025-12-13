# API Testing Execution Checklist

## Pre-Execution Checklist

### ✅ Step 1: Container Verification (2 minutes)

```bash
# Check container is running
□ docker ps | grep api-container

# Expected: Container shows as "Up"
# If not running: docker start api-container
```

### ✅ Step 2: Middleware Fix Verification (1 minute)

```bash
# Verify bodyParser middleware is in place
□ grep -A 5 "bodyParser" server.js

# Expected: Should see bodyParser.json() and bodyParser.urlencoded()
# If missing: Apply middleware fix first
```

### ✅ Step 3: API Health Check (1 minute)

```bash
# Test API is responding
□ curl http://localhost:3000/api/health

# Expected: 200 OK response
# If failed: Check server logs with docker logs api-container
```

### ✅ Step 4: Dependencies Installation (1 minute)

```bash
# Navigate to test directory
□ cd tests/api-comprehensive

# Install dependencies
□ npm install

# Expected: Dependencies installed without errors
```

### ✅ Step 5: Qdrant Setup (Optional, 2 minutes)

```bash
# Start Qdrant container
□ docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

# Verify Qdrant is running
□ curl http://localhost:6333/collections

# Expected: JSON response with collections
# If failed: Can skip this step, results will still save to files
```

## Execution Checklist

### 🚀 Step 6: Run Complete Test Suite (3-5 minutes)

```bash
# Execute all 232 API tests
□ ./run-tests.sh --all

# Expected output:
# ✅ API is available
# 📦 Testing NER APIs...
# 📦 Testing SBOM APIs...
# ... (continues for all categories)
# ============================================================
# 📊 TEST SUMMARY
# ============================================================
# Total Tests: 232
# ✅ Passed: XXX (XX.XX%)
# ❌ Failed: XX (X.XX%)
# ⚠️ Errors: X (X.XX%)
# ⏱️ Total Time: XXX.XXs
# ============================================================
```

### 📊 Step 7: Review Results (5 minutes)

```bash
# View summary report
□ cat results/COMPLETE_API_TEST_RESULTS.md | head -100

# Check for failures
□ jq '.[] | select(.status != "PASS")' results/results-*.json | tail -1 | head -20

# Review performance
□ jq 'sort_by(.response_time) | reverse | .[0:10]' results/results-*.json | tail -1

# Expected:
# - Pass rate > 90%
# - Average response time < 500ms
# - Detailed failure information available
```

### 💾 Step 8: Store in Qdrant (2 minutes)

```bash
# Find latest results file
□ LATEST=$(ls -t results/results-*.json | head -1)

# Store in Qdrant
□ npx ts-node qdrant-storage.ts store "$LATEST"

# Get statistics
□ npx ts-node qdrant-storage.ts stats

# Expected:
# ✅ All results stored in Qdrant
# Statistics showing test breakdown
```

### 📈 Step 9: Analysis and Reporting (5 minutes)

```bash
# Generate category breakdown
□ jq -r '.[] | .category' results/results-*.json | tail -1 | sort | uniq -c

# Check failed tests by category
□ jq -r '.[] | select(.status != "PASS") | .category' results/results-*.json | tail -1 | sort | uniq -c

# Get slowest endpoints
□ jq 'sort_by(.response_time) | reverse | .[0:10] | .[] | {endpoint: .endpoint, time: .response_time}' results/results-*.json | tail -1

# Expected: Clear breakdown of results by category and performance
```

## Post-Execution Checklist

### ✅ Step 10: Document Findings (10 minutes)

```bash
# Copy main report to docs
□ cp results/COMPLETE_API_TEST_RESULTS.md ../../docs/API_TEST_RESULTS_$(date +%Y%m%d).md

# Expected: Report saved for reference
```

### ✅ Step 11: Identify Issues (Variable)

```bash
# List all failed tests with details
□ jq '.[] | select(.status != "PASS") | {category, endpoint, status, error}' results/results-*.json | tail -1

# Expected: Clear list of issues to address
```

### ✅ Step 12: Create Action Items (10 minutes)

Based on results, create issues for:

```
□ Fix all 5xx server errors (highest priority)
□ Review 4xx client errors (verify if expected or bug)
□ Optimize slow endpoints (>1000ms response time)
□ Document any expected failures
□ Plan retest after fixes
```

## Success Criteria Verification

### Overall Metrics

```
□ Total APIs tested: 232 ✓
□ Pass rate: ___% (Target: > 95%)
□ Average response time: ___ms (Target: < 200ms)
□ Server errors (5xx): ___% (Target: 0%)
□ Total test time: ___s (Target: < 300s)
```

### Category Metrics

```
□ NER APIs: ___/5 passed (Target: 100%)
□ SBOM APIs: ___/32 passed (Target: > 95%)
□ Vendor Equipment APIs: ___/28 passed (Target: > 90%)
□ Threat Intel APIs: ___/27 passed (Target: > 95%)
□ Risk Scoring APIs: ___/26 passed (Target: > 95%)
□ Remediation APIs: ___/29 passed (Target: > 90%)
□ Compliance APIs: ___/28 passed (Target: > 95%)
□ Scanning APIs: ___/30 passed (Target: > 90%)
□ Alerts APIs: ___/32 passed (Target: > 95%)
□ Economic APIs: ___/26 passed (Target: > 90%)
□ Demographics APIs: ___/24 passed (Target: > 90%)
□ Prioritization APIs: ___/28 passed (Target: > 95%)
□ Next.js APIs: ___/64 passed (Target: > 95%)
□ OpenSPG APIs: ___/40 passed (Target: > 90%)
```

## Deliverables Checklist

### Required Files

```
□ results/COMPLETE_API_TEST_RESULTS.md (Primary deliverable)
□ results/results-TIMESTAMP.json (Detailed results)
□ results/results-TIMESTAMP.csv (Spreadsheet export)
□ Qdrant storage completed (if using)
```

### Documentation

```
□ Test summary documented
□ Failures documented with details
□ Performance issues identified
□ Recommendations created
□ Next steps defined
```

## Troubleshooting Checklist

If tests fail to run:

```
□ Verify container is running
□ Check API health endpoint
□ Review server logs
□ Verify middleware fix
□ Check network connectivity
□ Verify dependencies installed
```

If high failure rate:

```
□ Test single category to isolate
□ Review server error logs
□ Check middleware configuration
□ Verify API endpoints exist
□ Test manually with curl
```

If Qdrant fails:

```
□ Check Qdrant container running
□ Verify port 6333 accessible
□ Test with curl
□ Restart Qdrant if needed
□ Skip Qdrant and use file results
```

## Timeline Estimate

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Pre-execution checks | 5 min | 5 min |
| Test execution | 3-5 min | 8-10 min |
| Results review | 5 min | 13-15 min |
| Qdrant storage | 2 min | 15-17 min |
| Analysis | 5 min | 20-22 min |
| Documentation | 10 min | 30-32 min |
| Action items | 10 min | 40-42 min |
| **TOTAL** | **40-42 min** | - |

## Final Sign-Off

```
□ All 232 APIs tested
□ Results documented in COMPLETE_API_TEST_RESULTS.md
□ Results stored in Qdrant (if applicable)
□ Failures documented and analyzed
□ Action items created
□ Next steps defined
□ Deliverable ready for review
```

## Notes

- Keep results files for historical comparison
- Store in version control for tracking
- Use Qdrant for long-term trend analysis
- Retest after fixes are applied
- Compare results across test runs

---

**Status**: Ready for execution
**Command**: `./run-tests.sh --all`
**Expected Duration**: 40-42 minutes total
**Primary Deliverable**: `results/COMPLETE_API_TEST_RESULTS.md`
