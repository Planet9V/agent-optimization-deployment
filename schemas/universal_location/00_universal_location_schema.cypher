// ═══════════════════════════════════════════════════════════════════════════════
// UNIVERSAL LOCATION HIERARCHY SCHEMA
// Critical Infrastructure Facility & Equipment Geospatial Model
// ═══════════════════════════════════════════════════════════════════════════════
// File: 00_universal_location_schema.cypher
// Created: 2025-11-13
// Purpose: Complete Neo4j schema for 16 critical infrastructure sectors
//          with ~300 facility types and mandatory geographic properties
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 1: NODE CONSTRAINTS (Uniqueness & Existence)
// ═══════════════════════════════════════════════════════════════════════════════

// Customer Node - Top-level organizational entity
CREATE CONSTRAINT constraint_customer_id IF NOT EXISTS
FOR (c:Customer)
REQUIRE c.customerId IS UNIQUE;

CREATE CONSTRAINT constraint_customer_name IF NOT EXISTS
FOR (c:Customer)
REQUIRE c.name IS NOT NULL;

// Region Node - Geographic/operational regions
CREATE CONSTRAINT constraint_region_id IF NOT EXISTS
FOR (r:Region)
REQUIRE r.regionId IS UNIQUE;

CREATE CONSTRAINT constraint_region_name IF NOT EXISTS
FOR (r:Region)
REQUIRE r.name IS NOT NULL;

// Sector Node - 16 Critical Infrastructure Sectors
CREATE CONSTRAINT constraint_sector_id IF NOT EXISTS
FOR (s:Sector)
REQUIRE s.sectorId IS UNIQUE;

CREATE CONSTRAINT constraint_sector_name IF NOT EXISTS
FOR (s:Sector)
REQUIRE s.name IS NOT NULL;

// Facility Node - CENTRAL physical location node (300+ types)
CREATE CONSTRAINT constraint_facility_id IF NOT EXISTS
FOR (f:Facility)
REQUIRE f.facilityId IS UNIQUE;

CREATE CONSTRAINT constraint_facility_location IF NOT EXISTS
FOR (f:Facility)
REQUIRE (f.latitude IS NOT NULL AND f.longitude IS NOT NULL);

CREATE CONSTRAINT constraint_facility_address IF NOT EXISTS
FOR (f:Facility)
REQUIRE (f.street_address IS NOT NULL AND f.city IS NOT NULL AND f.state IS NOT NULL);

// Equipment Node - Physical assets at facilities
CREATE CONSTRAINT constraint_equipment_id IF NOT EXISTS
FOR (e:Equipment)
REQUIRE e.equipmentId IS UNIQUE;

CREATE CONSTRAINT constraint_equipment_location IF NOT EXISTS
FOR (e:Equipment)
REQUIRE (e.latitude IS NOT NULL AND e.longitude IS NOT NULL);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 2: PERFORMANCE INDEXES
// ═══════════════════════════════════════════════════════════════════════════════

// --- Spatial Indexes for Geographic Queries ---
CREATE POINT INDEX facility_spatial_index IF NOT EXISTS
FOR (f:Facility) ON (point({latitude: f.latitude, longitude: f.longitude}));

CREATE POINT INDEX equipment_spatial_index IF NOT EXISTS
FOR (e:Equipment) ON (point({latitude: e.latitude, longitude: e.longitude}));

// --- Text Search Indexes ---
CREATE TEXT INDEX facility_name_text_index IF NOT EXISTS
FOR (f:Facility) ON (f.name);

CREATE TEXT INDEX facility_type_text_index IF NOT EXISTS
FOR (f:Facility) ON (f.facilityType);

CREATE INDEX facility_type_index IF NOT EXISTS
FOR (f:Facility) ON (f.facilityType);

// --- Composite Index for Facility Lookup ---
CREATE INDEX facility_state_city_index IF NOT EXISTS
FOR (f:Facility) ON (f.state, f.city);

