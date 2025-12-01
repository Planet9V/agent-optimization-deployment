import subprocess

print("="*70)
print("PHASE 2 FIX: Creating LOCATED_AT Relationships for ALL 3 Sectors")
print("="*70)
print()

# Healthcare Facilities (60) - using ACTUAL facility IDs
healthcare_facilities = [
    # Major Hospitals (20)
    "HEALTH-ATL-001", "HEALTH-BOS-001", "HEALTH-CHI-001", "HEALTH-CLE-001", "HEALTH-DAL-001",
    "HEALTH-DEN-001", "HEALTH-DET-001", "HEALTH-HOU-001", "HEALTH-LA-001", "HEALTH-MIA-001",
    "HEALTH-NY-001", "HEALTH-PHI-001", "HEALTH-PHX-001", "HEALTH-SF-001", "HEALTH-SEA-001",
    "HEALTH-STL-001", "HEALTH-WASH-001", "HEALTH-BAL-001", "HEALTH-MIN-001", "HEALTH-PITT-001",

    # Regional Medical Centers (15)
    "HEALTH-AUS-MED-001", "HEALTH-CHA-MED-001", "HEALTH-CINCI-MED-001", "HEALTH-IND-MED-001",
    "HEALTH-KC-MED-001", "HEALTH-LV-MED-001", "HEALTH-MEM-MED-001", "HEALTH-MIL-MED-001",
    "HEALTH-NASH-MED-001", "HEALTH-NO-MED-001", "HEALTH-OKC-MED-001", "HEALTH-OMA-MED-001",
    "HEALTH-PORT-MED-001", "HEALTH-SAC-MED-001", "HEALTH-SLC-MED-001",

    # Urgent Care Centers (10)
    "HEALTH-URGENT-ATL-001", "HEALTH-URGENT-BOS-001", "HEALTH-URGENT-CHI-001", "HEALTH-URGENT-DAL-001",
    "HEALTH-URGENT-HOU-001", "HEALTH-URGENT-LA-001", "HEALTH-URGENT-MIA-001", "HEALTH-URGENT-NY-001",
    "HEALTH-URGENT-PHI-001", "HEALTH-URGENT-SF-001",

    # Specialty Clinics (8)
    "HEALTH-CLINIC-ATL-001", "HEALTH-CLINIC-CHI-001", "HEALTH-CLINIC-DAL-001", "HEALTH-CLINIC-HOU-001",
    "HEALTH-CLINIC-LA-001", "HEALTH-CLINIC-MIA-001", "HEALTH-CLINIC-NY-001", "HEALTH-CLINIC-SF-001",

    # Rehabilitation Centers (4)
    "HEALTH-REHAB-CHI-001", "HEALTH-REHAB-LA-001", "HEALTH-REHAB-NY-001", "HEALTH-REHAB-SF-001",

    # Medical Laboratories (3)
    "HEALTH-LAB-CHI-001", "HEALTH-LAB-NY-001", "HEALTH-LAB-SF-001"
]

# Chemical Facilities (40)
chemical_facilities = []
# Chemical Manufacturing Plants (10)
for i in range(1, 11):
    prefix = ["TX", "LA", "NJ", "OH", "IL", "PA", "MI", "CA", "NC", "TN"][i-1]
    chemical_facilities.append(f"CHEM-{prefix}-{'00' if i < 10 else '0'}{i}")
# Petrochemical Plants (8)
for i in range(1, 9):
    prefix = ["TX", "LA", "TX", "LA", "AL", "MS", "TX", "CA"][i-1]
    suffix = ["PETRO-001", "PETRO-001", "PETRO-002", "PETRO-002", "PETRO-001", "PETRO-001", "PETRO-003", "PETRO-001"][i-1]
    chemical_facilities.append(f"CHEM-{prefix}-{suffix}")
# Pharmaceutical (6), Fertilizer (6), Hazardous (5), Waste Treatment (5)
pharma_states = ["NJ", "PA", "CA", "MA", "NC", "IL"]
for i, state in enumerate(pharma_states, 1):
    chemical_facilities.append(f"CHEM-{state}-PHARMA-001")
fert_states = ["IA", "IL", "KS", "NE", "OK", "TX"]
for i, state in enumerate(fert_states, 1):
    chemical_facilities.append(f"CHEM-{state}-FERT-001")
haz_states = ["TX", "LA", "NJ", "CA", "IL"]
for i, state in enumerate(haz_states, 1):
    chemical_facilities.append(f"CHEM-{state}-HAZ-001")
waste_states = ["TX", "LA", "OH", "CA", "MI"]
for i, state in enumerate(waste_states, 1):
    chemical_facilities.append(f"CHEM-{state}-WASTE-001")

