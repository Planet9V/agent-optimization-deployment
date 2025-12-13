// ============================================================================
// AEON v3.1 Schema Validation Queries
// ============================================================================
// Use these queries to verify the hierarchical schema fix worked correctly
//
// File: VALIDATION_QUERIES.cypher
// Created: 2025-12-12
// Version: 1.0.0
// ============================================================================

// ============================================================================
// VALIDATION 1: Node Count Preservation
// ============================================================================
// REQUIREMENT: Total node count should not decrease (baseline: 1,104,066)
// EXPECTED: >= 1,104,066 nodes

MATCH (n)
RETURN count(n) as total_nodes;

// Expected: 1,426,989 (or higher if new data added)
// Status: PASS if >= 1,104,066


// ============================================================================
// VALIDATION 2: Super Label Coverage
// ============================================================================
// REQUIREMENT: All nodes should have at least one super label
// EXPECTED: 100% coverage (or close to it)

// Count nodes WITH super labels
MATCH (n)
WHERE n:ThreatActor OR n:Malware OR n:Technique OR n:Vulnerability OR
      n:Indicator OR n:Campaign OR n:Asset OR n:Organization OR
      n:Location OR n:PsychTrait OR n:EconomicMetric OR n:Protocol OR
      n:Role OR n:Software OR n:Control OR n:Event
RETURN count(n) as nodes_with_super_labels;

// Expected: ~1,400,000+ nodes
// Status: PASS if > 1,000,000


// Total coverage percentage
MATCH (n)
OPTIONAL MATCH (s)
WHERE s:ThreatActor OR s:Malware OR s:Technique OR s:Vulnerability OR
      s:Indicator OR s:Campaign OR s:Asset OR s:Organization OR
      s:Location OR s:PsychTrait OR s:EconomicMetric OR s:Protocol OR
      s:Role OR s:Software OR s:Control OR s:Event
WITH count(DISTINCT n) as total, count(DISTINCT s) as with_super
RETURN total,
       with_super,
       round(100.0 * with_super / total, 2) as coverage_pct;

// Expected: coverage_pct > 50%
// Status: PASS if > 50%


// ============================================================================
// VALIDATION 3: Tier Property Coverage
// ============================================================================
// REQUIREMENT: All super-labeled nodes should have tier1, tier2, tier properties
// EXPECTED: 100% of super-labeled nodes have tier properties

MATCH (n)
WHERE n:ThreatActor OR n:Malware OR n:Technique OR n:Vulnerability OR
      n:Indicator OR n:Campaign OR n:Asset OR n:Organization OR
      n:Location OR n:PsychTrait OR n:EconomicMetric OR n:Protocol OR
      n:Role OR n:Software OR n:Control OR n:Event
RETURN
  count(CASE WHEN n.tier1 IS NOT NULL THEN 1 END) as with_tier1,
  count(CASE WHEN n.tier2 IS NOT NULL THEN 1 END) as with_tier2,
  count(CASE WHEN n.tier IS NOT NULL THEN 1 END) as with_tier,
  count(n) as total_super_labeled_nodes,
  round(100.0 * count(CASE WHEN n.tier IS NOT NULL THEN 1 END) / count(n), 2) as tier_coverage_pct;

// Expected: tier_coverage_pct ~100%
// Status: PASS if > 90%


// ============================================================================
// VALIDATION 4: Tier Distribution
// ============================================================================
// REQUIREMENT: Tier 2 + Tier 3 > Tier 1 (validates hierarchy depth)
// EXPECTED: More tier 2 and tier 3 entities than tier 1

MATCH (n)
WHERE n.tier IS NOT NULL
RETURN n.tier as tier, count(n) as count
ORDER BY tier;

// Expected:
// tier 1 (TECHNICAL): ~300,000-500,000
// tier 2 (OPERATIONAL/ASSET/ORGANIZATIONAL): ~500,000-700,000
// tier 3 (CONTEXTUAL): ~200,000-400,000
// Status: PASS if (tier2_count + tier3_count) > tier1_count


// Validation check
MATCH (n)
WHERE n.tier IS NOT NULL
WITH n.tier as tier, count(n) as count
WITH collect({tier: tier, count: count}) as tier_counts
WITH [x IN tier_counts WHERE x.tier = 1 | x.count][0] as tier1_count,
     [x IN tier_counts WHERE x.tier = 2 | x.count][0] as tier2_count,
     [x IN tier_counts WHERE x.tier = 3 | x.count][0] as tier3_count
RETURN
  tier1_count,
  tier2_count,
  tier3_count,
  (tier2_count + tier3_count) > tier1_count as validation_passed;

// Expected: validation_passed = true
// Status: PASS if validation_passed = true


// ============================================================================
// VALIDATION 5: Property Discriminator Coverage
// ============================================================================
// REQUIREMENT: Super-labeled nodes should have property discriminators
// EXPECTED: Significant coverage (>30%)

