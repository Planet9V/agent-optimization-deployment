"""
Orchestrator Agent
Central coordination agent managing the entire document ingestion pipeline
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import threading
import queue

from .base_agent import BaseAgent
from .file_watcher_agent import FileWatcherAgent
from .format_converter_agent import FormatConverterAgent
from .classifier_agent import ClassifierAgent
from .ner_agent import NERAgent
from .ingestion_agent import IngestionAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """Central orchestrator managing the document ingestion workflow"""

    def _setup(self):
        """Initialize orchestrator and sub-agents"""
        # Initialize sub-agents
        self.file_watcher = FileWatcherAgent("FileWatcher", self.config)
        self.format_converter = FormatConverterAgent("FormatConverter", self.config)
        self.classifier = ClassifierAgent("Classifier", self.config)
        self.ner = NERAgent("NER", self.config)
        self.ingestion = IngestionAgent("Ingestion", self.config)

        # Processing configuration
        self.parallel_workers = self.config.get('monitoring', {}).get('parallel_workers', 3)
        self.batch_size = self.config.get('monitoring', {}).get('batch_size', 5)

        # Processing queue
        self.processing_queue = queue.Queue()

        # State tracking
        self.state = {
            'status': 'initialized',
            'started_at': None,
            'files_discovered': 0,
            'files_converted': 0,
            'files_classified': 0,
            'files_ner_processed': 0,
            'files_ingested': 0,
            'errors': []
        }

        # Worker threads
        self.workers: List[threading.Thread] = []
        self.running = False

        logger.info(f"OrchestratorAgent initialized with {self.parallel_workers} workers")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the document ingestion pipeline

        Args:
            input_data: Dictionary with optional 'mode' and 'duration'
                - mode: 'watch' (continuous monitoring) or 'batch' (one-time processing)
                - duration: monitoring duration in seconds (for watch mode)

        Returns:
            Dictionary with pipeline execution results
        """
        mode = input_data.get('mode', 'watch')
        duration = input_data.get('duration', None)

        self.state['status'] = 'running'
        self.state['started_at'] = datetime.now().isoformat()
        self.running = True

        logger.info(f"Starting orchestrator in {mode} mode")

        if mode == 'watch':
            return self._run_watch_mode(duration)
        elif mode == 'batch':
            return self._run_batch_mode(input_data)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _run_watch_mode(self, duration: Optional[int] = None) -> Dict[str, Any]:
        """
        Run in continuous monitoring mode

        Args:
            duration: Optional duration in seconds

        Returns:
            Execution results
        """
        logger.info("Starting watch mode...")

        # Start worker threads
        self._start_workers()

        # Set up file watcher callback
        def on_batch_ready(batch: List[Dict[str, Any]]):
            """Callback when file watcher has a batch ready"""
            logger.info(f"Batch ready with {len(batch)} files")
            self.state['files_discovered'] += len(batch)

            # Add to processing queue
            for item in batch:
                self.processing_queue.put(item)

        # Start file watcher
        try:
            self.file_watcher.run({
                'duration': duration,
                'on_batch_ready': on_batch_ready
            })
        except KeyboardInterrupt:
            logger.info("Watch mode interrupted by user")
        finally:
            self.stop()

        return {
            'status': 'completed',
            'mode': 'watch',
            'state': self.get_state()
        }

    def _run_batch_mode(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run in one-time batch processing mode

        Args:
            input_data: Dictionary with 'files' list

        Returns:
            Execution results
        """
        files = input_data.get('files', [])

        if not files:
            raise ValueError("files list required for batch mode")

        logger.info(f"Starting batch mode with {len(files)} files")

        # Start worker threads
        self._start_workers()

        # Add files to processing queue
        for file_path in files:
            metadata = self.file_watcher._extract_metadata_from_path(file_path)
            self.processing_queue.put({
                'file_path': file_path,
                'metadata': metadata
            })

        self.state['files_discovered'] = len(files)

        # Wait for processing to complete
        self.processing_queue.join()

        # Stop workers
        self.stop()

        return {
            'status': 'completed',
            'mode': 'batch',
            'state': self.get_state()
        }

    def _start_workers(self):
        """Start worker threads for parallel processing"""
        logger.info(f"Starting {self.parallel_workers} worker threads...")

        for i in range(self.parallel_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"Worker-{i+1}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)

        logger.info(f"{len(self.workers)} workers started")

    def _worker_loop(self):
        """Worker thread main loop"""
        thread_name = threading.current_thread().name

        logger.info(f"{thread_name} started")

        while self.running:
            try:
                # Get item from queue with timeout
                item = self.processing_queue.get(timeout=1)

                try:
                    # Process the document through the pipeline
                    self._process_document(item)
                except Exception as e:
                    logger.error(f"{thread_name} error processing {item.get('file_path')}: {e}")
                    self.state['errors'].append({
                        'file_path': item.get('file_path'),
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
                finally:
                    self.processing_queue.task_done()

            except queue.Empty:
                # No items in queue, continue loop
                continue
            except Exception as e:
                logger.error(f"{thread_name} unexpected error: {e}")

        logger.info(f"{thread_name} stopped")

    def _process_document(self, item: Dict[str, Any]):
        """
        Process document through the pipeline

        Args:
            item: Dictionary with 'file_path' and 'metadata'
        """
        file_path = item['file_path']
        metadata = item['metadata']

        logger.info(f"Processing: {file_path}")

        # Step 1: Format Conversion
        conversion_result = self.format_converter.run(item)

        if conversion_result.get('status') != 'success':
            logger.warning(f"Conversion failed for {file_path}: {conversion_result.get('reason')}")
            return

        self.state['files_converted'] += 1

        # Step 2: Classification
        try:
            # Read converted markdown
            from agents.base_agent import read_file_safe
            markdown_content = read_file_safe(conversion_result['output_file'])

            classification_result = self.classifier.run({
                'markdown_content': markdown_content,
                'metadata': metadata
            })

            if classification_result.get('status') == 'success':
                self.state['files_classified'] += 1
                # Update metadata with classification
                metadata.update({
                    'sector': classification_result.get('sector'),
                    'subsector': classification_result.get('subsector'),
                    'document_type': classification_result.get('document_type'),
                    'classification_confidence': classification_result.get('confidence')
                })
                logger.info(f"Classified as {classification_result.get('sector')}/{classification_result.get('subsector')}")
            else:
                logger.warning(f"Classification failed: {classification_result.get('reason')}")
        except Exception as e:
            logger.error(f"Classification error: {e}")

        # Step 3: NER Processing
        try:
            ner_result = self.ner.run({
                'markdown_content': markdown_content,
                'sector': metadata.get('sector', 'general'),
                'metadata': metadata
            })

            if ner_result.get('status') == 'success':
                self.state['files_ner_processed'] += 1
                entities = ner_result.get('entities', [])
                relationships = ner_result.get('relationships', [])
                metadata['entities_count'] = len(entities)
                metadata['entities'] = entities
                logger.info(f"Extracted {len(entities)} entities")
            else:
                logger.warning(f"NER processing failed: {ner_result.get('reason')}")
        except Exception as e:
            logger.error(f"NER processing error: {e}")

        # Step 4: Neo4j Ingestion
        try:
            ingestion_result = self.ingestion.run({
                'entities': ner_result.get('entities', []),
                'relationships': ner_result.get('relationships', []),
                'metadata': metadata,
                'markdown_content': markdown_content,
                'source_file': file_path
            })

            if ingestion_result.get('status') == 'success':
                self.state['files_ingested'] += 1
                metadata['neo4j_doc_id'] = ingestion_result.get('doc_id')
                logger.info(f"Ingested to Neo4j: {ingestion_result.get('doc_id')}")
            else:
                logger.warning(f"Ingestion failed: {ingestion_result.get('reason')}")
        except Exception as e:
            logger.error(f"Ingestion error: {e}")

        logger.info(f"Completed processing: {file_path}")

    def stop(self):
        """Stop the orchestrator and all workers"""
        logger.info("Stopping orchestrator...")

        self.running = False

        # Stop file watcher if running
        try:
            self.file_watcher.stop()
        except:
            pass

        # Wait for workers to finish
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=5)

        self.workers.clear()

        self.state['status'] = 'stopped'
        logger.info("Orchestrator stopped")

    def get_state(self) -> Dict[str, Any]:
        """Get current orchestrator state"""
        return {
            **self.state,
            'queue_size': self.processing_queue.qsize(),
            'workers_active': sum(1 for w in self.workers if w.is_alive()),
            'file_watcher_stats': self.file_watcher.get_stats(),
            'converter_stats': self.format_converter.get_stats(),
            'ingestion_stats': self.ingestion.get_stats()
        }

    def get_progress_report(self) -> str:
        """Generate human-readable progress report"""
        state = self.get_state()
        ingestion_stats = state.get('ingestion_stats', {})

        report = f"""
╔══════════════════════════════════════════════════════════╗
║  AEON Document Ingestion Pipeline - Progress Report     ║
╚══════════════════════════════════════════════════════════╝

Status: {state['status'].upper()}
Started: {state['started_at']}

Pipeline Progress:
  📂 Files Discovered:    {state['files_discovered']}
  🔄 Files Converted:     {state['files_converted']}
  🏷️  Files Classified:   {state['files_classified']}
  🔍 Files NER Processed: {state['files_ner_processed']}
  💾 Files Ingested:      {state['files_ingested']}

Processing:
  ⏳ Queue Size:          {state['queue_size']}
  👷 Active Workers:      {state['workers_active']}/{self.parallel_workers}

Errors: {len(state['errors'])}

Format Converter Stats:
  ✅ Successful:          {state['converter_stats'].get('successful', 0)}
  ❌ Failed:              {state['converter_stats'].get('failed', 0)}
  ⏭️  Skipped:            {state['converter_stats'].get('skipped', 0)}
  📊 Success Rate:        {state['converter_stats'].get('success_rate', 0):.1f}%

Neo4j Ingestion Stats:
  📝 Documents Ingested:  {ingestion_stats.get('documents_ingested', 0)}
  🏷️  Entities Created:   {ingestion_stats.get('entities_created', 0)}
  🔗 Relationships:       {ingestion_stats.get('relationships_created', 0)}
  ❌ Failed:              {ingestion_stats.get('failed', 0)}
  📊 Success Rate:        {ingestion_stats.get('success_rate', 0):.1f}%

"""

        if state['errors']:
            report += "\nRecent Errors:\n"
            for error in state['errors'][-5:]:  # Last 5 errors
                report += f"  - {error['file_path']}: {error['error']}\n"

        report += "\n" + "="*60 + "\n"

        return report
