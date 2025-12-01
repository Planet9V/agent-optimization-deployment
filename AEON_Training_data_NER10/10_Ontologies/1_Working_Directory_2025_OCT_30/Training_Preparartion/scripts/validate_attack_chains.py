#!/usr/bin/env python3
"""
Validation Script: Complete Attack Chain Testing
Tests CVE→CWE→CAPEC→ATT&CK attack chain completeness in Neo4j database

Author: Testing Agent
Created: 2025-11-07
Purpose: Validate complete attack chain paths exist and report coverage statistics
"""

import os
import sys
from neo4j import GraphDatabase
from typing import Dict, List, Tuple
import json
from datetime import datetime


class AttackChainValidator:
    """Validates complete attack chains in Neo4j database"""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.results = {}

    def close(self):
        """Close database connection"""
        self.driver.close()

    def validate_complete_chains(self) -> Dict:
        """
        Validate complete CVE→CWE→CAPEC→ATT&CK chains
        Returns: Dictionary with validation results
        """
        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        RETURN
            count(DISTINCT cve) as complete_cve_count,
            count(DISTINCT cwe) as cwe_in_chains,
            count(DISTINCT capec) as capec_in_chains,
            count(DISTINCT attack) as attack_in_chains,
            count(*) as total_chain_paths
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            return {
                'complete_cve_count': record['complete_cve_count'],
                'cwe_in_chains': record['cwe_in_chains'],
                'capec_in_chains': record['capec_in_chains'],
                'attack_in_chains': record['attack_in_chains'],
                'total_chain_paths': record['total_chain_paths']
            }

    def get_chain_coverage_by_cwe(self) -> List[Dict]:
        """Get coverage statistics grouped by CWE"""
        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        RETURN
            cwe.id as cwe_id,
            cwe.name as cwe_name,
            count(DISTINCT cve) as cve_count,
            count(DISTINCT capec) as capec_count,
            count(DISTINCT attack) as attack_count,
            count(*) as chain_count
        ORDER BY chain_count DESC
        LIMIT 20
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def get_chain_coverage_by_capec(self) -> List[Dict]:
        """Get coverage statistics grouped by CAPEC"""
        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        RETURN
            capec.id as capec_id,
            capec.name as capec_name,
            count(DISTINCT cve) as cve_count,
            count(DISTINCT cwe) as cwe_count,
            count(DISTINCT attack) as attack_count,
            count(*) as chain_count
        ORDER BY chain_count DESC
        LIMIT 20
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def get_chain_coverage_by_attack(self) -> List[Dict]:
        """Get coverage statistics grouped by ATT&CK technique"""
        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
              -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        RETURN
            attack.id as attack_id,
            attack.name as attack_name,
            count(DISTINCT cve) as cve_count,
            count(DISTINCT cwe) as cwe_count,
            count(DISTINCT capec) as capec_count,
            count(*) as chain_count
        ORDER BY chain_count DESC
        LIMIT 20
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def get_sample_chains(self, limit: int = 10) -> List[Dict]:
        """Get sample complete attack chains for verification"""
        query = """
        MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                     -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                     -[:USES_TECHNIQUE]->(attack:AttackTechnique)
        RETURN
            cve.id as cve_id,
            cve.description as cve_description,
            cwe.id as cwe_id,
            cwe.name as cwe_name,
            capec.id as capec_id,
            capec.name as capec_name,
            attack.id as attack_id,
            attack.name as attack_name
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            return [dict(record) for record in result]

    def validate_minimum_threshold(self, threshold: int = 124) -> Tuple[bool, str]:
        """
        Validate that at least threshold complete chains exist
        Returns: (passed, message)
        """
        stats = self.validate_complete_chains()
        complete_count = stats['complete_cve_count']

        passed = complete_count >= threshold
        message = f"Found {complete_count} complete chains. "

        if passed:
            message += f"✓ PASSED (threshold: {threshold})"
        else:
            message += f"✗ FAILED (threshold: {threshold}, shortfall: {threshold - complete_count})"

        return passed, message


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def print_table_header(headers: List[str], widths: List[int]):
    """Print formatted table header"""
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))


def generate_report(validator: AttackChainValidator) -> Dict:
    """Generate comprehensive validation report"""
    print_section("ATTACK CHAIN VALIDATION REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Database: Neo4j CVE-CWE-CAPEC-ATT&CK")

    # Overall statistics
    print_section("1. OVERALL CHAIN STATISTICS")
    stats = validator.validate_complete_chains()

    print(f"Complete CVE count (with full chains):  {stats['complete_cve_count']:>6}")
    print(f"CWE nodes in complete chains:           {stats['cwe_in_chains']:>6}")
    print(f"CAPEC nodes in complete chains:         {stats['capec_in_chains']:>6}")
    print(f"ATT&CK nodes in complete chains:        {stats['attack_in_chains']:>6}")
    print(f"Total unique chain paths:               {stats['total_chain_paths']:>6}")

    # Threshold validation
    print_section("2. THRESHOLD VALIDATION")
    passed, message = validator.validate_minimum_threshold(124)
    print(message)

    if not passed:
        print("\n⚠ WARNING: Minimum threshold not met!")
        print("   Expected: At least 124 complete CVE→CWE→CAPEC→ATT&CK chains")
        print(f"   Actual:   {stats['complete_cve_count']} complete chains")

    # CWE coverage
    print_section("3. TOP 20 CWE COVERAGE")
    cwe_coverage = validator.get_chain_coverage_by_cwe()

    headers = ["CWE ID", "CWE Name", "CVEs", "CAPECs", "ATT&CKs", "Chains"]
    widths = [12, 40, 6, 7, 8, 7]
    print_table_header(headers, widths)

    for row in cwe_coverage:
        print(f"{row['cwe_id']:<12} | {row['cwe_name'][:40]:<40} | "
              f"{row['cve_count']:>6} | {row['capec_count']:>7} | "
              f"{row['attack_count']:>8} | {row['chain_count']:>7}")

    # CAPEC coverage
    print_section("4. TOP 20 CAPEC COVERAGE")
    capec_coverage = validator.get_chain_coverage_by_capec()

    headers = ["CAPEC ID", "CAPEC Name", "CVEs", "CWEs", "ATT&CKs", "Chains"]
    widths = [12, 40, 6, 6, 8, 7]
    print_table_header(headers, widths)

    for row in capec_coverage:
        print(f"{row['capec_id']:<12} | {row['capec_name'][:40]:<40} | "
              f"{row['cve_count']:>6} | {row['cwe_count']:>6} | "
              f"{row['attack_count']:>8} | {row['chain_count']:>7}")

    # ATT&CK coverage
    print_section("5. TOP 20 ATT&CK TECHNIQUE COVERAGE")
    attack_coverage = validator.get_chain_coverage_by_attack()

    headers = ["ATT&CK ID", "Technique Name", "CVEs", "CWEs", "CAPECs", "Chains"]
    widths = [12, 40, 6, 6, 7, 7]
    print_table_header(headers, widths)

    for row in attack_coverage:
        print(f"{row['attack_id']:<12} | {row['attack_name'][:40]:<40} | "
              f"{row['cve_count']:>6} | {row['cwe_count']:>6} | "
              f"{row['capec_count']:>7} | {row['chain_count']:>7}")

    # Sample chains
    print_section("6. SAMPLE COMPLETE CHAINS (First 10)")
    samples = validator.get_sample_chains(10)

    for i, chain in enumerate(samples, 1):
        print(f"\nChain {i}:")
        print(f"  CVE:    {chain['cve_id']}")
        print(f"          {chain['cve_description'][:100]}...")
        print(f"  CWE:    {chain['cwe_id']} - {chain['cwe_name']}")
        print(f"  CAPEC:  {chain['capec_id']} - {chain['capec_name']}")
        print(f"  ATT&CK: {chain['attack_id']} - {chain['attack_name']}")

    # Summary
    print_section("7. VALIDATION SUMMARY")

    if passed:
        print("✓ VALIDATION PASSED")
        print(f"  - Found {stats['complete_cve_count']} complete attack chains")
        print(f"  - Exceeds minimum threshold of 124 chains")
        print(f"  - Coverage spans {stats['cwe_in_chains']} CWEs, "
              f"{stats['capec_in_chains']} CAPECs, {stats['attack_in_chains']} ATT&CK techniques")
    else:
        print("✗ VALIDATION FAILED")
        print(f"  - Found only {stats['complete_cve_count']} complete attack chains")
        print(f"  - Below minimum threshold of 124 chains")
        print(f"  - Need {124 - stats['complete_cve_count']} more complete chains")

    print("\n" + "="*80 + "\n")

    # Return data for JSON export
    return {
        'timestamp': datetime.now().isoformat(),
        'validation_passed': passed,
        'statistics': stats,
        'cwe_coverage': cwe_coverage,
        'capec_coverage': capec_coverage,
        'attack_coverage': attack_coverage,
        'sample_chains': samples
    }


def main():
    """Main execution function"""
    # Get Neo4j credentials from environment
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')

    print("Connecting to Neo4j database...")
    print(f"URI: {uri}")
    print(f"User: {user}")

    validator = None
    try:
        # Initialize validator
        validator = AttackChainValidator(uri, user, password)

        # Generate report
        report_data = generate_report(validator)

        # Export JSON report
        report_file = 'tests/attack_chain_validation_report.json'
        os.makedirs('tests', exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"JSON report exported to: {report_file}")

        # Exit with appropriate code
        sys.exit(0 if report_data['validation_passed'] else 1)

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)

    finally:
        if validator:
            validator.close()


if __name__ == "__main__":
    main()
