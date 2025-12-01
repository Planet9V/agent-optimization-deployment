#!/usr/bin/env python3
"""
Import Complete CWE Catalog v4.18 into Neo4j
Fixes NULL ID issues and imports all missing CWE definitions

Based on validation findings:
- 1,079 CWE nodes have NULL IDs (48.7% of database)
- 8 critical CWEs missing: cwe-327, cwe-125, cwe-120, cwe-20, cwe-119, cwe-434, cwe-290, cwe-522

This script will:
1. Parse CWE v4.18 XML catalog
2. Fix NULL CWE IDs by extracting from name field
3. Import all missing CWE definitions
4. Verify all critical CWEs exist
5. Validate database state

Author: AEON Protocol - Complete Implementation
Date: 2025-11-07
Version: 1.0.0
"""

import xml.etree.ElementTree as ET
import re
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('import_cwe_catalog.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# File paths
XML_PATH = Path(__file__).parent.parent / "cwec_v4.18.xml"

class CWEImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'null_ids_fixed': 0,
            'cwes_inserted': 0,
            'cwes_updated': 0,
            'cwes_skipped': 0
        }

    def close(self):
        self.driver.close()

    def extract_cwe_id(self, text):
        """Extract CWE number from text like 'CWE-79' or 'SQL Injection (CWE-89)'"""
        if not text:
            return None
        match = re.search(r'CWE-(\d+)', text, re.IGNORECASE)
        return match.group(1) if match else None

    def parse_cwe_xml(self, xml_path):
        """Parse CWE XML and extract all weakness definitions"""
        logger.info(f"Parsing CWE XML from: {xml_path}")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Namespace handling
        ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}

        cwes = []

        # Parse Weaknesses
        for weakness in root.findall('.//cwe:Weakness', ns):
            cwe_id = weakness.get('ID')
            name = weakness.get('Name')
            abstraction = weakness.get('Abstraction')

            # Get description
            desc_elem = weakness.find('.//cwe:Description', ns)
            description = desc_elem.text if desc_elem is not None else ""

            # Get extended description if available
            ext_desc_elem = weakness.find('.//cwe:Extended_Description', ns)
            if ext_desc_elem is not None and ext_desc_elem.text:
                description += "\n\n" + ext_desc_elem.text

            cwes.append({
                'cwe_id': cwe_id,
                'name': name,
                'description': description.strip() if description else "",
                'abstraction': abstraction or 'Base',
                'type': 'Weakness'
            })

        # Parse Categories
        for category in root.findall('.//cwe:Category', ns):
            cwe_id = category.get('ID')
            name = category.get('Name')

            # Get summary
            summary_elem = category.find('.//cwe:Summary', ns)
            description = summary_elem.text if summary_elem is not None else ""

            cwes.append({
                'cwe_id': cwe_id,
                'name': name,
                'description': description.strip() if description else "",
                'abstraction': 'Category',
                'type': 'Category'
            })

        # Parse Views
        for view in root.findall('.//cwe:View', ns):
            cwe_id = view.get('ID')
            name = view.get('Name')

            # Get objective
            obj_elem = view.find('.//cwe:Objective', ns)
            description = obj_elem.text if obj_elem is not None else ""

            cwes.append({
                'cwe_id': cwe_id,
                'name': name,
                'description': description.strip() if description else "",
                'abstraction': 'View',
                'type': 'View'
            })

        logger.info(f"Parsed {len(cwes)} CWE entries from XML")
        return cwes

    def fix_null_ids(self, tx):
        """Fix CWE nodes with NULL IDs by extracting from name field"""
        # Find nodes with NULL cwe_id but CWE in name
        query = """
        MATCH (c:CWE)
        WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
        RETURN elementId(c) as node_id, c.name as name
        """
        result = tx.run(query)
        null_nodes = [(record['node_id'], record['name']) for record in result]

        logger.info(f"Found {len(null_nodes)} nodes with NULL/empty CWE IDs")

        fixed_count = 0
        for node_id, name in null_nodes:
            cwe_num = self.extract_cwe_id(name)
            if cwe_num:
                update_query = """
                MATCH (c:CWE)
                WHERE elementId(c) = $node_id
                SET c.cwe_id = $cwe_id,
                    c.updated_at = datetime()
                """
                tx.run(update_query, node_id=node_id, cwe_id=cwe_num)
                fixed_count += 1

        self.stats['null_ids_fixed'] = fixed_count
        logger.info(f"Fixed {fixed_count} nodes by extracting CWE ID from name")
        return fixed_count

    def import_cwe(self, tx, cwe_data):
        """Import or update a single CWE definition"""
        cwe_id = cwe_data['cwe_id']
        name = cwe_data['name']
        description = cwe_data['description']
        abstraction = cwe_data['abstraction']
        cwe_type = cwe_data['type']

        # Check if CWE exists
        check_query = """
        MATCH (c:CWE {cwe_id: $cwe_id})
        RETURN c.name as name, c.description as description
        """
        result = tx.run(check_query, cwe_id=cwe_id)
        existing = result.single()

        if existing:
            # Update if description is empty or significantly different
            existing_desc = existing['description'] or ""

            if not existing_desc or len(description) > len(existing_desc):
                update_query = """
                MATCH (c:CWE {cwe_id: $cwe_id})
                SET c.name = $name,
                    c.description = $description,
                    c.abstraction_level = $abstraction,
                    c.updated_at = datetime()
                """
                tx.run(update_query,
                       cwe_id=cwe_id,
                       name=name,
                       description=description,
                       abstraction=abstraction)
                return 'updated'
            else:
                return 'skipped'
        else:
            # Insert new CWE
            insert_query = """
            CREATE (c:CWE {
                cwe_id: $cwe_id,
                name: $name,
                description: $description,
                abstraction_level: $abstraction,
                created_at: datetime(),
                updated_at: datetime()
            })
            """
            tx.run(insert_query,
                   cwe_id=cwe_id,
                   name=name,
                   description=description,
                   abstraction=abstraction)
            return 'inserted'

    def import_cwe_catalog(self, cwes):
        """Import all CWE definitions from parsed XML"""
        logger.info(f"Importing {len(cwes)} CWE definitions...")

        with self.driver.session() as session:
            for i, cwe in enumerate(cwes):
                result = session.execute_write(self.import_cwe, cwe)

                if result == 'inserted':
                    self.stats['cwes_inserted'] += 1
                elif result == 'updated':
                    self.stats['cwes_updated'] += 1
                else:
                    self.stats['cwes_skipped'] += 1

                if (i + 1) % 100 == 0:
                    logger.info(f"Progress: {i + 1}/{len(cwes)} CWEs processed")

        logger.info(f"\nImport Results:")
        logger.info(f"  Inserted: {self.stats['cwes_inserted']} new CWEs")
        logger.info(f"  Updated: {self.stats['cwes_updated']} existing CWEs")
        logger.info(f"  Skipped: {self.stats['cwes_skipped']} (already complete)")

    def verify_critical_cwes(self):
        """Verify all 8 critical CWEs exist"""
        critical_cwes = ['327', '125', '120', '20', '119', '434', '290', '522']

        logger.info("\nVerifying critical CWEs:")

        with self.driver.session() as session:
            missing = []

            for cwe_id in critical_cwes:
                query = """
                MATCH (c:CWE {cwe_id: $cwe_id})
                RETURN c.name as name
                """
                result = session.run(query, cwe_id=cwe_id)
                record = result.single()

                if record:
                    logger.info(f"✓ CWE-{cwe_id}: {record['name']}")
                else:
                    logger.warning(f"✗ CWE-{cwe_id}: MISSING")
                    missing.append(cwe_id)

            return missing

    def validate_database(self):
        """Validate database state after import"""
        with self.driver.session() as session:
            # Count total CWEs
            total_query = "MATCH (c:CWE) RETURN count(c) as total"
            total = session.run(total_query).single()['total']

            # Count NULL IDs
            null_query = """
            MATCH (c:CWE)
            WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
            RETURN count(c) as null_count
            """
            null_ids = session.run(null_query).single()['null_count']

            # Count by abstraction level
            abstraction_query = """
            MATCH (c:CWE)
            RETURN c.abstraction_level as level, count(c) as count
            ORDER BY count DESC
            """
            abstractions = [(record['level'], record['count'])
                          for record in session.run(abstraction_query)]

            logger.info(f"\n{'='*60}")
            logger.info("DATABASE VALIDATION RESULTS")
            logger.info(f"{'='*60}")
            logger.info(f"Total CWE nodes: {total:,}")
            logger.info(f"NULL IDs remaining: {null_ids:,} ({null_ids/total*100:.1f}%)")
            logger.info(f"\nAbstraction Levels:")
            for level, count in abstractions:
                logger.info(f"  {level or 'NULL'}: {count:,}")

            return total, null_ids

