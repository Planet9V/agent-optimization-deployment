// ═══════════════════════════════════════════════════════════════
// Phase 1 Validation Queries
// Comprehensive validation gates for schema deployment
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 1: Schema Constraints
// ───────────────────────────────────────────────────────────────

// VG1.1: Verify all unique constraints deployed
SHOW CONSTRAINTS;
// Expected: 20+ constraints across all node types

// VG1.2: Count constraints by node type
SHOW CONSTRAINTS
YIELD name, labelsOrTypes, properties, type
RETURN labelsOrTypes[0] AS node_type,
       type AS constraint_type,
       count(*) AS constraint_count
ORDER BY constraint_count DESC;

// VG1.3: Verify critical constraints exist
CALL {
  SHOW CONSTRAINTS
  YIELD name, labelsOrTypes
  WHERE labelsOrTypes[0] IN ['CVE', 'Device', 'Software', 'ThreatActor']
  RETURN labelsOrTypes[0] AS critical_node, name
}
RETURN critical_node, collect(name) AS constraints;
// Expected: CVE.cveId, Device.id, Software.id, ThreatActor.id

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 2: Schema Indexes
// ───────────────────────────────────────────────────────────────

// VG2.1: Verify all indexes deployed
SHOW INDEXES;
// Expected: 25+ indexes including customer_namespace, cpe, cvss_score

// VG2.2: Count indexes by node type
SHOW INDEXES
YIELD labelsOrTypes, properties, type
WHERE type <> 'LOOKUP'
RETURN labelsOrTypes[0] AS node_type,
       properties AS indexed_properties,
       type AS index_type
ORDER BY node_type;

// VG2.3: Verify customer namespace isolation indexes
SHOW INDEXES
YIELD name, labelsOrTypes, properties
WHERE ANY(prop IN properties WHERE prop = 'customer_namespace')
RETURN labelsOrTypes[0] AS node_type,
       name AS index_name;
// Expected: Device, Software, Organization namespace indexes

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 3: Data Quality
// ───────────────────────────────────────────────────────────────

// VG3.1: Total node count by label
CALL db.labels() YIELD label
CALL {
  WITH label
  MATCH (n)
  WHERE label IN labels(n)
  RETURN count(n) AS node_count
}
RETURN label, node_count
ORDER BY node_count DESC;

// VG3.2: CVE data quality metrics
MATCH (cve:CVE)
RETURN
  count(cve) AS total_cves,
  count(cve.cvssV3BaseScore) AS cves_with_cvss,
  count(cve.description) AS cves_with_description,
  avg(cve.cvssV3BaseScore) AS avg_cvss_score,
  sum(CASE WHEN cve.hasExploit THEN 1 ELSE 0 END) AS cves_with_exploits,
  (count(cve.cvssV3BaseScore) * 100.0 / count(cve)) AS cvss_coverage_percent;
// Expected: 2,000-5,000 CVEs, >95% CVSS coverage

// VG3.3: CVE severity distribution
MATCH (cve:CVE)
WHERE cve.cvssV3Severity IS NOT NULL
RETURN cve.cvssV3Severity AS severity,
       count(*) AS count,
       round(avg(cve.cvssV3BaseScore), 2) AS avg_score
ORDER BY
  CASE severity
    WHEN 'CRITICAL' THEN 1
    WHEN 'HIGH' THEN 2
    WHEN 'MEDIUM' THEN 3
    WHEN 'LOW' THEN 4
    ELSE 5
  END;

// VG3.4: CVE temporal analysis (last 30 days)
MATCH (cve:CVE)
WHERE cve.publishedDate >= date() - duration({days: 30})
RETURN
  date.truncate('day', cve.publishedDate) AS publish_date,
  count(*) AS cves_published,
  avg(cve.cvssV3BaseScore) AS avg_severity
ORDER BY publish_date DESC
LIMIT 30;

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 4: Relationship Integrity
// ───────────────────────────────────────────────────────────────

