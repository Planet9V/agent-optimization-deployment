"""
PDF to Markdown Converter
Supports PyMuPDF (primary), pdfplumber (fallback), and Camelot (tables)
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class PDFConverter:
    """Convert PDF documents to Markdown format"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize PDF converter

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.strategy = config.get('pdf_strategy', 'pymupdf_primary')
        self.fallback_order = config.get('fallback_order', {}).get('pdf', ['PyMuPDF', 'pdfplumber'])
        self.extract_tables = config.get('table_extraction', True)
        self.max_file_size_mb = config.get('max_file_size_mb', 100)

    def convert(self, pdf_path: str) -> Optional[str]:
        """
        Convert PDF to Markdown

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown text or None if conversion failed
        """
        try:
            # Check file size
            file_size_mb = Path(pdf_path).stat().st_size / (1024 * 1024)
            if file_size_mb > self.max_file_size_mb:
                logger.warning(f"PDF file too large ({file_size_mb:.2f} MB): {pdf_path}")
                return None

            # Try converters in fallback order
            for converter_name in self.fallback_order:
                try:
                    if converter_name == 'PyMuPDF':
                        result = self._convert_with_pymupdf(pdf_path)
                    elif converter_name == 'pdfplumber':
                        result = self._convert_with_pdfplumber(pdf_path)
                    elif converter_name == 'Camelot':
                        result = self._convert_with_camelot(pdf_path)
                    else:
                        logger.warning(f"Unknown converter: {converter_name}")
                        continue

                    if result:
                        logger.info(f"Successfully converted {pdf_path} using {converter_name}")
                        return result

                except ImportError as e:
                    logger.warning(f"{converter_name} not available: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"{converter_name} conversion failed: {e}")
                    continue

            logger.error(f"All converters failed for: {pdf_path}")
            return None

        except Exception as e:
            logger.error(f"Error converting PDF {pdf_path}: {e}")
            return None

    def _convert_with_pymupdf(self, pdf_path: str) -> Optional[str]:
        """
        Convert PDF using PyMuPDF (fitz)
        Fastest and most accurate for most PDFs

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown text or None
        """
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(pdf_path)
            markdown_parts = []

            for page_num, page in enumerate(doc, 1):
                # Extract text
                text = page.get_text()

                if text.strip():
                    # Add page marker
                    markdown_parts.append(f"## Page {page_num}\n\n")
                    markdown_parts.append(text)
                    markdown_parts.append("\n\n")

            doc.close()

            # Extract tables if enabled
            if self.extract_tables:
                try:
                    table_md = self._extract_tables_camelot(pdf_path)
                    if table_md:
                        markdown_parts.append("\n\n## Tables\n\n")
                        markdown_parts.append(table_md)
                except Exception as e:
                    logger.debug(f"Table extraction failed: {e}")

            return ''.join(markdown_parts)

        except ImportError:
            raise  # Re-raise to try fallback
        except Exception as e:
            logger.warning(f"PyMuPDF conversion failed: {e}")
            return None

    def _convert_with_pdfplumber(self, pdf_path: str) -> Optional[str]:
        """
        Convert PDF using pdfplumber
        Better for layout-aware extraction

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown text or None
        """
        try:
            import pdfplumber

            markdown_parts = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()

                    if text:
                        markdown_parts.append(f"## Page {page_num}\n\n")
                        markdown_parts.append(text)
                        markdown_parts.append("\n\n")

                    # Extract tables
                    if self.extract_tables:
                        tables = page.extract_tables()
                        if tables:
                            markdown_parts.append(f"### Tables on Page {page_num}\n\n")
                            for i, table in enumerate(tables, 1):
                                markdown_parts.append(self._table_to_markdown(table))
                                markdown_parts.append("\n\n")

            return ''.join(markdown_parts)

        except ImportError:
            raise  # Re-raise to try fallback
        except Exception as e:
            logger.warning(f"pdfplumber conversion failed: {e}")
            return None

    def _extract_tables_camelot(self, pdf_path: str) -> Optional[str]:
        """
        Extract tables using Camelot (95%+ table accuracy)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown representation of tables or None
        """
        try:
            import camelot

            tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')

            if len(tables) == 0:
                return None

            markdown_parts = []
            for i, table in enumerate(tables, 1):
                markdown_parts.append(f"### Table {i} (Page {table.page})\n\n")
                # Convert DataFrame to markdown
                markdown_parts.append(table.df.to_markdown(index=False))
                markdown_parts.append("\n\n")

            return ''.join(markdown_parts)

        except ImportError:
            logger.debug("Camelot not available for table extraction")
            return None
        except Exception as e:
            logger.debug(f"Camelot table extraction failed: {e}")
            return None

    def _convert_with_camelot(self, pdf_path: str) -> Optional[str]:
        """
        Extract only tables using Camelot

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown text or None
        """
        # Camelot is table-only, so fall back to PyMuPDF for text
        return None

    def _table_to_markdown(self, table: list) -> str:
        """
        Convert table list to markdown format

        Args:
            table: List of lists representing table

        Returns:
            Markdown table
        """
        if not table or len(table) < 2:
            return ""

        # Header row
        header = table[0]
        markdown_parts = ['| ' + ' | '.join(str(cell) for cell in header) + ' |\n']

        # Separator
        markdown_parts.append('| ' + ' | '.join(['---'] * len(header)) + ' |\n')

        # Data rows
        for row in table[1:]:
            markdown_parts.append('| ' + ' | '.join(str(cell) for cell in row) + ' |\n')

        return ''.join(markdown_parts)

    def get_stats(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get PDF file statistics

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with PDF stats
        """
        try:
            path = Path(pdf_path)
            stats = {
                'file_name': path.name,
                'file_size_bytes': path.stat().st_size,
                'file_size_mb': path.stat().st_size / (1024 * 1024),
                'extension': path.suffix
            }

            # Try to get page count
            try:
                import fitz
                doc = fitz.open(pdf_path)
                stats['page_count'] = len(doc)
                doc.close()
            except:
                stats['page_count'] = None

            return stats

        except Exception as e:
            logger.error(f"Error getting PDF stats: {e}")
            return {}
