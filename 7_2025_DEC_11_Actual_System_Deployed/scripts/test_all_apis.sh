#!/bin/bash
# Comprehensive API Testing Script - All 181 APIs
# Generated: 2025-12-12
# Developer: Backend Testing Agent

set -e

# Configuration
BASE_URL_PHASE_B="http://localhost:8000"
BASE_URL_NEXTJS="http://localhost:3000"
CUSTOMER_ID="dev"
RESULTS_FILE="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/DEVELOPER_TEST_RESULTS.md"
TEMP_LOG="/tmp/api_test_log.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0
ERRORS=0

# Test function
test_api() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local port=$5

    TOTAL=$((TOTAL + 1))

    echo "Testing: $description"
    echo "  Method: $method"
    echo "  Endpoint: $endpoint"

    if [ "$port" == "3000" ]; then
        BASE_URL="$BASE_URL_NEXTJS"
        HEADERS="-H 'Content-Type: application/json'"
    else
        BASE_URL="$BASE_URL_PHASE_B"
        HEADERS="-H 'X-Customer-ID: $CUSTOMER_ID' -H 'Content-Type: application/json'"
    fi

    if [ -n "$data" ]; then
        CMD="curl -X $method '$BASE_URL$endpoint' $HEADERS -d '$data' -w '\nHTTP_STATUS:%{http_code}\nTIME:%{time_total}s\n' -s --max-time 10"
    else
        CMD="curl -X $method '$BASE_URL$endpoint' $HEADERS -w '\nHTTP_STATUS:%{http_code}\nTIME:%{time_total}s\n' -s --max-time 10"
    fi

    echo "  Command: $CMD" >> $TEMP_LOG

    RESPONSE=$(eval $CMD 2>&1)
    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
    TIME=$(echo "$RESPONSE" | grep "TIME" | cut -d: -f2)
    BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS/,$d')

    echo "  Status: $HTTP_CODE (${TIME})" >> $TEMP_LOG
    echo "  Response: $BODY" >> $TEMP_LOG
    echo "" >> $TEMP_LOG

    # Classify result
    if [[ "$HTTP_CODE" =~ ^2[0-9][0-9]$ ]]; then
        echo -e "  ${GREEN}✅ PASS${NC} ($HTTP_CODE in ${TIME})"
        PASSED=$((PASSED + 1))
        echo "| $TOTAL | $description | ✅ PASS | $HTTP_CODE | ${TIME} | $method $endpoint |" >> $RESULTS_FILE
    elif [[ "$HTTP_CODE" =~ ^4[0-9][0-9]$ ]]; then
        echo -e "  ${YELLOW}⚠️ CLIENT ERROR${NC} ($HTTP_CODE in ${TIME})"
        FAILED=$((FAILED + 1))
        echo "| $TOTAL | $description | ⚠️ CLIENT ERROR | $HTTP_CODE | ${TIME} | $method $endpoint |" >> $RESULTS_FILE
    elif [[ "$HTTP_CODE" =~ ^5[0-9][0-9]$ ]]; then
        echo -e "  ${RED}❌ SERVER ERROR${NC} ($HTTP_CODE in ${TIME})"
        ERRORS=$((ERRORS + 1))
        echo "| $TOTAL | $description | ❌ SERVER ERROR | $HTTP_CODE | ${TIME} | $method $endpoint |" >> $RESULTS_FILE
    else
        echo -e "  ${RED}❌ UNKNOWN${NC} ($HTTP_CODE in ${TIME})"
        ERRORS=$((ERRORS + 1))
        echo "| $TOTAL | $description | ❌ UNKNOWN | $HTTP_CODE | ${TIME} | $method $endpoint |" >> $RESULTS_FILE
    fi

    echo ""
}

# Initialize results file
cat > $RESULTS_FILE << 'EOF'
# DEVELOPER API TEST RESULTS - SYSTEMATIC EXECUTION

**Date**: 2025-12-12
**Tester**: Backend Developer Agent
**Status**: TESTING IN PROGRESS

---

## TEST RESULTS

| # | API Name | Status | HTTP Code | Time | Endpoint |
|---|----------|--------|-----------|------|----------|
EOF

echo "" > $TEMP_LOG

echo "========================================="
echo "API TESTING - ALL 181 ENDPOINTS"
echo "========================================="
echo ""

# ============================================
# NEXT.JS APIs (Port 3000) - Test First
# ============================================

echo "========================================="
echo "NEXT.JS APIs (Port 3000)"
echo "========================================="

