// AEON Cyber Digital Twin - Sample Sector and Organization Data
// Created: 2025-11-26
// Purpose: Bootstrap essential reference data

// ============================================================================
// SECTORS (Critical Infrastructure per CISA)
// ============================================================================

MERGE (s1:Sector {sectorId: 'SECTOR-ENERGY'})
SET s1 += {
  name: 'Energy',
  description: 'Electric power generation, transmission, and distribution',
  criticalityLevel: 5,
  knownThreatActors: ['APT33', 'APT28', 'Lazarus', 'XENOTIME'],
  regulatoryFramework: ['NERC-CIP', 'FERC', 'NIST-CSF'],
  estimatedAssets: 5000
};

MERGE (s2:Sector {sectorId: 'SECTOR-WATER'})
SET s2 += {
  name: 'Water and Wastewater',
  description: 'Drinking water and wastewater treatment facilities',
  criticalityLevel: 5,
  knownThreatActors: ['APT41', 'APT28'],
  regulatoryFramework: ['EPA', 'AWIA', 'NIST-CSF'],
  estimatedAssets: 3500
};

MERGE (s3:Sector {sectorId: 'SECTOR-CHEMICAL'})
SET s3 += {
  name: 'Chemical',
  description: 'Chemical manufacturing and distribution',
  criticalityLevel: 4,
  knownThreatActors: ['APT33', 'TEMP.Veles'],
  regulatoryFramework: ['CFATS', 'OSHA-PSM', 'EPA-RMP'],
  estimatedAssets: 2000
};

MERGE (s4:Sector {sectorId: 'SECTOR-MANUFACTURING'})
SET s4 += {
  name: 'Critical Manufacturing',
  description: 'Primary metals, machinery, electrical equipment',
  criticalityLevel: 4,
  knownThreatActors: ['APT10', 'APT41', 'FIN7'],
  regulatoryFramework: ['NIST-CSF', 'IEC62443'],
  estimatedAssets: 8000
};

MERGE (s5:Sector {sectorId: 'SECTOR-COMMUNICATIONS'})
SET s5 += {
  name: 'Communications',
  description: 'Telecommunications infrastructure',
  criticalityLevel: 5,
  knownThreatActors: ['APT41', 'LightBasin'],
  regulatoryFramework: ['FCC', 'CISA-CIRCIA'],
  estimatedAssets: 4000
};

// ============================================================================
// COMPLIANCE FRAMEWORKS
// ============================================================================

MERGE (cf1:ComplianceFramework {frameworkId: 'NERC-CIP'})
SET cf1 += {
  name: 'NERC Critical Infrastructure Protection',
  description: 'Mandatory cybersecurity standards for bulk power system',
  version: 'v8',
  effectiveDate: date('2024-01-01'),
  applicableSectors: ['Energy'],
  controlCount: 85
};

MERGE (cf2:ComplianceFramework {frameworkId: 'NIST-CSF'})
SET cf2 += {
  name: 'NIST Cybersecurity Framework',
  description: 'Voluntary framework for managing cybersecurity risk',
  version: '2.0',
  effectiveDate: date('2024-02-26'),
  applicableSectors: ['All'],
  controlCount: 108
};

MERGE (cf3:ComplianceFramework {frameworkId: 'IEC62443'})
SET cf3 += {
  name: 'IEC 62443 Industrial Automation Security',
  description: 'International standard for industrial control systems security',
  version: '4.2',
  effectiveDate: date('2023-06-01'),
  applicableSectors: ['Manufacturing', 'Energy', 'Chemical'],
  controlCount: 127
};

// ============================================================================
// SAMPLE THREAT ACTORS (Major APT Groups)
// ============================================================================

MERGE (ta1:ThreatActor {actorId: 'TA-APT33'})
SET ta1 += {
  name: 'APT33',
  aliases: ['Elfin', 'Refined Kitten', 'Magnallium'],
  country: 'IR',
  attributionConfidence: 0.9,
  capabilityLevel: 'advanced',
  operatingModel: 'state-sponsored',
  primaryTargets: ['Energy', 'Aviation', 'Petrochemical'],
  sophistication: 4,
  description: 'Iranian state-sponsored group targeting energy and aviation sectors'
};

MERGE (ta2:ThreatActor {actorId: 'TA-APT28'})
SET ta2 += {
  name: 'APT28',
  aliases: ['Fancy Bear', 'Sofacy', 'Sednit', 'STRONTIUM'],
  country: 'RU',
  attributionConfidence: 0.95,
  capabilityLevel: 'advanced',
  operatingModel: 'state-sponsored',
  primaryTargets: ['Government', 'Defense', 'Energy'],
  sophistication: 5,
  description: 'Russian GRU-affiliated group with global targeting'
};

