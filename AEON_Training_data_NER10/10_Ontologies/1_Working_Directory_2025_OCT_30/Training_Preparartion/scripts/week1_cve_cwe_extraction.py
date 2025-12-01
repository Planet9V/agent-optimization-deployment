#!/usr/bin/env python3
"""
Week 1: CVE → CWE Relationship Extraction
AEON Protocol Phase 2 - Implementation Week 1

Purpose: Extract CWE references from CVE descriptions using regex pattern matching
         and create IS_WEAKNESS_TYPE relationships in Neo4j graph database.

Database State (FACTS):
- CVEs: 316,552 nodes
- CWEs: 2,214 nodes
- Existing CVE→CWE relationships: 0
- CVEs with "CWE-" text: 1,513

Expected Outcome: 1,500-2,000 IS_WEAKNESS_TYPE relationships

Author: AEON Protocol Implementation
Date: 2025-11-07
Version: 1.0.0
"""

import re
import logging
from typing import List, Dict, Set, Tuple
from neo4j import GraphDatabase
from collections import defaultdict
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week1_cve_cwe_extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j connection configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# CWE extraction patterns (ordered by specificity)
CWE_PATTERNS = [
    r'CWE-(\d+)',                           # Standard: CWE-94
    r'CWE\s*ID\s*(\d+)',                    # Variant: CWE ID 94
    r'CWE\s*#\s*(\d+)',                     # Variant: CWE #94
    r'weakness\s+CWE-(\d+)',                # Contextual: weakness CWE-94
    r'classified\s+as\s+CWE-(\d+)',         # Explicit: classified as CWE-94
    r'related\s+to\s+CWE-(\d+)',            # Related: related to CWE-94
    r'vulnerability\s+type.*?(\d{1,4})',    # Contextual: vulnerability type 94
]


