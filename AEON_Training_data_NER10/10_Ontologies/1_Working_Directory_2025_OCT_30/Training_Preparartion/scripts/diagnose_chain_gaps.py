#!/usr/bin/env python3
"""
Diagnostic Script: Attack Chain Gap Analysis
Identifies why complete CVE→CWE→CAPEC→ATT&CK chains don't exist

Author: Testing Agent
Created: 2025-11-07
Purpose: Diagnose data quality issues preventing complete attack chains
"""

import os
from neo4j import GraphDatabase
from typing import Dict, List


class ChainGapDiagnostic:
    """Diagnoses gaps preventing complete attack chains"""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close database connection"""
        self.driver.close()

    def get_cwe_samples(self) -> Dict:
        """Get sample CWEs from both sets for manual inspection"""
        query = """
        // Get CWEs with CVEs
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
        WITH collect(DISTINCT cwe.id) as cve_cwe_ids

        // Get CWEs with CAPECs
        MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH cve_cwe_ids, collect(DISTINCT cwe2.id) as capec_cwe_ids

        RETURN
            cve_cwe_ids[0..10] as sample_cve_cwes,
            capec_cwe_ids[0..10] as sample_capec_cwes
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            return {
                'cve_cwes': record['sample_cve_cwes'],
                'capec_cwes': record['sample_capec_cwes']
            }

    def check_cwe_hierarchy_bridges(self) -> Dict:
        """Check if CWE parent-child relationships could bridge the gap"""
        query = """
        // Get CWEs with CVEs
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
        WITH collect(DISTINCT cwe1) as cve_cwes

        // Get CWEs with CAPECs
        MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH cve_cwes, collect(DISTINCT cwe2) as capec_cwes

        // Check for parent-child relationships
        UNWIND cve_cwes as cve_cwe
        UNWIND capec_cwes as capec_cwe
        MATCH path = (cve_cwe)-[:CHILDOF*1..3]-(capec_cwe)

        RETURN
            count(DISTINCT cve_cwe) as cve_cwes_with_hierarchy,
            count(DISTINCT capec_cwe) as capec_cwes_with_hierarchy,
            count(path) as total_hierarchy_paths,
            min(length(path)) as min_hops,
            max(length(path)) as max_hops
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            if record is None or record['total_hierarchy_paths'] == 0:
                return {
                    'hierarchy_exists': False,
                    'potential_bridges': 0
                }

            return {
                'hierarchy_exists': True,
                'cve_cwes_with_hierarchy': record['cve_cwes_with_hierarchy'],
                'capec_cwes_with_hierarchy': record['capec_cwes_with_hierarchy'],
                'total_paths': record['total_hierarchy_paths'],
                'min_hops': record['min_hops'],
                'max_hops': record['max_hops']
            }

    def analyze_cwe_id_patterns(self) -> Dict:
        """Analyze CWE ID patterns to identify systematic differences"""
        query = """
        // Get CWE IDs with CVEs
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
        WITH cwe.id as id
        WITH split(id, '-')[1] as num_str
        WITH toInteger(num_str) as cwe_num
        WHERE cwe_num IS NOT NULL
        WITH collect(cwe_num) as cve_cwe_nums

        // Get CWE IDs with CAPECs
        MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH cve_cwe_nums, cwe2.id as id
        WITH cve_cwe_nums, split(id, '-')[1] as num_str
        WITH cve_cwe_nums, toInteger(num_str) as capec_cwe_num
        WHERE capec_cwe_num IS NOT NULL
        WITH cve_cwe_nums, collect(capec_cwe_num) as capec_cwe_nums

        // Analyze ranges
        RETURN
            min(cve_cwe_nums) as cve_min,
            max(cve_cwe_nums) as cve_max,
            avg(cve_cwe_nums) as cve_avg,
            min(capec_cwe_nums) as capec_min,
            max(capec_cwe_nums) as capec_max,
            avg(capec_cwe_nums) as capec_avg
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            return {
                'cve_range': (record['cve_min'], record['cve_max']),
                'cve_avg': record['cve_avg'],
                'capec_range': (record['capec_min'], record['capec_max']),
                'capec_avg': record['capec_avg']
            }

    def find_closest_matches(self) -> List[Dict]:
        """Find CVE-CWEs that are numerically closest to CAPEC-CWEs"""
        query = """
        // Get CWE IDs with CVEs
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)
        WITH DISTINCT cwe1.id as cve_cwe_id, split(cwe1.id, '-')[1] as num1
        WITH cve_cwe_id, toInteger(num1) as cve_num
        WHERE cve_num IS NOT NULL

        // Get CWE IDs with CAPECs
        MATCH (cwe2:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH cve_cwe_id, cve_num, DISTINCT cwe2.id as capec_cwe_id, split(cwe2.id, '-')[1] as num2
        WITH cve_cwe_id, cve_num, capec_cwe_id, toInteger(num2) as capec_num
        WHERE capec_num IS NOT NULL

        // Calculate distance
        WITH cve_cwe_id, cve_num, capec_cwe_id, capec_num, abs(cve_num - capec_num) as distance
        ORDER BY distance ASC
        LIMIT 20

        RETURN
            cve_cwe_id,
            capec_cwe_id,
            distance
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]


def main():
    """Run diagnostic analysis"""
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')

    print("="*80)
    print("  ATTACK CHAIN GAP DIAGNOSTIC")
    print("="*80)
    print()

    diagnostic = None
    try:
        diagnostic = ChainGapDiagnostic(uri, user, password)

        # 1. Sample CWEs
        print("1. SAMPLE CWE IDs FROM EACH SET")
        print("-" * 80)
        samples = diagnostic.get_cwe_samples()
        print(f"CVE-connected CWEs:   {', '.join(samples['cve_cwes'])}")
        print(f"CAPEC-connected CWEs: {', '.join(samples['capec_cwes'])}")
        print()

        # 2. CWE ID Pattern Analysis
        print("2. CWE ID RANGE ANALYSIS")
        print("-" * 80)
        patterns = diagnostic.analyze_cwe_id_patterns()
        print(f"CVE-CWEs:   Range {patterns['cve_range'][0]}-{patterns['cve_range'][1]}, "
              f"Average: {patterns['cve_avg']:.0f}")
        print(f"CAPEC-CWEs: Range {patterns['capec_range'][0]}-{patterns['capec_range'][1]}, "
              f"Average: {patterns['capec_avg']:.0f}")
        print()

        overlap = not (patterns['cve_range'][1] < patterns['capec_range'][0] or
                      patterns['capec_range'][1] < patterns['cve_range'][0])
        if overlap:
            print("✓ Ranges overlap - issue is not due to disjoint CWE ID ranges")
        else:
            print("✗ Ranges do NOT overlap - CVE and CAPEC use different CWE generations")
        print()

        # 3. CWE Hierarchy Check
        print("3. CWE HIERARCHY BRIDGE ANALYSIS")
        print("-" * 80)
        hierarchy = diagnostic.check_cwe_hierarchy_bridges()

        if hierarchy['hierarchy_exists']:
            print(f"✓ CWE parent-child relationships exist!")
            print(f"  CVE-CWEs with hierarchy connections: {hierarchy['cve_cwes_with_hierarchy']}")
            print(f"  CAPEC-CWEs with hierarchy connections: {hierarchy['capec_cwes_with_hierarchy']}")
            print(f"  Total potential bridge paths: {hierarchy['total_paths']}")
            print(f"  Hop distance: {hierarchy['min_hops']} to {hierarchy['max_hops']}")
            print()
            print("  RECOMMENDATION: Use CWE hierarchy to create transitive chains!")
        else:
            print("✗ No CWE parent-child relationships found between the two sets")
            print()
            print("  RECOMMENDATION: Check if CHILDOF relationships exist in database")
        print()

        # 4. Closest Matches
        print("4. NUMERICALLY CLOSEST CWE MATCHES")
        print("-" * 80)
        print("CVE-CWE          CAPEC-CWE        Distance")
        print("-" * 50)
        matches = diagnostic.find_closest_matches()
        for match in matches[:10]:
            print(f"{match['cve_cwe_id']:<15} {match['capec_cwe_id']:<15} {match['distance']:>6}")
        print()

        # Summary and Recommendations
        print("="*80)
        print("  SUMMARY & RECOMMENDATIONS")
        print("="*80)
        print()

        if hierarchy['hierarchy_exists']:
            print("✓ SOLUTION AVAILABLE: Use CWE parent-child relationships")
            print()
            print("  Next Steps:")
            print("  1. Create transitive relationships through CWE hierarchy")
            print("  2. Query: MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe1:CWE)")
            print("            -[:CHILDOF*1..3]-(cwe2:CWE)")
            print("            -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)")
            print("  3. Create new relationship: (cwe1)-[:ENABLES_ATTACK_PATTERN]->(capec)")
            print("  4. Re-run validation")
        else:
            print("⚠ MANUAL INTERVENTION REQUIRED")
            print()
            print("  Options:")
            print("  1. Check if CHILDOF relationships exist in database")
            print("  2. Import CWE hierarchy data if missing")
            print("  3. Manually create CWE→CAPEC links for CVE-connected CWEs")
            print("  4. Find alternative CVE sources that map to CAPEC-connected CWEs")

        print()

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if diagnostic:
            diagnostic.close()

    return 0


if __name__ == "__main__":
    exit(main())
