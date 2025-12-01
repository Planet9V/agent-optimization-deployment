# NER Enhancement Roadmap
**File**: NER_ENHANCEMENT_ROADMAP.md
**Created**: 2025-11-05
**Author**: NER Enhancement Specialist
**Purpose**: Comprehensive strategy to improve entity extraction from 29% to 80%+ accuracy
**Status**: ACTIVE

## Executive Summary

**Current State**: Pattern-Neural Hybrid NER system with 29% entity classification accuracy
- 202 patterns across 8 entity types (industrial domain)
- 28 relationship patterns across 8 relationship types
- spaCy 3.8.7 with en_core_web_lg v3.8.0 neural baseline
- Pattern-based NER currently DISABLED (critical issue)

**Target State**: 80%+ entity classification accuracy with multi-domain support
- Cybersecurity + Industrial patterns (500+ patterns)
- Multi-label classification (entities can have multiple types)
- Context-aware extraction (sector-specific patterns)
- Trained spaCy NER models for domain-specific entities

**Gap Analysis**: 51% improvement needed
- Root cause: Pattern NER disabled, neural model not domain-specific
- Impact: Misclassifying PROTOCOL → ORG, COMPONENT → ORG, etc.

---

## Current System Analysis

### Architecture (agents/ner_agent.py)

```python
class NERAgent(BaseAgent):
    ENTITY_TYPES = [
        # Industrial (original 8 types)
        "VENDOR", "PROTOCOL", "STANDARD", "COMPONENT",
        "MEASUREMENT", "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER",

        # Cybersecurity (added 2025-11-04, 9 types)
        "CVE", "CWE", "CAPEC", "THREAT_ACTOR", "CAMPAIGN",
        "ATTACK_TECHNIQUE", "MALWARE", "IOC", "APT_GROUP"
    ]
```

**Total Entity Types**: 17 (8 industrial + 9 cybersecurity)

### Pattern Library Analysis

**Industrial Patterns** (202 total):
- VENDOR: 8 patterns (Siemens, Rockwell, ABB, Schneider, Honeywell, Emerson, Yokogawa, GE Digital)
- PROTOCOL: 8 patterns (Modbus, OPC UA, Profinet, EtherCAT, HART, Foundation Fieldbus, DeviceNet, BACnet)
- STANDARD: 5 regex patterns (IEC, IEEE, ISO, ANSI, NFPA)
- COMPONENT: 10 patterns (PLC, HMI, RTU, SCADA, transmitter, actuator, sensor, controller, VFD)
- MEASUREMENT: 6 regex patterns (PSI, GPM, °C/°F, kW, HP, bar)
- SAFETY_CLASS: 3 patterns (SIL 0-4, ASIL A-D, CAT 1-4)
- SYSTEM_LAYER: 9 patterns (L0-L5, field/control/supervisory/enterprise levels)

**Cybersecurity Patterns** (100 total):
- CVE: 1 regex pattern (CVE-YYYY-NNNN)
- CWE: 1 regex pattern (CWE-NNN)
- CAPEC: 1 regex pattern (CAPEC-NNN)
- ATTACK_TECHNIQUE: 1 regex pattern (T1234.123)
- APT_GROUP: 2 patterns (APT\d+)
- THREAT_ACTOR: 7 patterns (Lazarus Group, Fancy Bear, Cozy Bear, etc.)
- MALWARE: 10 patterns (WannaCry, NotPetya, Stuxnet, Triton, etc.)
- IOC: 4 regex patterns (IPv4, MD5, SHA1, SHA256)

**Total Patterns**: 202 patterns across 17 entity types

### Relationship Extraction Patterns

**8 Relationship Types** (28 total patterns):
1. **EXPLOITS**: 4 patterns (THREAT_ACTOR/MALWARE → CVE)
2. **MITIGATES**: 3 patterns (COMPONENT/STANDARD/VENDOR → CVE)
3. **TARGETS**: 3 patterns (THREAT_ACTOR/MALWARE → VENDOR/COMPONENT)
4. **USES_TTP**: 3 patterns (THREAT_ACTOR/MALWARE → ATTACK_TECHNIQUE)
5. **ATTRIBUTED_TO**: 3 patterns (MALWARE/CAMPAIGN → THREAT_ACTOR/APT_GROUP)
6. **AFFECTS**: 3 patterns (CVE/MALWARE → VENDOR/COMPONENT)
7. **CONTAINS**: 2 patterns (COMPONENT → PROTOCOL)
8. **IMPLEMENTS**: 2 patterns (VENDOR/COMPONENT → PROTOCOL/STANDARD)

### Current Performance Issues

**From E2E Validation Report (2025-11-05)**:

```
Input: "The Siemens S7-1500 PLC system controls ABB variable frequency drives
        through Profinet protocol..."

Extracted: 17 entities
Correctly classified: 5/17 (29%)
Misclassified: 12/17 (71%)
```

**Misclassification Examples**:
- "Profinet" (PROTOCOL) → ORGANIZATION ❌
- "OPC UA" (PROTOCOL) → ORGANIZATION ❌
- "PLC" (COMPONENT) → ORGANIZATION ❌
- "IEC" (STANDARD) → ORGANIZATION ❌
- "Foundation Fieldbus" (PROTOCOL) → ORGANIZATION ❌

**Root Causes**:
1. Pattern-based NER DISABLED (despite spaCy being available)
2. Neural model (en_core_web_lg) trained on general text, not industrial/cyber domains
3. EntityRuler not properly integrated
4. Pattern library not loaded for unknown/default sector

---

## Enhancement Strategy

### Phase 1: Quick Wins (Week 1) - Target: 60% Accuracy

#### 1.1 Fix Pattern-Based NER Integration (CRITICAL)

**Problem**: Pattern NER returns empty despite spaCy being available

```python
# Current issue (agents/ner_agent.py:256-259)
if not self.nlp or not self.entity_ruler:
    self.logger.warning("spaCy not available for pattern NER")
    return self._fallback_pattern_ner(text, patterns)
```

**Evidence from logs**:
```
2025-11-05 08:30:56,043 - NERAgent - WARNING - spaCy not available for pattern NER
```

**Solution**:
```python
def _setup(self):
    """Setup NER pipeline with patterns and neural model"""
    if SPACY_AVAILABLE:
        try:
            self.logger.info("Loading spaCy model: en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

            # FIX: Add entity_ruler AFTER ner, not before
            # This ensures patterns override neural predictions
            if "entity_ruler" not in self.nlp.pipe_names:
                self.entity_ruler = self.nlp.add_pipe(
                    "entity_ruler",
                    after="ner"  # Changed from "before"
                )
            else:
                self.entity_ruler = self.nlp.get_pipe("entity_ruler")

            self.logger.info(f"spaCy pipeline: {self.nlp.pipe_names}")
        except Exception as e:
            self.logger.error(f"Could not load spaCy model: {e}")
            self.nlp = None
```

