#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
MITRE ATT&CK STIX 2.1 Importer
Phase 1: Core Schema Foundation
Created: 2025-10-29
═══════════════════════════════════════════════════════════════

Purpose:
  - Import MITRE ATT&CK Enterprise, Mobile, and ICS matrices from STIX 2.1 format
  - Transform STIX bundles to Neo4j Cypher statements
  - Support incremental updates with version tracking

STIX 2.1 Data Sources:
  - Enterprise ATT&CK: https://github.com/mitre-attack/attack-stix-data
  - ICS ATT&CK: https://github.com/mitre-attack/attack-stix-data
  - Local path: /home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/

Dependencies:
  pip install stix2 neo4j python-dotenv tqdm

Environment Variables:
  NEO4J_URI: Neo4j connection URI
  NEO4J_USER: Neo4j username
  NEO4J_PASSWORD: Neo4j password
  ATTACK_STIX_PATH: Path to STIX data files (default: ../10_Ontologies/MITRE-ATT-CK-STIX/)
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

import stix2
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
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ATT&CK STIX Data Path
ATTACK_STIX_PATH = os.getenv(
    "ATTACK_STIX_PATH",
    "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/"
)

# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class ATTACKTechnique:
    """MITRE ATT&CK Technique."""
    techniqueId: str
    name: str
    description: str
    tactic: List[str]
    platform: List[str]
    data_sources: List[str]
    detection: Optional[str]
    mitigation: List[str]
    is_subtechnique: bool
    parent_technique: Optional[str]
    stix_id: str
    is_shared: bool = True
    customer_namespace: str = "shared:attack"

@dataclass
class ATTACKTactic:
    """MITRE ATT&CK Tactic."""
    tacticId: str
    name: str
    description: str
    shortname: str
    stix_id: str

@dataclass
class ATTACKGroup:
    """MITRE ATT&CK Threat Actor Group."""
    groupId: str
    name: str
    aliases: List[str]
    description: str
    techniques_used: List[str]
    stix_id: str

# ═══════════════════════════════════════════════════════════════
# STIX Parser
# ═══════════════════════════════════════════════════════════════

