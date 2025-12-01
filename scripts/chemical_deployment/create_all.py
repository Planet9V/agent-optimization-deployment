import subprocess
import json

# Chemical Sector: 40 facilities, 300 equipment
# Applying PATTERN-7: Comprehensive 3-Phase Deployment Script

facilities = [
    # Chemical Manufacturing Plants (10)
    ("CHEM-TX-001", "Chemical Manufacturing Plant", "TX", 29.7433, -95.3461),
    ("CHEM-LA-001", "Chemical Manufacturing Plant", "LA", 30.2241, -92.0198),
    ("CHEM-NJ-001", "Chemical Manufacturing Plant", "NJ", 40.8426, -74.2734),
    ("CHEM-OH-001", "Chemical Manufacturing Plant", "OH", 41.0814, -81.5190),
    ("CHEM-IL-001", "Chemical Manufacturing Plant", "IL", 41.5051, -90.5151),
    ("CHEM-PA-001", "Chemical Manufacturing Plant", "PA", 40.4406, -79.9959),
    ("CHEM-MI-001", "Chemical Manufacturing Plant", "MI", 42.9634, -82.4242),
    ("CHEM-CA-001", "Chemical Manufacturing Plant", "CA", 33.9425, -118.4081),
    ("CHEM-NC-001", "Chemical Manufacturing Plant", "NC", 35.2271, -80.8431),
    ("CHEM-TN-001", "Chemical Manufacturing Plant", "TN", 35.0456, -85.3097),

    # Petrochemical Plants (8)
    ("CHEM-TX-PETRO-001", "Petrochemical Plant", "TX", 29.6994, -95.2089),
    ("CHEM-LA-PETRO-001", "Petrochemical Plant", "LA", 29.9499, -90.0701),
    ("CHEM-TX-PETRO-002", "Petrochemical Plant", "TX", 29.7502, -95.0632),
    ("CHEM-LA-PETRO-002", "Petrochemical Plant", "LA", 30.0075, -90.4782),
    ("CHEM-AL-PETRO-001", "Petrochemical Plant", "AL", 30.6944, -88.0431),
    ("CHEM-MS-PETRO-001", "Petrochemical Plant", "MS", 30.3960, -89.0928),
    ("CHEM-TX-PETRO-003", "Petrochemical Plant", "TX", 28.0369, -97.0403),
    ("CHEM-CA-PETRO-001", "Petrochemical Plant", "CA", 33.7701, -118.1937),

    # Pharmaceutical Manufacturing (6)
    ("CHEM-NJ-PHARMA-001", "Pharmaceutical Manufacturing", "NJ", 40.4862, -74.4518),
    ("CHEM-PA-PHARMA-001", "Pharmaceutical Manufacturing", "PA", 40.0379, -75.0811),
    ("CHEM-CA-PHARMA-001", "Pharmaceutical Manufacturing", "CA", 37.5485, -121.9886),
    ("CHEM-MA-PHARMA-001", "Pharmaceutical Manufacturing", "MA", 42.4072, -71.3824),
    ("CHEM-NC-PHARMA-001", "Pharmaceutical Manufacturing", "NC", 35.9132, -79.0558),
    ("CHEM-IL-PHARMA-001", "Pharmaceutical Manufacturing", "IL", 41.7606, -87.7036),

    # Fertilizer Production Plants (6)
    ("CHEM-IA-FERT-001", "Fertilizer Production Plant", "IA", 42.0308, -93.6319),
    ("CHEM-IL-FERT-001", "Fertilizer Production Plant", "IL", 40.1164, -88.2434),
    ("CHEM-KS-FERT-001", "Fertilizer Production Plant", "KS", 38.8403, -97.6114),
    ("CHEM-NE-FERT-001", "Fertilizer Production Plant", "NE", 41.2565, -95.9345),
    ("CHEM-OK-FERT-001", "Fertilizer Production Plant", "OK", 35.4676, -97.5164),
    ("CHEM-TX-FERT-001", "Fertilizer Production Plant", "TX", 33.2148, -97.1331),

    # Hazardous Material Storage (5)
    ("CHEM-TX-HAZ-001", "Hazardous Material Storage", "TX", 29.7355, -95.5133),
    ("CHEM-LA-HAZ-001", "Hazardous Material Storage", "LA", 30.4515, -91.1871),
    ("CHEM-NJ-HAZ-001", "Hazardous Material Storage", "NJ", 40.5796, -74.3227),
    ("CHEM-CA-HAZ-001", "Hazardous Material Storage", "CA", 33.8366, -118.3897),
    ("CHEM-IL-HAZ-001", "Hazardous Material Storage", "IL", 41.7658, -87.7321),

    # Waste Treatment Facilities (5)
    ("CHEM-TX-WASTE-001", "Chemical Waste Treatment", "TX", 29.5805, -95.6389),
    ("CHEM-LA-WASTE-001", "Chemical Waste Treatment", "LA", 30.2672, -92.0211),
    ("CHEM-OH-WASTE-001", "Chemical Waste Treatment", "OH", 41.2565, -81.8552),
    ("CHEM-CA-WASTE-001", "Chemical Waste Treatment", "CA", 34.0007, -118.2468),
    ("CHEM-MI-WASTE-001", "Chemical Waste Treatment", "MI", 42.7325, -84.5555)
]

