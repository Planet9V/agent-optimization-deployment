// ═══════════════════════════════════════════════════════════════════════════════
// PHASE 4 FIX: COMPREHENSIVE TAGGING SYSTEM
// ═══════════════════════════════════════════════════════════════════════════════
// File: PHASE4_FIX_tagging.cypher
// Created: 2025-11-13
// Purpose: Add 5-dimensional tags to all nodes and compute inherited_tags
// Strategy: Use SET for tag addition, proper WHERE for matching, inheritance computation
// ═══════════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// STEP 1: TAG FACILITIES (GEO_*, OPS_*, REG_*, TECH_*)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize tags array for all Facilities if not exists
MATCH (f:Facility)
WHERE f.tags IS NULL
SET f.tags = [];

// Add Geographic tags based on location
MATCH (f:Facility)
WHERE f.latitude IS NOT NULL
WITH f,
     CASE
       WHEN f.latitude > 35 THEN 'GEO_cold_climate'
       WHEN f.latitude < 32 THEN 'GEO_hot_climate'
       ELSE 'GEO_moderate_climate'
     END AS climate_tag,
     CASE
       WHEN f.state IN ['CA', 'TX', 'NY', 'FL'] THEN 'GEO_high_density'
       ELSE 'GEO_medium_density'
     END AS density_tag
SET f.tags = f.tags + [climate_tag, density_tag];

// Add hazard zone tags
MATCH (f:Facility)
WHERE f.state IN ['CA', 'FL', 'TX', 'LA', 'MS', 'AL']
WITH f,
     CASE
       WHEN f.state = 'CA' THEN 'GEO_seismic_zone'
       WHEN f.state IN ['FL', 'LA', 'MS', 'AL'] THEN 'GEO_hurricane_zone'
       WHEN f.state = 'TX' THEN 'GEO_extreme_weather'
       ELSE 'GEO_moderate_hazard'
     END AS hazard_tag
SET f.tags = f.tags + [hazard_tag];

// Add Operational tags based on voltage level
MATCH (f:Facility)
WHERE f.voltage_level IS NOT NULL
WITH f,
     CASE
       WHEN f.voltage_level >= 345 THEN 'OPS_high_voltage'
       WHEN f.voltage_level >= 115 THEN 'OPS_medium_voltage'
       ELSE 'OPS_low_voltage'
     END AS voltage_tag,
     COALESCE(f.operational_status, 'active') AS status
SET f.tags = f.tags + [voltage_tag, 'OPS_status_' + status, 'OPS_utility_owned'];

// Add Regulatory tags (all facilities get base compliance tags)
MATCH (f:Facility)
WITH f,
     CASE
       WHEN f.voltage_level >= 200 THEN ['REG_NERC_CIP_critical', 'REG_IEC_62443_level3', 'REG_FERC_compliance']
       WHEN f.voltage_level >= 100 THEN ['REG_NERC_CIP_medium', 'REG_IEC_62443_level2', 'REG_FERC_compliance']
       ELSE ['REG_NERC_CIP_low', 'REG_IEC_62443_level1']
     END AS reg_tags
SET f.tags = f.tags + reg_tags;

// Add Technical tags based on facility type
MATCH (f:Facility)
WHERE f.facility_type IS NOT NULL
WITH f,
     CASE
       WHEN f.facility_type = 'substation' THEN ['TECH_substation', 'TECH_scada_enabled', 'TECH_ethernet_connected']
       WHEN f.facility_type = 'generation' THEN ['TECH_generation', 'TECH_scada_enabled', 'TECH_modbus_protocol']
       WHEN f.facility_type = 'transmission' THEN ['TECH_transmission', 'TECH_scada_enabled', 'TECH_dnp3_protocol']
       ELSE ['TECH_distribution', 'TECH_basic_monitoring']
     END AS tech_tags
SET f.tags = f.tags + tech_tags;

// Add Temporal tags based on commissioning date (if available)
MATCH (f:Facility)
WITH f,
     CASE
       WHEN f.commissioned_date IS NOT NULL AND f.commissioned_date > '2015-01-01' THEN 'TIME_modern_era'
       WHEN f.commissioned_date IS NOT NULL AND f.commissioned_date > '2000-01-01' THEN 'TIME_digital_era'
       WHEN f.commissioned_date IS NOT NULL AND f.commissioned_date > '1980-01-01' THEN 'TIME_legacy_era'
       ELSE 'TIME_historic_era'
     END AS era_tag
SET f.tags = f.tags + [era_tag, 'TIME_quarterly_maintenance'];

// ─────────────────────────────────────────────────────────────────────────────
// STEP 2: TAG REGIONS (GEO_*, REG_*)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize tags for Regions
MATCH (r:Region)
WHERE r.tags IS NULL
SET r.tags = [];

// Add geographic and regulatory tags to each Region
MATCH (r:Region)
WITH r,
     CASE
       WHEN r.name = 'North Region' THEN ['GEO_cold_climate', 'GEO_seismic_zone', 'REG_NERC_CIP_critical', 'REG_state_PUC_oversight', 'GEO_high_renewable']
       WHEN r.name = 'South Region' THEN ['GEO_hot_climate', 'GEO_hurricane_zone', 'REG_NERC_CIP_medium', 'REG_state_PUC_oversight', 'GEO_high_solar']
       WHEN r.name = 'Central Region' THEN ['GEO_moderate_climate', 'GEO_tornado_zone', 'REG_NERC_CIP_medium', 'REG_state_PUC_oversight', 'GEO_wind_corridor']
       ELSE ['GEO_moderate_climate', 'REG_NERC_CIP_low']
     END AS region_tags
