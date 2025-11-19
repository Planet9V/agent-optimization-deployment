// ========================================
// STEP 5: CRITICAL VALIDATION QUERIES
// File: step5_validation_queries.cypher
// Created: 2025-10-30
// Purpose: Validate CVE preservation and customer implementation
// ========================================

// ========================================
// VALIDATION 1: CVE Count Verification
// CRITICAL: EXPECTED = 147,923
// ========================================
MATCH (cve:CVE)
RETURN count(cve) AS cve_count;

// ========================================
// VALIDATION 2: CVE Modification Check
// CRITICAL: EXPECTED = 0
// ========================================
MATCH (cve:CVE)
WHERE EXISTS(cve.customer_id) OR EXISTS(cve.organization_id) OR EXISTS(cve.asset_owner)
RETURN count(cve) AS incorrectly_modified_cves;

// ========================================
// VALIDATION 3: Customer Filtering Test
// ========================================
MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset)
RETURN
  labels(asset)[0] AS asset_type,
  count(asset) AS my_equipment_count;

// ========================================
// VALIDATION 4: CVE Impact Query Test (Question 1)
// ========================================
MATCH (customer:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(server:Server)
MATCH (server)-[:RUNS]->(app:Application)
      -[:CONTAINS]->(comp:SoftwareComponent)
      -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_base_score >= 7.0
RETURN
  server.hostname AS my_equipment,
  comp.name AS vulnerable_component,
  cve.cve_id AS cve_id
LIMIT 5;

// ========================================
// VALIDATION 5: Multi-Customer Isolation Test
// EXPECTED: 0
// ========================================
MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset1)
MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})-[:OWNS_EQUIPMENT]->(asset2)
WHERE asset1 = asset2 AND asset1.shared_asset <> true
RETURN count(asset1) AS incorrectly_shared_assets;

// ========================================
// VALIDATION 6: Comprehensive Validation Report
// ========================================
CALL {
  MATCH (cve:CVE) RETURN count(cve) AS cve_count
}
CALL {
  MATCH (c:Customer) RETURN count(c) AS customer_count
}
CALL {
  MATCH (o:Organization) RETURN count(o) AS organization_count
}
CALL {
  MATCH (asset)
  WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
    AND asset.customer_id IS NOT NULL
  RETURN count(asset) AS assigned_assets
}
CALL {
  MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
  RETURN count(r) AS ownership_relationships
}
RETURN
  cve_count,
  customer_count,
  organization_count,
  assigned_assets,
  ownership_relationships,
  CASE WHEN cve_count = 147923 THEN '✅ PASS' ELSE '❌ FAIL' END AS cve_preservation_check;
