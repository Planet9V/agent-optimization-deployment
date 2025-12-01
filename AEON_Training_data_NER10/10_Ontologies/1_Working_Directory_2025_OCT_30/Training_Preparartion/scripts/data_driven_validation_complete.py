#!/usr/bin/env python3
"""
DATA-DRIVEN VALIDATION AND COMPLETION SCRIPT
Using NVD API and FIRST.org EPSS to ensure COMPLETE relationships

Purpose: Query authoritative sources to validate and complete Neo4j database
         - NVD API: Official CVE→CWE mappings
         - FIRST.org: EPSS scores (verify 100% coverage)
         - CWE XML: Missing weakness definitions
         - CAPEC XML: Attack pattern mappings

This ensures training data completeness through FACT-BASED validation.

Author: AEON Protocol - Revised Implementation
Date: 2025-11-07
Version: 2.0.0
"""

import requests
import time
import logging
import sys
import json
from typing import Dict, List, Set, Tuple
from neo4j import GraphDatabase
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_driven_validation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
NVD_API_KEY = "534786f5-5359-40b8-8e54-b28eb742de7c"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
EPSS_API_URL = "https://api.first.org/data/v1/epss"

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# Rate limiting
NVD_RATE_LIMIT = 5  # requests per 30 seconds with API key
NVD_REQUESTS = []


