// AEON Cyber Digital Twin - Neo4j Indexes
// Created: 2025-11-26
// Purpose: Define indexes for query optimization

// ============================================================================
// CVE INDEXES
// ============================================================================
CREATE INDEX idx_cve_id IF NOT EXISTS FOR (n:CVE) ON (n.cveId);
CREATE INDEX idx_cve_severity IF NOT EXISTS FOR (n:CVE) ON (n.severity);
CREATE INDEX idx_cve_cvss_score IF NOT EXISTS FOR (n:CVE) ON (n.cvssScore);
CREATE INDEX idx_cve_actively_exploited IF NOT EXISTS FOR (n:CVE) ON (n.activelyExploited);
CREATE INDEX idx_cve_publication_date IF NOT EXISTS FOR (n:CVE) ON (n.publicationDate);
CREATE INDEX idx_cve_epss_score IF NOT EXISTS FOR (n:CVE) ON (n.epssScore);

// Composite indexes for common query patterns
CREATE INDEX idx_cve_severity_exploited IF NOT EXISTS FOR (n:CVE) ON (n.severity, n.activelyExploited);

// ============================================================================
// ENERGY DEVICE INDEXES
// ============================================================================
CREATE INDEX idx_device_id IF NOT EXISTS FOR (n:EnergyDevice) ON (n.deviceId);
CREATE INDEX idx_device_type IF NOT EXISTS FOR (n:EnergyDevice) ON (n.deviceType);
CREATE INDEX idx_device_criticality IF NOT EXISTS FOR (n:EnergyDevice) ON (n.criticality);
CREATE INDEX idx_device_vulnerability_count IF NOT EXISTS FOR (n:EnergyDevice) ON (n.vulnerabilityCount);
CREATE INDEX idx_device_patch_status IF NOT EXISTS FOR (n:EnergyDevice) ON (n.patchStatus);
CREATE INDEX idx_device_operational_status IF NOT EXISTS FOR (n:EnergyDevice) ON (n.operationalStatus);
CREATE INDEX idx_device_vendor IF NOT EXISTS FOR (n:EnergyDevice) ON (n.vendor);

// Composite indexes
CREATE INDEX idx_device_criticality_vulns IF NOT EXISTS FOR (n:EnergyDevice) ON (n.criticality, n.vulnerabilityCount);

// ============================================================================
// WATER SYSTEM INDEXES
// ============================================================================
CREATE INDEX idx_water_system_id IF NOT EXISTS FOR (n:WaterSystem) ON (n.waterSystemId);
CREATE INDEX idx_water_system_type IF NOT EXISTS FOR (n:WaterSystem) ON (n.systemType);
CREATE INDEX idx_water_criticality IF NOT EXISTS FOR (n:WaterSystem) ON (n.criticality);

// ============================================================================
// THREAT INTELLIGENCE INDEXES
// ============================================================================
CREATE INDEX idx_threat_actor_id IF NOT EXISTS FOR (n:ThreatActor) ON (n.actorId);
CREATE INDEX idx_threat_actor_name IF NOT EXISTS FOR (n:ThreatActor) ON (n.name);
CREATE INDEX idx_threat_actor_country IF NOT EXISTS FOR (n:ThreatActor) ON (n.country);
CREATE INDEX idx_threat_actor_capability IF NOT EXISTS FOR (n:ThreatActor) ON (n.capabilityLevel);

CREATE INDEX idx_attack_pattern_id IF NOT EXISTS FOR (n:AttackPattern) ON (n.patternId);
CREATE INDEX idx_attack_pattern_mitre IF NOT EXISTS FOR (n:AttackPattern) ON (n.mitreId);
CREATE INDEX idx_attack_pattern_tactic IF NOT EXISTS FOR (n:AttackPattern) ON (n.tacticName);

CREATE INDEX idx_malware_id IF NOT EXISTS FOR (n:MalwareVariant) ON (n.malwareId);
CREATE INDEX idx_malware_type IF NOT EXISTS FOR (n:MalwareVariant) ON (n.malwareType);

// ============================================================================
// INCIDENT & REPORT INDEXES
// ============================================================================
CREATE INDEX idx_incident_id IF NOT EXISTS FOR (n:IncidentReport) ON (n.incidentId);
CREATE INDEX idx_incident_severity IF NOT EXISTS FOR (n:IncidentReport) ON (n.severity);
CREATE INDEX idx_incident_date IF NOT EXISTS FOR (n:IncidentReport) ON (n.discoveryDate);

// Composite indexes
CREATE INDEX idx_incident_date_severity IF NOT EXISTS FOR (n:IncidentReport) ON (n.discoveryDate, n.severity);

// ============================================================================
// ORGANIZATION & LOCATION INDEXES
// ============================================================================
CREATE INDEX idx_org_id IF NOT EXISTS FOR (n:Organization) ON (n.organizationId);
CREATE INDEX idx_org_name IF NOT EXISTS FOR (n:Organization) ON (n.name);
CREATE INDEX idx_org_sector IF NOT EXISTS FOR (n:Organization) ON (n.sector);

CREATE INDEX idx_location_id IF NOT EXISTS FOR (n:Location) ON (n.locationId);
CREATE INDEX idx_location_type IF NOT EXISTS FOR (n:Location) ON (n.locationType);
CREATE INDEX idx_location_country IF NOT EXISTS FOR (n:Location) ON (n.country);

CREATE INDEX idx_sector_id IF NOT EXISTS FOR (n:Sector) ON (n.sectorId);
CREATE INDEX idx_sector_name IF NOT EXISTS FOR (n:Sector) ON (n.name);

// ============================================================================
// INFRASTRUCTURE INDEXES
// ============================================================================
CREATE INDEX idx_substation_id IF NOT EXISTS FOR (n:Substation) ON (n.substationId);
CREATE INDEX idx_substation_type IF NOT EXISTS FOR (n:Substation) ON (n.substationType);
CREATE INDEX idx_substation_criticality IF NOT EXISTS FOR (n:Substation) ON (n.criticality);

CREATE INDEX idx_transmission_line_id IF NOT EXISTS FOR (n:TransmissionLine) ON (n.lineId);
CREATE INDEX idx_transmission_voltage IF NOT EXISTS FOR (n:TransmissionLine) ON (n.voltageClass);

CREATE INDEX idx_ems_id IF NOT EXISTS FOR (n:EnergyManagementSystem) ON (n.emsId);
CREATE INDEX idx_ems_type IF NOT EXISTS FOR (n:EnergyManagementSystem) ON (n.systemType);

CREATE INDEX idx_der_id IF NOT EXISTS FOR (n:DistributedEnergyResource) ON (n.derId);
CREATE INDEX idx_der_type IF NOT EXISTS FOR (n:DistributedEnergyResource) ON (n.resourceType);

// ============================================================================
// COMPLIANCE INDEXES
// ============================================================================
CREATE INDEX idx_nerc_cip_id IF NOT EXISTS FOR (n:NERCCIPStandard) ON (n.standardId);
CREATE INDEX idx_compliance_id IF NOT EXISTS FOR (n:ComplianceFramework) ON (n.frameworkId);
