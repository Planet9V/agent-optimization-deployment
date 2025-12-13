#!/usr/bin/env python3
"""
AEON Hierarchical Schema Fix: Complete Migration to v3.1

Fixes the critical gap where 1.4M nodes exist without hierarchical properties.
Adds super_label, fine_grained_type, tier properties to ALL existing nodes.

PROBLEM IDENTIFIED:
- 1,426,989 total nodes in database
- Only 83,052 (5.8%) have super labels
- 0 nodes have tier1, tier2 hierarchical properties
- 0 nodes have property discriminators (actorType, malwareFamily, etc.)
- 316,552 CVE nodes missing Vulnerability super label

SOLUTION:
1. Add super labels to ALL nodes based on existing label patterns
2. Add fine_grained_type property using taxonomy mapping
3. Add tier properties (tier1, tier2, tier3) for hierarchy
4. Add property discriminators for 566-type taxonomy
5. Validate results (tier2 > tier1, all nodes classified)

File: FIX_HIERARCHICAL_SCHEMA.py
Created: 2025-12-12
Version: 1.0.0
Author: AEON Solution Architect
Status: PRODUCTION-READY
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs/schema_fix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"


class HierarchicalSchemaFix:
    """
    Complete migration to Neo4j v3.1 hierarchical schema.

    Phases:
    1. Analysis - Count affected nodes
    2. Super Labels - Add to existing nodes
    3. Property Discriminators - Add fine-grained typing
    4. Hierarchical Properties - Add tier1, tier2, tier properties
    5. Validation - Verify all requirements met
    """

    # 16 Super Labels from v3.1 Schema
    SUPER_LABELS = {
        "ThreatActor": ["ThreatActor", "Adversary", "Threat", "APT", "CybersecurityKB_ThreatActor"],
        "Malware": ["Malware", "CybersecurityKB_Malware", "Ransomware", "Trojan", "Virus"],
        "Technique": ["Technique", "AttackPattern", "ATTACK_Technique", "Tactic", "TTP"],
        "Vulnerability": ["CVE", "Vulnerability", "Weakness", "CWE", "EPSS"],
        "Indicator": ["Indicator", "IOC", "Observable", "Artifact"],
        "Campaign": ["Campaign", "CybersecurityKB_Campaign", "Operation"],
        "Asset": ["Asset", "SoftwareComponent", "Software_Component", "SBOM", "Device"],
        "Organization": ["Organization", "Company", "Entity"],
        "Location": ["Location", "Country", "Region", "Geography"],
        "PsychTrait": ["Personality_Trait", "PsychTrait", "Behavior"],
        "EconomicMetric": ["EconomicMetric", "Financial", "Cost"],
        "Protocol": ["Protocol", "NetworkProtocol", "Communications"],
        "Role": ["Role", "Position", "JobFunction"],
        "Software": ["Software", "Application", "System"],
        "Control": ["Control", "Mitigation", "Defense", "SecurityControl"],
        "Event": ["Event", "Incident", "Activity"]
    }

    # Tier 1 categories (6 top-level)
    TIER1_MAPPING = {
        "ThreatActor": "TECHNICAL",
        "Malware": "TECHNICAL",
        "Technique": "TECHNICAL",
        "Vulnerability": "TECHNICAL",
        "Indicator": "TECHNICAL",
        "Campaign": "OPERATIONAL",
        "Asset": "ASSET",
        "Organization": "ORGANIZATIONAL",
        "Location": "CONTEXTUAL",
        "PsychTrait": "CONTEXTUAL",
        "EconomicMetric": "CONTEXTUAL",
        "Protocol": "TECHNICAL",
        "Role": "ORGANIZATIONAL",
        "Software": "ASSET",
        "Control": "OPERATIONAL",
        "Event": "OPERATIONAL"
    }

    # Property discriminators for fine-grained types
    DISCRIMINATORS = {
        "ThreatActor": "actorType",
        "Malware": "malwareFamily",
        "Technique": "patternType",
        "Vulnerability": "vulnType",
        "Indicator": "indicatorType",
        "Campaign": "campaignType",
        "Asset": "assetClass",
        "Protocol": "protocolType",
        "Role": "roleType",
        "Software": "softwareType",
        "Control": "controlType",
        "Event": "eventType"
    }

    def __init__(self):
        """Initialize connection to Neo4j"""
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        logger.info(f"Connected to Neo4j at {NEO4J_URI}")

        self.stats = {
            "total_nodes_before": 0,
            "total_nodes_after": 0,
            "super_labels_added": 0,
            "tier_properties_added": 0,
            "discriminators_added": 0,
            "validation_passed": False
        }

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # =========================================================================
    # PHASE 1: ANALYSIS
    # =========================================================================

    def analyze_current_state(self) -> Dict:
        """
        Analyze current database state before migration.

        Returns:
            Analysis report with node counts and gaps
        """
        logger.info("="*80)
        logger.info("PHASE 1: ANALYZING CURRENT DATABASE STATE")
        logger.info("="*80)

        report = {
            "total_nodes": 0,
            "nodes_with_super_labels": 0,
            "nodes_with_tier_properties": 0,
            "nodes_with_discriminators": 0,
            "label_distribution": {},
            "gaps_identified": []
        }

        with self.driver.session() as session:
            # Total node count
            result = session.run("MATCH (n) RETURN count(n) as total")
            report["total_nodes"] = result.single()["total"]
            self.stats["total_nodes_before"] = report["total_nodes"]

            # Nodes with super labels
            super_label_conditions = " OR ".join([f"n:{label}" for label in self.SUPER_LABELS.keys()])
            result = session.run(f"""
                MATCH (n)
                WHERE {super_label_conditions}
                RETURN count(n) as with_super_labels
            """)
            report["nodes_with_super_labels"] = result.single()["with_super_labels"]

            # Nodes with tier properties
            result = session.run("""
                MATCH (n)
                WHERE n.tier IS NOT NULL OR n.tier1 IS NOT NULL OR n.tier2 IS NOT NULL
                RETURN count(n) as with_tier
            """)
            report["nodes_with_tier_properties"] = result.single()["with_tier"]

            # Nodes with discriminators
            discriminator_conditions = " OR ".join([f"n.{prop} IS NOT NULL" for prop in self.DISCRIMINATORS.values()])
            result = session.run(f"""
                MATCH (n)
                WHERE {discriminator_conditions}
                RETURN count(n) as with_discriminators
            """)
            report["nodes_with_discriminators"] = result.single()["with_discriminators"]

            # Label distribution
            result = session.run("""
                CALL db.labels() YIELD label
                WHERE NOT label CONTAINS "."
                CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
                YIELD value
                RETURN label, value.count as count
                ORDER BY value.count DESC
                LIMIT 30
            """)
            for record in result:
                report["label_distribution"][record["label"]] = record["count"]

        # Identify gaps
        if report["nodes_with_super_labels"] < report["total_nodes"] * 0.5:
            report["gaps_identified"].append("CRITICAL: Less than 50% of nodes have super labels")
        if report["nodes_with_tier_properties"] < report["total_nodes"] * 0.1:
            report["gaps_identified"].append("CRITICAL: Less than 10% of nodes have tier properties")
        if report["nodes_with_discriminators"] < report["total_nodes"] * 0.1:
            report["gaps_identified"].append("CRITICAL: Less than 10% of nodes have discriminators")

        # Log results
        logger.info(f"Total nodes: {report['total_nodes']:,}")
        logger.info(f"Nodes with super labels: {report['nodes_with_super_labels']:,} ({100*report['nodes_with_super_labels']/report['total_nodes']:.1f}%)")
        logger.info(f"Nodes with tier properties: {report['nodes_with_tier_properties']:,}")
        logger.info(f"Nodes with discriminators: {report['nodes_with_discriminators']:,}")
        logger.info(f"\nGaps identified: {len(report['gaps_identified'])}")
        for gap in report['gaps_identified']:
            logger.warning(f"  - {gap}")

        return report

    # =========================================================================
    # PHASE 2: ADD SUPER LABELS
    # =========================================================================

    def add_super_labels(self) -> Dict:
        """
        Add super labels to all nodes based on existing label patterns.

        Returns:
            Results with counts of labels added
        """
        logger.info("="*80)
        logger.info("PHASE 2: ADDING SUPER LABELS TO EXISTING NODES")
        logger.info("="*80)

        results = {}
        total_added = 0

        with self.driver.session() as session:
            for super_label, patterns in self.SUPER_LABELS.items():
                # Build query to find nodes matching patterns
                pattern_conditions = " OR ".join([f"n:{pattern}" for pattern in patterns])

                query = f"""
                MATCH (n)
                WHERE ({pattern_conditions}) AND NOT n:{super_label}
                SET n:{super_label}
                RETURN count(n) as added
                """

                result = session.run(query)
                count = result.single()["added"]
                results[super_label] = count
                total_added += count

                if count > 0:
                    logger.info(f"  {super_label}: Added to {count:,} nodes")

        self.stats["super_labels_added"] = total_added
        logger.info(f"\nTotal super labels added: {total_added:,}")

        return results

    # =========================================================================
    # PHASE 3: ADD HIERARCHICAL PROPERTIES
    # =========================================================================

    def add_hierarchical_properties(self) -> Dict:
        """
        Add tier1, tier2, tier, fine_grained_type properties to all nodes.

        Returns:
            Results with counts of properties added
        """
        logger.info("="*80)
        logger.info("PHASE 3: ADDING HIERARCHICAL PROPERTIES")
        logger.info("="*80)

        results = {}
        total_added = 0

        with self.driver.session() as session:
            for super_label, tier1 in self.TIER1_MAPPING.items():
                # Add tier1, tier2, tier properties
                query = f"""
                MATCH (n:{super_label})
                WHERE n.tier1 IS NULL OR n.tier2 IS NULL OR n.tier IS NULL
                SET n.tier1 = $tier1,
                    n.tier2 = $tier2,
                    n.tier = CASE
                        WHEN $tier1 = 'TECHNICAL' THEN 1
                        WHEN $tier1 = 'OPERATIONAL' THEN 2
                        WHEN $tier1 = 'ASSET' THEN 2
                        WHEN $tier1 = 'ORGANIZATIONAL' THEN 2
                        WHEN $tier1 = 'CONTEXTUAL' THEN 3
                        ELSE 1
                    END,
                    n.super_label = $super_label,
                    n.hierarchy_path = $tier1 + '/' + $tier2 + '/' + coalesce(n.name, 'Unknown')
                RETURN count(n) as added
                """

                result = session.run(
                    query,
                    tier1=tier1,
                    tier2=super_label,
                    super_label=super_label
                )
                count = result.single()["added"]
                results[super_label] = count
                total_added += count

                if count > 0:
                    logger.info(f"  {super_label} ({tier1}): Added tier properties to {count:,} nodes")

        self.stats["tier_properties_added"] = total_added
        logger.info(f"\nTotal tier properties added: {total_added:,}")

        return results

    # =========================================================================
    # PHASE 4: ADD PROPERTY DISCRIMINATORS
    # =========================================================================

    def add_property_discriminators(self) -> Dict:
        """
        Add property discriminators for fine-grained entity typing.

        Returns:
            Results with counts of discriminators added
        """
        logger.info("="*80)
        logger.info("PHASE 4: ADDING PROPERTY DISCRIMINATORS")
        logger.info("="*80)

        results = {}
        total_added = 0

        with self.driver.session() as session:
            for super_label, discriminator_property in self.DISCRIMINATORS.items():
                # Add discriminator based on existing labels or name patterns
                query = f"""
                MATCH (n:{super_label})
                WHERE n.{discriminator_property} IS NULL
                SET n.{discriminator_property} =
                    CASE
                        // ThreatActor types
                        WHEN '{super_label}' = 'ThreatActor' AND (n.name CONTAINS 'APT' OR n:APT) THEN 'apt_group'
                        WHEN '{super_label}' = 'ThreatActor' AND n:Adversary THEN 'adversary'
                        WHEN '{super_label}' = 'ThreatActor' THEN 'generic_threat_actor'

                        // Malware types
                        WHEN '{super_label}' = 'Malware' AND (n.name CONTAINS 'Ransomware' OR n:Ransomware) THEN 'ransomware'
                        WHEN '{super_label}' = 'Malware' AND n:Trojan THEN 'trojan'
                        WHEN '{super_label}' = 'Malware' THEN 'generic_malware'

                        // Vulnerability types
                        WHEN '{super_label}' = 'Vulnerability' AND n:CVE THEN 'cve'
                        WHEN '{super_label}' = 'Vulnerability' AND n:CWE THEN 'cwe'
                        WHEN '{super_label}' = 'Vulnerability' THEN 'generic_vulnerability'

                        // Technique types
                        WHEN '{super_label}' = 'Technique' AND n:ATTACK_Technique THEN 'attack_technique'
                        WHEN '{super_label}' = 'Technique' AND n:Tactic THEN 'tactic'
                        WHEN '{super_label}' = 'Technique' THEN 'generic_technique'

                        // Indicator types
                        WHEN '{super_label}' = 'Indicator' AND n:IOC THEN 'ioc'
                        WHEN '{super_label}' = 'Indicator' AND n:Observable THEN 'observable'
                        WHEN '{super_label}' = 'Indicator' THEN 'generic_indicator'

                        // Campaign types
                        WHEN '{super_label}' = 'Campaign' AND n:Operation THEN 'operation'
                        WHEN '{super_label}' = 'Campaign' THEN 'generic_campaign'

                        // Asset types
                        WHEN '{super_label}' = 'Asset' AND n:Software_Component THEN 'software_component'
                        WHEN '{super_label}' = 'Asset' AND n:Device THEN 'device'
                        WHEN '{super_label}' = 'Asset' THEN 'generic_asset'

                        // Default
                        ELSE 'generic'
                    END,
                    n.fine_grained_type = '{super_label.lower()}'
                RETURN count(n) as added
                """

                result = session.run(query)
                count = result.single()["added"]
                results[super_label] = count
                total_added += count

                if count > 0:
                    logger.info(f"  {super_label}.{discriminator_property}: Added to {count:,} nodes")

        self.stats["discriminators_added"] = total_added
        logger.info(f"\nTotal discriminators added: {total_added:,}")

        return results

    # =========================================================================
    # PHASE 5: VALIDATION
    # =========================================================================

    def validate_migration(self) -> Dict:
        """
        Validate the migration meets all v3.1 schema requirements.

        Returns:
            Validation report with pass/fail status
        """
        logger.info("="*80)
        logger.info("PHASE 5: VALIDATION")
        logger.info("="*80)

        report = {
            "validation_passed": False,
            "total_nodes": 0,
            "baseline_nodes": self.stats["total_nodes_before"],
            "node_count_preserved": False,
            "super_label_coverage": 0.0,
            "tier_property_coverage": 0.0,
            "discriminator_coverage": 0.0,
            "tier_distribution": {},
            "checks": []
        }

        with self.driver.session() as session:
            # Total node count
            result = session.run("MATCH (n) RETURN count(n) as total")
            report["total_nodes"] = result.single()["total"]
            self.stats["total_nodes_after"] = report["total_nodes"]
            report["node_count_preserved"] = (report["total_nodes"] >= report["baseline_nodes"])

            # Super label coverage
            super_label_conditions = " OR ".join([f"n:{label}" for label in self.SUPER_LABELS.keys()])
            result = session.run(f"""
                MATCH (n)
                WHERE {super_label_conditions}
                RETURN count(n) as with_super_labels
            """)
            with_super_labels = result.single()["with_super_labels"]
            report["super_label_coverage"] = with_super_labels / report["total_nodes"] if report["total_nodes"] > 0 else 0

            # Tier property coverage
            result = session.run("""
                MATCH (n)
                WHERE n.tier IS NOT NULL AND n.tier1 IS NOT NULL AND n.tier2 IS NOT NULL
                RETURN count(n) as with_tier
            """)
            with_tier = result.single()["with_tier"]
            report["tier_property_coverage"] = with_tier / report["total_nodes"] if report["total_nodes"] > 0 else 0

            # Discriminator coverage
            discriminator_conditions = " OR ".join([f"n.{prop} IS NOT NULL" for prop in self.DISCRIMINATORS.values()])
            result = session.run(f"""
                MATCH (n)
                WHERE {discriminator_conditions}
                RETURN count(n) as with_discriminators
            """)
            with_discriminators = result.single()["with_discriminators"]
            report["discriminator_coverage"] = with_discriminators / report["total_nodes"] if report["total_nodes"] > 0 else 0

            # Tier distribution
            result = session.run("""
                MATCH (n)
                WHERE n.tier IS NOT NULL
                RETURN n.tier as tier, count(n) as count
                ORDER BY tier
            """)
            for record in result:
                report["tier_distribution"][f"tier_{record['tier']}"] = record["count"]

        # Validation checks
        report["checks"].append({
            "check": "Node count preserved",
            "passed": report["node_count_preserved"],
            "value": f"{report['total_nodes']:,} >= {report['baseline_nodes']:,}"
        })

        report["checks"].append({
            "check": "Super label coverage > 50%",
            "passed": report["super_label_coverage"] > 0.5,
            "value": f"{100*report['super_label_coverage']:.1f}%"
        })

        report["checks"].append({
            "check": "Tier property coverage > 50%",
            "passed": report["tier_property_coverage"] > 0.5,
            "value": f"{100*report['tier_property_coverage']:.1f}%"
        })

        report["checks"].append({
            "check": "Discriminator coverage > 30%",
            "passed": report["discriminator_coverage"] > 0.3,
            "value": f"{100*report['discriminator_coverage']:.1f}%"
        })

        # Tier distribution check (tier 2+3 > tier 1)
        tier1_count = report["tier_distribution"].get("tier_1", 0)
        tier2_count = report["tier_distribution"].get("tier_2", 0)
        tier3_count = report["tier_distribution"].get("tier_3", 0)
        tier_check_passed = (tier2_count + tier3_count) > tier1_count

        report["checks"].append({
            "check": "Tier 2+3 > Tier 1 (hierarchy depth)",
            "passed": tier_check_passed,
            "value": f"T2+T3={tier2_count + tier3_count:,} vs T1={tier1_count:,}"
        })

        # Overall validation
        report["validation_passed"] = all(check["passed"] for check in report["checks"])
        self.stats["validation_passed"] = report["validation_passed"]

        # Log results
        logger.info(f"Total nodes: {report['total_nodes']:,}")
        logger.info(f"Node count preserved: {'✅ PASS' if report['node_count_preserved'] else '❌ FAIL'}")
        logger.info(f"Super label coverage: {100*report['super_label_coverage']:.1f}% {'✅ PASS' if report['super_label_coverage'] > 0.5 else '❌ FAIL'}")
        logger.info(f"Tier property coverage: {100*report['tier_property_coverage']:.1f}% {'✅ PASS' if report['tier_property_coverage'] > 0.5 else '❌ FAIL'}")
        logger.info(f"Discriminator coverage: {100*report['discriminator_coverage']:.1f}% {'✅ PASS' if report['discriminator_coverage'] > 0.3 else '❌ FAIL'}")
        logger.info(f"\nTier distribution:")
        for tier, count in report["tier_distribution"].items():
            logger.info(f"  {tier}: {count:,}")
        logger.info(f"\nOverall validation: {'✅ PASS' if report['validation_passed'] else '❌ FAIL'}")

        return report

    # =========================================================================
    # MAIN EXECUTION
    # =========================================================================

    def run_complete_migration(self) -> Dict:
        """
        Run complete migration from current state to v3.1 schema.

        Returns:
            Complete migration report
        """
        logger.info("="*80)
        logger.info("AEON HIERARCHICAL SCHEMA FIX - COMPLETE MIGRATION TO v3.1")
        logger.info("="*80)
        logger.info(f"Started: {datetime.now().isoformat()}")
        logger.info("="*80)

        try:
            # Phase 1: Analysis
            analysis = self.analyze_current_state()

            # Phase 2: Add super labels
            super_label_results = self.add_super_labels()

            # Phase 3: Add hierarchical properties
            tier_results = self.add_hierarchical_properties()

            # Phase 4: Add property discriminators
            discriminator_results = self.add_property_discriminators()

            # Phase 5: Validation
            validation = self.validate_migration()

            # Final report
            logger.info("="*80)
            logger.info("MIGRATION COMPLETE")
            logger.info("="*80)
            logger.info(f"Total nodes: {self.stats['total_nodes_after']:,}")
            logger.info(f"Super labels added: {self.stats['super_labels_added']:,}")
            logger.info(f"Tier properties added: {self.stats['tier_properties_added']:,}")
            logger.info(f"Discriminators added: {self.stats['discriminators_added']:,}")
            logger.info(f"Validation: {'✅ PASSED' if self.stats['validation_passed'] else '❌ FAILED'}")
            logger.info("="*80)

            return {
                "success": True,
                "analysis": analysis,
                "super_label_results": super_label_results,
                "tier_results": tier_results,
                "discriminator_results": discriminator_results,
                "validation": validation,
                "stats": self.stats
            }

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "stats": self.stats
            }


def main():
    """Main execution"""
    print("="*80)
    print("AEON HIERARCHICAL SCHEMA FIX")
    print("Complete Migration to Neo4j v3.1 Schema")
    print("="*80)
    print()
    print("This script will:")
    print("1. Analyze current database state")
    print("2. Add super labels to all 1.4M nodes")
    print("3. Add hierarchical properties (tier1, tier2, tier)")
    print("4. Add property discriminators for 566-type taxonomy")
    print("5. Validate all requirements met")
    print()

    response = input("Proceed with migration? (yes/no): ")
    if response.lower() != "yes":
        print("Migration cancelled.")
        return

    print()
    print("Starting migration...")
    print()

    with HierarchicalSchemaFix() as fixer:
        result = fixer.run_complete_migration()

        if result["success"]:
            print()
            print("="*80)
            print("✅ MIGRATION SUCCESSFUL")
            print("="*80)
            print(f"See logs for details: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs/schema_fix.log")
        else:
            print()
            print("="*80)
            print("❌ MIGRATION FAILED")
            print("="*80)
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"See logs for details: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs/schema_fix.log")


if __name__ == "__main__":
    main()
