#!/bin/bash
#
# Enhanced Document Processing Setup Script
# Installs all dependencies for .docx, PDF, URL, and HTML processing
#

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║         ENHANCED DOCUMENT PROCESSING - DEPENDENCY INSTALLATION                ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment detected. Activating venv..."
    source venv/bin/activate
fi

echo "📦 Installing Python packages..."
echo ""

# Core document processing packages
pip install --upgrade \
    python-docx \
    PyPDF2 \
    pdfplumber \
    beautifulsoup4 \
    lxml \
    requests \
    html5lib

echo ""
echo "✅ Python packages installed"
echo ""

# Check OS and install system packages
echo "🖥️  Checking system packages..."
echo ""

if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu system"
    echo "Installing system packages..."

    sudo apt-get update
    sudo apt-get install -y \
        poppler-utils \
        antiword \
        docx2txt \
        libreoffice-writer \
        wv

    echo "✅ System packages installed (Debian/Ubuntu)"

elif command -v brew &> /dev/null; then
    echo "Detected macOS system"
    echo "Installing system packages..."

    brew install \
        poppler \
        antiword \
        docx2txt \
        libreoffice

    echo "✅ System packages installed (macOS)"

else
    echo "⚠️  Could not detect package manager (apt-get or brew)"
    echo "   Please manually install:"
    echo "   - poppler-utils (pdftotext)"
    echo "   - antiword"
    echo "   - docx2txt"
    echo "   - libreoffice (optional)"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                     INSTALLATION COMPLETE                                     ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Testing document processor capabilities..."
echo ""

python scripts/document_processor.py

echo ""
echo "✅ Setup complete! You can now process:"
echo "   • Markdown (.md)"
echo "   • Plain text (.txt)"
echo "   • Word documents (.docx, .doc)"
echo "   • PDF files (.pdf)"
echo "   • HTML files (.html)"
echo "   • URLs (http://, https://)"
