#!/usr/bin/env python3
"""
Neo4j test data cleanup utility
- Namespace-based test data removal
- Selective node type deletion
- Relationship cleanup
- Index rebuild
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Tuple

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import Neo4jError
except ImportError:
    print("Error: neo4j-driver package required. Install with: pip install neo4j")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing/logs/clear_test_data.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestDataCleaner:
    """Manages Neo4j test data cleanup operations"""

    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """Initialize cleaner with Neo4j connection details"""
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver = None
        self.session = None
        self.stats = {
            'nodes_deleted': 0,
            'relationships_deleted': 0,
            'indexes_checked': 0,
            'errors': 0
        }

    def connect(self) -> bool:
        """Establish Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info(f"{Colors.OKGREEN}✓ Connected to Neo4j{Colors.ENDC}")
            return True
        except Neo4jError as e:
            logger.error(f"{Colors.FAIL}✗ Connection failed: {e}{Colors.ENDC}")
            return False

    def disconnect(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info(f"{Colors.OKGREEN}✓ Disconnected from Neo4j{Colors.ENDC}")

    def get_namespace_count(self, namespace: str) -> int:
        """Count nodes in a namespace"""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (n)
                WHERE n.namespace = $namespace
                RETURN count(n) as count
                """,
                namespace=namespace
            )
            return result.single()['count']

    def delete_by_namespace(self, namespace: str, dry_run: bool = False) -> Tuple[int, int]:
        """
        Delete all nodes and relationships in a namespace

        Args:
            namespace: Namespace identifier (e.g., 'test_2024', 'dev_01')
            dry_run: If True, only count deletions without executing

        Returns:
            Tuple of (nodes_deleted, relationships_deleted)
        """
        logger.info(f"Deleting test data in namespace: {namespace}")

        with self.driver.session(database=self.database) as session:
            # Count before deletion
            count_result = session.run(
                """
                MATCH (n)
                WHERE n.namespace = $namespace
                RETURN count(n) as count
                """,
                namespace=namespace
            )
            node_count = count_result.single()['count']

            if dry_run:
                logger.info(f"{Colors.WARNING}[DRY RUN] Would delete {node_count} nodes in namespace '{namespace}'{Colors.ENDC}")
                return node_count, 0

            # Delete all nodes and their relationships
            result = session.run(
                """
                MATCH (n)
                WHERE n.namespace = $namespace
                WITH n, size((n)-[]-()) as rel_count
                DETACH DELETE n
                RETURN count(n) as nodes_deleted
                """,
                namespace=namespace
            )

            deleted = result.single()['nodes_deleted']
            self.stats['nodes_deleted'] += deleted
            logger.info(f"{Colors.OKGREEN}✓ Deleted {deleted} nodes from namespace '{namespace}'{Colors.ENDC}")

            return deleted, 0

    def delete_by_node_type(self, node_type: str, dry_run: bool = False) -> int:
        """
        Delete all nodes of a specific type

        Args:
            node_type: Node type/label (e.g., 'TEST_CVE', 'TEST_VULNERABILITY')
            dry_run: If True, only count deletions

        Returns:
            Number of nodes deleted
        """
        logger.info(f"Deleting nodes of type: {node_type}")

        with self.driver.session(database=self.database) as session:
            # Count before deletion
            count_result = session.run(
                f"""
                MATCH (n:{node_type})
                RETURN count(n) as count
                """
            )
            node_count = count_result.single()['count']

            if dry_run:
                logger.info(f"{Colors.WARNING}[DRY RUN] Would delete {node_count} nodes of type '{node_type}'{Colors.ENDC}")
                return node_count

            # Delete all nodes
            result = session.run(
                f"""
                MATCH (n:{node_type})
                DETACH DELETE n
                RETURN count(n) as deleted
                """
            )

            deleted = result.single()['deleted']
            self.stats['nodes_deleted'] += deleted
            logger.info(f"{Colors.OKGREEN}✓ Deleted {deleted} nodes of type '{node_type}'{Colors.ENDC}")

            return deleted

    def cleanup_orphaned_relationships(self, dry_run: bool = False) -> int:
        """
        Remove relationships where one endpoint is missing

        Returns:
            Number of relationships deleted
        """
        logger.info("Cleaning up orphaned relationships...")

        with self.driver.session(database=self.database) as session:
            if dry_run:
                result = session.run(
                    """
                    MATCH (n)-[r]-() WHERE n IS NULL OR NOT EXISTS(n)
                    RETURN count(r) as count
                    """
                )
                count = result.single()['count']
                logger.info(f"{Colors.WARNING}[DRY RUN] Would delete {count} orphaned relationships{Colors.ENDC}")
                return count

            result = session.run(
                """
                MATCH (n)-[r]-() WHERE n IS NULL OR NOT EXISTS(n)
                DELETE r
                RETURN count(r) as deleted
                """
            )

            deleted = result.single()['deleted']
            self.stats['relationships_deleted'] += deleted
            logger.info(f"{Colors.OKGREEN}✓ Deleted {deleted} orphaned relationships{Colors.ENDC}")

            return deleted

    def rebuild_indexes(self) -> bool:
        """Rebuild all Neo4j indexes for consistency"""
        logger.info("Rebuilding indexes...")

        try:
            with self.driver.session(database=self.database) as session:
                # Get all indexes
                result = session.run("SHOW INDEXES")
                indexes = list(result)

                if not indexes:
                    logger.info(f"{Colors.WARNING}No indexes found to rebuild{Colors.ENDC}")
                    return True

                logger.info(f"Found {len(indexes)} indexes")

                # Trigger index rebuild
                for index in indexes:
                    try:
                        session.run(f"CALL db.index.rebuild('{index['name']}')")
                        self.stats['indexes_checked'] += 1
                    except Exception as e:
                        logger.warning(f"Could not rebuild index {index['name']}: {e}")

                logger.info(f"{Colors.OKGREEN}✓ Index rebuild completed{Colors.ENDC}")
                return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ Index rebuild failed: {e}{Colors.ENDC}")
            self.stats['errors'] += 1
            return False

    def get_database_stats(self) -> Dict:
        """Get current database statistics"""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (n)
                RETURN
                    count(n) as total_nodes,
                    size(collect(distinct labels(n))) as label_count
                """
            )
            row = result.single()
            return {
                'total_nodes': row['total_nodes'],
                'label_count': row['label_count']
            }

    def print_stats(self):
        """Print cleanup statistics"""
        print("\n" + "=" * 50)
        print(f"{Colors.BOLD}Cleanup Statistics{Colors.ENDC}")
        print("=" * 50)
        print(f"Nodes Deleted:          {self.stats['nodes_deleted']}")
        print(f"Relationships Deleted:  {self.stats['relationships_deleted']}")
        print(f"Indexes Checked:        {self.stats['indexes_checked']}")
        print(f"Errors:                 {self.stats['errors']}")
        print("=" * 50 + "\n")


