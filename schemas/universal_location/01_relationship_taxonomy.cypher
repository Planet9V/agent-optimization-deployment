// ═══════════════════════════════════════════════════════════════════════════════
// UNIVERSAL LOCATION ARCHITECTURE - RELATIONSHIP TAXONOMY
// ═══════════════════════════════════════════════════════════════════════════════
// File: 01_relationship_taxonomy.cypher
// Created: 2025-01-13
// Version: v1.0.0
// Purpose: Standardized relationship vocabulary for universal location graph
// Status: ACTIVE
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP CATEGORY: OWNERSHIP RELATIONSHIPS
// Semantic Domain: Legal and operational control
// ═══════════════════════════════════════════════════════════════════════════════

// OWNS_FACILITY: Customer → Facility
// Semantic Definition: Legal ownership of facility asset
// Cardinality: One-to-Many (Customer can own multiple Facilities)
// Business Rule: Ownership implies legal responsibility and asset control
// Example: "Utility Company OWNS_FACILITY Power Plant A"
CREATE CONSTRAINT owns_facility_unique IF NOT EXISTS
FOR ()-[r:OWNS_FACILITY]-()
REQUIRE (r.relationship_type, r.established_date, r.verified) IS NOT NULL;

// Standard properties for OWNS_FACILITY
// {
//   relationship_type: "OWNS_FACILITY",
//   established_date: date("2024-01-15"),
//   verified: true,
//   confidence_score: 0.95,
//   source: "Corporate Registry",
//   ownership_percentage: 100.0,  // Additional property for partial ownership
//   legal_entity: "Primary owner legal name"
// }

// OWNS_EQUIPMENT: Customer → Equipment
// Semantic Definition: Legal ownership of equipment asset
// Cardinality: One-to-Many (Customer can own multiple Equipment items)
// Business Rule: Ownership implies maintenance responsibility and liability
// Example: "Utility Company OWNS_EQUIPMENT Transformer #12345"
CREATE CONSTRAINT owns_equipment_unique IF NOT EXISTS
FOR ()-[r:OWNS_EQUIPMENT]-()
REQUIRE (r.relationship_type, r.established_date, r.verified) IS NOT NULL;

// OPERATES: Customer → Facility
// Semantic Definition: Operational control without ownership
// Cardinality: One-to-Many
// Business Rule: Operations can exist without ownership (leased/contracted facilities)
// Distinction: OPERATES ≠ OWNS_FACILITY (can operate facilities owned by others)
// Example: "Company A OPERATES Facility X" while "Company B OWNS_FACILITY Facility X"
CREATE CONSTRAINT operates_unique IF NOT EXISTS
FOR ()-[r:OPERATES]-()
REQUIRE (r.relationship_type, r.verified) IS NOT NULL;

// Additional properties for OPERATES
// {
//   contract_start_date: date("2023-06-01"),
//   contract_end_date: date("2028-05-31"),
//   operational_scope: "Full operations and maintenance"
// }

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP CATEGORY: LOCATION RELATIONSHIPS
// Semantic Domain: Physical and geographic positioning
// ═══════════════════════════════════════════════════════════════════════════════

// LOCATED_AT: Equipment → Facility
// Semantic Definition: Physical containment of equipment within facility
// Cardinality: Many-to-One (Equipment must be at exactly one Facility)
// Business Rule: MANDATORY - Every Equipment node MUST have exactly one LOCATED_AT relationship
// Bidirectional Implication: If A LOCATED_AT B, then B HOUSES_EQUIPMENT A
// Example: "Transformer #12345 LOCATED_AT Substation Alpha"
CREATE CONSTRAINT located_at_mandatory IF NOT EXISTS
FOR (e:Equipment)
REQUIRE e.facility_id IS NOT NULL;

CREATE CONSTRAINT located_at_unique IF NOT EXISTS
FOR ()-[r:LOCATED_AT]-()
REQUIRE (r.relationship_type, r.verified) IS NOT NULL;

