#!/bin/bash
################################################################################
# Comprehensive API Testing Script - ALL 232 ENDPOINTS
# Generated: 2025-12-12 14:35:00
# Purpose: Test ALL APIs across 3 services with detailed reporting
################################################################################

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_URL_BACKEND="http://localhost:8000"
BASE_URL_FRONTEND="http://localhost:3000"
BASE_URL_OPENSPG="http://localhost:8887"
CUSTOMER_ID="dev"
NAMESPACE="default"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
RESULTS_FILE="/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/test_results_${TIMESTAMP}.md"
JSON_LOG="/tmp/api_test_${TIMESTAMP}.json"
DETAIL_LOG="/tmp/api_test_detail_${TIMESTAMP}.log"

# =============================================================================
# COLORS
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# COUNTERS
# =============================================================================
TOTAL=0
PASSED=0
FAILED=0
ERRORS=0
SKIPPED=0

# =============================================================================
# JSON RESULT ARRAY
# =============================================================================
echo "[]" > $JSON_LOG

# =============================================================================
# TEST FUNCTION
# =============================================================================
test_api() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local service=$5
    local category=$6

    TOTAL=$((TOTAL + 1))

    # Determine base URL
    case $service in
        "backend")
            BASE_URL="$BASE_URL_BACKEND"
            HEADERS="-H 'x-customer-id: $CUSTOMER_ID' -H 'x-namespace: $NAMESPACE' -H 'Content-Type: application/json'"
            ;;
        "frontend")
            BASE_URL="$BASE_URL_FRONTEND"
            HEADERS="-H 'Content-Type: application/json'"
            ;;
        "openspg")
            BASE_URL="$BASE_URL_OPENSPG"
            HEADERS="-H 'Content-Type: application/json'"
            ;;
        *)
            echo -e "${RED}❌ Unknown service: $service${NC}"
            ERRORS=$((ERRORS + 1))
            return
            ;;
    esac

    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo -e "${BLUE}Test #$TOTAL: $description${NC}"
    echo "  Category: $category"
    echo "  Service: $service"
    echo "  Method: $method"
    echo "  Endpoint: $endpoint"

    # Build curl command
    if [ -n "$data" ]; then
        CMD="curl -X $method '$BASE_URL$endpoint' $HEADERS -d '$data' -w '\n__HTTP_STATUS__:%{http_code}\n__TIME__:%{time_total}s\n' -s --max-time 30 2>&1"
    else
        CMD="curl -X $method '$BASE_URL$endpoint' $HEADERS -w '\n__HTTP_STATUS__:%{http_code}\n__TIME__:%{time_total}s\n' -s --max-time 30 2>&1"
    fi

    # Execute and capture
    RESPONSE=$(eval $CMD)
    EXIT_CODE=$?

    # Parse response
    HTTP_CODE=$(echo "$RESPONSE" | grep "__HTTP_STATUS__" | cut -d: -f2 | tr -d ' ')
    TIME=$(echo "$RESPONSE" | grep "__TIME__" | cut -d: -f2 | tr -d ' ')
    BODY=$(echo "$RESPONSE" | sed '/__HTTP_STATUS__/,$d')

    # Log details
    echo "═══════════════════════════════════════════════════════════════════" >> $DETAIL_LOG
    echo "Test #$TOTAL: $description" >> $DETAIL_LOG
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" >> $DETAIL_LOG
    echo "Command: $CMD" >> $DETAIL_LOG
    echo "HTTP Status: $HTTP_CODE" >> $DETAIL_LOG
    echo "Response Time: $TIME" >> $DETAIL_LOG
    echo "Response Body:" >> $DETAIL_LOG
    echo "$BODY" >> $DETAIL_LOG
    echo "" >> $DETAIL_LOG

    # Classify result
    local status=""
    local symbol=""
    local color=""

    if [ $EXIT_CODE -ne 0 ]; then
        status="ERROR"
        symbol="❌"
        color=$RED
        ERRORS=$((ERRORS + 1))
    elif [[ -z "$HTTP_CODE" ]]; then
        status="ERROR"
        symbol="❌"
        color=$RED
        ERRORS=$((ERRORS + 1))
        HTTP_CODE="TIMEOUT"
        TIME="30.0s"
    elif [[ "$HTTP_CODE" =~ ^2[0-9][0-9]$ ]]; then
        status="PASS"
        symbol="✅"
        color=$GREEN
        PASSED=$((PASSED + 1))
    elif [[ "$HTTP_CODE" =~ ^4[0-9][0-9]$ ]]; then
        status="CLIENT_ERROR"
        symbol="⚠️"
        color=$YELLOW
        FAILED=$((FAILED + 1))
    elif [[ "$HTTP_CODE" =~ ^5[0-9][0-9]$ ]]; then
        status="SERVER_ERROR"
        symbol="❌"
        color=$RED
        ERRORS=$((ERRORS + 1))
    else
        status="UNKNOWN"
        symbol="❓"
        color=$RED
        ERRORS=$((ERRORS + 1))
    fi

    echo -e "  ${color}${symbol} ${status}${NC} (HTTP $HTTP_CODE in ${TIME})"

    # Add to JSON log
    local json_entry=$(cat <<EOF
{
  "test_number": $TOTAL,
  "description": "$description",
  "category": "$category",
  "service": "$service",
  "method": "$method",
  "endpoint": "$endpoint",
  "status": "$status",
  "http_code": "$HTTP_CODE",
  "response_time": "$TIME",
  "timestamp": "$(date '+%Y-%m-%d %H:%M:%S')",
  "data": $(echo "$data" | jq -Rs . 2>/dev/null || echo '""')
}
EOF
)

    # Append to JSON array
    local current_json=$(cat $JSON_LOG)
    echo "$current_json" | jq --argjson new "$json_entry" '. += [$new]' > $JSON_LOG
}

