#!/usr/bin/env python3
"""
Phase 4a: Reconstruct THREATENS_GRID_STABILITY Relationships
Restores 3,000 critical infrastructure relationships from metadata export

File: phase4a_reconstruct_grid_stability.py
Created: 2025-11-01 22:56:00
Version: 1.0.0
Author: Automation Agent
Purpose: Reconstruct THREATENS_GRID_STABILITY relationships after CVE cleanup
Status: ACTIVE
"""

import json
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any
from neo4j import GraphDatabase
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'../logs/phase4a_reconstruct_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GridStabilityReconstructor:
    """Reconstructs THREATENS_GRID_STABILITY relationships from export"""

    def __init__(self, config_path: str = '../config.yaml'):
        """Initialize with configuration"""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.driver = GraphDatabase.driver(
            config['neo4j']['uri'],
            auth=(config['neo4j']['user'], config['neo4j']['password'])
        )

        self.export_dir = Path('../../exports/metadata_export_2025-11-01_22-06-17')
        self.stats = {
            'total_relationships': 0,
            'reconstructed': 0,
            'skipped_no_cve': 0,
            'skipped_no_source': 0,
            'errors': 0
        }

    def load_export_data(self) -> List[Dict[str, Any]]:
        """Load THREATENS_GRID_STABILITY export"""
        export_file = self.export_dir / 'threatens_grid_stability.json'

        if not export_file.exists():
            raise FileNotFoundError(f"Export file not found: {export_file}")

        logger.info(f"Loading export from: {export_file}")
        with open(export_file) as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} relationship records")
        return data

    def reconstruct_relationship(self, session, record: Dict[str, Any]) -> bool:
        """
        Reconstruct single THREATENS_GRID_STABILITY relationship

        Returns True if successful, False otherwise
        """
        # Extract relationship properties from all_properties
        props = record.get('all_properties', {})

        # Get source node info
        source_node_id = record.get('source_node_id')
        source_label = record.get('source_label')

        # Get CVE ID - check both direct field and properties
        cve_id = record.get('cve_id')
        if not cve_id and 'cve_id' in props:
            cve_id = props['cve_id']

        if not cve_id:
            self.stats['skipped_no_cve'] += 1
            logger.warning(f"No CVE ID found for source_node_id: {source_node_id}")
            return False

        if not source_node_id:
            self.stats['skipped_no_source'] += 1
            logger.warning(f"No source node ID for CVE: {cve_id}")
            return False

        # Reconstruct relationship with all original properties
        query = """
        MATCH (source) WHERE id(source) = $source_node_id
        MATCH (cve:CVE {id: $cve_id})
        MERGE (source)-[r:THREATENS_GRID_STABILITY]->(cve)
        SET r = $properties
        RETURN id(r) as relationship_id
        """

        try:
            result = session.run(query,
                source_node_id=source_node_id,
                cve_id=cve_id,
                properties=props
            )

            if result.single():
                self.stats['reconstructed'] += 1
                return True
            else:
                logger.warning(f"Failed to create relationship for CVE: {cve_id}, source: {source_node_id}")
                self.stats['errors'] += 1
                return False

        except Exception as e:
            logger.error(f"Error reconstructing relationship for CVE {cve_id}: {str(e)}")
            self.stats['errors'] += 1
            return False

    def reconstruct_all(self) -> Dict[str, int]:
        """Reconstruct all THREATENS_GRID_STABILITY relationships"""
        logger.info("="*80)
        logger.info("PHASE 4A: THREATENS_GRID_STABILITY RECONSTRUCTION")
        logger.info("="*80)

        # Load export data
        relationships = self.load_export_data()
        self.stats['total_relationships'] = len(relationships)

        # Reconstruct in batches
        batch_size = 1000
        with self.driver.session() as session:
            for i in range(0, len(relationships), batch_size):
                batch = relationships[i:i+batch_size]
                logger.info(f"Processing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, len(relationships))} of {len(relationships)})")

                for record in batch:
                    self.reconstruct_relationship(session, record)

        # Log final statistics
        logger.info("="*80)
        logger.info("RECONSTRUCTION COMPLETE")
        logger.info("="*80)
        logger.info(f"Total relationships in export: {self.stats['total_relationships']}")
        logger.info(f"Successfully reconstructed: {self.stats['reconstructed']}")
        logger.info(f"Skipped (no CVE ID): {self.stats['skipped_no_cve']}")
        logger.info(f"Skipped (no source node): {self.stats['skipped_no_source']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("="*80)

        return self.stats

    def verify_reconstruction(self) -> int:
        """Verify reconstructed relationships"""
        query = """
        MATCH ()-[r:THREATENS_GRID_STABILITY]->()
        RETURN count(r) as total
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()['total']
            logger.info(f"Verification: {count} THREATENS_GRID_STABILITY relationships in database")
            return count

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()


def main():
    """Main execution"""
    reconstructor = GridStabilityReconstructor()

    try:
        # Reconstruct relationships
        stats = reconstructor.reconstruct_all()

        # Verify
        final_count = reconstructor.verify_reconstruction()

        # Check if we reached expected count
        if final_count < 2500:  # Allow for some skipped records
            logger.warning(f"Expected ~3,000 relationships, got {final_count}")
        else:
            logger.info(f"✅ Phase 4a COMPLETE: {final_count} relationships reconstructed")

    except Exception as e:
        logger.error(f"Phase 4a FAILED: {str(e)}")
        raise
    finally:
        reconstructor.close()


if __name__ == "__main__":
    main()
