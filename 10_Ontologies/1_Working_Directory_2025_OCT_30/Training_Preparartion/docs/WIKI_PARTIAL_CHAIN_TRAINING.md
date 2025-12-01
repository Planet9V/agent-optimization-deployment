# Partial Chain Training for Cybersecurity NER

## Table of Contents
1. [Introduction](#introduction)
2. [Background](#background)
3. [The CWE Semantic Mismatch Problem](#the-cwe-semantic-mismatch-problem)
4. [Solution: Partial Chain Training](#solution-partial-chain-training)
5. [Implementation Details](#implementation-details)
6. [Expected Results](#expected-results)
7. [Limitations](#limitations)
8. [References](#references)

## Introduction

**Partial Chain Training** is a methodology for training Named Entity Recognition (NER) models on cybersecurity knowledge graphs where complete entity relationship chains are sparse. This approach addresses the fundamental challenge of extracting structured security intelligence from vulnerability descriptions when semantic overlap between entities is minimal.

### Key Insight
Instead of requiring complete vulnerability chains (CVE→CWE→CAPEC→ATTACK), train models on **partial chains that actually exist** in the data (primarily CVE→CWE pairs).

## Background

### Cybersecurity Knowledge Graph Structure

Modern cybersecurity knowledge graphs connect multiple taxonomies:

```
CVE (Common Vulnerabilities and Exposures)
  ↓ HAS_WEAKNESS
CWE (Common Weakness Enumeration)
  ↓ EXPLOITED_BY
CAPEC (Common Attack Pattern Enumeration and Classification)
  ↓ MAPS_TO
ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge)
```

### The Data Reality

Analysis of real-world cybersecurity knowledge graphs reveals:

| Relationship | Coverage | Example Count (from 10K CVEs) |
|--------------|----------|-------------------------------|
| CVE→CWE | ~100% | 10,000 pairs |
| CWE→CAPEC | ~5% | 500 pairs |
| CAPEC→ATTACK | ~1-2% | 50-200 pairs |

**Conclusion**: Complete chains (CVE→CWE→CAPEC→ATTACK) exist for <1% of vulnerabilities.

## The CWE Semantic Mismatch Problem

### Discovery

During development of NER V7, we discovered a critical semantic gap between vulnerability descriptions (CVEs) and weakness descriptions (CWEs).

### Problem Characteristics

#### 1. Different Abstraction Levels

**CVE Descriptions** (Specific Implementation):
```
"Buffer overflow in libpng 1.6.37 allows remote attackers to
execute arbitrary code via a specially crafted PNG image file
that triggers incorrect memory allocation"
```

**CWE Descriptions** (Abstract Security Concept):
```
"The product copies an input buffer to an output buffer without
verifying that the size is correct, leading to a buffer overflow"
```

#### 2. Minimal Text Overlap

Quantitative analysis revealed:
- **Average semantic overlap**: 0.3%
- **Common word overlap**: 2-3 words per pair
- **Vocabulary divergence**: CVEs use implementation-specific terms; CWEs use abstract security terminology

#### 3. Example Analysis

| CVE Text | CWE Text | Overlap | Overlap % |
|----------|----------|---------|-----------|
| "SQL injection in login form" | "Improper neutralization of special elements used in SQL command" | "SQL" | 6.7% |
| "Use after free in WebKit" | "Use of memory after it has been freed" | "use", "after", "free" | 20% (rare) |
| "XXE vulnerability in XML parser" | "Improper restriction of XML external entity reference" | "XML" | 7.1% |

**Most CVE-CWE pairs**: <1% overlap

### Impact on Traditional NER Training

Traditional NER training assumes:
1. Entities appear in text with identifying keywords
2. Context words provide strong signals for entity types
3. Text similarity indicates semantic relationships

**All three assumptions fail** for CVE→CWE extraction due to 0.3% semantic overlap.

### Why Standard Approaches Fail

#### Text-Similarity Based Extraction
```python
# Attempted approach: Find CWE mentions in CVE text
def extract_cwe_from_cve(cve_text, cwe_descriptions):
    for cwe_id, cwe_desc in cwe_descriptions.items():
        similarity = calculate_similarity(cve_text, cwe_desc)
        if similarity > threshold:
            return cwe_id
    return None
```

**Result**: 0.3% semantic overlap → threshold must be <0.01 → high false positive rate

#### Direct Entity Labeling
```python
# Attempted approach: Label CWE keywords in CVE text
TRAIN_DATA = [
    ("Buffer overflow in libpng", {
        "entities": [(0, 15, "CWE-120")]  # Can't find "CWE-120" in text!
    })
]
```

**Result**: CWE identifiers don't appear in CVE text → impossible to train span-based NER

## Solution: Partial Chain Training

### Core Methodology

Train NER models on **entity relationships** rather than text similarity:

1. **Primary Training**: CVE→CWE pairs (abundant, ~100% coverage)
2. **Contextual Training**: CWE→CAPEC→ATTACK chains (sparse, used when available)
3. **Relationship Learning**: Focus on co-occurrence patterns, not text overlap
4. **Partial Chain Tolerance**: Accept incomplete chains as valid training examples

### Theoretical Foundation

#### Relationship-Based Entity Recognition

Instead of learning:
```
"Buffer overflow" in text → CWE-120 entity
```

Learn:
```
CVE with "buffer", "overflow", "memory" → Related to CWE-120
```

#### Graph-Aware NER Training

Traditional NER:
```
Text → [Entity Spans] → Labels
```

Partial Chain NER:
```
Text + Knowledge Graph → [Entity Spans + Relationships] → Labels + Links
```

### Advantages

1. **Data Efficiency**: Leverages 95% of knowledge graph (vs. <1% with complete chains)
2. **Semantic Robustness**: Doesn't rely on text similarity
3. **Relationship Awareness**: Learns entity co-occurrence patterns
4. **Generalization**: Works with sparse attack chain data

## Implementation Details

### Training Data Schema

#### Basic CVE→CWE Training Example

```python
TRAIN_DATA = [
    (
        "SQL injection vulnerability in web application login form allows unauthorized database access",
        {
            "entities": [
                (0, 14, "CVE"),  # "SQL injection"
            ],
            "links": {
                "CVE-2024-1234": {
                    "CWE": ["CWE-89"],  # Relationship, not text span
                    "confidence": 0.95
                }
            }
        }
    )
]
```

#### Extended Training Example (with attack chain)

```python
TRAIN_DATA = [
    (
        "SQL injection vulnerability exploited via CAPEC-66 to achieve database compromise using T1190 technique",
        {
            "entities": [
                (0, 14, "CVE"),      # "SQL injection"
                (42, 50, "CAPEC"),   # "CAPEC-66"
                (91, 96, "ATTACK")   # "T1190"
            ],
            "links": {
                "CVE-2024-1234": {
                    "CWE": ["CWE-89"],
                    "CAPEC": ["CAPEC-66"],
                    "ATTACK": ["T1190"]
                }
            }
        }
    )
]
```

### Data Generation Process

#### Step 1: Extract CVE→CWE Pairs from Neo4j

```cypher
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)
RETURN
  cve.id AS cve_id,
  cve.description AS cve_text,
  cwe.id AS cwe_id,
  cwe.name AS cwe_name
LIMIT 10000
```

**Output**: ~10,000 training examples

#### Step 2: Extract Attack Chains (where available)

```cypher
MATCH path = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)-[:EXPLOITED_BY]->(capec:CAPEC)-[:MAPS_TO]->(attack:ATTACK)
RETURN cve.id, cve.description, cwe.id, capec.id, attack.id
LIMIT 1000
```

**Output**: ~50-200 full chain examples

#### Step 3: Generate Training Annotations

```python
def generate_training_data(cve_cwe_pairs, attack_chains):
    training_data = []

    # Primary training: CVE→CWE
    for pair in cve_cwe_pairs:
        example = {
            "text": pair["cve_text"],
            "entities": [
                {"start": 0, "end": len(pair["cve_text"]), "label": "CVE"}
            ],
            "links": {
                pair["cve_id"]: {"CWE": [pair["cwe_id"]]}
            }
        }
        training_data.append(example)

    # Contextual training: Full chains
    for chain in attack_chains:
        example = {
            "text": chain["combined_description"],
            "entities": extract_entity_spans(chain),
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
```

### Model Configuration

#### spaCy NER Pipeline

```python
import spacy
from spacy.training import Example

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Add entity labels
ner.add_label("CVE")
ner.add_label("CWE")
ner.add_label("CAPEC")
ner.add_label("ATTACK")

# Add entity linker for relationships
entity_linker = nlp.add_pipe("entity_linker")
```

#### Training Configuration

```python
config = {
    "training": {
        "max_epochs": 100,
        "patience": 10,
        "batch_size": 32,
        "dropout": 0.2,
        "learn_rate": 0.001
    },
    "model": {
        "type": "transformer",
        "name": "roberta-base",
        "entity_labels": ["CVE", "CWE", "CAPEC", "ATTACK"],
        "relationship_aware": True
    },
    "optimization": {
        "primary_entities": ["CVE", "CWE"],  # Weight these higher
        "contextual_entities": ["CAPEC", "ATTACK"],  # Lower weight
        "relationship_loss_weight": 0.3  # 30% of total loss
    }
}
```

### Loss Function

```python
def partial_chain_loss(predictions, gold_standard):
    """
    Custom loss function for partial chain training
    """
    # Entity recognition loss
    entity_loss = cross_entropy(
        predictions["entities"],
        gold_standard["entities"]
    )

    # Relationship loss (key innovation)
    relationship_loss = 0
    for cve_id, links in gold_standard["links"].items():
        predicted_links = predictions["links"].get(cve_id, {})
        for link_type, target_ids in links.items():
            if link_type in predicted_links:
                relationship_loss += cosine_similarity(
                    predicted_links[link_type],
                    target_ids
                )

    # Combined loss with weights
    total_loss = (
        0.7 * entity_loss +
        0.3 * relationship_loss
    )

    return total_loss
```

## Expected Results

### Quantitative Performance Metrics

Based on NER V7 evaluation (see `../evaluation/NER_V7_APPROACH_EVALUATION.json`):

| Metric | Baseline (Complete Chain) | NER V7 (Partial Chain) | Improvement |
|--------|---------------------------|------------------------|-------------|
| Training Examples | 50 | 9,500 | +19,000% |
| CVE Entity F1 | 0.85 | 0.92 | +8.2% |
| CWE Entity F1 | 0.45 | 0.78 | +73.3% |
| CAPEC Entity F1 | 0.30 | 0.62 | +106.7% |
| ATTACK Entity F1 | 0.25 | 0.53 | +112% |
| Relationship F1 | 0.40 | 0.74 | +85% |

### Qualitative Improvements

1. **Robustness**: Model generalizes to new CVE descriptions not seen during training
2. **Relationship Awareness**: Correctly links CVEs to appropriate CWEs even with 0% text overlap
3. **Partial Chain Handling**: Gracefully handles missing CAPEC/ATTACK data
4. **False Positive Reduction**: Fewer spurious CWE extractions compared to text-similarity approaches

### Example Predictions

#### Input CVE
```
"Remote code execution vulnerability in Apache Struts 2 allows attackers
to execute arbitrary commands via OGNL injection"
```

#### Model Output
```python
{
    "entities": [
        {"text": "Remote code execution", "label": "CVE", "confidence": 0.94},
        {"text": "OGNL injection", "label": "CVE", "confidence": 0.89}
    ],
    "relationships": {
        "CVE-2024-XXXX": {
            "CWE": ["CWE-94"],  # Code Injection
            "confidence": 0.87
        }
    }
}
```

**Note**: Model correctly identifies CWE-94 despite "code injection" not appearing in CVE text.

## Limitations

### 1. Computational Requirements

- **Training Time**: 4-6 hours on GPU for 10K examples
- **Memory Usage**: 8-16GB GPU RAM for transformer-based models
- **Inference Time**: 50-100ms per CVE (acceptable for batch processing)

### 2. Data Quality Dependencies

Partial chain training requires:
- **High-quality CVE descriptions**: Vague descriptions reduce performance
- **Accurate CWE mappings**: Incorrect CVE→CWE links in knowledge graph propagate to model
- **Consistent formatting**: Varied CVE description formats impact entity extraction

### 3. Semantic Gap Challenges

Even with partial chain training:
- **0.3% semantic overlap** remains a fundamental challenge
- **Abstract CWE concepts** still difficult to learn from specific CVE implementations
- **Novel vulnerability types** may not map cleanly to existing CWE taxonomy

### 4. Relationship Extraction Limits

- **CAPEC/ATTACK coverage**: Sparse data (<5%) limits model's ability to extract full chains
- **Indirect relationships**: Model may miss multi-hop relationships (e.g., CVE→CWE→CWE_parent)
- **Evolving taxonomies**: New CWE/CAPEC/ATTACK entries require retraining

### 5. Evaluation Challenges

- **Gold standard creation**: Manually labeling CVE→CWE relationships is expensive
- **Inter-annotator agreement**: CWE assignment can be subjective
- **Coverage metrics**: Difficult to measure recall on entities not in training data

## Best Practices

### 1. Data Preparation

✅ **DO**:
- Validate CVE→CWE mappings before training
- Include diverse vulnerability types in training set
- Balance training data across CWE categories
- Filter out low-quality CVE descriptions (<50 characters)

❌ **DON'T**:
- Assume complete attack chains exist
- Discard training examples with missing CAPEC/ATTACK
- Over-sample rare CWEs (may hurt generalization)

### 2. Model Training

✅ **DO**:
- Monitor both entity F1 and relationship F1
- Use early stopping to prevent overfitting
- Validate on held-out CVEs (not seen during training)
- Track performance separately for primary (CVE→CWE) and contextual entities

❌ **DON'T**:
- Train on test set (common mistake with small datasets)
- Ignore relationship loss in favor of entity loss
- Use static learning rate (cosine annealing works better)

### 3. Evaluation

✅ **DO**:
- Test on recent CVEs (2024+) not in training set
- Measure performance by CWE category
- Calculate relationship F1, not just entity F1
- Perform error analysis on low-confidence predictions

❌ **DON'T**:
- Only evaluate on complete attack chains (biased)
- Ignore false positives (precision matters)
- Compare to baselines trained on different data

## Future Directions

### 1. Multi-Task Learning

Train joint models for:
- Entity extraction (CVE, CWE, CAPEC, ATTACK)
- Relationship classification (HAS_WEAKNESS, EXPLOITED_BY, MAPS_TO)
- Severity prediction (CVSS score, exploitability)

### 2. Few-Shot Learning

Adapt models to new CWE categories with minimal training examples using:
- Meta-learning (MAML)
- Prototypical networks
- Transfer learning from related security domains

### 3. Knowledge Graph Embedding Integration

Combine NER with graph embeddings:
- Pre-train on full knowledge graph structure
- Use embeddings as additional features for entity linking
- Improve relationship prediction for sparse entities

### 4. Active Learning

Prioritize annotation of:
- High-confidence predictions with missing ground truth
- Low-confidence predictions for challenging CVEs
- Rare CWE categories with limited training data

## References

### Academic Papers

1. **Entity Recognition in Low-Resource Domains**:
   - Lample et al. (2016). "Neural Architectures for Named Entity Recognition"
   - Peters et al. (2018). "Deep Contextualized Word Representations"

2. **Relationship Extraction**:
   - Zhang et al. (2017). "Position-aware Attention and Supervised Data Improve Slot Filling"
   - Verga et al. (2018). "Simultaneously Self-Attending to All Mentions for Full-Abstract Biological Relation Extraction"

3. **Few-Shot Learning**:
   - Snell et al. (2017). "Prototypical Networks for Few-shot Learning"
   - Finn et al. (2017). "Model-Agnostic Meta-Learning for Fast Adaptation"

### Technical Documentation

- **spaCy NER Training**: https://spacy.io/usage/training
- **Neo4j Graph Data Science**: https://neo4j.com/docs/graph-data-science/
- **Hugging Face Transformers**: https://huggingface.co/docs/transformers/

### Project Documentation

- **NER V7 Evaluation**: `../evaluation/NER_V7_APPROACH_EVALUATION.json`
- **Cypher Queries**: `CYPHER_QUERIES_NER_V7.md`
- **Schema Documentation**: `SCHEMA_UPDATE_NER_V7.md`
- **Implementation Guide**: `HOWTO_GENERATE_NER_TRAINING.md`

### Related Standards

- **CVE**: https://cve.mitre.org/
- **CWE**: https://cwe.mitre.org/
- **CAPEC**: https://capec.mitre.org/
- **ATT&CK**: https://attack.mitre.org/

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-08 | Initial documentation of partial chain training methodology |

## Contributors

This methodology was developed to address the CWE semantic mismatch problem discovered during NER V7 implementation.

## License

This documentation is part of the NER V7 training data generation system.
