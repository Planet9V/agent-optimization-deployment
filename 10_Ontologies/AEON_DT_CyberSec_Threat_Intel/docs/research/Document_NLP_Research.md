# Document NLP Research: Entity Extraction and Relationship Recognition for Threat Intelligence

**Date:** 2025-10-29
**Version:** 1.0
**Purpose:** Comprehensive guide to spaCy NLP framework, entity extraction, relationship recognition patterns, and performance optimization for cybersecurity documents

---

## 1. spaCy Architecture and Capabilities

### 1.1 spaCy Core Components

spaCy is an industrial-strength NLP library designed for production-grade text processing with integrated neural models.

**Core Components:**

| Component | Purpose | Performance |
|-----------|---------|-------------|
| **Tokenizer** | Segment text into tokens | ~1M tokens/second |
| **Tagger** | POS and morphological tags | ~50K tokens/second |
| **Parser** | Dependency parsing | ~10K sentences/second |
| **NER** | Named entity recognition | ~50K tokens/second |
| **Vectors** | Word embeddings | Fast lookup |
| **Matcher** | Pattern-based matching | Real-time |

### 1.2 Pipeline Architecture

```python
import spacy
from spacy import Language
from typing import List

# Load pre-trained model
nlp = spacy.load("en_core_web_lg")

# Pipeline components in order:
# 1. Tokenizer: "text" -> ["text"]
# 2. Tagger: assigns POS tags
# 3. Parser: creates dependency tree
# 4. NER: recognizes entities

doc = nlp("Microsoft disclosed a critical vulnerability in Windows")

# Inspect pipeline
for component_name, component in nlp.pipeline:
    print(f"{component_name}: {component}")
```

### 1.3 Available Models

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `en_core_web_sm` | 40MB | Fast | 85% | Quick processing |
| `en_core_web_md` | 40MB | Medium | 90% | Production default |
| `en_core_web_lg` | 740MB | Slower | 92% | Maximum accuracy |
| `en_core_web_trf` | 450MB | Slowest | 95%+ | State-of-the-art |

### 1.4 Model Architecture: Transformer vs Traditional

**Traditional (Small/Medium/Large models):**
- Word vectors + CNN-based NER
- Fast inference, lower memory
- Suitable for real-time processing
- Word embedding-based (no context)

**Transformer (trf models):**
- BERT-based processing
- Contextual embeddings
- Higher accuracy, slower inference
- Best for complex documents

---

## 2. Entity Extraction Techniques

### 2.1 Built-in Named Entity Recognition

```python
import spacy

nlp = spacy.load("en_core_web_lg")

threat_report = """
APT28 (also known as Fancy Bear) was identified conducting cyber operations
against NATO members using malware variants including Sofacy and Sakula.
The attack involved phishing emails from attacker@example.com targeting
employees at 192.168.1.1 networks.
"""

doc = nlp(threat_report)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text:25} {ent.label_:10} {spacy.explain(ent.label_)}")

# Output example:
# APT28                     ORG        Companies, agencies, institutions, etc.
# Fancy Bear                PERSON     People, including fictional
# NATO                      ORG        Organizations
# attacker@example.com      ORG        (email addresses often misclassified)
# 192.168.1.1              GPE        Countries, cities, states
```

### 2.2 Custom Entity Recognition for Threat Intelligence

```python
from spacy.training import Example
from spacy.util import minibatch, compounding
import random

def create_custom_ner_pipeline():
    """Create custom NER pipeline for threat intelligence."""

    # Training data for custom entities
    TRAIN_DATA = [
        (
            "CVE-2025-1234 affects Windows Server 2019",
            {
                "entities": [
                    (0, 11, "CVE"),  # CVE-2025-1234
                    (29, 43, "PRODUCT"),  # Windows Server 2019
                ]
            }
        ),
        (
            "Malware hash: d41d8cd98f00b204e9800998ecf8427e identified",
            {
                "entities": [
                    (14, 46, "HASH"),  # MD5 hash
                ]
            }
        ),
        (
            "IP address 10.0.0.1 was command and control server",
            {
                "entities": [
                    (12, 20, "IP_ADDRESS"),
                ]
            }
        ),
    ]

    # Load base model
    nlp = spacy.load("en_core_web_sm")

    # Create NER component if not exists
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add custom labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    # Disable other components during training
    disabled_pipes = [
        pipe for pipe in nlp.pipe_names if pipe != "ner"
    ]

    with nlp.disable_pipes(*disabled_pipes):
        optimizer = nlp.create_optimizer()

        for iteration in range(30):
            random.shuffle(TRAIN_DATA)
            losses = {}

            for batch in minibatch(TRAIN_DATA, size=8):
                examples = [
                    Example.from_dict(nlp.make_doc(text), annotations)
                    for text, annotations in batch
                ]
                nlp.update(
                    examples,
                    drop=0.5,
                    sgd=optimizer,
                    losses=losses,
                )
            print(f"Iteration {iteration}: {losses}")

    return nlp
```

