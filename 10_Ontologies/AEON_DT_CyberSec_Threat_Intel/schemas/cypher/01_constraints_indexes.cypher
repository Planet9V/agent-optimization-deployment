// ============================================================================
// AEON DIGITAL TWIN CYBER SECURITY THREAT INTELLIGENCE
// Neo4j Constraints and Indexes
// Version: 1.0.0
// Created: 2025-10-29
// ============================================================================

// ============================================================================
// UNIQUE CONSTRAINTS (15 Node Types)
// ============================================================================

// Organization
CREATE CONSTRAINT org_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE;

// Site
CREATE CONSTRAINT site_id IF NOT EXISTS FOR (s:Site) REQUIRE s.id IS UNIQUE;

// Train
CREATE CONSTRAINT train_id IF NOT EXISTS FOR (t:Train) REQUIRE t.id IS UNIQUE;

// Component
CREATE CONSTRAINT component_id IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE;

// Software
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (sw:Software) REQUIRE sw.id IS UNIQUE;

// Library
CREATE CONSTRAINT library_id IF NOT EXISTS FOR (l:Library) REQUIRE l.id IS UNIQUE;

// NetworkInterface
CREATE CONSTRAINT net_interface_id IF NOT EXISTS FOR (ni:NetworkInterface) REQUIRE ni.id IS UNIQUE;

// NetworkSegment
CREATE CONSTRAINT net_segment_id IF NOT EXISTS FOR (ns:NetworkSegment) REQUIRE ns.id IS UNIQUE;

// FirewallRule
CREATE CONSTRAINT firewall_rule_id IF NOT EXISTS FOR (fr:FirewallRule) REQUIRE fr.id IS UNIQUE;

// Protocol
CREATE CONSTRAINT protocol_id IF NOT EXISTS FOR (p:Protocol) REQUIRE p.id IS UNIQUE;

// CVE
CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE;

// ThreatActor
CREATE CONSTRAINT threat_actor_id IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.id IS UNIQUE;

// Campaign
CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (c:Campaign) REQUIRE c.id IS UNIQUE;

// AttackTechnique
CREATE CONSTRAINT attack_technique_id IF NOT EXISTS FOR (at:AttackTechnique) REQUIRE at.id IS UNIQUE;

// Document
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;

// ============================================================================
// PROPERTY INDEXES FOR PERFORMANCE
// ============================================================================

// Organization Indexes
CREATE INDEX org_name IF NOT EXISTS FOR (o:Organization) ON (o.name);
CREATE INDEX org_type IF NOT EXISTS FOR (o:Organization) ON (o.type);
CREATE INDEX org_country IF NOT EXISTS FOR (o:Organization) ON (o.country);

// Site Indexes
CREATE INDEX site_name IF NOT EXISTS FOR (s:Site) ON (s.name);
CREATE INDEX site_type IF NOT EXISTS FOR (s:Site) ON (s.type);
CREATE INDEX site_location IF NOT EXISTS FOR (s:Site) ON (s.location);

// Train Indexes
CREATE INDEX train_name IF NOT EXISTS FOR (t:Train) ON (t.name);
CREATE INDEX train_type IF NOT EXISTS FOR (t:Train) ON (t.type);
CREATE INDEX train_status IF NOT EXISTS FOR (t:Train) ON (t.status);
CREATE INDEX train_manufacturer IF NOT EXISTS FOR (t:Train) ON (t.manufacturer);

// Component Indexes
CREATE INDEX component_name IF NOT EXISTS FOR (c:Component) ON (c.name);
CREATE INDEX component_type IF NOT EXISTS FOR (c:Component) ON (c.type);
CREATE INDEX component_manufacturer IF NOT EXISTS FOR (c:Component) ON (c.manufacturer);
CREATE INDEX component_criticality IF NOT EXISTS FOR (c:Component) ON (c.criticalityLevel);

// Software Indexes
CREATE INDEX software_name IF NOT EXISTS FOR (sw:Software) ON (sw.name);
CREATE INDEX software_version IF NOT EXISTS FOR (sw:Software) ON (sw.version);
CREATE INDEX software_vendor IF NOT EXISTS FOR (sw:Software) ON (sw.vendor);
CREATE INDEX software_type IF NOT EXISTS FOR (sw:Software) ON (sw.type);

// Library Indexes
CREATE INDEX library_name IF NOT EXISTS FOR (l:Library) ON (l.name);
CREATE INDEX library_version IF NOT EXISTS FOR (l:Library) ON (l.version);

// NetworkInterface Indexes
CREATE INDEX net_interface_ip IF NOT EXISTS FOR (ni:NetworkInterface) ON (ni.ipAddress);
CREATE INDEX net_interface_mac IF NOT EXISTS FOR (ni:NetworkInterface) ON (ni.macAddress);
CREATE INDEX net_interface_type IF NOT EXISTS FOR (ni:NetworkInterface) ON (ni.type);

// NetworkSegment Indexes
CREATE INDEX net_segment_name IF NOT EXISTS FOR (ns:NetworkSegment) ON (ns.name);
CREATE INDEX net_segment_type IF NOT EXISTS FOR (ns:NetworkSegment) ON (ns.type);
CREATE INDEX net_segment_vlan IF NOT EXISTS FOR (ns:NetworkSegment) ON (ns.vlanId);

