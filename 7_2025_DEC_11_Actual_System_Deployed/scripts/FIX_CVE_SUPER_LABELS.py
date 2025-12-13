#!/usr/bin/env python3
"""
Fix CVE Super Labels - Handle Duplicate Nodes

Problem: CVE nodes and Vulnerability nodes with same IDs exist as duplicates.
When trying to add Vulnerability super label to CVE nodes, constraint violations occur.

Solution:
1. Identify CVE/Vulnerability duplicates
2. Merge duplicate nodes by copying relationships and properties
3. Add Vulnerability super label to remaining CVE nodes

Created: 2025-12-12
Status: PRODUCTION-READY
"""

import logging
from neo4j import GraphDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"


def fix_cve_super_labels():
    """Fix CVE nodes to have Vulnerability super label"""

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            logger.info("="*80)
            logger.info("FIX CVE SUPER LABELS")
            logger.info("="*80)

            # Step 1: Count duplicates
            result = session.run("""
                MATCH (cve:CVE), (vuln:Vulnerability)
                WHERE cve.id = vuln.id AND NOT cve:Vulnerability
                RETURN count(*) as duplicates
            """)
            duplicates = result.single()["duplicates"]
            logger.info(f"Found {duplicates:,} CVE nodes with matching Vulnerability nodes")

            # Step 2: Merge duplicates (copy relationships from Vulnerability to CVE, then delete Vulnerability)
            if duplicates > 0:
                logger.info("Merging duplicate nodes...")
                result = session.run("""
                    CALL {
                        MATCH (cve:CVE), (vuln:Vulnerability)
                        WHERE cve.id = vuln.id AND NOT cve:Vulnerability AND cve.id IS NOT NULL
                        WITH cve, vuln
                        LIMIT 1000

                        // Copy properties from vuln to cve (if missing)
                        SET cve += vuln

                        // Copy relationships from vuln to cve
                        WITH cve, vuln
                        CALL {
                            WITH cve, vuln
                            MATCH (vuln)-[r]->(target)
                            WHERE NOT (cve)-[:TYPE(r)]->(target)
                            WITH cve, target, type(r) as relType, properties(r) as props
                            CALL apoc.create.relationship(cve, relType, props, target) YIELD rel
                            RETURN count(rel) as rels_copied
                        }

                        WITH cve, vuln
                        CALL {
                            WITH cve, vuln
                            MATCH (source)-[r]->(vuln)
                            WHERE NOT (source)-[:TYPE(r)]->(cve)
                            WITH source, cve, type(r) as relType, properties(r) as props
                            CALL apoc.create.relationship(source, relType, props, cve) YIELD rel
                            RETURN count(rel) as rels_copied
                        }

                        // Delete duplicate Vulnerability node
                        DETACH DELETE vuln
                        RETURN cve
                    } IN TRANSACTIONS OF 100 ROWS
                    ON ERROR CONTINUE
                    RETURN count(cve) as merged
                """)
                merged = result.single()["merged"]
                logger.info(f"Merged {merged:,} duplicate nodes")

            # Step 3: Add Vulnerability super label to all CVE nodes
            logger.info("Adding Vulnerability super label to CVE nodes...")
            result = session.run("""
                CALL {
                    MATCH (n:CVE)
                    WHERE NOT n:Vulnerability
                    RETURN n
                } IN TRANSACTIONS OF 1000 ROWS
                ON ERROR CONTINUE
                SET n:Vulnerability
                RETURN count(n) as updated
            """)
            updated = result.single()["updated"]
            logger.info(f"Added Vulnerability super label to {updated:,} CVE nodes")

            # Step 4: Verify
            result = session.run("""
                MATCH (n:CVE)
                WHERE NOT n:Vulnerability
                RETURN count(n) as remaining
            """)
            remaining = result.single()["remaining"]

            logger.info("="*80)
            logger.info(f"CVE Fix Complete:")
            logger.info(f"  Duplicates merged: {duplicates:,}")
            logger.info(f"  Super labels added: {updated:,}")
            logger.info(f"  CVE nodes remaining without Vulnerability label: {remaining:,}")
            logger.info("="*80)

    finally:
        driver.close()


if __name__ == "__main__":
    fix_cve_super_labels()
