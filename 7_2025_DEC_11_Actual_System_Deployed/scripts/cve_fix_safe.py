#!/usr/bin/env python3
"""
Safe CVE Label Fix - Add Vulnerability label with error handling

Uses CALL {...} IN TRANSACTIONS to safely skip constraint violations
while adding Vulnerability super label to CVE nodes.

Created: 2025-12-12
"""

from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

with driver.session() as session:
    logger.info("Adding Vulnerability label to CVE nodes (safe mode)...")
    logger.info("Using transaction batching with error continuation...")

    # Use CALL {...} IN TRANSACTIONS with ON ERROR CONTINUE
    result = session.run("""
        CALL {
            MATCH (n:CVE)
            WHERE NOT n:Vulnerability
            WITH n LIMIT 15000
            SET n:Vulnerability
            RETURN count(n) as updated
        } IN TRANSACTIONS OF 100 ROWS
        ON ERROR CONTINUE
        RETURN sum(updated) as total_updated
    """)

    total = result.single()["total_updated"] or 0
    logger.info(f"Successfully updated: {total:,} CVE nodes")

    # Verify final state
    result = session.run("""
        MATCH (n:CVE)
        RETURN
            count(n) as total_cve,
            count(CASE WHEN n:Vulnerability THEN 1 END) as with_vuln,
            count(CASE WHEN NOT n:Vulnerability THEN 1 END) as without_vuln
    """)

    stats = result.single()
    logger.info("="*80)
    logger.info(f"Total CVE nodes: {stats['total_cve']:,}")
    logger.info(f"With Vulnerability label: {stats['with_vuln']:,} ({100*stats['with_vuln']/stats['total_cve']:.1f}%)")
    logger.info(f"Without Vulnerability label: {stats['without_vuln']:,} ({100*stats['without_vuln']/stats['total_cve']:.1f}%)")
    logger.info("="*80)

    if stats['without_vuln'] > 0:
        logger.info(f"\n⚠️  {stats['without_vuln']:,} nodes couldn't be updated (likely constraint conflicts)")
        logger.info("These may be duplicate nodes that need manual merge resolution")

driver.close()
