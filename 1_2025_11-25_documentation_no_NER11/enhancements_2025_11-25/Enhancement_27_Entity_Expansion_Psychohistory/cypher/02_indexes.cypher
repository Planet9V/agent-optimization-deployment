// ============================================================
// Enhancement 27: Performance Indexes
// File: 02_indexes.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Define composite and single-property indexes for query optimization
// ============================================================

// ------------------------------------------------------------
// SECTION 1: Discriminator Property Indexes (CRITICAL)
// These indexes enable O(log n) lookups on property-based queries
// ------------------------------------------------------------

// 1.1 Asset - Class and device type composite
CREATE INDEX asset_class_device IF NOT EXISTS
FOR (n:Asset) ON (n.assetClass, n.deviceType);

// 1.2 Asset - Purdue level for ICS queries
CREATE INDEX asset_purdue IF NOT EXISTS
FOR (n:Asset) ON (n.purdue_level);

// 1.3 PsychTrait - Type and subtype composite
CREATE INDEX psych_trait_type IF NOT EXISTS
FOR (n:PsychTrait) ON (n.traitType, n.subtype);

// 1.4 PsychTrait - Intensity for threshold queries
CREATE INDEX psych_trait_intensity IF NOT EXISTS
FOR (n:PsychTrait) ON (n.intensity);

// 1.5 Vulnerability - Type discriminator
CREATE INDEX vuln_type IF NOT EXISTS
FOR (n:Vulnerability) ON (n.vulnType);

// 1.6 Vulnerability - CVSS score for prioritization
CREATE INDEX vuln_cvss IF NOT EXISTS
FOR (n:Vulnerability) ON (n.cvss_score);

// 1.7 AttackPattern - Type discriminator
CREATE INDEX pattern_type IF NOT EXISTS
FOR (n:AttackPattern) ON (n.patternType);

// 1.8 Malware - Family discriminator
CREATE INDEX malware_family IF NOT EXISTS
FOR (n:Malware) ON (n.malwareFamily);

// 1.9 Control - Type discriminator
CREATE INDEX control_type IF NOT EXISTS
FOR (n:Control) ON (n.controlType);

// 1.10 Event - Type discriminator
CREATE INDEX event_type IF NOT EXISTS
FOR (n:Event) ON (n.eventType);

// 1.11 Protocol - Type discriminator
CREATE INDEX protocol_type IF NOT EXISTS
FOR (n:Protocol) ON (n.protocolType);

// 1.12 EconomicMetric - Type discriminator
CREATE INDEX metric_type IF NOT EXISTS
FOR (n:EconomicMetric) ON (n.metricType);

// 1.13 Indicator - Type discriminator
CREATE INDEX indicator_type IF NOT EXISTS
FOR (n:Indicator) ON (n.indicatorType);

// 1.14 Organization - Type discriminator
CREATE INDEX org_type IF NOT EXISTS
FOR (n:Organization) ON (n.orgType);

// 1.15 Location - Type discriminator
CREATE INDEX location_type IF NOT EXISTS
FOR (n:Location) ON (n.locationType);

// 1.16 Role - Type discriminator
CREATE INDEX role_type IF NOT EXISTS
FOR (n:Role) ON (n.roleType);

// 1.17 Campaign - Type discriminator
CREATE INDEX campaign_type IF NOT EXISTS
FOR (n:Campaign) ON (n.campaignType);

// 1.18 ThreatActor - Type discriminator
CREATE INDEX actor_type IF NOT EXISTS
FOR (n:ThreatActor) ON (n.actorType);

// ------------------------------------------------------------
// SECTION 2: Name/Search Indexes
// For common lookup patterns
// ------------------------------------------------------------

// 2.1 ThreatActor name search
CREATE INDEX threat_actor_name_search IF NOT EXISTS
FOR (n:ThreatActor) ON (n.name);

// 2.2 Software name search
CREATE INDEX software_name_search IF NOT EXISTS
FOR (n:Software) ON (n.name);

// 2.3 Organization name search
CREATE INDEX org_name_search IF NOT EXISTS
FOR (n:Organization) ON (n.name);

// 2.4 Asset name search
CREATE INDEX asset_name_search IF NOT EXISTS
FOR (n:Asset) ON (n.name);

// ------------------------------------------------------------
// SECTION 3: Temporal Indexes
// For time-series and event queries
// ------------------------------------------------------------

// 3.1 Event timestamp for chronological queries
CREATE INDEX event_timestamp IF NOT EXISTS
FOR (n:Event) ON (n.timestamp);

// 3.2 Campaign active period
CREATE INDEX campaign_dates IF NOT EXISTS
FOR (n:Campaign) ON (n.start_date, n.end_date);

// 3.3 Vulnerability discovery date
CREATE INDEX vuln_discovered IF NOT EXISTS
FOR (n:Vulnerability) ON (n.discovered_date);

// ------------------------------------------------------------
// SECTION 4: Psychohistory-Specific Indexes
// For mathematical model queries
// ------------------------------------------------------------

// 4.1 PsychTrait Lacanian register
CREATE INDEX psych_lacanian IF NOT EXISTS
FOR (n:PsychTrait) ON (n.traitType)
WHERE n.traitType = 'lacanian';

// 4.2 PsychTrait cognitive bias
CREATE INDEX psych_cognitive IF NOT EXISTS
FOR (n:PsychTrait) ON (n.traitType)
WHERE n.traitType = 'cognitive_bias';

// ------------------------------------------------------------
// SECTION 5: Full-Text Indexes (Optional)
// For natural language search
// ------------------------------------------------------------

// 5.1 Attack pattern description search
CREATE FULLTEXT INDEX attack_pattern_fulltext IF NOT EXISTS
FOR (n:AttackPattern) ON EACH [n.name, n.description];

// 5.2 Vulnerability description search
CREATE FULLTEXT INDEX vulnerability_fulltext IF NOT EXISTS
FOR (n:Vulnerability) ON EACH [n.name, n.description];

// 5.3 Control description search
CREATE FULLTEXT INDEX control_fulltext IF NOT EXISTS
FOR (n:Control) ON EACH [n.name, n.description];

// ------------------------------------------------------------
// VERIFICATION QUERY
// ------------------------------------------------------------
// Run after execution to verify all indexes:
// SHOW INDEXES YIELD name, type, entityType, properties, state
// WHERE state = 'ONLINE'
// RETURN name, type, entityType, properties
// ORDER BY name;

// Expected: 25+ indexes across all Super Labels
