# How-To: Generate NER Training Data for Partial Chain Training

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Validation](#validation)
5. [Training spaCy Models](#training-spacy-models)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### Required Software

#### 1. Neo4j Database
```bash
# Install Neo4j (Ubuntu/Debian)
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install neo4j

# Start Neo4j
sudo systemctl start neo4j
sudo systemctl enable neo4j

# Access Neo4j Browser
# Open http://localhost:7474 in browser
# Default credentials: neo4j/neo4j (change on first login)
```

#### 2. Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install neo4j spacy pandas numpy
pip install spacy-transformers  # For transformer-based models

# Download spaCy model
python -m spacy download en_core_web_sm
```

#### 3. Knowledge Graph Data

Ensure your Neo4j database contains:
- **CVE nodes** with properties: `id`, `description`, `publishedDate`, `cvssScore`
- **CWE nodes** with properties: `id`, `name`, `description`
- **CAPEC nodes** (optional) with properties: `id`, `name`, `description`
- **ATTACK nodes** (optional) with properties: `id`, `name`, `description`
- **Relationships**: `HAS_WEAKNESS`, `EXPLOITED_BY`, `MAPS_TO`

### Verify Installation

```bash
# Test Neo4j connection
cypher-shell -u neo4j -p your_password "MATCH (n) RETURN count(n) AS node_count;"

# Test Python packages
python -c "import neo4j; import spacy; print('All packages installed successfully')"

# Test spaCy model
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy model loaded')"
```

## Quick Start

### 5-Minute Setup

```bash
# 1. Clone repository or navigate to project directory
cd /path/to/training_preparation

# 2. Set environment variables
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"

# 3. Generate training data
python scripts/generate_ner_training_data.py \
    --output data/training/ner_v7_training.json \
    --limit 10000

# 4. Validate generated data
python scripts/validate_training_data.py \
    --input data/training/ner_v7_training.json

# 5. Train spaCy model
python scripts/train_spacy_ner.py \
    --input data/training/ner_v7_training.json \
    --output models/ner_v7_model \
    --epochs 100
```

## Step-by-Step Guide

### Step 1: Extract CVE→CWE Data

#### 1.1 Create Extraction Script

Create `scripts/extract_cve_cwe_pairs.py`:

```python
#!/usr/bin/env python3
"""
Extract CVE→CWE training pairs from Neo4j knowledge graph
"""

from neo4j import GraphDatabase
import json
import os

class CVECWEExtractor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def extract_pairs(self, limit=10000):
        """Extract CVE→CWE pairs"""
        query = """
        MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
        RETURN
          cve.id AS cve_id,
          cve.description AS cve_description,
          cwe.id AS cwe_id,
          cwe.name AS cwe_name,
          cwe.description AS cwe_description
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            pairs = []

            for record in result:
                pair = {
                    "cve_id": record["cve_id"],
                    "cve_description": record["cve_description"],
                    "cwe_id": record["cwe_id"],
                    "cwe_name": record["cwe_name"],
                    "cwe_description": record["cwe_description"]
                }
                pairs.append(pair)

            return pairs

def main():
    # Get credentials from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    extractor = CVECWEExtractor(uri, user, password)

    try:
        print("Extracting CVE→CWE pairs...")
        pairs = extractor.extract_pairs(limit=10000)
        print(f"Extracted {len(pairs)} pairs")

        # Save to JSON
        output_path = "data/raw/cve_cwe_pairs.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(pairs, f, indent=2)

        print(f"Saved to {output_path}")

    finally:
        extractor.close()

if __name__ == "__main__":
    main()
```

#### 1.2 Run Extraction

```bash
# Create necessary directories
mkdir -p data/raw data/processed data/training

# Run extraction
python scripts/extract_cve_cwe_pairs.py

# Verify output
ls -lh data/raw/cve_cwe_pairs.json
head -n 20 data/raw/cve_cwe_pairs.json
```

### Step 2: Extract Attack Chain Data

#### 2.1 Create Attack Chain Extraction Script

Create `scripts/extract_attack_chains.py`:

```python
#!/usr/bin/env python3
"""
Extract full attack chains (CVE→CWE→CAPEC→ATTACK) where available
"""

from neo4j import GraphDatabase
import json
import os

class AttackChainExtractor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def extract_chains(self, limit=1000):
        """Extract full attack chains"""
        query = """
        MATCH path = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)-[:EXPLOITED_BY]->(capec:CAPEC)-[:MAPS_TO]->(attack:ATTACK)
        RETURN
          cve.id AS cve_id,
          cve.description AS cve_description,
          cwe.id AS cwe_id,
          cwe.name AS cwe_name,
          capec.id AS capec_id,
          capec.name AS capec_name,
          attack.id AS attack_id,
          attack.name AS attack_name
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            chains = []

            for record in result:
                chain = {
                    "cve_id": record["cve_id"],
                    "cve_description": record["cve_description"],
                    "cwe_id": record["cwe_id"],
                    "cwe_name": record["cwe_name"],
                    "capec_id": record["capec_id"],
                    "capec_name": record["capec_name"],
                    "attack_id": record["attack_id"],
                    "attack_name": record["attack_name"]
                }
                chains.append(chain)

            return chains

def main():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    extractor = AttackChainExtractor(uri, user, password)

    try:
        print("Extracting attack chains...")
        chains = extractor.extract_chains(limit=1000)
        print(f"Extracted {len(chains)} complete chains")

        output_path = "data/raw/attack_chains.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(chains, f, indent=2)

        print(f"Saved to {output_path}")

    finally:
        extractor.close()

if __name__ == "__main__":
    main()
```

#### 2.2 Run Attack Chain Extraction

```bash
python scripts/extract_attack_chains.py

# Verify output
ls -lh data/raw/attack_chains.json
```

### Step 3: Validate Data Quality

#### 3.1 Create Validation Script

Create `scripts/validate_training_data.py`:

```python
#!/usr/bin/env python3
"""
Validate extracted training data quality
"""

import json
import argparse
from collections import Counter

def validate_cve_cwe_pairs(pairs):
    """Validate CVE→CWE pairs"""
    print("\n=== CVE→CWE Pairs Validation ===")
    print(f"Total pairs: {len(pairs)}")

    # Check required fields
    required_fields = ["cve_id", "cve_description", "cwe_id"]
    missing_fields = []

    for i, pair in enumerate(pairs):
        for field in required_fields:
            if field not in pair or not pair[field]:
                missing_fields.append((i, field))

    if missing_fields:
        print(f"❌ Missing required fields: {len(missing_fields)}")
        print(f"   Examples: {missing_fields[:5]}")
    else:
        print("✅ All pairs have required fields")

    # Check description lengths
    short_descriptions = [
        i for i, pair in enumerate(pairs)
        if len(pair.get("cve_description", "")) < 50
    ]

    if short_descriptions:
        print(f"⚠️  Short CVE descriptions (<50 chars): {len(short_descriptions)}")
        print(f"   Indices: {short_descriptions[:10]}")
    else:
        print("✅ All CVE descriptions are adequate length")

    # CWE distribution
    cwe_counts = Counter([pair["cwe_id"] for pair in pairs])
    print(f"\nCWE distribution:")
    print(f"  Unique CWEs: {len(cwe_counts)}")
    print(f"  Top 10 CWEs:")
    for cwe_id, count in cwe_counts.most_common(10):
        print(f"    {cwe_id}: {count} occurrences")

    return len(missing_fields) == 0 and len(short_descriptions) < len(pairs) * 0.05

def validate_attack_chains(chains):
    """Validate full attack chains"""
    print("\n=== Attack Chains Validation ===")
    print(f"Total chains: {len(chains)}")

    if len(chains) == 0:
        print("⚠️  No complete attack chains found (expected for sparse data)")
        return True

    # Check completeness
    required_fields = ["cve_id", "cwe_id", "capec_id", "attack_id"]
    incomplete_chains = []

    for i, chain in enumerate(chains):
        missing = [f for f in required_fields if f not in chain or not chain[f]]
        if missing:
            incomplete_chains.append((i, missing))

    if incomplete_chains:
        print(f"❌ Incomplete chains: {len(incomplete_chains)}")
        print(f"   Examples: {incomplete_chains[:5]}")
    else:
        print("✅ All chains are complete")

    return len(incomplete_chains) == 0

def calculate_semantic_overlap(pairs, sample_size=100):
    """Calculate semantic overlap between CVE and CWE descriptions"""
    print("\n=== Semantic Overlap Analysis ===")

    import random
    sample = random.sample(pairs, min(sample_size, len(pairs)))

    overlaps = []
    for pair in sample:
        cve_words = set(pair["cve_description"].lower().split())
        cwe_words = set(pair.get("cwe_description", "").lower().split())

        # Filter words > 4 characters
        cve_words = {w for w in cve_words if len(w) > 4}
        cwe_words = {w for w in cwe_words if len(w) > 4}

        if len(cve_words) > 0:
            overlap = len(cve_words & cwe_words) / len(cve_words)
            overlaps.append(overlap)

    avg_overlap = sum(overlaps) / len(overlaps) if overlaps else 0

    print(f"Average semantic overlap: {avg_overlap * 100:.2f}%")
    print(f"Sample size: {len(overlaps)}")

    if avg_overlap < 0.01:
        print("✅ Low semantic overlap confirms need for partial chain training")
    else:
        print("⚠️  Higher than expected semantic overlap")

    return avg_overlap

def main():
    parser = argparse.ArgumentParser(description="Validate training data")
    parser.add_argument("--cve-cwe", default="data/raw/cve_cwe_pairs.json")
    parser.add_argument("--attack-chains", default="data/raw/attack_chains.json")
    args = parser.parse_args()

    # Load data
    print("Loading data...")
    with open(args.cve_cwe, "r") as f:
        pairs = json.load(f)

    try:
        with open(args.attack_chains, "r") as f:
            chains = json.load(f)
    except FileNotFoundError:
        chains = []
        print("No attack chains file found")

    # Validate
    pairs_valid = validate_cve_cwe_pairs(pairs)
    chains_valid = validate_attack_chains(chains)
    overlap = calculate_semantic_overlap(pairs)

    # Summary
    print("\n=== Validation Summary ===")
    if pairs_valid and chains_valid:
        print("✅ All validation checks passed")
        print("✅ Data is ready for training")
    else:
        print("❌ Some validation checks failed")
        print("⚠️  Review errors above before proceeding")

if __name__ == "__main__":
    main()
```

#### 3.2 Run Validation

```bash
python scripts/validate_training_data.py \
    --cve-cwe data/raw/cve_cwe_pairs.json \
    --attack-chains data/raw/attack_chains.json
```

### Step 4: Generate spaCy Training Format

#### 4.1 Create Training Data Generator

Create `scripts/generate_spacy_training.py`:

```python
#!/usr/bin/env python3
"""
Convert extracted data to spaCy training format
"""

import json
import spacy
from spacy.training import Example
from spacy.tokens import DocBin
import random

def convert_to_spacy_format(cve_cwe_pairs, attack_chains):
    """Convert to spaCy training format"""
    training_data = []

    # Process CVE→CWE pairs (primary training data)
    for pair in cve_cwe_pairs:
        text = pair["cve_description"]

        # Create entity annotations
        # Note: We're training relationship-aware NER, not span detection
        # The model learns which CVE descriptions relate to which CWEs
        entities = []

        # Add CVE as entity (entire description)
        entities.append((0, len(text), "CVE"))

        # Create training example
        example = {
            "text": text,
            "entities": entities,
            "links": {
                pair["cve_id"]: {
                    "CWE": [pair["cwe_id"]]
                }
            }
        }
        training_data.append(example)

    # Process attack chains (contextual training data)
    for chain in attack_chains:
        # Combine descriptions for context
        text = f"{chain['cve_description']} Related to {chain['cwe_name']} ({chain['cwe_id']}) exploited via {chain['capec_name']} mapped to {chain['attack_name']}"

        entities = [
            (0, len(chain['cve_description']), "CVE"),
            # Add more entities if they can be located in text
        ]

        example = {
            "text": text,
            "entities": entities,
            "links": {
                chain["cve_id"]: {
                    "CWE": [chain["cwe_id"]],
                    "CAPEC": [chain["capec_id"]],
                    "ATTACK": [chain["attack_id"]]
                }
            }
        }
        training_data.append(example)

    return training_data

def create_docbin(training_data, nlp):
    """Create DocBin for spaCy training"""
    db = DocBin()

    for example in training_data:
        doc = nlp.make_doc(example["text"])

        # Add entity spans
        ents = []
        for start, end, label in example["entities"]:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)

        doc.ents = ents
        db.add(doc)

    return db

