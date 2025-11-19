#!/usr/bin/env python3
"""
Threat Intelligence Importer - Complete implementation for importing STIX/TAXII threat intel
Handles ThreatActor, Campaign, IoC creation, sector/geography filtering, confidence scoring.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import requests
from neo4j import GraphDatabase, Driver
from tqdm import tqdm
from stix2 import FileSystemSource, Filter
from taxii2client.v20 import Server, Collection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('threat_intel_importer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ImportMetrics:
    """Track import statistics"""
    threat_actors: int = 0
    campaigns: int = 0
    indicators: int = 0
    attack_patterns: int = 0
    malware: int = 0
    tools: int = 0
    relationships: int = 0
    errors: int = 0


class ThreatIntelImporter:
    """Import threat intelligence from STIX/TAXII feeds into Neo4j"""

    # Confidence levels
    CONFIDENCE_LEVELS = {
        'high': 0.8,
        'medium': 0.5,
        'low': 0.3,
        'unknown': 0.0
    }

    # Supported indicator types
    INDICATOR_TYPES = [
        'ipv4-addr', 'ipv6-addr', 'domain-name', 'url',
        'file', 'email-addr', 'mutex', 'windows-registry-key'
    ]

    # Industry sectors for filtering
    RAILWAY_SECTORS = [
        'transportation', 'rail', 'critical-infrastructure',
        'industrial-control-systems', 'ics', 'scada'
    ]

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize threat intelligence importer

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.metrics = ImportMetrics()
        self._verify_connection()
        self._create_indexes()

        # Cache for relationship mapping
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
            "CREATE CONSTRAINT threat_actor_id IF NOT EXISTS FOR (t:ThreatActor) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (c:Campaign) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT indicator_id IF NOT EXISTS FOR (i:Indicator) REQUIRE i.id IS UNIQUE",
            "CREATE INDEX threat_actor_name IF NOT EXISTS FOR (t:ThreatActor) ON (t.name)",
            "CREATE INDEX campaign_name IF NOT EXISTS FOR (c:Campaign) ON (c.name)",
            "CREATE INDEX indicator_pattern IF NOT EXISTS FOR (i:Indicator) ON (i.pattern)",
            "CREATE INDEX indicator_type IF NOT EXISTS FOR (i:Indicator) ON (i.indicator_type)",
        ]

        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"Created index/constraint: {index_query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")

    def fetch_from_taxii(self, server_url: str, collection_id: str,
                        api_root: str = 'taxii/',
                        username: Optional[str] = None,
                        password: Optional[str] = None) -> List[Dict]:
        """
        Fetch threat intelligence from TAXII 2.0 server

        Args:
            server_url: TAXII server URL
            collection_id: Collection ID to fetch from
            api_root: API root path
            username: Optional username for authentication
            password: Optional password for authentication

        Returns:
            List of STIX objects
        """
        logger.info(f"Fetching from TAXII server: {server_url}")

        try:
            # Connect to TAXII server
            if username and password:
                server = Server(server_url, user=username, password=password)
            else:
                server = Server(server_url)

            # Get API root
            api_root_obj = server.api_roots[0] if server.api_roots else None
            if not api_root_obj:
                raise ValueError("No API root found")

            # Get collection
            collection = None
            for coll in api_root_obj.collections:
                if coll.id == collection_id or coll.title == collection_id:
                    collection = coll
                    break

            if not collection:
                raise ValueError(f"Collection not found: {collection_id}")

            logger.info(f"Found collection: {collection.title}")

            # Fetch objects
            objects = collection.get_objects()
            stix_objects = objects.get('objects', [])

            logger.info(f"Fetched {len(stix_objects)} STIX objects from TAXII")
            return stix_objects

        except Exception as e:
            logger.error(f"Failed to fetch from TAXII: {e}")
            raise

    def load_from_stix_bundle(self, bundle_path: str) -> List[Dict]:
        """
        Load STIX bundle from file

        Args:
            bundle_path: Path to STIX bundle JSON file

        Returns:
            List of STIX objects
        """
        logger.info(f"Loading STIX bundle from {bundle_path}")

        try:
            with open(bundle_path, 'r', encoding='utf-8') as f:
                bundle = json.load(f)

            objects = bundle.get('objects', [])
            logger.info(f"Loaded {len(objects)} STIX objects from bundle")
            return objects

        except Exception as e:
            logger.error(f"Failed to load STIX bundle: {e}")
            raise

    def _extract_confidence(self, obj: Dict) -> float:
        """Extract and normalize confidence score"""
        confidence = obj.get('confidence', 0)

        # STIX 2.1 uses 0-100 scale
        if isinstance(confidence, int):
            return confidence / 100.0

        # STIX 2.0 uses string values
        if isinstance(confidence, str):
            return self.CONFIDENCE_LEVELS.get(confidence.lower(), 0.0)

        return 0.5  # Default to medium confidence

    def _extract_labels(self, obj: Dict) -> List[str]:
        """Extract labels from STIX object"""
        return obj.get('labels', [])

    def _extract_external_references(self, obj: Dict) -> List[Dict]:
        """Extract external references"""
        refs = []
        for ref in obj.get('external_references', []):
            refs.append({
                'source_name': ref.get('source_name', ''),
                'url': ref.get('url', ''),
                'description': ref.get('description', '')
            })
        return refs

    def _parse_threat_actors(self, objects: List[Dict]) -> List[Dict]:
        """Parse threat actor objects"""
        threat_actors = []

        for obj in objects:
            if obj.get('type') == 'threat-actor':
                threat_actors.append({
                    'id': obj['id'],
                    'name': obj.get('name', 'Unknown'),
                    'description': obj.get('description', ''),
                    'labels': self._extract_labels(obj),
                    'aliases': obj.get('aliases', []),
                    'first_seen': obj.get('first_seen'),
                    'last_seen': obj.get('last_seen'),
                    'goals': obj.get('goals', []),
                    'sophistication': obj.get('sophistication', 'unknown'),
                    'resource_level': obj.get('resource_level', 'unknown'),
                    'primary_motivation': obj.get('primary_motivation', 'unknown'),
                    'confidence': self._extract_confidence(obj),
                    'external_refs': self._extract_external_references(obj)
                })

                self.stix_id_map[obj['id']] = obj.get('name', obj['id'])

        logger.info(f"Parsed {len(threat_actors)} threat actors")
        return threat_actors

    def _parse_campaigns(self, objects: List[Dict]) -> List[Dict]:
        """Parse campaign objects"""
        campaigns = []

        for obj in objects:
            if obj.get('type') == 'campaign':
                campaigns.append({
                    'id': obj['id'],
                    'name': obj.get('name', 'Unknown'),
                    'description': obj.get('description', ''),
                    'first_seen': obj.get('first_seen'),
                    'last_seen': obj.get('last_seen'),
                    'objective': obj.get('objective', ''),
                    'confidence': self._extract_confidence(obj),
                    'external_refs': self._extract_external_references(obj)
                })

                self.stix_id_map[obj['id']] = obj.get('name', obj['id'])

        logger.info(f"Parsed {len(campaigns)} campaigns")
        return campaigns

    def _parse_indicators(self, objects: List[Dict]) -> List[Dict]:
        """Parse indicator objects"""
        indicators = []

        for obj in objects:
            if obj.get('type') == 'indicator':
                # Extract indicator type from pattern
                pattern = obj.get('pattern', '')
                indicator_type = self._extract_indicator_type(pattern)

                indicators.append({
                    'id': obj['id'],
                    'name': obj.get('name', 'Unknown'),
                    'description': obj.get('description', ''),
                    'pattern': pattern,
                    'indicator_type': indicator_type,
                    'valid_from': obj.get('valid_from'),
                    'valid_until': obj.get('valid_until'),
                    'labels': self._extract_labels(obj),
                    'confidence': self._extract_confidence(obj)
                })

                self.stix_id_map[obj['id']] = pattern

        logger.info(f"Parsed {len(indicators)} indicators")
        return indicators

    def _extract_indicator_type(self, pattern: str) -> str:
        """Extract indicator type from STIX pattern"""
        for ioc_type in self.INDICATOR_TYPES:
            if ioc_type in pattern:
                return ioc_type
        return 'unknown'

    def _parse_relationships(self, objects: List[Dict]) -> List[Dict]:
        """Parse relationship objects"""
        relationships = []

        for obj in objects:
            if obj.get('type') == 'relationship':
                source_ref = obj.get('source_ref')
                target_ref = obj.get('target_ref')

                if source_ref and target_ref:
                    relationships.append({
                        'source_id': source_ref,
                        'target_id': target_ref,
                        'relationship_type': obj.get('relationship_type'),
                        'description': obj.get('description', '')
                    })

        logger.info(f"Parsed {len(relationships)} relationships")
        return relationships

    def filter_by_sector(self, objects: List[Dict], sectors: Set[str]) -> List[Dict]:
        """
        Filter STIX objects by relevant sectors

        Args:
            objects: List of STIX objects
            sectors: Set of relevant sectors

        Returns:
            Filtered list of STIX objects
        """
        filtered = []

        for obj in objects:
            # Check labels
            labels = set(label.lower() for label in obj.get('labels', []))
            if labels & sectors:
                filtered.append(obj)
                continue

            # Check description
            description = obj.get('description', '').lower()
            if any(sector in description for sector in sectors):
                filtered.append(obj)

        logger.info(f"Filtered to {len(filtered)} objects relevant to sectors: {sectors}")
        return filtered

    def import_threat_actors(self, threat_actors: List[Dict]):
        """Import threat actors into Neo4j"""
        if not threat_actors:
            return

        cypher = """
        UNWIND $actors as actor
        MERGE (t:ThreatActor {id: actor.id})
        SET t.name = actor.name,
            t.description = actor.description,
            t.labels = actor.labels,
            t.aliases = actor.aliases,
            t.first_seen = datetime(actor.first_seen),
            t.last_seen = datetime(actor.last_seen),
            t.goals = actor.goals,
            t.sophistication = actor.sophistication,
            t.resource_level = actor.resource_level,
            t.primary_motivation = actor.primary_motivation,
            t.confidence = actor.confidence,
            t.source = 'STIX_FEED',
            t.lastImported = datetime()

        WITH t, actor
        UNWIND actor.external_refs as ref
        MERGE (r:Reference {url: ref.url})
        SET r.source = ref.source_name,
            r.description = ref.description
        MERGE (t)-[:HAS_REFERENCE]->(r)
        """

        with self.driver.session() as session:
            session.run(cypher, actors=threat_actors)
            self.metrics.threat_actors = len(threat_actors)

        logger.info(f"Imported {len(threat_actors)} threat actors")

    def import_campaigns(self, campaigns: List[Dict]):
        """Import campaigns into Neo4j"""
        if not campaigns:
            return

        cypher = """
        UNWIND $campaigns as camp
        MERGE (c:Campaign {id: camp.id})
        SET c.name = camp.name,
            c.description = camp.description,
            c.first_seen = datetime(camp.first_seen),
            c.last_seen = datetime(camp.last_seen),
            c.objective = camp.objective,
            c.confidence = camp.confidence,
            c.lastImported = datetime()

        WITH c, camp
        UNWIND camp.external_refs as ref
        MERGE (r:Reference {url: ref.url})
        SET r.source = ref.source_name,
            r.description = ref.description
        MERGE (c)-[:HAS_REFERENCE]->(r)
        """

        with self.driver.session() as session:
            session.run(cypher, campaigns=campaigns)
            self.metrics.campaigns = len(campaigns)

        logger.info(f"Imported {len(campaigns)} campaigns")

    def import_indicators(self, indicators: List[Dict]):
        """Import indicators of compromise into Neo4j"""
        if not indicators:
            return

        cypher = """
        UNWIND $indicators as ind
        MERGE (i:Indicator {id: ind.id})
        SET i.name = ind.name,
            i.description = ind.description,
            i.pattern = ind.pattern,
            i.indicator_type = ind.indicator_type,
            i.valid_from = datetime(ind.valid_from),
            i.valid_until = datetime(ind.valid_until),
            i.labels = ind.labels,
            i.confidence = ind.confidence,
            i.lastImported = datetime()
        """

        with self.driver.session() as session:
            with tqdm(total=len(indicators), desc="Importing indicators") as pbar:
                batch_size = 1000
                for i in range(0, len(indicators), batch_size):
                    batch = indicators[i:i + batch_size]
                    session.run(cypher, indicators=batch)
                    pbar.update(len(batch))

            self.metrics.indicators = len(indicators)

        logger.info(f"Imported {len(indicators)} indicators")

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

    def import_full_feed(self, objects: List[Dict],
                        filter_sectors: bool = True):
        """
        Import full threat intelligence feed

        Args:
            objects: List of STIX objects
            filter_sectors: Whether to filter by railway-relevant sectors
        """
        logger.info(f"Starting import of {len(objects)} STIX objects")

        # Filter by sector if requested
        if filter_sectors:
            objects = self.filter_by_sector(objects, set(self.RAILWAY_SECTORS))

        # Parse objects
        threat_actors = self._parse_threat_actors(objects)
        campaigns = self._parse_campaigns(objects)
        indicators = self._parse_indicators(objects)
        relationships = self._parse_relationships(objects)

        # Import in order
        self.import_threat_actors(threat_actors)
        self.import_campaigns(campaigns)
        self.import_indicators(indicators)
        self.import_relationships(relationships)

        logger.info("Import complete")

    def get_metrics(self) -> ImportMetrics:
        """Return import metrics"""
        return self.metrics

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("Threat intelligence importer closed")


def main():
    """Main execution function"""
    # Configuration from environment or defaults
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # Initialize importer
    importer = ThreatIntelImporter(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD
    )

    try:
        # Example: Load from STIX bundle
        bundle_path = 'threat_intel_bundle.json'
        if os.path.exists(bundle_path):
            objects = importer.load_from_stix_bundle(bundle_path)
            importer.import_full_feed(objects, filter_sectors=True)

        # Print metrics
        metrics = importer.get_metrics()
        logger.info(f"""
        Import Metrics:
        - Threat Actors: {metrics.threat_actors}
        - Campaigns: {metrics.campaigns}
        - Indicators: {metrics.indicators}
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
