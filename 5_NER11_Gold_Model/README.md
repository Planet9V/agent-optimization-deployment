# NER11 Gold Standard Model

**Version**: 3.0 (Gold Standard)  
**Release Date**: November 30, 2025  
**Training Duration**: 47 hours 47 minutes  
**Final F-Score**: 0.93  

---

## Overview

The **NER11 Gold Standard** is a state-of-the-art Named Entity Recognition model specifically designed for **cybersecurity, critical infrastructure, and psychometric analysis**. It recognizes **566 distinct entity types** across multiple domains, making it one of the most comprehensive NER models available for security and behavioral analysis.

### Key Features

- ✅ **566 Entity Types**: Comprehensive coverage of cybersecurity, psychometrics, economics, and critical infrastructure
- ✅ **High Performance**: 0.93 F-Score on validation set
- ✅ **Transformer-Based**: Built on spaCy 3.x with transformer architecture
- ✅ **GPU-Optimized**: Trained on NVIDIA A100 with CUDA 11.8
- ✅ **Production-Ready**: Includes checkpoints, configs, and integration scripts
- ✅ **Fully Documented**: Complete training history, metrics, and audit trail

### Entity Categories

| Category | Entity Count | Examples |
|----------|--------------|----------|
| **Cybersecurity** | 180 | `MALWARE`, `VULNERABILITY`, `ATTACK_VECTOR`, `IOC` |
| **Psychometrics** | 95 | `PERSONALITY_TRAIT`, `COGNITIVE_BIAS`, `EMOTIONAL_STATE` |
| **Critical Infrastructure** | 120 | `OT_DEVICE`, `SCADA_SYSTEM`, `INDUSTRIAL_PROTOCOL` |
| **Economics** | 65 | `FINANCIAL_INSTRUMENT`, `MARKET_INDICATOR`, `ECONOMIC_POLICY` |
| **Organizations** | 45 | `THREAT_ACTOR`, `SECURITY_VENDOR`, `GOV_AGENCY` |
| **Technical** | 61 | `SOFTWARE`, `HARDWARE`, `PROTOCOL`, `ALGORITHM` |

### Use Cases

1. **Threat Intelligence**: Extract IOCs, TTPs, and threat actor information from security reports
2. **Incident Response**: Identify affected systems, vulnerabilities, and attack patterns
3. **Behavioral Analysis**: Detect psychological patterns in communications
4. **Knowledge Graph Construction**: Populate Neo4j with structured security intelligence
5. **Automated Triage**: Classify and prioritize security events

---

## Quick Start

### Installation

```bash
# Clone or extract this package
cd NER11_Gold_Model

# Run automated installation
./scripts/install.sh

# Or manual installation:
python3 -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
```

### Basic Usage

```python
import spacy

# Load the model
nlp = spacy.load("./models/model-best")

# Process text
text = """
The APT29 group exploited CVE-2023-12345 using a zero-day 
vulnerability in the SCADA system. The malware established 
persistence via a scheduled task.
"""

doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text:30} → {ent.label_}")
```

**Output**:
```
APT29                          → THREAT_ACTOR
CVE-2023-12345                 → VULNERABILITY
zero-day                       → ATTACK_TYPE
SCADA system                   → OT_DEVICE
malware                        → MALWARE
scheduled task                 → PERSISTENCE_MECHANISM
```

---

## Package Contents

```
NER11_Gold_Model/
├── models/
│   ├── model-best/          # Best checkpoint (F-Score: 0.94)
│   └── model-last/          # Final model (F-Score: 0.93)
├── config/
│   ├── config.cfg           # spaCy training configuration
│   ├── requirements.txt     # Python dependencies
│   └── docker-compose.yml   # Docker deployment (optional)
├── docs/
│   ├── 01_OVERVIEW.md       # This file
│   ├── 02_INSTALLATION.md   # Detailed installation guide
│   ├── 03_INTEGRATION_GUIDE.md
│   ├── 04_NEO4J_INTEGRATION.md
│   ├── 05_TRAINING_HISTORY.md
│   ├── 06_METRICS_ANALYSIS.md
│   └── 07_ENTITY_SCHEMA.md
├── training_data/
│   ├── TRAINING_DATA_MANIFEST.md
│   ├── weights_and_sources.json
│   └── training_local_window64.log
├── scripts/
│   ├── install.sh
│   ├── test_model.py
│   ├── neo4j_integration.py
│   └── batch_process.py
├── examples/
│   ├── basic_usage.py
│   ├── neo4j_example.py
│   └── batch_processing_example.py
└── tests/
    ├── test_installation.py
    └── test_model_inference.py
```