**Expected Impact**: +20% accuracy (pattern matching will correctly identify PROTOCOL, COMPONENT, STANDARD)

#### 1.2 Create Default Pattern Library

**Problem**: No fallback when sector="unknown"

```
2025-11-05 08:30:56,041 - NERAgent - WARNING - Pattern file not found: pattern_library/unknown.json, using default
2025-11-05 08:30:56,043 - NERAgent - INFO - Loaded 0 patterns from unknown
```

**Solution**: Create `pattern_library/default.json` with all patterns

```python
def load_sector_patterns(self, sector_name: str) -> List[Dict[str, Any]]:
    """Load sector-specific patterns from pattern library"""
    pattern_file = self.pattern_library_path / f"{sector_name}.json"

    # FIX: Add default.json fallback
    if not pattern_file.exists():
        self.logger.warning(f"Pattern file not found: {pattern_file}")

        # Try default.json first
        default_file = self.pattern_library_path / "default.json"
        if default_file.exists():
            pattern_file = default_file
            self.logger.info("Using default.json pattern library")
        else:
            # Fall back to industrial.json
            pattern_file = self.pattern_library_path / "industrial.json"
            self.logger.info("Using industrial.json pattern library")
```

**Files to Create**:
- `pattern_library/default.json` - Combines industrial + cybersecurity patterns
- `pattern_library/cybersecurity.json` - Pure cybersecurity patterns
- `pattern_library/industrial.json` - Already exists, enhance with more vendors

**Expected Impact**: +15% accuracy (all patterns available regardless of classifier output)

#### 1.3 Expand Cybersecurity Entity Patterns

**Current Coverage**: Basic CVE/CWE/CAPEC patterns
**Enhancement**: Add 200+ cybersecurity patterns

**Pattern Additions**:

```json
{
  "cybersecurity": {
    "patterns": [
      // CVE patterns (enhanced)
      {"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]},
      {"label": "CVE", "pattern": [{"LOWER": "cve"}, {"TEXT": {"REGEX": "\\d{4}"}}]},

      // CWE patterns (enhanced)
      {"label": "CWE", "pattern": [{"TEXT": {"REGEX": "CWE-\\d+"}}]},
      {"label": "CWE", "pattern": [{"LOWER": "cwe"}, {"IS_DIGIT": true}]},

      // CAPEC patterns (enhanced)
      {"label": "CAPEC", "pattern": [{"TEXT": {"REGEX": "CAPEC-\\d+"}}]},

      // MITRE ATT&CK Techniques (expanded)
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"TEXT": {"REGEX": "T\\d{4}(\\.\\d{3})?"}}]},
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"LOWER": "initial"}, {"LOWER": "access"}]},
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"LOWER": "privilege"}, {"LOWER": "escalation"}]},
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"LOWER": "lateral"}, {"LOWER": "movement"}]},
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"LOWER": "command"}, {"LOWER": "and"}, {"LOWER": "control"}]},
      {"label": "ATTACK_TECHNIQUE", "pattern": [{"LOWER": "exfiltration"}]},

      // Threat Actors (50+ known groups)
      {"label": "THREAT_ACTOR", "pattern": [{"TEXT": {"REGEX": "APT\\s*\\d+"}}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "lazarus"}, {"LOWER": "group"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "fancy"}, {"LOWER": "bear"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "cozy"}, {"LOWER": "bear"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "sandworm"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "dragonfly"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "energetic"}, {"LOWER": "bear"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "winnti"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "turla"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "kimsuky"}]},
      {"label": "THREAT_ACTOR", "pattern": [{"LOWER": "mustang"}, {"LOWER": "panda"}]},

      // Malware families (100+ families)
      {"label": "MALWARE", "pattern": [{"LOWER": "wannacry"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "notpetya"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "stuxnet"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "triton"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "trisis"}]},  // Triton variant
      {"label": "MALWARE", "pattern": [{"LOWER": "industroyer"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "crashoverride"}]},  // Industroyer variant
      {"label": "MALWARE", "pattern": [{"LOWER": "blackenergy"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "havex"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "trickbot"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "emotet"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "ryuk"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "conti"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "lockbit"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "darkside"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "revil"}]},
      {"label": "MALWARE", "pattern": [{"LOWER": "sodinokibi"}]},

      // IOC patterns (enhanced)
      {"label": "IOC", "pattern": [{"TEXT": {"REGEX": "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b"}}]},
      {"label": "IOC", "pattern": [{"TEXT": {"REGEX": "\\b[a-fA-F0-9]{32}\\b"}}]},  // MD5
      {"label": "IOC", "pattern": [{"TEXT": {"REGEX": "\\b[a-fA-F0-9]{40}\\b"}}]},  // SHA1
      {"label": "IOC", "pattern": [{"TEXT": {"REGEX": "\\b[a-fA-F0-9]{64}\\b"}}]},  // SHA256
      {"label": "IOC", "pattern": [{"TEXT": {"REGEX": "[a-zA-Z0-9.-]+\\.(com|net|org|info|biz)\\b"}}]},  // Domains

      // Campaign names
      {"label": "CAMPAIGN", "pattern": [{"LOWER": "solarwinds"}]},
      {"label": "CAMPAIGN", "pattern": [{"LOWER": "supply"}, {"LOWER": "chain"}, {"LOWER": "attack"}]},
      {"label": "CAMPAIGN", "pattern": [{"LOWER": "operation"}, {"IS_ALPHA": true}]},

      // Vulnerability types (semantic patterns)
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "buffer"}, {"LOWER": "overflow"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "sql"}, {"LOWER": "injection"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "xss"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "csrf"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "rce"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "remote"}, {"LOWER": "code"}, {"LOWER": "execution"}]},
      {"label": "VULNERABILITY_TYPE", "pattern": [{"LOWER": "privilege"}, {"LOWER": "escalation"}]},
    ]
  }
}
```

**Expected Impact**: +10% accuracy (better cybersecurity entity coverage)

#### 1.4 Add Multi-Label Classification Support

**Problem**: One entity can have multiple valid types

Example: "CVE-2024-1234" is both:
- CVE (identifier)
- VULNERABILITY (semantic type)
- EXPLOIT (if being actively exploited)

**Solution**: Allow entities to have multiple labels

