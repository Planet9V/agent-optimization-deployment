#!/usr/bin/env python3
"""
AEON Cyber Digital Twin - STIX/MITRE ATT&CK Loader
===================================================
Loads STIX 2.1 bundles (MITRE ATT&CK) into Neo4j.
Supports threat actors, attack patterns, malware, campaigns, tools.

Usage:
    NEO4J_PASSWORD="neo4j@openspg" python3 load_stix_attack.py enterprise-attack.json

Sources:
    - https://github.com/mitre/cti
    - https://attack.mitre.org/

Created: 2025-11-29
Version: 1.0.0
"""

import json
import os
import sys
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from neo4j import GraphDatabase

try:
    from stix2 import parse, Bundle
except ImportError:
    print("stix2 library not found. Install with: pip install stix2")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class STIXLoader:
    """Loads STIX 2.1 bundles into Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize the loader with Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'objects_processed': 0,
            'attack_patterns': 0,
            'malware': 0,
            'tools': 0,
            'intrusion_sets': 0,
            'campaigns': 0,
            'relationships': 0,
            'tactics': 0,
            'data_sources': 0,
            'errors': []
        }
        self.stix_id_map = {}  # Track STIX IDs for relationship resolution

    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()

    def create_indexes(self):
        """Create indexes for STIX objects."""
        queries = [
            # Attack pattern indexes
            "CREATE CONSTRAINT attack_pattern_stix IF NOT EXISTS FOR (a:AttackPattern) REQUIRE a.stixId IS UNIQUE",
            "CREATE INDEX attack_pattern_mitre IF NOT EXISTS FOR (a:AttackPattern) ON (a.mitreId)",
            "CREATE INDEX attack_pattern_name IF NOT EXISTS FOR (a:AttackPattern) ON (a.name)",

            # Malware indexes
            "CREATE CONSTRAINT malware_stix IF NOT EXISTS FOR (m:Malware) REQUIRE m.stixId IS UNIQUE",
            "CREATE INDEX malware_name IF NOT EXISTS FOR (m:Malware) ON (m.name)",

            # Tool indexes
            "CREATE CONSTRAINT tool_stix IF NOT EXISTS FOR (t:Tool) REQUIRE t.stixId IS UNIQUE",
            "CREATE INDEX tool_name IF NOT EXISTS FOR (t:Tool) ON (t.name)",

            # Intrusion Set (Threat Actor) indexes
            "CREATE CONSTRAINT intrusion_set_stix IF NOT EXISTS FOR (i:IntrusionSet) REQUIRE i.stixId IS UNIQUE",
            "CREATE INDEX intrusion_set_name IF NOT EXISTS FOR (i:IntrusionSet) ON (i.name)",

            # Campaign indexes
            "CREATE CONSTRAINT campaign_stix IF NOT EXISTS FOR (c:Campaign) REQUIRE c.stixId IS UNIQUE",
            "CREATE INDEX campaign_name IF NOT EXISTS FOR (c:Campaign) ON (c.name)",

            # Tactic indexes
            "CREATE CONSTRAINT tactic_stix IF NOT EXISTS FOR (t:Tactic) REQUIRE t.stixId IS UNIQUE",
            "CREATE INDEX tactic_short IF NOT EXISTS FOR (t:Tactic) ON (t.shortName)",

            # Data source indexes
            "CREATE CONSTRAINT data_source_stix IF NOT EXISTS FOR (d:DataSource) REQUIRE d.stixId IS UNIQUE"
        ]

        with self.driver.session() as session:
            for query in queries:
                try:
                    session.run(query)
                    logger.info(f"Executed: {query[:60]}...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        logger.warning(f"Index creation warning: {e}")

    def extract_mitre_id(self, obj: Dict) -> Optional[str]:
        """Extract MITRE technique/software ID from external references."""
        for ref in obj.get('external_references', []):
            if ref.get('source_name') == 'mitre-attack':
                return ref.get('external_id')
        return None

    def extract_url(self, obj: Dict) -> Optional[str]:
        """Extract MITRE URL from external references."""
        for ref in obj.get('external_references', []):
            if ref.get('source_name') == 'mitre-attack':
                return ref.get('url')
        return None

    def extract_kill_chain_phases(self, obj: Dict) -> List[str]:
        """Extract kill chain phases (tactics)."""
        phases = []
        for phase in obj.get('kill_chain_phases', []):
            if phase.get('kill_chain_name') == 'mitre-attack':
                phases.append(phase.get('phase_name'))
        return phases

    def load_attack_patterns(self, session, objects: List[Dict]):
        """Load attack patterns (techniques)."""
        patterns = [obj for obj in objects if obj.get('type') == 'attack-pattern']
        logger.info(f"Loading {len(patterns)} attack patterns...")

        for obj in patterns:
            mitre_id = self.extract_mitre_id(obj)
            if not mitre_id:
                continue

            # Determine if it's a subtechnique
            is_subtechnique = '.' in mitre_id if mitre_id else False

            query = """
            MERGE (a:AttackPattern {stixId: $stixId})
            ON CREATE SET
                a.createdAt = datetime()
            SET
                a.name = $name,
                a.description = $description,
                a.mitreId = $mitreId,
                a.url = $url,
                a.isSubtechnique = $isSubtechnique,
                a.deprecated = $deprecated,
                a.revoked = $revoked,
                a.platforms = $platforms,
                a.detectionDescription = $detection,
                a.stixCreated = $created,
                a.stixModified = $modified,
                a.updatedAt = datetime()
            RETURN a
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:10000],
                'mitreId': mitre_id,
                'url': self.extract_url(obj),
                'isSubtechnique': is_subtechnique,
                'deprecated': obj.get('x_mitre_deprecated', False),
                'revoked': obj.get('revoked', False),
                'platforms': obj.get('x_mitre_platforms', []),
                'detection': (obj.get('x_mitre_detection', '') or '')[:5000],
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['attack_patterns'] += 1
                self.stix_id_map[obj.get('id')] = ('AttackPattern', mitre_id)

                # Link to tactics (kill chain phases)
                for phase in self.extract_kill_chain_phases(obj):
                    tactic_query = """
                    MATCH (a:AttackPattern {stixId: $stixId})
                    MATCH (t:Tactic {shortName: $shortName})
                    MERGE (a)-[:PART_OF_TACTIC]->(t)
                    """
                    session.run(tactic_query, {
                        'stixId': obj.get('id'),
                        'shortName': phase.replace('-', '_')
                    })
            except Exception as e:
                logger.debug(f"Attack pattern error: {e}")

    def load_tactics(self, session, objects: List[Dict]):
        """Load tactics (x-mitre-tactic)."""
        tactics = [obj for obj in objects if obj.get('type') == 'x-mitre-tactic']
        logger.info(f"Loading {len(tactics)} tactics...")

        for obj in tactics:
            query = """
            MERGE (t:Tactic {stixId: $stixId})
            ON CREATE SET
                t.createdAt = datetime()
            SET
                t.name = $name,
                t.description = $description,
                t.shortName = $shortName,
                t.mitreId = $mitreId,
                t.url = $url,
                t.stixCreated = $created,
                t.stixModified = $modified,
                t.updatedAt = datetime()
            RETURN t
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:5000],
                'shortName': obj.get('x_mitre_shortname', '').replace('-', '_'),
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['tactics'] += 1
                self.stix_id_map[obj.get('id')] = ('Tactic', obj.get('name'))
            except Exception as e:
                logger.debug(f"Tactic error: {e}")

    def load_malware(self, session, objects: List[Dict]):
        """Load malware objects."""
        malware = [obj for obj in objects if obj.get('type') == 'malware']
        logger.info(f"Loading {len(malware)} malware...")

        for obj in malware:
            query = """
            MERGE (m:Malware {stixId: $stixId})
            ON CREATE SET
                m.createdAt = datetime()
            SET
                m.name = $name,
                m.description = $description,
                m.mitreId = $mitreId,
                m.url = $url,
                m.aliases = $aliases,
                m.malwareTypes = $malwareTypes,
                m.platforms = $platforms,
                m.deprecated = $deprecated,
                m.revoked = $revoked,
                m.stixCreated = $created,
                m.stixModified = $modified,
                m.updatedAt = datetime()
            RETURN m
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:10000],
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'aliases': obj.get('x_mitre_aliases', []),
                'malwareTypes': obj.get('malware_types', []),
                'platforms': obj.get('x_mitre_platforms', []),
                'deprecated': obj.get('x_mitre_deprecated', False),
                'revoked': obj.get('revoked', False),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['malware'] += 1
                self.stix_id_map[obj.get('id')] = ('Malware', obj.get('name'))
            except Exception as e:
                logger.debug(f"Malware error: {e}")

    def load_tools(self, session, objects: List[Dict]):
        """Load tool objects."""
        tools = [obj for obj in objects if obj.get('type') == 'tool']
        logger.info(f"Loading {len(tools)} tools...")

        for obj in tools:
            query = """
            MERGE (t:Tool {stixId: $stixId})
            ON CREATE SET
                t.createdAt = datetime()
            SET
                t.name = $name,
                t.description = $description,
                t.mitreId = $mitreId,
                t.url = $url,
                t.aliases = $aliases,
                t.platforms = $platforms,
                t.deprecated = $deprecated,
                t.revoked = $revoked,
                t.stixCreated = $created,
                t.stixModified = $modified,
                t.updatedAt = datetime()
            RETURN t
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:10000],
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'aliases': obj.get('x_mitre_aliases', []),
                'platforms': obj.get('x_mitre_platforms', []),
                'deprecated': obj.get('x_mitre_deprecated', False),
                'revoked': obj.get('revoked', False),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['tools'] += 1
                self.stix_id_map[obj.get('id')] = ('Tool', obj.get('name'))
            except Exception as e:
                logger.debug(f"Tool error: {e}")

    def load_intrusion_sets(self, session, objects: List[Dict]):
        """Load intrusion sets (threat actor groups)."""
        intrusion_sets = [obj for obj in objects if obj.get('type') == 'intrusion-set']
        logger.info(f"Loading {len(intrusion_sets)} intrusion sets...")

        for obj in intrusion_sets:
            query = """
            MERGE (i:IntrusionSet:ThreatActor {stixId: $stixId})
            ON CREATE SET
                i.createdAt = datetime()
            SET
                i.name = $name,
                i.description = $description,
                i.mitreId = $mitreId,
                i.url = $url,
                i.aliases = $aliases,
                i.deprecated = $deprecated,
                i.revoked = $revoked,
                i.stixCreated = $created,
                i.stixModified = $modified,
                i.updatedAt = datetime()
            RETURN i
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:10000],
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'aliases': obj.get('aliases', []),
                'deprecated': obj.get('x_mitre_deprecated', False),
                'revoked': obj.get('revoked', False),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['intrusion_sets'] += 1
                self.stix_id_map[obj.get('id')] = ('IntrusionSet', obj.get('name'))
            except Exception as e:
                logger.debug(f"Intrusion set error: {e}")

    def load_campaigns(self, session, objects: List[Dict]):
        """Load campaign objects."""
        campaigns = [obj for obj in objects if obj.get('type') == 'campaign']
        logger.info(f"Loading {len(campaigns)} campaigns...")

        for obj in campaigns:
            query = """
            MERGE (c:Campaign {stixId: $stixId})
            ON CREATE SET
                c.createdAt = datetime()
            SET
                c.name = $name,
                c.description = $description,
                c.mitreId = $mitreId,
                c.url = $url,
                c.aliases = $aliases,
                c.firstSeen = $firstSeen,
                c.lastSeen = $lastSeen,
                c.deprecated = $deprecated,
                c.revoked = $revoked,
                c.stixCreated = $created,
                c.stixModified = $modified,
                c.updatedAt = datetime()
            RETURN c
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:10000],
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'aliases': obj.get('aliases', []),
                'firstSeen': obj.get('first_seen'),
                'lastSeen': obj.get('last_seen'),
                'deprecated': obj.get('x_mitre_deprecated', False),
                'revoked': obj.get('revoked', False),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['campaigns'] += 1
                self.stix_id_map[obj.get('id')] = ('Campaign', obj.get('name'))
            except Exception as e:
                logger.debug(f"Campaign error: {e}")

    def load_data_sources(self, session, objects: List[Dict]):
        """Load data source objects."""
        data_sources = [obj for obj in objects if obj.get('type') == 'x-mitre-data-source']
        logger.info(f"Loading {len(data_sources)} data sources...")

        for obj in data_sources:
            query = """
            MERGE (d:DataSource {stixId: $stixId})
            ON CREATE SET
                d.createdAt = datetime()
            SET
                d.name = $name,
                d.description = $description,
                d.mitreId = $mitreId,
                d.url = $url,
                d.platforms = $platforms,
                d.collectionLayers = $collectionLayers,
                d.stixCreated = $created,
                d.stixModified = $modified,
                d.updatedAt = datetime()
            RETURN d
            """

            params = {
                'stixId': obj.get('id'),
                'name': obj.get('name'),
                'description': (obj.get('description', '') or '')[:5000],
                'mitreId': self.extract_mitre_id(obj),
                'url': self.extract_url(obj),
                'platforms': obj.get('x_mitre_platforms', []),
                'collectionLayers': obj.get('x_mitre_collection_layers', []),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                session.run(query, params)
                self.stats['data_sources'] += 1
                self.stix_id_map[obj.get('id')] = ('DataSource', obj.get('name'))
            except Exception as e:
                logger.debug(f"Data source error: {e}")

    def load_relationships(self, session, objects: List[Dict]):
        """Load STIX relationships between objects."""
        relationships = [obj for obj in objects if obj.get('type') == 'relationship']
        logger.info(f"Loading {len(relationships)} relationships...")

        # Relationship type mapping for Neo4j
        rel_mapping = {
            'uses': 'USES',
            'mitigates': 'MITIGATES',
            'targets': 'TARGETS',
            'attributed-to': 'ATTRIBUTED_TO',
            'subtechnique-of': 'SUBTECHNIQUE_OF',
            'detects': 'DETECTS',
            'related-to': 'RELATED_TO',
            'revoked-by': 'REVOKED_BY'
        }

        for obj in relationships:
            rel_type = obj.get('relationship_type', 'related-to')
            neo4j_rel = rel_mapping.get(rel_type, 'RELATED_TO')

            source_ref = obj.get('source_ref')
            target_ref = obj.get('target_ref')

            if not source_ref or not target_ref:
                continue

            # Generic relationship query that works across all node types
            query = f"""
            MATCH (source {{stixId: $sourceRef}})
            MATCH (target {{stixId: $targetRef}})
            MERGE (source)-[r:{neo4j_rel}]->(target)
            SET r.stixId = $stixId,
                r.description = $description,
                r.stixCreated = $created,
                r.stixModified = $modified
            RETURN type(r) as relType
            """

            params = {
                'sourceRef': source_ref,
                'targetRef': target_ref,
                'stixId': obj.get('id'),
                'description': (obj.get('description', '') or '')[:2000],
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }

            try:
                result = session.run(query, params)
                if result.single():
                    self.stats['relationships'] += 1
            except Exception as e:
                logger.debug(f"Relationship error: {e}")

    def load_bundle(self, filepath: str):
        """Load a STIX bundle from a JSON file."""
        logger.info(f"Loading STIX bundle from: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        objects = data.get('objects', [])
        total = len(objects)
        logger.info(f"Found {total} STIX objects")

        with self.driver.session() as session:
            # Load objects in order (tactics first, then nodes, then relationships)
            self.load_tactics(session, objects)
            self.load_attack_patterns(session, objects)
            self.load_malware(session, objects)
            self.load_tools(session, objects)
            self.load_intrusion_sets(session, objects)
            self.load_campaigns(session, objects)
            self.load_data_sources(session, objects)
            self.load_relationships(session, objects)

        self.stats['objects_processed'] = total
        logger.info(f"Completed loading STIX bundle")

    def link_cves(self, session):
        """Link CVEs to attack patterns based on CWE relationships."""
        logger.info("Linking CVEs to attack patterns via CWE...")

        # This creates links where attack patterns and CVEs share common CWEs
        query = """
        MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)
        MATCH (ap:AttackPattern)
        WHERE ap.description CONTAINS cwe.cweId
        MERGE (cve)-[r:RELATED_TO_ATTACK]->(ap)
        SET r.linkMethod = 'cwe_description_match',
            r.cweId = cwe.cweId
        RETURN count(r) as links
        """

        try:
            result = session.run(query)
            links = result.single()['links']
            logger.info(f"Created {links} CVE-to-AttackPattern links")
        except Exception as e:
            logger.warning(f"CVE linking warning: {e}")

    def print_stats(self):
        """Print loading statistics."""
        print("\n" + "="*50)
        print("STIX Loading Statistics")
        print("="*50)
        print(f"Objects processed:   {self.stats['objects_processed']}")
        print(f"Attack patterns:     {self.stats['attack_patterns']}")
        print(f"Malware:             {self.stats['malware']}")
        print(f"Tools:               {self.stats['tools']}")
        print(f"Intrusion sets:      {self.stats['intrusion_sets']}")
        print(f"Campaigns:           {self.stats['campaigns']}")
        print(f"Tactics:             {self.stats['tactics']}")
        print(f"Data sources:        {self.stats['data_sources']}")
        print(f"Relationships:       {self.stats['relationships']}")
        if self.stats['errors']:
            print(f"Errors:              {len(self.stats['errors'])}")
        print("="*50)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 load_stix_attack.py <stix_bundle.json>")
        print("\nExample:")
        print("  NEO4J_PASSWORD='password' python3 load_stix_attack.py enterprise-attack.json")
        sys.exit(1)

    # Get Neo4j connection settings
    uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    user = os.environ.get('NEO4J_USER', 'neo4j')
    password = os.environ.get('NEO4J_PASSWORD', 'neo4j@openspg')

    logger.info(f"Connecting to Neo4j at {uri}")

    try:
        loader = STIXLoader(uri, user, password)

        # Create indexes first
        logger.info("Creating indexes...")
        loader.create_indexes()

        # Load each bundle
        for filepath in sys.argv[1:]:
            if os.path.exists(filepath):
                loader.load_bundle(filepath)
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
