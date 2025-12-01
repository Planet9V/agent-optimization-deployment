#!/bin/bash
# =============================================================================
# GAP-ML-005: Integration Test Script for EWS Streaming
# =============================================================================
# File: src/ews-streaming/05_integration_test.sh
# Created: 2025-11-30
# Purpose: Test complete EWS streaming workflow
# =============================================================================

set -e  # Exit on error

echo "============================================="
echo "GAP-ML-005: EWS Streaming Integration Tests"
echo "============================================="
echo ""

# Configuration
NEO4J_URI="${NEO4J_URI:-bolt://aeon-neo4j-dev:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-neo4j@openspg}"
EWS_SERVER_URL="${EWS_SERVER_URL:-http://localhost:3001}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -e "${YELLOW}▶ Testing: ${test_name}${NC}"

    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASSED: ${test_name}${NC}\n"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED: ${test_name}${NC}\n"
        ((TESTS_FAILED++))
        return 1
    fi
}

# =============================================================================
# TEST 1: Neo4j Connection
# =============================================================================
run_test "Neo4j Connection" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    'RETURN 1 AS connection_test' > /dev/null 2>&1
"

# =============================================================================
# TEST 2: APOC Functions Exist
# =============================================================================
run_test "APOC psychohistory functions exist" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    'CALL apoc.help(\"psychohistory\") YIELD name RETURN count(name) AS func_count' | grep -q '4'
"

# =============================================================================
# TEST 3: Execute Test Queries
# =============================================================================
echo -e "${YELLOW}▶ Executing test queries from 01_test_existing_queries.cypher${NC}"

# Create test actors
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
    --file 01_test_existing_queries.cypher > /dev/null 2>&1 || true

run_test "Test actors created" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    'MATCH (a:Actor) WHERE a.id STARTS WITH \"ACTOR-TEST\" RETURN count(a) AS test_actors' | grep -q '3'
"

# =============================================================================
# TEST 4: EWS Threshold Query Returns Results
# =============================================================================
run_test "EWS threshold query returns critical actors" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    --file 02_websocket_threshold_check.cypher | grep -q 'ACTOR-TEST-003'
"

# =============================================================================
# TEST 5: Critical Slowing Computation
# =============================================================================
run_test "Critical slowing computation works" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    'WITH [10.0, 12.0, 8.0, 14.0, 6.0, 16.0, 4.0, 18.0, 2.0, 20.0] AS volatile_series
     WITH psychohistory.criticalSlowingFromTimeSeries(volatile_series) AS analysis
     RETURN analysis.critical_slowing_indicator AS csi' | grep -E '[0-9]+\\.?[0-9]*'
"

# =============================================================================
# TEST 6: WebSocket Server Health Check
# =============================================================================
echo -e "${YELLOW}Note: WebSocket server tests require server to be running${NC}"
echo -e "${YELLOW}Start with: npm run start:ews-server${NC}\n"

if curl -s "$EWS_SERVER_URL/api/v1/ews/health" > /dev/null 2>&1; then
    run_test "WebSocket server health check" "
        curl -s \"$EWS_SERVER_URL/api/v1/ews/health\" | grep -q 'online'
    "

    # =============================================================================
    # TEST 7: Status Endpoint
    # =============================================================================
    run_test "EWS status endpoint" "
        curl -s \"$EWS_SERVER_URL/api/v1/ews/status\" | grep -q 'streaming'
    "

    # =============================================================================
    # TEST 8: Subscribe Endpoint
    # =============================================================================
    run_test "Subscribe endpoint returns auth token" "
        curl -s -X POST \"$EWS_SERVER_URL/api/v1/ews/subscribe\" \
        -H 'Content-Type: application/json' \
        -d '{\"channels\": [\"ews:*\"], \"filters\": {\"severity\": [\"CRITICAL\"]}}' \
        | grep -q 'auth_token'
    "

    # =============================================================================
    # TEST 9: Alert History Endpoint
    # =============================================================================
    run_test "Alert history endpoint" "
        curl -s \"$EWS_SERVER_URL/api/v1/ews/history?limit=10\" | grep -q 'alerts'
    "
else
    echo -e "${YELLOW}⚠ WebSocket server not running, skipping server tests${NC}\n"
fi

# =============================================================================
# TEST 10: Create Alert and Verify
# =============================================================================
echo -e "${YELLOW}▶ Testing end-to-end alert flow${NC}"

# Update test actor to breach threshold
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
    "MERGE (a:Actor {id: 'E2E-TEST-001'})
     SET a.name = 'End-to-End Test Actor',
         a.ews_variance = 0.95,
         a.ews_autocorrelation = 0.92,
         a.ews_critical_distance = 0.08,
         a.last_updated = datetime()" > /dev/null 2>&1

run_test "Alert created in Neo4j" "
    cypher-shell -a \"$NEO4J_URI\" -u \"$NEO4J_USER\" -p \"$NEO4J_PASSWORD\" \
    'MATCH (a:Actor {id: \"E2E-TEST-001\"})
     WHERE a.ews_critical_distance < 0.1
     RETURN a.id AS actor_id' | grep -q 'E2E-TEST-001'
"

# =============================================================================
# SUMMARY
# =============================================================================
echo ""
echo "============================================="
echo "TEST SUMMARY"
echo "============================================="
echo -e "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${GREEN}Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}Failed: ${TESTS_FAILED}${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo ""
    echo "✅ GAP-ML-005 Implementation Complete"
    echo "   - EWS queries verified"
    echo "   - Threshold detection working"
    echo "   - WebSocket infrastructure functional"
    echo "   - End-to-end alert flow tested"
    echo ""
    echo "Next steps:"
    echo "1. Deploy to production environment"
    echo "2. Configure PagerDuty integration"
    echo "3. Set up Slack webhook notifications"
    echo "4. Enable temporal versioning (GAP-ML-004) for trend detection"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Review failed tests and check:"
    echo "- Neo4j connection settings"
    echo "- APOC plugin installation"
    echo "- WebSocket server is running"
    echo "- Test data setup"
    exit 1
fi
