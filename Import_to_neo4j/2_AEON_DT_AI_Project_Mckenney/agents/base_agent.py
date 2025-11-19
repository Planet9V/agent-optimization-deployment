"""
Base Agent Class
Provides common functionality for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from datetime import datetime
from pathlib import Path


def read_file_safe(file_path: str) -> str:
    """
    Read file with UTF-8 fallback to handle encoding issues

    Args:
        file_path: Path to the file to read

    Returns:
        File content as string

    Raises:
        Exception: If file cannot be read with any supported encoding
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")

    raise Exception(f"Could not decode file {file_path} with any supported encoding")


class BaseAgent(ABC):
    """Base class for all agents with common functionality"""

    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base agent

        Args:
            name: Agent name for logging and identification
            config: Configuration dictionary
        """
        self.name = name
        self.config = config
        self.logger = self._setup_logger()
        self.start_time = None
        self.end_time = None
        self._setup()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for this agent"""
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(self.name)

        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # File handler
            file_handler = logging.FileHandler(
                f'logs/{self.name}_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)

        return logger

    @abstractmethod
    def _setup(self):
        """Agent-specific setup - must be implemented by subclasses"""
        pass

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Main execution logic - must be implemented by subclasses"""
        pass

    def pre_execute(self, input_data: Any) -> Any:
        """
        Hook before execution (validation, logging)

        Args:
            input_data: Input to be processed

        Returns:
            Validated/preprocessed input
        """
        self.start_time = datetime.now()
        self.logger.info(f"Starting execution with input: {input_data}")
        return input_data

    def post_execute(self, result: Any) -> Any:
        """
        Hook after execution (cleanup, reporting)

        Args:
            result: Execution result

        Returns:
            Post-processed result
        """
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.logger.info(f"Completed execution in {duration:.2f}s with result: {result}")
        return result

    def on_error(self, error: Exception) -> Optional[Any]:
        """
        Error handling hook

        Args:
            error: Exception that occurred

        Returns:
            Recovery result or None
        """
        self.logger.error(f"Error in {self.name}: {error}", exc_info=True)
        return None

    def run(self, input_data: Any) -> Any:
        """
        Main run method with pre/post hooks and error handling

        Args:
            input_data: Input to process

        Returns:
            Execution result
        """
        try:
            validated_input = self.pre_execute(input_data)
            result = self.execute(validated_input)
            return self.post_execute(result)
        except Exception as e:
            return self.on_error(e)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get agent execution statistics

        Returns:
            Dictionary with agent stats
        """
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()

        return {
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_seconds': duration
        }