// Standard properties for LOCATED_AT
// {
//   relationship_type: "LOCATED_AT",
//   established_date: date("2023-03-15"),
//   verified: true,
//   confidence_score: 0.98,
//   source: "Asset Management System",
//   installation_date: date("2023-03-15"),
//   physical_location_detail: "Building 2, Floor 3, Room 301",
//   gps_coordinates: point({latitude: 40.7128, longitude: -74.0060})
// }

// LOCATED_IN: Facility → Region
// Semantic Definition: Geographic containment of facility within region
// Cardinality: Many-to-One (Facility must be in exactly one Region)
// Business Rule: Regional assignment for geographic aggregation and analysis
// Example: "Power Plant A LOCATED_IN Northeast Region"
CREATE CONSTRAINT located_in_unique IF NOT EXISTS
FOR ()-[r:LOCATED_IN]-()
REQUIRE (r.relationship_type, r.verified) IS NOT NULL;

// SITUATED_IN: Equipment → Region
// Semantic Definition: Derived geographic location from Facility.LOCATED_IN
// Cardinality: Many-to-One (derived relationship)
// Business Rule: DERIVED - Automatically inferred from Equipment.LOCATED_AT.Facility.LOCATED_IN
// Derivation Rule: Equipment -[:LOCATED_AT]-> Facility -[:LOCATED_IN]-> Region
// Example: "Transformer #12345 SITUATED_IN Northeast Region" (derived)
CREATE CONSTRAINT situated_in_derived IF NOT EXISTS
FOR ()-[r:SITUATED_IN]-()
REQUIRE (r.relationship_type, r.derived_from) IS NOT NULL;

// Additional properties for SITUATED_IN
// {
//   derived_from: ["LOCATED_AT", "LOCATED_IN"],
//   derivation_timestamp: datetime("2024-01-15T10:30:00Z")
// }

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP CATEGORY: HIERARCHICAL RELATIONSHIPS
// Semantic Domain: Containment and organizational structure
// ═══════════════════════════════════════════════════════════════════════════════

// CONTAINS_FACILITY: Region → Facility
// Semantic Definition: Region contains multiple facilities
// Cardinality: One-to-Many (Region contains many Facilities)
// Bidirectional Implication: Inverse of LOCATED_IN
// Business Rule: Used for regional aggregation and hierarchical queries
// Example: "Northeast Region CONTAINS_FACILITY Power Plant A"
CREATE CONSTRAINT contains_facility_unique IF NOT EXISTS
FOR ()-[r:CONTAINS_FACILITY]-()
REQUIRE (r.relationship_type) IS NOT NULL;

// HOUSES_EQUIPMENT: Facility → Equipment
// Semantic Definition: Facility contains equipment
// Cardinality: One-to-Many (Facility contains many Equipment items)
// Bidirectional Implication: Inverse of LOCATED_AT
// Business Rule: Used for facility inventory and capacity analysis
// Example: "Substation Alpha HOUSES_EQUIPMENT Transformer #12345"
CREATE CONSTRAINT houses_equipment_unique IF NOT EXISTS
FOR ()-[r:HOUSES_EQUIPMENT]-()
REQUIRE (r.relationship_type) IS NOT NULL;

// PART_OF_REGION: Facility → Region
// Semantic Definition: Facility belongs to region (synonym of LOCATED_IN)
// Cardinality: Many-to-One
// Business Rule: Alternative semantic for organizational hierarchy
// Usage Note: Prefer LOCATED_IN for geographic context, PART_OF_REGION for organizational context
// Example: "Power Plant A PART_OF_REGION Northeast Operating Division"
CREATE CONSTRAINT part_of_region_unique IF NOT EXISTS
FOR ()-[r:PART_OF_REGION]-()
REQUIRE (r.relationship_type) IS NOT NULL;

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP CATEGORY: ORGANIZATIONAL RELATIONSHIPS
// Semantic Domain: Business operations and service delivery
// ═══════════════════════════════════════════════════════════════════════════════