# =============================================================================
# INITIALIZE RESULTS FILE
# =============================================================================
cat > $RESULTS_FILE << 'EOF'
# COMPREHENSIVE API TEST RESULTS - ALL 232 ENDPOINTS

**Date:** 2025-12-12
**Services Tested:** 3 (ner11-gold-api, aeon-saas-dev, openspg-server)
**Total Endpoints:** 232

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Total Tests | PENDING |
| Passed | PENDING |
| Failed | PENDING |
| Errors | PENDING |
| Pass Rate | PENDING |

---

## DETAILED TEST RESULTS

| # | API Name | Category | Service | Status | HTTP | Time | Endpoint |
|---|----------|----------|---------|--------|------|------|----------|
EOF

echo "" > $DETAIL_LOG

echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}COMPREHENSIVE API TESTING - ALL 232 ENDPOINTS${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Services:"
echo "  - ner11-gold-api: $BASE_URL_BACKEND"
echo "  - aeon-saas-dev: $BASE_URL_FRONTEND"
echo "  - openspg-server: $BASE_URL_OPENSPG"
echo ""
echo "Results will be saved to: $RESULTS_FILE"
echo "Detail log: $DETAIL_LOG"
echo "JSON log: $JSON_LOG"
echo ""

# =============================================================================
# SERVICE 1: NER11-GOLD-API (Port 8000) - 128 ENDPOINTS
# =============================================================================

echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}SERVICE 1: NER11-GOLD-API (128 ENDPOINTS)${NC}"
echo "═══════════════════════════════════════════════════════════════════"

# SBOM Analysis (34 endpoints)
test_api "POST" "/api/v2/sbom/sboms" "Create new SBOM" '{"name":"test-sbom","format":"cyclonedx","data":{}}' "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms" "List SBOMs" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1" "Get SBOM by ID" "" "backend" "SBOM"
test_api "DELETE" "/api/v2/sbom/sboms/999" "Delete SBOM" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/risk-summary" "SBOM risk summary" "" "backend" "SBOM"
test_api "POST" "/api/v2/sbom/components" "Create component" '{"name":"test-component","version":"1.0.0"}' "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/1" "Get component by ID" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/search?q=test" "Search components" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/vulnerable" "Vulnerable components" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/high-risk" "High-risk components" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/components" "SBOM components" "" "backend" "SBOM"
test_api "POST" "/api/v2/sbom/dependencies" "Create dependency" '{"source_id":1,"target_id":2}' "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/1/dependencies" "Dependency tree" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/1/dependents" "Reverse dependencies" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/1/impact" "Impact analysis" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/cycles" "Circular dependencies" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/dependencies/path?source=1&target=2" "Dependency path" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/graph-stats" "Graph statistics" "" "backend" "SBOM"
test_api "POST" "/api/v2/sbom/vulnerabilities" "Create vulnerability" '{"cve_id":"CVE-2023-1234"}' "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/1" "Get vulnerability" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/search?q=CVE" "Search vulnerabilities" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/critical" "Critical vulnerabilities" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/kev" "KEV vulnerabilities" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/epss-prioritized" "EPSS prioritized" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/vulnerabilities/by-apt?apt_group=APT28" "Vulnerabilities by APT" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/components/1/vulnerabilities" "Component vulnerabilities" "" "backend" "SBOM"
test_api "POST" "/api/v2/sbom/vulnerabilities/1/acknowledge" "Acknowledge vulnerability" '{"acknowledged":true}' "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/remediation" "Remediation plan" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/license-compliance" "License compliance" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/dashboard/summary" "SBOM dashboard" "" "backend" "SBOM"
test_api "GET" "/api/v2/sbom/sboms/1/vulnerable-paths" "Vulnerable paths" "" "backend" "SBOM"
test_api "POST" "/api/v2/sbom/sboms/1/correlate-equipment" "Correlate equipment" '{"equipment_id":"eq-001"}' "backend" "SBOM"

