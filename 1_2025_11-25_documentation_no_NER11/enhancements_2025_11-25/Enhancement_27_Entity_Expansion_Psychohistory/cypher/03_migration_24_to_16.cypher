// ============================================================
// Enhancement 27: Schema Migration (24 → 16 Super Labels)
// File: 03_migration_24_to_16.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Migrate existing 24 labels to 16 Super Label architecture
// ============================================================

// ============================================================
// PHASE 1: BACKUP VERIFICATION
// ============================================================
// CRITICAL: Run backup before executing migration
// CALL apoc.export.cypher.all('/backup/pre_e27_migration.cypher', {format: 'cypher-shell'});

// ============================================================
// PHASE 2: ADD DISCRIMINATOR PROPERTIES TO KEPT LABELS
// ============================================================

// 2.1 ThreatActor - Add actorType if missing
MATCH (n:ThreatActor)
WHERE n.actorType IS NULL
SET n.actorType = CASE
  WHEN n.type IS NOT NULL THEN n.type
  WHEN n.name CONTAINS 'APT' THEN 'apt'
  WHEN n.name CONTAINS 'State' THEN 'nation_state'
  ELSE 'unknown'
END;

// 2.2 AttackPattern - Add patternType if missing
MATCH (n:AttackPattern)
WHERE n.patternType IS NULL
SET n.patternType = CASE
  WHEN n.external_id STARTS WITH 'T' THEN 'technique'
  WHEN n.external_id STARTS WITH 'TA' THEN 'tactic'
  WHEN n.external_id STARTS WITH 'CAPEC' THEN 'capec'
  ELSE 'technique'
END;

// 2.3 Organization - Add orgType if missing
MATCH (n:Organization)
WHERE n.orgType IS NULL
SET n.orgType = CASE
  WHEN n.sector IS NOT NULL THEN 'company'
  WHEN n.name CONTAINS 'Agency' THEN 'government'
  WHEN n.name CONTAINS 'University' THEN 'academic'
  ELSE 'company'
END;

// 2.4 Location - Add locationType if missing
MATCH (n:Location)
WHERE n.locationType IS NULL
SET n.locationType = CASE
  WHEN n.type IS NOT NULL THEN n.type
  WHEN n.coordinates IS NOT NULL THEN 'geo'
  ELSE 'facility'
END;

// 2.5 Software - Add softwareType if missing
MATCH (n:Software)
WHERE n.softwareType IS NULL
SET n.softwareType = CASE
  WHEN n.is_malware = true THEN 'malware_tool'
  WHEN n.type IS NOT NULL THEN n.type
  ELSE 'application'
END;

// ============================================================
// PHASE 3: CONSOLIDATE ATTACK LABELS
// ============================================================

// 3.1 AttackTechnique → AttackPattern
MATCH (n:AttackTechnique)
SET n:AttackPattern
SET n.patternType = 'technique'
SET n.migrated_from = 'AttackTechnique'
SET n.migration_date = datetime()
REMOVE n:AttackTechnique;

// ============================================================
// PHASE 4: CONSOLIDATE VULNERABILITY LABELS
// ============================================================

// 4.1 CVE → Vulnerability
MATCH (n:CVE)
SET n:Vulnerability
SET n.vulnType = 'cve'
SET n.migrated_from = 'CVE'
SET n.migration_date = datetime()
REMOVE n:CVE;

// 4.2 Exploit → Vulnerability
MATCH (n:Exploit)
SET n:Vulnerability
SET n.vulnType = 'exploit'
SET n.migrated_from = 'Exploit'
SET n.migration_date = datetime()
REMOVE n:Exploit;

// 4.3 VulnerabilityReport → Vulnerability
MATCH (n:VulnerabilityReport)
SET n:Vulnerability
SET n.vulnType = 'report'
SET n.migrated_from = 'VulnerabilityReport'
SET n.migration_date = datetime()
REMOVE n:VulnerabilityReport;

// ============================================================
// PHASE 5: CONSOLIDATE MALWARE LABELS
// ============================================================

// 5.1 MalwareVariant → Malware
MATCH (n:MalwareVariant)
SET n:Malware
SET n.malwareFamily = coalesce(n.family, 'unknown')
SET n.migrated_from = 'MalwareVariant'
SET n.migration_date = datetime()
REMOVE n:MalwareVariant;

// ============================================================
// PHASE 6: CONSOLIDATE CONTROL/MITIGATION LABELS
// ============================================================

// 6.1 Mitigation → Control
MATCH (n:Mitigation)
SET n:Control
SET n.controlType = 'mitigation'
SET n.migrated_from = 'Mitigation'
SET n.migration_date = datetime()
REMOVE n:Mitigation;

// 6.2 ComplianceFramework → Control
MATCH (n:ComplianceFramework)
SET n:Control
SET n.controlType = 'compliance'
SET n.migrated_from = 'ComplianceFramework'
SET n.migration_date = datetime()
REMOVE n:ComplianceFramework;

// 6.3 NERCCIPStandard → Control
MATCH (n:NERCCIPStandard)
SET n:Control
SET n.controlType = 'nerc_cip'
SET n.migrated_from = 'NERCCIPStandard'
SET n.migration_date = datetime()
REMOVE n:NERCCIPStandard;

// ============================================================
// PHASE 7: CONSOLIDATE EVENT LABELS
// ============================================================

