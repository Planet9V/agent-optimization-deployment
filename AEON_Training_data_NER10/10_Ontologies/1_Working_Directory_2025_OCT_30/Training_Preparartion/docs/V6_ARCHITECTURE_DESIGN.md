# v6 Architecture Design
**Version:** 6.0.0
**Created:** 2025-11-06
**Status:** Design Phase
**Purpose:** Comprehensive quality framework for NER training pipeline

## Executive Summary

v6 introduces a systematic quality framework to address critical issues identified in v4/v5:
- **Primary Goal:** Achieve VENDOR F1 ≥ 75% (from 24.44%)
- **Approach:** Quality gates, entity separation, boundary standardization, training optimization
- **Impact:** Projected overall F1 improvement from 77.67% → 92%

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    v6 QUALITY FRAMEWORK                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐    ┌──────────────┐    ┌─────────────┐ │
│  │ Pre-Training  │ -> │   Training   │ -> │ Post-Train  │ │
│  │ Quality Gates │    │ Optimization │    │ Validation  │ │
│  └───────────────┘    └──────────────┘    └─────────────┘ │
│         │                     │                    │        │
│         v                     v                    v        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │            Continuous Quality Monitoring              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## A. Quality Gates Framework

### 1. Pre-Training Validation

**Purpose:** Detect and prevent quality issues before training starts

#### Overlap Detection Gate
```python
def validate_no_overlaps(doc_bin_path):
    """
    Validates that no entities have overlapping spans.

    Blocks training if:
    - Any document has overlapping entity spans
    - Overlap conflicts are unresolved

    Returns:
        ValidationResult with:
        - overlap_count: int
        - affected_docs: List[str]
        - conflict_details: List[dict]
    """
    pass
```

**Acceptance Criteria:**
- Zero overlapping spans across all documents
- Automatic conflict resolution applied
- Detailed conflict report generated

#### Boundary Alignment Gate
```python
def validate_entity_boundaries(doc_bin_path):
    """
    Validates entity boundary consistency.

    Checks:
    - Word boundaries (no partial words)
    - Punctuation handling (standardized)
    - Whitespace normalization
    - Multi-word entity coherence

    Returns:
        BoundaryValidationResult with:
        - boundary_errors: List[dict]
        - inconsistencies: List[dict]
        - standardization_applied: bool
    """
    pass
```

**Acceptance Criteria:**
- All entities start/end on word boundaries
- Consistent punctuation handling (quotes, parentheses)
- No leading/trailing whitespace
- Multi-word entities properly segmented

#### Entity Distribution Gate
```python
def validate_entity_distribution(doc_bin_path):
    """
    Validates balanced entity representation.

    Checks:
    - Minimum examples per entity type (≥50)
    - Class balance ratios (no type >50% of total)
    - Training/validation split balance

    Returns:
        DistributionValidationResult with:
        - entity_counts: Dict[str, int]
        - balance_ratios: Dict[str, float]
        - warnings: List[str]
    """
    pass
```

**Acceptance Criteria:**
- VENDOR: ≥100 examples (currently underrepresented)
- No entity type >40% of total examples
- Balanced train/dev split (80/20 ±5%)

### 2. Training Validation

**Purpose:** Monitor training quality in real-time

#### Loss Monitoring
```python
class TrainingMonitor:
    """
    Real-time training quality monitoring.
    """

    def __init__(self, config):
        self.loss_threshold = config.get("max_loss", 10.0)
        self.improvement_window = config.get("patience", 5)
        self.min_improvement = config.get("min_delta", 0.01)

    def check_loss_convergence(self, losses):
        """
        Detect training issues from loss patterns.

        Returns:
            - is_converging: bool
            - early_stop: bool
            - warnings: List[str]
        """
        pass
```

**Early Stopping Criteria:**
- No improvement for 5 epochs
- Loss increase for 3 consecutive epochs
- Loss exceeds 10.0 (indicates training failure)

#### Per-Entity Performance Tracking
```python
def track_entity_performance(scorer, entity_type):
    """
    Track performance per entity type during training.

    Monitors:
    - Per-entity F1 scores
    - Confusion patterns (VENDOR→EQUIPMENT)
    - Boundary accuracy

    Returns:
        EntityPerformanceMetrics
    """
    pass
```

**Monitoring Thresholds:**
- VENDOR F1 < 50% after 10 epochs → trigger review
- EQUIPMENT F1 drop >5% → investigate feature competition
- Overall F1 plateau >5 epochs → adjust learning rate

