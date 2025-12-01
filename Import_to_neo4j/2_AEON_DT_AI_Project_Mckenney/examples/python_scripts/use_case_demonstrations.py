"""
Cyber Digital Twin - Use Case Demonstrations

Complete working examples for all 7 use cases with Neo4j integration.
Shows query construction, result processing, and visualization preparation.

Author: Cyber Digital Twin Project
Date: 2025-10-29
"""

from neo4j import GraphDatabase
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ConnectionConfig:
    """Neo4j connection configuration"""
    uri: str = "bolt://localhost:7687"
    username: str = "neo4j"
    password: str = "password"


class CyberDigitalTwinDemo:
    """Demonstrates all 7 use cases for Cyber Digital Twin"""

    def __init__(self, config: ConnectionConfig):
        """Initialize Neo4j driver"""
        self.driver = GraphDatabase.driver(
            config.uri,
            auth=(config.username, config.password)
        )

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    # ========================================================================
    # USE CASE 1: Find vulnerabilities in a specific asset
    # ========================================================================

    def use_case_1_brake_controller_vulnerabilities(self):
        """
        Use Case 1: Find all vulnerabilities in brake controller

        Returns:
            Dict with vulnerability details organized by device
        """
        query = """
        MATCH (comp:HardwareComponent {name: 'Brake Controller'})
          -[:INSTALLED_IN]->(device:Device)
          -[:RUNS_FIRMWARE]->(fw:Firmware)
          -[:HAS_VULNERABILITY]->(cve:CVE)
          -[:HAS_CVSS]->(cvss:CVSSScore)

        OPTIONAL MATCH (cve)-[:CAUSED_BY]->(cwe:CWE)
        OPTIONAL MATCH (cve)-[:HAS_EXPLOIT]->(exploit:Exploit)

        RETURN
          device.name AS device_name,
          fw.version AS firmware_version,
          cve.cveId AS cve_id,
          cvss.score AS cvss_score,
          cvss.severity AS severity,
          cwe.id AS cwe_id,
          CASE WHEN exploit IS NOT NULL THEN 'Yes' ELSE 'No' END AS has_exploit

        ORDER BY cvss.score DESC
        LIMIT 100
        """

        with self.driver.session() as session:
            results = session.run(query)
            vulnerabilities = []

            for record in results:
                vulnerability = {
                    'device': record['device_name'],
                    'firmware_version': record['firmware_version'],
                    'cve_id': record['cve_id'],
                    'cvss_score': record['cvss_score'],
                    'severity': record['severity'],
                    'weakness_id': record['cwe_id'],
                    'exploited': record['has_exploit'] == 'Yes'
                }
                vulnerabilities.append(vulnerability)

            return {
                'use_case': 'Brake Controller Vulnerabilities',
                'total_vulnerabilities': len(vulnerabilities),
                'critical_count': sum(1 for v in vulnerabilities if v['severity'] == 'CRITICAL'),
                'high_count': sum(1 for v in vulnerabilities if v['severity'] == 'HIGH'),
                'has_exploits': sum(1 for v in vulnerabilities if v['exploited']),
                'vulnerabilities': vulnerabilities
            }

    # ========================================================================
    # USE CASE 2: Critical vulnerabilities due within 30 days
    # ========================================================================

    def use_case_2_critical_vulnerabilities_by_deadline(self):
        """
        Use Case 2: Find critical vulnerabilities with near-term remediation deadlines

        Returns:
            Sorted list of critical vulnerabilities by urgency
        """
        query = """
        MATCH (cve:CVE)
          -[:HAS_CVSS]->(cvss:CVSSScore)

        WHERE cvss.score >= 9.0
          AND cve.remediationDeadline <= datetime.now() + duration({days: 30})

        OPTIONAL MATCH (cve)-[:AFFECTS]->(product:SoftwareProduct)
        OPTIONAL MATCH (product)-[:INSTALLED_IN]->(fleet:Fleet)

        RETURN
          cve.cveId AS cve_id,
          cvss.score AS cvss_score,
          cve.remediationDeadline AS deadline,
          COUNT(DISTINCT product) AS affected_products,
          COUNT(DISTINCT fleet) AS affected_fleets,
          duration.inDays(datetime.now(), cve.remediationDeadline).days AS days_until_deadline

        ORDER BY days_until_deadline ASC
        """

        with self.driver.session() as session:
            results = session.run(query)
            critical_vulns = []

            for record in results:
                vuln = {
                    'cve_id': record['cve_id'],
                    'cvss_score': record['cvss_score'],
                    'deadline': record['deadline'],
                    'affected_products': record['affected_products'],
                    'affected_fleets': record['affected_fleets'],
                    'days_remaining': record['days_until_deadline'],
                    'urgency': 'IMMEDIATE' if record['days_until_deadline'] <= 7 else 'HIGH'
                }
                critical_vulns.append(vuln)

            return {
                'use_case': 'Critical Vulnerabilities by Deadline',
                'total_critical': len(critical_vulns),
                'immediate_action': sum(1 for v in critical_vulns if v['urgency'] == 'IMMEDIATE'),
                'vulnerabilities': critical_vulns
            }

    # ========================================================================
    # USE CASE 3: Attack path analysis
    # ========================================================================

    def use_case_3_attack_path_analysis(self):
        """
        Use Case 3: Determine attack paths from external to SCADA systems

        Returns:
            Shortest attack paths with hop counts
        """
        query = """
        MATCH path = (external:NetworkZone {name: 'EXTERNAL'})
          -[*1..8]-(scada:Device {zone: 'SCADA'})

        WITH
          path,
          length(path) AS hop_count,
          [n IN nodes(path) | n.name] AS node_names

        RETURN
          node_names AS attack_chain,
          hop_count AS hops,
          reduce(risk = 0, n IN nodes(path) | risk + COALESCE(n.vulnerability_score, 0)) AS path_risk

        ORDER BY hop_count ASC
        LIMIT 20
        """

        with self.driver.session() as session:
            results = session.run(query)
            attack_paths = []

            for record in results:
                path = {
                    'chain': record['attack_chain'],
                    'hops': record['hops'],
                    'risk_score': record['path_risk'],
                    'risk_level': 'CRITICAL' if record['path_risk'] >= 50 else 'HIGH'
                }
                attack_paths.append(path)

            return {
                'use_case': 'Attack Path Analysis',
                'total_paths_found': len(attack_paths),
                'shortest_path_hops': min((p['hops'] for p in attack_paths), default=None),
                'critical_paths': sum(1 for p in attack_paths if p['risk_level'] == 'CRITICAL'),
                'attack_paths': attack_paths
            }

    # ========================================================================
    # USE CASE 4: Threat actor correlation
    # ========================================================================

    def use_case_4_threat_actor_correlation(self, sector: str = 'Energy'):
        """
        Use Case 4: Correlate threat actors to CVEs in target sector

        Args:
            sector: Target industry sector (default: 'Energy')

        Returns:
            Threat actors ranked by activity in sector
        """
        query = """
        MATCH (ta:ThreatActor)
          -[:EXPLOITS]->(cve:CVE)
          -[:AFFECTS]->(product:SoftwareProduct)
          -[:USED_IN_SECTOR]->(s:Sector {name: $sector})

        OPTIONAL MATCH (cve)-[:HAS_CVSS]->(cvss:CVSSScore)

        WITH
          ta.name AS actor_name,
          COUNT(DISTINCT cve) AS cve_count,
          AVG(cvss.score) AS avg_severity,
          MAX(cvss.score) AS max_severity

        RETURN
          actor_name,
          cve_count,
          ROUND(avg_severity, 2) AS average_severity,
          ROUND(max_severity, 2) AS maximum_severity,
          CASE
            WHEN cve_count >= 100 THEN 'ADVANCED'
            WHEN cve_count >= 50 THEN 'SOPHISTICATED'
            ELSE 'MODERATE'
          END AS threat_level

        ORDER BY cve_count DESC
        """

        with self.driver.session() as session:
            results = session.run(query, sector=sector)
            threat_actors = []

            for record in results:
                actor = {
                    'name': record['actor_name'],
                    'exploits_in_sector': record['cve_count'],
                    'average_severity': record['average_severity'],
                    'maximum_severity': record['maximum_severity'],
                    'threat_level': record['threat_level']
                }
                threat_actors.append(actor)

            return {
                'use_case': f'Threat Actor Correlation - {sector}',
                'total_actors': len(threat_actors),
                'advanced_threat_actors': sum(1 for a in threat_actors if a['threat_level'] == 'ADVANCED'),
                'threat_actors': threat_actors
            }

    # ========================================================================
    # USE CASE 5: Vulnerability explosion analysis
    # ========================================================================

    def use_case_5_vulnerability_explosion(self, cve_id: str = 'CVE-2024-1234'):
        """
        Use Case 5: Analyze how one CVE cascades through the fleet

        Args:
            cve_id: CVE ID to analyze

        Returns:
            Blast radius and affected asset counts
        """
        query = """
        MATCH (cve:CVE {cveId: $cve_id})
          <-[:HAS_VULNERABILITY]-(fw:Firmware)
          <-[:RUNS_FIRMWARE]-(device:Device)
          <-[:CONTAINS*1..3]-(fleet:Fleet)

        WITH
          cve.cveId AS cve_id,
          COUNT(DISTINCT fw) AS firmware_versions,
          COUNT(DISTINCT device) AS devices_affected,
          COUNT(DISTINCT fleet) AS fleets_affected

        RETURN
          cve_id,
          firmware_versions,
          devices_affected,
          fleets_affected,
          devices_affected * fleets_affected AS blast_radius
        """

        with self.driver.session() as session:
            results = session.run(query, cve_id=cve_id)

            for record in results:
                return {
                    'use_case': 'Vulnerability Explosion Analysis',
                    'cve_id': record['cve_id'],
                    'firmware_versions_affected': record['firmware_versions'],
                    'total_devices_affected': record['devices_affected'],
                    'total_fleets_affected': record['fleets_affected'],
                    'blast_radius': record['blast_radius'],
                    'impact_level': 'CRITICAL' if record['blast_radius'] > 1000 else 'HIGH'
                }

    # ========================================================================
    # USE CASE 6: SEVD Prioritization (Now/Next/Never)
    # ========================================================================

    def use_case_6_sevd_prioritization(self):
        """
        Use Case 6: Prioritize vulnerabilities using SEVD methodology

        Returns:
            Vulnerabilities classified as Now/Next/Never
        """
        query = """
        MATCH (cve:CVE)
          -[:HAS_CVSS]->(cvss:CVSSScore)

        OPTIONAL MATCH (cve)-[:HAS_EXPLOIT]-(exploit:Exploit)
        OPTIONAL MATCH (cve)-[:AFFECTS]->(product:SoftwareProduct)
          -[:INSTALLED_IN]->(device:Device)

        WITH
          cve.cveId AS cve_id,
          cvss.score AS cvss_score,
          CASE WHEN exploit IS NOT NULL THEN true ELSE false END AS is_exploited,
          COUNT(DISTINCT device) AS devices_affected,
          CASE
            WHEN cvss.score >= 9.0 AND exploit IS NOT NULL THEN 'NOW'
            WHEN cvss.score >= 7.0 THEN 'NEXT'
            ELSE 'NEVER'
          END AS priority

        RETURN
          priority,
          COUNT(cve_id) AS count,
          AVG(cvss_score) AS avg_severity,
          SUM(devices_affected) AS total_devices_affected

        ORDER BY
          CASE WHEN priority = 'NOW' THEN 0 WHEN priority = 'NEXT' THEN 1 ELSE 2 END
        """

        with self.driver.session() as session:
            results = session.run(query)
            prioritization = {}

            for record in results:
                prioritization[record['priority']] = {
                    'count': record['count'],
                    'average_severity': round(record['avg_severity'], 2),
                    'total_devices_affected': record['total_devices_affected']
                }

            return {
                'use_case': 'SEVD Prioritization',
                'prioritization': prioritization,
                'total_vulnerabilities': sum(v['count'] for v in prioritization.values())
            }

    # ========================================================================
    # USE CASE 7: Compliance mapping
    # ========================================================================

    def use_case_7_compliance_mapping(self, framework: str = 'IEC 62443'):
        """
        Use Case 7: Map vulnerabilities to compliance framework requirements

        Args:
            framework: Compliance framework name

        Returns:
            CVEs mapped to compliance requirements with gaps
        """
        query = """
        MATCH (cve:CVE)
          -[:MAPS_TO]->(cwe:CWE)
          -[:COVERED_BY]->(cf:ComplianceFramework {name: $framework})

        WITH
          cve.cveId AS cve_id,
          COUNT(DISTINCT cf.requirement) AS requirements_covered

        RETURN
          cve_id,
          requirements_covered

        UNION

        MATCH (framework:ComplianceFramework {name: $framework})

        RETURN
          'Total Requirements' AS cve_id,
          COUNT(framework.requirement) AS requirements_covered
        """

        with self.driver.session() as session:
            results = session.run(query, framework=framework)
            coverage = {'covered': [], 'total': 0}

            for record in results:
                if record['cve_id'] == 'Total Requirements':
                    coverage['total'] = record['requirements_covered']
                else:
                    coverage['covered'].append({
                        'cve': record['cve_id'],
                        'requirements': record['requirements_covered']
                    })

            return {
                'use_case': f'Compliance Mapping - {framework}',
                'framework': framework,
                'total_requirements': coverage['total'],
                'mapped_cves': len(coverage['covered']),
                'compliance_gap': coverage['total'] - sum(
                    c['requirements'] for c in coverage['covered']
                ),
                'coverage_percent': round(
                    sum(c['requirements'] for c in coverage['covered']) / coverage['total'] * 100,
                    2
                ) if coverage['total'] > 0 else 0
            }