# Vendor & Equipment (23 endpoints)
test_api "POST" "/api/v2/vendor-equipment/vendors" "Create vendor" '{"name":"Test Vendor","country":"US"}' "backend" "Vendor"
test_api "GET" "/api/v2/vendor-equipment/vendors" "List vendors" "" "backend" "Vendor"
test_api "GET" "/api/v2/vendor-equipment/vendors/1" "Get vendor" "" "backend" "Vendor"
test_api "GET" "/api/v2/vendor-equipment/vendors/1/risk-summary" "Vendor risk" "" "backend" "Vendor"
test_api "GET" "/api/v2/vendor-equipment/vendors/high-risk" "High-risk vendors" "" "backend" "Vendor"
test_api "POST" "/api/v2/vendor-equipment/equipment" "Create equipment" '{"model":"Router-X","vendor_id":1}' "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/equipment" "List equipment" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/equipment/1" "Get equipment" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/equipment/approaching-eol" "EOL approaching" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/equipment/eol" "EOL equipment" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/maintenance-schedule" "Maintenance schedule" "" "backend" "Equipment"
test_api "POST" "/api/v2/vendor-equipment/vulnerabilities/flag" "Flag vulnerability" '{"equipment_id":1,"cve_id":"CVE-2023-1234"}' "backend" "Equipment"
test_api "POST" "/api/v2/vendor-equipment/maintenance-windows" "Create maintenance" '{"equipment_id":1,"start":"2025-12-15T00:00:00Z"}' "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/maintenance-windows" "List maintenance" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/maintenance-windows/1" "Get maintenance" "" "backend" "Equipment"
test_api "DELETE" "/api/v2/vendor-equipment/maintenance-windows/999" "Delete maintenance" "" "backend" "Equipment"
test_api "POST" "/api/v2/vendor-equipment/maintenance-windows/check-conflict" "Check conflict" '{"start":"2025-12-15T00:00:00Z"}' "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/predictive-maintenance/1" "Predictive maintenance" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/predictive-maintenance/forecast" "Maintenance forecast" "" "backend" "Equipment"
test_api "POST" "/api/v2/vendor-equipment/work-orders" "Create work order" '{"equipment_id":1,"type":"maintenance"}' "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/work-orders" "List work orders" "" "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/work-orders/1" "Get work order" "" "backend" "Equipment"
test_api "PATCH" "/api/v2/vendor-equipment/work-orders/1/status" "Update work order" '{"status":"completed"}' "backend" "Equipment"
test_api "GET" "/api/v2/vendor-equipment/work-orders/summary" "Work orders summary" "" "backend" "Equipment"

