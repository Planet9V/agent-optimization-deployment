#!/usr/bin/env python3
"""
Phase 4b: Reconstruct VULNERABLE_TO Relationships
Restores 24,664 vulnerability relationships from metadata export

File: phase4b_reconstruct_vulnerable_to.py
Created: 2025-11-01 22:56:00
Version: 1.0.0
Author: Automation Agent
Purpose: Reconstruct VULNERABLE_TO relationships after CVE cleanup
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
        logging.FileHandler(f'../logs/phase4b_reconstruct_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VulnerableToReconstructor:
    """Reconstructs VULNERABLE_TO relationships from export"""

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
            'cve_not_found': 0,
            'source_not_found': 0,
            'errors': 0
        }

    def load_export_data(self) -> List[Dict[str, Any]]:
        """Load VULNERABLE_TO export"""
        export_file = self.export_dir / 'vulnerable_to_relationships.json'

        if not export_file.exists():
            raise FileNotFoundError(f"Export file not found: {export_file}")

        logger.info(f"Loading export from: {export_file}")
        with open(export_file) as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} relationship records")
        return data

    def reconstruct_relationship(self, session, record: Dict[str, Any]) -> bool:
        """
        Reconstruct single VULNERABLE_TO relationship

        Returns True if successful, False otherwise
        """
        # Get CVE ID
        cve_id = record.get('cve_id') or record.get('relationship_cve_id')

        # Get source node info
        source_label = record.get('source_label')
        source_id = record.get('source_id')

        # Get all relationship properties
        props = record.get('all_properties', {})

        if not cve_id:
            self.stats['skipped_no_cve'] += 1
            logger.warning(f"No CVE ID found in record: {record}")
            return False

        if not source_label:
            self.stats['skipped_no_source'] += 1
            logger.warning(f"No source label for CVE: {cve_id}")
            return False

        # Reconstruct relationship
        # Match source by label and id (if available)
        if source_id:
            source_match = f"MATCH (source:{source_label} {{id: $source_id}})"
        else:
            # If no source_id, we can't reliably match - log and skip
            self.stats['skipped_no_source'] += 1
            logger.warning(f"No source ID for CVE: {cve_id}, label: {source_label}")
            return False

        query = f"""
        {source_match}
        MATCH (cve:CVE {{id: $cve_id}})
        MERGE (source)-[r:VULNERABLE_TO]->(cve)
        SET r = $properties
        RETURN id(r) as relationship_id
        """

        try:
            result = session.run(query,
                source_id=source_id,
                cve_id=cve_id,
                properties=props
            )

            if result.single():
                self.stats['reconstructed'] += 1
                return True
            else:
                # Check which node wasn't found
                check_cve = session.run("MATCH (cve:CVE {id: $cve_id}) RETURN count(cve) as c", cve_id=cve_id)
                cve_exists = check_cve.single()['c'] > 0

                if not cve_exists:
                    self.stats['cve_not_found'] += 1
                    logger.debug(f"CVE not found: {cve_id}")
                else:
                    self.stats['source_not_found'] += 1
                    logger.debug(f"Source node not found: {source_label} id={source_id}")

                return False

        except Exception as e:
            logger.error(f"Error reconstructing relationship for CVE {cve_id}, source {source_label}/{source_id}: {str(e)}")
            self.stats['errors'] += 1
            return False

    def reconstruct_all(self) -> Dict[str, int]:
        """Reconstruct all VULNERABLE_TO relationships"""
        logger.info("="*80)
        logger.info("PHASE 4B: VULNERABLE_TO RECONSTRUCTION")
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

                # Log progress every batch
                if (i // batch_size) % 5 == 0:
                    logger.info(f"Progress: {self.stats['reconstructed']} reconstructed, "
                              f"{self.stats['cve_not_found']} CVE not found, "
                              f"{self.stats['source_not_found']} source not found")

        # Log final statistics
        logger.info("="*80)
        logger.info("RECONSTRUCTION COMPLETE")
        logger.info("="*80)
        logger.info(f"Total relationships in export: {self.stats['total_relationships']}")
        logger.info(f"Successfully reconstructed: {self.stats['reconstructed']}")
        logger.info(f"Skipped (no CVE ID): {self.stats['skipped_no_cve']}")
        logger.info(f"Skipped (no source info): {self.stats['skipped_no_source']}")
        logger.info(f"CVE not found in database: {self.stats['cve_not_found']}")
        logger.info(f"Source node not found: {self.stats['source_not_found']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("="*80)

        return self.stats

    def verify_reconstruction(self) -> int:
        """Verify reconstructed relationships"""
        query = """
        MATCH ()-[r:VULNERABLE_TO]->()
        RETURN count(r) as total
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()['total']
            logger.info(f"Verification: {count} VULNERABLE_TO relationships in database")
            return count

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()


def main():
    """Main execution"""
    reconstructor = VulnerableToReconstructor()

    try:
        # Reconstruct relationships
        stats = reconstructor.reconstruct_all()

        # Verify
        final_count = reconstructor.verify_reconstruction()

        # Check if we reached expected count
        if final_count < 20000:  # Allow for some skipped/missing records
            logger.warning(f"Expected ~24,664 relationships, got {final_count}")
        else:
            logger.info(f"✅ Phase 4b COMPLETE: {final_count} relationships reconstructed")

    except Exception as e:
        logger.error(f"Phase 4b FAILED: {str(e)}")
        raise
    finally:
        reconstructor.close()


if __name__ == "__main__":
    main()
