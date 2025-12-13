// ═══════════════════════════════════════════════════════════════════════════
// VALIDATION QUERIES - COMPREHENSIVE SYSTEM VALIDATION
// Database: Neo4j 5.x (bolt://localhost:7687)
// Validation Date: 2025-12-12
// Purpose: Concrete examples of validation queries and findings
// ═══════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────
// 1. SCHEMA ANALYSIS QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 1.1 Check super label coverage
MATCH (n)
RETURN
  count(n) as total_nodes,
  count(CASE WHEN any(label IN labels(n) WHERE label IN [
    'ThreatActor', 'Malware', 'AttackPattern', 'Vulnerability',
    'Indicator', 'Campaign', 'Asset', 'Organization', 'Location',
    'User', 'Software', 'Event', 'Control', 'PsychTrait', 'Role', 'EconomicMetric'
  ]) THEN 1 END) as nodes_with_super_labels,
  count(CASE WHEN NOT any(label IN labels(n) WHERE label IN [
    'ThreatActor', 'Malware', 'AttackPattern', 'Vulnerability',
    'Indicator', 'Campaign', 'Asset', 'Organization', 'Location',
    'User', 'Software', 'Event', 'Control', 'PsychTrait', 'Role', 'EconomicMetric'
  ]) THEN 1 END) as nodes_without_super_labels;

// Expected: total_nodes: 1,207,032
// Actual: nodes_with_super_labels: 83,052 (6.9%)
// Finding: 93.1% of nodes lack super label classification


// 1.2 Check property discriminator implementation
MATCH (n)
WHERE n.fine_grained_type IS NOT NULL
RETURN
  labels(n)[0] as label,
  count(n) as count,
  collect(DISTINCT n.fine_grained_type)[0..5] as sample_types
ORDER BY count DESC;

// Expected: All nodes have fine_grained_type
// Actual: 7,950 nodes (0.66% of total)
// Finding: Property discriminators only on recent ingestion


// 1.3 Check hierarchical property coverage
MATCH (n)
RETURN
  count(n) as total_nodes,
  count(CASE WHEN n.tier IS NOT NULL THEN 1 END) as nodes_with_tier,
  count(CASE WHEN n.hierarchy_path IS NOT NULL THEN 1 END) as nodes_with_hierarchy_path,
  count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) as nodes_with_fine_grained_type;

// Expected: All nodes have hierarchical properties
// Actual: tier: 7,950, hierarchy_path: 0, fine_grained_type: 7,950
// Finding: Hierarchical properties missing on 99% of nodes


// ───────────────────────────────────────────────────────────────────────────
// 2. RELATIONSHIP ONTOLOGY QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 2.1 Count orphan nodes
MATCH (n)
WHERE NOT (n)--()
RETURN count(n) as orphan_nodes;

// Expected: Low orphan rate (<5%)
// Actual: 698,127 orphan nodes (58% of database)
// Finding: CRITICAL - More than half of nodes disconnected


// 2.2 CVE orphan analysis
MATCH (cve:CVE)
OPTIONAL MATCH (cve)-[r]-()
WITH cve, count(r) as rel_count
RETURN
  count(cve) as total_cve_nodes,
  count(CASE WHEN rel_count = 0 THEN 1 END) as orphan_cves,
  (count(CASE WHEN rel_count = 0 THEN 1 END) * 100.0 / count(cve)) as orphan_percentage;

// Expected: <10% orphan rate
// Actual: 280,872 orphan CVEs (88.7%)
// Finding: CRITICAL - CVE nodes lack vulnerability-to-software relationships


// 2.3 Relationship type distribution
CALL db.relationshipTypes() YIELD relationshipType
CALL apoc.cypher.run(
  'MATCH ()-[r:' + relationshipType + ']->() RETURN count(r) as count',
  {}
) YIELD value
RETURN relationshipType, value.count as count
ORDER BY count DESC
LIMIT 20;

// Expected: USES, TARGETS, EXPLOITS, AFFECTS in top 10
// Actual: IMPACTS (39.5%), VULNERABLE_TO (25.7%) dominate
// Finding: Bulk ingestion relationships differ from expected patterns


// 2.4 Recent relationship creation validation
MATCH ()-[r]->()
WHERE r.created_at >= datetime('2025-12-11T00:00:00Z')
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC;

// Expected: Recent ingestion created pattern-based relationships
// Actual: 216,973 relationships with expected types (USES, TARGETS, etc.)
// Finding: New pipeline creates correct relationship patterns


