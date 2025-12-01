#!/usr/bin/env python3
"""
Complete Communications Sector Deployment
Creates missing node types and relationships for COMMUNICATIONS sector
"""

from neo4j import GraphDatabase
import json
import random
from datetime import datetime, timedelta

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Subsectors for Communications
SUBSECTORS = [
    "Wireless (except Satellite)",
    "Satellite",
    "Cable",
    "Wireline"
]

class CommunicationsDeployer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log = []

    def close(self):
        self.driver.close()

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.log.append(log_entry)

    def save_log(self, filepath):
        with open(filepath, 'w') as f:
            f.write('\n'.join(self.log))

    def create_routing_processes(self, session, count=1000):
        """Create RoutingProcess nodes"""
        self.log_message(f"Creating {count} RoutingProcess nodes...")

        batch_size = 100
        created = 0

        for i in range(0, count, batch_size):
            batch = min(batch_size, count - i)

            query = """
            UNWIND range(1, $batch) as idx
            WITH idx, $i + idx as id
            CREATE (p:Process:RoutingProcess:Communications:COMMUNICATIONS)
            SET p.uid = 'routing-process-' + toString(id),
                p.name = 'Routing Process ' + toString(id),
                p.process_type = ['BGP', 'OSPF', 'EIGRP', 'RIP', 'IS-IS'][id % 5],
                p.protocol = ['BGP', 'OSPF', 'EIGRP', 'RIP', 'IS-IS', 'MPLS'][id % 6],
                p.traffic_volume_gbps = toFloat(rand() * 100),
                p.active = true,
                p.priority = toInteger(rand() * 10) + 1,
                p.routes_count = toInteger(rand() * 10000),
                p.subsector = ['Wireless (except Satellite)', 'Satellite', 'Cable', 'Wireline'][id % 4],
                p.created_at = datetime(),
                p.updated_at = datetime()
            RETURN count(p) as created
            """

            result = session.run(query, i=i, batch=batch)
            record = result.single()
            created += record['created'] if record else 0

            if (i + batch) % 500 == 0:
                self.log_message(f"  Created {i + batch}/{count} RoutingProcess nodes")

        self.log_message(f"✅ Created {created} RoutingProcess nodes")
        return created

    def create_network_management_systems(self, session, count=500):
        """Create NetworkManagementSystem (Control) nodes"""
        self.log_message(f"Creating {count} NetworkManagementSystem nodes...")

        batch_size = 50
        created = 0

        for i in range(0, count, batch_size):
            batch = min(batch_size, count - i)

            query = """
            UNWIND range(1, $batch) as idx
            WITH idx, $i + idx as id
            CREATE (n:Control:NetworkManagementSystem:Communications:COMMUNICATIONS)
            SET n.uid = 'nms-' + toString(id),
                n.name = 'Network Management System ' + toString(id),
                n.vendor = ['Cisco', 'Juniper', 'HPE', 'Nokia', 'Ericsson'][id % 5],
                n.version = '1.' + toString(id % 10) + '.' + toString(id % 100),
                n.management_protocol = ['SNMP', 'NetFlow', 'sFlow', 'IPFIX'][id % 4],
                n.monitoring_interval_sec = [30, 60, 120, 300][id % 4],
                n.managed_devices_count = toInteger(rand() * 500) + 50,
                n.alert_threshold = toFloat(rand() * 100),
                n.subsector = ['Wireless (except Satellite)', 'Satellite', 'Cable', 'Wireline'][id % 4],
                n.created_at = datetime(),
                n.updated_at = datetime()
            RETURN count(n) as created
            """

            result = session.run(query, i=i, batch=batch)
            record = result.single()
            created += record['created'] if record else 0

            if (i + batch) % 250 == 0:
                self.log_message(f"  Created {i + batch}/{count} NetworkManagementSystem nodes")

        self.log_message(f"✅ Created {created} NetworkManagementSystem nodes")
        return created

    def create_communications_alerts(self, session, count=300):
        """Create CommunicationsAlert nodes"""
        self.log_message(f"Creating {count} CommunicationsAlert nodes...")

        batch_size = 50
        created = 0

        for i in range(0, count, batch_size):
            batch = min(batch_size, count - i)

            query = """
            UNWIND range(1, $batch) as idx
            WITH idx, $i + idx as id
            CREATE (a:CommunicationsAlert:Alert:Monitoring:COMMUNICATIONS)
            SET a.uid = 'comm-alert-' + toString(id),
                a.name = 'Alert ' + toString(id),
                a.alert_type = ['Bandwidth_Threshold', 'Latency_Spike', 'Packet_Loss', 'Device_Down', 'Security_Event'][id % 5],
                a.severity = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'][id % 5],
                a.status = ['ACTIVE', 'ACKNOWLEDGED', 'RESOLVED'][id % 3],
                a.triggered_at = datetime() - duration({hours: toInteger(rand() * 168)}),
                a.resolved_at = CASE WHEN id % 3 = 2 THEN datetime() - duration({hours: toInteger(rand() * 24)}) ELSE null END,
                a.description = 'Communications alert for event ' + toString(id),
                a.affected_devices_count = toInteger(rand() * 20) + 1,
                a.subsector = ['Wireless (except Satellite)', 'Satellite', 'Cable', 'Wireline'][id % 4],
                a.created_at = datetime(),
                a.updated_at = datetime()
            RETURN count(a) as created
            """

            result = session.run(query, i=i, batch=batch)
            record = result.single()
            created += record['created'] if record else 0

        self.log_message(f"✅ Created {created} CommunicationsAlert nodes")
        return created

    def create_communications_zones(self, session, count=150):
        """Create CommunicationsZone nodes"""
        self.log_message(f"Creating {count} CommunicationsZone nodes...")

        batch_size = 50
        created = 0

        for i in range(0, count, batch_size):
            batch = min(batch_size, count - i)

            query = """
            UNWIND range(1, $batch) as idx
            WITH idx, $i + idx as id
            CREATE (z:CommunicationsZone:Zone:Asset:COMMUNICATIONS)
            SET z.uid = 'comm-zone-' + toString(id),
                z.name = 'Communications Zone ' + toString(id),
                z.zone_type = ['Core_Network', 'Edge_Network', 'Access_Network', 'Backhaul', 'Distribution'][id % 5],
                z.location = ['Region-' + toString((id % 10) + 1), 'City-' + toString((id % 20) + 1)][id % 2],
                z.capacity_gbps = toFloat((rand() * 1000) + 100),
                z.device_count = toInteger(rand() * 50) + 10,
                z.redundancy_level = ['Primary', 'Secondary', 'Tertiary'][id % 3],
                z.subsector = ['Wireless (except Satellite)', 'Satellite', 'Cable', 'Wireline'][id % 4],
                z.created_at = datetime(),
                z.updated_at = datetime()
            RETURN count(z) as created
            """

            result = session.run(query, i=i, batch=batch)
            record = result.single()
            created += record['created'] if record else 0

        self.log_message(f"✅ Created {created} CommunicationsZone nodes")
        return created

    def create_major_assets(self, session, count=50):
        """Create MajorAsset nodes"""
        self.log_message(f"Creating {count} MajorAsset nodes...")

        query = """
        UNWIND range(1, $count) as id
        CREATE (m:MajorAsset:Asset:Communications:COMMUNICATIONS)
        SET m.uid = 'major-asset-' + toString(id),
            m.name = 'Major Asset ' + toString(id),
            m.asset_type = ['Data_Center', 'Network_Operations_Center', 'Switching_Station', 'Satellite_Ground_Station', 'Cable_Head_End'][id % 5],
            m.location = 'Region-' + toString((id % 10) + 1),
            m.total_capacity_gbps = toFloat((rand() * 10000) + 1000),
            m.criticality_score = toFloat((rand() * 5) + 5),
            m.commissioned_date = date() - duration({days: toInteger(rand() * 3650)}),
            m.devices_count = toInteger(rand() * 500) + 100,
            m.subsector = ['Wireless (except Satellite)', 'Satellite', 'Cable', 'Wireline'][id % 4],
            m.created_at = datetime(),
            m.updated_at = datetime()
        RETURN count(m) as created
        """

        result = session.run(query, count=count)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} MajorAsset nodes")
        return created

    def create_has_property_relationships(self, session):
        """Create HAS_PROPERTY relationships: Device/Process → Property"""
        self.log_message(f"Creating HAS_PROPERTY relationships...")

        # Device → Property (target: ~2300, 1 per device)
        query = """
        MATCH (d:CommunicationsDevice)
        WHERE 'COMMUNICATIONS' IN labels(d)
        WITH d
        CALL {
            WITH d
            MATCH (p:CommunicationsProperty)
            WHERE 'COMMUNICATIONS' IN labels(p) AND p.subsector = d.subsector
            RETURN p ORDER BY rand() LIMIT 1
        }
        MERGE (d)-[r:HAS_PROPERTY]->(p)
        ON CREATE SET r.created_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        device_props = record['created'] if record else 0

        # Process → Property (target: ~2000, 1-2 per process)
        query = """
        MATCH (rp:RoutingProcess)
        WHERE 'COMMUNICATIONS' IN labels(rp)
        WITH rp
        CALL {
            WITH rp
            MATCH (p:CommunicationsProperty)
            WHERE 'COMMUNICATIONS' IN labels(p) AND p.subsector = rp.subsector
            RETURN p ORDER BY rand() LIMIT 2
        }
        MERGE (rp)-[r:HAS_PROPERTY]->(p)
        ON CREATE SET r.created_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        process_props = record['created'] if record else 0

        total = device_props + process_props
        self.log_message(f"✅ Created {total} HAS_PROPERTY relationships")
        return total

    def create_controls_relationships(self, session):
        """Create CONTROLS relationships: NetworkManagementSystem → Device/Process"""
        self.log_message(f"Creating CONTROLS relationships...")

        # NMS → Device (target: ~2300, every device managed)
        query = """
        MATCH (nms:NetworkManagementSystem)
        WHERE 'COMMUNICATIONS' IN labels(nms)
        WITH nms
        CALL {
            WITH nms
            MATCH (d:CommunicationsDevice)
            WHERE 'COMMUNICATIONS' IN labels(d) AND d.subsector = nms.subsector
            RETURN d ORDER BY rand() LIMIT 5
        }
        MERGE (nms)-[r:CONTROLS]->(d)
        ON CREATE SET r.control_type = 'monitoring',
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        device_controls = record['created'] if record else 0

        # NMS → Process (target: ~1500)
        query = """
        MATCH (nms:NetworkManagementSystem)
        WHERE 'COMMUNICATIONS' IN labels(nms)
        WITH nms
        CALL {
            WITH nms
            MATCH (rp:RoutingProcess)
            WHERE 'COMMUNICATIONS' IN labels(rp) AND rp.subsector = nms.subsector
            RETURN rp ORDER BY rand() LIMIT 3
        }
        MERGE (nms)-[r:CONTROLS]->(rp)
        ON CREATE SET r.control_type = 'process_management',
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        process_controls = record['created'] if record else 0

        total = device_controls + process_controls
        self.log_message(f"✅ Created {total} CONTROLS relationships")
        return total

    def create_contains_relationships(self, session):
        """Create CONTAINS relationships: Zone → Device"""
        self.log_message(f"Creating CONTAINS relationships...")

        query = """
        MATCH (z:CommunicationsZone)
        WHERE 'COMMUNICATIONS' IN labels(z)
        WITH z
        CALL {
            WITH z
            MATCH (d:CommunicationsDevice)
            WHERE 'COMMUNICATIONS' IN labels(d) AND d.subsector = z.subsector
            RETURN d ORDER BY rand() LIMIT 15
        }
        MERGE (z)-[r:CONTAINS]->(d)
        ON CREATE SET r.placement_date = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} CONTAINS relationships")
        return created

    def create_routes_through_relationships(self, session):
        """Create ROUTES_THROUGH relationships: Device → Device"""
        self.log_message(f"Creating ROUTES_THROUGH relationships...")

        query = """
        MATCH (d1:CommunicationsDevice)
        WHERE 'COMMUNICATIONS' IN labels(d1) AND d1.device_type IN ['Router', 'Switch', 'Gateway']
        WITH d1
        CALL {
            WITH d1
            MATCH (d2:CommunicationsDevice)
            WHERE 'COMMUNICATIONS' IN labels(d2)
                AND d2.device_type IN ['Router', 'Switch', 'Gateway']
                AND d1.subsector = d2.subsector
                AND d1.uid <> d2.uid
            RETURN d2 ORDER BY rand() LIMIT 2
        }
        MERGE (d1)-[r:ROUTES_THROUGH]->(d2)
        ON CREATE SET r.bandwidth_mbps = toFloat(rand() * 10000),
            r.latency_ms = toFloat(rand() * 100),
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} ROUTES_THROUGH relationships")
        return created

    def create_connects_to_network_relationships(self, session):
        """Create CONNECTS_TO_NETWORK relationships: Device → Zone"""
        self.log_message(f"Creating CONNECTS_TO_NETWORK relationships...")

        query = """
        MATCH (d:CommunicationsDevice)
        WHERE 'COMMUNICATIONS' IN labels(d)
        WITH d
        CALL {
            WITH d
            MATCH (z:CommunicationsZone)
            WHERE 'COMMUNICATIONS' IN labels(z) AND z.subsector = d.subsector
            RETURN z ORDER BY rand() LIMIT 1
        }
        MERGE (d)-[r:CONNECTS_TO_NETWORK]->(z)
        ON CREATE SET r.connection_type = ['Primary', 'Secondary', 'Backup'][toInteger(rand() * 3)],
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} CONNECTS_TO_NETWORK relationships")
        return created

    def create_managed_by_nms_relationships(self, session):
        """Create MANAGED_BY_NMS relationships: Device → NetworkManagementSystem"""
        self.log_message(f"Creating MANAGED_BY_NMS relationships...")

        query = """
        MATCH (d:CommunicationsDevice)
        WHERE 'COMMUNICATIONS' IN labels(d)
        WITH d
        CALL {
            WITH d
            MATCH (nms:NetworkManagementSystem)
            WHERE 'COMMUNICATIONS' IN labels(nms) AND nms.subsector = d.subsector
            RETURN nms ORDER BY rand() LIMIT 1
        }
        MERGE (d)-[r:MANAGED_BY_NMS]->(nms)
        ON CREATE SET r.management_protocol = ['SNMP', 'NetFlow', 'sFlow'][toInteger(rand() * 3)],
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} MANAGED_BY_NMS relationships")
        return created

    def create_uses_device_relationships(self, session):
        """Create USES_DEVICE relationships: Process → Device"""
        self.log_message(f"Creating USES_DEVICE relationships...")

        query = """
        MATCH (rp:RoutingProcess)
        WHERE 'COMMUNICATIONS' IN labels(rp)
        WITH rp
        CALL {
            WITH rp
            MATCH (d:CommunicationsDevice)
            WHERE 'COMMUNICATIONS' IN labels(d)
                AND d.device_type IN ['Router', 'Switch', 'Gateway']
                AND d.subsector = rp.subsector
            RETURN d ORDER BY rand() LIMIT 2
        }
        MERGE (rp)-[r:USES_DEVICE]->(d)
        ON CREATE SET r.usage_type = 'routing',
            r.established_at = datetime()
        RETURN count(r) as created
        """

        result = session.run(query)
        record = result.single()
        created = record['created'] if record else 0

        self.log_message(f"✅ Created {created} USES_DEVICE relationships")
        return created

    def verify_deployment(self, session):
        """Verify the complete deployment"""
        self.log_message("\n=== VERIFICATION ===")

        # Total nodes
        result = session.run("""
            MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n)
            RETURN count(n) as total
        """)
        total_nodes = result.single()['total']
        self.log_message(f"Total COMMUNICATIONS nodes: {total_nodes}")

        # Node types
        result = session.run("""
            MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n)
            WITH DISTINCT labels(n) as lbls
            UNWIND lbls as lbl
            WITH DISTINCT lbl
            WHERE lbl IN ['CommunicationsDevice', 'CommunicationsProperty',
                'NetworkMeasurement', 'RoutingProcess', 'NetworkManagementSystem',
                'CommunicationsAlert', 'CommunicationsZone', 'MajorAsset']
            RETURN collect(lbl) as types, count(lbl) as type_count
        """)
        record = result.single()
        self.log_message(f"Unique node types: {record['type_count']}")
        self.log_message(f"Types: {record['types']}")

        # Node counts by type
        node_types = [
            'CommunicationsDevice', 'CommunicationsProperty', 'NetworkMeasurement',
            'RoutingProcess', 'NetworkManagementSystem', 'CommunicationsAlert',
            'CommunicationsZone', 'MajorAsset'
        ]

        self.log_message("\nNode counts by type:")
        for node_type in node_types:
            result = session.run(f"""
                MATCH (n:{node_type})
                WHERE 'COMMUNICATIONS' IN labels(n)
                RETURN count(n) as count
            """)
            count = result.single()['count']
            self.log_message(f"  {node_type}: {count}")

        # Total relationships
        result = session.run("""
            MATCH (n)-[r]->(m)
            WHERE 'COMMUNICATIONS' IN labels(n)
            RETURN count(r) as total
        """)
        total_rels = result.single()['total']
        self.log_message(f"\nTotal relationships: {total_rels}")

        # Relationships by type
        result = session.run("""
            MATCH (n)-[r]->(m)
            WHERE 'COMMUNICATIONS' IN labels(n)
            RETURN type(r) as rel_type, count(r) as count
            ORDER BY count DESC
        """)

        self.log_message("\nRelationships by type:")
        for record in result:
            self.log_message(f"  {record['rel_type']}: {record['count']}")

        return total_nodes, total_rels

    def deploy_all(self):
        """Execute full deployment"""
        self.log_message("="*60)
        self.log_message("COMMUNICATIONS SECTOR COMPLETION DEPLOYMENT")
        self.log_message("="*60)

        with self.driver.session() as session:
            # Create missing node types
            self.log_message("\n--- CREATING MISSING NODE TYPES ---\n")
            self.create_routing_processes(session, 1000)
            self.create_network_management_systems(session, 500)
            self.create_communications_alerts(session, 300)
            self.create_communications_zones(session, 150)
            self.create_major_assets(session, 50)

            # Create relationships
            self.log_message("\n--- CREATING RELATIONSHIPS ---\n")
            self.create_has_property_relationships(session)
            self.create_controls_relationships(session)
            self.create_contains_relationships(session)
            self.create_routes_through_relationships(session)
            self.create_connects_to_network_relationships(session)
            self.create_managed_by_nms_relationships(session)
            self.create_uses_device_relationships(session)

            # Verify
            total_nodes, total_rels = self.verify_deployment(session)

        self.log_message("\n" + "="*60)
        self.log_message("DEPLOYMENT COMPLETE")
        self.log_message(f"Total Nodes: {total_nodes}")
        self.log_message(f"Total Relationships: {total_rels}")
        self.log_message("="*60)

def main():
    deployer = CommunicationsDeployer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        deployer.deploy_all()
        deployer.save_log('/home/jim/2_OXOT_Projects_Dev/temp/sector-COMMUNICATIONS-completion-log.txt')
        print("\n✅ Log saved to: temp/sector-COMMUNICATIONS-completion-log.txt")
    finally:
        deployer.close()

if __name__ == "__main__":
    main()
