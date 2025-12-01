#!/usr/bin/env python3
"""
AEON Digital Twin Cyber Security Threat Intelligence
Schema Gap Analyzer
Version: 1.0.0
Created: 2025-10-29

Analyzes gaps between current Neo4j schema and required schema.
Generates remediation scripts.
"""

import json
from typing import Dict, List, Set
from pathlib import Path
from neo4j import GraphDatabase
import sys


class GapAnalyzer:
    """Analyzes schema gaps and generates remediation."""

    def __init__(self, uri: str = "bolt://localhost:7687",
                 user: str = "neo4j", password: str = "password"):
        """Initialize connection to Neo4j."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.schema_path = Path(__file__).parent.parent / "json" / "schema_complete.json"
        self.expected_schema = self._load_expected_schema()

    def _load_expected_schema(self) -> Dict:
        """Load expected schema from JSON."""
        with open(self.schema_path, 'r') as f:
            return json.load(f)

    def analyze_gaps(self) -> Dict[str, any]:
        """Identify all schema gaps."""
        return {
            "missing_constraints": self._find_missing_constraints(),
            "missing_indexes": self._find_missing_indexes(),
            "missing_node_types": self._find_missing_node_types(),
            "missing_relationships": self._find_missing_relationships(),
            "data_quality_issues": self._find_data_quality_issues()
        }

    def _find_missing_constraints(self) -> List[Dict]:
        """Find missing unique constraints."""
        with self.driver.session() as session:
            result = session.run("SHOW CONSTRAINTS")
            actual_constraints = {
                (record["labelsOrTypes"][0], record["properties"][0])
                for record in result
                if record["type"] == "UNIQUENESS"
            }

        expected_node_types = [nt["label"] for nt in self.expected_schema["nodeTypes"]]
        expected_constraints = {(label, "id") for label in expected_node_types}

        missing = expected_constraints - actual_constraints

        return [
            {
                "label": label,
                "property": prop,
                "cypher": f"CREATE CONSTRAINT {label.lower()}_id IF NOT EXISTS FOR (n:{label}) REQUIRE n.{prop} IS UNIQUE;"
            }
            for label, prop in missing
        ]

    def _find_missing_indexes(self) -> List[Dict]:
        """Find missing indexes."""
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            actual_indexes = {
                (record["labelsOrTypes"][0] if record["labelsOrTypes"] else None,
                 record["properties"][0] if record["properties"] else None)
                for record in result
            }

        expected_indexes = set()
        for node_type in self.expected_schema["nodeTypes"]:
            label = node_type["label"]
            for prop_name, prop_def in node_type["properties"].items():
                if prop_def.get("indexed"):
                    expected_indexes.add((label, prop_name))

        missing = expected_indexes - actual_indexes

        return [
            {
                "label": label,
                "property": prop,
                "cypher": f"CREATE INDEX {label.lower()}_{prop.lower()} IF NOT EXISTS FOR (n:{label}) ON (n.{prop});"
            }
            for label, prop in missing
        ]

    def _find_missing_node_types(self) -> List[Dict]:
        """Find missing node types."""
        with self.driver.session() as session:
            result = session.run("CALL db.labels()")
            actual_labels = {record[0] for record in result}

        expected_labels = {nt["label"] for nt in self.expected_schema["nodeTypes"]}
        missing = expected_labels - actual_labels

        return [
            {
                "label": label,
                "note": f"Node type '{label}' is defined in schema but has no instances in database"
            }
            for label in missing
        ]

    def _find_missing_relationships(self) -> List[Dict]:
        """Find missing relationship types."""
        with self.driver.session() as session:
            result = session.run("CALL db.relationshipTypes()")
            actual_rels = {record[0] for record in result}

        expected_rels = {rt["type"] for rt in self.expected_schema["relationshipTypes"]}
        missing = expected_rels - actual_rels

        return [
            {
                "type": rel_type,
                "note": f"Relationship type '{rel_type}' is defined in schema but has no instances in database",
                "definition": next(
                    (rt for rt in self.expected_schema["relationshipTypes"] if rt["type"] == rel_type),
                    None
                )
            }
            for rel_type in missing
        ]

    def _find_data_quality_issues(self) -> List[Dict]:
        """Find data quality issues."""
        issues = []

        with self.driver.session() as session:
            # Check for nodes without required ID property
            result = session.run("""
                MATCH (n)
                WHERE n.id IS NULL
                RETURN labels(n)[0] as label, count(*) as count
            """)
            for record in result:
                issues.append({
                    "type": "missing_required_property",
                    "label": record["label"],
                    "property": "id",
                    "count": record["count"],
                    "severity": "critical"
                })

            # Check for invalid CVE format
            result = session.run("""
                MATCH (c:CVE)
                WHERE NOT c.id =~ 'CVE-\\d{4}-\\d{4,}'
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            if count > 0:
                issues.append({
                    "type": "invalid_format",
                    "label": "CVE",
                    "property": "id",
                    "count": count,
                    "severity": "high",
                    "expected_format": "CVE-YYYY-NNNNN"
                })

            # Check for invalid MITRE ATT&CK IDs
            result = session.run("""
                MATCH (at:AttackTechnique)
                WHERE NOT at.mitreId =~ 'T\\d{4}(\\.\\d{3})?'
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            if count > 0:
                issues.append({
                    "type": "invalid_format",
                    "label": "AttackTechnique",
                    "property": "mitreId",
                    "count": count,
                    "severity": "high",
                    "expected_format": "TNNNN or TNNNN.NNN"
                })

            # Check for orphaned nodes (no relationships)
            result = session.run("""
                MATCH (n)
                WHERE NOT (n)--()
                RETURN labels(n)[0] as label, count(*) as count
            """)
            for record in result:
                if record["count"] > 0:
                    issues.append({
                        "type": "orphaned_node",
                        "label": record["label"],
                        "count": record["count"],
                        "severity": "medium"
                    })

            # Check for missing critical relationships
            result = session.run("""
                MATCH (comp:Component)
                WHERE NOT (comp)-[:HAS_VULNERABILITY]->(:CVE)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            if count > 0:
                issues.append({
                    "type": "missing_critical_relationship",
                    "from": "Component",
                    "relationship": "HAS_VULNERABILITY",
                    "to": "CVE",
                    "count": count,
                    "severity": "low",
                    "note": "Components without vulnerability data may indicate incomplete security assessment"
                })

        return issues

    def generate_remediation_script(self, gaps: Dict) -> str:
        """Generate Cypher script to remediate gaps."""
        script = []
        script.append("// ============================================================================")
        script.append("// SCHEMA REMEDIATION SCRIPT")
        script.append("// Generated: 2025-10-29")
        script.append("// ============================================================================")
        script.append("")

        # Missing constraints
        if gaps["missing_constraints"]:
            script.append("// Missing Unique Constraints")
            script.append("// ----------------------------------------------------------------------------")
            for constraint in gaps["missing_constraints"]:
                script.append(constraint["cypher"])
            script.append("")

        # Missing indexes
        if gaps["missing_indexes"]:
            script.append("// Missing Indexes")
            script.append("// ----------------------------------------------------------------------------")
            for index in gaps["missing_indexes"]:
                script.append(index["cypher"])
            script.append("")

        # Missing node types
        if gaps["missing_node_types"]:
            script.append("// Missing Node Types")
            script.append("// ----------------------------------------------------------------------------")
            script.append("// The following node types are defined but have no instances:")
            for node in gaps["missing_node_types"]:
                script.append(f"// - {node['label']}: {node['note']}")
            script.append("// Consider loading sample data from 04_sample_data.cypher")
            script.append("")

        # Missing relationships
        if gaps["missing_relationships"]:
            script.append("// Missing Relationship Types")
            script.append("// ----------------------------------------------------------------------------")
            script.append("// The following relationship types are defined but have no instances:")
            for rel in gaps["missing_relationships"]:
                script.append(f"// - {rel['type']}: {rel['note']}")
            script.append("// Consider loading sample data from 04_sample_data.cypher")
            script.append("")

        # Data quality issues
        if gaps["data_quality_issues"]:
            script.append("// Data Quality Issues")
            script.append("// ----------------------------------------------------------------------------")
            for issue in gaps["data_quality_issues"]:
                script.append(f"// {issue['type']}: {issue.get('label', 'N/A')} - Severity: {issue['severity']}")
                if issue['type'] == 'missing_required_property':
                    script.append(f"// Found {issue['count']} {issue['label']} nodes without '{issue['property']}' property")
                    script.append(f"// Manual intervention required to assign unique IDs")
                elif issue['type'] == 'invalid_format':
                    script.append(f"// Found {issue['count']} {issue['label']} nodes with invalid '{issue['property']}' format")
                    script.append(f"// Expected format: {issue['expected_format']}")
                elif issue['type'] == 'orphaned_node':
                    script.append(f"// Found {issue['count']} orphaned {issue['label']} nodes")
                    script.append(f"// Consider creating relationships or removing orphans")
            script.append("")

        script.append("// ============================================================================")
        script.append("// END OF REMEDIATION SCRIPT")
        script.append("// ============================================================================")

        return "\n".join(script)

    def generate_report(self, gaps: Dict) -> str:
        """Generate human-readable gap analysis report."""
        report = []
        report.append("=" * 80)
        report.append("AEON DIGITAL TWIN CYBERSECURITY - GAP ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary
        total_gaps = (
            len(gaps["missing_constraints"]) +
            len(gaps["missing_indexes"]) +
            len(gaps["missing_node_types"]) +
            len(gaps["missing_relationships"]) +
            len(gaps["data_quality_issues"])
        )

        report.append(f"TOTAL GAPS IDENTIFIED: {total_gaps}")
        report.append("")

        # Missing Constraints
        if gaps["missing_constraints"]:
            report.append(f"MISSING CONSTRAINTS: {len(gaps['missing_constraints'])}")
            for constraint in gaps["missing_constraints"]:
                report.append(f"  - {constraint['label']}.{constraint['property']}")
            report.append("")
        else:
            report.append("MISSING CONSTRAINTS: None ✓")
            report.append("")

        # Missing Indexes
        if gaps["missing_indexes"]:
            report.append(f"MISSING INDEXES: {len(gaps['missing_indexes'])}")
            for index in gaps["missing_indexes"]:
                report.append(f"  - {index['label']}.{index['property']}")
            report.append("")
        else:
            report.append("MISSING INDEXES: None ✓")
            report.append("")

        # Missing Node Types
        if gaps["missing_node_types"]:
            report.append(f"MISSING NODE TYPES: {len(gaps['missing_node_types'])}")
            for node in gaps["missing_node_types"]:
                report.append(f"  - {node['label']}")
            report.append("")
        else:
            report.append("MISSING NODE TYPES: None ✓")
            report.append("")

        # Missing Relationships
        if gaps["missing_relationships"]:
            report.append(f"MISSING RELATIONSHIP TYPES: {len(gaps['missing_relationships'])}")
            for rel in gaps["missing_relationships"]:
                report.append(f"  - {rel['type']}")
            report.append("")
        else:
            report.append("MISSING RELATIONSHIP TYPES: None ✓")
            report.append("")

        # Data Quality Issues
        if gaps["data_quality_issues"]:
            report.append(f"DATA QUALITY ISSUES: {len(gaps['data_quality_issues'])}")
            critical = [i for i in gaps["data_quality_issues"] if i["severity"] == "critical"]
            high = [i for i in gaps["data_quality_issues"] if i["severity"] == "high"]
            medium = [i for i in gaps["data_quality_issues"] if i["severity"] == "medium"]
            low = [i for i in gaps["data_quality_issues"] if i["severity"] == "low"]

            if critical:
                report.append(f"  Critical: {len(critical)}")
                for issue in critical:
                    report.append(f"    - {issue['type']}: {issue.get('label', 'N/A')} ({issue.get('count', 0)} instances)")
            if high:
                report.append(f"  High: {len(high)}")
                for issue in high:
                    report.append(f"    - {issue['type']}: {issue.get('label', 'N/A')} ({issue.get('count', 0)} instances)")
            if medium:
                report.append(f"  Medium: {len(medium)}")
            if low:
                report.append(f"  Low: {len(low)}")
            report.append("")
        else:
            report.append("DATA QUALITY ISSUES: None ✓")
            report.append("")

        report.append("=" * 80)
        report.append("REMEDIATION ACTIONS:")
        report.append("")

        if gaps["missing_constraints"] or gaps["missing_indexes"]:
            report.append("1. Run generated remediation script to create missing constraints/indexes")
        if gaps["missing_node_types"] or gaps["missing_relationships"]:
            report.append("2. Load sample data from 04_sample_data.cypher")
        if gaps["data_quality_issues"]:
            report.append("3. Address data quality issues (manual review may be required)")

        report.append("=" * 80)

        return "\n".join(report)

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()


def main():
    """Main gap analysis entry point."""
    # Parse command line arguments
    uri = sys.argv[1] if len(sys.argv) > 1 else "bolt://localhost:7687"
    user = sys.argv[2] if len(sys.argv) > 2 else "neo4j"
    password = sys.argv[3] if len(sys.argv) > 3 else "password"

    print(f"Connecting to Neo4j at {uri}...")

    try:
        analyzer = GapAnalyzer(uri, user, password)

        print("Analyzing schema gaps...")
        gaps = analyzer.analyze_gaps()

        # Generate and print report
        report = analyzer.generate_report(gaps)
        print(report)

        # Generate remediation script
        remediation = analyzer.generate_remediation_script(gaps)
        remediation_path = Path(__file__).parent / "remediation.cypher"
        with open(remediation_path, 'w') as f:
            f.write(remediation)
        print(f"\nRemediation script saved to: {remediation_path}")

        # Save results to JSON
        output_path = Path(__file__).parent / "gap_analysis_results.json"
        with open(output_path, 'w') as f:
            json.dump(gaps, f, indent=2)
        print(f"Detailed results saved to: {output_path}")

        analyzer.close()

        # Exit with appropriate code
        total_gaps = sum(len(v) for v in gaps.values() if isinstance(v, list))
        sys.exit(0 if total_gaps == 0 else 1)

    except Exception as e:
        print(f"ERROR: Gap analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