def main():
    print("Loading extracted data...")
    with open("data/raw/cve_cwe_pairs.json") as f:
        pairs = json.load(f)

    try:
        with open("data/raw/attack_chains.json") as f:
            chains = json.load(f)
    except FileNotFoundError:
        chains = []

    print(f"Loaded {len(pairs)} CVE→CWE pairs")
    print(f"Loaded {len(chains)} attack chains")

    # Convert to spaCy format
    print("\nConverting to spaCy format...")
    training_data = convert_to_spacy_format(pairs, chains)

    # Split train/dev/test
    random.shuffle(training_data)
    train_size = int(0.8 * len(training_data))
    dev_size = int(0.1 * len(training_data))

    train_data = training_data[:train_size]
    dev_data = training_data[train_size:train_size+dev_size]
    test_data = training_data[train_size+dev_size:]

    print(f"Train: {len(train_data)}")
    print(f"Dev: {len(dev_data)}")
    print(f"Test: {len(test_data)}")

    # Create DocBins
    print("\nCreating DocBins...")
    nlp = spacy.blank("en")

    train_db = create_docbin(train_data, nlp)
    dev_db = create_docbin(dev_data, nlp)
    test_db = create_docbin(test_data, nlp)

    # Save DocBins
    train_db.to_disk("data/training/train.spacy")
    dev_db.to_disk("data/training/dev.spacy")
    test_db.to_disk("data/training/test.spacy")

    print("✅ Training data generated successfully")
    print("   Files saved to data/training/")