### 3. Post-Training Validation

**Purpose:** Comprehensive quality assessment before deployment

#### Performance Gate
```python
def validate_model_performance(model, test_data):
    """
    Validates model meets performance targets.

    Checks:
    - Overall F1 ≥ 92%
    - VENDOR F1 ≥ 75%
    - EQUIPMENT F1 ≥ 93%
    - PROTOCOL F1 ≥ 85%

    Returns:
        PerformanceValidationResult with:
        - passed: bool
        - scores: Dict[str, Dict[str, float]]
        - failed_targets: List[str]
    """
    pass
```

**Release Criteria:**
- All F1 targets met
- No critical regressions (>5% drop in any entity)
- Confusion matrix analysis complete

#### Confusion Analysis Gate
```python
def analyze_confusion_patterns(predictions, gold_standard):
    """
    Identifies systematic misclassification patterns.

    Focus Areas:
    - VENDOR→EQUIPMENT misclassifications
    - PROTOCOL→EQUIPMENT confusion
    - Boundary errors (partial matches)

    Returns:
        ConfusionAnalysisResult with:
        - confusion_matrix: Dict
        - pattern_analysis: List[dict]
        - recommendations: List[str]
    """
    pass
```

**Acceptance Criteria:**
- VENDOR→EQUIPMENT misclassification < 10%
- Boundary errors (FP rate) < 20%
- No systematic confusion patterns

### 4. Automated Quality Checks

**Integration Points:**
```python
# In training pipeline
def run_training_with_quality_gates():
    """
    Automated quality gate execution.
    """
    # Pre-training
    pre_validation = run_pre_training_gates()
    if not pre_validation.passed:
        raise QualityGateFailure(pre_validation.errors)

    # Training with monitoring
    monitor = TrainingMonitor(config)
    for epoch in training_loop():
        metrics = train_epoch()
        if not monitor.check_quality(metrics):
            trigger_early_stop(monitor.warnings)

    # Post-training
    post_validation = run_post_training_gates()
    if not post_validation.passed:
        raise ModelRejection(post_validation.failures)

    return trained_model
```

## B. Entity Separation Strategy

### Problem Analysis

**Current Issue:** VENDOR and EQUIPMENT feature competition
- VENDOR F1 = 24.44% (P=53.11%, R=15.87%)
- EQUIPMENT F1 = 92.83% (P=94.14%, R=91.57%)
- Hypothesis: EQUIPMENT absorbing VENDOR mentions

**Evidence:**
```
Example misclassifications:
- "Siemens" (standalone) → Predicted: EQUIPMENT, Gold: VENDOR
- "Siemens PLC" → Predicted: EQUIPMENT, Gold: EQUIPMENT ✓
- "manufactured by Siemens" → Predicted: EQUIPMENT, Gold: VENDOR
```

### Disambiguation Rules

#### 1. Syntactic Pattern Analysis

**Rule: Standalone vs Compound**
```python
def is_vendor_mention(text, context):
    """
    Distinguishes VENDOR from EQUIPMENT based on syntax.

    VENDOR indicators:
    - Standalone company name (no product suffix)
    - Near vendor-specific verbs (manufactured, produced, developed)
    - In ownership/attribution phrases

    EQUIPMENT indicators:
    - Company name + product model/type
    - Technical specifications present
    - Near equipment-specific terms (device, controller, system)
    """
    # Standalone company name pattern
    if is_company_name(text) and not has_product_suffix(text):
        return "VENDOR"

    # Compound with product
    if is_company_name(text.split()[0]) and has_product_model(text):
        return "EQUIPMENT"

    # Context-based decision
    return classify_by_context(text, context)
```

**Examples:**
| Text | Classification | Rationale |
|------|---------------|-----------|
| "Siemens" | VENDOR | Standalone company name |
| "Siemens S7-1500" | EQUIPMENT | Company + model number |
| "Rockwell Automation" | VENDOR | Company name without product |
| "Allen-Bradley PLC" | EQUIPMENT | Brand + device type |

#### 2. Context Clue Detection