equipment_types = [
    'Reactor Vessels',
    'Storage Tanks',
    'Process Control Systems',
    'Safety Monitoring Equipment',
    'Hazmat Handling Systems',
    'Ventilation Systems',
    'Emergency Shutdown Systems',
    'Leak Detection Systems'
]

print(f"═══════════════════════════════════════════════════════════════")
print(f"CHEMICAL SECTOR DEPLOYMENT")
print(f"═══════════════════════════════════════════════════════════════")
print(f"Facilities: {len(facilities)}")
print(f"Target Equipment: 300")
print(f"Equipment Types: {', '.join(equipment_types)}")
print()

# PHASE 1: Create 300 Equipment nodes
print("PHASE 1: Creating 300 Chemical equipment nodes...")
equipment_count = 0
for i in range(300):
    eq_id = f"EQ-CHEM-{40000 + i + 1}"
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
  serial_number: 'SN-C-{400000 + i + 1}',
  installation_date: date('2023-01-01'),
  operational_status: '{status}',
  criticality_level: '{criticality}',
  tags: ['CHEM_EQUIP', 'SECTOR_CHEMICAL'],
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
        if equipment_count % 30 == 0:
            print(f"  Created {equipment_count}/300 equipment...")

print(f"✅ Equipment created: {equipment_count}")

# PHASE 2: Create LOCATED_AT relationships
print("\nPHASE 2: Creating LOCATED_AT relationships...")
relationships_count = 0

# Distribute 300 equipment across 40 facilities (7-8 per facility)
for fac_idx, (fac_id, fac_type, state, lat, lon) in enumerate(facilities):
    # 7 or 8 equipment per facility
    equipment_per_facility = 8 if fac_idx < 20 else 7

    for eq_offset in range(equipment_per_facility):
        eq_num = (fac_idx * 7) + eq_offset + (20 if fac_idx < 20 else 0)
        if eq_num >= 300:
            break
        eq_id = f"EQ-CHEM-{40000 + eq_num + 1}"

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
            if relationships_count % 30 == 0:
                print(f"  Created {relationships_count}/300 relationships...")

print(f"✅ Relationships created: {relationships_count}")

# PHASE 3: Apply 5-dimensional tags
print("\nPHASE 3: Applying 5-dimensional tags...")