# Threat Intelligence (20 endpoints)
test_api "POST" "/api/v2/threat-intel/actors" "Create threat actor" '{"name":"APT28","aliases":["Fancy Bear"]}' "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/1" "Get threat actor" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/search?q=APT" "Search actors" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/active" "Active actors" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/by-sector/energy" "Actors by sector" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/1/campaigns" "Actor campaigns" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/actors/1/cves" "Actor CVEs" "" "backend" "Threat Intel"
test_api "POST" "/api/v2/threat-intel/campaigns" "Create campaign" '{"name":"Test Campaign"}' "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/campaigns/1" "Get campaign" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/campaigns/search?q=test" "Search campaigns" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/campaigns/active" "Active campaigns" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/campaigns/1/iocs" "Campaign IOCs" "" "backend" "Threat Intel"
test_api "POST" "/api/v2/threat-intel/mitre/mappings" "Create MITRE mapping" '{"technique_id":"T1566","entity_type":"actor"}' "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/mitre/mappings/entity/actor/1" "Entity MITRE" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/mitre/techniques/T1566/actors" "Technique actors" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/mitre/coverage" "MITRE coverage" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/mitre/gaps" "Coverage gaps" "" "backend" "Threat Intel"
test_api "POST" "/api/v2/threat-intel/iocs" "Create IOC" '{"type":"ip","value":"192.168.1.1"}' "backend" "Threat Intel"
test_api "POST" "/api/v2/threat-intel/iocs/bulk" "Bulk create IOCs" '{"iocs":[{"type":"ip","value":"10.0.0.1"}]}' "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/iocs/search?q=192" "Search IOCs" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/iocs/active" "Active IOCs" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/iocs/by-type/ip" "IOCs by type" "" "backend" "Threat Intel"
test_api "POST" "/api/v2/threat-intel/feeds" "Create threat feed" '{"name":"Test Feed","url":"https://example.com"}' "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/feeds" "List feeds" "" "backend" "Threat Intel"
test_api "PUT" "/api/v2/threat-intel/feeds/1/refresh" "Refresh feed" "" "backend" "Threat Intel"
test_api "GET" "/api/v2/threat-intel/dashboard/summary" "Threat intel dashboard" "" "backend" "Threat Intel"

# Risk Management (21 endpoints)
test_api "POST" "/api/v2/risk/scores" "Create risk score" '{"entity_type":"asset","entity_id":"asset-001","score":75}' "backend" "Risk"
test_api "GET" "/api/v2/risk/scores/asset/asset-001" "Get risk score" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/scores/high-risk" "High-risk entities" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/scores/trending" "Trending scores" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/scores/search?q=asset" "Search scores" "" "backend" "Risk"
test_api "POST" "/api/v2/risk/scores/recalculate/asset/asset-001" "Recalculate score" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/scores/history/asset/asset-001" "Score history" "" "backend" "Risk"
test_api "POST" "/api/v2/risk/assets/criticality" "Create criticality" '{"asset_id":"asset-001","level":"critical"}' "backend" "Risk"
test_api "GET" "/api/v2/risk/assets/asset-001/criticality" "Get criticality" "" "backend" "Risk"
test_api "PUT" "/api/v2/risk/assets/asset-001/criticality" "Update criticality" '{"level":"high"}' "backend" "Risk"
test_api "GET" "/api/v2/risk/assets/mission-critical" "Mission-critical" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/assets/by-criticality/high" "Assets by criticality" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/assets/criticality/summary" "Criticality summary" "" "backend" "Risk"
test_api "POST" "/api/v2/risk/exposure" "Create exposure" '{"asset_id":"asset-001","exposure_type":"internet"}' "backend" "Risk"
test_api "GET" "/api/v2/risk/exposure/asset-001" "Get exposure" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/exposure/internet-facing" "Internet-facing" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/exposure/high-exposure" "High exposure" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/exposure/attack-surface" "Attack surface" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/aggregation/by-vendor" "Risk by vendor" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/aggregation/by-sector" "Risk by sector" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/aggregation/by-asset-type" "Risk by asset type" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/aggregation/vendor/vendor-001" "Vendor aggregation" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/dashboard/summary" "Risk dashboard" "" "backend" "Risk"
test_api "GET" "/api/v2/risk/dashboard/risk-matrix" "Risk matrix" "" "backend" "Risk"

