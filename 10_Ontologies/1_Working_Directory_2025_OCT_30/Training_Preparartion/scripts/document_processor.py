#!/usr/bin/env python3
"""
Enhanced Document Processor for NER Testing
Supports: .md, .txt, .docx, .pdf, URLs with multiple fallback methods
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict
import tempfile
import os

class DocumentProcessor:
    """Enhanced document processor with multi-format support"""

    def __init__(self):
        self.supported_formats = ['.md', '.txt', '.docx', '.doc', '.pdf', '.html']
        self._check_dependencies()

    def _check_dependencies(self) -> Dict[str, bool]:
        """Check which document processing libraries are available"""
        self.capabilities = {
            'python_docx': False,
            'pypdf2': False,
            'pdfplumber': False,
            'beautifulsoup4': False,
            'requests': False,
            'docx2txt': False,
            'antiword': False,
            'pdftotext': False
        }

        # Check Python libraries
        try:
            import docx
            self.capabilities['python_docx'] = True
        except ImportError:
            pass

        try:
            import PyPDF2
            self.capabilities['pypdf2'] = True
        except ImportError:
            pass

        try:
            import pdfplumber
            self.capabilities['pdfplumber'] = True
        except ImportError:
            pass

        try:
            from bs4 import BeautifulSoup
            self.capabilities['beautifulsoup4'] = True
        except ImportError:
            pass

        try:
            import requests
            self.capabilities['requests'] = True
        except ImportError:
            pass

        # Check command-line tools
        for tool in ['docx2txt', 'antiword', 'pdftotext']:
            try:
                result = subprocess.run([tool, '--version'],
                                      capture_output=True,
                                      timeout=2)
                self.capabilities[tool] = True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return self.capabilities

    def read_document(self, source: str) -> Optional[str]:
        """
        Read document from file path or URL

        Args:
            source: File path or URL to document

        Returns:
            Extracted text or None if failed
        """
        # Check if URL
        if source.startswith('http://') or source.startswith('https://'):
            return self.read_url(source)

        # File path
        path = Path(source)
        if not path.exists():
            print(f"⚠️  File not found: {source}")
            return None

        # Route to appropriate handler
        ext = path.suffix.lower()

        if ext in ['.md', '.txt']:
            return self.read_text_file(path)
        elif ext in ['.docx', '.doc']:
            return self.read_docx(path)
        elif ext == '.pdf':
            return self.read_pdf(path)
        elif ext in ['.html', '.htm']:
            return self.read_html(path)
        else:
            print(f"⚠️  Unsupported format: {ext}")
            return None

    def read_text_file(self, path: Path) -> Optional[str]:
        """Read plain text or markdown file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️  Error reading {path.name}: {e}")
            return None

    def read_docx(self, path: Path) -> Optional[str]:
        """
        Read .docx file with multiple fallback methods
        Priority: python-docx > docx2txt > antiword
        """
        # Method 1: python-docx (best quality)
        if self.capabilities['python_docx']:
            try:
                from docx import Document
                doc = Document(path)
                text = '\n'.join([para.text for para in doc.paragraphs])
                if text and len(text) > 50:
                    return text
            except Exception as e:
                print(f"  ⚠️  python-docx failed: {e}")

        # Method 2: docx2txt command-line tool
        if self.capabilities['docx2txt']:
            try:
                result = subprocess.run(['docx2txt', str(path)],
                                      capture_output=True,
                                      text=True,
                                      timeout=30)
                if result.returncode == 0 and result.stdout:
                    return result.stdout
            except Exception as e:
                print(f"  ⚠️  docx2txt failed: {e}")

        # Method 3: Convert to text via libreoffice (if available)
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = subprocess.run([
                    'libreoffice', '--headless', '--convert-to', 'txt:Text',
                    '--outdir', tmpdir, str(path)
                ], capture_output=True, timeout=30)

                if result.returncode == 0:
                    txt_file = Path(tmpdir) / f"{path.stem}.txt"
                    if txt_file.exists():
                        with open(txt_file, 'r', encoding='utf-8') as f:
                            return f.read()
        except Exception as e:
            print(f"  ⚠️  libreoffice conversion failed: {e}")

        # Method 4: antiword (for older .doc files)
        if self.capabilities['antiword'] and path.suffix.lower() == '.doc':
            try:
                result = subprocess.run(['antiword', str(path)],
                                      capture_output=True,
                                      text=True,
                                      timeout=30)
                if result.returncode == 0 and result.stdout:
                    return result.stdout
            except Exception as e:
                print(f"  ⚠️  antiword failed: {e}")

        print(f"⚠️  All DOCX extraction methods failed for {path.name}")
        return None

    def read_pdf(self, path: Path) -> Optional[str]:
        """
        Read PDF file with multiple fallback methods
        Priority: pdfplumber > PyPDF2 > pdftotext
        """
        # Method 1: pdfplumber (best quality, handles complex layouts)
        if self.capabilities['pdfplumber']:
            try:
                import pdfplumber
                text = []
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text.append(page_text)
                result = '\n'.join(text)
                if result and len(result) > 50:
                    return result
            except Exception as e:
                print(f"  ⚠️  pdfplumber failed: {e}")

        # Method 2: PyPDF2 (good fallback)
        if self.capabilities['pypdf2']:
            try:
                import PyPDF2
                text = []
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text.append(page_text)
                result = '\n'.join(text)
                if result and len(result) > 50:
                    return result
            except Exception as e:
                print(f"  ⚠️  PyPDF2 failed: {e}")

        # Method 3: pdftotext command-line tool (Poppler utils)
        if self.capabilities['pdftotext']:
            try:
                result = subprocess.run(['pdftotext', '-layout', str(path), '-'],
                                      capture_output=True,
                                      text=True,
                                      timeout=60)
                if result.returncode == 0 and result.stdout:
                    return result.stdout
            except Exception as e:
                print(f"  ⚠️  pdftotext failed: {e}")

        print(f"⚠️  All PDF extraction methods failed for {path.name}")
        return None

    def read_html(self, path: Path) -> Optional[str]:
        """Read HTML file and extract text"""
        if not self.capabilities['beautifulsoup4']:
            print(f"⚠️  BeautifulSoup not available for HTML parsing")
            return None

        try:
            from bs4 import BeautifulSoup
            with open(path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text
        except Exception as e:
            print(f"⚠️  Error reading HTML {path.name}: {e}")
            return None

    def read_url(self, url: str) -> Optional[str]:
        """Fetch and extract text from URL"""
        if not self.capabilities['requests']:
            print(f"⚠️  requests library not available for URL fetching")
            return None

        try:
            import requests
            from bs4 import BeautifulSoup

            # Fetch with timeout
            response = requests.get(url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"⚠️  Error fetching URL {url}: {e}")
            return None

    def get_capability_report(self) -> str:
        """Generate report of available capabilities"""
        report = ["\n📋 Document Processing Capabilities:"]
        report.append("\n✅ Available:")
        for tool, available in self.capabilities.items():
            if available:
                report.append(f"  • {tool}")

        report.append("\n❌ Missing:")
        missing = [tool for tool, available in self.capabilities.items() if not available]
        if missing:
            for tool in missing:
                report.append(f"  • {tool}")
        else:
            report.append("  None - all capabilities available!")

        return '\n'.join(report)

    def install_dependencies(self) -> str:
        """Generate installation instructions for missing dependencies"""
        missing_python = []
        missing_system = []

        if not self.capabilities['python_docx']:
            missing_python.append('python-docx')
        if not self.capabilities['pypdf2']:
            missing_python.append('PyPDF2')
        if not self.capabilities['pdfplumber']:
            missing_python.append('pdfplumber')
        if not self.capabilities['beautifulsoup4']:
            missing_python.append('beautifulsoup4 lxml')
        if not self.capabilities['requests']:
            missing_python.append('requests')

        if not self.capabilities['pdftotext']:
            missing_system.append('poppler-utils')
        if not self.capabilities['antiword']:
            missing_system.append('antiword')
        if not self.capabilities['docx2txt']:
            missing_system.append('docx2txt')

        instructions = ["\n📦 Installation Instructions:"]

        if missing_python:
            instructions.append(f"\n🐍 Python packages:")
            instructions.append(f"   pip install {' '.join(missing_python)}")

        if missing_system:
            instructions.append(f"\n🖥️  System packages (Ubuntu/Debian):")
            instructions.append(f"   sudo apt-get install {' '.join(missing_system)}")
            instructions.append(f"\n🖥️  System packages (macOS):")
            instructions.append(f"   brew install {' '.join(missing_system)}")

        if not missing_python and not missing_system:
            instructions.append("\n✅ All dependencies installed!")

        return '\n'.join(instructions)


def main():
    """Test document processor capabilities"""
    print("="*80)
    print("DOCUMENT PROCESSOR - CAPABILITY CHECK")
    print("="*80)

    processor = DocumentProcessor()

    # Print capability report
    print(processor.get_capability_report())

    # Print installation instructions
    print(processor.install_dependencies())

    print("\n" + "="*80)
    print("TESTING DOCUMENT EXTRACTION")
    print("="*80)

    # Test files if provided as arguments
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            print(f"\n📄 Testing: {file_path}")
            text = processor.read_document(file_path)
            if text:
                print(f"✅ Extracted {len(text):,} characters")
                print(f"   Preview: {text[:200]}...")
            else:
                print(f"❌ Failed to extract text")

if __name__ == "__main__":
    main()
