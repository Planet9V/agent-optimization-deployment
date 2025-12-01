#!/usr/bin/env python3
"""
Network Topology Loader - Complete implementation for loading network topology and security zones
Handles firewall rules, network segments (IEC 62443 zones), security zone assignment, IP/VLAN mapping.
"""

import os
import sys
import json
import csv
import re
import logging
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from ipaddress import ip_address, ip_network, IPv4Address, IPv4Network
from pathlib import Path
from neo4j import GraphDatabase, Driver
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_loader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class NetworkSegment:
    """Network segment data structure"""
    id: str
    name: str
    zone: str  # IEC 62443 zone
    network: str  # CIDR notation
    vlan_id: Optional[int] = None
    description: str = ''
    properties: Dict[str, any] = field(default_factory=dict)


@dataclass
class FirewallRule:
    """Firewall rule data structure"""
    id: str
    source: str
    destination: str
    protocol: str
    port: Optional[str] = None
    action: str = 'allow'
    description: str = ''


@dataclass
class ImportMetrics:
    """Track import statistics"""
    segments: int = 0
    devices: int = 0
    firewall_rules: int = 0
    connections: int = 0
    errors: int = 0


class NetworkTopologyLoader:
    """Load network topology and security zones into Neo4j"""

    # IEC 62443 security zones for railways
    SECURITY_ZONES = {
        'CONTROL': {
            'level': 4,
            'description': 'Critical control systems (signaling, traction)',
            'isolation': 'HIGH'
        },
        'PROCESS': {
            'level': 3,
            'description': 'Process control and monitoring',
            'isolation': 'MEDIUM'
        },
        'DMZ': {
            'level': 2,
            'description': 'Demilitarized zone for external interfaces',
            'isolation': 'MEDIUM'
        },
        'CORPORATE': {
            'level': 1,
            'description': 'Corporate network',
            'isolation': 'LOW'
        },
        'EXTERNAL': {
            'level': 0,
            'description': 'External networks (Internet)',
            'isolation': 'VERY_HIGH'
        }
    }

    # Common protocols and ports
    PROTOCOLS = {
        'tcp': 6,
        'udp': 17,
        'icmp': 1,
        'gre': 47,
        'esp': 50,
        'ah': 51
    }

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize network topology loader

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.metrics = ImportMetrics()
        self._verify_connection()
        self._create_indexes()

    def _verify_connection(self):
        """Verify Neo4j connection"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            logger.info("Neo4j connection verified")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _create_indexes(self):
        """Create necessary indexes and constraints"""
        indexes = [
            "CREATE CONSTRAINT segment_id IF NOT EXISTS FOR (s:NetworkSegment) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT device_ip IF NOT EXISTS FOR (d:NetworkDevice) REQUIRE d.ip_address IS UNIQUE",
            "CREATE INDEX segment_zone IF NOT EXISTS FOR (s:NetworkSegment) ON (s.zone)",
            "CREATE INDEX segment_vlan IF NOT EXISTS FOR (s:NetworkSegment) ON (s.vlan_id)",
            "CREATE INDEX device_zone IF NOT EXISTS FOR (d:NetworkDevice) ON (d.zone)",
        ]

        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"Created index/constraint: {index_query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")

    def load_segments_from_csv(self, csv_path: str) -> List[NetworkSegment]:
        """
        Load network segments from CSV

        Expected format: id,name,zone,network,vlan_id,description

        Args:
            csv_path: Path to CSV file

        Returns:
            List of NetworkSegment objects
        """
        segments = []

        logger.info(f"Loading network segments from CSV: {csv_path}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    vlan_id = None
                    if row.get('vlan_id'):
                        try:
                            vlan_id = int(row['vlan_id'])
                        except ValueError:
                            logger.warning(f"Invalid VLAN ID: {row['vlan_id']}")

                    segment = NetworkSegment(
                        id=row['id'],
                        name=row['name'],
                        zone=row['zone'],
                        network=row['network'],
                        vlan_id=vlan_id,
                        description=row.get('description', '')
                    )
                    segments.append(segment)

            logger.info(f"Loaded {len(segments)} network segments from CSV")
            return segments

        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise

    def parse_iptables_rules(self, rules_file: str) -> List[FirewallRule]:
        """
        Parse iptables firewall rules

        Example format:
        -A INPUT -s 10.1.0.0/24 -d 10.2.0.0/24 -p tcp --dport 22 -j ACCEPT

        Args:
            rules_file: Path to iptables rules file

        Returns:
            List of FirewallRule objects
        """
        rules = []
        rule_id = 0

        logger.info(f"Parsing iptables rules from {rules_file}")

        try:
            with open(rules_file, 'r') as f:
                for line in f:
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse iptables rule
                    if line.startswith('-A'):
                        rule_id += 1

                        # Extract components
                        source = self._extract_iptables_field(line, '-s')
                        dest = self._extract_iptables_field(line, '-d')
                        protocol = self._extract_iptables_field(line, '-p')
                        port = self._extract_iptables_field(line, '--dport')
                        action = 'allow' if '-j ACCEPT' in line else 'deny'

                        if source and dest:
                            rule = FirewallRule(
                                id=f"iptables-{rule_id}",
                                source=source,
                                destination=dest,
                                protocol=protocol or 'any',
                                port=port,
                                action=action,
                                description=f"IPTables rule {rule_id}"
                            )
                            rules.append(rule)

            logger.info(f"Parsed {len(rules)} iptables rules")
            return rules

        except Exception as e:
            logger.error(f"Failed to parse iptables rules: {e}")
            raise

    def _extract_iptables_field(self, line: str, field: str) -> Optional[str]:
        """Extract field value from iptables rule"""
        pattern = f"{field}\\s+([^\\s]+)"
        match = re.search(pattern, line)
        return match.group(1) if match else None

    def parse_cisco_acl(self, acl_file: str) -> List[FirewallRule]:
        """
        Parse Cisco ACL rules

        Example format:
        access-list 101 permit tcp 10.1.0.0 0.0.0.255 10.2.0.0 0.0.0.255 eq 22

        Args:
            acl_file: Path to Cisco ACL file

        Returns:
            List of FirewallRule objects
        """
        rules = []
        rule_id = 0

        logger.info(f"Parsing Cisco ACL from {acl_file}")

        try:
            with open(acl_file, 'r') as f:
                for line in f:
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith('!'):
                        continue

                    # Parse ACL rule
                    if line.startswith('access-list'):
                        rule_id += 1
                        parts = line.split()

                        if len(parts) < 7:
                            continue

                        action = parts[2]  # permit/deny
                        protocol = parts[3]
                        source_ip = parts[4]
                        source_mask = parts[5]
                        dest_ip = parts[6]
                        dest_mask = parts[7] if len(parts) > 7 else '0.0.0.0'

                        # Convert wildcard mask to CIDR
                        source = self._wildcard_to_cidr(source_ip, source_mask)
                        dest = self._wildcard_to_cidr(dest_ip, dest_mask)

                        # Extract port if present
                        port = None
                        if 'eq' in parts:
                            port_idx = parts.index('eq') + 1
                            if port_idx < len(parts):
                                port = parts[port_idx]

                        rule = FirewallRule(
                            id=f"cisco-acl-{rule_id}",
                            source=source,
                            destination=dest,
                            protocol=protocol,
                            port=port,
                            action=action,
                            description=f"Cisco ACL rule {rule_id}"
                        )
                        rules.append(rule)

            logger.info(f"Parsed {len(rules)} Cisco ACL rules")
            return rules

        except Exception as e:
            logger.error(f"Failed to parse Cisco ACL: {e}")
            raise

    def _wildcard_to_cidr(self, ip: str, wildcard: str) -> str:
        """Convert Cisco wildcard mask to CIDR notation"""
        try:
            # Handle 'any' keyword
            if ip == 'any':
                return '0.0.0.0/0'

            # Convert wildcard to netmask
            wildcard_parts = [int(x) for x in wildcard.split('.')]
            netmask_parts = [255 - x for x in wildcard_parts]

            # Calculate prefix length
            prefix_len = sum(bin(x).count('1') for x in netmask_parts)

            return f"{ip}/{prefix_len}"
        except Exception:
            return f"{ip}/32"

    def validate_network(self, network_str: str) -> bool:
        """Validate network CIDR notation"""
        try:
            ip_network(network_str)
            return True
        except ValueError:
            return False

    def assign_device_to_segment(self, ip: str, segments: List[NetworkSegment]) -> Optional[NetworkSegment]:
        """
        Assign device IP to network segment

        Args:
            ip: Device IP address
            segments: List of network segments

        Returns:
            Matching NetworkSegment or None
        """
        try:
            device_ip = ip_address(ip)

            for segment in segments:
                try:
                    segment_network = ip_network(segment.network)
                    if device_ip in segment_network:
                        return segment
                except ValueError:
                    continue

            return None
        except ValueError:
            logger.warning(f"Invalid IP address: {ip}")
            return None

    def import_segments(self, segments: List[NetworkSegment]):
        """
        Import network segments into Neo4j

        Args:
            segments: List of network segments
        """
        if not segments:
            logger.warning("No segments to import")
            return

        # Validate segments
        valid_segments = []
        for segment in segments:
            if not self.validate_network(segment.network):
                logger.error(f"Invalid network CIDR: {segment.network}")
                self.metrics.errors += 1
                continue

            if segment.zone not in self.SECURITY_ZONES:
                logger.error(f"Invalid security zone: {segment.zone}")
                self.metrics.errors += 1
                continue

            valid_segments.append(segment)

        # Prepare data
        segment_data = []
        for segment in valid_segments:
            zone_info = self.SECURITY_ZONES[segment.zone]

            segment_data.append({
                'id': segment.id,
                'name': segment.name,
                'zone': segment.zone,
                'zone_level': zone_info['level'],
                'zone_isolation': zone_info['isolation'],
                'network': segment.network,
                'vlan_id': segment.vlan_id,
                'description': segment.description
            })

        # Import
        cypher = """
        UNWIND $segments as seg
        MERGE (s:NetworkSegment {id: seg.id})
        SET s.name = seg.name,
            s.zone = seg.zone,
            s.zone_level = seg.zone_level,
            s.zone_isolation = seg.zone_isolation,
            s.network = seg.network,
            s.vlan_id = seg.vlan_id,
            s.description = seg.description,
            s.lastImported = datetime()
        """

        with self.driver.session() as session:
            session.run(cypher, segments=segment_data)
            self.metrics.segments = len(segment_data)

        logger.info(f"Imported {len(segment_data)} network segments")

    def import_firewall_rules(self, rules: List[FirewallRule]):
        """
        Import firewall rules into Neo4j

        Args:
            rules: List of firewall rules
        """
        if not rules:
            logger.warning("No firewall rules to import")
            return

        rule_data = []
        for rule in rules:
            rule_data.append({
                'id': rule.id,
                'source': rule.source,
                'destination': rule.destination,
                'protocol': rule.protocol,
                'port': rule.port,
                'action': rule.action,
                'description': rule.description
            })

        cypher = """
        UNWIND $rules as rule
        MERGE (r:FirewallRule {id: rule.id})
        SET r.source = rule.source,
            r.destination = rule.destination,
            r.protocol = rule.protocol,
            r.port = rule.port,
            r.action = rule.action,
            r.description = rule.description,
            r.lastImported = datetime()

        WITH r, rule
        MATCH (src:NetworkSegment)
        WHERE rule.source STARTS WITH src.network OR rule.source = 'any'
        MERGE (src)-[:HAS_RULE]->(r)

        WITH r, rule
        MATCH (dst:NetworkSegment)
        WHERE rule.destination STARTS WITH dst.network OR rule.destination = 'any'
        MERGE (r)-[:ALLOWS_ACCESS_TO]->(dst)
        """

        with self.driver.session() as session:
            with tqdm(total=len(rule_data), desc="Importing firewall rules") as pbar:
                batch_size = 500
                for i in range(0, len(rule_data), batch_size):
                    batch = rule_data[i:i + batch_size]
                    session.run(cypher, rules=batch)
                    pbar.update(len(batch))

            self.metrics.firewall_rules = len(rule_data)

        logger.info(f"Imported {len(rule_data)} firewall rules")

    def link_devices_to_segments(self):
        """Link existing devices to network segments based on IP address"""
        cypher = """
        MATCH (d:NetworkDevice)
        WHERE d.ip_address IS NOT NULL
        MATCH (s:NetworkSegment)
        WHERE apoc.network.inSubnet(d.ip_address, s.network)
        MERGE (d)-[:IN_SEGMENT]->(s)
        SET d.zone = s.zone,
            d.vlan_id = s.vlan_id
        RETURN count(d) as linked
        """

        with self.driver.session() as session:
            result = session.run(cypher)
            linked = result.single()['linked']
            logger.info(f"Linked {linked} devices to network segments")

    def get_metrics(self) -> ImportMetrics:
        """Return import metrics"""
        return self.metrics

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("Network topology loader closed")


def main():
    """Main execution function"""
    # Configuration from environment or defaults
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # Initialize loader
    loader = NetworkTopologyLoader(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD
    )

    try:
        # Example: Load segments from CSV
        segments_csv = 'network_segments.csv'
        if Path(segments_csv).exists():
            segments = loader.load_segments_from_csv(segments_csv)
            loader.import_segments(segments)

        # Example: Parse and load firewall rules
        iptables_file = 'iptables.rules'
        if Path(iptables_file).exists():
            rules = loader.parse_iptables_rules(iptables_file)
            loader.import_firewall_rules(rules)

        # Link devices to segments
        loader.link_devices_to_segments()

        # Print metrics
        metrics = loader.get_metrics()
        logger.info(f"""
        Import Metrics:
        - Network Segments: {metrics.segments}
        - Firewall Rules: {metrics.firewall_rules}
        - Errors: {metrics.errors}
        """)

    except Exception as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    finally:
        loader.close()


if __name__ == "__main__":
    main()
