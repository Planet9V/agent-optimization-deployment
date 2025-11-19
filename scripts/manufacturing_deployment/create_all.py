import subprocess
import json

# Critical Manufacturing Sector: 50 facilities, 400 equipment
# Applying PATTERN-7: Comprehensive 3-Phase Deployment Script

facilities = [
    # Automotive Manufacturing (10)
    ("MFG-MI-AUTO-001", "Automotive Manufacturing", "MI", 42.3314, -83.0458),
    ("MFG-OH-AUTO-001", "Automotive Manufacturing", "OH", 39.9612, -82.9988),
    ("MFG-IN-AUTO-001", "Automotive Manufacturing", "IN", 39.7684, -86.1581),
    ("MFG-KY-AUTO-001", "Automotive Manufacturing", "KY", 38.2527, -85.7585),
    ("MFG-TN-AUTO-001", "Automotive Manufacturing", "TN", 35.8456, -86.3903),
    ("MFG-AL-AUTO-001", "Automotive Manufacturing", "AL", 32.3668, -86.2999),
    ("MFG-TX-AUTO-001", "Automotive Manufacturing", "TX", 32.7555, -97.3308),
    ("MFG-IL-AUTO-001", "Automotive Manufacturing", "IL", 41.5868, -88.0819),
    ("MFG-MO-AUTO-001", "Automotive Manufacturing", "MO", 38.5767, -92.1736),
    ("MFG-SC-AUTO-001", "Automotive Manufacturing", "SC", 34.5034, -82.6501),

    # Aerospace Manufacturing (8)
    ("MFG-WA-AERO-001", "Aerospace Manufacturing", "WA", 47.9064, -122.2814),
    ("MFG-CA-AERO-001", "Aerospace Manufacturing", "CA", 33.6846, -117.8265),
    ("MFG-TX-AERO-001", "Aerospace Manufacturing", "TX", 32.8483, -96.8511),
    ("MFG-FL-AERO-001", "Aerospace Manufacturing", "FL", 28.5383, -81.3792),
    ("MFG-CT-AERO-001", "Aerospace Manufacturing", "CT", 41.7658, -72.6734),
    ("MFG-AZ-AERO-001", "Aerospace Manufacturing", "AZ", 33.3062, -111.8413),
    ("MFG-GA-AERO-001", "Aerospace Manufacturing", "GA", 33.6407, -84.4277),
    ("MFG-OH-AERO-001", "Aerospace Manufacturing", "OH", 39.7817, -84.0773),

    # Steel Mills (6)
    ("MFG-IN-STEEL-001", "Steel Mill", "IN", 41.5892, -87.3095),
    ("MFG-PA-STEEL-001", "Steel Mill", "PA", 40.4406, -79.9959),
    ("MFG-OH-STEEL-001", "Steel Mill", "OH", 41.5051, -81.6934),
    ("MFG-IL-STEEL-001", "Steel Mill", "IL", 41.5394, -87.6648),
    ("MFG-MI-STEEL-001", "Steel Mill", "MI", 42.2395, -83.1753),
    ("MFG-AL-STEEL-001", "Steel Mill", "AL", 33.5186, -86.8104),

    # Shipbuilding (6)
    ("MFG-VA-SHIP-001", "Shipbuilding Yard", "VA", 36.8508, -76.2859),
    ("MFG-MS-SHIP-001", "Shipbuilding Yard", "MS", 30.3674, -88.5558),
    ("MFG-ME-SHIP-001", "Shipbuilding Yard", "ME", 43.6591, -70.2568),
    ("MFG-CA-SHIP-001", "Shipbuilding Yard", "CA", 32.7157, -117.1611),
    ("MFG-WA-SHIP-001", "Shipbuilding Yard", "WA", 47.5480, -122.6501),
    ("MFG-CT-SHIP-001", "Shipbuilding Yard", "CT", 41.3557, -72.0995),

    # Engine/Turbine Manufacturing (6)
    ("MFG-NC-ENG-001", "Engine Manufacturing", "NC", 35.5951, -82.5515),
    ("MFG-WI-ENG-001", "Engine Manufacturing", "WI", 43.0389, -87.9065),
    ("MFG-OH-ENG-001", "Engine Manufacturing", "OH", 40.1084, -83.0188),
    ("MFG-IL-ENG-001", "Engine Manufacturing", "IL", 40.6331, -89.3985),
    ("MFG-IN-ENG-001", "Engine Manufacturing", "IN", 39.5237, -87.3887),
    ("MFG-NY-ENG-001", "Engine Manufacturing", "NY", 42.9634, -78.7381),

    # Defense Manufacturing (6)
    ("MFG-CT-DEF-001", "Defense Systems Manufacturing", "CT", 41.2033, -73.1123),
    ("MFG-MA-DEF-001", "Defense Systems Manufacturing", "MA", 42.4184, -71.0656),
    ("MFG-VA-DEF-001", "Defense Systems Manufacturing", "VA", 38.9072, -77.4739),
    ("MFG-CA-DEF-001", "Defense Systems Manufacturing", "CA", 32.8801, -117.2340),
    ("MFG-AZ-DEF-001", "Defense Systems Manufacturing", "AZ", 33.4255, -111.9400),
    ("MFG-TX-DEF-001", "Defense Systems Manufacturing", "TX", 32.7295, -97.1081),

    # Aluminum Production (4)
    ("MFG-WA-ALU-001", "Aluminum Production", "WA", 48.7519, -122.4787),
    ("MFG-NY-ALU-001", "Aluminum Production", "NY", 44.6995, -75.1449),
    ("MFG-MT-ALU-001", "Aluminum Production", "MT", 48.1918, -114.3122),
    ("MFG-KY-ALU-001", "Aluminum Production", "KY", 37.0688, -87.5594),

    # Heavy Machinery (4)
    ("MFG-IL-HEAVY-001", "Heavy Machinery Manufacturing", "IL", 40.6936, -89.5890),
    ("MFG-IA-HEAVY-001", "Heavy Machinery Manufacturing", "IA", 42.0046, -93.6140),
    ("MFG-WI-HEAVY-001", "Heavy Machinery Manufacturing", "WI", 44.5192, -88.0198),
    ("MFG-PA-HEAVY-001", "Heavy Machinery Manufacturing", "PA", 40.2732, -76.8867)
]

