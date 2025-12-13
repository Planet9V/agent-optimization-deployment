# Comprehensive API Testing Framework

Systematic testing of all 232 APIs after middleware fixes.

## Overview

This framework provides:
- **Complete API Inventory**: All 232 endpoints across 14 categories
- **Automated Testing**: TypeScript-based testing framework
- **Detailed Reporting**: Markdown, JSON, and CSV outputs
- **Qdrant Integration**: Store and analyze results in vector database
- **Category Testing**: Test specific API categories
- **Progress Tracking**: Real-time testing progress

## API Categories

| Category | Count | Base Path |
|----------|-------|-----------|
| NER | 5 | `/api/ner` |
| SBOM | 32 | `/api/sbom` |
| Vendor Equipment | 28 | `/api/vendor-equipment` |
| Threat Intel | 27 | `/api/threat-intel` |
| Risk Scoring | 26 | `/api/risk-scoring` |
| Remediation | 29 | `/api/remediation` |
| Compliance | 28 | `/api/compliance` |
| Scanning | 30 | `/api/scanning` |
| Alerts | 32 | `/api/alerts` |
| Economic | 26 | `/api/economic` |
| Demographics | 24 | `/api/demographics` |
| Prioritization | 28 | `/api/prioritization` |
| Next.js | 64 | `/api` |
| OpenSPG | 40 | `/api/openspg` |
| **TOTAL** | **232** | - |

## Prerequisites

```bash
# Install dependencies
npm install axios @qdrant/js-client-rest

# Ensure API is running
curl http://localhost:3000/api/health

# Ensure Qdrant is running (optional)
docker run -p 6333:6333 qdrant/qdrant
```

## Quick Start

### Test All APIs

```bash
# Run all 232 API tests
cd tests/api-comprehensive
./run-tests.sh

# Or directly with TypeScript
npx ts-node test-all-apis.ts
```

### Test Specific Category

```bash
# Test SBOM APIs only
./run-tests.sh --category sbom

# Test Next.js APIs only
npx ts-node test-all-apis.ts nextjs
```

### Check API Availability

```bash
./run-tests.sh --check
```

## Test Results

### Output Files

All results are saved to `results/` directory:

1. **Markdown Report**: `COMPLETE_API_TEST_RESULTS.md`
   - Overall summary
   - Category summaries
   - Detailed results
   - Failed test details
   - Recommendations

2. **JSON Results**: `results-TIMESTAMP.json`
   - Raw test data
   - Full response schemas
   - Complete error information

3. **CSV Export**: `results-TIMESTAMP.csv`
   - Spreadsheet-friendly format
   - For analysis in Excel/Google Sheets

### Result Structure

Each test result includes:
- **Category**: API category name
- **Endpoint**: API endpoint path
- **Method**: HTTP method (GET, POST, PUT, DELETE)
- **URL**: Full request URL
- **Status**: PASS, FAIL, or ERROR
- **HTTP Status**: Response status code
- **Response Time**: Request duration in ms
- **Error**: Error message (if applicable)
- **Response Schema**: Structure of response data
- **Timestamp**: When test was executed

## Qdrant Integration

### Store Results

```bash
# Store latest results in Qdrant
npx ts-node qdrant-storage.ts store results/results-latest.json
```

### Query Results

```bash
# Query by category
npx ts-node qdrant-storage.ts query sbom

# Get all failed tests
npx ts-node qdrant-storage.ts failed

# Get test statistics
npx ts-node qdrant-storage.ts stats
```

### Qdrant Collection Schema

```typescript
{
  collection_name: "api_test_results",
  vectors: {
    size: 384,
    distance: "Cosine"
  },
  payload: {
    category: string,
    endpoint: string,
    method: string,
    url: string,
    status: "PASS" | "FAIL" | "ERROR",
    http_status?: number,
    response_time?: number,
    error?: string,
    response_schema?: any,
    timestamp: string,
    test_run_id: string,
    stored_at: string
  }
}
```

## Test Execution Process

### 1. Pre-Test Validation

```bash
# Verify container is running
docker ps | grep api-container

# Verify middleware fix is applied
curl http://localhost:3000/api/health

# Check Qdrant availability (optional)
curl http://localhost:6333/collections
```

### 2. Run Tests

```bash
# Full test suite
./run-tests.sh

# Progress will show:
📦 Testing NER APIs...
  ✅ [1/5] POST /extract (234ms) - PASS
  ✅ [2/5] GET /entities (123ms) - PASS
  ❌ [3/5] POST /analyze (456ms) - FAIL
  ...
```

### 3. Review Results

