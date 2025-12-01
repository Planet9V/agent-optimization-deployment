# Installation Guide - NER11 Gold Standard Model

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Automated Installation](#automated-installation)
3. [Manual Installation](#manual-installation)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS 11+, Windows 10+ (WSL2)
- **Python**: 3.9 or higher
- **RAM**: 16 GB
- **Disk Space**: 5 GB free
- **Internet**: Required for initial dependency download

### Recommended Requirements
- **Operating System**: Ubuntu 22.04 LTS
- **Python**: 3.10+
- **RAM**: 32 GB
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **CUDA**: 11.8 or 12.0+
- **Disk Space**: 10 GB free

### GPU Support (Optional but Recommended)
For GPU-accelerated inference:
- NVIDIA GPU with CUDA Compute Capability 7.0+
- CUDA Toolkit 11.8 or 12.0
- cuDNN 8.6+
- NVIDIA Driver 520+

---

## Automated Installation

### Quick Install (Recommended)

```bash
# Navigate to package directory
cd NER11_Gold_Model

# Run installation script
chmod +x scripts/install.sh
./scripts/install.sh
```

The script will:
1. ✅ Check Python version
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Verify model files
5. ✅ Run basic tests

**Installation time**: ~5-10 minutes (depending on internet speed)

---

## Manual Installation

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv ner11_env

# Activate environment
source ner11_env/bin/activate  # Linux/macOS
# OR
ner11_env\Scripts\activate     # Windows
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r config/requirements.txt
```

**Core Dependencies**:
- `spacy>=3.7.0`
- `spacy-transformers>=1.3.0`
- `torch>=2.0.0`
- `neo4j>=5.14.0`
- `pandas>=2.0.0`
- `numpy>=1.24.0`

### Step 3: Install spaCy Language Model

```bash
# Download English language model
python -m spacy download en_core_web_trf
```

### Step 4: Verify Installation

```bash
# Run test script
python scripts/test_model.py
```

---

## Verification

### Test 1: Model Loading

```python
import spacy

# Load model
nlp = spacy.load("./models/model-best")
print(f"✓ Model loaded successfully")
print(f"  Pipeline components: {nlp.pipe_names}")
print(f"  Entity labels: {len(nlp.get_pipe('ner').labels)} types")
```

**Expected Output**:
```
✓ Model loaded successfully
  Pipeline components: ['transformer', 'ner']
  Entity labels: 566 types
```

### Test 2: Entity Extraction

```python
text = "APT29 exploited CVE-2023-12345 in the SCADA system."
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text:20} → {ent.label_}")
```

**Expected Output**:
```
APT29                → THREAT_ACTOR
CVE-2023-12345       → VULNERABILITY
SCADA system         → OT_DEVICE
```

### Test 3: Performance Benchmark

```bash
# Run performance test
python tests/test_model_inference.py
```

**Expected Results**:
- **CPU Inference**: ~50-100 docs/second
- **GPU Inference**: ~200-500 docs/second
- **Memory Usage**: ~2-4 GB

---

## GPU Setup (Optional)

### CUDA Installation

#### Ubuntu/Linux
```bash
# Install CUDA Toolkit 12.0
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

#### Verify CUDA
```bash
nvidia-smi
nvcc --version
```

### PyTorch with CUDA

```bash
# Install PyTorch with CUDA 12.0
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu120
```

### Verify GPU Support

```python
import torch
import spacy

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

# Load model with GPU
spacy.require_gpu()
nlp = spacy.load("./models/model-best")
```

---

## Docker Installation (Alternative)

### Using Docker Compose

```bash
# Build and start container
docker-compose -f config/docker-compose.yml up -d

# Access container
docker exec -it ner11_gold bash

# Test model
python /app/scripts/test_model.py
```

### Manual Docker Build

```bash
# Build image
docker build -t ner11-gold:latest .

# Run container
docker run -it --gpus all \
  -v $(pwd):/app \
  ner11-gold:latest \
  python /app/scripts/test_model.py
```

---

## Troubleshooting

### Issue 1: "No module named 'spacy'"

**Solution**:
```bash
pip install spacy>=3.7.0
```

### Issue 2: "Can't find model 'en_core_web_trf'"

**Solution**:
```bash
python -m spacy download en_core_web_trf
```

### Issue 3: CUDA Out of Memory

**Solution**:
```python
# Reduce batch size
nlp.batch_size = 8  # Default is 128

# Or use CPU
spacy.prefer_gpu(0)  # Try GPU
if not spacy.prefer_gpu():
    print("Using CPU")
```

### Issue 4: Slow Inference on CPU

**Solution**:
```bash
# Use smaller model for CPU
# Or enable multiprocessing
nlp.pipe(texts, n_process=4)
```

### Issue 5: Permission Denied on Scripts

**Solution**:
```bash
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### Issue 6: Model Files Not Found

**Solution**:
```bash
# Verify model files exist
ls -lh models/model-best/
ls -lh models/model-last/

# Check file permissions
chmod -R 755 models/
```

---

## Environment Variables

### Optional Configuration

```bash
# Set model path
export NER11_MODEL_PATH="/path/to/NER11_Gold_Model/models/model-best"

# Set batch size
export NER11_BATCH_SIZE=32

# Enable GPU
export CUDA_VISIBLE_DEVICES=0

# Set log level
export NER11_LOG_LEVEL=INFO
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate environment
deactivate

# Remove environment
rm -rf ner11_env/
```

### Remove Package

```bash
# Remove entire package
rm -rf NER11_Gold_Model/
```

---

## Next Steps

After successful installation:

1. **Basic Usage**: See `README.md` for quick start examples
2. **Integration**: Review `docs/03_INTEGRATION_GUIDE.md`
3. **Neo4j Setup**: See `docs/04_NEO4J_INTEGRATION.md`
4. **Advanced Usage**: Explore `examples/` directory

---

## Support

For installation issues:
1. Check `tests/test_installation.py` output
2. Review system requirements
3. Consult troubleshooting section above
4. Check spaCy documentation: https://spacy.io/usage

---

**Installation Complete!** ✅

You're now ready to use the NER11 Gold Standard model.