# Manufacturing Facilities (50)
manufacturing_facilities = [
    # Automotive (10)
    "MFG-MI-AUTO-001", "MFG-OH-AUTO-001", "MFG-IN-AUTO-001", "MFG-KY-AUTO-001", "MFG-TN-AUTO-001",
    "MFG-AL-AUTO-001", "MFG-TX-AUTO-001", "MFG-IL-AUTO-001", "MFG-MO-AUTO-001", "MFG-SC-AUTO-001",

    # Aerospace (8)
    "MFG-WA-AERO-001", "MFG-CA-AERO-001", "MFG-TX-AERO-001", "MFG-FL-AERO-001",
    "MFG-CT-AERO-001", "MFG-AZ-AERO-001", "MFG-GA-AERO-001", "MFG-OH-AERO-001",

    # Steel Mills (6)
    "MFG-IN-STEEL-001", "MFG-PA-STEEL-001", "MFG-OH-STEEL-001", "MFG-IL-STEEL-001",
    "MFG-MI-STEEL-001", "MFG-AL-STEEL-001",

    # Shipbuilding (6)
    "MFG-VA-SHIP-001", "MFG-MS-SHIP-001", "MFG-ME-SHIP-001", "MFG-CA-SHIP-001",
    "MFG-WA-SHIP-001", "MFG-CT-SHIP-001",

    # Engine/Turbine (6)
    "MFG-NC-ENG-001", "MFG-WI-ENG-001", "MFG-OH-ENG-001", "MFG-IL-ENG-001",
    "MFG-IN-ENG-001", "MFG-NY-ENG-001",

    # Defense (6)
    "MFG-CT-DEF-001", "MFG-MA-DEF-001", "MFG-VA-DEF-001", "MFG-CA-DEF-001",
    "MFG-AZ-DEF-001", "MFG-TX-DEF-001",

    # Aluminum (4)
    "MFG-WA-ALU-001", "MFG-NY-ALU-001", "MFG-MT-ALU-001", "MFG-KY-ALU-001",

    # Heavy Machinery (4)
    "MFG-IL-HEAVY-001", "MFG-IA-HEAVY-001", "MFG-WI-HEAVY-001", "MFG-PA-HEAVY-001"
]

def create_relationships(sector_name, equipment_prefix, equipment_start, equipment_count, facilities):
    """Create LOCATED_AT relationships by querying facilities from DB"""
    print(f"\n{'─'*70}")
    print(f"{sector_name} SECTOR - Creating {equipment_count} relationships")
    print(f"{'─'*70}")

    count = 0
    equipment_per_facility = equipment_count // len(facilities)
    remainder = equipment_count % len(facilities)

    eq_idx = 0
    for fac_idx, fac_id in enumerate(facilities):
        # Distribute equipment: give extra to first facilities
        num_equipment = equipment_per_facility + (1 if fac_idx < remainder else 0)

        for eq_offset in range(num_equipment):
            if eq_idx >= equipment_count:
                break

            eq_id = f"{equipment_prefix}{equipment_start + eq_idx}"

            # Query to get facility coordinates from database
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
                count += 1
                if count % 50 == 0:
                    print(f"  Created {count}/{equipment_count} relationships...")
            else:
                # Log errors
                if "Cannot access property" in result.stderr or result.stderr:
                    print(f"  ERROR for {eq_id} → {fac_id}: {result.stderr[:100]}")

            eq_idx += 1

    print(f"✅ {sector_name} relationships created: {count}/{equipment_count}")
    return count

# Execute for all 3 sectors
total_relationships = 0

print("\n" + "="*70)
print("CREATING RELATIONSHIPS")
print("="*70)

total_relationships += create_relationships(
    "HEALTHCARE", "EQ-HEALTH-", 30001, 500, healthcare_facilities
)

total_relationships += create_relationships(
    "CHEMICAL", "EQ-CHEM-", 40001, 300, chemical_facilities
)

total_relationships += create_relationships(
    "MANUFACTURING", "EQ-MFG-", 50001, 400, manufacturing_facilities
)

# VERIFICATION
print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

verify = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
     """MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
     WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' OR eq.equipmentId STARTS WITH 'EQ-CHEM-' OR eq.equipmentId STARTS WITH 'EQ-MFG-'
     RETURN COUNT(r) AS total_relationships, COUNT(DISTINCT eq) AS unique_equipment, COUNT(DISTINCT f) AS unique_facilities;"""],
    capture_output=True,
    text=True
)
print("\nTotal Relationships:")
print(verify.stdout)

# Sector breakdown
sector_verify = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
     """MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
     WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' OR eq.equipmentId STARTS WITH 'EQ-CHEM-' OR eq.equipmentId STARTS WITH 'EQ-MFG-'
     WITH eq.equipmentId AS eqId
     RETURN
       CASE
         WHEN eqId STARTS WITH 'EQ-HEALTH-' THEN 'Healthcare'
         WHEN eqId STARTS WITH 'EQ-CHEM-' THEN 'Chemical'
         WHEN eqId STARTS WITH 'EQ-MFG-' THEN 'Manufacturing'
       END AS sector,
       COUNT(*) AS count
     ORDER BY sector;"""],
    capture_output=True,
    text=True
)
print("\nBy Sector:")
print(sector_verify.stdout)

print("\n" + "="*70)
print(f"✅ PHASE 2 FIX COMPLETE: {total_relationships} target relationships")
print("="*70)
