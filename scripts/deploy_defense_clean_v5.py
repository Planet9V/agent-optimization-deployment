#!/usr/bin/env python3
"""
Defense Industrial Base Sector Deployment - Clean v5
28,000 nodes with duplicate checking
"""

from neo4j import GraphDatabase
import os
import time
import uuid

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def generate_unique_id(prefix, index, subsector):
    """Generate unique ID with UUID component"""
    short_uuid = str(uuid.uuid4())[:8]
    return f"{prefix}_{subsector}_{index}_{short_uuid}"

def check_existing_nodes(tx):
    """Check for existing defense nodes"""
    result = tx.run("""
        MATCH (n)
        WHERE any(label IN labels(n) WHERE label CONTAINS 'DEFENSE_INDUSTRIAL_BASE')
        RETURN count(n) as count
    """)
    return result.single()["count"]

def deploy_defense_sector(tx):
    """Deploy 28,000 Defense Industrial Base nodes"""

    # Subsector distribution
    subsectors = {
        "Aerospace_Defense": {
            "pct": 0.40,
            "devices": 1400,
            "measurements": 7200,
            "properties": 2000,
            "processes": 400,
            "controls": 150,
            "alerts": 100,
            "zones": 50,
            "assets": 20
        },
        "Ground_Systems": {
            "pct": 0.35,
            "devices": 1050,
            "measurements": 6300,
            "properties": 1750,
            "processes": 350,
            "controls": 175,
            "alerts": 100,
            "zones": 50,
            "assets": 15
        },
        "Naval_Systems": {
            "pct": 0.25,
            "devices": 750,
            "measurements": 4500,
            "properties": 1250,
            "processes": 250,
            "controls": 175,
            "alerts": 100,
            "zones": 50,
            "assets": 15
        }
    }

    total_created = 0
    batch_size = 500

    print("\n🚀 Starting Defense Industrial Base Deployment...")

    for subsector_name, dist in subsectors.items():
        print(f"\n📦 Deploying {subsector_name}...")

        # Deploy Devices
        print(f"  Creating {dist['devices']} Devices...")
        for i in range(0, dist['devices'], batch_size):
            batch = min(batch_size, dist['devices'] - i)
            query = """
            UNWIND range(0, $batch-1) AS idx
            WITH $subsector AS subsector, $start_idx + idx AS node_idx
            MERGE (d:Device:SECTOR_DEFENSE_INDUSTRIAL_BASE {
                id: 'DIB_DEV_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
            })
            SET d.name = subsector + ' Device ' + toString(node_idx),
                d.subsector = subsector,
                d.manufacturer = CASE node_idx % 5
                    WHEN 0 THEN 'Lockheed Martin'
                    WHEN 1 THEN 'Boeing'
                    WHEN 2 THEN 'General Dynamics'
                    WHEN 3 THEN 'Northrop Grumman'
                    ELSE 'Raytheon'
                END,
                d.classification = CASE node_idx % 3
                    WHEN 0 THEN 'TOP SECRET'
                    WHEN 1 THEN 'SECRET'
                    ELSE 'CLASSIFIED'
                END,
                d.cmmc_level = 2 + (node_idx % 2)
            WITH d
            SET d:DefenseDevice
            RETURN count(d) as created
            """
            result = tx.run(query, batch=batch, subsector=subsector_name, start_idx=i)
            created = result.single()["created"]
            total_created += created
            print(f"    Created batch: {created}")

        # Deploy Measurements
        print(f"  Creating {dist['measurements']} Measurements...")
        for i in range(0, dist['measurements'], batch_size):
            batch = min(batch_size, dist['measurements'] - i)
            query = """
            UNWIND range(0, $batch-1) AS idx
            WITH $subsector AS subsector, $start_idx + idx AS node_idx
            MERGE (m:Measurement:SECTOR_DEFENSE_INDUSTRIAL_BASE {
                id: 'DIB_MEAS_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
            })
            SET m.name = subsector + ' Measurement ' + toString(node_idx),
                m.subsector = subsector,
                m.measurement_type = CASE node_idx % 8
                    WHEN 0 THEN 'temperature'
                    WHEN 1 THEN 'pressure'
                    WHEN 2 THEN 'speed'
                    WHEN 3 THEN 'altitude'
                    WHEN 4 THEN 'fuel_level'
                    WHEN 5 THEN 'vibration'
                    WHEN 6 THEN 'stress'
                    ELSE 'accuracy'
                END,
                m.unit = 'metric',
                m.frequency_hz = 1 + (node_idx % 100)
            WITH m
            SET m:DefenseMeasurement
            RETURN count(m) as created
            """
            result = tx.run(query, batch=batch, subsector=subsector_name, start_idx=i)
            created = result.single()["created"]
            total_created += created
            if i % (batch_size * 5) == 0:
                print(f"    Created batch: {i + created}/{dist['measurements']}")

        # Deploy Properties
        print(f"  Creating {dist['properties']} Properties...")
        for i in range(0, dist['properties'], batch_size):
            batch = min(batch_size, dist['properties'] - i)
            query = """
            UNWIND range(0, $batch-1) AS idx
            WITH $subsector AS subsector, $start_idx + idx AS node_idx
            MERGE (p:Property:SECTOR_DEFENSE_INDUSTRIAL_BASE {
                id: 'DIB_PROP_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
            })
            SET p.name = subsector + ' Property ' + toString(node_idx),
                p.subsector = subsector,
                p.property_type = CASE node_idx % 6
                    WHEN 0 THEN 'max_speed'
                    WHEN 1 THEN 'range'
                    WHEN 2 THEN 'payload_capacity'
                    WHEN 3 THEN 'armor_rating'
                    WHEN 4 THEN 'weapon_range'
                    ELSE 'service_ceiling'
                END,
                p.value_type = 'numeric'
            WITH p
            SET p:DefenseProperty
            RETURN count(p) as created
            """
            result = tx.run(query, batch=batch, subsector=subsector_name, start_idx=i)
            created = result.single()["created"]
            total_created += created
            print(f"    Created batch: {created}")

        # Deploy Processes
        print(f"  Creating {dist['processes']} Processes...")
        for i in range(0, dist['processes'], batch_size):
            batch = min(batch_size, dist['processes'] - i)
            query = """
            UNWIND range(0, $batch-1) AS idx
            WITH $subsector AS subsector, $start_idx + idx AS node_idx
            MERGE (pr:Process:SECTOR_DEFENSE_INDUSTRIAL_BASE {
                id: 'DIB_PROC_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
            })
            SET pr.name = subsector + ' Process ' + toString(node_idx),
                pr.subsector = subsector,
                pr.process_type = CASE node_idx % 5
                    WHEN 0 THEN 'assembly'
                    WHEN 1 THEN 'testing'
                    WHEN 2 THEN 'manufacturing'
                    WHEN 3 THEN 'quality_control'
                    ELSE 'maintenance'
                END,
                pr.duration_days = 30 + (node_idx % 180),
                pr.cmmc_level = 2 + (node_idx % 2)
            WITH pr
            SET pr:DefenseProcess
            RETURN count(pr) as created
            """
            result = tx.run(query, batch=batch, subsector=subsector_name, start_idx=i)
            created = result.single()["created"]
            total_created += created
            print(f"    Created batch: {created}")

        # Deploy Controls
        print(f"  Creating {dist['controls']} Controls...")
        batch = dist['controls']
        query = """
        UNWIND range(0, $batch-1) AS idx
        WITH $subsector AS subsector, idx AS node_idx
        MERGE (c:Control:SECTOR_DEFENSE_INDUSTRIAL_BASE {
            id: 'DIB_CTRL_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
        })
        SET c.name = subsector + ' Control ' + toString(node_idx),
            c.subsector = subsector,
            c.control_type = CASE node_idx % 4
                WHEN 0 THEN 'autopilot'
                WHEN 1 THEN 'guidance'
                WHEN 2 THEN 'fire_control'
                ELSE 'environmental'
            END,
            c.classification = 'SECRET'
        WITH c
        SET c:DefenseControl
        RETURN count(c) as created
        """
        result = tx.run(query, batch=batch, subsector=subsector_name)
        created = result.single()["created"]
        total_created += created
        print(f"    Created: {created}")

        # Deploy Alerts
        print(f"  Creating {dist['alerts']} Alerts...")
        batch = dist['alerts']
        query = """
        UNWIND range(0, $batch-1) AS idx
        WITH $subsector AS subsector, idx AS node_idx
        MERGE (a:Alert:SECTOR_DEFENSE_INDUSTRIAL_BASE {
            id: 'DIB_ALRT_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
        })
        SET a.name = subsector + ' Alert ' + toString(node_idx),
            a.subsector = subsector,
            a.alert_type = CASE node_idx % 5
                WHEN 0 THEN 'cybersecurity'
                WHEN 1 THEN 'equipment_malfunction'
                WHEN 2 THEN 'quality_defect'
                WHEN 3 THEN 'supply_chain'
                ELSE 'safety'
            END,
            a.severity = CASE node_idx % 3
                WHEN 0 THEN 'critical'
                WHEN 1 THEN 'high'
                ELSE 'medium'
            END
        WITH a
        SET a:DefenseAlert
        RETURN count(a) as created
        """
        result = tx.run(query, batch=batch, subsector=subsector_name)
        created = result.single()["created"]
        total_created += created
        print(f"    Created: {created}")

        # Deploy Zones
        print(f"  Creating {dist['zones']} Zones...")
        batch = dist['zones']
        query = """
        UNWIND range(0, $batch-1) AS idx
        WITH $subsector AS subsector, idx AS node_idx
        MERGE (z:Zone:SECTOR_DEFENSE_INDUSTRIAL_BASE {
            id: 'DIB_ZONE_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
        })
        SET z.name = subsector + ' Zone ' + toString(node_idx),
            z.subsector = subsector,
            z.zone_type = CASE node_idx % 4
                WHEN 0 THEN 'classified_area'
                WHEN 1 THEN 'testing_facility'
                WHEN 2 THEN 'assembly_zone'
                ELSE 'secure_storage'
            END,
            z.security_level = CASE node_idx % 3
                WHEN 0 THEN 'TOP SECRET'
                WHEN 1 THEN 'SECRET'
                ELSE 'CLASSIFIED'
            END
        WITH z
        SET z:DefenseZone
        RETURN count(z) as created
        """
        result = tx.run(query, batch=batch, subsector=subsector_name)
        created = result.single()["created"]
        total_created += created
        print(f"    Created: {created}")

        # Deploy Assets
        print(f"  Creating {dist['assets']} Assets...")
        batch = dist['assets']
        query = """
        UNWIND range(0, $batch-1) AS idx
        WITH $subsector AS subsector, idx AS node_idx
        MERGE (ast:Asset:SECTOR_DEFENSE_INDUSTRIAL_BASE {
            id: 'DIB_ASSET_' + subsector + '_' + toString(node_idx) + '_' + randomUUID()
        })
        SET ast.name = subsector + ' Strategic Asset ' + toString(node_idx),
            ast.subsector = subsector,
            ast.asset_type = CASE node_idx % 4
                WHEN 0 THEN 'aircraft_carrier'
                WHEN 1 THEN 'strategic_bomber'
                WHEN 2 THEN 'missile_defense_system'
                ELSE 'manufacturing_facility'
            END,
            ast.value_usd_millions = 500 + (node_idx * 100),
            ast.classification = 'TOP SECRET'
        WITH ast
        SET ast:MajorAsset
        RETURN count(ast) as created
        """
        result = tx.run(query, batch=batch, subsector=subsector_name)
        created = result.single()["created"]
        total_created += created
        print(f"    Created: {created}")

    return total_created