---

## Performance Metrics

### Final Training Results

- **Epochs**: 3
- **Total Steps**: 20,000
- **Final F-Score**: 0.93
- **Final Loss**: 2096.10
- **Training Time**: 47h 47m
- **GPU**: NVIDIA A100 (40GB)

### Per-Entity Performance

| Entity Type | Precision | Recall | F-Score |
|-------------|-----------|--------|---------|
| MALWARE | 0.96 | 0.94 | 0.95 |
| VULNERABILITY | 0.95 | 0.93 | 0.94 |
| THREAT_ACTOR | 0.94 | 0.92 | 0.93 |
| OT_DEVICE | 0.93 | 0.91 | 0.92 |
| PERSONALITY_TRAIT | 0.91 | 0.89 | 0.90 |

*(See `docs/06_METRICS_ANALYSIS.md` for complete breakdown)*

---

## System Requirements

### Minimum Requirements
- **Python**: 3.9+
- **RAM**: 16 GB
- **Disk Space**: 5 GB
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional but recommended)
- **CUDA**: 11.8+ (for GPU inference)

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 32 GB
- **GPU**: NVIDIA A100, V100, or RTX 4090
- **CUDA**: 12.0+

---

## Integration Options

### 1. **spaCy Pipeline** (Recommended)
```python
import spacy
nlp = spacy.load("./models/model-best")
doc = nlp(text)
```

### 2. **Neo4j Knowledge Graph**
```python
from scripts.neo4j_integration import NER11Neo4jIntegrator

integrator = NER11Neo4jIntegrator(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

integrator.process_and_ingest(text)
```

### 3. **REST API**
```bash
# Start API server
python scripts/api_server.py --port 8000

# Query endpoint
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 exploited CVE-2023-12345"}'
```

### 4. **Batch Processing**
```python
from scripts.batch_process import BatchProcessor

processor = BatchProcessor(model_path="./models/model-best")
processor.process_directory("./input_texts/", "./output_json/")
```

---

## Training Data Provenance

### Custom Data (3.0x Weight)
- **Gold Standard Texts**: 45 curated documents
- **Total Tokens**: 12.5 million
- **Entity Density**: High (avg 15 entities per 100 tokens)
- **Domains**: Cybersecurity reports, psychological assessments, OT/ICS documentation

### External Datasets (1.0x Weight)
- **9 Harmonized Datasets**: 8.2 million tokens
- **Sources**: CoNLL, OntoNotes, custom security corpora
- **Schema Mapping**: All entities mapped to NER11 566-type schema

*(See `training_data/TRAINING_DATA_MANIFEST.md` for complete details)*

---

## Citation

If you use this model in your research or production systems, please cite:

```bibtex
@software{ner11_gold_2025,
  title={NER11 Gold Standard: A Comprehensive NER Model for Cybersecurity and Behavioral Analysis},
  author={McKenney, Jim},
  year={2025},
  version={3.0},
  note={Trained on 566 entity types over 47 hours}
}
```

---

## License

This model is released under the **MIT License** for the model weights and code. Training data sources retain their original licenses.

---

## Support & Documentation

- **Full Documentation**: See `docs/` directory
- **Training History**: `docs/05_TRAINING_HISTORY.md`
- **Entity Schema**: `docs/07_ENTITY_SCHEMA.md`
- **Neo4j Integration**: `docs/04_NEO4J_INTEGRATION.md`

---

## Version History

- **v3.0 (Gold Standard)** - November 30, 2025
  - 566 entity types
  - F-Score: 0.93
  - 47h training on A100 GPU
  - Complete audit trail

---

**For questions or issues, refer to the comprehensive documentation in the `docs/` directory.**
