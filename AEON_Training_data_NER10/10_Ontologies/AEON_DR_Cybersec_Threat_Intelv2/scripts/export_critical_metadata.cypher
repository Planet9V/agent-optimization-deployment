// Export Critical Metadata Before CVE Deletion
// Created: 2025-11-01
// Purpose: Preserve THREATENS_GRID_STABILITY and other critical relationship metadata

// Export 1: THREATENS_GRID_STABILITY relationships (3,000+ critical infrastructure relationships)
// These contain irreplaceable metadata about power grid impacts
MATCH (n)-[r:THREATENS_GRID_STABILITY]->(cve:CVE)
RETURN
    id(n) as source_node_id,
    labels(n) as source_labels,
    n.id as source_id,
    cve.id as cve_id,
    type(r) as relationship_type,
    r.population_impact as population_impact,
    r.grid_severity as grid_severity,
    r.cascade_risk as cascade_risk,
    r.recovery_time_hours as recovery_time_hours,
    properties(r) as all_properties
ORDER BY cve.id;

// Export 2: All CVE relationships with cve_id properties (for reconstruction)
// This captures all relationship metadata that references CVE IDs
MATCH (cve:CVE)-[r]-(n)
WHERE EXISTS(r.cve_id)
RETURN
    cve.id as cve_id,
    type(r) as relationship_type,
    labels(n) as connected_node_labels,
    n.id as connected_node_id,
    r.cve_id as relationship_cve_id,
    properties(r) as all_properties
ORDER BY cve.id, type(r);

// Export 3: All VULNERABLE_TO relationships (24,000+ relationships)
MATCH (n)-[r:VULNERABLE_TO]->(cve:CVE)
RETURN
    labels(n) as source_labels,
    n.id as source_id,
    cve.id as cve_id,
    r.cve_id as relationship_cve_id,
    r.severity as severity,
    r.exploitability as exploitability,
    properties(r) as all_properties
ORDER BY cve.id;

// Export 4: CVE node properties (for validation after re-import)
MATCH (cve:CVE)
WHERE cve.id IS NOT NULL
RETURN
    cve.id as cve_id,
    cve.description as description,
    cve.published_date as published_date,
    cve.modified_date as modified_date,
    cve.cvss_score as cvss_score,
    cve.cvss_vector as cvss_vector,
    cve.epss_score as epss_score,
    cve.epss_percentile as epss_percentile,
    properties(cve) as all_properties
ORDER BY cve.id;

// Summary: Relationship counts before deletion (for validation)
MATCH (cve:CVE)
WITH count(cve) as total_cves
MATCH (cve:CVE)-[r]-()
RETURN
    total_cves,
    count(r) as total_relationships,
    count(DISTINCT type(r)) as relationship_types
;