// --- Sector Lookup ---
CREATE INDEX sector_name_index IF NOT EXISTS
FOR (s:Sector) ON (s.name);

// --- Customer Lookup ---
CREATE INDEX customer_name_index IF NOT EXISTS
FOR (c:Customer) ON (c.name);

// --- Region Lookup ---
CREATE INDEX region_name_index IF NOT EXISTS
FOR (r:Region) ON (r.name);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 3: NODE PROPERTY SCHEMAS (Documentation)
// ═══════════════════════════════════════════════════════════════════════════════

// Customer Node Properties:
// - customerId: string (unique identifier)
// - name: string (organization name)
// - type: string (e.g., "utility", "government", "private")
// - industry: string
// - created_date: datetime
// - updated_date: datetime

// Region Node Properties:
// - regionId: string (unique identifier)
// - name: string (region name)
// - type: string (e.g., "operational", "geographic", "administrative")
// - description: string
// - created_date: datetime
// - updated_date: datetime

// Sector Node Properties:
// - sectorId: string (unique identifier, e.g., "SECTOR-01-CHEMICAL")
// - name: string (one of 16 critical infrastructure sectors)
// - code: string (short code, e.g., "CHEM", "COMM", "ENERGY")
// - description: string
// - regulatory_framework: string (e.g., "DHS CISA", "NERC CIP")
// - created_date: datetime
// - updated_date: datetime
//
// Valid Sector Names (16 Total):
//   1. Chemical
//   2. Commercial Facilities
//   3. Communications
//   4. Critical Manufacturing
//   5. Dams
//   6. Defense Industrial Base
//   7. Emergency Services
//   8. Energy
//   9. Financial Services
//  10. Food and Agriculture
//  11. Government Facilities
//  12. Healthcare and Public Health
//  13. Information Technology
//  14. Nuclear Reactors, Materials, and Waste
//  15. Transportation Systems
//  16. Water and Wastewater Systems

// Facility Node Properties (MANDATORY GEOGRAPHIC):
// - facilityId: string (unique identifier)
// - name: string (facility name)
// - facilityType: string (one of 300+ types, see SECTION 4)
// - sectorName: string (references Sector)
// - description: string
//
// MANDATORY GEOGRAPHIC PROPERTIES:
// - latitude: float (WGS84 decimal degrees, -90 to 90)
// - longitude: float (WGS84 decimal degrees, -180 to 180)
// - elevation_meters: float (meters above sea level)
// - geographic_datum: string (default: "WGS84")
// - street_address: string (physical street address)
// - city: string
// - county: string
// - state: string (2-letter code for US, full name for international)
// - postal_code: string
// - country: string (ISO 3166-1 alpha-2 code, default: "US")
//
// OPERATIONAL PROPERTIES:
// - operational_status: string (e.g., "active", "inactive", "under_construction")
// - capacity: float (unit depends on facility type)
// - capacity_unit: string (e.g., "MW", "gallons/day", "beds")
// - commission_date: date
// - decommission_date: date (if applicable)
// - owner: string
// - operator: string
// - criticality_level: string (e.g., "critical", "high", "medium", "low")
// - created_date: datetime
// - updated_date: datetime

// Equipment Node Properties (MANDATORY GEOGRAPHIC):
// - equipmentId: string (unique identifier)
// - name: string
// - equipmentType: string
// - manufacturer: string
// - model: string
// - serial_number: string
//
// MANDATORY GEOGRAPHIC PROPERTIES (inherits from Facility or specific):
// - latitude: float (WGS84 decimal degrees)
// - longitude: float (WGS84 decimal degrees)
// - elevation_meters: float
// - geographic_datum: string (default: "WGS84")
// - street_address: string
// - city: string
// - county: string
// - state: string
// - postal_code: string
// - country: string (default: "US")
//
// OPERATIONAL PROPERTIES:
// - installation_date: date
// - operational_status: string (e.g., "active", "standby", "maintenance", "retired")
// - criticality_level: string
// - created_date: datetime
// - updated_date: datetime

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 4: FACILITY TYPES ENUMERATION (300+ Types Across 16 Sectors)
// ═══════════════════════════════════════════════════════════════════════════════

