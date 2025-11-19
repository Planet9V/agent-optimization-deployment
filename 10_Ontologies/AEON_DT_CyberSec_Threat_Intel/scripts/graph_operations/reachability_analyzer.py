#!/usr/bin/env python3
"""
Reachability Analyzer - Network path and connectivity analysis
"""

import json
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import heapq
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NetworkPath:
    """Represents a network path between two nodes"""
    source: str
    destination: str
    hops: List[str]
    protocols: List[str]
    zones_crossed: List[str]
    firewall_rules: List[Dict]
    is_allowed: bool
    cost: float
    latency_ms: float


class ReachabilityAnalyzer:
    """Analyze network reachability and path validation"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def check_reachability(
        self,
        source: str,
        destination: str,
        protocol: Optional[str] = None,
        port: Optional[int] = None
    ) -> Tuple[bool, Optional[NetworkPath]]:
        """
        Check if destination is reachable from source

        Args:
            source: Source node name/IP
            destination: Destination node name/IP
            protocol: Optional protocol filter (TCP/UDP/ICMP)
            port: Optional port filter

        Returns:
            (is_reachable, path_details)
        """
        protocol_clause = "AND r.protocol = $protocol" if protocol else ""
        port_clause = "AND r.port = $port" if port else ""

        query = f'''
        MATCH path = (src {{name: $source}})-[r:CONNECTS_TO*1..10]->(dst {{name: $destination}})
        WHERE ALL(rel IN r WHERE rel.allowed = true {protocol_clause} {port_clause})
        WITH path, relationships(path) as rels, nodes(path) as nodes
        RETURN
            nodes,
            rels,
            length(path) as hops,
            [rel IN rels | rel.protocol] as protocols,
            [n IN nodes | n.zone] as zones
        ORDER BY hops ASC
        LIMIT 1
        '''

        params = {"source": source, "destination": destination}
        if protocol:
            params["protocol"] = protocol
        if port:
            params["port"] = port

        with self.driver.session() as session:
            result = session.run(query, **params)
            record = result.single()

            if not record:
                return False, None

            nodes = [dict(n.items()) for n in record["nodes"]]
            rels = [dict(r.items()) for r in record["rels"]]

            # Extract firewall rules
            firewall_rules = []
            for rel in rels:
                if "firewall_rule" in rel:
                    firewall_rules.append({
                        "rule_id": rel.get("firewall_rule"),
                        "action": rel.get("action", "allow"),
                        "protocol": rel.get("protocol", "TCP"),
                        "port": rel.get("port")
                    })

            # Calculate path cost and latency
            cost = sum(rel.get("cost", 1.0) for rel in rels)
            latency = sum(rel.get("latency_ms", 1.0) for rel in rels)

            path = NetworkPath(
                source=source,
                destination=destination,
                hops=[n.get("name", "") for n in nodes],
                protocols=record["protocols"],
                zones_crossed=list(filter(None, record["zones"])),
                firewall_rules=firewall_rules,
                is_allowed=True,
                cost=cost,
                latency_ms=latency
            )

            return True, path

    def find_shortest_path(
        self,
        source: str,
        destination: str
    ) -> Optional[NetworkPath]:
        """
        Find shortest path using Dijkstra's algorithm
        Uses cost metric for optimization
        """
        query = '''
        MATCH (src {name: $source})
        MATCH (dst {name: $destination})
        CALL gds.shortestPath.dijkstra.stream({
            sourceNode: src,
            targetNode: dst,
            relationshipWeightProperty: 'cost',
            relationshipTypes: ['CONNECTS_TO']
        })
        YIELD nodeIds, costs, totalCost
        RETURN nodeIds, costs, totalCost
        '''

        # Fallback to basic path finding if GDS not available
        fallback_query = '''
        MATCH path = shortestPath((src {name: $source})-[:CONNECTS_TO*]-(dst {name: $destination}))
        WHERE ALL(r IN relationships(path) WHERE r.allowed = true)
        RETURN path, relationships(path) as rels, nodes(path) as nodes
        '''

        with self.driver.session() as session:
            try:
                result = session.run(query, source=source, destination=destination)
                record = result.single()

                if record:
                    # Process GDS result
                    node_ids = record["nodeIds"]
                    total_cost = record["totalCost"]
                    # Get node details
                    nodes_query = '''
                    MATCH (n) WHERE id(n) IN $node_ids
                    RETURN COLLECT(n) as nodes
                    '''
                    nodes_result = session.run(nodes_query, node_ids=node_ids)
                    nodes = [dict(n.items()) for n in nodes_result.single()["nodes"]]

                    return NetworkPath(
                        source=source,
                        destination=destination,
                        hops=[n.get("name", "") for n in nodes],
                        protocols=[],
                        zones_crossed=[n.get("zone") for n in nodes if n.get("zone")],
                        firewall_rules=[],
                        is_allowed=True,
                        cost=total_cost,
                        latency_ms=0.0
                    )
            except:
                # Use fallback
                result = session.run(fallback_query, source=source, destination=destination)
                record = result.single()

                if record:
                    nodes = [dict(n.items()) for n in record["nodes"]]
                    rels = [dict(r.items()) for r in record["rels"]]

                    return NetworkPath(
                        source=source,
                        destination=destination,
                        hops=[n.get("name", "") for n in nodes],
                        protocols=[r.get("protocol", "TCP") for r in rels],
                        zones_crossed=[n.get("zone") for n in nodes if n.get("zone")],
                        firewall_rules=[],
                        is_allowed=True,
                        cost=len(rels),
                        latency_ms=0.0
                    )

        return None

    def analyze_zone_crossings(
        self,
        path: NetworkPath
    ) -> Dict[str, List[str]]:
        """Analyze security zone crossings in a path"""
        crossings = []
        zones = path.zones_crossed

        for i in range(len(zones) - 1):
            if zones[i] != zones[i+1]:
                crossings.append({
                    "from": zones[i],
                    "to": zones[i+1],
                    "hop": i
                })

        # Identify risky crossings
        risky = []
        for crossing in crossings:
            if self._is_risky_crossing(crossing["from"], crossing["to"]):
                risky.append(crossing)

        return {
            "total_crossings": len(crossings),
            "crossings": crossings,
            "risky_crossings": risky
        }

    def _is_risky_crossing(self, from_zone: str, to_zone: str) -> bool:
        """Determine if zone crossing is risky"""
        # Define zone trust levels
        trust_levels = {
            "external": 0,
            "dmz": 1,
            "internal": 2,
            "restricted": 3,
            "critical": 4
        }

        from_trust = trust_levels.get(from_zone, 1)
        to_trust = trust_levels.get(to_zone, 1)

        # Risky if going from lower trust to higher trust
        return from_trust < to_trust

    def validate_firewall_rules(
        self,
        path: NetworkPath
    ) -> Dict[str, any]:
        """Validate firewall rules along path"""
        validation = {
            "is_valid": True,
            "blocked_at": None,
            "violations": []
        }

        for i, rule in enumerate(path.firewall_rules):
            if rule["action"] == "deny":
                validation["is_valid"] = False
                validation["blocked_at"] = i
                validation["violations"].append({
                    "hop": i,
                    "rule_id": rule["rule_id"],
                    "reason": f"Blocked by rule {rule['rule_id']}"
                })

            # Check protocol allowlist
            if rule["protocol"] not in ["TCP", "UDP", "ICMP", "HTTP", "HTTPS"]:
                validation["violations"].append({
                    "hop": i,
                    "rule_id": rule["rule_id"],
                    "reason": f"Unsupported protocol: {rule['protocol']}"
                })

        return validation

    def find_all_paths(
        self,
        source: str,
        destination: str,
        max_paths: int = 10,
        max_hops: int = 10
    ) -> List[NetworkPath]:
        """Find multiple paths between nodes"""
        query = f'''
        MATCH path = (src {{name: $source}})-[:CONNECTS_TO*1..{max_hops}]->(dst {{name: $destination}})
        WHERE ALL(r IN relationships(path) WHERE r.allowed = true)
        WITH path, relationships(path) as rels, nodes(path) as nodes
        RETURN DISTINCT
            nodes,
            rels,
            length(path) as hops
        ORDER BY hops ASC
        LIMIT $max_paths
        '''

        with self.driver.session() as session:
            result = session.run(query, source=source, destination=destination, max_paths=max_paths)

            paths = []
            for record in result:
                nodes = [dict(n.items()) for n in record["nodes"]]
                rels = [dict(r.items()) for r in record["rels"]]

                path = NetworkPath(
                    source=source,
                    destination=destination,
                    hops=[n.get("name", "") for n in nodes],
                    protocols=[r.get("protocol", "TCP") for r in rels],
                    zones_crossed=[n.get("zone") for n in nodes if n.get("zone")],
                    firewall_rules=[],
                    is_allowed=True,
                    cost=sum(r.get("cost", 1.0) for r in rels),
                    latency_ms=sum(r.get("latency_ms", 1.0) for r in rels)
                )
                paths.append(path)

            logger.info(f"Found {len(paths)} paths from {source} to {destination}")
            return paths

    def export_visualization(
        self,
        paths: List[NetworkPath],
        output_file: str
    ):
        """Export paths for network visualization"""
        viz_data = {
            "nodes": [],
            "links": [],
            "paths": []
        }

        node_set = set()

        for i, path in enumerate(paths):
            # Add path metadata
            viz_data["paths"].append({
                "id": i,
                "source": path.source,
                "destination": path.destination,
                "hops": len(path.hops),
                "cost": path.cost,
                "latency_ms": path.latency_ms,
                "is_allowed": path.is_allowed
            })

            # Add nodes
            for j, hop in enumerate(path.hops):
                if hop not in node_set:
                    node_set.add(hop)
                    zone = path.zones_crossed[j] if j < len(path.zones_crossed) else "unknown"
                    viz_data["nodes"].append({
                        "id": hop,
                        "label": hop,
                        "zone": zone
                    })

            # Add links
            for j in range(len(path.hops) - 1):
                protocol = path.protocols[j] if j < len(path.protocols) else "TCP"
                viz_data["links"].append({
                    "source": path.hops[j],
                    "target": path.hops[j+1],
                    "protocol": protocol,
                    "path_id": i
                })

        with open(output_file, 'w') as f:
            json.dump(viz_data, f, indent=2)

        logger.info(f"Exported visualization to {output_file}")


def main():
    """Example usage"""
    analyzer = ReachabilityAnalyzer(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Check reachability
        is_reachable, path = analyzer.check_reachability(
            source="web-server-1",
            destination="database-1",
            protocol="TCP",
            port=5432
        )

        if is_reachable:
            print(f"✓ Destination is reachable")
            print(f"  Hops: {len(path.hops)}")
            print(f"  Path: {' → '.join(path.hops)}")
            print(f"  Zones: {' → '.join(path.zones_crossed)}")

            # Analyze zone crossings
            crossings = analyzer.analyze_zone_crossings(path)
            print(f"\nZone Analysis:")
            print(f"  Total crossings: {crossings['total_crossings']}")
            print(f"  Risky crossings: {len(crossings['risky_crossings'])}")

            # Validate firewall rules
            validation = analyzer.validate_firewall_rules(path)
            print(f"\nFirewall Validation:")
            print(f"  Valid: {validation['is_valid']}")
            if validation['violations']:
                print(f"  Violations: {len(validation['violations'])}")
        else:
            print("✗ Destination is not reachable")

        # Find all paths
        all_paths = analyzer.find_all_paths("web-server-1", "database-1")
        print(f"\nFound {len(all_paths)} total paths")

        # Export visualization
        analyzer.export_visualization(all_paths, "/tmp/network_paths.json")

    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
