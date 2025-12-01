#!/usr/bin/env python3
"""
Attack Path Simulator - Find and analyze attack paths in the network graph
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AttackPath:
    """Represents a potential attack path"""
    nodes: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    hops: int
    cvss_score: float
    risk_score: float
    vulnerabilities: List[str]
    firewall_rules_validated: bool
    protocol_compliant: bool


class AttackPathSimulator:
    """Simulate and analyze attack paths through the network"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_attack_paths(
        self,
        source_zone: str,
        target_criticality: str = "critical",
        max_hops: int = 20,
        algorithm: str = "bfs"
    ) -> List[AttackPath]:
        """
        Find attack paths from source zone to target assets

        Args:
            source_zone: Starting network zone (e.g., "dmz", "external")
            target_criticality: Target asset criticality
            max_hops: Maximum path length
            algorithm: "bfs" or "dfs"
        """
        query = f'''
        MATCH path = (start:NetworkInterface {{zone: $source_zone}})
                     -[:CONNECTS_TO*1..{max_hops}]->(target:Component {{criticality: $target_criticality}})
        WHERE ALL(r IN relationships(path) WHERE r.allowed = true)
        WITH path, relationships(path) as rels, nodes(path) as nodes
        // Calculate path risk score based on vulnerabilities
        OPTIONAL MATCH (vuln:Vulnerability)-[:AFFECTS]->(n)
        WHERE n IN nodes
        WITH path, rels, nodes,
             COLLECT(DISTINCT vuln) as vulns,
             AVG(vuln.cvss_score) as avg_cvss
        RETURN
            nodes,
            rels,
            length(path) as hops,
            COALESCE(avg_cvss, 0.0) as cvss_score,
            vulns,
            SIZE(vulns) as vuln_count
        ORDER BY hops ASC, cvss_score DESC
        LIMIT 50
        '''

        with self.driver.session() as session:
            result = session.run(query, source_zone=source_zone)
            paths = []

            for record in result:
                nodes = [self._node_to_dict(n) for n in record["nodes"]]
                rels = [self._rel_to_dict(r) for r in record["rels"]]

                # Calculate composite risk score
                cvss = record["cvss_score"]
                vuln_count = record["vuln_count"]
                hop_penalty = record["hops"] * 0.1  # Longer paths slightly less risky
                risk_score = (cvss * 0.7) + (vuln_count * 0.2) - hop_penalty

                path = AttackPath(
                    nodes=nodes,
                    relationships=rels,
                    hops=record["hops"],
                    cvss_score=cvss,
                    risk_score=risk_score,
                    vulnerabilities=[v["id"] for v in record["vulns"]],
                    firewall_rules_validated=self._validate_firewall_rules(rels),
                    protocol_compliant=self._check_protocol_compliance(rels)
                )
                paths.append(path)

            logger.info(f"Found {len(paths)} attack paths from {source_zone} to {target_criticality} assets")
            return paths

    def find_critical_paths(
        self,
        min_cvss: float = 7.0,
        max_hops: int = 10
    ) -> List[AttackPath]:
        """Find paths with high CVSS vulnerabilities"""
        query = f'''
        MATCH (vuln:Vulnerability)
        WHERE vuln.cvss_score >= $min_cvss
        MATCH (vuln)-[:AFFECTS]->(component:Component)
        MATCH path = (external:NetworkInterface {{zone: "external"}})
                     -[:CONNECTS_TO*1..{max_hops}]->(component)
        WHERE ALL(r IN relationships(path) WHERE r.allowed = true)
        RETURN DISTINCT path, vuln, relationships(path) as rels, nodes(path) as nodes
        ORDER BY vuln.cvss_score DESC
        LIMIT 25
        '''

        with self.driver.session() as session:
            result = session.run(query, min_cvss=min_cvss)
            paths = []

            for record in result:
                nodes = [self._node_to_dict(n) for n in record["nodes"]]
                rels = [self._rel_to_dict(r) for r in record["rels"]]
                vuln = record["vuln"]

                path = AttackPath(
                    nodes=nodes,
                    relationships=rels,
                    hops=len(rels),
                    cvss_score=vuln["cvss_score"],
                    risk_score=vuln["cvss_score"],
                    vulnerabilities=[vuln["id"]],
                    firewall_rules_validated=self._validate_firewall_rules(rels),
                    protocol_compliant=self._check_protocol_compliance(rels)
                )
                paths.append(path)

            return paths

    def enumerate_multi_hop_paths(
        self,
        start_component: str,
        end_component: str,
        min_hops: int = 1,
        max_hops: int = 20
    ) -> List[AttackPath]:
        """Enumerate all paths between two components"""
        query = f'''
        MATCH path = (start:Component {{name: $start}})
                     -[:CONNECTS_TO|DEPENDS_ON*{min_hops}..{max_hops}]->
                     (end:Component {{name: $end}})
        WITH path, relationships(path) as rels, nodes(path) as nodes
        OPTIONAL MATCH (vuln:Vulnerability)-[:AFFECTS]->(n)
        WHERE n IN nodes
        WITH path, rels, nodes, COLLECT(DISTINCT vuln) as vulns
        RETURN nodes, rels, length(path) as hops, vulns
        LIMIT 100
        '''

        with self.driver.session() as session:
            result = session.run(query, start=start_component, end=end_component)
            paths = []

            for record in result:
                nodes = [self._node_to_dict(n) for n in record["nodes"]]
                rels = [self._rel_to_dict(r) for r in record["rels"]]
                vulns = [v["id"] for v in record["vulns"]]
                avg_cvss = sum(v.get("cvss_score", 0) for v in record["vulns"]) / max(len(record["vulns"]), 1)

                path = AttackPath(
                    nodes=nodes,
                    relationships=rels,
                    hops=record["hops"],
                    cvss_score=avg_cvss,
                    risk_score=avg_cvss * 0.8,
                    vulnerabilities=vulns,
                    firewall_rules_validated=self._validate_firewall_rules(rels),
                    protocol_compliant=self._check_protocol_compliance(rels)
                )
                paths.append(path)

            return paths

    def _validate_firewall_rules(self, relationships: List[Dict]) -> bool:
        """Validate firewall rules allow path traversal"""
        for rel in relationships:
            if rel.get("type") == "CONNECTS_TO":
                if not rel.get("allowed", True):
                    return False
                if rel.get("firewall_rule") and rel.get("action") == "deny":
                    return False
        return True

    def _check_protocol_compliance(self, relationships: List[Dict]) -> bool:
        """Check if protocols used are allowed"""
        allowed_protocols = {"TCP", "UDP", "HTTP", "HTTPS", "SSH", "RDP", "ICMP"}
        for rel in relationships:
            protocol = rel.get("protocol", "TCP")
            if protocol not in allowed_protocols:
                return False
        return True

    def export_for_visualization(self, paths: List[AttackPath], output_file: str):
        """Export paths in D3.js compatible JSON format"""
        visualization_data = {
            "nodes": [],
            "links": [],
            "paths": []
        }

        node_ids = set()

        for i, path in enumerate(paths):
            path_data = {
                "id": i,
                "risk_score": path.risk_score,
                "cvss_score": path.cvss_score,
                "hops": path.hops,
                "vulnerabilities": path.vulnerabilities,
                "validated": path.firewall_rules_validated and path.protocol_compliant
            }
            visualization_data["paths"].append(path_data)

            # Add unique nodes
            for node in path.nodes:
                node_id = node.get("id", node.get("name"))
                if node_id not in node_ids:
                    node_ids.add(node_id)
                    visualization_data["nodes"].append({
                        "id": node_id,
                        "label": node.get("name", node_id),
                        "type": node.get("type", "Component"),
                        "criticality": node.get("criticality", "medium"),
                        "zone": node.get("zone", "internal")
                    })

            # Add links
            for j, rel in enumerate(path.relationships):
                if j < len(path.nodes) - 1:
                    visualization_data["links"].append({
                        "source": path.nodes[j].get("id", path.nodes[j].get("name")),
                        "target": path.nodes[j+1].get("id", path.nodes[j+1].get("name")),
                        "type": rel.get("type", "CONNECTS_TO"),
                        "protocol": rel.get("protocol", "TCP"),
                        "allowed": rel.get("allowed", True),
                        "path_id": i
                    })

        with open(output_file, 'w') as f:
            json.dump(visualization_data, f, indent=2)

        logger.info(f"Exported visualization data to {output_file}")

    def _node_to_dict(self, node) -> Dict[str, Any]:
        """Convert Neo4j node to dictionary"""
        return dict(node.items())

    def _rel_to_dict(self, rel) -> Dict[str, Any]:
        """Convert Neo4j relationship to dictionary"""
        return dict(rel.items())

    def generate_attack_report(self, paths: List[AttackPath]) -> Dict[str, Any]:
        """Generate comprehensive attack path analysis report"""
        if not paths:
            return {"error": "No attack paths found"}

        report = {
            "summary": {
                "total_paths": len(paths),
                "avg_hops": sum(p.hops for p in paths) / len(paths),
                "avg_cvss": sum(p.cvss_score for p in paths) / len(paths),
                "avg_risk": sum(p.risk_score for p in paths) / len(paths),
                "validated_paths": sum(1 for p in paths if p.firewall_rules_validated),
                "compliant_paths": sum(1 for p in paths if p.protocol_compliant)
            },
            "top_risks": [
                {
                    "hops": p.hops,
                    "risk_score": p.risk_score,
                    "cvss_score": p.cvss_score,
                    "vulnerabilities": p.vulnerabilities[:5],  # Top 5
                    "start": p.nodes[0].get("name", "unknown"),
                    "end": p.nodes[-1].get("name", "unknown")
                }
                for p in sorted(paths, key=lambda x: x.risk_score, reverse=True)[:10]
            ],
            "shortest_paths": [
                {
                    "hops": p.hops,
                    "risk_score": p.risk_score,
                    "path": [n.get("name", "unknown") for n in p.nodes]
                }
                for p in sorted(paths, key=lambda x: x.hops)[:5]
            ]
        }

        return report


def main():
    """Example usage"""
    simulator = AttackPathSimulator(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Find attack paths from DMZ to critical assets
        paths = simulator.find_attack_paths(
            source_zone="dmz",
            target_criticality="critical",
            max_hops=15
        )

        # Generate report
        report = simulator.generate_attack_report(paths)
        print(json.dumps(report, indent=2))

        # Export for visualization
        simulator.export_for_visualization(paths, "/tmp/attack_paths.json")

        # Find critical vulnerability paths
        critical_paths = simulator.find_critical_paths(min_cvss=8.0)
        print(f"\nFound {len(critical_paths)} critical vulnerability paths")

    finally:
        simulator.close()


if __name__ == "__main__":
    main()
