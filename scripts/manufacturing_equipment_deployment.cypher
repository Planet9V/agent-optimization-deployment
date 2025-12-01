// ═══════════════════════════════════════════════════════════════
// GAP-004 MANUFACTURING SECTOR - EQUIPMENT DEPLOYMENT
// ═══════════════════════════════════════════════════════════════
// Part 2: 400 Equipment Nodes with 5D Tagging
// Pattern: PATTERN-7 Batch Equipment Creation
// ═══════════════════════════════════════════════════════════════

// PHASE 2: CREATE 400 EQUIPMENT NODES (8 per facility × 50 facilities)
// Equipment distributed across 50 facilities

// Equipment Types Distribution:
// - Production Robots (100 units)
// - Assembly Line Systems (80 units)
// - Quality Control Systems (60 units)
// - Industrial Automation Controllers (60 units)
// - Conveyor Systems (40 units)
// - Material Handling Equipment (30 units)
// - Environmental Control Systems (20 units)
// - Safety Monitoring Systems (10 units)

// BATCH 1: Production Robots (Equipment 50001-50100)
:auto UNWIND range(1, 100) AS i
WITH i,
  ['Automotive Assembly', 'Electronics Manufacturing', 'Aerospace Manufacturing', 'Heavy Machinery Manufacturing', 'Food Processing', 'Pharmaceutical Manufacturing'] AS facTypes,
  ['MFG-MI-AUTO-001', 'MFG-OH-AUTO-001', 'MFG-KY-AUTO-001', 'MFG-TN-AUTO-001', 'MFG-AL-AUTO-001',
   'MFG-SC-AUTO-001', 'MFG-TX-AUTO-001', 'MFG-CA-AUTO-001', 'MFG-IN-AUTO-001', 'MFG-IL-AUTO-001',
   'MFG-CA-ELEC-001', 'MFG-TX-ELEC-001', 'MFG-OR-ELEC-001', 'MFG-AZ-ELEC-001', 'MFG-MA-ELEC-001',
   'MFG-NY-ELEC-001', 'MFG-NC-ELEC-001', 'MFG-CO-ELEC-001', 'MFG-MN-ELEC-001', 'MFG-WA-ELEC-001',
   'MFG-WA-AERO-001', 'MFG-CA-AERO-001', 'MFG-TX-AERO-001', 'MFG-CT-AERO-001', 'MFG-FL-AERO-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Production Robot Unit ' + toString(i),
  equipmentType: 'Production Robots',
  manufacturer: 'ABB Robotics',
  model: 'IRB-6700-' + toString(2023 + (i % 3)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2023-01-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'critical' WHEN 1 THEN 'high' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_ROBOT', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-1) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Production Floor Zone ' + toString((i % 8) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 2: Assembly Line Systems (Equipment 50101-50180)
:auto UNWIND range(101, 180) AS i
WITH i,
  ['MFG-MI-AUTO-001', 'MFG-OH-AUTO-001', 'MFG-KY-AUTO-001', 'MFG-TN-AUTO-001', 'MFG-AL-AUTO-001',
   'MFG-SC-AUTO-001', 'MFG-TX-AUTO-001', 'MFG-CA-AUTO-001', 'MFG-IN-AUTO-001', 'MFG-IL-AUTO-001',
   'MFG-CA-ELEC-001', 'MFG-TX-ELEC-001', 'MFG-OR-ELEC-001', 'MFG-AZ-ELEC-001', 'MFG-MA-ELEC-001',
   'MFG-IL-HEAVY-001', 'MFG-WI-HEAVY-001', 'MFG-IA-HEAVY-001', 'MFG-PA-HEAVY-001', 'MFG-GA-HEAVY-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Assembly Line System ' + toString(i - 100),
  equipmentType: 'Assembly Line Systems',
  manufacturer: 'Siemens Industrial',
  model: 'ALX-' + toString(5000 + (i % 10)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2022-06-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'critical' WHEN 1 THEN 'high' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_ASSEMBLY', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-101) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Assembly Line ' + toString((i % 8) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 3: Quality Control Systems (Equipment 50181-50240)
:auto UNWIND range(181, 240) AS i
WITH i,
  ['MFG-CA-ELEC-001', 'MFG-TX-ELEC-001', 'MFG-OR-ELEC-001', 'MFG-AZ-ELEC-001', 'MFG-MA-ELEC-001',
   'MFG-NY-ELEC-001', 'MFG-NC-ELEC-001', 'MFG-CO-ELEC-001', 'MFG-MN-ELEC-001', 'MFG-WA-ELEC-001',
   'MFG-NJ-PHARMA-001', 'MFG-MA-PHARMA-001', 'MFG-PA-PHARMA-001', 'MFG-CA-PHARMA-001', 'MFG-NC-PHARMA-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Quality Control System ' + toString(i - 180),
  equipmentType: 'Quality Control Systems',
  manufacturer: 'Keyence Corporation',
  model: 'QCS-' + toString(3000 + (i % 15)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2023-03-15'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'critical' WHEN 1 THEN 'high' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_QC', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-181) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'QC Station ' + toString((i % 6) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 4: Industrial Automation Controllers (Equipment 50241-50300)
:auto UNWIND range(241, 300) AS i
WITH i,
  ['MFG-WA-AERO-001', 'MFG-CA-AERO-001', 'MFG-TX-AERO-001', 'MFG-CT-AERO-001', 'MFG-FL-AERO-001',
   'MFG-AL-AERO-001', 'MFG-CO-AERO-001', 'MFG-AZ-AERO-001',
   'MFG-IL-HEAVY-001', 'MFG-WI-HEAVY-001', 'MFG-IA-HEAVY-001', 'MFG-PA-HEAVY-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Automation Controller ' + toString(i - 240),
  equipmentType: 'Industrial Automation Controllers',
  manufacturer: 'Rockwell Automation',
  model: 'ControlLogix-' + toString(5500 + (i % 12)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2022-09-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'critical' WHEN 1 THEN 'high' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_AUTOMATION', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-241) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Control Room ' + toString((i % 5) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 5: Conveyor Systems (Equipment 50301-50340)
:auto UNWIND range(301, 340) AS i
WITH i,
  ['MFG-IA-FOOD-001', 'MFG-WI-FOOD-001', 'MFG-CA-FOOD-001', 'MFG-AR-FOOD-001',
   'MFG-NE-FOOD-001', 'MFG-KS-FOOD-001', 'MFG-MN-FOOD-001',
   'MFG-MI-AUTO-001', 'MFG-OH-AUTO-001', 'MFG-IL-AUTO-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Conveyor System ' + toString(i - 300),
  equipmentType: 'Conveyor Systems',
  manufacturer: 'Dorner Conveyors',
  model: 'FlexMove-' + toString(2200 + (i % 10)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2022-11-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'high' WHEN 1 THEN 'medium' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_CONVEYOR', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-301) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Material Flow Zone ' + toString((i % 4) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 6: Material Handling Equipment (Equipment 50341-50370)
:auto UNWIND range(341, 370) AS i
WITH i,
  ['MFG-GA-HEAVY-001', 'MFG-NC-HEAVY-001', 'MFG-OH-HEAVY-001', 'MFG-MO-HEAVY-001',
   'MFG-IL-PHARMA-001', 'MFG-IN-PHARMA-001',
   'MFG-SC-AUTO-001', 'MFG-TN-AUTO-001', 'MFG-AL-AUTO-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Material Handler ' + toString(i - 340),
  equipmentType: 'Material Handling Equipment',
  manufacturer: 'KION Group',
  model: 'Linde-H' + toString(25 + (i % 9)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2023-02-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: CASE i % 3 WHEN 0 THEN 'high' WHEN 1 THEN 'medium' ELSE 'medium' END,
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_MATERIAL_HANDLING', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-341) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Warehouse Section ' + toString((i % 3) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 7: Environmental Control Systems (Equipment 50371-50390)
:auto UNWIND range(371, 390) AS i
WITH i,
  ['MFG-NJ-PHARMA-001', 'MFG-MA-PHARMA-001', 'MFG-PA-PHARMA-001', 'MFG-CA-PHARMA-001',
   'MFG-CA-ELEC-001', 'MFG-TX-ELEC-001', 'MFG-OR-ELEC-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Environmental Control Unit ' + toString(i - 370),
  equipmentType: 'Environmental Control Systems',
  manufacturer: 'Johnson Controls',
  model: 'Metasys-' + toString(4000 + (i % 7)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2023-04-01'),
  operational_status: CASE i % 3 WHEN 0 THEN 'active' WHEN 1 THEN 'standby' ELSE 'maintenance' END,
  criticality_level: 'critical',
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_ENVIRONMENTAL', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-371) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'HVAC Room ' + toString((i % 2) + 1),
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// BATCH 8: Safety Monitoring Systems (Equipment 50391-50400)
:auto UNWIND range(391, 400) AS i
WITH i,
  ['MFG-WA-AERO-001', 'MFG-CA-AERO-001', 'MFG-TX-AERO-001', 'MFG-FL-AERO-001',
   'MFG-NJ-PHARMA-001', 'MFG-MA-PHARMA-001'] AS facilities
CREATE (eq:Equipment {
  equipmentId: 'EQ-MFG-' + toString(50000 + i),
  name: 'Safety Monitor System ' + toString(i - 390),
  equipmentType: 'Safety Monitoring Systems',
  manufacturer: 'Honeywell Safety',
  model: 'SafetyNet-' + toString(3500 + (i % 6)),
  serial_number: 'SN-MFG-' + toString(500000 + i),
  installation_date: date('2023-05-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING', 'EQUIP_TYPE_SAFETY', 'TIME_ERA_CURRENT'],
  created_date: datetime(),
  updated_date: datetime()
})
WITH eq, facilities, i
MATCH (f:Facility {facilityId: facilities[(i-391) % size(facilities)]})
CREATE (eq)-[:LOCATED_AT {
  installation_date: eq.installation_date,
  location: 'Safety Control Center',
  exact_coordinates: point({
    latitude: f.coordinates.latitude + (rand() * 0.001 - 0.0005),
    longitude: f.coordinates.longitude + (rand() * 0.001 - 0.0005)
  })
}]->(f);

// ═══════════════════════════════════════════════════════════════
// VERIFICATION QUERIES
// ═══════════════════════════════════════════════════════════════

// Count equipment by type
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq.equipmentType AS type, count(*) AS count
RETURN type, count
ORDER BY count DESC;

// Count total equipment and relationships
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
RETURN
  count(DISTINCT eq) AS total_equipment,
  count(DISTINCT f) AS facilities_used,
  count(r) AS relationships_created;

// Verify tag distribution
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
RETURN
  size(eq.tags) AS tag_count,
  count(*) AS equipment_count
ORDER BY tag_count DESC;
