import subprocess
import json

# All 50 Transportation facilities
facilities = [
    ("TRANSPORT-ATL-001", "Airport", "GA"),
    ("TRANSPORT-ATL-FREIGHT-001", "Freight Terminal", "GA"),
    ("TRANSPORT-BAL-001", "Seaport", "MD"),
    ("TRANSPORT-BB-001", "Bridge", "NY"),
    ("TRANSPORT-BOS-001", "Airport", "MA"),
    ("TRANSPORT-BOS-SOUTH-001", "Railroad Station", "MA"),
    ("TRANSPORT-CHA-001", "Seaport", "SC"),
    ("TRANSPORT-CHI-FREIGHT-001", "Freight Terminal", "IL"),
    ("TRANSPORT-CHI-TMC-001", "Traffic Control Center", "IL"),
    ("TRANSPORT-CHI-UNION-001", "Railroad Station", "IL"),
    ("TRANSPORT-DAL-FREIGHT-001", "Freight Terminal", "TX"),
    ("TRANSPORT-DEN-001", "Airport", "CO"),
    ("TRANSPORT-DEN-UNION-001", "Railroad Station", "CO"),
    ("TRANSPORT-DFW-001", "Airport", "TX"),
    ("TRANSPORT-EWR-001", "Airport", "NJ"),
    ("TRANSPORT-GB-001", "Bridge", "CA"),
    ("TRANSPORT-GWB-001", "Bridge", "NY"),
    ("TRANSPORT-HOL-001", "Tunnel", "NY"),
    ("TRANSPORT-HOU-001", "Seaport", "TX"),
    ("TRANSPORT-HOU-TMC-001", "Traffic Control Center", "TX"),
    ("TRANSPORT-IAH-001", "Airport", "TX"),
    ("TRANSPORT-JFK-001", "Airport", "NY"),
    ("TRANSPORT-KC-UNION-001", "Railroad Station", "MO"),
    ("TRANSPORT-LA-FREIGHT-001", "Freight Terminal", "CA"),
    ("TRANSPORT-LA-TMC-001", "Traffic Control Center", "CA"),
    ("TRANSPORT-LALB-001", "Seaport", "CA"),
    ("TRANSPORT-LAX-001", "Airport", "CA"),
    ("TRANSPORT-LAX-UNION-001", "Railroad Station", "CA"),
    ("TRANSPORT-LC-001", "Tunnel", "NY"),
    ("TRANSPORT-MCO-001", "Airport", "FL"),
    ("TRANSPORT-MEM-FREIGHT-001", "Freight Terminal", "TN"),
    ("TRANSPORT-MIA-001", "Airport", "FL"),
    ("TRANSPORT-MIA-PORT-001", "Seaport", "FL"),
    ("TRANSPORT-MSP-001", "Airport", "MN"),
    ("TRANSPORT-NY-TMC-001", "Traffic Control Center", "NY"),
    ("TRANSPORT-NYC-PENN-001", "Railroad Station", "NY"),
    ("TRANSPORT-NYNJ-001", "Seaport", "NY"),
    ("TRANSPORT-OAK-001", "Seaport", "CA"),
    ("TRANSPORT-ORD-001", "Airport", "IL"),
    ("TRANSPORT-PHIL-30TH-001", "Railroad Station", "PA"),
    ("TRANSPORT-PHX-001", "Airport", "AZ"),
    ("TRANSPORT-PORT-UNION-001", "Railroad Station", "OR"),
    ("TRANSPORT-SAV-001", "Seaport", "GA"),
    ("TRANSPORT-SEA-001", "Airport", "WA"),
    ("TRANSPORT-SEA-KING-001", "Railroad Station", "WA"),
    ("TRANSPORT-SEA-PORT-001", "Seaport", "WA"),
    ("TRANSPORT-SF-TMC-001", "Traffic Control Center", "CA"),
    ("TRANSPORT-SFO-001", "Airport", "CA"),
    ("TRANSPORT-TAC-001", "Seaport", "WA"),
    ("TRANSPORT-WASH-UNION-001", "Railroad Station", "DC")
]

