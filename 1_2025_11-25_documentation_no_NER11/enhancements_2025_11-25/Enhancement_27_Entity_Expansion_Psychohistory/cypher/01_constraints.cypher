// ============================================================
// Enhancement 27: Uniqueness Constraints
// File: 01_constraints.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Define uniqueness constraints for all 16 Super Labels
// ============================================================

// ------------------------------------------------------------
// SECTION 1: Core Threat Intelligence Labels
// ------------------------------------------------------------

// 1.1 ThreatActor - Primary key on name
CREATE CONSTRAINT threat_actor_name IF NOT EXISTS
FOR (n:ThreatActor) REQUIRE n.name IS UNIQUE;

// 1.2 AttackPattern - Primary key on external_id (MITRE ATT&CK ID)
CREATE CONSTRAINT attack_pattern_id IF NOT EXISTS
FOR (n:AttackPattern) REQUIRE n.external_id IS UNIQUE;

// 1.3 Vulnerability - Primary key on external_id (CVE/CWE ID)
CREATE CONSTRAINT vulnerability_id IF NOT EXISTS
FOR (n:Vulnerability) REQUIRE n.external_id IS UNIQUE;

// 1.4 Malware - Primary key on name
CREATE CONSTRAINT malware_name IF NOT EXISTS
FOR (n:Malware) REQUIRE n.name IS UNIQUE;

// 1.5 Indicator - Primary key on indicator_value (hash, IP, etc.)
CREATE CONSTRAINT indicator_id IF NOT EXISTS
FOR (n:Indicator) REQUIRE n.indicator_value IS UNIQUE;

// ------------------------------------------------------------
// SECTION 2: Infrastructure Labels
// ------------------------------------------------------------

// 2.1 Asset - Primary key on asset_id
CREATE CONSTRAINT asset_id IF NOT EXISTS
FOR (n:Asset) REQUIRE n.asset_id IS UNIQUE;

// 2.2 Organization - Primary key on name
CREATE CONSTRAINT org_name IF NOT EXISTS
FOR (n:Organization) REQUIRE n.name IS UNIQUE;

// 2.3 Location - Composite key on name + locationType
CREATE CONSTRAINT location_id IF NOT EXISTS
FOR (n:Location) REQUIRE (n.name, n.locationType) IS NODE KEY;

// 2.4 Protocol - Primary key on protocol_name
CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (n:Protocol) REQUIRE n.protocol_name IS UNIQUE;

// 2.5 Software - Primary key on name
CREATE CONSTRAINT software_name IF NOT EXISTS
FOR (n:Software) REQUIRE n.name IS UNIQUE;

// ------------------------------------------------------------
// SECTION 3: Psychometric Labels
// ------------------------------------------------------------

// 3.1 PsychTrait - Composite key on traitType + subtype
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS
FOR (n:PsychTrait) REQUIRE (n.traitType, n.subtype) IS NODE KEY;

// 3.2 Role - Primary key on role_name
CREATE CONSTRAINT role_id IF NOT EXISTS
FOR (n:Role) REQUIRE n.role_name IS UNIQUE;

// ------------------------------------------------------------
// SECTION 4: Economic & Event Labels
// ------------------------------------------------------------

// 4.1 EconomicMetric - Primary key on metric_id
CREATE CONSTRAINT economic_metric_id IF NOT EXISTS
FOR (n:EconomicMetric) REQUIRE n.metric_id IS UNIQUE;

// 4.2 Campaign - Primary key on campaign_id
CREATE CONSTRAINT campaign_id IF NOT EXISTS
FOR (n:Campaign) REQUIRE n.campaign_id IS UNIQUE;

// 4.3 Event - Primary key on event_id
CREATE CONSTRAINT event_id IF NOT EXISTS
FOR (n:Event) REQUIRE n.event_id IS UNIQUE;

// 4.4 Control - Primary key on control_id
CREATE CONSTRAINT control_id IF NOT EXISTS
FOR (n:Control) REQUIRE n.control_id IS UNIQUE;

// ------------------------------------------------------------
// VERIFICATION QUERY
// ------------------------------------------------------------
// Run after execution to verify all constraints:
// SHOW CONSTRAINTS YIELD name, type, entityType, properties
// WHERE type = 'UNIQUENESS' OR type = 'NODE_KEY'
// RETURN name, type, entityType, properties
// ORDER BY name;

// Expected: 16 constraints (one per Super Label)
