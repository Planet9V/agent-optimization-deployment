#!/usr/bin/env python3
"""
MITRE ATT&CK Importer - Complete implementation for importing MITRE ATT&CK data
Handles STIX 2.1 parsing, technique hierarchy, mitigation linking, and platform filtering.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import requests
from neo4j import GraphDatabase, Driver
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mitre_attack_importer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ImportMetrics:
    """Track import statistics"""
    tactics: int = 0
    techniques: int = 0
    sub_techniques: int = 0
    mitigations: int = 0
    groups: int = 0
    software: int = 0
    relationships: int = 0
    errors: int = 0


class MITREAttackImporter:
    """Import MITRE ATT&CK data from STIX 2.1 format into Neo4j"""

    # MITRE ATT&CK STIX data URLs
    ENTERPRISE_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    ICS_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json"
    MOBILE_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json"

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize MITRE ATT&CK importer

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.metrics = ImportMetrics()
        self._verify_connection()
        self._create_indexes()

        # Cache for object lookups
        self.stix_id_map = {}

    def _verify_connection(self):
        """Verify Neo4j connection"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            logger.info("Neo4j connection verified")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _create_indexes(self):
        """Create necessary indexes and constraints"""
        indexes = [
            "CREATE CONSTRAINT tactic_id IF NOT EXISTS FOR (t:AttackTactic) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT technique_id IF NOT EXISTS FOR (t:AttackTechnique) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT mitigation_id IF NOT EXISTS FOR (m:Mitigation) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT group_id IF NOT EXISTS FOR (g:ThreatActor) REQUIRE g.id IS UNIQUE",
            "CREATE CONSTRAINT software_id IF NOT EXISTS FOR (s:Malware) REQUIRE s.id IS UNIQUE",
            "CREATE INDEX technique_name IF NOT EXISTS FOR (t:AttackTechnique) ON (t.name)",
            "CREATE INDEX tactic_name IF NOT EXISTS FOR (t:AttackTactic) ON (t.name)",
        ]

        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"Created index/constraint: {index_query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")

    def fetch_attack_data(self, matrix: str = 'enterprise') -> Dict:
        """
        Fetch MITRE ATT&CK STIX data

        Args:
            matrix: 'enterprise', 'ics', or 'mobile'

        Returns:
            STIX bundle dictionary
        """
        url_map = {
            'enterprise': self.ENTERPRISE_ATTACK_URL,
            'ics': self.ICS_ATTACK_URL,
            'mobile': self.MOBILE_ATTACK_URL
        }

        url = url_map.get(matrix)
        if not url:
            raise ValueError(f"Invalid matrix: {matrix}")

        logger.info(f"Fetching {matrix} ATT&CK data from {url}")

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data.get('objects', []))} STIX objects")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch ATT&CK data: {e}")
            raise

    def _extract_external_id(self, obj: Dict) -> Optional[str]:
        """Extract ATT&CK ID from external references"""
        external_refs = obj.get('external_references', [])
        for ref in external_refs:
            if ref.get('source_name') == 'mitre-attack':
                return ref.get('external_id')
        return None

    def _extract_platforms(self, obj: Dict) -> List[str]:
        """Extract platform list"""
        return obj.get('x_mitre_platforms', [])

    def _extract_kill_chain_phases(self, obj: Dict) -> List[str]:
        """Extract tactic names from kill chain phases"""
        phases = obj.get('kill_chain_phases', [])
        return [phase['phase_name'] for phase in phases if phase.get('kill_chain_name') == 'mitre-attack']

    def _parse_tactics(self, objects: List[Dict]) -> List[Dict]:
        """Parse tactic objects"""
        tactics = []

        for obj in objects:
            if obj.get('type') == 'x-mitre-tactic':
                tactic_id = self._extract_external_id(obj)
                if not tactic_id:
                    continue

                tactics.append({
                    'id': tactic_id,
                    'stix_id': obj['id'],
                    'name': obj.get('name'),
                    'description': obj.get('description', ''),
                    'shortname': obj.get('x_mitre_shortname', '')
                })

                self.stix_id_map[obj['id']] = tactic_id

        logger.info(f"Parsed {len(tactics)} tactics")
        return tactics

    def _parse_techniques(self, objects: List[Dict]) -> List[Dict]:
        """Parse technique and sub-technique objects"""
        techniques = []

        for obj in objects:
            if obj.get('type') == 'attack-pattern':
                tech_id = self._extract_external_id(obj)
                if not tech_id:
                    continue

                # Determine if sub-technique
                is_subtechnique = obj.get('x_mitre_is_subtechnique', False)
                parent_id = None

                if is_subtechnique:
                    # Extract parent technique ID from technique ID (e.g., T1566.001 -> T1566)
                    parent_id = tech_id.split('.')[0] if '.' in tech_id else None

                techniques.append({
                    'id': tech_id,
                    'stix_id': obj['id'],
                    'name': obj.get('name'),
                    'description': obj.get('description', ''),
                    'is_subtechnique': is_subtechnique,
                    'parent_id': parent_id,
                    'platforms': self._extract_platforms(obj),
                    'tactics': self._extract_kill_chain_phases(obj),
                    'detection': obj.get('x_mitre_detection', ''),
                    'data_sources': obj.get('x_mitre_data_sources', []),
                    'deprecated': obj.get('x_mitre_deprecated', False)
                })

                self.stix_id_map[obj['id']] = tech_id

        logger.info(f"Parsed {len(techniques)} techniques/sub-techniques")
        return techniques

    def _parse_mitigations(self, objects: List[Dict]) -> List[Dict]:
        """Parse mitigation objects"""
        mitigations = []

        for obj in objects:
            if obj.get('type') == 'course-of-action':
                mitigation_id = self._extract_external_id(obj)
                if not mitigation_id:
                    continue

                mitigations.append({
                    'id': mitigation_id,
                    'stix_id': obj['id'],
                    'name': obj.get('name'),
                    'description': obj.get('description', ''),
                    'deprecated': obj.get('x_mitre_deprecated', False)
                })

                self.stix_id_map[obj['id']] = mitigation_id

        logger.info(f"Parsed {len(mitigations)} mitigations")
        return mitigations

    def _parse_groups(self, objects: List[Dict]) -> List[Dict]:
        """Parse threat group objects"""
        groups = []

        for obj in objects:
            if obj.get('type') == 'intrusion-set':
                group_id = self._extract_external_id(obj)
                if not group_id:
                    continue

                groups.append({
                    'id': group_id,
                    'stix_id': obj['id'],
                    'name': obj.get('name'),
                    'description': obj.get('description', ''),
                    'aliases': obj.get('aliases', [])
                })

                self.stix_id_map[obj['id']] = group_id

        logger.info(f"Parsed {len(groups)} threat groups")
        return groups

    def _parse_software(self, objects: List[Dict]) -> List[Dict]:
        """Parse malware and tool objects"""
        software = []

        for obj in objects:
            if obj.get('type') in ['malware', 'tool']:
                software_id = self._extract_external_id(obj)
                if not software_id:
                    continue

                software.append({
                    'id': software_id,
                    'stix_id': obj['id'],
                    'name': obj.get('name'),
                    'description': obj.get('description', ''),
                    'type': obj.get('type'),
                    'platforms': self._extract_platforms(obj),
                    'aliases': obj.get('x_mitre_aliases', [])
                })

                self.stix_id_map[obj['id']] = software_id

        logger.info(f"Parsed {len(software)} software/tools")
        return software

    def _parse_relationships(self, objects: List[Dict]) -> List[Dict]:
        """Parse relationship objects"""
        relationships = []

        for obj in objects:
            if obj.get('type') == 'relationship':
                source_ref = obj.get('source_ref')
                target_ref = obj.get('target_ref')

                # Map STIX IDs to ATT&CK IDs
                source_id = self.stix_id_map.get(source_ref)
                target_id = self.stix_id_map.get(target_ref)

                if source_id and target_id:
                    relationships.append({
                        'source_id': source_id,
                        'target_id': target_id,
                        'relationship_type': obj.get('relationship_type'),
                        'description': obj.get('description', '')
                    })

        logger.info(f"Parsed {len(relationships)} relationships")
        return relationships

    def import_tactics(self, tactics: List[Dict]):
        """Import tactics into Neo4j"""
        if not tactics:
            return

        cypher = """
        UNWIND $tactics as tactic
        MERGE (t:AttackTactic {id: tactic.id})
        SET t.stix_id = tactic.stix_id,
            t.name = tactic.name,
            t.description = tactic.description,
            t.shortname = tactic.shortname,
            t.lastImported = datetime()
        """

        with self.driver.session() as session:
            session.run(cypher, tactics=tactics)
            self.metrics.tactics = len(tactics)

        logger.info(f"Imported {len(tactics)} tactics")

    def import_techniques(self, techniques: List[Dict]):
        """Import techniques and sub-techniques into Neo4j"""
        if not techniques:
            return

        cypher = """
        UNWIND $techniques as tech
        MERGE (t:AttackTechnique {id: tech.id})
        SET t.stix_id = tech.stix_id,
            t.name = tech.name,
            t.description = tech.description,
            t.is_subtechnique = tech.is_subtechnique,
            t.platforms = tech.platforms,
            t.detection = tech.detection,
            t.data_sources = tech.data_sources,
            t.deprecated = tech.deprecated,
            t.lastImported = datetime()

        WITH t, tech
        WHERE tech.parent_id IS NOT NULL
        MATCH (parent:AttackTechnique {id: tech.parent_id})
        MERGE (t)-[:SUBTECHNIQUE_OF]->(parent)

        WITH t, tech
        UNWIND tech.tactics as tactic_name
        MATCH (tactic:AttackTactic {shortname: tactic_name})
        MERGE (t)-[:USES_TACTIC]->(tactic)
        """

        with self.driver.session() as session:
            with tqdm(total=len(techniques), desc="Importing techniques") as pbar:
                batch_size = 500
                for i in range(0, len(techniques), batch_size):
                    batch = techniques[i:i + batch_size]
                    session.run(cypher, techniques=batch)
                    pbar.update(len(batch))

            # Count sub-techniques
            self.metrics.techniques = sum(1 for t in techniques if not t['is_subtechnique'])
            self.metrics.sub_techniques = sum(1 for t in techniques if t['is_subtechnique'])

        logger.info(f"Imported {self.metrics.techniques} techniques and {self.metrics.sub_techniques} sub-techniques")

    def import_mitigations(self, mitigations: List[Dict]):
        """Import mitigations into Neo4j"""
        if not mitigations:
            return

        cypher = """
        UNWIND $mitigations as mitigation
        MERGE (m:Mitigation {id: mitigation.id})
        SET m.stix_id = mitigation.stix_id,
            m.name = mitigation.name,
            m.description = mitigation.description,
            m.deprecated = mitigation.deprecated,
            m.lastImported = datetime()
        """

        with self.driver.session() as session:
            session.run(cypher, mitigations=mitigations)
            self.metrics.mitigations = len(mitigations)

        logger.info(f"Imported {len(mitigations)} mitigations")

    def import_groups(self, groups: List[Dict]):
        """Import threat groups into Neo4j"""
        if not groups:
            return

        cypher = """
        UNWIND $groups as grp
        MERGE (g:ThreatActor {id: grp.id})
        SET g.stix_id = grp.stix_id,
            g.name = grp.name,
            g.description = grp.description,
            g.aliases = grp.aliases,
            g.source = 'MITRE_ATT&CK',
            g.lastImported = datetime()
        """

        with self.driver.session() as session:
            session.run(cypher, groups=groups)
            self.metrics.groups = len(groups)

        logger.info(f"Imported {len(groups)} threat groups")

    def import_software(self, software: List[Dict]):
        """Import malware and tools into Neo4j"""
        if not software:
            return

        cypher = """
        UNWIND $software as sw
        MERGE (s:Malware {id: sw.id})
        SET s.stix_id = sw.stix_id,
            s.name = sw.name,
            s.description = sw.description,
            s.type = sw.type,
            s.platforms = sw.platforms,
            s.aliases = sw.aliases,
            s.lastImported = datetime()
        """

        with self.driver.session() as session:
            session.run(cypher, software=software)
            self.metrics.software = len(software)

        logger.info(f"Imported {len(software)} software/tools")

    def import_relationships(self, relationships: List[Dict]):
        """Import relationships into Neo4j"""
        if not relationships:
            return

        # Group by relationship type
        rel_by_type = {}
        for rel in relationships:
            rel_type = rel['relationship_type']
            if rel_type not in rel_by_type:
                rel_by_type[rel_type] = []
            rel_by_type[rel_type].append(rel)

        with self.driver.session() as session:
            for rel_type, rels in rel_by_type.items():
                # Map relationship types to Cypher relationship names
                cypher_rel_type = rel_type.upper().replace('-', '_')

                cypher = f"""
                UNWIND $rels as rel
                MATCH (source {{id: rel.source_id}})
                MATCH (target {{id: rel.target_id}})
                MERGE (source)-[r:{cypher_rel_type}]->(target)
                SET r.description = rel.description
                """

                try:
                    session.run(cypher, rels=rels)
                    self.metrics.relationships += len(rels)
                except Exception as e:
                    logger.warning(f"Failed to import {rel_type} relationships: {e}")

        logger.info(f"Imported {self.metrics.relationships} relationships")

    def import_full_matrix(self, matrix: str = 'enterprise',
                          platform_filter: Optional[Set[str]] = None):
        """
        Import full ATT&CK matrix

        Args:
            matrix: 'enterprise', 'ics', or 'mobile'
            platform_filter: Set of platforms to filter (e.g., {'Windows', 'Linux'})
        """
        logger.info(f"Starting full import of {matrix} ATT&CK matrix")

        # Fetch data
        data = self.fetch_attack_data(matrix)
        objects = data.get('objects', [])

        # Parse all objects
        tactics = self._parse_tactics(objects)
        techniques = self._parse_techniques(objects)
        mitigations = self._parse_mitigations(objects)
        groups = self._parse_groups(objects)
        software = self._parse_software(objects)
        relationships = self._parse_relationships(objects)

        # Apply platform filter if specified
        if platform_filter:
            logger.info(f"Filtering by platforms: {platform_filter}")
            techniques = [t for t in techniques
                         if not t['platforms'] or any(p in platform_filter for p in t['platforms'])]
            software = [s for s in software
                       if not s['platforms'] or any(p in platform_filter for p in s['platforms'])]

        # Import in order
        self.import_tactics(tactics)
        self.import_techniques(techniques)
        self.import_mitigations(mitigations)
        self.import_groups(groups)
        self.import_software(software)
        self.import_relationships(relationships)

        logger.info("Import complete")

    def get_metrics(self) -> ImportMetrics:
        """Return import metrics"""
        return self.metrics

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("MITRE ATT&CK importer closed")


def main():
    """Main execution function"""
    # Configuration from environment or defaults
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # Initialize importer
    importer = MITREAttackImporter(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD
    )

    try:
        # Import enterprise matrix with Windows/Linux focus
        platform_filter = {'Windows', 'Linux', 'Network'}
        importer.import_full_matrix(
            matrix='enterprise',
            platform_filter=platform_filter
        )

        # Print metrics
        metrics = importer.get_metrics()
        logger.info(f"""
        Import Metrics:
        - Tactics: {metrics.tactics}
        - Techniques: {metrics.techniques}
        - Sub-techniques: {metrics.sub_techniques}
        - Mitigations: {metrics.mitigations}
        - Threat Groups: {metrics.groups}
        - Software/Tools: {metrics.software}
        - Relationships: {metrics.relationships}
        - Errors: {metrics.errors}
        """)

    except Exception as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    finally:
        importer.close()


if __name__ == "__main__":
    main()