// OPERATES_IN: Customer → Region
// Semantic Definition: Customer has operational presence in region
// Cardinality: Many-to-Many (Customer can operate in multiple Regions)
// Business Rule: Indicates service area or operational jurisdiction
// Example: "Utility Company OPERATES_IN Northeast Region, Southeast Region"
CREATE CONSTRAINT operates_in_unique IF NOT EXISTS
FOR ()-[r:OPERATES_IN]-()
REQUIRE (r.relationship_type) IS NOT NULL;

// Additional properties for OPERATES_IN
// {
//   service_start_date: date("2020-01-01"),
//   service_type: "Electricity Distribution",
//   market_share: 65.5,  // Percentage
//   regulatory_authority: "State Public Utility Commission"
// }

// SERVES_CUSTOMER: Facility → Customer
// Semantic Definition: Facility serves customer operational needs
// Cardinality: Many-to-Many (Facility can serve multiple Customers)
// Business Rule: Service relationship independent of ownership
// Example: "Substation Alpha SERVES_CUSTOMER Utility Company A, Utility Company B"
CREATE CONSTRAINT serves_customer_unique IF NOT EXISTS
FOR ()-[r:SERVES_CUSTOMER]-()
REQUIRE (r.relationship_type) IS NOT NULL;

// BELONGS_TO_SECTOR: Facility → Sector
// Semantic Definition: Critical infrastructure sector classification
// Cardinality: Many-to-One (Facility belongs to one primary Sector)
// Business Rule: Based on CISA Critical Infrastructure Sectors
// Reference: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors
// Example: "Power Plant A BELONGS_TO_SECTOR Energy Sector"
CREATE CONSTRAINT belongs_to_sector_unique IF NOT EXISTS
FOR ()-[r:BELONGS_TO_SECTOR]-()
REQUIRE (r.relationship_type, r.sector_classification) IS NOT NULL;

// Standard properties for BELONGS_TO_SECTOR
// {
//   relationship_type: "BELONGS_TO_SECTOR",
//   sector_classification: "Energy",  // CISA sector
//   subsector: "Electric Power Generation",
//   criticality_level: "HIGH",  // HIGH, MEDIUM, LOW
//   verified: true,
//   confidence_score: 1.0,
//   source: "CISA Critical Infrastructure Registry"
// }

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP CATEGORY: CONNECTION RELATIONSHIPS
// Semantic Domain: Physical and logical interconnections
// ═══════════════════════════════════════════════════════════════════════════════

// CONNECTS_TO: Equipment → Equipment
// Semantic Definition: Physical or logical connection between equipment
// Cardinality: Many-to-Many (Equipment can connect to multiple Equipment)
// Business Rule: Represents network topology and dependencies
// Connection Types: Physical wire, logical network, control signal, power flow
// Example: "Circuit Breaker A CONNECTS_TO Transformer B"
CREATE CONSTRAINT connects_to_unique IF NOT EXISTS
FOR ()-[r:CONNECTS_TO]-()
REQUIRE (r.relationship_type, r.connection_type) IS NOT NULL;

// Standard properties for CONNECTS_TO
// {
//   relationship_type: "CONNECTS_TO",
//   connection_type: "PHYSICAL_WIRE",  // PHYSICAL_WIRE, LOGICAL_NETWORK, CONTROL_SIGNAL, POWER_FLOW
//   established_date: date("2023-05-20"),
//   verified: true,
//   confidence_score: 0.92,
//   source: "Network Topology System",
//   bandwidth_mbps: 1000.0,  // For network connections
//   voltage_kv: 115.0,  // For power connections
//   bidirectional: true,
//   connection_status: "ACTIVE"  // ACTIVE, INACTIVE, MAINTENANCE
// }

// CONNECTS_FACILITY: Facility → Facility
// Semantic Definition: Inter-facility connection (e.g., transmission lines)
// Cardinality: Many-to-Many (Facilities can interconnect)
// Business Rule: Represents facility-level network topology
// Example: "Power Plant A CONNECTS_FACILITY Substation B via 230kV Transmission Line"
CREATE CONSTRAINT connects_facility_unique IF NOT EXISTS
FOR ()-[r:CONNECTS_FACILITY]-()
REQUIRE (r.relationship_type, r.connection_type) IS NOT NULL;