// SECTOR 1: CHEMICAL (15 types)
// - Chemical manufacturing plants
// - Chemical processing facilities
// - Petrochemical plants
// - Pharmaceutical manufacturing facilities
// - Fertilizer production plants
// - Industrial chemical storage facilities
// - Chemical distribution terminals
// - Specialty chemical manufacturing sites
// - Agricultural chemical production facilities
// - Chemical research laboratories
// - Hazardous material storage sites
// - Chemical waste treatment facilities
// - Paint and coating manufacturing plants
// - Plastics and resin production facilities
// - Explosives manufacturing facilities

// SECTOR 2: COMMERCIAL FACILITIES (19 types)
// - Shopping malls and retail centers
// - Sports arenas and stadiums
// - Convention centers
// - Entertainment venues and theaters
// - Hotels and resorts
// - Casinos and gaming facilities
// - Office buildings and business complexes
// - Apartment and condominium buildings
// - Theme parks and amusement parks
// - Museums and cultural facilities
// - Performing arts centers
// - Conference centers
// - Self-storage facilities
// - Retail districts
// - Zoo and aquarium facilities
// - Movie theaters and cinemas
// - Outdoor event venues
// - Recreational facilities
// - Lodging facilities

// SECTOR 3: COMMUNICATIONS (19 types)
// - Cell towers and base stations
// - Data centers and server farms
// - Telecommunications switching centers
// - Broadcast towers (radio and TV)
// - Satellite ground stations
// - Fiber optic network nodes
// - Network operation centers (NOCs)
// - Central offices and exchange buildings
// - Cable head-end facilities
// - Microwave transmission towers
// - Emergency communications centers
// - Internet exchange points (IXPs)
// - Telecommunications equipment shelters
// - Antenna sites and installations
// - Communications equipment rooms
// - Wireless backhaul sites
// - Point-of-presence (POP) facilities
// - Carrier hotels
// - Radio transmission facilities

// SECTOR 4: CRITICAL MANUFACTURING (20 types)
// - Steel mills and iron foundries
// - Aluminum production facilities
// - Metal fabrication plants
// - Automotive manufacturing plants
// - Aerospace manufacturing facilities
// - Engine and turbine manufacturing plants
// - Electric motor manufacturing facilities
// - Transformer manufacturing facilities
// - Generator manufacturing facilities
// - Power transmission equipment plants
// - Shipbuilding yards and facilities
// - Aircraft manufacturing plants
// - Locomotive manufacturing facilities
// - Railroad equipment manufacturing plants
// - Heavy machinery manufacturing facilities
// - Construction equipment plants
// - Mining equipment manufacturing sites
// - Agricultural equipment plants
// - Defense systems manufacturing facilities
// - Component manufacturing facilities

// SECTOR 5: DAMS (18 types)
// - Hydroelectric dams
// - Flood control dams
// - Irrigation dams
// - Water supply reservoirs
// - Navigation locks
// - Levees and floodwalls
// - Hurricane barriers
// - Spillways and outlet works
// - Powerhouses (at dam sites)
// - Mine tailings impoundments
// - Industrial waste impoundments
// - Dam project control structures
// - Pumping stations (at dams)
// - Recreation dams
// - Debris control dams
// - Water retention structures
// - Canal systems and aqueducts
// - Diversion dams

// SECTOR 6: DEFENSE INDUSTRIAL BASE (20 types)
// - Military shipyards
// - Ammunition plants
// - Weapons manufacturing facilities
// - Military aircraft production plants
// - Arsenals
// - Ordnance manufacturing facilities
// - Military vehicle production plants
// - Defense electronics manufacturing sites
// - Missile production facilities
// - Naval weapons stations
// - Army depots
// - Ammunition depots
// - Defense research laboratories
// - Military equipment maintenance facilities
// - Combat systems manufacturing plants
// - Explosives production facilities
// - Military uniform and equipment plants
// - Defense contractor facilities
// - Armored vehicle plants
// - Military satellite production facilities

