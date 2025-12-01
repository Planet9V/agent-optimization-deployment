#!/usr/bin/env python3
"""
Verification script for Enhancement 1 deployment
Checks database state and relationship counts
"""

import sys
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def verify_deployment():
    """Verify the deployment status"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            # Check node counts
            stream_count = session.run("MATCH (s:InformationStream) RETURN count(s) as count").single()["count"]
            bias_count = session.run("MATCH (b:CognitiveBias) RETURN count(b) as count").single()["count"]

            print("=" * 80)
            print("Enhancement 1 Database Verification")
            print("=" * 80)
            print(f"\nNode Counts:")
            print(f"  InformationStream nodes: {stream_count}")
            print(f"  CognitiveBias nodes: {bias_count}")

            # Check relationship counts
            has_bias_count = session.run("MATCH ()-[r:HAS_BIAS]->() RETURN count(r) as count").single()["count"]
            print(f"\nRelationship Counts:")
            print(f"  HAS_BIAS relationships: {has_bias_count}")

            # Expected count
            expected_count = 18000
            print(f"\nExpected HAS_BIAS relationships: {expected_count}")

            if has_bias_count == expected_count:
                print("\n✓ VERIFICATION PASSED - Relationship count matches expected")
            elif has_bias_count > 0:
                print(f"\n⚠ PARTIAL DEPLOYMENT - Found {has_bias_count}/{expected_count} relationships")
            else:
                print("\n✗ NOT DEPLOYED - No HAS_BIAS relationships found")

            # Sample relationships
            if has_bias_count > 0:
                print("\nSample Relationships:")
                results = session.run("""
                    MATCH (s:InformationStream)-[r:HAS_BIAS]->(b:CognitiveBias:Level5)
                    RETURN s.id as stream, b.biasId as bias,
                           r.strength as strength, r.activationThreshold as threshold
                    LIMIT 5
                """).data()

                for i, rel in enumerate(results, 1):
                    print(f"  {i}. {rel['stream']} -> {rel['bias']}")
                    print(f"     Strength: {rel['strength']}, Threshold: {rel['threshold']}")

            # Check property distribution
            if has_bias_count > 0:
                print("\nProperty Statistics:")
                stats = session.run("""
                    MATCH ()-[r:HAS_BIAS]->()
                    RETURN
                        avg(r.strength) as avg_strength,
                        min(r.strength) as min_strength,
                        max(r.strength) as max_strength,
                        avg(r.activationThreshold) as avg_threshold
                """).single()

                print(f"  Strength - Avg: {stats['avg_strength']:.4f}, "
                      f"Min: {stats['min_strength']:.4f}, Max: {stats['max_strength']:.4f}")
                print(f"  Threshold - Avg: {stats['avg_threshold']:.4f}")

            print("=" * 80)

            return has_bias_count == expected_count

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        driver.close()

if __name__ == "__main__":
    success = verify_deployment()
    sys.exit(0 if success else 1)