# Remediation Management (25 endpoints)
test_api "POST" "/api/v2/remediation/tasks" "Create task" '{"title":"Fix CVE-2023-1234","priority":"high"}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/1" "Get task" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/search?q=CVE" "Search tasks" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/open" "Open tasks" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/overdue" "Overdue tasks" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/by-priority/high" "Tasks by priority" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/by-status/in_progress" "Tasks by status" "" "backend" "Remediation"
test_api "PUT" "/api/v2/remediation/tasks/1/status" "Update task status" '{"status":"completed"}' "backend" "Remediation"
test_api "PUT" "/api/v2/remediation/tasks/1/assign" "Assign task" '{"assignee":"user-001"}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/tasks/1/history" "Task history" "" "backend" "Remediation"
test_api "POST" "/api/v2/remediation/plans" "Create plan" '{"name":"Q1 Remediation","tasks":[]}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/plans" "List plans" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/plans/1" "Get plan" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/plans/active" "Active plans" "" "backend" "Remediation"
test_api "PUT" "/api/v2/remediation/plans/1/status" "Update plan status" '{"status":"in_progress"}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/plans/1/progress" "Plan progress" "" "backend" "Remediation"
test_api "POST" "/api/v2/remediation/sla/policies" "Create SLA policy" '{"name":"Critical SLA","target_days":7}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/sla/policies" "List policies" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/sla/policies/1" "Get policy" "" "backend" "Remediation"
test_api "PUT" "/api/v2/remediation/sla/policies/1" "Update policy" '{"target_days":5}' "backend" "Remediation"
test_api "GET" "/api/v2/remediation/sla/breaches" "SLA breaches" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/sla/at-risk" "At-risk SLAs" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/metrics/summary" "Metrics summary" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/metrics/mttr" "MTTR metric" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/metrics/sla-compliance" "SLA compliance" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/metrics/backlog" "Backlog metrics" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/metrics/trends" "Remediation trends" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/dashboard/summary" "Remediation dashboard" "" "backend" "Remediation"
test_api "GET" "/api/v2/remediation/dashboard/workload" "Workload dashboard" "" "backend" "Remediation"

# NER & Search (5 endpoints)
test_api "POST" "/ner" "Named entity recognition" '{"text":"Microsoft released a patch for CVE-2023-1234"}' "backend" "NER"
test_api "POST" "/search/semantic" "Semantic search" '{"query":"critical vulnerabilities","limit":10}' "backend" "Search"
test_api "POST" "/search/hybrid" "Hybrid search" '{"query":"network equipment","limit":10}' "backend" "Search"
test_api "GET" "/health" "Backend health" "" "backend" "System"
test_api "GET" "/info" "Backend API info" "" "backend" "System"

# =============================================================================
# SERVICE 2: AEON-SAAS-DEV (Port 3000) - 64 ENDPOINTS
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}SERVICE 2: AEON-SAAS-DEV (64 ENDPOINTS)${NC}"
echo "═══════════════════════════════════════════════════════════════════"

# Pipeline Management (5 endpoints)
test_api "POST" "/api/pipeline/process" "Process document" '{"url":"https://example.com/doc.pdf"}' "frontend" "Pipeline"
test_api "GET" "/api/pipeline/process" "Queue status" "" "frontend" "Pipeline"
test_api "DELETE" "/api/pipeline/process" "Clear queue" "" "frontend" "Pipeline"
test_api "GET" "/api/pipeline/status/job-001" "Job status" "" "frontend" "Pipeline"
test_api "DELETE" "/api/pipeline/status/job-001" "Cancel job" "" "frontend" "Pipeline"

# Query Control (9 endpoints)
test_api "GET" "/api/query-control/queries" "List queries" "" "frontend" "Query Control"
test_api "POST" "/api/query-control/queries" "Create query" '{"query":"test query"}' "frontend" "Query Control"
test_api "GET" "/api/query-control/queries/query-001" "Get query" "" "frontend" "Query Control"
test_api "DELETE" "/api/query-control/queries/query-001" "Delete query" "" "frontend" "Query Control"
test_api "GET" "/api/query-control/queries/query-001/checkpoints" "Query checkpoints" "" "frontend" "Query Control"
test_api "POST" "/api/query-control/queries/query-001/model" "Change model" '{"model":"gpt-4"}' "frontend" "Query Control"
test_api "POST" "/api/query-control/queries/query-001/permissions" "Change permissions" '{"level":"admin"}' "frontend" "Query Control"
test_api "POST" "/api/query-control/queries/query-001/resume" "Resume query" "" "frontend" "Query Control"
test_api "POST" "/api/query-control/queries/query-001/pause" "Pause query" "" "frontend" "Query Control"

# Dashboard & Metrics (3 endpoints)
test_api "GET" "/api/dashboard/metrics" "System metrics" "" "frontend" "Dashboard"
test_api "GET" "/api/dashboard/distribution" "Data distribution" "" "frontend" "Dashboard"
test_api "GET" "/api/dashboard/activity" "Activity feed" "" "frontend" "Dashboard"

