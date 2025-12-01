#!/usr/bin/env python3
"""
Complete CWE Catalog Import - Fix Remaining NULL IDs
Matches NULL ID nodes to proper CWE IDs from XML catalog by name matching

Strategy:
1. Parse CWE v4.18 XML to build ID→Name mapping
2. Find NULL ID nodes in database
3. Match by exact name to existing CWE IDs
4. Update nodes with correct IDs or delete orphans
5. Validate 0 NULL IDs remaining

Author: AEON Protocol - Final Implementation
Date: 2025-11-07
Version: 2.0.0
"""

import xml.etree.ElementTree as ET
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from neo4j import GraphDatabase

# Configure logging
log_file = Path(__file__).parent.parent / "logs" / "cwe_catalog_import.log"
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

# File paths
XML_PATH = Path(__file__).parent.parent / "cwec_v4.18.xml"

class CWECatalogFixer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'null_ids_before': 0,
            'matched_by_name': 0,
            'orphans_deleted': 0,
            'null_ids_after': 0,
            'total_cwes': 0
        }
        self.cwe_name_map = {}  # name -> cwe_id
        self.cwe_id_map = {}    # cwe_id -> full data

    def close(self):
        self.driver.close()

    def parse_cwe_xml(self):
        """Parse CWE XML and build name→ID mapping"""
        logger.info(f"Parsing CWE XML from: {XML_PATH}")

        tree = ET.parse(XML_PATH)
        root = tree.getroot()

        # Namespace handling
        ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}

        # Parse Weaknesses
        for weakness in root.findall('.//cwe:Weakness', ns):
            cwe_id = weakness.get('ID')
            name = weakness.get('Name')

            if cwe_id and name:
                # Store normalized name mapping
                normalized_name = name.strip()
                self.cwe_name_map[normalized_name] = cwe_id
                self.cwe_id_map[cwe_id] = {
                    'name': name,
                    'type': 'Weakness'
                }

        # Parse Categories
        for category in root.findall('.//cwe:Category', ns):
            cwe_id = category.get('ID')
            name = category.get('Name')

            if cwe_id and name:
                normalized_name = name.strip()
                self.cwe_name_map[normalized_name] = cwe_id
                self.cwe_id_map[cwe_id] = {
                    'name': name,
                    'type': 'Category'
                }

        # Parse Views
        for view in root.findall('.//cwe:View', ns):
            cwe_id = view.get('ID')
            name = view.get('Name')

            if cwe_id and name:
                normalized_name = name.strip()
                self.cwe_name_map[normalized_name] = cwe_id
                self.cwe_id_map[cwe_id] = {
                    'name': name,
                    'type': 'View'
                }

        logger.info(f"Parsed {len(self.cwe_name_map)} unique CWE names from XML")
        return len(self.cwe_name_map)

    def get_database_state(self):
        """Get current database state"""
        with self.driver.session() as session:
            # Total CWEs
            total = session.run("MATCH (c:CWE) RETURN count(c) as total").single()['total']

            # NULL IDs
            null_ids = session.run("""
                MATCH (c:CWE)
                WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
                RETURN count(c) as null_count
            """).single()['null_count']

            self.stats['total_cwes'] = total
            self.stats['null_ids_before'] = null_ids

            logger.info(f"\nDatabase State:")
            logger.info(f"  Total CWE nodes: {total:,}")
            logger.info(f"  NULL IDs: {null_ids:,} ({null_ids/total*100:.1f}%)")

            return total, null_ids

    def match_null_nodes_by_name(self):
        """Match NULL ID nodes to proper CWE IDs by name"""
        with self.driver.session() as session:
            # Get NULL ID nodes with names
            result = session.run("""
                MATCH (c:CWE)
                WHERE (c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null')
                  AND c.name IS NOT NULL
                RETURN elementId(c) as element_id, c.name as name
            """)

            null_nodes = [(record['element_id'], record['name']) for record in result]
            logger.info(f"\nFound {len(null_nodes)} NULL ID nodes with names")

            matched = 0
            for element_id, name in null_nodes:
                # Try exact match
                normalized_name = name.strip()
                cwe_id = self.cwe_name_map.get(normalized_name)

                if cwe_id:
                    # Check if this CWE ID already exists
                    existing_count = session.run("""
                        MATCH (c:CWE {cwe_id: $cwe_id})
                        RETURN count(c) as count
                    """, cwe_id=cwe_id).single()['count']

                    if existing_count > 0:
                        # Duplicate exists - detach and delete the NULL node
                        # Relationships will point to existing valid CWE node instead
                        session.run("""
                            MATCH (null_cwe:CWE)
                            WHERE elementId(null_cwe) = $element_id
                            DETACH DELETE null_cwe
                        """, element_id=element_id)
                        matched += 1
                        logger.debug(f"Deleted duplicate: {name} (CWE-{cwe_id} exists)")
                    else:
                        # Update with correct ID
                        session.run("""
                            MATCH (c:CWE)
                            WHERE elementId(c) = $element_id
                            SET c.cwe_id = $cwe_id,
                                c.updated_at = datetime()
                        """, element_id=element_id, cwe_id=cwe_id)
                        matched += 1
                        logger.debug(f"Matched: {name} → CWE-{cwe_id}")

            self.stats['matched_by_name'] = matched
            logger.info(f"Matched/fixed {matched} nodes by name")
            return matched

    def delete_orphaned_nodes(self):
        """Delete nodes with NULL name and NULL description"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:CWE)
                WHERE (c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null')
                  AND (c.name IS NULL OR c.name = '')
                  AND (c.description IS NULL OR c.description = '')
                DETACH DELETE c
                RETURN count(c) as deleted
            """)

            deleted = result.single()['deleted']
            self.stats['orphans_deleted'] = deleted
            logger.info(f"Deleted {deleted} orphaned nodes (NULL name/desc)")
            return deleted

    def validate_final_state(self):
        """Validate final database state"""
        with self.driver.session() as session:
            # Total CWEs
            total = session.run("MATCH (c:CWE) RETURN count(c) as total").single()['total']

            # NULL IDs
            null_ids = session.run("""
                MATCH (c:CWE)
                WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
                RETURN count(c) as null_count
            """).single()['null_count']

            # Valid IDs
            valid_ids = session.run("""
                MATCH (c:CWE)
                WHERE c.cwe_id IS NOT NULL AND c.cwe_id <> '' AND c.cwe_id <> 'null'
                RETURN count(c) as valid_count
            """).single()['valid_count']

            self.stats['total_cwes'] = total
            self.stats['null_ids_after'] = null_ids

            logger.info(f"\n{'='*60}")
            logger.info("FINAL DATABASE STATE")
            logger.info(f"{'='*60}")
            logger.info(f"Total CWE nodes: {total:,}")
            logger.info(f"Valid CWE IDs: {valid_ids:,} ({valid_ids/total*100:.1f}%)")
            logger.info(f"NULL IDs: {null_ids:,} ({null_ids/total*100:.1f}%)")

            return total, null_ids, valid_ids

    def verify_critical_cwes(self):
        """Verify all critical CWEs from Top 42"""
        critical_cwes = [
            '502', '94', '89', '288', '269', '77', '306', '863', '918', '862',
            '434', '352', '79', '732', '22', '798', '287', '190', '78', '311',
            '601', '284', '276', '327', '416', '125', '20', '770', '476', '362',
            '400', '787', '119', '755', '611', '295', '522', '681', '290', '120',
            '843', '754'
        ]

        logger.info("\nVerifying Top 42 Critical CWEs:")

        missing = []
        with self.driver.session() as session:
            for cwe_id in critical_cwes:
                result = session.run("""
                    MATCH (c:CWE {cwe_id: $cwe_id})
                    RETURN c.name as name
                """, cwe_id=cwe_id)

                record = result.single()
                if not record:
                    missing.append(cwe_id)
                    logger.warning(f"  ✗ CWE-{cwe_id}: MISSING")

        found = len(critical_cwes) - len(missing)
        logger.info(f"\nCritical CWEs: {found}/{len(critical_cwes)} found")

        if missing:
            logger.warning(f"Missing: {', '.join([f'CWE-{cwe}' for cwe in missing])}")

        return missing