**Rule: Surrounding Linguistic Context**
```python
VENDOR_CONTEXT_PATTERNS = [
    r"manufactured by \{ENTITY\}",
    r"produced by \{ENTITY\}",
    r"developed by \{ENTITY\}",
    r"\{ENTITY\}'s product",
    r"from \{ENTITY\}",
    r"\{ENTITY\} supplies",
]

EQUIPMENT_CONTEXT_PATTERNS = [
    r"\{ENTITY\} device",
    r"\{ENTITY\} controller",
    r"\{ENTITY\} running",
    r"configure \{ENTITY\}",
    r"\{ENTITY\} firmware",
    r"\{ENTITY\} specifications",
]

def classify_by_context(entity_text, surrounding_text, window=10):
    """
    Use surrounding words to disambiguate.

    Args:
        entity_text: The entity span text
        surrounding_text: Full sentence or paragraph
        window: Words before/after to consider

    Returns:
        "VENDOR" or "EQUIPMENT" or "AMBIGUOUS"
    """
    before, after = get_context_window(entity_text, surrounding_text, window)

    vendor_score = count_pattern_matches(before + after, VENDOR_CONTEXT_PATTERNS)
    equipment_score = count_pattern_matches(before + after, EQUIPMENT_CONTEXT_PATTERNS)

    if vendor_score > equipment_score:
        return "VENDOR"
    elif equipment_score > vendor_score:
        return "EQUIPMENT"
    else:
        return "AMBIGUOUS"  # Fall back to syntactic rules
```

**Example Context Analysis:**
```
Sentence: "The Siemens SCADA system was manufactured by Siemens in Germany."

Entity 1: "Siemens SCADA system"
- Context: "The [ENTITY] was manufactured by"
- Equipment patterns: "SCADA system" (device type)
- Classification: EQUIPMENT ✓

Entity 2: "Siemens"
- Context: "manufactured by [ENTITY] in Germany"
- Vendor patterns: "manufactured by [ENTITY]"
- Classification: VENDOR ✓
```

#### 3. Feature Engineering

**Vendor-Specific Features:**
```python
def extract_vendor_features(entity, context):
    """
    Extract features that distinguish VENDOR from EQUIPMENT.
    """
    return {
        # Syntactic features
        "is_standalone_company": not has_product_suffix(entity.text),
        "has_legal_suffix": bool(re.search(r"\b(Inc|LLC|GmbH|Ltd)\b", entity.text)),
        "word_count": len(entity.text.split()),

        # Context features
        "near_vendor_verb": has_vendor_verb_nearby(entity, context, distance=5),
        "in_attribution_phrase": in_attribution_context(entity, context),
        "near_location": has_location_nearby(entity, context, distance=10),

        # Negation features
        "has_technical_terms": has_technical_terms_nearby(entity, context, distance=5),
        "has_model_number": bool(re.search(r"\d{3,}", entity.text)),
        "has_device_type": has_device_type_suffix(entity.text),
    }
```

**Equipment-Specific Features:**
```python
def extract_equipment_features(entity, context):
    """
    Extract features that distinguish EQUIPMENT from VENDOR.
    """
    return {
        # Syntactic features
        "has_product_model": has_model_pattern(entity.text),
        "has_device_suffix": has_device_type(entity.text),
        "is_compound": len(entity.text.split()) > 1,

        # Context features
        "near_technical_spec": has_specs_nearby(entity, context, distance=10),
        "near_configuration": has_config_terms_nearby(entity, context, distance=5),
        "in_technical_description": in_technical_context(entity, context),

        # Domain features
        "matches_equipment_pattern": matches_known_equipment_pattern(entity.text),
        "has_version_number": bool(re.search(r"v?\d+\.\d+", entity.text)),
    }
```

### Implementation in Pipeline

**Annotation Extraction Enhancement:**
```python
def extract_entity_with_disambiguation(annotation, doc_text):
    """
    Enhanced entity extraction with VENDOR/EQUIPMENT disambiguation.
    """
    entity_text = annotation["value"]["text"]
    label = annotation["value"]["labels"][0]

    # Apply disambiguation for VENDOR/EQUIPMENT
    if label in ["VENDOR", "EQUIPMENT"]:
        context = get_entity_context(entity_text, doc_text, window=20)

        # Syntactic check
        syntactic_label = classify_by_syntax(entity_text)

        # Context check
        context_label = classify_by_context(entity_text, context)

        # Resolve conflicts
        if syntactic_label != context_label:
            # Context wins for VENDOR (prioritize recall)
            if context_label == "VENDOR":
                label = "VENDOR"
            # Syntax wins for EQUIPMENT (prioritize precision)
            elif syntactic_label == "EQUIPMENT":
                label = "EQUIPMENT"
        else:
            label = syntactic_label

    return {
        "text": entity_text,
        "label": label,
        "start": annotation["value"]["start"],
        "end": annotation["value"]["end"],
        "disambiguation": {
            "syntactic": syntactic_label,
            "contextual": context_label,
            "final": label,
        }
    }
```

