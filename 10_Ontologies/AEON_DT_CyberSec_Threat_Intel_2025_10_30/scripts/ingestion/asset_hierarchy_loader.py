#!/usr/bin/env python3
"""
Asset Hierarchy Loader - Complete implementation for loading organizational asset hierarchies
Handles CSV/JSON/API imports, Organization→Site→Train→Component modeling, criticality assignment.
"""

import os
import sys
import json
import csv
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import requests
from neo4j import GraphDatabase, Driver
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('asset_loader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Asset:
    """Asset data structure"""
    id: str
    name: str
    type: str
    parent_id: Optional[str] = None
    criticality: Optional[str] = None
    status: str = 'active'
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImportMetrics:
    """Track import statistics"""
    organizations: int = 0
    sites: int = 0
    trains: int = 0
    components: int = 0
    software: int = 0
    relationships: int = 0
    duplicates: int = 0
    errors: int = 0


class AssetHierarchyLoader:
    """Load organizational asset hierarchies into Neo4j"""

    # Criticality levels based on IEC 62443
    CRITICALITY_LEVELS = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']

    # Asset types
    ASSET_TYPES = {
        'organization': 'Organization',
        'site': 'Site',
        'train': 'Train',
        'system': 'System',
        'component': 'Component',
        'plc': 'PLC',
        'hmi': 'HMI',
        'scada': 'SCADA',
        'server': 'Server',
        'workstation': 'Workstation',
        'network_device': 'NetworkDevice'
    }

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize asset hierarchy loader

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.metrics = ImportMetrics()
        self._verify_connection()
        self._create_indexes()

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
            "CREATE CONSTRAINT org_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE",
            "CREATE CONSTRAINT site_id IF NOT EXISTS FOR (s:Site) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT train_id IF NOT EXISTS FOR (t:Train) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT component_id IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE",
            "CREATE INDEX asset_criticality IF NOT EXISTS FOR (a:Asset) ON (a.criticality)",
            "CREATE INDEX asset_status IF NOT EXISTS FOR (a:Asset) ON (a.status)",
            "CREATE INDEX component_type IF NOT EXISTS FOR (c:Component) ON (c.type)",
        ]

        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"Created index/constraint: {index_query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")

    def load_from_csv(self, csv_path: str) -> List[Asset]:
        """
        Load assets from CSV file

        Expected CSV format:
        id,name,type,parent_id,criticality,status,properties

        Args:
            csv_path: Path to CSV file

        Returns:
            List of Asset objects
        """
        assets = []

        logger.info(f"Loading assets from CSV: {csv_path}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Parse properties JSON if present
                    properties = {}
                    if 'properties' in row and row['properties']:
                        try:
                            properties = json.loads(row['properties'])
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON in properties for {row.get('id')}")

                    asset = Asset(
                        id=row['id'],
                        name=row['name'],
                        type=row['type'],
                        parent_id=row.get('parent_id') or None,
                        criticality=row.get('criticality') or None,
                        status=row.get('status', 'active'),
                        properties=properties
                    )
                    assets.append(asset)

            logger.info(f"Loaded {len(assets)} assets from CSV")
            return assets

        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise

    def load_from_json(self, json_path: str) -> List[Asset]:
        """
        Load assets from JSON file

        Expected JSON format:
        {
            "assets": [
                {
                    "id": "ORG-001",
                    "name": "Railway Corp",
                    "type": "organization",
                    "criticality": "CRITICAL",
                    "properties": {...}
                },
                ...
            ]
        }

        Args:
            json_path: Path to JSON file

        Returns:
            List of Asset objects
        """
        assets = []

        logger.info(f"Loading assets from JSON: {json_path}")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            asset_data = data.get('assets', [])

            for item in asset_data:
                asset = Asset(
                    id=item['id'],
                    name=item['name'],
                    type=item['type'],
                    parent_id=item.get('parent_id'),
                    criticality=item.get('criticality'),
                    status=item.get('status', 'active'),
                    properties=item.get('properties', {})
                )
                assets.append(asset)

            logger.info(f"Loaded {len(assets)} assets from JSON")
            return assets

        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            raise

    def load_from_api(self, api_url: str, api_key: Optional[str] = None) -> List[Asset]:
        """
        Load assets from REST API

        Args:
            api_url: API endpoint URL
            api_key: Optional API key for authentication

        Returns:
            List of Asset objects
        """
        assets = []

        logger.info(f"Loading assets from API: {api_url}")

        headers = {}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"

        try:
            response = requests.get(api_url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            asset_data = data.get('assets', [])

            for item in asset_data:
                asset = Asset(
                    id=item['id'],
                    name=item['name'],
                    type=item['type'],
                    parent_id=item.get('parent_id'),
                    criticality=item.get('criticality'),
                    status=item.get('status', 'active'),
                    properties=item.get('properties', {})
                )
                assets.append(asset)

            logger.info(f"Loaded {len(assets)} assets from API")
            return assets

        except Exception as e:
            logger.error(f"Failed to load from API: {e}")
            raise

    def calculate_criticality(self, asset: Asset, parent_criticality: Optional[str] = None) -> str:
        """
        Calculate asset criticality using inheritance and business rules

        Args:
            asset: Asset to calculate criticality for
            parent_criticality: Parent asset criticality for inheritance

        Returns:
            Criticality level
        """
        # If explicitly set, use it
        if asset.criticality and asset.criticality in self.CRITICALITY_LEVELS:
            return asset.criticality

        # Inherit from parent if available
        if parent_criticality:
            # Trains and Sites inherit parent criticality
            if asset.type in ['site', 'train']:
                return parent_criticality

        # Business rules for automatic assignment
        if asset.type == 'organization':
            return 'CRITICAL'

        # Railway-specific criticality rules
        asset_name_lower = asset.name.lower()
        asset_type_lower = asset.type.lower()

        # Safety-critical systems
        if any(keyword in asset_name_lower for keyword in ['signaling', 'control', 'safety', 'braking']):
            return 'CRITICAL'

        # Operational systems
        if any(keyword in asset_name_lower for keyword in ['traction', 'power', 'communication']):
            return 'HIGH'

        # Type-based rules
        if asset_type_lower in ['plc', 'scada', 'hmi']:
            return 'HIGH'

        if asset_type_lower in ['server', 'network_device']:
            return 'MEDIUM'

        # Default to MEDIUM for unknown
        return 'MEDIUM'

    def validate_asset(self, asset: Asset) -> Tuple[bool, Optional[str]]:
        """
        Validate asset data

        Args:
            asset: Asset to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        if not asset.id:
            return False, "Missing asset ID"

        if not asset.name:
            return False, "Missing asset name"

        if not asset.type:
            return False, "Missing asset type"

        # Validate type
        if asset.type not in self.ASSET_TYPES:
            return False, f"Invalid asset type: {asset.type}"

        # Validate criticality if set
        if asset.criticality and asset.criticality not in self.CRITICALITY_LEVELS:
            return False, f"Invalid criticality: {asset.criticality}"

        return True, None

    def detect_duplicates(self, assets: List[Asset]) -> Dict[str, List[Asset]]:
        """
        Detect duplicate assets by ID

        Args:
            assets: List of assets to check

        Returns:
            Dictionary mapping duplicate IDs to list of duplicate assets
        """
        id_map = {}
        duplicates = {}

        for asset in assets:
            if asset.id in id_map:
                if asset.id not in duplicates:
                    duplicates[asset.id] = [id_map[asset.id]]
                duplicates[asset.id].append(asset)
            else:
                id_map[asset.id] = asset

        if duplicates:
            logger.warning(f"Found {len(duplicates)} duplicate asset IDs")

        return duplicates

    def merge_duplicate_assets(self, duplicates: List[Asset]) -> Asset:
        """
        Merge duplicate assets, preferring more complete data

        Args:
            duplicates: List of duplicate assets

        Returns:
            Merged asset
        """
        # Start with first asset
        merged = duplicates[0]

        # Merge properties from other duplicates
        for dup in duplicates[1:]:
            # Prefer non-null values
            if dup.criticality and not merged.criticality:
                merged.criticality = dup.criticality

            if dup.parent_id and not merged.parent_id:
                merged.parent_id = dup.parent_id

            # Merge properties
            merged.properties.update(dup.properties)

        return merged

    def import_assets(self, assets: List[Asset], batch_size: int = 1000):
        """
        Import assets into Neo4j with hierarchy relationships

        Args:
            assets: List of assets to import
            batch_size: Number of assets per batch
        """
        if not assets:
            logger.warning("No assets to import")
            return

        # Validate all assets
        valid_assets = []
        for asset in assets:
            is_valid, error = self.validate_asset(asset)
            if is_valid:
                valid_assets.append(asset)
            else:
                logger.error(f"Invalid asset {asset.id}: {error}")
                self.metrics.errors += 1

        # Detect and merge duplicates
        duplicates = self.detect_duplicates(valid_assets)
        if duplicates:
            self.metrics.duplicates = len(duplicates)

            # Merge duplicates
            merged_assets = []
            processed_ids = set()

            for asset in valid_assets:
                if asset.id in processed_ids:
                    continue

                if asset.id in duplicates:
                    merged = self.merge_duplicate_assets(duplicates[asset.id])
                    merged_assets.append(merged)
                    processed_ids.add(asset.id)
                else:
                    merged_assets.append(asset)
                    processed_ids.add(asset.id)

            valid_assets = merged_assets

        # Calculate criticality for all assets
        asset_map = {a.id: a for a in valid_assets}

        for asset in valid_assets:
            parent_criticality = None
            if asset.parent_id and asset.parent_id in asset_map:
                parent = asset_map[asset.parent_id]
                parent_criticality = parent.criticality

            asset.criticality = self.calculate_criticality(asset, parent_criticality)

        # Prepare data for Neo4j
        asset_data = []
        for asset in valid_assets:
            asset_data.append({
                'id': asset.id,
                'name': asset.name,
                'type': asset.type,
                'label': self.ASSET_TYPES.get(asset.type, 'Asset'),
                'parent_id': asset.parent_id,
                'criticality': asset.criticality,
                'status': asset.status,
                'properties': json.dumps(asset.properties)
            })

        # Import in batches
        cypher = """
        UNWIND $batch as asset
        CALL apoc.create.node([asset.label, 'Asset'], {
            id: asset.id,
            name: asset.name,
            type: asset.type,
            criticality: asset.criticality,
            status: asset.status,
            properties: asset.properties,
            lastImported: datetime()
        }) YIELD node

        WITH node, asset
        WHERE asset.parent_id IS NOT NULL
        MATCH (parent:Asset {id: asset.parent_id})
        MERGE (node)-[:BELONGS_TO]->(parent)

        RETURN count(node) as imported
        """

        with self.driver.session() as session:
            total_batches = (len(asset_data) + batch_size - 1) // batch_size

            with tqdm(total=len(asset_data), desc="Importing assets") as pbar:
                for i in range(0, len(asset_data), batch_size):
                    batch = asset_data[i:i + batch_size]

                    try:
                        result = session.run(cypher, batch=batch)
                        count = result.single()['imported']

                        # Update metrics by type
                        for asset_dict in batch:
                            asset_type = asset_dict['type']
                            if asset_type == 'organization':
                                self.metrics.organizations += 1
                            elif asset_type == 'site':
                                self.metrics.sites += 1
                            elif asset_type == 'train':
                                self.metrics.trains += 1
                            else:
                                self.metrics.components += 1

                        pbar.update(len(batch))

                    except Exception as e:
                        logger.error(f"Batch import failed: {e}")
                        self.metrics.errors += len(batch)

        logger.info(f"Import complete: {len(asset_data)} assets processed")

    def link_to_software(self, cpe_mapping_file: Optional[str] = None):
        """
        Link components to software using CPE matching

        Args:
            cpe_mapping_file: Optional CSV file with asset_id,cpe_uri mappings
        """
        if cpe_mapping_file:
            logger.info(f"Loading CPE mappings from {cpe_mapping_file}")

            mappings = []
            with open(cpe_mapping_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    mappings.append({
                        'asset_id': row['asset_id'],
                        'cpe_uri': row['cpe_uri']
                    })

            cypher = """
            UNWIND $mappings as mapping
            MATCH (asset:Component {id: mapping.asset_id})
            MATCH (cpe:CPE {uri: mapping.cpe_uri})
            MERGE (asset)-[:RUNS_SOFTWARE]->(cpe)
            """

            with self.driver.session() as session:
                session.run(cypher, mappings=mappings)

            logger.info(f"Linked {len(mappings)} components to software")

    def get_metrics(self) -> ImportMetrics:
        """Return import metrics"""
        return self.metrics

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("Asset hierarchy loader closed")


def main():
    """Main execution function"""
    # Configuration from environment or defaults
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # Initialize loader
    loader = AssetHierarchyLoader(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD
    )

    try:
        # Example: Load from CSV
        csv_path = 'assets.csv'
        if Path(csv_path).exists():
            assets = loader.load_from_csv(csv_path)
            loader.import_assets(assets)

        # Print metrics
        metrics = loader.get_metrics()
        logger.info(f"""
        Import Metrics:
        - Organizations: {metrics.organizations}
        - Sites: {metrics.sites}
        - Trains: {metrics.trains}
        - Components: {metrics.components}
        - Duplicates Merged: {metrics.duplicates}
        - Errors: {metrics.errors}
        """)

    except Exception as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    finally:
        loader.close()


if __name__ == "__main__":
    main()
