#!/usr/bin/env python3
"""
Phase 2: Selective Deletion
Keep CVE/CWE/CAPEC/MITRE/IEC62443 files, delete others
"""
from neo4j import GraphDatabase
import sys

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

print("=" * 80)
print("PHASE 2: SELECTIVE DELETION")
print("=" * 80)

with driver.session() as session:
    # Step 1: Count documents to preserve
    print("\n📊 Step 1: Identifying documents to preserve...")

    preserve_query = """
    MATCH (m:Metadata)
    WHERE m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*'
       OR m.file_name =~ '(?i).*(vulnerability|weakness|threat|cve|cwe|capec).*'
    RETURN count(m) as preserve_count
    """

    result = session.run(preserve_query)
    preserve_count = result.single()['preserve_count']
    print(f"   ✓ Documents to preserve: {preserve_count}")

    # Step 2: Count documents to delete
    delete_count_query = """
    MATCH (m:Metadata)
    WHERE NOT (m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*')
      AND NOT (m.file_name =~ '(?i).*(vulnerability|weakness|threat|cve|cwe|capec).*')
    RETURN count(m) as delete_count
    """

    result = session.run(delete_count_query)
    delete_count = result.single()['delete_count']
    print(f"   ✓ Documents to delete: {delete_count}")

    if preserve_count + delete_count == 0:
        print("\n⚠️  No documents found in database!")
        sys.exit(0)

    print(f"\n   Total metadata nodes: {preserve_count + delete_count}")
    print(f"   Preservation rate: {preserve_count / (preserve_count + delete_count) * 100:.1f}%")

    # Step 3: Mark documents to preserve
    print("\n📋 Step 2: Marking documents to preserve...")

    mark_query = """
    MATCH (m:Metadata)
    WHERE m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*'
       OR m.file_name =~ '(?i).*(vulnerability|weakness|threat|cve|cwe|capec).*'
    SET m:Preserve
    RETURN count(m) as marked
    """

    result = session.run(mark_query)
    marked = result.single()['marked']
    print(f"   ✓ Marked {marked} documents for preservation")

    # Step 4: Delete non-preserved documents (in batches)
    print("\n🗑️  Step 3: Deleting non-preserved documents...")

    # Count entities and relationships to delete
    count_query = """
    MATCH (m:Metadata)
    WHERE NOT m:Preserve
    OPTIONAL MATCH (m)-[:METADATA_FOR]->(d:Document)
    OPTIONAL MATCH (d)-[:CONTAINS_ENTITY]->(e:Entity)
    WITH count(DISTINCT m) as meta_count,
         count(DISTINCT d) as doc_count,
         count(DISTINCT e) as entity_count
    MATCH ()-[r:RELATIONSHIP]->()
    WHERE NOT EXISTS {
        MATCH (preserved:Metadata:Preserve)-[:METADATA_FOR]->(pd:Document {id: r.doc_id})
    }
    RETURN meta_count, doc_count, entity_count, count(r) as rel_count
    """

    result = session.run(count_query)
    record = result.single()
    print(f"   Will delete:")
    print(f"     - {record['meta_count']} Metadata nodes")
    print(f"     - {record['doc_count']} Document nodes")
    print(f"     - {record['entity_count']} Entity nodes")
    print(f"     - {record['rel_count']} RELATIONSHIP edges")

    # Delete in batches to avoid memory issues
    print("\n   Executing deletion...")

    # First, delete relationships for non-preserved documents
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
    while True:
        result = session.run(rel_delete_query)
        rel_count = result.single()['deleted_rels']
        if rel_count == 0:
            break
        total_rels += rel_count
        print(f"     Deleted {total_rels} relationships...", end='\r')

    print(f"\n   ✓ Deleted {total_rels} relationships")

    # Then delete documents with their entities
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
    while True:
        result = session.run(delete_query)
        batch_count = result.single()['deleted_batch']
        if batch_count == 0:
            break
        total_deleted += batch_count
        print(f"     Deleted {total_deleted} batches...", end='\r')

    print(f"\n   ✓ Deleted {total_deleted} document sets")

    # Step 5: Clean up orphaned entities
    print("\n🧹 Step 4: Cleaning up orphaned entities...")

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

    # Step 6: Remove Preserve label
    print("\n🏷️  Step 5: Cleaning up temporary labels...")

    cleanup_query = """
    MATCH (m:Metadata:Preserve)
    REMOVE m:Preserve
    RETURN count(m) as cleaned
    """

    result = session.run(cleanup_query)
    cleaned = result.single()['cleaned']
    print(f"   ✓ Cleaned {cleaned} Preserve labels")

    # Final statistics
    print("\n" + "=" * 80)
    print("FINAL DATABASE STATE")
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

    print(f"Metadata nodes: {stats['metadata_count']}")
    print(f"Document nodes: {stats['doc_count']}")
    print(f"Entity nodes: {stats['entity_count']}")
    print(f"Relationships: {stats['rel_count']}")
    print("\n✅ Selective deletion complete!")
    print("=" * 80)

driver.close()
