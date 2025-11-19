// ═══════════════════════════════════════════════════════════════════════════════
// PHASE 4 ACTUAL: COMPREHENSIVE TAGGING - WORKS WITH REAL DATA
// ═══════════════════════════════════════════════════════════════════════════════
// File: PHASE4_ACTUAL_tagging.cypher
// Created: 2025-11-13
// Purpose: Add 5-dimensional tags working with actual node properties
// Strategy: Work with existing data, add new tags alongside old ones
// ═══════════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// STEP 1: TAG FACILITIES (ALL 4 FACILITIES)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize new_tags array for all Facilities (keep old tags)
MATCH (f:Facility)
SET f.new_tags = COALESCE(f.new_tags, []);

// Add Geographic tags based on facility name/type
MATCH (f:Facility)
WITH f,
     CASE
       WHEN f.name CONTAINS 'Northeast' THEN ['GEO_northeast', 'GEO_cold_climate', 'GEO_high_density']
       WHEN f.name CONTAINS 'Pacific' THEN ['GEO_pacific', 'GEO_moderate_climate', 'GEO_seismic_zone']
       WHEN f.name CONTAINS 'Springfield' THEN ['GEO_midwest', 'GEO_moderate_climate', 'GEO_tornado_zone']
       WHEN f.name CONTAINS 'Railway' THEN ['GEO_regional', 'GEO_moderate_climate', 'GEO_distributed']
       ELSE ['GEO_general']
     END AS geo_tags
SET f.new_tags = f.new_tags + geo_tags;

// Add Operational tags based on facility type
MATCH (f:Facility)
WITH f,
     CASE
       WHEN f.name CONTAINS 'SCADA' OR f.name CONTAINS 'Control' THEN ['OPS_control_center', 'OPS_critical_ops', 'OPS_24x7', 'OPS_high_availability']
       WHEN f.name CONTAINS 'Substation' THEN ['OPS_substation', 'OPS_high_voltage', 'OPS_transmission', 'OPS_automated']
       WHEN f.name CONTAINS 'Water Treatment' THEN ['OPS_treatment_plant', 'OPS_continuous_operation', 'OPS_process_control', 'OPS_automated']
       WHEN f.name CONTAINS 'Railway' THEN ['OPS_rail_control', 'OPS_safety_critical', 'OPS_automated', 'OPS_real_time']
       ELSE ['OPS_general_facility']
     END AS ops_tags
SET f.new_tags = f.new_tags + ops_tags;

// Add Regulatory tags based on sector (from existing tags)
MATCH (f:Facility)
WITH f,
     CASE
       WHEN 'energy_sector' IN f.tags THEN ['REG_NERC_CIP_critical', 'REG_FERC_compliance', 'REG_IEC_62443_level3', 'REG_state_PUC']
       WHEN 'water_sector' IN f.tags THEN ['REG_EPA_compliance', 'REG_SDWA_compliance', 'REG_state_water_board', 'REG_IEC_62443_level2']
       WHEN 'transportation_sector' IN f.tags THEN ['REG_FRA_compliance', 'REG_safety_critical', 'REG_IEC_62443_level3', 'REG_state_DOT']
       ELSE ['REG_general_compliance']
     END AS reg_tags
SET f.new_tags = f.new_tags + reg_tags;

// Add Technical tags based on facility type
MATCH (f:Facility)
WITH f,
     CASE
       WHEN f.name CONTAINS 'SCADA' THEN ['TECH_scada_master', 'TECH_dnp3_protocol', 'TECH_ethernet_network', 'TECH_redundant_systems']
       WHEN f.name CONTAINS 'Substation' THEN ['TECH_scada_rtu', 'TECH_iec61850_protocol', 'TECH_fiber_optic', 'TECH_automated_switching']
       WHEN f.name CONTAINS 'Water' THEN ['TECH_scada_plc', 'TECH_modbus_protocol', 'TECH_wireless_sensors', 'TECH_process_monitoring']
       WHEN f.name CONTAINS 'Railway' THEN ['TECH_atc_system', 'TECH_proprietary_protocol', 'TECH_radio_network', 'TECH_gps_tracking']
       ELSE ['TECH_basic_monitoring']
     END AS tech_tags
SET f.new_tags = f.new_tags + tech_tags;

// Add Temporal tags (all facilities get maintenance schedules)
MATCH (f:Facility)
SET f.new_tags = f.new_tags + ['TIME_quarterly_maintenance', 'TIME_annual_audit', 'TIME_modern_era'];

// ─────────────────────────────────────────────────────────────────────────────
// STEP 2: TAG REGIONS (ACTUAL REGION NAMES)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize new_tags for Regions
MATCH (r:Region)
SET r.new_tags = COALESCE(r.new_tags, []);

