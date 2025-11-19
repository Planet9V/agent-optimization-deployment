#!/usr/bin/env python3
"""
Master Document Processing Script
Processes all 932 documents in /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j
Uses parallel processing with progress tracking and metadata deduplication.
"""

import os
import sys
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Tuple
import argparse

# Add NLP pipeline to path
sys.path.insert(0, '/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney')

try:
    from nlp_ingestion_pipeline import NLPIngestionPipeline, Neo4jBatchInserter
except ImportError as e:
    print(f"ERROR: Failed to import NLP pipeline: {e}")
    print("Ensure the NLP pipeline is in: /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def _process_single_document_worker(file_path: Path, file_hash: str, neo4j_uri: str, neo4j_user: str, neo4j_password: str) -> Dict:
    """
    Worker function to process a single document.
    This must be a module-level function (not instance method) to avoid pickle errors.
    """
    try:
        # Create fresh processor instance for this process
        processor = NLPIngestionPipeline(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password
        )

        # Process the document
        result = processor.process_document(str(file_path))

        # Cleanup
        processor.close()

        # Parse result and return standardized format
        if result.get('status') == 'success':
            return {
                'file_path': str(file_path),
                'sha256_hash': file_hash,
                'status': 'SUCCESS',
                'entities': result.get('entities', 0),
                'relationships': result.get('relationships', 0),
                'doc_id': result.get('doc_id', '')
            }
        elif result.get('status') == 'duplicate':
            return {
                'file_path': str(file_path),
                'sha256_hash': file_hash,
                'status': 'DUPLICATE',
                'entities': 0,
                'relationships': 0
            }
        else:
            return {
                'file_path': str(file_path),
                'sha256_hash': file_hash,
                'status': 'FAILED',
                'error': result.get('error', 'Unknown error'),
                'entities': 0,
                'relationships': 0
            }

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return {
            'file_path': str(file_path),
            'sha256_hash': file_hash,
            'status': 'FAILED',
            'error': str(e),
            'entities': 0,
            'relationships': 0
        }


class MasterDocumentProcessor:
    """Orchestrates processing of all documents with parallel execution."""

    def __init__(self, root_dir: str, neo4j_uri: str, neo4j_user: str, neo4j_password: str, max_workers: int = 4):
        self.root_dir = Path(root_dir)
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.max_workers = max_workers

        # DON'T initialize Neo4j here - will cause pickle errors in multiprocessing
        # Create connections inside worker functions instead

        # Supported file extensions
        self.supported_extensions = {'.md', '.txt', '.pdf', '.docx', '.json'}

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def is_already_processed(self, file_hash: str) -> bool:
        """Check if file hash exists in Metadata nodes."""
        # Create temporary connection for checking (not picklable, so do it here)
        neo4j = Neo4jBatchInserter(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
        result = neo4j.check_document_exists(file_hash)
        neo4j.close()
        return result

    def discover_all_documents(self) -> List[Tuple[Path, str]]:
        """
        Find all processable documents in directory tree.
        Returns list of (file_path, sha256_hash) tuples.
        """
        documents = []

        logger.info(f"Scanning directory: {self.root_dir}")

        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    file_hash = self.calculate_file_hash(file_path)
                    documents.append((file_path, file_hash))
                except Exception as e:
                    logger.error(f"Error hashing {file_path}: {e}")

        logger.info(f"Found {len(documents)} documents")
        return documents

    def filter_unprocessed(self, documents: List[Tuple[Path, str]]) -> List[Tuple[Path, str]]:
        """Filter out already processed documents."""
        unprocessed = []
        processed_count = 0

        logger.info("Checking for already processed documents...")

        for file_path, file_hash in documents:
            if self.is_already_processed(file_hash):
                processed_count += 1
                logger.debug(f"Already processed: {file_path}")
            else:
                unprocessed.append((file_path, file_hash))

        logger.info(f"Already processed: {processed_count}")
        logger.info(f"Remaining to process: {len(unprocessed)}")

        return unprocessed

    def process_all_documents(self, documents: List[Tuple[Path, str]]) -> Dict:
        """
        Process all documents in parallel.
        Returns statistics dictionary.
        """
        stats = {
            'total': len(documents),
            'successful': 0,
            'duplicates': 0,
            'failed': 0,
            'total_entities': 0,
            'total_relationships': 0,
            'start_time': datetime.now(),
            'failed_files': []
        }

        logger.info(f"Processing {len(documents)} documents with {self.max_workers} workers...")

        # Process in parallel
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks to module-level worker function (avoids pickle errors)
            future_to_doc = {
                executor.submit(
                    _process_single_document_worker,
                    file_path,
                    file_hash,
                    self.neo4j_uri,
                    self.neo4j_user,
                    self.neo4j_password
                ): (file_path, file_hash)
                for file_path, file_hash in documents
            }

            # Process results as they complete
            for future in as_completed(future_to_doc):
                file_path, file_hash = future_to_doc[future]

                try:
                    result = future.result()

                    if result['status'] == 'SUCCESS':
                        stats['successful'] += 1
                        stats['total_entities'] += result.get('entities', 0)
                        stats['total_relationships'] += result.get('relationships', 0)
                        logger.info(f"✓ [{stats['successful']}/{stats['total']}] Processed: {file_path.name} "
                                  f"(Entities: {result.get('entities', 0)}, Relationships: {result.get('relationships', 0)})")
                    elif result['status'] == 'DUPLICATE':
                        stats['duplicates'] += 1
                        logger.info(f"⊗ [{stats['duplicates']} duplicates] Skipped (already processed): {file_path.name}")
                    else:
                        stats['failed'] += 1
                        stats['failed_files'].append(str(file_path))
                        logger.error(f"✗ [{stats['failed']} failed] Failed: {file_path.name} - {result.get('error', 'Unknown error')}")

                except Exception as e:
                    stats['failed'] += 1
                    stats['failed_files'].append(str(file_path))
                    logger.error(f"Exception processing {file_path}: {e}")

        stats['end_time'] = datetime.now()
        stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()

        return stats

    def print_final_report(self, stats: Dict):
        """Print comprehensive processing report."""
        print("\n" + "="*80)
        print("DOCUMENT PROCESSING COMPLETE")
        print("="*80)
        print(f"Total Documents: {stats['total']}")
        print(f"Successful: {stats['successful']} ({stats['successful']/stats['total']*100:.1f}%)")
        print(f"Failed: {stats['failed']} ({stats['failed']/stats['total']*100:.1f}%)")
        print(f"\nTotal Entities Extracted: {stats['total_entities']:,}")
        print(f"Total Relationships Created: {stats['total_relationships']:,}")
        print(f"\nProcessing Time: {stats['duration']:.1f} seconds")
        print(f"Processing Rate: {stats['successful']/stats['duration']:.2f} documents/second")

        if stats['failed_files']:
            print(f"\nFailed Files ({len(stats['failed_files'])}):")
            for failed_file in stats['failed_files'][:20]:  # Show first 20
                print(f"  - {failed_file}")
            if len(stats['failed_files']) > 20:
                print(f"  ... and {len(stats['failed_files'])-20} more")

        print("="*80)


def main():
    parser = argparse.ArgumentParser(description='Process all documents in Import_to_neo4j directory')
    parser.add_argument('--root-dir', default='/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j',
                       help='Root directory to scan for documents')
    parser.add_argument('--neo4j-uri', default='bolt://localhost:7687',
                       help='Neo4j connection URI')
    parser.add_argument('--neo4j-user', default='neo4j',
                       help='Neo4j username')
    parser.add_argument('--neo4j-password', required=True,
                       help='Neo4j password')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers (default: 4)')
    parser.add_argument('--skip-processed', action='store_true',
                       help='Skip already processed documents (check SHA256 hash)')

    args = parser.parse_args()

    # Initialize processor
    processor = MasterDocumentProcessor(
        root_dir=args.root_dir,
        neo4j_uri=args.neo4j_uri,
        neo4j_user=args.neo4j_user,
        neo4j_password=args.neo4j_password,
        max_workers=args.workers
    )

    # Discover all documents
    all_documents = processor.discover_all_documents()

    if not all_documents:
        logger.error("No documents found!")
        return 1

    # Filter if requested
    if args.skip_processed:
        documents_to_process = processor.filter_unprocessed(all_documents)
    else:
        documents_to_process = all_documents

    if not documents_to_process:
        logger.info("All documents already processed!")
        return 0

    # Process all documents
    stats = processor.process_all_documents(documents_to_process)

    # Print final report
    processor.print_final_report(stats)

    # Return exit code based on success rate
    success_rate = stats['successful'] / stats['total']
    if success_rate >= 0.95:
        return 0  # Success
    elif success_rate >= 0.80:
        return 1  # Partial success
    else:
        return 2  # Mostly failed


if __name__ == '__main__':
    sys.exit(main())