## C. Boundary Standardization

### Problem Analysis

**Current Issue:** 47% false positive rate due to boundary inconsistencies
- Partial word matches
- Inconsistent punctuation handling
- Whitespace variations
- Multi-word entity fragmentation

**Evidence:**
```
Boundary errors:
- "the SCADA system" → Predicted: "the SCADA", Gold: "SCADA system"
- "IEC-61850" → Predicted: "IEC", Gold: "IEC-61850"
- " Modbus TCP " → Leading/trailing whitespace
```

### Boundary Rules

#### 1. Word Boundary Enforcement

**Rule: Entities must start and end on word boundaries**
```python
def align_to_word_boundaries(text, start, end):
    """
    Adjust entity span to align with word boundaries.

    Rules:
    - Expand/contract to nearest word boundary
    - Preserve hyphenated compounds (IEC-61850)
    - Preserve acronyms with periods (U.S.A.)
    """
    # Get character at boundaries
    before_char = text[start-1] if start > 0 else " "
    after_char = text[end] if end < len(text) else " "

    # Adjust start
    while start > 0 and not is_word_boundary(before_char):
        start -= 1
        before_char = text[start-1] if start > 0 else " "

    # Adjust end
    while end < len(text) and not is_word_boundary(after_char):
        end += 1
        after_char = text[end] if end < len(text) else " "

    return start, end

def is_word_boundary(char):
    """
    Determines if character is a valid word boundary.
    """
    return char in [" ", "\n", "\t", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]"]
```

#### 2. Article and Preposition Handling

**Rule: Exclude leading articles and prepositions**
```python
LEADING_TOKENS_TO_EXCLUDE = [
    "the", "a", "an",           # Articles
    "of", "in", "on", "at",     # Prepositions
    "for", "with", "by",        # More prepositions
]

def remove_leading_noise(entity_text):
    """
    Remove articles and prepositions from entity start.

    Examples:
    - "the SCADA system" → "SCADA system"
    - "a Siemens PLC" → "Siemens PLC"
    - "in IEC-61850" → "IEC-61850"
    """
    words = entity_text.split()
    while words and words[0].lower() in LEADING_TOKENS_TO_EXCLUDE:
        words.pop(0)
    return " ".join(words)
```

#### 3. Punctuation Standardization

**Rule: Consistent handling of quotes and parentheses**
```python
def standardize_punctuation(entity_text, full_text, start, end):
    """
    Standardize punctuation inclusion/exclusion.

    Rules:
    - Include quotes if part of name: "FactoryTalk" → Include
    - Exclude wrapping quotes: The "SCADA" system → Exclude quotes
    - Include parentheses if part of acronym: ICS (Industrial Control System)
    - Exclude wrapping parentheses: The system (SCADA) → Exclude
    """
    # Check if quotes are part of entity name
    if entity_text.startswith('"') and entity_text.endswith('"'):
        # Check context: if surrounded by spaces, likely wrapping quotes
        if (start > 0 and full_text[start-1] == " " and
            end < len(full_text) and full_text[end] == " "):
            # Exclude wrapping quotes
            return entity_text[1:-1]

    # Similar logic for parentheses
    if entity_text.startswith("(") and entity_text.endswith(")"):
        if is_wrapping_parentheses(entity_text, full_text, start, end):
            return entity_text[1:-1]

    return entity_text
```

**Decision Tree for Quotes:**
```
Is entity wrapped in quotes?
├─ Yes
│  ├─ Is it a product name? (e.g., "FactoryTalk")
│  │  └─ INCLUDE quotes
│  └─ Is it emphasis/citation? (e.g., The "SCADA" system)
│     └─ EXCLUDE quotes
└─ No
   └─ Keep as-is
```

#### 4. Multi-Word Entity Coherence

