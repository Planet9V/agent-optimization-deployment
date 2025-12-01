import subprocess
import json

# Healthcare Sector: 60 facilities, 500 equipment
# Applying PATTERN-7: Comprehensive 3-Phase Deployment Script

facilities = [
    # Major Hospitals (20)
    ("HEALTH-ATL-001", "Hospital", "GA", 33.7490, -84.3880),
    ("HEALTH-BOS-001", "Hospital", "MA", 42.3601, -71.0589),
    ("HEALTH-CHI-001", "Hospital", "IL", 41.8781, -87.6298),
    ("HEALTH-DAL-001", "Hospital", "TX", 32.7767, -96.7970),
    ("HEALTH-DEN-001", "Hospital", "CO", 39.7392, -104.9903),
    ("HEALTH-HOU-001", "Hospital", "TX", 29.7604, -95.3698),
    ("HEALTH-LA-001", "Hospital", "CA", 34.0522, -118.2437),
    ("HEALTH-MIA-001", "Hospital", "FL", 25.7617, -80.1918),
    ("HEALTH-NY-001", "Hospital", "NY", 40.7128, -74.0060),
    ("HEALTH-PHI-001", "Hospital", "PA", 39.9526, -75.1652),
    ("HEALTH-PHX-001", "Hospital", "AZ", 33.4484, -112.0740),
    ("HEALTH-SD-001", "Hospital", "CA", 32.7157, -117.1611),
    ("HEALTH-SEA-001", "Hospital", "WA", 47.6062, -122.3321),
    ("HEALTH-SF-001", "Hospital", "CA", 37.7749, -122.4194),
    ("HEALTH-DC-001", "Hospital", "DC", 38.9072, -77.0369),
    ("HEALTH-BAL-001", "Hospital", "MD", 39.2904, -76.6122),
    ("HEALTH-MIN-001", "Hospital", "MN", 44.9778, -93.2650),
    ("HEALTH-DET-001", "Hospital", "MI", 42.3314, -83.0458),
    ("HEALTH-POR-001", "Hospital", "OR", 45.5152, -122.6784),
    ("HEALTH-CLE-001", "Hospital", "OH", 41.4993, -81.6944),

    # Medical Centers (10)
    ("HEALTH-ATL-MC-001", "Medical Center", "GA", 33.7550, -84.3950),
    ("HEALTH-BOS-MC-001", "Medical Center", "MA", 42.3651, -71.0639),
    ("HEALTH-CHI-MC-001", "Medical Center", "IL", 41.8831, -87.6348),
    ("HEALTH-LA-MC-001", "Medical Center", "CA", 34.0572, -118.2487),
    ("HEALTH-NY-MC-001", "Medical Center", "NY", 40.7178, -74.0110),
    ("HEALTH-HOU-MC-001", "Medical Center", "TX", 29.7654, -95.3748),
    ("HEALTH-PHI-MC-001", "Medical Center", "PA", 39.9576, -75.1702),
    ("HEALTH-SF-MC-001", "Medical Center", "CA", 37.7799, -122.4244),
    ("HEALTH-SEA-MC-001", "Medical Center", "WA", 47.6112, -122.3371),
    ("HEALTH-DC-MC-001", "Medical Center", "DC", 38.9122, -77.0419),

    # Public Health Laboratories (8)
    ("HEALTH-ATL-LAB-001", "Public Health Laboratory", "GA", 33.7600, -84.4000),
    ("HEALTH-CHI-LAB-001", "Public Health Laboratory", "IL", 41.8881, -87.6398),
    ("HEALTH-LA-LAB-001", "Public Health Laboratory", "CA", 34.0622, -118.2537),
    ("HEALTH-NY-LAB-001", "Public Health Laboratory", "NY", 40.7228, -74.0160),
    ("HEALTH-HOU-LAB-001", "Public Health Laboratory", "TX", 29.7704, -95.3798),
    ("HEALTH-SF-LAB-001", "Public Health Laboratory", "CA", 37.7849, -122.4294),
    ("HEALTH-SEA-LAB-001", "Public Health Laboratory", "WA", 47.6162, -122.3421),
    ("HEALTH-DC-LAB-001", "Public Health Laboratory", "DC", 38.9172, -77.0469),

    # Pharmaceutical Manufacturing (6)
    ("HEALTH-NJ-PHARMA-001", "Pharmaceutical Manufacturing", "NJ", 40.7357, -74.1724),
    ("HEALTH-PA-PHARMA-001", "Pharmaceutical Manufacturing", "PA", 40.2732, -76.8867),
    ("HEALTH-CA-PHARMA-001", "Pharmaceutical Manufacturing", "CA", 37.3875, -121.9636),
    ("HEALTH-MA-PHARMA-001", "Pharmaceutical Manufacturing", "MA", 42.3736, -71.1097),
    ("HEALTH-NC-PHARMA-001", "Pharmaceutical Manufacturing", "NC", 35.7796, -78.6382),
    ("HEALTH-IL-PHARMA-001", "Pharmaceutical Manufacturing", "IL", 41.8500, -87.6500),

    # Blood Banks (6)
    ("HEALTH-NY-BLOOD-001", "Blood Bank", "NY", 40.7278, -74.0210),
    ("HEALTH-LA-BLOOD-001", "Blood Bank", "CA", 34.0672, -118.2587),
    ("HEALTH-CHI-BLOOD-001", "Blood Bank", "IL", 41.8931, -87.6448),
    ("HEALTH-HOU-BLOOD-001", "Blood Bank", "TX", 29.7754, -95.3848),
    ("HEALTH-PHI-BLOOD-001", "Blood Bank", "PA", 39.9626, -75.1752),
    ("HEALTH-SF-BLOOD-001", "Blood Bank", "CA", 37.7899, -122.4344),

    # Nursing Homes (10)
    ("HEALTH-ATL-NH-001", "Nursing Home", "GA", 33.7650, -84.4050),
    ("HEALTH-BOS-NH-001", "Nursing Home", "MA", 42.3701, -71.0689),
    ("HEALTH-CHI-NH-001", "Nursing Home", "IL", 41.8981, -87.6498),
    ("HEALTH-LA-NH-001", "Nursing Home", "CA", 34.0722, -118.2637),
    ("HEALTH-NY-NH-001", "Nursing Home", "NY", 40.7328, -74.0260),
    ("HEALTH-HOU-NH-001", "Nursing Home", "TX", 29.7804, -95.3898),
    ("HEALTH-PHI-NH-001", "Nursing Home", "PA", 39.9676, -75.1802),
    ("HEALTH-SF-NH-001", "Nursing Home", "CA", 37.7949, -122.4394),
    ("HEALTH-SEA-NH-001", "Nursing Home", "WA", 47.6212, -122.3471),
    ("HEALTH-MIA-NH-001", "Nursing Home", "FL", 25.7667, -80.1968)
]

