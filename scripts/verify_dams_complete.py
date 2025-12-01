#!/usr/bin/env python3
"""
DAMS Sector Verification Script
Verifies complete deployment of all 7 node types and relationships
Expected: 35,184 nodes across Equipment, Process, Vulnerability, Threat, Mitigation, Incident, Standard
"""

from neo4j import GraphDatabase
import os
from datetime import datetime
import sys

# Neo4j connection configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

class DAMSVerifier:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.expected_counts = {
            'DamsEquipment': 14074,
            'DamsProcess': 5630,
            'DamsVulnerability': 4222,
            'DamsThreat': 4222,
            'DamsMitigation': 3518,
            'DamsIncident': 2111,
            'DamsStandard': 1407
        }
        self.total_expected = 35184

    def close(self):
        self.driver.close()

    def verify_node_counts(self, session):
        """Verify all node types are deployed with correct counts"""
        result = session.run("""
            MATCH (n)
            WHERE any(label IN labels(n) WHERE label STARTS WITH 'Dams')
            WITH [label IN labels(n) WHERE label STARTS WITH 'Dams'][0] as dams_label
            RETURN dams_label, count(*) as count
            ORDER BY dams_label
        """)

        actual_counts = {}
        total_actual = 0
        all_correct = True

        print("Node Type Verification:")
        print("-" * 70)

        for record in result:
            label = record['dams_label']
            actual = record['count']
            expected = self.expected_counts.get(label, 0)
            actual_counts[label] = actual
            total_actual += actual

            status = "✅" if actual == expected else "❌"
            if actual != expected:
                all_correct = False

            print(f"  {status} {label:25s}: {actual:6,} / {expected:6,}")

        print("-" * 70)
        total_status = "✅" if total_actual == self.total_expected else "❌"
        print(f"  {total_status} {'TOTAL':25s}: {total_actual:6,} / {self.total_expected:6,}")

        return all_correct and total_actual == self.total_expected, actual_counts, total_actual

    def verify_relationships(self, session):
        """Verify relationships exist between node types"""
        result = session.run("""
            MATCH (s)-[r]->(t)
            WHERE s.sector = 'DAMS' OR t.sector = 'DAMS'
            RETURN type(r) as rel_type, count(*) as count
            ORDER BY count DESC
        """)

        print("\n" + "=" * 70)
        print("Relationship Verification:")
        print("-" * 70)

        total_rels = 0
        rel_types = []

        for record in result:
            rel_type = record['rel_type']
            count = record['count']
            total_rels += count
            rel_types.append(rel_type)
            print(f"  ✅ {rel_type:30s}: {count:6,}")

        print("-" * 70)
        print(f"  {'TOTAL RELATIONSHIPS':30s}: {total_rels:6,}")

        # Verify expected relationship types exist
        expected_rels = [
            'HAS_VULNERABILITY', 'EXECUTES_PROCESS', 'EXPLOITED_BY',
            'MITIGATED_BY', 'INVOLVES', 'APPLIES_TO', 'REQUIRES_STANDARD'
        ]

        missing_rels = set(expected_rels) - set(rel_types)
        if missing_rels:
            print(f"\n  ⚠️  Missing relationship types: {', '.join(missing_rels)}")
            return False

        return total_rels > 0

    def verify_subsectors(self, session):
        """Verify subsector distribution"""
        result = session.run("""
            MATCH (n:DamsEquipment)
            RETURN n.subsector as subsector, count(*) as count
            ORDER BY count DESC
        """)

        print("\n" + "=" * 70)
        print("Subsector Verification:")
        print("-" * 70)

        expected_subsectors = ['Hydroelectric Generation', 'Flood Control', 'Water Supply']
        actual_subsectors = []

        for record in result:
            subsector = record['subsector']
            count = record['count']
            actual_subsectors.append(subsector)
            status = "✅" if subsector in expected_subsectors else "⚠️"
            print(f"  {status} {subsector:40s}: {count:6,}")

        missing_subsectors = set(expected_subsectors) - set(actual_subsectors)
        if missing_subsectors:
            print(f"\n  ⚠️  Missing subsectors: {', '.join(missing_subsectors)}")
            return False

        return True

    def verify_node_structure(self, session):
        """Verify node properties and structure"""
        result = session.run("""
            MATCH (n:DamsEquipment)
            RETURN n LIMIT 1
        """)

        record = result.single()
        if not record:
            print("\n❌ No DamsEquipment nodes found for structure verification")
            return False

        node = record['n']
        required_props = ['id', 'name', 'component', 'subsector', 'sector', 'type']

        print("\n" + "=" * 70)
        print("Node Structure Verification:")
        print("-" * 70)

        all_present = True
        for prop in required_props:
            if prop in node:
                print(f"  ✅ {prop:20s}: {node[prop]}")
            else:
                print(f"  ❌ {prop:20s}: MISSING")
                all_present = False

        return all_present

    def verify(self):
        """Execute complete verification"""
        print("=" * 70)
        print("DAMS SECTOR VERIFICATION")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        all_checks_passed = True

        with self.driver.session() as session:
            # Verify node counts
            nodes_ok, counts, total = self.verify_node_counts(session)
            if not nodes_ok:
                all_checks_passed = False

            # Verify relationships
            rels_ok = self.verify_relationships(session)
            if not rels_ok:
                all_checks_passed = False

            # Verify subsectors
            subsectors_ok = self.verify_subsectors(session)
            if not subsectors_ok:
                all_checks_passed = False

            # Verify node structure
            structure_ok = self.verify_node_structure(session)
            if not structure_ok:
                all_checks_passed = False

        print("\n" + "=" * 70)
        if all_checks_passed:
            print("VERIFICATION STATUS: ✅ ALL CHECKS PASSED")
            print("DAMS Sector deployment is COMPLETE and VERIFIED")
            return 0
        else:
            print("VERIFICATION STATUS: ❌ SOME CHECKS FAILED")
            print("Please review failed checks above")
            return 1
        print("=" * 70)

if __name__ == "__main__":
    verifier = DAMSVerifier(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        exit_code = verifier.verify()
        sys.exit(exit_code)
    finally:
        verifier.close()