// Additional properties for CONNECTS_FACILITY
// {
//   transmission_line_id: "TL-12345",
//   voltage_level_kv: 230.0,
//   capacity_mw: 500.0,
//   distance_km: 85.5,
//   connection_path: [point1, point2, ...]  // Geographic path
// }

// SUPPLIES_POWER_TO: Equipment → Facility
// Semantic Definition: Power supply chain relationship
// Cardinality: One-to-Many (Equipment can supply power to multiple Facilities)
// Business Rule: Represents energy flow and dependency chains
// Example: "Generator #1 SUPPLIES_POWER_TO Distribution Facility A"
CREATE CONSTRAINT supplies_power_to_unique IF NOT EXISTS
FOR ()-[r:SUPPLIES_POWER_TO]-()
REQUIRE (r.relationship_type, r.power_capacity_mw) IS NOT NULL;

// Standard properties for SUPPLIES_POWER_TO
// {
//   relationship_type: "SUPPLIES_POWER_TO",
//   established_date: date("2022-08-10"),
//   verified: true,
//   confidence_score: 0.95,
//   source: "Energy Management System",
//   power_capacity_mw: 250.0,
//   voltage_kv: 138.0,
//   reliability_percentage: 99.97,
//   backup_available: true,
//   supply_contract_end_date: date("2030-12-31")
// }

// ═══════════════════════════════════════════════════════════════════════════════
// SEMANTIC RULES AND BUSINESS LOGIC
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// RULE 1: MANDATORY RELATIONSHIPS
// ───────────────────────────────────────────────────────────────────────────────
// Every Equipment MUST have exactly one LOCATED_AT relationship to a Facility
// Enforcement: Database constraint and application-level validation
// Validation Query:
// MATCH (e:Equipment) WHERE NOT (e)-[:LOCATED_AT]->(:Facility) RETURN e
// Expected Result: Empty set (no orphaned equipment)

// ───────────────────────────────────────────────────────────────────────────────
// RULE 2: OWNERSHIP VS OPERATIONAL CONTROL
// ───────────────────────────────────────────────────────────────────────────────
// OWNS_FACILITY: Legal ownership with asset responsibility
// OPERATES: Operational control without ownership (leased, contracted)
// Business Logic: A Customer can OPERATE a Facility without OWNS_FACILITY
// Example Scenario: Customer A OWNS_FACILITY Plant X, Customer B OPERATES Plant X
// Validation: Both relationships can coexist for same Facility

// ───────────────────────────────────────────────────────────────────────────────
// RULE 3: BIDIRECTIONAL IMPLICATIONS
// ───────────────────────────────────────────────────────────────────────────────
// If Equipment A -[:LOCATED_AT]-> Facility B, then Facility B -[:HOUSES_EQUIPMENT]-> Equipment A
// If Facility X -[:LOCATED_IN]-> Region Y, then Region Y -[:CONTAINS_FACILITY]-> Facility X
// Enforcement: Symmetric relationship maintenance via triggers or application logic
// Sync Query Template:
// MATCH (a)-[r1:LOCATED_AT]->(b)
// WHERE NOT (b)-[:HOUSES_EQUIPMENT]->(a)
// CREATE (b)-[:HOUSES_EQUIPMENT {relationship_type: "HOUSES_EQUIPMENT",
//                                 derived_from: type(r1),
//                                 verified: r1.verified}]->(a)

