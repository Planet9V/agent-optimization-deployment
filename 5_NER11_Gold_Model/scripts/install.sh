#!/bin/bash
# NER11 Gold Standard - Installation Script

set -e  # Exit on error

echo "=================================="
echo "NER11 Gold Standard Installation"
echo "=================================="
echo ""

# Check Python version
echo "[1/6] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "✗ Python 3.9+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -d "ner11_env" ]; then
    echo "  Virtual environment already exists"
else
    python3 -m venv ner11_env
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source ner11_env/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "[4/6] Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "[5/6] Installing dependencies..."
echo "  This may take 5-10 minutes..."
pip install -r config/requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Download spaCy language model
echo "[6/6] Downloading spaCy language model..."
python -m spacy download en_core_web_trf --quiet
echo "✓ Language model downloaded"
echo ""

# Verify installation
echo "=================================="
echo "Verifying Installation"
echo "=================================="
echo ""

python3 << EOF
import spacy
import torch
from neo4j import GraphDatabase

print("✓ spaCy:", spacy.__version__)
print("✓ PyTorch:", torch.__version__)
print("✓ CUDA available:", torch.cuda.is_available())

# Try loading model
try:
    nlp = spacy.load("./models/model-best")
    print(f"✓ NER11 model loaded ({len(nlp.get_pipe('ner').labels)} entity types)")
except Exception as e:
    print(f"✗ Model loading failed: {e}")
    exit(1)

print("")
print("=" * 50)
print("Installation Complete!")
print("=" * 50)
print("")
print("Next steps:")
print("  1. Activate environment: source ner11_env/bin/activate")
print("  2. Test model: python scripts/test_model.py")
print("  3. See README.md for usage examples")
print("")
EOF

echo "Installation successful! ✅"