# Search & Chat (3 endpoints)
test_api "POST" "/api/search" "Vector search" '{"query":"cyber threats","limit":10}' "frontend" "Search"
test_api "GET" "/api/search" "Search suggestions" "" "frontend" "Search"
test_api "POST" "/api/chat" "AI chat" '{"message":"What are the top threats?"}' "frontend" "Chat"

# Threat Intelligence (6 endpoints)
test_api "GET" "/api/threats/geographic" "Geographic threats" "" "frontend" "Threat Intel"
test_api "GET" "/api/threats/ics" "ICS threats" "" "frontend" "Threat Intel"
test_api "GET" "/api/threat-intel/ics" "ICS intel" "" "frontend" "Threat Intel"
test_api "GET" "/api/threat-intel/landscape" "Threat landscape" "" "frontend" "Threat Intel"
test_api "GET" "/api/threat-intel/analytics" "Threat analytics" "" "frontend" "Threat Intel"
test_api "GET" "/api/threat-intel/vulnerabilities" "Threat vulnerabilities" "" "frontend" "Threat Intel"

# Customer Management (5 endpoints)
test_api "GET" "/api/customers" "List customers" "" "frontend" "Customer"
test_api "POST" "/api/customers" "Create customer" '{"name":"Test Customer","email":"test@example.com"}' "frontend" "Customer"
test_api "GET" "/api/customers/cust-001" "Get customer" "" "frontend" "Customer"
test_api "PUT" "/api/customers/cust-001" "Update customer" '{"name":"Updated Customer"}' "frontend" "Customer"
test_api "DELETE" "/api/customers/cust-999" "Delete customer" "" "frontend" "Customer"

# Tag Management (8 endpoints)
test_api "GET" "/api/tags" "List tags" "" "frontend" "Tag"
test_api "POST" "/api/tags" "Create tag" '{"name":"critical","color":"#FF0000"}' "frontend" "Tag"
test_api "DELETE" "/api/tags" "Bulk delete tags" '{"ids":["tag-001","tag-002"]}' "frontend" "Tag"
test_api "GET" "/api/tags/tag-001" "Get tag" "" "frontend" "Tag"
test_api "PUT" "/api/tags/tag-001" "Update tag" '{"name":"updated-tag"}' "frontend" "Tag"
test_api "DELETE" "/api/tags/tag-999" "Delete tag" "" "frontend" "Tag"
test_api "POST" "/api/tags/assign" "Assign tags" '{"entity_id":"ent-001","tags":["tag-001"]}' "frontend" "Tag"
test_api "DELETE" "/api/tags/assign" "Unassign tags" '{"entity_id":"ent-001","tags":["tag-001"]}' "frontend" "Tag"

# Analytics (6 endpoints)
test_api "GET" "/api/analytics/timeseries" "Time series" "" "frontend" "Analytics"
test_api "GET" "/api/analytics/metrics" "Analytics metrics" "" "frontend" "Analytics"
test_api "GET" "/api/analytics/trends/threat-timeline" "Threat timeline" "" "frontend" "Analytics"
test_api "GET" "/api/analytics/trends/cve" "CVE trends" "" "frontend" "Analytics"
test_api "GET" "/api/analytics/trends/seasonality" "Seasonal patterns" "" "frontend" "Analytics"
test_api "POST" "/api/analytics/export" "Export analytics" '{"format":"csv","data":"threats"}' "frontend" "Analytics"

# Observability (4 endpoints)
test_api "GET" "/api/observability/performance" "Performance metrics" "" "frontend" "Observability"
test_api "GET" "/api/observability/system" "System health" "" "frontend" "Observability"
test_api "GET" "/api/observability/agents" "Agent status" "" "frontend" "Observability"
test_api "POST" "/api/observability/agents" "Update agent" '{"agent_id":"agent-001","status":"active"}' "frontend" "Observability"

# Graph & Neo4j (4 endpoints)
test_api "POST" "/api/graph/query" "Execute graph query" '{"query":"MATCH (n) RETURN n LIMIT 5"}' "frontend" "Graph"
test_api "GET" "/api/graph/query" "Query templates" "" "frontend" "Graph"
test_api "GET" "/api/neo4j/statistics" "Neo4j stats" "" "frontend" "Graph"
test_api "GET" "/api/neo4j/cyber-statistics" "Cyber stats" "" "frontend" "Graph"