// Add tags based on actual Region names
MATCH (r:Region)
WITH r,
     CASE
       WHEN r.name CONTAINS 'Northeast' THEN ['GEO_northeast', 'GEO_cold_climate', 'GEO_high_density', 'REG_NERC_CIP_critical', 'REG_ISO_New_England', 'GEO_coastal_zone']
       WHEN r.name CONTAINS 'Pacific' THEN ['GEO_pacific_coast', 'GEO_seismic_zone', 'GEO_moderate_climate', 'REG_state_water_board', 'REG_EPA_region10', 'GEO_water_rich']
       WHEN r.name CONTAINS 'Railway' OR r.name CONTAINS 'Region 001' THEN ['GEO_regional_corridor', 'GEO_transportation_hub', 'REG_FRA_compliance', 'REG_safety_critical', 'GEO_multi_state']
       ELSE ['GEO_general_region']
     END AS region_tags
SET r.new_tags = r.new_tags + region_tags;

// ─────────────────────────────────────────────────────────────────────────────
// STEP 3: TAG CUSTOMERS (BASED ON ACTUAL CUSTOMER DATA)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize new_tags for Customers
MATCH (c:Customer)
SET c.new_tags = COALESCE(c.new_tags, []);

// Add operational tags based on customer name/type
MATCH (c:Customer)
WITH c,
     CASE
       WHEN c.name CONTAINS 'Hospital' OR c.name CONTAINS 'Medical' THEN ['OPS_healthcare', 'OPS_critical_load', 'OPS_24x7', 'REG_HIPAA_compliance', 'REG_backup_power_required']
       WHEN c.name CONTAINS 'University' OR c.name CONTAINS 'School' THEN ['OPS_education', 'OPS_seasonal_demand', 'OPS_daytime_peak', 'REG_state_oversight', 'REG_energy_efficiency']
       WHEN c.name CONTAINS 'Factory' OR c.name CONTAINS 'Manufacturing' THEN ['OPS_industrial', 'OPS_high_load', 'OPS_continuous_operation', 'REG_EPA_compliance', 'REG_power_quality']
       WHEN c.name CONTAINS 'Office' THEN ['OPS_commercial', 'OPS_standard_load', 'OPS_weekday_peak', 'REG_building_codes', 'REG_energy_star']
       WHEN c.name CONTAINS 'Residential' OR c.name CONTAINS 'Apartment' THEN ['OPS_residential', 'OPS_variable_load', 'OPS_evening_peak', 'REG_consumer_protection', 'REG_net_metering']
       ELSE ['OPS_general_customer']
     END AS customer_tags
SET c.new_tags = c.new_tags + customer_tags;

// Add load profile tags
MATCH (c:Customer)
WHERE c.monthly_consumption_kwh IS NOT NULL
WITH c,
     CASE
       WHEN c.monthly_consumption_kwh > 100000 THEN 'OPS_large_load'
       WHEN c.monthly_consumption_kwh > 10000 THEN 'OPS_medium_load'
       ELSE 'OPS_small_load'
     END AS load_tag
SET c.new_tags = c.new_tags + [load_tag];

// ─────────────────────────────────────────────────────────────────────────────
// STEP 4: TAG SECTORS (USING ACTUAL SECTOR NAMES)
// ─────────────────────────────────────────────────────────────────────────────

// Initialize new_tags for Sectors
MATCH (s:Sector)
SET s.new_tags = COALESCE(s.new_tags, []);