### 2.3 Pattern-Based Entity Recognition

```python
from spacy.matcher import Matcher, PhraseMatcher

nlp = spacy.load("en_core_web_lg")

# Pattern matcher for specific entity types
matcher = Matcher(nlp.vocab)

# CVE pattern: CVE-YYYY-NNNNN
cvE_pattern = [
    {"LOWER": "cve"},
    {"IS_PUNCT": True},
    {"IS_DIGIT": True, "LENGTH": {">=": 4}},
    {"IS_PUNCT": True},
    {"IS_DIGIT": True}
]
matcher.add("CVE", [cvE_pattern])

# IPv4 address pattern
ipv4_pattern = [
    {"IS_DIGIT": True},
    {"LITERAL": "."},
    {"IS_DIGIT": True},
    {"LITERAL": "."},
    {"IS_DIGIT": True},
    {"LITERAL": "."},
    {"IS_DIGIT": True}
]
matcher.add("IP_ADDRESS", [ipv4_pattern])

# Hash pattern (MD5: 32 hex chars)
hash_pattern = [
    {
        "IS_ALPHA": True,
        "IS_LOWER": True,
        "LENGTH": 32,
        "REGEX": "^[a-f0-9]{32}$"
    }
]
matcher.add("HASH", [hash_pattern])

# Phrase matcher for known threats
phrase_matcher = PhraseMatcher(nlp.vocab)
threat_phrases = [
    "APT28",
    "Fancy Bear",
    "Sofacy",
    "Emotet",
    "Wannacry"
]

patterns = [nlp.make_doc(phrase) for phrase in threat_phrases]
phrase_matcher.add("THREAT_ACTOR", patterns)

# Apply matchers
doc = nlp("CVE-2025-1234 targets 192.168.1.1, APT28 used Sofacy malware")

print("Pattern matches:")
for match_id, start, end in matcher(doc):
    span = doc[start:end]
    label = nlp.vocab.strings[match_id]
    print(f"  {label}: {span.text}")

print("\nPhrase matches:")
for match_id, start, end in phrase_matcher(doc):
    span = doc[start:end]
    label = nlp.vocab.strings[match_id]
    print(f"  {label}: {span.text}")
```

### 2.4 Regex-Based Extraction

```python
import re
from typing import Dict, List, Tuple

class ThreatIntelligenceExtractor:
    """Extract threat intelligence indicators from text."""

    # Regex patterns for common indicators
    PATTERNS = {
        'CVE': r'CVE-\d{4}-\d{4,}',
        'IPv4': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        'IPv6': r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}',
        'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'MD5': r'\b[a-fA-F0-9]{32}\b',
        'SHA1': r'\b[a-fA-F0-9]{40}\b',
        'SHA256': r'\b[a-fA-F0-9]{64}\b',
        'Domain': r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
        'URL': r'https?://[^\s]+',
    }

    @classmethod
    def extract_indicators(
        cls,
        text: str,
        indicator_types: List[str] = None
    ) -> Dict[str, List[Tuple[str, int]]]:
        """
        Extract threat indicators from text.

        Returns:
            Dict mapping indicator type to list of (value, position) tuples
        """
        if indicator_types is None:
            indicator_types = list(cls.PATTERNS.keys())

        results = {}

        for ind_type in indicator_types:
            if ind_type not in cls.PATTERNS:
                continue

            pattern = cls.PATTERNS[ind_type]
            matches = re.finditer(pattern, text, re.IGNORECASE)

            results[ind_type] = [
                (match.group(), match.start())
                for match in matches
            ]

        return results

# Usage
extractor = ThreatIntelligenceExtractor()
text = """
Critical vulnerability CVE-2025-1234 discovered in Windows Server.
Attack originated from 192.168.1.100 targeting company.com.
MD5 hash: d41d8cd98f00b204e9800998ecf8427e
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Attacker email: attacker@malicious.org
"""

indicators = extractor.extract_indicators(text)
for ind_type, matches in indicators.items():
    print(f"{ind_type}:")
    for value, position in matches:
        print(f"  {value} (position {position})")
```