// FirewallRule Indexes
CREATE INDEX firewall_rule_name IF NOT EXISTS FOR (fr:FirewallRule) ON (fr.name);
CREATE INDEX firewall_rule_action IF NOT EXISTS FOR (fr:FirewallRule) ON (fr.action);
CREATE INDEX firewall_rule_priority IF NOT EXISTS FOR (fr:FirewallRule) ON (fr.priority);

// Protocol Indexes
CREATE INDEX protocol_name IF NOT EXISTS FOR (p:Protocol) ON (p.name);
CREATE INDEX protocol_port IF NOT EXISTS FOR (p:Protocol) ON (p.port);
CREATE INDEX protocol_type IF NOT EXISTS FOR (p:Protocol) ON (p.type);

// CVE Indexes
CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity);
CREATE INDEX cve_score IF NOT EXISTS FOR (c:CVE) ON (c.cvssScore);
CREATE INDEX cve_published IF NOT EXISTS FOR (c:CVE) ON (c.publishedDate);
CREATE INDEX cve_status IF NOT EXISTS FOR (c:CVE) ON (c.status);

// ThreatActor Indexes
CREATE INDEX threat_actor_name IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.name);
CREATE INDEX threat_actor_type IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.type);
CREATE INDEX threat_actor_sophistication IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.sophisticationLevel);

// Campaign Indexes
CREATE INDEX campaign_name IF NOT EXISTS FOR (c:Campaign) ON (c.name);
CREATE INDEX campaign_start IF NOT EXISTS FOR (c:Campaign) ON (c.startDate);
CREATE INDEX campaign_status IF NOT EXISTS FOR (c:Campaign) ON (c.status);

// AttackTechnique Indexes
CREATE INDEX attack_technique_name IF NOT EXISTS FOR (at:AttackTechnique) ON (at.name);
CREATE INDEX attack_technique_mitre IF NOT EXISTS FOR (at:AttackTechnique) ON (at.mitreId);
CREATE INDEX attack_technique_tactic IF NOT EXISTS FOR (at:AttackTechnique) ON (at.tactic);

// Document Indexes
CREATE INDEX document_title IF NOT EXISTS FOR (d:Document) ON (d.title);
CREATE INDEX document_type IF NOT EXISTS FOR (d:Document) ON (d.type);
CREATE INDEX document_created IF NOT EXISTS FOR (d:Document) ON (d.createdDate);

// ============================================================================
// FULL-TEXT SEARCH INDEXES
// ============================================================================

// Full-text search on CVE descriptions
CREATE FULLTEXT INDEX cve_fulltext IF NOT EXISTS
FOR (c:CVE) ON EACH [c.description, c.impact];

// Full-text search on ThreatActor intelligence
CREATE FULLTEXT INDEX threat_actor_fulltext IF NOT EXISTS
FOR (ta:ThreatActor) ON EACH [ta.name, ta.description, ta.aliases];

// Full-text search on Campaign intelligence
CREATE FULLTEXT INDEX campaign_fulltext IF NOT EXISTS
FOR (c:Campaign) ON EACH [c.name, c.description, c.objectives];

// Full-text search on AttackTechnique descriptions
CREATE FULLTEXT INDEX attack_technique_fulltext IF NOT EXISTS
FOR (at:AttackTechnique) ON EACH [at.name, at.description, at.detection];

// Full-text search on Document content
CREATE FULLTEXT INDEX document_fulltext IF NOT EXISTS
FOR (d:Document) ON EACH [d.title, d.content, d.summary];

// ============================================================================
// COMPOSITE INDEXES FOR COMPLEX QUERIES
// ============================================================================

// Component criticality and type for risk assessment
CREATE INDEX component_criticality_type IF NOT EXISTS
FOR (c:Component) ON (c.criticalityLevel, c.type);

// Software version and vulnerability status
CREATE INDEX software_version_vuln IF NOT EXISTS
FOR (sw:Software) ON (sw.version, sw.hasKnownVulnerabilities);

// CVE severity and publication date for threat prioritization
CREATE INDEX cve_severity_date IF NOT EXISTS
FOR (c:CVE) ON (c.severity, c.publishedDate);

// Network interface IP and status for network monitoring
CREATE INDEX net_interface_ip_status IF NOT EXISTS
FOR (ni:NetworkInterface) ON (ni.ipAddress, ni.status);

// ============================================================================
// RELATIONSHIP INDEXES
// ============================================================================

// Attack path relationship properties
CREATE INDEX attack_path_likelihood IF NOT EXISTS
FOR ()-[r:ATTACK_PATH_STEP]-() ON (r.likelihood);

// Vulnerability relationship properties
CREATE INDEX vuln_exploited IF NOT EXISTS
FOR ()-[r:HAS_VULNERABILITY]-() ON (r.exploited);

// Software dependency relationship properties
CREATE INDEX dependency_version IF NOT EXISTS
FOR ()-[r:DEPENDS_ON]-() ON (r.versionConstraint);

// ============================================================================
// END OF CONSTRAINTS AND INDEXES
// ============================================================================
