#!/bin/bash
# ========================================
# STEP 5 VALIDATION EXECUTION SCRIPT
# File: step5_execute_validations.sh
# Created: 2025-10-30
# Purpose: Execute all critical validation tests
# ========================================

NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="adminadmin"
OUTPUT_DIR="validation_results"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')

echo "=========================================="
echo "STEP 5: CRITICAL VALIDATION EXECUTION"
echo "=========================================="
echo "Timestamp: $TIMESTAMP"
echo ""

mkdir -p "$OUTPUT_DIR"

# Validation 1: CVE Count Verification
echo "=========================================="
echo "VALIDATION 1: CVE Count Verification"
echo "EXPECTED: 147,923"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "MATCH (cve:CVE) RETURN count(cve) AS cve_count;" \
  > "$OUTPUT_DIR/validation_1_cve_count_$TIMESTAMP.txt" 2>&1

CVE_COUNT=$(grep -oP '\d+' "$OUTPUT_DIR/validation_1_cve_count_$TIMESTAMP.txt" | tail -1)
echo "Result: $CVE_COUNT CVEs found"
if [ "$CVE_COUNT" == "147923" ]; then
  echo "✅ PASS: CVE count matches expected value"
  VALIDATION_1_STATUS="PASS"
else
  echo "❌ FAIL: CVE count mismatch! ABORT IMPLEMENTATION!"
  VALIDATION_1_STATUS="FAIL"
fi
echo ""

# Validation 2: CVE Modification Check
echo "=========================================="
echo "VALIDATION 2: CVE Modification Check"
echo "EXPECTED: 0 (no CVEs should have customer properties)"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "MATCH (cve:CVE) WHERE EXISTS(cve.customer_id) OR EXISTS(cve.organization_id) OR EXISTS(cve.asset_owner) RETURN count(cve) AS incorrectly_modified_cves;" \
  > "$OUTPUT_DIR/validation_2_cve_modification_$TIMESTAMP.txt" 2>&1

MODIFIED_CVES=$(grep -oP '\d+' "$OUTPUT_DIR/validation_2_cve_modification_$TIMESTAMP.txt" | tail -1)
echo "Result: $MODIFIED_CVES CVEs with customer properties"
if [ "$MODIFIED_CVES" == "0" ]; then
  echo "✅ PASS: No CVEs were incorrectly modified"
  VALIDATION_2_STATUS="PASS"
else
  echo "❌ FAIL: CVEs have customer properties! ABORT AND ROLLBACK!"
  VALIDATION_2_STATUS="FAIL"
fi
echo ""

# Validation 3: Customer Filtering Test
echo "=========================================="
echo "VALIDATION 3: Customer Filtering Test"
echo "Testing Customer CUST-001-ENERGY equipment filtering"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset) RETURN labels(asset)[0] AS asset_type, count(asset) AS my_equipment_count;" \
  > "$OUTPUT_DIR/validation_3_customer_filtering_$TIMESTAMP.txt" 2>&1

cat "$OUTPUT_DIR/validation_3_customer_filtering_$TIMESTAMP.txt"
EQUIPMENT_COUNT=$(grep -oP '\d+' "$OUTPUT_DIR/validation_3_customer_filtering_$TIMESTAMP.txt" | tail -1)
if [ "$EQUIPMENT_COUNT" -gt "0" ]; then
  echo "✅ PASS: Customer filtering returns equipment"
  VALIDATION_3_STATUS="PASS"
else
  echo "⚠️ WARNING: No equipment found for customer"
  VALIDATION_3_STATUS="WARNING"
fi
echo ""

# Validation 4: CVE Impact Query Test
echo "=========================================="
echo "VALIDATION 4: CVE Impact Query Test (Question 1)"
echo "Testing MY equipment vulnerability query"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "MATCH (customer:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(server:Server) MATCH (server)-[:RUNS]->(app:Application)-[:CONTAINS]->(comp:SoftwareComponent)-[:HAS_VULNERABILITY]->(cve:CVE) WHERE cve.cvss_base_score >= 7.0 RETURN server.hostname AS my_equipment, comp.name AS vulnerable_component, cve.cve_id AS cve_id LIMIT 5;" \
  > "$OUTPUT_DIR/validation_4_cve_impact_query_$TIMESTAMP.txt" 2>&1

cat "$OUTPUT_DIR/validation_4_cve_impact_query_$TIMESTAMP.txt"
VULN_RESULTS=$(grep -c "my_equipment" "$OUTPUT_DIR/validation_4_cve_impact_query_$TIMESTAMP.txt" || echo "0")
if [ "$VULN_RESULTS" -gt "0" ]; then
  echo "✅ PASS: CVE impact query returns results"
  VALIDATION_4_STATUS="PASS"