---

## 3. Relationship Extraction Patterns

### 3.1 Dependency Parsing for Relationships

```python
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_lg")

def extract_relationships_from_dependencies(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract relationships using dependency parsing.

    Returns:
        List of (subject, relationship, object) tuples
    """
    doc = nlp(text)
    relationships = []

    for token in doc:
        # Subject-verb-object pattern
        if token.dep_ == "nsubj":  # Nominal subject
            verb = token.head
            # Find object
            for child in verb.children:
                if child.dep_ in ("dobj", "attr"):  # Direct object
                    relationships.append((
                        token.text,
                        verb.text,
                        child.text
                    ))

    return relationships

# Example
text = "APT28 used Sofacy malware to target NATO organizations"
rels = extract_relationships_from_dependencies(text)

for subj, verb, obj in rels:
    print(f"{subj} {verb} {obj}")
# Output: APT28 used Sofacy
```

### 3.2 Semantic Relationship Recognition

```python
from spacy.matcher import Matcher, DependencyMatcher
import spacy

nlp = spacy.load("en_core_web_lg")

def extract_threat_relationships(text: str) -> Dict[str, List]:
    """Extract threat intelligence relationships."""
    doc = nlp(text)

    # Initialize relationship extractors
    threat_actor_uses_malware = []
    malware_targets_sector = []
    vuln_in_product = []

    # Pattern 1: [Threat Actor] uses [Malware]
    actor_malware_matcher = Matcher(nlp.vocab)
    pattern1 = [
        {"ENT_TYPE": "ORG"},
        {"LEMMA": "use"},
        {"ENT_TYPE": {"IN": ["PRODUCT", "GPE"]}}
    ]
    actor_malware_matcher.add("ACTOR_USES", [pattern1])

    # Pattern 2: [Malware] targets [Sector]
    malware_target_matcher = Matcher(nlp.vocab)
    pattern2 = [
        {"ENT_TYPE": "PRODUCT"},
        {"LEMMA": {"IN": ["target", "affect"]}},
        {"ENT_TYPE": "ORG"}
    ]
    malware_target_matcher.add("MALWARE_TARGETS", [pattern2])

    # Extract matches
    for match_id, start, end in actor_malware_matcher(doc):
        span = doc[start:end]
        tokens = [token.text for token in span]
        threat_actor_uses_malware.append({
            'actor': tokens[0],
            'malware': tokens[-1],
            'context': span.text
        })

    return {
        'actor_uses_malware': threat_actor_uses_malware,
        'malware_targets': malware_targets_sector,
        'vuln_in_product': vuln_in_product
    }
```

### 3.3 Knowledge Graph Construction from Text

```python
from neo4j import GraphDatabase
from typing import List, Dict

class ThreatGraphBuilder:
    """Build threat intelligence knowledge graph from documents."""

    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def build_from_document(self, text: str, doc_id: str):
        """Extract entities and relationships, store in Neo4j."""
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(text)

        # Extract entities
        entities = {}
        for ent in doc.ents:
            if ent.label_ in ("ORG", "GPE", "PERSON"):
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

        # Extract relationships from text patterns
        relationships = self._extract_relationships(doc)

        # Store in graph
        with self.driver.session() as session:
            # Create document node
            session.run("""
                CREATE (d:Document {id: $doc_id, text: $text})
            """, {"doc_id": doc_id, "text": text})

            # Create entity nodes
            for ent_type, ent_list in entities.items():
                for ent in set(ent_list):
                    session.run("""
                        MERGE (e:{entity_type} {{name: $name}})
                        WITH e, d
                        MATCH (d:Document {{id: $doc_id}})
                        CREATE (d)-[:MENTIONS]->(e)
                    """.format(entity_type=ent_type),
                    {"name": ent, "doc_id": doc_id})

            # Create relationships
            for rel in relationships:
                session.run("""
                    MATCH (source {name: $source})
                    MATCH (target {name: $target})
                    CREATE (source)-[:{rel_type}]->(target)
                """.format(rel_type=rel['type']),
                {"source": rel['source'], "target": rel['target']})

    def _extract_relationships(self, doc) -> List[Dict]:
        """Extract relationships from parsed document."""
        relationships = []

        for token in doc:
            if token.dep_ == "nsubj":
                verb = token.head
                for child in verb.children:
                    if child.dep_ in ("dobj", "attr"):
                        relationships.append({
                            'source': token.text,
                            'type': verb.lemma_.upper(),
                            'target': child.text
                        })

        return relationships
```

