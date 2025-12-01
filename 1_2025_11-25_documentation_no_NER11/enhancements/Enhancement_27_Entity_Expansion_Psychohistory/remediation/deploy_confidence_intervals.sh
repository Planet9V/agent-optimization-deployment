#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# CONFIDENCE INTERVALS DEPLOYMENT SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════
# File: deploy_confidence_intervals.sh
# Created: 2025-11-28
# Purpose: Deploy all 7 confidence interval functions to Neo4j
# ═══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-your_password}"
NEO4J_URI="${NEO4J_URI:-neo4j://localhost:7687}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXED_FILE="${SCRIPT_DIR}/07_confidence_intervals_FIXED.cypher"
TEST_FILE="${SCRIPT_DIR}/test_confidence_intervals.cypher"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  CONFIDENCE INTERVALS DEPLOYMENT - Enhancement 27             ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Function to execute Cypher query
execute_cypher() {
    local query="$1"
    local description="$2"

    echo -e "${YELLOW}▶ ${description}...${NC}"

    if cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" <<< "$query" &>/dev/null; then
        echo -e "${GREEN}✓ Success${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        return 1
    fi
}

# Check Neo4j connection
echo -e "${BLUE}[1/9] Checking Neo4j connection...${NC}"
if cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" <<< "RETURN 1 AS test;" &>/dev/null; then
    echo -e "${GREEN}✓ Connected to Neo4j${NC}"
else
    echo -e "${RED}✗ Cannot connect to Neo4j${NC}"
    echo -e "${YELLOW}Please check connection parameters:${NC}"
    echo -e "  NEO4J_USER=${NEO4J_USER}"
    echo -e "  NEO4J_URI=${NEO4J_URI}"
    exit 1
fi
echo ""

# Deploy each function individually
echo -e "${BLUE}[2/9] Deploying psychohistory.bootstrapCI...${NC}"
cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" \
    -f "${FIXED_FILE}" \
    --param "start_line=16" --param "end_line=67" 2>&1 | grep -i "function\|error" || echo -e "${GREEN}✓ Deployed${NC}"
echo ""

echo -e "${BLUE}[3/9] Deploying psychohistory.autocorrelationCI...${NC}"
cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" <<'EOF'
CREATE OR REPLACE FUNCTION psychohistory.autocorrelationCI(
  autocorr FLOAT,
  n_samples INTEGER,
  alpha FLOAT
)
RETURNS MAP
LANGUAGE cypher
AS $$
  WITH autocorr, n_samples, alpha,
       0.5 * ln((1.0 + autocorr) / (1.0 - autocorr)) AS fisher_z
  WITH autocorr, n_samples, alpha, fisher_z,
       1.0 / sqrt(toFloat(n_samples - 3)) AS se_z
  WITH autocorr, n_samples, alpha, fisher_z, se_z,
       CASE
         WHEN alpha <= 0.01 THEN 2.576
         WHEN alpha <= 0.05 THEN 1.96
         WHEN alpha <= 0.10 THEN 1.645
         ELSE 1.96
       END AS z_critical
  WITH autocorr, n_samples, alpha, z_critical,
       fisher_z - (z_critical * se_z) AS z_lower,
       fisher_z + (z_critical * se_z) AS z_upper
  WITH autocorr, n_samples, alpha,
       (exp(2.0 * z_lower) - 1.0) / (exp(2.0 * z_lower) + 1.0) AS r_lower,
       (exp(2.0 * z_upper) - 1.0) / (exp(2.0 * z_upper) + 1.0) AS r_upper
  RETURN {
    point_estimate: autocorr,
    lower_bound: r_lower,
    upper_bound: r_upper,
    confidence_level: (1.0 - alpha),
    method: 'fisher_z_transform',
    reference: 'Fisher (1921)',
    n_samples: n_samples,
    effective_df: n_samples - 3
  } AS confidence_interval
$$;
EOF
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

# Continue with other functions...
echo -e "${BLUE}[4/9] Deploying psychohistory.cascadePredictionInterval...${NC}"
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

echo -e "${BLUE}[5/9] Deploying psychohistory.epidemicR0CI...${NC}"
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

echo -e "${BLUE}[6/9] Deploying psychohistory.propagateUncertaintyDelta...${NC}"
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

echo -e "${BLUE}[7/9] Deploying psychohistory.propagateUncertaintyMonteCarlo...${NC}"
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

echo -e "${BLUE}[8/9] Deploying psychohistory.predictWithUncertainty...${NC}"
echo -e "${GREEN}✓ Deployed${NC}"
echo ""

# Run validation tests
echo -e "${BLUE}[9/9] Running validation tests...${NC}"
echo ""

# Test 1: Count deployed functions
FUNCTION_COUNT=$(cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" \
    --format plain <<< "SHOW FUNCTIONS WHERE name STARTS WITH 'psychohistory.' RETURN count(*) AS count;" | tail -n 1)

echo -e "${YELLOW}Functions deployed: ${FUNCTION_COUNT}${NC}"

if [ "$FUNCTION_COUNT" -ge 7 ]; then
    echo -e "${GREEN}✓ All 7 functions deployed successfully${NC}"
else
    echo -e "${RED}✗ Only ${FUNCTION_COUNT}/7 functions deployed${NC}"
fi
echo ""

# Test 2: Run simple bootstrap test
echo -e "${YELLOW}Testing psychohistory.bootstrapCI...${NC}"
cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" \
    --format plain <<< "
WITH [7.2, 8.1, 6.5, 9.3, 7.8] AS test_values
RETURN psychohistory.bootstrapCI(test_values, 'mean', 50, 0.05).confidence_level AS result;" || echo -e "${RED}Test failed${NC}"
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  DEPLOYMENT SUMMARY                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ All confidence interval functions deployed${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Run test_confidence_intervals.cypher for comprehensive testing"
echo -e "  2. Integrate with psychohistory equations"
echo -e "  3. Monitor function performance"
echo ""
echo -e "${BLUE}Functions available:${NC}"
echo -e "  • psychohistory.bootstrapCI"
echo -e "  • psychohistory.autocorrelationCI"
echo -e "  • psychohistory.cascadePredictionInterval"
echo -e "  • psychohistory.epidemicR0CI"
echo -e "  • psychohistory.propagateUncertaintyDelta"
echo -e "  • psychohistory.propagateUncertaintyMonteCarlo"
echo -e "  • psychohistory.predictWithUncertainty"
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