// ───────────────────────────────────────────────────────────────────────────
// 3. 20-HOP PATH VALIDATION QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 3.1 Test basic cyber kill chain (5-hop)
MATCH path = (ta:ThreatActor)-[:USES]->
              (m:Malware)-[:EXPLOITS]->
              (v:Vulnerability)-[:AFFECTS]->
              (s:Software)-[:INSTALLED_ON]->
              (d:Device)
WHERE ta.name CONTAINS "APT"
RETURN path
LIMIT 5;

// Expected: Multiple complete kill chain paths
// Actual: Empty or incomplete results
// Finding: Path broken at Vulnerability node (88.7% orphaned)


// 3.2 Find maximum path depth in graph
MATCH path = (start)-[*1..10]->(end)
WHERE NOT (end)-->()
RETURN length(path) as path_length, count(*) as count
ORDER BY path_length DESC
LIMIT 10;

// Expected: Paths up to 20 hops
// Actual: Limited by orphan nodes fragmenting graph
// Finding: Graph density good but fragmentation prevents long paths


// 3.3 Concrete example: WannaCry to Siemens PLC
MATCH path = (m:Malware {name: "WannaCry"})-[:EXPLOITS]->
              (cve:CVE)-[:AFFECTS]->
              (software:Software)-[:INSTALLED_ON]->
              (device:Device)
WHERE device.vendor CONTAINS "Siemens"
  AND device.type CONTAINS "PLC"
RETURN path;

// Expected: WannaCry → CVE-2017-0144 → Windows SMB → Siemens PLC
// Actual: Empty (CVE relationships missing)
// Finding: Use case blocked by orphan CVEs


// ───────────────────────────────────────────────────────────────────────────
// 4. PROPERTY DISCRIMINATOR VALIDATION QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 4.1 Check for actorType property
MATCH (ta:ThreatActor)
RETURN
  count(ta) as total_threat_actors,
  count(CASE WHEN ta.actorType IS NOT NULL THEN 1 END) as with_actor_type,
  collect(DISTINCT ta.actorType)[0..5] as sample_types;

// Expected: All ThreatActor nodes have actorType
// Actual: 0 nodes with actorType
// Finding: Property discriminator not implemented


// 4.2 Check for malwareFamily property
MATCH (m:Malware)
RETURN
  count(m) as total_malware,
  count(CASE WHEN m.malwareFamily IS NOT NULL THEN 1 END) as with_malware_family,
  collect(DISTINCT m.malwareFamily)[0..5] as sample_families;

// Expected: All Malware nodes have malwareFamily
// Actual: 0 nodes with malwareFamily
// Finding: Property discriminator not implemented


// 4.3 Test fine-grained type query (should work on recent data)
MATCH (n)
WHERE n.fine_grained_type IS NOT NULL
RETURN
  labels(n)[0] as super_label,
  n.fine_grained_type as fine_type,
  count(n) as count
ORDER BY count DESC;

// Expected: 566 different fine-grained types
// Actual: Limited types, only on 7,950 nodes (0.66%)
// Finding: System works for recent data, legacy data incomplete


// ───────────────────────────────────────────────────────────────────────────
// 5. QDRANT-NEO4J ALIGNMENT VALIDATION QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 5.1 Check for Qdrant-expected properties
MATCH (n)
RETURN
  count(n) as total_nodes,
  count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) as has_fine_type,
  count(CASE WHEN n.hierarchy_path IS NOT NULL THEN 1 END) as has_hierarchy_path,
  count(CASE WHEN n.confidence IS NOT NULL THEN 1 END) as has_confidence,
  count(CASE WHEN n.ner_label IS NOT NULL THEN 1 END) as has_ner_label;

// Expected: All nodes have Qdrant-compatible properties
// Actual: Most properties missing
// Finding: Neo4j not aligned with Qdrant payload schema


// 5.2 Validate ID alignment for cross-system queries
MATCH (n)
WHERE n.id IS NOT NULL
RETURN count(n) as nodes_with_ids;

// Expected: All nodes have IDs for cross-system lookup
// Actual: 701,282 nodes have IDs (58%)
// Finding: 42% of nodes cannot be referenced from Qdrant


// 5.3 Check for recent ingestion with complete properties
MATCH (n)
WHERE n.created_at >= datetime('2025-12-11T00:00:00Z')
  AND n.fine_grained_type IS NOT NULL
  AND n.ner_label IS NOT NULL
RETURN count(n) as nodes_with_complete_properties;

// Expected: Recent ingestion complete
// Actual: ~7,950 nodes with properties
// Finding: Recent pipeline correctly implements Qdrant alignment