// ───────────────────────────────────────────────────────────────────────────────
// RULE 4: DERIVED RELATIONSHIPS
// ───────────────────────────────────────────────────────────────────────────────
// SITUATED_IN is DERIVED from: Equipment -[:LOCATED_AT]-> Facility -[:LOCATED_IN]-> Region
// Derivation Logic:
// MATCH (e:Equipment)-[:LOCATED_AT]->(f:Facility)-[:LOCATED_IN]->(r:Region)
// CREATE (e)-[:SITUATED_IN {relationship_type: "SITUATED_IN",
//                           derived_from: ["LOCATED_AT", "LOCATED_IN"],
//                           derivation_timestamp: datetime(),
//                           verified: true,
//                           confidence_score: min(locatedAt.confidence_score, locatedIn.confidence_score),
//                           source: "DERIVED"}]->(r)

// ───────────────────────────────────────────────────────────────────────────────
// RULE 5: RELATIONSHIP PROPERTY STANDARDS
// ───────────────────────────────────────────────────────────────────────────────
// ALL relationships MUST include:
// - relationship_type: string (standardized name matching relationship type)
// - established_date: date (when relationship was created/discovered)
// - verified: boolean (data quality flag)
// - confidence_score: float 0.0-1.0 (data confidence level)
// - source: string (data source system/process)
//
// Confidence Score Interpretation:
// 0.90-1.00: High confidence (verified from authoritative source)
// 0.70-0.89: Medium confidence (inferred from reliable data)
// 0.50-0.69: Low confidence (derived or estimated)
// 0.00-0.49: Very low confidence (requires verification)

// ───────────────────────────────────────────────────────────────────────────────
// RULE 6: TEMPORAL CONSISTENCY
// ───────────────────────────────────────────────────────────────────────────────
// Relationship timestamps must be logically consistent:
// - Equipment.installation_date <= LOCATED_AT.established_date
// - OWNS_FACILITY.established_date <= OPERATES.contract_start_date (if both exist)
// - CONNECTS_TO.established_date <= current_date
//
// Validation Query:
// MATCH (e:Equipment)-[r:LOCATED_AT]->(f:Facility)
// WHERE e.installation_date > r.established_date
// RETURN e.equipment_id, e.installation_date, r.established_date

// ───────────────────────────────────────────────────────────────────────────────
// RULE 7: SECTOR CLASSIFICATION AUTHORITY
// ───────────────────────────────────────────────────────────────────────────────
// BELONGS_TO_SECTOR must reference CISA Critical Infrastructure Sectors:
// 1. Chemical Sector
// 2. Commercial Facilities Sector
// 3. Communications Sector
// 4. Critical Manufacturing Sector
// 5. Dams Sector
// 6. Defense Industrial Base Sector
// 7. Emergency Services Sector
// 8. Energy Sector
// 9. Financial Services Sector
// 10. Food and Agriculture Sector
// 11. Government Facilities Sector
// 12. Healthcare and Public Health Sector
// 13. Information Technology Sector
// 14. Nuclear Reactors, Materials, and Waste Sector
// 15. Transportation Systems Sector
// 16. Water and Wastewater Systems Sector
//
// Reference: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors

