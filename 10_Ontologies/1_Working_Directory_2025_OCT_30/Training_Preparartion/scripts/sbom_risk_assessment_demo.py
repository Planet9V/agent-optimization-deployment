#!/usr/bin/env python3
"""
SBOM Risk Assessment Demonstration
Shows practical business value of complete CVE→CWE→CAPEC→ATT&CK chains
"""

from neo4j import GraphDatabase
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

# Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Update with actual password

class SBOMRiskAssessor:
    """Assesses SBOM component risk using complete attack chains"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.assessment_results = {
            'timestamp': datetime.now().isoformat(),
            'sbom_components': [],
            'summary': {}
        }

    def close(self):
        self.driver.close()

    def run_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def create_example_sbom(self) -> List[Dict]:
        """Create example SBOM for demonstration"""
        return [
            {
                'component': 'Apache Log4j',
                'version': '2.14.1',
                'known_cves': ['CVE-2021-44228', 'CVE-2021-45046', 'CVE-2021-45105']
            },
            {
                'component': 'OpenSSL',
                'version': '1.0.1',
                'known_cves': ['CVE-2014-0160']  # Heartbleed
            },
            {
                'component': 'Apache Struts',
                'version': '2.3.31',
                'known_cves': ['CVE-2017-5638']  # Equifax breach
            },
            {
                'component': 'Spring Framework',
                'version': '5.3.0',
                'known_cves': ['CVE-2022-22965']  # Spring4Shell
            }
        ]

    def assess_component_risk(self, component: Dict) -> Dict:
        """Assess risk for a single SBOM component"""
        print(f"\n{'=' * 80}")
        print(f"📦 COMPONENT: {component['component']} v{component['version']}")
        print(f"{'=' * 80}")

        component_risk = {
            'component': component['component'],
            'version': component['version'],
            'cves': [],
            'total_attack_techniques': 0,
            'total_attack_chains': 0,
            'tactics_exposed': set(),
            'critical_findings': []
        }

        for cve_id in component['known_cves']:
            print(f"\n🔍 Analyzing {cve_id}...")

            # Query for complete attack chains
            query = """
            MATCH chain = (cve:CVE {id: $cve_id})
                         -[:HAS_WEAKNESS]->(cwe:Weakness)
                         <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                         -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
            WHERE capec.source = 'CAPEC_v3.9_XML'
            OPTIONAL MATCH (attack)-[:PART_OF_TACTIC]->(tactic:Tactic)
            RETURN
                cve.id AS cve_id,
                cve.description AS cve_description,
                cve.cvss_base_score AS cvss_score,
                cwe.id AS cwe_id,
                cwe.name AS cwe_name,
                capec.id AS capec_id,
                capec.name AS capec_name,
                attack.id AS attack_id,
                attack.name AS attack_name,
                tactic.id AS tactic_id,
                tactic.name AS tactic_name
            """

            results = self.run_query(query, {'cve_id': cve_id})

            if not results:
                print(f"   ⚠️  No complete attack chains found")
                print(f"   ℹ️  This CVE may not have CWE mappings or CAPEC coverage")
                continue

            # Process results
            attack_techniques = {}
            tactics = set()

            for chain in results:
                attack_id = chain['attack_id']
                if attack_id not in attack_techniques:
                    attack_techniques[attack_id] = {
                        'name': chain['attack_name'],
                        'capec_patterns': set(),
                        'cwe_weaknesses': set(),
                        'tactics': set()
                    }

                attack_techniques[attack_id]['capec_patterns'].add(
                    f"{chain['capec_id']}: {chain['capec_name']}"
                )
                attack_techniques[attack_id]['cwe_weaknesses'].add(
                    f"{chain['cwe_id']}: {chain['cwe_name']}"
                )

                if chain.get('tactic_name'):
                    attack_techniques[attack_id]['tactics'].add(chain['tactic_name'])
                    tactics.add(chain['tactic_name'])

            print(f"\n   ✅ {len(results)} complete attack chains found")
            print(f"   🎯 {len(attack_techniques)} unique ATT&CK techniques enabled")
            print(f"   📊 {len(tactics)} MITRE ATT&CK tactics exposed")

            # Display attack techniques
            print(f"\n   📋 ATT&CK Techniques Enabled by {cve_id}:")
            for idx, (attack_id, data) in enumerate(sorted(attack_techniques.items()), 1):
                print(f"\n   {idx}. {attack_id}: {data['name']}")

                if data['tactics']:
                    print(f"      Tactics: {', '.join(sorted(data['tactics']))}")

                print(f"      Via {len(data['capec_patterns'])} attack pattern(s):")
                for capec in sorted(data['capec_patterns']):
                    print(f"         • {capec}")

            component_risk['cves'].append({
                'cve_id': cve_id,
                'cvss_score': results[0].get('cvss_score'),
                'attack_chains': len(results),
                'attack_techniques': list(attack_techniques.keys()),
                'tactics': list(tactics)
            })

            component_risk['total_attack_chains'] += len(results)
            component_risk['total_attack_techniques'] += len(attack_techniques)
            component_risk['tactics_exposed'].update(tactics)

        # Risk scoring
        component_risk['tactics_exposed'] = list(component_risk['tactics_exposed'])
        component_risk['risk_score'] = self.calculate_risk_score(component_risk)

        return component_risk

    def calculate_risk_score(self, component_risk: Dict) -> str:
        """Calculate overall risk score for component"""
        chains = component_risk['total_attack_chains']
        techniques = component_risk['total_attack_techniques']
        tactics = len(component_risk['tactics_exposed'])

        # Simple scoring logic
        if chains > 10 and techniques > 5:
            return "🔴 CRITICAL"
        elif chains > 5 and techniques > 3:
            return "🟠 HIGH"
        elif chains > 2:
            return "🟡 MEDIUM"
        elif chains > 0:
            return "🟢 LOW"
        else:
            return "⚪ NO CHAINS"

    def generate_comprehensive_report(self, components: List[Dict]):
        """Generate comprehensive SBOM risk report"""
        print("\n\n" + "=" * 80)
        print("📊 COMPREHENSIVE SBOM RISK ASSESSMENT REPORT")
        print("=" * 80)

        # Aggregate statistics
        total_chains = sum(c['total_attack_chains'] for c in components)
        total_techniques = sum(c['total_attack_techniques'] for c in components)
        all_tactics = set()
        for c in components:
            all_tactics.update(c['tactics_exposed'])

        print(f"\n📈 AGGREGATE STATISTICS:")
        print(f"   • Total Components Analyzed: {len(components)}")
        print(f"   • Total Attack Chains: {total_chains}")
        print(f"   • Unique ATT&CK Techniques: {total_techniques}")
        print(f"   • ATT&CK Tactics Exposed: {len(all_tactics)}")

        print(f"\n\n🎯 COMPONENT RISK SUMMARY:")
        print(f"{'=' * 80}")

        for component in sorted(components, key=lambda x: x['total_attack_chains'], reverse=True):
            print(f"\n{component['risk_score']} {component['component']} v{component['version']}")
            print(f"   └─ {component['total_attack_chains']} attack chains")
            print(f"   └─ {component['total_attack_techniques']} ATT&CK techniques")
            print(f"   └─ {len(component['tactics_exposed'])} tactics: {', '.join(sorted(component['tactics_exposed']))}")

            for cve in component['cves']:
                print(f"      • {cve['cve_id']}: {cve['attack_chains']} chains → {len(cve['attack_techniques'])} techniques")

        print(f"\n\n🔍 MITRE ATT&CK TACTICS COVERAGE:")
        print(f"{'=' * 80}")

        # Tactics analysis
        tactics_coverage = defaultdict(set)
        for component in components:
            for cve_info in component['cves']:
                for tactic in cve_info.get('tactics', []):
                    tactics_coverage[tactic].add(component['component'])

        for idx, (tactic, components_set) in enumerate(sorted(tactics_coverage.items()), 1):
            print(f"\n{idx}. {tactic}")
            print(f"   Affected Components: {', '.join(sorted(components_set))}")

        print(f"\n\n💡 KEY FINDINGS:")
        print(f"{'=' * 80}")

        # Critical findings
        critical_components = [c for c in components if c['risk_score'] == "🔴 CRITICAL"]
        if critical_components:
            print(f"\n🔴 CRITICAL RISK COMPONENTS:")
            for comp in critical_components:
                print(f"   • {comp['component']} - {comp['total_attack_techniques']} attack techniques enabled")

        high_risk = [c for c in components if c['risk_score'] == "🟠 HIGH"]
        if high_risk:
            print(f"\n🟠 HIGH RISK COMPONENTS:")
            for comp in high_risk:
                print(f"   • {comp['component']} - {comp['total_attack_techniques']} attack techniques enabled")

        # Most exposed tactics
        if tactics_coverage:
            most_exposed = max(tactics_coverage.items(), key=lambda x: len(x[1]))
            print(f"\n⚠️  MOST EXPOSED TACTIC:")
            print(f"   {most_exposed[0]} - affects {len(most_exposed[1])} component(s)")

        print(f"\n\n📋 RECOMMENDATIONS:")
        print(f"{'=' * 80}")
        print(f"1. Prioritize patching components with CRITICAL or HIGH risk scores")
        print(f"2. Implement detection controls for exposed ATT&CK techniques")
        print(f"3. Review security controls for tactics with multiple affected components")
        print(f"4. Consider alternative components with lower attack surface")
        print(f"5. Deploy monitoring for CAPEC attack patterns targeting your stack")

        # Save results
        self.assessment_results['sbom_components'] = components
        self.assessment_results['summary'] = {
            'total_components': len(components),
            'total_attack_chains': total_chains,
            'unique_attack_techniques': total_techniques,
            'exposed_tactics': list(all_tactics),
            'critical_components': len(critical_components),
            'high_risk_components': len(high_risk)
        }

        output_file = Path('data/capec_analysis/SBOM_RISK_ASSESSMENT.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(json.dumps(self.assessment_results, indent=2, default=str))
        print(f"\n💾 Risk assessment saved to: {output_file}")

    def demonstrate_single_chain_detail(self, cve_id: str = 'CVE-2021-44228'):
        """Show detailed breakdown of a single CVE attack chain"""
        print(f"\n\n" + "=" * 80)
        print(f"🔬 DETAILED CHAIN ANALYSIS: {cve_id}")
        print("=" * 80)

        query = """
        MATCH chain = (cve:CVE {id: $cve_id})
                     -[:HAS_WEAKNESS]->(cwe:Weakness)
                     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
                     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
        WHERE capec.source = 'CAPEC_v3.9_XML'
        RETURN
            cve.id AS cve_id,
            cve.description AS cve_desc,
            cwe.id AS cwe_id,
            cwe.name AS cwe_name,
            capec.id AS capec_id,
            capec.name AS capec_name,
            attack.id AS attack_id,
            attack.name AS attack_name
        LIMIT 1
        """

        results = self.run_query(query, {'cve_id': cve_id})

        if results:
            chain = results[0]
            print(f"\n1️⃣  CVE: {chain['cve_id']}")
            print(f"    └─ {chain['cve_desc'][:150]}...")
            print(f"\n         ⬇️  HAS_WEAKNESS")
            print(f"\n2️⃣  CWE: {chain['cwe_id']} - {chain['cwe_name']}")
            print(f"\n         ⬆️  EXPLOITS_WEAKNESS")
            print(f"\n3️⃣  CAPEC: {chain['capec_id']} - {chain['capec_name']}")
            print(f"\n         ⬇️  IMPLEMENTS_TECHNIQUE")
            print(f"\n4️⃣  ATT&CK: {chain['attack_id']} - {chain['attack_name']}")
            print(f"\n✅ Complete chain demonstrates semantic attack path")


def main():
    print("=" * 80)
    print("🚀 SBOM RISK ASSESSMENT DEMONSTRATION")
    print("=" * 80)
    print("Purpose: Demonstrate business value of complete attack chains")
    print("Use Case: SBOM component risk assessment with ATT&CK technique mapping\n")

    assessor = SBOMRiskAssessor(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Create example SBOM
        print("📦 Loading example SBOM components...")
        sbom_components = assessor.create_example_sbom()
        print(f"   ✅ {len(sbom_components)} components loaded\n")

        # Assess each component
        component_risks = []
        for component in sbom_components:
            risk_assessment = assessor.assess_component_risk(component)
            component_risks.append(risk_assessment)

        # Generate comprehensive report
        assessor.generate_comprehensive_report(component_risks)

        # Show detailed chain example
        assessor.demonstrate_single_chain_detail('CVE-2021-44228')

        print("\n" + "=" * 80)
        print("✅ SBOM RISK ASSESSMENT COMPLETE")
        print("=" * 80)
        print("\n💡 BUSINESS VALUE DEMONSTRATED:")
        print("   • CVE vulnerabilities mapped to ATT&CK techniques")
        print("   • Attack surface quantified per SBOM component")
        print("   • Risk prioritization based on attack chain analysis")
        print("   • Security control recommendations for exposed tactics")

    finally:
        assessor.close()


if __name__ == '__main__':
    main()