equipment_types = [
    'Medical Imaging Equipment',
    'Life Support Systems',
    'Laboratory Equipment',
    'Surgical Equipment',
    'Patient Monitoring Systems',
    'Sterilization Equipment',
    'HVAC Systems',
    'Emergency Power Systems'
]

print(f"═══════════════════════════════════════════════════════════════")
print(f"HEALTHCARE SECTOR DEPLOYMENT")
print(f"═══════════════════════════════════════════════════════════════")
print(f"Facilities: {len(facilities)}")
print(f"Target Equipment: 500")
print(f"Equipment Types: {', '.join(equipment_types)}")
print()

# PHASE 1: Create 500 Equipment nodes
print("PHASE 1: Creating 500 Healthcare equipment nodes...")
equipment_count = 0
for i in range(500):
    eq_id = f"EQ-HEALTH-{30000 + i + 1}"
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
  serial_number: 'SN-H-{300000 + i + 1}',
  installation_date: date('2023-01-01'),
  operational_status: '{status}',
  criticality_level: '{criticality}',
  tags: ['HEALTH_EQUIP', 'SECTOR_HEALTHCARE'],
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
        if equipment_count % 50 == 0:
            print(f"  Created {equipment_count}/500 equipment...")

print(f"✅ Equipment created: {equipment_count}")

# PHASE 2: Create LOCATED_AT relationships
print("\nPHASE 2: Creating LOCATED_AT relationships...")
relationships_count = 0

# Distribute 500 equipment across 60 facilities (~8-9 per facility)
for fac_idx, (fac_id, fac_type, state, lat, lon) in enumerate(facilities):
    # Calculate equipment per facility (8 or 9)
    equipment_per_facility = 9 if fac_idx < 20 else 8

    for eq_offset in range(equipment_per_facility):
        eq_num = (fac_idx * 8) + eq_offset + (20 if fac_idx < 20 else 0)
        if eq_num >= 500:
            break
        eq_id = f"EQ-HEALTH-{30000 + eq_num + 1}"

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
            if relationships_count % 50 == 0:
                print(f"  Created {relationships_count}/500 relationships...")

print(f"✅ Relationships created: {relationships_count}")

# PHASE 3: Apply 5-dimensional tags
print("\nPHASE 3: Applying 5-dimensional tags...")

