#!/usr/bin/env python3
"""
Enhancement 1: HAS_BIAS Relationship Deployment to Neo4j
Deploys 18,000 HAS_BIAS relationships in batches
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from neo4j import GraphDatabase

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
BATCH_SIZE = 500
INPUT_FILE = "/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/data/enhancement1_has_bias_relationships_VALIDATED.json"
LOG_FILE = "/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/reports/enhancement1_deployment_log.txt"

class RelationshipDeployer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_messages = []

    def close(self):
        self.driver.close()

    def log(self, message):
        """Log message to both console and internal log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.log_messages.append(log_msg)

    def save_log(self):
        """Save log to file"""
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'w') as f:
            f.write('\n'.join(self.log_messages))
        self.log(f"Log saved to {LOG_FILE}")

    def verify_nodes_exist(self, tx):
        """Verify that InformationStream and CognitiveBias nodes exist"""
        stream_count = tx.run("MATCH (s:InformationStream) RETURN count(s) as count").single()["count"]
        bias_count = tx.run("MATCH (b:CognitiveBias) RETURN count(b) as count").single()["count"]

        self.log(f"Database contains {stream_count} InformationStream nodes")
        self.log(f"Database contains {bias_count} CognitiveBias nodes")

        if stream_count == 0 or bias_count == 0:
            raise ValueError("Missing required nodes in database!")

        return stream_count, bias_count

    def create_relationships_batch(self, tx, relationships):
        """Create a batch of HAS_BIAS relationships"""
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

        result = tx.run(query, relationships=relationships)
        return result.single()["created"]

    def get_relationship_count(self, tx):
        """Get current count of HAS_BIAS relationships"""
        result = tx.run("MATCH ()-[r:HAS_BIAS]->() RETURN count(r) as count")
        return result.single()["count"]

    def verify_relationship_properties(self, tx, sample_size=10):
        """Verify random sample of relationship properties"""
        query = """
        MATCH (s:InformationStream)-[r:HAS_BIAS]->(b:CognitiveBias:Level5)
        RETURN s.id as streamId, b.biasId as biasId,
               r.strength as strength, r.activationThreshold as threshold,
               r.detectedAt as detectedAt, r.context as context,
               r.mitigationApplied as mitigation
        LIMIT $sample_size
        """

        results = tx.run(query, sample_size=sample_size).data()
        self.log(f"\nVerifying {len(results)} sample relationships:")

        for i, rel in enumerate(results, 1):
            self.log(f"  Sample {i}: {rel['streamId']} -> {rel['biasId']}")
            self.log(f"    Strength: {rel['strength']}, Threshold: {rel['threshold']}")
            self.log(f"    Detected: {rel['detectedAt']}, Mitigation: {rel['mitigation']}")

        return len(results)

    def deploy_relationships(self, relationships):
        """Deploy relationships in batches"""
        total_relationships = len(relationships)
        self.log(f"Starting deployment of {total_relationships} relationships")
        self.log(f"Batch size: {BATCH_SIZE}")

        with self.driver.session() as session:
            # Verify nodes exist
            session.execute_read(self.verify_nodes_exist)

            # Get initial relationship count
            initial_count = session.execute_read(self.get_relationship_count)
            self.log(f"Initial HAS_BIAS relationship count: {initial_count}")

            # Deploy in batches
            deployed = 0
            errors = 0

            for i in range(0, total_relationships, BATCH_SIZE):
                batch = relationships[i:i + BATCH_SIZE]
                batch_num = (i // BATCH_SIZE) + 1
                total_batches = (total_relationships + BATCH_SIZE - 1) // BATCH_SIZE

                try:
                    created = session.execute_write(self.create_relationships_batch, batch)
                    deployed += created

                    self.log(f"Batch {batch_num}/{total_batches}: Created {created} relationships "
                           f"(Total: {deployed}/{total_relationships})")

                    # Progress update every 10 batches
                    if batch_num % 10 == 0:
                        progress_pct = (deployed / total_relationships) * 100
                        self.log(f"Progress: {progress_pct:.1f}% complete")

                except Exception as e:
                    errors += 1
                    self.log(f"ERROR in batch {batch_num}: {str(e)}")
                    if errors > 5:
                        self.log("Too many errors, aborting deployment")
                        raise

                # Small delay between batches to avoid overwhelming database
                if batch_num % 20 == 0:
                    time.sleep(0.5)

            # Verify final count
            final_count = session.execute_read(self.get_relationship_count)
            new_relationships = final_count - initial_count

            self.log(f"\nDeployment Summary:")
            self.log(f"  Expected: {total_relationships}")
            self.log(f"  Deployed: {deployed}")
            self.log(f"  Initial count: {initial_count}")
            self.log(f"  Final count: {final_count}")
            self.log(f"  New relationships: {new_relationships}")
            self.log(f"  Errors: {errors}")

            # Verify sample of properties
            self.log("\nVerifying relationship properties:")
            session.execute_read(self.verify_relationship_properties, sample_size=10)

            if new_relationships == total_relationships:
                self.log("\n✓ DEPLOYMENT SUCCESSFUL - All relationships created")
                return True
            else:
                self.log(f"\n✗ DEPLOYMENT INCOMPLETE - Expected {total_relationships}, got {new_relationships}")
                return False

def main():
    """Main deployment function"""
    print("=" * 80)
    print("Enhancement 1: HAS_BIAS Relationship Deployment")
    print("=" * 80)

    # Check if input file exists
    if not Path(INPUT_FILE).exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        print("Please run Hour 2 validation first to generate the validated relationship file.")
        sys.exit(1)

    # Load relationships
    print(f"Loading relationships from {INPUT_FILE}...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    relationships = data.get('relationships', [])
    print(f"Loaded {len(relationships)} relationships")

    if len(relationships) == 0:
        print("ERROR: No relationships found in file")
        sys.exit(1)

    # Deploy relationships
    deployer = None
    try:
        deployer = RelationshipDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        success = deployer.deploy_relationships(relationships)
        deployer.save_log()

        if success:
            print("\n" + "=" * 80)
            print("DEPLOYMENT COMPLETE - All relationships successfully deployed to Neo4j")
            print("=" * 80)
            sys.exit(0)
        else:
            print("\n" + "=" * 80)
            print("DEPLOYMENT FAILED - See log for details")
            print("=" * 80)
            sys.exit(1)

    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        if deployer:
            deployer.close()

if __name__ == "__main__":
    main()
