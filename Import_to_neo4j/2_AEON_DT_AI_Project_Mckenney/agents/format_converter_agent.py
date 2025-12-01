"""
Format Converter Agent
Routes documents to appropriate converter based on file extension
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib

from .base_agent import BaseAgent
from converters import PDFConverter, DOCXConverter, HTMLConverter

logger = logging.getLogger(__name__)


class FormatConverterAgent(BaseAgent):
    """Agent responsible for converting various document formats to Markdown"""

    def _setup(self):
        """Initialize converters"""
        self.pdf_converter = PDFConverter(self.config)
        self.docx_converter = DOCXConverter(self.config)
        self.html_converter = HTMLConverter(self.config)

        self.output_dir = Path(self.config.get('conversion', {}).get('output_dir', '/tmp/aeon_processed_docs'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Supported file extensions
        self.supported_extensions = {
            '.pdf': self.pdf_converter,
            '.docx': self.docx_converter,
            '.doc': self.docx_converter,
            '.html': self.html_converter,
            '.htm': self.html_converter,
            '.md': None,  # Passthrough
            '.txt': None   # Passthrough
        }

        # Conversion statistics
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'by_format': {}
        }

        logger.info(f"FormatConverterAgent initialized with output dir: {self.output_dir}")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert document to Markdown

        Args:
            input_data: Dictionary with 'file_path' and optional 'metadata'

        Returns:
            Dictionary with conversion results
        """
        file_path = input_data.get('file_path')
        metadata = input_data.get('metadata', {})

        if not file_path:
            raise ValueError("file_path required in input_data")

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = file_path.suffix.lower()

        # Check if extension is supported
        if extension not in self.supported_extensions:
            logger.warning(f"Unsupported file extension: {extension}")
            self.stats['skipped'] += 1
            return {
                'status': 'skipped',
                'reason': f'Unsupported extension: {extension}',
                'file_path': str(file_path)
            }

        self.stats['total_files'] += 1
        self.stats['by_format'][extension] = self.stats['by_format'].get(extension, 0) + 1

        try:
            # Convert to markdown
            markdown_content = self._convert_file(file_path, extension)

            if markdown_content is None:
                logger.error(f"Conversion failed for: {file_path}")
                self.stats['failed'] += 1
                return {
                    'status': 'failed',
                    'reason': 'All converters failed',
                    'file_path': str(file_path)
                }

            # Save markdown file
            output_path = self._save_markdown(file_path, markdown_content, metadata)

            self.stats['successful'] += 1

            logger.info(f"Successfully converted: {file_path} → {output_path}")

            return {
                'status': 'success',
                'input_file': str(file_path),
                'output_file': str(output_path),
                'format': extension,
                'content_length': len(markdown_content),
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error converting {file_path}: {e}")
            self.stats['failed'] += 1
            return {
                'status': 'error',
                'reason': str(e),
                'file_path': str(file_path)
            }

    def _convert_file(self, file_path: Path, extension: str) -> Optional[str]:
        """
        Convert file using appropriate converter

        Args:
            file_path: Path to file
            extension: File extension

        Returns:
            Markdown content or None if conversion failed
        """
        converter = self.supported_extensions[extension]

        # Passthrough for markdown and text files
        if converter is None:
            try:
                from agents.base_agent import read_file_safe
                return read_file_safe(str(file_path))
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
                return None

        # Use appropriate converter
        try:
            return converter.convert(str(file_path))
        except Exception as e:
            logger.error(f"Converter error for {file_path}: {e}")
            return None

    def _save_markdown(self, source_file: Path, markdown_content: str, metadata: Dict[str, Any]) -> Path:
        """
        Save converted markdown to output directory

        Args:
            source_file: Original source file path
            markdown_content: Markdown content to save
            metadata: Document metadata

        Returns:
            Path to saved markdown file
        """
        # Generate output filename
        file_hash = hashlib.md5(str(source_file).encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create subdirectory structure if metadata contains sector/subsector
        output_subdir = self.output_dir

        if 'sector' in metadata:
            output_subdir = output_subdir / metadata['sector']
            if 'subsector' in metadata:
                output_subdir = output_subdir / metadata['subsector']

        output_subdir.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        base_name = source_file.stem
        output_filename = f"{base_name}_{file_hash}_{timestamp}.md"
        output_path = output_subdir / output_filename

        # Save markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write metadata header
            f.write("---\n")
            f.write(f"source_file: {source_file}\n")
            f.write(f"converted_at: {datetime.now().isoformat()}\n")
            f.write(f"original_format: {source_file.suffix}\n")

            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

            f.write("---\n\n")

            # Write markdown content
            f.write(markdown_content)

        logger.info(f"Saved markdown: {output_path}")
        return output_path

    def convert_batch(self, file_paths: List[str], metadata_list: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Convert multiple files in batch

        Args:
            file_paths: List of file paths to convert
            metadata_list: Optional list of metadata dictionaries (one per file)

        Returns:
            List of conversion results
        """
        if metadata_list is None:
            metadata_list = [{} for _ in file_paths]

        if len(file_paths) != len(metadata_list):
            raise ValueError("file_paths and metadata_list must have same length")

        results = []

        for file_path, metadata in zip(file_paths, metadata_list):
            result = self.run({'file_path': file_path, 'metadata': metadata})
            results.append(result)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get conversion statistics"""
        return {
            **self.stats,
            'success_rate': (self.stats['successful'] / self.stats['total_files'] * 100)
                           if self.stats['total_files'] > 0 else 0
        }

    def reset_stats(self):
        """Reset conversion statistics"""
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'by_format': {}
        }