```python
def extract_entities(self, markdown_text: str, sector: str = "industrial") -> List[Dict[str, Any]]:
    """Enhanced extraction with multi-label support"""

    # ... existing extraction ...

    # Add multi-label classification
    entities = self._add_multi_labels(entities)

    return entities

def _add_multi_labels(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add additional labels based on context and patterns"""

    multi_label_rules = {
        # CVE is also a VULNERABILITY
        'CVE': ['VULNERABILITY', 'SECURITY_ISSUE'],

        # CWE is a weakness type
        'CWE': ['WEAKNESS', 'VULNERABILITY_TYPE'],

        # ATTACK_TECHNIQUE is also a TTP
        'ATTACK_TECHNIQUE': ['TTP', 'TACTIC'],

        # MALWARE is a THREAT
        'MALWARE': ['THREAT', 'SECURITY_THREAT'],

        # THREAT_ACTOR is also an ACTOR
        'THREAT_ACTOR': ['ACTOR', 'ADVERSARY'],
    }

    for entity in entities:
        primary_label = entity['label']
        if primary_label in multi_label_rules:
            entity['labels'] = [primary_label] + multi_label_rules[primary_label]
            entity['primary_label'] = primary_label
        else:
            entity['labels'] = [primary_label]
            entity['primary_label'] = primary_label

    return entities
```

**Expected Impact**: +5% accuracy (better semantic understanding)

**Phase 1 Total Expected Improvement**: +50% (from 29% to ~79%)

---

### Phase 2: Medium-Term Improvements (Weeks 2-4) - Target: 80-85% Accuracy

#### 2.1 Train Custom spaCy NER Model

**Problem**: en_core_web_lg trained on general text (news, web), not industrial/cyber domains

**Solution**: Train domain-specific NER model

**Training Data Requirements**:

**Minimum Dataset Size**:
- Industrial domain: 1,000 documents (500K tokens)
- Cybersecurity domain: 1,000 documents (500K tokens)
- Mixed domain: 500 documents (250K tokens)
- **Total**: 2,500 documents (~1.25M tokens)

**Data Quality Requirements**:
- Manual annotation by domain experts
- Inter-annotator agreement >80%
- Balanced entity type distribution
- Real-world documents (not synthetic)

**Data Sources**:
1. **Industrial**:
   - Technical specifications
   - Safety reports (IEC 61508, IEC 61511)
   - Vendor manuals (Siemens, Rockwell, ABB)
   - SCADA/ICS documentation

2. **Cybersecurity**:
   - CVE descriptions from NIST NVD
   - MITRE ATT&CK framework documentation
   - Threat intelligence reports
   - Incident response reports

3. **Existing Labeled Data**:
   - Use existing test files as seed data
   - Bootstrap with pattern-matched entities
   - Active learning to expand dataset

**Training Approach**:

```python
# 1. Convert pattern library to training data
import spacy
from spacy.training import Example

def convert_patterns_to_training_data(pattern_file: str) -> List[Example]:
    """Convert pattern matches to training examples"""

    nlp = spacy.blank("en")
    examples = []

    # Load documents and apply patterns
    for doc_text in load_documents():
        doc = nlp(doc_text)

        # Apply patterns to get gold annotations
        pattern_entities = apply_patterns(doc_text)

        # Create training example
        entities = [(e['start'], e['end'], e['label']) for e in pattern_entities]
        example = Example.from_dict(doc, {"entities": entities})
        examples.append(example)

    return examples

# 2. Train custom NER model
def train_custom_ner_model(training_data: List[Example], output_dir: str):
    """Train spaCy NER model on domain-specific data"""

    # Initialize blank model
    nlp = spacy.blank("en")

    # Add NER component
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # Add entity labels
    for label in ENTITY_TYPES:
        ner.add_label(label)

    # Training configuration
    config = {
        "n_iter": 30,
        "batch_size": 32,
        "drop": 0.2,
        "learn_rate": 0.001
    }

    # Train model
    nlp.begin_training()
    for i in range(config["n_iter"]):
        losses = {}
        batches = spacy.util.minibatch(training_data, size=config["batch_size"])

        for batch in batches:
            nlp.update(batch, drop=config["drop"], losses=losses)

        print(f"Iteration {i}: {losses}")

    # Save model
    nlp.to_disk(output_dir)
    return nlp
```

**Evaluation Strategy**:

```python
def evaluate_ner_model(nlp, test_data: List[Example]) -> Dict[str, float]:
    """Evaluate NER model performance"""

    from spacy.scorer import Scorer

    scorer = Scorer()
    examples = []

    for example in test_data:
        pred = nlp(example.reference.text)
        examples.append(Example(pred, example.reference))

    scores = scorer.score(examples)

    return {
        'precision': scores['ents_p'],
        'recall': scores['ents_r'],
        'f1': scores['ents_f'],
        'per_type': scores['ents_per_type']
    }
```

**Expected Impact**: +5-10% accuracy (domain-specific neural NER)

#### 2.2 Context-Aware Pattern Matching

**Problem**: Some patterns are ambiguous without context

Example: "PLC" could be:
- COMPONENT (Programmable Logic Controller)
- ORGANIZATION (Public Limited Company)

**Solution**: Add context rules to patterns

```python
def apply_context_aware_patterns(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply context rules to disambiguate entities"""

    context_rules = {
        'PLC': {
            'COMPONENT_context': ['control', 'automation', 'siemens', 'rockwell', 'modbus'],
            'ORGANIZATION_context': ['company', 'limited', 'incorporated', 'corporate']
        },
        'IEC': {
            'STANDARD_context': ['61508', '61511', '62443', 'safety', 'compliance'],
            'ORGANIZATION_context': ['commission', 'electrotechnical']
        }
    }

    enhanced_entities = []

    for entity in entities:
        text_snippet = entity['text']

        # Get surrounding context (50 chars before/after)
        start = max(0, entity['start'] - 50)
        end = min(len(text), entity['end'] + 50)
        context = text[start:end].lower()

        # Check if entity needs disambiguation
        if text_snippet in context_rules:
            rules = context_rules[text_snippet]

            # Score each possible label based on context
            label_scores = {}
            for potential_label, keywords in rules.items():
                label = potential_label.split('_')[0]
                score = sum(1 for kw in keywords if kw in context)
                label_scores[label] = score

            # Use label with highest context score
            if label_scores:
                best_label = max(label_scores, key=label_scores.get)
                if label_scores[best_label] > 0:
                    entity['label'] = best_label
                    entity['context_score'] = label_scores[best_label]

        enhanced_entities.append(entity)

    return enhanced_entities
```

**Expected Impact**: +3-5% accuracy (better disambiguation)

#### 2.3 Active Learning Pipeline

