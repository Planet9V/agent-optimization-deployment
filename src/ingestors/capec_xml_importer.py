#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CAPEC XML Importer - Common Attack Pattern Enumeration
Phase 1: Import CAPEC v3.9 from existing XML file
Created: 2025-10-29
═══════════════════════════════════════════════════════════════

Purpose:
  - Import CAPEC attack patterns from XML
  - Link CAPEC to CWE (weakness exploitation)
  - Prepare for CAPEC → ATT&CK mapping

Data Source:
  /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/NVS Full CVE CAPEC CWE/capec_latest/capec_v3.9.xml

Dependencies:
  pip install lxml neo4j python-dotenv tqdm

Environment Variables:
  NEO4J_URI: Neo4j connection URI
  NEO4J_USER: Neo4j username
  NEO4J_PASSWORD: Neo4j password (default: neo4j@openspg)
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from lxml import etree

from neo4j import GraphDatabase
from dotenv import load_dotenv
from tqdm import tqdm

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

# CAPEC XML Path
CAPEC_XML_PATH = os.getenv(
    "CAPEC_XML_PATH",
    "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/NVS Full CVE CAPEC CWE/capec_latest/capec_v3.9.xml"
)

# XML Namespace
CAPEC_NS = {
    'capec': 'http://capec.mitre.org/capec-3'
}

# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class CAPECPattern:
    """CAPEC Attack Pattern."""
    capecId: str
    name: str
    description: str
    abstraction: str  # META, STANDARD, DETAILED
    likelihood: Optional[str]
    severity: Optional[str]
    prerequisites: List[str]
    related_cwes: List[str]
    is_shared: bool = True
    customer_namespace: str = "shared:capec"

# ═══════════════════════════════════════════════════════════════
# CAPEC XML Parser
# ═══════════════════════════════════════════════════════════════

class CAPECXMLParser:
    """Parser for CAPEC XML v3.9."""

    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.patterns = []

    def parse(self):
        """Parse CAPEC XML file."""
        if not self.xml_path.exists():
            logger.error(f"CAPEC XML file not found: {self.xml_path}")
            return

        logger.info(f"Parsing CAPEC XML: {self.xml_path}")

        try:
            tree = etree.parse(str(self.xml_path))
            root = tree.getroot()

            # Find all Attack_Patterns
            attack_patterns = root.findall('.//capec:Attack_Pattern', CAPEC_NS)
            logger.info(f"Found {len(attack_patterns)} attack patterns")

            for ap in tqdm(attack_patterns, desc="Parsing CAPEC patterns"):
                pattern = self.parse_attack_pattern(ap)
                if pattern:
                    self.patterns.append(pattern)

            logger.info(f"Parsed {len(self.patterns)} CAPEC patterns successfully")

        except Exception as e:
            logger.error(f"Failed to parse CAPEC XML: {e}")

    def parse_attack_pattern(self, elem) -> Optional[CAPECPattern]:
        """Parse single Attack_Pattern element."""
        try:
            # Extract CAPEC ID
            capec_id = elem.get('ID')
            if not capec_id:
                return None
            capec_id = f"CAPEC-{capec_id}"

            # Extract name
            name_elem = elem.find('capec:Name', CAPEC_NS)
            name = name_elem.text if name_elem is not None else ""

            # Extract description
            desc_elem = elem.find('capec:Description', CAPEC_NS)
            description = desc_elem.text if desc_elem is not None else ""

            # Extract abstraction level
            abstraction_elem = elem.find('capec:Abstraction', CAPEC_NS)
            abstraction = abstraction_elem.text if abstraction_elem is not None else "STANDARD"

            # Extract likelihood
            likelihood_elem = elem.find('.//capec:Likelihood_Of_Attack', CAPEC_NS)
            likelihood = likelihood_elem.text if likelihood_elem is not None else None

            # Extract severity
            severity_elem = elem.find('.//capec:Typical_Severity', CAPEC_NS)
            severity = severity_elem.text if severity_elem is not None else None

            # Extract prerequisites
            prerequisites = []
            prereq_elems = elem.findall('.//capec:Prerequisite', CAPEC_NS)
            for prereq in prereq_elems:
                if prereq.text:
                    prerequisites.append(prereq.text.strip())

            # Extract related CWEs
            related_cwes = []
            cwe_elems = elem.findall('.//capec:Related_Weakness', CAPEC_NS)
            for cwe_elem in cwe_elems:
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
            logger.error(f"Failed to parse attack pattern: {e}")
            return None

# ═══════════════════════════════════════════════════════════════
# Neo4j Ingestion
# ═══════════════════════════════════════════════════════════════

class Neo4jCAPECIngester:
    """Ingest CAPEC data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def ingest_pattern(self, pattern: CAPECPattern) -> bool:
        """Ingest single CAPEC pattern."""
        query = """
        MERGE (capec:CAPEC {capecId: $capecId})
        SET capec.name = $name,
            capec.description = $description,
            capec.abstraction = $abstraction,
            capec.likelihood = $likelihood,
            capec.severity = $severity,
            capec.prerequisites = $prerequisites,
            capec.is_shared = $is_shared,
            capec.customer_namespace = $customer_namespace

        // Link to related CWEs
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
                    related_cwes=pattern.related_cwes,
                    is_shared=pattern.is_shared,
                    customer_namespace=pattern.customer_namespace
                )
                record = result.single()
                return record is not None

        except Exception as e:
            logger.error(f"Failed to ingest CAPEC {pattern.capecId}: {e}")
            return False

    def ingest_batch(self, patterns: List[CAPECPattern]):
        """Ingest CAPEC patterns in batch."""
        successes = 0
        total = len(patterns)

        with tqdm(total=total, desc="Ingesting CAPEC patterns") as pbar:
            for pattern in patterns:
                if self.ingest_pattern(pattern):
                    successes += 1
                pbar.update(1)

        logger.info(f"Ingested {successes}/{total} CAPEC patterns successfully")
        return successes

    def create_cve_capec_relationships(self):
        """Create CVE → CAPEC relationships via CWE mapping."""
        query = """
        // Find CVEs linked to CWEs that are exploited by CAPEC
        MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
        MATCH (capec:CAPEC)-[:EXPLOITS_WEAKNESS]->(cwe)
        MERGE (cve)-[:ENABLES_ATTACK_PATTERN]->(capec)
        RETURN count(*) AS relationships_created
        """

        try:
            with self.driver.session() as session:
                result = session.run(query)
                count = result.single()['relationships_created']
                logger.info(f"Created {count} CVE → CAPEC relationships")
                return count

        except Exception as e:
            logger.error(f"Failed to create CVE-CAPEC relationships: {e}")
            return 0

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""

    # Validate XML file exists
    xml_path = Path(CAPEC_XML_PATH)
    if not xml_path.exists():
        logger.error(f"CAPEC XML file not found: {xml_path}")
        logger.info("Expected location: /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/NVS Full CVE CAPEC CWE/capec_latest/capec_v3.9.xml")
        sys.exit(1)

    # Parse CAPEC XML
    parser = CAPECXMLParser(CAPEC_XML_PATH)
    parser.parse()

    if not parser.patterns:
        logger.warning("No CAPEC patterns parsed from XML")
        return

    # Ingest into Neo4j
    ingester = Neo4jCAPECIngester(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Ingest patterns
        ingester.ingest_batch(parser.patterns)

        # Create CVE → CAPEC relationships
        logger.info("Creating CVE → CAPEC relationships via CWE mapping...")
        ingester.create_cve_capec_relationships()

    finally:
        ingester.close()

if __name__ == "__main__":
    main()