# ============================================================================
# Main demonstration
# ============================================================================

def demonstrate_all_use_cases():
    """Run all 7 use case demonstrations"""
    config = ConnectionConfig(
        uri="bolt://localhost:7687",
        username="neo4j",
        password="your_password"
    )

    demo = CyberDigitalTwinDemo(config)

    try:
        # Run all use cases
        results = {
            'use_case_1': demo.use_case_1_brake_controller_vulnerabilities(),
            'use_case_2': demo.use_case_2_critical_vulnerabilities_by_deadline(),
            'use_case_3': demo.use_case_3_attack_path_analysis(),
            'use_case_4': demo.use_case_4_threat_actor_correlation('Energy'),
            'use_case_5': demo.use_case_5_vulnerability_explosion('CVE-2024-1234'),
            'use_case_6': demo.use_case_6_sevd_prioritization(),
            'use_case_7': demo.use_case_7_compliance_mapping('IEC 62443')
        }

        # Output results
        print(json.dumps(results, indent=2, default=str))

        return results

    finally:
        demo.close()


if __name__ == '__main__':
    # Run demonstrations
    results = demonstrate_all_use_cases()

    # Print summary
    print("\n" + "="*80)
    print("CYBER DIGITAL TWIN - USE CASE DEMONSTRATION SUMMARY")
    print("="*80)

    for use_case, data in results.items():
        print(f"\n{use_case}: {data.get('use_case', 'Unknown')}")
        print(f"  Status: Results obtained")
        if 'total_vulnerabilities' in data:
            print(f"  Total items: {data['total_vulnerabilities']}")
