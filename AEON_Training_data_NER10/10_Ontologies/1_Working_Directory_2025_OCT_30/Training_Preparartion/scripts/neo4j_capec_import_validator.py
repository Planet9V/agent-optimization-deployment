#!/usr/bin/env python3
"""
Neo4j CAPEC Import Validator
Validates successful import of CAPEC v3.9 relationships and verifies attack chain connectivity
"""

from neo4j import GraphDatabase
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Neo4j connection (adjust as needed)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Update with actual password

class CAPECImportValidator:
    """Validates CAPEC v3.9 import and attack chain connectivity"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'summary': {}
        }

    def close(self):
        self.driver.close()

    def run_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def validate_capec_nodes(self):
        """Validate CAPEC attack pattern nodes"""
        print("\n🔍 Validating CAPEC Nodes...")

        query = """
        MATCH (capec:AttackPattern)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN count(capec) AS count,
               count(DISTINCT capec.abstraction) AS abstraction_types
        """

        result = self.run_query(query)[0]

        test_result = {
            'test': 'CAPEC Nodes',
            'expected': 615,
            'actual': result['count'],
            'abstraction_types': result['abstraction_types'],
            'passed': result['count'] >= 615
        }

        self.validation_results['tests'].append(test_result)

        if test_result['passed']:
            print(f"✅ CAPEC Nodes: {result['count']} (Expected: 615+)")
            print(f"   Abstraction Types: {result['abstraction_types']}")
        else:
            print(f"❌ CAPEC Nodes: {result['count']} (Expected: 615+)")

        return test_result['passed']

    def validate_capec_cwe_relationships(self):
        """Validate CAPEC→CWE relationships"""
        print("\n🔍 Validating CAPEC→CWE Relationships...")

        query = """
        MATCH (capec:AttackPattern)-[r:EXPLOITS_WEAKNESS]->(cwe:Weakness)
        WHERE r.source = 'CAPEC_v3.9_XML'
        RETURN count(r) AS count,
               count(DISTINCT capec) AS capec_count,
               count(DISTINCT cwe) AS cwe_count
        """

        result = self.run_query(query)[0]

        test_result = {
            'test': 'CAPEC→CWE Relationships',
            'expected': 1214,
            'actual': result['count'],
            'capec_with_cwe': result['capec_count'],
            'unique_cwes': result['cwe_count'],
            'passed': result['count'] >= 1214
        }

        self.validation_results['tests'].append(test_result)

        if test_result['passed']:
            print(f"✅ CAPEC→CWE: {result['count']} relationships (Expected: 1,214+)")
            print(f"   CAPECs with CWE: {result['capec_count']}")
            print(f"   Unique CWEs: {result['cwe_count']}")
        else:
            print(f"❌ CAPEC→CWE: {result['count']} (Expected: 1,214+)")

        return test_result['passed']

    def validate_capec_attack_relationships(self):
        """Validate CAPEC→ATT&CK relationships"""
        print("\n🔍 Validating CAPEC→ATT&CK Relationships...")

        query = """
        MATCH (capec:AttackPattern)-[r:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE r.source = 'CAPEC_v3.9_XML'
        RETURN count(r) AS count,
               count(DISTINCT capec) AS capec_count,
               count(DISTINCT attack) AS attack_count
        """

        result = self.run_query(query)[0]

        test_result = {
            'test': 'CAPEC→ATT&CK Relationships',
            'expected': 272,
            'actual': result['count'],
            'capec_with_attack': result['capec_count'],
            'unique_attacks': result['attack_count'],
            'passed': result['count'] >= 272
        }

        self.validation_results['tests'].append(test_result)

        if test_result['passed']:
            print(f"✅ CAPEC→ATT&CK: {result['count']} relationships (Expected: 272+)")
            print(f"   CAPECs with ATT&CK: {result['capec_count']}")
            print(f"   Unique ATT&CK Techniques: {result['attack_count']}")
        else:
            print(f"❌ CAPEC→ATT&CK: {result['count']} (Expected: 272+)")

        return test_result['passed']

    def validate_golden_bridge_patterns(self):
        """Validate Golden Bridge patterns (CAPEC with both CWE and ATT&CK)"""
        print("\n🔍 Validating Golden Bridge Patterns...")

        query = """
        MATCH (capec:AttackPattern)-[:EXPLOITS_WEAKNESS]->(cwe:Weakness)
        MATCH (capec)-[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN count(DISTINCT capec) AS golden_bridges
        """

        result = self.run_query(query)[0]

        test_result = {
            'test': 'Golden Bridge Patterns',
            'expected': 143,
            'actual': result['golden_bridges'],
            'passed': result['golden_bridges'] >= 143
        }

        self.validation_results['tests'].append(test_result)

        if test_result['passed']:
            print(f"✅ Golden Bridges: {result['golden_bridges']} patterns (Expected: 143+)")
            print(f"   These patterns enable complete CVE→CWE→CAPEC→ATT&CK chains")
        else:
            print(f"❌ Golden Bridges: {result['golden_bridges']} (Expected: 143+)")

        return test_result['passed']

    def count_complete_chains(self):
        """Count complete CVE→CWE→CAPEC→ATT&CK chains"""
        print("\n🔍 Counting Complete Attack Chains...")

        query = """
        MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
                     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN count(DISTINCT chain) AS complete_chains,
               count(DISTINCT cve) AS cves_with_chains,
               count(DISTINCT capec) AS capecs_in_chains,
               count(DISTINCT attack) AS attacks_reachable
        LIMIT 1
        """

        result = self.run_query(query)[0]

        test_result = {
            'test': 'Complete Attack Chains',
            'expected_min': 500,
            'actual': result['complete_chains'],
            'cves_with_chains': result['cves_with_chains'],
            'capecs_in_chains': result['capecs_in_chains'],
            'attacks_reachable': result['attacks_reachable'],
            'passed': result['complete_chains'] >= 500
        }

        self.validation_results['tests'].append(test_result)

        if test_result['passed']:
            print(f"✅ Complete Chains: {result['complete_chains']:,} (Expected: 500-2,000)")
            print(f"   CVEs with chains: {result['cves_with_chains']:,}")
            print(f"   CAPECs in chains: {result['capecs_in_chains']}")
            print(f"   ATT&CK techniques reachable: {result['attacks_reachable']}")
        else:
            print(f"⚠️  Complete Chains: {result['complete_chains']:,} (Expected: 500-2,000)")
            print(f"   Note: Chain count depends on CVE→CWE relationships")

        return test_result['passed']

    def sample_chains(self, limit: int = 5):
        """Get sample complete chains"""
        print(f"\n📋 Sample Complete Chains (showing {limit})...")

        query = """
        MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
                     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN cve.id AS cve_id,
               cwe.id AS cwe_id,
               capec.id AS capec_id,
               capec.name AS capec_name,
               attack.id AS attack_id,
               attack.name AS attack_name
        LIMIT $limit
        """

        results = self.run_query(query, {'limit': limit})

        for i, chain in enumerate(results, 1):
            print(f"\n{i}. {chain['cve_id']} → {chain['cwe_id']} → {chain['capec_id']} → {chain['attack_id']}")
            print(f"   CAPEC: {chain['capec_name']}")
            print(f"   ATT&CK: {chain['attack_name']}")

        return results

    def generate_summary(self):
        """Generate validation summary"""
        passed = sum(1 for test in self.validation_results['tests'] if test['passed'])
        total = len(self.validation_results['tests'])

        self.validation_results['summary'] = {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'success_rate': f"{(passed/total)*100:.1f}%"
        }

        print("\n" + "="*80)
        print("📊 VALIDATION SUMMARY")
        print("="*80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {self.validation_results['summary']['success_rate']}")

        if passed == total:
            print("\n✅ ALL VALIDATIONS PASSED - CAPEC IMPORT SUCCESSFUL")
        else:
            print(f"\n⚠️  {total - passed} VALIDATION(S) FAILED - REVIEW IMPORT")

        return self.validation_results


def main():
    print("="*80)
    print("🚀 NEO4J CAPEC V3.9 IMPORT VALIDATOR")
    print("="*80)
    print("Purpose: Validate CAPEC import and verify attack chain connectivity\n")

    # Initialize validator
    validator = CAPECImportValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Run validation tests
        validator.validate_capec_nodes()
        validator.validate_capec_cwe_relationships()
        validator.validate_capec_attack_relationships()
        validator.validate_golden_bridge_patterns()
        validator.count_complete_chains()

        # Sample chains
        validator.sample_chains(limit=5)

        # Generate summary
        results = validator.generate_summary()

        # Save results
        output_file = Path('data/capec_analysis/CAPEC_IMPORT_VALIDATION.json')
        output_file.write_text(json.dumps(results, indent=2))
        print(f"\n💾 Validation results saved to: {output_file}")

    finally:
        validator.close()

    print("\n" + "="*80)
    print("✅ VALIDATION COMPLETE")
    print("="*80)


if __name__ == '__main__':
    main()