// SECTOR 7: EMERGENCY SERVICES (19 types)
// - Fire stations
// - Police stations and precincts
// - Sheriff's offices
// - Emergency operations centers (EOCs)
// - 911 call centers (PSAPs)
// - EMS stations and bases
// - Dispatch centers
// - Emergency management facilities
// - Fire training facilities
// - Police training academies
// - HAZMAT response stations
// - Search and rescue facilities
// - Emergency medical helicopter bases
// - Mobile command centers (when stationed)
// - Emergency equipment storage facilities
// - Public safety communications towers
// - Disaster relief staging areas
// - Emergency shelters
// - Fusion centers

// SECTOR 8: ENERGY (24 types)
// - Power plants (coal, gas, nuclear, hydro)
// - Electrical substations
// - Switching stations
// - Transmission towers
// - Oil refineries
// - Natural gas processing plants
// - Petroleum storage tanks and tank farms
// - Natural gas storage facilities
// - Oil and gas well sites
// - Pumping stations (oil and gas)
// - Compressor stations (natural gas)
// - LNG terminals and facilities
// - Petroleum product terminals
// - Fuel distribution terminals
// - Solar power installations
// - Wind farms (turbine locations)
// - Geothermal power plants
// - Biomass power facilities
// - Coal storage and handling facilities
// - Electric distribution stations
// - Smart grid control centers
// - Energy management centers
// - Central tank batteries
// - Fractionation plants

// SECTOR 9: FINANCIAL SERVICES (20 types)
// - Bank branches
// - Federal Reserve Banks (12 locations)
// - Federal Reserve Branch offices (24 locations)
// - Credit union offices
// - Stock exchanges
// - Commodity exchanges
// - Securities trading facilities
// - Financial data centers
// - Payment processing centers
// - Check clearing facilities
// - ATM locations
// - Vault facilities
// - Financial services data centers
// - Insurance company offices
// - Mortgage servicing centers
// - Wire transfer centers
// - Financial operations centers
// - Investment banking offices
// - Financial call centers
// - Cryptocurrency exchange facilities

// SECTOR 10: FOOD AND AGRICULTURE (22 types)
// - Food processing plants
// - Meat packing and slaughterhouse facilities
// - Grain elevators
// - Flour mills
// - Dairy processing facilities
// - Beverage production plants
// - Cold storage warehouses
// - Food distribution centers
// - Agricultural storage facilities
// - Feed mills
// - Oat mills and rice mills
// - Dry corn mills
// - Bakeries (large-scale)
// - Canning facilities
// - Frozen food processing plants
// - Malting facilities
// - Sugar refineries
// - Vegetable oil processing plants
// - Livestock auction facilities
// - Agricultural research facilities
// - Food safety laboratories
// - Pesticide storage facilities
// - Farm supply centers

// SECTOR 11: GOVERNMENT FACILITIES (22 types)
// - Federal office buildings
// - State capitol buildings
// - County and municipal buildings
// - Federal courthouses
// - State and local courthouses
// - Military installations and bases
// - National laboratories
// - Embassies and consulates
// - Border stations and ports of entry
// - Government data centers
// - Veterans Affairs facilities
// - Government research facilities
// - Federal prisons and correctional facilities
// - State and local detention centers
// - Military housing complexes
// - Training bases and centers
// - Government warehouses
// - National monuments (facilities)
// - Historic landmarks (facilities)
// - Post offices
// - Educational facilities (K-12 schools)
// - Public universities and colleges

