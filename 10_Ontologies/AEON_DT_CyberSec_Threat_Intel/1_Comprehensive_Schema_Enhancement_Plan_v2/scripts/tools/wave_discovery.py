#!/usr/bin/env python3
"""
Wave Discovery Tool - Query actual Neo4j structure for ANY wave
Generates accurate taxonomy mapping for master_taxonomy.yaml

This tool solves the "taxonomy mismatch" problem by discovering the actual
database structure before creating enhancement scripts.

Usage:
    python3 scripts/tools/wave_discovery.py --wave 10
    python3 scripts/tools/wave_discovery.py --wave 11 --output-yaml

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from neo4j import GraphDatabase
    import yaml
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Required packages: neo4j-driver, pyyaml")
    sys.exit(1)


class WaveDiscovery:
    """Discover actual wave structure from Neo4j database"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg"
    ):
        """Initialize Wave Discovery tool"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

    def discover_wave_structure(self, wave_num: int) -> Dict[str, Any]:
        """
        Discover actual structure of a wave from Neo4j

        Args:
            wave_num: Wave number (9, 10, 11, 12)

        Returns:
            Dict with complete wave structure analysis
        """
        created_by = f"AEON_INTEGRATION_WAVE{wave_num}"

        with self.driver.session() as session:
            # Total wave count
            total_result = session.run(f"""
                MATCH (n)
                WHERE n.created_by = '{created_by}'
                RETURN count(n) as total
            """)
            total_count = total_result.single()["total"]

            # Get all label combinations
            labels_result = session.run(f"""
                MATCH (n)
                WHERE n.created_by = '{created_by}'
                WITH labels(n) as label_set, count(*) as count
                RETURN label_set, count
                ORDER BY count DESC
            """)

            label_combinations = []
            for record in labels_result:
                label_combinations.append({
                    "labels": record["label_set"],
                    "count": record["count"]
                })

            # Detect domain label (most common label across all nodes)
            domain_candidates = {}
            for combo in label_combinations:
                for label in combo["labels"]:
                    domain_candidates[label] = domain_candidates.get(label, 0) + combo["count"]

            # Domain is the label that appears in ALL or most nodes
            domain_label = max(domain_candidates.items(), key=lambda x: x[1])[0]

            # Check which nodes already have domain label
            labeled_result = session.run(f"""
                MATCH (n:{domain_label})
                WHERE n.created_by = '{created_by}'
                RETURN count(n) as labeled_count
            """)
            labeled_count = labeled_result.single()["labeled_count"]

            # Get unlabeled nodes structure
            unlabeled_result = session.run(f"""
                MATCH (n)
                WHERE n.created_by = '{created_by}'
                AND NOT n:{domain_label}
                WITH labels(n) as label_set, count(*) as count
                RETURN label_set, count
                ORDER BY count DESC
            """)

            unlabeled_combinations = []
            for record in unlabeled_result:
                unlabeled_combinations.append({
                    "labels": record["label_set"],
                    "count": record["count"]
                })

        return {
            "wave_number": wave_num,
            "created_by": created_by,
            "total_nodes": total_count,
            "domain_label": domain_label,
            "labeled_count": labeled_count,
            "unlabeled_count": total_count - labeled_count,
            "all_label_combinations": label_combinations,
            "unlabeled_combinations": unlabeled_combinations,
            "discovery_timestamp": datetime.now().isoformat()
        }

    def generate_taxonomy_yaml(self, discovery: Dict[str, Any],
                               domain_config: Dict[str, Any]) -> str:
        """
        Generate YAML snippet for master_taxonomy.yaml

        Args:
            discovery: Discovery results from discover_wave_structure()
            domain_config: Manual domain configuration (subdomains, roles)

        Returns:
            YAML string ready for master_taxonomy.yaml
        """
        wave_num = discovery["wave_number"]
        domain = discovery["domain_label"]

        # Build node type mappings from unlabeled nodes
        node_type_mappings = {}

        for combo in discovery["unlabeled_combinations"]:
            labels = combo["labels"]
            count = combo["count"]

            # Primary node type is the last label (or first if only one)
            primary_type = labels[-1] if len(labels) > 0 else "Unknown"

            # Determine subdomain and role from domain_config
            # This requires manual mapping based on node type
            subdomain = self._infer_subdomain(primary_type, domain_config)
            role = self._infer_role(primary_type, domain_config)

            # Labels to add
            labels_to_add = [domain]
            if subdomain:
                labels_to_add.append(subdomain)
            if role:
                labels_to_add.append(role)

            # Final labels
            final_labels = labels_to_add + [primary_type]

            node_type_mappings[primary_type] = {
                "add_labels": labels_to_add,
                "final_labels": final_labels,
                "count": count
            }

        # Generate YAML
        yaml_data = {
            f"wave_{wave_num}": {
                "domain": domain,
                "operation": "ADD_LABELS",
                "target_nodes": discovery["total_nodes"],
                "complexity": self._determine_complexity(node_type_mappings),
                "node_type_mappings": node_type_mappings,
                "discovery_metadata": {
                    "discovered_on": discovery["discovery_timestamp"],
                    "already_labeled": discovery["labeled_count"],
                    "needs_labeling": discovery["unlabeled_count"]
                }
            }
        }

        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

    def _infer_subdomain(self, node_type: str, domain_config: Dict[str, Any]) -> str:
        """Infer subdomain from node type (requires manual mapping)"""
        # This is a helper - actual mapping should be provided by user
        subdomain_keywords = domain_config.get("subdomain_keywords", {})

        for subdomain, keywords in subdomain_keywords.items():
            if any(keyword.lower() in node_type.lower() for keyword in keywords):
                return subdomain

        return None

    def _infer_role(self, node_type: str, domain_config: Dict[str, Any]) -> str:
        """Infer functional role from node type"""
        role_keywords = domain_config.get("role_keywords", {})

        for role, keywords in role_keywords.items():
            if any(keyword.lower() in node_type.lower() for keyword in keywords):
                return role

        return "Asset"  # Default role

    def _determine_complexity(self, node_type_mappings: Dict[str, Any]) -> str:
        """Determine complexity based on label count"""
        avg_labels = sum(len(v["final_labels"]) for v in node_type_mappings.values()) / len(node_type_mappings)

        if avg_labels >= 4:
            return "complex"
        elif avg_labels >= 3:
            return "moderate"
        else:
            return "simple"

    def print_discovery_report(self, discovery: Dict[str, Any]):
        """Print human-readable discovery report"""
        print("=" * 80)
        print(f"WAVE {discovery['wave_number']} DISCOVERY REPORT")
        print("=" * 80)
        print()

        print(f"Total Nodes: {discovery['total_nodes']:,}")
        print(f"Domain Label: {discovery['domain_label']}")
        print(f"Already Labeled: {discovery['labeled_count']:,} ({discovery['labeled_count']/discovery['total_nodes']*100:.1f}%)")
        print(f"Need Labeling: {discovery['unlabeled_count']:,} ({discovery['unlabeled_count']/discovery['total_nodes']*100:.1f}%)")
        print()

        print("=" * 80)
        print("ALL LABEL COMBINATIONS")
        print("=" * 80)
        for i, combo in enumerate(discovery['all_label_combinations'], 1):
            labels_str = ", ".join(combo['labels'])
            print(f"{i:2}. [{labels_str:60}] - {combo['count']:,} nodes")
        print()

        if discovery['unlabeled_count'] > 0:
            print("=" * 80)
            print("NODES NEEDING LABELS (Enhancement Targets)")
            print("=" * 80)
            for i, combo in enumerate(discovery['unlabeled_combinations'], 1):
                labels_str = ", ".join(combo['labels'])
                print(f"{i:2}. [{labels_str:60}] - {combo['count']:,} nodes")
            print()

    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Discover actual wave structure from Neo4j database"
    )
    parser.add_argument(
        "--wave",
        type=int,
        required=True,
        choices=[9, 10, 11, 12],
        help="Wave number to discover"
    )
    parser.add_argument(
        "--output-yaml",
        action="store_true",
        help="Output YAML snippet for master_taxonomy.yaml"
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="Output full discovery as JSON"
    )

    args = parser.parse_args()

    # Run discovery
    discoverer = WaveDiscovery()
    discovery = discoverer.discover_wave_structure(args.wave)

    # Print report
    discoverer.print_discovery_report(discovery)

    # Output formats
    if args.output_json:
        print("=" * 80)
        print("JSON OUTPUT")
        print("=" * 80)
        print(json.dumps(discovery, indent=2))

    if args.output_yaml:
        print("=" * 80)
        print("YAML SNIPPET FOR master_taxonomy.yaml")
        print("=" * 80)
        print("# Copy the unlabeled combinations above and manually map to subdomains/roles")
        print("# Then use this structure:")
        print()
        print(f"wave_{args.wave}:")
        print(f"  domain: {discovery['domain_label']}")
        print(f"  operation: ADD_LABELS")
        print(f"  target_nodes: {discovery['total_nodes']}")
        print(f"  node_type_mappings:")
        for combo in discovery['unlabeled_combinations']:
            primary_type = combo['labels'][-1] if combo['labels'] else "Unknown"
            print(f"    {primary_type}:")
            print(f"      add_labels: [{discovery['domain_label']}, <SUBDOMAIN>, <ROLE>]")
            print(f"      final_labels: [{discovery['domain_label']}, <SUBDOMAIN>, <ROLE>, {primary_type}]")
            print(f"      count: {combo['count']}")

    discoverer.close()


if __name__ == "__main__":
    main()
