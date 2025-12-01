// ═══════════════════════════════════════════════════════════════
// LAYER 8: Mitigation & Remediation Layer
// Now/Next/Never Prioritization, Mitigation Strategies
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Mitigation (Remediation action)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   mitigation_type: enum [PATCH, CONFIGURATION_CHANGE, COMPENSATING_CONTROL, ISOLATION, DECOMMISSION]
//   description: string
//   implementation_effort: enum [LOW, MEDIUM, HIGH, VERY_HIGH]
//   effectiveness: enum [LOW, MEDIUM, HIGH, COMPLETE]
//   deployment_method: enum [AUTOMATED, MANUAL, HYBRID]
//   requires_downtime: boolean
//   estimated_hours: float
//   cost_estimate: float
// ───────────────────────────────────────────────────────────────

CREATE (log4j_patch:Mitigation {
  id: 'mitigation-log4j-patch-001',
  name: 'Update Log4j to 2.17.1',
  mitigation_type: 'PATCH',
  description: 'Update all Apache Log4j dependencies to version 2.17.1 or later to remediate Log4Shell vulnerability',
  implementation_effort: 'MEDIUM',
  effectiveness: 'COMPLETE',
  deployment_method: 'AUTOMATED',
  requires_downtime: true,
  estimated_hours: 8.0,
  cost_estimate: 5000.00
});

CREATE (firewall_rule:Mitigation {
  id: 'mitigation-firewall-isolation-001',
  name: 'Block JNDI Outbound Connections',
  mitigation_type: 'COMPENSATING_CONTROL',
  description: 'Implement firewall rules to block outbound LDAP/RMI connections from application servers',
  implementation_effort: 'LOW',
  effectiveness: 'MEDIUM',
  deployment_method: 'MANUAL',
  requires_downtime: false,
  estimated_hours: 2.0,
  cost_estimate: 500.00
});

