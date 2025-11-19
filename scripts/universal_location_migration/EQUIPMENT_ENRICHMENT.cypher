// ═══════════════════════════════════════════════════════════════
// EQUIPMENT ENRICHMENT SCRIPT - Universal Location Architecture
// Purpose: Add missing properties to 114 Equipment nodes
// Created: 2025-11-13
// ═══════════════════════════════════════════════════════════════

// STRATEGY: Distribute equipment across 4 facilities based on type patterns
// - 40% → SCADA Control Center (Boston) - RTU, PLC, Control devices
// - 30% → Substation Alpha (Providence) - Power equipment
// - 20% → Water Treatment West (SF) - Water infrastructure
// - 10% → Railway Control Hub (NYC) - Railway systems

// ═══════════════════════════════════════════════════════════════
// SCADA CONTROL CENTER (Boston) - 40% of equipment
// Coordinates: 42.3601, -71.0589
// ═══════════════════════════════════════════════════════════════

// RTU devices at SCADA center (Floor 2)
MATCH (e:Equipment)
WHERE e.equipmentType CONTAINS 'RTU'
  OR e.equipmentType CONTAINS 'Remote Terminal Unit'
  OR e.equipmentType CONTAINS 'Data Acquisition'
WITH e LIMIT 20
SET e.location = 'SCADA Control Center Floor 2 Bay ' + toString(id(e) % 10 + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 42.3601 + (rand() * 0.01 - 0.005),
    e.longitude = -71.0589 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 15.0 + (rand() * 5.0);

// PLC and Control devices at SCADA center (Floor 3)
MATCH (e:Equipment)
WHERE (e.equipmentType CONTAINS 'PLC'
  OR e.equipmentType CONTAINS 'Programmable Logic'
  OR e.equipmentType CONTAINS 'Controller'
  OR e.equipmentType CONTAINS 'Control System')
  AND e.location IS NULL
WITH e LIMIT 15
SET e.location = 'SCADA Control Center Floor 3 Rack ' + toString(id(e) % 8 + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 42.3601 + (rand() * 0.01 - 0.005),
    e.longitude = -71.0589 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 18.0 + (rand() * 5.0);

// Remaining SCADA equipment
MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e LIMIT 11
SET e.location = 'SCADA Control Center Floor 1 Zone ' + toString(id(e) % 6 + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 42.3601 + (rand() * 0.01 - 0.005),
    e.longitude = -71.0589 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 12.0 + (rand() * 5.0);

// ═══════════════════════════════════════════════════════════════
// SUBSTATION ALPHA (Providence) - 30% of equipment
// Coordinates: 41.8240, -71.4128
// ═══════════════════════════════════════════════════════════════

// Transformers and power equipment
MATCH (e:Equipment)
WHERE (e.equipmentType CONTAINS 'Transformer'
  OR e.equipmentType CONTAINS 'Circuit Breaker'
  OR e.equipmentType CONTAINS 'Breaker'
  OR e.equipmentType CONTAINS 'Switch')
  AND e.location IS NULL
WITH e LIMIT 20
SET e.location = 'Substation Alpha Bay ' + toString(id(e) % 12 + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 41.8240 + (rand() * 0.01 - 0.005),
    e.longitude = -71.4128 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 8.0 + (rand() * 4.0);

// Metering and monitoring equipment at substation
MATCH (e:Equipment)
WHERE (e.equipmentType CONTAINS 'Meter'
  OR e.equipmentType CONTAINS 'Monitor'
  OR e.equipmentType CONTAINS 'Sensor')
  AND e.location IS NULL
WITH e LIMIT 14
SET e.location = 'Substation Alpha Control Room Panel ' + toString(id(e) % 8 + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 41.8240 + (rand() * 0.01 - 0.005),
    e.longitude = -71.4128 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 10.0 + (rand() * 3.0);

// ═══════════════════════════════════════════════════════════════
// WATER TREATMENT WEST (San Francisco) - 20% of equipment
// Coordinates: 37.7749, -122.4194
// ═══════════════════════════════════════════════════════════════

// Water treatment equipment
MATCH (e:Equipment)
WHERE (e.equipmentType CONTAINS 'Pump'
  OR e.equipmentType CONTAINS 'Valve'
  OR e.equipmentType CONTAINS 'Flow'
  OR e.equipmentType CONTAINS 'Tank')
  AND e.location IS NULL
WITH e LIMIT 15
SET e.location = 'Water Treatment West Building A Unit ' + toString(id(e) % 10 + 1),
    e.customer_namespace = 'pacific-water',
    e.latitude = 37.7749 + (rand() * 0.01 - 0.005),
    e.longitude = -122.4194 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 25.0 + (rand() * 8.0);

// Water monitoring systems
MATCH (e:Equipment)
WHERE e.equipmentType CONTAINS 'Quality'
  AND e.location IS NULL
WITH e LIMIT 8
SET e.location = 'Water Treatment West Lab Station ' + toString(id(e) % 5 + 1),
    e.customer_namespace = 'pacific-water',
    e.latitude = 37.7749 + (rand() * 0.01 - 0.005),
    e.longitude = -122.4194 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 28.0 + (rand() * 5.0);

// ═══════════════════════════════════════════════════════════════
// RAILWAY CONTROL HUB (New York) - 10% of equipment
// Coordinates: 40.7128, -74.0060
// ═══════════════════════════════════════════════════════════════

// Railway control and signaling equipment
MATCH (e:Equipment)
WHERE (e.equipmentType CONTAINS 'Signal'
  OR e.equipmentType CONTAINS 'Track'
  OR e.equipmentType CONTAINS 'Railway'
  OR e.equipmentType CONTAINS 'Train')
  AND e.location IS NULL
WITH e LIMIT 11
SET e.location = 'Railway Control Hub Track Section ' + toString(id(e) % 6 + 1),
    e.customer_namespace = 'northeast-rail',
    e.latitude = 40.7128 + (rand() * 0.01 - 0.005),
    e.longitude = -74.0060 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 5.0 + (rand() * 3.0);

// ═══════════════════════════════════════════════════════════════
// CATCH-ALL: Assign any remaining equipment
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e
SET e.location = CASE
    WHEN id(e) % 4 = 0 THEN 'SCADA Control Center Floor 1 Misc Zone ' + toString(id(e) % 5 + 1)
    WHEN id(e) % 4 = 1 THEN 'Substation Alpha Utility Bay ' + toString(id(e) % 5 + 1)
    WHEN id(e) % 4 = 2 THEN 'Water Treatment West Building B Room ' + toString(id(e) % 5 + 1)
    ELSE 'Railway Control Hub Equipment Room ' + toString(id(e) % 5 + 1)
    END,
    e.customer_namespace = CASE
    WHEN id(e) % 4 = 0 THEN 'northeast-power'
    WHEN id(e) % 4 = 1 THEN 'northeast-power'
    WHEN id(e) % 4 = 2 THEN 'pacific-water'
    ELSE 'northeast-rail'
    END,
    e.latitude = CASE
    WHEN id(e) % 4 = 0 THEN 42.3601 + (rand() * 0.01 - 0.005)
    WHEN id(e) % 4 = 1 THEN 41.8240 + (rand() * 0.01 - 0.005)
    WHEN id(e) % 4 = 2 THEN 37.7749 + (rand() * 0.01 - 0.005)
    ELSE 40.7128 + (rand() * 0.01 - 0.005)
    END,
    e.longitude = CASE
    WHEN id(e) % 4 = 0 THEN -71.0589 + (rand() * 0.01 - 0.005)
    WHEN id(e) % 4 = 1 THEN -71.4128 + (rand() * 0.01 - 0.005)
    WHEN id(e) % 4 = 2 THEN -122.4194 + (rand() * 0.01 - 0.005)
    ELSE -74.0060 + (rand() * 0.01 - 0.005)
    END,
    e.elevation_meters = CASE
    WHEN id(e) % 4 = 0 THEN 12.0 + (rand() * 5.0)
    WHEN id(e) % 4 = 1 THEN 8.0 + (rand() * 4.0)
    WHEN id(e) % 4 = 2 THEN 25.0 + (rand() * 8.0)
    ELSE 5.0 + (rand() * 3.0)
    END;

// ═══════════════════════════════════════════════════════════════
// VERIFICATION: Count enriched equipment
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NOT NULL
  AND e.customer_namespace IS NOT NULL
  AND e.latitude IS NOT NULL
  AND e.longitude IS NOT NULL
RETURN 'Equipment Enriched' as result, count(e) as total_enriched;
