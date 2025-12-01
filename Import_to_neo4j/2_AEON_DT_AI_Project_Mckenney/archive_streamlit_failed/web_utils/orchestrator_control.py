"""
Orchestrator Control Module for AEON Web Interface
Manages orchestrator lifecycle and provides status monitoring
"""

import sys
import os
import threading
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import yaml
from agents.orchestrator_agent import OrchestratorAgent

logger = logging.getLogger(__name__)


class OrchestratorController:
    """Manages orchestrator agent lifecycle for web interface"""

    def __init__(self, config_path: str = None):
        """
        Initialize orchestrator controller

        Args:
            config_path: Path to main_config.yaml (auto-detects if None)
        """
        if config_path is None:
            # Auto-detect config path
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "main_config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

        self._orchestrator: Optional[OrchestratorAgent] = None
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        logger.info(f"OrchestratorController initialized with config: {self.config_path}")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Resolve environment variables in config
            if 'neo4j' in config and 'password' in config['neo4j']:
                password = config['neo4j']['password']
                if password.startswith('${') and password.endswith('}'):
                    env_var = password[2:-1]
                    config['neo4j']['password'] = os.getenv(env_var, 'neo4j@openspg')

            return config
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            raise

    def start(self, mode: str = "watch") -> Dict[str, Any]:
        """
        Start the orchestrator agent

        Args:
            mode: Orchestrator mode ('watch' for continuous monitoring)

        Returns:
            Status dictionary
        """
        with self._lock:
            if self._orchestrator and hasattr(self._orchestrator, 'running') and self._orchestrator.running:
                return {
                    "status": "already_running",
                    "message": "Orchestrator is already running"
                }

            try:
                # Create orchestrator instance
                self._orchestrator = OrchestratorAgent("WebOrchestrator", self.config)

                # Start in background thread
                self._thread = threading.Thread(
                    target=self._run_orchestrator,
                    args=(mode,),
                    daemon=True,
                    name="OrchestratorThread"
                )
                self._thread.start()

                logger.info(f"Orchestrator started in {mode} mode")

                return {
                    "status": "started",
                    "message": f"Orchestrator started successfully in {mode} mode"
                }

            except Exception as e:
                logger.error(f"Failed to start orchestrator: {e}")
                return {
                    "status": "error",
                    "message": f"Failed to start: {str(e)}"
                }

    def _run_orchestrator(self, mode: str):
        """Internal method to run orchestrator in thread"""
        try:
            self._orchestrator.run({'mode': mode})
        except Exception as e:
            logger.error(f"Orchestrator execution error: {e}")

    def stop(self) -> Dict[str, Any]:
        """
        Stop the orchestrator agent

        Returns:
            Status dictionary
        """
        with self._lock:
            if not self._orchestrator:
                return {
                    "status": "not_running",
                    "message": "Orchestrator is not running"
                }

            try:
                # Stop orchestrator
                if hasattr(self._orchestrator, 'stop'):
                    self._orchestrator.stop()

                # Wait for thread to complete (with timeout)
                if self._thread and self._thread.is_alive():
                    self._thread.join(timeout=5.0)

                logger.info("Orchestrator stopped")

                return {
                    "status": "stopped",
                    "message": "Orchestrator stopped successfully"
                }

            except Exception as e:
                logger.error(f"Failed to stop orchestrator: {e}")
                return {
                    "status": "error",
                    "message": f"Failed to stop: {str(e)}"
                }

    def get_status(self) -> Dict[str, Any]:
        """
        Get current orchestrator status

        Returns:
            Status dictionary with comprehensive information
        """
        with self._lock:
            if not self._orchestrator:
                return {
                    "running": False,
                    "status": "not_initialized",
                    "message": "Orchestrator not initialized"
                }

            try:
                # Get state from orchestrator
                state = self._orchestrator.get_state()

                # Add thread status
                state["thread_alive"] = self._thread.is_alive() if self._thread else False

                return state

            except Exception as e:
                logger.error(f"Failed to get orchestrator status: {e}")
                return {
                    "running": False,
                    "status": "error",
                    "message": f"Failed to get status: {str(e)}"
                }

    def is_running(self) -> bool:
        """Check if orchestrator is currently running"""
        with self._lock:
            if not self._orchestrator:
                return False
            return hasattr(self._orchestrator, 'running') and self._orchestrator.running

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics from orchestrator"""
        status = self.get_status()

        if status.get("running"):
            return {
                "files_discovered": status.get("files_discovered", 0),
                "files_converted": status.get("files_converted", 0),
                "files_classified": status.get("files_classified", 0),
                "files_ner_processed": status.get("files_ner_processed", 0),
                "files_ingested": status.get("files_ingested", 0),
                "queue_size": status.get("queue_size", 0),
                "workers_active": status.get("workers_active", 0),
                "errors": status.get("errors", [])
            }
        else:
            return {
                "files_discovered": 0,
                "files_converted": 0,
                "files_classified": 0,
                "files_ner_processed": 0,
                "files_ingested": 0,
                "queue_size": 0,
                "workers_active": 0,
                "errors": []
            }

    def get_watch_directories(self) -> list:
        """Get configured watch directories from config"""
        return self.config.get("monitoring", {}).get("watch_directories", [])

    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        return {
            "watch_directories": self.get_watch_directories(),
            "batch_size": self.config.get("monitoring", {}).get("batch_size", 5),
            "parallel_workers": self.config.get("monitoring", {}).get("parallel_workers", 3),
            "neo4j_uri": self.config.get("neo4j", {}).get("uri", "bolt://localhost:7687"),
            "neo4j_batch_size": self.config.get("neo4j", {}).get("batch_size", 100),
            "spacy_model": self.config.get("ner", {}).get("spacy_model", "en_core_web_lg"),
            "classification_threshold": self.config.get("classification", {}).get("confidence_threshold", 0.75)
        }


# Global controller instance
_controller: Optional[OrchestratorController] = None


def get_controller() -> OrchestratorController:
    """Get global orchestrator controller instance"""
    global _controller
    if _controller is None:
        _controller = OrchestratorController()
    return _controller


def reset_controller():
    """Reset global controller (useful for testing)"""
    global _controller
    if _controller:
        _controller.stop()
        _controller = None
