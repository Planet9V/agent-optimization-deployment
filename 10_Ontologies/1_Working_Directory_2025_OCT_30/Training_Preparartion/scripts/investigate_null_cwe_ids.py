#!/usr/bin/env python3
"""
Investigate remaining NULL CWE IDs
Analyze patterns to understand why extraction failed
"""

import logging
import sys
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('investigate_null_ids.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            # Get sample of NULL ID nodes
            query = """
            MATCH (c:CWE)
            WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
            RETURN c.name as name, c.description as description
            LIMIT 20
            """

            logger.info("Sample of nodes with NULL CWE IDs:")
            logger.info("="*80)

            result = session.run(query)
            for i, record in enumerate(result, 1):
                name = record['name'] or 'NULL'
                desc = (record['description'] or 'NULL')[:100]
                logger.info(f"\n{i}. Name: {name}")
                logger.info(f"   Description: {desc}...")

            # Count patterns
            logger.info("\n" + "="*80)
            logger.info("Pattern Analysis:")

            # Nodes with no name
            no_name_query = """
            MATCH (c:CWE)
            WHERE (c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null')
            AND (c.name IS NULL OR c.name = '')
            RETURN count(c) as count
            """
            no_name = session.run(no_name_query).single()['count']
            logger.info(f"Nodes with NULL/empty name: {no_name}")

            # Nodes with name but no CWE pattern
            no_pattern_query = """
            MATCH (c:CWE)
            WHERE (c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null')
            AND c.name IS NOT NULL
            AND NOT c.name =~ '(?i).*CWE-\\d+.*'
            RETURN count(c) as count
            """
            no_pattern = session.run(no_pattern_query).single()['count']
            logger.info(f"Nodes with name but no 'CWE-###' pattern: {no_pattern}")

            # Nodes with CWE pattern but extraction failed
            failed_extraction_query = """
            MATCH (c:CWE)
            WHERE (c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null')
            AND c.name IS NOT NULL
            AND c.name =~ '(?i).*CWE-\\d+.*'
            RETURN count(c) as count
            """
            failed = session.run(failed_extraction_query).single()['count']
            logger.info(f"Nodes with CWE pattern but extraction failed: {failed}")

            # Get abstraction levels of NULL nodes
            abstraction_query = """
            MATCH (c:CWE)
            WHERE c.cwe_id IS NULL OR c.cwe_id = '' OR c.cwe_id = 'null'
            RETURN c.abstraction_level as level, count(c) as count
            ORDER BY count DESC
            """
            logger.info("\nAbstraction levels of NULL ID nodes:")
            result = session.run(abstraction_query)
            for record in result:
                level = record['level'] or 'NULL'
                count = record['count']
                logger.info(f"  {level}: {count}")

    finally:
        driver.close()

if __name__ == "__main__":
    main()
