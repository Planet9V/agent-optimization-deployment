"""
Ingestion Agent - Neo4j Document Ingestion with NLP Pipeline
Wraps NLPIngestionPipeline for batch document ingestion with progress tracking and validation
"""

import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from agents.base_agent import BaseAgent
from nlp_ingestion_pipeline import NLPIngestionPipeline
from memory.qdrant_memory_manager import QdrantMemoryManager


class IngestionAgent(BaseAgent):
    """
    Neo4j Ingestion Agent

    Features:
    - Wraps NLPIngestionPipeline for document ingestion
    - Batch transaction support with configurable batch sizes
    - Progress tracking and resumability
    - Qdrant memory integration for activity tracking
    - Validation gates for data quality
    - Integration with classification and NER metadata
    - Comprehensive error handling and recovery
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize ingestion agent

        Args:
            name: Agent name
            config: Configuration dictionary with Neo4j and pipeline settings
        """
        # Extract configuration before super().__init__()
        self.neo4j_config = config.get('neo4j', {})
        self.batch_size = self.neo4j_config.get('batch_size', 100)
        self.spacy_model = config.get('nlp', {}).get('spacy_model', 'en_core_web_lg')
        self.progress_file = config.get('ingestion', {}).get('progress_file', '.ingestion_progress.json')
        self.validation_enabled = config.get('ingestion', {}).get('validation_enabled', True)

        super().__init__(name, config)

        # Initialize memory manager
        memory_config = config.get('memory', {})
        self.memory_manager = QdrantMemoryManager(
            host=memory_config.get('host', 'localhost'),
            port=memory_config.get('port', 6333),
            use_qdrant=memory_config.get('enabled', True)
        )

        # Statistics tracking
        self.stats = {
            'total_documents': 0,
            'successful_ingestions': 0,
            'failed_ingestions': 0,
            'duplicate_documents': 0,
            'skipped_documents': 0,
            'total_entities': 0,
            'total_relationships': 0,
            'total_tables': 0,
            'validation_failures': 0,
            'by_file_type': defaultdict(int),
            'by_status': defaultdict(int),
            'batch_sizes': []
        }

        # Pipeline instance
        self.pipeline: Optional[NLPIngestionPipeline] = None

    def _setup(self):
        """Agent-specific setup - initialize NLPIngestionPipeline"""
        self.logger.info("Setting up IngestionAgent")

        # Validate Neo4j configuration
        required_keys = ['uri', 'user', 'password']
        missing = [k for k in required_keys if k not in self.neo4j_config]

        if missing:
            raise ValueError(f"Missing required Neo4j configuration keys: {missing}")

        # Initialize NLP ingestion pipeline
        try:
            self.logger.info(f"Initializing NLPIngestionPipeline with spaCy model: {self.spacy_model}")

            self.pipeline = NLPIngestionPipeline(
                neo4j_uri=self.neo4j_config['uri'],
                neo4j_user=self.neo4j_config['user'],
                neo4j_password=self.neo4j_config['password'],
                spacy_model=self.spacy_model,
                batch_size=self.batch_size,
                progress_file=self.progress_file
            )

            self.logger.info("NLPIngestionPipeline initialized successfully")

            # Track initialization in memory
            self.memory_manager.track_agent_activity(
                agent_name=self.name,
                activity_type="initialization",
                data={
                    'neo4j_uri': self.neo4j_config['uri'],
                    'batch_size': self.batch_size,
                    'spacy_model': self.spacy_model
                },
                metadata={'status': 'success'}
            )

        except Exception as e:
            self.logger.error(f"Failed to initialize NLPIngestionPipeline: {e}", exc_info=True)

            # Track initialization failure
            self.memory_manager.track_agent_activity(
                agent_name=self.name,
                activity_type="initialization_error",
                data={'error': str(e)},
                metadata={'status': 'failed'}
            )

            raise

    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """
        Validate document before ingestion

        Args:
            file_path: Path to document

        Returns:
            Validation result with status and issues
        """
        validation_result = {
            'valid': True,
            'issues': [],
            'warnings': []
        }

        file_path = Path(file_path)

        # Check file exists
        if not file_path.exists():
            validation_result['valid'] = False
            validation_result['issues'].append(f"File does not exist: {file_path}")
            return validation_result

        # Check file size (warn if > 10MB)
        file_size = file_path.stat().st_size
        if file_size > 10 * 1024 * 1024:
            validation_result['warnings'].append(
                f"Large file ({file_size / (1024*1024):.1f} MB) may take longer to process"
            )

        # Check file type
        ext = file_path.suffix.lower()
        supported_formats = ['.txt', '.md', '.json', '.pdf', '.docx']
        if ext not in supported_formats:
            validation_result['valid'] = False
            validation_result['issues'].append(
                f"Unsupported file format: {ext}. Supported: {supported_formats}"
            )

        # Check readability
        try:
            if ext in ['.txt', '.md', '.json']:
                from agents.base_agent import read_file_safe
                # Test read first 100 chars
                content = read_file_safe(file_path)
                _ = content[:100]
        except Exception as e:
            validation_result['valid'] = False
            validation_result['issues'].append(f"File not readable: {e}")

        return validation_result

    def ingest_document(
        self,
        file_path: str,
        classification: Optional[Dict[str, str]] = None,
        entities: Optional[List[Dict[str, Any]]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest single document into Neo4j

        Args:
            file_path: Path to document file
            classification: Optional classification metadata (sector, subsector, doc_type)
            entities: Optional pre-extracted entities from NER
            validate: Whether to validate before ingestion

        Returns:
            Ingestion result with doc_id, stats, and status
        """
        self.logger.info(f"Ingesting document: {file_path}")

        # Validation gate
        if validate and self.validation_enabled:
            validation = self.validate_document(file_path)

            if not validation['valid']:
                self.stats['validation_failures'] += 1
                self.stats['failed_ingestions'] += 1
                self.stats['by_status']['validation_failed'] += 1

                error_msg = f"Validation failed: {validation['issues']}"
                self.logger.error(error_msg)

                # Track validation failure
                self.memory_manager.track_agent_activity(
                    agent_name=self.name,
                    activity_type="validation_failure",
                    data={
                        'file_path': file_path,
                        'issues': validation['issues']
                    },
                    metadata={'status': 'failed'}
                )

                return {
                    'status': 'validation_failed',
                    'file_path': file_path,
                    'issues': validation['issues'],
                    'warnings': validation['warnings']
                }

            if validation['warnings']:
                self.logger.warning(f"Validation warnings: {validation['warnings']}")

        # Process document through pipeline
        try:
            result = self.pipeline.process_document(file_path)

            # Update statistics
            self.stats['total_documents'] += 1
            file_ext = Path(file_path).suffix.lower()
            self.stats['by_file_type'][file_ext] += 1

            if result['status'] == 'success':
                self.stats['successful_ingestions'] += 1
                self.stats['by_status']['success'] += 1
                self.stats['total_entities'] += result.get('entities', 0)
                self.stats['total_relationships'] += result.get('relationships', 0)
                self.stats['total_tables'] += result.get('tables', 0)

                # Enhance result with classification metadata if provided
                if classification:
                    result['classification'] = classification

                # Store checkpoint in memory
                self.memory_manager.store_checkpoint(
                    checkpoint_name=f"ingestion_{result['doc_id']}",
                    state_data={
                        'doc_id': result['doc_id'],
                        'file_path': file_path,
                        'sha256': result['sha256'],
                        'entities': result.get('entities', 0),
                        'relationships': result.get('relationships', 0),
                        'classification': classification
                    },
                    metadata={
                        'timestamp': datetime.now().isoformat(),
                        'agent': self.name
                    }
                )

                # Track successful ingestion
                self.memory_manager.track_agent_activity(
                    agent_name=self.name,
                    activity_type="document_ingestion",
                    data={
                        'file_path': file_path,
                        'doc_id': result['doc_id'],
                        'entities': result.get('entities', 0),
                        'relationships': result.get('relationships', 0)
                    },
                    metadata={'status': 'success'}
                )

                self.logger.info(
                    f"Document ingested successfully: {result['doc_id']} "
                    f"({result.get('entities', 0)} entities, "
                    f"{result.get('relationships', 0)} relationships)"
                )

            elif result['status'] == 'duplicate':
                self.stats['duplicate_documents'] += 1
                self.stats['by_status']['duplicate'] += 1

                self.logger.info(f"Document already exists (duplicate): {file_path}")

            else:  # error status
                self.stats['failed_ingestions'] += 1
                self.stats['by_status']['error'] += 1

                # Track error
                self.memory_manager.track_agent_activity(
                    agent_name=self.name,
                    activity_type="ingestion_error",
                    data={
                        'file_path': file_path,
                        'error': result.get('error', 'Unknown error')
                    },
                    metadata={'status': 'failed'}
                )

                self.logger.error(f"Document ingestion failed: {result.get('error', 'Unknown error')}")

            return result

        except Exception as e:
            self.stats['failed_ingestions'] += 1
            self.stats['by_status']['exception'] += 1

            error_msg = f"Unexpected error ingesting {file_path}: {e}"
            self.logger.error(error_msg, exc_info=True)

            # Track exception
            self.memory_manager.track_agent_activity(
                agent_name=self.name,
                activity_type="ingestion_exception",
                data={
                    'file_path': file_path,
                    'error': str(e)
                },
                metadata={'status': 'exception'}
            )

            return {
                'status': 'error',
                'file_path': file_path,
                'error': str(e)
            }

    def ingest_batch(
        self,
        file_paths: List[str],
        classifications: Optional[Dict[str, Dict[str, str]]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest batch of documents

        Args:
            file_paths: List of document paths
            classifications: Optional mapping of file_path -> classification metadata
            validate: Whether to validate before ingestion

        Returns:
            Batch ingestion results
        """
        self.logger.info(f"Starting batch ingestion of {len(file_paths)} documents")

        classifications = classifications or {}

        batch_results = {
            'total': len(file_paths),
            'successful': 0,
            'failed': 0,
            'duplicates': 0,
            'validation_failures': 0,
            'results': []
        }

        # Track batch size
        self.stats['batch_sizes'].append(len(file_paths))

        # Process each document
        for i, file_path in enumerate(file_paths, 1):
            self.logger.info(f"Processing {i}/{len(file_paths)}: {file_path}")

            # Get classification if available
            classification = classifications.get(file_path)

            # Ingest document
            result = self.ingest_document(
                file_path=file_path,
                classification=classification,
                validate=validate
            )

            batch_results['results'].append(result)

            # Update batch stats
            if result['status'] == 'success':
                batch_results['successful'] += 1
            elif result['status'] == 'duplicate':
                batch_results['duplicates'] += 1
            elif result['status'] == 'validation_failed':
                batch_results['validation_failures'] += 1
            else:
                batch_results['failed'] += 1

            # Periodic checkpoint
            if i % 10 == 0:
                self.memory_manager.store_checkpoint(
                    checkpoint_name=f"batch_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    state_data={
                        'batch_total': len(file_paths),
                        'batch_processed': i,
                        'batch_successful': batch_results['successful'],
                        'batch_failed': batch_results['failed']
                    },
                    metadata={
                        'agent': self.name,
                        'batch_checkpoint': True
                    }
                )

        # Final checkpoint
        self.memory_manager.store_checkpoint(
            checkpoint_name=f"batch_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            state_data=batch_results,
            metadata={
                'agent': self.name,
                'batch_complete': True
            }
        )

        self.logger.info(
            f"Batch ingestion complete: {batch_results['successful']} successful, "
            f"{batch_results['failed']} failed, {batch_results['duplicates']} duplicates"
        )

        return batch_results

    def ingest_directory(
        self,
        directory: str,
        file_pattern: str = "**/*.md",
        classifications: Optional[Dict[str, Dict[str, str]]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest all documents in a directory

        Args:
            directory: Directory path
            file_pattern: Glob pattern for file selection
            classifications: Optional file classifications
            validate: Whether to validate before ingestion

        Returns:
            Directory ingestion results
        """
        directory = Path(directory)

        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        self.logger.info(f"Ingesting directory: {directory} (pattern: {file_pattern})")

        # Use pipeline's directory processing
        try:
            results = self.pipeline.process_directory(
                directory=str(directory),
                file_pattern=file_pattern
            )

            # Track directory ingestion
            self.memory_manager.track_agent_activity(
                agent_name=self.name,
                activity_type="directory_ingestion",
                data={
                    'directory': str(directory),
                    'pattern': file_pattern,
                    'results': results
                },
                metadata={'status': 'complete'}
            )

            return results

        except Exception as e:
            self.logger.error(f"Directory ingestion failed: {e}", exc_info=True)

            # Track failure
            self.memory_manager.track_agent_activity(
                agent_name=self.name,
                activity_type="directory_ingestion_error",
                data={
                    'directory': str(directory),
                    'error': str(e)
                },
                metadata={'status': 'failed'}
            )

            raise

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution logic (required by BaseAgent)

        Args:
            input_data: {
                'operation': 'single' | 'batch' | 'directory',
                'file_path': str (for single),
                'file_paths': List[str] (for batch),
                'directory': str (for directory),
                'file_pattern': str (optional, for directory),
                'classification': Dict (optional, for single),
                'classifications': Dict (optional, for batch),
                'validate': bool (optional)
            }

        Returns:
            Execution result
        """
        operation = input_data.get('operation', 'single')
        validate = input_data.get('validate', True)

        if operation == 'single':
            file_path = input_data.get('file_path')
            if not file_path:
                raise ValueError("file_path required for single operation")

            classification = input_data.get('classification')
            return self.ingest_document(file_path, classification, validate=validate)

        elif operation == 'batch':
            file_paths = input_data.get('file_paths')
            if not file_paths:
                raise ValueError("file_paths required for batch operation")

            classifications = input_data.get('classifications')
            return self.ingest_batch(file_paths, classifications, validate=validate)

        elif operation == 'directory':
            directory = input_data.get('directory')
            if not directory:
                raise ValueError("directory required for directory operation")

            file_pattern = input_data.get('file_pattern', '**/*.md')
            classifications = input_data.get('classifications')
            return self.ingest_directory(directory, file_pattern, classifications, validate=validate)

        else:
            raise ValueError(f"Unknown operation: {operation}")

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive ingestion statistics"""
        base_stats = super().get_stats()

        # Add ingestion-specific stats
        base_stats.update({
            'total_documents': self.stats['total_documents'],
            'successful_ingestions': self.stats['successful_ingestions'],
            'failed_ingestions': self.stats['failed_ingestions'],
            'duplicate_documents': self.stats['duplicate_documents'],
            'skipped_documents': self.stats['skipped_documents'],
            'validation_failures': self.stats['validation_failures'],
            'total_entities': self.stats['total_entities'],
            'total_relationships': self.stats['total_relationships'],
            'total_tables': self.stats['total_tables'],
            'by_file_type': dict(self.stats['by_file_type']),
            'by_status': dict(self.stats['by_status']),
            'average_batch_size': (
                sum(self.stats['batch_sizes']) / len(self.stats['batch_sizes'])
                if self.stats['batch_sizes'] else 0
            ),
            'memory_stats': self.memory_manager.get_statistics()
        })

        return base_stats

    def close(self):
        """Close connections and cleanup"""
        if self.pipeline:
            self.logger.info("Closing NLPIngestionPipeline")
            self.pipeline.close()

        self.logger.info("IngestionAgent closed")


# Convenience function for standalone usage
def ingest_document(
    file_path: str,
    neo4j_config: Dict[str, str],
    classification: Optional[Dict[str, str]] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Standalone document ingestion function

    Args:
        file_path: Path to document
        neo4j_config: Neo4j connection configuration
        classification: Optional classification metadata
        config: Optional full configuration

    Returns:
        Ingestion result
    """
    if config is None:
        config = {'neo4j': neo4j_config}
    else:
        config['neo4j'] = neo4j_config

    agent = IngestionAgent("IngestionAgent", config)

    try:
        result = agent.run({
            'operation': 'single',
            'file_path': file_path,
            'classification': classification
        })
        return result
    finally:
        agent.close()