**Problem**: Manual annotation is expensive and slow

**Solution**: Use active learning to prioritize annotation efforts

```python
class ActiveLearningPipeline:
    """Active learning for continuous NER improvement"""

    def __init__(self, nlp, unlabeled_corpus):
        self.nlp = nlp
        self.unlabeled_corpus = unlabeled_corpus
        self.training_data = []

    def select_informative_examples(self, n: int = 100) -> List[str]:
        """Select most informative examples for annotation"""

        # Score examples by uncertainty
        scored_examples = []

        for text in self.unlabeled_corpus:
            doc = self.nlp(text)

            # Calculate uncertainty score
            uncertainty = 0
            for ent in doc.ents:
                # Low confidence entities are informative
                if hasattr(ent, 'confidence'):
                    uncertainty += (1 - ent.confidence)

            scored_examples.append((text, uncertainty))

        # Sort by uncertainty (highest first)
        scored_examples.sort(key=lambda x: x[1], reverse=True)

        # Return top N most uncertain examples
        return [text for text, score in scored_examples[:n]]

    def add_annotated_examples(self, annotated_examples: List[Example]):
        """Add newly annotated examples to training set"""
        self.training_data.extend(annotated_examples)

    def retrain_model(self):
        """Retrain model with expanded training set"""
        # ... training code from 2.1 ...
        pass
```

**Annotation Workflow**:
1. Run NER on unlabeled corpus
2. Select 100 most uncertain examples
3. Human annotator labels these examples
4. Add to training set
5. Retrain model
6. Repeat until target accuracy reached

**Expected Impact**: Reduces annotation effort by 50-70%

**Phase 2 Total Expected Improvement**: +8-15% (from ~79% to 87-94%)

---

### Phase 3: Advanced Enhancements (Weeks 5-8) - Target: 90%+ Accuracy

#### 3.1 Ensemble NER Model

**Approach**: Combine multiple NER models for better accuracy

```python
class EnsembleNER:
    """Ensemble of multiple NER models"""

    def __init__(self, models: List[spacy.Language]):
        self.models = models

    def predict(self, text: str) -> List[Dict[str, Any]]:
        """Combine predictions from all models"""

        all_predictions = []

        # Get predictions from each model
        for model in self.models:
            doc = model(text)
            predictions = [
                {
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': getattr(ent, 'confidence', 0.85)
                }
                for ent in doc.ents
            ]
            all_predictions.append(predictions)

        # Voting strategy: majority vote with confidence weighting
        merged = self._merge_predictions(all_predictions)

        return merged

    def _merge_predictions(self, all_predictions: List[List[Dict]]) -> List[Dict]:
        """Merge predictions using weighted voting"""

        # Group overlapping predictions
        prediction_groups = defaultdict(list)

        for model_preds in all_predictions:
            for pred in model_preds:
                key = (pred['start'], pred['end'])
                prediction_groups[key].append(pred)

        # Vote on label for each span
        merged = []
        for span, preds in prediction_groups.items():
            # Count votes weighted by confidence
            label_votes = defaultdict(float)
            for pred in preds:
                label_votes[pred['label']] += pred['confidence']

            # Select label with highest vote
            best_label = max(label_votes, key=label_votes.get)
            avg_confidence = label_votes[best_label] / len(preds)

            merged.append({
                'text': preds[0]['text'],
                'label': best_label,
                'start': span[0],
                'end': span[1],
                'confidence': avg_confidence,
                'source': 'ensemble'
            })

        return merged
```

**Models to Ensemble**:
1. Pattern-based NER (95%+ precision)
2. spaCy en_core_web_lg (general domain)
3. Custom trained industrial NER
4. Custom trained cybersecurity NER
5. Transformer-based NER (RoBERTa/BERT fine-tuned)

**Expected Impact**: +3-5% accuracy

#### 3.2 Entity Linking and Disambiguation

**Problem**: Same text can refer to different entities

Example: "Apache" could be:
- Apache Software Foundation (ORGANIZATION)
- Apache HTTP Server (COMPONENT)
- Apache Kafka (COMPONENT)

**Solution**: Entity linking to knowledge base

```python
class EntityLinker:
    """Link extracted entities to knowledge base"""

    def __init__(self, knowledge_base_path: str):
        self.kb = self._load_knowledge_base(knowledge_base_path)

    def _load_knowledge_base(self, path: str) -> Dict[str, List[Dict]]:
        """Load entity knowledge base (from Neo4j or JSON)"""
        # Load entity definitions with:
        # - Canonical name
        # - Aliases
        # - Entity type
        # - Context keywords
        # - Unique ID
        pass

    def link_entities(self, entities: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """Disambiguate and link entities to KB"""

        linked_entities = []

        for entity in entities:
            # Find candidate KB entries
            candidates = self._find_candidates(entity['text'])

            if not candidates:
                # No KB match, keep original
                entity['kb_id'] = None
                linked_entities.append(entity)
                continue

            # Get context around entity
            start = max(0, entity['start'] - 100)
            end = min(len(text), entity['end'] + 100)
            context = text[start:end]

            # Score candidates based on context
            best_candidate = self._score_candidates(candidates, context)

            # Link to KB
            entity['kb_id'] = best_candidate['id']
            entity['canonical_name'] = best_candidate['name']
            entity['kb_type'] = best_candidate['type']
            entity['linking_confidence'] = best_candidate['score']

            linked_entities.append(entity)

        return linked_entities

    def _score_candidates(self, candidates: List[Dict], context: str) -> Dict:
        """Score KB candidates based on context"""

        for candidate in candidates:
            score = 0

            # Check if context keywords are present
            for keyword in candidate.get('context_keywords', []):
                if keyword.lower() in context.lower():
                    score += 1

            # Prefer exact name matches
            if candidate['name'].lower() in context.lower():
                score += 2

            candidate['score'] = score

        # Return highest scoring candidate
        return max(candidates, key=lambda c: c['score'])
```

**Expected Impact**: +2-3% accuracy

#### 3.3 Relationship Pattern Enhancement

**Current**: 28 relationship patterns
**Target**: 100+ relationship patterns

**Additional Relationship Types**:

```python
ENHANCED_RELATIONSHIP_PATTERNS = {
    # Existing relationships (28)
    'EXPLOITS': [...],
    'MITIGATES': [...],
    'TARGETS': [...],
    'USES_TTP': [...],
    'ATTRIBUTED_TO': [...],
    'AFFECTS': [...],
    'CONTAINS': [...],
    'IMPLEMENTS': [...],

    # NEW: Cybersecurity relationships
    'REMEDIATES': [
        ('VENDOR', ['patch', 'fix', 'remediate', 'update'], 'CVE'),
        ('COMPONENT', ['update', 'upgrade', 'patch'], 'VULNERABILITY'),
    ],

    'DISCOVERS': [
        ('ORGANIZATION', ['discover', 'find', 'identify', 'detect'], 'CVE'),
        ('ORGANIZATION', ['disclose', 'report'], 'VULNERABILITY'),
    ],

    'PUBLISHES': [
        ('VENDOR', ['publish', 'release', 'issue'], 'STANDARD'),
        ('ORGANIZATION', ['publish', 'announce'], 'CVE'),
    ],

    'DEPENDS_ON': [
        ('COMPONENT', ['depend', 'require', 'need'], 'COMPONENT'),
        ('COMPONENT', ['use', 'rely on'], 'PROTOCOL'),
    ],

    'COMMUNICATES_VIA': [
        ('COMPONENT', ['communicate', 'connect', 'interface'], 'PROTOCOL'),
        ('SYSTEM_LAYER', ['communicate', 'exchange'], 'PROTOCOL'),
    ],

    # NEW: Industrial relationships
    'MONITORS': [
        ('COMPONENT', ['monitor', 'measure', 'sense'], 'MEASUREMENT'),
        ('COMPONENT', ['track', 'observe'], 'COMPONENT'),
    ],

    'CONTROLS': [
        ('COMPONENT', ['control', 'regulate', 'manage'], 'COMPONENT'),
        ('SYSTEM_LAYER', ['control', 'command'], 'SYSTEM_LAYER'),
    ],

    'MANUFACTURED_BY': [
        ('COMPONENT', ['manufactured', 'made', 'produced'], 'VENDOR'),
        ('COMPONENT', ['by', 'from'], 'VENDOR'),
    ],

    'COMPLIES_WITH': [
        ('COMPONENT', ['comply', 'meet', 'conform'], 'STANDARD'),
        ('SYSTEM_LAYER', ['comply', 'adhere'], 'STANDARD'),
    ],

    'CERTIFIED_FOR': [
        ('COMPONENT', ['certified', 'rated', 'approved'], 'SAFETY_CLASS'),
        ('VENDOR', ['certified', 'approved'], 'STANDARD'),
    ],

    # NEW: Temporal relationships
    'PRECEDES': [
        ('ATTACK_TECHNIQUE', ['before', 'precede', 'prior to'], 'ATTACK_TECHNIQUE'),
        ('CAMPAIGN', ['before', 'precede'], 'CAMPAIGN'),
    ],

    'FOLLOWS': [
        ('ATTACK_TECHNIQUE', ['after', 'follow', 'subsequent'], 'ATTACK_TECHNIQUE'),
        ('CVE', ['follow', 'after'], 'CVE'),
    ],

    # NEW: Similarity relationships
    'SIMILAR_TO': [
        ('MALWARE', ['similar', 'related', 'variant'], 'MALWARE'),
        ('CVE', ['similar', 'related'], 'CVE'),
    ],

    'BASED_ON': [
        ('MALWARE', ['based on', 'derived from', 'variant of'], 'MALWARE'),
        ('ATTACK_TECHNIQUE', ['based on', 'adapted from'], 'ATTACK_TECHNIQUE'),
    ],
}
```

**Total Relationship Patterns**: 100+ patterns across 20 relationship types

**Expected Impact**: Better knowledge graph connectivity

---

## Implementation Roadmap

### Week 1: Critical Fixes (Quick Wins)
```yaml
Day 1-2:
  - Fix EntityRuler integration (change "before" to "after")
  - Create default.json pattern library
  - Test pattern NER works correctly
  - Expected: 20% accuracy improvement

Day 3-4:
  - Add 200+ cybersecurity patterns
  - Expand industrial vendor patterns (20+ vendors)
  - Add context-aware disambiguation rules
  - Expected: 15% accuracy improvement

Day 5:
  - Implement multi-label classification
  - Create comprehensive test suite
  - Run end-to-end validation
  - Target: 60% accuracy
```

### Weeks 2-3: Model Training
```yaml
Week 2:
  - Collect and prepare training data (1,000+ documents)
  - Convert patterns to training examples
  - Set up spaCy training pipeline
  - Train initial custom NER model

Week 3:
  - Evaluate model on test set
  - Implement active learning pipeline
  - Annotate 500 most uncertain examples
  - Retrain model with expanded dataset
  - Target: 80% accuracy
```

### Weeks 4-6: Advanced Features
```yaml
Week 4:
  - Build ensemble NER system
  - Create entity knowledge base
  - Implement entity linking

Week 5-6:
  - Expand relationship patterns (100+ patterns)
  - Train relationship extraction model
  - Integrate with knowledge graph
  - Target: 85-90% accuracy
```

### Weeks 7-8: Production Hardening
```yaml
Week 7:
  - Performance optimization (batch processing)
  - Confidence calibration
  - Error analysis and fixing

Week 8:
  - Production deployment preparation
  - Monitoring and logging
  - Documentation and training
  - Final validation: 90%+ accuracy
```

---

## Training Data Requirements

### Data Collection Strategy

**Phase 1: Bootstrap (Week 1)**
- Use pattern-matched entities as seed data
- No manual annotation required
- Generate 10,000 training examples from 1,000 documents
- Quality: Medium (pattern precision 95%)

**Phase 2: Manual Annotation (Weeks 2-3)**
- Hire domain experts for annotation
- Tools: Prodigy, Label Studio, or Doccano
- Target: 2,500 manually annotated documents
- Cost estimate: $5,000-$10,000 (at $2-$4 per document)

**Phase 3: Active Learning (Weeks 4-6)**
- Use uncertainty sampling to select informative examples
- Reduces annotation effort by 50-70%
- Continuous improvement through user feedback

### Dataset Composition

```yaml
industrial_domain:
  total_documents: 1,000
  total_tokens: 500,000

  sources:
    - technical_specs: 400 documents
    - safety_reports: 200 documents
    - vendor_manuals: 300 documents
    - incident_reports: 100 documents

  entity_distribution:
    VENDOR: 5,000 instances
    PROTOCOL: 3,000 instances
    STANDARD: 2,000 instances
    COMPONENT: 8,000 instances
    MEASUREMENT: 4,000 instances
    SAFETY_CLASS: 1,500 instances
    SYSTEM_LAYER: 2,000 instances
    ORGANIZATION: 3,000 instances

cybersecurity_domain:
  total_documents: 1,000
  total_tokens: 500,000

  sources:
    - cve_descriptions: 500 documents (from NIST NVD)
    - threat_reports: 300 documents
    - mitre_attack: 150 documents
    - incident_reports: 50 documents

  entity_distribution:
    CVE: 8,000 instances
    CWE: 3,000 instances
    CAPEC: 1,000 instances
    THREAT_ACTOR: 2,000 instances
    MALWARE: 4,000 instances
    ATTACK_TECHNIQUE: 5,000 instances
    IOC: 6,000 instances
    APT_GROUP: 1,500 instances

mixed_domain:
  total_documents: 500
  total_tokens: 250,000

  sources:
    - ics_security_reports: 300 documents
    - vulnerability_assessments: 200 documents

  focus:
    - Cross-domain entity recognition
    - Multi-label classification
    - Contextual disambiguation
```