**Rule: Multi-word entities must be semantically coherent**
```python
def validate_multi_word_entity(entity_text, entity_label):
    """
    Ensures multi-word entities are complete and coherent.

    Rules:
    - Company + Product: "Siemens S7-1500" ✓
    - Protocol + Version: "Modbus TCP" ✓
    - Partial phrases: "SCADA system running" ✗
    """
    words = entity_text.split()

    if len(words) == 1:
        return True  # Single-word entities always valid

    # Check for known valid patterns
    if entity_label == "EQUIPMENT":
        # Pattern: [Company] [Product Model/Type]
        if is_company_name(words[0]) and is_product_identifier(words[1:]):
            return True

    elif entity_label == "PROTOCOL":
        # Pattern: [Protocol] [Version/Variant]
        if is_protocol_name(words[0]) and is_protocol_variant(words[1:]):
            return True

    # Check for semantic coherence
    return has_semantic_coherence(words, entity_label)
```

**Examples:**
| Entity Text | Label | Valid | Reason |
|-------------|-------|-------|--------|
| "Siemens S7-1500 PLC" | EQUIPMENT | ✓ | Company + Model + Type |
| "Modbus TCP/IP" | PROTOCOL | ✓ | Protocol + Variant |
| "SCADA system running" | EQUIPMENT | ✗ | Includes non-entity verb |
| "IEC 61850" | PROTOCOL | ✓ | Standard + Number |

### Implementation

**Boundary Normalization Pipeline:**
```python
def normalize_entity_boundaries(entities, doc_text):
    """
    Apply all boundary standardization rules.
    """
    normalized = []

    for entity in entities:
        start, end = entity["start"], entity["end"]
        text = doc_text[start:end]
        label = entity["label"]

        # Step 1: Align to word boundaries
        start, end = align_to_word_boundaries(doc_text, start, end)
        text = doc_text[start:end]

        # Step 2: Remove leading noise
        text = remove_leading_noise(text)
        # Recalculate start based on removed tokens
        start = doc_text.find(text, start)
        end = start + len(text)

        # Step 3: Standardize punctuation
        text = standardize_punctuation(text, doc_text, start, end)
        end = start + len(text)

        # Step 4: Validate multi-word coherence
        if not validate_multi_word_entity(text, label):
            # Log warning but keep entity (manual review needed)
            logger.warning(f"Incoherent multi-word entity: '{text}' ({label})")

        # Step 5: Trim whitespace
        text = text.strip()
        start = doc_text.find(text, start)
        end = start + len(text)

        normalized.append({
            "text": text,
            "label": label,
            "start": start,
            "end": end,
        })

    return normalized
```

## D. Training Optimization

### Problem Analysis

**Current Issues:**
- VENDOR underrepresented in training data
- Imbalanced learning (EQUIPMENT dominates)
- Fixed learning rate insufficient for problem entities
- Limited training examples for rare patterns

### 1. Class Weighting

**Strategy: Boost VENDOR learning to compensate for underrepresentation**

```python
def calculate_class_weights(entity_counts):
    """
    Calculate inverse frequency weights for class balancing.

    Formula: weight_i = total_samples / (n_classes * count_i)

    Example:
    - VENDOR: 500 examples
    - EQUIPMENT: 3000 examples
    - Total: 3500, Classes: 2

    VENDOR weight: 3500 / (2 * 500) = 3.5
    EQUIPMENT weight: 3500 / (2 * 3000) = 0.58
    """
    total = sum(entity_counts.values())
    n_classes = len(entity_counts)

    weights = {}
    for entity, count in entity_counts.items():
        weights[entity] = total / (n_classes * count)

    # Normalize to prevent extreme weights
    max_weight = max(weights.values())
    weights = {k: v / max_weight for k, v in weights.items()}

    return weights
```

**Integration into spaCy:**
```python
# In training configuration
config = {
    "ner": {
        "model": {
            "@architectures": "spacy.TransitionBasedParser.v2",
            "tok2vec": tok2vec_config,
        },
        # Add class weights
        "class_weights": {
            "VENDOR": 3.5,      # Boost VENDOR learning
            "EQUIPMENT": 1.0,    # Baseline
            "PROTOCOL": 1.2,     # Slight boost
            "SECURITY": 1.5,
            "MITIGATION": 1.8,
            "THREAT": 1.3,
            "VULNERABILITY": 2.0,
        }
    }
}
```

**Expected Impact:**
- VENDOR: Increased weight → more gradient updates → improved recall
- EQUIPMENT: Maintained weight → preserve current performance
- Overall: Better balance → reduced VENDOR→EQUIPMENT confusion

### 2. Adaptive Learning Rates

**Strategy: Different learning rates for different entity types**