else
  echo "ℹ️ INFO: No vulnerabilities found (may be expected)"
  VALIDATION_4_STATUS="INFO"
fi
echo ""

# Validation 5: Multi-Customer Isolation Test
echo "=========================================="
echo "VALIDATION 5: Multi-Customer Isolation Test"
echo "EXPECTED: 0 (no incorrectly shared assets)"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset1) MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})-[:OWNS_EQUIPMENT]->(asset2) WHERE asset1 = asset2 AND asset1.shared_asset <> true RETURN count(asset1) AS incorrectly_shared_assets;" \
  > "$OUTPUT_DIR/validation_5_isolation_test_$TIMESTAMP.txt" 2>&1

SHARED_ASSETS=$(grep -oP '\d+' "$OUTPUT_DIR/validation_5_isolation_test_$TIMESTAMP.txt" | tail -1)
echo "Result: $SHARED_ASSETS incorrectly shared assets"
if [ "$SHARED_ASSETS" == "0" ]; then
  echo "✅ PASS: Customer isolation maintained"
  VALIDATION_5_STATUS="PASS"
else
  echo "❌ FAIL: Assets incorrectly shared between customers"
  VALIDATION_5_STATUS="FAIL"
fi
echo ""

# Validation 6: Comprehensive Report
echo "=========================================="
echo "VALIDATION 6: Comprehensive Validation Report"
echo "=========================================="
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  --format plain \
  "CALL { MATCH (cve:CVE) RETURN count(cve) AS cve_count } CALL { MATCH (c:Customer) RETURN count(c) AS customer_count } CALL { MATCH (o:Organization) RETURN count(o) AS organization_count } CALL { MATCH (asset) WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device) AND asset.customer_id IS NOT NULL RETURN count(asset) AS assigned_assets } CALL { MATCH (:Customer)-[r:OWNS_EQUIPMENT]->() RETURN count(r) AS ownership_relationships } RETURN cve_count, customer_count, organization_count, assigned_assets, ownership_relationships, CASE WHEN cve_count = 147923 THEN '✅ PASS' ELSE '❌ FAIL' END AS cve_preservation_check;" \
  > "$OUTPUT_DIR/validation_6_comprehensive_report_$TIMESTAMP.txt" 2>&1

cat "$OUTPUT_DIR/validation_6_comprehensive_report_$TIMESTAMP.txt"
PRESERVATION_STATUS=$(grep -oP '(✅ PASS|❌ FAIL)' "$OUTPUT_DIR/validation_6_comprehensive_report_$TIMESTAMP.txt" | tail -1)
echo "CVE Preservation: $PRESERVATION_STATUS"
VALIDATION_6_STATUS="$PRESERVATION_STATUS"
echo ""

# Final Summary
echo "=========================================="
echo "VALIDATION SUMMARY"
echo "=========================================="
echo "Timestamp: $TIMESTAMP"
echo ""
echo "Validation 1 (CVE Count):              $VALIDATION_1_STATUS"
echo "Validation 2 (CVE Modification):       $VALIDATION_2_STATUS"
echo "Validation 3 (Customer Filtering):     $VALIDATION_3_STATUS"
echo "Validation 4 (CVE Impact Query):       $VALIDATION_4_STATUS"
echo "Validation 5 (Multi-Customer Isolation): $VALIDATION_5_STATUS"
echo "Validation 6 (Comprehensive Report):   $VALIDATION_6_STATUS"
echo ""

# GO/NO-GO Decision
if [ "$VALIDATION_1_STATUS" == "PASS" ] && [ "$VALIDATION_2_STATUS" == "PASS" ] && [ "$VALIDATION_5_STATUS" == "PASS" ]; then
  echo "=========================================="
  echo "✅ FINAL DECISION: GO"
  echo "=========================================="
  echo "All critical validations passed."
  echo "Customer/Organization implementation is successful."
  echo "CVE preservation confirmed (147,923 nodes intact)."
  echo "Multi-tenant isolation validated."
  echo ""
  echo "READY FOR PRODUCTION USE"
  exit 0
else
  echo "=========================================="
  echo "❌ FINAL DECISION: NO-GO"
  echo "=========================================="
  echo "Critical validation failures detected."
  echo "DO NOT PROCEED TO PRODUCTION."
  echo ""
  echo "RECOMMENDED ACTION: Execute rollback procedure"
  exit 1
fi
