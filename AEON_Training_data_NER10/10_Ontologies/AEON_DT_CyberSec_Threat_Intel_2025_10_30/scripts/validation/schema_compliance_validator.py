#!/usr/bin/env python3
"""
Schema Compliance Validator - Validate graph against ontology schema
"""

import json
from typing import Dict, List, Set
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SchemaViolation:
    """Represents a schema compliance violation"""
    severity: str
    violation_type: str
    description: str
    examples: List[str]
    count: int


class SchemaComplianceValidator:
    """Validate graph compliance with defined schema"""

    # Define expected schema
    SCHEMA = {
        "node_types": {
            "Vulnerability": {
                "required_props": ["id", "cvss_score", "description"],
                "optional_props": ["published_date", "last_modified", "references"],
                "allowed_relationships": {
                    "outgoing": ["AFFECTS", "HAS_EXPLOIT", "RELATED_TO"],
                    "incoming": ["MENTIONS", "MITIGATES"]
                }
            },
            "Component": {
                "required_props": ["name", "type", "criticality"],
                "optional_props": ["ip_address", "hostname", "zone"],
                "allowed_relationships": {
                    "outgoing": ["RUNS", "CONNECTS_TO", "DEPENDS_ON", "EXPOSED_TO"],
                    "incoming": ["AFFECTS", "CONTAINS"]
                }
            },
            "Software": {
                "required_props": ["name", "vendor", "product"],
                "optional_props": ["version", "cpe"],
                "allowed_relationships": {
                    "outgoing": ["HAS_VERSION"],
                    "incoming": ["RUNS", "AFFECTS"]
                }
            },
            "NetworkInterface": {
                "required_props": ["ip_address", "zone"],
                "optional_props": ["mac_address", "vlan"],
                "allowed_relationships": {
                    "outgoing": ["CONNECTS_TO"],
                    "incoming": ["EXPOSED_TO", "CONNECTS_TO"]
                }
            },
            "Exploit": {
                "required_props": ["id", "maturity"],
                "optional_props": ["source", "url"],
                "allowed_relationships": {
                    "outgoing": [],
                    "incoming": ["HAS_EXPLOIT"]
                }
            },
            "ThreatIntel": {
                "required_props": ["source", "timestamp"],
                "optional_props": ["confidence", "description"],
                "allowed_relationships": {
                    "outgoing": ["MENTIONS"],
                    "incoming": []
                }
            },
            "CPE": {
                "required_props": ["criteria", "vendor", "product"],
                "optional_props": ["version"],
                "allowed_relationships": {
                    "outgoing": [],
                    "incoming": ["AFFECTS"]
                }
            }
        },
        "relationship_types": {
            "AFFECTS": {
                "valid_source": ["Vulnerability"],
                "valid_target": ["Component", "Software", "CPE"],
                "required_props": [],
                "optional_props": ["severity"]
            },
            "CONNECTS_TO": {
                "valid_source": ["NetworkInterface", "Component"],
                "valid_target": ["NetworkInterface", "Component"],
                "required_props": ["allowed"],
                "optional_props": ["protocol", "port", "firewall_rule"]
            },
            "DEPENDS_ON": {
                "valid_source": ["Component"],
                "valid_target": ["Component", "Software"],
                "required_props": [],
                "optional_props": ["dependency_type"]
            },
            "RUNS": {
                "valid_source": ["Component"],
                "valid_target": ["Software"],
                "required_props": [],
                "optional_props": ["version"]
            },
            "HAS_EXPLOIT": {
                "valid_source": ["Vulnerability"],
                "valid_target": ["Exploit"],
                "required_props": [],
                "optional_props": []
            },
            "MENTIONS": {
                "valid_source": ["ThreatIntel"],
                "valid_target": ["Vulnerability"],
                "required_props": [],
                "optional_props": ["context"]
            }
        },
        "property_types": {
            "cvss_score": "float",
            "criticality": "enum:critical|high|medium|low|info",
            "zone": "enum:external|dmz|internal|restricted|critical",
            "allowed": "boolean",
            "port": "integer",
            "timestamp": "datetime"
        }
    }

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.violations: List[SchemaViolation] = []

    def close(self):
        self.driver.close()

    def validate_all(self) -> Dict:
        """Run all schema validation checks"""
        logger.info("Starting schema compliance validation...")

        self.validate_node_types()
        self.validate_relationship_types()
        self.validate_property_types()
        self.check_schema_gaps()

        return self.generate_report()

    def validate_node_types(self):
        """Validate node labels and properties against schema"""
        # Get all node labels in database
        query = '''
        CALL db.labels() YIELD label
        RETURN label
        '''

        with self.driver.session() as session:
            result = session.run(query)
            db_labels = [record["label"] for record in result]

            # Check for unknown labels
            known_labels = set(self.SCHEMA["node_types"].keys())
            unknown_labels = set(db_labels) - known_labels

            if unknown_labels:
                self.violations.append(SchemaViolation(
                    severity="warning",
                    violation_type="unknown_node_type",
                    description=f"Unknown node types in database: {', '.join(unknown_labels)}",
                    examples=list(unknown_labels),
                    count=len(unknown_labels)
                ))

            # Validate each node type
            for label, schema in self.SCHEMA["node_types"].items():
                self._validate_node_label(session, label, schema)

        logger.info("Validated node types")

    def _validate_node_label(self, session, label: str, schema: Dict):
        """Validate nodes of specific label"""
        # Check required properties
        for prop in schema["required_props"]:
            query = f'''
            MATCH (n:{label})
            WHERE n.{prop} IS NULL OR n.{prop} = ''
            RETURN count(*) as count, collect(n.id)[..5] as examples
            '''

            result = session.run(query)
            record = result.single()

            if record and record["count"] > 0:
                self.violations.append(SchemaViolation(
                    severity="critical",
                    violation_type="missing_required_property",
                    description=f"{label} nodes missing required property '{prop}'",
                    examples=record["examples"],
                    count=record["count"]
                ))

        # Check for unexpected properties
        query = f'''
        MATCH (n:{label})
        RETURN keys(n) as props
        LIMIT 100
        '''

        result = session.run(query)
        all_props = set()
        for record in result:
            all_props.update(record["props"])

        expected_props = set(schema["required_props"] + schema["optional_props"])
        unexpected_props = all_props - expected_props

        if unexpected_props:
            self.violations.append(SchemaViolation(
                severity="info",
                violation_type="unexpected_property",
                description=f"{label} nodes have unexpected properties: {', '.join(unexpected_props)}",
                examples=list(unexpected_props),
                count=len(unexpected_props)
            ))

    def validate_relationship_types(self):
        """Validate relationship types and constraints"""
        query = '''
        CALL db.relationshipTypes() YIELD relationshipType
        RETURN relationshipType
        '''

        with self.driver.session() as session:
            result = session.run(query)
            db_rel_types = [record["relationshipType"] for record in result]

            # Check for unknown relationship types
            known_rels = set(self.SCHEMA["relationship_types"].keys())
            unknown_rels = set(db_rel_types) - known_rels

            if unknown_rels:
                self.violations.append(SchemaViolation(
                    severity="warning",
                    violation_type="unknown_relationship_type",
                    description=f"Unknown relationship types: {', '.join(unknown_rels)}",
                    examples=list(unknown_rels),
                    count=len(unknown_rels)
                ))

            # Validate each relationship type
            for rel_type, schema in self.SCHEMA["relationship_types"].items():
                self._validate_relationship(session, rel_type, schema)

        logger.info("Validated relationship types")

    def _validate_relationship(self, session, rel_type: str, schema: Dict):
        """Validate specific relationship type"""
        # Check source/target node type constraints
        query = f'''
        MATCH (source)-[r:{rel_type}]->(target)
        RETURN DISTINCT labels(source) as source_labels, labels(target) as target_labels
        LIMIT 100
        '''

        result = session.run(query)

        for record in result:
            source_labels = record["source_labels"]
            target_labels = record["target_labels"]

            # Check if source type is valid
            valid_source = any(label in schema["valid_source"] for label in source_labels)
            if not valid_source:
                self.violations.append(SchemaViolation(
                    severity="critical",
                    violation_type="invalid_relationship_source",
                    description=f"{rel_type} has invalid source type: {source_labels}",
                    examples=[str(source_labels)],
                    count=1
                ))

            # Check if target type is valid
            valid_target = any(label in schema["valid_target"] for label in target_labels)
            if not valid_target:
                self.violations.append(SchemaViolation(
                    severity="critical",
                    violation_type="invalid_relationship_target",
                    description=f"{rel_type} has invalid target type: {target_labels}",
                    examples=[str(target_labels)],
                    count=1
                ))

    def validate_property_types(self):
        """Validate property data types"""
        with self.driver.session() as session:
            for prop, expected_type in self.SCHEMA["property_types"].items():
                if expected_type.startswith("enum:"):
                    self._validate_enum_property(session, prop, expected_type)
                elif expected_type == "float":
                    self._validate_float_property(session, prop)
                elif expected_type == "integer":
                    self._validate_integer_property(session, prop)
                elif expected_type == "boolean":
                    self._validate_boolean_property(session, prop)

        logger.info("Validated property types")

    def _validate_enum_property(self, session, prop: str, enum_type: str):
        """Validate enumeration property values"""
        valid_values = enum_type.split(":")[1].split("|")

        query = f'''
        MATCH (n)
        WHERE n.{prop} IS NOT NULL
        WITH DISTINCT n.{prop} as value
        WHERE NOT value IN $valid_values
        RETURN collect(value) as invalid_values, count(*) as count
        '''

        result = session.run(query, valid_values=valid_values)
        record = result.single()

        if record and record["count"] > 0:
            self.violations.append(SchemaViolation(
                severity="warning",
                violation_type="invalid_enum_value",
                description=f"Property '{prop}' has invalid enum values (expected: {', '.join(valid_values)})",
                examples=record["invalid_values"][:5],
                count=record["count"]
            ))

    def _validate_float_property(self, session, prop: str):
        """Validate float property"""
        query = f'''
        MATCH (n)
        WHERE n.{prop} IS NOT NULL
        WITH n.{prop} as value
        WHERE NOT (toFloat(toString(value)) = value)
        RETURN count(*) as count
        '''

        result = session.run(query)
        record = result.single()

        if record and record["count"] > 0:
            self.violations.append(SchemaViolation(
                severity="warning",
                violation_type="invalid_property_type",
                description=f"Property '{prop}' expected float but found non-float values",
                examples=[],
                count=record["count"]
            ))

    def _validate_integer_property(self, session, prop: str):
        """Validate integer property"""
        query = f'''
        MATCH (n)
        WHERE n.{prop} IS NOT NULL
        WITH n.{prop} as value
        WHERE NOT (toInteger(toString(value)) = value)
        RETURN count(*) as count
        '''

        result = session.run(query)
        record = result.single()

        if record and record["count"] > 0:
            self.violations.append(SchemaViolation(
                severity="warning",
                violation_type="invalid_property_type",
                description=f"Property '{prop}' expected integer but found non-integer values",
                examples=[],
                count=record["count"]
            ))

    def _validate_boolean_property(self, session, prop: str):
        """Validate boolean property"""
        query = f'''
        MATCH (n)
        WHERE n.{prop} IS NOT NULL
        WITH n.{prop} as value
        WHERE NOT (value IN [true, false, TRUE, FALSE, 'true', 'false'])
        RETURN count(*) as count
        '''

        result = session.run(query)
        record = result.single()

        if record and record["count"] > 0:
            self.violations.append(SchemaViolation(
                severity="warning",
                violation_type="invalid_property_type",
                description=f"Property '{prop}' expected boolean but found non-boolean values",
                examples=[],
                count=record["count"]
            ))

    def check_schema_gaps(self):
        """Check for missing expected node/relationship types"""
        with self.driver.session() as session:
            # Check for missing node types
            query = "CALL db.labels() YIELD label RETURN collect(label) as labels"
            result = session.run(query)
            db_labels = set(result.single()["labels"])

            expected_labels = set(self.SCHEMA["node_types"].keys())
            missing_labels = expected_labels - db_labels

            if missing_labels:
                self.violations.append(SchemaViolation(
                    severity="info",
                    violation_type="missing_node_type",
                    description=f"Expected node types not found in database: {', '.join(missing_labels)}",
                    examples=list(missing_labels),
                    count=len(missing_labels)
                ))

        logger.info("Checked for schema gaps")

    def generate_report(self) -> Dict:
        """Generate schema compliance report"""
        critical = [v for v in self.violations if v.severity == "critical"]
        warnings = [v for v in self.violations if v.severity == "warning"]
        info = [v for v in self.violations if v.severity == "info"]

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score()

        report = {
            "summary": {
                "total_violations": len(self.violations),
                "critical": len(critical),
                "warnings": len(warnings),
                "info": len(info),
                "compliance_score": compliance_score
            },
            "violations": {
                "critical": [
                    {
                        "type": v.violation_type,
                        "description": v.description,
                        "count": v.count,
                        "examples": v.examples[:3]
                    }
                    for v in critical
                ],
                "warnings": [
                    {
                        "type": v.violation_type,
                        "description": v.description,
                        "count": v.count
                    }
                    for v in warnings[:20]
                ],
                "info": [
                    {
                        "type": v.violation_type,
                        "description": v.description
                    }
                    for v in info[:10]
                ]
            }
        }

        return report

    def _calculate_compliance_score(self) -> float:
        """Calculate compliance score (0-100)"""
        if not self.violations:
            return 100.0

        penalties = {
            "critical": 15,
            "warning": 5,
            "info": 1
        }

        total_penalty = sum(
            penalties.get(v.severity, 1)
            for v in self.violations
        )

        score = max(0, 100 - total_penalty)
        return round(score, 2)

    def export_schema(self, output_file: str):
        """Export schema definition"""
        with open(output_file, 'w') as f:
            json.dump(self.SCHEMA, f, indent=2)

        logger.info(f"Schema exported to {output_file}")


def main():
    """Example usage"""
    validator = SchemaComplianceValidator(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Run validation
        report = validator.validate_all()

        print("\n=== Schema Compliance Report ===")
        print(f"Compliance Score: {report['summary']['compliance_score']}/100")
        print(f"Critical Violations: {report['summary']['critical']}")
        print(f"Warnings: {report['summary']['warnings']}")

        # Print critical violations
        if report['violations']['critical']:
            print("\n=== Critical Violations ===")
            for v in report['violations']['critical']:
                print(f"- {v['description']} (count: {v['count']})")

        # Export schema
        validator.export_schema("/tmp/schema.json")

    finally:
        validator.close()


if __name__ == "__main__":
    main()