```python
class AdaptiveLearningRateScheduler:
    """
    Adjusts learning rate based on per-entity performance.
    """

    def __init__(self, base_lr=1e-3, patience=3, factor=0.5):
        self.base_lr = base_lr
        self.patience = patience
        self.factor = factor
        self.entity_performance_history = defaultdict(list)

    def get_entity_lr(self, entity_type, current_f1, epoch):
        """
        Returns learning rate for specific entity type.

        Strategy:
        - If F1 improving: keep current LR
        - If F1 plateau (>patience epochs): reduce LR
        - If F1 degrading: increase LR (up to base_lr)
        """
        history = self.entity_performance_history[entity_type]
        history.append(current_f1)

        if len(history) < self.patience:
            return self.base_lr

        recent_history = history[-self.patience:]

        # Check for improvement
        if is_improving(recent_history):
            return self.base_lr

        # Check for plateau
        if is_plateau(recent_history):
            return self.base_lr * self.factor

        # Check for degradation
        if is_degrading(recent_history):
            return min(self.base_lr * 1.5, self.base_lr)

        return self.base_lr
```

**Schedule Example:**
```
Epoch 1-5: VENDOR F1 improving (15% → 25% → 35% → 42% → 48%)
  → LR = 1e-3 (base rate)

Epoch 6-8: VENDOR F1 plateau (48% → 49% → 49%)
  → LR = 5e-4 (reduced)

Epoch 9-10: VENDOR F1 jumps (49% → 55% → 62%)
  → LR = 1e-3 (restore base)
```

### 3. Data Augmentation (Optional)

**Strategy: Generate synthetic examples for rare VENDOR patterns**

```python
def augment_vendor_examples(training_docs, target_count=1000):
    """
    Generate synthetic VENDOR examples to balance dataset.

    Techniques:
    1. Synonym substitution: "manufactured by" → "produced by"
    2. Context variation: Different surrounding sentences
    3. Entity replacement: Swap similar company names
    """
    vendor_examples = extract_vendor_examples(training_docs)
    current_count = len(vendor_examples)

    if current_count >= target_count:
        return training_docs  # Already sufficient

    augmented = []
    needed = target_count - current_count

    for _ in range(needed):
        # Select random existing example
        source = random.choice(vendor_examples)

        # Apply augmentation
        augmented_example = apply_augmentation(source, techniques=[
            "synonym_substitution",
            "context_variation",
            "entity_replacement",
        ])

        augmented.append(augmented_example)

    return training_docs + augmented
```

**Augmentation Examples:**
```
Original:
"The SCADA system was manufactured by Siemens in Germany."

Augmented:
1. "The SCADA system was produced by Siemens in Germany." (synonym)
2. "Siemens, a German company, manufactured the SCADA system." (context)
3. "The SCADA system was manufactured by Rockwell in the USA." (entity swap)
```

**Quality Control:**
- Validate augmented examples don't introduce noise
- Limit augmentation to <20% of total dataset
- Manual review of sample augmentations
- Monitor for overfitting to synthetic patterns

### 4. Training Configuration

**Optimized spaCy Configuration:**
```ini
[training]
max_epochs = 50
patience = 5
eval_frequency = 100
dropout = 0.2
accumulate_gradient = 2

[training.optimizer]
@optimizers = "Adam.v1"
learn_rate = 0.001
beta1 = 0.9
beta2 = 0.999

[training.score_weights]
ents_f = 0.5
ents_p = 0.25
ents_r = 0.25

# Per-entity scoring (v6 addition)
[training.entity_scores]
VENDOR = 2.0      # Double weight for VENDOR
EQUIPMENT = 1.0
PROTOCOL = 1.2
SECURITY = 1.3
MITIGATION = 1.5

[components.ner]
# Class weights
[components.ner.class_weights]
VENDOR = 3.5
EQUIPMENT = 1.0
PROTOCOL = 1.2
SECURITY = 1.5
MITIGATION = 1.8
THREAT = 1.3
VULNERABILITY = 2.0
```

## E. Evaluation Framework

### 1. Performance Targets

**Overall Targets:**
- Overall F1 ≥ 92% (precision ≥ 95%, recall ≥ 89%)
- Zero training errors (E103, W030)
- Generalization: Dev F1 within 5% of train F1

**Per-Entity Targets:**
| Entity | Precision | Recall | F1 | Current (v4) | Improvement |
|--------|-----------|--------|----|--------------| ------------|
| VENDOR | ≥80% | ≥70% | ≥75% | 24.44% | +207% |
| EQUIPMENT | ≥95% | ≥91% | ≥93% | 92.83% | Maintain |
| PROTOCOL | ≥88% | ≥82% | ≥85% | 80.02% | +6% |
| SECURITY | ≥90% | ≥85% | ≥87% | - | New |
| MITIGATION | ≥85% | ≥80% | ≥82% | - | New |

