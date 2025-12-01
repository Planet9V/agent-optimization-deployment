"""
AEON Automated Document Ingestion - Agents Package
Specialized agents for document discovery, classification, conversion, and ingestion
"""

from .base_agent import BaseAgent
from .orchestrator_agent import OrchestratorAgent
from .file_watcher_agent import FileWatcherAgent
from .format_converter_agent import FormatConverterAgent
from .classifier_agent import ClassifierAgent
from .ner_agent import NERAgent

# Note: IngestionAgent functionality is provided by nlp_ingestion_pipeline.py
# The NLPIngestionPipeline class serves as the ingestion orchestrator

__all__ = [
    'BaseAgent',
    'OrchestratorAgent',
    'FileWatcherAgent',
    'FormatConverterAgent',
    'ClassifierAgent',
    'NERAgent',
]