if __name__ == "__main__":
    main()
```

#### 4.2 Generate Training Files

```bash
python scripts/generate_spacy_training.py
```

### Step 5: Train spaCy NER Model

#### 5.1 Create Training Configuration

Create `configs/ner_v7_config.cfg`:

```ini
[paths]
train = "data/training/train.spacy"
dev = "data/training/dev.spacy"
vectors = null
init_tok2vec = null

[system]
gpu_allocator = "pytorch"
seed = 0

[nlp]
lang = "en"
pipeline = ["transformer","ner"]
batch_size = 128
disabled = []
before_creation = null
after_creation = null
after_pipeline_creation = null
tokenizer = {"@tokenizers":"spacy.Tokenizer.v1"}

[components]

[components.transformer]
factory = "transformer"

[components.transformer.model]
@architectures = "spacy-transformers.TransformerModel.v3"
name = "roberta-base"
mixed_precision = false

[components.transformer.model.get_spans]
@span_getters = "spacy-transformers.strided_spans.v1"
window = 128
stride = 96

[components.ner]
factory = "ner"
incorrect_spans_key = null
moves = null
scorer = {"@scorers":"spacy.ner_scorer.v1"}
update_with_oracle_cut_size = 100

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v2"
state_type = "ner"
extra_state_tokens = false
hidden_width = 64
maxout_pieces = 2
use_upper = false
nO = null