// ───────────────────────────────────────────────────────────────────────────
// 6. DATA QUALITY MONITORING QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 6.1 Missing ID analysis by label
MATCH (n)
WHERE n.id IS NULL
WITH labels(n)[0] as label, count(n) as count
RETURN label, count
ORDER BY count DESC
LIMIT 20;

// Finding: Measurement (166,400), Control (56,007), Entity (55,569) top missing IDs


// 6.2 Duplicate node detection (Control example)
MATCH (c:Control)
WHERE c.id IS NOT NULL
WITH c.id as control_id, collect(c) as nodes
WHERE size(nodes) > 1
RETURN control_id, size(nodes) as duplicate_count
ORDER BY duplicate_count DESC
LIMIT 10;

// Expected: No duplicates
// Actual: Some Control IDs with 32.9x duplication
// Finding: MERGE operations not enforced for Control nodes


// 6.3 Tier distribution validation
MATCH (n)
WHERE n.tier IS NOT NULL
RETURN n.tier as tier, count(n) as count
ORDER BY tier;

// Expected: tier2_count > tier1_count (hierarchy depth validation)
// Actual: tier1: 7,907, tier2: 43
// Finding: Tier2 not greater than tier1 (validation failed)


// ───────────────────────────────────────────────────────────────────────────
// 7. REMEDIATION VALIDATION QUERIES
// ───────────────────────────────────────────────────────────────────────────

// 7.1 Count nodes requiring property backfill
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
    'ThreatActor', 'Malware', 'AttackPattern', 'Vulnerability',
    'Indicator', 'Campaign', 'Asset', 'Organization', 'Location',
    'User', 'Software', 'Event', 'Control', 'PsychTrait', 'Role', 'EconomicMetric'
  ])
  AND n.fine_grained_type IS NULL
RETURN count(n) as nodes_requiring_property_backfill;

// Result: ~75,000 nodes requiring backfill


// 7.2 Count orphan nodes by type for prioritization
MATCH (n)
WHERE NOT (n)--()
WITH labels(n)[0] as label, count(n) as orphan_count
RETURN label, orphan_count
ORDER BY orphan_count DESC
LIMIT 20;

// Priority targets: CVE (280,872), Measurement (131,538), Entity (49,242)


// 7.3 Estimate relationship creation impact
MATCH (cve:CVE)
WHERE NOT (cve)--()
RETURN count(cve) as orphan_cves_to_fix;

// Result: 280,872 CVE nodes need AFFECTS relationships
// Estimated relationships to create: ~500,000


// ───────────────────────────────────────────────────────────────────────────
// 8. BASELINE METRICS FOR POST-REMEDIATION COMPARISON
// ───────────────────────────────────────────────────────────────────────────

// 8.1 Current baseline
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
WITH n, count(r) as rel_count
RETURN
  count(n) as total_nodes,
  count(CASE WHEN rel_count = 0 THEN 1 END) as orphan_nodes,
  (count(CASE WHEN rel_count = 0 THEN 1 END) * 100.0 / count(n)) as orphan_percentage,
  count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) as nodes_with_properties,
  (count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) * 100.0 / count(n)) as property_coverage_percentage;

// Baseline: 58% orphan rate, 0.66% property coverage
// Target: <10% orphan rate, >95% property coverage


// 8.2 Relationship count baseline
MATCH ()-[r]->()
RETURN count(r) as total_relationships;

// Baseline: 12,108,716 relationships
// Target after remediation: ~13,000,000+ (add ~1M CVE relationships)


// ═══════════════════════════════════════════════════════════════════════════
// VALIDATION SUMMARY
// ═══════════════════════════════════════════════════════════════════════════
//
// Status: COMPLETE
// Critical Findings: 5
// Validation Date: 2025-12-12
// Database: Neo4j 5.x (1,207,032 nodes, 12,108,716 relationships)
//
// Key Metrics:
//   - Super label coverage: 6.9% (target: >95%)
//   - Property discriminators: 0.66% (target: >95%)
//   - Orphan nodes: 58% (target: <10%)
//   - Missing IDs: 42% (target: 0%)
//   - 20-hop capability: BLOCKED (target: FUNCTIONAL)
//
// Recommended Actions:
//   1. Execute Schema v3.1 Property Backfill (40 hours)
//   2. Fix CVE Orphan Nodes (30 hours)
//   3. Backfill Missing Node IDs (20 hours)
//   4. Fix SBOM Dependency Relationships (25 hours)
//   5. Align Qdrant-Neo4j Properties (30 hours)
//
// Total Remediation Effort: 190 hours (5-6 weeks)
//
// ═══════════════════════════════════════════════════════════════════════════