MATCH (n)
WHERE n:ThreatActor OR n:Malware OR n:Technique OR n:Vulnerability OR
      n:Indicator OR n:Campaign OR n:Asset OR n:Organization OR
      n:Location OR n:PsychTrait OR n:EconomicMetric OR n:Protocol OR
      n:Role OR n:Software OR n:Control OR n:Event
RETURN
  count(CASE WHEN n.actorType IS NOT NULL THEN 1 END) as with_actorType,
  count(CASE WHEN n.malwareFamily IS NOT NULL THEN 1 END) as with_malwareFamily,
  count(CASE WHEN n.patternType IS NOT NULL THEN 1 END) as with_patternType,
  count(CASE WHEN n.vulnType IS NOT NULL THEN 1 END) as with_vulnType,
  count(CASE WHEN n.indicatorType IS NOT NULL THEN 1 END) as with_indicatorType,
  count(CASE WHEN n.campaignType IS NOT NULL THEN 1 END) as with_campaignType,
  count(CASE WHEN n.assetClass IS NOT NULL THEN 1 END) as with_assetClass,
  count(n) as total_nodes;

// Expected: Each discriminator should have counts
// Status: PASS if total discriminators > 30% of total_nodes


// ============================================================================
// VALIDATION 6: CVE Vulnerability Classification
// ============================================================================
// REQUIREMENT: All CVE nodes should have Vulnerability super label
// EXPECTED: 0 unclassified CVE nodes

MATCH (n:CVE)
WHERE NOT n:Vulnerability
RETURN count(n) as unclassified_cves;

// Expected: 0
// Status: PASS if = 0


// Verify CVE nodes have Vulnerability label
MATCH (n:CVE)
WHERE n:Vulnerability
RETURN count(n) as cve_nodes_with_vulnerability_label;

// Expected: ~316,552 (all CVEs)
// Status: PASS if matches total CVE count


// ============================================================================
// VALIDATION 7: Super Label Distribution
// ============================================================================
// REQUIREMENT: All 16 super labels should be in use
// EXPECTED: Non-zero counts for all 16 labels

MATCH (n:ThreatActor) RETURN 'ThreatActor' as label, count(n) as count
UNION
MATCH (n:Malware) RETURN 'Malware' as label, count(n) as count
UNION
MATCH (n:Technique) RETURN 'Technique' as label, count(n) as count
UNION
MATCH (n:Vulnerability) RETURN 'Vulnerability' as label, count(n) as count
UNION
MATCH (n:Indicator) RETURN 'Indicator' as label, count(n) as count
UNION
MATCH (n:Campaign) RETURN 'Campaign' as label, count(n) as count
UNION
MATCH (n:Asset) RETURN 'Asset' as label, count(n) as count
UNION
MATCH (n:Organization) RETURN 'Organization' as label, count(n) as count
UNION
MATCH (n:Location) RETURN 'Location' as label, count(n) as count
UNION
MATCH (n:PsychTrait) RETURN 'PsychTrait' as label, count(n) as count
UNION
MATCH (n:EconomicMetric) RETURN 'EconomicMetric' as label, count(n) as count
UNION
MATCH (n:Protocol) RETURN 'Protocol' as label, count(n) as count
UNION
MATCH (n:Role) RETURN 'Role' as label, count(n) as count
UNION
MATCH (n:Software) RETURN 'Software' as label, count(n) as count
UNION
MATCH (n:Control) RETURN 'Control' as label, count(n) as count
UNION
MATCH (n:Event) RETURN 'Event' as label, count(n) as count
ORDER BY count DESC;

// Expected: All 16 labels with non-zero counts
// Status: PASS if all 16 labels present


// ============================================================================
// VALIDATION 8: Hierarchical Property Consistency
// ============================================================================
// REQUIREMENT: All nodes with tier property should also have tier1, tier2
// EXPECTED: 100% consistency

MATCH (n)
WHERE n.tier IS NOT NULL
RETURN
  count(CASE WHEN n.tier1 IS NULL THEN 1 END) as missing_tier1,
  count(CASE WHEN n.tier2 IS NULL THEN 1 END) as missing_tier2,
  count(CASE WHEN n.super_label IS NULL THEN 1 END) as missing_super_label,
  count(CASE WHEN n.hierarchy_path IS NULL THEN 1 END) as missing_hierarchy_path,
  count(n) as total_nodes_with_tier;

// Expected: All counts = 0
// Status: PASS if all missing_* = 0


// ============================================================================
// VALIDATION 9: Fine-Grained Type Assignment
// ============================================================================
// REQUIREMENT: All super-labeled nodes should have fine_grained_type
// EXPECTED: High coverage (>80%)