// Add comprehensive tags for each actual Sector
MATCH (s:Sector)
WITH s,
     CASE
       WHEN s.name = 'Energy' THEN ['SECTOR_energy', 'REG_NERC_CIP', 'REG_FERC_compliance', 'OPS_critical_infrastructure', 'OPS_grid_operations', 'TECH_scada_systems', 'REG_environmental_permits']
       WHEN s.name = 'Water and Wastewater' THEN ['SECTOR_water', 'REG_EPA_compliance', 'REG_SDWA_compliance', 'OPS_treatment_operations', 'OPS_continuous_service', 'TECH_process_control', 'REG_discharge_permits']
       WHEN s.name = 'Transportation' THEN ['SECTOR_transportation', 'REG_FRA_compliance', 'REG_safety_critical', 'OPS_rail_operations', 'OPS_automated_control', 'TECH_atc_systems', 'REG_maintenance_standards']
       WHEN s.name = 'Healthcare and Public Health' THEN ['SECTOR_healthcare', 'REG_HIPAA_compliance', 'REG_emergency_priority', 'OPS_critical_services', 'OPS_backup_power', 'TECH_UPS_required', 'REG_accreditation']
       WHEN s.name = 'Critical Infrastructure' THEN ['SECTOR_critical_infra', 'REG_CISA_oversight', 'REG_security_clearance', 'OPS_national_security', 'OPS_redundancy_required', 'TECH_secure_communications', 'REG_incident_reporting']
       WHEN s.name = 'Education' THEN ['SECTOR_education', 'REG_state_oversight', 'REG_energy_efficiency', 'OPS_seasonal_operations', 'OPS_daytime_peak', 'TECH_smart_building', 'REG_renewable_incentives']
       WHEN s.name = 'Financial Services' THEN ['SECTOR_financial', 'REG_SOX_compliance', 'REG_data_protection', 'OPS_high_reliability', 'OPS_disaster_recovery', 'TECH_redundant_power', 'REG_business_continuity']
       WHEN s.name = 'Manufacturing' THEN ['SECTOR_manufacturing', 'REG_EPA_compliance', 'REG_OSHA_standards', 'OPS_industrial_load', 'OPS_power_quality', 'TECH_power_monitoring', 'REG_pollution_control']
       WHEN s.name = 'Technology' THEN ['SECTOR_technology', 'REG_data_center_standards', 'REG_energy_efficiency', 'OPS_high_density', 'OPS_cooling_critical', 'TECH_UPS_systems', 'REG_uptime_requirements']
       WHEN s.name = 'Legal and Professional Services' THEN ['SECTOR_professional', 'REG_data_protection', 'REG_building_codes', 'OPS_office_load', 'OPS_weekday_operations', 'TECH_standard_systems', 'REG_business_licensing']
       WHEN s.name = 'State and Local Government' THEN ['SECTOR_government', 'REG_public_sector', 'REG_transparency_requirements', 'OPS_public_services', 'OPS_standard_hours', 'TECH_government_networks', 'REG_procurement_rules']
       ELSE ['SECTOR_general']
     END AS sector_tags
SET s.new_tags = s.new_tags + sector_tags;

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
     COALESCE(f.new_tags, []) AS facility_tags,
     COALESCE(r.new_tags, []) AS region_tags,
     COALESCE(c.new_tags, []) AS customer_tags,
     COALESCE(s.new_tags, []) AS sector_tags
SET e.inherited_tags = facility_tags + region_tags + customer_tags + sector_tags;

// ─────────────────────────────────────────────────────────────────────────────
// STEP 6: VALIDATION QUERIES
// ─────────────────────────────────────────────────────────────────────────────

// Count Facilities with new_tags
MATCH (f:Facility)
WHERE f.new_tags IS NOT NULL AND size(f.new_tags) > 0
RETURN 'Facilities with new_tags' AS type, count(f) AS count, avg(size(f.new_tags)) AS avg_tags;

// Count Regions with new_tags
MATCH (r:Region)
WHERE r.new_tags IS NOT NULL AND size(r.new_tags) > 0
RETURN 'Regions with new_tags' AS type, count(r) AS count, avg(size(r.new_tags)) AS avg_tags;

// Count Customers with new_tags
MATCH (c:Customer)
WHERE c.new_tags IS NOT NULL AND size(c.new_tags) > 0
RETURN 'Customers with new_tags' AS type, count(c) AS count, avg(size(c.new_tags)) AS avg_tags;

// Count Sectors with new_tags (unique sectors only)
MATCH (s:Sector)
WHERE s.new_tags IS NOT NULL AND size(s.new_tags) > 0
WITH s.name AS sector_name, count(s) AS duplicates, avg(size(s.new_tags)) AS avg_tags
RETURN 'Unique Sectors with new_tags' AS type, count(sector_name) AS count, avg(avg_tags) AS avg_tags;

// Count Equipment with inherited_tags
MATCH (e:Equipment)
WHERE e.inherited_tags IS NOT NULL AND size(e.inherited_tags) > 0
RETURN 'Equipment with inherited_tags' AS type, count(e) AS count, avg(size(e.inherited_tags)) AS avg_tags;

// Sample Equipment showing tag inheritance sources
MATCH (e:Equipment)-[:LOCATED_AT]->(f:Facility)
OPTIONAL MATCH (e)-[:IN_REGION]->(r:Region)
OPTIONAL MATCH (e)-[:SERVES]->(c:Customer)
OPTIONAL MATCH (c)-[:BELONGS_TO]->(s:Sector)
WHERE size(e.inherited_tags) > 0
RETURN e.name AS equipment,
       size(e.inherited_tags) AS total_tags,
       size(COALESCE(f.new_tags, [])) AS facility_tags,
       size(COALESCE(r.new_tags, [])) AS region_tags,
       size(COALESCE(c.new_tags, [])) AS customer_tags,
       size(COALESCE(s.new_tags, [])) AS sector_tags
LIMIT 10;
