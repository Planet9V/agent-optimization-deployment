#!/usr/bin/env python3
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    # Count all Transportation nodes
    result = session.run("MATCH (n:Transportation) RETURN count(n) as total")
    total = result.single()['total']
    
    # Count relationships
    result = session.run("MATCH ()-[r]->() WHERE (startNode(r):Transportation OR endNode(r):Transportation) RETURN count(r) as total")
    rels = result.single()['total']
    
    # Count by type
    result = session.run("MATCH (n:Transportation) RETURN n.type as type, count(n) as count ORDER BY count DESC")
    
    print(f"\n{'='*70}")
    print(f"TRANSPORTATION SECTOR - FINAL VERIFICATION")
    print(f"{'='*70}")
    print(f"Total Nodes:        {total:>8,}")
    print(f"Total Relationships: {rels:>8,}")
    print(f"\nNode Distribution:")
    
    for record in result:
        print(f"  {record['type']:20} {record['count']:>6,} nodes")

driver.close()
