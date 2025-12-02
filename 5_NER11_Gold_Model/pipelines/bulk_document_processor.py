#!/usr/bin/env python3
"""
Module: bulk_document_processor.py (was 03_bulk_document_processor.py)
Specification: TASKMASTER Task 1.4
Section: Bulk Document Processing Pipeline
Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
Author: AEON Architecture Team
Purpose: Bulk process training corpus through NER11 → Hierarchy → Qdrant

CRITICAL TASK: Process 1,000+ documents → 10,000+ entities
REQUIREMENT: Idempotent processing (skip already processed)
VALIDATION: Ensure tier2 > tier1 for entire corpus
OUTPUT: Comprehensive processing log + validation report

Pipeline: Training Corpus → NER11 API → HierarchicalEntityProcessor → Embeddings → Qdrant
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

# Progress tracking
from tqdm import tqdm

# Import the embedding service
from pipelines.entity_embedding_service_hierarchical import NER11HierarchicalEmbeddingService

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/bulk_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# DOCUMENT TRACKING
# ============================================================================

@dataclass
class ProcessedDocument:
    """Record of a processed document."""
    doc_id: str
    file_path: str
    file_hash: str
    entities_extracted: int
    entities_stored: int
    tier1_unique: int
    tier2_unique: int
    hierarchy_valid: bool
    processing_time: float
    batch_id: str
    timestamp: str
    status: str  # success, failed, skipped
    error_message: Optional[str] = None


class DocumentRegistry:
    """
    Track processed documents to enable idempotent processing.

    Features:
    - File hash-based deduplication
    - Persistent state in JSONL format
    - Skip already processed documents
    - Resume interrupted processing
    """

    def __init__(self, registry_path: str):
        """
        Initialize document registry.

        Args:
            registry_path: Path to JSONL registry file
        """
        self.registry_path = Path(registry_path)
        self.processed_docs: Dict[str, ProcessedDocument] = {}
        self.processed_hashes: Set[str] = set()

        # Load existing registry
        self._load_registry()

    def _load_registry(self):
        """Load existing processed documents from registry."""
        if not self.registry_path.exists():
            logger.info(f"No existing registry found at {self.registry_path}")
            return

        try:
            with open(self.registry_path, 'r') as f:
                for line in f:
                    if line.strip():
                        doc_data = json.loads(line)
                        doc = ProcessedDocument(**doc_data)
                        self.processed_docs[doc.doc_id] = doc
                        self.processed_hashes.add(doc.file_hash)

            logger.info(f"Loaded {len(self.processed_docs)} processed documents from registry")

        except Exception as e:
            logger.error(f"Error loading registry: {str(e)}")
            raise

    def is_processed(self, file_hash: str) -> bool:
        """Check if document with this hash was already processed."""
        return file_hash in self.processed_hashes

    def add_document(self, doc: ProcessedDocument):
        """Add processed document to registry."""
        self.processed_docs[doc.doc_id] = doc
        self.processed_hashes.add(doc.file_hash)

        # Append to JSONL file
        try:
            with open(self.registry_path, 'a') as f:
                f.write(json.dumps(asdict(doc)) + '\n')
        except Exception as e:
            logger.error(f"Error writing to registry: {str(e)}")
            raise

    def get_stats(self) -> Dict:
        """Get processing statistics."""
        total = len(self.processed_docs)
        success = sum(1 for d in self.processed_docs.values() if d.status == "success")
        failed = sum(1 for d in self.processed_docs.values() if d.status == "failed")
        skipped = sum(1 for d in self.processed_docs.values() if d.status == "skipped")

        total_entities = sum(d.entities_stored for d in self.processed_docs.values() if d.status == "success")

        return {
            "total_documents": total,
            "successful": success,
            "failed": failed,
            "skipped": skipped,
            "total_entities": total_entities
        }


# ============================================================================
# DOCUMENT LOADER
# ============================================================================

class DocumentLoader:
    """
    Load documents from training data directory.

    Supports:
    - Text files (.txt)
    - JSON files (.json)
    - Recursive directory scanning
    - File hash computation for deduplication
    """

    def __init__(self, data_dir: str):
        """
        Initialize document loader.

        Args:
            data_dir: Root directory containing training data
        """
        self.data_dir = Path(data_dir)
        logger.info(f"Document loader initialized for: {data_dir}")

    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file content."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error computing hash for {file_path}: {str(e)}")
            return ""

    def load_text_file(self, file_path: Path) -> str:
        """Load text from .txt file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {str(e)}")
            return ""

    def load_json_file(self, file_path: Path) -> str:
        """Load and flatten JSON file to text."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Flatten JSON to text for entity extraction
            def flatten_json(obj, prefix=''):
                text_parts = []
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        text_parts.append(f"{key}: {value}")
                        if isinstance(value, (dict, list)):
                            text_parts.append(flatten_json(value, f"{key}."))
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            text_parts.append(flatten_json(item))
                        else:
                            text_parts.append(str(item))
                else:
                    text_parts.append(str(obj))
                return " ".join(text_parts)

            return flatten_json(data)

        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {str(e)}")
            return ""

    def discover_documents(self) -> List[Tuple[Path, str]]:
        """
        Discover all processable documents in data directory.

        Returns:
            List of (file_path, file_hash) tuples
        """
        documents = []

        # Supported file extensions
        extensions = {'.txt', '.json'}

        logger.info(f"Scanning {self.data_dir} for documents...")

        for file_path in self.data_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                file_hash = self.compute_file_hash(file_path)
                if file_hash:
                    documents.append((file_path, file_hash))

        logger.info(f"Discovered {len(documents)} documents")

        return documents

    def load_document(self, file_path: Path) -> str:
        """Load document content based on file type."""
        if file_path.suffix == '.txt':
            return self.load_text_file(file_path)
        elif file_path.suffix == '.json':
            return self.load_json_file(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return ""


# ============================================================================
# BULK DOCUMENT PROCESSOR
# ============================================================================

class BulkDocumentProcessor:
    """
    Bulk process documents through NER11 → Hierarchy → Qdrant pipeline.

    Features:
    - Idempotent processing (skip duplicates)
    - Progress tracking with tqdm
    - Error handling and retry logic
    - Comprehensive logging
    - Validation reporting
    - Batch processing optimization
    """

    def __init__(
        self,
        data_dir: str = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data",
        registry_path: str = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/processed_documents.jsonl",
        ner_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        """
        Initialize bulk document processor.

        Args:
            data_dir: Root directory containing training data
            registry_path: Path to processing registry (JSONL)
            ner_api_url: NER11 API endpoint
            qdrant_host: Qdrant host
            qdrant_port: Qdrant port
            max_retries: Maximum retry attempts for failed documents
            retry_delay: Delay between retries (seconds)
        """
        logger.info("="*70)
        logger.info("BULK DOCUMENT PROCESSOR INITIALIZATION")
        logger.info("="*70)

        # Components
        self.loader = DocumentLoader(data_dir)
        self.registry = DocumentRegistry(registry_path)
        self.service = NER11HierarchicalEmbeddingService(
            ner_api_url=ner_api_url,
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port
        )

        # Processing parameters
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Statistics
        self.stats = {
            "documents_discovered": 0,
            "documents_processed": 0,
            "documents_skipped": 0,
            "documents_failed": 0,
            "total_entities": 0,
            "tier1_distribution": defaultdict(int),
            "tier2_distribution": defaultdict(int),
            "processing_start": None,
            "processing_end": None
        }

        logger.info("Bulk processor initialized successfully")

    def process_document_with_retry(
        self,
        file_path: Path,
        file_hash: str,
        doc_id: str,
        batch_id: str
    ) -> ProcessedDocument:
        """
        Process a single document with retry logic.

        Args:
            file_path: Path to document
            file_hash: File content hash
            doc_id: Document ID
            batch_id: Batch ID

        Returns:
            ProcessedDocument record
        """
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = time.time()

                # Load document
                text = self.loader.load_document(file_path)

                if not text or len(text.strip()) < 10:
                    return ProcessedDocument(
                        doc_id=doc_id,
                        file_path=str(file_path),
                        file_hash=file_hash,
                        entities_extracted=0,
                        entities_stored=0,
                        tier1_unique=0,
                        tier2_unique=0,
                        hierarchy_valid=False,
                        processing_time=0.0,
                        batch_id=batch_id,
                        timestamp=datetime.utcnow().isoformat(),
                        status="skipped",
                        error_message="Empty or too short document"
                    )

                # Process through pipeline
                entities_stored, validation = self.service.process_document(
                    text=text,
                    doc_id=doc_id,
                    batch_id=batch_id
                )

                processing_time = time.time() - start_time

                # Create success record
                return ProcessedDocument(
                    doc_id=doc_id,
                    file_path=str(file_path),
                    file_hash=file_hash,
                    entities_extracted=validation.get('total_entities', 0),
                    entities_stored=entities_stored,
                    tier1_unique=validation.get('tier1_unique_labels', 0),
                    tier2_unique=validation.get('tier2_unique_types', 0),
                    hierarchy_valid=validation.get('hierarchy_preserved', False),
                    processing_time=processing_time,
                    batch_id=batch_id,
                    timestamp=datetime.utcnow().isoformat(),
                    status="success"
                )

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed for {file_path}: {last_error}")

                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        # All retries failed
        return ProcessedDocument(
            doc_id=doc_id,
            file_path=str(file_path),
            file_hash=file_hash,
            entities_extracted=0,
            entities_stored=0,
            tier1_unique=0,
            tier2_unique=0,
            hierarchy_valid=False,
            processing_time=0.0,
            batch_id=batch_id,
            timestamp=datetime.utcnow().isoformat(),
            status="failed",
            error_message=last_error
        )

    def process_all_documents(self) -> Dict:
        """
        Process all documents in training data directory.

        Returns:
            Processing statistics and validation report
        """
        logger.info("="*70)
        logger.info("STARTING BULK DOCUMENT PROCESSING")
        logger.info("="*70)

        self.stats["processing_start"] = datetime.utcnow().isoformat()

        # Discover documents
        documents = self.loader.discover_documents()
        self.stats["documents_discovered"] = len(documents)

        logger.info(f"Discovered {len(documents)} documents")
        logger.info(f"Registry contains {len(self.registry.processed_docs)} previously processed documents")

        # Generate batch ID
        batch_id = f"bulk_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Process documents with progress bar
        with tqdm(total=len(documents), desc="Processing documents") as pbar:
            for file_path, file_hash in documents:
                # Check if already processed (idempotent)
                if self.registry.is_processed(file_hash):
                    logger.debug(f"Skipping already processed: {file_path}")
                    self.stats["documents_skipped"] += 1
                    pbar.update(1)
                    continue

                # Generate document ID
                doc_id = f"doc_{hashlib.md5(file_hash.encode()).hexdigest()[:12]}"

                # Process document
                logger.info(f"Processing: {file_path}")
                result = self.process_document_with_retry(file_path, file_hash, doc_id, batch_id)

                # Update registry
                self.registry.add_document(result)

                # Update statistics
                if result.status == "success":
                    self.stats["documents_processed"] += 1
                    self.stats["total_entities"] += result.entities_stored
                elif result.status == "failed":
                    self.stats["documents_failed"] += 1
                elif result.status == "skipped":
                    self.stats["documents_skipped"] += 1

                pbar.update(1)

        self.stats["processing_end"] = datetime.utcnow().isoformat()

        # Generate final validation report
        validation_report = self._generate_validation_report()

        logger.info("="*70)
        logger.info("BULK PROCESSING COMPLETE")
        logger.info("="*70)

        return {
            "statistics": self.stats,
            "validation": validation_report
        }

    def _generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report for entire corpus."""
        logger.info("Generating validation report...")

        # Aggregate from registry
        successful_docs = [d for d in self.registry.processed_docs.values() if d.status == "success"]

        # Count tier distributions
        tier1_counts = defaultdict(int)
        tier2_counts = defaultdict(int)

        total_tier1 = 0
        total_tier2 = 0
        hierarchy_valid_count = 0

        for doc in successful_docs:
            total_tier1 += doc.tier1_unique
            total_tier2 += doc.tier2_unique
            if doc.hierarchy_valid:
                hierarchy_valid_count += 1

        # Calculate averages
        avg_entities_per_doc = (
            sum(d.entities_stored for d in successful_docs) / len(successful_docs)
            if successful_docs else 0
        )

        avg_tier1_per_doc = total_tier1 / len(successful_docs) if successful_docs else 0
        avg_tier2_per_doc = total_tier2 / len(successful_docs) if successful_docs else 0

        # Corpus-level validation
        corpus_tier2_valid = total_tier2 >= total_tier1

        validation_report = {
            "corpus_statistics": {
                "total_documents": len(successful_docs),
                "total_entities": sum(d.entities_stored for d in successful_docs),
                "avg_entities_per_document": round(avg_entities_per_doc, 2),
                "avg_tier1_per_document": round(avg_tier1_per_doc, 2),
                "avg_tier2_per_document": round(avg_tier2_per_doc, 2)
            },
            "hierarchy_validation": {
                "total_tier1_labels": total_tier1,
                "total_tier2_types": total_tier2,
                "tier2_greater_than_tier1": corpus_tier2_valid,
                "documents_with_valid_hierarchy": hierarchy_valid_count,
                "hierarchy_validation_rate": round(
                    hierarchy_valid_count / len(successful_docs) * 100, 2
                ) if successful_docs else 0
            },
            "quality_metrics": {
                "processing_success_rate": round(
                    len(successful_docs) / self.stats["documents_discovered"] * 100, 2
                ) if self.stats["documents_discovered"] > 0 else 0,
                "failed_documents": self.stats["documents_failed"],
                "skipped_documents": self.stats["documents_skipped"]
            },
            "validation_passed": corpus_tier2_valid and hierarchy_valid_count >= len(successful_docs) * 0.95
        }

        return validation_report

    def print_report(self, report: Dict):
        """Print formatted processing report."""
        print("\n" + "="*70)
        print("BULK DOCUMENT PROCESSING REPORT")
        print("="*70)

        print("\n📊 PROCESSING STATISTICS")
        print("-" * 70)
        stats = report["statistics"]
        print(f"Documents discovered:  {stats['documents_discovered']}")
        print(f"Documents processed:   {stats['documents_processed']}")
        print(f"Documents skipped:     {stats['documents_skipped']}")
        print(f"Documents failed:      {stats['documents_failed']}")
        print(f"Total entities stored: {stats['total_entities']}")

        print("\n🔍 CORPUS STATISTICS")
        print("-" * 70)
        corpus = report["validation"]["corpus_statistics"]
        print(f"Total entities:        {corpus['total_entities']}")
        print(f"Avg entities/doc:      {corpus['avg_entities_per_document']}")
        print(f"Avg tier1/doc:         {corpus['avg_tier1_per_document']}")
        print(f"Avg tier2/doc:         {corpus['avg_tier2_per_document']}")

        print("\n✅ HIERARCHY VALIDATION")
        print("-" * 70)
        hierarchy = report["validation"]["hierarchy_validation"]
        print(f"Total tier1 labels:    {hierarchy['total_tier1_labels']}")
        print(f"Total tier2 types:     {hierarchy['total_tier2_types']}")
        print(f"Tier2 > Tier1:         {'✅ YES' if hierarchy['tier2_greater_than_tier1'] else '❌ NO'}")
        print(f"Valid documents:       {hierarchy['documents_with_valid_hierarchy']}")
        print(f"Validation rate:       {hierarchy['hierarchy_validation_rate']}%")

        print("\n📈 QUALITY METRICS")
        print("-" * 70)
        quality = report["validation"]["quality_metrics"]
        print(f"Success rate:          {quality['processing_success_rate']}%")
        print(f"Failed documents:      {quality['failed_documents']}")
        print(f"Skipped documents:     {quality['skipped_documents']}")

        print("\n🎯 FINAL VALIDATION")
        print("-" * 70)
        if report["validation"]["validation_passed"]:
            print("Status: ✅ PASSED - Corpus meets all validation criteria")
        else:
            print("Status: ❌ FAILED - Corpus validation issues detected")

        print("\n" + "="*70)
        print("📁 Outputs:")
        print(f"  - Processing log: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/bulk_processor.log")
        print(f"  - Document registry: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/processed_documents.jsonl")
        print("="*70 + "\n")


