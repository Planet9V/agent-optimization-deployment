import subprocess

print("=" * 70)
print("CLEANUP: Remove Duplicate LOCATED_AT Relationships")
print("Keep Only First Relationship Per Equipment")
print("=" * 70)
print()

def cleanup_duplicates(sector_name, equipment_prefix):
    """Find and remove duplicate LOCATED_AT relationships"""
    print(f"\n{'─' * 70}")
    print(f"{sector_name} SECTOR - Cleaning duplicates")
    print(f"{'─' * 70}")

    # Find equipment with multiple LOCATED_AT relationships
    check_query = f"""
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH '{equipment_prefix}'
WITH eq, collect(r) AS rels, collect(f) AS facilities
WHERE size(rels) > 1
RETURN eq.equipmentId AS eqId, size(rels) AS relCount
ORDER BY eq.equipmentId;
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', check_query],
        capture_output=True,
        text=True
    )

    duplicate_equipment = []
    for line in result.stdout.strip().split('\n')[1:]:
        if line and not line.startswith('eq'):
            parts = line.split(',')
            if len(parts) >= 2:
                eq_id = parts[0].strip().strip('"')
                rel_count = parts[1].strip()
                if eq_id and rel_count:
                    duplicate_equipment.append((eq_id, rel_count))

    print(f"Found {len(duplicate_equipment)} equipment with multiple relationships")

    if len(duplicate_equipment) == 0:
        print(f"✅ No duplicate relationships for {sector_name}")
        return 0

    # For each equipment with duplicates, keep only the first relationship
    cleaned_count = 0
    for eq_id, rel_count in duplicate_equipment:
        # Delete all but the first relationship
        cleanup_query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}})-[r:LOCATED_AT]->(f:Facility)
WITH eq, r, f
ORDER BY id(r)
WITH eq, collect(r) AS rels
WHERE size(rels) > 1
FOREACH (rel IN tail(rels) | DELETE rel);
"""

        result = subprocess.run(
            ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', cleanup_query],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            cleaned_count += 1
            if cleaned_count % 25 == 0:
                print(f"  Cleaned {cleaned_count}/{len(duplicate_equipment)} equipment...")

    print(f"✅ {sector_name} duplicates cleaned: {cleaned_count}/{len(duplicate_equipment)}")
    return cleaned_count

# Execute cleanup for all 3 sectors
total_cleaned = 0

print("\n" + "=" * 70)
print("CLEANING DUPLICATE RELATIONSHIPS")
print("=" * 70)

total_cleaned += cleanup_duplicates("HEALTHCARE", "EQ-HEALTH-")
total_cleaned += cleanup_duplicates("CHEMICAL", "EQ-CHEM-")
total_cleaned += cleanup_duplicates("MANUFACTURING", "EQ-MFG-")

# FINAL VERIFICATION
print("\n" + "=" * 70)
print("FINAL VERIFICATION AFTER CLEANUP")
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
print(f"✅ CLEANUP COMPLETE: {total_cleaned} equipment had duplicates removed")
print("=" * 70)
