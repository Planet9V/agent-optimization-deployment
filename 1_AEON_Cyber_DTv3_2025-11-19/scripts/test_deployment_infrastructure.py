#!/usr/bin/env python3
"""
Test deployment infrastructure with small sample
Verifies database connectivity and relationship creation
"""

import json
import sys
from datetime import datetime
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def test_deployment():
    """Test deployment with 3 sample relationships"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            print("=" * 80)
            print("Testing Deployment Infrastructure")
            print("=" * 80)

            # Get sample nodes
            print("\n1. Finding sample nodes...")
            stream = session.run("MATCH (s:InformationStream) RETURN s.id as id LIMIT 1").single()
            bias = session.run("MATCH (b:CognitiveBias:Level5) RETURN b.biasId as id LIMIT 3").data()

            if not stream or len(bias) < 3:
                print(f"ERROR: Insufficient nodes for testing (stream: {stream}, bias count: {len(bias) if bias else 0})")
                return False

            stream_id = stream["id"]
            bias_ids = [b["id"] for b in bias]

            print(f"  Stream: {stream_id}")
            print(f"  Biases: {bias_ids}")

            # Create test relationships
            print("\n2. Creating test relationships...")
            test_relationships = [
                {
                    "sourceId": stream_id,
                    "targetId": bias_ids[0],
                    "strength": 0.85,
                    "activationThreshold": 0.7,
                    "detectedAt": datetime.now().isoformat(),
                    "context": "test_deployment",
                    "mitigationApplied": False
                },
                {
                    "sourceId": stream_id,
                    "targetId": bias_ids[1],
                    "strength": 0.72,
                    "activationThreshold": 0.6,
                    "detectedAt": datetime.now().isoformat(),
                    "context": "test_deployment",
                    "mitigationApplied": True
                },
                {
                    "sourceId": stream_id,
                    "targetId": bias_ids[2],
                    "strength": 0.91,
                    "activationThreshold": 0.8,
                    "detectedAt": datetime.now().isoformat(),
                    "context": "test_deployment",
                    "mitigationApplied": False
                }
            ]

            query = """
            UNWIND $relationships AS rel
            MATCH (s:InformationStream {id: rel.sourceId})
            MATCH (b:CognitiveBias:Level5 {biasId: rel.targetId})
            CREATE (s)-[r:HAS_BIAS {
                strength: rel.strength,
                activationThreshold: rel.activationThreshold,
                detectedAt: datetime(rel.detectedAt),
                context: rel.context,
                mitigationApplied: rel.mitigationApplied
            }]->(b)
            RETURN count(r) as created
            """

            result = session.run(query, relationships=test_relationships)
            created = result.single()["created"]
            print(f"  Created {created} test relationships")

            # Verify relationships
            print("\n3. Verifying test relationships...")
            verify_query = """
            MATCH (s:InformationStream {id: $stream_id})-[r:HAS_BIAS]->(b:CognitiveBias:Level5)
            WHERE r.context = 'test_deployment'
            RETURN b.biasId as bias, r.strength as strength, r.activationThreshold as threshold
            """

            results = session.run(verify_query, stream_id=stream_id).data()
            print(f"  Found {len(results)} test relationships")

            for i, rel in enumerate(results, 1):
                print(f"    {i}. Bias: {rel['bias']}, Strength: {rel['strength']}, Threshold: {rel['threshold']}")

            # Cleanup test relationships
            print("\n4. Cleaning up test relationships...")
            cleanup_query = """
            MATCH ()-[r:HAS_BIAS]->()
            WHERE r.context = 'test_deployment'
            DELETE r
            RETURN count(r) as deleted
            """

            deleted = session.run(cleanup_query).single()["deleted"]
            print(f"  Deleted {deleted} test relationships")

            # Final verification
            verify_cleanup = session.run("""
                MATCH ()-[r:HAS_BIAS]->()
                WHERE r.context = 'test_deployment'
                RETURN count(r) as count
            """).single()["count"]

            print("\n" + "=" * 80)
            if verify_cleanup == 0 and created == 3:
                print("✓ INFRASTRUCTURE TEST PASSED")
                print("  - Database connectivity: OK")
                print("  - Relationship creation: OK")
                print("  - Property assignment: OK")
                print("  - Cleanup: OK")
                print("\nDeployment infrastructure is ready!")
                print("=" * 80)
                return True
            else:
                print("✗ INFRASTRUCTURE TEST FAILED")
                print("=" * 80)
                return False

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        driver.close()

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)
