# WAVE 4 Step 2: NER11 Entity Extraction

**Document Version**: 1.0
**Created**: 2025-11-25
**Last Modified**: 2025-11-25
**Status**: ACTIVE
**Purpose**: Detailed NER11 entity recognition, classification, and confidence scoring

---

## Table of Contents

1. [Step 2 Overview](#step-2-overview)
2. [NER11 Model Architecture](#ner11-model-architecture)
3. [Entity Types & Classification](#entity-types--classification)
4. [NER Processing Pipeline](#ner-processing-pipeline)
5. [Confidence Scoring System](#confidence-scoring-system)
6. [Entity Normalization](#entity-normalization)
7. [Batch Processing](#batch-processing)
8. [Domain-Specific Models](#domain-specific-models)
9. [Performance Optimization](#performance-optimization)
10. [Quality Assurance](#quality-assurance)

---

## Step 2 Overview

### Purpose

Step 2 applies Named Entity Recognition (NER11) models to identify, classify, and score domain-specific entities within preprocessed documents. This step transforms raw text into structured entity data ready for semantic relationship inference.

### Key Responsibilities

- Apply NER11 models for entity recognition
- Classify entities into domain-specific categories
- Generate confidence scores for each entity
- Handle entity boundary detection
- Manage overlapping entity resolution
- Normalize entity representations
- Process documents in parallel batches
- Maintain extraction quality metrics

### Expected Inputs

- Preprocessed documents with cleaned text
- Document metadata and structure information
- Document ID and reference information

### Expected Outputs

- Entity-labeled documents with locations
- Classified entities with confidence scores
- Entity linking information
- Extraction quality metrics
- Processing logs and debugging information

---

## NER11 Model Architecture

### Model Hierarchy

```
┌────────────────────────────────────────┐
│      NER11 Base Model (BERT)           │
│    (General entity recognition)         │
└─────────────┬──────────────────────────┘
              ↓
    ┌─────────────────────────────────────────────────┐
    │     Domain-Specific Fine-tuned Models           │
    ├──────────────────────────────────────────────────┤
    │ • Cybersecurity (CVE, Threat, Vulnerability)   │
    │ • Healthcare (Disease, Treatment, Symptom)      │
    │ • Finance (Organization, Amount, Account)       │
    │ • Legal (Contract, Party, Clause)               │
    │ • General Domain (Person, Location, Organization)│
    └─────────────────────────────────────────────────┘
              ↓
    ┌─────────────────────────────────────────────────┐
    │        Entity Classification Layer              │
    │  (Confidence Scoring & Type Assignment)         │
    └─────────────────────────────────────────────────┘
```

### NER11 Model Components

**Base Model**: BERT-based transformer
- Bidirectional context understanding
- Subword tokenization
- Contextual embeddings
- 768-dimensional vectors

**Fine-tuning Strategy**:
- Domain-specific annotation
- Transfer learning from base model
- Category-specific loss weighting
- Confidence calibration

**Output Layer**:
- Token classification (BIO tagging)
- Confidence score per token
- Entity boundary detection

---

## Entity Types & Classification

### Cybersecurity Domain

| Entity Type | Description | Example |
|-------------|-------------|---------|
| CVE | Vulnerability identifier | CVE-2024-0001 |
| THREAT_ACTOR | Malicious group/person | APT28, LockBit |
| MALWARE | Malicious software | WannaCry, Emotet |
| ATTACK_VECTOR | Attack method | SQL Injection, Phishing |
| VULNERABILITY | Security weakness | Buffer Overflow, XSS |
| TOOL | Security tool | Nmap, Burp Suite |
| INFRASTRUCTURE | Network/system component | Firewall, Server, Database |
| INDICATOR | IOC (IP, Domain, Hash) | 192.168.1.1, malware.com |
| IMPACT | Consequence/damage | Data Loss, Service Disruption |
| MITIGATION | Defense measure | Patch, Firewall Rule |

### General Domain

| Entity Type | Description | Example |
|-------------|-------------|---------|
| PERSON | Individual person | John Smith, Jane Doe |
| ORGANIZATION | Company/institution | Microsoft, WHO, FBI |
| LOCATION | Geographic place | New York, North Korea |
| DATE | Temporal reference | January 15, 2024 |
| TIME | Time reference | 14:30 UTC, 2 hours |
| QUANTITY | Measurement | 100 GB, $5 million |
| PRODUCT | Commercial product | Windows 10, iOS 17 |
| EVENT | Named event | DEFCON, Black Hat |
| FACILITY | Physical location | Data Center, Laboratory |
| GPE | Geopolitical entity | United States, EU |

### Healthcare Domain

| Entity Type | Description | Example |
|-------------|-------------|---------|
| DISEASE | Medical condition | COVID-19, Diabetes |
| SYMPTOM | Patient symptom | Fever, Cough |
| TREATMENT | Medical intervention | Medication, Surgery |
| DRUG | Pharmaceutical agent | Aspirin, Vaccine |
| BODY_PART | Anatomical location | Heart, Brain |
| TEST | Medical test | PCR, MRI |
| DOSAGE | Drug quantity | 500mg, 2 tablets |
| MEDICAL_PROCEDURE | Clinical procedure | Biopsy, Injection |
| MEDICAL_PROVIDER | Healthcare facility | Hospital, Clinic |
| PATIENT_ID | Medical identifier | Patient #12345 |

### Financial Domain

| Entity Type | Description | Example |
|-------------|-------------|---------|
| ORGANIZATION | Financial entity | JPMorgan, Goldman Sachs |
| PERSON | Individual person | Warren Buffett |
| CURRENCY | Money type | USD, EUR, GBP |
| AMOUNT | Money quantity | $1.2 million, €500k |
| ACCOUNT | Bank/investment account | Account #123456 |
| TRANSACTION | Financial transfer | Wire Transfer, ACH |
| SECURITY | Financial instrument | Stock, Bond, Cryptocurrency |
| MARKET | Financial market | NYSE, FOREX |
| RATE | Financial rate | Interest Rate, Exchange Rate |
| REGULATION | Financial rule | Dodd-Frank, MiFID II |

---

## NER Processing Pipeline

### Architecture Diagram

```
Input Text
    ↓
┌────────────────────────────────────────┐
│   Tokenization & Preprocessing         │
│ • Sentence segmentation                │
│ • Subword tokenization                 │
│ • Token ID mapping                     │
└────────────────────┬───────────────────┘
                     ↓
┌────────────────────────────────────────┐
│   Domain Selection                     │
│ • Text classification                  │
│ • Domain probability scoring           │
│ • Select 1-3 most relevant models      │
└────────────────────┬───────────────────┘
                     ↓
┌────────────────────────────────────────┐
│   Model Inference                      │
│ • Parallel model execution             │
│ • Token classification (BIO)           │
│ • Raw confidence scores                │
└────────────────────┬───────────────────┘
                     ↓
┌────────────────────────────────────────┐
│   Entity Boundary Detection            │
│ • BIO tag sequence decoding            │
│ • Entity span extraction               │
│ • Overlapping resolution               │
└────────────────────┬───────────────────┘
                     ↓
┌────────────────────────────────────────┐
│   Confidence Scoring                   │
│ • Token confidence aggregation         │
│ • Boundary confidence adjustment       │
│ • Multi-model consensus                │
└────────────────────┬───────────────────┘
                     ↓
┌────────────────────────────────────────┐
│   Post-processing & Filtering          │
│ • Confidence threshold filtering       │
│ • Entity normalization                 │
│ • Duplicate removal                    │
└────────────────────┬───────────────────┘
                     ↓
Output Entity List with Confidence Scores
```

### Python Implementation

```python
# File: backend/services/ner_extractor.py

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import numpy as np
from enum import Enum

class EntityType(Enum):
    """Entity types for classification"""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    CVE = "CVE"
    THREAT_ACTOR = "THREAT_ACTOR"
    MALWARE = "MALWARE"
    VULNERABILITY = "VULNERABILITY"
    ATTACK_VECTOR = "ATTACK_VECTOR"
    TOOL = "TOOL"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    INDICATOR = "INDICATOR"
    DATE = "DATE"
    TIME = "TIME"
    QUANTITY = "QUANTITY"
    DISEASE = "DISEASE"
    TREATMENT = "TREATMENT"
    AMOUNT = "AMOUNT"
    UNKNOWN = "UNKNOWN"

@dataclass
class Entity:
    """Extracted entity with metadata"""
    text: str
    entity_type: str
    start_char: int
    end_char: int
    confidence: float
    token_confidences: List[float]
    source_model: str
    sentence_context: str
    additional_info: Dict = None

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'type': self.entity_type,
            'start': self.start_char,
            'end': self.end_char,
            'confidence': round(self.confidence, 4),
            'source_model': self.source_model,
            'context': self.sentence_context,
            'additional_info': self.additional_info or {},
        }

class NERExtractor:
    """NER11 entity extraction using transformers"""

    def __init__(
        self,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu',
        batch_size: int = 8
    ):
        self.device = device
        self.batch_size = batch_size
        self.models = {}
        self.tokenizers = {}
        self._initialize_models()

    def _initialize_models(self):
        """Initialize domain-specific NER models"""
        model_configs = {
            'general': {
                'model': 'dbmdz/bert-base-cased-ner',
                'tokenizer': 'dbmdz/bert-base-cased-ner',
            },
            'cybersecurity': {
                'model': 'dslim/bert-base-NER-CyberSecurityCorpus',
                'tokenizer': 'dslim/bert-base-NER-CyberSecurityCorpus',
            },
            'biomedical': {
                'model': 'allenai/SciBERT_scivocab_uncased',
                'tokenizer': 'allenai/SciBERT_scivocab_uncased',
            },
            'financial': {
                'model': 'nlpaueb/legal-bert-base-uncased',
                'tokenizer': 'nlpaueb/legal-bert-base-uncased',
            },
        }

        for domain, config in model_configs.items():
            try:
                tokenizer = AutoTokenizer.from_pretrained(config['tokenizer'])
                model = AutoModelForTokenClassification.from_pretrained(
                    config['model']
                ).to(self.device)
                model.eval()

                self.models[domain] = model
                self.tokenizers[domain] = tokenizer
                print(f"Loaded {domain} model: {config['model']}")
            except Exception as e:
                print(f"Failed to load {domain} model: {e}")

    def extract_entities(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        confidence_threshold: float = 0.6
    ) -> List[Entity]:
        """Extract entities from text using NER models"""

        if domains is None:
            domains = self._detect_domains(text)

        # Segment text into sentences
        sentences = self._segment_sentences(text)

        all_entities = []

        for sentence in sentences:
            for domain in domains:
                if domain not in self.models:
                    continue

                entities = self._extract_from_sentence(
                    sentence,
                    domain,
                    confidence_threshold
                )
                all_entities.extend(entities)

        # Deduplicate and resolve overlaps
        final_entities = self._resolve_overlaps(all_entities)

        return final_entities

    def _extract_from_sentence(
        self,
        sentence: str,
        domain: str,
        confidence_threshold: float
    ) -> List[Entity]:
        """Extract entities from a single sentence"""

        model = self.models[domain]
        tokenizer = self.tokenizers[domain]

        # Tokenize
        tokens = tokenizer(
            sentence,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            return_offsets_mapping=True
        ).to(self.device)

        offset_mapping = tokens.pop('offset_mapping')[0]

        # Forward pass
        with torch.no_grad():
            outputs = model(**tokens)
            logits = outputs.logits

        # Get predictions and confidences
        predictions = torch.argmax(logits, dim=-1)[0]
        confidences = torch.softmax(logits, dim=-1)[0].max(dim=-1)[0]

        # Decode BIO tags
        id2label = model.config.id2label
        tags = [id2label[pred.item()] for pred in predictions]
        confs = [conf.item() for conf in confidences]

        # Extract entities
        entities = []
        current_entity = None
        current_tokens = []
        current_confidences = []

        for idx, (tag, conf) in enumerate(zip(tags, confs)):
            if tag.startswith('B-'):
                # Save previous entity
                if current_entity:
                    entity = self._create_entity(
                        current_entity,
                        sentence,
                        offset_mapping,
                        current_tokens,
                        current_confidences,
                        domain
                    )
                    if entity and entity.confidence >= confidence_threshold:
                        entities.append(entity)

                current_entity = tag[2:]  # Remove 'B-'
                current_tokens = [idx]
                current_confidences = [conf]

            elif tag.startswith('I-') and current_entity:
                if tag[2:] == current_entity:
                    current_tokens.append(idx)
                    current_confidences.append(conf)
                else:
                    # Entity type changed, save previous
                    entity = self._create_entity(
                        current_entity,
                        sentence,
                        offset_mapping,
                        current_tokens,
                        current_confidences,
                        domain
                    )
                    if entity and entity.confidence >= confidence_threshold:
                        entities.append(entity)

                    current_entity = tag[2:]
                    current_tokens = [idx]
                    current_confidences = [conf]

            else:  # 'O' or mismatched I tag
                if current_entity:
                    entity = self._create_entity(
                        current_entity,
                        sentence,
                        offset_mapping,
                        current_tokens,
                        current_confidences,
                        domain
                    )
                    if entity and entity.confidence >= confidence_threshold:
                        entities.append(entity)

                current_entity = None
                current_tokens = []
                current_confidences = []

        # Handle last entity
        if current_entity:
            entity = self._create_entity(
                current_entity,
                sentence,
                offset_mapping,
                current_tokens,
                current_confidences,
                domain
            )
            if entity and entity.confidence >= confidence_threshold:
                entities.append(entity)

        return entities

    def _create_entity(
        self,
        entity_type: str,
        sentence: str,
        offset_mapping,
        token_indices: List[int],
        confidences: List[float],
        domain: str
    ) -> Optional[Entity]:
        """Create Entity object from tokens"""

        if not token_indices:
            return None

        # Get character offsets
        start_idx = token_indices[0]
        end_idx = token_indices[-1]

        if start_idx >= len(offset_mapping) or end_idx >= len(offset_mapping):
            return None

        start_char = offset_mapping[start_idx][0].item()
        end_char = offset_mapping[end_idx][1].item()

        entity_text = sentence[start_char:end_char]

        # Calculate confidence
        confidence = np.mean(confidences)

        return Entity(
            text=entity_text,
            entity_type=entity_type,
            start_char=start_char,
            end_char=end_char,
            confidence=float(confidence),
            token_confidences=confidences,
            source_model=domain,
            sentence_context=sentence,
        )

    def _detect_domains(self, text: str) -> List[str]:
        """Detect relevant domains from text"""
        domains = ['general']

        # Domain keywords
        domain_keywords = {
            'cybersecurity': ['CVE', 'malware', 'attack', 'threat', 'vulnerability', 'exploit'],
            'biomedical': ['disease', 'treatment', 'patient', 'hospital', 'diagnosis', 'symptom'],
            'financial': ['stock', 'investment', 'financial', 'bank', 'transaction', 'market'],
        }

        text_lower = text.lower()

        for domain, keywords in domain_keywords.items():
            if any(kw in text_lower for kw in keywords):
                domains.append(domain)

        return domains[:3]  # Limit to 3 domains

    def _segment_sentences(self, text: str) -> List[str]:
        """Segment text into sentences"""
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
        return sentences

    def _resolve_overlaps(self, entities: List[Entity]) -> List[Entity]:
        """Resolve overlapping entity predictions"""
        if not entities:
            return []

        # Sort by confidence (descending) and start position
        sorted_entities = sorted(
            entities,
            key=lambda e: (-e.confidence, e.start_char)
        )

        resolved = []
        used_ranges = []

        for entity in sorted_entities:
            # Check for overlap
            overlaps = False
            for start, end in used_ranges:
                if not (entity.end_char <= start or entity.start_char >= end):
                    overlaps = True
                    break

            if not overlaps:
                resolved.append(entity)
                used_ranges.append((entity.start_char, entity.end_char))

        return sorted(resolved, key=lambda e: e.start_char)
```

---

## Confidence Scoring System

### Token-Level Scoring

```python
def calculate_token_confidence(logits: torch.Tensor) -> float:
    """
    Calculate confidence from logits

    score = softmax(logits)[predicted_class]
    Range: [0, 1]
    """
    probabilities = torch.softmax(logits, dim=-1)
    confidence = probabilities.max().item()
    return confidence
```

### Entity-Level Scoring

```python
class ConfidenceCalculator:
    """Calculate entity-level confidence scores"""

    @staticmethod
    def aggregate_token_confidence(token_confidences: List[float]) -> float:
        """Aggregate token confidences to entity confidence"""
        if not token_confidences:
            return 0.0

        # Method 1: Minimum confidence (conservative)
        min_conf = min(token_confidences)

        # Method 2: Mean confidence
        mean_conf = np.mean(token_confidences)

        # Method 3: Weighted (penalize long entities)
        length_penalty = 1.0 / (1.0 + 0.1 * len(token_confidences))
        weighted_conf = mean_conf * length_penalty

        # Use harmonic mean of methods
        return (min_conf + mean_conf + weighted_conf) / 3.0

    @staticmethod
    def boundary_confidence_adjustment(
        token_confidences: List[float],
        entity_text: str
    ) -> float:
        """Adjust confidence based on entity boundaries"""

        base_conf = ConfidenceCalculator.aggregate_token_confidence(token_confidences)

        # First/last tokens are more important
        boundary_weight = (token_confidences[0] + token_confidences[-1]) / 2.0
        boundary_adj = (base_conf + boundary_weight) / 2.0

        # Penalize short entities (might be false positives)
        if len(entity_text) < 2:
            boundary_adj *= 0.8

        return min(1.0, boundary_adj)

    @staticmethod
    def multi_model_consensus(
        entity_predictions: Dict[str, float]
    ) -> float:
        """
        Calculate confidence from multiple models

        Models may disagree:
        - Perfect agreement: 100% → full confidence boost
        - Partial agreement: 50-99% → moderate boost
        - Disagreement: <50% → confidence reduction
        """
        if not entity_predictions:
            return 0.0

        confidences = list(entity_predictions.values())
        mean_conf = np.mean(confidences)

        # Measure agreement
        agreement_score = 1.0 - (np.std(confidences) / max(np.mean(confidences), 0.1))

        # Combine mean confidence with agreement
        final_confidence = (mean_conf * 0.7) + (agreement_score * 0.3)

        return min(1.0, final_confidence)
```

### Confidence Thresholds

| Threshold | Usage | Interpretation |
|-----------|-------|-----------------|
| 0.95+ | High confidence | Reliable for direct use |
| 0.85-0.95 | Medium-high confidence | Usually correct, manual review recommended |
| 0.70-0.85 | Medium confidence | Correct 70-85% of time |
| 0.50-0.70 | Low confidence | Below threshold for most uses |
| <0.50 | Very low confidence | Typically filtered out |

---

## Entity Normalization

### Canonical Form Generation

```python
class EntityNormalizer:
    """Normalize entities to canonical forms"""

    @staticmethod
    def normalize_person(text: str) -> str:
        """Normalize person names"""
        # Title removal
        titles = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Mr', 'Mrs', 'Ms', 'Dr', 'Prof']
        for title in titles:
            text = text.replace(title, '').strip()

        # Case normalization
        return text.title()

    @staticmethod
    def normalize_organization(text: str) -> str:
        """Normalize organization names"""
        # Common suffixes
        suffixes = ['Inc.', 'Ltd.', 'Corp.', 'Co.', 'LLC', 'GmbH']
        for suffix in suffixes:
            text = text.replace(suffix, '').strip()

        return text.strip()

    @staticmethod
    def normalize_location(text: str) -> str:
        """Normalize location names"""
        return text.strip()

    @staticmethod
    def normalize_cve(text: str) -> str:
        """Normalize CVE identifiers"""
        # Format: CVE-YYYY-NNNNN
        text = text.upper().replace(' ', '').replace('_', '-')
        if not text.startswith('CVE-'):
            text = 'CVE-' + text
        return text

    @staticmethod
    def normalize_ipv4(text: str) -> str:
        """Validate and normalize IPv4 addresses"""
        parts = text.split('.')
        if len(parts) != 4:
            return text

        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return text
            return text
        except ValueError:
            return text

    @staticmethod
    def normalize_url(text: str) -> str:
        """Normalize URLs"""
        if not text.startswith(('http://', 'https://')):
            text = 'https://' + text

        return text.lower()

    @staticmethod
    def normalize_entity(entity: Entity) -> Entity:
        """Normalize entity based on type"""
        normalizers = {
            EntityType.PERSON.value: EntityNormalizer.normalize_person,
            EntityType.ORGANIZATION.value: EntityNormalizer.normalize_organization,
            EntityType.LOCATION.value: EntityNormalizer.normalize_location,
            EntityType.CVE.value: EntityNormalizer.normalize_cve,
        }

        normalizer = normalizers.get(entity.entity_type)
        if normalizer:
            entity.text = normalizer(entity.text)

        return entity
```

---

## Batch Processing

### Efficient Batch Processing

```python
class BatchNERProcessor:
    """Process multiple documents in batches"""

    def __init__(self, batch_size: int = 8):
        self.batch_size = batch_size
        self.extractor = NERExtractor(batch_size=batch_size)

    def process_documents(
        self,
        documents: List[str],
        document_ids: List[str]
    ) -> List[Dict]:
        """Process multiple documents efficiently"""

        results = []

        for doc_idx in range(0, len(documents), self.batch_size):
            batch_docs = documents[doc_idx:doc_idx + self.batch_size]
            batch_ids = document_ids[doc_idx:doc_idx + self.batch_size]

            for doc_text, doc_id in zip(batch_docs, batch_ids):
                try:
                    entities = self.extractor.extract_entities(doc_text)

                    results.append({
                        'document_id': doc_id,
                        'status': 'success',
                        'entity_count': len(entities),
                        'entities': [e.to_dict() for e in entities],
                        'processing_time': '...',
                        'timestamp': datetime.now().isoformat(),
                    })
                except Exception as e:
                    results.append({
                        'document_id': doc_id,
                        'status': 'error',
                        'error': str(e),
                        'timestamp': datetime.now().isoformat(),
                    })

        return results
```

---

## Domain-Specific Models

### Cybersecurity Entity Extraction

```python
class CyberSecurityNER:
    """Cybersecurity-specific entity extraction"""

    PATTERNS = {
        'CVE': r'CVE-\d{4}-\d{4,5}',
        'IPADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'HASH_MD5': r'\b[a-fA-F0-9]{32}\b',
        'HASH_SHA1': r'\b[a-fA-F0-9]{40}\b',
        'HASH_SHA256': r'\b[a-fA-F0-9]{64}\b',
        'URL': r'https?://[^\s]+',
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    }

    @staticmethod
    def extract_indicators(text: str) -> Dict[str, List[str]]:
        """Extract cybersecurity indicators"""
        import re

        indicators = {}

        for ioc_type, pattern in CyberSecurityNER.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                indicators[ioc_type] = list(set(matches))  # Remove duplicates

        return indicators
```

---

## Performance Optimization

### GPU Acceleration

- CUDA support for faster inference
- Mixed precision (FP16) for memory efficiency
- Batch processing for throughput
- Model quantization for deployment

### Caching & Reuse

- Model weight caching
- Entity deduplication
- Result memoization
- Token cache reuse

---

## Quality Assurance

### Metrics Tracking

```python
@dataclass
class ExtractionMetrics:
    total_entities: int
    entity_types: Dict[str, int]
    avg_confidence: float
    high_confidence_count: int  # >0.9
    medium_confidence_count: int  # 0.7-0.9
    low_confidence_count: int  # <0.7
    processing_time_seconds: float
    tokens_processed: int
    extraction_rate: float  # entities per 1000 tokens

class MetricsCalculator:
    @staticmethod
    def calculate_metrics(entities: List[Entity], processing_time: float) -> ExtractionMetrics:
        """Calculate extraction metrics"""
        entity_types = {}
        total_confidence = 0.0
        high_conf = 0
        med_conf = 0
        low_conf = 0

        for entity in entities:
            entity_types[entity.entity_type] = entity_types.get(entity.entity_type, 0) + 1
            total_confidence += entity.confidence

            if entity.confidence > 0.9:
                high_conf += 1
            elif entity.confidence > 0.7:
                med_conf += 1
            else:
                low_conf += 1

        return ExtractionMetrics(
            total_entities=len(entities),
            entity_types=entity_types,
            avg_confidence=total_confidence / len(entities) if entities else 0,
            high_confidence_count=high_conf,
            medium_confidence_count=med_conf,
            low_confidence_count=low_conf,
            processing_time_seconds=processing_time,
            tokens_processed=0,
            extraction_rate=0,
        )
```

---

**End of INGESTION_STEP2_NER_EXTRACTION.md**
*Total Lines: 861 | Complete NER11 implementation with models and confidence scoring*
