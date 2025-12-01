#!/usr/bin/env python3
"""
MITRE ATT&CK Technique Import Script
Imports ATT&CK techniques as ATT_CK_Technique nodes into Neo4j

Processes STIX 2.1 formatted MITRE ATT&CK Enterprise data and creates:
- ATT_CK_Technique nodes with full metadata
- Proper indexing for performance
- Tactic relationships

Author: AEON Protocol - Actual Implementation
Date: 2025-11-07
Version: 1.0.0
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
from neo4j import GraphDatabase

# Configure logging
log_file = Path(__file__).parent.parent / "logs" / "attack_import.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# File path
ATTACK_JSON_PATH = Path(__file__).parent.parent / "enterprise-attack.json"


class ATTACKImporter:
    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j driver"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("✅ Connected to Neo4j")

    def close(self):
        """Close Neo4j driver"""
        self.driver.close()
        logger.info("🔌 Neo4j connection closed")

    def create_indexes(self):
        """Create indexes for performance"""
        with self.driver.session() as session:
            # Index on technique_id for fast lookups
            session.run("""
                CREATE INDEX attack_technique_id IF NOT EXISTS
                FOR (t:ATT_CK_Technique)
                ON (t.technique_id)
            """)
            logger.info("✅ Created index on technique_id")

            # Index on name for searches
            session.run("""
                CREATE INDEX attack_technique_name IF NOT EXISTS
                FOR (t:ATT_CK_Technique)
                ON (t.name)
            """)
            logger.info("✅ Created index on name")

    def load_attack_data(self) -> Dict:
        """Load and parse MITRE ATT&CK JSON"""
        logger.info(f"📖 Loading ATT&CK data from {ATTACK_JSON_PATH}")

        if not ATTACK_JSON_PATH.exists():
            raise FileNotFoundError(f"ATT&CK data file not found: {ATTACK_JSON_PATH}")

        with open(ATTACK_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"✅ Loaded {len(data.get('objects', []))} STIX objects")
        return data

    def extract_techniques(self, attack_data: Dict) -> List[Dict]:
        """Extract technique objects from STIX data"""
        techniques = []

        for obj in attack_data.get('objects', []):
            # Filter for attack-pattern type (techniques)
            if obj.get('type') != 'attack-pattern':
                continue

            # Skip revoked or deprecated techniques
            if obj.get('revoked', False) or obj.get('x_mitre_deprecated', False):
                continue

            # Extract technique metadata
            external_refs = obj.get('external_references', [])
            technique_id = None
            technique_url = None

            # Find MITRE ATT&CK ID
            for ref in external_refs:
                if ref.get('source_name') == 'mitre-attack':
                    technique_id = ref.get('external_id')
                    technique_url = ref.get('url')
                    break

            if not technique_id:
                continue

            # Extract tactics (kill chain phases)
            tactics = []
            for kcp in obj.get('kill_chain_phases', []):
                if kcp.get('kill_chain_name') == 'mitre-attack':
                    tactics.append(kcp.get('phase_name'))

            # Build technique record
            technique = {
                'technique_id': technique_id,
                'name': obj.get('name', ''),
                'description': obj.get('description', ''),
                'tactics': tactics,
                'url': technique_url,
                'created': obj.get('created', ''),
                'modified': obj.get('modified', ''),
                'version': obj.get('x_mitre_version', ''),
                'stix_id': obj.get('id', ''),
                'is_subtechnique': '.' in technique_id  # T1234.001 format
            }

            techniques.append(technique)

        logger.info(f"✅ Extracted {len(techniques)} valid techniques")
        return techniques

    def import_techniques(self, techniques: List[Dict]) -> int:
        """Import techniques into Neo4j as ATT_CK_Technique nodes"""
        count = 0
        batch_size = 100

        with self.driver.session() as session:
            for i in range(0, len(techniques), batch_size):
                batch = techniques[i:i + batch_size]

                # Batch import using UNWIND
                result = session.run("""
                    UNWIND $techniques AS tech
                    MERGE (t:ATT_CK_Technique {technique_id: tech.technique_id})
                    SET t.name = tech.name,
                        t.description = tech.description,
                        t.tactics = tech.tactics,
                        t.url = tech.url,
                        t.created = tech.created,
                        t.modified = tech.modified,
                        t.version = tech.version,
                        t.stix_id = tech.stix_id,
                        t.is_subtechnique = tech.is_subtechnique,
                        t.import_date = datetime()
                    RETURN count(t) AS imported
                """, techniques=batch)

                batch_count = result.single()['imported']
                count += batch_count
                logger.info(f"⚡ Imported batch {i//batch_size + 1}: {batch_count} techniques")

        logger.info(f"✅ Total techniques imported: {count}")
        return count

    def create_tactic_relationships(self):
        """Create relationships between techniques and their tactics"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:ATT_CK_Technique)
                WHERE t.tactics IS NOT NULL
                UNWIND t.tactics AS tactic
                MERGE (tact:ATT_CK_Tactic {name: tactic})
                MERGE (t)-[:BELONGS_TO_TACTIC]->(tact)
                RETURN count(DISTINCT t) AS techniques, count(DISTINCT tact) AS tactics
            """)

            stats = result.single()
            logger.info(f"✅ Created tactic relationships: {stats['techniques']} techniques → {stats['tactics']} tactics")

    def verify_import(self) -> Dict:
        """Verify the import was successful"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:ATT_CK_Technique)
                RETURN
                    count(t) AS total_techniques,
                    count(CASE WHEN t.is_subtechnique THEN 1 END) AS subtechniques,
                    count(CASE WHEN NOT t.is_subtechnique THEN 1 END) AS main_techniques
            """)

            stats = result.single()

            logger.info("=" * 60)
            logger.info("📊 IMPORT VERIFICATION")
            logger.info("=" * 60)
            logger.info(f"Total ATT&CK Techniques: {stats['total_techniques']}")
            logger.info(f"Main Techniques: {stats['main_techniques']}")
            logger.info(f"Sub-techniques: {stats['subtechniques']}")
            logger.info("=" * 60)

            return dict(stats)


def main():
    """Main execution flow"""
    logger.info("=" * 60)
    logger.info("🚀 MITRE ATT&CK TECHNIQUE IMPORT")
    logger.info("=" * 60)
    logger.info(f"Start time: {datetime.now()}")

    importer = None
    try:
        # Initialize importer
        importer = ATTACKImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

        # Create indexes
        logger.info("\n📑 Creating indexes...")
        importer.create_indexes()

        # Load ATT&CK data
        logger.info("\n📖 Loading ATT&CK data...")
        attack_data = importer.load_attack_data()

        # Extract techniques
        logger.info("\n🔍 Extracting techniques...")
        techniques = importer.extract_techniques(attack_data)

        # Import techniques
        logger.info(f"\n⚡ Importing {len(techniques)} techniques...")
        count = importer.import_techniques(techniques)

        # Create tactic relationships
        logger.info("\n🔗 Creating tactic relationships...")
        importer.create_tactic_relationships()

        # Verify import
        logger.info("\n✅ Verifying import...")
        stats = importer.verify_import()

        # Final report
        logger.info("\n" + "=" * 60)
        logger.info("✅ IMPORT COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"✅ Successfully imported {count} ATT&CK techniques")
        logger.info(f"✅ Main techniques: {stats['main_techniques']}")
        logger.info(f"✅ Sub-techniques: {stats['subtechniques']}")
        logger.info(f"End time: {datetime.now()}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"❌ Import failed: {e}", exc_info=True)
        return 1

    finally:
        if importer:
            importer.close()


if __name__ == "__main__":
    sys.exit(main())
