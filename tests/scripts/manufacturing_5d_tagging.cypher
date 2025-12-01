// ═══════════════════════════════════════════════════════════════
// GAP-004 MANUFACTURING SECTOR - 5-DIMENSIONAL TAGGING
// ═══════════════════════════════════════════════════════════════
// Part 3: Apply comprehensive 5D tags to all manufacturing equipment
// Dimensions: GEO, OPS, REG, TECH, TIME
// ═══════════════════════════════════════════════════════════════

// PHASE 3: APPLY 5-DIMENSIONAL TAGS
// ═══════════════════════════════════════════════════════════════

// GEO DIMENSION: Geographic tags based on facility location
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq, f,
  CASE f.state
    WHEN 'CA' THEN ['GEO_REGION_WEST_COAST', 'GEO_STATE_CA']
    WHEN 'WA' THEN ['GEO_REGION_WEST_COAST', 'GEO_STATE_WA']
    WHEN 'OR' THEN ['GEO_REGION_WEST_COAST', 'GEO_STATE_OR']
    WHEN 'TX' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_TX']
    WHEN 'AL' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_AL']
    WHEN 'TN' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_TN']
    WHEN 'SC' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_SC']
    WHEN 'GA' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_GA']
    WHEN 'NC' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_NC']
    WHEN 'FL' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_FL']
    WHEN 'AR' THEN ['GEO_REGION_SOUTH', 'GEO_STATE_AR']
    WHEN 'MI' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_MI']
    WHEN 'OH' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_OH']
    WHEN 'IL' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_IL']
    WHEN 'IN' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_IN']
    WHEN 'WI' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_WI']
    WHEN 'IA' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_IA']
    WHEN 'MN' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_MN']
    WHEN 'MO' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_MO']
    WHEN 'KS' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_KS']
    WHEN 'NE' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_NE']
    WHEN 'KY' THEN ['GEO_REGION_MIDWEST', 'GEO_STATE_KY']
    WHEN 'MA' THEN ['GEO_REGION_NORTHEAST', 'GEO_STATE_MA']
    WHEN 'NY' THEN ['GEO_REGION_NORTHEAST', 'GEO_STATE_NY']
    WHEN 'NJ' THEN ['GEO_REGION_NORTHEAST', 'GEO_STATE_NJ']
    WHEN 'PA' THEN ['GEO_REGION_NORTHEAST', 'GEO_STATE_PA']
    WHEN 'CT' THEN ['GEO_REGION_NORTHEAST', 'GEO_STATE_CT']
    WHEN 'AZ' THEN ['GEO_REGION_SOUTHWEST', 'GEO_STATE_AZ']
    WHEN 'CO' THEN ['GEO_REGION_SOUTHWEST', 'GEO_STATE_CO']
    ELSE ['GEO_REGION_UNKNOWN']
  END AS geoTags
SET eq.tags = eq.tags + geoTags;

