import subprocess
import json

print("=" * 70)
print("PHASE 3: Apply 5-Dimensional Tags to ALL 3 Sectors")
print("Healthcare (500) + Chemical (300) + Manufacturing (400) = 1,200 Equipment")
print("=" * 70)
print()

def apply_5d_tags(sector_name, equipment_prefix):
    """Apply 5-dimensional tagging to equipment in a sector"""
    print(f"\n{'─' * 70}")
    print(f"{sector_name} SECTOR - Applying 5D Tags")
    print(f"{'─' * 70}")

    # Get equipment with facility context
    get_equipment = f"""
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH '{equipment_prefix}'
RETURN eq.equipmentId AS eqId, eq.equipmentType AS eqType,
       f.state AS state, f.facilityType AS facType
ORDER BY eq.equipmentId;
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

        # Base tags
        base_tag = f'SECTOR_{sector_name.upper()}'
        tags = [f'{sector_name.upper()}_EQUIP', base_tag]

        # GEO tags
        state_to_region = {
            'CA': 'WEST_COAST', 'OR': 'NORTHWEST', 'WA': 'NORTHWEST',
            'TX': 'SOUTH', 'LA': 'SOUTH', 'AL': 'SOUTH', 'MS': 'SOUTH', 'FL': 'SOUTH', 'GA': 'SOUTH', 'TN': 'SOUTH', 'KY': 'SOUTH', 'SC': 'SOUTH', 'NC': 'SOUTH', 'VA': 'SOUTH', 'OK': 'SOUTH',
            'MI': 'MIDWEST', 'OH': 'MIDWEST', 'IN': 'MIDWEST', 'IL': 'MIDWEST', 'MO': 'MIDWEST', 'WI': 'MIDWEST', 'IA': 'MIDWEST', 'KS': 'MIDWEST', 'NE': 'MIDWEST', 'MN': 'MIDWEST',
            'NY': 'NORTHEAST', 'PA': 'NORTHEAST', 'NJ': 'NORTHEAST', 'MA': 'NORTHEAST', 'CT': 'NORTHEAST', 'ME': 'NORTHEAST',
            'AZ': 'MOUNTAIN', 'CO': 'MOUNTAIN', 'UT': 'MOUNTAIN', 'NV': 'MOUNTAIN', 'MT': 'MOUNTAIN'
        }
        if state in state_to_region:
            tags.extend([f'GEO_REGION_{state_to_region[state]}', f'GEO_STATE_{state}'])

        # OPS tags (sector-specific)
        if sector_name == 'HEALTHCARE':
            if 'Hospital' in fac_type:
                tags.extend(['OPS_FACILITY_HOSPITAL', 'OPS_FUNCTION_PATIENT_CARE'])
            elif 'Medical Center' in fac_type:
                tags.extend(['OPS_FACILITY_MEDICAL_CENTER', 'OPS_FUNCTION_HEALTHCARE'])
            elif 'Urgent Care' in fac_type:
                tags.extend(['OPS_FACILITY_URGENT_CARE', 'OPS_FUNCTION_EMERGENCY'])
            elif 'Clinic' in fac_type:
                tags.extend(['OPS_FACILITY_CLINIC', 'OPS_FUNCTION_OUTPATIENT'])
            elif 'Rehabilitation' in fac_type:
                tags.extend(['OPS_FACILITY_REHAB', 'OPS_FUNCTION_THERAPY'])
            elif 'Laboratory' in fac_type:
                tags.extend(['OPS_FACILITY_LAB', 'OPS_FUNCTION_DIAGNOSTICS'])

        elif sector_name == 'CHEMICAL':
            if 'Manufacturing' in fac_type:
                tags.extend(['OPS_FACILITY_MANUFACTURING', 'OPS_FUNCTION_CHEMICAL_PRODUCTION'])
            elif 'Petrochemical' in fac_type:
                tags.extend(['OPS_FACILITY_PETROCHEMICAL', 'OPS_FUNCTION_REFINING'])
            elif 'Pharmaceutical' in fac_type:
                tags.extend(['OPS_FACILITY_PHARMA', 'OPS_FUNCTION_DRUG_PRODUCTION'])
            elif 'Fertilizer' in fac_type:
                tags.extend(['OPS_FACILITY_FERTILIZER', 'OPS_FUNCTION_AGRICULTURAL_CHEM'])
            elif 'Storage' in fac_type or 'Hazardous' in fac_type:
                tags.extend(['OPS_FACILITY_STORAGE', 'OPS_FUNCTION_HAZMAT_STORAGE'])
            elif 'Waste' in fac_type:
                tags.extend(['OPS_FACILITY_WASTE_TREATMENT', 'OPS_FUNCTION_WASTE_PROCESSING'])

        elif sector_name == 'MANUFACTURING':
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

        # REG tags (sector-specific)
        if sector_name == 'HEALTHCARE':
            tags.extend(['REG_HIPAA_COMPLIANCE', 'REG_FDA_REGULATION', 'REG_STATE_HEALTH'])
            if 'Hospital' in fac_type or 'Medical Center' in fac_type:
                tags.extend(['REG_CMS_COMPLIANCE', 'REG_JOINT_COMMISSION'])

        elif sector_name == 'CHEMICAL':
            tags.extend(['REG_EPA_CAA', 'REG_EPA_RCRA', 'REG_OSHA_PSM'])
            if 'Petrochemical' in fac_type or 'Hazardous' in fac_type:
                tags.extend(['REG_EPA_RMP', 'REG_DHS_CFATS'])
            elif 'Pharmaceutical' in fac_type:
                tags.extend(['REG_FDA_PHARMA', 'REG_GMP_COMPLIANCE'])

        elif sector_name == 'MANUFACTURING':
            tags.extend(['REG_OSHA_MANUFACTURING', 'REG_EPA_AIR_QUALITY'])
            if 'Defense' in fac_type:
                tags.extend(['REG_DOD_CMMC', 'REG_ITAR_COMPLIANCE'])
            elif 'Automotive' in fac_type or 'Aerospace' in fac_type:
                tags.extend(['REG_ISO_9001', 'REG_NIST_COMPLIANCE'])

        # TECH tags (equipment-specific)
        tech_mapping = {
            'Medical Imaging': ['TECH_EQUIP_IMAGING', 'TECH_DIAGNOSTICS'],
            'Life Support': ['TECH_EQUIP_LIFE_SUPPORT', 'TECH_CRITICAL_CARE'],
            'Laboratory Equipment': ['TECH_EQUIP_LAB', 'TECH_ANALYSIS'],
            'Surgical Equipment': ['TECH_EQUIP_SURGICAL', 'TECH_PRECISION'],
            'Patient Monitoring': ['TECH_EQUIP_MONITORING', 'TECH_SENSORS'],
            'Sterilization': ['TECH_EQUIP_STERILIZATION', 'TECH_SAFETY'],
            'Reactor Vessels': ['TECH_EQUIP_REACTOR', 'TECH_PROCESS_CONTROL'],
            'Storage Tanks': ['TECH_EQUIP_STORAGE', 'TECH_CONTAINMENT'],
            'Process Control': ['TECH_EQUIP_CONTROL', 'TECH_AUTOMATION'],
            'Safety Monitoring': ['TECH_EQUIP_SAFETY', 'TECH_MONITORING'],
            'Hazmat Handling': ['TECH_EQUIP_HAZMAT', 'TECH_MATERIAL_HANDLING'],
            'Ventilation': ['TECH_EQUIP_VENTILATION', 'TECH_AIR_QUALITY'],
            'Emergency Shutdown': ['TECH_EQUIP_EMERGENCY', 'TECH_SHUTDOWN_SYSTEMS'],
            'Leak Detection': ['TECH_EQUIP_DETECTION', 'TECH_LEAK_MONITORING'],
            'CNC Machines': ['TECH_EQUIP_CNC', 'TECH_PRECISION_MACHINING'],
            'Industrial Robots': ['TECH_EQUIP_ROBOTICS', 'TECH_AUTOMATION'],
            'Welding': ['TECH_EQUIP_WELDING', 'TECH_JOINING'],
            'Assembly Line': ['TECH_EQUIP_ASSEMBLY', 'TECH_PRODUCTION_LINE'],
            'Quality Control': ['TECH_EQUIP_QC', 'TECH_INSPECTION'],
            'Material Handling': ['TECH_EQUIP_MATERIAL_HANDLING', 'TECH_LOGISTICS'],
            'HVAC': ['TECH_EQUIP_HVAC', 'TECH_CLIMATE_CONTROL'],
            'Safety Systems': ['TECH_EQUIP_SAFETY', 'TECH_PROTECTION']
        }
        for key, tech_tags in tech_mapping.items():
            if key in eq_type:
                tags.extend(tech_tags)
                break

        # TIME tags
        tags.extend(['TIME_ERA_CURRENT'])
        if sector_name == 'HEALTHCARE' or sector_name == 'CHEMICAL':
            tags.append('TIME_MAINT_PRIORITY_CRITICAL')
        else:
            tags.append('TIME_MAINT_PRIORITY_HIGH')

        # Update equipment tags
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
            print(f"  Tagged {tags_count} equipment...")

    print(f"✅ {sector_name} equipment tagged: {tags_count}")
    return tags_count

# Execute tagging for all 3 sectors
total_tagged = 0

print("\n" + "=" * 70)
print("APPLYING 5-DIMENSIONAL TAGS")
print("=" * 70)

total_tagged += apply_5d_tags("HEALTHCARE", "EQ-HEALTH-")
total_tagged += apply_5d_tags("CHEMICAL", "EQ-CHEM-")
total_tagged += apply_5d_tags("MANUFACTURING", "EQ-MFG-")

# FINAL VERIFICATION
print("\n" + "=" * 70)
print("FINAL VERIFICATION - TAG STATISTICS")
print("=" * 70)

verify = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
     """MATCH (eq:Equipment)
     WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' OR eq.equipmentId STARTS WITH 'EQ-CHEM-' OR eq.equipmentId STARTS WITH 'EQ-MFG-'
     WITH eq, size(eq.tags) AS tc
     RETURN AVG(tc) AS avg_tags, MIN(tc) AS min_tags, MAX(tc) AS max_tags, COUNT(eq) AS total_equipment;"""],
    capture_output=True,
    text=True
)
print("\nOverall Tag Statistics:")
print(verify.stdout)

sector_verify = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
     """MATCH (eq:Equipment)
     WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' OR eq.equipmentId STARTS WITH 'EQ-CHEM-' OR eq.equipmentId STARTS WITH 'EQ-MFG-'
     WITH eq.equipmentId AS eqId, size(eq.tags) AS tc
     RETURN
       CASE
         WHEN eqId STARTS WITH 'EQ-HEALTH-' THEN 'Healthcare'
         WHEN eqId STARTS WITH 'EQ-CHEM-' THEN 'Chemical'
         WHEN eqId STARTS WITH 'EQ-MFG-' THEN 'Manufacturing'
       END AS sector,
       AVG(tc) AS avg_tags,
       MIN(tc) AS min_tags,
       MAX(tc) AS max_tags,
       COUNT(*) AS equipment_count
     ORDER BY sector;"""],
    capture_output=True,
    text=True
)
print("\nBy Sector:")
print(sector_verify.stdout)

print("\n" + "=" * 70)
print(f"✅ PHASE 3 COMPLETE: {total_tagged} equipment tagged with 5D tags")
print("=" * 70)
