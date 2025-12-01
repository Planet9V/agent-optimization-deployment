// AEON Cyber Digital Twin - Neo4j Constraints
// Created: 2025-11-26
// Purpose: Define uniqueness constraints for all entity types

// Core Security Nodes
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (n:CVE) REQUIRE n.cveId IS UNIQUE;
CREATE CONSTRAINT exploit_id_unique IF NOT EXISTS FOR (n:Exploit) REQUIRE n.exploitId IS UNIQUE;
CREATE CONSTRAINT threat_actor_id_unique IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.actorId IS UNIQUE;
CREATE CONSTRAINT attack_pattern_id_unique IF NOT EXISTS FOR (n:AttackPattern) REQUIRE n.patternId IS UNIQUE;
CREATE CONSTRAINT malware_id_unique IF NOT EXISTS FOR (n:MalwareVariant) REQUIRE n.malwareId IS UNIQUE;

// Energy Infrastructure Nodes
CREATE CONSTRAINT device_id_unique IF NOT EXISTS FOR (n:EnergyDevice) REQUIRE n.deviceId IS UNIQUE;
CREATE CONSTRAINT property_id_unique IF NOT EXISTS FOR (n:EnergyProperty) REQUIRE n.propertyId IS UNIQUE;
CREATE CONSTRAINT measurement_id_unique IF NOT EXISTS FOR (n:Measurement) REQUIRE n.measurementId IS UNIQUE;
CREATE CONSTRAINT substation_id_unique IF NOT EXISTS FOR (n:Substation) REQUIRE n.substationId IS UNIQUE;
CREATE CONSTRAINT transmission_line_id_unique IF NOT EXISTS FOR (n:TransmissionLine) REQUIRE n.lineId IS UNIQUE;
CREATE CONSTRAINT ems_id_unique IF NOT EXISTS FOR (n:EnergyManagementSystem) REQUIRE n.emsId IS UNIQUE;
CREATE CONSTRAINT der_id_unique IF NOT EXISTS FOR (n:DistributedEnergyResource) REQUIRE n.derId IS UNIQUE;

// Water Infrastructure Nodes
CREATE CONSTRAINT water_system_id_unique IF NOT EXISTS FOR (n:WaterSystem) REQUIRE n.waterSystemId IS UNIQUE;
CREATE CONSTRAINT water_property_id_unique IF NOT EXISTS FOR (n:WaterProperty) REQUIRE n.propertyId IS UNIQUE;

// Organizational & Administrative Nodes
CREATE CONSTRAINT org_id_unique IF NOT EXISTS FOR (n:Organization) REQUIRE n.organizationId IS UNIQUE;
CREATE CONSTRAINT location_id_unique IF NOT EXISTS FOR (n:Location) REQUIRE n.locationId IS UNIQUE;
CREATE CONSTRAINT sector_id_unique IF NOT EXISTS FOR (n:Sector) REQUIRE n.sectorId IS UNIQUE;

// Report & Intelligence Nodes
CREATE CONSTRAINT incident_id_unique IF NOT EXISTS FOR (n:IncidentReport) REQUIRE n.incidentId IS UNIQUE;
CREATE CONSTRAINT vuln_report_id_unique IF NOT EXISTS FOR (n:VulnerabilityReport) REQUIRE n.reportId IS UNIQUE;

// Compliance Nodes
CREATE CONSTRAINT nerc_cip_id_unique IF NOT EXISTS FOR (n:NERCCIPStandard) REQUIRE n.standardId IS UNIQUE;
CREATE CONSTRAINT compliance_id_unique IF NOT EXISTS FOR (n:ComplianceFramework) REQUIRE n.frameworkId IS UNIQUE;
