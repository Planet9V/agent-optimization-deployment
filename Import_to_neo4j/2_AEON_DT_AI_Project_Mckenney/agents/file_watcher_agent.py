"""
File Watcher Agent
Monitors directories for new documents and triggers processing
"""

import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Set, Callable
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DocumentEventHandler(FileSystemEventHandler):
    """Handler for document file system events"""

    def __init__(self, agent: 'FileWatcherAgent'):
        super().__init__()
        self.agent = agent

    def on_created(self, event: FileSystemEvent):
        """Handle file creation events"""
        if not event.is_directory:
            self.agent.handle_new_file(event.src_path)

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events"""
        if not event.is_directory:
            self.agent.handle_modified_file(event.src_path)

    def on_moved(self, event: FileSystemEvent):
        """Handle file move events"""
        if not event.is_directory:
            self.agent.handle_moved_file(event.src_path, event.dest_path)


class FileWatcherAgent(BaseAgent):
    """Agent responsible for monitoring directories for new documents"""

    def _setup(self):
        """Initialize file watcher"""
        # Get configuration
        monitoring_config = self.config.get('monitoring', {})

        self.watch_directories = monitoring_config.get('watch_directories', [])
        self.supported_extensions = set(monitoring_config.get('supported_extensions', []))
        self.check_interval = monitoring_config.get('check_interval_seconds', 10)
        self.batch_size = monitoring_config.get('batch_size', 5)
        self.recursive = monitoring_config.get('recursive', True)

        # Initialize state
        self.discovered_files: Set[str] = set()
        self.pending_files: List[Dict[str, Any]] = []
        self.processed_files: Set[str] = set()

        # Callbacks
        self.on_batch_ready: Optional[Callable] = None

        # Observer
        self.observer = Observer()
        self.event_handler = DocumentEventHandler(self)

        # Statistics
        self.stats = {
            'files_discovered': 0,
            'files_processed': 0,
            'files_pending': 0,
            'batches_created': 0
        }

        logger.info(f"FileWatcherAgent initialized watching {len(self.watch_directories)} directories")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start monitoring directories

        Args:
            input_data: Dictionary with optional 'duration' (seconds to monitor)

        Returns:
            Dictionary with monitoring results
        """
        duration = input_data.get('duration', None)  # None = run indefinitely
        on_batch_ready = input_data.get('on_batch_ready', None)

        if on_batch_ready:
            self.on_batch_ready = on_batch_ready

        # Initial scan of directories
        self._initial_scan()

        # Start watching
        self._start_watching()

        # Monitor for specified duration or until stopped
        if duration:
            logger.info(f"Monitoring for {duration} seconds...")
            time.sleep(duration)
            self.stop()
        else:
            logger.info("Monitoring indefinitely (call stop() to end)...")
            # Keep running until stop() is called
            try:
                while self.observer.is_alive():
                    time.sleep(self.check_interval)
                    self._process_pending_batch()
            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
                self.stop()

        return {
            'status': 'completed',
            'stats': self.get_stats()
        }

    def _initial_scan(self):
        """Perform initial scan of watch directories"""
        logger.info("Performing initial directory scan...")

        for watch_dir in self.watch_directories:
            watch_path = Path(watch_dir)

            if not watch_path.exists():
                logger.warning(f"Watch directory does not exist: {watch_dir}")
                continue

            # Scan directory
            if self.recursive:
                files = watch_path.rglob('*')
            else:
                files = watch_path.glob('*')

            for file_path in files:
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    self.handle_new_file(str(file_path))

        logger.info(f"Initial scan complete: {len(self.discovered_files)} files discovered")

    def _start_watching(self):
        """Start watching directories for changes"""
        for watch_dir in self.watch_directories:
            watch_path = Path(watch_dir)

            if watch_path.exists():
                self.observer.schedule(
                    self.event_handler,
                    str(watch_path),
                    recursive=self.recursive
                )
                logger.info(f"Watching: {watch_dir}")
            else:
                logger.warning(f"Cannot watch non-existent directory: {watch_dir}")

        self.observer.start()
        logger.info("File monitoring started")

    def stop(self):
        """Stop watching directories"""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logger.info("File monitoring stopped")

        # Process any remaining pending files
        if self.pending_files:
            self._process_pending_batch(force=True)

    def handle_new_file(self, file_path: str):
        """
        Handle new file discovery

        Args:
            file_path: Path to new file
        """
        file_path = str(Path(file_path).resolve())

        # Check if already discovered
        if file_path in self.discovered_files or file_path in self.processed_files:
            return

        # Check extension
        if Path(file_path).suffix.lower() not in self.supported_extensions:
            return

        # Extract metadata from path
        metadata = self._extract_metadata_from_path(file_path)

        # Add to discovered and pending
        self.discovered_files.add(file_path)
        self.pending_files.append({
            'file_path': file_path,
            'discovered_at': datetime.now().isoformat(),
            'metadata': metadata
        })

        self.stats['files_discovered'] += 1
        self.stats['files_pending'] = len(self.pending_files)

        logger.info(f"New file discovered: {file_path}")

        # Check if batch is ready
        if len(self.pending_files) >= self.batch_size:
            self._process_pending_batch()

    def handle_modified_file(self, file_path: str):
        """Handle file modification (treat as new file if not already processed)"""
        file_path = str(Path(file_path).resolve())

        if file_path not in self.processed_files:
            self.handle_new_file(file_path)

    def handle_moved_file(self, src_path: str, dest_path: str):
        """Handle file move (treat destination as new file)"""
        self.handle_new_file(dest_path)

    def _process_pending_batch(self, force: bool = False):
        """
        Process pending files as batch

        Args:
            force: Force processing even if batch size not reached
        """
        if not self.pending_files:
            return

        if not force and len(self.pending_files) < self.batch_size:
            return

        # Get batch
        batch = self.pending_files[:self.batch_size]
        self.pending_files = self.pending_files[self.batch_size:]

        # Mark as processed
        for item in batch:
            self.processed_files.add(item['file_path'])

        self.stats['batches_created'] += 1
        self.stats['files_processed'] += len(batch)
        self.stats['files_pending'] = len(self.pending_files)

        logger.info(f"Created batch with {len(batch)} files")

        # Trigger callback if set
        if self.on_batch_ready:
            self.on_batch_ready(batch)

        return batch

    def _extract_metadata_from_path(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from file path structure

        Args:
            file_path: File path

        Returns:
            Dictionary with extracted metadata
        """
        path = Path(file_path)
        parts = path.parts

        metadata = {
            'filename': path.name,
            'extension': path.suffix.lower(),
            'file_size': path.stat().st_size if path.exists() else 0
        }

        # Try to extract customer from path (folder name before sector/subsector)
        # Example: /customers/ACME_Corp/energy/power_grid/document.pdf
        # Look for common indicators
        for i, part in enumerate(parts):
            part_lower = part.lower()

            # Check for customer indicators
            if 'customer' in part_lower and i + 1 < len(parts):
                metadata['customer'] = parts[i + 1]

            # Check for sector indicators (from sectors.yaml)
            sectors = ['energy', 'water', 'manufacturing', 'transportation', 'chemical',
                      'communications', 'healthcare', 'commercial', 'dams', 'emergency',
                      'food', 'agriculture', 'nuclear', 'government']

            for sector in sectors:
                if sector in part_lower:
                    metadata['sector'] = sector

                    # Next part might be subsector
                    if i + 1 < len(parts) and parts[i + 1] not in ['', '.', '..']:
                        next_part = parts[i + 1]
                        # Only consider as subsector if it's a directory, not a file
                        if not next_part.endswith(tuple(self.supported_extensions)):
                            metadata['subsector'] = next_part

        return metadata

    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return {
            **self.stats,
            'discovered_files_count': len(self.discovered_files),
            'processed_files_count': len(self.processed_files),
            'pending_files_count': len(self.pending_files)
        }

    def get_pending_files(self) -> List[Dict[str, Any]]:
        """Get list of pending files"""
        return self.pending_files.copy()

    def clear_pending(self):
        """Clear pending files list"""
        self.pending_files.clear()
        self.stats['files_pending'] = 0