MERGE (ta3:ThreatActor {actorId: 'TA-LAZARUS'})
SET ta3 += {
  name: 'Lazarus Group',
  aliases: ['HIDDEN COBRA', 'Guardians of Peace', 'APT38'],
  country: 'KP',
  attributionConfidence: 0.92,
  capabilityLevel: 'advanced',
  operatingModel: 'state-sponsored',
  primaryTargets: ['Financial', 'Energy', 'Cryptocurrency'],
  sophistication: 5,
  description: 'North Korean state-sponsored group targeting financial systems'
};

MERGE (ta4:ThreatActor {actorId: 'TA-XENOTIME'})
SET ta4 += {
  name: 'XENOTIME',
  aliases: ['Triton', 'TEMP.Veles'],
  country: 'RU',
  attributionConfidence: 0.85,
  capabilityLevel: 'expert',
  operatingModel: 'state-sponsored',
  primaryTargets: ['Energy', 'Industrial Control Systems'],
  sophistication: 5,
  description: 'Advanced ICS-focused group behind TRITON/TRISIS malware'
};

// ============================================================================
// SAMPLE LOCATIONS
// ============================================================================

MERGE (loc1:Location {locationId: 'LOC-US-NYC'})
SET loc1 += {
  name: 'New York City Metropolitan Area',
  locationType: 'metropolitan',
  country: 'US',
  state: 'NY',
  city: 'New York',
  timezone: 'America/New_York',
  riskProfile: 'high',
  criticalAssets: 2847,
  population: 8336000
};

MERGE (loc2:Location {locationId: 'LOC-US-LA'})
SET loc2 += {
  name: 'Los Angeles Metropolitan Area',
  locationType: 'metropolitan',
  country: 'US',
  state: 'CA',
  city: 'Los Angeles',
  timezone: 'America/Los_Angeles',
  riskProfile: 'high',
  criticalAssets: 2100,
  population: 3900000
};

MERGE (loc3:Location {locationId: 'LOC-US-CHI'})
SET loc3 += {
  name: 'Chicago Metropolitan Area',
  locationType: 'metropolitan',
  country: 'US',
  state: 'IL',
  city: 'Chicago',
  timezone: 'America/Chicago',
  riskProfile: 'high',
  criticalAssets: 1800,
  population: 2746000
};

// ============================================================================
// SAMPLE ORGANIZATIONS
// ============================================================================

MERGE (org1:Organization {organizationId: 'ORG-LADWP'})
SET org1 += {
  name: 'Los Angeles Department of Water and Power',
  acronym: 'LADWP',
  organizationType: 'utility',
  country: 'US',
  state: 'CA',
  sector: 'Energy',
  primaryMission: 'Electric power and water services for Los Angeles',
  employeeCount: 11000,
  criticality: 5,
  riskProfile: 'high'
};

MERGE (org2:Organization {organizationId: 'ORG-NYISO'})
SET org2 += {
  name: 'New York Independent System Operator',
  acronym: 'NYISO',
  organizationType: 'grid-operator',
  country: 'US',
  state: 'NY',
  sector: 'Energy',
  primaryMission: 'Electric grid management for New York State',
  employeeCount: 650,
  criticality: 5,
  riskProfile: 'critical'
};

// ============================================================================
// RELATIONSHIPS
// ============================================================================

// Organizations operate in locations
MATCH (org:Organization {organizationId: 'ORG-LADWP'}), (loc:Location {locationId: 'LOC-US-LA'})
MERGE (org)-[:OPERATES_IN]->(loc);

MATCH (org:Organization {organizationId: 'ORG-NYISO'}), (loc:Location {locationId: 'LOC-US-NYC'})
MERGE (org)-[:OPERATES_IN]->(loc);

// Organizations belong to sectors
MATCH (org:Organization {organizationId: 'ORG-LADWP'}), (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (org)-[:BELONGS_TO_SECTOR]->(s);

MATCH (org:Organization {organizationId: 'ORG-LADWP'}), (s:Sector {sectorId: 'SECTOR-WATER'})
MERGE (org)-[:BELONGS_TO_SECTOR]->(s);

MATCH (org:Organization {organizationId: 'ORG-NYISO'}), (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (org)-[:BELONGS_TO_SECTOR]->(s);

// Threat actors target sectors
MATCH (ta:ThreatActor {actorId: 'TA-APT33'}), (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (ta)-[:TARGETS_SECTOR {confidence: 0.9, lastObserved: date('2024-06-15')}]->(s);

MATCH (ta:ThreatActor {actorId: 'TA-XENOTIME'}), (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (ta)-[:TARGETS_SECTOR {confidence: 0.95, lastObserved: date('2024-08-20')}]->(s);

MATCH (ta:ThreatActor {actorId: 'TA-APT28'}), (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (ta)-[:TARGETS_SECTOR {confidence: 0.85, lastObserved: date('2024-10-01')}]->(s);
