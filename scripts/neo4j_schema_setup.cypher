// ═══════════════════════════════════════════════════════════════
// Neo4j Schema Setup for CVE/CAPEC/CWE Data Loading
// Created: 2025-11-28
// Purpose: Create constraints and indexes for efficient data loading
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// CVE Constraints and Indexes
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT cve_id_unique IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cveId IS UNIQUE;

CREATE INDEX cve_namespace IF NOT EXISTS
FOR (c:CVE) ON (c.customer_namespace);

CREATE INDEX cve_severity IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3Severity);

CREATE INDEX cve_published IF NOT EXISTS
FOR (c:CVE) ON (c.publishedDate);

CREATE INDEX cve_has_exploit IF NOT EXISTS
FOR (c:CVE) ON (c.hasExploit);

// ───────────────────────────────────────────────────────────────
// CAPEC Constraints and Indexes
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT capec_id_unique IF NOT EXISTS
FOR (cap:CAPEC) REQUIRE cap.capecId IS UNIQUE;

CREATE INDEX capec_abstraction IF NOT EXISTS
FOR (cap:CAPEC) ON (cap.abstraction);

CREATE INDEX capec_severity IF NOT EXISTS
FOR (cap:CAPEC) ON (cap.severity);

CREATE INDEX capec_namespace IF NOT EXISTS
FOR (cap:CAPEC) ON (cap.customer_namespace);

// ───────────────────────────────────────────────────────────────
// CWE Constraints and Indexes
// ───────────────────────────────────────────────────────────────

CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS
FOR (cwe:CWE) REQUIRE cwe.cweId IS UNIQUE;

CREATE INDEX cwe_namespace IF NOT EXISTS
FOR (cwe:CWE) ON (cwe.customer_namespace);

CREATE INDEX cwe_abstraction IF NOT EXISTS
FOR (cwe:CWE) ON (cwe.abstraction);

// ───────────────────────────────────────────────────────────────
// Verification Query
// ───────────────────────────────────────────────────────────────

CALL db.constraints() YIELD name, type
RETURN name, type
ORDER BY name;

CALL db.indexes() YIELD name, type, state
RETURN name, type, state
ORDER BY name;
