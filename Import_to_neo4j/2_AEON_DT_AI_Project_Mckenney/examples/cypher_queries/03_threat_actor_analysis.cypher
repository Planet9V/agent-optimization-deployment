// ============================================================================
// USE CASE 4: Correlate threat actors to vulnerabilities in target sector
// ============================================================================
// Purpose: Identify which threat actors are actively exploiting vulnerabilities
//          that affect critical systems in specific industry sectors.
//
// Query Structure:
// 1. Match ThreatActor nodes
// 2. Follow exploits to CVEs they use
// 3. Traverse to affected products
// 4. Filter by target sector (e.g., Energy, Transportation)
// 5. Rank actors by exploitation activity and capability
//
// Expected Results: 5-50 threat actors per sector
// Performance Target: < 2 seconds
// ============================================================================

MATCH (ta:ThreatActor)
  -[:EXPLOITS]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)
  -[:USED_IN_SECTOR]->(sector:Sector {name: 'Energy'})

OPTIONAL MATCH (ta)-[:HAS_CAPABILITY]->(capability:Capability)
OPTIONAL MATCH (cve)-[:HAS_CVSS]->(cvss:CVSSScore)
OPTIONAL MATCH (ta)-[:OBSERVED_IN_CAMPAIGN]->(campaign:Campaign)

WITH
  ta.name AS actor_name,
  COUNT(DISTINCT cve) AS cve_count,
  AVG(cvss.score) AS avg_target_severity,
  MAX(cvss.score) AS max_target_severity,
  sector.name AS sector,
  COLLECT(DISTINCT capability.name) AS capabilities,
  COUNT(DISTINCT campaign) AS active_campaigns

RETURN
  actor_name,
  cve_count AS vulnerabilities_exploited,
  ROUND(avg_target_severity, 2) AS average_severity,
  ROUND(max_target_severity, 2) AS maximum_severity,
  sector,
  capabilities,
  active_campaigns,
  CASE
    WHEN cve_count >= 100 THEN 'ADVANCED'
    WHEN cve_count >= 50 THEN 'SOPHISTICATED'
    WHEN cve_count >= 20 THEN 'MODERATE'
    ELSE 'BASIC'
  END AS estimated_capability_level

ORDER BY cve_count DESC

// ============================================================================
// Alternative: Threat actor timeline (activity over time)
// ============================================================================

MATCH (ta:ThreatActor {name: 'APT28'})
  -[:EXPLOITS]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)
  -[:USED_IN_SECTOR]->(sector:Sector)

WITH
  ta.name AS actor,
  DATE_TRUNC('month', cve.publishedDate) AS month,
  COUNT(DISTINCT cve) AS new_exploits,
  sector.name AS sector

RETURN
  actor,
  month,
  new_exploits,
  sector

ORDER BY month ASC

// ============================================================================
// Alternative: Threat actor TTPs (Tactics, Techniques, Procedures)
// ============================================================================

MATCH (ta:ThreatActor)
  -[:USES_TECHNIQUE]->(technique:ATTACKTechnique)
  -[:USED_TO_EXPLOIT]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)
  -[:USED_IN_SECTOR]->(sector:Sector {name: 'Transportation'})

WITH
  ta.name AS actor_name,
  technique.id AS technique_id,
  technique.name AS technique_name,
  COUNT(DISTINCT cve) AS technique_effectiveness

RETURN
  actor_name,
  technique_id,
  technique_name,
  technique_effectiveness

ORDER BY technique_effectiveness DESC

// ============================================================================
// Alternative: Target products by threat actor
// ============================================================================

MATCH (ta:ThreatActor {name: 'APT28'})
  -[:EXPLOITS]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)

WITH ta, product, COUNT(DISTINCT cve) AS cve_count

RETURN
  ta.name AS threat_actor,
  product.name AS targeted_product,
  product.vendor AS vendor,
  cve_count AS known_exploits,
  CASE
    WHEN cve_count >= 50 THEN 'PRIMARY_TARGET'
    WHEN cve_count >= 20 THEN 'SECONDARY_TARGET'
    ELSE 'OPPORTUNISTIC'
  END AS targeting_priority

ORDER BY cve_count DESC

// ============================================================================
// Alternative: Compare multiple threat actors in sector
// ============================================================================

MATCH (ta:ThreatActor)
  -[:EXPLOITS]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)
  -[:USED_IN_SECTOR]->(sector:Sector {name: 'Energy'})

WITH
  ta.name AS actor,
  COUNT(DISTINCT cve) AS exploit_count,
  COUNT(DISTINCT product) AS product_count

RETURN
  actor,
  exploit_count,
  product_count,
  exploit_count * 10 + product_count * 5 AS threat_score  // Simple scoring

ORDER BY threat_score DESC

// ============================================================================
// Alternative: Attribution (which attacks are likely by which actors)
// ============================================================================

MATCH (campaign:Campaign)
  -[:ATTRIBUTED_TO]->(ta:ThreatActor)
  -[:EXPLOITS]->(cve:CVE)
  -[:AFFECTS]->(product:SoftwareProduct)
  -[:USED_IN_SECTOR]->(sector:Sector {name: 'Energy'})

WITH
  campaign.name AS operation_name,
  ta.name AS attributed_actor,
  COUNT(DISTINCT cve) AS cvEs_used,
  MAX(campaign.confidence_score) AS attribution_confidence

RETURN
  operation_name,
  attributed_actor,
  cvEs_used,
  attribution_confidence,
  CASE
    WHEN attribution_confidence >= 0.9 THEN 'CONFIRMED'
    WHEN attribution_confidence >= 0.7 THEN 'HIGH_CONFIDENCE'
    WHEN attribution_confidence >= 0.5 THEN 'MODERATE_CONFIDENCE'
    ELSE 'LOW_CONFIDENCE'
  END AS confidence_level

ORDER BY attribution_confidence DESC

// ============================================================================
// Notes on Performance Optimization:
// ============================================================================
// 1. Create index on ThreatActor.name for initial lookup
// 2. Cache sector membership data for frequent sector filtering
// 3. Pre-compute threat actor capability scores for sorting
// 4. Use DISTINCT to eliminate duplicate relationships
// 5. Consider materialized views for common sector queries
//
// For large datasets:
// 1. Partition threat actor data by region/sector
// 2. Cache TTP mappings (TTPs don't change frequently)
// 3. Use separate queries for trend analysis
// 4. Aggregate CVE counts at ingestion time where possible
//
// Query variants for different use cases:
// - Recent threats: Filter by campaign.date >= date.today() - 30 days
// - Emerging trends: Filter by CVE.publishedDate
// - Attribution analysis: Use campaign.confidence_score threshold
// - Capability assessment: Aggregate exploit complexity and recency
