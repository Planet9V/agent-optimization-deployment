// ═══════════════════════════════════════════════════════════════
// EQUIPMENT ENRICHMENT V2 - Universal Location Architecture
// Purpose: Add missing properties to ALL 114 Equipment nodes
// Strategy: Distribute based on node ID since equipmentType is sparse
// Created: 2025-11-13
// ═══════════════════════════════════════════════════════════════

// Distribution: 40% Boston, 30% Providence, 20% SF, 10% NYC

// ═══════════════════════════════════════════════════════════════
// BATCH 1: SCADA Control Center (Boston) - First 46 nodes (40%)
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e ORDER BY id(e)
LIMIT 46
SET e.location = 'SCADA Control Center Floor ' + toString((id(e) % 3) + 1) + ' Bay ' + toString((id(e) % 10) + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 42.3601 + (rand() * 0.01 - 0.005),
    e.longitude = -71.0589 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 12.0 + (rand() * 8.0),
    e.equipmentType = COALESCE(e.equipmentType,
        CASE id(e) % 5
            WHEN 0 THEN 'RTU Controller'
            WHEN 1 THEN 'PLC Unit'
            WHEN 2 THEN 'Data Acquisition System'
            WHEN 3 THEN 'Control Panel'
            ELSE 'SCADA Terminal'
        END);

// ═══════════════════════════════════════════════════════════════
// BATCH 2: Substation Alpha (Providence) - Next 34 nodes (30%)
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e ORDER BY id(e)
LIMIT 34
SET e.location = 'Substation Alpha Bay ' + toString((id(e) % 12) + 1) + ' Panel ' + toString((id(e) % 8) + 1),
    e.customer_namespace = 'northeast-power',
    e.latitude = 41.8240 + (rand() * 0.01 - 0.005),
    e.longitude = -71.4128 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 6.0 + (rand() * 6.0),
    e.equipmentType = COALESCE(e.equipmentType,
        CASE id(e) % 5
            WHEN 0 THEN 'Transformer'
            WHEN 1 THEN 'Circuit Breaker'
            WHEN 2 THEN 'Power Meter'
            WHEN 3 THEN 'Voltage Regulator'
            ELSE 'Switch Gear'
        END);

// ═══════════════════════════════════════════════════════════════
// BATCH 3: Water Treatment West (SF) - Next 23 nodes (20%)
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e ORDER BY id(e)
LIMIT 23
SET e.location = 'Water Treatment West Building ' +
        CASE (id(e) % 2) WHEN 0 THEN 'A' ELSE 'B' END +
        ' Unit ' + toString((id(e) % 10) + 1),
    e.customer_namespace = 'pacific-water',
    e.latitude = 37.7749 + (rand() * 0.01 - 0.005),
    e.longitude = -122.4194 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 20.0 + (rand() * 12.0),
    e.equipmentType = COALESCE(e.equipmentType,
        CASE id(e) % 5
            WHEN 0 THEN 'Water Pump'
            WHEN 1 THEN 'Flow Valve'
            WHEN 2 THEN 'Quality Sensor'
            WHEN 3 THEN 'Filtration Unit'
            ELSE 'Storage Tank Monitor'
        END);

// ═══════════════════════════════════════════════════════════════
// BATCH 4: Railway Control Hub (NYC) - Remaining nodes (10%)
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NULL
WITH e ORDER BY id(e)
SET e.location = 'Railway Control Hub Track Section ' + toString((id(e) % 8) + 1) +
        ' Equipment ' + toString((id(e) % 6) + 1),
    e.customer_namespace = 'northeast-rail',
    e.latitude = 40.7128 + (rand() * 0.01 - 0.005),
    e.longitude = -74.0060 + (rand() * 0.01 - 0.005),
    e.elevation_meters = 3.0 + (rand() * 5.0),
    e.equipmentType = COALESCE(e.equipmentType,
        CASE id(e) % 5
            WHEN 0 THEN 'Signal Controller'
            WHEN 1 THEN 'Track Switch'
            WHEN 2 THEN 'Platform Monitor'
            WHEN 3 THEN 'Railway Sensor'
            ELSE 'Communication Gateway'
        END);

// ═══════════════════════════════════════════════════════════════
// VERIFICATION: Final count and sample
// ═══════════════════════════════════════════════════════════════

MATCH (e:Equipment)
WHERE e.location IS NOT NULL
RETURN
    'Total Enriched' as status,
    count(e) as total,
    count(DISTINCT e.customer_namespace) as namespaces,
    count(DISTINCT e.location) as unique_locations;
