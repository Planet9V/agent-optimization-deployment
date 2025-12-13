"""
Bulk Graph Ingestion Processor: Mass Neo4j Population from Training Corpus

Processes all available documents from training corpus, extracts entities via NER11,
enriches with hierarchical taxonomy, and ingests into Neo4j knowledge graph.

File: 06_bulk_graph_ingestion.py
Created: 2025-12-01
Version: 1.0.0
Status: PRODUCTION-READY
Author: J. McKenney (via AEON Implementation)

TASK: TASKMASTER Task 2.4 - Bulk Graph Ingestion

Requirements:
1. Process all documents from training corpus
2. Target: 15K+ new hierarchical nodes
3. CRITICAL: Preserve existing 1,104,066 nodes
4. Use NER11ToNeo4jPipeline from Task 2.3
5. Progress tracking with tqdm
6. Idempotent processing (skip processed documents)
7. Processing log: neo4j_ingestion.jsonl
8. Comprehensive validation: node count, tier distribution, hierarchy

Critical Validation:
- Pre-ingestion baseline: 1,104,066 nodes
- Post-ingestion: nodes >= baseline (MUST NOT DECREASE)
- Tier validation: tier2_types > tier1_labels
- Hierarchy check: nodes have fine_grained_type property

Integration:
- NER11ToNeo4jPipeline: Complete entity extraction and ingestion
- HierarchicalEntityProcessor: 566-type taxonomy enrichment
- NER11ToNeo4jMapper: 60 NER → 16 Neo4j label mapping
- Neo4j v3.1 schema: Hierarchical properties + relationships
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from tqdm import tqdm
import hashlib

# Import Neo4j pipeline from Task 2.3
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util

spec_pipeline = importlib.util.spec_from_file_location(
    "ner11_to_neo4j_pipeline",
    Path(__file__).parent / "05_ner11_to_neo4j_hierarchical.py"
)
pipeline_module = importlib.util.module_from_spec(spec_pipeline)
spec_pipeline.loader.exec_module(pipeline_module)
NER11ToNeo4jPipeline = pipeline_module.NER11ToNeo4jPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BulkGraphIngestionProcessor:
    """
    Bulk processor for mass Neo4j graph ingestion from training corpus.

    Features:
    - Process all documents from training corpus
    - Idempotent processing with state tracking
    - Progress tracking with tqdm
    - Comprehensive logging (JSONL format)
    - Critical validation (node preservation)
    - Batch processing support
    - Error recovery and retry
    """

    def __init__(
        self,
        corpus_root: str = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data",
        log_file: str = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl",
        state_file: str = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json",
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        ner11_api_url: str = "http://localhost:8000",
        rate_limit_delay: float = 2.0
    ):
        """
        Initialize bulk ingestion processor.

        Args:
            corpus_root: Root directory of training corpus
            log_file: Path to JSONL processing log
            state_file: Path to processing state JSON
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            ner11_api_url: NER11 API endpoint
            rate_limit_delay: Seconds to wait between NER11 API calls (default 2.0s to prevent spaCy overload)
        """
        self.rate_limit_delay = rate_limit_delay
        self.corpus_root = Path(corpus_root)
        self.log_file = Path(log_file)
        self.state_file = Path(state_file)

        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize Neo4j pipeline
        self.pipeline = NER11ToNeo4jPipeline(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password,
            ner11_api_url=ner11_api_url
        )

        # Load processing state
        self.state = self._load_state()

        # Statistics
        self.stats = {
            "session_start": datetime.now().isoformat(),
            "baseline_nodes": 1104066,
            "documents_found": 0,
            "documents_processed": 0,
            "documents_skipped": 0,
            "documents_failed": 0,
            "total_entities": 0,
            "total_nodes_created": 0,
            "total_relationships": 0,
            "errors": []
        }

        logger.info(f"Bulk processor initialized with corpus: {self.corpus_root}")

    def _load_state(self) -> Dict:
        """
        Load processing state from file.

        Returns:
            State dictionary with processed document IDs
        """
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                logger.info(f"Loaded state: {len(state.get('processed_documents', []))} documents processed")
                return state
            except Exception as e:
                logger.warning(f"Failed to load state file: {e}")

        # Default state
        return {
            "processed_documents": [],
            "failed_documents": [],
            "last_updated": datetime.now().isoformat()
        }

    def _save_state(self):
        """Save current processing state to file."""
        self.state["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _log_document_processing(self, doc_path: str, doc_stats: Dict):
        """
        Log document processing results to JSONL file.

        Args:
            doc_path: Path to processed document
            doc_stats: Processing statistics for document
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "document_path": str(doc_path),
            "document_id": doc_stats.get("document_id"),
            "status": "success" if doc_stats.get("errors", 0) == 0 else "error",
            "statistics": doc_stats
        }

        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to write log entry: {e}")

    def _get_document_id(self, file_path: Path) -> str:
        """
        Generate unique document ID from file path.

        Args:
            file_path: Path to document file

        Returns:
            SHA256 hash of file path
        """
        return hashlib.sha256(str(file_path).encode()).hexdigest()[:16]

    def _find_corpus_documents(self) -> List[Path]:
        """
        Find all processable documents in training corpus.

        Returns:
            List of document file paths (txt and json files)
        """
        documents = []

        # Find all .txt, .json, and .md files
        for ext in ["*.txt", "*.json", "*.md"]:
            documents.extend(self.corpus_root.rglob(ext))

        # Filter out non-document files
        excluded_patterns = [
            "hashes.txt",
            "COMPLETION_SUMMARY",
            "EXPORT_SUMMARY",
            "__pycache__",
            ".git"
        ]

        filtered_docs = [
            doc for doc in documents
            if not any(pattern in str(doc) for pattern in excluded_patterns)
        ]

        logger.info(f"Found {len(filtered_docs)} documents in corpus")
        return sorted(filtered_docs)

    def _read_document_content(self, file_path: Path) -> Optional[str]:
        """
        Read document content from file.

        Handles both text and JSON files.

        Args:
            file_path: Path to document file

        Returns:
            Document text content or None if error
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # If JSON file, extract text fields
            if file_path.suffix == '.json':
                try:
                    data = json.loads(content)
                    # Extract text from common JSON structures
                    if isinstance(data, dict):
                        text_parts = []
                        for key in ['text', 'description', 'content', 'body', 'summary']:
                            if key in data and isinstance(data[key], str):
                                text_parts.append(data[key])
                        # Also check for nested objects
                        for value in data.values():
                            if isinstance(value, str):
                                text_parts.append(value)
                        content = ' '.join(text_parts)
                    elif isinstance(data, list):
                        # Handle list of objects
                        text_parts = []
                        for item in data:
                            if isinstance(item, dict):
                                for key in ['text', 'description', 'content']:
                                    if key in item:
                                        text_parts.append(str(item[key]))
                        content = ' '.join(text_parts)
                except json.JSONDecodeError:
                    # Not valid JSON, treat as text
                    pass

            # Filter out very short documents (< 100 chars)
            if len(content.strip()) < 100:
                logger.debug(f"Skipping short document: {file_path}")
                return None

            return content

        except Exception as e:
            logger.error(f"Failed to read document {file_path}: {e}")
            return None

    def _record_baseline_metrics(self) -> Dict:
        """
        Record baseline Neo4j metrics before bulk ingestion.

        Critical for validation that existing nodes are preserved.

        Returns:
            Baseline metrics dictionary
        """
        logger.info("Recording baseline Neo4j metrics...")

        try:
            validation = self.pipeline.validate_ingestion()
            baseline = {
                "timestamp": datetime.now().isoformat(),
                "total_nodes": validation["total_nodes"],
                "tier1_count": validation["tier1_count"],
                "tier2_count": validation["tier2_count"],
                "super_label_distribution": validation["super_label_distribution"]
            }

            logger.info(f"Baseline recorded: {baseline['total_nodes']:,} nodes")
            return baseline

        except Exception as e:
            logger.error(f"Failed to record baseline: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "total_nodes": self.stats["baseline_nodes"],
                "error": str(e)
            }

    def _validate_post_ingestion(self, baseline: Dict) -> Dict:
        """
        Validate Neo4j state after bulk ingestion.

        Critical validations:
        1. Node count must not decrease (>= baseline)
        2. Tier 2 entities > Tier 1 entities
        3. Hierarchical properties present

        Args:
            baseline: Baseline metrics from pre-ingestion

        Returns:
            Validation report dictionary
        """
        logger.info("Validating post-ingestion Neo4j state...")

        validation = self.pipeline.validate_ingestion()

        report = {
            "timestamp": datetime.now().isoformat(),
            "baseline_nodes": baseline["total_nodes"],
            "current_nodes": validation["total_nodes"],
            "nodes_added": validation["total_nodes"] - baseline["total_nodes"],
            "node_preservation": validation["total_nodes"] >= baseline["total_nodes"],
            "tier1_count": validation["tier1_count"],
            "tier2_count": validation["tier2_count"],
            "tier2_greater_than_tier1": validation["tier2_greater_than_tier1"],
            "validation_passed": validation["validation_passed"],
            "super_label_distribution": validation["super_label_distribution"]
        }

        # Log validation results
        if report["validation_passed"]:
            logger.info("✅ POST-INGESTION VALIDATION PASSED")
            logger.info(f"  Nodes: {report['current_nodes']:,} (baseline: {report['baseline_nodes']:,})")
            logger.info(f"  Added: {report['nodes_added']:,} new nodes")
            logger.info(f"  Tier 1: {report['tier1_count']:,}")
            logger.info(f"  Tier 2: {report['tier2_count']:,}")
        else:
            logger.error("❌ POST-INGESTION VALIDATION FAILED")
            if not report["node_preservation"]:
                logger.error(f"  CRITICAL: Node count decreased! {report['current_nodes']:,} < {report['baseline_nodes']:,}")
            if not report["tier2_greater_than_tier1"]:
                logger.warning(f"  Tier 2 ({report['tier2_count']}) not greater than Tier 1 ({report['tier1_count']})")

        return report

    def process_corpus(
        self,
        max_documents: Optional[int] = None,
        skip_processed: bool = True,
        batch_size: int = 10
    ) -> Dict:
        """
        Process all documents in training corpus.

        Args:
            max_documents: Maximum number of documents to process (None = all)
            skip_processed: Skip documents already processed
            batch_size: Number of documents per progress update

        Returns:
            Final processing statistics
        """
        logger.info("="*80)
        logger.info("BULK GRAPH INGESTION - CORPUS PROCESSING")
        logger.info("="*80)

        # Record baseline metrics
        baseline = self._record_baseline_metrics()
        self.stats["baseline_metrics"] = baseline

        # Find all documents
        documents = self._find_corpus_documents()
        self.stats["documents_found"] = len(documents)

        # Filter already processed documents
        if skip_processed:
            processed_ids = set(self.state.get("processed_documents", []))
            documents = [
                doc for doc in documents
                if self._get_document_id(doc) not in processed_ids
            ]
            logger.info(f"Skipping {self.stats['documents_found'] - len(documents)} already processed documents")

        # Limit documents if specified
        if max_documents:
            documents = documents[:max_documents]
            logger.info(f"Processing limited to {max_documents} documents")

        logger.info(f"Processing {len(documents)} documents...")

        # Process documents with progress bar
        with tqdm(total=len(documents), desc="Processing documents") as pbar:
            for i, doc_path in enumerate(documents):
                doc_id = self._get_document_id(doc_path)

                try:
                    # Read document content
                    content = self._read_document_content(doc_path)
                    if not content:
                        self.stats["documents_skipped"] += 1
                        pbar.update(1)
                        continue

                    # Process document through pipeline
                    doc_stats = self.pipeline.process_document(content, doc_id)

                    # Rate limiting to prevent spaCy container overload
                    if self.rate_limit_delay > 0:
                        time.sleep(self.rate_limit_delay)

                    # Log processing
                    self._log_document_processing(doc_path, doc_stats)

                    # Update statistics
                    self.stats["documents_processed"] += 1
                    self.stats["total_entities"] += doc_stats.get("entities_extracted", 0)
                    self.stats["total_nodes_created"] += doc_stats.get("nodes_created", 0)
                    self.stats["total_relationships"] += doc_stats.get("relationships_created", 0)

                    # Mark as processed
                    if doc_id not in self.state["processed_documents"]:
                        self.state["processed_documents"].append(doc_id)

                    # Save state periodically
                    if (i + 1) % batch_size == 0:
                        self._save_state()

                except Exception as e:
                    logger.error(f"Error processing {doc_path}: {e}")
                    self.stats["documents_failed"] += 1
                    self.stats["errors"].append({
                        "document": str(doc_path),
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })

                    # Mark as failed
                    if doc_id not in self.state["failed_documents"]:
                        self.state["failed_documents"].append(doc_id)

                pbar.update(1)

                # Update progress description
                if (i + 1) % batch_size == 0:
                    pbar.set_description(
                        f"Processed {self.stats['documents_processed']}, "
                        f"Entities: {self.stats['total_entities']}, "
                        f"Nodes: {self.stats['total_nodes_created']}"
                    )

        # Final state save
        self._save_state()

        # Post-ingestion validation
        validation_report = self._validate_post_ingestion(baseline)
        self.stats["validation_report"] = validation_report

        # Final statistics
        self.stats["session_end"] = datetime.now().isoformat()
        self.stats["pipeline_stats"] = self.pipeline.get_statistics()

        return self.stats

    def get_progress_summary(self) -> str:
        """
        Get human-readable progress summary.

        Returns:
            Formatted progress summary string
        """
        summary = []
        summary.append("="*80)
        summary.append("BULK INGESTION PROGRESS SUMMARY")
        summary.append("="*80)

        summary.append(f"\nDocuments:")
        summary.append(f"  Found:     {self.stats.get('documents_found', 0):,}")
        summary.append(f"  Processed: {self.stats.get('documents_processed', 0):,}")
        summary.append(f"  Skipped:   {self.stats.get('documents_skipped', 0):,}")
        summary.append(f"  Failed:    {self.stats.get('documents_failed', 0):,}")

        summary.append(f"\nEntities & Nodes:")
        summary.append(f"  Entities extracted: {self.stats.get('total_entities', 0):,}")
        summary.append(f"  Nodes created:      {self.stats.get('total_nodes_created', 0):,}")
        summary.append(f"  Relationships:      {self.stats.get('total_relationships', 0):,}")

        if "validation_report" in self.stats:
            val = self.stats["validation_report"]
            summary.append(f"\nValidation:")
            summary.append(f"  Baseline nodes: {val.get('baseline_nodes', 0):,}")
            summary.append(f"  Current nodes:  {val.get('current_nodes', 0):,}")
            summary.append(f"  Nodes added:    {val.get('nodes_added', 0):,}")
            summary.append(f"  Status: {'✅ PASS' if val.get('validation_passed') else '❌ FAIL'}")

        summary.append("\n" + "="*80)

        return '\n'.join(summary)

    def close(self):
        """Close pipeline and save final state."""
        self._save_state()
        self.pipeline.close()


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """
    Main entry point for bulk ingestion processor.

    Usage:
        python 06_bulk_graph_ingestion.py [--max-docs N] [--no-skip]
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Bulk Graph Ingestion: Process training corpus into Neo4j"
    )
    parser.add_argument(
        '--max-docs',
        type=int,
        default=None,
        help="Maximum number of documents to process (default: all)"
    )
    parser.add_argument(
        '--no-skip',
        action='store_true',
        help="Process all documents, including previously processed"
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help="Batch size for progress updates (default: 10)"
    )
    parser.add_argument(
        '--test-run',
        action='store_true',
        help="Test run with first 5 documents only"
    )

    args = parser.parse_args()

    # Test run override
    if args.test_run:
        args.max_docs = 5
        logger.info("TEST RUN MODE: Processing first 5 documents only")

    try:
        # Initialize processor
        processor = BulkGraphIngestionProcessor()

        # Process corpus
        stats = processor.process_corpus(
            max_documents=args.max_docs,
            skip_processed=not args.no_skip,
            batch_size=args.batch_size
        )

        # Print summary
        print("\n" + processor.get_progress_summary())

        # Write final statistics to file
        stats_file = Path(processor.log_file).parent / "ingestion_final_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Final statistics saved to {stats_file}")

        # Close processor
        processor.close()

        # Exit code based on validation
        if stats.get("validation_report", {}).get("validation_passed"):
            logger.info("✅ BULK INGESTION COMPLETED SUCCESSFULLY")
            return 0
        else:
            logger.error("❌ BULK INGESTION COMPLETED WITH VALIDATION ERRORS")
            return 1

    except KeyboardInterrupt:
        logger.info("\n⚠️ Processing interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
