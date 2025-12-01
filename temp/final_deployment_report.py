#!/usr/bin/env python3
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    # Get all sector counts
    result = session.run("""
        MATCH (n:CriticalInfrastructure)
        RETURN n.sector as sector, count(n) as nodes
        ORDER BY nodes DESC
    """)
    
    sectors = list(result)
    total_nodes = sum(s['nodes'] for s in sectors)
    
    print("\n" + "="*70)
    print("CRITICAL INFRASTRUCTURE ONTOLOGY - FINAL DEPLOYMENT STATUS")
    print("="*70)
    print(f"\nTotal Nodes Deployed: {total_nodes:,}\n")
    
    for record in sectors:
        sector = record['sector'] if record['sector'] else 'UNASSIGNED'
        nodes = record['nodes']
        percentage = (nodes / total_nodes * 100) if total_nodes > 0 else 0
        print(f"  {sector:25} {nodes:>8,} nodes ({percentage:>5.1f}%)")
    
    # Count total relationships
    result = session.run("MATCH ()-[r]->() RETURN count(r) as total")
    total_rels = result.single()['total']
    
    print(f"\n{'='*70}")
    print(f"Total Relationships: {total_rels:,}")
    print(f"{'='*70}\n")
    
    # Deployment completion
    deployed_count = len([s for s in sectors if s['sector'] and s['sector'] != 'UNASSIGNED'])
    print(f"✓ Sectors Deployed: {deployed_count}/16")
    print(f"✓ Deployment Status: {(deployed_count/16)*100:.0f}% COMPLETE")
    
    if deployed_count == 16:
        print("\n🎉 ALL 16 CRITICAL INFRASTRUCTURE SECTORS DEPLOYED!")

driver.close()
