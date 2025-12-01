#!/usr/bin/env python3
"""
PDF Document Processor for Cybersecurity Threat Intelligence
Extracts text, tables, and metadata from PDF documents
"""

import pdfplumber
import logging
from pathlib import Path
from typing import Dict, List, Optional
import json
import argparse
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFProcessor:
    """Process PDF documents and extract structured content"""

    def __init__(self, ocr_fallback: bool = False):
        """
        Initialize PDF processor

        Args:
            ocr_fallback: Use OCR for scanned PDFs (requires pytesseract)
        """
        self.ocr_fallback = ocr_fallback

        if ocr_fallback:
            try:
                import pytesseract
                from PIL import Image
                self.pytesseract = pytesseract
                logger.info("OCR fallback enabled")
            except ImportError:
                logger.warning("pytesseract not installed. OCR fallback disabled.")
                self.ocr_fallback = False

    def extract_metadata(self, pdf_path: Path) -> Dict:
        """
        Extract metadata from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary of metadata
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata = pdf.metadata or {}

                return {
                    'filename': pdf_path.name,
                    'title': metadata.get('Title', ''),
                    'author': metadata.get('Author', ''),
                    'creator': metadata.get('Creator', ''),
                    'producer': metadata.get('Producer', ''),
                    'subject': metadata.get('Subject', ''),
                    'creation_date': metadata.get('CreationDate', ''),
                    'modification_date': metadata.get('ModDate', ''),
                    'num_pages': len(pdf.pages),
                    'extracted_at': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {
                'filename': pdf_path.name,
                'error': str(e)
            }

    def extract_text(self, pdf_path: Path, page_chunks: bool = True) -> Dict:
        """
        Extract text from PDF with page-level chunking

        Args:
            pdf_path: Path to PDF file
            page_chunks: Return text as page chunks for context preservation

        Returns:
            Dictionary containing text and page information
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if page_chunks:
                    pages = []
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()

                        if not text and self.ocr_fallback:
                            text = self._ocr_page(page)

                        pages.append({
                            'page_number': i + 1,
                            'text': text or '',
                            'width': page.width,
                            'height': page.height
                        })

                    return {
                        'type': 'page_chunks',
                        'num_pages': len(pages),
                        'pages': pages
                    }
                else:
                    # Extract all text as single string
                    full_text = []
                    for page in pdf.pages:
                        text = page.extract_text()

                        if not text and self.ocr_fallback:
                            text = self._ocr_page(page)

                        if text:
                            full_text.append(text)

                    return {
                        'type': 'full_text',
                        'num_pages': len(pdf.pages),
                        'text': '\n\n'.join(full_text)
                    }

        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return {'error': str(e)}

    def extract_tables(self, pdf_path: Path) -> List[Dict]:
        """
        Extract tables from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of table dictionaries with page numbers
        """
        tables = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()

                    for j, table in enumerate(page_tables):
                        if table:
                            # Structure table data
                            headers = table[0] if table else []
                            rows = table[1:] if len(table) > 1 else []

                            tables.append({
                                'page_number': i + 1,
                                'table_number': j + 1,
                                'headers': headers,
                                'rows': rows,
                                'num_rows': len(rows),
                                'num_columns': len(headers)
                            })

        except Exception as e:
            logger.error(f"Error extracting tables from {pdf_path}: {e}")

        return tables

    def detect_figures(self, pdf_path: Path) -> List[Dict]:
        """
        Detect figures and diagrams in PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of figure locations and metadata
        """
        figures = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Extract images
                    images = page.images

                    for j, img in enumerate(images):
                        figures.append({
                            'page_number': i + 1,
                            'figure_number': j + 1,
                            'x0': img.get('x0'),
                            'y0': img.get('y0'),
                            'x1': img.get('x1'),
                            'y1': img.get('y1'),
                            'width': img.get('width'),
                            'height': img.get('height')
                        })

        except Exception as e:
            logger.error(f"Error detecting figures in {pdf_path}: {e}")

        return figures

    def process_pdf(self, pdf_path: Path, extract_tables: bool = True,
                    detect_figures: bool = True) -> Dict:
        """
        Comprehensive PDF processing

        Args:
            pdf_path: Path to PDF file
            extract_tables: Extract tables from PDF
            detect_figures: Detect figures and diagrams

        Returns:
            Dictionary containing all extracted information
        """
        logger.info(f"Processing PDF: {pdf_path}")

        result = {
            'source_file': str(pdf_path),
            'metadata': self.extract_metadata(pdf_path),
            'text': self.extract_text(pdf_path, page_chunks=True)
        }

        if extract_tables:
            result['tables'] = self.extract_tables(pdf_path)
            logger.info(f"Extracted {len(result['tables'])} tables")

        if detect_figures:
            result['figures'] = self.detect_figures(pdf_path)
            logger.info(f"Detected {len(result['figures'])} figures")

        return result

    def _ocr_page(self, page) -> Optional[str]:
        """
        Perform OCR on a page using pytesseract

        Args:
            page: pdfplumber page object

        Returns:
            OCR text or None
        """
        if not self.ocr_fallback:
            return None

        try:
            # Convert page to image
            img = page.to_image(resolution=300)
            pil_img = img.original

            # Perform OCR
            text = self.pytesseract.image_to_string(pil_img)
            return text

        except Exception as e:
            logger.error(f"OCR error: {e}")
            return None

    def batch_process(self, pdf_directory: Path, output_dir: Path) -> List[Dict]:
        """
        Process multiple PDFs in batch

        Args:
            pdf_directory: Directory containing PDF files
            output_dir: Output directory for results

        Returns:
            List of processing results
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_files = list(pdf_directory.glob('*.pdf'))
        results = []

        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")

            try:
                result = self.process_pdf(pdf_file)

                # Save individual result
                output_file = output_dir / f"{pdf_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                results.append({
                    'file': pdf_file.name,
                    'status': 'success',
                    'output': str(output_file)
                })

            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {e}")
                results.append({
                    'file': pdf_file.name,
                    'status': 'error',
                    'error': str(e)
                })

        return results


def main():
    """CLI interface for PDF processing"""
    parser = argparse.ArgumentParser(description='Process PDF documents for threat intelligence')
    parser.add_argument('input', help='Input PDF file or directory')
    parser.add_argument('-o', '--output', help='Output directory', default='tmp')
    parser.add_argument('--no-tables', action='store_true', help='Skip table extraction')
    parser.add_argument('--no-figures', action='store_true', help='Skip figure detection')
    parser.add_argument('--ocr', action='store_true', help='Enable OCR for scanned PDFs')
    parser.add_argument('--single-text', action='store_true', help='Extract as single text (not page chunks)')

    args = parser.parse_args()

    # Initialize processor
    processor = PDFProcessor(ocr_fallback=args.ocr)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        # Process single PDF
        result = processor.process_pdf(
            input_path,
            extract_tables=not args.no_tables,
            detect_figures=not args.no_figures
        )

        # Save result
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / f"{input_path.stem}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {output_file}")
        logger.info(f"Pages: {result['metadata']['num_pages']}")
        logger.info(f"Tables: {len(result.get('tables', []))}")
        logger.info(f"Figures: {len(result.get('figures', []))}")

    elif input_path.is_dir():
        # Batch process directory
        results = processor.batch_process(input_path, output_path)

        # Save summary
        summary_file = output_path / 'processing_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        success_count = sum(1 for r in results if r['status'] == 'success')
        logger.info(f"Processed {success_count}/{len(results)} PDFs successfully")
        logger.info(f"Summary saved to {summary_file}")

    else:
        logger.error(f"Invalid input path: {input_path}")


if __name__ == '__main__':
    main()
