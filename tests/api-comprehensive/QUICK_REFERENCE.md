# API Testing Quick Reference

## 🚀 Quick Start

```bash
# Navigate to test directory
cd tests/api-comprehensive

# Install dependencies (first time only)
npm install

# Test all 232 APIs
./run-tests.sh --all

# View results
cat results/COMPLETE_API_TEST_RESULTS.md
```

## 📋 Common Commands

### Testing

```bash
# Test all APIs
./run-tests.sh --all

# Test specific category
./run-tests.sh --category sbom

# Check API availability
./run-tests.sh --check

# Get help
./run-tests.sh --help
```

### Analysis

```bash
# View summary
cat results/COMPLETE_API_TEST_RESULTS.md | head -50

# Find failed tests
jq '.[] | select(.status != "PASS")' results/results-*.json | tail -1

# Find slowest APIs
jq 'sort_by(.response_time) | reverse | .[0:10]' results/results-*.json | tail -1

# Count by status
jq 'group_by(.status) | map({status: .[0].status, count: length})' results/results-*.json | tail -1
```

### Qdrant

```bash
# Store results
npx ts-node qdrant-storage.ts store results/results-latest.json

# Get statistics
npx ts-node qdrant-storage.ts stats

# Query category
npx ts-node qdrant-storage.ts query sbom

# Get failed tests
npx ts-node qdrant-storage.ts failed
```

## 📊 API Categories

| Category | Count | Path |
|----------|-------|------|
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

## 🎯 Test Status

- ✅ **PASS**: HTTP 2xx response
- ❌ **FAIL**: HTTP 4xx client error
- ⚠️ **ERROR**: HTTP 5xx or network error

## 📁 File Locations

```
tests/api-comprehensive/
├── api-inventory.json          # All 232 APIs
├── test-all-apis.ts            # Test framework
├── qdrant-storage.ts           # Qdrant integration
├── run-tests.sh                # Execution script
├── README.md                   # Full documentation
├── TESTING_GUIDE.md            # Step-by-step guide
└── results/                    # Test results
    ├── COMPLETE_API_TEST_RESULTS.md
    ├── results-TIMESTAMP.json
    └── results-TIMESTAMP.csv
```

## 🔧 Troubleshooting

### API Not Available

```bash
docker ps | grep api-container
curl http://localhost:3000/api/health
```

### Tests Failing

```bash
# Test one category to isolate
./run-tests.sh --category ner

# Check logs
docker logs api-container
```

### Qdrant Not Working

```bash
# Start Qdrant
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

# Test connection
curl http://localhost:6333/collections
```

## 📈 Success Criteria

- **Pass Rate**: > 95%
- **Avg Response Time**: < 200ms
- **Server Errors**: 0%
- **Total Time**: < 5 minutes

## 🔗 Resources

- **Full Docs**: `README.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Framework Summary**: `../../docs/API_TESTING_FRAMEWORK_COMPLETE.md`

## ⚡ NPM Scripts

```bash
npm test                    # Run all tests
npm run test:category sbom  # Test category
npm run store:qdrant        # Store in Qdrant
npm run stats:qdrant        # Get statistics
npm run failed:qdrant       # Get failed tests
```

## 🎯 One-Line Commands

```bash
# Complete test cycle
./run-tests.sh --all && npx ts-node qdrant-storage.ts store results/results-*.json | tail -1

# Test and view failures
./run-tests.sh --all && jq '.[] | select(.status != "PASS")' results/results-*.json | tail -1

# Quick category test
./run-tests.sh --category sbom && cat results/COMPLETE_API_TEST_RESULTS.md | grep -A 50 "### SBOM"
```
