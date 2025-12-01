#!/usr/bin/env python3
"""
Neo4j MITRE ATT&CK Import Validation Script
============================================

Validates the integrity and completeness of MITRE ATT&CK data imported into Neo4j.

Usage:
    python validate_neo4j_mitre_import.py [--detailed] [--export-report]

Requirements:
    - neo4j Python driver: pip install neo4j
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

try:
    from neo4j import GraphDatabase
except ImportError:
    print("ERROR: neo4j Python driver not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)


class MITREValidator:
    """Validates MITRE ATT&CK data in Neo4j database"""

    # Expected counts based on Cypher script analysis
    EXPECTED_COUNTS = {
        'AttackTechnique': 823,
        'Mitigation': 46,
        'ThreatActor': 152,
        'Software': 747,
        'Campaign': 36,
        'DataSource': 39,
        'DataComponent': 208,
    }

    EXPECTED_TOTAL_NODES = 2051
    EXPECTED_TOTAL_RELATIONSHIPS = 40886

    # Relationship types (bi-directional pairs)
    RELATIONSHIP_PAIRS = [
        ('USES', 'USED_BY'),
        ('MITIGATES', 'MITIGATED_BY'),
        ('DETECTS', 'DETECTED_BY'),
        ('ATTRIBUTED_TO', 'ATTRIBUTES'),
        ('TARGETS', 'TARGETED_BY'),
    ]

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'uri': uri,
            'checks': [],
            'errors': [],
            'warnings': [],
            'summary': {}
        }

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def _run_query(self, query: str) -> List[Dict]:
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    def _count_nodes(self, label: str) -> int:
        """Count nodes with specific label"""
        query = f"MATCH (n:{label}) RETURN count(n) AS count"
        result = self._run_query(query)
        return result[0]['count'] if result else 0

    def _count_relationships(self, rel_type: Optional[str] = None) -> int:
        """Count relationships of specific type or all relationships"""
        if rel_type:
            query = f"MATCH ()-[r:{rel_type}]->() RETURN count(r) AS count"
        else:
            query = "MATCH ()-[r]->() RETURN count(r) AS count"
        result = self._run_query(query)
        return result[0]['count'] if result else 0

    def check_node_counts(self) -> Dict[str, Tuple[int, int, bool]]:
        """
        Validate node counts for each entity type

        Returns:
            Dict mapping label to (actual_count, expected_count, is_valid)
        """
        print("=" * 60)
        print("ENTITY COUNT VALIDATION")
        print("=" * 60)

        results = {}
        all_valid = True

        for label, expected in self.EXPECTED_COUNTS.items():
            actual = self._count_nodes(label)
            tolerance = max(5, int(expected * 0.05))  # 5% tolerance or minimum 5
            is_valid = abs(actual - expected) <= tolerance

            status = "✓" if is_valid else "✗"
            variance = actual - expected
            variance_str = f"+{variance}" if variance > 0 else str(variance)

            print(f"{status} {label:20s}: {actual:4d} (expected: {expected:4d}, variance: {variance_str})")

            results[label] = (actual, expected, is_valid)

            if not is_valid:
                all_valid = False
                self.validation_results['errors'].append(
                    f"{label} count mismatch: {actual} (expected ~{expected})"
                )
            elif abs(variance) > 0:
                self.validation_results['warnings'].append(
                    f"{label} has variance of {variance_str} from expected"
                )

        # Total node count
        total_actual = sum(r[0] for r in results.values())
        total_valid = abs(total_actual - self.EXPECTED_TOTAL_NODES) <= 100

        print("-" * 60)
        status = "✓" if total_valid else "✗"
        print(f"{status} TOTAL NODES: {total_actual} (expected: ~{self.EXPECTED_TOTAL_NODES})")
        print()

        self.validation_results['checks'].append({
            'check': 'node_counts',
            'passed': all_valid and total_valid,
            'details': results
        })

        return results

    def check_relationship_counts(self) -> Dict[str, int]:
        """
        Validate relationship counts

        Returns:
            Dict mapping relationship type to count
        """
        print("=" * 60)
        print("RELATIONSHIP COUNT VALIDATION")
        print("=" * 60)

        # Get all relationship types
        query = "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType"
        rel_types_result = self._run_query(query)
        rel_types = [r['relationshipType'] for r in rel_types_result]

        results = {}
        for rel_type in sorted(rel_types):
            count = self._count_relationships(rel_type)
            results[rel_type] = count
            print(f"  {rel_type:25s}: {count:6d}")

        total_rels = self._count_relationships()
        tolerance = int(self.EXPECTED_TOTAL_RELATIONSHIPS * 0.05)
        is_valid = abs(total_rels - self.EXPECTED_TOTAL_RELATIONSHIPS) <= tolerance

        print("-" * 60)
        status = "✓" if is_valid else "✗"
        variance = total_rels - self.EXPECTED_TOTAL_RELATIONSHIPS
        variance_str = f"+{variance}" if variance > 0 else str(variance)
        print(f"{status} TOTAL RELATIONSHIPS: {total_rels} (expected: ~{self.EXPECTED_TOTAL_RELATIONSHIPS}, variance: {variance_str})")
        print()

        if not is_valid:
            self.validation_results['errors'].append(
                f"Total relationship count mismatch: {total_rels} (expected ~{self.EXPECTED_TOTAL_RELATIONSHIPS})"
            )

        self.validation_results['checks'].append({
            'check': 'relationship_counts',
            'passed': is_valid,
            'total': total_rels,
            'expected': self.EXPECTED_TOTAL_RELATIONSHIPS,
            'details': results
        })

        return results

    def check_bidirectional_integrity(self) -> List[Tuple[str, str, bool]]:
        """
        Validate bi-directional relationship integrity

        Returns:
            List of (forward_rel, reverse_rel, is_valid) tuples
        """
        print("=" * 60)
        print("BI-DIRECTIONAL RELATIONSHIP INTEGRITY")
        print("=" * 60)

        results = []
        all_valid = True

        for forward, reverse in self.RELATIONSHIP_PAIRS:
            forward_count = self._count_relationships(forward)
            reverse_count = self._count_relationships(reverse)

            is_valid = forward_count == reverse_count
            status = "✓" if is_valid else "✗"

            print(f"{status} {forward:20s} ↔ {reverse:20s}")
            print(f"   Forward: {forward_count:6d} | Reverse: {reverse_count:6d}")

            if not is_valid:
                diff = abs(forward_count - reverse_count)
                print(f"   ✗ MISMATCH: {diff} unpaired relationships")
                all_valid = False
                self.validation_results['errors'].append(
                    f"Bi-directional mismatch: {forward}={forward_count}, {reverse}={reverse_count}"
                )

            results.append((forward, reverse, is_valid))

        print()

        self.validation_results['checks'].append({
            'check': 'bidirectional_integrity',
            'passed': all_valid,
            'details': results
        })

        return results

    def check_constraints_and_indexes(self) -> Dict[str, List[str]]:
        """
        Validate database constraints and indexes

        Returns:
            Dict with 'constraints' and 'indexes' lists
        """
        print("=" * 60)
        print("CONSTRAINTS AND INDEXES")
        print("=" * 60)

        # Get constraints
        query_constraints = "SHOW CONSTRAINTS"
        constraints_result = self._run_query(query_constraints)
        constraints = [c.get('name', c.get('description', str(c))) for c in constraints_result]

        print(f"✓ Constraints found: {len(constraints)}")
        for constraint in constraints:
            print(f"  - {constraint}")

        # Get indexes
        query_indexes = "SHOW INDEXES"
        indexes_result = self._run_query(query_indexes)
        indexes = [idx.get('name', idx.get('description', str(idx))) for idx in indexes_result]

        print(f"\n✓ Indexes found: {len(indexes)}")
        for index in indexes:
            print(f"  - {index}")

        print()

        results = {
            'constraints': constraints,
            'indexes': indexes
        }

        self.validation_results['checks'].append({
            'check': 'constraints_and_indexes',
            'passed': True,
            'details': results
        })

        return results

    def run_sample_queries(self) -> List[Dict]:
        """
        Execute sample queries to validate data quality

        Returns:
            List of query results
        """
        print("=" * 60)
        print("SAMPLE QUERY VALIDATION")
        print("=" * 60)

        sample_queries = [
            {
                'name': 'Techniques by Tactic',
                'query': """
                    MATCH (t:AttackTechnique)
                    UNWIND t.tactics AS tactic
                    RETURN tactic, count(t) AS technique_count
                    ORDER BY technique_count DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Top Threat Actors by Technique Usage',
                'query': """
                    MATCH (actor:ThreatActor)-[:USES]->(tech:AttackTechnique)
                    RETURN actor.name AS actor, count(tech) AS techniques_used
                    ORDER BY techniques_used DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Most Targeted Techniques',
                'query': """
                    MATCH (tech:AttackTechnique)<-[:USES]-(actor:ThreatActor)
                    RETURN tech.id AS technique_id, tech.name AS technique,
                           count(actor) AS threat_actor_count
                    ORDER BY threat_actor_count DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Software with Most Techniques',
                'query': """
                    MATCH (s:Software)-[:USES]->(tech:AttackTechnique)
                    RETURN s.name AS software, count(tech) AS techniques
                    ORDER BY techniques DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Mitigations Effectiveness',
                'query': """
                    MATCH (m:Mitigation)-[:MITIGATES]->(tech:AttackTechnique)
                    RETURN m.name AS mitigation, count(tech) AS techniques_mitigated
                    ORDER BY techniques_mitigated DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Subtechnique Distribution',
                'query': """
                    MATCH (t:AttackTechnique)
                    WHERE t.is_subtechnique = true
                    WITH substring(t.id, 0, 5) AS parent_id, count(t) AS subtechnique_count
                    RETURN parent_id, subtechnique_count
                    ORDER BY subtechnique_count DESC
                    LIMIT 5
                """
            },
            {
                'name': 'Data Source Coverage',
                'query': """
                    MATCH (ds:DataSource)-[:HAS_COMPONENT]->(dc:DataComponent)
                    RETURN ds.name AS data_source, count(dc) AS components
                    ORDER BY components DESC
                    LIMIT 5
                """
            }
        ]

        results = []

        for query_info in sample_queries:
            try:
                print(f"\n{query_info['name']}:")
                print("-" * 60)

                query_results = self._run_query(query_info['query'])

                if query_results:
                    # Print table header
                    headers = list(query_results[0].keys())
                    header_str = " | ".join(f"{h:20s}" for h in headers)
                    print(header_str)
                    print("-" * len(header_str))

                    # Print rows
                    for row in query_results:
                        row_str = " | ".join(f"{str(row[h])[:20]:20s}" for h in headers)
                        print(row_str)

                    results.append({
                        'query': query_info['name'],
                        'success': True,
                        'results': query_results
                    })
                else:
                    print("  (No results)")
                    results.append({
                        'query': query_info['name'],
                        'success': True,
                        'results': []
                    })

            except Exception as e:
                print(f"  ✗ ERROR: {str(e)}")
                self.validation_results['errors'].append(
                    f"Sample query '{query_info['name']}' failed: {str(e)}"
                )
                results.append({
                    'query': query_info['name'],
                    'success': False,
                    'error': str(e)
                })

        print()

        self.validation_results['checks'].append({
            'check': 'sample_queries',
            'passed': all(r['success'] for r in results),
            'details': results
        })

        return results

    def check_data_quality(self) -> Dict[str, any]:
        """
        Validate data quality (required fields, data integrity)

        Returns:
            Dict with quality check results
        """
        print("=" * 60)
        print("DATA QUALITY VALIDATION")
        print("=" * 60)

        quality_checks = []

        # Check for nodes missing required properties
        print("\nChecking for missing required properties...")

        checks = [
            ("AttackTechnique missing ID", "MATCH (t:AttackTechnique) WHERE t.id IS NULL RETURN count(t) AS count"),
            ("AttackTechnique missing name", "MATCH (t:AttackTechnique) WHERE t.name IS NULL RETURN count(t) AS count"),
            ("ThreatActor missing name", "MATCH (a:ThreatActor) WHERE a.name IS NULL RETURN count(a) AS count"),
            ("Software missing name", "MATCH (s:Software) WHERE s.name IS NULL RETURN count(s) AS count"),
            ("Mitigation missing name", "MATCH (m:Mitigation) WHERE m.name IS NULL RETURN count(m) AS count"),
        ]

        all_valid = True
        for check_name, query in checks:
            result = self._run_query(query)
            count = result[0]['count'] if result else 0

            status = "✓" if count == 0 else "✗"
            print(f"{status} {check_name}: {count}")

            quality_checks.append({
                'check': check_name,
                'count': count,
                'passed': count == 0
            })

            if count > 0:
                all_valid = False
                self.validation_results['errors'].append(f"{check_name}: {count} occurrences")

        # Check for orphaned nodes (nodes with no relationships)
        print("\nChecking for orphaned nodes...")

        orphan_query = """
            MATCH (n)
            WHERE NOT (n)--()
            RETURN labels(n)[0] AS label, count(n) AS count
            ORDER BY count DESC
        """

        orphan_result = self._run_query(orphan_query)
        if orphan_result:
            for row in orphan_result:
                print(f"  ⚠ {row['label']}: {row['count']} orphaned nodes")
                self.validation_results['warnings'].append(
                    f"{row['label']} has {row['count']} orphaned nodes"
                )
        else:
            print("  ✓ No orphaned nodes found")

        print()

        self.validation_results['checks'].append({
            'check': 'data_quality',
            'passed': all_valid,
            'details': quality_checks
        })

        return {
            'quality_checks': quality_checks,
            'orphaned_nodes': orphan_result
        }

    def generate_summary(self):
        """Generate validation summary"""
        print("=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        total_checks = len(self.validation_results['checks'])
        passed_checks = sum(1 for c in self.validation_results['checks'] if c['passed'])

        print(f"\nTotal Checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {total_checks - passed_checks}")

        if self.validation_results['errors']:
            print(f"\nErrors ({len(self.validation_results['errors'])}):")
            for error in self.validation_results['errors']:
                print(f"  ✗ {error}")

        if self.validation_results['warnings']:
            print(f"\nWarnings ({len(self.validation_results['warnings'])}):")
            for warning in self.validation_results['warnings']:
                print(f"  ⚠ {warning}")

        overall_status = "PASSED" if passed_checks == total_checks and not self.validation_results['errors'] else "FAILED"
        print(f"\nOVERALL STATUS: {overall_status}")
        print("=" * 60)

        self.validation_results['summary'] = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': total_checks - passed_checks,
            'error_count': len(self.validation_results['errors']),
            'warning_count': len(self.validation_results['warnings']),
            'overall_status': overall_status
        }

    def export_report(self, filepath: str):
        """Export validation report to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        print(f"\nValidation report exported to: {filepath}")


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate MITRE ATT&CK data in Neo4j database'
    )
    parser.add_argument(
        '--uri',
        default=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
        help='Neo4j connection URI (default: bolt://localhost:7687)'
    )
    parser.add_argument(
        '--user',
        default=os.getenv('NEO4J_USER', 'neo4j'),
        help='Neo4j username (default: neo4j)'
    )
    parser.add_argument(
        '--password',
        default=os.getenv('NEO4J_PASSWORD'),
        help='Neo4j password (can also use NEO4J_PASSWORD env var)'
    )
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Run detailed validation checks'
    )
    parser.add_argument(
        '--export-report',
        metavar='FILEPATH',
        help='Export validation report to JSON file'
    )

    args = parser.parse_args()

    if not args.password:
        print("ERROR: Neo4j password required (use --password or NEO4J_PASSWORD env var)")
        sys.exit(1)

    print(f"\nConnecting to Neo4j at {args.uri}...")

    try:
        validator = MITREValidator(args.uri, args.user, args.password)

        print("✓ Connected successfully\n")

        # Run validation checks
        validator.check_node_counts()
        validator.check_relationship_counts()
        validator.check_bidirectional_integrity()
        validator.check_constraints_and_indexes()

        if args.detailed:
            validator.check_data_quality()
            validator.run_sample_queries()

        validator.generate_summary()

        # Export report if requested
        if args.export_report:
            validator.export_report(args.export_report)

        validator.close()

        # Exit with appropriate code
        if validator.validation_results['summary']['overall_status'] == 'PASSED':
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