# ============================================================================
# TEST & DEMONSTRATION
# ============================================================================

def test_bulk_processor():
    """Test bulk document processor with real training data."""
    print("="*70)
    print("BULK DOCUMENT PROCESSOR TEST")
    print("="*70)

    try:
        # Initialize processor
        print("\n📦 Initializing bulk processor...")
        processor = BulkDocumentProcessor(
            data_dir="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data",
            registry_path="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/processed_documents.jsonl",
            max_retries=3,
            retry_delay=5
        )

        # Process all documents
        print("\n🔄 Starting bulk processing...")
        report = processor.process_all_documents()

        # Print report
        processor.print_report(report)

        # Save report to file
        report_path = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/bulk_processing_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 Full report saved to: {report_path}")

        # Verify target achievement
        print("\n🎯 TARGET VALIDATION:")
        print("-" * 70)

        total_docs = report["statistics"]["documents_processed"]
        total_entities = report["statistics"]["total_entities"]

        doc_target = 1000
        entity_target = 10000

        print(f"Documents target: {doc_target} | Achieved: {total_docs} | {'✅ PASS' if total_docs >= doc_target else '⚠️ PENDING'}")
        print(f"Entities target:  {entity_target} | Achieved: {total_entities} | {'✅ PASS' if total_entities >= entity_target else '⚠️ PENDING'}")

        print("\n" + "="*70)
        print("✅ BULK PROCESSING TEST COMPLETE")
        print("="*70)

        return report

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Run bulk processing test
    test_bulk_processor()