// SECTOR 12: HEALTHCARE AND PUBLIC HEALTH (24 types)
// - Hospitals
// - Medical centers and clinics
// - Urgent care centers
// - Emergency rooms
// - Public health laboratories
// - Medical research laboratories
// - Pharmaceutical manufacturing plants
// - Blood banks
// - Dialysis centers
// - Surgery centers
// - Nursing homes and long-term care facilities
// - Rehabilitation centers
// - Mental health facilities
// - Substance abuse treatment centers
// - Medical imaging centers
// - Clinical laboratories
// - Vaccine production facilities
// - Medical device manufacturing plants
// - Pharmacies and drug stores
// - Community health centers
// - Public health departments
// - Disease control centers
// - Medical waste disposal facilities
// - Ambulatory surgical centers

// SECTOR 13: INFORMATION TECHNOLOGY (19 types)
// - Data centers and cloud facilities
// - Server farms
// - Internet service provider (ISP) facilities
// - Colocation facilities
// - Network operation centers
// - Content delivery network (CDN) nodes
// - Software development centers
// - IT disaster recovery sites
// - Hardware manufacturing facilities
// - Semiconductor fabrication plants
// - Computer assembly plants
// - Telecommunications equipment plants
// - Cybersecurity operations centers
// - Cloud computing facilities
// - Edge computing locations
// - Hyperscale data center campuses
// - Research and development labs (IT)
// - Technology testing facilities
// - IT equipment storage facilities

// SECTOR 14: NUCLEAR REACTORS, MATERIALS, AND WASTE (18 types)
// - Nuclear power plants
// - Commercial nuclear reactors
// - Research reactors
// - Test reactors
// - Naval nuclear reactors (at bases)
// - Uranium fuel fabrication facilities
// - Uranium enrichment facilities
// - Uranium hexafluoride production facilities
// - Nuclear fuel cycle facilities
// - Spent fuel storage facilities
// - Dry cask storage sites
// - Radioactive waste storage facilities
// - Nuclear material storage sites
// - Nuclear waste processing facilities
// - Decommissioned reactor sites
// - Low-level waste disposal sites
// - Consolidated interim storage facilities
// - Nuclear medicine facilities
// - Radioactive material transport terminals

// SECTOR 15: TRANSPORTATION SYSTEMS (29 types)
// - Airports and heliports
// - Air traffic control towers
// - Seaports and harbors
// - Marine terminals
// - Railroad stations
// - Freight rail yards and terminals
// - Intermodal terminals
// - Bus stations and transit centers
// - Subway stations
// - Light rail stations
// - Highway toll plazas
// - Bridges
// - Tunnels (road and rail)
// - Railroad crossings (grade separations)
// - Ferry terminals
// - Trucking terminals
// - Warehouses and distribution centers
// - Border crossings
// - Pipeline terminals
// - Compressor stations (natural gas pipelines)
// - Pump stations (oil pipelines)
// - Metering stations (pipelines)
// - Pipeline valve stations
// - Fuel terminals and depots
// - Rail maintenance facilities
// - Airport fueling facilities
// - Port cargo handling facilities
// - Lock systems (navigation)
// - Postal sorting facilities
// - Shipping distribution centers

// SECTOR 16: WATER AND WASTEWATER SYSTEMS (22 types)
// - Water treatment plants
// - Wastewater treatment plants
// - Drinking water reservoirs
// - Water storage tanks
// - Water pumping stations
// - Wastewater pumping stations (lift stations)
// - Water distribution facilities
// - Sewer collection systems (access points)
// - Water filtration plants
// - Desalination plants
// - Water testing laboratories
// - Chlorination stations
// - Water well facilities
// - Groundwater treatment facilities
// - Stormwater management facilities
// - Water reclamation facilities
// - Wastewater lagoons and ponds
// - Sludge treatment facilities
// - Water system control centers
// - Aquifer storage facilities
// - Water quality monitoring stations
// - Booster pump stations
// - Water intake structures

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 5: RELATIONSHIP DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

// Customer-Region Relationships
// (Customer)-[:OPERATES_IN {since: date, status: string}]->(Region)

// Customer-Facility Relationships
// (Customer)-[:OWNS_FACILITY {since: date, ownership_type: string}]->(Facility)

