// ═══════════════════════════════════════════════════════════════════════════
// UNIVERSAL LOCATION TAGGING ARCHITECTURE
// Multi-Dimensional Hierarchical Tag System with Inheritance
// ═══════════════════════════════════════════════════════════════════════════
// File: 02_tagging_architecture.cypher
// Created: 2025-11-13
// Purpose: Region/Customer/Sector tagging with property propagation
// Dependencies: 01_core_schema.cypher
// Status: ACTIVE
// ═══════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════
// 1. REGION NODE SCHEMA - Geographic/Political Boundaries
// ═══════════════════════════════════════════════════════════════════════════

// Region Node Definition
// Represents geographic, political, utility territory, or market boundaries
// Supports hierarchical nesting (e.g., Panhandle → Texas → USA → North America)

CREATE CONSTRAINT region_id_unique IF NOT EXISTS
FOR (r:Region) REQUIRE r.regionId IS UNIQUE;

// Example: Texas Panhandle Region
CREATE (panhandle:Region {
  regionId: 'REGION_US_TX_PANHANDLE',
  name: 'Texas Panhandle',
  region_type: 'geographic',  // geographic, political, utility_territory, market, climate_zone
  parent_region: 'REGION_US_TX',  // Hierarchical nesting
  country: 'USA',
  state: 'Texas',
  county: null,  // Multi-county region
  bounding_box: {
    north_lat: 36.5,
    south_lat: 34.0,
    west_lon: -103.0,
    east_lon: -100.0
  },
  population_density: 'sparse',  // sparse, moderate, dense, urban
  climate_zone: 'semi_arid',
  grid_operator: 'ERCOT',
  utility_territories: ['Xcel Energy', 'Southwestern Public Service'],
  tags: [
    'ercot',
    'xcel_territory',
    'sparse_grid',
    'wind_resource_zone',
    'rural',
    'agriculture',
    'high_wind_exposure'
  ],
  metadata: {
    total_area_sq_km: 65000,
    major_cities: ['Amarillo', 'Lubbock', 'Pampa'],
    transmission_corridors: ['345kV_Panhandle_to_DFW', 'Hartley_to_Tolk'],
    renewable_capacity_mw: 8500,
    peak_demand_mw: 3200
  },
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Example: Parent Texas Region
CREATE (texas:Region {
  regionId: 'REGION_US_TX',
  name: 'Texas',
  region_type: 'political',
  parent_region: 'REGION_US',
  country: 'USA',
  state: 'Texas',
  bounding_box: {
    north_lat: 36.5,
    south_lat: 25.8,
    west_lon: -106.6,
    east_lon: -93.5
  },
  grid_operator: 'ERCOT',
  tags: [
    'ercot',
    'independent_grid',
    'deregulated_market',
    'renewable_leader',
    'oil_gas_hub'
  ],
  metadata: {
    total_area_sq_km: 695662,
    population: 30000000,
    installed_generation_gw: 140,
    renewable_percentage: 0.28
  },
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Hierarchical Region Relationship
CREATE (panhandle)-[:BELONGS_TO_REGION {
  relationship_type: 'geographic_containment',
  inheritance_enabled: true
}]->(texas);

// ═══════════════════════════════════════════════════════════════════════════
// 2. SECTOR NODE SCHEMA - Critical Infrastructure Classification
// ═══════════════════════════════════════════════════════════════════════════

// Sector Node Definition
// Based on CISA Critical Infrastructure Sectors (16 sectors)
// Defines regulatory frameworks, subsectors, and security requirements

CREATE CONSTRAINT sector_id_unique IF NOT EXISTS
FOR (s:Sector) REQUIRE s.sectorId IS UNIQUE;

// Example: Energy Sector
CREATE (energy:Sector {
  sectorId: 'SECTOR_ENERGY',
  name: 'Energy',
  cisa_designation: 'Critical Infrastructure Sector',
  sector_number: 3,  // CISA numbering
  description: 'Electricity generation, transmission, distribution; oil & gas production, refining, distribution',
  subsectors: [
    'Electric Grid',
    'Oil & Gas Production',
    'Oil & Gas Refining',
    'Natural Gas Distribution',
    'Renewable Energy',
    'Nuclear Power'
  ],
  regulatory_framework: [
    'NERC CIP',  // North American Electric Reliability Corporation Critical Infrastructure Protection
    'DOE',       // Department of Energy
    'FERC',      // Federal Energy Regulatory Commission
    'NRC',       // Nuclear Regulatory Commission
    'TSA',       // Transportation Security Administration (pipelines)
    'PHMSA'      // Pipeline and Hazardous Materials Safety Administration
  ],
  security_standards: [
    'NERC CIP-002 through CIP-014',
    'IEC 62443',  // Industrial cybersecurity
    'NIST Cybersecurity Framework',
    'ISA/IEC 62443-3-3',  // System security requirements
    'IEEE 1686'  // Substation intelligent electronic devices
  ],
  interdependencies: [
    'SECTOR_WATER',          // Cooling systems, hydroelectric
    'SECTOR_COMMUNICATIONS', // SCADA networks
    'SECTOR_TRANSPORTATION', // Fuel delivery
    'SECTOR_CHEMICAL'        // Emissions control
  ],
  tags: [
    'critical',
    'regulated',
    'national_security',
    'cyber_physical',
    'high_consequence',
    'nerc_registered',
    'essential_service'
  ],
  risk_profile: {
    cyber_threat_level: 'critical',
    physical_threat_level: 'high',
    climate_vulnerability: 'high',
    single_point_failure_risk: 'high'
  },
  metadata: {
    total_us_facilities: 55000,
    workforce_size: 1800000,
    gdp_contribution_pct: 0.08,
    foreign_ownership_restrictions: true
  },
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Example: Water Sector (for interdependency demonstration)
CREATE (water:Sector {
  sectorId: 'SECTOR_WATER',
  name: 'Water and Wastewater Systems',
  cisa_designation: 'Critical Infrastructure Sector',
  sector_number: 16,
  subsectors: [
    'Drinking Water',
    'Wastewater Treatment',
    'Stormwater Management'
  ],
  regulatory_framework: ['EPA', 'SDWA', 'CWA'],
  tags: ['critical', 'regulated', 'essential_service', 'environmental'],
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Sector Interdependency Relationship
CREATE (energy)-[:INTERDEPENDENT_WITH {
  dependency_type: 'bidirectional',
  criticality: 'high',
  description: 'Energy facilities require water for cooling; water systems require energy for pumping and treatment'
}]->(water);

// ═══════════════════════════════════════════════════════════════════════════
// 3. CUSTOMER NODE SCHEMA - Ownership/Operational Entities
// ═══════════════════════════════════════════════════════════════════════════

// Customer Node Definition
// Represents utilities, government agencies, private operators, corporate entities
// Links to regions, sectors, and owned facilities

CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer) REQUIRE c.customerId IS UNIQUE;

// Example: Xcel Energy (Investor-Owned Utility)
CREATE (xcel:Customer {
  customerId: 'CUSTOMER_XCEL_ENERGY',
  name: 'Xcel Energy',
  customer_type: 'investor_owned_utility',  // utility_operator, government, private_operator, public_power, cooperative
  parent_organization: 'Xcel Energy Inc.',
  ownership_structure: 'publicly_traded',  // publicly_traded, municipal, cooperative, federal, state, private
  stock_ticker: 'XEL',
  operating_regions: [
    'REGION_US_TX_PANHANDLE',
    'REGION_US_CO',
    'REGION_US_MN',
    'REGION_US_WI',
    'REGION_US_NM',
    'REGION_US_SD',
    'REGION_US_ND',
    'REGION_US_MI'
  ],
  sectors_served: ['SECTOR_ENERGY'],
  grid_operators: ['ERCOT', 'SPP', 'MISO'],  // ERCOT, SPP (Southwest Power Pool), MISO (Midcontinent ISO)
  service_territory: {
    customers_served: 3700000,
    states: 8,
    service_area_sq_km: 1500000
  },
  generation_portfolio: {
    total_capacity_mw: 19500,
    coal_mw: 4200,
    natural_gas_mw: 7800,
    nuclear_mw: 1700,
    wind_mw: 4500,
    solar_mw: 1000,
    hydro_mw: 300,
    renewable_percentage: 0.30
  },
  regulatory_compliance: {
    nerc_registration_id: 'NCR01163',
    ferc_regulated: true,
    state_puc_oversight: ['Texas PUC', 'Colorado PUC', 'Minnesota PUC'],
    nerc_cip_compliance: true,
    tsa_pipeline_oversight: false
  },
  tags: [
    'investor_owned_utility',
    'ercot_member',
    'nerc_registered',
    'multi_state_operator',
    'renewable_transition',
    'critical_infrastructure_owner',
    'publicly_traded',
    'ferc_regulated'
  ],
  contact_info: {
    headquarters: 'Minneapolis, MN',
    emergency_contact: '1-800-895-1999',
    regional_office_tx: 'Amarillo, TX',
    website: 'xcelenergy.com'
  },
  metadata: {
    founded_year: 2000,  // Merger of Northern States Power and New Century Energies
    employees: 11000,
    annual_revenue_usd: 13500000000,
    credit_rating: 'A-',
    climate_commitments: ['Carbon-free electricity by 2050', '80% reduction by 2030']
  },
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Example: Oncor Electric Delivery (Texas Transmission & Distribution Utility)
CREATE (oncor:Customer {
  customerId: 'CUSTOMER_ONCOR',
  name: 'Oncor Electric Delivery',
  customer_type: 'transmission_distribution_utility',
  parent_organization: 'Sempra Energy',
  ownership_structure: 'investor_owned',
  operating_regions: ['REGION_US_TX_NORTH', 'REGION_US_TX_CENTRAL', 'REGION_US_TX_WEST'],
  sectors_served: ['SECTOR_ENERGY'],
  grid_operators: ['ERCOT'],
  service_territory: {
    customers_served: 10000000,
    states: 1,
    service_area_sq_km: 300000
  },
  regulatory_compliance: {
    nerc_registration_id: 'NCR01234',
    ferc_regulated: false,  // Texas intrastate, not interstate commerce
    state_puc_oversight: ['Texas PUC'],
    nerc_cip_compliance: true
  },
  tags: [
    'transmission_operator',
    'distribution_operator',
    'ercot_member',
    'nerc_registered',
    'texas_only',
    'wires_only',  // Does not generate or sell electricity
    'largest_texas_tdsp'
  ],
  metadata: {
    transmission_lines_miles: 19000,
    distribution_lines_miles: 140000,
    substations: 750
  },
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Customer-Region Relationship
CREATE (xcel)-[:OPERATES_IN_REGION {
  service_type: 'full_service',  // full_service, transmission_only, distribution_only
  market_share_pct: 0.85,
  primary_operator: true
}]->(panhandle);

// Customer-Sector Relationship
CREATE (xcel)-[:OPERATES_IN_SECTOR {
  primary_sector: true,
  regulatory_status: 'compliant',
  certification_date: date('2024-01-01')
}]->(energy);

// ═══════════════════════════════════════════════════════════════════════════
// 4. TAG INHERITANCE RULES - Property Propagation Logic
// ═══════════════════════════════════════════════════════════════════════════

// Tag Inheritance Hierarchy:
// Equipment → Facility → Region + Customer + Sector
//
// Equipment inherits tags from:
// 1. Facility (direct container) - LOCATION tags
// 2. Region (geographic context) - GEOGRAPHIC tags
// 3. Customer (ownership context) - OPERATIONAL tags
// 4. Sector (infrastructure classification) - REGULATORY tags
//
// Inheritance Priority (highest to lowest):
// 1. Equipment-specific tags (explicit overrides)
// 2. Facility tags (operational context)
// 3. Customer tags (ownership/responsibility)
// 4. Sector tags (regulatory/classification)
// 5. Region tags (geographic/environmental)

// ─────────────────────────────────────────────────────────────────────────────
// 4.1 Facility Tag Inheritance Schema
// ─────────────────────────────────────────────────────────────────────────────

// Facility inherits from:
// - Region (via LOCATED_IN relationship)
// - Customer (via OWNS_FACILITY relationship)
// - Sector (via BELONGS_TO_SECTOR relationship)

// Example Query: Get all inherited tags for a Facility
// MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
// OPTIONAL MATCH (f)-[:LOCATED_IN]->(r:Region)
// OPTIONAL MATCH (c:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// RETURN f.facilityId AS facility,
//        f.tags AS facility_tags,
//        r.tags AS region_tags,
//        c.tags AS customer_tags,
//        s.tags AS sector_tags,
//        f.tags + COALESCE(r.tags, []) + COALESCE(c.tags, []) + COALESCE(s.tags, []) AS all_inherited_tags;

// ─────────────────────────────────────────────────────────────────────────────
// 4.2 Equipment Tag Inheritance Schema
// ─────────────────────────────────────────────────────────────────────────────

// Equipment inherits from:
// - Facility (via LOCATED_AT relationship)
// - Region (via Facility → LOCATED_IN)
// - Customer (via Facility ← OWNS_FACILITY)
// - Sector (via Facility → BELONGS_TO_SECTOR)

// Example: Equipment at Xcel Hitchland Substation inherits:
// - Facility tags: ['transmission', '345kv', 'critical_node', 'unmanned', 'outdoor']
// - Region tags: ['ercot', 'xcel_territory', 'sparse_grid', 'wind_resource_zone', 'rural']
// - Customer tags: ['investor_owned_utility', 'ercot_member', 'nerc_registered', 'multi_state_operator']
// - Sector tags: ['critical', 'regulated', 'national_security', 'cyber_physical', 'nerc_registered']

// Example Query: Get full tag inheritance chain for Equipment
// MATCH (eq:Equipment {equipmentId: 'EQ_XCEL_HITCH_TX_345_1'})
// MATCH (eq)-[:LOCATED_AT]->(f:Facility)
// OPTIONAL MATCH (f)-[:LOCATED_IN]->(r:Region)
// OPTIONAL MATCH (c:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WITH eq, f, r, c, s,
//      eq.tags AS eq_tags,
//      f.tags AS fac_tags,
//      COALESCE(r.tags, []) AS reg_tags,
//      COALESCE(c.tags, []) AS cust_tags,
//      COALESCE(s.tags, []) AS sect_tags
// RETURN eq.equipmentId,
//        eq_tags AS equipment_specific,
//        fac_tags AS from_facility,
//        reg_tags AS from_region,
//        cust_tags AS from_customer,
//        sect_tags AS from_sector,
//        eq_tags + fac_tags + reg_tags + cust_tags + sect_tags AS all_tags_merged;

// ─────────────────────────────────────────────────────────────────────────────
// 4.3 Tag Deduplication and Conflict Resolution
// ─────────────────────────────────────────────────────────────────────────────

// Deduplication Rule: Use DISTINCT to remove duplicate tags from inheritance chain
// Conflict Resolution: Equipment-specific tags override inherited tags

// Example: Equipment has explicit tag 'maintenance_exempt', facility has 'maintenance_required'
// Resolution: Equipment tag wins (equipment_specific > facility)

// Query with deduplication:
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)-[:LOCATED_IN]->(r:Region)
// MATCH (f)<-[:OWNS_FACILITY]-(c:Customer)
// MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WITH eq,
//      REDUCE(tags = [], tag_list IN [eq.tags, f.tags, r.tags, c.tags, s.tags] |
//        tags + [t IN tag_list WHERE NOT t IN tags]
//      ) AS deduplicated_tags
// RETURN eq.equipmentId, deduplicated_tags;

// ═══════════════════════════════════════════════════════════════════════════
// 5. MULTI-DIMENSIONAL TAGGING TAXONOMY
// ═══════════════════════════════════════════════════════════════════════════

// Tag Namespace Convention: [DIMENSION]_[CATEGORY]_[VALUE]
// Example: 'GEO_CLIMATE_SEMI_ARID', 'REG_NERC_CIP_002', 'OPS_VOLTAGE_345KV'

// ─────────────────────────────────────────────────────────────────────────────
// 5.1 Geographic Dimension (GEO_*)
// ─────────────────────────────────────────────────────────────────────────────
// Inherited from: Region nodes

// Climate tags:
// - GEO_CLIMATE_TROPICAL
// - GEO_CLIMATE_ARID
// - GEO_CLIMATE_SEMI_ARID
// - GEO_CLIMATE_TEMPERATE
// - GEO_CLIMATE_CONTINENTAL
// - GEO_CLIMATE_POLAR

// Population density tags:
// - GEO_DENSITY_SPARSE
// - GEO_DENSITY_MODERATE
// - GEO_DENSITY_DENSE
// - GEO_DENSITY_URBAN

// Geographic features:
// - GEO_FEATURE_COASTAL
// - GEO_FEATURE_MOUNTAIN
// - GEO_FEATURE_PLAINS
// - GEO_FEATURE_DESERT
// - GEO_FEATURE_WETLAND

// Natural hazard exposure:
// - GEO_HAZARD_HURRICANE
// - GEO_HAZARD_TORNADO
// - GEO_HAZARD_EARTHQUAKE
// - GEO_HAZARD_FLOOD
// - GEO_HAZARD_WILDFIRE
// - GEO_HAZARD_ICE_STORM

// ─────────────────────────────────────────────────────────────────────────────
// 5.2 Operational Dimension (OPS_*)
// ─────────────────────────────────────────────────────────────────────────────
// Inherited from: Customer nodes, Facility nodes

// Ownership type:
// - OPS_OWNER_IOU (Investor-Owned Utility)
// - OPS_OWNER_MUNI (Municipal)
// - OPS_OWNER_COOP (Cooperative)
// - OPS_OWNER_FEDERAL
// - OPS_OWNER_STATE
// - OPS_OWNER_PRIVATE

// Grid operator:
// - OPS_GRID_ERCOT
// - OPS_GRID_SPP
// - OPS_GRID_MISO
// - OPS_GRID_PJM
// - OPS_GRID_CAISO
// - OPS_GRID_NYISO
// - OPS_GRID_ISONE

// Voltage level:
// - OPS_VOLTAGE_765KV
// - OPS_VOLTAGE_500KV
// - OPS_VOLTAGE_345KV
// - OPS_VOLTAGE_230KV
// - OPS_VOLTAGE_138KV
// - OPS_VOLTAGE_69KV
// - OPS_VOLTAGE_34_5KV
// - OPS_VOLTAGE_12_47KV

// Function type:
// - OPS_FUNCTION_GENERATION
// - OPS_FUNCTION_TRANSMISSION
// - OPS_FUNCTION_DISTRIBUTION
// - OPS_FUNCTION_SUBSTATION
// - OPS_FUNCTION_INTERCONNECTION

// Operational status:
// - OPS_STATUS_ACTIVE
// - OPS_STATUS_STANDBY
// - OPS_STATUS_MAINTENANCE
// - OPS_STATUS_DECOMMISSIONED
// - OPS_STATUS_PLANNED

// ─────────────────────────────────────────────────────────────────────────────
// 5.3 Regulatory Dimension (REG_*)
// ─────────────────────────────────────────────────────────────────────────────
// Inherited from: Sector nodes, Customer nodes

// NERC CIP standards:
// - REG_NERC_CIP_002 (BES Cyber System Categorization)
// - REG_NERC_CIP_003 (Security Management Controls)
// - REG_NERC_CIP_004 (Personnel & Training)
// - REG_NERC_CIP_005 (Electronic Security Perimeter)
// - REG_NERC_CIP_006 (Physical Security)
// - REG_NERC_CIP_007 (System Security Management)
// - REG_NERC_CIP_008 (Incident Reporting)
// - REG_NERC_CIP_009 (Recovery Plans)
// - REG_NERC_CIP_010 (Configuration Change Management)
// - REG_NERC_CIP_011 (Information Protection)
// - REG_NERC_CIP_013 (Supply Chain Risk Management)
// - REG_NERC_CIP_014 (Physical Security - Transmission Stations)

// IEC 62443 security levels:
// - REG_IEC62443_SL1 (Protection against casual violation)
// - REG_IEC62443_SL2 (Protection against intentional violation using simple means)
// - REG_IEC62443_SL3 (Protection against intentional violation using sophisticated means)
// - REG_IEC62443_SL4 (Protection against intentional violation using sophisticated means with extended resources)

// FERC oversight:
// - REG_FERC_REGULATED
// - REG_FERC_EXEMPT

// State regulatory:
// - REG_STATE_PUC_TX
// - REG_STATE_PUC_CA
// - REG_STATE_PSC_NY

// ─────────────────────────────────────────────────────────────────────────────
// 5.4 Technical Dimension (TECH_*)
// ─────────────────────────────────────────────────────────────────────────────
// Inherited from: Equipment nodes, Facility nodes

// Equipment type:
// - TECH_EQUIP_TRANSFORMER
// - TECH_EQUIP_CIRCUIT_BREAKER
// - TECH_EQUIP_DISCONNECT_SWITCH
// - TECH_EQUIP_RELAY
// - TECH_EQUIP_CAPACITOR_BANK
// - TECH_EQUIP_REACTOR

// Technology generation:
// - TECH_GEN_LEGACY (Pre-2000)
// - TECH_GEN_MODERN (2000-2015)
// - TECH_GEN_CONTEMPORARY (2015-2025)
// - TECH_GEN_FUTURE (Post-2025)

// Communication protocol:
// - TECH_PROTO_DNP3
// - TECH_PROTO_MODBUS
// - TECH_PROTO_IEC61850
// - TECH_PROTO_GOOSE
// - TECH_PROTO_MMS

// Monitoring capability:
// - TECH_MON_SCADA
// - TECH_MON_PMU
// - TECH_MON_DFR
// - TECH_MON_RTU
// - TECH_MON_IED

// ─────────────────────────────────────────────────────────────────────────────
// 5.5 Temporal Dimension (TIME_*)
// ─────────────────────────────────────────────────────────────────────────────
// Inherited from: All nodes with temporal properties

// Commissioning era:
// - TIME_ERA_PRE_1950
// - TIME_ERA_1950_1979
// - TIME_ERA_1980_1999
// - TIME_ERA_2000_2014
// - TIME_ERA_2015_PRESENT

// Maintenance schedule:
// - TIME_MAINT_DAILY
// - TIME_MAINT_WEEKLY
// - TIME_MAINT_MONTHLY
// - TIME_MAINT_QUARTERLY
// - TIME_MAINT_ANNUAL
// - TIME_MAINT_BIENNIAL

// Inspection status:
// - TIME_INSPECT_CURRENT (Within schedule)
// - TIME_INSPECT_DUE (Due within 30 days)
// - TIME_INSPECT_OVERDUE (Past due date)
// - TIME_INSPECT_CRITICAL (Overdue >90 days)

// ═══════════════════════════════════════════════════════════════════════════
// 6. TAG QUERY OPTIMIZATION - Indexes and Full-Text Search
// ═══════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// 6.1 Standard Indexes on Tag Arrays
// ─────────────────────────────────────────────────────────────────────────────

CREATE INDEX facility_tags_idx IF NOT EXISTS
FOR (f:Facility) ON (f.tags);

CREATE INDEX equipment_tags_idx IF NOT EXISTS
FOR (eq:Equipment) ON (eq.tags);

CREATE INDEX region_tags_idx IF NOT EXISTS
FOR (r:Region) ON (r.tags);

CREATE INDEX customer_tags_idx IF NOT EXISTS
FOR (c:Customer) ON (c.tags);

CREATE INDEX sector_tags_idx IF NOT EXISTS
FOR (s:Sector) ON (s.tags);

// ─────────────────────────────────────────────────────────────────────────────
// 6.2 Full-Text Search Indexes for Tag Discovery
// ─────────────────────────────────────────────────────────────────────────────

CREATE FULLTEXT INDEX tag_fulltext_search IF NOT EXISTS
FOR (n:Facility|Equipment|Customer|Region|Sector)
ON EACH [n.tags];

// Example full-text search query:
// CALL db.index.fulltext.queryNodes('tag_fulltext_search', 'nerc AND critical')
// YIELD node, score
// RETURN node.name, labels(node), node.tags, score
// ORDER BY score DESC
// LIMIT 20;

// ─────────────────────────────────────────────────────────────────────────────
// 6.3 Composite Indexes for Multi-Dimensional Tag Queries
// ─────────────────────────────────────────────────────────────────────────────

// Index for Region + Customer tag combinations
CREATE INDEX region_customer_composite_idx IF NOT EXISTS
FOR (f:Facility) ON (f.region_id, f.customer_id, f.tags);

// Index for Voltage + Grid Operator combinations
CREATE INDEX voltage_grid_composite_idx IF NOT EXISTS
FOR (eq:Equipment) ON (eq.voltage_kv, eq.grid_operator, eq.tags);

// ─────────────────────────────────────────────────────────────────────────────
// 6.4 Performance-Optimized Tag Queries
// ─────────────────────────────────────────────────────────────────────────────

// Query 1: Find all NERC CIP-006 compliant facilities in ERCOT
// MATCH (f:Facility)-[:LOCATED_IN]->(r:Region)
// WHERE 'ercot' IN r.tags
//   AND ANY(tag IN f.tags WHERE tag STARTS WITH 'REG_NERC_CIP_006')
// RETURN f.facilityId, f.name, f.tags;

// Query 2: Find all 345kV equipment owned by investor-owned utilities
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)<-[:OWNS_FACILITY]-(c:Customer)
// WHERE 'OPS_VOLTAGE_345KV' IN eq.tags
//   AND 'OPS_OWNER_IOU' IN c.tags
// RETURN eq.equipmentId, f.name, c.name, eq.tags;

// Query 3: Find facilities in high-wind regions with renewable generation
// MATCH (f:Facility)-[:LOCATED_IN]->(r:Region)
// WHERE 'GEO_HAZARD_TORNADO' IN r.tags OR 'wind_resource_zone' IN r.tags
//   AND 'OPS_FUNCTION_GENERATION' IN f.tags
//   AND ANY(tag IN f.tags WHERE tag CONTAINS 'renewable')
// RETURN f.facilityId, f.name, r.name, f.tags;

// Query 4: Critical infrastructure requiring IEC 62443 SL3 or higher
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WHERE 'critical' IN s.tags
//   AND (ANY(tag IN eq.tags WHERE tag IN ['REG_IEC62443_SL3', 'REG_IEC62443_SL4'])
//        OR ANY(tag IN f.tags WHERE tag IN ['REG_IEC62443_SL3', 'REG_IEC62443_SL4']))
// RETURN eq.equipmentId, f.name, s.name, eq.tags + f.tags AS combined_tags;

// ═══════════════════════════════════════════════════════════════════════════
// 7. TAG INHERITANCE QUERY EXAMPLES - Practical Use Cases
// ═══════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// 7.1 Complete Tag Inheritance for Single Equipment
// ─────────────────────────────────────────────────────────────────────────────

// Query: Get full tag inheritance chain for transformer EQ_XCEL_HITCH_TX_345_1
// MATCH (eq:Equipment {equipmentId: 'EQ_XCEL_HITCH_TX_345_1'})
// MATCH (eq)-[:LOCATED_AT]->(f:Facility)
// OPTIONAL MATCH (f)-[:LOCATED_IN]->(r:Region)
// OPTIONAL MATCH (c:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WITH eq, f, r, c, s,
//      COALESCE(eq.tags, []) AS eq_tags,
//      COALESCE(f.tags, []) AS fac_tags,
//      COALESCE(r.tags, []) AS reg_tags,
//      COALESCE(c.tags, []) AS cust_tags,
//      COALESCE(s.tags, []) AS sect_tags
// RETURN {
//   equipment_id: eq.equipmentId,
//   equipment_name: eq.name,
//   tag_sources: {
//     equipment_specific: eq_tags,
//     from_facility: fac_tags,
//     from_region: reg_tags,
//     from_customer: cust_tags,
//     from_sector: sect_tags
//   },
//   all_tags_merged: eq_tags + fac_tags + reg_tags + cust_tags + sect_tags,
//   total_tag_count: SIZE(eq_tags + fac_tags + reg_tags + cust_tags + sect_tags)
// } AS tag_inheritance_report;

// ─────────────────────────────────────────────────────────────────────────────
// 7.2 Bulk Equipment Tag Inheritance (All equipment at a facility)
// ─────────────────────────────────────────────────────────────────────────────

// Query: Get tag inheritance for all equipment at Hitchland Substation
// MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f)
// OPTIONAL MATCH (f)-[:LOCATED_IN]->(r:Region)
// OPTIONAL MATCH (c:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WITH eq, f, r, c, s,
//      COALESCE(eq.tags, []) + COALESCE(f.tags, []) +
//      COALESCE(r.tags, []) + COALESCE(c.tags, []) +
//      COALESCE(s.tags, []) AS all_tags
// RETURN eq.equipmentId,
//        eq.name,
//        eq.equipment_type,
//        SIZE(all_tags) AS total_tags,
//        [tag IN all_tags WHERE tag STARTS WITH 'REG_'] AS regulatory_tags,
//        [tag IN all_tags WHERE tag STARTS WITH 'OPS_'] AS operational_tags
// ORDER BY SIZE(all_tags) DESC;

// ─────────────────────────────────────────────────────────────────────────────
// 7.3 Tag-Based Security Classification
// ─────────────────────────────────────────────────────────────────────────────

// Query: Find all equipment requiring NERC CIP compliance based on inherited tags
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
// OPTIONAL MATCH (f)-[:LOCATED_IN]->(r:Region)
// OPTIONAL MATCH (c:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WITH eq, f, c,
//      COALESCE(eq.tags, []) + COALESCE(f.tags, []) +
//      COALESCE(r.tags, []) + COALESCE(c.tags, []) +
//      COALESCE(s.tags, []) AS all_tags
// WHERE ANY(tag IN all_tags WHERE tag STARTS WITH 'REG_NERC_CIP')
// RETURN eq.equipmentId,
//        f.name AS facility_name,
//        c.name AS customer_name,
//        [tag IN all_tags WHERE tag STARTS WITH 'REG_NERC_CIP'] AS cip_requirements,
//        CASE
//          WHEN ANY(tag IN all_tags WHERE tag = 'REG_IEC62443_SL4') THEN 'Critical - SL4'
//          WHEN ANY(tag IN all_tags WHERE tag = 'REG_IEC62443_SL3') THEN 'High - SL3'
//          WHEN ANY(tag IN all_tags WHERE tag = 'REG_IEC62443_SL2') THEN 'Medium - SL2'
//          ELSE 'Standard - SL1'
//        END AS security_level
// ORDER BY security_level DESC;

// ─────────────────────────────────────────────────────────────────────────────
// 7.4 Geographic Risk Analysis Using Inherited Tags
// ─────────────────────────────────────────────────────────────────────────────

// Query: Identify critical equipment in high-hazard regions
// MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)-[:LOCATED_IN]->(r:Region)
// MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// WHERE 'critical' IN s.tags
//   AND (ANY(tag IN r.tags WHERE tag STARTS WITH 'GEO_HAZARD'))
// WITH eq, f, r, s,
//      [tag IN r.tags WHERE tag STARTS WITH 'GEO_HAZARD'] AS hazards,
//      COALESCE(eq.tags, []) + COALESCE(f.tags, []) + COALESCE(r.tags, []) AS all_tags
// RETURN eq.equipmentId,
//        f.name AS facility,
//        r.name AS region,
//        hazards AS natural_hazards,
//        CASE
//          WHEN 'GEO_HAZARD_HURRICANE' IN r.tags OR 'GEO_HAZARD_TORNADO' IN r.tags THEN 'High Wind Risk'
//          WHEN 'GEO_HAZARD_FLOOD' IN r.tags THEN 'Flood Risk'
//          WHEN 'GEO_HAZARD_WILDFIRE' IN r.tags THEN 'Fire Risk'
//          WHEN 'GEO_HAZARD_EARTHQUAKE' IN r.tags THEN 'Seismic Risk'
//          ELSE 'Multiple Hazards'
//        END AS primary_risk_category
// ORDER BY SIZE(hazards) DESC;

// ─────────────────────────────────────────────────────────────────────────────
// 7.5 Regulatory Compliance Audit by Tag Aggregation
// ─────────────────────────────────────────────────────────────────────────────

// Query: Generate compliance summary for all Xcel Energy facilities
// MATCH (c:Customer {customerId: 'CUSTOMER_XCEL_ENERGY'})-[:OWNS_FACILITY]->(f:Facility)
// MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector)
// OPTIONAL MATCH (eq:Equipment)-[:LOCATED_AT]->(f)
// WITH c, f, s, COLLECT(DISTINCT eq) AS equipment_list,
//      COALESCE(f.tags, []) + COALESCE(s.tags, []) AS facility_sector_tags
// RETURN c.name AS customer,
//        COUNT(DISTINCT f) AS total_facilities,
//        SIZE(equipment_list) AS total_equipment,
//        SIZE([tag IN facility_sector_tags WHERE tag STARTS WITH 'REG_NERC_CIP']) AS nerc_cip_facilities,
//        SIZE([tag IN facility_sector_tags WHERE tag STARTS WITH 'REG_IEC62443']) AS iec62443_facilities,
//        SIZE([tag IN facility_sector_tags WHERE tag = 'critical']) AS critical_infrastructure_count,
//        [tag IN facility_sector_tags WHERE tag STARTS WITH 'REG_'] AS all_regulatory_tags;

// ═══════════════════════════════════════════════════════════════════════════
// 8. TAG MAINTENANCE AND GOVERNANCE
// ═══════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// 8.1 Tag Validation Rules
// ─────────────────────────────────────────────────────────────────────────────

// Constraint: All tags must follow namespace convention [DIMENSION]_[CATEGORY]_[VALUE]
// Valid dimensions: GEO, OPS, REG, TECH, TIME
// Enforcement: Application-level validation before tag insertion

// Example validation function (pseudo-code):
// FUNCTION validate_tag(tag: String) -> Boolean:
//   valid_prefixes = ['GEO_', 'OPS_', 'REG_', 'TECH_', 'TIME_']
//   legacy_allowed = ['ercot', 'nerc_registered', 'critical', 'rural']  // Grandfather clause
//   RETURN tag STARTS WITH ANY(valid_prefixes) OR tag IN legacy_allowed

// ─────────────────────────────────────────────────────────────────────────────
// 8.2 Tag Deprecation and Migration
// ─────────────────────────────────────────────────────────────────────────────

// Query: Find all nodes using deprecated tag 'old_tag' and migrate to 'NEW_TAG'
// MATCH (n)
// WHERE 'old_tag' IN n.tags
// SET n.tags = [tag IN n.tags WHERE tag <> 'old_tag'] + ['NEW_TAG']
// RETURN COUNT(n) AS nodes_updated;

// ─────────────────────────────────────────────────────────────────────────────
// 8.3 Tag Usage Analytics
// ─────────────────────────────────────────────────────────────────────────────

// Query: Most frequently used tags across all nodes
// MATCH (n)
// WHERE n.tags IS NOT NULL
// UNWIND n.tags AS tag
// RETURN tag,
//        COUNT(*) AS usage_count,
//        COLLECT(DISTINCT labels(n)) AS node_types
// ORDER BY usage_count DESC
// LIMIT 50;

// Query: Identify orphaned tags (tags used on only 1-2 nodes)
// MATCH (n)
// WHERE n.tags IS NOT NULL
// UNWIND n.tags AS tag
// WITH tag, COUNT(*) AS usage_count
// WHERE usage_count <= 2
// RETURN tag, usage_count
// ORDER BY usage_count ASC;

// ═══════════════════════════════════════════════════════════════════════════
// 9. EXAMPLE DATA - Hitchland Substation Full Tag Inheritance
// ═══════════════════════════════════════════════════════════════════════════

// Create example Facility with all relationships for tag inheritance demonstration

CREATE (hitchland:Facility {
  facilityId: 'FAC_XCEL_HITCHLAND_SUB',
  name: 'Hitchland Substation',
  facility_type: 'transmission_substation',
  voltage_levels: [345.0, 138.0],
  gps_coordinates: {
    latitude: 35.4523,
    longitude: -101.8934,
    elevation_m: 1088
  },
  tags: [
    'OPS_FUNCTION_TRANSMISSION',
    'OPS_VOLTAGE_345KV',
    'OPS_VOLTAGE_138KV',
    'TECH_MON_SCADA',
    'REG_NERC_CIP_006',
    'critical_node',
    'unmanned',
    'outdoor'
  ],
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Link Hitchland to Panhandle Region
MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
MATCH (r:Region {regionId: 'REGION_US_TX_PANHANDLE'})
CREATE (f)-[:LOCATED_IN {
  relationship_type: 'geographic_containment',
  inheritance_enabled: true
}]->(r);

// Link Hitchland to Xcel Energy Customer
MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
MATCH (c:Customer {customerId: 'CUSTOMER_XCEL_ENERGY'})
CREATE (c)-[:OWNS_FACILITY {
  ownership_type: 'full_ownership',
  operational_control: true,
  inheritance_enabled: true
}]->(f);

// Link Hitchland to Energy Sector
MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
MATCH (s:Sector {sectorId: 'SECTOR_ENERGY'})
CREATE (f)-[:BELONGS_TO_SECTOR {
  primary_sector: true,
  inheritance_enabled: true
}]->(s);

// Create example Equipment at Hitchland
CREATE (transformer:Equipment {
  equipmentId: 'EQ_XCEL_HITCH_TX_345_1',
  name: 'Hitchland 345/138kV Transformer #1',
  equipment_type: 'power_transformer',
  manufacturer: 'ABB',
  model: 'GSU-345-300MVA',
  serial_number: 'ABB-TX-2018-45623',
  voltage_primary_kv: 345.0,
  voltage_secondary_kv: 138.0,
  rated_power_mva: 300.0,
  tags: [
    'TECH_EQUIP_TRANSFORMER',
    'TECH_GEN_CONTEMPORARY',
    'OPS_STATUS_ACTIVE',
    'REG_NERC_CIP_007',
    'high_voltage',
    'critical_asset'
  ],
  installation_date: date('2018-06-15'),
  last_inspection_date: date('2025-09-01'),
  next_maintenance_date: date('2026-06-15'),
  created_date: datetime('2025-11-13T00:00:00Z'),
  updated_date: datetime('2025-11-13T00:00:00Z')
});

// Link Equipment to Facility
MATCH (eq:Equipment {equipmentId: 'EQ_XCEL_HITCH_TX_345_1'})
MATCH (f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
CREATE (eq)-[:LOCATED_AT {
  bay_number: 'Bay 1',
  position: 'Primary',
  inheritance_enabled: true
}]->(f);

// ═══════════════════════════════════════════════════════════════════════════
// 10. VERIFICATION QUERY - Full Tag Inheritance Demo
// ═══════════════════════════════════════════════════════════════════════════

// Query to demonstrate complete tag inheritance for Hitchland Transformer
// RUN THIS QUERY TO VALIDATE TAG INHERITANCE ARCHITECTURE:

// MATCH (eq:Equipment {equipmentId: 'EQ_XCEL_HITCH_TX_345_1'})
// MATCH (eq)-[:LOCATED_AT]->(f:Facility {facilityId: 'FAC_XCEL_HITCHLAND_SUB'})
// MATCH (f)-[:LOCATED_IN]->(r:Region {regionId: 'REGION_US_TX_PANHANDLE'})
// MATCH (c:Customer {customerId: 'CUSTOMER_XCEL_ENERGY'})-[:OWNS_FACILITY]->(f)
// MATCH (f)-[:BELONGS_TO_SECTOR]->(s:Sector {sectorId: 'SECTOR_ENERGY'})
// RETURN {
//   equipment: {
//     id: eq.equipmentId,
//     name: eq.name,
//     type: eq.equipment_type,
//     specific_tags: eq.tags
//   },
//   facility: {
//     id: f.facilityId,
//     name: f.name,
//     tags: f.tags
//   },
//   region: {
//     id: r.regionId,
//     name: r.name,
//     tags: r.tags
//   },
//   customer: {
//     id: c.customerId,
//     name: c.name,
//     tags: c.tags
//   },
//   sector: {
//     id: s.sectorId,
//     name: s.name,
//     tags: s.tags
//   },
//   tag_inheritance_summary: {
//     equipment_specific: SIZE(eq.tags),
//     from_facility: SIZE(f.tags),
//     from_region: SIZE(r.tags),
//     from_customer: SIZE(c.tags),
//     from_sector: SIZE(s.tags),
//     total_inherited: SIZE(eq.tags + f.tags + r.tags + c.tags + s.tags),
//     all_tags_merged: eq.tags + f.tags + r.tags + c.tags + s.tags
//   }
// } AS complete_tag_inheritance;

// Expected Result:
// - Equipment-specific tags: 6 (TECH_EQUIP_TRANSFORMER, etc.)
// - Facility tags: 8 (OPS_FUNCTION_TRANSMISSION, etc.)
// - Region tags: 7 (ercot, xcel_territory, sparse_grid, etc.)
// - Customer tags: 8 (investor_owned_utility, ercot_member, etc.)
// - Sector tags: 7 (critical, regulated, national_security, etc.)
// - Total inherited tags: 36

// ═══════════════════════════════════════════════════════════════════════════
// END OF TAGGING ARCHITECTURE
// ═══════════════════════════════════════════════════════════════════════════
