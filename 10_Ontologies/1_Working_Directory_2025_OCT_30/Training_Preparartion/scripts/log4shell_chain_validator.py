#!/usr/bin/env python3
"""
Log4Shell (CVE-2021-44228) Attack Chain Validator
Demonstrates complete CVE→CWE→CAPEC→ATT&CK path traversal after CAPEC v3.9 import
"""

from neo4j import GraphDatabase
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Update with actual password

class Log4ShellChainValidator:
    """Validates complete attack chains for CVE-2021-44228 (Log4Shell)"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'cve_id': 'CVE-2021-44228',
            'cve_name': 'Log4Shell - Apache Log4j2 Remote Code Execution',
            'chains': [],
            'summary': {}
        }

    def close(self):
        self.driver.close()

    def run_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def find_log4shell_complete_chains(self):
        """Find all complete attack chains for Log4Shell"""
        print("\n🔍 Searching for Log4Shell Complete Attack Chains...")
        print("=" * 80)

        query = """
        MATCH chain = (cve:CVE {id: 'CVE-2021-44228'})
                     -[:HAS_WEAKNESS]->(cwe:Weakness)
                     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN
            cve.id AS cve_id,
            cve.description AS cve_description,
            cwe.id AS cwe_id,
            cwe.name AS cwe_name,
            capec.id AS capec_id,
            capec.name AS capec_name,
            capec.abstraction AS capec_abstraction,
            attack.id AS attack_id,
            attack.name AS attack_name
        """

        results = self.run_query(query)

        if not results:
            print("❌ NO COMPLETE CHAINS FOUND")
            print("   This means CAPEC v3.9 data has not been imported yet.")
            print("   Run: cypher-shell < data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher")
            return False

        print(f"✅ FOUND {len(results)} COMPLETE ATTACK CHAINS")
        print("\n📊 Log4Shell Attack Chain Analysis:")
        print("=" * 80)

        # Group by ATT&CK technique
        attack_techniques = {}
        for chain in results:
            attack_id = chain['attack_id']
            if attack_id not in attack_techniques:
                attack_techniques[attack_id] = {
                    'name': chain['attack_name'],
                    'capec_patterns': [],
                    'cwe_weaknesses': set()
                }

            attack_techniques[attack_id]['capec_patterns'].append({
                'capec_id': chain['capec_id'],
                'capec_name': chain['capec_name'],
                'abstraction': chain['capec_abstraction']
            })
            attack_techniques[attack_id]['cwe_weaknesses'].add(
                f"{chain['cwe_id']}: {chain['cwe_name']}"
            )

            self.validation_results['chains'].append(chain)

        # Display results
        print(f"\n🎯 CVE-2021-44228 enables {len(attack_techniques)} distinct ATT&CK techniques:\n")

        for idx, (attack_id, data) in enumerate(attack_techniques.items(), 1):
            print(f"{idx}. {attack_id}: {data['name']}")
            print(f"   └─ via {len(data['capec_patterns'])} CAPEC patterns:")

            for capec in data['capec_patterns']:
                print(f"      • {capec['capec_id']}: {capec['capec_name']} ({capec['abstraction']})")

            print(f"   └─ exploiting {len(data['cwe_weaknesses'])} CWE weaknesses:")
            for cwe in sorted(data['cwe_weaknesses']):
                print(f"      • {cwe}")
            print()

        # Validate expected techniques
        print("\n🔬 VALIDATION CHECK: Expected ATT&CK Techniques")
        print("=" * 80)

        expected_techniques = {
            'T1190': 'Exploit Public-Facing Application',
            'T1059': 'Command and Scripting Interpreter',
            'T1203': 'Exploitation for Client Execution'
        }

        found_expected = {tid: tid in attack_techniques for tid in expected_techniques}

        for tid, name in expected_techniques.items():
            status = "✅ FOUND" if found_expected[tid] else "❌ NOT FOUND"
            print(f"{status} - {tid}: {name}")

        all_found = all(found_expected.values())

        if all_found:
            print("\n✅ ALL EXPECTED TECHNIQUES VALIDATED")
        else:
            print(f"\n⚠️  {sum(not v for v in found_expected.values())} expected techniques missing")

        self.validation_results['summary'] = {
            'total_chains': len(results),
            'unique_attack_techniques': len(attack_techniques),
            'expected_techniques_found': sum(found_expected.values()),
            'validation_passed': all_found
        }

        return all_found

    def trace_specific_chain(self, capec_id: str = None):
        """Trace a specific CAPEC pattern chain in detail"""
        print(f"\n🔬 DETAILED CHAIN TRACE: {capec_id or 'First Available Chain'}")
        print("=" * 80)

        query = """
        MATCH chain = (cve:CVE {id: 'CVE-2021-44228'})
                     -[:HAS_WEAKNESS]->(cwe:Weakness)
                     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        """

        if capec_id:
            query += f"\nWHERE capec.id = '{capec_id}' AND capec.source = 'CAPEC_v3.9_XML'"
        else:
            query += "\nWHERE capec.source = 'CAPEC_v3.9_XML'\nLIMIT 1"

        query += """
        RETURN
            cve.id AS cve_id,
            cve.description AS cve_description,
            cve.cvss_base_score AS cvss_score,
            cwe.id AS cwe_id,
            cwe.name AS cwe_name,
            cwe.description AS cwe_description,
            capec.id AS capec_id,
            capec.name AS capec_name,
            capec.abstraction AS abstraction,
            capec.description AS capec_description,
            attack.id AS attack_id,
            attack.name AS attack_name
        """

        results = self.run_query(query)

        if not results:
            print("❌ No chain found")
            return

        chain = results[0]

        print(f"\n1️⃣  CVE (Vulnerability)")
        print(f"    ID: {chain['cve_id']}")
        print(f"    CVSS: {chain.get('cvss_score', 'N/A')}")
        print(f"    Description: {chain['cve_description'][:200]}...")

        print(f"\n    ⬇️  HAS_WEAKNESS")

        print(f"\n2️⃣  CWE (Weakness)")
        print(f"    ID: {chain['cwe_id']}")
        print(f"    Name: {chain['cwe_name']}")
        if chain.get('cwe_description'):
            print(f"    Description: {chain['cwe_description'][:200]}...")

        print(f"\n    ⬆️  EXPLOITS_WEAKNESS")

        print(f"\n3️⃣  CAPEC (Attack Pattern)")
        print(f"    ID: {chain['capec_id']}")
        print(f"    Name: {chain['capec_name']}")
        print(f"    Abstraction: {chain['abstraction']}")
        if chain.get('capec_description'):
            print(f"    Description: {chain['capec_description'][:200]}...")

        print(f"\n    ⬇️  IMPLEMENTS_TECHNIQUE")

        print(f"\n4️⃣  ATT&CK (Technique)")
        print(f"    ID: {chain['attack_id']}")
        print(f"    Name: {chain['attack_name']}")

        print("\n✅ COMPLETE CHAIN VALIDATED")

    def analyze_attack_surface(self):
        """Analyze the attack surface enabled by Log4Shell"""
        print("\n📊 ATTACK SURFACE ANALYSIS")
        print("=" * 80)

        # Get tactics distribution
        query = """
        MATCH (cve:CVE {id: 'CVE-2021-44228'})
             -[:HAS_WEAKNESS]->(cwe:Weakness)
             <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
             -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
             -[:PART_OF_TACTIC]->(tactic:Tactic)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN
            tactic.id AS tactic_id,
            tactic.name AS tactic_name,
            count(DISTINCT attack) AS techniques_count,
            collect(DISTINCT attack.id) AS techniques
        ORDER BY techniques_count DESC
        """

        results = self.run_query(query)

        if results:
            print("\n🎯 MITRE ATT&CK Tactics Coverage:\n")
            for idx, tactic in enumerate(results, 1):
                print(f"{idx}. {tactic['tactic_name']} ({tactic['tactic_id']})")
                print(f"   └─ {tactic['techniques_count']} technique(s): {', '.join(tactic['techniques'])}")
                print()
        else:
            print("⚠️  No tactic information available (ATT&CK tactics not in database)")

        # Get CWE weakness types
        query = """
        MATCH (cve:CVE {id: 'CVE-2021-44228'})
             -[:HAS_WEAKNESS]->(cwe:Weakness)
        RETURN
            cwe.id AS cwe_id,
            cwe.name AS cwe_name,
            cwe.weakness_abstraction AS abstraction
        """

        results = self.run_query(query)

        if results:
            print("\n🛡️  Underlying CWE Weaknesses:\n")
            for idx, cwe in enumerate(results, 1):
                print(f"{idx}. {cwe['cwe_id']}: {cwe['cwe_name']}")
                if cwe.get('abstraction'):
                    print(f"   Abstraction: {cwe['abstraction']}")
                print()

    def generate_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "=" * 80)
        print("📋 LOG4SHELL CHAIN VALIDATION REPORT")
        print("=" * 80)

        summary = self.validation_results['summary']

        print(f"\nTimestamp: {self.validation_results['timestamp']}")
        print(f"CVE: {self.validation_results['cve_id']}")
        print(f"CVE Name: {self.validation_results['cve_name']}")

        print(f"\n📊 Results:")
        print(f"  • Complete Chains Found: {summary.get('total_chains', 0)}")
        print(f"  • Unique ATT&CK Techniques: {summary.get('unique_attack_techniques', 0)}")
        print(f"  • Expected Techniques Found: {summary.get('expected_techniques_found', 0)}/3")
        print(f"  • Validation Status: {'✅ PASSED' if summary.get('validation_passed') else '❌ FAILED'}")

        # Save results
        output_file = Path('data/capec_analysis/LOG4SHELL_CHAIN_VALIDATION.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(json.dumps(self.validation_results, indent=2))
        print(f"\n💾 Validation results saved to: {output_file}")

        return summary.get('validation_passed', False)


def main():
    print("=" * 80)
    print("🚀 LOG4SHELL (CVE-2021-44228) ATTACK CHAIN VALIDATOR")
    print("=" * 80)
    print("Purpose: Demonstrate complete CVE→CWE→CAPEC→ATT&CK path")
    print("Expected: Multiple complete chains after CAPEC v3.9 import\n")

    validator = Log4ShellChainValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Find all complete chains
        chains_found = validator.find_log4shell_complete_chains()

        if chains_found:
            # Trace detailed example
            validator.trace_specific_chain()

            # Analyze attack surface
            validator.analyze_attack_surface()

        # Generate final report
        validation_passed = validator.generate_report()

        print("\n" + "=" * 80)
        if validation_passed:
            print("✅ VALIDATION COMPLETE - CAPEC IMPORT SUCCESSFUL")
            print("   Log4Shell demonstrates complete attack chain traversal")
        else:
            print("⚠️  VALIDATION INCOMPLETE - IMPORT CAPEC v3.9 DATA")
            print("   Run: cypher-shell < data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher")
        print("=" * 80)

    finally:
        validator.close()


if __name__ == '__main__':
    main()
