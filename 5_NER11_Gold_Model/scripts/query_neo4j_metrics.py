#!/usr/bin/env python3
"""
Query Neo4j for E01 APT ingestion metrics.
"""
from neo4j import GraphDatabase
import os
from datetime import datetime

def query_metrics():
    """Query Neo4j for comprehensive metrics."""
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'your-password')

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            # Total nodes by label
            node_counts = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """).data()

            # Total relationships by type
            rel_counts = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY count DESC
            """).data()

            # E01 specific metrics
            e01_metrics = session.run("""
                MATCH (d:Document {collection: 'E01_APT_MITRE'})
                WITH count(d) as total_docs
                MATCH (e:Entity)
                WHERE e.source_collection = 'E01_APT_MITRE'
                WITH total_docs, count(e) as total_entities
                MATCH (e:Entity)-[r]->()
                WHERE e.source_collection = 'E01_APT_MITRE'
                RETURN total_docs, total_entities, count(r) as total_relationships
            """).single()

            # APT groups
            apt_groups = session.run("""
                MATCH (a:APTGroup)
                RETURN count(a) as apt_count
            """).single()

            # Techniques
            techniques = session.run("""
                MATCH (t:Technique)
                RETURN count(t) as technique_count
            """).single()

        driver.close()

        # Format output
        print(f"\n{'='*60}")
        print(f"NEO4J E01 APT INGESTION METRICS")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        print(f"\n📊 NODE COUNTS BY LABEL:")
        for item in node_counts:
            print(f"   {item['label']:20s}: {item['count']:,}")

        print(f"\n🔗 RELATIONSHIP COUNTS BY TYPE:")
        for item in rel_counts[:15]:  # Top 15
            print(f"   {item['type']:30s}: {item['count']:,}")

        if e01_metrics:
            print(f"\n📁 E01 COLLECTION METRICS:")
            print(f"   Documents:      {e01_metrics['total_docs']:,}")
            print(f"   Entities:       {e01_metrics['total_entities']:,}")
            print(f"   Relationships:  {e01_metrics['total_relationships']:,}")

        if apt_groups:
            print(f"\n🎯 SPECIALIZED ENTITIES:")
            print(f"   APT Groups:     {apt_groups['apt_count']:,}")
            print(f"   Techniques:     {techniques['technique_count']:,}")

        print(f"\n{'='*60}")

    except Exception as e:
        print(f"❌ Error querying Neo4j: {str(e)}")
        print(f"   URI: {uri}")
        print(f"   User: {user}")

if __name__ == '__main__':
    query_metrics()