test_api "GET" "/api/health" "Next.js Health Check" "" "3000"
test_api "GET" "/api/neo4j/stats" "Neo4j Statistics" "" "3000"
test_api "GET" "/api/mysql/stats" "MySQL Statistics" "" "3000"
test_api "GET" "/api/qdrant/collections" "Qdrant Collections" "" "3000"
test_api "GET" "/api/minio/buckets" "MinIO Buckets" "" "3000"

# ============================================
# PHASE B APIs (Port 8000)
# ============================================

echo "========================================="
echo "REMEDIATION APIs"
echo "========================================="

test_api "GET" "/api/v2/remediation/dashboard/summary" "Remediation Dashboard Summary" "" "8000"
test_api "GET" "/api/v2/remediation/dashboard/workload" "Remediation Workload" "" "8000"
test_api "GET" "/api/v2/remediation/tasks" "List Remediation Tasks" "" "8000"
test_api "GET" "/api/v2/remediation/tasks/open" "Open Remediation Tasks" "" "8000"
test_api "GET" "/api/v2/remediation/tasks/overdue" "Overdue Remediation Tasks" "" "8000"
test_api "GET" "/api/v2/remediation/plans" "List Remediation Plans" "" "8000"
test_api "GET" "/api/v2/remediation/plans/active" "Active Remediation Plans" "" "8000"
test_api "GET" "/api/v2/remediation/metrics/summary" "Remediation Metrics Summary" "" "8000"
test_api "GET" "/api/v2/remediation/metrics/mttr" "Mean Time To Remediate" "" "8000"
test_api "GET" "/api/v2/remediation/metrics/sla-compliance" "SLA Compliance Metrics" "" "8000"

echo "========================================="
echo "RISK APIs"
echo "========================================="

test_api "GET" "/api/v2/risk/dashboard/summary" "Risk Dashboard Summary" "" "8000"
test_api "GET" "/api/v2/risk/scores" "Risk Scores List" "" "8000"
test_api "GET" "/api/v2/risk/alerts" "Risk Alerts List" "" "8000"
test_api "GET" "/api/v2/risk/alerts/active" "Active Risk Alerts" "" "8000"
test_api "GET" "/api/v2/risk/trends/by-severity" "Risk Trends by Severity" "" "8000"
test_api "GET" "/api/v2/risk/aggregation/by-vendor" "Risk Aggregation by Vendor" "" "8000"
test_api "GET" "/api/v2/risk/aggregation/by-sector" "Risk Aggregation by Sector" "" "8000"
test_api "GET" "/api/v2/risk/aggregation/by-asset-type" "Risk Aggregation by Asset Type" "" "8000"

echo "========================================="
echo "SBOM APIs"
echo "========================================="

test_api "GET" "/api/v2/sbom/sboms" "List SBOMs" "" "8000"
test_api "POST" "/api/v2/sbom/search" "Search SBOM Components" '{"query":"test","limit":10}' "8000"
test_api "POST" "/api/v2/sbom/analyze" "Analyze SBOM" '{"sbom_data":"test","format":"cyclonedx"}' "8000"

echo "========================================="
echo "THREAT INTELLIGENCE APIs"
echo "========================================="

test_api "GET" "/api/v2/threat-intel/dashboard/summary" "Threat Intel Dashboard" "" "8000"
test_api "GET" "/api/v2/threat-intel/feeds" "List Threat Feeds" "" "8000"
test_api "GET" "/api/v2/threat-intel/indicators" "List Threat Indicators" "" "8000"
test_api "GET" "/api/v2/threat-intel/reports" "List Threat Reports" "" "8000"

echo "========================================="
echo "VENDOR EQUIPMENT APIs"
echo "========================================="

test_api "GET" "/api/v2/vendor-equipment/vendors" "List Vendors" "" "8000"
test_api "GET" "/api/v2/vendor-equipment/equipment" "List Equipment" "" "8000"
test_api "GET" "/api/v2/vendor-equipment/dashboard/summary" "Equipment Dashboard" "" "8000"

# Summary
echo ""
echo "========================================="
echo "TEST SUMMARY"
echo "========================================="
echo "Total Tests:   $TOTAL"
echo "Passed:        $PASSED ($(( PASSED * 100 / TOTAL ))%)"
echo "Client Errors: $FAILED"
echo "Server Errors: $ERRORS"
echo "========================================="

# Append summary to results file
cat >> $RESULTS_FILE << EOF

---

## SUMMARY

**Total Tests**: $TOTAL
**Passed**: $PASSED ($(( PASSED * 100 / TOTAL ))%)
**Client Errors**: $FAILED
**Server Errors**: $ERRORS

**Test Log**: $TEMP_LOG
**Generated**: $(date '+%Y-%m-%d %H:%M:%S')

EOF

echo ""
echo "Results saved to: $RESULTS_FILE"
echo "Detailed log saved to: $TEMP_LOG"
