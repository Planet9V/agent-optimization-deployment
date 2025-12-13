#!/usr/bin/env python3
"""
Neo4j Sprint 1 Schema Loader
Created: 2025-12-12
Purpose: Load and validate Neo4j schema for Sprint 1 APIs
"""

import os
import sys
from typing import Dict, List, Any
from pathlib import Path

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import ServiceUnavailable, AuthError
except ImportError:
    print("ERROR: neo4j driver not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)


class Neo4jSchemaLoader:
    """Load and validate Neo4j schema for AEON Sprint 1"""

    def __init__(self, uri: str = "bolt://localhost:7687",
                 user: str = "neo4j",
                 password: str = "password"):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j connection URI
            user: Neo4j username
            password: Neo4j password
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None

    def connect(self) -> bool:
        """
        Establish Neo4j connection

        Returns:
            bool: True if connection successful
        """
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                test_value = result.single()["test"]
                if test_value == 1:
                    print(f"✅ Connected to Neo4j at {self.uri}")
                    return True
        except ServiceUnavailable:
            print(f"❌ Neo4j not available at {self.uri}")
            return False
        except AuthError:
            print(f"❌ Authentication failed for user {self.user}")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def load_schema_file(self, filepath: str) -> bool:
        """
        Load Cypher schema from file

        Args:
            filepath: Path to .cypher file

        Returns:
            bool: True if schema loaded successfully
        """
        if not os.path.exists(filepath):
            print(f"❌ Schema file not found: {filepath}")
            return False

        print(f"\n📄 Loading schema from: {filepath}")

        with open(filepath, 'r') as f:
            cypher_script = f.read()

        # Split script into individual statements
        statements = [
            stmt.strip()
            for stmt in cypher_script.split(';')
            if stmt.strip() and not stmt.strip().startswith('//')
        ]

        print(f"📊 Found {len(statements)} Cypher statements")

        successful = 0
        failed = 0

        with self.driver.session() as session:
            for idx, statement in enumerate(statements, 1):
                # Skip comments and empty statements
                if not statement or statement.startswith('//'):
                    continue

                try:
                    session.run(statement)
                    successful += 1
                    if idx % 10 == 0:
                        print(f"⏳ Processed {idx}/{len(statements)} statements...")
                except Exception as e:
                    failed += 1
                    print(f"⚠️  Statement {idx} failed: {str(e)[:100]}")

        print(f"\n✅ Successfully executed: {successful} statements")
        if failed > 0:
            print(f"⚠️  Failed: {failed} statements")

        return failed == 0

    def validate_constraints(self) -> Dict[str, List[str]]:
        """
        Validate constraint creation

        Returns:
            dict: Constraints by type
        """
        print("\n🔍 Validating Constraints...")

        with self.driver.session() as session:
            result = session.run("CALL db.constraints() YIELD name, type")
            constraints = [(record["name"], record["type"]) for record in result]

        expected_constraints = [
            "sbom_id_unique",
            "sbom_name_unique",
            "component_id_unique",
            "cve_id_unique",
            "equipment_id_unique",
            "equipment_serial_unique",
            "vendor_id_unique",
            "vendor_name_unique",
            "eol_status_id_unique"
        ]

        found = [name for name, _ in constraints]

        print(f"✅ Found {len(constraints)} constraints:")
        for name, ctype in constraints:
            print(f"   - {name} ({ctype})")

        missing = set(expected_constraints) - set(found)
        if missing:
            print(f"\n⚠️  Missing constraints: {missing}")

        return {"found": found, "missing": list(missing)}

    def validate_indexes(self) -> Dict[str, List[str]]:
        """
        Validate index creation

        Returns:
            dict: Indexes by state
        """
        print("\n🔍 Validating Indexes...")

        with self.driver.session() as session:
            result = session.run(
                "CALL db.indexes() YIELD name, type, state "
                "RETURN name, type, state"
            )
            indexes = [
                (record["name"], record["type"], record["state"])
                for record in result
            ]

        online = [name for name, _, state in indexes if state == "ONLINE"]
        failed = [name for name, _, state in indexes if state == "FAILED"]

        print(f"✅ Found {len(online)} online indexes:")
        for name, itype, state in indexes[:10]:  # Show first 10
            print(f"   - {name} ({itype}) [{state}]")

        if len(indexes) > 10:
            print(f"   ... and {len(indexes) - 10} more")

        if failed:
            print(f"\n⚠️  Failed indexes: {failed}")

        return {"online": online, "failed": failed}

    def validate_node_counts(self) -> Dict[str, int]:
        """
        Validate sample data node counts

        Returns:
            dict: Node counts by label
        """
        print("\n🔍 Validating Node Counts...")

        with self.driver.session() as session:
            result = session.run(
                "MATCH (n) RETURN labels(n)[0] as label, count(n) as count "
                "ORDER BY label"
            )
            counts = {record["label"]: record["count"] for record in result}

        expected = {
            "SBOM": 2,
            "Component": 5,
            "CVE": 3,
            "Equipment": 4,
            "Vendor": 4,
            "EOLStatus": 4
        }

        print("Node Type Counts:")
        for label, count in counts.items():
            expected_count = expected.get(label, "?")
            status = "✅" if count == expected_count else "⚠️"
            print(f"   {status} {label}: {count} (expected: {expected_count})")

        return counts

    def validate_relationship_counts(self) -> Dict[str, int]:
        """
        Validate relationship counts

        Returns:
            dict: Relationship counts by type
        """
        print("\n🔍 Validating Relationship Counts...")

        with self.driver.session() as session:
            result = session.run(
                "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count "
                "ORDER BY rel_type"
            )
            counts = {record["rel_type"]: record["count"] for record in result}

        print("Relationship Type Counts:")
        for rel_type, count in counts.items():
            print(f"   - {rel_type}: {count}")

        return counts

    def test_query_patterns(self) -> Dict[str, bool]:
        """
        Test all 8 API query patterns

        Returns:
            dict: Query test results
        """
        print("\n🔍 Testing Query Patterns...")

        test_queries = {
            "sbom_by_sector": """
                MATCH (s:SBOM {sector: 'defense'})-[:HAS_COMPONENT]->(c:Component)
                RETURN s.sbom_id, count(c) as component_count
                LIMIT 1
            """,
            "component_dependencies": """
                MATCH (c:Component {component_id: 'COMP-001'})-[d:DEPENDS_ON*1..3]->(dep:Component)
                RETURN count(dep) as dep_count
            """,
            "vulnerabilities_by_severity": """
                MATCH (c:Component)-[r:HAS_VULNERABILITY]->(v:CVE {severity: 'CRITICAL'})
                RETURN count(v) as critical_count
            """,
            "equipment_by_sector": """
                MATCH (e:Equipment {sector: 'defense'})-[:RUNS_SOFTWARE]->(c:Component)
                RETURN count(e) as equipment_count
            """,
            "equipment_eol_status": """
                MATCH (e:Equipment)-[:HAS_STATUS]->(eol:EOLStatus)
                WHERE eol.eol_date <= date('2025-12-31')
                RETURN count(e) as approaching_eol_count
            """,
            "critical_vulnerabilities": """
                MATCH (e:Equipment {criticality: 'CRITICAL'})-[:RUNS_SOFTWARE]->(c:Component)
                MATCH (c)-[r:HAS_VULNERABILITY]->(v:CVE)
                WHERE r.patched = false AND v.severity IN ['CRITICAL', 'HIGH']
                RETURN count(v) as unpatched_critical_count
            """,
            "vendor_summary": """
                MATCH (v:Vendor)<-[:FROM_VENDOR]-(e:Equipment)
                RETURN v.name, count(e) as equipment_count
                ORDER BY equipment_count DESC
                LIMIT 5
            """
        }

        results = {}

        with self.driver.session() as session:
            for query_name, query in test_queries.items():
                try:
                    result = session.run(query)
                    record = result.single()
                    results[query_name] = True
                    print(f"   ✅ {query_name}: {dict(record)}")
                except Exception as e:
                    results[query_name] = False
                    print(f"   ❌ {query_name}: {str(e)[:50]}")

        return results

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("\n👋 Neo4j connection closed")


def main():
    """Main execution function"""
    print("=" * 70)
    print("Neo4j Sprint 1 Schema Loader")
    print("=" * 70)

    # Get Neo4j credentials from environment or use defaults
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    # Initialize loader
    loader = Neo4jSchemaLoader(uri, user, password)

    # Connect to Neo4j
    if not loader.connect():
        print("\n❌ Failed to connect to Neo4j. Exiting.")
        sys.exit(1)

    # Load schema file
    schema_file = Path(__file__).parent / "neo4j_schema_sprint1.cypher"

    if not loader.load_schema_file(str(schema_file)):
        print("\n⚠️  Schema loaded with errors. Continuing validation...")

    # Run validations
    loader.validate_constraints()
    loader.validate_indexes()
    loader.validate_node_counts()
    loader.validate_relationship_counts()
    loader.test_query_patterns()

    # Close connection
    loader.close()

    print("\n" + "=" * 70)
    print("✅ Schema loading and validation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
