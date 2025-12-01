// ═══════════════════════════════════════════════════════════════
// PHASE 2: Add Relationships (100% ADDITIVE)
// Universal Location Architecture Migration
// Created: 2025-11-13
// Status: READY FOR DEPLOYMENT
// Constitution: GAP-004 Zero Breaking Changes
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// PREREQUISITE: Sample Facility/Customer/Region/Sector Nodes
// (For demonstration - production would import from data source)
// ───────────────────────────────────────────────────────────────

// Create sample Sector nodes (Critical Infrastructure Sectors)
MERGE (s_energy:Sector {sectorId: 'SECTOR-ENERGY'})
SET s_energy.name = 'Energy',
    s_energy.criticalInfrastructure = true,
    s_energy.regulatoryFramework = 'IEC 62443, NERC CIP',
    s_energy.created = datetime();

MERGE (s_water:Sector {sectorId: 'SECTOR-WATER'})
SET s_water.name = 'Water and Wastewater',
    s_water.criticalInfrastructure = true,
    s_water.regulatoryFramework = 'IEC 62443, AWWA',
    s_water.created = datetime();

MERGE (s_transport:Sector {sectorId: 'SECTOR-TRANSPORT'})
SET s_transport.name = 'Transportation',
    s_transport.criticalInfrastructure = true,
    s_transport.regulatoryFramework = 'IEC 62443, TSA',
    s_transport.created = datetime();

// Create sample Region nodes (Geographic Operational Regions)
MERGE (r_northeast:Region {regionId: 'REGION-NE-GRID'})
SET r_northeast.name = 'Northeast Power Grid',
    r_northeast.regionType = 'GRID_REGION',
    r_northeast.created = datetime();

MERGE (r_pacific:Region {regionId: 'REGION-PACIFIC-WATER'})
SET r_pacific.name = 'Pacific Water District',
    r_pacific.regionType = 'WATER_DISTRICT',
    r_pacific.created = datetime();

MERGE (r_rail:Region {regionId: 'REGION-RAIL-001'})
SET r_rail.name = 'Railway Network - Region 001',
    r_rail.regionType = 'TRANSPORTATION_ZONE',
    r_rail.created = datetime();

// Create sample Customer nodes (Multi-tenant Organizations)
MERGE (c_utility:Customer {customerId: 'CUSTOMER-UTILITY-001'})
SET c_utility.name = 'Northeast Power Utility',
    c_utility.customerType = 'UTILITY',
    c_utility.customer_namespace = 'utility_operator_001',
    c_utility.tags = ['electric_utility', 'ISO27001_certified'],
    c_utility.created = datetime();

MERGE (c_water:Customer {customerId: 'CUSTOMER-WATER-001'})
SET c_water.name = 'Pacific Water Authority',
    c_water.customerType = 'GOVERNMENT',
    c_water.customer_namespace = 'water_operator_001',
    c_water.tags = ['municipal_water', 'critical_infrastructure'],
    c_water.created = datetime();

MERGE (c_railway:Customer {customerId: 'CUSTOMER-RAILWAY-001'})
SET c_railway.name = 'Railway Operator 001',
    c_railway.customerType = 'UTILITY',
    c_railway.customer_namespace = 'railway_operator_001',
    c_railway.tags = ['passenger_rail', 'critical_infrastructure'],
    c_railway.created = datetime();

// Create sample Facility nodes (Physical Locations)
MERGE (fac_scada:Facility {facilityId: 'FAC-SCADA-NE-001'})
SET fac_scada.name = 'SCADA Control Center - Northeast',
    fac_scada.facilityType = 'SCADA_CONTROL_CENTER',
    fac_scada.address = '123 Grid Control Way, Boston, MA',
    fac_scada.`geographic.latitude` = 42.3601,
    fac_scada.`geographic.longitude` = -71.0589,
    fac_scada.customer_namespace = 'utility_operator_001',
    fac_scada.tags = ['critical_infrastructure', 'energy_sector', 'IEC62443_applicable'],
    fac_scada.created = datetime();

MERGE (fac_substation:Facility {facilityId: 'FAC-SUBSTATION-001'})
SET fac_substation.name = 'Substation Alpha',
    fac_substation.facilityType = 'SUBSTATION',
    fac_substation.address = '456 Transformer Rd, Providence, RI',
    fac_substation.`geographic.latitude` = 41.8240,
    fac_substation.`geographic.longitude` = -71.4128,
    fac_substation.customer_namespace = 'utility_operator_001',
    fac_substation.tags = ['critical_infrastructure', 'energy_sector'],
    fac_substation.created = datetime();

MERGE (fac_water:Facility {facilityId: 'FAC-WATER-TREATMENT-001'})
SET fac_water.name = 'Water Treatment Plant - Pacific',
    fac_water.facilityType = 'WATER_TREATMENT_PLANT',
    fac_water.address = '789 Aqua Drive, San Francisco, CA',
    fac_water.`geographic.latitude` = 37.7749,
    fac_water.`geographic.longitude` = -122.4194,
    fac_water.customer_namespace = 'water_operator_001',
    fac_water.tags = ['critical_infrastructure', 'water_sector'],
    fac_water.created = datetime();