### Data Quality Standards

**Annotation Guidelines**:
1. **Consistency**: Inter-annotator agreement >80%
2. **Completeness**: Annotate ALL entities, even uncertain ones
3. **Boundaries**: Precise span boundaries (no extra spaces)
4. **Types**: Use primary label + additional labels for multi-label
5. **Context**: Include surrounding sentences for context

**Quality Assurance Process**:
1. Initial annotation by primary annotator
2. Review by second annotator
3. Conflict resolution by senior expert
4. Automated validation (span overlap, label consistency)
5. Periodic quality audits (every 100 documents)

---

## Target Accuracy Metrics

### Accuracy Targets by Phase

```yaml
baseline:
  entity_accuracy: 29%
  pattern_precision: 0%  # Currently disabled
  neural_recall: 85%
  f1_score: 0.44

phase_1_quick_wins:
  entity_accuracy: 60%
  pattern_precision: 95%
  neural_recall: 85%
  f1_score: 0.73

phase_2_model_training:
  entity_accuracy: 80%
  pattern_precision: 95%
  neural_recall: 90%
  f1_score: 0.85

phase_3_advanced:
  entity_accuracy: 90%
  pattern_precision: 96%
  neural_recall: 92%
  f1_score: 0.91
```

### Per-Entity-Type Targets

```yaml
industrial_entities:
  VENDOR:
    target_precision: 95%
    target_recall: 90%
    strategy: Pattern + neural ensemble

  PROTOCOL:
    target_precision: 95%
    target_recall: 92%
    strategy: Pattern-first, neural validation

  STANDARD:
    target_precision: 96%
    target_recall: 88%
    strategy: Regex patterns + context

  COMPONENT:
    target_precision: 90%
    target_recall: 85%
    strategy: Pattern + context-aware disambiguation

  MEASUREMENT:
    target_precision: 98%
    target_recall: 95%
    strategy: Regex patterns (high precision)

cybersecurity_entities:
  CVE:
    target_precision: 99%
    target_recall: 98%
    strategy: Regex pattern (CVE-YYYY-NNNN)

  CWE:
    target_precision: 98%
    target_recall: 95%
    strategy: Regex pattern (CWE-NNN)

  THREAT_ACTOR:
    target_precision: 92%
    target_recall: 85%
    strategy: Pattern library + neural

  MALWARE:
    target_precision: 93%
    target_recall: 88%
    strategy: Pattern library + context

  ATTACK_TECHNIQUE:
    target_precision: 95%
    target_recall: 90%
    strategy: Regex (T1234) + semantic patterns
```

---

## Validation and Testing

### Test Suite Structure

```python
# tests/test_ner_enhanced.py

class TestPatternNER:
    """Test pattern-based NER extraction"""

    def test_cybersecurity_patterns(self):
        """Test CVE, CWE, CAPEC extraction"""
        text = "CVE-2024-1234 is related to CWE-79 and CAPEC-66"

        agent = NERAgent({})
        result = agent.extract_entities(text, sector='cybersecurity')

        assert len(result) >= 3
        assert any(e['text'] == 'CVE-2024-1234' and e['label'] == 'CVE' for e in result)
        assert any(e['text'] == 'CWE-79' and e['label'] == 'CWE' for e in result)
        assert any(e['text'] == 'CAPEC-66' and e['label'] == 'CAPEC' for e in result)

    def test_industrial_patterns(self):
        """Test industrial entity extraction"""
        text = "Siemens S7-1500 PLC uses Profinet protocol"

        agent = NERAgent({})
        result = agent.extract_entities(text, sector='industrial')

        assert any(e['text'] == 'Siemens' and e['label'] == 'VENDOR' for e in result)
        assert any(e['text'] == 'PLC' and e['label'] == 'COMPONENT' for e in result)
        assert any(e['text'] == 'Profinet' and e['label'] == 'PROTOCOL' for e in result)

    def test_pattern_ner_enabled(self):
        """Verify pattern NER is actually running"""
        agent = NERAgent({})

        # EntityRuler should be in pipeline
        assert agent.nlp is not None
        assert agent.entity_ruler is not None
        assert 'entity_ruler' in agent.nlp.pipe_names

class TestContextAwareExtraction:
    """Test context-aware disambiguation"""

    def test_plc_disambiguation(self):
        """Test PLC context disambiguation"""

        # Industrial context
        text1 = "The Siemens S7-1500 PLC controls the process"
        agent = NERAgent({})
        result1 = agent.extract_entities(text1, sector='industrial')
        plc_entities = [e for e in result1 if e['text'] == 'PLC']
        assert len(plc_entities) > 0
        assert plc_entities[0]['label'] == 'COMPONENT'

        # Corporate context (rare, but possible)
        text2 = "ABC Technologies PLC announced quarterly earnings"
        result2 = agent.extract_entities(text2, sector='industrial')
        plc_entities2 = [e for e in result2 if e['text'] == 'PLC']
        # Should either be ORGANIZATION or have low confidence
        if plc_entities2:
            assert plc_entities2[0]['label'] in ['ORGANIZATION', 'COMPONENT']

class TestMultiLabelClassification:
    """Test multi-label entity classification"""

    def test_cve_multi_labels(self):
        """CVE should have multiple labels"""
        text = "CVE-2024-1234 is a critical vulnerability"

        agent = NERAgent({})
        result = agent.extract_entities(text, sector='cybersecurity')

        cve_entities = [e for e in result if 'CVE-2024-1234' in e['text']]
        assert len(cve_entities) > 0

        cve = cve_entities[0]
        assert 'labels' in cve
        assert 'CVE' in cve['labels']
        assert 'VULNERABILITY' in cve['labels']

class TestAccuracyBenchmarks:
    """Test against accuracy targets"""

    def test_phase1_accuracy_target(self):
        """Test Phase 1 target: 60% accuracy"""

        # Use validation dataset with known entities
        validation_data = load_validation_dataset()

        agent = NERAgent({})
        total_correct = 0
        total_entities = 0

        for doc in validation_data:
            result = agent.extract_entities(doc['text'], doc['sector'])

            # Compare with gold standard
            correct = count_correct_entities(result['entities'], doc['gold_entities'])
            total_correct += correct
            total_entities += len(doc['gold_entities'])

        accuracy = total_correct / total_entities
        assert accuracy >= 0.60, f"Accuracy {accuracy:.1%} below Phase 1 target (60%)"

    def test_pattern_precision(self):
        """Test pattern-based precision target: 95%+"""

        # Test on documents with known pattern matches
        test_docs = load_pattern_test_documents()

        agent = NERAgent({})
        total_tp = 0  # True positives
        total_fp = 0  # False positives

        for doc in test_docs:
            result = agent.extract_entities(doc['text'], doc['sector'])

            # Count pattern-based entities
            pattern_entities = [e for e in result['entities'] if e['source'] == 'pattern']

            for entity in pattern_entities:
                if is_correct(entity, doc['gold_entities']):
                    total_tp += 1
                else:
                    total_fp += 1

        precision = total_tp / (total_tp + total_fp)
        assert precision >= 0.95, f"Pattern precision {precision:.1%} below target (95%)"
```

