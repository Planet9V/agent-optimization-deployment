#!/usr/bin/env python3
"""
Simple CVE Fix - Add Vulnerability Super Label

Directly add Vulnerability super label to CVE nodes,
bypassing duplicate node issues by using IGNORE errors.

Created: 2025-12-12
"""

from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

with driver.session() as session:
    logger.info("Adding Vulnerability label to CVE nodes...")

    # Simple approach: Just add the label in batches, ignore errors
    batch_size = 5000
    offset = 0
    total_updated = 0

    while True:
        result = session.run(f"""
            MATCH (n:CVE)
            WHERE NOT n:Vulnerability
            WITH n SKIP {offset} LIMIT {batch_size}
            SET n:Vulnerability
            RETURN count(n) as updated
        """)

        updated = result.single()["updated"]
        total_updated += updated

        logger.info(f"Batch {offset//batch_size + 1}: Updated {updated:,} nodes (Total: {total_updated:,})")

        if updated < batch_size:
            break

        offset += batch_size

    # Verify
    result = session.run("""
        MATCH (n:CVE)
        WHERE NOT n:Vulnerability
        RETURN count(n) as remaining
    """)
    remaining = result.single()["remaining"]

    logger.info("="*80)
    logger.info(f"Total CVE nodes updated: {total_updated:,}")
    logger.info(f"Remaining without Vulnerability label: {remaining:,}")
    logger.info("="*80)

driver.close()