SET r.tags = r.tags + region_tags;

// ─────────────────────────────────────────────────────────────────────────────
// STEP 3: TAG CUSTOMERS (OPS_*, REG_*)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize tags for Customers
MATCH (c:Customer)
WHERE c.tags IS NULL
SET c.tags = [];

// Add operational and regulatory tags based on customer type
MATCH (c:Customer)
WITH c,
     CASE
       WHEN c.customer_type = 'commercial' THEN ['OPS_commercial', 'OPS_peak_demand', 'REG_demand_response', 'REG_net_metering', 'OPS_load_management']
       WHEN c.customer_type = 'industrial' THEN ['OPS_industrial', 'OPS_high_load', 'REG_demand_response', 'REG_power_quality', 'OPS_critical_load', 'REG_EPA_reporting']
       WHEN c.customer_type = 'residential' THEN ['OPS_residential', 'OPS_standard_load', 'REG_consumer_protection', 'REG_net_metering', 'OPS_variable_load']
       ELSE ['OPS_standard', 'REG_basic_compliance']
     END AS customer_tags
SET c.tags = c.tags + customer_tags;

// Add load profile tags
MATCH (c:Customer)
WHERE c.peak_demand_kw IS NOT NULL
WITH c,
     CASE
       WHEN c.peak_demand_kw > 500 THEN 'OPS_large_load'
       WHEN c.peak_demand_kw > 100 THEN 'OPS_medium_load'
       ELSE 'OPS_small_load'
     END AS load_tag
SET c.tags = c.tags + [load_tag];

// ─────────────────────────────────────────────────────────────────────────────
// STEP 4: TAG SECTORS (SECTOR_*, REG_*)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize tags for Sectors
MATCH (s:Sector)
WHERE s.tags IS NULL
SET s.tags = [];

// Add sector-specific tags
MATCH (s:Sector)
WITH s,
     CASE
       WHEN s.name = 'Healthcare' THEN ['SECTOR_healthcare', 'REG_HIPAA_compliance', 'OPS_critical_infrastructure', 'REG_backup_power_required', 'OPS_24x7_operation', 'REG_emergency_priority', 'TECH_UPS_required']
       WHEN s.name = 'Education' THEN ['SECTOR_education', 'REG_state_oversight', 'OPS_seasonal_demand', 'REG_energy_efficiency', 'OPS_daytime_peak', 'TECH_smart_building', 'REG_renewable_incentive']
       WHEN s.name = 'Manufacturing' THEN ['SECTOR_manufacturing', 'REG_EPA_compliance', 'OPS_high_power_quality', 'REG_demand_charge', 'OPS_continuous_operation', 'TECH_power_monitoring', 'REG_pollution_control']
       ELSE ['SECTOR_general', 'REG_basic_compliance']
     END AS sector_tags
SET s.tags = s.tags + sector_tags;

// ─────────────────────────────────────────────────────────────────────────────
// STEP 5: COMPUTE INHERITED_TAGS FOR EQUIPMENT
// ─────────────────────────────────────────────────────────────────────────────

// Compute inherited_tags from Facility, Region, Customer, Sector
MATCH (e:Equipment)
OPTIONAL MATCH (e)-[:LOCATED_AT]->(f:Facility)
OPTIONAL MATCH (e)-[:IN_REGION]->(r:Region)
OPTIONAL MATCH (e)-[:SERVES]->(c:Customer)
OPTIONAL MATCH (c)-[:BELONGS_TO]->(s:Sector)
WITH e,
     COALESCE(f.tags, []) AS facility_tags,
     COALESCE(r.tags, []) AS region_tags,
     COALESCE(c.tags, []) AS customer_tags,
     COALESCE(s.tags, []) AS sector_tags
SET e.inherited_tags = facility_tags + region_tags + customer_tags + sector_tags;

// ─────────────────────────────────────────────────────────────────────────────
// STEP 6: VALIDATION QUERIES
// ─────────────────────────────────────────────────────────────────────────────

// Count Facilities with tags
MATCH (f:Facility)
WHERE f.tags IS NOT NULL AND size(f.tags) > 0
RETURN 'Facilities with tags' AS type, count(f) AS count, avg(size(f.tags)) AS avg_tags;

// Count Regions with tags
MATCH (r:Region)
WHERE r.tags IS NOT NULL AND size(r.tags) > 0
RETURN 'Regions with tags' AS type, count(r) AS count, avg(size(r.tags)) AS avg_tags;

// Count Customers with tags
MATCH (c:Customer)
WHERE c.tags IS NOT NULL AND size(c.tags) > 0
RETURN 'Customers with tags' AS type, count(c) AS count, avg(size(c.tags)) AS avg_tags;

// Count Sectors with tags
MATCH (s:Sector)
WHERE s.tags IS NOT NULL AND size(s.tags) > 0
RETURN 'Sectors with tags' AS type, count(s) AS count, avg(size(s.tags)) AS avg_tags;

// Count Equipment with inherited_tags
MATCH (e:Equipment)
WHERE e.inherited_tags IS NOT NULL AND size(e.inherited_tags) > 0
RETURN 'Equipment with inherited_tags' AS type, count(e) AS count, avg(size(e.inherited_tags)) AS avg_tags;

// Sample Equipment showing tag inheritance
MATCH (e:Equipment)
WHERE size(e.inherited_tags) > 0
RETURN e.name AS equipment,
       size(e.inherited_tags) AS tag_count,
       e.inherited_tags AS tags
LIMIT 5;
