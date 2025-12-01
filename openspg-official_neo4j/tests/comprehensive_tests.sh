#!/bin/bash
#═══════════════════════════════════════════════════════════════════════
# COMPREHENSIVE NEO4J TEST SUITE - 40 TESTS
#═══════════════════════════════════════════════════════════════════════

PASSED=0
FAILED=0
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/comprehensive_results_${TIMESTAMP}.md"

echo "Executing comprehensive test suite..."
echo "Results will be saved to: $RESULTS"

# Initialize results file
cat > "$RESULTS" << 'EOF'
# NEO4J COMPREHENSIVE TEST SUITE RESULTS

**Test Suite**: Neo4j Database Comprehensive Validation
**Timestamp**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Database**: openspg-neo4j
**Target Pass Rate**: 95%

## Test Results

| ID | Test Name | Description | Expected | Actual | Status |
|----|-----------|-------------|----------|--------|--------|
EOF

# Helper function
run_test() {
    local id="$1"
    local name="$2"
    local desc="$3"
    local query="$4"
    local expected="$5"

    echo -n "  Running $id: $name... "

    RESULT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" --format plain "$query" 2>&1 | tail -1)

    if [[ "$RESULT" =~ ^[0-9]+$ ]]; then
        ACTUAL=$RESULT
        if [[ "$expected" == ">"* ]]; then
            THRESHOLD=${expected:1}
            if [[ $ACTUAL -gt $THRESHOLD ]]; then
                STATUS="PASS ✓"
                ((PASSED++))
            else
                STATUS="FAIL ✗"
                ((FAILED++))
            fi
        elif [[ "$ACTUAL" == "$expected" ]]; then
            STATUS="PASS ✓"
            ((PASSED++))
        else
            STATUS="FAIL ✗"
            ((FAILED++))
        fi
    else
        ACTUAL="ERROR"
        STATUS="ERROR ⚠"
        ((FAILED++))
    fi

    echo "$STATUS"
    echo "| $id | $name | $desc | $expected | $ACTUAL | $STATUS |" >> "$RESULTS"
}

echo ""
echo "Running tests..."

# Core Database Tests
run_test "T001" "Database Populated" "Total nodes in database" "MATCH (n) RETURN count(n);" ">0"
run_test "T002" "Seldon Crises Count" "All 3 Seldon Crises exist" "MATCH (c:SeldonCrisis) RETURN count(c);" "3"
run_test "T003" "Crisis 1 Exists" "Great Resignation Cascade" "MATCH (c:SeldonCrisis {name: 'Great Resignation Cascade'}) RETURN count(c);" "1"
run_test "T004" "Crisis 2 Exists" "Supply Chain Collapse" "MATCH (c:SeldonCrisis {name: 'Supply Chain Collapse'}) RETURN count(c);" "1"
run_test "T005" "Crisis 3 Exists" "Medical Device Pandemic" "MATCH (c:SeldonCrisis {name: 'Medical Device Pandemic'}) RETURN count(c);" "1"

# Tier Property Tests
run_test "T006" "Tier Property Exists" "Nodes with tier property" "MATCH (n) WHERE n.tier IS NOT NULL RETURN count(n);" ">0"
run_test "T007" "Multiple Tiers" "Distinct tier values" "MATCH (n) WHERE n.tier IS NOT NULL WITH DISTINCT n.tier AS t RETURN count(t);" ">3"
run_test "T008" "Tier 5 Nodes" "T5 tier nodes exist" "MATCH (n {tier: 5}) RETURN count(n);" ">0"
run_test "T009" "Tier 7 Nodes" "T7 tier nodes exist" "MATCH (n {tier: 7}) RETURN count(n);" ">0"
run_test "T010" "Tier 8 Nodes" "T8 tier nodes exist" "MATCH (n {tier: 8}) RETURN count(n);" ">0"
run_test "T011" "Tier 9 Nodes" "T9 tier nodes exist" "MATCH (n {tier: 9}) RETURN count(n);" ">0"

