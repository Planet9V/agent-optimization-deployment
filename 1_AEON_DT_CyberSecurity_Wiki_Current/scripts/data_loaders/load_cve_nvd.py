#!/usr/bin/env python3
"""
AEON Cyber Digital Twin - CVE NVD Loader
=========================================
Loads CVE data from NVD JSON format into Neo4j.
Supports the enhanced AEON schema with CWE, CPE, and sector mappings.

Usage:
    NEO4J_PASSWORD="neo4j@openspg" python3 load_cve_nvd.py /path/to/CVE-2024.json

Sources:
    - https://github.com/fkie-cad/nvd-json-data-feeds

Created: 2025-11-29
Version: 1.0.0
"""

import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CVELoader:
    """Loads CVE data from NVD JSON into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize the loader with Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'cves_processed': 0,
            'cves_loaded': 0,
            'cwe_links_created': 0,
            'cpe_links_created': 0,
            'errors': []
        }

    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()

    def create_indexes(self):
        """Create indexes for optimal query performance."""
        queries = [
            # CVE indexes
            "CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.cveId IS UNIQUE",
            "CREATE INDEX cve_cvss IF NOT EXISTS FOR (c:CVE) ON (c.cvssBase)",
            "CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity)",
            "CREATE INDEX cve_published IF NOT EXISTS FOR (c:CVE) ON (c.publishedDate)",
            "CREATE INDEX cve_exploited IF NOT EXISTS FOR (c:CVE) ON (c.activelyExploited)",

            # CWE indexes
            "CREATE CONSTRAINT cwe_id IF NOT EXISTS FOR (w:CWE) REQUIRE w.cweId IS UNIQUE",

            # CPE indexes
            "CREATE CONSTRAINT cpe_criteria IF NOT EXISTS FOR (p:CPE) REQUIRE p.criteria IS UNIQUE",

            # Full-text search
            "CREATE FULLTEXT INDEX cve_description IF NOT EXISTS FOR (c:CVE) ON EACH [c.descriptionEN]"
        ]

        with self.driver.session() as session:
            for query in queries:
                try:
                    session.run(query)
                    logger.info(f"Executed: {query[:60]}...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        logger.warning(f"Index creation warning: {e}")

    def parse_cvss(self, metrics: Dict) -> Dict:
        """Extract CVSS data from metrics."""
        result = {
            'cvssVersion': None,
            'cvssBase': 0.0,
            'cvssVector': None,
            'severity': 'UNKNOWN',
            'exploitabilityScore': 0.0,
            'impactScore': 0.0,
            'attackVector': None,
            'attackComplexity': None,
            'privilegesRequired': None,
            'userInteraction': None,
            'scope': None,
            'confidentialityImpact': None,
            'integrityImpact': None,
            'availabilityImpact': None
        }

        # Try CVSS v3.1 first, then v3.0, then v2.0
        cvss_sources = [
            ('cvssMetricV31', '3.1'),
            ('cvssMetricV30', '3.0'),
            ('cvssMetricV2', '2.0')
        ]

        for source_key, version in cvss_sources:
            if source_key in metrics and metrics[source_key]:
                cvss_list = metrics[source_key]
                # Get the primary source (usually from NVD)
                for cvss in cvss_list:
                    cvss_data = cvss.get('cvssData', {})
                    if cvss_data:
                        result['cvssVersion'] = version
                        result['cvssBase'] = cvss_data.get('baseScore', 0.0)
                        result['cvssVector'] = cvss_data.get('vectorString')
                        result['severity'] = cvss_data.get('baseSeverity', 'UNKNOWN')
                        result['exploitabilityScore'] = cvss.get('exploitabilityScore', 0.0)
                        result['impactScore'] = cvss.get('impactScore', 0.0)
                        result['attackVector'] = cvss_data.get('attackVector')
                        result['attackComplexity'] = cvss_data.get('attackComplexity')
                        result['privilegesRequired'] = cvss_data.get('privilegesRequired')
                        result['userInteraction'] = cvss_data.get('userInteraction')
                        result['scope'] = cvss_data.get('scope')
                        result['confidentialityImpact'] = cvss_data.get('confidentialityImpact')
                        result['integrityImpact'] = cvss_data.get('integrityImpact')
                        result['availabilityImpact'] = cvss_data.get('availabilityImpact')
                        break
                if result['cvssBase']:
                    break

        return result

    def parse_cve(self, vuln: Dict) -> Optional[Dict]:
        """Parse a single CVE entry from NVD format."""
        try:
            cve = vuln if 'id' in vuln else vuln.get('cve', {})

            cve_id = cve.get('id')
            if not cve_id:
                return None

            # Get description
            descriptions = cve.get('descriptions', [])
            desc_en = next(
                (d['value'] for d in descriptions if d.get('lang') == 'en'),
                ''
            )

            # Parse CVSS
            metrics = cve.get('metrics', {})
            cvss = self.parse_cvss(metrics)

            # Parse weaknesses (CWE)
            weaknesses = []
            for weakness in cve.get('weaknesses', []):
                for desc in weakness.get('description', []):
                    cwe_id = desc.get('value')
                    if cwe_id and cwe_id.startswith('CWE-'):
                        weaknesses.append({
                            'cweId': cwe_id,
                            'type': weakness.get('type', 'Secondary')
                        })

            # Parse configurations (CPE)
            cpe_matches = []
            for config in cve.get('configurations', []):
                for node in config.get('nodes', []):
                    for match in node.get('cpeMatch', []):
                        if match.get('vulnerable'):
                            cpe_matches.append({
                                'criteria': match.get('criteria'),
                                'versionStartIncluding': match.get('versionStartIncluding'),
                                'versionEndExcluding': match.get('versionEndExcluding'),
                                'versionStartExcluding': match.get('versionStartExcluding'),
                                'versionEndIncluding': match.get('versionEndIncluding'),
                                'matchCriteriaId': match.get('matchCriteriaId')
                            })

            # Parse references
            references = [
                {'url': ref.get('url'), 'source': ref.get('source')}
                for ref in cve.get('references', [])
            ]

            return {
                'cveId': cve_id,
                'publishedDate': cve.get('published'),
                'lastModified': cve.get('lastModified'),
                'vulnStatus': cve.get('vulnStatus'),
                'sourceIdentifier': cve.get('sourceIdentifier'),
                'descriptionEN': desc_en[:10000] if desc_en else '',  # Truncate very long descriptions
                **cvss,
                'weaknesses': weaknesses,
                'cpe_matches': cpe_matches,
                'references': references[:10]  # Limit references
            }
        except Exception as e:
            logger.error(f"Error parsing CVE: {e}")
            return None

    def load_batch(self, cves: List[Dict]):
        """Load a batch of CVEs into Neo4j."""
        if not cves:
            return

        # Create/update CVE nodes
        cve_query = """
        UNWIND $cves AS cveData
        MERGE (cve:CVE {cveId: cveData.cveId})
        ON CREATE SET
            cve.publishedDate = datetime(cveData.publishedDate),
            cve.createdAt = datetime()
        ON MATCH SET
            cve.lastModified = datetime(cveData.lastModified),
            cve.updatedAt = datetime()
        SET
            cve.vulnStatus = cveData.vulnStatus,
            cve.sourceIdentifier = cveData.sourceIdentifier,
            cve.descriptionEN = cveData.descriptionEN,
            cve.cvssVersion = cveData.cvssVersion,
            cve.cvssBase = cveData.cvssBase,
            cve.cvssVector = cveData.cvssVector,
            cve.severity = cveData.severity,
            cve.exploitabilityScore = cveData.exploitabilityScore,
            cve.impactScore = cveData.impactScore,
            cve.attackVector = cveData.attackVector,
            cve.attackComplexity = cveData.attackComplexity,
            cve.privilegesRequired = cveData.privilegesRequired,
            cve.userInteraction = cveData.userInteraction,
            cve.scope = cveData.scope,
            cve.confidentialityImpact = cveData.confidentialityImpact,
            cve.integrityImpact = cveData.integrityImpact,
            cve.availabilityImpact = cveData.availabilityImpact,
            cve.nvdLastSync = datetime()
        RETURN count(cve) as count
        """

        with self.driver.session() as session:
            result = session.run(cve_query, {'cves': cves})
            count = result.single()['count']
            self.stats['cves_loaded'] += count

            # Create CWE relationships
            for cve_data in cves:
                for weakness in cve_data.get('weaknesses', []):
                    cwe_query = """
                    MATCH (cve:CVE {cveId: $cveId})
                    MERGE (cwe:CWE {cweId: $cweId})
                    MERGE (cve)-[r:HAS_WEAKNESS]->(cwe)
                    SET r.weaknessType = $type
                    RETURN 1 as count
                    """
                    try:
                        session.run(cwe_query, {
                            'cveId': cve_data['cveId'],
                            'cweId': weakness['cweId'],
                            'type': weakness['type']
                        })
                        self.stats['cwe_links_created'] += 1
                    except Exception as e:
                        logger.debug(f"CWE link error: {e}")

            # Create CPE relationships (limit to prevent explosion)
            for cve_data in cves:
                for cpe in cve_data.get('cpe_matches', [])[:5]:  # Limit to 5 CPE per CVE
                    if cpe.get('criteria'):
                        cpe_query = """
                        MATCH (cve:CVE {cveId: $cveId})
                        MERGE (cpe:CPE {criteria: $criteria})
                        MERGE (cve)-[r:AFFECTS_CPE]->(cpe)
                        SET r.versionStartIncluding = $versionStartIncluding,
                            r.versionEndExcluding = $versionEndExcluding,
                            r.matchCriteriaId = $matchCriteriaId
                        RETURN 1 as count
                        """
                        try:
                            session.run(cpe_query, {
                                'cveId': cve_data['cveId'],
                                'criteria': cpe['criteria'],
                                'versionStartIncluding': cpe.get('versionStartIncluding'),
                                'versionEndExcluding': cpe.get('versionEndExcluding'),
                                'matchCriteriaId': cpe.get('matchCriteriaId')
                            })
                            self.stats['cpe_links_created'] += 1
                        except Exception as e:
                            logger.debug(f"CPE link error: {e}")

    def load_file(self, filepath: str, batch_size: int = 100):
        """Load CVEs from a JSON file."""
        logger.info(f"Loading CVEs from: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Handle different JSON formats
        vulnerabilities = data.get('vulnerabilities', data.get('cve_items', []))
        total = len(vulnerabilities)
        logger.info(f"Found {total} CVEs to process")

        batch = []
        for i, vuln in enumerate(vulnerabilities):
            self.stats['cves_processed'] += 1
            parsed = self.parse_cve(vuln)

            if parsed:
                batch.append(parsed)

            if len(batch) >= batch_size:
                self.load_batch(batch)
                batch = []
                if (i + 1) % 1000 == 0:
                    logger.info(f"Progress: {i + 1}/{total} ({100*(i+1)/total:.1f}%)")

        # Load remaining batch
        if batch:
            self.load_batch(batch)

        logger.info(f"Completed loading {filepath}")

    def print_stats(self):
        """Print loading statistics."""
        print("\n" + "="*50)
        print("CVE Loading Statistics")
        print("="*50)
        print(f"CVEs processed: {self.stats['cves_processed']}")
        print(f"CVEs loaded:    {self.stats['cves_loaded']}")
        print(f"CWE links:      {self.stats['cwe_links_created']}")
        print(f"CPE links:      {self.stats['cpe_links_created']}")
        if self.stats['errors']:
            print(f"Errors:         {len(self.stats['errors'])}")
        print("="*50)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 load_cve_nvd.py <json_file> [<json_file2> ...]")
        print("\nExample:")
        print("  NEO4J_PASSWORD='password' python3 load_cve_nvd.py /tmp/CVE-2024.json")
        sys.exit(1)

    # Get Neo4j connection settings
    uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    user = os.environ.get('NEO4J_USER', 'neo4j')
    password = os.environ.get('NEO4J_PASSWORD', 'neo4j@openspg')

    logger.info(f"Connecting to Neo4j at {uri}")

    try:
        loader = CVELoader(uri, user, password)

        # Create indexes first
        logger.info("Creating indexes...")
        loader.create_indexes()

        # Load each file
        for filepath in sys.argv[1:]:
            if os.path.exists(filepath):
                loader.load_file(filepath)
            else:
                logger.error(f"File not found: {filepath}")

        # Print statistics
        loader.print_stats()

    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        loader.close()


if __name__ == '__main__':
    main()