# Get all equipment with facility info
get_equipment = """
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN eq.equipmentId AS eqId, eq.equipmentType AS eqType,
       f.state AS state, f.facilityType AS facType
LIMIT 500;
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

    tags = ['HEALTH_EQUIP', 'SECTOR_HEALTHCARE']

    # GEO tags - state and region
    state_to_region = {
        'CA': 'WEST_COAST', 'OR': 'NORTHWEST', 'WA': 'NORTHWEST',
        'MA': 'NORTHEAST', 'NY': 'NORTHEAST', 'PA': 'NORTHEAST', 'NJ': 'NORTHEAST', 'MD': 'NORTHEAST', 'DC': 'NORTHEAST',
        'IL': 'MIDWEST', 'MN': 'MIDWEST', 'OH': 'MIDWEST', 'MI': 'MIDWEST',
        'TX': 'SOUTH', 'FL': 'SOUTH', 'GA': 'SOUTH', 'NC': 'SOUTH',
        'CO': 'MOUNTAIN', 'AZ': 'MOUNTAIN'
    }
    if state in state_to_region:
        tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])

    # OPS tags - facility type
    if 'Hospital' in fac_type:
        tags.extend(['OPS_FACILITY_HOSPITAL', 'OPS_FUNCTION_PATIENT_CARE'])
    elif 'Medical Center' in fac_type:
        tags.extend(['OPS_FACILITY_MEDICAL_CENTER', 'OPS_FUNCTION_MULTI_SPECIALTY'])
    elif 'Laboratory' in fac_type:
        tags.extend(['OPS_FACILITY_LABORATORY', 'OPS_FUNCTION_DIAGNOSTIC'])
    elif 'Pharmaceutical' in fac_type:
        tags.extend(['OPS_FACILITY_PHARMA', 'OPS_FUNCTION_DRUG_MANUFACTURING'])
    elif 'Blood Bank' in fac_type:
        tags.extend(['OPS_FACILITY_BLOOD_BANK', 'OPS_FUNCTION_BLOOD_SERVICES'])
    elif 'Nursing Home' in fac_type:
        tags.extend(['OPS_FACILITY_NURSING_HOME', 'OPS_FUNCTION_LONG_TERM_CARE'])

    # REG tags - regulatory compliance
    tags.extend(['REG_HIPAA_COMPLIANCE', 'REG_OSHA_HEALTHCARE'])
    if 'Hospital' in fac_type or 'Medical Center' in fac_type:
        tags.extend(['REG_CMS_STANDARDS', 'REG_JCAHO_ACCREDITATION'])
    elif 'Laboratory' in fac_type:
        tags.extend(['REG_CDC_GUIDELINES', 'REG_STATE_HEALTH_DEPT'])
    elif 'Pharmaceutical' in fac_type:
        tags.extend(['REG_FDA_APPROVAL', 'REG_DEA_COMPLIANCE'])

    # TECH tags - equipment specific
    if 'Imaging' in eq_type:
        tags.extend(['TECH_EQUIP_IMAGING', 'TECH_DIAGNOSTIC'])
    elif 'Life Support' in eq_type:
        tags.extend(['TECH_EQUIP_LIFE_SUPPORT', 'TECH_CRITICAL_CARE'])
    elif 'Laboratory' in eq_type:
        tags.extend(['TECH_EQUIP_LAB', 'TECH_ANALYSIS'])
    elif 'Surgical' in eq_type:
        tags.extend(['TECH_EQUIP_SURGICAL', 'TECH_OPERATIVE'])
    elif 'Monitoring' in eq_type:
        tags.extend(['TECH_EQUIP_MONITORING', 'TECH_PATIENT_TRACKING'])
    elif 'Sterilization' in eq_type:
        tags.extend(['TECH_EQUIP_STERILIZATION', 'TECH_INFECTION_CONTROL'])
    elif 'HVAC' in eq_type:
        tags.extend(['TECH_EQUIP_HVAC', 'TECH_ENVIRONMENTAL_CONTROL'])
    elif 'Power' in eq_type:
        tags.extend(['TECH_EQUIP_POWER', 'TECH_BACKUP_SYSTEMS'])

    # TIME tags
    tags.extend(['TIME_ERA_CURRENT', 'TIME_MAINT_PRIORITY_HIGH'])

    # Update equipment
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
    if tags_count % 50 == 0:
        print(f"  Tagged {tags_count}/500 equipment...")

print(f"✅ Equipment tagged: {tags_count}")

# VERIFICATION
print("\n" + "═"*60)
print("VERIFICATION")
print("═"*60)

verify_queries = [
    ("Equipment count", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' RETURN COUNT(eq) AS count;"),
    ("Relationships count", "MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility) WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' RETURN COUNT(r) AS count, COUNT(DISTINCT eq) AS unique_equipment, COUNT(DISTINCT f) AS unique_facilities;"),
    ("Tag statistics", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' WITH eq, size(eq.tags) AS tc RETURN AVG(tc) AS avg_tags, MIN(tc) AS min_tags, MAX(tc) AS max_tags;")
]

for desc, query in verify_queries:
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )
    print(f"\n{desc}:")
    print(result.stdout)

print("\n✅ HEALTHCARE SECTOR DEPLOYMENT COMPLETE")