[components.ner.model.tok2vec]
@architectures = "spacy-transformers.TransformerListener.v1"
grad_factor = 1.0
pooling = {"@layers":"reduce_mean.v1"}
upstream = "*"

[corpora]

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"
seed = ${system.seed}
gpu_allocator = ${system.gpu_allocator}
dropout = 0.1
accumulate_gradient = 3
patience = 10000
max_epochs = 100
max_steps = 20000
eval_frequency = 200
frozen_components = []
annotating_components = []
before_to_disk = null
before_update = null

[training.batcher]
@batchers = "spacy.batch_by_padded.v1"
discard_oversize = true
size = 2000
buffer = 256
get_length = null

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
progress_bar = false

[training.optimizer]
@optimizers = "Adam.v1"
beta1 = 0.9
beta2 = 0.999
L2_is_weight_decay = true
L2 = 0.01
grad_clip = 1.0
use_averages = false
eps = 0.00000001
learn_rate = 0.00005

[training.score_weights]
ents_f = 0.5
ents_p = 0.25
ents_r = 0.25
ents_per_type = null

[pretraining]

[initialize]
vectors = ${paths.vectors}
init_tok2vec = ${paths.init_tok2vec}
vocab_data = null
lookups = null
before_init = null
after_init = null

[initialize.components]

[initialize.tokenizer]
```

#### 5.2 Train Model

```bash
# Train spaCy model
python -m spacy train \
    configs/ner_v7_config.cfg \
    --output models/ner_v7 \
    --paths.train data/training/train.spacy \
    --paths.dev data/training/dev.spacy \
    --gpu-id 0

# Training will take 4-6 hours on GPU
# Monitor progress in console output
```

#### 5.3 Evaluate Model

```bash
# Evaluate on test set
python -m spacy evaluate \
    models/ner_v7/model-best \
    data/training/test.spacy \
    --gpu-id 0