// OPS DIMENSION: Operational tags based on facility and equipment type
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq, f,
  CASE
    WHEN f.facilityType CONTAINS 'Automotive' THEN
      ['OPS_FACILITY_AUTOMOTIVE', 'OPS_FUNCTION_VEHICLE_ASSEMBLY', 'OPS_SECTOR_TRANSPORTATION']
    WHEN f.facilityType CONTAINS 'Electronics' THEN
      ['OPS_FACILITY_ELECTRONICS', 'OPS_FUNCTION_SEMICONDUCTOR_FAB', 'OPS_SECTOR_TECHNOLOGY']
    WHEN f.facilityType CONTAINS 'Aerospace' THEN
      ['OPS_FACILITY_AEROSPACE', 'OPS_FUNCTION_AIRCRAFT_ASSEMBLY', 'OPS_SECTOR_DEFENSE']
    WHEN f.facilityType CONTAINS 'Heavy Machinery' THEN
      ['OPS_FACILITY_HEAVY_MACHINERY', 'OPS_FUNCTION_EQUIPMENT_MANUFACTURING', 'OPS_SECTOR_INDUSTRIAL']
    WHEN f.facilityType CONTAINS 'Food' THEN
      ['OPS_FACILITY_FOOD_PROCESSING', 'OPS_FUNCTION_FOOD_PRODUCTION', 'OPS_SECTOR_FOOD_SAFETY']
    WHEN f.facilityType CONTAINS 'Pharmaceutical' THEN
      ['OPS_FACILITY_PHARMACEUTICAL', 'OPS_FUNCTION_DRUG_MANUFACTURING', 'OPS_SECTOR_HEALTHCARE']
    ELSE ['OPS_FACILITY_MANUFACTURING']
  END AS opsFacilityTags,
  CASE
    WHEN eq.equipmentType CONTAINS 'Robot' THEN
      ['OPS_EQUIP_ROBOT', 'OPS_AUTOMATION_HIGH']
    WHEN eq.equipmentType CONTAINS 'Assembly' THEN
      ['OPS_EQUIP_ASSEMBLY_LINE', 'OPS_PRODUCTION_PRIMARY']
    WHEN eq.equipmentType CONTAINS 'Quality' THEN
      ['OPS_EQUIP_QC', 'OPS_FUNCTION_INSPECTION']
    WHEN eq.equipmentType CONTAINS 'Automation' THEN
      ['OPS_EQUIP_CONTROL', 'OPS_FUNCTION_AUTOMATION']
    WHEN eq.equipmentType CONTAINS 'Conveyor' THEN
      ['OPS_EQUIP_MATERIAL_FLOW', 'OPS_FUNCTION_LOGISTICS']
    WHEN eq.equipmentType CONTAINS 'Material' THEN
      ['OPS_EQUIP_HANDLING', 'OPS_FUNCTION_WAREHOUSING']
    WHEN eq.equipmentType CONTAINS 'Environmental' THEN
      ['OPS_EQUIP_HVAC', 'OPS_FUNCTION_CLIMATE_CONTROL']
    WHEN eq.equipmentType CONTAINS 'Safety' THEN
      ['OPS_EQUIP_SAFETY', 'OPS_FUNCTION_MONITORING']
    ELSE ['OPS_EQUIP_GENERAL']
  END AS opsEquipTags
SET eq.tags = eq.tags + opsFacilityTags + opsEquipTags;

// REG DIMENSION: Regulatory compliance tags
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq, f,
  // Base regulatory tags for all manufacturing
  ['REG_OSHA_GENERAL', 'REG_EPA_ENVIRONMENTAL'] AS baseTags,
  // Facility-specific regulatory tags
  CASE
    WHEN f.facilityType CONTAINS 'Automotive' THEN
      ['REG_DOT_VEHICLE', 'REG_EPA_EMISSIONS', 'REG_NHTSA_SAFETY']
    WHEN f.facilityType CONTAINS 'Electronics' THEN
      ['REG_FCC_COMPLIANCE', 'REG_RoHS_HAZMAT', 'REG_EPA_WASTE']
    WHEN f.facilityType CONTAINS 'Aerospace' THEN
      ['REG_FAA_AVIATION', 'REG_ITAR_DEFENSE', 'REG_NASA_SPACE', 'REG_MILITARY_SPEC']
    WHEN f.facilityType CONTAINS 'Heavy' THEN
      ['REG_ANSI_STANDARDS', 'REG_ISO_QUALITY', 'REG_OSHA_HEAVY']
    WHEN f.facilityType CONTAINS 'Food' THEN
      ['REG_FDA_FOOD_SAFETY', 'REG_HACCP_COMPLIANCE', 'REG_FSMA_PREVENTIVE', 'REG_USDA_INSPECTION']
    WHEN f.facilityType CONTAINS 'Pharmaceutical' THEN
      ['REG_FDA_DRUG', 'REG_GMP_PHARMA', 'REG_21CFR_PART11', 'REG_DEA_CONTROLLED']
    ELSE []
  END AS facRegTags,
  // Equipment-specific regulatory tags
  CASE
    WHEN eq.equipmentType CONTAINS 'Robot' THEN
      ['REG_ISO_13849_SAFETY', 'REG_ANSI_RIA_ROBOT']
    WHEN eq.equipmentType CONTAINS 'Quality' THEN
      ['REG_ISO_9001_QMS', 'REG_CALIBRATION_REQ']
    WHEN eq.equipmentType CONTAINS 'Safety' THEN
      ['REG_NFPA_LIFE_SAFETY', 'REG_UL_CERTIFICATION']
    WHEN eq.equipmentType CONTAINS 'Environmental' THEN
      ['REG_ASHRAE_STANDARDS', 'REG_EPA_AIR_QUALITY']
    ELSE []
  END AS eqRegTags
