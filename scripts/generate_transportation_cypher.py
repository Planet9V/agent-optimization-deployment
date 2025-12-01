#!/usr/bin/env python3
"""
Generate complete Cypher deployment file for Transportation sector
200 equipment nodes + 200 LOCATED_AT relationships + 5D tagging
"""

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

state_to_region = {
    'CA': 'WEST_COAST', 'OR': 'NORTHWEST', 'WA': 'NORTHWEST',
    'MA': 'NORTHEAST', 'NY': 'NORTHEAST', 'PA': 'NORTHEAST', 'NJ': 'NORTHEAST', 'MD': 'NORTHEAST', 'DC': 'NORTHEAST',
    'IL': 'MIDWEST', 'MN': 'MIDWEST', 'MO': 'MIDWEST',
    'TX': 'SOUTH', 'FL': 'SOUTH', 'GA': 'SOUTH', 'SC': 'SOUTH', 'TN': 'SOUTH',
    'CO': 'MOUNTAIN', 'AZ': 'MOUNTAIN'
}

def get_tags_for_equipment(eq_num, eq_type, fac_type, state):
    """Generate 5-dimensional tags for equipment"""
    tags = ['TRANS_EQUIP', 'SECTOR_TRANSPORTATION']

    # GEO tags
    if state in state_to_region:
        tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])

    # OPS tags
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

    # REG tags
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

    # TECH tags
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

    return tags

# Generate Cypher file
output = []
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("// GAP-004 TRANSPORTATION SECTOR DEPLOYMENT")
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("// Equipment: 200 nodes (EQ-TRANS-20001 to EQ-TRANS-20200)")
output.append("// Facilities: 50 transportation hubs")
output.append("// Relationships: 200 LOCATED_AT (4 equipment per facility)")
output.append("// Tagging: 5-dimensional (GEO, OPS, REG, TECH, TIME)")
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("")

# Generate all 200 equipment CREATE statements
for i in range(200):
    eq_id = f"EQ-TRANS-{20001 + i}"
    eq_type = equipment_types[i % len(equipment_types)]
    criticality = ['critical', 'high', 'medium'][i % 3]
    status = ['active', 'standby', 'maintenance'][i % 3]

    # Determine facility for this equipment (4 per facility)
    fac_idx = i // 4
    if fac_idx < len(facilities):
        fac_id, fac_type, state = facilities[fac_idx]
        tags = get_tags_for_equipment(i, eq_type, fac_type, state)
        tags_str = str(tags).replace("'", '"')

        output.append(f"CREATE (eq:Equipment {{")
        output.append(f"  equipmentId: '{eq_id}',")
        output.append(f"  name: '{eq_type} Unit {i+1}',")
        output.append(f"  equipmentType: '{eq_type}',")
        output.append(f"  manufacturer: 'Manufacturer-{eq_type.replace(' ', '')}',")
        output.append(f"  model: '{eq_type.replace(' ', '-')}-2022',")
        output.append(f"  serial_number: 'SN-T-{200001 + i}',")
        output.append(f"  installation_date: date('2022-01-01'),")
        output.append(f"  operational_status: '{status}',")
        output.append(f"  criticality_level: '{criticality}',")
        output.append(f"  tags: {tags_str},")
        output.append(f"  created_date: datetime(),")
        output.append(f"  updated_date: datetime()")
        output.append(f"}});")
        output.append("")

output.append("// ═══════════════════════════════════════════════════════════════")
output.append("// RELATIONSHIPS: LOCATED_AT (200 relationships)")
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("")

# Generate all 200 LOCATED_AT relationships
for fac_idx, (fac_id, fac_type, state) in enumerate(facilities):
    for eq_offset in range(4):
        eq_num = (fac_idx * 4) + eq_offset
        if eq_num >= 200:
            break
        eq_id = f"EQ-TRANS-{20001 + eq_num}"
        zone = eq_offset + 1

        output.append(f"MATCH (eq:Equipment {{equipmentId: '{eq_id}'}}), (f:Facility {{facilityId: '{fac_id}'}})")
        output.append(f"CREATE (eq)-[:LOCATED_AT {{")
        output.append(f"  installation_date: date('2022-01-01'),")
        output.append(f"  location: 'Zone {zone}',")
        output.append(f"  exact_coordinates: point({{latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005}})")
        output.append(f"}}]->(f);")
        output.append("")

output.append("// ═══════════════════════════════════════════════════════════════")
output.append("// VERIFICATION QUERIES")
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("")
output.append("// Count equipment")
output.append("MATCH (eq:Equipment)")
output.append("WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'")
output.append("RETURN COUNT(eq) AS equipment_count;")
output.append("")
output.append("// Count relationships")
output.append("MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)")
output.append("WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'")
output.append("RETURN COUNT(r) AS relationship_count,")
output.append("       COUNT(DISTINCT eq) AS unique_equipment,")
output.append("       COUNT(DISTINCT f) AS unique_facilities;")
output.append("")
output.append("// Tag statistics")
output.append("MATCH (eq:Equipment)")
output.append("WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'")
output.append("WITH eq, size(eq.tags) AS tag_count")
output.append("RETURN AVG(tag_count) AS avg_tags,")
output.append("       MIN(tag_count) AS min_tags,")
output.append("       MAX(tag_count) AS max_tags;")
output.append("")
output.append("// ═══════════════════════════════════════════════════════════════")
output.append("// END OF TRANSPORTATION SECTOR DEPLOYMENT")
output.append("// ═══════════════════════════════════════════════════════════════")

# Write to file
with open('/home/jim/2_OXOT_Projects_Dev/scripts/gap004_transportation_sector.cypher', 'w') as f:
    f.write('\n'.join(output))

print(f"✅ Generated complete Cypher file with {len([l for l in output if 'CREATE (eq:Equipment' in l])} equipment nodes")
print(f"✅ Generated {len([l for l in output if 'CREATE (eq)-[:LOCATED_AT' in l])} LOCATED_AT relationships")
print(f"✅ File: /home/jim/2_OXOT_Projects_Dev/scripts/gap004_transportation_sector.cypher")