### Continuous Validation

```python
# tools/validate_ner.py

def continuous_validation():
    """Run continuous NER validation on test set"""

    # Load test set
    test_set = load_test_set()

    # Initialize NER agent
    agent = NERAgent({})

    # Evaluate
    metrics = {
        'total_docs': len(test_set),
        'total_entities': 0,
        'correct_entities': 0,
        'by_type': defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0})
    }

    for doc in test_set:
        result = agent.extract_entities(doc['text'], doc['sector'])

        # Calculate metrics
        for gold_ent in doc['gold_entities']:
            metrics['total_entities'] += 1

            # Find matching predicted entity
            matched = False
            for pred_ent in result['entities']:
                if entities_match(gold_ent, pred_ent):
                    if gold_ent['label'] == pred_ent['label']:
                        metrics['correct_entities'] += 1
                        metrics['by_type'][gold_ent['label']]['tp'] += 1
                        matched = True
                        break
                    else:
                        # Wrong label
                        metrics['by_type'][gold_ent['label']]['fn'] += 1
                        metrics['by_type'][pred_ent['label']]['fp'] += 1
                        matched = True
                        break

            if not matched:
                # Missed entity
                metrics['by_type'][gold_ent['label']]['fn'] += 1

    # Calculate accuracy
    accuracy = metrics['correct_entities'] / metrics['total_entities']

    # Calculate per-type metrics
    for entity_type, counts in metrics['by_type'].items():
        tp = counts['tp']
        fp = counts['fp']
        fn = counts['fn']

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        metrics['by_type'][entity_type]['precision'] = precision
        metrics['by_type'][entity_type]['recall'] = recall
        metrics['by_type'][entity_type]['f1'] = f1

    # Print report
    print(f"\n{'='*60}")
    print(f"NER Validation Report")
    print(f"{'='*60}")
    print(f"Overall Accuracy: {accuracy:.1%}")
    print(f"Total Entities: {metrics['total_entities']}")
    print(f"Correct: {metrics['correct_entities']}")
    print(f"\nPer-Type Performance:")
    print(f"{'Entity Type':<20} {'Precision':<12} {'Recall':<12} {'F1':<12}")
    print(f"{'-'*60}")

    for entity_type in sorted(metrics['by_type'].keys()):
        m = metrics['by_type'][entity_type]
        print(f"{entity_type:<20} {m['precision']:<12.1%} {m['recall']:<12.1%} {m['f1']:<12.1%}")

    return metrics
```

---

## Success Criteria

### Phase 1 (Week 1) - PASS Criteria
- ✅ Pattern NER enabled (not returning 0 patterns)
- ✅ EntityRuler in spaCy pipeline
- ✅ Default.json pattern library exists with 300+ patterns
- ✅ Entity accuracy ≥60%
- ✅ Pattern precision ≥95%

### Phase 2 (Weeks 2-4) - PASS Criteria
- ✅ Custom NER model trained (1,000+ documents)
- ✅ Entity accuracy ≥80%
- ✅ Per-type F1 score ≥0.75 for all major entity types
- ✅ Active learning pipeline operational

### Phase 3 (Weeks 5-8) - PASS Criteria
- ✅ Ensemble NER system deployed
- ✅ Entity linking functional
- ✅ Entity accuracy ≥90%
- ✅ Relationship extraction accuracy ≥75%
- ✅ Production-ready system

---

## Risk Mitigation

### Risk 1: Insufficient Training Data
**Impact**: Cannot train custom NER model
**Probability**: Medium
**Mitigation**:
- Use pattern-generated training data as seed
- Active learning to reduce annotation requirements
- Data augmentation techniques
- Fallback to pattern-only NER (still achieves 60%+)

### Risk 2: Pattern Explosion
**Impact**: Too many patterns, maintenance burden
**Probability**: Medium
**Mitigation**:
- Organize patterns hierarchically by sector
- Use regex for scalable patterns (CVE, CWE, etc.)
- Pattern validation and deduplication tools
- Regular pattern library audits

### Risk 3: Accuracy Plateau
**Impact**: Cannot reach 80%+ accuracy target
**Probability**: Low
**Mitigation**:
- Ensemble approach (combine multiple models)
- Entity linking for disambiguation
- Human-in-the-loop validation
- Continuous improvement via active learning

### Risk 4: Performance Degradation
**Impact**: NER too slow for production use
**Probability**: Low
**Mitigation**:
- Batch processing for large documents
- Model optimization (quantization, pruning)
- Caching frequently processed documents
- Parallel processing for multi-document workflows

---

## Appendix A: Pattern Library Structure

### default.json (Comprehensive Pattern Library)

