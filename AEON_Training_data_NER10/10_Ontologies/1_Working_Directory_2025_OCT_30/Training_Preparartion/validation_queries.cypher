// 1. Total CVE→CWE relationships
MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN count(r) AS total_cve_cwe_relationships,
       count(DISTINCT cve) AS unique_cves_with_cwe,
       count(DISTINCT cwe) AS unique_cwes_referenced;

// 2. Complete attack chain count
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN count(path) AS complete_chains,
       count(DISTINCT cve) AS cves_with_chains,
       count(DISTINCT tech) AS techniques_reached;

// 3. KEV coverage
MATCH (cve:CVE) WHERE cve.is_kev = true
RETURN count(cve) AS kev_flagged_cves;

// 4. EPSS coverage
MATCH (c:CVE) WHERE c.epss_score IS NOT NULL
WITH count(c) AS with_epss
MATCH (all:CVE)
RETURN with_epss, count(all) AS total_cves,
       round(100.0 * with_epss / count(all), 2) AS epss_coverage_percent;

// 5. Database totals
MATCH (cve:CVE) WITH count(cve) AS total_cves
MATCH (cwe:CWE) WITH total_cves, count(cwe) AS total_cwes
MATCH (capec:CAPEC) WITH total_cves, total_cwes, count(capec) AS total_capecs
MATCH (tech:AttackTechnique)
RETURN total_cves, total_cwes, total_capecs, count(tech) AS total_techniques;

// 6. Priority distribution
MATCH (c:CVE) WHERE c.epss_score IS NOT NULL
RETURN c.priority AS priority, count(c) AS count
ORDER BY priority;

// 7. KEV with complete chains
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(tech:AttackTechnique)
WHERE cve.is_kev = true
RETURN count(DISTINCT cve) AS kev_with_complete_chains,
       count(path) AS total_kev_chains;

// 8. Top CWEs by CVE count
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN cwe.id AS cwe_id, cwe.name AS cwe_name, count(cve) AS cve_count
ORDER BY cve_count DESC
LIMIT 10;

// 9. Top ATT&CK techniques reached
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
      -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
      -[:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN tech.id AS technique_id, tech.name AS technique_name, 
       count(DISTINCT cve) AS reachable_cves
ORDER BY reachable_cves DESC
LIMIT 10;