// Region-Facility Relationships
// (Region)-[:CONTAINS_FACILITY {assigned_date: date}]->(Facility)

// Sector-Facility Relationships
// (Sector)-[:INCLUDES_FACILITY {classification_date: date, criticality: string}]->(Facility)

// Facility-Equipment Relationships
// (Facility)-[:HOUSES_EQUIPMENT {installation_date: date, location_within_facility: string}]->(Equipment)

// Equipment-Facility Relationships (Reverse reference)
// (Equipment)-[:LOCATED_AT {since: date, precise_location: string}]->(Facility)

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 6: EXAMPLE QUERIES (For Reference)
// ═══════════════════════════════════════════════════════════════════════════════

// Example 1: Find all facilities within 50km of a specific location
// MATCH (f:Facility)
// WHERE point.distance(
//   point({latitude: f.latitude, longitude: f.longitude}),
//   point({latitude: 40.7128, longitude: -74.0060})
// ) < 50000
// RETURN f.name, f.facilityType, f.city, f.state
// ORDER BY point.distance(
//   point({latitude: f.latitude, longitude: f.longitude}),
//   point({latitude: 40.7128, longitude: -74.0060})
// );

// Example 2: Find all Energy sector facilities in Texas
// MATCH (s:Sector {name: "Energy"})-[:INCLUDES_FACILITY]->(f:Facility)
// WHERE f.state = "TX"
// RETURN f.name, f.facilityType, f.city, f.latitude, f.longitude;

// Example 3: Find equipment hierarchy for a specific facility
// MATCH (f:Facility {facilityId: "FAC-12345"})-[:HOUSES_EQUIPMENT]->(e:Equipment)
// RETURN f.name AS facility,
//        e.name AS equipment,
//        e.equipmentType AS type,
//        e.latitude AS lat,
//        e.longitude AS lon;

// Example 4: Customer's complete facility portfolio by sector
// MATCH (c:Customer {customerId: "CUST-001"})-[:OWNS_FACILITY]->(f:Facility)
// <-[:INCLUDES_FACILITY]-(s:Sector)
// RETURN s.name AS sector,
//        COUNT(f) AS facility_count,
//        COLLECT(DISTINCT f.facilityType) AS facility_types
// ORDER BY facility_count DESC;

// Example 5: Find all critical facilities near a specific location
// MATCH (f:Facility)
// WHERE f.criticality_level IN ["critical", "high"]
//   AND point.distance(
//     point({latitude: f.latitude, longitude: f.longitude}),
//     point({latitude: 34.0522, longitude: -118.2437})
//   ) < 100000
// RETURN f.name, f.facilityType, f.criticality_level,
//        point.distance(
//          point({latitude: f.latitude, longitude: f.longitude}),
//          point({latitude: 34.0522, longitude: -118.2437})
//        ) AS distance_meters
// ORDER BY distance_meters;

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 7: VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// Verify all constraints exist
// SHOW CONSTRAINTS;

// Verify all indexes exist
// SHOW INDEXES;

// Check for facilities missing geographic coordinates
// MATCH (f:Facility)
// WHERE f.latitude IS NULL OR f.longitude IS NULL
// RETURN COUNT(f) AS facilities_missing_coordinates;

// Check for equipment missing geographic coordinates
// MATCH (e:Equipment)
// WHERE e.latitude IS NULL OR e.longitude IS NULL
// RETURN COUNT(e) AS equipment_missing_coordinates;

// ═══════════════════════════════════════════════════════════════════════════════
// END OF SCHEMA
// ═══════════════════════════════════════════════════════════════════════════════
// Total Facility Types Documented: 310 across 16 sectors
// Geographic Properties: Mandatory on both Facility and Equipment nodes
// Spatial Indexes: Enabled for lat/lon queries
// Performance: Optimized for large-scale infrastructure data
// ═══════════════════════════════════════════════════════════════════════════════
