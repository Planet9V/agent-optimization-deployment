// ═══════════════════════════════════════════════════════════════
// Neo4j Schema Foundation - Constraints and Indexes
// Phase 1: Core Schema Foundation
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// LAYER 1: Physical Asset Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT device_id IF NOT EXISTS
FOR (d:Device) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT component_id IF NOT EXISTS
FOR (c:HardwareComponent) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT location_id IF NOT EXISTS
FOR (l:Location) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT physical_asset_id IF NOT EXISTS
FOR (p:PhysicalAsset) REQUIRE p.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 2: Network & Communication Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT network_interface_id IF NOT EXISTS
FOR (n:NetworkInterface) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT network_id IF NOT EXISTS
FOR (n:Network) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT security_zone_id IF NOT EXISTS
FOR (s:SecurityZone) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT conduit_id IF NOT EXISTS
FOR (c:Conduit) REQUIRE c.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 3: Software & Application Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT software_id IF NOT EXISTS
FOR (s:Software) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT software_component_id IF NOT EXISTS
FOR (sc:SoftwareComponent) REQUIRE sc.id IS UNIQUE;

CREATE CONSTRAINT application_id IF NOT EXISTS
FOR (a:Application) REQUIRE a.id IS UNIQUE;

CREATE CONSTRAINT firmware_id IF NOT EXISTS
FOR (f:Firmware) REQUIRE f.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 4: Vulnerability & Threat Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT cve_id IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cveId IS UNIQUE;

CREATE CONSTRAINT cwe_id IF NOT EXISTS
FOR (c:CWE) REQUIRE c.cweId IS UNIQUE;

CREATE CONSTRAINT capec_id IF NOT EXISTS
FOR (c:CAPEC) REQUIRE c.capecId IS UNIQUE;

CREATE CONSTRAINT technique_id IF NOT EXISTS
FOR (t:Technique) REQUIRE t.techniqueId IS UNIQUE;

CREATE CONSTRAINT threat_actor_id IF NOT EXISTS
FOR (ta:ThreatActor) REQUIRE ta.id IS UNIQUE;

CREATE CONSTRAINT exploit_id IF NOT EXISTS
FOR (e:Exploit) REQUIRE e.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 5: Attack Surface & Exposure Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT attack_surface_id IF NOT EXISTS
FOR (as:AttackSurface) REQUIRE as.id IS UNIQUE;

CREATE CONSTRAINT attack_path_id IF NOT EXISTS
FOR (ap:AttackPath) REQUIRE ap.id IS UNIQUE;

CREATE CONSTRAINT attack_path_step_id IF NOT EXISTS
FOR (aps:AttackPathStep) REQUIRE aps.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 6: Organizational & Business Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT organization_id IF NOT EXISTS
FOR (o:Organization) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT business_process_id IF NOT EXISTS
FOR (bp:BusinessProcess) REQUIRE bp.id IS UNIQUE;

CREATE CONSTRAINT compliance_id IF NOT EXISTS
FOR (c:Compliance) REQUIRE c.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 7: Failure Propagation & Impact Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT failure_mode_id IF NOT EXISTS
FOR (fm:FailureMode) REQUIRE fm.id IS UNIQUE;

CREATE CONSTRAINT failure_scenario_id IF NOT EXISTS
FOR (fs:FailureScenario) REQUIRE fs.id IS UNIQUE;

CREATE CONSTRAINT impact_id IF NOT EXISTS
FOR (i:Impact) REQUIRE i.id IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// LAYER 8: Mitigation & Remediation Layer - Constraints
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT mitigation_id IF NOT EXISTS
FOR (m:Mitigation) REQUIRE m.id IS UNIQUE;

CREATE CONSTRAINT priority_id IF NOT EXISTS
FOR (p:Priority) REQUIRE p.id IS UNIQUE;

// ═══════════════════════════════════════════════════════════════
// PERFORMANCE INDEXES - Critical for Multi-Hop Queries
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// Customer Namespace Isolation (Critical for Multi-Tenancy)
// ───────────────────────────────────────────────────────────────

CREATE INDEX device_namespace IF NOT EXISTS
FOR (d:Device) ON (d.customer_namespace);

CREATE INDEX software_namespace IF NOT EXISTS
FOR (s:Software) ON (s.customer_namespace);

CREATE INDEX organization_namespace IF NOT EXISTS
FOR (o:Organization) ON (o.customer_namespace);

// ───────────────────────────────────────────────────────────────
// Asset Identification (CPE/PURL for SBOM)
// ───────────────────────────────────────────────────────────────

CREATE INDEX device_cpe IF NOT EXISTS
FOR (d:Device) ON (d.cpe);

CREATE INDEX software_cpe IF NOT EXISTS
FOR (s:Software) ON (d.cpe);

CREATE INDEX software_purl IF NOT EXISTS
FOR (s:Software) ON (s.packageUrl);

CREATE INDEX firmware_version IF NOT EXISTS
FOR (f:Firmware) ON (f.version);

// ───────────────────────────────────────────────────────────────
// Vulnerability Severity (CVSS Scoring)
// ───────────────────────────────────────────────────────────────

CREATE INDEX cve_cvss_score IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3BaseScore);

CREATE INDEX cve_published_date IF NOT EXISTS
FOR (c:CVE) ON (c.publishedDate);

CREATE INDEX cve_exploitability IF NOT EXISTS
FOR (c:CVE) ON (c.exploitabilityScore);

// ───────────────────────────────────────────────────────────────
// ATT&CK Framework Navigation
// ───────────────────────────────────────────────────────────────

CREATE INDEX technique_tactic IF NOT EXISTS
FOR (t:Technique) ON (t.tactic);

CREATE INDEX technique_platform IF NOT EXISTS
FOR (t:Technique) ON (t.platform);

// ───────────────────────────────────────────────────────────────
// IEC 62443 Security Zones
// ───────────────────────────────────────────────────────────────

CREATE INDEX security_zone_level IF NOT EXISTS
FOR (sz:SecurityZone) ON (sz.securityLevel);

// ───────────────────────────────────────────────────────────────
// Now/Next/Never Prioritization
// ───────────────────────────────────────────────────────────────

CREATE INDEX priority_type IF NOT EXISTS
FOR (p:Priority) ON (p.type);

CREATE INDEX priority_score IF NOT EXISTS
FOR (p:Priority) ON (p.score);

// ───────────────────────────────────────────────────────────────
// Composite Indexes for Complex Queries
// ───────────────────────────────────────────────────────────────

CREATE INDEX device_criticality_namespace IF NOT EXISTS
FOR (d:Device) ON (d.criticalityLevel, d.customer_namespace);

CREATE INDEX cve_severity_exploitable IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3BaseScore, c.hasExploit);

// ═══════════════════════════════════════════════════════════════
// FULL-TEXT SEARCH INDEXES
// ═══════════════════════════════════════════════════════════════

CREATE FULLTEXT INDEX cve_description_search IF NOT EXISTS
FOR (c:CVE) ON EACH [c.description, c.summary];

CREATE FULLTEXT INDEX software_search IF NOT EXISTS
FOR (s:Software) ON EACH [s.name, s.vendor, s.product];

CREATE FULLTEXT INDEX technique_search IF NOT EXISTS
FOR (t:Technique) ON EACH [t.name, t.description];

// ═══════════════════════════════════════════════════════════════
// VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════

// Show all constraints
SHOW CONSTRAINTS;

// Show all indexes
SHOW INDEXES;

// Verify constraint coverage
CALL db.schema.visualization();
