# GAP-004 Test Suite - Quick Start Guide

## 🚀 Run All Tests (One Command)

```bash
cd /home/jim/2_OXOT_Projects_Dev/tests

for test in gap004_*.cypher; do
  echo "=========================================="
  echo "Running: $test"
  echo "=========================================="
  docker exec openspg-neo4j cypher-shell \
    -u neo4j -p "neo4j@openspg" \
    --format plain < "$test" 2>&1 | tee "results_${test%.cypher}.log"
  echo ""
done

echo "All tests complete. Check results_*.log files."
```

## 📊 Individual Test Suites

### 1. Schema Validation (20 tests)
```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  < gap004_schema_validation_tests.cypher
```

### 2. Cyber-Physical Systems (20 tests)
```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  < gap004_uc2_cyber_physical_tests.cypher
```

### 3. Cascade Analysis (20 tests)
```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  < gap004_uc3_cascade_tests.cypher
```

### 4. Temporal Management (20 tests)
```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  < gap004_r6_temporal_tests.cypher
```

### 5. Operational Metrics (20 tests)
```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  < gap004_cg9_operational_tests.cypher
```

## 📈 Check Results

```bash
# Count PASS/FAIL in all result logs
grep -h "PASS\|FAIL" results_*.log | sort | uniq -c

# View specific test results
cat results_gap004_schema_validation_tests.log
```

## 🔍 Verify Schema Before Testing

```bash
# Count constraints
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  "SHOW CONSTRAINTS;"

# Count indexes
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  "SHOW INDEXES;"

# Verify APOC is installed
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  "RETURN apoc.version() AS apoc_version;"
```

## ⚡ Quick Test Sample

Run one test query to verify connectivity:

```bash
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p "neo4j@openspg" \
  "CREATE (test:TestNode {id: 'test123'})
   MATCH (t:TestNode {id: 'test123'})
   DELETE t
   RETURN 'Connection OK' AS status;"
```

## 📋 Expected Output

Each test returns results like:
```
test_1_result | test_1_description
PASS          | Verify all 34 constraints exist
```

## 🎯 Success Criteria

- **Total Tests**: 100
- **Expected PASS**: 100
- **Expected FAIL**: 0
- **Execution Time**: ~2-5 minutes total

## 🐛 Troubleshooting

**Issue**: `no procedure with the name db.constraints`
- **Solution**: Use `SHOW CONSTRAINTS` instead (Neo4j 4.x+)

**Issue**: JSON parsing errors
- **Solution**: Verify APOC plugin is installed

**Issue**: No test data found
- **Solution**: Tests create their own data - no pre-population needed

**Issue**: Long-running queries
- **Solution**: 8-15 hop queries are expected to take time

## 📁 Test Files

| File | Tests | Focus |
|------|-------|-------|
| `gap004_schema_validation_tests.cypher` | 20 | Constraints & Indexes |
| `gap004_uc2_cyber_physical_tests.cypher` | 20 | Digital Twins & Sensors |
| `gap004_uc3_cascade_tests.cypher` | 20 | Failure Propagation |
| `gap004_r6_temporal_tests.cypher` | 20 | Bitemporal Queries |
| `gap004_cg9_operational_tests.cypher` | 20 | SLA & Revenue Models |

## 💡 Tips

1. Run tests in order (schema → use cases → temporal → operational)
2. Check logs for detailed error messages
3. Tests are idempotent - safe to run multiple times
4. Each suite cleans up its test data automatically
5. Use `--format plain` for readable output

## 🔄 Continuous Testing

Add to cron or CI/CD:
```bash
#!/bin/bash
cd /home/jim/2_OXOT_Projects_Dev/tests
for test in gap004_*.cypher; do
  docker exec openspg-neo4j cypher-shell \
    -u neo4j -p "neo4j@openspg" < "$test"
done
```

## 📞 Support

- **Documentation**: See `README.md`
- **Test Summary**: See `TEST_SUMMARY.md`
- **Neo4j Logs**: `docker logs openspg-neo4j`
- **Schema Visualization**: `CALL db.schema.visualization()`
