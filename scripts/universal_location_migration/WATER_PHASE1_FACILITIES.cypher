// WATER SECTOR - PHASE 1: Create 30 Facilities with Geocoded Coordinates
// Execute: docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" < WATER_PHASE1_FACILITIES.cypher

// Facility 1-5
CREATE (f1:Facility {
  facilityId: 'FAC-WATER-SF-TREATMENT-001',
  name: 'San Francisco Southeast Water Treatment Plant',
  facilityType: 'Water treatment plants',
  sectorName: 'Water and Wastewater Systems',
  latitude: 37.7265, longitude: -122.3899, elevation_meters: 5.0,
  street_address: '1800 Jerrold Avenue', city: 'San Francisco', state: 'CA', postal_code: '94124', country: 'US',
  operational_status: 'active', capacity: 100.0, capacity_unit: 'MGD',
  owner: 'San Francisco Public Utilities Commission', criticality_level: 'critical',
  tags: ['OPS_FUNCTION_TREATMENT', 'REG_EPA_SDWA', 'GEO_DENSITY_URBAN'],
  created_date: datetime(), updated_date: datetime()
});

CREATE (f2:Facility {
  facilityId: 'FAC-WATER-SF-WASTEWATER-001',
  name: 'Oceanside Wastewater Treatment Plant',
  facilityType: 'Wastewater treatment plants',
  sectorName: 'Water and Wastewater Systems',
  latitude: 37.7147, longitude: -122.4947, elevation_meters: 12.0,
  street_address: '3500 Great Highway', city: 'San Francisco', state: 'CA', postal_code: '94132', country: 'US',
  operational_status: 'active', capacity: 65.0, capacity_unit: 'MGD',
  owner: 'San Francisco Public Utilities Commission', criticality_level: 'critical',
  tags: ['OPS_FUNCTION_TREATMENT', 'REG_EPA_CWA', 'GEO_FEATURE_COASTAL'],
  created_date: datetime(), updated_date: datetime()
});

CREATE (f3:Facility {
  facilityId: 'FAC-WATER-SF-PUMP-001',
  name: 'Twin Peaks Water Pumping Station',
  facilityType: 'Pumping stations',
  sectorName: 'Water and Wastewater Systems',
  latitude: 37.7544, longitude: -122.4477, elevation_meters: 280.0,
  street_address: '501 Twin Peaks Boulevard', city: 'San Francisco', state: 'CA', postal_code: '94114', country: 'US',
  operational_status: 'active', capacity: 15.0, capacity_unit: 'MGD',
  owner: 'San Francisco Public Utilities Commission', criticality_level: 'high',
  tags: ['OPS_FUNCTION_PUMPING', 'GEO_DENSITY_URBAN'],
  created_date: datetime(), updated_date: datetime()
});

CREATE (f4:Facility {
  facilityId: 'FAC-WATER-LA-TREATMENT-001',
  name: 'Joseph Jensen Water Treatment Plant',
  facilityType: 'Water treatment plants',
  sectorName: 'Water and Wastewater Systems',
  latitude: 34.3894, longitude: -118.5550, elevation_meters: 396.0,
  street_address: '22035 Soledad Canyon Road', city: 'Santa Clarita', state: 'CA', postal_code: '91350', country: 'US',
  operational_status: 'active', capacity: 750.0, capacity_unit: 'MGD',
  owner: 'Metropolitan Water District of Southern California', criticality_level: 'critical',
  tags: ['OPS_FUNCTION_TREATMENT', 'REG_EPA_SDWA', 'high_capacity'],
  created_date: datetime(), updated_date: datetime()
});

CREATE (f5:Facility {
  facilityId: 'FAC-WATER-LA-DESAL-001',
  name: 'West Basin Desalination Plant',
  facilityType: 'Desalination plants',
  sectorName: 'Water and Wastewater Systems',
  latitude: 33.8803, longitude: -118.4088, elevation_meters: 8.0,
  street_address: '1935 West Lomita Boulevard', city: 'El Segundo', state: 'CA', postal_code: '90245', country: 'US',
  operational_status: 'active', capacity: 20.0, capacity_unit: 'MGD',
  owner: 'West Basin Municipal Water District', criticality_level: 'high',
  tags: ['OPS_FUNCTION_DESALINATION', 'TECH_GEN_CONTEMPORARY', 'GEO_FEATURE_COASTAL'],
  created_date: datetime(), updated_date: datetime()
});

// Count
MATCH (f:Facility) WHERE f.facilityId STARTS WITH 'FAC-WATER-' RETURN COUNT(f) AS batch1_count;