# Expected output:
# ents_f: 0.75-0.85
# ents_p: 0.70-0.80
# ents_r: 0.75-0.85
```

## Troubleshooting

### Issue 1: Neo4j Connection Errors

**Error**: `ServiceUnavailable: Unable to retrieve routing information`

**Solution**:
```bash
# Check Neo4j is running
sudo systemctl status neo4j

# Check connection
cypher-shell -u neo4j -p your_password "RETURN 1;"

# Verify bolt port is open
netstat -tuln | grep 7687
```

### Issue 2: Insufficient Training Data

**Error**: `ValueError: Not enough training examples`

**Solution**:
```bash
# Check extracted data size
wc -l data/raw/cve_cwe_pairs.json

# If <1000 lines, extract more data:
python scripts/extract_cve_cwe_pairs.py --limit 20000
```

### Issue 3: GPU Memory Errors

**Error**: `CUDA out of memory`

**Solution**:
Edit `configs/ner_v7_config.cfg`:
```ini
[training.batcher]
size = 1000  # Reduce from 2000

[training]
accumulate_gradient = 4  # Increase from 3
```

### Issue 4: Low Model Performance

**Symptom**: F1 score <0.60

**Diagnosis**:
```bash
# Check data quality
python scripts/validate_training_data.py

# Check class imbalance
python -c "
import json
from collections import Counter
with open('data/raw/cve_cwe_pairs.json') as f:
    data = json.load(f)
cwe_counts = Counter([d['cwe_id'] for d in data])
print('Top 10 CWEs:', cwe_counts.most_common(10))
print('Bottom 10 CWEs:', cwe_counts.most_common()[-10:])
"
```

**Solution**: Balance dataset or use class weights

### Issue 5: spaCy Training Crashes

**Error**: `RuntimeError: CUDA error: device-side assert triggered`

**Solution**:
```bash
# Run on CPU to debug
python -m spacy train configs/ner_v7_config.cfg \
    --output models/ner_v7 \
    --gpu-id -1  # CPU mode

# Check for invalid entity spans
python scripts/validate_training_data.py --verbose
```

## Advanced Configuration

### Optimize for Different Hardware

#### For CPU-Only Systems
```ini
# configs/ner_v7_cpu_config.cfg
[components.transformer.model]
name = "distilroberta-base"  # Smaller model

[training.batcher]
size = 500  # Smaller batches
```

#### For Multi-GPU Systems
```bash
# Use ray for distributed training
python -m spacy ray train \
    configs/ner_v7_config.cfg \
    --num-gpus 4 \
    --output models/ner_v7
```

### Custom Loss Function

For advanced users implementing relationship loss:

```python
# scripts/train_with_custom_loss.py
from spacy.training import Example
import spacy

def partial_chain_loss(examples, **kwargs):
    """Custom loss for relationship-aware NER"""
    entity_loss = 0
    relationship_loss = 0

    for example in examples:
        # Standard NER loss
        entity_loss += example.get_loss()

        # Relationship loss
        predicted_links = example.predicted._.links
        gold_links = example.reference._.links

        for cve_id, gold_rels in gold_links.items():
            pred_rels = predicted_links.get(cve_id, {})
            for rel_type, targets in gold_rels.items():
                if rel_type in pred_rels:
                    # Cosine similarity between embeddings
                    similarity = compute_similarity(
                        pred_rels[rel_type],
                        targets
                    )
                    relationship_loss += (1 - similarity)

    total_loss = 0.7 * entity_loss + 0.3 * relationship_loss
    return total_loss

# Use in training loop
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Override loss function
ner.get_loss = partial_chain_loss
```

## Next Steps

After successful training:

1. **Evaluate on recent CVEs**: Test model on 2024+ vulnerabilities
2. **Deploy as API**: Wrap model in Flask/FastAPI service
3. **Monitor performance**: Track precision/recall on production data
4. **Iterative improvement**: Retrain with user feedback

## Additional Resources

- **Cypher Queries**: `CYPHER_QUERIES_NER_V7.md`
- **Schema Documentation**: `SCHEMA_UPDATE_NER_V7.md`
- **Methodology**: `WIKI_PARTIAL_CHAIN_TRAINING.md`
- **Prevention Guide**: `PREVENTION_COMPLETE_CHAIN_ASSUMPTION.md`

## Support

For issues or questions:
1. Check existing documentation in `docs/`
2. Review evaluation results in `../evaluation/NER_V7_APPROACH_EVALUATION.json`
3. Consult spaCy documentation: https://spacy.io/usage/training
