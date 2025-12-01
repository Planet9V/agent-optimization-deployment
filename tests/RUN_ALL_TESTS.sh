#!/bin/bash
# GAP-004 Complete Test Suite Runner
# Executes all 100 validation tests for GAP-004 schema

echo "=========================================="
echo "GAP-004 VALIDATION TEST SUITE"
echo "Total Tests: 100 (5 suites x 20 tests)"
echo "=========================================="
echo ""

# Test configuration
NEO4J_CONTAINER="openspg-neo4j"
NEO4J_USER="neo4j"
NEO4J_PASS="neo4j@openspg"
TEST_DIR="/home/jim/2_OXOT_Projects_Dev/tests"
RESULTS_DIR="${TEST_DIR}/results"

# Create results directory
mkdir -p "${RESULTS_DIR}"

# Test suite files
declare -a TEST_SUITES=(
    "gap004_schema_validation_tests.cypher:Schema Validation"
    "gap004_uc2_cyber_physical_tests.cypher:UC2 Cyber-Physical"
    "gap004_uc3_cascade_tests.cypher:UC3 Cascade Analysis"
    "gap004_r6_temporal_tests.cypher:R6 Temporal Management"
    "gap004_cg9_operational_tests.cypher:CG9 Operational Metrics"
)

# Initialize counters
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
START_TIME=$(date +%s)

# Run each test suite
for suite in "${TEST_SUITES[@]}"; do
    IFS=':' read -r test_file test_name <<< "$suite"

    echo "=========================================="
    echo "Running: ${test_name}"
    echo "File: ${test_file}"
    echo "=========================================="

    SUITE_START=$(date +%s)

    # Run tests
    docker exec "${NEO4J_CONTAINER}" \
        cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASS}" \
        --format plain \
        < "${TEST_DIR}/${test_file}" \
        > "${RESULTS_DIR}/${test_file%.cypher}_results.txt" 2>&1

    EXIT_CODE=$?
    SUITE_END=$(date +%s)
    SUITE_TIME=$((SUITE_END - SUITE_START))

    # Parse results
    PASS_COUNT=$(grep -c "PASS" "${RESULTS_DIR}/${test_file%.cypher}_results.txt" 2>/dev/null || echo 0)
    FAIL_COUNT=$(grep -c "FAIL" "${RESULTS_DIR}/${test_file%.cypher}_results.txt" 2>/dev/null || echo 0)

    echo "Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed"
    echo "Execution time: ${SUITE_TIME}s"
    echo ""

    TOTAL_TESTS=$((TOTAL_TESTS + 20))
    TOTAL_PASSED=$((TOTAL_PASSED + PASS_COUNT))
    TOTAL_FAILED=$((TOTAL_FAILED + FAIL_COUNT))
done

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

# Generate summary report
echo "=========================================="
echo "TEST EXECUTION SUMMARY"
echo "=========================================="
echo "Total Tests: ${TOTAL_TESTS}"
echo "Passed: ${TOTAL_PASSED}"
echo "Failed: ${TOTAL_FAILED}"
echo "Success Rate: $(awk "BEGIN {printf \"%.2f\", (${TOTAL_PASSED}/${TOTAL_TESTS})*100}")%"
echo "Total Execution Time: ${TOTAL_TIME}s"
echo "=========================================="
echo ""

# Create detailed summary file
SUMMARY_FILE="${RESULTS_DIR}/test_summary_$(date +%Y%m%d_%H%M%S).txt"
cat > "${SUMMARY_FILE}" << EOF
GAP-004 Validation Test Suite Summary
Generated: $(date)

OVERALL RESULTS
===============
Total Tests: ${TOTAL_TESTS}
Passed: ${TOTAL_PASSED}
Failed: ${TOTAL_FAILED}
Success Rate: $(awk "BEGIN {printf \"%.2f\", (${TOTAL_PASSED}/${TOTAL_TESTS})*100}")%
Execution Time: ${TOTAL_TIME}s

SUITE BREAKDOWN
===============
$(for suite in "${TEST_SUITES[@]}"; do
    IFS=':' read -r test_file test_name <<< "$suite"
    PASS=$(grep -c "PASS" "${RESULTS_DIR}/${test_file%.cypher}_results.txt" 2>/dev/null || echo 0)
    FAIL=$(grep -c "FAIL" "${RESULTS_DIR}/${test_file%.cypher}_results.txt" 2>/dev/null || echo 0)
    echo "${test_name}: ${PASS}/20 passed"
done)

DETAILED RESULTS
================
See individual result files in: ${RESULTS_DIR}/

Test Files:
$(ls -1 ${RESULTS_DIR}/*_results.txt)

EOF

echo "Detailed summary saved to: ${SUMMARY_FILE}"
echo ""

# Exit with failure if any tests failed
if [ ${TOTAL_FAILED} -gt 0 ]; then
    echo "WARNING: ${TOTAL_FAILED} test(s) failed!"
    exit 1
else
    echo "SUCCESS: All tests passed!"
    exit 0
fi