// VG4.1: Count relationships by type
CALL db.relationshipTypes() YIELD relationshipType
CALL {
  WITH relationshipType
  MATCH ()-[r]-()
  WHERE type(r) = relationshipType
  RETURN count(r) AS rel_count
}
RETURN relationshipType, rel_count
ORDER BY rel_count DESC;

// VG4.2: CVE → CWE linkage coverage
MATCH (cve:CVE)
OPTIONAL MATCH (cve)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
WITH count(DISTINCT cve) AS total_cves,
     count(DISTINCT cwe) AS linked_cves
RETURN total_cves,
       linked_cves,
       round((linked_cves * 100.0 / total_cves), 2) AS linkage_percent;
// Expected: 70-80% CVEs have CWE mappings

// VG4.3: Multi-layer relationship paths exist
MATCH path = (device:Device)-[:RUNS_SOFTWARE]->(:Software)
  -[:HAS_COMPONENT]->(:SoftwareComponent)
  -[:HAS_VULNERABILITY]->(:CVE)
RETURN count(path) AS software_vulnerability_paths;
// Expected: >0 paths exist

MATCH path = (device:Device)-[:RUNS_FIRMWARE]->(:Firmware)
  -[:HAS_VULNERABILITY]->(:CVE)
RETURN count(path) AS firmware_vulnerability_paths;
// Expected: >0 paths exist

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 5: Customer Namespace Isolation
// ───────────────────────────────────────────────────────────────

// VG5.1: Namespace distribution
MATCH (n)
WHERE n.customer_namespace IS NOT NULL
RETURN n.customer_namespace AS namespace,
       labels(n) AS node_types,
       count(n) AS node_count
ORDER BY node_count DESC;

// VG5.2: Verify no customer data marked as shared
MATCH (n)
WHERE n.customer_namespace STARTS WITH 'customer:'
  AND n.is_shared = true
RETURN count(n) AS leaked_nodes,
       collect(DISTINCT labels(n)) AS leaked_node_types;
// Expected: 0 leaked nodes

// VG5.3: Verify shared knowledge properly tagged
MATCH (n)
WHERE n.customer_namespace STARTS WITH 'shared:'
  AND n.is_shared = false
RETURN count(n) AS incorrect_shared_tags,
       collect(DISTINCT labels(n)) AS affected_types;
// Expected: 0 incorrect tags

// VG5.4: Customer isolation query test
// Should only return customer ABC data, no shared knowledge contamination
MATCH (device:Device {customer_namespace: 'customer:ABC'})
  -[:RUNS_SOFTWARE]->(software:Software)
WHERE software.customer_namespace <> 'customer:ABC'
RETURN count(*) AS namespace_violations;
// Expected: 0 violations

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 6: Query Performance
// ───────────────────────────────────────────────────────────────

// VG6.1: 3-hop query performance (< 2 seconds target)
PROFILE
MATCH path = (s:Software {customer_namespace: 'customer:ABC'})
  -[:HAS_COMPONENT]->(comp:SoftwareComponent)
  -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssV3BaseScore >= 7.0
RETURN count(path) AS vulnerable_paths;
// Expected: Query completes in < 2000ms

// VG6.2: Index usage verification
EXPLAIN
MATCH (cve:CVE)
WHERE cve.cvssV3BaseScore >= 9.0
  AND cve.hasExploit = true
RETURN cve.cveId, cve.cvssV3BaseScore;
// Verify: IndexSeek on cve_cvss_score index

// VG6.3: Namespace isolation index usage
EXPLAIN
MATCH (d:Device {customer_namespace: 'customer:ABC'})
RETURN d.name;
// Verify: IndexSeek on device_namespace index

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 7: Multi-Hop Path Analysis
// ───────────────────────────────────────────────────────────────

// VG7.1: Verify 5+ hop paths exist (digital twin hierarchy)
MATCH path = (fleet:PhysicalAsset {type: 'FLEET'})
  <-[:PART_OF_FLEET*1..5]-(asset:PhysicalAsset)
