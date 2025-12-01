// ============================================================================
// AEON DIGITAL TWIN CYBER SECURITY THREAT INTELLIGENCE
// Complete Schema Deployment Script
// Version: 1.0.0
// Created: 2025-10-29
//
// This script combines all schema components for complete deployment
// Execute in order: Constraints → Indexes → Node Definitions → Relationships → Sample Data
// ============================================================================

// ============================================================================
// STEP 1: CREATE CONSTRAINTS AND INDEXES
// ============================================================================

// UNIQUE CONSTRAINTS (15 Node Types)
CREATE CONSTRAINT org_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT site_id IF NOT EXISTS FOR (s:Site) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT train_id IF NOT EXISTS FOR (t:Train) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT component_id IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (sw:Software) REQUIRE sw.id IS UNIQUE;
CREATE CONSTRAINT library_id IF NOT EXISTS FOR (l:Library) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT net_interface_id IF NOT EXISTS FOR (ni:NetworkInterface) REQUIRE ni.id IS UNIQUE;
CREATE CONSTRAINT net_segment_id IF NOT EXISTS FOR (ns:NetworkSegment) REQUIRE ns.id IS UNIQUE;
CREATE CONSTRAINT firewall_rule_id IF NOT EXISTS FOR (fr:FirewallRule) REQUIRE fr.id IS UNIQUE;
CREATE CONSTRAINT protocol_id IF NOT EXISTS FOR (p:Protocol) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT threat_actor_id IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.id IS UNIQUE;
CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (c:Campaign) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT attack_technique_id IF NOT EXISTS FOR (at:AttackTechnique) REQUIRE at.id IS UNIQUE;
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;

// PROPERTY INDEXES FOR PERFORMANCE
CREATE INDEX org_name IF NOT EXISTS FOR (o:Organization) ON (o.name);
CREATE INDEX site_name IF NOT EXISTS FOR (s:Site) ON (s.name);
CREATE INDEX train_name IF NOT EXISTS FOR (t:Train) ON (t.name);
CREATE INDEX component_name IF NOT EXISTS FOR (c:Component) ON (c.name);
CREATE INDEX software_name IF NOT EXISTS FOR (sw:Software) ON (sw.name);
CREATE INDEX library_name IF NOT EXISTS FOR (l:Library) ON (l.name);
CREATE INDEX net_interface_ip IF NOT EXISTS FOR (ni:NetworkInterface) ON (ni.ipAddress);
CREATE INDEX net_segment_name IF NOT EXISTS FOR (ns:NetworkSegment) ON (ns.name);
CREATE INDEX firewall_rule_name IF NOT EXISTS FOR (fr:FirewallRule) ON (fr.name);
CREATE INDEX protocol_name IF NOT EXISTS FOR (p:Protocol) ON (p.name);
CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity);
CREATE INDEX threat_actor_name IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.name);
CREATE INDEX campaign_name IF NOT EXISTS FOR (c:Campaign) ON (c.name);
CREATE INDEX attack_technique_mitre IF NOT EXISTS FOR (at:AttackTechnique) ON (at.mitreId);
CREATE INDEX document_title IF NOT EXISTS FOR (d:Document) ON (d.title);

// FULL-TEXT SEARCH INDEXES
CREATE FULLTEXT INDEX cve_fulltext IF NOT EXISTS FOR (c:CVE) ON EACH [c.description, c.impact];
CREATE FULLTEXT INDEX threat_actor_fulltext IF NOT EXISTS FOR (ta:ThreatActor) ON EACH [ta.name, ta.description];
CREATE FULLTEXT INDEX campaign_fulltext IF NOT EXISTS FOR (c:Campaign) ON EACH [c.name, c.description];
CREATE FULLTEXT INDEX attack_technique_fulltext IF NOT EXISTS FOR (at:AttackTechnique) ON EACH [at.name, at.description];
CREATE FULLTEXT INDEX document_fulltext IF NOT EXISTS FOR (d:Document) ON EACH [d.title, d.content];

// ============================================================================
// STEP 2: NODE TYPE DEFINITIONS
// Schema defines 15 node types with complete properties
// See 02_node_definitions.cypher for detailed property specifications
// ============================================================================

// Organization, Site, Train, Component, Software, Library
// NetworkInterface, NetworkSegment, FirewallRule, Protocol
// CVE, ThreatActor, Campaign, AttackTechnique, Document

// ============================================================================
// STEP 3: RELATIONSHIP TYPE DEFINITIONS
// Schema defines 25 relationship types
// ============================================================================

// 1. OPERATES - Organization operates Sites
// 2. HOSTS - Site hosts Trains
// 3. HAS_COMPONENT - Train/Site has Components
// 4. RUNS_SOFTWARE - Component runs Software
// 5. DEPENDS_ON - Software depends on Library
// 6. HAS_VULNERABILITY - Software/Component/Library has CVE
// 7. HAS_INTERFACE - Component has NetworkInterface
// 8. BELONGS_TO - NetworkInterface belongs to NetworkSegment
// 9. CONNECTS_TO - NetworkSegment connects to NetworkSegment
// 10. PROTECTED_BY - NetworkSegment protected by FirewallRule
// 11. USES_PROTOCOL - Component/Software uses Protocol
// 12. EXPLOITS - ThreatActor exploits CVE
// 13. TARGETS - ThreatActor targets Organization
// 14. CONDUCTS - ThreatActor conducts Campaign
// 15. USES - ThreatActor/Campaign uses AttackTechnique
// 16. TARGETS_SECTOR - Campaign targets specific sectors
// 17. MENTIONS - Document mentions CVE/ThreatActor/Campaign
// 18. DESCRIBES - Document describes AttackTechnique/Mitigation
// 19. ATTACK_PATH_STEP - Attack path graph steps
// 20. MITIGATES - Control mitigates Vulnerability/Threat
// 21. MONITORS - Monitoring system monitors Component/Network
// 22. AUTHENTICATES - Authentication between systems
// 23. SUPPLIES - Manufacturer/Vendor supplies Component/Software
// 24. REQUIRES_UPDATE - Component/Software requires update/patch
// 25. COMMUNICATES_WITH - Component/System communicates with another

