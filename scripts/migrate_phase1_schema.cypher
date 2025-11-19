// ═══════════════════════════════════════════════════════════════
// Phase 1 Schema Migration - Enhance Existing Neo4j Database
// NON-DESTRUCTIVE: Preserves all existing data
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// STEP 1: Backup Reminder
// ───────────────────────────────────────────────────────────────
// CRITICAL: Create backup before running this migration!
// Command: neo4j-admin database backup neo4j --to-path=/home/jim/neo4j_backup_2025-10-29

// ───────────────────────────────────────────────────────────────
// STEP 2: Add New Constraints (IF NOT EXISTS = safe)
// ───────────────────────────────────────────────────────────────

// CVE constraints
CREATE CONSTRAINT cve_cveid IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cveId IS UNIQUE;

// Map existing CVE.id to CVE.cveId for backward compatibility
MATCH (cve:CVE)
WHERE cve.cveId IS NULL AND cve.id IS NOT NULL
SET cve.cveId = cve.id;

// CWE constraints
CREATE CONSTRAINT cwe_cweid IF NOT EXISTS
FOR (c:CWE) REQUIRE c.cweId IS UNIQUE;

// CAPEC constraints (new)
CREATE CONSTRAINT capec_id IF NOT EXISTS
FOR (c:CAPEC) REQUIRE c.capecId IS UNIQUE;

// Technique (ATT&CK) constraints (new)
CREATE CONSTRAINT technique_id IF NOT EXISTS
FOR (t:Technique) REQUIRE t.techniqueId IS UNIQUE;

// ThreatActor constraints
CREATE CONSTRAINT threat_actor_id IF NOT EXISTS
FOR (ta:ThreatActor) REQUIRE ta.id IS UNIQUE;

// Malware constraints
CREATE CONSTRAINT malware_id IF NOT EXISTS
FOR (m:Malware) REQUIRE m.id IS UNIQUE;

// Document constraints (existing, add if missing)
CREATE CONSTRAINT document_hash IF NOT EXISTS
FOR (d:Document) REQUIRE d.file_hash IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// STEP 3: Add Customer Namespace to Existing Data
// ───────────────────────────────────────────────────────────────

// Map existing CVEs to shared namespace
MATCH (cve:CVE)
WHERE cve.customer_namespace IS NULL
SET cve.customer_namespace =
  CASE
    WHEN cve.namespace = 'CybersecurityKB' THEN 'shared:nvd'
    WHEN cve.namespace IS NOT NULL THEN 'shared:' + toLower(cve.namespace)
    ELSE 'shared:nvd'
  END,
  cve.is_shared = true;

// Map existing CWEs to shared namespace
MATCH (cwe:CWE)
WHERE cwe.customer_namespace IS NULL
SET cwe.customer_namespace = 'shared:cwe',
    cwe.is_shared = true;

// Map existing ThreatActors to shared namespace
MATCH (ta:ThreatActor)
WHERE ta.customer_namespace IS NULL
SET ta.customer_namespace = 'shared:threat-intel',
    ta.is_shared = true;

// Map existing Malware to shared namespace
MATCH (m:Malware)
WHERE m.customer_namespace IS NULL
SET m.customer_namespace = 'shared:malware',
    m.is_shared = true;

// ───────────────────────────────────────────────────────────────
// STEP 4: Add New Performance Indexes
// ───────────────────────────────────────────────────────────────

// Customer namespace isolation indexes
CREATE INDEX cve_namespace IF NOT EXISTS
FOR (c:CVE) ON (c.customer_namespace);

CREATE INDEX cwe_namespace IF NOT EXISTS
FOR (c:CWE) ON (c.customer_namespace);

CREATE INDEX threat_actor_namespace IF NOT EXISTS
FOR (ta:ThreatActor) ON (ta.customer_namespace);

// CVSS scoring indexes
CREATE INDEX cve_cvss_score IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3BaseScore);

CREATE INDEX cve_severity IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3Severity);

CREATE INDEX cve_published_date IF NOT EXISTS
FOR (c:CVE) ON (c.publishedDate);

// ATT&CK framework indexes
CREATE INDEX technique_tactic IF NOT EXISTS
FOR (t:Technique) ON (t.tactic);

CREATE INDEX technique_platform IF NOT EXISTS
FOR (t:Technique) ON (t.platform);

// Full-text search indexes
CREATE FULLTEXT INDEX cve_description_search IF NOT EXISTS
FOR (c:CVE) ON EACH [c.description];

CREATE FULLTEXT INDEX technique_search IF NOT EXISTS
FOR (t:Technique) ON EACH [t.name, t.description];

// ───────────────────────────────────────────────────────────────
// STEP 5: Add Missing Properties to Existing CVEs
// ───────────────────────────────────────────────────────────────

// Add default values for new properties if missing
MATCH (cve:CVE)
WHERE cve.hasExploit IS NULL
SET cve.hasExploit = false,
    cve.exploitMaturity = 'NOT_DEFINED';

// ───────────────────────────────────────────────────────────────
// STEP 6: Validation Queries
// ───────────────────────────────────────────────────────────────

// Count nodes before and after (run before migration, then after)
CALL db.labels() YIELD label
CALL {
  WITH label
  MATCH (n) WHERE label IN labels(n)
  RETURN count(n) AS count
}
RETURN label, count
ORDER BY count DESC;

// Verify constraints deployed
SHOW CONSTRAINTS;

// Verify indexes deployed
SHOW INDEXES;

// Check customer namespace coverage
MATCH (n)
WHERE n.customer_namespace IS NOT NULL
RETURN labels(n) AS node_type,
       n.customer_namespace AS namespace,
       count(n) AS node_count
ORDER BY node_count DESC;

// Check for duplicate CVEs
MATCH (cve:CVE)
WITH cve.cveId AS cve_id, count(*) AS dup_count
WHERE dup_count > 1
RETURN cve_id, dup_count;
// Expected: 0 rows (no duplicates)

// ═══════════════════════════════════════════════════════════════
// MIGRATION COMPLETE
// ═══════════════════════════════════════════════════════════════
// Expected outcomes:
// - All existing data preserved
// - New constraints added safely
// - Customer namespace isolation enabled
// - Performance indexes created
// - Zero data loss
// - Ready for CAPEC and ATT&CK import
// ═══════════════════════════════════════════════════════════════