class CVECWEExtractor:
    """
    Extracts CWE references from CVE descriptions and creates Neo4j relationships.
    """

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()
        logger.info("Neo4j connection closed")

    def extract_cwe_ids(self, description: str) -> List[str]:
        """
        Extract all CWE IDs from a CVE description using regex patterns.

        Args:
            description: CVE description text

        Returns:
            List of unique CWE IDs in lowercase format "cwe-XXX" (matching database format)
        """
        if not description:
            return []

        cwe_ids = set()

        for pattern in CWE_PATTERNS:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                try:
                    cwe_num = int(match)
                    # Validate CWE number range (CWE-1 to CWE-9999)
                    if 1 <= cwe_num <= 9999:
                        # Use lowercase to match database format
                        cwe_ids.add(f"cwe-{cwe_num}")
                except ValueError:
                    continue

        return sorted(list(cwe_ids))

    def fetch_cves_batch(self, skip: int, limit: int) -> List[Dict]:
        """
        Fetch batch of CVEs with descriptions from Neo4j.

        Args:
            skip: Number of CVEs to skip
            limit: Maximum CVEs to return

        Returns:
            List of CVE dictionaries with id and description
        """
        query = """
        MATCH (c:CVE)
        WHERE c.description IS NOT NULL AND c.description <> ''
        RETURN c.id AS cveId, c.description AS description
        SKIP $skip LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, skip=skip, limit=limit)
            return [dict(record) for record in result]

    def verify_cwe_exists(self, cwe_id: str) -> Tuple[bool, str]:
        """
        Verify that a CWE node exists in the database (case-insensitive).

        Args:
            cwe_id: CWE identifier (e.g., "cwe-94")

        Returns:
            Tuple of (exists, actual_id) where actual_id is the database format
        """
        # Try both lowercase and uppercase formats
        query = """
        MATCH (w:CWE)
        WHERE toLower(w.id) = toLower($cwe_id)
        RETURN w.id AS actual_id LIMIT 1
        """

        with self.driver.session() as session:
            result = session.run(query, cwe_id=cwe_id)
            record = result.single()
            if record:
                return True, record['actual_id']
            return False, None

    def create_cve_cwe_relationship(self, cve_id: str, cwe_id: str) -> bool:
        """
        Create IS_WEAKNESS_TYPE relationship between CVE and CWE.

        Args:
            cve_id: CVE identifier
            cwe_id: CWE identifier

        Returns:
            True if relationship created, False if already exists or CWE not found
        """
        query = """
        MATCH (cve:CVE {id: $cve_id})
        MATCH (cwe:CWE {id: $cwe_id})
        MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
        RETURN r IS NOT NULL AS created
        """

        try:
            with self.driver.session() as session:
                result = session.run(query, cve_id=cve_id, cwe_id=cwe_id)
                return result.single()['created']
        except Exception as e:
            logger.error(f"Error creating relationship {cve_id} → {cwe_id}: {e}")
            return False

    def get_total_cve_count(self) -> int:
        """Get total count of CVE nodes with descriptions."""
        query = """
        MATCH (c:CVE)
        WHERE c.description IS NOT NULL AND c.description <> ''
        RETURN count(c) AS total
        """

        with self.driver.session() as session:
            result = session.run(query)
            return result.single()['total']

    def get_relationship_statistics(self) -> Dict:
        """
        Get statistics about created relationships.

        Returns:
            Dictionary with relationship counts and coverage metrics
        """
        query = """
        MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
        WITH count(r) AS total_relationships,
             count(DISTINCT cve) AS unique_cves,
             count(DISTINCT cwe) AS unique_cwes
        MATCH (c:CVE)
        WITH total_relationships, unique_cves, unique_cwes, count(c) AS total_cves
        RETURN total_relationships,
               unique_cves,
               unique_cwes,
               total_cves,
               round(100.0 * unique_cves / total_cves, 2) AS coverage_percentage
        """

        with self.driver.session() as session:
            result = session.run(query)
            return dict(result.single())

    def process_all_cves(self, batch_size: int = 2000):
        """
        Process all CVEs in batches to extract CWE relationships.

        Args:
            batch_size: Number of CVEs to process per batch
        """
        total_cves = self.get_total_cve_count()
        logger.info(f"Total CVEs with descriptions: {total_cves:,}")

        processed = 0
        relationships_created = 0
        relationships_skipped = 0
        cwe_not_found = defaultdict(int)
        cve_cwe_map = defaultdict(list)

        while processed < total_cves:
            # Fetch batch
            cves = self.fetch_cves_batch(skip=processed, limit=batch_size)

            if not cves:
                break

            logger.info(f"Processing batch {processed:,} to {processed + len(cves):,}")

            for cve_data in cves:
                cve_id = cve_data['cveId']
                description = cve_data['description']

                # Extract CWE IDs
                cwe_ids = self.extract_cwe_ids(description)

                if not cwe_ids:
                    continue

                # Create relationships
                for cwe_id in cwe_ids:
                    # Verify CWE exists (case-insensitive)
                    exists, actual_cwe_id = self.verify_cwe_exists(cwe_id)
                    if not exists:
                        cwe_not_found[cwe_id] += 1
                        logger.warning(f"CWE not found in database: {cwe_id} (from {cve_id})")
                        continue

                    # Create relationship using actual database ID
                    if self.create_cve_cwe_relationship(cve_id, actual_cwe_id):
                        relationships_created += 1
                        cve_cwe_map[cve_id].append(actual_cwe_id)
                    else:
                        relationships_skipped += 1

            processed += len(cves)

            # Progress update
            if processed % 10000 == 0:
                logger.info(f"Progress: {processed:,}/{total_cves:,} CVEs processed, "
                          f"{relationships_created:,} relationships created")

        # Final statistics
        logger.info("=" * 80)
        logger.info("EXTRACTION COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total CVEs processed: {processed:,}")
        logger.info(f"Relationships created: {relationships_created:,}")
        logger.info(f"Relationships skipped (duplicates): {relationships_skipped:,}")
        logger.info(f"Unique CWEs not found: {len(cwe_not_found)}")

        if cwe_not_found:
            logger.warning("\nTop 10 missing CWEs:")
            for cwe_id, count in sorted(cwe_not_found.items(),
                                       key=lambda x: x[1],
                                       reverse=True)[:10]:
                logger.warning(f"  {cwe_id}: {count} occurrences")

        # Get final database statistics
        stats = self.get_relationship_statistics()
        logger.info("\n" + "=" * 80)
        logger.info("DATABASE STATISTICS")
        logger.info("=" * 80)
        logger.info(f"Total IS_WEAKNESS_TYPE relationships: {stats['total_relationships']:,}")
        logger.info(f"Unique CVEs with CWE relationships: {stats['unique_cves']:,}")
        logger.info(f"Unique CWEs referenced: {stats['unique_cwes']:,}")
        logger.info(f"Total CVEs in database: {stats['total_cves']:,}")
        logger.info(f"Coverage: {stats['coverage_percentage']}%")

        # Validation
        if stats['total_relationships'] >= 1500:
            logger.info("\n✅ SUCCESS: Met target of 1,500+ relationships")
        else:
            logger.warning(f"\n⚠️ WARNING: Below target (expected 1,500+, got {stats['total_relationships']})")

        return {
            'processed': processed,
            'created': relationships_created,
            'skipped': relationships_skipped,
            'stats': stats,
            'missing_cwes': dict(cwe_not_found)
        }


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("WEEK 1: CVE → CWE RELATIONSHIP EXTRACTION")
    logger.info("AEON Protocol Phase 2 - Implementation")
    logger.info("=" * 80)

    extractor = CVECWEExtractor(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        results = extractor.process_all_cves(batch_size=2000)

        logger.info("\n" + "=" * 80)
        logger.info("WEEK 1 EXECUTION COMPLETE")
        logger.info("=" * 80)

        # Write summary to file
        with open('week1_completion_report.txt', 'w') as f:
            f.write("WEEK 1 COMPLETION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"CVEs Processed: {results['processed']:,}\n")
            f.write(f"Relationships Created: {results['created']:,}\n")
            f.write(f"Unique CVEs with CWE: {results['stats']['unique_cves']:,}\n")
            f.write(f"Unique CWEs Referenced: {results['stats']['unique_cwes']:,}\n")
            f.write(f"Coverage: {results['stats']['coverage_percentage']}%\n")
            f.write(f"\nStatus: {'✅ SUCCESS' if results['stats']['total_relationships'] >= 1500 else '⚠️ BELOW TARGET'}\n")

        logger.info("Summary written to: week1_completion_report.txt")

    except Exception as e:
        logger.error(f"Fatal error during execution: {e}", exc_info=True)
        raise
    finally:
        extractor.close()


if __name__ == "__main__":
    main()