equipment_types = ['Radar System', 'Security Scanner', 'Navigation Equipment', 'Traffic Control System']
print(f"═══════════════════════════════════════════════════════════════")
print(f"TRANSPORTATION SECTOR DEPLOYMENT")
print(f"═══════════════════════════════════════════════════════════════")
print(f"Facilities: {len(facilities)}")
print(f"Target Equipment: 200 (4 per facility)")
print(f"Equipment Types: {', '.join(equipment_types)}")
print()

# PHASE 1: Create 200 Equipment nodes
print("PHASE 1: Creating 200 Transportation equipment nodes...")
equipment_count = 0
for i in range(200):
    eq_id = f"EQ-TRANS-{20000 + i + 1}"
    eq_type = equipment_types[i % len(equipment_types)]
    criticality = ['critical', 'high', 'medium'][i % 3]
    status = ['active', 'standby', 'maintenance'][i % 3]
    
    query = f"""
CREATE (eq:Equipment {{
  equipmentId: '{eq_id}',
  name: '{eq_type} Unit {i+1}',
  equipmentType: '{eq_type}',
  manufacturer: 'Manufacturer-{eq_type.replace(" ", "")}',
  model: '{eq_type.replace(" ", "-")}-2022',
  serial_number: 'SN-T-{200000 + i + 1}',
  installation_date: date('2022-01-01'),
  operational_status: '{status}',
  criticality_level: '{criticality}',
  tags: ['TRANS_EQUIP', 'SECTOR_TRANSPORTATION'],
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
        if equipment_count % 25 == 0:
            print(f"  Created {equipment_count}/200 equipment...")

print(f"✅ Equipment created: {equipment_count}")

# PHASE 2: Create LOCATED_AT relationships
print("\nPHASE 2: Creating LOCATED_AT relationships...")
relationships_count = 0
for fac_idx, (fac_id, fac_type, state) in enumerate(facilities):
    # Each facility gets 4 equipment
    for eq_offset in range(4):
        eq_num = (fac_idx * 4) + eq_offset
        if eq_num >= 200:
            break
        eq_id = f"EQ-TRANS-{20000 + eq_num + 1}"
        
        query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}}), (f:Facility {{facilityId: '{fac_id}'}})
CREATE (eq)-[:LOCATED_AT {{
  installation_date: eq.installation_date,
  location: 'Zone {eq_offset + 1}',
  exact_coordinates: point({{latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005}})
}}]->(f);
"""
        
        result = subprocess.run(
            ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            relationships_count += 1
            if relationships_count % 25 == 0:
                print(f"  Created {relationships_count}/200 relationships...")

print(f"✅ Relationships created: {relationships_count}")

# PHASE 3: Apply 5-dimensional tags
print("\nPHASE 3: Applying 5-dimensional tags...")

# Get all equipment with facility info
get_equipment = """
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'
RETURN eq.equipmentId AS eqId, eq.equipmentType AS eqType, 
       f.state AS state, f.facilityType AS facType
LIMIT 200;
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
    
    tags = ['TRANS_EQUIP', 'SECTOR_TRANSPORTATION']
    
    # GEO tags - state and region
    state_to_region = {
        'CA': 'WEST_COAST', 'OR': 'NORTHWEST', 'WA': 'NORTHWEST',
        'MA': 'NORTHEAST', 'NY': 'NORTHEAST', 'PA': 'NORTHEAST', 'NJ': 'NORTHEAST', 'MD': 'NORTHEAST', 'DC': 'NORTHEAST',
        'IL': 'MIDWEST', 'MN': 'MIDWEST', 'MO': 'MIDWEST',
        'TX': 'SOUTH', 'FL': 'SOUTH', 'GA': 'SOUTH', 'SC': 'SOUTH', 'TN': 'SOUTH',
        'CO': 'MOUNTAIN', 'AZ': 'MOUNTAIN'
    }
    if state in state_to_region:
        tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])
    
    # OPS tags - facility type
    if fac_type == 'Airport':
        tags.extend(['OPS_FACILITY_AIRPORT', 'OPS_FUNCTION_AVIATION'])
    elif fac_type == 'Seaport':
        tags.extend(['OPS_FACILITY_SEAPORT', 'OPS_FUNCTION_MARITIME'])
    elif fac_type == 'Railroad Station':
        tags.extend(['OPS_FACILITY_RAILROAD', 'OPS_FUNCTION_RAIL_PASSENGER'])
    elif fac_type == 'Freight Terminal':
        tags.extend(['OPS_FACILITY_FREIGHT', 'OPS_FUNCTION_CARGO'])
    elif fac_type == 'Bridge':
        tags.extend(['OPS_FACILITY_BRIDGE', 'OPS_FUNCTION_HIGHWAY'])
    elif fac_type == 'Tunnel':
        tags.extend(['OPS_FACILITY_TUNNEL', 'OPS_FUNCTION_HIGHWAY'])
    elif fac_type == 'Traffic Control Center':
        tags.extend(['OPS_FACILITY_CONTROL', 'OPS_FUNCTION_TRAFFIC_MGMT'])
    
    # REG tags - regulatory compliance
    if fac_type == 'Airport':
        tags.extend(['REG_TSA_AVIATION_SEC', 'REG_FAA_AIRSPACE'])
    elif fac_type == 'Seaport':
        tags.extend(['REG_USCG_MARITIME', 'REG_MTSA_SECURITY'])
    elif fac_type in ['Railroad Station', 'Freight Terminal']:
        tags.extend(['REG_DOT_RAIL_SAFETY', 'REG_FRA_COMPLIANCE'])
    elif fac_type in ['Bridge', 'Tunnel']:
        tags.extend(['REG_DOT_HIGHWAY_SAFETY', 'REG_FHWA_STANDARDS'])
    elif fac_type == 'Traffic Control Center':
        tags.extend(['REG_DOT_ITS', 'REG_STATE_TRANSPORT'])
    
    # TECH tags - equipment specific
    if 'Radar' in eq_type:
        tags.extend(['TECH_EQUIP_RADAR', 'TECH_DETECTION'])
    elif 'Scanner' in eq_type:
        tags.extend(['TECH_EQUIP_SCANNER', 'TECH_SECURITY'])
    elif 'Navigation' in eq_type:
        tags.extend(['TECH_EQUIP_NAV', 'TECH_GUIDANCE'])
    elif 'Traffic Control' in eq_type:
        tags.extend(['TECH_EQUIP_CONTROL', 'TECH_AUTOMATION'])
    
    # TIME tags
    tags.extend(['TIME_ERA_CURRENT', 'TIME_MAINT_PRIORITY_MEDIUM'])
    
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
    if tags_count % 25 == 0:
        print(f"  Tagged {tags_count}/200 equipment...")

print(f"✅ Equipment tagged: {tags_count}")

# VERIFICATION
print("\n" + "═"*60)
print("VERIFICATION")
print("═"*60)

verify_queries = [
    ("Equipment count", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-' RETURN COUNT(eq) AS count;"),
    ("Relationships count", "MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility) WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-' RETURN COUNT(r) AS count, COUNT(DISTINCT eq) AS unique_equipment, COUNT(DISTINCT f) AS unique_facilities;"),
    ("Tag statistics", "MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-' WITH eq, size(eq.tags) AS tc RETURN AVG(tc) AS avg_tags, MIN(tc) AS min_tags, MAX(tc) AS max_tags;")
]

for desc, query in verify_queries:
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )
    print(f"\n{desc}:")
    print(result.stdout)

print("\n✅ TRANSPORTATION SECTOR DEPLOYMENT COMPLETE")