def main():
    logger.info("="*60)
    logger.info("CWE CATALOG IMPORT - v4.18 (Neo4j)")
    logger.info("="*60)
    logger.info(f"Start time: {datetime.now().isoformat()}")

    importer = CWEImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Step 1: Fix NULL IDs
        logger.info("\n[STEP 1] Fixing NULL IDs...")
        with importer.driver.session() as session:
            session.execute_write(importer.fix_null_ids)

        # Step 2: Parse CWE XML
        logger.info("\n[STEP 2] Parsing CWE XML catalog...")
        cwes = importer.parse_cwe_xml(XML_PATH)

        # Step 3: Import CWE catalog
        logger.info("\n[STEP 3] Importing CWE definitions...")
        importer.import_cwe_catalog(cwes)

        # Step 4: Verify critical CWEs
        logger.info("\n[STEP 4] Verifying critical CWEs...")
        missing = importer.verify_critical_cwes()

        if missing:
            logger.warning(f"\n⚠ WARNING: {len(missing)} critical CWEs still missing!")
        else:
            logger.info("\n✓ All 8 critical CWEs verified!")

        # Step 5: Validate database
        logger.info("\n[STEP 5] Validating database...")
        total, null_ids = importer.validate_database()

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info("IMPORT COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"End time: {datetime.now().isoformat()}")

        if null_ids == 0:
            logger.info("\n✅ SUCCESS: All CWE nodes have proper IDs")
        else:
            logger.warning(f"\n⚠ WARNING: {null_ids} nodes still have NULL IDs")

        logger.info(f"\nFinal Statistics:")
        logger.info(f"  NULL IDs fixed: {importer.stats['null_ids_fixed']}")
        logger.info(f"  CWEs inserted: {importer.stats['cwes_inserted']}")
        logger.info(f"  CWEs updated: {importer.stats['cwes_updated']}")
        logger.info(f"  CWEs skipped: {importer.stats['cwes_skipped']}")

    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        raise
    finally:
        importer.close()

if __name__ == "__main__":
    main()