def main():
    """Main cleanup routine"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Neo4j test data cleanup utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Delete test namespace (dry run)
  %(prog)s --namespace test_2024 --dry-run

  # Delete specific node type
  %(prog)s --type TEST_CVE

  # Full cleanup (namespace + orphans)
  %(prog)s --namespace dev_01 --cleanup-orphans
        """
    )

    parser.add_argument('--uri', default=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
                        help='Neo4j connection URI')
    parser.add_argument('--user', default=os.getenv('NEO4J_USER', 'neo4j'),
                        help='Neo4j username')
    parser.add_argument('--password', default=os.getenv('NEO4J_PASSWORD'),
                        help='Neo4j password')
    parser.add_argument('--namespace', help='Namespace to delete (e.g., test_2024)')
    parser.add_argument('--type', help='Node type/label to delete')
    parser.add_argument('--cleanup-orphans', action='store_true',
                        help='Remove orphaned relationships')
    parser.add_argument('--rebuild-indexes', action='store_true',
                        help='Rebuild indexes after cleanup')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without executing')
    parser.add_argument('--stats', action='store_true',
                        help='Show database statistics only')

    args = parser.parse_args()

    # Verify password
    if not args.password:
        print(f"{Colors.FAIL}Error: NEO4J_PASSWORD environment variable required{Colors.ENDC}")
        sys.exit(1)

    # Initialize cleaner
    cleaner = TestDataCleaner(args.uri, args.user, args.password)

    if not cleaner.connect():
        sys.exit(1)

    try:
        # Show current stats
        if args.stats or (not args.namespace and not args.type):
            stats = cleaner.get_database_stats()
            print(f"\n{Colors.OKBLUE}Database Statistics:{Colors.ENDC}")
            print(f"  Total Nodes: {stats['total_nodes']}")
            print(f"  Label Types: {stats['label_count']}\n")

        # Execute cleanup operations
        if args.namespace:
            cleaner.delete_by_namespace(args.namespace, dry_run=args.dry_run)

        if args.type:
            cleaner.delete_by_node_type(args.type, dry_run=args.dry_run)

        if args.cleanup_orphans:
            cleaner.cleanup_orphaned_relationships(dry_run=args.dry_run)

        if args.rebuild_indexes and not args.dry_run:
            cleaner.rebuild_indexes()

        cleaner.print_stats()

    finally:
        cleaner.disconnect()


if __name__ == '__main__':
    main()