class ATTACKSTIXParser:
    """Parser for MITRE ATT&CK STIX 2.1 data."""

    def __init__(self, stix_path: str):
        self.stix_path = Path(stix_path)
        self.techniques = []
        self.tactics = []
        self.groups = []

    def load_stix_bundle(self, filepath: Path) -> stix2.Bundle:
        """Load STIX bundle from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return stix2.parse(data, allow_custom=True)
        except Exception as e:
            logger.error(f"Failed to load STIX bundle from {filepath}: {e}")
            return None

    def parse_technique(self, stix_obj: dict) -> Optional[ATTACKTechnique]:
        """Parse ATT&CK technique from STIX attack-pattern object."""
        try:
            # Extract ATT&CK ID (e.g., T1190)
            external_refs = stix_obj.get('external_references', [])
            attack_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    attack_id = ref.get('external_id')
                    break

            if not attack_id:
                return None

            # Extract kill chain phases (tactics)
            kill_chain_phases = stix_obj.get('kill_chain_phases', [])
            tactics = [phase['phase_name'] for phase in kill_chain_phases]

            # Extract platforms
            platforms = stix_obj.get('x_mitre_platforms', [])

            # Extract data sources
            data_sources = stix_obj.get('x_mitre_data_sources', [])

            # Detect subtechniques (contain '.' in ID)
            is_subtechnique = '.' in attack_id
            parent_technique = attack_id.split('.')[0] if is_subtechnique else None

            # Extract detection guidance
            detection = stix_obj.get('x_mitre_detection', '')

            return ATTACKTechnique(
                techniqueId=attack_id,
                name=stix_obj.get('name', ''),
                description=stix_obj.get('description', ''),
                tactic=tactics,
                platform=platforms,
                data_sources=data_sources,
                detection=detection,
                mitigation=[],  # Will be populated from relationship objects
                is_subtechnique=is_subtechnique,
                parent_technique=parent_technique,
                stix_id=stix_obj.get('id', '')
            )

        except Exception as e:
            logger.error(f"Failed to parse technique: {e}")
            return None

    def parse_tactic(self, stix_obj: dict) -> Optional[ATTACKTactic]:
        """Parse ATT&CK tactic from STIX x-mitre-tactic object."""
        try:
            # Extract ATT&CK ID
            external_refs = stix_obj.get('external_references', [])
            tactic_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    tactic_id = ref.get('external_id')
                    break

            if not tactic_id:
                return None

            return ATTACKTactic(
                tacticId=tactic_id,
                name=stix_obj.get('name', ''),
                description=stix_obj.get('description', ''),
                shortname=stix_obj.get('x_mitre_shortname', ''),
                stix_id=stix_obj.get('id', '')
            )

        except Exception as e:
            logger.error(f"Failed to parse tactic: {e}")
            return None

    def parse_group(self, stix_obj: dict) -> Optional[ATTACKGroup]:
        """Parse ATT&CK group from STIX intrusion-set object."""
        try:
            # Extract ATT&CK ID
            external_refs = stix_obj.get('external_references', [])
            group_id = None
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    group_id = ref.get('external_id')
                    break

            if not group_id:
                return None

            # Extract aliases
            aliases = stix_obj.get('aliases', [])

            return ATTACKGroup(
                groupId=group_id,
                name=stix_obj.get('name', ''),
                aliases=aliases,
                description=stix_obj.get('description', ''),
                techniques_used=[],  # Will be populated from relationships
                stix_id=stix_obj.get('id', '')
            )

        except Exception as e:
            logger.error(f"Failed to parse group: {e}")
            return None

    def parse_bundle(self, bundle: stix2.Bundle):
        """Parse all objects from STIX bundle."""
        logger.info(f"Parsing bundle with {len(bundle.objects)} objects")

        for obj in tqdm(bundle.objects, desc="Parsing STIX objects"):
            obj_type = obj.get('type')

            if obj_type == 'attack-pattern':
                technique = self.parse_technique(obj)
                if technique:
                    self.techniques.append(technique)

            elif obj_type == 'x-mitre-tactic':
                tactic = self.parse_tactic(obj)
                if tactic:
                    self.tactics.append(tactic)

            elif obj_type == 'intrusion-set':
                group = self.parse_group(obj)
                if group:
                    self.groups.append(group)

        logger.info(f"Parsed {len(self.techniques)} techniques, "
                   f"{len(self.tactics)} tactics, {len(self.groups)} groups")

    def load_enterprise_attack(self):
        """Load Enterprise ATT&CK matrix."""
        enterprise_file = self.stix_path / "enterprise-attack" / "enterprise-attack.json"
        if enterprise_file.exists():
            logger.info(f"Loading Enterprise ATT&CK from {enterprise_file}")
            bundle = self.load_stix_bundle(enterprise_file)
            if bundle:
                self.parse_bundle(bundle)
        else:
            logger.warning(f"Enterprise ATT&CK file not found: {enterprise_file}")

    def load_ics_attack(self):
        """Load ICS ATT&CK matrix."""
        ics_file = self.stix_path / "ics-attack" / "ics-attack.json"
        if ics_file.exists():
            logger.info(f"Loading ICS ATT&CK from {ics_file}")
            bundle = self.load_stix_bundle(ics_file)
            if bundle:
                self.parse_bundle(bundle)
        else:
            logger.warning(f"ICS ATT&CK file not found: {ics_file}")

# ═══════════════════════════════════════════════════════════════
# Neo4j Ingestion
# ═══════════════════════════════════════════════════════════════

class Neo4jATTACKIngester:
    """Ingest ATT&CK data into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def ingest_technique(self, technique: ATTACKTechnique) -> bool:
        """Ingest ATT&CK technique into Neo4j."""
        query = """
        MERGE (t:Technique {techniqueId: $techniqueId})
        SET t.name = $name,
            t.description = $description,
            t.tactic = $tactic,
            t.platform = $platform,
            t.data_sources = $data_sources,
            t.detection = $detection,
            t.is_subtechnique = $is_subtechnique,
            t.parent_technique = $parent_technique,
            t.stix_id = $stix_id,
            t.is_shared = $is_shared,
            t.customer_namespace = $customer_namespace

        // Link subtechniques to parent
        WITH t
        WHERE t.is_subtechnique = true AND t.parent_technique IS NOT NULL
        MERGE (parent:Technique {techniqueId: t.parent_technique})
        MERGE (t)-[:SUBTECHNIQUE_OF]->(parent)

        RETURN t.techniqueId AS techniqueId
        """

        try:
            with self.driver.session() as session:
                result = session.run(query,
                    techniqueId=technique.techniqueId,
                    name=technique.name,
                    description=technique.description,
                    tactic=technique.tactic,
                    platform=technique.platform,
                    data_sources=technique.data_sources,
                    detection=technique.detection,
                    is_subtechnique=technique.is_subtechnique,
                    parent_technique=technique.parent_technique,
                    stix_id=technique.stix_id,
                    is_shared=technique.is_shared,
                    customer_namespace=technique.customer_namespace
                )
                record = result.single()
                return record is not None

        except Exception as e:
            logger.error(f"Failed to ingest technique {technique.techniqueId}: {e}")
            return False

    def ingest_batch(self, techniques: List[ATTACKTechnique]):
        """Ingest techniques in batch."""
        successes = 0
        total = len(techniques)

        with tqdm(total=total, desc="Ingesting ATT&CK techniques") as pbar:
            for technique in techniques:
                if self.ingest_technique(technique):
                    successes += 1
                pbar.update(1)

        logger.info(f"Ingested {successes}/{total} techniques successfully")
        return successes

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

def main():
    """Main execution function."""

    # Validate Neo4j credentials
    if not NEO4J_PASSWORD:
        logger.error("NEO4J_PASSWORD environment variable not set")
        sys.exit(1)

    # Validate STIX data path
    stix_path = Path(ATTACK_STIX_PATH)
    if not stix_path.exists():
        logger.error(f"ATT&CK STIX data path not found: {stix_path}")
        sys.exit(1)

    # Parse STIX data
    parser = ATTACKSTIXParser(ATTACK_STIX_PATH)
    parser.load_enterprise_attack()
    parser.load_ics_attack()

    if not parser.techniques:
        logger.warning("No techniques parsed from STIX data")
        return

    # Ingest into Neo4j
    ingester = Neo4jATTACKIngester(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        ingester.ingest_batch(parser.techniques)
    finally:
        ingester.close()

if __name__ == "__main__":
    main()