```json
{
  "meta": {
    "version": "2.0.0",
    "created": "2025-11-05",
    "total_patterns": 500,
    "domains": ["industrial", "cybersecurity", "mixed"]
  },

  "patterns": [
    // VENDORS (50 patterns)
    {"label": "VENDOR", "pattern": [{"LOWER": "siemens"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "rockwell"}, {"LOWER": "automation"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "abb"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "schneider"}, {"LOWER": "electric"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "honeywell"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "emerson"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "yokogawa"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "ge"}, {"LOWER": "digital"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "allen-bradley"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "mitsubishi"}, {"LOWER": "electric"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "omron"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "phoenix"}, {"LOWER": "contact"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "wago"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "beckhoff"}]},
    {"label": "VENDOR", "pattern": [{"LOWER": "b&r"}, {"LOWER": "automation"}]},
    // ... 35 more vendor patterns

    // PROTOCOLS (30 patterns)
    {"label": "PROTOCOL", "pattern": [{"LOWER": "modbus"}, {"LOWER": "tcp"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "modbus"}, {"LOWER": "rtu"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "opc"}, {"LOWER": "ua"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "profinet"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "ethercat"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "hart"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "foundation"}, {"LOWER": "fieldbus"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "devicenet"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "bacnet"}]},
    {"label": "PROTOCOL", "pattern": [{"LOWER": "dnp3"}]},
    // ... 20 more protocol patterns

    // CYBERSECURITY (200 patterns)
    {"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]},
    {"label": "CWE", "pattern": [{"TEXT": {"REGEX": "CWE-\\d+"}}]},
    {"label": "CAPEC", "pattern": [{"TEXT": {"REGEX": "CAPEC-\\d+"}}]},
    // ... threat actors, malware, IOCs, etc.

    // MEASUREMENTS (50 patterns)
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": "\\d+(\\.\\d+)?\\s*PSI"}}]},
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": "\\d+(\\.\\d+)?\\s*bar"}}]},
    // ... more measurement patterns

    // STANDARDS (40 patterns)
    {"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": "IEC\\s*\\d{5}"}}]},
    {"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": "IEEE\\s*\\d+"}}]},
    // ... more standard patterns

    // COMPONENTS (80 patterns)
    {"label": "COMPONENT", "pattern": [{"LOWER": "plc"}]},
    {"label": "COMPONENT", "pattern": [{"LOWER": "programmable"}, {"LOWER": "logic"}, {"LOWER": "controller"}]},
    // ... more component patterns

    // SAFETY_CLASS (20 patterns)
    {"label": "SAFETY_CLASS", "pattern": [{"TEXT": {"REGEX": "SIL\\s*[0-4]"}}]},
    // ... more safety patterns

    // SYSTEM_LAYER (30 patterns)
    {"label": "SYSTEM_LAYER", "pattern": [{"TEXT": {"REGEX": "L[0-5]"}}]},
    // ... more layer patterns
  ]
}
```

---

## Appendix B: Training Pipeline Example

### Complete Training Script

```python
#!/usr/bin/env python3
"""
Train custom spaCy NER model for industrial/cybersecurity domains
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch
import json
from pathlib import Path
import random

def load_training_data(data_dir: Path) -> List[Example]:
    """Load training data from annotated documents"""

    nlp = spacy.blank("en")
    examples = []

    # Load annotated documents
    for json_file in data_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

            text = data['text']
            entities = data['entities']

            # Create spaCy example
            doc = nlp.make_doc(text)
            ents = [(e['start'], e['end'], e['label']) for e in entities]

            example = Example.from_dict(doc, {"entities": ents})
            examples.append(example)

    return examples

def train_ner_model(
    training_data: List[Example],
    output_dir: Path,
    n_iter: int = 30,
    batch_size: int = 32
):
    """Train custom NER model"""

    # Initialize blank model
    nlp = spacy.blank("en")

    # Add NER component
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # Add entity labels
    entity_types = [
        "VENDOR", "PROTOCOL", "STANDARD", "COMPONENT",
        "MEASUREMENT", "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER",
        "CVE", "CWE", "CAPEC", "THREAT_ACTOR", "CAMPAIGN",
        "ATTACK_TECHNIQUE", "MALWARE", "IOC", "APT_GROUP"
    ]

    for label in entity_types:
        ner.add_label(label)

    # Initialize training
    nlp.begin_training()

    # Training loop
    for iteration in range(n_iter):
        random.shuffle(training_data)
        losses = {}

        # Batch training
        batches = minibatch(training_data, size=batch_size)
        for batch in batches:
            nlp.update(batch, drop=0.2, losses=losses)

        print(f"Iteration {iteration + 1}/{n_iter}: Loss = {losses.get('ner', 0):.4f}")

    # Save model
    output_dir.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"\nModel saved to {output_dir}")

    return nlp

def evaluate_model(nlp, test_data: List[Example]) -> Dict[str, float]:
    """Evaluate trained model"""

    from spacy.scorer import Scorer

    scorer = Scorer()
    examples = []

    for example in test_data:
        pred = nlp(example.reference.text)
        examples.append(Example(pred, example.reference))

    scores = scorer.score(examples)

    print("\n" + "="*60)
    print("Evaluation Results")
    print("="*60)
    print(f"Precision: {scores['ents_p']:.3f}")
    print(f"Recall:    {scores['ents_r']:.3f}")
    print(f"F1 Score:  {scores['ents_f']:.3f}")

    print("\nPer-Type Performance:")
    for entity_type, metrics in scores['ents_per_type'].items():
        print(f"{entity_type:20s} P={metrics['p']:.3f} R={metrics['r']:.3f} F1={metrics['f']:.3f}")

    return scores

if __name__ == "__main__":
    # Load data
    data_dir = Path("training_data/annotated")
    training_examples = load_training_data(data_dir / "train")
    test_examples = load_training_data(data_dir / "test")

    print(f"Loaded {len(training_examples)} training examples")
    print(f"Loaded {len(test_examples)} test examples")

    # Train model
    output_dir = Path("models/custom_ner_v1")
    nlp = train_ner_model(training_examples, output_dir, n_iter=30)

    # Evaluate
    scores = evaluate_model(nlp, test_examples)

    # Save evaluation report
    with open(output_dir / "evaluation.json", "w") as f:
        json.dump(scores, f, indent=2)
```

---

## Conclusion

This roadmap provides a comprehensive, evidence-based strategy to improve NER accuracy from 29% to 80%+ through:

1. **Immediate fixes** (Week 1): Enable pattern NER, create comprehensive pattern libraries
2. **Model training** (Weeks 2-4): Train custom spaCy models on domain-specific data
3. **Advanced features** (Weeks 5-8): Ensemble models, entity linking, expanded relationships

**Key Success Factors**:
- Pattern-based NER provides high-precision foundation (95%+)
- Custom neural models add contextual understanding
- Active learning reduces annotation burden
- Multi-label classification captures semantic richness
- Continuous validation ensures sustained accuracy

**Resource Requirements**:
- 8 weeks development time
- $5,000-$10,000 annotation budget
- 2,500+ training documents
- spaCy 3.8.7+ with transformer support

**Expected Outcome**: 90%+ entity classification accuracy enabling high-quality knowledge graph construction for cybersecurity and industrial domains.

---

**Document Status**: Complete
**Next Steps**: Begin Phase 1 implementation (Week 1)
**Review Date**: 2025-11-12 (after Phase 1 completion)