### 2. Confusion Matrix Analysis

**Purpose:** Track systematic misclassification patterns

```python
def analyze_confusion_matrix(predictions, gold_standard):
    """
    Generate and analyze entity confusion patterns.

    Focus on:
    - VENDOR→EQUIPMENT (primary concern)
    - PROTOCOL→EQUIPMENT
    - Boundary errors (partial matches)
    """
    confusion = defaultdict(lambda: defaultdict(int))

    for pred, gold in zip(predictions, gold_standard):
        if pred["label"] != gold["label"]:
            confusion[gold["label"]][pred["label"]] += 1

    # Calculate confusion rates
    confusion_rates = {}
    for true_label, pred_counts in confusion.items():
        total_gold = count_gold_entities(gold_standard, true_label)
        for pred_label, count in pred_counts.items():
            rate = count / total_gold
            confusion_rates[f"{true_label}→{pred_label}"] = {
                "count": count,
                "rate": rate,
                "severity": "HIGH" if rate > 0.1 else "MEDIUM" if rate > 0.05 else "LOW"
            }

    return confusion_rates
```

**Threshold Alerts:**
- VENDOR→EQUIPMENT rate >10% → CRITICAL
- PROTOCOL→EQUIPMENT rate >5% → WARNING
- Any confusion rate >15% → BLOCKER

### 3. Boundary Error Analysis

**Purpose:** Quantify and classify boundary errors

```python
def analyze_boundary_errors(predictions, gold_standard):
    """
    Categorize boundary-related errors.

    Categories:
    - Partial Match: Overlaps but not exact
    - Over-Extension: Predicted span too long
    - Under-Extension: Predicted span too short
    - Offset Error: Correct length, wrong position
    """
    boundary_errors = {
        "partial_match": [],
        "over_extension": [],
        "under_extension": [],
        "offset_error": [],
    }

    for pred, gold in align_predictions(predictions, gold_standard):
        if pred["start"] == gold["start"] and pred["end"] == gold["end"]:
            continue  # Exact match

        # Calculate overlap
        overlap = calculate_overlap(pred, gold)

        if overlap > 0:
            # Partial match
            if pred["end"] > gold["end"]:
                boundary_errors["over_extension"].append((pred, gold))
            elif pred["end"] < gold["end"]:
                boundary_errors["under_extension"].append((pred, gold))
            else:
                boundary_errors["offset_error"].append((pred, gold))

    # Calculate rates
    total_gold = len(gold_standard)
    error_rates = {
        category: len(errors) / total_gold
        for category, errors in boundary_errors.items()
    }

    return boundary_errors, error_rates
```

**Target Rates:**
- Partial match rate <10%
- Over-extension rate <5%
- Under-extension rate <5%
- Offset error rate <2%

### 4. Comprehensive Evaluation Report

**Report Structure:**
```python
def generate_evaluation_report(model, test_data):
    """
    Generate comprehensive v6 evaluation report.
    """
    # 1. Overall Performance
    overall_scores = evaluate_overall(model, test_data)

    # 2. Per-Entity Performance
    entity_scores = evaluate_per_entity(model, test_data)

    # 3. Confusion Analysis
    confusion_matrix = analyze_confusion_matrix(predictions, gold)

    # 4. Boundary Error Analysis
    boundary_errors, error_rates = analyze_boundary_errors(predictions, gold)

    # 5. Comparison with Baselines
    comparison = compare_with_baselines(entity_scores, v4_scores, v5_scores)

    # 6. Quality Gate Results
    quality_gates = check_quality_gates(overall_scores, entity_scores, confusion_matrix)

    report = {
        "timestamp": datetime.now(),
        "model_version": "v6",
        "overall": overall_scores,
        "per_entity": entity_scores,
        "confusion": confusion_matrix,
        "boundary_errors": boundary_errors,
        "comparison": comparison,
        "quality_gates": quality_gates,
        "passed": all(gate["passed"] for gate in quality_gates.values()),
    }

    return report
```