// ───────────────────────────────────────────────────────────────────────────────
// RULE 8: CONNECTION TYPE VALIDATION
// ───────────────────────────────────────────────────────────────────────────────
// CONNECTS_TO.connection_type must be one of:
// - PHYSICAL_WIRE: Physical electrical connection
// - LOGICAL_NETWORK: Network/communication connection
// - CONTROL_SIGNAL: Control system connection
// - POWER_FLOW: Electrical power flow path
//
// Validation ensures consistent connection classification

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP USAGE PATTERNS AND QUERY EXAMPLES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 1: Find all equipment at a facility
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (f:Facility {facility_name: "Substation Alpha"})-[:HOUSES_EQUIPMENT]->(e:Equipment)
// RETURN f.facility_name, collect(e.equipment_id) AS equipment_list

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 2: Find facility owner and operator
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (f:Facility {facility_id: "FAC-12345"})
// OPTIONAL MATCH (owner:Customer)-[:OWNS_FACILITY]->(f)
// OPTIONAL MATCH (operator:Customer)-[:OPERATES]->(f)
// RETURN f.facility_name, owner.customer_name AS owner, operator.customer_name AS operator

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 3: Equipment location hierarchy (Equipment → Facility → Region)
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (e:Equipment {equipment_id: "EQ-67890"})-[:LOCATED_AT]->(f:Facility)-[:LOCATED_IN]->(r:Region)
// RETURN e.equipment_id, f.facility_name, r.region_name

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 4: Find all equipment in a region (using derived relationship)
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (r:Region {region_name: "Northeast"})<-[:SITUATED_IN]-(e:Equipment)
// RETURN r.region_name, count(e) AS equipment_count, collect(e.equipment_type) AS equipment_types

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 5: Power supply chain
// ───────────────────────────────────────────────────────────────────────────────
// MATCH path = (gen:Equipment {equipment_type: "Generator"})-[:SUPPLIES_POWER_TO*]->(f:Facility)
// RETURN gen.equipment_id AS generator,
//        [node IN nodes(path) | node.facility_name] AS supply_chain,
//        length(path) AS chain_length

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 6: Facility network topology
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (f1:Facility)-[c:CONNECTS_FACILITY]->(f2:Facility)
// WHERE c.voltage_level_kv >= 230
// RETURN f1.facility_name, f2.facility_name, c.transmission_line_id, c.capacity_mw

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 7: Customer operational footprint
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (c:Customer {customer_name: "Utility Company A"})-[:OPERATES_IN]->(r:Region)
// MATCH (c)-[:OWNS_FACILITY]->(f:Facility)-[:LOCATED_IN]->(r)
// RETURN c.customer_name, r.region_name, count(f) AS facilities_in_region

// ───────────────────────────────────────────────────────────────────────────────
// PATTERN 8: Critical infrastructure by sector
// ───────────────────────────────────────────────────────────────────────────────
// MATCH (f:Facility)-[b:BELONGS_TO_SECTOR]->(s:Sector {sector_name: "Energy"})
// WHERE b.criticality_level = "HIGH"
// RETURN f.facility_name, b.subsector, f.location_coordinates

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP PROPERTY TEMPLATES
// ═══════════════════════════════════════════════════════════════════════════════

// Template for creating standardized relationships with all required properties:
/*
CREATE (a)-[r:RELATIONSHIP_TYPE {
  relationship_type: "RELATIONSHIP_TYPE",
  established_date: date("YYYY-MM-DD"),
  verified: true,
  confidence_score: 0.95,
  source: "Data Source Name",
  // Additional domain-specific properties...
}]->(b)
*/

// ═══════════════════════════════════════════════════════════════════════════════
// DATA QUALITY AND GOVERNANCE
// ═══════════════════════════════════════════════════════════════════════════════

// Confidence Score Calculation Guidelines:
// 1.00: Verified from authoritative source with cross-validation
// 0.95: Verified from authoritative source
// 0.90: Verified from reliable internal system
// 0.85: Derived from high-confidence relationships
// 0.75: Inferred from multiple data points
// 0.65: Derived from single data source
// 0.50: Estimated based on patterns
// <0.50: Requires manual verification before use

// Data Source Authority Hierarchy:
// Tier 1 (Highest): Corporate asset registry, regulatory filings, legal documents
// Tier 2: Enterprise asset management systems, SCADA systems
// Tier 3: Geographic information systems (GIS), network topology databases
// Tier 4: Derived/calculated relationships, third-party data sources
// Tier 5 (Lowest): Manual entry, estimated data

// ═══════════════════════════════════════════════════════════════════════════════
// VERSION HISTORY
// ═══════════════════════════════════════════════════════════════════════════════
// v1.0.0 (2025-01-13): Initial taxonomy creation
//   - 15 relationship types defined
//   - 5 relationship categories established
//   - 8 semantic rules documented
//   - Complete property templates and validation patterns
//   - Query examples and usage patterns
//
// ═══════════════════════════════════════════════════════════════════════════════
// END OF RELATIONSHIP TAXONOMY
// ═══════════════════════════════════════════════════════════════════════════════
