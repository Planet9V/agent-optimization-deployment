import subprocess
import json

print("=" * 70)
print("PHASE 2 FINAL FIX: Create Remaining Relationships")
print("Query Database for Actual Facility IDs")
print("=" * 70)
print()

def get_facilities_from_db(prefix):
    """Query database for actual facility IDs"""
    query = f"MATCH (f:Facility) WHERE f.facilityId STARTS WITH '{prefix}' RETURN f.facilityId ORDER BY f.facilityId;"
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )

    facilities = []
    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
        fac_id = line.strip().strip('"')
        if fac_id and not fac_id.startswith('f.facilityId'):
            facilities.append(fac_id)
    return facilities

def create_missing_relationships(sector_name, equipment_prefix, equipment_start, equipment_count, facility_prefix):
    """Create relationships using actual facility IDs from database"""
    print(f"\n{'─' * 70}")
    print(f"{sector_name} SECTOR - Fixing relationships")
    print(f"{'─' * 70}")

    # Get actual facilities from database
    facilities = get_facilities_from_db(facility_prefix)
    print(f"Found {len(facilities)} facilities in database")

    if len(facilities) == 0:
        print(f"❌ No facilities found with prefix {facility_prefix}")
        return 0

    # Find equipment that don't have relationships yet
    check_query = f"""
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH '{equipment_prefix}'
  AND NOT (eq)-[:LOCATED_AT]->()
RETURN eq.equipmentId
ORDER BY eq.equipmentId;
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', check_query],
        capture_output=True,
        text=True
    )

    missing_equipment = []
    for line in result.stdout.strip().split('\n')[1:]:
        eq_id = line.strip().strip('"')
        if eq_id and not eq_id.startswith('eq.equipmentId'):
            missing_equipment.append(eq_id)

    print(f"Found {len(missing_equipment)} equipment without relationships")

    if len(missing_equipment) == 0:
        print(f"✅ No missing relationships for {sector_name}")
        return 0

    # Distribute equipment across facilities
    count = 0
    for idx, eq_id in enumerate(missing_equipment):
        fac_id = facilities[idx % len(facilities)]
        zone_num = (idx // len(facilities)) + 1

        query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}}), (f:Facility {{facilityId: '{fac_id}'}})
CREATE (eq)-[:LOCATED_AT {{
  installation_date: eq.installation_date,
  location: 'Zone {zone_num}',
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
                print(f"  Created {count}/{len(missing_equipment)} relationships...")

    print(f"✅ {sector_name} relationships created: {count}/{len(missing_equipment)}")
    return count

# Execute fixes for sectors with missing relationships
total = 0

print("\n" + "=" * 70)
print("FIXING MISSING RELATIONSHIPS")
print("=" * 70)

total += create_missing_relationships(
    "HEALTHCARE", "EQ-HEALTH-", 30001, 500, "HEALTH-"
)

total += create_missing_relationships(
    "CHEMICAL", "EQ-CHEM-", 40001, 300, "CHEM-"
)

total += create_missing_relationships(
    "MANUFACTURING", "EQ-MFG-", 50001, 400, "MFG-"
)

# FINAL VERIFICATION
print("\n" + "=" * 70)
print("FINAL VERIFICATION")
print("=" * 70)

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

print("\n" + "=" * 70)
print(f"✅ PHASE 2 FINAL FIX COMPLETE: {total} new relationships created")
print("=" * 70)
