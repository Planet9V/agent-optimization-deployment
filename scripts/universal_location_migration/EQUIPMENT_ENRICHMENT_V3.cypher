// ═══════════════════════════════════════════════════════════════
// EQUIPMENT ENRICHMENT V3 - Direct Assignment Approach
// Purpose: Enrich ALL 114 Equipment nodes with location data
// Strategy: Use modulo on ID for deterministic distribution
// Created: 2025-11-13
// ═══════════════════════════════════════════════════════════════

// Enrich ALL Equipment nodes in single pass based on ID distribution
MATCH (e:Equipment)
SET
    // Assign location based on ID % 10 distribution
    e.location = CASE
        WHEN id(e) % 10 < 4 THEN 'SCADA Control Center Floor ' + toString((id(e) % 3) + 1) + ' Bay ' + toString((id(e) % 12) + 1)
        WHEN id(e) % 10 < 7 THEN 'Substation Alpha Bay ' + toString((id(e) % 15) + 1) + ' Panel ' + toString((id(e) % 8) + 1)
        WHEN id(e) % 10 < 9 THEN 'Water Treatment West Building ' + CASE (id(e) % 2) WHEN 0 THEN 'A' ELSE 'B' END + ' Unit ' + toString((id(e) % 10) + 1)
        ELSE 'Railway Control Hub Track Section ' + toString((id(e) % 8) + 1) + ' Equipment ' + toString((id(e) % 6) + 1)
    END,

    // Assign customer_namespace
    e.customer_namespace = CASE
        WHEN id(e) % 10 < 4 THEN 'northeast-power'
        WHEN id(e) % 10 < 7 THEN 'northeast-power'
        WHEN id(e) % 10 < 9 THEN 'pacific-water'
        ELSE 'northeast-rail'
    END,

    // Assign latitude
    e.latitude = CASE
        WHEN id(e) % 10 < 4 THEN 42.3601 + (rand() * 0.01 - 0.005)
        WHEN id(e) % 10 < 7 THEN 41.8240 + (rand() * 0.01 - 0.005)
        WHEN id(e) % 10 < 9 THEN 37.7749 + (rand() * 0.01 - 0.005)
        ELSE 40.7128 + (rand() * 0.01 - 0.005)
    END,

    // Assign longitude
    e.longitude = CASE
        WHEN id(e) % 10 < 4 THEN -71.0589 + (rand() * 0.01 - 0.005)
        WHEN id(e) % 10 < 7 THEN -71.4128 + (rand() * 0.01 - 0.005)
        WHEN id(e) % 10 < 9 THEN -122.4194 + (rand() * 0.01 - 0.005)
        ELSE -74.0060 + (rand() * 0.01 - 0.005)
    END,

    // Assign elevation
    e.elevation_meters = CASE
        WHEN id(e) % 10 < 4 THEN 12.0 + (rand() * 8.0)
        WHEN id(e) % 10 < 7 THEN 6.0 + (rand() * 6.0)
        WHEN id(e) % 10 < 9 THEN 20.0 + (rand() * 12.0)
        ELSE 3.0 + (rand() * 5.0)
    END,

    // Fill in equipmentType if missing
    e.equipmentType = COALESCE(e.equipmentType,
        CASE
            WHEN id(e) % 10 < 4 THEN
                CASE id(e) % 5
                    WHEN 0 THEN 'RTU Controller'
                    WHEN 1 THEN 'PLC Unit'
                    WHEN 2 THEN 'Data Acquisition System'
                    WHEN 3 THEN 'Control Panel'
                    ELSE 'SCADA Terminal'
                END
            WHEN id(e) % 10 < 7 THEN
                CASE id(e) % 5
                    WHEN 0 THEN 'Transformer'
                    WHEN 1 THEN 'Circuit Breaker'
                    WHEN 2 THEN 'Power Meter'
                    WHEN 3 THEN 'Voltage Regulator'
                    ELSE 'Switch Gear'
                END
            WHEN id(e) % 10 < 9 THEN
                CASE id(e) % 5
                    WHEN 0 THEN 'Water Pump'
                    WHEN 1 THEN 'Flow Valve'
                    WHEN 2 THEN 'Quality Sensor'
                    WHEN 3 THEN 'Filtration Unit'
                    ELSE 'Storage Tank Monitor'
                END
            ELSE
                CASE id(e) % 5
                    WHEN 0 THEN 'Signal Controller'
                    WHEN 1 THEN 'Track Switch'
                    WHEN 2 THEN 'Platform Monitor'
                    WHEN 3 THEN 'Railway Sensor'
                    ELSE 'Communication Gateway'
                END
        END);

// Return statistics
MATCH (e:Equipment)
RETURN
    'Equipment Enrichment Complete' as status,
    count(e) as total_equipment,
    count(e.location) as with_location,
    count(e.customer_namespace) as with_namespace,
    count(e.latitude) as with_latitude,
    count(e.longitude) as with_longitude,
    count(e.elevation_meters) as with_elevation,
    count(DISTINCT e.customer_namespace) as unique_namespaces;