MATCH (n)
WHERE n:ThreatActor OR n:Malware OR n:Technique OR n:Vulnerability OR
      n:Indicator OR n:Campaign OR n:Asset OR n:Organization OR
      n:Location OR n:PsychTrait OR n:EconomicMetric OR n:Protocol OR
      n:Role OR n:Software OR n:Control OR n:Event
RETURN
  count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) as with_fine_grained_type,
  count(n) as total,
  round(100.0 * count(CASE WHEN n.fine_grained_type IS NOT NULL THEN 1 END) / count(n), 2) as coverage_pct;

// Expected: coverage_pct > 80%
// Status: PASS if > 80%


// ============================================================================
// VALIDATION 10: Sample Node Structure
// ============================================================================
// REQUIREMENT: Verify nodes have complete v3.1 schema properties
// EXPECTED: All required properties present

// Sample ThreatActor
MATCH (n:ThreatActor)
RETURN n.name as name,
       n.super_label as super_label,
       n.tier1 as tier1,
       n.tier2 as tier2,
       n.tier as tier,
       n.actorType as actorType,
       n.fine_grained_type as fine_grained_type,
       n.hierarchy_path as hierarchy_path,
       labels(n) as all_labels
LIMIT 5;

// Expected: All properties populated
// Status: PASS if all properties non-null


// Sample Vulnerability (CVE)
MATCH (n:Vulnerability:CVE)
RETURN n.name as name,
       n.super_label as super_label,
       n.tier1 as tier1,
       n.tier2 as tier2,
       n.tier as tier,
       n.vulnType as vulnType,
       n.fine_grained_type as fine_grained_type,
       labels(n) as all_labels
LIMIT 5;

// Expected: All properties populated with vulnType = 'cve'
// Status: PASS if all properties non-null


// ============================================================================
// VALIDATION 11: Tier1 Category Distribution
// ============================================================================
// REQUIREMENT: Verify tier1 categories are correctly assigned
// EXPECTED: 6 categories (TECHNICAL, OPERATIONAL, ASSET, ORGANIZATIONAL, CONTEXTUAL)

MATCH (n)
WHERE n.tier1 IS NOT NULL
RETURN n.tier1 as tier1_category, count(n) as count
ORDER BY count DESC;

// Expected:
// TECHNICAL: ~500,000-700,000 (ThreatActor, Malware, Technique, Vulnerability, Indicator, Protocol)
// OPERATIONAL: ~200,000-400,000 (Campaign, Control, Event)
// ASSET: ~200,000-400,000 (Asset, Software)
// ORGANIZATIONAL: ~50,000-100,000 (Organization, Role)
// CONTEXTUAL: ~50,000-200,000 (Location, PsychTrait, EconomicMetric)
// Status: PASS if all 5 categories present


// ============================================================================
// VALIDATION SUMMARY QUERY
// ============================================================================
// Single query to check all critical validations

MATCH (n)
WITH count(n) as total_nodes
MATCH (s)
WHERE s:ThreatActor OR s:Malware OR s:Technique OR s:Vulnerability OR
      s:Indicator OR s:Campaign OR s:Asset OR s:Organization OR
      s:Location OR s:PsychTrait OR s:EconomicMetric OR s:Protocol OR
      s:Role OR s:Software OR s:Control OR s:Event
WITH total_nodes, count(s) as super_labeled_nodes
MATCH (t)
WHERE t.tier IS NOT NULL
WITH total_nodes, super_labeled_nodes, count(t) as nodes_with_tier
MATCH (d)
WHERE d.actorType IS NOT NULL OR d.malwareFamily IS NOT NULL OR
      d.patternType IS NOT NULL OR d.vulnType IS NOT NULL OR
      d.indicatorType IS NOT NULL OR d.campaignType IS NOT NULL OR
      d.assetClass IS NOT NULL
WITH total_nodes, super_labeled_nodes, nodes_with_tier, count(d) as nodes_with_discriminators
RETURN
  total_nodes,
  super_labeled_nodes,
  round(100.0 * super_labeled_nodes / total_nodes, 2) as super_label_coverage_pct,
  nodes_with_tier,
  round(100.0 * nodes_with_tier / super_labeled_nodes, 2) as tier_coverage_pct,
  nodes_with_discriminators,
  round(100.0 * nodes_with_discriminators / super_labeled_nodes, 2) as discriminator_coverage_pct,
  // Overall validation
  CASE
    WHEN super_labeled_nodes > total_nodes * 0.5
     AND nodes_with_tier > super_labeled_nodes * 0.9
     AND nodes_with_discriminators > super_labeled_nodes * 0.3
    THEN 'PASS ✅'
    ELSE 'FAIL ❌'
  END as overall_validation;

// Expected:
// super_label_coverage_pct > 50%
// tier_coverage_pct > 90%
// discriminator_coverage_pct > 30%
// overall_validation = 'PASS ✅'


// ============================================================================
// END OF VALIDATION QUERIES
// ============================================================================