// 7.1 IncidentReport → Event
MATCH (n:IncidentReport)
SET n:Event
SET n.eventType = 'incident'
SET n.migrated_from = 'IncidentReport'
SET n.migration_date = datetime()
REMOVE n:IncidentReport;

// ============================================================
// PHASE 8: CONSOLIDATE ORGANIZATION LABELS
// ============================================================

// 8.1 Sector → Organization
MATCH (n:Sector)
SET n:Organization
SET n.orgType = 'sector'
SET n.migrated_from = 'Sector'
SET n.migration_date = datetime()
REMOVE n:Sector;

// ============================================================
// PHASE 9: CONSOLIDATE OT/INFRASTRUCTURE ASSETS
// ============================================================

// 9.1 Substation → Asset
MATCH (n:Substation)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'substation'
SET n.purdue_level = 1
SET n.migrated_from = 'Substation'
SET n.migration_date = datetime()
REMOVE n:Substation;

// 9.2 TransmissionLine → Asset
MATCH (n:TransmissionLine)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'transmission_line'
SET n.purdue_level = 0
SET n.migrated_from = 'TransmissionLine'
SET n.migration_date = datetime()
REMOVE n:TransmissionLine;

// 9.3 EnergyDevice → Asset
MATCH (n:EnergyDevice)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'energy_device'
SET n.purdue_level = 1
SET n.migrated_from = 'EnergyDevice'
SET n.migration_date = datetime()
REMOVE n:EnergyDevice;

// 9.4 EnergyManagementSystem → Asset
MATCH (n:EnergyManagementSystem)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'ems'
SET n.purdue_level = 2
SET n.migrated_from = 'EnergyManagementSystem'
SET n.migration_date = datetime()
REMOVE n:EnergyManagementSystem;

// 9.5 DistributedEnergyResource → Asset
MATCH (n:DistributedEnergyResource)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'der'
SET n.purdue_level = 0
SET n.migrated_from = 'DistributedEnergyResource'
SET n.migration_date = datetime()
REMOVE n:DistributedEnergyResource;

// 9.6 WaterSystem → Asset
MATCH (n:WaterSystem)
SET n:Asset
SET n.assetClass = 'OT'
SET n.deviceType = 'water_system'
SET n.purdue_level = 1
SET n.migrated_from = 'WaterSystem'
SET n.migration_date = datetime()
REMOVE n:WaterSystem;

// ============================================================
// PHASE 10: CONSOLIDATE INDICATOR LABELS
// ============================================================

// 10.1 Measurement → Indicator
MATCH (n:Measurement)
SET n:Indicator
SET n.indicatorType = 'measurement'
SET n.migrated_from = 'Measurement'
SET n.migration_date = datetime()
REMOVE n:Measurement;

// 10.2 EnergyProperty → Indicator
MATCH (n:EnergyProperty)
SET n:Indicator
SET n.indicatorType = 'energy_property'
SET n.migrated_from = 'EnergyProperty'
SET n.migration_date = datetime()
REMOVE n:EnergyProperty;

// 10.3 WaterProperty → Indicator
MATCH (n:WaterProperty)
SET n:Indicator
SET n.indicatorType = 'water_property'
SET n.migrated_from = 'WaterProperty'
SET n.migration_date = datetime()
REMOVE n:WaterProperty;

// ============================================================
// PHASE 11: CREATE NEW SUPER LABELS (Empty initialization)
// ============================================================

// 11.1 Create PsychTrait schema node (for APOC procedures)
CREATE (schema:_Schema {
  label: 'PsychTrait',
  created: datetime(),
  properties: ['traitType', 'subtype', 'name', 'intensity', 'description']
});

// 11.2 Create EconomicMetric schema node
CREATE (schema:_Schema {
  label: 'EconomicMetric',
  created: datetime(),
  properties: ['metricType', 'metric_id', 'amount', 'currency', 'category']
});

// 11.3 Create Role schema node
CREATE (schema:_Schema {
  label: 'Role',
  created: datetime(),
  properties: ['roleType', 'role_name', 'privilege_level', 'description']
});

// 11.4 Create Protocol schema node
CREATE (schema:_Schema {
  label: 'Protocol',
  created: datetime(),
  properties: ['protocolType', 'protocol_name', 'layer', 'security_level']
});

// 11.5 Create Campaign schema node
CREATE (schema:_Schema {
  label: 'Campaign',
  created: datetime(),
  properties: ['campaignType', 'campaign_id', 'name', 'attribution', 'confidence']
});

// ============================================================
// VERIFICATION QUERIES
// ============================================================

// V1: Count nodes per label (should show 16 Super Labels)
// CALL db.labels() YIELD label
// MATCH (n) WHERE label IN labels(n)
// RETURN label, count(n) as node_count
// ORDER BY label;

// V2: Check for any remaining deprecated labels
// MATCH (n)
// WHERE any(l IN labels(n) WHERE l IN [
//   'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport',
//   'MalwareVariant', 'Mitigation', 'ComplianceFramework', 'NERCCIPStandard',
//   'IncidentReport', 'Sector', 'Substation', 'TransmissionLine',
//   'EnergyDevice', 'EnergyManagementSystem', 'DistributedEnergyResource',
//   'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
// ])
// RETURN labels(n)[0] as deprecated_label, count(*) as remaining
// ORDER BY deprecated_label;

// V3: Verify migration tracking
// MATCH (n)
// WHERE n.migrated_from IS NOT NULL
// RETURN n.migrated_from as source_label, count(*) as migrated_count
// ORDER BY source_label;