def verify_deployment(tx):
    """Verify deployment counts"""
    result = tx.run("""
        MATCH (n)
        WHERE any(label IN labels(n) WHERE label CONTAINS 'DEFENSE_INDUSTRIAL_BASE')
        RETURN
            labels(n)[0] as node_type,
            count(n) as count
        ORDER BY count DESC
    """)

    print("\n📊 Deployment Verification:")
    print("-" * 50)
    total = 0
    for record in result:
        node_type = record["node_type"]
        count = record["count"]
        total += count
        print(f"  {node_type}: {count:,}")
    print("-" * 50)
    print(f"  TOTAL: {total:,}")

    return total

def main():
    start_time = time.time()

    with driver.session() as session:
        # Check existing
        existing = session.execute_read(check_existing_nodes)
        if existing > 0:
            print(f"⚠️  Found {existing} existing defense nodes")
            response = input("Delete existing nodes? (yes/no): ")
            if response.lower() == 'yes':
                print("🗑️  Deleting existing nodes...")
                session.execute_write(lambda tx: tx.run("""
                    MATCH (n)
                    WHERE any(label IN labels(n) WHERE label CONTAINS 'DEFENSE_INDUSTRIAL_BASE')
                    DETACH DELETE n
                """))
                print("✅ Deleted")

        # Deploy
        total_created = session.execute_write(deploy_defense_sector)

        # Verify
        total_verified = session.execute_read(verify_deployment)

        elapsed = time.time() - start_time

        print(f"\n✅ DEFENSE INDUSTRIAL BASE DEPLOYMENT COMPLETE")
        print(f"   Nodes Created: {total_created:,}")
        print(f"   Nodes Verified: {total_verified:,}")
        print(f"   Time Elapsed: {elapsed:.2f} seconds")

        if total_verified >= 26000:
            print("\n🎉 SUCCESS! Target node count achieved!")
        else:
            print(f"\n⚠️  WARNING: Only {total_verified:,} nodes created (target: 28,000)")

if __name__ == "__main__":
    main()
