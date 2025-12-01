#!/usr/bin/env python3
"""Quick verification of ATT&CK import"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with driver.session() as session:
    # Count techniques
    result = session.run("""
        MATCH (t:ATT_CK_Technique)
        RETURN count(t) AS total
    """)
    total = result.single()['total']
    print(f"✅ Total ATT&CK Techniques: {total}")
    
    # Sample techniques
    result = session.run("""
        MATCH (t:ATT_CK_Technique)
        WHERE NOT t.is_subtechnique
        RETURN t.technique_id, t.name, t.tactics
        LIMIT 10
    """)
    
    print("\n📋 Sample ATT&CK Techniques:")
    print("-" * 80)
    for record in result:
        tid = record['t.technique_id']
        name = record['t.name']
        tactics = ', '.join(record['t.tactics'][:3]) if record['t.tactics'] else 'N/A'
        print(f"{tid:12} | {name[:40]:40} | {tactics}")
    
    # Count tactics
    result = session.run("""
        MATCH (t:ATT_CK_Tactic)
        RETURN count(t) AS total
    """)
    tactics_count = result.single()['total']
    print(f"\n✅ Total ATT&CK Tactics: {tactics_count}")
    
    # Sample tactics
    result = session.run("""
        MATCH (tact:ATT_CK_Tactic)<-[:BELONGS_TO_TACTIC]-(t:ATT_CK_Technique)
        RETURN tact.name, count(t) AS technique_count
        ORDER BY technique_count DESC
    """)
    
    print("\n📊 Techniques per Tactic:")
    print("-" * 60)
    for record in result:
        tactic = record['tact.name']
        count = record['technique_count']
        print(f"{tactic:30} | {count:4} techniques")

driver.close()