CREATE (firmware_upgrade:Mitigation {
  id: 'mitigation-plc-firmware-upgrade',
  name: 'Upgrade PLC Firmware to v2.9.4',
  mitigation_type: 'PATCH',
  description: 'Upgrade Siemens S7-1500 firmware to version 2.9.4 to address critical vulnerabilities',
  implementation_effort: 'HIGH',
  effectiveness: 'COMPLETE',
  deployment_method: 'MANUAL',
  requires_downtime: true,
  estimated_hours: 16.0,
  cost_estimate: 12000.00
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Priority (Now/Next/Never prioritization)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   type: enum [NOW, NEXT, NEVER]
//   score: float (0.0-100.0, calculated risk-based priority)
//   rationale: string
//   deadline: date
//   assigned_to: string
//   status: enum [PLANNED, IN_PROGRESS, COMPLETED, DEFERRED, CANCELLED]
//
// Priority Score Calculation:
//   - NOW: score >= 80 (CRITICAL severity + exploit available + internet-facing)
//   - NEXT: 50 <= score < 80 (HIGH severity OR exploit available OR business-critical)
//   - NEVER: score < 50 (LOW/MEDIUM severity + no exploit + compensating controls)
// ───────────────────────────────────────────────────────────────

CREATE (now_priority:Priority {
  id: 'priority-log4j-now',
  type: 'NOW',
  score: 95.0,
  rationale: 'CRITICAL CVSS 10.0 vulnerability with active exploitation in the wild. Affects internet-facing application server.',
  deadline: date('2025-11-05'),
  assigned_to: 'Security Team',
  status: 'IN_PROGRESS'
});

CREATE (next_priority:Priority {
  id: 'priority-plc-firmware-next',
  type: 'NEXT',
  score: 65.0,
  rationale: 'HIGH severity vulnerability in critical OT device, but isolated in secure network zone with compensating controls.',
  deadline: date('2025-12-15'),
  assigned_to: 'OT Engineering Team',
  status: 'PLANNED'
});

CREATE (never_priority:Priority {
  id: 'priority-legacy-system-never',
  type: 'NEVER',
  score: 35.0,
  rationale: 'MEDIUM severity vulnerability in legacy system scheduled for decommissioning in 6 months. Air-gapped from production network.',
  deadline: null,
  assigned_to: null,
  status: 'DEFERRED'
});

// ═══════════════════════════════════════════════════════════════
// RELATIONSHIP PATTERNS - Layer 8
// ═══════════════════════════════════════════════════════════════

// CVE → Mitigation (remediation options)
MATCH (cve:CVE {cveId: 'CVE-2021-44228'})
CREATE (cve)-[:MITIGATED_BY {
  effectiveness_rating: 0.95,
  recommended: true
}]->(log4j_patch);

CREATE (cve)-[:MITIGATED_BY {
  effectiveness_rating: 0.60,
  recommended: false
}]->(firewall_rule);

// Mitigation → Priority (prioritization)
CREATE (log4j_patch)-[:HAS_PRIORITY]->(now_priority);
CREATE (firmware_upgrade)-[:HAS_PRIORITY]->(next_priority);

// Priority dependencies (must complete X before Y)
CREATE (now_priority)-[:BLOCKS]->(next_priority);

// ═══════════════════════════════════════════════════════════════
// QUERY EXAMPLES - Prioritization & Remediation Planning
// ═══════════════════════════════════════════════════════════════

// Example 1: Now/Next/Never Dashboard
MATCH (p:Priority)
OPTIONAL MATCH (p)<-[:HAS_PRIORITY]-(m:Mitigation)
OPTIONAL MATCH (m)<-[:MITIGATED_BY]-(cve:CVE)
RETURN p.type AS priority_level,
       count(DISTINCT m) AS mitigation_count,
       count(DISTINCT cve) AS cve_count,
       sum(m.estimated_hours) AS total_effort_hours,
       sum(m.cost_estimate) AS total_cost,
       collect(DISTINCT p.status) AS statuses
ORDER BY
  CASE p.type
    WHEN 'NOW' THEN 1
    WHEN 'NEXT' THEN 2
    WHEN 'NEVER' THEN 3
  END;

// Example 2: Critical Path Analysis (dependencies)
MATCH path = (p1:Priority {type: 'NOW'})-[:BLOCKS*1..3]->(p2:Priority)
OPTIONAL MATCH (p1)<-[:HAS_PRIORITY]-(m1:Mitigation)
OPTIONAL MATCH (p2)<-[:HAS_PRIORITY]-(m2:Mitigation)
RETURN p1.type AS blocking_priority,
       m1.name AS blocking_mitigation,
       p1.deadline AS must_complete_by,
       length(path) AS dependency_depth,
       p2.type AS blocked_priority,
       m2.name AS blocked_mitigation;

// Example 3: Customer-Specific Remediation Plan
MATCH (device:Device {customer_namespace: 'customer:EnterpriseCorp'})
  -[:RUNS_SOFTWARE]->(software:Software)
  -[:HAS_COMPONENT]->(comp:SoftwareComponent)
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:MITIGATED_BY]->(mitigation:Mitigation)
  -[:HAS_PRIORITY]->(priority:Priority)
WHERE cve.cvssV3Severity IN ['HIGH', 'CRITICAL']
  AND priority.type IN ['NOW', 'NEXT']
RETURN device.name AS affected_device,
       software.name AS vulnerable_software,
       cve.cveId AS vulnerability,
       cve.cvssV3BaseScore AS severity,
       mitigation.name AS remediation_action,
       mitigation.implementation_effort AS effort,
       mitigation.estimated_hours AS hours,
       priority.type AS priority,
       priority.deadline AS deadline,
       priority.status AS status
ORDER BY
  CASE priority.type WHEN 'NOW' THEN 1 WHEN 'NEXT' THEN 2 END,
  cve.cvssV3BaseScore DESC;

// Example 4: Resource Allocation Planning
MATCH (m:Mitigation)-[:HAS_PRIORITY]->(p:Priority {type: 'NOW'})
WHERE p.status IN ['PLANNED', 'IN_PROGRESS']
RETURN p.assigned_to AS team,
       count(m) AS mitigation_count,
       sum(m.estimated_hours) AS total_hours,
       sum(m.cost_estimate) AS total_budget,
       min(p.deadline) AS earliest_deadline,
       collect(m.name)[0..3] AS sample_mitigations
ORDER BY total_hours DESC;

// ═══════════════════════════════════════════════════════════════
// PRIORITIZATION ALGORITHM (Risk-Based Scoring)
// ═══════════════════════════════════════════════════════════════

// Calculate priority scores for all CVEs
MATCH (cve:CVE)
OPTIONAL MATCH (cve)<-[:HAS_VULNERABILITY]-(software:Software)<-[:RUNS_SOFTWARE]-(device:Device)
OPTIONAL MATCH (device)-[:HAS_INTERFACE]->(:NetworkInterface)-[:CONNECTED_TO]->(:Network)-[:PART_OF]->(zone:SecurityZone)

WITH cve, device, zone,
  // Base score from CVSS
  cve.cvssV3BaseScore AS cvss_score,
  // Exploit availability bonus
  CASE WHEN cve.hasExploit THEN 20 ELSE 0 END AS exploit_bonus,
  // Internet-facing bonus
  CASE WHEN zone.zone_type IN ['ENTERPRISE', 'DMZ'] THEN 15 ELSE 0 END AS exposure_bonus,
  // Device criticality bonus
  CASE device.criticalityLevel
    WHEN 'CRITICAL' THEN 15
    WHEN 'HIGH' THEN 10
    WHEN 'MEDIUM' THEN 5
    ELSE 0
  END AS criticality_bonus

WITH cve,
  (cvss_score * 6) + exploit_bonus + exposure_bonus + criticality_bonus AS priority_score

// Assign Now/Next/Never based on score
MERGE (p:Priority {id: 'priority-' + cve.cveId})
SET p.type = CASE
    WHEN priority_score >= 80 THEN 'NOW'
    WHEN priority_score >= 50 THEN 'NEXT'
    ELSE 'NEVER'
  END,
  p.score = priority_score,
  p.status = 'PLANNED'

WITH cve, p
MERGE (cve)-[:HAS_PRIORITY_SCORE]->(p)
RETURN p.type AS priority,
       count(cve) AS cve_count,
       avg(p.score) AS avg_score,
       min(p.score) AS min_score,
       max(p.score) AS max_score
ORDER BY
  CASE p.type WHEN 'NOW' THEN 1 WHEN 'NEXT' THEN 2 WHEN 'NEVER' THEN 3 END;

// ═══════════════════════════════════════════════════════════════
// VALIDATION METRICS
// ═══════════════════════════════════════════════════════════════

// Mitigation effectiveness distribution
MATCH (m:Mitigation)
RETURN m.effectiveness AS effectiveness_level,
       count(m) AS mitigation_count,
       avg(m.estimated_hours) AS avg_effort_hours,
       avg(m.cost_estimate) AS avg_cost
ORDER BY effectiveness_level DESC;

// Priority status tracking
MATCH (p:Priority)
RETURN p.type AS priority,
       p.status AS status,
       count(*) AS count
ORDER BY priority, status;
