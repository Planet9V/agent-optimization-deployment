#!/usr/bin/env python3
"""
AEON Digital Twin Cyber Security Threat Intelligence
Neo4j Schema Validator
Version: 1.0.0
Created: 2025-10-29

Validates Neo4j graph schema completeness and consistency.
"""

import json
from typing import Dict, List, Set, Tuple
from pathlib import Path
from neo4j import GraphDatabase
import sys


class SchemaValidator:
    """Validates Neo4j schema against expected structure."""

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

    def validate_all(self) -> Dict[str, any]:
        """Run all validation checks."""
        results = {
            "constraints": self.validate_constraints(),
            "indexes": self.validate_indexes(),
            "node_types": self.validate_node_types(),
            "relationship_types": self.validate_relationship_types(),
            "data_integrity": self.validate_data_integrity(),
            "summary": {}
        }

        # Generate summary
        total_checks = sum(len(v.get("missing", [])) + len(v.get("extra", []))
                          for v in results.values() if isinstance(v, dict))
        results["summary"] = {
            "total_checks": total_checks,
            "passed": sum(1 for v in results.values()
                         if isinstance(v, dict) and not v.get("missing") and not v.get("extra")),
            "failed": sum(1 for v in results.values()
                         if isinstance(v, dict) and (v.get("missing") or v.get("extra")))
        }

        return results

    def validate_constraints(self) -> Dict[str, List[str]]:
        """Validate all unique constraints exist."""
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
        extra = actual_constraints - expected_constraints

        return {
            "expected": len(expected_constraints),
            "actual": len(actual_constraints),
            "missing": list(missing),
            "extra": list(extra),
            "valid": len(missing) == 0
        }

    def validate_indexes(self) -> Dict[str, List[str]]:
        """Validate all indexes exist."""
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            actual_indexes = {
                (record["labelsOrTypes"][0] if record["labelsOrTypes"] else None,
                 record["properties"][0] if record["properties"] else None)
                for record in result
            }

        # Extract expected indexes from schema
        expected_indexes = set()
        for node_type in self.expected_schema["nodeTypes"]:
            label = node_type["label"]
            for prop_name, prop_def in node_type["properties"].items():
                if prop_def.get("indexed"):
                    expected_indexes.add((label, prop_name))

        missing = expected_indexes - actual_indexes

        return {
            "expected": len(expected_indexes),
            "actual": len(actual_indexes),
            "missing": list(missing),
            "valid": len(missing) == 0
        }

    def validate_node_types(self) -> Dict[str, any]:
        """Validate all node types exist with correct properties."""
        with self.driver.session() as session:
            # Get all node labels
            result = session.run("CALL db.labels()")
            actual_labels = {record[0] for record in result}

        expected_labels = {nt["label"] for nt in self.expected_schema["nodeTypes"]}

        missing = expected_labels - actual_labels
        extra = actual_labels - expected_labels

        # Validate properties for existing labels
        property_issues = []
        for node_type in self.expected_schema["nodeTypes"]:
            label = node_type["label"]
            if label in actual_labels:
                issues = self._validate_node_properties(label, node_type["properties"])
                if issues:
                    property_issues.append({label: issues})

        return {
            "expected": len(expected_labels),
            "actual": len(actual_labels),
            "missing": list(missing),
            "extra": list(extra),
            "property_issues": property_issues,
            "valid": len(missing) == 0 and len(property_issues) == 0
        }

    def _validate_node_properties(self, label: str, expected_props: Dict) -> List[str]:
        """Validate properties for a specific node type."""
        with self.driver.session() as session:
            # Sample a node to check properties
            result = session.run(f"MATCH (n:{label}) RETURN n LIMIT 1")
            record = result.single()

            if not record:
                return [f"No {label} nodes found"]

            actual_props = set(record["n"].keys())
            expected_prop_names = set(expected_props.keys())

            missing = expected_prop_names - actual_props
            if missing:
                return [f"Missing properties: {missing}"]

        return []

    def validate_relationship_types(self) -> Dict[str, any]:
        """Validate all relationship types exist."""
        with self.driver.session() as session:
            result = session.run("CALL db.relationshipTypes()")
            actual_rels = {record[0] for record in result}

        expected_rels = {rt["type"] for rt in self.expected_schema["relationshipTypes"]}

        missing = expected_rels - actual_rels
        extra = actual_rels - expected_rels

        return {
            "expected": len(expected_rels),
            "actual": len(actual_rels),
            "missing": list(missing),
            "extra": list(extra),
            "valid": len(missing) == 0
        }

    def validate_data_integrity(self) -> Dict[str, any]:
        """Validate data integrity constraints."""
        issues = []

        with self.driver.session() as session:
            # Check for orphaned nodes
            result = session.run("""
                MATCH (n)
                WHERE NOT (n)--()
                RETURN labels(n)[0] as label, count(*) as count
            """)
            orphaned = {record["label"]: record["count"] for record in result}
            if orphaned:
                issues.append({"orphaned_nodes": orphaned})

            # Check for missing required properties
            result = session.run("""
                MATCH (n)
                WHERE n.id IS NULL
                RETURN labels(n)[0] as label, count(*) as count
            """)
            missing_ids = {record["label"]: record["count"] for record in result}
            if missing_ids:
                issues.append({"missing_required_id": missing_ids})

            # Check for invalid CVE IDs
            result = session.run("""
                MATCH (c:CVE)
                WHERE NOT c.id =~ 'CVE-\\d{4}-\\d{4,}'
                RETURN count(*) as count
            """)
            invalid_cves = result.single()["count"]
            if invalid_cves > 0:
                issues.append({"invalid_cve_format": invalid_cves})

            # Check for invalid MITRE ATT&CK IDs
            result = session.run("""
                MATCH (at:AttackTechnique)
                WHERE NOT at.mitreId =~ 'T\\d{4}(\\.\\d{3})?'
                RETURN count(*) as count
            """)
            invalid_mitre = result.single()["count"]
            if invalid_mitre > 0:
                issues.append({"invalid_mitre_format": invalid_mitre})

        return {
            "issues": issues,
            "valid": len(issues) == 0
        }

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append("=" * 80)
        report.append("AEON DIGITAL TWIN CYBERSECURITY - SCHEMA VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary
        summary = results["summary"]
        report.append(f"SUMMARY: {summary['passed']}/{summary['total_checks']} checks passed")
        report.append("")

        # Constraints
        constraints = results["constraints"]
        report.append(f"CONSTRAINTS: {'✓ VALID' if constraints['valid'] else '✗ INVALID'}")
        report.append(f"  Expected: {constraints['expected']}")
        report.append(f"  Actual: {constraints['actual']}")
        if constraints['missing']:
            report.append(f"  Missing: {constraints['missing']}")
        if constraints['extra']:
            report.append(f"  Extra: {constraints['extra']}")
        report.append("")

        # Indexes
        indexes = results["indexes"]
        report.append(f"INDEXES: {'✓ VALID' if indexes['valid'] else '✗ INVALID'}")
        report.append(f"  Expected: {indexes['expected']}")
        report.append(f"  Actual: {indexes['actual']}")
        if indexes['missing']:
            report.append(f"  Missing: {indexes['missing']}")
        report.append("")

        # Node Types
        nodes = results["node_types"]
        report.append(f"NODE TYPES: {'✓ VALID' if nodes['valid'] else '✗ INVALID'}")
        report.append(f"  Expected: {nodes['expected']}")
        report.append(f"  Actual: {nodes['actual']}")
        if nodes['missing']:
            report.append(f"  Missing: {nodes['missing']}")
        if nodes['extra']:
            report.append(f"  Extra: {nodes['extra']}")
        if nodes['property_issues']:
            report.append(f"  Property Issues: {nodes['property_issues']}")
        report.append("")

        # Relationship Types
        rels = results["relationship_types"]
        report.append(f"RELATIONSHIP TYPES: {'✓ VALID' if rels['valid'] else '✗ INVALID'}")
        report.append(f"  Expected: {rels['expected']}")
        report.append(f"  Actual: {rels['actual']}")
        if rels['missing']:
            report.append(f"  Missing: {rels['missing']}")
        if rels['extra']:
            report.append(f"  Extra: {rels['extra']}")
        report.append("")

        # Data Integrity
        integrity = results["data_integrity"]
        report.append(f"DATA INTEGRITY: {'✓ VALID' if integrity['valid'] else '✗ INVALID'}")
        if integrity['issues']:
            for issue in integrity['issues']:
                report.append(f"  Issue: {issue}")
        report.append("")

        report.append("=" * 80)

        return "\n".join(report)

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()


def main():
    """Main validation entry point."""
    # Parse command line arguments
    uri = sys.argv[1] if len(sys.argv) > 1 else "bolt://localhost:7687"
    user = sys.argv[2] if len(sys.argv) > 2 else "neo4j"
    password = sys.argv[3] if len(sys.argv) > 3 else "password"

    print(f"Connecting to Neo4j at {uri}...")

    try:
        validator = SchemaValidator(uri, user, password)

        print("Running validation checks...")
        results = validator.validate_all()

        # Generate and print report
        report = validator.generate_report(results)
        print(report)

        # Save results to JSON
        output_path = Path(__file__).parent / "validation_results.json"
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: {output_path}")

        validator.close()

        # Exit with appropriate code
        sys.exit(0 if results["summary"]["failed"] == 0 else 1)

    except Exception as e:
        print(f"ERROR: Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