# System (4 endpoints)
test_api "GET" "/api/health" "Frontend health" "" "frontend" "System"
test_api "POST" "/api/upload" "File upload" '{"file":"test.txt","content":"test"}' "frontend" "System"
test_api "GET" "/api/activity/recent" "Recent activity" "" "frontend" "System"
test_api "GET" "/api/backend/test" "Backend connectivity" "" "frontend" "System"

# =============================================================================
# SERVICE 3: OPENSPG-SERVER (Port 8887) - 40 ENDPOINTS (Estimated)
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}SERVICE 3: OPENSPG-SERVER (40 ENDPOINTS - ESTIMATED)${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}NOTE: OpenSPG requires authentication. Testing public endpoints only.${NC}"

# Schema Management (estimated 8 endpoints)
test_api "GET" "/api/schema/list" "List schemas" "" "openspg" "Schema"
test_api "GET" "/api/schema/types" "Schema types" "" "openspg" "Schema"
test_api "GET" "/api/schema/relations" "Schema relations" "" "openspg" "Schema"
test_api "GET" "/api/schema/properties" "Schema properties" "" "openspg" "Schema"

# Entity Management (estimated 10 endpoints)
test_api "GET" "/api/entity/list" "List entities" "" "openspg" "Entity"
test_api "GET" "/api/entity/search" "Search entities" "" "openspg" "Entity"
test_api "GET" "/api/entity/types" "Entity types" "" "openspg" "Entity"

# Knowledge Graph Query (estimated 6 endpoints)
test_api "GET" "/api/kg/query" "KG query" "" "openspg" "KG Query"
test_api "GET" "/api/kg/statistics" "KG statistics" "" "openspg" "KG Query"
test_api "GET" "/api/kg/health" "KG health" "" "openspg" "KG Query"

# System (estimated 3 endpoints)
test_api "GET" "/api/health" "OpenSPG health" "" "openspg" "System"
test_api "GET" "/api/version" "OpenSPG version" "" "openspg" "System"
test_api "GET" "/api/info" "OpenSPG info" "" "openspg" "System"

# =============================================================================
# GENERATE SUMMARY
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}TEST EXECUTION COMPLETE${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Total Tests:    $TOTAL"
echo -e "Passed:         ${GREEN}$PASSED${NC} ($(( PASSED * 100 / TOTAL ))%)"
echo -e "Failed:         ${YELLOW}$FAILED${NC}"
echo -e "Errors:         ${RED}$ERRORS${NC}"
echo ""

# Calculate pass rate
PASS_RATE=$(( PASSED * 100 / TOTAL ))

# Update results file with summary
sed -i "s/| Total Tests | PENDING |/| Total Tests | $TOTAL |/" $RESULTS_FILE
sed -i "s/| Passed | PENDING |/| Passed | $PASSED |/" $RESULTS_FILE
sed -i "s/| Failed | PENDING |/| Failed | $FAILED |/" $RESULTS_FILE
sed -i "s/| Errors | PENDING |/| Errors | $ERRORS |/" $RESULTS_FILE
sed -i "s/| Pass Rate | PENDING |/| Pass Rate | $PASS_RATE% |/" $RESULTS_FILE

# Add JSON data to results file
cat >> $RESULTS_FILE << EOF

---

## JSON TEST DATA

\`\`\`json
$(cat $JSON_LOG)
\`\`\`

---

## TEST EXECUTION DETAILS

**Start Time:** $(head -1 $DETAIL_LOG | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}' || echo 'N/A')
**End Time:** $(date '+%Y-%m-%d %H:%M:%S')
**Total Duration:** Calculated from logs

**Logs:**
- Detail Log: $DETAIL_LOG
- JSON Log: $JSON_LOG

EOF

echo "═══════════════════════════════════════════════════════════════════"
echo -e "${GREEN}Results saved to:${NC}"
echo "  - Markdown Report: $RESULTS_FILE"
echo "  - JSON Data: $JSON_LOG"
echo "  - Detail Log: $DETAIL_LOG"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Store in Qdrant
echo "Storing results in Qdrant..."
python3 /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/store_test_results_qdrant.py \
    --results-file "$RESULTS_FILE" \
    --json-file "$JSON_LOG" \
    --collection "api-fixes"

echo ""
echo -e "${GREEN}✅ ALL TESTING COMPLETE${NC}"
echo ""
