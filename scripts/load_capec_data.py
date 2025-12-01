#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CAPEC Attack Pattern Loader
Created: 2025-11-28
Purpose: Load CAPEC v3.9 attack patterns into Neo4j
Data: 3778 attack patterns with CWE mappings
═══════════════════════════════════════════════════════════════
"""

import logging
import sys
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from lxml import etree
from neo4j import GraphDatabase
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

CAPEC_XML_PATH = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/NVS Full CVE CAPEC CWE EMBED/capec_latest/capec_v3.9.xml"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

CAPEC_NS = {'capec': 'http://capec.mitre.org/capec-3'}

# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class CAPECPattern:
    """CAPEC Attack Pattern."""
    capecId: str
    name: str
    description: str
    abstraction: str
    likelihood: Optional[str]
    severity: Optional[str]
    prerequisites: List[str]
    related_cwes: List[str]

# ═══════════════════════════════════════════════════════════════
# CAPEC Parser
# ═══════════════════════════════════════════════════════════════

class CAPECParser:
    """Parse CAPEC XML file."""

    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.patterns = []

    def parse(self):
        """Parse CAPEC XML and extract attack patterns."""
        if not self.xml_path.exists():
            logger.error(f"CAPEC XML not found: {self.xml_path}")
            return

        logger.info(f"Parsing CAPEC XML: {self.xml_path}")

        try:
            tree = etree.parse(str(self.xml_path))
            root = tree.getroot()

            patterns = root.findall('.//capec:Attack_Pattern', CAPEC_NS)
            logger.info(f"Found {len(patterns)} attack patterns")

            for ap in tqdm(patterns, desc="Parsing CAPEC"):
                pattern = self._parse_pattern(ap)
                if pattern:
                    self.patterns.append(pattern)

            logger.info(f"Successfully parsed {len(self.patterns)} patterns")

        except Exception as e:
            logger.error(f"Failed to parse CAPEC XML: {e}")

    def _parse_pattern(self, elem) -> Optional[CAPECPattern]:
        """Parse single attack pattern element."""
        try:
            capec_id = elem.get('ID')
            if not capec_id:
                return None
            capec_id = f"CAPEC-{capec_id}"

            name_elem = elem.find('capec:Name', CAPEC_NS)
            name = name_elem.text if name_elem is not None else ""

            desc_elem = elem.find('capec:Description', CAPEC_NS)
            description = desc_elem.text if desc_elem is not None else ""

            abstraction_elem = elem.find('capec:Abstraction', CAPEC_NS)
            abstraction = abstraction_elem.text if abstraction_elem is not None else "STANDARD"

            likelihood_elem = elem.find('.//capec:Likelihood_Of_Attack', CAPEC_NS)
            likelihood = likelihood_elem.text if likelihood_elem is not None else None

            severity_elem = elem.find('.//capec:Typical_Severity', CAPEC_NS)
            severity = severity_elem.text if severity_elem is not None else None

            prerequisites = []
            for prereq in elem.findall('.//capec:Prerequisite', CAPEC_NS):
                if prereq.text:
                    prerequisites.append(prereq.text.strip())

            related_cwes = []
            for cwe_elem in elem.findall('.//capec:Related_Weakness', CAPEC_NS):
                cwe_id = cwe_elem.get('CWE_ID')
                if cwe_id:
                    related_cwes.append(f"CWE-{cwe_id}")

            return CAPECPattern(
                capecId=capec_id,
                name=name,
                description=description,
                abstraction=abstraction,
                likelihood=likelihood,
                severity=severity,
                prerequisites=prerequisites,
                related_cwes=related_cwes
            )

        except Exception as e:
            logger.error(f"Failed to parse pattern: {e}")
            return None

# ═══════════════════════════════════════════════════════════════
# Neo4j Loader
# ═══════════════════════════════════════════════════════════════

class CAPECLoader:
    """Load CAPEC data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_pattern(self, pattern: CAPECPattern) -> bool:
        """Load single CAPEC pattern."""
        query = """
        MERGE (capec:CAPEC {capecId: $capecId})
        SET capec.name = $name,
            capec.description = $description,
            capec.abstraction = $abstraction,
            capec.likelihood = $likelihood,
            capec.severity = $severity,
            capec.prerequisites = $prerequisites,
            capec.is_shared = true,
            capec.customer_namespace = 'shared:capec'

        // Link to CWEs
        WITH capec
        UNWIND $related_cwes AS cwe_id
        MERGE (cwe:CWE {cweId: cwe_id})
        ON CREATE SET
          cwe.customer_namespace = 'shared:cwe',
          cwe.is_shared = true
        MERGE (capec)-[:EXPLOITS_WEAKNESS]->(cwe)

        RETURN capec.capecId AS capecId
        """

        try:
            with self.driver.session() as session:
                result = session.run(query,
                    capecId=pattern.capecId,
                    name=pattern.name,
                    description=pattern.description,
                    abstraction=pattern.abstraction,
                    likelihood=pattern.likelihood,
                    severity=pattern.severity,
                    prerequisites=pattern.prerequisites,
                    related_cwes=pattern.related_cwes
                )
                return True

        except Exception as e:
            logger.error(f"Failed to load {pattern.capecId}: {e}")
            return False

    def load_all(self, patterns: List[CAPECPattern]):
        """Load all CAPEC patterns."""
        successes = 0

        with tqdm(total=len(patterns), desc="Loading CAPEC") as pbar:
            for pattern in patterns:
                if self.load_pattern(pattern):
                    successes += 1
                pbar.update(1)

        logger.info(f"Successfully loaded {successes}/{len(patterns)} patterns")
        return successes

    def create_cve_capec_links(self):
        """Create CVE → CAPEC relationships via CWE."""
        query = """
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
        MATCH (capec:CAPEC)-[:EXPLOITS_WEAKNESS]->(cwe)
        MERGE (cve)-[:ENABLES_ATTACK_PATTERN]->(capec)
        RETURN count(*) AS count
        """

        try:
            with self.driver.session() as session:
                result = session.run(query)
                count = result.single()['count']
                logger.info(f"Created {count} CVE → CAPEC relationships")
                return count

        except Exception as e:
            logger.error(f"Failed to create CVE-CAPEC links: {e}")
            return 0

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    parser = CAPECParser(CAPEC_XML_PATH)
    parser.parse()

    if not parser.patterns:
        logger.error("No patterns parsed")
        sys.exit(1)

    loader = CAPECLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        loader.load_all(parser.patterns)
        loader.create_cve_capec_links()

        # Verify counts
        with loader.driver.session() as session:
            result = session.run("MATCH (c:CAPEC) RETURN count(c) AS count")
            logger.info(f"Total CAPEC patterns: {result.single()['count']}")

    finally:
        loader.close()

if __name__ == "__main__":
    main()