equipment_types = [
    'CNC Machines',
    'Industrial Robots',
    'Welding Equipment',
    'Assembly Line Systems',
    'Quality Control Systems',
    'Material Handling Equipment',
    'Industrial HVAC',
    'Safety Systems'
]

print(f"═══════════════════════════════════════════════════════════════")
print(f"CRITICAL MANUFACTURING SECTOR DEPLOYMENT")
print(f"═══════════════════════════════════════════════════════════════")
print(f"Facilities: {len(facilities)}")
print(f"Target Equipment: 400")
print(f"Equipment Types: {', '.join(equipment_types)}")
print()

# PHASE 1: Create 400 Equipment nodes
print("PHASE 1: Creating 400 Manufacturing equipment nodes...")
equipment_count = 0
for i in range(400):
    eq_id = f"EQ-MFG-{50000 + i + 1}"
    eq_type = equipment_types[i % len(equipment_types)]
    criticality = ['critical', 'high', 'medium'][i % 3]
    status = ['active', 'standby', 'maintenance'][i % 3]

    query = f"""
CREATE (eq:Equipment {{
  equipmentId: '{eq_id}',
  name: '{eq_type} Unit {i+1}',
  equipmentType: '{eq_type}',
  manufacturer: 'Manufacturer-{eq_type.replace(" ", "")}',
  model: '{eq_type.replace(" ", "-")}-2023',
  serial_number: 'SN-M-{500000 + i + 1}',
  installation_date: date('2023-01-01'),
  operational_status: '{status}',
  criticality_level: '{criticality}',
  tags: ['MFG_EQUIP', 'SECTOR_MANUFACTURING'],
  created_date: datetime(),
  updated_date: datetime()
}});
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        equipment_count += 1
        if equipment_count % 40 == 0:
            print(f"  Created {equipment_count}/400 equipment...")

print(f"✅ Equipment created: {equipment_count}")

# PHASE 2: Create LOCATED_AT relationships
print("\nPHASE 2: Creating LOCATED_AT relationships...")
relationships_count = 0

# Distribute 400 equipment across 50 facilities (8 per facility)
for fac_idx, (fac_id, fac_type, state, lat, lon) in enumerate(facilities):
    for eq_offset in range(8):
        eq_num = (fac_idx * 8) + eq_offset
        if eq_num >= 400:
            break
        eq_id = f"EQ-MFG-{50000 + eq_num + 1}"

        query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}}), (f:Facility {{facilityId: '{fac_id}'}})
CREATE (eq)-[:LOCATED_AT {{
  installation_date: eq.installation_date,
  location: 'Zone {eq_offset + 1}',
  exact_coordinates: point({{latitude: {lat + 0.0005}, longitude: {lon + 0.0005}}})
}}]->(f);
"""

        result = subprocess.run(
            ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            relationships_count += 1
            if relationships_count % 40 == 0:
                print(f"  Created {relationships_count}/400 relationships...")

print(f"✅ Relationships created: {relationships_count}")

# PHASE 3: Apply 5-dimensional tags
print("\nPHASE 3: Applying 5-dimensional tags...")

get_equipment = """
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-MFG-'
RETURN eq.equipmentId AS eqId, eq.equipmentType AS eqType,
       f.state AS state, f.facilityType AS facType
LIMIT 400;
"""

result = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', get_equipment],
    capture_output=True,
    text=True
)

