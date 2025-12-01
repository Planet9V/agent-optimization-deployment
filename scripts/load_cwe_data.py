#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
CWE Weakness Loader
Created: 2025-11-28
Purpose: Load CWE v4.18 weakness data into Neo4j
Data: Complete CWE taxonomy with hierarchical relationships
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

CWE_XML_PATH = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/NVS Full CVE CAPEC CWE EMBED/cwec_v4.18.xml"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

CWE_NS = {'cwe': 'http://cwe.mitre.org/cwe-7'}

# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class CWEWeakness:
    """CWE Weakness."""
    cweId: str
    name: str
    description: str
    abstraction: str
    status: str
    parent_cwes: List[str]

# ═══════════════════════════════════════════════════════════════
# CWE Parser
# ═══════════════════════════════════════════════════════════════

class CWEParser:
    """Parse CWE XML file."""

    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.weaknesses = []

    def parse(self):
        """Parse CWE XML and extract weaknesses."""
        if not self.xml_path.exists():
            logger.error(f"CWE XML not found: {self.xml_path}")
            return

        logger.info(f"Parsing CWE XML: {self.xml_path}")

        try:
            tree = etree.parse(str(self.xml_path))
            root = tree.getroot()

            weaknesses = root.findall('.//cwe:Weakness', CWE_NS)
            logger.info(f"Found {len(weaknesses)} weaknesses")

            for w in tqdm(weaknesses, desc="Parsing CWE"):
                weakness = self._parse_weakness(w)
                if weakness:
                    self.weaknesses.append(weakness)

            logger.info(f"Successfully parsed {len(self.weaknesses)} weaknesses")

        except Exception as e:
            logger.error(f"Failed to parse CWE XML: {e}")

    def _parse_weakness(self, elem) -> Optional[CWEWeakness]:
        """Parse single weakness element."""
        try:
            cwe_id = elem.get('ID')
            if not cwe_id:
                return None
            cwe_id = f"CWE-{cwe_id}"

            name_elem = elem.get('Name')
            name = name_elem if name_elem else ""

            desc_elem = elem.find('cwe:Description', CWE_NS)
            description = desc_elem.text if desc_elem is not None and desc_elem.text else ""

            abstraction = elem.get('Abstraction', 'Base')
            status = elem.get('Status', 'Incomplete')

            # Extract parent relationships
            parent_cwes = []
            for rel in elem.findall('.//cwe:Related_Weakness', CWE_NS):
                nature = rel.get('Nature')
                if nature == 'ChildOf':
                    parent_id = rel.get('CWE_ID')
                    if parent_id:
                        parent_cwes.append(f"CWE-{parent_id}")

            return CWEWeakness(
                cweId=cwe_id,
                name=name,
                description=description,
                abstraction=abstraction,
                status=status,
                parent_cwes=parent_cwes
            )

        except Exception as e:
            logger.error(f"Failed to parse weakness: {e}")
            return None

# ═══════════════════════════════════════════════════════════════
# Neo4j Loader
# ═══════════════════════════════════════════════════════════════

class CWELoader:
    """Load CWE data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_weakness(self, weakness: CWEWeakness) -> bool:
        """Load single CWE weakness."""
        query = """
        MERGE (cwe:CWE {cweId: $cweId})
        SET cwe.name = $name,
            cwe.description = $description,
            cwe.abstraction = $abstraction,
            cwe.status = $status,
            cwe.is_shared = true,
            cwe.customer_namespace = 'shared:cwe'

        RETURN cwe.cweId AS cweId
        """

        try:
            with self.driver.session() as session:
                result = session.run(query,
                    cweId=weakness.cweId,
                    name=weakness.name,
                    description=weakness.description,
                    abstraction=weakness.abstraction,
                    status=weakness.status
                )
                return True

        except Exception as e:
            logger.error(f"Failed to load {weakness.cweId}: {e}")
            return False

    def create_hierarchy(self, weaknesses: List[CWEWeakness]):
        """Create CWE parent-child relationships."""
        logger.info("Creating CWE hierarchy relationships...")

        query = """
        MATCH (child:CWE {cweId: $childId})
        MATCH (parent:CWE {cweId: $parentId})
        MERGE (child)-[:CHILD_OF]->(parent)
        """

        count = 0
        with tqdm(total=len(weaknesses), desc="Creating hierarchy") as pbar:
            for weakness in weaknesses:
                for parent_id in weakness.parent_cwes:
                    try:
                        with self.driver.session() as session:
                            session.run(query,
                                childId=weakness.cweId,
                                parentId=parent_id
                            )
                            count += 1
                    except Exception as e:
                        logger.error(f"Failed to link {weakness.cweId} → {parent_id}: {e}")
                pbar.update(1)

        logger.info(f"Created {count} hierarchy relationships")
        return count

    def load_all(self, weaknesses: List[CWEWeakness]):
        """Load all CWE weaknesses."""
        successes = 0

        with tqdm(total=len(weaknesses), desc="Loading CWE") as pbar:
            for weakness in weaknesses:
                if self.load_weakness(weakness):
                    successes += 1
                pbar.update(1)

        logger.info(f"Successfully loaded {successes}/{len(weaknesses)} weaknesses")
        return successes

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    parser = CWEParser(CWE_XML_PATH)
    parser.parse()

    if not parser.weaknesses:
        logger.error("No weaknesses parsed")
        sys.exit(1)

    loader = CWELoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        loader.load_all(parser.weaknesses)
        loader.create_hierarchy(parser.weaknesses)

        # Verify counts
        with loader.driver.session() as session:
            result = session.run("MATCH (c:CWE) RETURN count(c) AS count")
            logger.info(f"Total CWE weaknesses: {result.single()['count']}")

            result = session.run("MATCH ()-[r:CHILD_OF]->() RETURN count(r) AS count")
            logger.info(f"Total hierarchy relationships: {result.single()['count']}")

    finally:
        loader.close()

if __name__ == "__main__":
    main()
