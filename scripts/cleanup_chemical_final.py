import subprocess

print("=" * 70)
print("FINAL CHEMICAL CLEANUP: Remove Remaining Duplicate Relationships")
print("=" * 70)
print()

# Find Chemical equipment with multiple LOCATED_AT relationships
check_query = """
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-CHEM-'
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

print(f"Found {len(duplicate_equipment)} Chemical equipment with duplicate relationships")

if len(duplicate_equipment) == 0:
    print("✅ No duplicate relationships remaining for Chemical sector")
    exit(0)

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
        if cleaned_count % 10 == 0:
            print(f"  Cleaned {cleaned_count}/{len(duplicate_equipment)} equipment...")

print(f"✅ Chemical duplicates cleaned: {cleaned_count}/{len(duplicate_equipment)}")

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
print(f"✅ FINAL CHEMICAL CLEANUP COMPLETE")
print("=" * 70)