// ============================================================================
// DEPLOYMENT INSTRUCTIONS
// ============================================================================

// Option 1: Deploy Complete Schema with Sample Data
// Execute all files in sequence:
// 1. cypher-shell < 01_constraints_indexes.cypher
// 2. cypher-shell < 02_node_definitions.cypher (contains examples)
// 3. cypher-shell < 03_relationship_definitions.cypher (contains examples)
// 4. cypher-shell < 04_sample_data.cypher (full sample dataset)

// Option 2: Deploy Schema Only (No Sample Data)
// Execute only structure files:
// 1. cypher-shell < 01_constraints_indexes.cypher
// 2. Extract CREATE statements without data from 02_node_definitions.cypher
// 3. Define relationships without creating instances

// Option 3: Deploy via Neo4j Browser
// Copy and paste each script section into Neo4j Browser
// Execute in order: constraints → indexes → verify → data

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================

// Count all node types
// MATCH (n) RETURN labels(n)[0] AS NodeType, count(*) AS Count ORDER BY Count DESC;

// Count all relationship types
// MATCH ()-[r]->() RETURN type(r) AS RelType, count(*) AS Count ORDER BY Count DESC;

// Verify constraints
// SHOW CONSTRAINTS;

// Verify indexes
// SHOW INDEXES;

// Sample query: Find high-risk components with vulnerabilities
// MATCH (comp:Component)-[:HAS_VULNERABILITY]->(cve:CVE)
// WHERE comp.criticalityLevel = 'critical' AND cve.severity = 'critical'
// RETURN comp.name, comp.riskScore, cve.id, cve.cvssScore
// ORDER BY comp.riskScore DESC, cve.cvssScore DESC;

// Sample query: Trace attack paths to critical components
// MATCH path = (start:NetworkSegment)-[:ATTACK_PATH_STEP*]->(target:Component)
// WHERE start.securityZone = 'public' AND target.criticalityLevel = 'critical'
// RETURN path, length(path) AS PathLength
// ORDER BY PathLength
// LIMIT 10;

// Sample query: Identify threat actors targeting organization
// MATCH (ta:ThreatActor)-[t:TARGETS]->(org:Organization)
// WHERE org.id = 'ORG-001' AND t.isActive = true
// RETURN ta.name, ta.sophisticationLevel, ta.primaryMotivation, t.lastActivity
// ORDER BY ta.sophisticationLevel DESC;

// Sample query: Find unpatched critical vulnerabilities
// MATCH (sw:Software)-[hv:HAS_VULNERABILITY]->(cve:CVE)
// WHERE cve.severity = 'critical' AND hv.mitigationStatus <> 'patched'
// RETURN sw.name, sw.version, cve.id, cve.cvssScore, cve.description
// ORDER BY cve.cvssScore DESC;

// ============================================================================
// SCHEMA STATISTICS (After Sample Data Load)
// ============================================================================

// Expected Node Counts:
// - Organizations: 3
// - Sites: 10
// - Trains: 20
// - Components: 100
// - Software: 200
// - Libraries: 50
// - NetworkInterfaces: 150
// - NetworkSegments: 20
// - FirewallRules: 50
// - Protocols: 10
// - CVEs: 500
// - ThreatActors: 10
// - Campaigns: 5
// - AttackTechniques: 20
// - Documents: 10
// TOTAL NODES: ~1,148

// Expected Relationship Counts:
// - Various relationship types: ~2,000+ relationships

// ============================================================================
// PERFORMANCE TUNING RECOMMENDATIONS
// ============================================================================

// 1. Configure Neo4j memory settings
// dbms.memory.heap.initial_size=2G
// dbms.memory.heap.max_size=4G
// dbms.memory.pagecache.size=4G

// 2. Enable query logging for optimization
// dbms.logs.query.enabled=true
// dbms.logs.query.threshold=1s

// 3. Monitor index usage
// CALL db.stats.retrieve('QUERIES');

// 4. Periodic maintenance
// CALL apoc.periodic.iterate(
//   "MATCH (n) RETURN n",
//   "SET n.lastChecked = datetime()",
//   {batchSize:1000}
// );

// ============================================================================
// BACKUP AND RESTORE
// ============================================================================

// Create backup
// neo4j-admin dump --database=neo4j --to=/backups/aeon-dt-$(date +%Y%m%d).dump

// Restore backup
// neo4j-admin load --from=/backups/aeon-dt-20251029.dump --database=neo4j --force

// ============================================================================
// END OF COMPLETE SCHEMA DEPLOYMENT SCRIPT
// ============================================================================
