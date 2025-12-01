#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# COMPREHENSIVE NEO4J TEST EXECUTION - BASH IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════

set -e

CONTAINER="openspg-neo4j"
USER="neo4j"
PASS="neo4j@openspg"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests"
RESULTS_FILE="${RESULTS_DIR}/test_results_${TIMESTAMP}.md"

echo "═══════════════════════════════════════════════════════════════════════"
echo "NEO4J COMPREHENSIVE TEST SUITE EXECUTION"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Starting test execution at: $(date)"
echo "Results file: $RESULTS_FILE"
echo ""

# Initialize results file
cat > "$RESULTS_FILE" << 'EOF'
# NEO4J COMPREHENSIVE TEST SUITE RESULTS

**Test Suite**: Neo4j Database Validation
**Timestamp**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Database**: openspg-neo4j

## Executive Summary

EOF

# Function to execute a test
execute_test() {
    local test_id="$1"
    local test_name="$2"
    local query="$3"

    echo "  Executing $test_id: $test_name"

    # Execute query
    result=$(docker exec "$CONTAINER" cypher-shell -u "$USER" -p "$PASS" --format plain "$query" 2>&1 || echo "ERROR")

    # Parse result
    if [[ "$result" == *"ERROR"* ]] || [[ "$result" == *"error"* ]]; then
        status="ERROR"
        actual="N/A"
    else
        # Extract status from result (last column)
        status=$(echo "$result" | tail -1 | awk -F',' '{print $NF}' | tr -d ' "')
        actual=$(echo "$result" | tail -1 | awk -F',' '{print $(NF-1)}' | tr -d ' "')
    fi

    # Append to results
    echo "| $test_id | $test_name | $actual | $status |" >> "$RESULTS_FILE"

    # Track stats
    if [[ "$status" == "PASS" ]]; then
        ((PASSED++))
    elif [[ "$status" == "FAIL" ]]; then
        ((FAILED++))
    else
        ((ERRORS++))
    fi
}

# Initialize counters
PASSED=0
FAILED=0
ERRORS=0
TOTAL=0

# Add test results table header
cat >> "$RESULTS_FILE" << 'EOF'

## Test Results

| Test ID | Test Name | Result | Status |
|---------|-----------|--------|--------|
EOF

echo "Executing tests..."
echo ""

# TEST 001: Database populated
execute_test "TEST_001" "Database Populated" \
"MATCH (n) WITH count(n) AS total RETURN 'TEST_001', 'Database has nodes', total, CASE WHEN total > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 002: Seldon Crises exist
execute_test "TEST_002" "Seldon Crises Exist" \
"MATCH (c:SeldonCrisis) RETURN 'TEST_002', 'All 3 crises', count(c), CASE WHEN count(c) = 3 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 003: First Crisis
execute_test "TEST_003" "Great Resignation Crisis" \
"MATCH (c:SeldonCrisis {name: 'Great Resignation Cascade'}) RETURN 'TEST_003', 'First crisis', count(c), CASE WHEN count(c) = 1 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 004: Second Crisis
execute_test "TEST_004" "Supply Chain Crisis" \
"MATCH (c:SeldonCrisis {name: 'Supply Chain Collapse'}) RETURN 'TEST_004', 'Second crisis', count(c), CASE WHEN count(c) = 1 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 005: Third Crisis
execute_test "TEST_005" "Pandemic Crisis" \
"MATCH (c:SeldonCrisis {name: 'Medical Device Pandemic'}) RETURN 'TEST_005', 'Third crisis', count(c), CASE WHEN count(c) = 1 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 006: Tier property exists
execute_test "TEST_006" "Tier Property Exists" \
"MATCH (n) WHERE n.tier IS NOT NULL WITH count(n) AS total RETURN 'TEST_006', 'Nodes with tier', total, CASE WHEN total > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 007: Multiple tiers
execute_test "TEST_007" "Multiple Tiers Present" \
"MATCH (n) WHERE n.tier IS NOT NULL WITH DISTINCT n.tier AS tier WITH count(tier) AS tiers RETURN 'TEST_007', 'Distinct tiers', tiers, CASE WHEN tiers >= 3 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 008-011: Tier counts
execute_test "TEST_008" "T5 Nodes Exist" \
"MATCH (n {tier: 5}) RETURN 'TEST_008', 'T5 nodes', count(n), CASE WHEN count(n) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_009" "T7 Nodes Exist" \
"MATCH (n {tier: 7}) RETURN 'TEST_009', 'T7 nodes', count(n), CASE WHEN count(n) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_010" "T8 Nodes Exist" \
"MATCH (n {tier: 8}) RETURN 'TEST_010', 'T8 nodes', count(n), CASE WHEN count(n) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_011" "T9 Nodes Exist" \
"MATCH (n {tier: 9}) RETURN 'TEST_011', 'T9 nodes', count(n), CASE WHEN count(n) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# TEST 012-026: Entity types exist
execute_test "TEST_012" "AttackPattern Exists" \
"MATCH (a:AttackPattern) RETURN 'TEST_012', 'AttackPatterns', count(a), CASE WHEN count(a) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_013" "Control Exists" \
"MATCH (c:Control) RETURN 'TEST_013', 'Controls', count(c), CASE WHEN count(c) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_014" "ThreatActor Exists" \
"MATCH (t:ThreatActor) RETURN 'TEST_014', 'ThreatActors', count(t), CASE WHEN count(t) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_015" "Indicator Exists" \
"MATCH (i:Indicator) RETURN 'TEST_015', 'Indicators', count(i), CASE WHEN count(i) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_016" "Event Exists" \
"MATCH (e:Event) RETURN 'TEST_016', 'Events', count(e), CASE WHEN count(e) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_017" "EconomicMetric Exists" \
"MATCH (e:EconomicMetric) RETURN 'TEST_017', 'EconomicMetrics', count(e), CASE WHEN count(e) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_018" "Asset Exists" \
"MATCH (a:Asset) RETURN 'TEST_018', 'Assets', count(a), CASE WHEN count(a) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_019" "Vulnerability Exists" \
"MATCH (v:Vulnerability) RETURN 'TEST_019', 'Vulnerabilities', count(v), CASE WHEN count(v) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

execute_test "TEST_020" "Campaign Exists" \
"MATCH (c:Campaign) RETURN 'TEST_020', 'Campaigns', count(c), CASE WHEN count(c) > 0 THEN 'PASS' ELSE 'FAIL' END;"
((TOTAL++))

# Calculate pass rate
PASS_RATE=$(awk "BEGIN {printf \"%.2f\", ($PASSED / $TOTAL) * 100}")

# Add summary to top of file
sed -i "/## Executive Summary/a\\
\\
- **Total Tests**: $TOTAL\\
- **Passed**: $PASSED ✓\\
- **Failed**: $FAILED ✗\\
- **Errors**: $ERRORS ⚠\\
- **Pass Rate**: ${PASS_RATE}%\\
- **Target Pass Rate**: 95%\\
- **Target Met**: $(if (( $(echo "$PASS_RATE >= 95" | bc -l) )); then echo "YES ✓"; else echo "NO ✗"; fi)" \
"$RESULTS_FILE"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "TEST EXECUTION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo "Total Tests: $TOTAL"
echo "Passed: $PASSED ✓"
echo "Failed: $FAILED ✗"
echo "Errors: $ERRORS ⚠"
echo "Pass Rate: ${PASS_RATE}%"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Results saved to: $RESULTS_FILE"
echo ""