SET eq.tags = eq.tags + baseTags + facRegTags + eqRegTags;

// TECH DIMENSION: Technology and capability tags
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq,
  CASE
    WHEN eq.equipmentType CONTAINS 'Robot' THEN
      ['TECH_EQUIP_ROBOT', 'TECH_AUTOMATION_ADVANCED', 'TECH_AI_CAPABLE', 'TECH_NETWORK_CONNECTED']
    WHEN eq.equipmentType CONTAINS 'Assembly' THEN
      ['TECH_EQUIP_ASSEMBLY', 'TECH_AUTOMATION_PARTIAL', 'TECH_MODULAR_SYSTEM', 'TECH_NETWORK_CONNECTED']
    WHEN eq.equipmentType CONTAINS 'Quality' THEN
      ['TECH_EQUIP_QC', 'TECH_VISION_SYSTEM', 'TECH_MEASUREMENT_PRECISION', 'TECH_DATA_ANALYTICS']
    WHEN eq.equipmentType CONTAINS 'Automation' THEN
      ['TECH_EQUIP_CONTROL', 'TECH_PLC_BASED', 'TECH_SCADA_INTEGRATION', 'TECH_NETWORK_CRITICAL']
    WHEN eq.equipmentType CONTAINS 'Conveyor' THEN
      ['TECH_EQUIP_MATERIAL_TRANSPORT', 'TECH_AUTOMATION_BASIC', 'TECH_MECHANICAL_SYSTEM']
    WHEN eq.equipmentType CONTAINS 'Material' THEN
      ['TECH_EQUIP_HANDLING', 'TECH_HYDRAULIC_SYSTEM', 'TECH_ELECTRIC_DRIVE']
    WHEN eq.equipmentType CONTAINS 'Environmental' THEN
      ['TECH_EQUIP_HVAC', 'TECH_IOT_SENSORS', 'TECH_BUILDING_AUTOMATION', 'TECH_ENERGY_MANAGEMENT']
    WHEN eq.equipmentType CONTAINS 'Safety' THEN
      ['TECH_EQUIP_SAFETY', 'TECH_MONITORING_REALTIME', 'TECH_ALERT_SYSTEM', 'TECH_REDUNDANT']
    ELSE ['TECH_EQUIP_STANDARD']
  END AS techTags,
  // Add manufacturer-specific technology tags
  CASE
    WHEN eq.manufacturer CONTAINS 'ABB' THEN ['TECH_VENDOR_ABB']
    WHEN eq.manufacturer CONTAINS 'Siemens' THEN ['TECH_VENDOR_SIEMENS']
    WHEN eq.manufacturer CONTAINS 'Rockwell' THEN ['TECH_VENDOR_ROCKWELL']
    WHEN eq.manufacturer CONTAINS 'Honeywell' THEN ['TECH_VENDOR_HONEYWELL']
    WHEN eq.manufacturer CONTAINS 'Johnson' THEN ['TECH_VENDOR_JOHNSON_CONTROLS']
    ELSE ['TECH_VENDOR_GENERIC']
  END AS vendorTags
SET eq.tags = eq.tags + techTags + vendorTags;

