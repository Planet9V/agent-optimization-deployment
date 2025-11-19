"""
HTML to Markdown Converter
Supports BeautifulSoup (primary), markdownify (fallback), and pandoc
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class HTMLConverter:
    """Convert HTML documents to Markdown format"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize HTML converter

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.strategy = config.get('html_strategy', 'beautifulsoup')
        self.fallback_order = config.get('fallback_order', {}).get('html', ['BeautifulSoup', 'markdownify', 'pandoc'])
        self.preserve_formatting = config.get('preserve_formatting', True)

    def convert(self, html_path: str) -> Optional[str]:
        """
        Convert HTML to Markdown

        Args:
            html_path: Path to HTML file

        Returns:
            Markdown text or None if conversion failed
        """
        try:
            # Try converters in fallback order
            for converter_name in self.fallback_order:
                try:
                    if converter_name == 'BeautifulSoup':
                        result = self._convert_with_beautifulsoup(html_path)
                    elif converter_name == 'markdownify':
                        result = self._convert_with_markdownify(html_path)
                    elif converter_name == 'pandoc':
                        result = self._convert_with_pandoc(html_path)
                    else:
                        logger.warning(f"Unknown converter: {converter_name}")
                        continue

                    if result:
                        logger.info(f"Successfully converted {html_path} using {converter_name}")
                        return result

                except ImportError as e:
                    logger.warning(f"{converter_name} not available: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"{converter_name} conversion failed: {e}")
                    continue

            logger.error(f"All converters failed for: {html_path}")
            return None

        except Exception as e:
            logger.error(f"Error converting HTML {html_path}: {e}")
            return None

    def _convert_with_beautifulsoup(self, html_path: str) -> Optional[str]:
        """
        Convert HTML using BeautifulSoup + html2text
        Best for clean HTML with good structure (95%+ extraction)

        Args:
            html_path: Path to HTML file

        Returns:
            Markdown text or None
        """
        try:
            from bs4 import BeautifulSoup
            import html2text

            # Read HTML file
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
                element.decompose()

            # Get cleaned HTML
            cleaned_html = str(soup)

            # Convert to Markdown using html2text
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.ignore_emphasis = False
            h.body_width = 0  # Don't wrap lines
            h.unicode_snob = True
            h.skip_internal_links = True

            markdown = h.handle(cleaned_html)

            return markdown

        except ImportError:
            raise  # Re-raise to try fallback
        except Exception as e:
            logger.warning(f"BeautifulSoup conversion failed: {e}")
            return None

    def _convert_with_markdownify(self, html_path: str) -> Optional[str]:
        """
        Convert HTML using markdownify library
        Good Markdown fidelity (90-95%)

        Args:
            html_path: Path to HTML file

        Returns:
            Markdown text or None
        """
        try:
            from markdownify import markdownify as md

            # Read HTML file
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            # Convert to Markdown
            markdown = md(
                html_content,
                heading_style="ATX",  # Use # for headings
                bullets="-",  # Use - for bullet lists
                code_language="",  # Don't add language to code blocks
                strip=['script', 'style', 'nav', 'footer']
            )

            return markdown

        except ImportError:
            raise  # Re-raise to try fallback
        except Exception as e:
            logger.warning(f"markdownify conversion failed: {e}")
            return None

    def _convert_with_pandoc(self, html_path: str) -> Optional[str]:
        """
        Convert HTML using pandoc command-line tool
        Fallback option if libraries not available

        Args:
            html_path: Path to HTML file

        Returns:
            Markdown text or None
        """
        try:
            import subprocess

            # Try pandoc command
            result = subprocess.run(
                ['pandoc', '-f', 'html', '-t', 'markdown', html_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return result.stdout
            else:
                logger.warning(f"pandoc conversion failed: {result.stderr}")
                return None

        except FileNotFoundError:
            logger.debug("pandoc not found in system PATH")
            return None
        except subprocess.TimeoutExpired:
            logger.warning("pandoc conversion timeout")
            return None
        except Exception as e:
            logger.warning(f"pandoc conversion failed: {e}")
            return None

    def extract_metadata(self, html_path: str) -> Dict[str, Any]:
        """
        Extract metadata from HTML file

        Args:
            html_path: Path to HTML file

        Returns:
            Dictionary with HTML metadata
        """
        try:
            from bs4 import BeautifulSoup

            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            metadata = {
                'file_name': Path(html_path).name,
                'file_size_bytes': Path(html_path).stat().st_size,
                'title': None,
                'description': None,
                'keywords': None,
                'author': None
            }

            # Extract title
            if soup.title:
                metadata['title'] = soup.title.string

            # Extract meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                property_name = meta.get('property', '').lower()
                content = meta.get('content', '')

                if name == 'description' or property_name == 'og:description':
                    metadata['description'] = content
                elif name == 'keywords':
                    metadata['keywords'] = content
                elif name == 'author':
                    metadata['author'] = content

            return metadata

        except Exception as e:
            logger.error(f"Error extracting HTML metadata: {e}")
            return {}

    def get_stats(self, html_path: str) -> Dict[str, Any]:
        """
        Get HTML file statistics

        Args:
            html_path: Path to HTML file

        Returns:
            Dictionary with HTML stats
        """
        try:
            from bs4 import BeautifulSoup

            path = Path(html_path)
            stats = {
                'file_name': path.name,
                'file_size_bytes': path.stat().st_size,
                'extension': path.suffix
            }

            # Try to get element counts
            try:
                with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()

                soup = BeautifulSoup(html_content, 'html.parser')

                stats['headings'] = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
                stats['paragraphs'] = len(soup.find_all('p'))
                stats['links'] = len(soup.find_all('a'))
                stats['images'] = len(soup.find_all('img'))
                stats['tables'] = len(soup.find_all('table'))
                stats['lists'] = len(soup.find_all(['ul', 'ol']))

            except:
                stats['elements_count'] = None

            return stats

        except Exception as e:
            logger.error(f"Error getting HTML stats: {e}")
            return {}