MERGE (fac_railway:Facility {facilityId: 'FAC-RAILWAY-STATION-001'})
SET fac_railway.name = 'Railway Control Station - Region 001',
    fac_railway.facilityType = 'RAILWAY_CONTROL_CENTER',
    fac_railway.address = '101 Rail Plaza, New York, NY',
    fac_railway.`geographic.latitude` = 40.7128,
    fac_railway.`geographic.longitude` = -74.0060,
    fac_railway.customer_namespace = 'railway_operator_001',
    fac_railway.tags = ['critical_infrastructure', 'transportation_sector'],
    fac_railway.created = datetime();

// ───────────────────────────────────────────────────────────────
// RELATIONSHIPS - Organizational Hierarchy
// ───────────────────────────────────────────────────────────────

// Facility → Customer (OWNED_BY)
MATCH (fac:Facility {facilityId: 'FAC-SCADA-NE-001'})
MATCH (c:Customer {customerId: 'CUSTOMER-UTILITY-001'})
WHERE fac.customer_namespace = c.customer_namespace
MERGE (fac)-[:OWNED_BY {
  since: datetime(),
  ownershipType: 'DIRECT'
}]->(c);

MATCH (fac:Facility {facilityId: 'FAC-SUBSTATION-001'})
MATCH (c:Customer {customerId: 'CUSTOMER-UTILITY-001'})
WHERE fac.customer_namespace = c.customer_namespace
MERGE (fac)-[:OWNED_BY {
  since: datetime(),
  ownershipType: 'DIRECT'
}]->(c);

MATCH (fac:Facility {facilityId: 'FAC-WATER-TREATMENT-001'})
MATCH (c:Customer {customerId: 'CUSTOMER-WATER-001'})
WHERE fac.customer_namespace = c.customer_namespace
MERGE (fac)-[:OWNED_BY {
  since: datetime(),
  ownershipType: 'DIRECT'
}]->(c);

MATCH (fac:Facility {facilityId: 'FAC-RAILWAY-STATION-001'})
MATCH (c:Customer {customerId: 'CUSTOMER-RAILWAY-001'})
WHERE fac.customer_namespace = c.customer_namespace
MERGE (fac)-[:OWNED_BY {
  since: datetime(),
  ownershipType: 'DIRECT'
}]->(c);

// Facility → Region (IN_REGION)
MATCH (fac:Facility)
MATCH (r:Region)
WHERE (fac.facilityId IN ['FAC-SCADA-NE-001', 'FAC-SUBSTATION-001'] AND r.regionId = 'REGION-NE-GRID')
   OR (fac.facilityId = 'FAC-WATER-TREATMENT-001' AND r.regionId = 'REGION-PACIFIC-WATER')
   OR (fac.facilityId = 'FAC-RAILWAY-STATION-001' AND r.regionId = 'REGION-RAIL-001')
MERGE (fac)-[:IN_REGION {
  assigned: datetime()
}]->(r);

// Region → Sector (OPERATES_IN)
MATCH (r:Region {regionId: 'REGION-NE-GRID'})
MATCH (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (r)-[:OPERATES_IN {
  primarySector: true
}]->(s);

MATCH (r:Region {regionId: 'REGION-PACIFIC-WATER'})
MATCH (s:Sector {sectorId: 'SECTOR-WATER'})
MERGE (r)-[:OPERATES_IN {
  primarySector: true
}]->(s);

MATCH (r:Region {regionId: 'REGION-RAIL-001'})
MATCH (s:Sector {sectorId: 'SECTOR-TRANSPORT'})
MERGE (r)-[:OPERATES_IN {
  primarySector: true
}]->(s);

// Customer → Sector (OPERATES_IN)
MATCH (c:Customer {customerId: 'CUSTOMER-UTILITY-001'})
MATCH (s:Sector {sectorId: 'SECTOR-ENERGY'})
MERGE (c)-[:OPERATES_IN {
  primarySector: true
}]->(s);

MATCH (c:Customer {customerId: 'CUSTOMER-WATER-001'})
MATCH (s:Sector {sectorId: 'SECTOR-WATER'})
MERGE (c)-[:OPERATES_IN {
  primarySector: true
}]->(s);

MATCH (c:Customer {customerId: 'CUSTOMER-RAILWAY-001'})
MATCH (s:Sector {sectorId: 'SECTOR-TRANSPORT'})
MERGE (c)-[:OPERATES_IN {
  primarySector: true
}]->(s);

// ───────────────────────────────────────────────────────────────
// VALIDATION - Verify Existing Schema Untouched
// ───────────────────────────────────────────────────────────────

// Verify existing Equipment nodes accessible
MATCH (eq:Equipment) RETURN count(eq) AS equipment_count;

// Verify existing CONNECTS_TO relationships intact
MATCH ()-[r:CONNECTS_TO]->() RETURN count(r) AS connects_to_count;

// Verify new organizational relationships created
MATCH ()-[r:OWNED_BY]->() RETURN count(r) AS owned_by_count;
MATCH ()-[r:IN_REGION]->() RETURN count(r) AS in_region_count;
MATCH ()-[r:OPERATES_IN]->() RETURN count(r) AS operates_in_count;

// ───────────────────────────────────────────────────────────────
// COMPLETION MESSAGE
// ───────────────────────────────────────────────────────────────

// Phase 2 Complete: Organizational relationships added
// Zero existing nodes/relationships/properties deleted
// Ready for Phase 3: Migrate Coordinates
