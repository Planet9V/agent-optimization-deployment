#!/usr/bin/env python3
"""
Level 5 Neo4j Deployment Script - AEON Digital Twin
Deploys 6,000 Level 5 nodes to Neo4j database with relationships
"""

import json
import os
import sys
from neo4j import GraphDatabase
from datetime import datetime
import random
import traceback

# Neo4j connection settings
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'aeon_dt$2025!')

class Level5Deployer:
    def __init__(self, uri, user, password):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'nodes_created': 0,
            'relationships_created': 0,
            'errors': [],
            'start_time': datetime.now()
        }

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def clear_level5_nodes(self, session):
        """Clear existing Level 5 nodes (optional - for clean deployment)"""
        print("Clearing existing Level 5 nodes...")

        queries = [
            "MATCH (n:Level5) DETACH DELETE n",
            "MATCH (n:InformationEvent) DETACH DELETE n",
            "MATCH (n:GeopoliticalEvent) DETACH DELETE n",
            "MATCH (n:ThreatFeed) DETACH DELETE n",
            "MATCH (n:EventProcessor) DETACH DELETE n"
        ]

        for query in queries:
            try:
                result = session.run(query)
                summary = result.consume()
                print(f"  Cleared {summary.counters.nodes_deleted} nodes")
            except Exception as e:
                print(f"  Warning: {e}")

    def create_indexes(self, session):
        """Create indexes for Level 5 nodes"""
        print("Creating indexes...")

        indexes = [
            "CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.eventId)",
            "CREATE INDEX IF NOT EXISTS FOR (n:GeopoliticalEvent) ON (n.eventId)",
            "CREATE INDEX IF NOT EXISTS FOR (n:ThreatFeed) ON (n.feedId)",
            "CREATE INDEX IF NOT EXISTS FOR (n:CognitiveBias) ON (n.biasId)",
            "CREATE INDEX IF NOT EXISTS FOR (n:EventProcessor) ON (n.processorId)",
            "CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.severity)",
            "CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.timestamp)",
            "CREATE INDEX IF NOT EXISTS FOR (n:GeopoliticalEvent) ON (n.tensionLevel)"
        ]

        for index_query in indexes:
            try:
                session.run(index_query)
                print(f"  Created index: {index_query.split('ON')[1]}")
            except Exception as e:
                print(f"  Index exists or error: {e}")

    def deploy_information_events(self, session, events):
        """Deploy InformationEvent nodes"""
        print(f"Deploying {len(events)} InformationEvents...")

        batch_size = 500
        for i in range(0, len(events), batch_size):
            batch = events[i:i+batch_size]

            query = """
            UNWIND $events AS event
            CREATE (ie:InformationEvent:Event:Information:RealTime:Level5)
            SET ie = event,
                ie.created = datetime(),
                ie.nodeType = 'InformationEvent',
                ie.level = 5
            RETURN count(ie) as created
            """

            result = session.run(query, events=batch)
            count = result.single()['created']
            self.stats['nodes_created'] += count
            print(f"  Created batch {i//batch_size + 1}: {count} nodes")

        return True

    def deploy_geopolitical_events(self, session, events):
        """Deploy GeopoliticalEvent nodes"""
        print(f"Deploying {len(events)} GeopoliticalEvents...")

        query = """
        UNWIND $events AS event
        CREATE (ge:GeopoliticalEvent:Event:Geopolitical:RealTime:Level5)
        SET ge = event,
            ge.created = datetime(),
            ge.nodeType = 'GeopoliticalEvent',
            ge.level = 5
        RETURN count(ge) as created
        """

        result = session.run(query, events=events)
        count = result.single()['created']
        self.stats['nodes_created'] += count
        print(f"  Created {count} GeopoliticalEvents")

        return True

    def deploy_threat_feeds(self, session, feeds):
        """Deploy ThreatFeed nodes"""
        print(f"Deploying {len(feeds)} ThreatFeeds...")

        query = """
        UNWIND $feeds AS feed
        CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5)
        SET tf = feed,
            tf.created = datetime(),
            tf.nodeType = 'ThreatFeed',
            tf.level = 5
        RETURN count(tf) as created
        """

        result = session.run(query, feeds=feeds)
        count = result.single()['created']
        self.stats['nodes_created'] += count
        print(f"  Created {count} ThreatFeeds")

        return True

    def deploy_cognitive_biases(self, session, biases):
        """Deploy or update CognitiveBias nodes"""
        print(f"Deploying {len(biases)} CognitiveBiases...")

        # First check existing biases
        existing = session.run("MATCH (cb:CognitiveBias) RETURN cb.biasName as name").values()
        existing_names = [record[0] for record in existing if record[0]]

        new_biases = [b for b in biases if b['biasName'] not in existing_names]
        update_biases = [b for b in biases if b['biasName'] in existing_names]

        # Create new biases
        if new_biases:
            query = """
            UNWIND $biases AS bias
            CREATE (cb:CognitiveBias:Psychology:Decision:Level4:Level5)
            SET cb = bias,
                cb.created = datetime(),
                cb.nodeType = 'CognitiveBias',
                cb.level = 5
            RETURN count(cb) as created
            """

            result = session.run(query, biases=new_biases)
            count = result.single()['created']
            self.stats['nodes_created'] += count
            print(f"  Created {count} new CognitiveBiases")

        # Update existing biases with Level 5 properties
        if update_biases:
            query = """
            UNWIND $biases AS bias
            MATCH (cb:CognitiveBias {biasName: bias.biasName})
            SET cb += bias,
                cb:Level5,
                cb.updated = datetime()
            RETURN count(cb) as updated
            """

            result = session.run(query, biases=update_biases)
            count = result.single()['updated']
            print(f"  Updated {count} existing CognitiveBiases")

        return True

    def deploy_event_processors(self, session, processors):
        """Deploy EventProcessor nodes"""
        print(f"Deploying {len(processors)} EventProcessors...")

        query = """
        UNWIND $processors AS processor
        CREATE (ep:EventProcessor:Pipeline:Processing:Level5)
        SET ep = processor,
            ep.created = datetime(),
            ep.nodeType = 'EventProcessor',
            ep.level = 5
        RETURN count(ep) as created
        """

        result = session.run(query, processors=processors)
        count = result.single()['created']
        self.stats['nodes_created'] += count
        print(f"  Created {count} EventProcessors")

        return True

    def create_relationships(self, session):
        """Create relationships between Level 5 nodes and existing infrastructure"""
        print("\nCreating relationships...")

        # 1. PUBLISHES: ThreatFeed -> InformationEvent
        query1 = """
        MATCH (tf:ThreatFeed)
        MATCH (ie:InformationEvent)
        WITH tf, ie, rand() as r
        WHERE r < 0.33  // Each feed publishes ~1/3 of events
        MERGE (tf)-[pub:PUBLISHES {
            created: datetime(),
            reliability: tf.reliability,
            latency: tf.latency
        }]->(ie)
        RETURN count(pub) as created
        """
        result = session.run(query1)
        count = result.single()['created']
        self.stats['relationships_created'] += count
        print(f"  Created {count} PUBLISHES relationships")

        # 2. ACTIVATES_BIAS: InformationEvent -> CognitiveBias
        query2 = """
        MATCH (ie:InformationEvent)
        WHERE ie.fearRealityGap > 2.0
        MATCH (cb:CognitiveBias)
        WITH ie, cb, rand() as r
        WHERE r < 0.2  // 20% chance of activation
        MERGE (ie)-[ab:ACTIVATES_BIAS {
            created: datetime(),
            activationStrength: ie.fearRealityGap / 10.0,
            trigger: 'fear_reality_gap'
        }]->(cb)
        RETURN count(ab) as created
        """
        result = session.run(query2)
        count = result.single()['created']
        self.stats['relationships_created'] += count
        print(f"  Created {count} ACTIVATES_BIAS relationships")

        # 3. AFFECTS_SECTOR: InformationEvent -> Sector (if sectors exist)
        try:
            # Check if sectors exist
            sector_check = session.run("MATCH (s:Sector) RETURN count(s) as count")
            sector_count = sector_check.single()['count']

            if sector_count > 0:
                query3 = """
                MATCH (ie:InformationEvent)
                UNWIND ie.affectedSectors as sectorName
                MATCH (s:Sector)
                WHERE s.name = sectorName OR s.sector = sectorName
                MERGE (ie)-[aff:AFFECTS_SECTOR {
                    created: datetime(),
                    severity: ie.severity,
                    impact: ie.cvssScore / 10.0
                }]->(s)
                RETURN count(aff) as created
                """
                result = session.run(query3)
                count = result.single()['created']
                self.stats['relationships_created'] += count
                print(f"  Created {count} AFFECTS_SECTOR relationships")
            else:
                print("  No Sector nodes found - creating basic sectors")
                self.create_basic_sectors(session)
        except Exception as e:
            print(f"  Warning: Could not create sector relationships: {e}")

        # 4. INCREASES_ACTIVITY: GeopoliticalEvent -> ThreatActor (if exists)
        try:
            actor_check = session.run("MATCH (ta:ThreatActor) RETURN count(ta) as count")
            actor_count = actor_check.single()['count']

            if actor_count > 0:
                query4 = """
                MATCH (ge:GeopoliticalEvent)
                WHERE ge.tensionLevel > 7.0
                MATCH (ta:ThreatActor)
                WITH ge, ta, rand() as r
                WHERE r < 0.3  // 30% correlation
                MERGE (ge)-[inc:INCREASES_ACTIVITY {
                    created: datetime(),
                    correlation: ge.cyberCorrelation,
                    tensionLevel: ge.tensionLevel
                }]->(ta)
                RETURN count(inc) as created
                """
                result = session.run(query4)
                count = result.single()['created']
                self.stats['relationships_created'] += count
                print(f"  Created {count} INCREASES_ACTIVITY relationships")
        except Exception as e:
            print(f"  Warning: Could not create threat actor relationships: {e}")

        # 5. PROCESSES_EVENT: EventProcessor -> Events
        query5 = """
        MATCH (ep:EventProcessor)
        MATCH (e:Event)
        WHERE e:InformationEvent OR e:GeopoliticalEvent
        WITH ep, e, rand() as r
        WHERE r < 0.1  // Each processor handles 10% of events
        MERGE (ep)-[proc:PROCESSES_EVENT {
            created: datetime(),
            processingType: ep.processorType,
            latency: ep.latency
        }]->(e)
        RETURN count(proc) as created
        """
        result = session.run(query5)
        count = result.single()['created']
        self.stats['relationships_created'] += count
        print(f"  Created {count} PROCESSES_EVENT relationships")

        # 6. CORRELATES_WITH: InformationEvent -> InformationEvent
        query6 = """
        MATCH (ie1:InformationEvent)
        MATCH (ie2:InformationEvent)
        WHERE ie1.eventId < ie2.eventId
        AND (
            (ie1.severity = ie2.severity AND rand() < 0.05) OR
            (ANY(s IN ie1.affectedSectors WHERE s IN ie2.affectedSectors) AND rand() < 0.03)
        )
        MERGE (ie1)-[corr:CORRELATES_WITH {
            created: datetime(),
            correlationType: CASE
                WHEN ie1.severity = ie2.severity THEN 'severity'
                ELSE 'sector'
            END,
            strength: rand()
        }]->(ie2)
        RETURN count(corr) as created
        LIMIT 5000
        """
        result = session.run(query6)
        count = result.single()['created']
        self.stats['relationships_created'] += count
        print(f"  Created {count} CORRELATES_WITH relationships")

    def create_basic_sectors(self, session):
        """Create basic sector nodes if they don't exist"""
        sectors = [
            'Energy', 'Water', 'Transportation', 'Healthcare',
            'Financial', 'Communications', 'Manufacturing', 'IT',
            'Chemical', 'Nuclear', 'Defense', 'Food',
            'Government', 'Emergency', 'Dams', 'Commercial'
        ]

        query = """
        UNWIND $sectors AS sectorName
        MERGE (s:Sector {name: sectorName})
        SET s.created = datetime(),
            s.sector = sectorName,
            s.level = 2
        RETURN count(s) as created
        """

        result = session.run(query, sectors=sectors)
        count = result.single()['created']
        print(f"    Created {count} basic Sector nodes")

    def validate_deployment(self, session):
        """Validate the deployment"""
        print("\n=== Deployment Validation ===")

        validation_queries = [
            ("InformationEvents", "MATCH (n:InformationEvent) RETURN count(n) as count"),
            ("GeopoliticalEvents", "MATCH (n:GeopoliticalEvent) RETURN count(n) as count"),
            ("ThreatFeeds", "MATCH (n:ThreatFeed) RETURN count(n) as count"),
            ("CognitiveBiases", "MATCH (n:CognitiveBias) RETURN count(n) as count"),
            ("EventProcessors", "MATCH (n:EventProcessor) RETURN count(n) as count"),
            ("Level5 Nodes", "MATCH (n:Level5) RETURN count(n) as count"),
            ("Total Relationships", "MATCH ()-[r]->() WHERE type(r) IN ['PUBLISHES', 'ACTIVATES_BIAS', 'AFFECTS_SECTOR', 'PROCESSES_EVENT', 'CORRELATES_WITH'] RETURN count(r) as count")
        ]

        total_nodes = 0
        for name, query in validation_queries:
            result = session.run(query)
            count = result.single()['count']
            print(f"{name}: {count:,}")
            if name != "Total Relationships" and name != "CognitiveBiases":
                total_nodes += count

        # Special handling for CognitiveBias (only count new ones for total)
        cb_result = session.run("MATCH (n:CognitiveBias:Level5) RETURN count(n) as count")
        level5_cb_count = cb_result.single()['count']
        total_nodes += level5_cb_count

        print(f"\nTotal Level 5 Nodes: {total_nodes:,}")

        # Check relationship counts
        print("\n=== Relationship Counts ===")
        rel_queries = [
            ("PUBLISHES", "MATCH ()-[r:PUBLISHES]->() RETURN count(r) as count"),
            ("ACTIVATES_BIAS", "MATCH ()-[r:ACTIVATES_BIAS]->() RETURN count(r) as count"),
            ("AFFECTS_SECTOR", "MATCH ()-[r:AFFECTS_SECTOR]->() RETURN count(r) as count"),
            ("PROCESSES_EVENT", "MATCH ()-[r:PROCESSES_EVENT]->() RETURN count(r) as count"),
            ("CORRELATES_WITH", "MATCH ()-[r:CORRELATES_WITH]->() RETURN count(r) as count")
        ]

        for name, query in rel_queries:
            result = session.run(query)
            count = result.single()['count']
            print(f"{name}: {count:,}")

        return total_nodes

    def deploy(self, data_file):
        """Main deployment function"""
        print(f"\n=== Level 5 Deployment Starting ===")
        print(f"Time: {datetime.now()}")

        # Load data
        with open(data_file, 'r') as f:
            data = json.load(f)

        print(f"Loaded {data['metadata']['total_nodes']} nodes from {data_file}")

        with self.driver.session() as session:
            try:
                # Optional: Clear existing Level 5 nodes (commented out for safety)
                # self.clear_level5_nodes(session)

                # Create indexes
                self.create_indexes(session)

                # Deploy nodes
                self.deploy_information_events(session, data['data']['information_events'])
                self.deploy_geopolitical_events(session, data['data']['geopolitical_events'])
                self.deploy_threat_feeds(session, data['data']['threat_feeds'])
                self.deploy_cognitive_biases(session, data['data']['cognitive_biases'])
                self.deploy_event_processors(session, data['data']['event_processors'])

                # Create relationships
                self.create_relationships(session)

                # Validate deployment
                total = self.validate_deployment(session)

                # Print summary
                elapsed = (datetime.now() - self.stats['start_time']).seconds
                print(f"\n=== Deployment Complete ===")
                print(f"Nodes created: {self.stats['nodes_created']:,}")
                print(f"Relationships created: {self.stats['relationships_created']:,}")
                print(f"Errors: {len(self.stats['errors'])}")
                print(f"Time elapsed: {elapsed} seconds")

                # Success criteria check
                if total >= 5500:
                    print(f"\n✅ SUCCESS: Deployed {total:,} Level 5 nodes (target: 6,000)")
                else:
                    print(f"\n⚠️  WARNING: Only {total:,} nodes deployed (target: 6,000)")

                return True

            except Exception as e:
                print(f"\n❌ ERROR: Deployment failed")
                print(f"Error: {e}")
                traceback.print_exc()
                self.stats['errors'].append(str(e))
                return False

def main():
    """Main execution"""
    # Check for data file
    data_file = '/home/jim/2_OXOT_Projects_Dev/data/level5_generated_data.json'
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        print("Please run level5_data_generator.py first")
        sys.exit(1)

    # Deploy to Neo4j
    deployer = Level5Deployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        success = deployer.deploy(data_file)

        if success:
            print("\n🎯 Level 5 deployment completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Level 5 deployment failed")
            sys.exit(1)

    finally:
        deployer.close()

if __name__ == "__main__":
    main()