# Entity Type Tests
run_test "T012" "AttackPattern" "AttackPattern entities" "MATCH (a:AttackPattern) RETURN count(a);" ">0"
run_test "T013" "Control" "Control entities" "MATCH (c:Control) RETURN count(c);" ">0"
run_test "T014" "ThreatActor" "ThreatActor entities" "MATCH (t:ThreatActor) RETURN count(t);" ">0"
run_test "T015" "Indicator" "Indicator entities" "MATCH (i:Indicator) RETURN count(i);" ">0"
run_test "T016" "Event" "Event entities" "MATCH (e:Event) RETURN count(e);" ">0"
run_test "T017" "EconomicMetric" "EconomicMetric entities" "MATCH (e:EconomicMetric) RETURN count(e);" ">0"
run_test "T018" "Asset" "Asset entities" "MATCH (a:Asset) RETURN count(a);" ">0"
run_test "T019" "Vulnerability" "Vulnerability entities" "MATCH (v:Vulnerability) RETURN count(v);" ">0"
run_test "T020" "Campaign" "Campaign entities" "MATCH (c:Campaign) RETURN count(c);" ">0"
run_test "T021" "Malware" "Malware entities" "MATCH (m:Malware) RETURN count(m);" ">0"
run_test "T022" "PsychTrait" "PsychTrait entities" "MATCH (p:PsychTrait) RETURN count(p);" ">0"
run_test "T023" "Software" "Software entities" "MATCH (s:Software) RETURN count(s);" ">0"
run_test "T024" "Protocol" "Protocol entities" "MATCH (p:Protocol) RETURN count(p);" ">0"
run_test "T025" "Organization" "Organization entities" "MATCH (o:Organization) RETURN count(o);" ">0"
run_test "T026" "Location" "Location entities" "MATCH (l:Location) RETURN count(l);" ">0"

# Relationship Tests
run_test "T027" "Relationships Exist" "Total relationships" "MATCH ()-[r]->() RETURN count(r);" ">0"
run_test "T028" "Relationship Types" "Distinct relationship types" "MATCH ()-[r]->() WITH DISTINCT type(r) AS t RETURN count(t);" ">3"

# Property Tests
run_test "T029" "Names Exist" "Nodes with name property" "MATCH (n) WHERE n.name IS NOT NULL RETURN count(n);" ">0"
run_test "T030" "Crisis Properties" "Seldon Crises have required properties" "MATCH (c:SeldonCrisis) WHERE c.name IS NOT NULL RETURN count(c);" "3"

# Sample Tier Queries
run_test "T031" "T5 AttackPatterns" "AttackPattern at tier 5" "MATCH (a:AttackPattern {tier: 5}) RETURN count(a);" ">0"
run_test "T032" "T7 Controls" "Control at tier 7" "MATCH (c:Control {tier: 7}) RETURN count(c);" ">0"
run_test "T033" "T8 ThreatActors" "ThreatActor at tier 8" "MATCH (t:ThreatActor {tier: 8}) RETURN count(t);" ">0"
run_test "T034" "T9 Indicators" "Indicator at tier 9" "MATCH (i:Indicator {tier: 9}) RETURN count(i);" ">0"

# Label Distribution
run_test "T035" "Label Diversity" "Distinct node labels" "CALL db.labels() YIELD label RETURN count(label);" ">10"

# Additional Entity Types
run_test "T036" "CVE Entities" "CVE vulnerability entities" "MATCH (c:CVE) RETURN count(c);" ">0"
run_test "T037" "Exploit Entities" "Exploit entities" "MATCH (e:Exploit) RETURN count(e);" ">0"
run_test "T038" "MalwareVariant" "Malware variant entities" "MATCH (m:MalwareVariant) RETURN count(m);" ">0"
run_test "T039" "Sector Entities" "Sector/Industry entities" "MATCH (s:Sector) RETURN count(s);" ">0"
run_test "T040" "Role Entities" "Role entities" "MATCH (r:Role) RETURN count(r);" ">0"

# Calculate statistics
TOTAL=$((PASSED + FAILED))
if [[ $TOTAL -gt 0 ]]; then
    PASS_RATE=$(awk "BEGIN {printf \"%.2f\", ($PASSED/$TOTAL)*100}")
else
    PASS_RATE="0.00"
fi

# Determine if target met
if (( $(echo "$PASS_RATE >= 95" | bc -l) )); then
    TARGET_MET="YES ✓"
else
    TARGET_MET="NO ✗"
fi

# Add summary
cat >> "$RESULTS" << EOF

## Executive Summary

- **Total Tests**: $TOTAL
- **Passed**: $PASSED ✓
- **Failed**: $FAILED ✗
- **Pass Rate**: ${PASS_RATE}%
- **Target Pass Rate**: 95%
- **Target Met**: $TARGET_MET

## Test Categories

### Core Database (5 tests)
Tests 001-005: Database population and Seldon Crisis entities

### Tier System (6 tests)
Tests 006-011: Hierarchical tier property validation

### Entity Types (14 tests)
Tests 012-026: Various entity type existence checks

### Relationships (2 tests)
Tests 027-028: Relationship existence and diversity

### Properties (2 tests)
Tests 029-030: Property completeness validation

### Tier Queries (4 tests)
Tests 031-034: Sample queries by tier level

### System Metadata (7 tests)
Tests 035-040: Label diversity and additional entity types

---

**Generated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Report File**: $RESULTS
EOF

# Print summary
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "TEST EXECUTION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo "Total Tests:     $TOTAL"
echo "Passed:          $PASSED ✓"
echo "Failed:          $FAILED ✗"
echo "Pass Rate:       ${PASS_RATE}%"
echo "Target Met:      $TARGET_MET"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Results saved to: $RESULTS"
echo ""