```bash
# View markdown report
cat results/COMPLETE_API_TEST_RESULTS.md

# View JSON for detailed analysis
jq '.[] | select(.status != "PASS")' results/results-latest.json

# Open CSV in spreadsheet
libreoffice results/results-latest.csv
```

### 4. Store in Qdrant

```bash
# Store for long-term analysis
npx ts-node qdrant-storage.ts store results/results-latest.json

# Query and analyze
npx ts-node qdrant-storage.ts stats
```

## Interpreting Results

### Test Status Meanings

- **✅ PASS**: API responded with 2xx status code successfully
- **❌ FAIL**: API responded with 4xx client error (bad request format)
- **⚠️ ERROR**: API responded with 5xx server error or network failure

### Common Failure Reasons

1. **404 Not Found**: Endpoint not implemented yet
2. **400 Bad Request**: Invalid request payload
3. **401 Unauthorized**: Missing authentication
4. **500 Internal Server Error**: Server-side bug
5. **Connection Refused**: API not running
6. **Timeout**: API took longer than 5 seconds

### Recommended Actions

1. **Fix Failed Tests First**: These are client-side issues
   - Review request format
   - Check required parameters
   - Verify authentication

2. **Fix Error Tests Next**: These are server-side issues
   - Check server logs
   - Debug middleware
   - Fix route handlers

3. **Optimize Slow Tests**: Response time > 1000ms
   - Add caching
   - Optimize database queries
   - Review business logic

## Environment Variables

```bash
# API base URL (default: http://localhost:3000)
export API_BASE_URL=http://localhost:3000

# Qdrant URL (default: http://localhost:6333)
export QDRANT_URL=http://localhost:6333
```

## Test Categories in Detail

### NER APIs (5 endpoints)
Named Entity Recognition services

### SBOM APIs (32 endpoints)
Software Bill of Materials management

### Vendor Equipment APIs (28 endpoints)
Vendor and equipment tracking

### Threat Intel APIs (27 endpoints)
Threat intelligence feeds and analysis

### Risk Scoring APIs (26 endpoints)
Risk assessment and scoring

### Remediation APIs (29 endpoints)
Vulnerability remediation planning

### Compliance APIs (28 endpoints)
Compliance frameworks and controls

### Scanning APIs (30 endpoints)
Security and vulnerability scanning

### Alerts APIs (32 endpoints)
Alert management and notifications

### Economic APIs (26 endpoints)
Economic data and indicators

### Demographics APIs (24 endpoints)
Demographic statistics and analysis

### Prioritization APIs (28 endpoints)
Task and issue prioritization

### Next.js APIs (64 endpoints)
Next.js application APIs

### OpenSPG APIs (40 endpoints)
Knowledge graph APIs

## Advanced Usage

### Custom Test Scenarios

```typescript
import { ComprehensiveAPITester } from './test-all-apis';

const tester = new ComprehensiveAPITester('http://custom-url:3000');

// Test specific category
await tester.testCategoryOnly('sbom');

// Run all tests
await tester.runAllTests();
```

### Batch Testing Multiple Environments

```bash
# Test dev, staging, and production
for env in dev staging prod; do
  export API_BASE_URL="https://api-${env}.example.com"
  ./run-tests.sh
  mv results/COMPLETE_API_TEST_RESULTS.md results/results-${env}.md
done
```

### Continuous Testing

```bash
# Add to crontab for hourly testing
0 * * * * cd /path/to/tests/api-comprehensive && ./run-tests.sh
```

## Troubleshooting

### Tests Not Running

```bash
# Check TypeScript compilation
npx tsc --noEmit test-all-apis.ts

# Check dependencies
npm install

# Verify API is accessible
curl -v http://localhost:3000/api/health
```

### Qdrant Connection Issues

```bash
# Check Qdrant is running
docker ps | grep qdrant

# Test connection
curl http://localhost:6333/collections

# Restart Qdrant
docker restart qdrant-container
```

### High Failure Rate

1. Check middleware fixes are applied
2. Verify API is fully started
3. Review server logs
4. Test individual endpoints manually

## Performance Benchmarks

Expected performance:
- **Total test time**: 2-5 minutes for all 232 APIs
- **Average response time**: < 200ms per API
- **Success rate**: > 95% after middleware fixes
- **Parallel execution**: Supports concurrent testing

## Integration with CI/CD

```yaml
# Example GitHub Actions workflow
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start API
        run: docker-compose up -d
      - name: Run API Tests
        run: |
          cd tests/api-comprehensive
          ./run-tests.sh
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: tests/api-comprehensive/results/
```

## Support

For issues or questions:
1. Review test results in `COMPLETE_API_TEST_RESULTS.md`
2. Check server logs for errors
3. Verify middleware fixes are applied
4. Run individual category tests for isolation

## License

Part of the OXOT API Testing Suite