lines = [l.strip() for l in result.stdout.strip().split('\n')[1:] if l.strip() and not l.startswith('eq')]
tags_count = 0

for line in lines:
    if not line:
        continue
    parts = [p.strip().strip('"') for p in line.split(',')]
    if len(parts) < 4:
        continue

    eq_id, eq_type, state, fac_type = parts[0], parts[1], parts[2], parts[3]

    tags = ['MFG_EQUIP', 'SECTOR_MANUFACTURING']

    # GEO tags
    state_to_region = {
        'MI': 'MIDWEST', 'OH': 'MIDWEST', 'IN': 'MIDWEST', 'IL': 'MIDWEST', 'MO': 'MIDWEST', 'WI': 'MIDWEST', 'IA': 'MIDWEST',
        'WA': 'NORTHWEST', 'OR': 'NORTHWEST', 'MT': 'MOUNTAIN',
        'CA': 'WEST_COAST', 'AZ': 'MOUNTAIN',
        'TX': 'SOUTH', 'KY': 'SOUTH', 'TN': 'SOUTH', 'AL': 'SOUTH', 'SC': 'SOUTH', 'FL': 'SOUTH', 'VA': 'SOUTH', 'NC': 'SOUTH', 'MS': 'SOUTH',
        'PA': 'NORTHEAST', 'NY': 'NORTHEAST', 'CT': 'NORTHEAST', 'MA': 'NORTHEAST', 'ME': 'NORTHEAST'
    }
    if state in state_to_region:
        tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])

    # OPS tags
    if 'Automotive' in fac_type:
        tags.extend(['OPS_FACILITY_AUTOMOTIVE', 'OPS_FUNCTION_VEHICLE_ASSEMBLY'])
    elif 'Aerospace' in fac_type:
        tags.extend(['OPS_FACILITY_AEROSPACE', 'OPS_FUNCTION_AIRCRAFT_PRODUCTION'])
    elif 'Steel' in fac_type:
        tags.extend(['OPS_FACILITY_STEEL_MILL', 'OPS_FUNCTION_METAL_PRODUCTION'])
    elif 'Shipbuilding' in fac_type:
        tags.extend(['OPS_FACILITY_SHIPYARD', 'OPS_FUNCTION_SHIP_CONSTRUCTION'])
    elif 'Engine' in fac_type:
        tags.extend(['OPS_FACILITY_ENGINE_MFG', 'OPS_FUNCTION_ENGINE_PRODUCTION'])
    elif 'Defense' in fac_type:
        tags.extend(['OPS_FACILITY_DEFENSE', 'OPS_FUNCTION_DEFENSE_SYSTEMS'])
    elif 'Aluminum' in fac_type:
        tags.extend(['OPS_FACILITY_ALUMINUM', 'OPS_FUNCTION_ALUMINUM_PRODUCTION'])
    elif 'Heavy Machinery' in fac_type:
        tags.extend(['OPS_FACILITY_HEAVY_MFG', 'OPS_FUNCTION_MACHINERY_PRODUCTION'])

    # REG tags
    tags.extend(['REG_OSHA_MANUFACTURING', 'REG_EPA_AIR_QUALITY'])
    if 'Defense' in fac_type:
        tags.extend(['REG_DOD_CMMC', 'REG_ITAR_COMPLIANCE'])
    if 'Automotive' in fac_type or 'Aerospace' in fac_type:
        tags.extend(['REG_ISO_9001', 'REG_NIST_COMPLIANCE'])
    if 'Steel' in fac_type or 'Aluminum' in fac_type:
        tags.extend(['REG_STATE_INDUSTRIAL', 'REG_LABOR_STANDARDS'])

    # TECH tags
    if 'CNC' in eq_type:
        tags.extend(['TECH_EQUIP_CNC', 'TECH_PRECISION_MACHINING'])
    elif 'Robot' in eq_type:
        tags.extend(['TECH_EQUIP_ROBOTICS', 'TECH_AUTOMATION'])
    elif 'Welding' in eq_type:
        tags.extend(['TECH_EQUIP_WELDING', 'TECH_JOINING'])
    elif 'Assembly' in eq_type:
        tags.extend(['TECH_EQUIP_ASSEMBLY', 'TECH_PRODUCTION_LINE'])
    elif 'Quality' in eq_type:
        tags.extend(['TECH_EQUIP_QC', 'TECH_INSPECTION'])
    elif 'Material Handling' in eq_type:
        tags.extend(['TECH_EQUIP_MATERIAL_HANDLING', 'TECH_LOGISTICS'])
    elif 'HVAC' in eq_type:
        tags.extend(['TECH_EQUIP_HVAC', 'TECH_CLIMATE_CONTROL'])
    elif 'Safety' in eq_type:
        tags.extend(['TECH_EQUIP_SAFETY', 'TECH_PROTECTION'])

    # TIME tags
    tags.extend(['TIME_ERA_CURRENT', 'TIME_MAINT_PRIORITY_HIGH'])

    tags_json = json.dumps(tags)
    update_query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}})
SET eq.tags = {tags_json};
"""

    subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', update_query],
        capture_output=True,
        text=True
    )

    tags_count += 1
    if tags_count % 40 == 0:
        print(f"  Tagged {tags_count}/400 equipment...")

print(f"✅ Equipment tagged: {tags_count}")

# VERIFICATION
print("\n" + "═"*60)
print("VERIFICATION")
print("═"*60)

verify_queries = [
    ("Equipment count", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-MFG-' RETURN COUNT(eq) AS count;"),
    ("Relationships count", "MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility) WHERE eq.equipmentId STARTS WITH 'EQ-MFG-' RETURN COUNT(r) AS count, COUNT(DISTINCT eq) AS unique_equipment, COUNT(DISTINCT f) AS unique_facilities;"),
    ("Tag statistics", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-MFG-' WITH eq, size(eq.tags) AS tc RETURN AVG(tc) AS avg_tags, MIN(tc) AS min_tags, MAX(tc) AS max_tags;")
]

for desc, query in verify_queries:
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )
    print(f"\n{desc}:")
    print(result.stdout)

print("\n✅ CRITICAL MANUFACTURING SECTOR DEPLOYMENT COMPLETE")
