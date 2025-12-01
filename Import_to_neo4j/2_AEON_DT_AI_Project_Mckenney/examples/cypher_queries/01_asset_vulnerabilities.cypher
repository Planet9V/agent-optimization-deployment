// ============================================================================
// USE CASE 1: Find all vulnerabilities in a specific asset (Brake Controller)
// ============================================================================
// Purpose: Identify all CVEs affecting a particular hardware component through
//          its installed devices, firmware, and known vulnerabilities.
//
// Query Structure:
// 1. Start with specific HardwareComponent (Brake Controller)
// 2. Traverse to Device(s) where component is installed
// 3. Follow firmware running on device
// 4. Find all CVEs affecting that firmware
// 5. Return comprehensive vulnerability data with risk scores
//
// Expected Results: 50-200 vulnerabilities depending on ecosystem size
// Performance Target: < 2 seconds
// ============================================================================

MATCH (comp:HardwareComponent {name: 'Brake Controller'})
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:HAS_CVSS]->(cvss:CVSSScore)

OPTIONAL MATCH (cve)-[:CAUSED_BY]->(cwe:CWE)
OPTIONAL MATCH (cve)-[:HAS_EXPLOIT]->(exploit:Exploit)
OPTIONAL MATCH (exploit)-[:USED_BY_THREAT_ACTOR]->(ta:ThreatActor)

RETURN
  comp.name AS component_name,
  device.name AS device_name,
  device.type AS device_type,
  fw.name AS firmware_name,
  fw.version AS firmware_version,
  cve.cveId AS vulnerability_id,
  cve.description AS vulnerability_description,
  cvss.score AS cvss_score,
  cvss.severity AS severity_level,
  cwe.id AS weakness_id,
  cwe.name AS weakness_name,
  CASE
    WHEN exploit IS NOT NULL THEN 'Yes'
    ELSE 'No'
  END AS has_public_exploit,
  CASE
    WHEN ta IS NOT NULL THEN ta.name
    ELSE 'Unknown'
  END AS threat_actor_using_cve,
  cve.publishedDate AS publication_date

ORDER BY cvss.score DESC, cve.publishedDate DESC

// ============================================================================
// Alternative: Find vulnerabilities by asset class
// ============================================================================

MATCH (assetClass:AssetClass {name: 'Automotive'})
  <-[:BELONGS_TO_CLASS]-(comp:HardwareComponent)
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)

WITH comp.name AS component, COUNT(DISTINCT cve) AS vulnerability_count

RETURN component, vulnerability_count

ORDER BY vulnerability_count DESC

// ============================================================================
// Alternative: Find critical vulnerabilities only (CVSS >= 9.0)
// ============================================================================

MATCH (comp:HardwareComponent {name: 'Brake Controller'})
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:HAS_CVSS]->(cvss:CVSSScore)

WHERE cvss.score >= 9.0

RETURN
  comp.name,
  device.name,
  fw.version,
  cve.cveId,
  cvss.score,
  cvss.severity

ORDER BY cvss.score DESC

// ============================================================================
// Alternative: Find vulnerabilities with available patches
// ============================================================================

MATCH (comp:HardwareComponent {name: 'Brake Controller'})
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:HAS_PATCH]->(patch:Patch)

RETURN
  comp.name,
  fw.version,
  cve.cveId,
  patch.version AS patched_version,
  patch.releaseDate AS patch_release_date

ORDER BY patch.releaseDate DESC

// ============================================================================
// Alternative: Timeline - when vulnerabilities were discovered
// ============================================================================

MATCH (comp:HardwareComponent {name: 'Brake Controller'})
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)

WITH cve.publishedDate AS month, COUNT(cve) AS new_vulnerabilities

RETURN month, new_vulnerabilities

ORDER BY month ASC

// ============================================================================
// Notes on Performance Optimization:
// ============================================================================
// 1. Index on HardwareComponent.name for fast initial lookup
// 2. Index on CVE.cveId for cross-reference validation
// 3. Consider pagination for large result sets
// 4. Use LIMIT for exploratory queries during development
// 5. For 10K+ vulnerabilities, consider sampling or aggregation
//
// Sample results with LIMIT:
//   LIMIT 100
//
// For aggregated view (total impact):
//   WITH COUNT(DISTINCT cve) as total_vulns, AVG(cvss.score) as avg_risk