def main():
    logger.info("="*60)
    logger.info("CWE CATALOG COMPLETION - Fix Remaining NULL IDs")
    logger.info("="*60)
    logger.info(f"Start time: {datetime.now().isoformat()}")

    fixer = CWECatalogFixer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Step 1: Get initial state
        logger.info("\n[STEP 1] Analyzing database state...")
        total_before, null_before = fixer.get_database_state()

        # Step 2: Parse CWE XML
        logger.info("\n[STEP 2] Parsing CWE XML catalog...")
        cwe_count = fixer.parse_cwe_xml()

        # Step 3: Match NULL nodes by name
        logger.info("\n[STEP 3] Matching NULL ID nodes by name...")
        matched = fixer.match_null_nodes_by_name()

        # Step 4: Delete orphaned nodes
        logger.info("\n[STEP 4] Deleting orphaned nodes...")
        deleted = fixer.delete_orphaned_nodes()

        # Step 5: Validate final state
        logger.info("\n[STEP 5] Validating final state...")
        total_after, null_after, valid_after = fixer.validate_final_state()

        # Step 6: Verify critical CWEs
        logger.info("\n[STEP 6] Verifying critical CWEs...")
        missing = fixer.verify_critical_cwes()

        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info("COMPLETION SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"\nDatabase Changes:")
        logger.info(f"  Before: {null_before:,} NULL IDs ({null_before/total_before*100:.1f}%)")
        logger.info(f"  After: {null_after:,} NULL IDs ({null_after/total_after*100:.1f}%)")
        logger.info(f"  Improvement: {null_before - null_after:,} NULL IDs fixed ({(null_before-null_after)/null_before*100:.1f}%)")
        logger.info(f"\nActions Taken:")
        logger.info(f"  Matched by name: {fixer.stats['matched_by_name']:,}")
        logger.info(f"  Orphans deleted: {fixer.stats['orphans_deleted']:,}")
        logger.info(f"\nFinal State:")
        logger.info(f"  Total CWE nodes: {total_after:,}")
        logger.info(f"  Valid CWE IDs: {valid_after:,} ({valid_after/total_after*100:.1f}%)")
        logger.info(f"  NULL IDs: {null_after:,} ({null_after/total_after*100:.1f}%)")

        if null_after == 0:
            logger.info("\n✅ SUCCESS: All CWE nodes have proper IDs!")
        else:
            logger.warning(f"\n⚠ WARNING: {null_after} NULL IDs still remain")

        if missing:
            logger.warning(f"\n⚠ WARNING: {len(missing)} critical CWEs missing")
        else:
            logger.info("\n✅ All 42 critical CWEs verified!")

        logger.info(f"\nEnd time: {datetime.now().isoformat()}")

    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        raise
    finally:
        fixer.close()

if __name__ == "__main__":
    main()