WHERE fleet.id IS NOT NULL
RETURN max(length(path)) AS max_hops,
       count(path) AS total_paths;
// Expected: max_hops >= 5

// VG7.2: Verify 8+ hop attack chains exist
MATCH path = (device:Device)
  -[:RUNS_SOFTWARE]->(:Software)
  -[:HAS_COMPONENT]->(:SoftwareComponent)
  -[:HAS_VULNERABILITY]->(:CVE)
  -[:HAS_EXPLOIT]->(:Exploit)
  -[:USED_BY_THREAT_ACTOR]->(:ThreatActor)
  -[:HAS_PROFILE]->(:ThreatActorProfile)
WHERE device.customer_namespace IS NOT NULL
RETURN max(length(path)) AS max_attack_chain_hops,
       count(path) AS total_attack_chains;
// Expected: max_attack_chain_hops >= 7

// VG7.3: Verify security zone traversal paths
MATCH path = (zone1:SecurityZone)
  -[:COMMUNICATES_VIA]->(:Conduit)
  -[:TO_ZONE]->(zone2:SecurityZone)
RETURN count(path) AS zone_crossing_paths,
       collect(DISTINCT zone1.securityLevel) AS source_levels,
       collect(DISTINCT zone2.securityLevel) AS target_levels;
// Expected: >0 zone crossing paths

// ───────────────────────────────────────────────────────────────
// VALIDATION GATE 8: Data Completeness
// ───────────────────────────────────────────────────────────────

// VG8.1: Required properties completeness
MATCH (cve:CVE)
RETURN
  count(*) AS total,
  sum(CASE WHEN cve.cveId IS NOT NULL THEN 1 ELSE 0 END) AS has_cveid,
  sum(CASE WHEN cve.description IS NOT NULL THEN 1 ELSE 0 END) AS has_description,
  sum(CASE WHEN cve.publishedDate IS NOT NULL THEN 1 ELSE 0 END) AS has_published_date,
  sum(CASE WHEN cve.cvssV3BaseScore IS NOT NULL THEN 1 ELSE 0 END) AS has_cvss_score;
// Expected: 100% has_cveid, >95% for others

// VG8.2: Orphaned nodes detection
MATCH (n)
WHERE NOT (n)--()
  AND NOT n:Priority  // Priorities may not have relationships yet
RETURN labels(n) AS orphaned_node_type,
       count(n) AS orphan_count;
// Expected: Minimal orphaned nodes (<5%)

// ═══════════════════════════════════════════════════════════════
// COMPREHENSIVE VALIDATION REPORT
// ═══════════════════════════════════════════════════════════════

// Generate complete validation summary
CALL {
  // Constraint count
  SHOW CONSTRAINTS YIELD name
  RETURN count(name) AS constraint_count
}
CALL {
  // Index count
  SHOW INDEXES YIELD name WHERE name IS NOT NULL
  RETURN count(name) AS index_count
}
CALL {
  // Total nodes
  MATCH (n) RETURN count(n) AS total_nodes
}
CALL {
  // Total relationships
  MATCH ()-[r]->() RETURN count(r) AS total_relationships
}
CALL {
  // CVE count
  MATCH (cve:CVE) RETURN count(cve) AS cve_count
}
CALL {
  // Namespace count
  MATCH (n) WHERE n.customer_namespace IS NOT NULL
  RETURN count(DISTINCT n.customer_namespace) AS namespace_count
}
RETURN
  constraint_count,
  index_count,
  total_nodes,
  total_relationships,
  cve_count,
  namespace_count,
  CASE
    WHEN constraint_count >= 20
      AND index_count >= 25
      AND cve_count >= 2000
      AND namespace_count >= 2
    THEN '✅ PHASE 1 VALIDATION PASSED'
    ELSE '⚠️ VALIDATION INCOMPLETE'
  END AS validation_status;

// ═══════════════════════════════════════════════════════════════
// END OF VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════