get_equipment = """
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-CHEM-'
RETURN eq.equipmentId AS eqId, eq.equipmentType AS eqType,
       f.state AS state, f.facilityType AS facType
LIMIT 300;
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

    tags = ['CHEM_EQUIP', 'SECTOR_CHEMICAL']

    # GEO tags
    state_to_region = {
        'CA': 'WEST_COAST', 'TX': 'SOUTH', 'LA': 'SOUTH', 'AL': 'SOUTH', 'MS': 'SOUTH',
        'NJ': 'NORTHEAST', 'PA': 'NORTHEAST', 'MA': 'NORTHEAST',
        'OH': 'MIDWEST', 'IL': 'MIDWEST', 'MI': 'MIDWEST', 'IA': 'MIDWEST', 'KS': 'MIDWEST', 'NE': 'MIDWEST',
        'NC': 'SOUTH', 'TN': 'SOUTH', 'OK': 'SOUTH'
    }
    if state in state_to_region:
        tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])

    # OPS tags
    if 'Manufacturing' in fac_type:
        tags.extend(['OPS_FACILITY_MANUFACTURING', 'OPS_FUNCTION_CHEMICAL_PRODUCTION'])
    elif 'Petrochemical' in fac_type:
        tags.extend(['OPS_FACILITY_PETROCHEMICAL', 'OPS_FUNCTION_REFINING'])
    elif 'Pharmaceutical' in fac_type:
        tags.extend(['OPS_FACILITY_PHARMA', 'OPS_FUNCTION_DRUG_PRODUCTION'])
    elif 'Fertilizer' in fac_type:
        tags.extend(['OPS_FACILITY_FERTILIZER', 'OPS_FUNCTION_AGRICULTURAL_CHEM'])
    elif 'Storage' in fac_type:
        tags.extend(['OPS_FACILITY_STORAGE', 'OPS_FUNCTION_HAZMAT_STORAGE'])
    elif 'Waste' in fac_type:
        tags.extend(['OPS_FACILITY_WASTE_TREATMENT', 'OPS_FUNCTION_WASTE_PROCESSING'])

    # REG tags
    tags.extend(['REG_EPA_CAA', 'REG_EPA_RCRA', 'REG_OSHA_PSM'])
    if 'Petrochemical' in fac_type:
        tags.extend(['REG_EPA_RMP', 'REG_DHS_CFATS'])
    elif 'Hazardous' in fac_type or 'Waste' in fac_type:
        tags.extend(['REG_DHS_CFATS', 'REG_STATE_ENVIRONMENTAL'])

    # TECH tags
    if 'Reactor' in eq_type:
        tags.extend(['TECH_EQUIP_REACTOR', 'TECH_PROCESS_CONTROL'])
    elif 'Storage' in eq_type or 'Tank' in eq_type:
        tags.extend(['TECH_EQUIP_STORAGE', 'TECH_CONTAINMENT'])
    elif 'Control' in eq_type:
        tags.extend(['TECH_EQUIP_CONTROL', 'TECH_AUTOMATION'])
    elif 'Safety' in eq_type or 'Monitoring' in eq_type:
        tags.extend(['TECH_EQUIP_SAFETY', 'TECH_MONITORING'])
    elif 'Hazmat' in eq_type:
        tags.extend(['TECH_EQUIP_HAZMAT', 'TECH_MATERIAL_HANDLING'])
    elif 'Ventilation' in eq_type:
        tags.extend(['TECH_EQUIP_VENTILATION', 'TECH_AIR_QUALITY'])
    elif 'Shutdown' in eq_type:
        tags.extend(['TECH_EQUIP_EMERGENCY', 'TECH_SHUTDOWN_SYSTEMS'])
    elif 'Leak' in eq_type:
        tags.extend(['TECH_EQUIP_DETECTION', 'TECH_LEAK_MONITORING'])

    # TIME tags
    tags.extend(['TIME_ERA_CURRENT', 'TIME_MAINT_PRIORITY_CRITICAL'])

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
    if tags_count % 30 == 0:
        print(f"  Tagged {tags_count}/300 equipment...")

print(f"✅ Equipment tagged: {tags_count}")

# VERIFICATION
print("\n" + "═"*60)
print("VERIFICATION")
print("═"*60)

verify_queries = [
    ("Equipment count", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-CHEM-' RETURN COUNT(eq) AS count;"),
    ("Relationships count", "MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility) WHERE eq.equipmentId STARTS WITH 'EQ-CHEM-' RETURN COUNT(r) AS count, COUNT(DISTINCT eq) AS unique_equipment, COUNT(DISTINCT f) AS unique_facilities;"),
    ("Tag statistics", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-CHEM-' WITH eq, size(eq.tags) AS tc RETURN AVG(tc) AS avg_tags, MIN(tc) AS min_tags, MAX(tc) AS max_tags;")
]

for desc, query in verify_queries:
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )
    print(f"\n{desc}:")
    print(result.stdout)

print("\n✅ CHEMICAL SECTOR DEPLOYMENT COMPLETE")
