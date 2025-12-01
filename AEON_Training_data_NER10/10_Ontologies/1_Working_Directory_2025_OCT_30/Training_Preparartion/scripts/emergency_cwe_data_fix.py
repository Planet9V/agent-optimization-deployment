#!/usr/bin/env python3
"""
EMERGENCY CWE DATA FIX
Critical fix for CWE database integrity issues

ISSUES ADDRESSED:
1. Import 12 critical missing CWEs
2. Fix 1,424 CWE nodes with NULL IDs
3. Normalize case to lowercase 'cwe-XXX'
4. Remove duplicate CWE nodes
5. Validate completeness

Author: AEON Protocol - Emergency Response
Date: 2025-11-07
Version: 1.0.0 - CRITICAL FIX
"""

import requests
import xml.etree.ElementTree as ET
import logging
import sys
from typing import Dict, List, Set
from neo4j import GraphDatabase
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('emergency_cwe_fix.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# CWE Catalog URL
CWE_XML_URL = "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"

# Critical missing CWEs (manual definitions)
CRITICAL_CWES = {
    '20': 'Improper Input Validation',
    '119': 'Improper Restriction of Operations within the Bounds of a Memory Buffer',
    '125': 'Out-of-bounds Read',
    '327': 'Use of a Broken or Risky Cryptographic Algorithm',
    '290': 'Authentication Bypass by Spoofing',
    '522': 'Insufficiently Protected Credentials',
    '434': 'Unrestricted Upload of File with Dangerous Type',
    '120': 'Buffer Copy without Checking Size of Input (Classic Buffer Overflow)',
    '200': 'Exposure of Sensitive Information to an Unauthorized Actor',
    '269': 'Improper Privilege Management',
    '88': 'Improper Neutralization of Argument Delimiters in a Command (Argument Injection)',
    '400': 'Uncontrolled Resource Consumption'
}


class EmergencyCWEFixer:
    """Emergency fixer for CWE database integrity."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            max_connection_lifetime=3600,
            max_connection_pool_size=50,
            connection_timeout=30,
            keep_alive=True
        )
        self.stats = {
            'critical_imported': 0,
            'null_ids_fixed': 0,
            'duplicates_removed': 0,
            'case_normalized': 0,
            'validation_passed': 0
        }
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close connections."""
        self.driver.close()

    def import_critical_cwes(self):
        """Import 12 critical missing CWEs."""
        logger.info("=" * 80)
        logger.info("STEP 1: IMPORTING CRITICAL MISSING CWEs")
        logger.info("=" * 80)

        query = """
        MERGE (w:CWE {id: $cwe_id})
        ON CREATE SET
            w.name = $name,
            w.number = $number,
            w.created_by = 'emergency_fix',
            w.created_at = datetime()
        ON MATCH SET
            w.name = COALESCE(w.name, $name),
            w.number = COALESCE(w.number, $number)
        RETURN w.id AS id, w.name AS name
        """

        for number, name in CRITICAL_CWES.items():
            cwe_id = f"cwe-{number}"

            try:
                with self.driver.session() as session:
                    result = session.run(query, cwe_id=cwe_id, name=name, number=int(number))
                    record = result.single()

                    if record:
                        self.stats['critical_imported'] += 1
                        logger.info(f"✅ Imported/Updated: {record['id']} - {record['name']}")
                    else:
                        logger.error(f"❌ Failed to import: {cwe_id}")

            except Exception as e:
                logger.error(f"❌ Error importing {cwe_id}: {e}")

        logger.info(f"\n✅ Critical CWEs imported: {self.stats['critical_imported']}/12\n")

    def fix_null_ids(self):
        """Fix CWE nodes with NULL IDs using the 'number' property."""
        logger.info("=" * 80)
        logger.info("STEP 2: FIXING NULL IDS")
        logger.info("=" * 80)

        # Find CWEs with NULL ids but valid numbers
        find_query = """
        MATCH (w:CWE)
        WHERE w.id IS NULL AND w.number IS NOT NULL
        RETURN w.number AS number, count(*) AS count
        LIMIT 100
        """

        fix_query = """
        MATCH (w:CWE)
        WHERE w.id IS NULL AND w.number = $number
        SET w.id = $cwe_id
        RETURN count(w) AS fixed
        """

        with self.driver.session() as session:
            # Find NULL IDs
            result = session.run(find_query)
            null_id_cwes = list(result)

            logger.info(f"Found {len(null_id_cwes)} CWEs with NULL IDs and valid numbers")

            # Fix them
            for record in null_id_cwes:
                number = record['number']
                cwe_id = f"cwe-{number}"

                try:
                    result = session.run(fix_query, number=number, cwe_id=cwe_id)
                    fixed_count = result.single()['fixed']
                    self.stats['null_ids_fixed'] += fixed_count
                    if fixed_count > 0:
                        logger.info(f"✅ Fixed NULL ID: cwe-{number} ({fixed_count} nodes)")

                except Exception as e:
                    logger.error(f"❌ Error fixing cwe-{number}: {e}")

        logger.info(f"\n✅ NULL IDs fixed: {self.stats['null_ids_fixed']}\n")

    def normalize_case(self):
        """Normalize all CWE IDs to lowercase 'cwe-XXX'."""
        logger.info("=" * 80)
        logger.info("STEP 3: NORMALIZING CASE TO lowercase")
        logger.info("=" * 80)

        query = """
        MATCH (w:CWE)
        WHERE w.id STARTS WITH 'CWE-'
        WITH w, toLower(w.id) AS lowercase_id
        SET w.id = lowercase_id
        RETURN count(w) AS normalized
        """

        try:
            with self.driver.session() as session:
                result = session.run(query)
                normalized_count = result.single()['normalized']
                self.stats['case_normalized'] = normalized_count
                logger.info(f"✅ Case normalized: {normalized_count} CWEs\n")

        except Exception as e:
            logger.error(f"❌ Error normalizing case: {e}")

    def remove_duplicates(self):
        """Remove duplicate CWE nodes (same CWE in different cases)."""
        logger.info("=" * 80)
        logger.info("STEP 4: REMOVING DUPLICATES")
        logger.info("=" * 80)

        # Find duplicates
        find_query = """
        MATCH (w:CWE)
        WHERE w.id IS NOT NULL
        WITH toLower(w.id) AS normalized_id, collect(w) AS nodes
        WHERE size(nodes) > 1
        RETURN normalized_id, size(nodes) AS count
        """

        # Merge duplicates
        merge_query = """
        MATCH (w1:CWE), (w2:CWE)
        WHERE w1.id <> w2.id
          AND toLower(w1.id) = toLower(w2.id)
          AND w1.id STARTS WITH 'cwe-'
        WITH w1, w2
        MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(w2)
        MERGE (cve)-[:IS_WEAKNESS_TYPE]->(w1)
        DELETE r
        WITH w2
        DETACH DELETE w2
        RETURN count(*) AS removed
        """

        try:
            with self.driver.session() as session:
                # Find duplicates
                result = session.run(find_query)
                duplicates = list(result)

                logger.info(f"Found {len(duplicates)} sets of duplicate CWEs")

                if duplicates:
                    # Remove duplicates
                    result = session.run(merge_query)
                    removed_count = result.single()['removed']
                    self.stats['duplicates_removed'] = removed_count
                    logger.info(f"✅ Duplicates removed: {removed_count} nodes\n")
                else:
                    logger.info("No duplicates found\n")

        except Exception as e:
            logger.error(f"❌ Error removing duplicates: {e}")

    def validate_fixes(self):
        """Validate that all fixes were successful."""
        logger.info("=" * 80)
        logger.info("STEP 5: VALIDATION")
        logger.info("=" * 80)

        with self.driver.session() as session:
            # Check critical CWEs
            critical_check_query = """
            MATCH (w:CWE)
            WHERE w.id IN $critical_ids
            RETURN count(w) AS found
            """

            critical_ids = [f"cwe-{num}" for num in CRITICAL_CWES.keys()]
            result = session.run(critical_check_query, critical_ids=critical_ids)
            critical_found = result.single()['found']

            logger.info(f"✅ Critical CWEs present: {critical_found}/12")

            # Check NULL IDs
            null_check_query = """
            MATCH (w:CWE)
            WHERE w.id IS NULL
            RETURN count(w) AS null_count
            """

            result = session.run(null_check_query)
            null_count = result.single()['null_count']

            logger.info(f"⚠️ NULL IDs remaining: {null_count}")

            # Check case format
            case_check_query = """
            MATCH (w:CWE)
            WHERE w.id IS NOT NULL
            WITH w.id AS cwe_id,
                 CASE
                     WHEN cwe_id STARTS WITH 'CWE-' THEN 'UPPERCASE'
                     WHEN cwe_id STARTS WITH 'cwe-' THEN 'lowercase'
                     ELSE 'OTHER'
                 END AS format_type
            RETURN format_type, count(*) AS count
            ORDER BY count DESC
            """

            result = session.run(case_check_query)
            case_distribution = list(result)

            logger.info("\n📊 Case Distribution:")
            for record in case_distribution:
                logger.info(f"  {record['format_type']}: {record['count']:,} CWEs")

            # Overall stats
            total_query = """
            MATCH (w:CWE)
            RETURN count(w) AS total_cwes,
                   count(w.id) AS cwes_with_id
            """

            result = session.run(total_query)
            stats = result.single()

            logger.info(f"\n📈 Final Stats:")
            logger.info(f"  Total CWEs: {stats['total_cwes']:,}")
            logger.info(f"  CWEs with IDs: {stats['cwes_with_id']:,}")
            logger.info(f"  Percentage with IDs: {100 * stats['cwes_with_id'] / stats['total_cwes']:.1f}%")

            # Success criteria
            success = (
                critical_found == 12 and
                null_count < stats['total_cwes'] * 0.05  # Less than 5% NULL
            )

            if success:
                logger.info("\n✅ ALL VALIDATION CHECKS PASSED")
                self.stats['validation_passed'] = 1
            else:
                logger.warning("\n⚠️ SOME VALIDATION CHECKS FAILED")
                logger.warning(f"  Critical CWEs: {critical_found}/12")
                logger.warning(f"  NULL IDs: {null_count} (target: <{stats['total_cwes'] * 0.05:.0f})")

    def execute_emergency_fix(self):
        """Execute all emergency fix steps."""
        logger.info("=" * 80)
        logger.info("EMERGENCY CWE DATA FIX")
        logger.info("=" * 80)

        try:
            # Step 1: Import critical CWEs
            self.import_critical_cwes()

            # Step 2: Fix NULL IDs
            self.fix_null_ids()

            # Step 3: Normalize case
            self.normalize_case()

            # Step 4: Remove duplicates
            self.remove_duplicates()

            # Step 5: Validate
            self.validate_fixes()

            # Summary
            logger.info("\n" + "=" * 80)
            logger.info("EMERGENCY FIX COMPLETE")
            logger.info("=" * 80)
            logger.info(f"Critical CWEs imported: {self.stats['critical_imported']}")
            logger.info(f"NULL IDs fixed: {self.stats['null_ids_fixed']}")
            logger.info(f"Case normalized: {self.stats['case_normalized']}")
            logger.info(f"Duplicates removed: {self.stats['duplicates_removed']}")
            logger.info(f"Validation passed: {'YES' if self.stats['validation_passed'] else 'NO'}")
            logger.info("=" * 80)

            return self.stats['validation_passed'] == 1

        except Exception as e:
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
            return False


def main():
    """Main execution function."""
    fixer = EmergencyCWEFixer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        success = fixer.execute_emergency_fix()
        return 0 if success else 1

    except Exception as e:
        logger.error(f"❌ Critical failure: {e}", exc_info=True)
        return 1

    finally:
        fixer.close()


if __name__ == "__main__":
    sys.exit(main())