class DataDrivenValidator:
    """
    Validates and completes Neo4j database using authoritative API sources.
    """

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.nvd_api_key = NVD_API_KEY
        self.session = requests.Session()
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close connections."""
        self.driver.close()
        self.session.close()
        logger.info("Connections closed")

    def rate_limit_nvd(self):
        """Enforce NVD API rate limiting (5 requests per 30 seconds)."""
        global NVD_REQUESTS
        now = time.time()

        # Remove requests older than 30 seconds
        NVD_REQUESTS = [req_time for req_time in NVD_REQUESTS if now - req_time < 30]

        # Wait if at rate limit
        if len(NVD_REQUESTS) >= NVD_RATE_LIMIT:
            sleep_time = 30 - (now - NVD_REQUESTS[0])
            if sleep_time > 0:
                logger.info(f"Rate limit reached, sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                NVD_REQUESTS = []

        NVD_REQUESTS.append(time.time())

    def get_neo4j_cve_sample(self, limit: int = 100) -> List[str]:
        """Get sample of CVE IDs from Neo4j to validate against NVD."""
        query = """
        MATCH (c:CVE)
        RETURN c.id AS cve_id
        ORDER BY c.id
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            return [record['cve_id'] for record in result]

    def query_nvd_cve(self, cve_id: str) -> Dict:
        """
        Query NVD API for official CVE data including CWE mappings.

        Returns:
            Dictionary with CVE data including official CWE IDs
        """
        self.rate_limit_nvd()

        url = f"{NVD_API_URL}?cveId={cve_id}"
        headers = {"apiKey": self.nvd_api_key}

        try:
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('vulnerabilities'):
                vuln = data['vulnerabilities'][0]['cve']

                # Extract CWE IDs from weaknesses
                cwe_ids = []
                if 'weaknesses' in vuln:
                    for weakness in vuln['weaknesses']:
                        for desc in weakness.get('description', []):
                            if desc['value'].startswith('CWE-'):
                                # Normalize to lowercase format
                                cwe_ids.append(desc['value'].lower())

                return {
                    'cve_id': cve_id,
                    'description': vuln.get('descriptions', [{}])[0].get('value', ''),
                    'cwe_ids': cwe_ids,
                    'published': vuln.get('published'),
                    'cvss_v3': vuln.get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseScore'),
                }

            return {'cve_id': cve_id, 'cwe_ids': [], 'error': 'No data'}

        except Exception as e:
            logger.error(f"Error querying NVD for {cve_id}: {e}")
            return {'cve_id': cve_id, 'cwe_ids': [], 'error': str(e)}

    def query_epss_batch(self, cve_ids: List[str]) -> Dict[str, float]:
        """
        Query FIRST.org EPSS API for batch of CVEs.

        Args:
            cve_ids: List of CVE IDs (max 1000)

        Returns:
            Dictionary mapping CVE ID to EPSS score
        """
        if not cve_ids or len(cve_ids) > 1000:
            logger.warning(f"Invalid batch size: {len(cve_ids)}")
            return {}

        # Join CVE IDs with commas
        cve_param = ','.join(cve_ids)
        url = f"{EPSS_API_URL}?cve={cve_param}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            epss_scores = {}
            if data.get('status') == 'OK' and 'data' in data:
                for entry in data['data']:
                    cve_id = entry['cve']
                    epss_score = float(entry['epss'])
                    epss_scores[cve_id] = epss_score

            return epss_scores

        except Exception as e:
            logger.error(f"Error querying EPSS for batch: {e}")
            return {}

    def validate_neo4j_state(self) -> Dict:
        """
        Query Neo4j to get current database state.

        Returns:
            Dictionary with node counts, relationship counts, and coverage stats
        """
        query = """
        // Node counts
        MATCH (cve:CVE) WITH count(cve) AS total_cves
        MATCH (cwe:CWE) WITH total_cves, count(cwe) AS total_cwes
        MATCH (capec:CAPEC) WITH total_cves, total_cwes, count(capec) AS total_capecs
        MATCH (tech:AttackTechnique) WITH total_cves, total_cwes, total_capecs, count(tech) AS total_techniques

        // Relationship counts
        OPTIONAL MATCH (cve:CVE)-[r1:IS_WEAKNESS_TYPE]->(cwe:CWE)
        WITH total_cves, total_cwes, total_capecs, total_techniques, count(r1) AS cve_cwe_rels

        OPTIONAL MATCH (cwe:CWE)-[r2:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
        WITH total_cves, total_cwes, total_capecs, total_techniques, cve_cwe_rels, count(r2) AS cwe_capec_rels

        OPTIONAL MATCH (capec:CAPEC)-[r3:USES_TECHNIQUE]->(tech:AttackTechnique)
        WITH total_cves, total_cwes, total_capecs, total_techniques, cve_cwe_rels, cwe_capec_rels, count(r3) AS capec_tech_rels

        // EPSS coverage
        OPTIONAL MATCH (c:CVE) WHERE c.epss_score IS NOT NULL
        WITH total_cves, total_cwes, total_capecs, total_techniques,
             cve_cwe_rels, cwe_capec_rels, capec_tech_rels,
             count(c) AS cves_with_epss

        // CWE with NULL IDs
        OPTIONAL MATCH (w:CWE) WHERE w.id IS NULL
        WITH total_cves, total_cwes, total_capecs, total_techniques,
             cve_cwe_rels, cwe_capec_rels, capec_tech_rels, cves_with_epss,
             count(w) AS cwes_null_id

        RETURN total_cves, total_cwes, total_capecs, total_techniques,
               cve_cwe_rels, cwe_capec_rels, capec_tech_rels,
               cves_with_epss, cwes_null_id
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()

            state = {
                'nodes': {
                    'cve': record['total_cves'],
                    'cwe': record['total_cwes'],
                    'capec': record['total_capecs'],
                    'attack_technique': record['total_techniques']
                },
                'relationships': {
                    'cve_cwe': record['cve_cwe_rels'],
                    'cwe_capec': record['cwe_capec_rels'],
                    'capec_technique': record['capec_tech_rels']
                },
                'coverage': {
                    'epss': record['cves_with_epss'],
                    'epss_percent': round(100.0 * record['cves_with_epss'] / record['total_cves'], 2) if record['total_cves'] > 0 else 0
                },
                'issues': {
                    'cwes_null_id': record['cwes_null_id']
                }
            }

            logger.info("=" * 80)
            logger.info("NEO4J DATABASE STATE (FACTS)")
            logger.info("=" * 80)
            logger.info(f"CVE nodes: {state['nodes']['cve']:,}")
            logger.info(f"CWE nodes: {state['nodes']['cwe']:,}")
            logger.info(f"CAPEC nodes: {state['nodes']['capec']:,}")
            logger.info(f"AttackTechnique nodes: {state['nodes']['attack_technique']:,}")
            logger.info(f"\nCVE→CWE relationships: {state['relationships']['cve_cwe']:,}")
            logger.info(f"CWE→CAPEC relationships: {state['relationships']['cwe_capec']:,}")
            logger.info(f"CAPEC→Technique relationships: {state['relationships']['capec_technique']:,}")
            logger.info(f"\nEPSS coverage: {state['coverage']['epss']:,} ({state['coverage']['epss_percent']}%)")
            logger.info(f"CWEs with NULL ID: {state['issues']['cwes_null_id']:,}")

            return state

    def sample_nvd_validation(self, sample_size: int = 50) -> Dict:
        """
        Sample NVD API to validate CVE→CWE mappings.

        Args:
            sample_size: Number of CVEs to sample and validate

        Returns:
            Validation results with CWE coverage analysis
        """
        logger.info(f"\n=== SAMPLING NVD API ({sample_size} CVEs) ===")

        # Get sample CVEs from Neo4j
        cve_sample = self.get_neo4j_cve_sample(limit=sample_size)
        logger.info(f"Retrieved {len(cve_sample)} CVEs from Neo4j")

        # Query NVD for each CVE
        nvd_results = []
        cwe_frequency = defaultdict(int)
        cves_with_cwe = 0
        cves_without_cwe = 0

        for i, cve_id in enumerate(cve_sample, 1):
            logger.info(f"Querying NVD: {i}/{len(cve_sample)} - {cve_id}")

            nvd_data = self.query_nvd_cve(cve_id)
            nvd_results.append(nvd_data)

            if nvd_data.get('cwe_ids'):
                cves_with_cwe += 1
                for cwe_id in nvd_data['cwe_ids']:
                    cwe_frequency[cwe_id] += 1
            else:
                cves_without_cwe += 1

        # Analysis
        coverage_percent = round(100.0 * cves_with_cwe / len(cve_sample), 2) if cve_sample else 0

        logger.info("\n" + "=" * 80)
        logger.info("NVD VALIDATION RESULTS (SAMPLE)")
        logger.info("=" * 80)
        logger.info(f"CVEs sampled: {len(cve_sample)}")
        logger.info(f"CVEs with CWE mappings: {cves_with_cwe} ({coverage_percent}%)")
        logger.info(f"CVEs without CWE: {cves_without_cwe}")
        logger.info(f"Unique CWEs found: {len(cwe_frequency)}")

        # Top CWEs
        logger.info("\nTop 10 CWEs in sample:")
        for cwe_id, count in sorted(cwe_frequency.items(), key=lambda x: x[1], reverse=True)[:10]:
            logger.info(f"  {cwe_id}: {count} occurrences")

        return {
            'sample_size': len(cve_sample),
            'cves_with_cwe': cves_with_cwe,
            'cves_without_cwe': cves_without_cwe,
            'coverage_percent': coverage_percent,
            'unique_cwes': len(cwe_frequency),
            'cwe_frequency': dict(cwe_frequency),
            'nvd_results': nvd_results
        }

    def identify_missing_cwes(self, cwe_ids: Set[str]) -> List[str]:
        """
        Check which CWEs from NVD data are missing in Neo4j.

        Args:
            cwe_ids: Set of CWE IDs found in NVD data

        Returns:
            List of missing CWE IDs
        """
        query = """
        UNWIND $cwe_ids AS cwe_id
        OPTIONAL MATCH (w:CWE)
        WHERE toLower(w.id) = toLower(cwe_id)
        WITH cwe_id, count(w) AS exists
        WHERE exists = 0
        RETURN cwe_id
        """

        with self.driver.session() as session:
            result = session.run(query, cwe_ids=list(cwe_ids))
            missing = [record['cwe_id'] for record in result]

        logger.info(f"\nMissing CWEs in Neo4j: {len(missing)} out of {len(cwe_ids)}")
        if missing:
            logger.warning(f"Sample missing: {missing[:20]}")

        return missing

    def generate_validation_report(self, neo4j_state: Dict, nvd_sample: Dict) -> Dict:
        """
        Generate comprehensive validation report.

        Returns:
            Complete validation report with recommendations
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'neo4j_state': neo4j_state,
            'nvd_validation': nvd_sample,
            'gaps_identified': {
                'cve_cwe_relationships': {
                    'current': neo4j_state['relationships']['cve_cwe'],
                    'expected_minimum': int(neo4j_state['nodes']['cve'] * (nvd_sample['coverage_percent'] / 100)),
                    'gap': 'CRITICAL' if neo4j_state['relationships']['cve_cwe'] < 1500 else 'ACCEPTABLE'
                },
                'cwe_completeness': {
                    'current': neo4j_state['nodes']['cwe'],
                    'null_ids': neo4j_state['issues']['cwes_null_id'],
                    'status': 'INCOMPLETE' if neo4j_state['issues']['cwes_null_id'] > 0 else 'COMPLETE'
                },
                'epss_coverage': {
                    'current': neo4j_state['coverage']['epss_percent'],
                    'status': 'COMPLETE' if neo4j_state['coverage']['epss_percent'] >= 99 else 'INCOMPLETE'
                }
            },
            'recommendations': []
        }

        # Generate recommendations
        if report['gaps_identified']['cve_cwe_relationships']['gap'] == 'CRITICAL':
            report['recommendations'].append({
                'priority': 'HIGH',
                'action': 'Fetch official CVE→CWE mappings from NVD API for all 316K CVEs',
                'rationale': f"Only {neo4j_state['relationships']['cve_cwe']} relationships exist, need 100K+"
            })

        if report['gaps_identified']['cwe_completeness']['status'] == 'INCOMPLETE':
            report['recommendations'].append({
                'priority': 'HIGH',
                'action': f"Import CWE v4.18 XML to fix {neo4j_state['issues']['cwes_null_id']} NULL IDs",
                'rationale': 'Missing CWE definitions prevent relationship creation'
            })

        if neo4j_state['relationships']['cwe_capec'] == 0:
            report['recommendations'].append({
                'priority': 'MEDIUM',
                'action': 'Download and parse CAPEC v3.9 XML for CWE→CAPEC mappings',
                'rationale': 'Required for complete attack chain creation'
            })

        # Save report
        with open('data_validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION REPORT GENERATED")
        logger.info("=" * 80)
        logger.info(f"Saved to: data_validation_report.json")

        return report


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("DATA-DRIVEN VALIDATION AND COMPLETION")
    logger.info("Using NVD API and FIRST.org EPSS to ensure completeness")
    logger.info("=" * 80)

    validator = DataDrivenValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Step 1: Validate current Neo4j state
        logger.info("\n[STEP 1] Validating Neo4j database state...")
        neo4j_state = validator.validate_neo4j_state()

        # Step 2: Sample NVD API to validate CVE→CWE coverage
        logger.info("\n[STEP 2] Sampling NVD API for validation...")
        nvd_sample = validator.sample_nvd_validation(sample_size=50)

        # Step 3: Identify missing CWEs
        logger.info("\n[STEP 3] Identifying missing CWEs...")
        all_cwes = set(nvd_sample['cwe_frequency'].keys())
        missing_cwes = validator.identify_missing_cwes(all_cwes)

        # Step 4: Generate validation report
        logger.info("\n[STEP 4] Generating validation report...")
        report = validator.generate_validation_report(neo4j_state, nvd_sample)

        # Step 5: Display recommendations
        logger.info("\n" + "=" * 80)
        logger.info("RECOMMENDATIONS FOR COMPLETION")
        logger.info("=" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            logger.info(f"\n{i}. [{rec['priority']}] {rec['action']}")
            logger.info(f"   Rationale: {rec['rationale']}")

        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION COMPLETE")
        logger.info("=" * 80)
        logger.info("Next: Execute recommendations using Claude-Flow swarm")

        return report

    except Exception as e:
        logger.error(f"Fatal error during validation: {e}", exc_info=True)
        raise
    finally:
        validator.close()


if __name__ == "__main__":
    report = main()
