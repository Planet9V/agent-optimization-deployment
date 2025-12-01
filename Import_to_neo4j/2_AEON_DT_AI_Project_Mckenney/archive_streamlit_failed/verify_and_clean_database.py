#!/usr/bin/env python3
"""
STRICT CLEANUP: Keep ONLY CVE/CWE/CAPEC/MITRE/IEC62443 files
Delete everything else to ensure 100% compliance with Option 1
"""
from neo4j import GraphDatabase
import sys

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

print("=" * 80)
print("STRICT DATABASE CLEANUP - OPTION 1 COMPLIANCE")
print("=" * 80)

with driver.session() as session:
    # Step 1: Identify files to preserve
    print("\n📋 Step 1: Identifying CVE/CWE/CAPEC/MITRE/IEC62443 files...")

    preserve_query = """
    MATCH (m:Metadata)
    WHERE m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*'
       OR m.file_name =~ '(?i).*(cve-|cwe-|capec-|attack).*'
    RETURN m.file_path as path, m.file_name as name
    ORDER BY m.file_path
    """

    result = session.run(preserve_query)
    preserved_files = list(result)

    print(f"\n✅ Files to PRESERVE ({len(preserved_files)}):")
    for i, record in enumerate(preserved_files[:20], 1):
        print(f"   {i}. {record['name']} ({record['path'][:80]}...)")
    if len(preserved_files) > 20:
        print(f"   ... and {len(preserved_files) - 20} more")

    # Step 2: Count files to DELETE
    delete_count_query = """
    MATCH (m:Metadata)
    WHERE NOT (m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*')
      AND NOT (m.file_name =~ '(?i).*(cve-|cwe-|capec-|attack).*')
    RETURN count(m) as delete_count
    """

    result = session.run(delete_count_query)
    delete_count = result.single()['delete_count']

    print(f"\n🗑️  Files to DELETE: {delete_count}")

    if delete_count == 0:
        print("\n✅ Database is clean! Only CVE/CWE/CAPEC/MITRE files present.")
        driver.close()
        sys.exit(0)

    # Step 3: Show sample of files to be deleted
    sample_delete_query = """
    MATCH (m:Metadata)
    WHERE NOT (m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*')
      AND NOT (m.file_name =~ '(?i).*(cve-|cwe-|capec-|attack).*')
    RETURN m.file_path as path, m.file_name as name
    LIMIT 10
    """

    result = session.run(sample_delete_query)
    print("\n📄 Sample files to be DELETED:")
    for i, record in enumerate(result, 1):
        print(f"   {i}. {record['name']}")

    # Step 4: Mark files to preserve
    print(f"\n🏷️  Step 2: Marking {len(preserved_files)} files for preservation...")

    mark_query = """
    MATCH (m:Metadata)
    WHERE m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*'
       OR m.file_name =~ '(?i).*(cve-|cwe-|capec-|attack).*'
    SET m:Preserve
    RETURN count(m) as marked
    """

    result = session.run(mark_query)
    marked = result.single()['marked']
    print(f"   ✓ Marked {marked} files for preservation")

    # Step 5: Delete ALL non-preserved content
    print(f"\n🗑️  Step 3: Deleting {delete_count} non-preserved files and their data...")

    # First, delete relationships
    rel_delete_query = """
    MATCH (m:Metadata)
    WHERE NOT m:Preserve
    MATCH (m)-[:METADATA_FOR]->(d:Document)
    WITH d.id as doc_id LIMIT 500
    MATCH ()-[r:RELATIONSHIP {doc_id: doc_id}]->()
    DELETE r
    RETURN count(r) as deleted_rels
    """

    total_rels = 0
    print("   Deleting relationships...")
    while True:
        result = session.run(rel_delete_query)
        rel_count = result.single()['deleted_rels']
        if rel_count == 0:
            break
        total_rels += rel_count
        print(f"     Deleted {total_rels} relationships...", end='\r')

    print(f"\n   ✓ Deleted {total_rels} relationships")

    # Then delete documents and entities
    delete_query = """
    MATCH (m:Metadata)
    WHERE NOT m:Preserve
    OPTIONAL MATCH (m)-[:METADATA_FOR]->(d:Document)
    OPTIONAL MATCH (d)-[:CONTAINS_ENTITY]->(e:Entity)
    WITH m, d, e LIMIT 500
    DETACH DELETE m, d, e
    RETURN count(DISTINCT m) as deleted_batch
    """

    total_deleted = 0
    print("   Deleting documents and entities...")
    while True:
        result = session.run(delete_query)
        batch_count = result.single()['deleted_batch']
        if batch_count == 0:
            break
        total_deleted += batch_count
        print(f"     Deleted {total_deleted} document sets...", end='\r')

    print(f"\n   ✓ Deleted {total_deleted} document sets")

    # Step 6: Clean up orphaned entities
    print("\n🧹 Step 4: Cleaning orphaned entities...")

    orphan_query = """
    MATCH (e:Entity)
    WHERE NOT (e)<-[:CONTAINS_ENTITY]-()
    WITH e LIMIT 1000
    DETACH DELETE e
    RETURN count(e) as orphans_deleted
    """

    total_orphans = 0
    while True:
        result = session.run(orphan_query)
        orphan_count = result.single()['orphans_deleted']
        if orphan_count == 0:
            break
        total_orphans += orphan_count
        print(f"     Cleaned {total_orphans} orphaned entities...", end='\r')

    print(f"\n   ✓ Removed {total_orphans} orphaned entities")

    # Step 7: Remove Preserve labels
    print("\n🏷️  Step 5: Cleaning up temporary labels...")

    cleanup_query = """
    MATCH (m:Metadata:Preserve)
    REMOVE m:Preserve
    RETURN count(m) as cleaned
    """

    result = session.run(cleanup_query)
    cleaned = result.single()['cleaned']
    print(f"   ✓ Cleaned {cleaned} Preserve labels")

    # Final verification
    print("\n" + "=" * 80)
    print("FINAL DATABASE STATE - VERIFICATION")
    print("=" * 80)

    final_stats = """
    MATCH (m:Metadata) WITH count(m) as metadata_count
    MATCH (d:Document) WITH metadata_count, count(d) as doc_count
    MATCH (e:Entity) WITH metadata_count, doc_count, count(e) as entity_count
    MATCH ()-[r:RELATIONSHIP]->() WITH metadata_count, doc_count, entity_count, count(r) as rel_count
    RETURN metadata_count, doc_count, entity_count, rel_count
    """

    result = session.run(final_stats)
    stats = result.single()

    print(f"Metadata nodes: {stats['metadata_count']} (should be ~84-90)")
    print(f"Document nodes: {stats['doc_count']}")
    print(f"Entity nodes: {stats['entity_count']}")
    print(f"Relationships: {stats['rel_count']}")

    # Verify only CVE/CWE/CAPEC/MITRE remain
    verify_query = """
    MATCH (m:Metadata)
    WHERE NOT (m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*')
      AND NOT (m.file_name =~ '(?i).*(cve-|cwe-|capec-|attack).*')
    RETURN count(m) as non_compliant
    """

    result = session.run(verify_query)
    non_compliant = result.single()['non_compliant']

    if non_compliant == 0:
        print("\n✅ VERIFICATION PASSED: Only CVE/CWE/CAPEC/MITRE files remain!")
    else:
        print(f"\n⚠️  WARNING: {non_compliant} non-compliant files still present!")

    print("=" * 80)

driver.close()