**Report Example:**
```yaml
v6 Evaluation Report
====================
Timestamp: 2025-11-06 14:30:00
Model: v6.0.0
Test Set: 39 documents

Overall Performance:
  Precision: 95.2% (target: ≥95%) ✓
  Recall: 89.4% (target: ≥89%) ✓
  F1: 92.2% (target: ≥92%) ✓

Per-Entity Performance:
  VENDOR:
    Precision: 82.1% (target: ≥80%) ✓
    Recall: 71.3% (target: ≥70%) ✓
    F1: 76.3% (target: ≥75%) ✓
    Improvement: +212% vs v4

  EQUIPMENT:
    Precision: 96.2% (target: ≥95%) ✓
    Recall: 92.1% (target: ≥91%) ✓
    F1: 94.1% (target: ≥93%) ✓
    Regression: -1.3% vs v4 (acceptable)

Confusion Analysis:
  VENDOR→EQUIPMENT: 8.2% (target: <10%) ✓
  PROTOCOL→EQUIPMENT: 3.1% (target: <5%) ✓
  No critical confusion patterns

Boundary Errors:
  Partial Match: 7.3% (target: <10%) ✓
  Over-Extension: 3.2% (target: <5%) ✓
  Under-Extension: 4.1% (target: <5%) ✓

Quality Gates:
  ✓ Performance Gate: PASSED
  ✓ Confusion Gate: PASSED
  ✓ Boundary Gate: PASSED
  ✓ Regression Gate: PASSED

Overall: PASSED ✓
Ready for deployment
```

## Integration Points

### Pipeline Integration
```python
# v6 Enhanced Training Pipeline
def train_v6_model(config_path, data_path):
    """
    Complete v6 training pipeline with quality framework.
    """
    # 1. Pre-Training Quality Gates
    logger.info("Running pre-training quality gates...")
    pre_gates = run_pre_training_gates(data_path)
    if not pre_gates.passed:
        raise QualityGateFailure(f"Pre-training gates failed: {pre_gates.errors}")

    # 2. Apply Entity Disambiguation
    logger.info("Applying VENDOR/EQUIPMENT disambiguation...")
    disambiguated_data = apply_entity_disambiguation(data_path)

    # 3. Standardize Boundaries
    logger.info("Standardizing entity boundaries...")
    normalized_data = apply_boundary_normalization(disambiguated_data)

    # 4. Optional: Data Augmentation
    if config.get("augmentation_enabled"):
        logger.info("Augmenting training data...")
        augmented_data = augment_vendor_examples(normalized_data)
    else:
        augmented_data = normalized_data

    # 5. Train with Monitoring
    logger.info("Starting training with quality monitoring...")
    monitor = TrainingMonitor(config)
    model = train_with_monitoring(config_path, augmented_data, monitor)

    # 6. Post-Training Quality Gates
    logger.info("Running post-training quality gates...")
    post_gates = run_post_training_gates(model, test_data)
    if not post_gates.passed:
        raise ModelRejection(f"Post-training gates failed: {post_gates.failures}")

    # 7. Generate Evaluation Report
    logger.info("Generating comprehensive evaluation report...")
    report = generate_evaluation_report(model, test_data)
    save_report(report, "v6_evaluation_report.json")

    logger.info("✓ v6 training complete - all quality gates passed")
    return model, report
```

## Success Metrics

### Critical Success Factors
1. **VENDOR Performance:** F1 ≥ 75% (from 24.44%)
2. **Zero Regressions:** EQUIPMENT F1 ≥ 92% (maintain v4)
3. **Overall Excellence:** F1 ≥ 92% (from 77.67%)
4. **Quality Gates:** 100% pass rate on all gates
5. **Confusion Reduction:** VENDOR→EQUIPMENT <10%

### Validation Criteria
- All automated quality gates pass
- Manual review of sample predictions (100 examples)
- Confusion matrix analysis shows improvement
- Boundary error rate <20%
- No training warnings or errors

### Release Readiness
```yaml
Release Checklist:
  ✓ All quality gates passed
  ✓ Performance targets met
  ✓ Confusion analysis complete
  ✓ Boundary errors acceptable
  ✓ Documentation updated
  ✓ Evaluation report generated
  ✓ Manual review completed
  ✓ Regression testing passed
```

## Next Steps

1. **Implement Quality Gates** (Phase 2)
2. **Deploy Entity Disambiguation** (Phase 3)
3. **Apply Boundary Standardization** (Phase 4)
4. **Optimize Training Configuration** (Phase 5)
5. **Execute Comprehensive Validation** (Phase 6)

---
**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Ready for Implementation