// TIME DIMENSION: Temporal and lifecycle tags
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq,
  ['TIME_ERA_CURRENT', 'TIME_INSTALLATION_2020s'] AS baseTempTags,
  CASE eq.operational_status
    WHEN 'active' THEN ['TIME_STATUS_OPERATIONAL', 'TIME_MAINT_SCHEDULED']
    WHEN 'standby' THEN ['TIME_STATUS_STANDBY', 'TIME_MAINT_ROUTINE']
    WHEN 'maintenance' THEN ['TIME_STATUS_MAINTENANCE', 'TIME_MAINT_ACTIVE']
    ELSE ['TIME_STATUS_UNKNOWN']
  END AS statusTags,
  CASE eq.criticality_level
    WHEN 'critical' THEN ['TIME_MAINT_PRIORITY_CRITICAL', 'TIME_UPTIME_REQUIRED_99_9']
    WHEN 'high' THEN ['TIME_MAINT_PRIORITY_HIGH', 'TIME_UPTIME_REQUIRED_99']
    WHEN 'medium' THEN ['TIME_MAINT_PRIORITY_MEDIUM', 'TIME_UPTIME_REQUIRED_95']
    ELSE ['TIME_MAINT_PRIORITY_LOW']
  END AS criticalityTags,
  // Lifecycle tags based on installation date
  CASE
    WHEN duration.between(eq.installation_date, date()).years < 1 THEN
      ['TIME_LIFECYCLE_NEW', 'TIME_WARRANTY_ACTIVE']
    WHEN duration.between(eq.installation_date, date()).years < 3 THEN
      ['TIME_LIFECYCLE_MODERN', 'TIME_WARRANTY_EXTENDED']
    ELSE
      ['TIME_LIFECYCLE_MATURE', 'TIME_WARRANTY_EXPIRED']
  END AS lifecycleTags
SET eq.tags = eq.tags + baseTempTags + statusTags + criticalityTags + lifecycleTags;

// ═══════════════════════════════════════════════════════════════
// VERIFICATION AND STATISTICS
// ═══════════════════════════════════════════════════════════════

// Verify tag dimensions applied
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq,
  size([tag IN eq.tags WHERE tag STARTS WITH 'GEO_']) AS geoCount,
  size([tag IN eq.tags WHERE tag STARTS WITH 'OPS_']) AS opsCount,
  size([tag IN eq.tags WHERE tag STARTS WITH 'REG_']) AS regCount,
  size([tag IN eq.tags WHERE tag STARTS WITH 'TECH_']) AS techCount,
  size([tag IN eq.tags WHERE tag STARTS WITH 'TIME_']) AS timeCount
RETURN
  count(eq) AS total_equipment,
  avg(geoCount) AS avg_geo_tags,
  avg(opsCount) AS avg_ops_tags,
  avg(regCount) AS avg_reg_tags,
  avg(techCount) AS avg_tech_tags,
  avg(timeCount) AS avg_time_tags,
  avg(size(eq.tags)) AS avg_total_tags;

// Show sample of fully tagged equipment
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq, f
ORDER BY size(eq.tags) DESC
LIMIT 5
RETURN
  eq.equipmentId,
  eq.equipmentType,
  f.facilityType,
  f.state,
  size(eq.tags) AS total_tags,
  eq.tags AS all_tags;

// Tag distribution by dimension
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
UNWIND eq.tags AS tag
WITH tag,
  CASE
    WHEN tag STARTS WITH 'GEO_' THEN 'Geographic'
    WHEN tag STARTS WITH 'OPS_' THEN 'Operational'
    WHEN tag STARTS WITH 'REG_' THEN 'Regulatory'
    WHEN tag STARTS WITH 'TECH_' THEN 'Technology'
    WHEN tag STARTS WITH 'TIME_' THEN 'Temporal'
    ELSE 'Other'
  END AS dimension
RETURN dimension, count(*) AS tag_instances
ORDER BY tag_instances DESC;
