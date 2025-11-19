#!/usr/bin/env python3
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

with driver.session() as session:
    # Count documents
    result = session.run("MATCH (d:Document) RETURN count(d) as count")
    doc_count = result.single()["count"]

    # Count entities
    result = session.run("MATCH (e:Entity) RETURN count(e) as count")
    entity_count = result.single()["count"]

    # Count metadata
    result = session.run("MATCH (m:Metadata) RETURN count(m) as count")
    metadata_count = result.single()["count"]

    # Count relationships
    result = session.run("MATCH ()-[r:RELATIONSHIP]->() RETURN count(r) as count")
    rel_count = result.single()["count"]

    print(f"Documents: {doc_count}")
    print(f"Entities: {entity_count}")
    print(f"Metadata: {metadata_count}")
    print(f"Relationships: {rel_count}")

driver.close()