---

## 4. Performance Benchmarks and Optimization

### 4.1 Processing Speed Benchmarks

| Operation | Model | Speed | Notes |
|-----------|-------|-------|-------|
| Tokenization | All | ~1M tokens/sec | Very fast |
| POS Tagging | `sm` | ~50K tokens/sec | CPU-bound |
| Dependency Parsing | `sm` | ~10K tokens/sec | Most expensive |
| NER | `lg` | ~30K tokens/sec | With vectors |
| NER | `trf` | ~1K tokens/sec | BERT-based, accurate |

### 4.2 Optimization Techniques

```python
import spacy
from spacy.util import get_lang_class

class OptimizedNLPPipeline:
    """Optimized NLP pipeline for high-throughput processing."""

    def __init__(self, model_name: str = "en_core_web_md"):
        self.nlp = spacy.load(model_name)

        # Disable unnecessary components
        disabled = []
        if "parser" in self.nlp.pipe_names:
            self.nlp.disable_pipes("parser")  # If not needed
            disabled.append("parser")

        print(f"Disabled components: {disabled}")

    def process_batch(self, texts: List[str], batch_size: int = 128):
        """Process texts in batches for better performance."""
        results = []

        # Use pipe() for batch processing (2-3x faster than individual calls)
        for doc in self.nlp.pipe(texts, batch_size=batch_size, n_process=4):
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            results.append(entities)

        return results

    def process_with_filtering(self, texts: List[str]) -> List[Dict]:
        """Process with output filtering to reduce memory."""
        results = []

        for doc in self.nlp.pipe(texts, batch_size=128):
            # Only keep entities of interest
            filtered_ents = [
                {
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                }
                for ent in doc.ents
                if ent.label_ in ("ORG", "GPE", "PERSON", "PRODUCT")
            ]

            if filtered_ents:
                results.append({'doc': doc.text[:100], 'entities': filtered_ents})

        return results

# Benchmark comparison
import time

nlp_full = spacy.load("en_core_web_md")
pipeline = OptimizedNLPPipeline("en_core_web_md")

sample_texts = [
    "APT28 was identified conducting cyber operations against NATO members.",
] * 1000

# Full pipeline
start = time.time()
for doc in nlp_full.pipe(sample_texts, batch_size=128):
    _ = doc.ents
full_time = time.time() - start

# Optimized pipeline
start = time.time()
results = pipeline.process_batch(sample_texts)
opt_time = time.time() - start

print(f"Full pipeline: {full_time:.2f}s")
print(f"Optimized: {opt_time:.2f}s")
print(f"Speedup: {full_time / opt_time:.1f}x")
```

### 4.3 Memory Optimization

```python
import spacy
from spacy.util import ensure_path

class MemoryOptimizedNLP:
    """Optimize memory usage for large-scale processing."""

    @staticmethod
    def process_large_file(
        file_path: str,
        chunk_size: int = 100
    ) -> Dict:
        """Process large files in chunks to minimize memory."""
        nlp = spacy.load("en_core_web_md", disable=["parser"])

        with open(file_path, 'r') as f:
            chunk = []
            for i, line in enumerate(f):
                chunk.append(line.strip())

                if len(chunk) >= chunk_size:
                    # Process chunk and clear
                    docs = list(nlp.pipe(chunk))
                    yield from docs
                    chunk = []

            # Process remaining
            if chunk:
                yield from nlp.pipe(chunk)

    @staticmethod
    def use_gpu_acceleration():
        """Enable GPU acceleration if available."""
        import spacy
        spacy.prefer_gpu()
        nlp = spacy.load("en_core_web_lg")
        return nlp
```

---

## References

Honnibal, M., Montani, I., Van Landeghem, S., & Boyd, A. (2020). spaCy: Industrial-strength natural language processing in Python. https://doi.org/10.5281/zenodo.1212303

Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. *Proceedings of ICLR Workshop*, 2.

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. *arXiv preprint arXiv:1810.04805*.

Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularization. *International Conference on Learning Representations*, ICLR 2019.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.

Goldberg, Y. (2016). A primer on neural network architectures for natural language processing. *Journal of Artificial Intelligence Research*, 57, 345–420.
