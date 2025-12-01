# Complete Annotation Workflow for ICS Security Corpus
**File**: 03_ANNOTATION_WORKFLOW_v1.0.md
**Created**: 2025-11-23 (System Date)
**Version**: v1.0.0
**Author**: AEON Cyber DT Project
**Purpose**: End-to-end annotation system for 678 files with psychological + technical entities
**Status**: ACTIVE

---

## Executive Summary

This document provides a production-ready annotation workflow for creating a 678-file corpus with 18 entity types (8 psychological + 10 technical) and 20+ relationship types. The system achieves >85% inter-annotator agreement through structured validation gates and quality control mechanisms.

**Key Metrics**:
- **Total Files**: 678 markdown documents
- **Entity Types**: 18 (detailed schema below)
- **Relationship Types**: 24 (detailed schema below)
- **Target IAA**: >0.85 (Inter-Annotator Agreement)
- **Batch Size**: 50 files per annotation batch
- **Total Batches**: 14 batches (13×50 + 1×28)
- **Estimated Timeline**: 12-16 weeks with 3-person team

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tool Selection & Rationale](#tool-selection--rationale)
3. [File Preparation Pipeline](#file-preparation-pipeline)
4. [Entity Schema Specification](#entity-schema-specification)
5. [Relationship Schema Specification](#relationship-schema-specification)
6. [Annotation Interface Configuration](#annotation-interface-configuration)
7. [Quality Control System](#quality-control-system)
8. [Validation Workflow](#validation-workflow)
9. [Test & Verification Strategy](#test--verification-strategy)
10. [Team Roles & Responsibilities](#team-roles--responsibilities)
11. [Timeline & Milestones](#timeline--milestones)
12. [Technical Implementation](#technical-implementation)
13. [Metrics & Monitoring](#metrics--monitoring)
14. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Architecture Overview

### 1.1 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANNOTATION WORKFLOW SYSTEM                    │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │  PREPARE  │      │ ANNOTATE  │      │ VALIDATE  │
    └───────────┘      └───────────┘      └───────────┘
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │   Parse   │      │  Primary  │      │   Test    │
    │  Convert  │      │ Annotator │      │ Validator │
    │   Batch   │      └─────┬─────┘      └─────┬─────┘
    └─────┬─────┘            │                   │
          │            ┌─────▼─────┐      ┌─────▼─────┐
          │            │Independent│      │  Quality  │
          │            │ Validator │      │   Agent   │
          │            └─────┬─────┘      └─────┬─────┘
          │                  │                   │
          └──────────────────┴───────────────────┘
                             │
                      ┌──────▼──────┐
                      │  FINALIZE   │
                      │  - Export   │
                      │  - Metrics  │
                      │  - DocBin   │
                      └─────────────┘
```

### 1.2 Data Flow

```
SOURCE FILES (678 .md)
    │
    ├─→ [PRE-PROCESSING] → Cleaned markdown + metadata
    │
    ├─→ [BATCHING] → 14 batches (50 files each)
    │
    ├─→ [ANNOTATION] → Primary annotator (Prodigy)
    │
    ├─→ [VALIDATION 1] → Independent validator review
    │
    ├─→ [VALIDATION 2] → Test agent automated checks
    │
    ├─→ [CONSENSUS] → Resolve disagreements (IAA >0.85)
    │
    ├─→ [EXPORT] → spaCy DocBin format
    │
    └─→ [TRAINING DATA] → Ready for NER model
```

### 1.3 Quality Gates

Each batch must pass through 4 quality gates:

1. **Gate 1: Pre-Annotation** - File structure validation, entity guidelines review
2. **Gate 2: Post-Annotation** - Primary annotation completeness check
3. **Gate 3: Validation** - Independent validator agreement >85%
4. **Gate 4: Testing** - Automated quality agent verification

---

## 2. Tool Selection & Rationale

### 2.1 Recommended Tool: Prodigy (2025 Best Practice)

**Selected Tool**: **Prodigy v1.14+** (as of 2025)

**Rationale**:
- ✅ **spaCy Integration**: Native DocBin export for seamless training pipeline
- ✅ **Custom Recipes**: Full Python customization for 18 entity types + 24 relationships
- ✅ **Active Learning**: Reduces annotation time by 40-60%
- ✅ **Real-time Validation**: Immediate feedback on entity boundaries
- ✅ **Batch Management**: Built-in batch tracking and progress monitoring
- ✅ **Multi-Annotator**: Native support for IAA calculation
- ✅ **Relationship Annotation**: Built-in relation interface (critical for our 24 relationship types)

**Alternative**: Label Studio v1.11+ (if Prodigy license unavailable)
- Open-source, but requires more custom development
- Weaker spaCy integration (custom export pipeline needed)
- Better for distributed teams (web-based)

### 2.2 Tool Comparison Matrix

| Feature | Prodigy v1.14+ | Label Studio v1.11+ | Doccano v1.8+ |
|---------|----------------|---------------------|---------------|
| spaCy Integration | ★★★★★ Native | ★★★☆☆ Custom | ★★☆☆☆ Export only |
| Relationship Annotation | ★★★★★ Built-in | ★★★★☆ Plugin | ★★☆☆☆ Limited |
| Active Learning | ★★★★★ Advanced | ★★★☆☆ Basic | ★☆☆☆☆ None |
| Custom Entity Types | ★★★★★ Unlimited | ★★★★★ Unlimited | ★★★★☆ Limited |
| IAA Calculation | ★★★★★ Built-in | ★★★☆☆ Custom | ★★☆☆☆ Manual |
| Batch Management | ★★★★★ Native | ★★★★☆ Good | ★★★☆☆ Basic |
| Team Collaboration | ★★★★☆ Good | ★★★★★ Excellent | ★★★☆☆ Basic |
| Cost | $$$$ (License) | FREE (Open-source) | FREE (Open-source) |
| Learning Curve | ★★★☆☆ Moderate | ★★★★☆ Steeper | ★★☆☆☆ Easier |

**Decision**: Prodigy v1.14+ for production annotation due to spaCy native integration and relationship annotation capabilities.

### 2.3 Infrastructure Requirements

**Hardware**:
- **Primary Annotator**: Standard workstation (16GB RAM, modern browser)
- **Validation Station**: Same as above
- **Test Agent Server**: 32GB RAM, 8+ cores (for automated validation)

**Software Stack**:
```bash
# Core annotation environment
prodigy==1.14.0  # Annotation tool (2025 version)
spacy==3.7.2     # NLP library (latest 2025 version)
python==3.11.6   # Python runtime

# Validation & testing
scikit-learn==1.4.0  # IAA calculation
pandas==2.1.4        # Data processing
jupyter==1.0.0       # Analysis notebooks

# Storage & export
sqlite3              # Prodigy database backend
jsonl                # Intermediate format
DocBin               # spaCy training format
```

---

## 3. File Preparation Pipeline

### 3.1 Pre-Processing Steps

```python
# FILE: prepare_corpus.py
"""
Convert 678 markdown files to Prodigy-ready JSONL format
Preserve structure, citations, metadata
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
import hashlib

def prepare_corpus(source_dir: Path, output_dir: Path) -> None:
    """
    Convert markdown files to annotatable JSONL format.

    Args:
        source_dir: Directory containing 678 .md files
        output_dir: Directory for processed JSONL batches
    """
    files = sorted(source_dir.glob("*.md"))
    batch_size = 50
    batch_num = 0

    for i in range(0, len(files), batch_size):
        batch_files = files[i:i+batch_size]
        batch_data = []

        for file_path in batch_files:
            doc = process_markdown(file_path)
            batch_data.append(doc)

        # Save batch as JSONL
        batch_file = output_dir / f"batch_{batch_num:02d}.jsonl"
        with open(batch_file, 'w', encoding='utf-8') as f:
            for doc in batch_data:
                f.write(json.dumps(doc) + '\n')

        print(f"Batch {batch_num}: {len(batch_data)} files → {batch_file}")
        batch_num += 1

def process_markdown(file_path: Path) -> Dict[str, Any]:
    """
    Parse markdown file and extract structure.

    Returns:
        Dictionary with text, metadata, and structure
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from frontmatter (if present)
    metadata = extract_frontmatter(content)

    # Clean markdown for annotation
    text = clean_markdown(content)

    # Preserve structure hints (headers, lists, code blocks)
    structure = extract_structure(content)

    # Calculate unique ID
    doc_id = hashlib.md5(text.encode()).hexdigest()[:12]

    return {
        "text": text,
        "meta": {
            "source_file": str(file_path.name),
            "doc_id": doc_id,
            "word_count": len(text.split()),
            "structure": structure,
            **metadata
        }
    }

def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter if present."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        # Simple key-value extraction (not full YAML parser)
        lines = match.group(1).split('\n')
        metadata = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        return metadata
    return {}

def clean_markdown(content: str) -> str:
    """
    Clean markdown for annotation while preserving important structure.

    Preserves:
    - Inline citations [1], [Smith, 2020]
    - Technical terms (CVE-2024-1234)
    - Headers (as text)
    - List items (as text)

    Removes:
    - Markdown syntax (* ** # - etc.)
    - Code blocks (```...```)
    - HTML tags
    - URLs (convert to anchor text only)
    """
    # Remove code blocks
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Convert URLs to anchor text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove markdown syntax but preserve structure
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)  # List bullets

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text

def extract_structure(content: str) -> Dict[str, Any]:
    """
    Extract document structure hints for annotators.

    Returns:
        Dictionary with sections, lists, citations
    """
    structure = {
        "sections": [],
        "has_citations": False,
        "has_technical_terms": False,
        "has_lists": False
    }

    # Extract section headers
    headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    structure["sections"] = headers[:5]  # First 5 headers

    # Check for citations
    if re.search(r'\[\d+\]|\[[A-Z][a-z]+,\s*\d{4}\]', content):
        structure["has_citations"] = True

    # Check for technical terms (CVE, ICS, SCADA, etc.)
    if re.search(r'CVE-\d{4}-\d+|ICS|SCADA|PLC|HMI|MITRE', content):
        structure["has_technical_terms"] = True

    # Check for lists
    if re.search(r'^[-*]\s+', content, re.MULTILINE):
        structure["has_lists"] = True

    return structure

# Usage
if __name__ == "__main__":
    source = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current")
    output = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/15_NER10_Approach/annotation/batches")
    output.mkdir(parents=True, exist_ok=True)

    prepare_corpus(source, output)
    print("\n✅ Corpus preparation complete!")
    print(f"   Output: {output}")
    print(f"   Batches: 14 (13×50 + 1×28)")
```

### 3.2 Batch Organization

```
annotation/batches/
├── batch_00.jsonl  # Files 001-050
├── batch_01.jsonl  # Files 051-100
├── batch_02.jsonl  # Files 101-150
├── ...
├── batch_12.jsonl  # Files 601-650
└── batch_13.jsonl  # Files 651-678 (28 files)

Each JSONL file contains:
{
  "text": "Cleaned document text...",
  "meta": {
    "source_file": "01_Introduction_to_ICS_Security.md",
    "doc_id": "a3f2c8d1b4e5",
    "word_count": 2847,
    "structure": {
      "sections": ["Introduction", "Background", "Key Concepts"],
      "has_citations": true,
      "has_technical_terms": true,
      "has_lists": true
    }
  }
}
```

### 3.3 Batch Metadata Tracking

```python
# FILE: batch_metadata.json
{
  "corpus_name": "ICS_Security_Corpus_v1",
  "total_files": 678,
  "total_batches": 14,
  "batch_size": 50,
  "created_date": "2025-11-23",
  "batches": [
    {
      "batch_id": "batch_00",
      "file_range": "001-050",
      "status": "prepared",
      "assigned_annotator": null,
      "annotation_start": null,
      "annotation_end": null,
      "validation_status": "pending"
    },
    // ... all 14 batches
  ],
  "quality_metrics": {
    "target_iaa": 0.85,
    "current_iaa": null,
    "completed_batches": 0
  }
}
```

---

## 4. Entity Schema Specification

### 4.1 Complete Entity Taxonomy (18 Types)

#### **Category A: Technical Entities (10 types)**

| Entity Type | Description | Examples | Color Code |
|-------------|-------------|----------|------------|
| `EQUIPMENT` | ICS/SCADA devices, PLCs, controllers | "Siemens S7-1200 PLC", "Schneider Electric HMI" | `#FF6B6B` (Red) |
| `CVE` | Vulnerability identifiers | "CVE-2024-1234", "CVE-2023-5678" | `#FF9F43` (Orange) |
| `SECTOR` | Critical infrastructure sectors | "Energy Sector", "Water Treatment", "Manufacturing" | `#48C9B0` (Teal) |
| `THREAT_ACTOR` | Malicious entities | "APT28", "Sandworm", "Insider threat" | `#8E44AD` (Purple) |
| `TECHNIQUE` | MITRE ATT&CK techniques | "Spear Phishing", "Lateral Movement", "T1566.001" | `#3498DB` (Blue) |
| `ORGANIZATION` | Companies, agencies, groups | "DHS CISA", "Siemens", "NIST" | `#95A5A6` (Gray) |
| `FACILITY` | Physical locations | "Nuclear power plant", "Water treatment facility" | `#E74C3C` (Dark Red) |
| `PROCESS` | Industrial processes | "Batch production", "Continuous monitoring" | `#1ABC9C` (Green) |
| `MEASUREMENT` | Quantitative values | "100 psi", "75% capacity", "5000 units" | `#F39C12` (Yellow) |
| `PROPERTY` | System characteristics | "Real-time requirement", "Safety-critical" | `#34495E` (Navy) |

#### **Category B: Psychological Entities (8 types)**

| Entity Type | Description | Examples | Color Code |
|-------------|-------------|----------|------------|
| `COGNITIVE_BIAS` | 30 cognitive biases (see full list) | "Normalcy bias", "Confirmation bias" | `#E91E63` (Pink) |
| `EMOTION` | Psychological states | "Anxiety", "Panic", "Denial", "Complacency" | `#9C27B0` (Deep Purple) |
| `THREAT_PERCEPTION` | How threats are perceived | "Real threat", "Imaginary threat", "Symbolic threat" | `#FF5722` (Deep Orange) |
| `ATTACKER_MOTIVATION` | MICE framework + cybercriminal motives | "Ideology", "Money", "Coercion", "Ego" | `#795548` (Brown) |
| `DEFENSE_MECHANISM` | Psychological defense responses | "Denial", "Rationalization", "Projection" | `#607D8B` (Blue Gray) |
| `SECURITY_CULTURE` | Organizational security mindset | "Blame culture", "Security-first culture" | `#009688` (Cyan) |
| `HISTORICAL_PATTERN` | Past incident patterns | "Repeated failures", "Learning from incidents" | `#FFC107` (Amber) |
| `FUTURE_THREAT` | Emerging threats | "AI-powered attacks", "Quantum threats" | `#00BCD4` (Light Blue) |

### 4.2 Cognitive Bias Complete List (30 Types)

The `COGNITIVE_BIAS` entity includes these 30 specific biases:

```yaml
cognitive_biases:
  perception_biases:
    - normalcy_bias: "Underestimating threat likelihood based on past stability"
    - availability_heuristic: "Overweighting recent/memorable events"
    - recency_bias: "Prioritizing recent information over historical patterns"
    - anchoring_bias: "Over-relying on first piece of information"
    - framing_effect: "Different responses to same info based on presentation"

  decision_biases:
    - confirmation_bias: "Seeking info that confirms existing beliefs"
    - overconfidence_bias: "Overestimating one's knowledge or abilities"
    - optimism_bias: "Believing negative events are less likely for us"
    - status_quo_bias: "Preferring current state over change"
    - sunk_cost_fallacy: "Continuing investment due to past commitment"

  group_biases:
    - groupthink: "Desire for harmony leads to irrational decisions"
    - authority_bias: "Attributing greater accuracy to authority opinions"
    - bandwagon_effect: "Adopting beliefs because many others do"
    - in_group_bias: "Favoring one's own group members"
    - halo_effect: "Overall impression influences specific judgments"

  temporal_biases:
    - present_bias: "Prioritizing immediate rewards over future benefits"
    - planning_fallacy: "Underestimating time/resources needed"
    - hindsight_bias: "Seeing past events as more predictable"
    - temporal_discounting: "Devaluing future risks"

  attribution_biases:
    - fundamental_attribution_error: "Overemphasizing personality vs situation"
    - self_serving_bias: "Attributing success to self, failure to external"
    - actor_observer_bias: "Different attributions for self vs others"

  attention_biases:
    - selective_attention: "Focusing on some info while ignoring other"
    - inattentional_blindness: "Failing to notice unexpected events"
    - change_blindness: "Failing to detect changes in environment"

  complexity_biases:
    - complexity_bias: "Preferring complex solutions over simple ones"
    - dunning_kruger_effect: "Low ability → overconfidence; high ability → underconfidence"
    - illusory_correlation: "Seeing relationships where none exist"
    - clustering_illusion: "Seeing patterns in random data"
    - gambler_fallacy: "Believing past events affect independent future events"
```

### 4.3 Annotation Guidelines Per Entity

#### 4.3.1 EQUIPMENT Guidelines

**What to Annotate**:
- Specific device models: "Siemens S7-1200 PLC"
- Generic device categories: "programmable logic controller", "HMI"
- System components: "industrial router", "field device"

**What NOT to Annotate**:
- General computing terms: "computer", "server" (unless ICS-specific context)
- Software applications (annotate as TECHNIQUE if relevant)

**Boundary Rules**:
```
✅ Correct: "Siemens S7-1200 PLC"
❌ Wrong: "Siemens" alone (incomplete)
✅ Correct: "SCADA system"
❌ Wrong: "SCADA system at the facility" (over-extended)
```

#### 4.3.2 COGNITIVE_BIAS Guidelines

**What to Annotate**:
- Explicit bias mentions: "normalcy bias led to..."
- Implicit bias descriptions: "operators assumed the system was secure because it had never been attacked before" (annotate as normalcy_bias)

**What NOT to Annotate**:
- General cognitive descriptions: "operators thought about..."
- Neutral decision-making: "operators evaluated the options"

**Attribute Assignment**:
Each COGNITIVE_BIAS span must have a `bias_type` attribute from the 30-bias taxonomy.

```json
{
  "text": "normalcy bias",
  "label": "COGNITIVE_BIAS",
  "start": 45,
  "end": 58,
  "attributes": {
    "bias_type": "normalcy_bias",
    "bias_category": "perception_biases"
  }
}
```

#### 4.3.3 CVE Guidelines

**Pattern Matching**:
- Standard format: `CVE-YYYY-NNNNN` (e.g., CVE-2024-1234)
- Always include full CVE identifier
- Capture year and number

**Validation**:
- Verify CVE format with regex: `CVE-\d{4}-\d{4,7}`
- Flag malformed CVEs for review

#### 4.3.4 THREAT_PERCEPTION Guidelines

**Three Categories**:
1. **Real Threat**: Actual, verified threat with evidence
   - "The confirmed attack on the nuclear facility..."

2. **Imaginary Threat**: Perceived threat with no evidence
   - "Operators feared a cyberattack despite no indicators..."

3. **Symbolic Threat**: Threat to identity/values rather than physical
   - "The breach represented a threat to the organization's reputation..."

**Attribute Assignment**:
```json
{
  "text": "perceived cyberattack threat",
  "label": "THREAT_PERCEPTION",
  "attributes": {
    "perception_type": "imaginary",
    "evidence_level": "low"
  }
}
```

#### 4.3.5 ATTACKER_MOTIVATION Guidelines

**MICE Framework**:
- **M**oney: Financial gain
- **I**deology: Political/religious beliefs
- **C**oercion: Forced participation (blackmail)
- **E**go: Recognition, revenge, challenge

**Additional Cybercriminal Motives**:
- Hacktivism
- Espionage
- Sabotage
- Insider threat

```json
{
  "text": "financially motivated attacker",
  "label": "ATTACKER_MOTIVATION",
  "attributes": {
    "motivation_type": "money",
    "framework": "MICE"
  }
}
```

### 4.4 Entity Schema Export Format

```json
{
  "entity_schema_version": "1.0.0",
  "total_entities": 18,
  "categories": {
    "technical": 10,
    "psychological": 8
  },
  "entities": [
    {
      "label": "EQUIPMENT",
      "category": "technical",
      "description": "ICS/SCADA devices, PLCs, controllers",
      "color": "#FF6B6B",
      "examples": ["Siemens S7-1200 PLC", "Schneider Electric HMI"],
      "attributes": {
        "device_type": ["PLC", "HMI", "RTU", "IED", "DCS", "SCADA"],
        "manufacturer": "string",
        "model": "string"
      },
      "guidelines": "See section 4.3.1"
    },
    {
      "label": "COGNITIVE_BIAS",
      "category": "psychological",
      "description": "30 cognitive biases affecting security decisions",
      "color": "#E91E63",
      "examples": ["normalcy bias", "confirmation bias"],
      "attributes": {
        "bias_type": ["normalcy_bias", "confirmation_bias", "..."],
        "bias_category": ["perception_biases", "decision_biases", "..."],
        "severity": ["low", "medium", "high"]
      },
      "guidelines": "See section 4.3.2"
    }
    // ... all 18 entities
  ]
}
```

---

## 5. Relationship Schema Specification

### 5.1 Complete Relationship Taxonomy (24 Types)

#### **Category A: Psychological Relationships (8 types)**

| Relationship | Head Entity | Tail Entity | Description | Example |
|--------------|-------------|-------------|-------------|---------|
| `EXHIBITS` | ORGANIZATION | COGNITIVE_BIAS | Organization displays bias | "ABC Corp" EXHIBITS "normalcy bias" |
| `CAUSED_BY` | Incident/Breach | COGNITIVE_BIAS | Incident resulted from bias | "Data breach" CAUSED_BY "overconfidence" |
| `INFLUENCED_BY` | Decision | COGNITIVE_BIAS | Decision affected by bias | "Delayed response" INFLUENCED_BY "anchoring" |
| `PERCEIVES` | Person/Org | THREAT_PERCEPTION | How threat is perceived | "Operators" PERCEIVES "imaginary threat" |
| `MOTIVATED_BY` | THREAT_ACTOR | ATTACKER_MOTIVATION | Attacker's motive | "APT28" MOTIVATED_BY "ideology" |
| `DEFENDS_WITH` | Person/Org | DEFENSE_MECHANISM | Psychological defense used | "Team" DEFENDS_WITH "denial" |
| `SHAPED_BY` | SECURITY_CULTURE | COGNITIVE_BIAS | Culture influenced by bias | "Blame culture" SHAPED_BY "groupthink" |
| `RESULTS_IN` | COGNITIVE_BIAS | EMOTION | Bias leads to emotion | "Normalcy bias" RESULTS_IN "complacency" |

#### **Category B: Technical Relationships (10 types)**

| Relationship | Head Entity | Tail Entity | Description | Example |
|--------------|-------------|-------------|-------------|---------|
| `EXPLOITS` | THREAT_ACTOR | CVE | Attacker exploits vulnerability | "APT28" EXPLOITS "CVE-2024-1234" |
| `USES` | THREAT_ACTOR | TECHNIQUE | Attacker uses technique | "Sandworm" USES "Spear Phishing" |
| `TARGETS` | THREAT_ACTOR | SECTOR | Attacker targets sector | "APT28" TARGETS "Energy Sector" |
| `AFFECTS` | CVE | EQUIPMENT | Vulnerability affects equipment | "CVE-2024-1234" AFFECTS "Siemens PLC" |
| `LOCATED_IN` | EQUIPMENT | FACILITY | Equipment located at facility | "PLC" LOCATED_IN "Nuclear plant" |
| `BELONGS_TO` | FACILITY | SECTOR | Facility part of sector | "Power plant" BELONGS_TO "Energy Sector" |
| `CONTROLS` | EQUIPMENT | PROCESS | Equipment controls process | "PLC" CONTROLS "Batch production" |
| `MEASURES` | EQUIPMENT | MEASUREMENT | Equipment measures value | "Sensor" MEASURES "100 psi" |
| `HAS_PROPERTY` | EQUIPMENT/PROCESS | PROPERTY | Entity has characteristic | "PLC" HAS_PROPERTY "Safety-critical" |
| `MITIGATES` | Technique/Control | CVE | Control mitigates vulnerability | "Network segmentation" MITIGATES "CVE-2024-1234" |

#### **Category C: Hybrid Relationships (6 types)**

| Relationship | Head Entity | Tail Entity | Description | Example |
|--------------|-------------|-------------|-------------|---------|
| `INCREASES_RISK` | COGNITIVE_BIAS | CVE/THREAT | Bias increases vulnerability | "Complacency" INCREASES_RISK "Unpatched CVE" |
| `EXPLOITED_VIA` | COGNITIVE_BIAS | TECHNIQUE | Bias exploited by technique | "Authority bias" EXPLOITED_VIA "Social Engineering" |
| `HISTORICALLY_LED_TO` | COGNITIVE_BIAS | Incident | Past pattern of bias→incident | "Normalcy bias" HISTORICALLY_LED_TO "Ukrainian grid attack" |
| `FUTURE_THREAT_TO` | FUTURE_THREAT | SECTOR | Emerging threat to sector | "AI attacks" FUTURE_THREAT_TO "Energy Sector" |
| `LEARNED_FROM` | SECURITY_CULTURE | HISTORICAL_PATTERN | Culture evolved from pattern | "Security-first" LEARNED_FROM "Past breaches" |
| `PREVENTS` | SECURITY_CULTURE | COGNITIVE_BIAS | Culture prevents bias | "Questioning culture" PREVENTS "Groupthink" |

### 5.2 Relationship Annotation Rules

#### 5.2.1 General Rules

1. **Directionality**: All relationships are directed (head → tail)
2. **Span Boundaries**: Head and tail must be valid entity spans
3. **Cross-Sentence**: Relationships can span multiple sentences (within same document)
4. **Maximum Distance**: Head and tail must be within 5 sentences of each other
5. **No Self-Loops**: Head ≠ Tail (same entity cannot relate to itself)

#### 5.2.2 Relationship Attributes

Each relationship annotation includes:

```json
{
  "head": 45,           // Character offset of head entity start
  "head_span": {
    "start": 45,
    "end": 58,
    "text": "normalcy bias",
    "label": "COGNITIVE_BIAS"
  },
  "tail": 120,          // Character offset of tail entity start
  "tail_span": {
    "start": 120,
    "end": 135,
    "text": "data breach",
    "label": "INCIDENT"  // May be unlabeled if not in entity schema
  },
  "label": "CAUSED_BY",
  "attributes": {
    "confidence": "high",      // Annotator confidence: low/medium/high
    "evidence": "explicit",    // explicit (stated) or implicit (inferred)
    "distance": 2              // Sentences between head and tail
  }
}
```

#### 5.2.3 Evidence Classification

**Explicit Evidence** (stated directly in text):
```
Text: "The normalcy bias caused the data breach."
Relationship: normalcy bias [CAUSED_BY] data breach
Evidence: explicit
```

**Implicit Evidence** (inferred from context):
```
Text: "Operators assumed the system was secure based on past stability.
       This assumption led to the breach when attackers exploited the vulnerability."
Relationship: normalcy bias [CAUSED_BY] data breach
Evidence: implicit
```

#### 5.2.4 Confidence Scoring

**High Confidence**:
- Explicit statement of relationship
- Clear causal language ("caused", "resulted in", "led to")
- No ambiguity in entity references

**Medium Confidence**:
- Implicit relationship with strong contextual evidence
- Some ambiguity in directionality
- Requires domain knowledge to infer

**Low Confidence**:
- Weak or speculative relationship
- Ambiguous entity references
- Requires significant inference

### 5.3 Relationship Annotation Interface

#### 5.3.1 Prodigy Custom Recipe

```python
# FILE: relation_recipe.py
"""
Custom Prodigy recipe for relationship annotation.
Supports 24 relationship types with attributes.
"""

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.util import split_string
from typing import List, Dict, Any

# Relationship schema
RELATION_LABELS = [
    # Psychological (8)
    "EXHIBITS", "CAUSED_BY", "INFLUENCED_BY", "PERCEIVES",
    "MOTIVATED_BY", "DEFENDS_WITH", "SHAPED_BY", "RESULTS_IN",

    # Technical (10)
    "EXPLOITS", "USES", "TARGETS", "AFFECTS", "LOCATED_IN",
    "BELONGS_TO", "CONTROLS", "MEASURES", "HAS_PROPERTY", "MITIGATES",

    # Hybrid (6)
    "INCREASES_RISK", "EXPLOITED_VIA", "HISTORICALLY_LED_TO",
    "FUTURE_THREAT_TO", "LEARNED_FROM", "PREVENTS"
]

@prodigy.recipe(
    "ics-relations",
    dataset=("Dataset to save annotations", "positional", None, str),
    source=("Source JSONL file", "positional", None, str),
    labels=("Relationship labels", "option", "l", split_string)
)
def ics_relations(
    dataset: str,
    source: str,
    labels: List[str] = RELATION_LABELS
):
    """
    Annotate relationships between entities in ICS security documents.

    Usage:
        prodigy ics-relations rel_dataset batch_00.jsonl -F relation_recipe.py
    """

    # Load pre-annotated entities (from previous NER step)
    stream = JSONL(source)

    # Add relationship annotation interface
    blocks = [
        {"view_id": "relations"},
        {"view_id": "text"}
    ]

    config = {
        "relations_span_labels": labels,
        "custom_theme": {
            "cardMaxWidth": 1200
        }
    }

    def add_options(example: Dict[str, Any]) -> Dict[str, Any]:
        """Add confidence and evidence options to each relationship."""
        example["options"] = [
            {"id": "confidence", "text": "Confidence Level"},
            {"id": "evidence", "text": "Evidence Type"}
        ]
        return example

    stream = (add_options(eg) for eg in stream)

    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": blocks,
        "config": config
    }
```

#### 5.3.2 Annotation Workflow Steps

**Step 1: Entity Pre-Annotation** (automated)
- Use pre-trained NER model or patterns to suggest entities
- Annotator reviews and corrects

**Step 2: Relationship Annotation** (manual)
1. View document with highlighted entities
2. Click head entity → click tail entity
3. Select relationship type from dropdown (24 options)
4. Set confidence level (high/medium/low)
5. Set evidence type (explicit/implicit)
6. Repeat for all relationships in document

**Step 3: Review & Validate** (automated + manual)
- Automated checks (see section 7.2)
- Independent validator reviews relationships
- Resolve disagreements through consensus

### 5.4 Relationship Schema Export Format

```json
{
  "relationship_schema_version": "1.0.0",
  "total_relationships": 24,
  "categories": {
    "psychological": 8,
    "technical": 10,
    "hybrid": 6
  },
  "relationships": [
    {
      "label": "CAUSED_BY",
      "category": "psychological",
      "head_entity": ["INCIDENT", "BREACH", "FAILURE"],
      "tail_entity": ["COGNITIVE_BIAS"],
      "description": "Incident resulted from bias",
      "directionality": "directed",
      "symmetry": false,
      "examples": [
        {
          "head": "data breach",
          "tail": "overconfidence bias",
          "context": "The data breach was caused by overconfidence in security measures."
        }
      ],
      "validation_rules": {
        "max_distance_sentences": 5,
        "require_evidence": true,
        "minimum_confidence": "medium"
      }
    }
    // ... all 24 relationships
  ]
}
```

---

## 6. Annotation Interface Configuration

### 6.1 Prodigy Setup Script

```bash
#!/bin/bash
# FILE: setup_prodigy.sh
# Setup Prodigy annotation environment for ICS corpus

set -e

echo "🔧 Setting up Prodigy annotation environment..."

# 1. Install Prodigy (requires license key)
if [ -z "$PRODIGY_LICENSE" ]; then
    echo "❌ Error: PRODIGY_LICENSE environment variable not set"
    echo "   Set license: export PRODIGY_LICENSE=YOUR_KEY"
    exit 1
fi

pip install prodigy=1.14.0 --extra-index-url https://PRODIGY_LICENSE:@download.prodi.gy

# 2. Install dependencies
pip install spacy==3.7.2 scikit-learn==1.4.0 pandas==2.1.4

# 3. Download spaCy model (for pre-annotation)
python -m spacy download en_core_web_trf

# 4. Create Prodigy project structure
mkdir -p annotation/{batches,datasets,exports,recipes,logs}

# 5. Initialize databases
prodigy db-in entities_db annotation/datasets/entities.jsonl
prodigy db-in relations_db annotation/datasets/relations.jsonl

# 6. Copy custom recipes
cp relation_recipe.py annotation/recipes/
cp quality_checks.py annotation/recipes/

# 7. Configure Prodigy
cat > prodigy.json <<EOF
{
  "db": "sqlite",
  "db_settings": {
    "sqlite": {
      "path": "annotation/prodigy.db"
    }
  },
  "custom_theme": {
    "cardMaxWidth": 1200,
    "labels": {
      "EQUIPMENT": "#FF6B6B",
      "CVE": "#FF9F43",
      "COGNITIVE_BIAS": "#E91E63",
      "THREAT_ACTOR": "#8E44AD"
    }
  },
  "auto_save": true,
  "instant_submit": false,
  "feed_overlap": false,
  "history_size": 50
}
EOF

echo "✅ Prodigy setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start entity annotation: prodigy ner.manual entities_dataset annotation/batches/batch_00.jsonl -l EQUIPMENT,CVE,..."
echo "  2. Start relation annotation: prodigy ics-relations rel_dataset annotation/batches/batch_00_entities.jsonl -F annotation/recipes/relation_recipe.py"
```

### 6.2 Entity Annotation Command Template

```bash
# Entity annotation for batch 00
prodigy ner.manual \
  entities_batch00 \
  annotation/batches/batch_00.jsonl \
  --label EQUIPMENT,CVE,SECTOR,COGNITIVE_BIAS,EMOTION,THREAT_PERCEPTION,ATTACKER_MOTIVATION,DEFENSE_MECHANISM,SECURITY_CULTURE,HISTORICAL_PATTERN,FUTURE_THREAT,ORGANIZATION,THREAT_ACTOR,TECHNIQUE,FACILITY,PROCESS,MEASUREMENT,PROPERTY \
  --patterns entity_patterns.jsonl \
  --highlight-chars
```

### 6.3 Relationship Annotation Command Template

```bash
# Relationship annotation for batch 00 (after entities are done)
prodigy ics-relations \
  relations_batch00 \
  annotation/batches/batch_00_entities.jsonl \
  -F annotation/recipes/relation_recipe.py
```

### 6.4 Pattern-Based Pre-Annotation

```python
# FILE: entity_patterns.jsonl
# Pre-annotation patterns for common entities

{"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "plc"}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "scada"}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "hmi"}]}
{"label": "EQUIPMENT", "pattern": [{"TEXT": {"REGEX": "S7-\\d{4}"}}]}
{"label": "SECTOR", "pattern": [{"LOWER": "energy"}, {"LOWER": "sector"}]}
{"label": "SECTOR", "pattern": [{"LOWER": "water"}, {"LOWER": "treatment"}]}
{"label": "TECHNIQUE", "pattern": [{"LOWER": "spear"}, {"LOWER": "phishing"}]}
{"label": "TECHNIQUE", "pattern": [{"LOWER": "lateral"}, {"LOWER": "movement"}]}
{"label": "COGNITIVE_BIAS", "pattern": [{"LOWER": "normalcy"}, {"LOWER": "bias"}]}
{"label": "COGNITIVE_BIAS", "pattern": [{"LOWER": "confirmation"}, {"LOWER": "bias"}]}
{"label": "COGNITIVE_BIAS", "pattern": [{"LOWER": "overconfidence"}]}
{"label": "THREAT_ACTOR", "pattern": [{"TEXT": {"REGEX": "APT\\d+"}}]}
{"label": "THREAT_ACTOR", "pattern": [{"LOWER": "sandworm"}]}
{"label": "ORGANIZATION", "pattern": [{"UPPER": "CISA"}]}
{"label": "ORGANIZATION", "pattern": [{"UPPER": "NIST"}]}
```

### 6.5 Annotation Guidelines Document

```markdown
# FILE: annotation/ANNOTATION_GUIDELINES_v1.md

# ICS Security Corpus Annotation Guidelines v1.0

## Overview
This document provides detailed instructions for annotating 678 ICS security documents with 18 entity types and 24 relationship types.

## Getting Started
1. Read this entire document before starting annotation
2. Complete training batch (batch_00 sample: 5 files)
3. Take annotation quiz (see section 10)
4. Begin assigned batches after passing quiz

## Entity Annotation Process
1. Read document completely (skim once)
2. Annotate entities in this order:
   - Technical entities first (EQUIPMENT, CVE, etc.)
   - Psychological entities second (COGNITIVE_BIAS, etc.)
3. Review and refine annotations
4. Submit batch

## Relationship Annotation Process
1. Review pre-annotated entities
2. Identify head entity
3. Scan forward (within 5 sentences) for tail entity
4. Select relationship type
5. Set confidence and evidence attributes
6. Review and submit

## Common Mistakes
1. ❌ Annotating "computer" as EQUIPMENT (too generic)
   ✅ Annotate "industrial control computer" as EQUIPMENT

2. ❌ Over-extending spans: "The Siemens S7-1200 PLC at the facility"
   ✅ Correct span: "Siemens S7-1200 PLC"

3. ❌ Missing implicit relationships
   ✅ Infer relationships from context when evidence is strong

## Entity-Specific Guidelines
[See Section 4.3 for detailed guidelines per entity]

## Quality Checklist
Before submitting each batch:
- [ ] All technical terms annotated
- [ ] All psychological concepts annotated
- [ ] Relationships have confidence scores
- [ ] No overlapping entity spans
- [ ] No entities crossing sentence boundaries (unless multiword)
- [ ] All CVEs have correct format

## Getting Help
- Slack channel: #annotation-questions
- Weekly office hours: Wednesdays 2-3pm
- Guidelines updates: Check weekly for version changes
```

---

## 7. Quality Control System

### 7.1 Three-Tier Quality Assurance

```
┌─────────────────────────────────────────────┐
│         QUALITY ASSURANCE SYSTEM            │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
   │ TIER 1  │ │ TIER 2  │ │ TIER 3  │
   │ Primary │ │Validator│ │   Test  │
   │Annotator│ │  Human  │ │  Agent  │
   └─────────┘ └─────────┘ └─────────┘
        │           │           │
        └───────────┴───────────┘
                    │
              ┌─────▼─────┐
              │ CONSENSUS │
              │  (IAA>85%)│
              └───────────┘
```

### 7.2 Automated Quality Checks

```python
# FILE: quality_checks.py
"""
Automated quality checks for ICS corpus annotations.
Validates entity boundaries, relationships, schema compliance.
"""

import spacy
from spacy.tokens import Doc, Span
from typing import List, Dict, Any, Tuple
import re

class QualityChecker:
    """Automated quality validation for annotations."""

    def __init__(self, entity_schema: Dict, relation_schema: Dict):
        self.entity_schema = entity_schema
        self.relation_schema = relation_schema
        self.errors = []
        self.warnings = []

    def validate_batch(self, annotations: List[Dict]) -> Tuple[bool, List[str]]:
        """
        Validate entire batch of annotations.

        Returns:
            (is_valid, error_messages)
        """
        self.errors = []
        self.warnings = []

        for doc_ann in annotations:
            self.validate_document(doc_ann)

        is_valid = len(self.errors) == 0
        all_messages = self.errors + self.warnings

        return is_valid, all_messages

    def validate_document(self, doc_ann: Dict) -> None:
        """Validate single document annotation."""
        # Check 1: Entity boundary validation
        self._check_entity_boundaries(doc_ann)

        # Check 2: Entity label validation
        self._check_entity_labels(doc_ann)

        # Check 3: Relationship validation
        self._check_relationships(doc_ann)

        # Check 4: Attribute validation
        self._check_attributes(doc_ann)

        # Check 5: Coverage validation
        self._check_coverage(doc_ann)

    def _check_entity_boundaries(self, doc_ann: Dict) -> None:
        """Validate entity span boundaries."""
        text = doc_ann["text"]
        spans = doc_ann.get("spans", [])

        for span in spans:
            start = span["start"]
            end = span["end"]
            span_text = span["text"]

            # Rule 1: Span must match actual text
            actual_text = text[start:end]
            if actual_text != span_text:
                self.errors.append(
                    f"Span mismatch: '{span_text}' != '{actual_text}' at {start}-{end}"
                )

            # Rule 2: No overlapping spans
            for other_span in spans:
                if other_span == span:
                    continue
                if self._spans_overlap(span, other_span):
                    self.errors.append(
                        f"Overlapping spans: '{span_text}' and '{other_span['text']}'"
                    )

            # Rule 3: No trailing/leading whitespace
            if span_text != span_text.strip():
                self.warnings.append(
                    f"Whitespace in span: '{span_text}' at {start}-{end}"
                )

            # Rule 4: No sentence-crossing (except for multiword entities)
            if '\n\n' in span_text and len(span_text.split()) < 10:
                self.warnings.append(
                    f"Span crosses paragraph: '{span_text}' at {start}-{end}"
                )

    def _check_entity_labels(self, doc_ann: Dict) -> None:
        """Validate entity labels against schema."""
        valid_labels = [e["label"] for e in self.entity_schema["entities"]]

        for span in doc_ann.get("spans", []):
            label = span["label"]
            if label not in valid_labels:
                self.errors.append(
                    f"Invalid label: '{label}' not in schema (valid: {valid_labels})"
                )

            # Label-specific validation
            if label == "CVE":
                self._validate_cve(span)
            elif label == "COGNITIVE_BIAS":
                self._validate_cognitive_bias(span)

    def _validate_cve(self, span: Dict) -> None:
        """Validate CVE format."""
        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        if not re.fullmatch(cve_pattern, span["text"]):
            self.errors.append(
                f"Invalid CVE format: '{span['text']}' (expected CVE-YYYY-NNNN)"
            )

    def _validate_cognitive_bias(self, span: Dict) -> None:
        """Validate cognitive bias has bias_type attribute."""
        attrs = span.get("attributes", {})
        if "bias_type" not in attrs:
            self.errors.append(
                f"COGNITIVE_BIAS missing bias_type attribute: '{span['text']}'"
            )
        else:
            # Validate bias_type is in 30-bias taxonomy
            valid_biases = [
                "normalcy_bias", "confirmation_bias", "overconfidence_bias",
                # ... all 30 biases
            ]
            if attrs["bias_type"] not in valid_biases:
                self.errors.append(
                    f"Invalid bias_type: '{attrs['bias_type']}' for '{span['text']}'"
                )

    def _check_relationships(self, doc_ann: Dict) -> None:
        """Validate relationships between entities."""
        relations = doc_ann.get("relations", [])
        spans = doc_ann.get("spans", [])

        # Create span lookup
        span_lookup = {span["token_start"]: span for span in spans}

        for rel in relations:
            # Rule 1: Head and tail must be valid entities
            head_token = rel["head"]
            tail_token = rel["tail"]

            if head_token not in span_lookup:
                self.errors.append(
                    f"Relationship head not found: token {head_token}"
                )
                continue
            if tail_token not in span_lookup:
                self.errors.append(
                    f"Relationship tail not found: token {tail_token}"
                )
                continue

            head_span = span_lookup[head_token]
            tail_span = span_lookup[tail_token]

            # Rule 2: Relationship type must be valid
            rel_label = rel["label"]
            valid_relations = [r["label"] for r in self.relation_schema["relationships"]]
            if rel_label not in valid_relations:
                self.errors.append(
                    f"Invalid relationship: '{rel_label}' not in schema"
                )

            # Rule 3: Entity types must match relationship schema
            rel_schema = next(
                (r for r in self.relation_schema["relationships"] if r["label"] == rel_label),
                None
            )
            if rel_schema:
                head_label = head_span["label"]
                tail_label = tail_span["label"]

                if head_label not in rel_schema["head_entity"]:
                    self.warnings.append(
                        f"Unusual head entity for {rel_label}: {head_label} "
                        f"(expected {rel_schema['head_entity']})"
                    )
                if tail_label not in rel_schema["tail_entity"]:
                    self.warnings.append(
                        f"Unusual tail entity for {rel_label}: {tail_label} "
                        f"(expected {rel_schema['tail_entity']})"
                    )

            # Rule 4: Distance constraint (max 5 sentences)
            distance = self._calculate_sentence_distance(
                doc_ann["text"], head_span["start"], tail_span["start"]
            )
            if distance > 5:
                self.warnings.append(
                    f"Long-distance relationship: {head_span['text']} → {tail_span['text']} "
                    f"({distance} sentences apart)"
                )

            # Rule 5: Required attributes
            attrs = rel.get("attributes", {})
            if "confidence" not in attrs:
                self.warnings.append(
                    f"Relationship missing confidence: {head_span['text']} → {tail_span['text']}"
                )
            if "evidence" not in attrs:
                self.warnings.append(
                    f"Relationship missing evidence type: {head_span['text']} → {tail_span['text']}"
                )

    def _check_attributes(self, doc_ann: Dict) -> None:
        """Validate entity and relationship attributes."""
        for span in doc_ann.get("spans", []):
            attrs = span.get("attributes", {})

            # Check for required attributes per entity type
            label = span["label"]
            if label == "COGNITIVE_BIAS":
                if "bias_type" not in attrs:
                    self.errors.append(
                        f"COGNITIVE_BIAS missing required attribute 'bias_type': {span['text']}"
                    )
            elif label == "THREAT_PERCEPTION":
                if "perception_type" not in attrs:
                    self.errors.append(
                        f"THREAT_PERCEPTION missing required attribute 'perception_type': {span['text']}"
                    )

    def _check_coverage(self, doc_ann: Dict) -> None:
        """Check annotation coverage and density."""
        text = doc_ann["text"]
        spans = doc_ann.get("spans", [])
        relations = doc_ann.get("relations", [])

        word_count = len(text.split())
        entity_count = len(spans)
        relation_count = len(relations)

        # Rule 1: Minimum entity density (at least 1 entity per 100 words)
        min_expected_entities = word_count / 100
        if entity_count < min_expected_entities:
            self.warnings.append(
                f"Low entity density: {entity_count} entities for {word_count} words "
                f"(expected >{min_expected_entities:.0f})"
            )

        # Rule 2: Relationship-entity ratio (at least 1 relation per 5 entities)
        min_expected_relations = entity_count / 5
        if relation_count < min_expected_relations and entity_count > 10:
            self.warnings.append(
                f"Low relationship density: {relation_count} relations for {entity_count} entities "
                f"(expected >{min_expected_relations:.0f})"
            )

        # Rule 3: Check for likely missed annotations
        # (Simple pattern-based check for common terms)
        common_terms = {
            "PLC": "EQUIPMENT",
            "SCADA": "EQUIPMENT",
            "CVE-": "CVE",
            "bias": "COGNITIVE_BIAS",
            "sector": "SECTOR"
        }

        for term, expected_label in common_terms.items():
            if term in text:
                # Check if annotated
                annotated = any(
                    term.lower() in span["text"].lower()
                    for span in spans
                    if span["label"] == expected_label
                )
                if not annotated:
                    self.warnings.append(
                        f"Possible missed annotation: '{term}' found but not annotated as {expected_label}"
                    )

    def _spans_overlap(self, span1: Dict, span2: Dict) -> bool:
        """Check if two spans overlap."""
        return not (span1["end"] <= span2["start"] or span2["end"] <= span1["start"])

    def _calculate_sentence_distance(self, text: str, start1: int, start2: int) -> int:
        """Calculate sentence distance between two character positions."""
        # Simple sentence splitting (not perfect, but good enough)
        sentences = re.split(r'[.!?]\s+', text)

        char_pos = 0
        sent1 = sent2 = -1

        for i, sent in enumerate(sentences):
            sent_len = len(sent) + 2  # +2 for separator
            if char_pos <= start1 < char_pos + sent_len:
                sent1 = i
            if char_pos <= start2 < char_pos + sent_len:
                sent2 = i
            char_pos += sent_len

        return abs(sent1 - sent2)

# Usage
if __name__ == "__main__":
    # Load schemas
    with open("entity_schema.json") as f:
        entity_schema = json.load(f)
    with open("relation_schema.json") as f:
        relation_schema = json.load(f)

    # Initialize checker
    checker = QualityChecker(entity_schema, relation_schema)

    # Load batch annotations
    with open("batch_00_annotated.jsonl") as f:
        annotations = [json.loads(line) for line in f]

    # Validate
    is_valid, messages = checker.validate_batch(annotations)

    if is_valid:
        print("✅ Batch passed all quality checks!")
    else:
        print(f"❌ Batch has {len([m for m in messages if 'Error' in m])} errors")
        print(f"⚠️  Batch has {len([m for m in messages if 'Warning' in m])} warnings")

        for msg in messages:
            print(f"  {msg}")
```

### 7.3 Inter-Annotator Agreement (IAA) Calculation

```python
# FILE: iaa_calculator.py
"""
Calculate Inter-Annotator Agreement for entity and relationship annotations.
Uses multiple metrics: Cohen's Kappa, F1, Exact Match.
"""

from sklearn.metrics import cohen_kappa_score, f1_score
from typing import List, Dict, Tuple, Set
import json

class IAACalculator:
    """Calculate agreement between two annotators."""

    def __init__(self, tolerance: int = 2):
        """
        Args:
            tolerance: Character tolerance for span matching (default 2)
        """
        self.tolerance = tolerance

    def calculate_entity_agreement(
        self,
        annotator1: List[Dict],
        annotator2: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate entity annotation agreement.

        Returns:
            {
                "exact_match": float,  # Exact span match
                "partial_match": float,  # Overlap match
                "label_agreement": float,  # Same label for matched spans
                "cohen_kappa": float,  # Cohen's Kappa
                "f1_score": float  # F1 score
            }
        """
        # Convert annotations to span sets
        spans1 = self._extract_spans(annotator1)
        spans2 = self._extract_spans(annotator2)

        # Exact match
        exact_matches = spans1 & spans2
        exact_match_score = len(exact_matches) / max(len(spans1), len(spans2))

        # Partial match (with tolerance)
        partial_matches = self._partial_match(spans1, spans2)
        partial_match_score = len(partial_matches) / max(len(spans1), len(spans2))

        # Label agreement (for matched spans)
        label_agreements = sum(
            1 for s1, s2 in partial_matches
            if s1[2] == s2[2]  # Same label
        )
        label_agreement_score = label_agreements / max(len(partial_matches), 1)

        # Cohen's Kappa (requires token-level labels)
        token_labels1, token_labels2 = self._tokenize_labels(annotator1, annotator2)
        cohen_kappa = cohen_kappa_score(token_labels1, token_labels2)

        # F1 Score (treating annotator1 as gold)
        precision = len(exact_matches) / max(len(spans2), 1)
        recall = len(exact_matches) / max(len(spans1), 1)
        f1 = 2 * precision * recall / max(precision + recall, 0.0001)

        return {
            "exact_match": exact_match_score,
            "partial_match": partial_match_score,
            "label_agreement": label_agreement_score,
            "cohen_kappa": cohen_kappa,
            "f1_score": f1
        }

    def calculate_relation_agreement(
        self,
        annotator1: List[Dict],
        annotator2: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate relationship annotation agreement.

        Returns:
            {
                "exact_match": float,  # Exact head-tail-label match
                "partial_match": float,  # Same entities, different label
                "directionality_agreement": float,  # Correct direction
                "label_agreement": float  # Same label for matched relations
            }
        """
        # Extract relations
        relations1 = self._extract_relations(annotator1)
        relations2 = self._extract_relations(annotator2)

        # Exact match (head, tail, label)
        exact_matches = relations1 & relations2
        exact_match_score = len(exact_matches) / max(len(relations1), len(relations2))

        # Partial match (head, tail, any label)
        partial_matches = self._partial_match_relations(relations1, relations2)
        partial_match_score = len(partial_matches) / max(len(relations1), len(relations2))

        # Directionality agreement
        correct_direction = sum(
            1 for r1, r2 in partial_matches
            if r1[:2] == r2[:2]  # Same (head, tail) order
        )
        directionality_score = correct_direction / max(len(partial_matches), 1)

        # Label agreement
        label_agreements = sum(
            1 for r1, r2 in partial_matches
            if r1[2] == r2[2]  # Same label
        )
        label_agreement_score = label_agreements / max(len(partial_matches), 1)

        return {
            "exact_match": exact_match_score,
            "partial_match": partial_match_score,
            "directionality_agreement": directionality_score,
            "label_agreement": label_agreement_score
        }

    def _extract_spans(self, annotations: List[Dict]) -> Set[Tuple]:
        """Extract spans as (start, end, label) tuples."""
        spans = set()
        for doc in annotations:
            for span in doc.get("spans", []):
                spans.add((span["start"], span["end"], span["label"]))
        return spans

    def _extract_relations(self, annotations: List[Dict]) -> Set[Tuple]:
        """Extract relations as (head_start, tail_start, label) tuples."""
        relations = set()
        for doc in annotations:
            for rel in doc.get("relations", []):
                # Get head and tail span starts
                head_span = next(
                    s for s in doc["spans"]
                    if s["token_start"] == rel["head"]
                )
                tail_span = next(
                    s for s in doc["spans"]
                    if s["token_start"] == rel["tail"]
                )
                relations.add((
                    head_span["start"],
                    tail_span["start"],
                    rel["label"]
                ))
        return relations

    def _partial_match(
        self,
        spans1: Set[Tuple],
        spans2: Set[Tuple]
    ) -> Set[Tuple[Tuple, Tuple]]:
        """Find partially matching spans (within tolerance)."""
        matches = set()
        for s1 in spans1:
            for s2 in spans2:
                if self._spans_overlap_with_tolerance(s1, s2):
                    matches.add((s1, s2))
        return matches

    def _spans_overlap_with_tolerance(
        self,
        span1: Tuple[int, int, str],
        span2: Tuple[int, int, str]
    ) -> bool:
        """Check if spans overlap within tolerance."""
        start1, end1, _ = span1
        start2, end2, _ = span2

        return not (
            end1 + self.tolerance < start2 or
            end2 + self.tolerance < start1
        )

    def _partial_match_relations(
        self,
        relations1: Set[Tuple],
        relations2: Set[Tuple]
    ) -> Set[Tuple[Tuple, Tuple]]:
        """Find relations with same entities (any label, any direction)."""
        matches = set()
        for r1 in relations1:
            head1, tail1, label1 = r1
            for r2 in relations2:
                head2, tail2, label2 = r2
                # Check if same entities (forward or reverse)
                if (abs(head1 - head2) <= self.tolerance and
                    abs(tail1 - tail2) <= self.tolerance):
                    matches.add((r1, r2))
                elif (abs(head1 - tail2) <= self.tolerance and
                      abs(tail1 - head2) <= self.tolerance):
                    matches.add((r1, r2))
        return matches

    def _tokenize_labels(
        self,
        annotations1: List[Dict],
        annotations2: List[Dict]
    ) -> Tuple[List[str], List[str]]:
        """
        Convert annotations to token-level labels for Cohen's Kappa.
        Uses BIO tagging scheme.
        """
        # Assumes annotations1 and annotations2 are for same documents
        labels1 = []
        labels2 = []

        for doc1, doc2 in zip(annotations1, annotations2):
            text = doc1["text"]
            tokens = text.split()  # Simple tokenization

            # Create token labels for annotator 1
            doc_labels1 = ["O"] * len(tokens)
            for span in doc1.get("spans", []):
                start_token = len(text[:span["start"]].split())
                end_token = len(text[:span["end"]].split())
                doc_labels1[start_token] = f"B-{span['label']}"
                for i in range(start_token + 1, end_token):
                    doc_labels1[i] = f"I-{span['label']}"

            # Create token labels for annotator 2
            doc_labels2 = ["O"] * len(tokens)
            for span in doc2.get("spans", []):
                start_token = len(text[:span["start"]].split())
                end_token = len(text[:span["end"]].split())
                doc_labels2[start_token] = f"B-{span['label']}"
                for i in range(start_token + 1, end_token):
                    doc_labels2[i] = f"I-{span['label']}"

            labels1.extend(doc_labels1)
            labels2.extend(doc_labels2)

        return labels1, labels2

# Usage
if __name__ == "__main__":
    calculator = IAACalculator(tolerance=2)

    # Load annotations from two annotators
    with open("batch_00_annotator1.jsonl") as f:
        annotator1 = [json.loads(line) for line in f]
    with open("batch_00_annotator2.jsonl") as f:
        annotator2 = [json.loads(line) for line in f]

    # Calculate entity agreement
    entity_agreement = calculator.calculate_entity_agreement(annotator1, annotator2)
    print("Entity Agreement:")
    for metric, score in entity_agreement.items():
        print(f"  {metric}: {score:.3f}")

    # Calculate relation agreement
    relation_agreement = calculator.calculate_relation_agreement(annotator1, annotator2)
    print("\nRelation Agreement:")
    for metric, score in relation_agreement.items():
        print(f"  {metric}: {score:.3f}")

    # Overall assessment
    avg_agreement = (entity_agreement["f1_score"] + relation_agreement["exact_match"]) / 2
    print(f"\n📊 Overall Agreement: {avg_agreement:.3f}")

    if avg_agreement >= 0.85:
        print("✅ Target IAA achieved (>0.85)")
    else:
        print(f"⚠️  Below target IAA ({avg_agreement:.3f} < 0.85)")
        print("   → Requires consensus review")
```

---

## 8. Validation Workflow

### 8.1 Validation Process Overview

```
PRIMARY ANNOTATION
    │
    ├─→ [AUTOMATED CHECKS] (quality_checks.py)
    │       ├─→ ✅ Pass → Continue
    │       └─→ ❌ Fail → Return to annotator
    │
    ├─→ [INDEPENDENT VALIDATOR] (Human review)
    │       ├─→ Review entities
    │       ├─→ Review relationships
    │       ├─→ Flag disagreements
    │       └─→ Submit validation
    │
    ├─→ [IAA CALCULATION] (iaa_calculator.py)
    │       ├─→ Calculate agreement scores
    │       ├─→ ✅ IAA >0.85 → Approve
    │       └─→ ❌ IAA <0.85 → Consensus review
    │
    ├─→ [CONSENSUS REVIEW] (if needed)
    │       ├─→ Annotator + Validator meet
    │       ├─→ Discuss disagreements
    │       ├─→ Reach consensus
    │       └─→ Update annotations
    │
    └─→ [FINAL APPROVAL]
            └─→ Batch marked complete
```

### 8.2 Independent Validator Protocol

**Validator Responsibilities**:
1. Review all entity annotations for accuracy
2. Review all relationship annotations for correctness
3. Flag any disagreements with primary annotator
4. DO NOT see primary annotator's work during initial review (blind validation)
5. Submit independent annotations for IAA calculation

**Validation Checklist** (per document):
```markdown
- [ ] All technical entities annotated correctly
- [ ] All psychological entities annotated correctly
- [ ] Entity boundaries are precise
- [ ] No missing entities (check guidelines)
- [ ] All relationships have head/tail entities
- [ ] Relationship types are appropriate
- [ ] Confidence scores are reasonable
- [ ] Evidence types are marked correctly
- [ ] No quality check errors
```

**Validation Timeline**:
- Primary annotation: 2-3 days per batch (50 files)
- Validation review: 1-2 days per batch
- Consensus (if needed): 0.5-1 day per batch
- **Total per batch**: 3.5-6 days

### 8.3 Consensus Review Process

**Trigger Conditions**:
- IAA <0.85 for entities OR relationships
- >10% disagreement on entity labels
- >15% disagreement on relationship types

**Consensus Meeting Protocol**:
1. **Preparation** (30 min before meeting):
   - Generate disagreement report (see script below)
   - Both parties review disagreements

2. **Meeting** (1-2 hours):
   - Discuss each disagreement
   - Refer to annotation guidelines
   - Decide consensus annotation
   - Document rationale for difficult cases

3. **Post-Meeting** (30 min):
   - Update annotations with consensus decisions
   - Recalculate IAA
   - Update guidelines if needed (for future batches)

**Disagreement Report Script**:

```python
# FILE: generate_disagreements.py
"""
Generate report of annotation disagreements between annotators.
"""

import json
from typing import List, Dict, Any
from iaa_calculator import IAACalculator

def generate_disagreement_report(
    annotator1: List[Dict],
    annotator2: List[Dict],
    output_file: str
) -> None:
    """Generate detailed disagreement report."""

    calculator = IAACalculator(tolerance=2)

    report = {
        "summary": {},
        "entity_disagreements": [],
        "relationship_disagreements": []
    }

    # Calculate overall agreement
    entity_agreement = calculator.calculate_entity_agreement(annotator1, annotator2)
    relation_agreement = calculator.calculate_relation_agreement(annotator1, annotator2)

    report["summary"] = {
        "entity_iaa": entity_agreement["f1_score"],
        "relation_iaa": relation_agreement["exact_match"],
        "overall_iaa": (entity_agreement["f1_score"] + relation_agreement["exact_match"]) / 2
    }

    # Find entity disagreements
    for doc1, doc2 in zip(annotator1, annotator2):
        doc_id = doc1["meta"]["doc_id"]

        spans1 = {(s["start"], s["end"], s["label"]) for s in doc1.get("spans", [])}
        spans2 = {(s["start"], s["end"], s["label"]) for s in doc2.get("spans", [])}

        # Only in annotator 1
        only_ann1 = spans1 - spans2
        for span in only_ann1:
            report["entity_disagreements"].append({
                "doc_id": doc_id,
                "type": "missing_in_annotator2",
                "span": {
                    "start": span[0],
                    "end": span[1],
                    "label": span[2],
                    "text": doc1["text"][span[0]:span[1]]
                }
            })

        # Only in annotator 2
        only_ann2 = spans2 - spans1
        for span in only_ann2:
            report["entity_disagreements"].append({
                "doc_id": doc_id,
                "type": "missing_in_annotator1",
                "span": {
                    "start": span[0],
                    "end": span[1],
                    "label": span[2],
                    "text": doc2["text"][span[0]:span[1]]
                }
            })

        # Label disagreements (same span, different label)
        for s1 in doc1.get("spans", []):
            for s2 in doc2.get("spans", []):
                if (abs(s1["start"] - s2["start"]) <= 2 and
                    abs(s1["end"] - s2["end"]) <= 2 and
                    s1["label"] != s2["label"]):
                    report["entity_disagreements"].append({
                        "doc_id": doc_id,
                        "type": "label_conflict",
                        "span": {
                            "text": s1["text"],
                            "annotator1_label": s1["label"],
                            "annotator2_label": s2["label"]
                        }
                    })

    # Find relationship disagreements
    # (Similar logic for relationships)

    # Write report
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    # Print summary
    print(f"\n📊 Disagreement Report")
    print(f"   Entity IAA: {report['summary']['entity_iaa']:.3f}")
    print(f"   Relation IAA: {report['summary']['relation_iaa']:.3f}")
    print(f"   Overall IAA: {report['summary']['overall_iaa']:.3f}")
    print(f"   Entity Disagreements: {len(report['entity_disagreements'])}")
    print(f"   Relation Disagreements: {len(report['relationship_disagreements'])}")
    print(f"\n   Report saved: {output_file}")

# Usage
if __name__ == "__main__":
    with open("batch_00_annotator1.jsonl") as f:
        annotator1 = [json.loads(line) for line in f]
    with open("batch_00_annotator2.jsonl") as f:
        annotator2 = [json.loads(line) for line in f]

    generate_disagreement_report(annotator1, annotator2, "batch_00_disagreements.json")
```

### 8.4 Validation Metrics Tracking

```python
# FILE: validation_metrics.json
{
  "corpus_validation_status": {
    "total_batches": 14,
    "completed_batches": 0,
    "in_progress_batches": 0,
    "pending_batches": 14
  },
  "quality_metrics": {
    "target_entity_iaa": 0.85,
    "target_relation_iaa": 0.85,
    "current_avg_entity_iaa": null,
    "current_avg_relation_iaa": null
  },
  "batch_metrics": [
    {
      "batch_id": "batch_00",
      "status": "completed",
      "primary_annotator": "annotator_1",
      "validator": "annotator_2",
      "annotation_date": "2025-12-01",
      "validation_date": "2025-12-03",
      "entity_iaa": 0.89,
      "relation_iaa": 0.87,
      "consensus_required": false,
      "quality_checks_passed": true,
      "files_annotated": 50
    }
    // ... all batches
  ],
  "annotator_performance": {
    "annotator_1": {
      "batches_completed": 7,
      "avg_entity_iaa": 0.88,
      "avg_relation_iaa": 0.86,
      "avg_time_per_batch_hours": 18.5
    },
    "annotator_2": {
      "batches_completed": 7,
      "avg_entity_iaa": 0.87,
      "avg_relation_iaa": 0.85,
      "avg_time_per_batch_hours": 20.2
    }
  }
}
```

---

## 9. Test & Verification Strategy

### 9.1 Automated Test Agent

```python
# FILE: test_agent.py
"""
Automated test agent for validating annotation quality.
Runs comprehensive checks on completed batches.
"""

import json
from typing import List, Dict, Any, Tuple
from quality_checks import QualityChecker
from iaa_calculator import IAACalculator
import spacy

class TestAgent:
    """Automated testing agent for annotation validation."""

    def __init__(self):
        self.quality_checker = None  # Initialized in run()
        self.iaa_calculator = IAACalculator(tolerance=2)
        self.nlp = spacy.load("en_core_web_trf")

    def run_full_test_suite(
        self,
        batch_file: str,
        entity_schema: Dict,
        relation_schema: Dict
    ) -> Dict[str, Any]:
        """
        Run complete test suite on annotation batch.

        Returns:
            Test results with pass/fail status and detailed metrics
        """
        self.quality_checker = QualityChecker(entity_schema, relation_schema)

        # Load annotations
        with open(batch_file) as f:
            annotations = [json.loads(line) for line in f]

        results = {
            "batch_file": batch_file,
            "total_documents": len(annotations),
            "tests": {}
        }

        # Test 1: Schema compliance
        results["tests"]["schema_compliance"] = self._test_schema_compliance(
            annotations, entity_schema, relation_schema
        )

        # Test 2: Quality checks
        results["tests"]["quality_checks"] = self._test_quality_checks(annotations)

        # Test 3: Coverage analysis
        results["tests"]["coverage"] = self._test_coverage(annotations)

        # Test 4: Entity distribution
        results["tests"]["entity_distribution"] = self._test_entity_distribution(
            annotations, entity_schema
        )

        # Test 5: Relationship validity
        results["tests"]["relationship_validity"] = self._test_relationship_validity(
            annotations, relation_schema
        )

        # Test 6: F1 score per entity type (if gold standard available)
        # results["tests"]["f1_scores"] = self._test_f1_scores(annotations, gold_standard)

        # Overall pass/fail
        all_passed = all(
            test_result["status"] == "pass"
            for test_result in results["tests"].values()
        )
        results["overall_status"] = "pass" if all_passed else "fail"

        return results

    def _test_schema_compliance(
        self,
        annotations: List[Dict],
        entity_schema: Dict,
        relation_schema: Dict
    ) -> Dict[str, Any]:
        """Test that all annotations comply with schema."""
        valid_entities = {e["label"] for e in entity_schema["entities"]}
        valid_relations = {r["label"] for r in relation_schema["relationships"]}

        entity_violations = []
        relation_violations = []

        for doc in annotations:
            # Check entity labels
            for span in doc.get("spans", []):
                if span["label"] not in valid_entities:
                    entity_violations.append({
                        "doc_id": doc["meta"]["doc_id"],
                        "invalid_label": span["label"],
                        "text": span["text"]
                    })

            # Check relationship labels
            for rel in doc.get("relations", []):
                if rel["label"] not in valid_relations:
                    relation_violations.append({
                        "doc_id": doc["meta"]["doc_id"],
                        "invalid_label": rel["label"]
                    })

        passed = len(entity_violations) == 0 and len(relation_violations) == 0

        return {
            "status": "pass" if passed else "fail",
            "entity_violations": entity_violations,
            "relation_violations": relation_violations,
            "total_violations": len(entity_violations) + len(relation_violations)
        }

    def _test_quality_checks(self, annotations: List[Dict]) -> Dict[str, Any]:
        """Run automated quality checks."""
        is_valid, messages = self.quality_checker.validate_batch(annotations)

        errors = [m for m in messages if "Error" in m]
        warnings = [m for m in messages if "Warning" in m]

        return {
            "status": "pass" if is_valid else "fail",
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings)
        }

    def _test_coverage(self, annotations: List[Dict]) -> Dict[str, Any]:
        """Test annotation coverage and density."""
        total_words = 0
        total_entities = 0
        total_relations = 0

        docs_below_threshold = []

        for doc in annotations:
            words = len(doc["text"].split())
            entities = len(doc.get("spans", []))
            relations = len(doc.get("relations", []))

            total_words += words
            total_entities += entities
            total_relations += relations

            # Check minimum thresholds
            min_expected_entities = words / 100
            if entities < min_expected_entities:
                docs_below_threshold.append({
                    "doc_id": doc["meta"]["doc_id"],
                    "words": words,
                    "entities": entities,
                    "expected_min": min_expected_entities
                })

        avg_entity_density = (total_entities / total_words) * 100
        avg_relation_density = (total_relations / total_entities) if total_entities > 0 else 0

        # Pass criteria: avg entity density >1% and <3% below threshold
        passed = avg_entity_density >= 1.0 and len(docs_below_threshold) < len(annotations) * 0.03

        return {
            "status": "pass" if passed else "fail",
            "avg_entity_density": avg_entity_density,
            "avg_relation_density": avg_relation_density,
            "docs_below_threshold": len(docs_below_threshold),
            "details": docs_below_threshold[:10]  # First 10 for brevity
        }

    def _test_entity_distribution(
        self,
        annotations: List[Dict],
        entity_schema: Dict
    ) -> Dict[str, Any]:
        """Test distribution of entity types."""
        entity_counts = {e["label"]: 0 for e in entity_schema["entities"]}

        for doc in annotations:
            for span in doc.get("spans", []):
                if span["label"] in entity_counts:
                    entity_counts[span["label"]] += 1

        # Check for missing entity types
        missing_entities = [label for label, count in entity_counts.items() if count == 0]

        # Check for imbalanced distribution (any type <1% of total)
        total_entities = sum(entity_counts.values())
        imbalanced_entities = [
            label for label, count in entity_counts.items()
            if count < total_entities * 0.01 and count > 0
        ]

        passed = len(missing_entities) == 0

        return {
            "status": "pass" if passed else "warning",
            "entity_counts": entity_counts,
            "missing_entities": missing_entities,
            "imbalanced_entities": imbalanced_entities,
            "total_entities": total_entities
        }

    def _test_relationship_validity(
        self,
        annotations: List[Dict],
        relation_schema: Dict
    ) -> Dict[str, Any]:
        """Test relationship annotation validity."""
        invalid_relations = []

        for doc in annotations:
            spans = {s["token_start"]: s for s in doc.get("spans", [])}

            for rel in doc.get("relations", []):
                # Check head and tail exist
                if rel["head"] not in spans or rel["tail"] not in spans:
                    invalid_relations.append({
                        "doc_id": doc["meta"]["doc_id"],
                        "issue": "missing_entity",
                        "relation": rel["label"]
                    })
                    continue

                # Check entity type compatibility
                head_label = spans[rel["head"]]["label"]
                tail_label = spans[rel["tail"]]["label"]

                rel_schema = next(
                    (r for r in relation_schema["relationships"] if r["label"] == rel["label"]),
                    None
                )

                if rel_schema:
                    if head_label not in rel_schema["head_entity"]:
                        invalid_relations.append({
                            "doc_id": doc["meta"]["doc_id"],
                            "issue": "invalid_head_type",
                            "relation": rel["label"],
                            "head_type": head_label,
                            "expected": rel_schema["head_entity"]
                        })

                    if tail_label not in rel_schema["tail_entity"]:
                        invalid_relations.append({
                            "doc_id": doc["meta"]["doc_id"],
                            "issue": "invalid_tail_type",
                            "relation": rel["label"],
                            "tail_type": tail_label,
                            "expected": rel_schema["tail_entity"]
                        })

        passed = len(invalid_relations) == 0

        return {
            "status": "pass" if passed else "fail",
            "invalid_relations": invalid_relations,
            "total_invalid": len(invalid_relations)
        }

# Usage
if __name__ == "__main__":
    # Load schemas
    with open("entity_schema.json") as f:
        entity_schema = json.load(f)
    with open("relation_schema.json") as f:
        relation_schema = json.load(f)

    # Initialize test agent
    agent = TestAgent()

    # Run tests
    results = agent.run_full_test_suite(
        "batch_00_final.jsonl",
        entity_schema,
        relation_schema
    )

    # Print results
    print(f"\n🧪 Test Agent Results")
    print(f"   Batch: {results['batch_file']}")
    print(f"   Overall Status: {results['overall_status'].upper()}")
    print(f"\n   Test Results:")

    for test_name, test_result in results["tests"].items():
        status_icon = "✅" if test_result["status"] == "pass" else "❌"
        print(f"   {status_icon} {test_name}: {test_result['status']}")

    # Save results
    with open("test_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n   Detailed results saved: test_results.json")
```

### 9.2 F1 Score Calculation Per Entity Type

```python
# FILE: calculate_f1_per_entity.py
"""
Calculate F1 score per entity type for annotated corpus.
Useful for evaluating annotation quality against gold standard.
"""

from sklearn.metrics import precision_recall_fscore_support
from typing import List, Dict, Tuple
import json

def calculate_f1_per_entity(
    predictions: List[Dict],
    gold_standard: List[Dict]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate precision, recall, F1 per entity type.

    Args:
        predictions: Annotated documents
        gold_standard: Gold standard annotations

    Returns:
        Dictionary with metrics per entity type
    """
    # Extract all entity labels
    all_labels = set()
    for doc in predictions + gold_standard:
        for span in doc.get("spans", []):
            all_labels.add(span["label"])

    # Convert to token-level predictions
    y_true, y_pred = convert_to_token_labels(gold_standard, predictions, all_labels)

    # Calculate metrics per label
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=list(all_labels), average=None, zero_division=0
    )

    results = {}
    for i, label in enumerate(all_labels):
        results[label] = {
            "precision": precision[i],
            "recall": recall[i],
            "f1_score": f1[i],
            "support": support[i]
        }

    # Calculate macro average
    macro_f1 = sum(r["f1_score"] for r in results.values()) / len(results)
    results["MACRO_AVG"] = {
        "precision": sum(r["precision"] for r in results.values()) / len(results),
        "recall": sum(r["recall"] for r in results.values()) / len(results),
        "f1_score": macro_f1
    }

    return results

def convert_to_token_labels(
    gold: List[Dict],
    pred: List[Dict],
    labels: set
) -> Tuple[List[str], List[str]]:
    """Convert span annotations to token-level BIO labels."""
    y_true = []
    y_pred = []

    for doc_gold, doc_pred in zip(gold, pred):
        text = doc_gold["text"]
        tokens = text.split()

        # Gold labels
        gold_labels = ["O"] * len(tokens)
        for span in doc_gold.get("spans", []):
            start_token = len(text[:span["start"]].split())
            end_token = len(text[:span["end"]].split())
            if start_token < len(tokens):
                gold_labels[start_token] = span["label"]
                for i in range(start_token + 1, min(end_token, len(tokens))):
                    gold_labels[i] = span["label"]

        # Predicted labels
        pred_labels = ["O"] * len(tokens)
        for span in doc_pred.get("spans", []):
            start_token = len(text[:span["start"]].split())
            end_token = len(text[:span["end"]].split())
            if start_token < len(tokens):
                pred_labels[start_token] = span["label"]
                for i in range(start_token + 1, min(end_token, len(tokens))):
                    pred_labels[i] = span["label"]

        y_true.extend(gold_labels)
        y_pred.extend(pred_labels)

    return y_true, y_pred

# Usage
if __name__ == "__main__":
    # Load annotations and gold standard
    with open("batch_00_annotated.jsonl") as f:
        predictions = [json.loads(line) for line in f]
    with open("batch_00_gold.jsonl") as f:
        gold_standard = [json.loads(line) for line in f]

    # Calculate F1 scores
    results = calculate_f1_per_entity(predictions, gold_standard)

    # Print results
    print("\n📊 F1 Scores Per Entity Type")
    print("─" * 60)
    print(f"{'Entity Type':<25} {'Precision':<12} {'Recall':<12} {'F1':<12}")
    print("─" * 60)

    for entity_type, metrics in sorted(results.items()):
        if entity_type != "MACRO_AVG":
            print(f"{entity_type:<25} {metrics['precision']:<12.3f} {metrics['recall']:<12.3f} {metrics['f1_score']:<12.3f}")

    print("─" * 60)
    print(f"{'MACRO AVERAGE':<25} {results['MACRO_AVG']['precision']:<12.3f} {results['MACRO_AVG']['recall']:<12.3f} {results['MACRO_AVG']['f1_score']:<12.3f}")
    print("─" * 60)
```

---

## 10. Team Roles & Responsibilities

### 10.1 Annotation Team Structure

**Recommended Team Size**: 3-4 people

**Roles**:

1. **Lead Annotator** (1 person)
   - Responsibilities:
     - Primary annotation for batches 1-7 (350 files)
     - Schema refinement and guideline updates
     - Quality gate oversight
     - Team coordination
   - Required Skills:
     - ICS security domain expertise
     - Psychology background (cognitive biases)
     - Attention to detail
   - Time Commitment: Full-time (40 hrs/week) for 12-16 weeks

2. **Validator/Secondary Annotator** (1 person)
   - Responsibilities:
     - Independent validation for all batches
     - Primary annotation for batches 8-14 (328 files)
     - Consensus review participation
     - IAA calculation and reporting
   - Required Skills:
     - Same as Lead Annotator
   - Time Commitment: Full-time (40 hrs/week) for 12-16 weeks

3. **Test Engineer** (1 person, part-time)
   - Responsibilities:
     - Automated test agent development
     - Quality check script maintenance
     - Batch testing and validation
     - Metrics tracking and reporting
   - Required Skills:
     - Python programming
     - NLP/annotation tools experience
     - Testing methodologies
   - Time Commitment: Part-time (20 hrs/week) for 12-16 weeks

4. **Project Manager** (1 person, part-time)
   - Responsibilities:
     - Timeline management
     - Resource allocation
     - Progress tracking
     - Stakeholder communication
   - Required Skills:
     - Project management
     - NLP project experience
   - Time Commitment: Part-time (10 hrs/week) for 12-16 weeks

### 10.2 Training Requirements

**Week 1: Onboarding (40 hours)**
- Day 1-2: Schema and guidelines study
  - Read complete annotation guidelines (Section 6.5)
  - Study entity and relationship schemas (Sections 4-5)
  - Review examples and common mistakes

- Day 3-4: Tool training
  - Prodigy interface walkthrough
  - Practice batch annotation (5 sample files)
  - Quality check tools familiarization

- Day 5: Assessment
  - Annotate test batch (10 files)
  - Take annotation quiz (see below)
  - Must achieve >80% agreement with gold standard

**Annotation Quiz** (required pass: 9/10):
1. What is the correct span for "Siemens S7-1200 PLC at the facility"?
2. How many cognitive bias categories are in the schema?
3. What is the maximum sentence distance for relationships?
4. What are the three threat perception types?
5. Name 3 MICE framework motivations.
6. What is the minimum IAA target?
7. When should a relationship be marked "implicit" evidence?
8. What is the correct CVE format?
9. Can entity spans overlap? (Yes/No)
10. What triggers a consensus review?

### 10.3 Work Schedule Template

**Typical 2-Week Sprint** (per batch):

| Day | Lead Annotator | Validator | Test Engineer | PM |
|-----|----------------|-----------|---------------|-----|
| Mon Week 1 | Start annotation batch N | Review batch N-1 | Setup batch N tests | Progress review |
| Tue-Thu Week 1 | Annotate batch N | Validate batch N-1 | Develop test scripts | Check blockers |
| Fri Week 1 | Complete batch N | Submit validation N-1 | Run automated tests | Weekly report |
| Mon Week 2 | Start batch N+1 | Calculate IAA batch N | Analyze test results | Review IAA scores |
| Tue Week 2 | Annotate batch N+1 | Consensus meeting (if needed) | Fix quality issues | Update timeline |
| Wed-Thu Week 2 | Annotate batch N+1 | Start validation batch N | Final batch N tests | Track metrics |
| Fri Week 2 | Complete batch N+1 | Submit validation N | Approve batch N | Sprint retrospective |

**Cadence**:
- 1 batch per week per annotator (50 files)
- 2-day validation turnaround
- 1-day consensus review (if needed)
- Total: 7 batches/annotator × 2 annotators = 14 batches in 8-10 weeks

---

## 11. Timeline & Milestones

### 11.1 Project Timeline (12-16 Weeks)

**Phase 1: Setup (Weeks 1-2)**
- Week 1: Tool setup, schema finalization, team onboarding
- Week 2: Training, pilot batch annotation, workflow validation

**Phase 2: Annotation (Weeks 3-12)**
- Weeks 3-7: Batches 1-7 (Lead Annotator primary)
- Weeks 8-12: Batches 8-14 (Validator primary)
- Parallel validation throughout

**Phase 3: Quality Assurance (Weeks 13-14)**
- Week 13: Final validation, consensus reviews
- Week 14: Complete testing, metrics analysis

**Phase 4: Export & Documentation (Weeks 15-16)**
- Week 15: spaCy DocBin export, format conversion
- Week 16: Documentation, handoff to model training team

### 11.2 Milestone Checklist

**Milestone 1: Setup Complete** (Week 2)
- [ ] Prodigy installed and configured
- [ ] 14 batches prepared (JSONL format)
- [ ] Entity and relationship schemas finalized
- [ ] Annotation guidelines v1.0 published
- [ ] Team trained and quiz passed
- [ ] Pilot batch annotated and validated

**Milestone 2: 50% Annotation Complete** (Week 7)
- [ ] Batches 1-7 annotated (350 files)
- [ ] All batches validated (IAA >0.85)
- [ ] No major schema changes needed
- [ ] Quality metrics on track

**Milestone 3: 100% Annotation Complete** (Week 12)
- [ ] All 678 files annotated
- [ ] All batches validated
- [ ] Average IAA >0.85
- [ ] All quality checks passed

**Milestone 4: Final QA Complete** (Week 14)
- [ ] All consensus reviews complete
- [ ] Test agent approvals (all batches)
- [ ] Final metrics calculated
- [ ] Guidelines v1.1 published (lessons learned)

**Milestone 5: Export Complete** (Week 16)
- [ ] spaCy DocBin format exported
- [ ] Entity and relationship statistics documented
- [ ] Annotation report published
- [ ] Training data handed off

### 11.3 Risk Management

**Risk 1: Low IAA (<0.85)**
- **Probability**: Medium
- **Impact**: High (delays project)
- **Mitigation**:
  - Thorough training (Week 1)
  - Pilot batch to identify issues early
  - Frequent consensus reviews
  - Guidelines updates based on feedback
- **Contingency**: Add third annotator for tie-breaking

**Risk 2: Schema Changes Mid-Project**
- **Probability**: Low-Medium
- **Impact**: High (re-annotation needed)
- **Mitigation**:
  - Extensive pilot batch (50 files) before bulk annotation
  - Schema freeze after Week 2
  - Change control process for schema updates
- **Contingency**: Only allow additive changes (new entity types, not modifications)

**Risk 3: Annotator Turnover**
- **Probability**: Low
- **Impact**: High (knowledge loss, delays)
- **Mitigation**:
  - Comprehensive written guidelines
  - Video training recordings
  - Cross-training between annotators
  - Knowledge base of difficult cases
- **Contingency**: 2-week onboarding for replacement annotator

**Risk 4: Tool Failures**
- **Probability**: Low
- **Impact**: Medium (productivity loss)
- **Mitigation**:
  - Prodigy license backup
  - Regular database backups (daily)
  - Label Studio as fallback tool
- **Contingency**: Switch to Label Studio within 2 days

**Risk 5: Scope Creep (New Entity Types)**
- **Probability**: Medium
- **Impact**: Medium (timeline extension)
- **Mitigation**:
  - Clear scope definition (18 entities, 24 relationships)
  - Change control board for scope changes
  - "Parking lot" for future enhancements
- **Contingency**: Defer new entity types to v2.0 of corpus

---

## 12. Technical Implementation

### 12.1 Complete Setup Script

```bash
#!/bin/bash
# FILE: complete_setup.sh
# Complete setup for ICS annotation workflow

set -e

echo "🚀 ICS Security Corpus Annotation - Complete Setup"
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 required"; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "❌ pip required"; exit 1; }

# Create project structure
echo "Creating project structure..."
mkdir -p annotation/{batches,datasets,exports,recipes,logs,schemas,reports}

# Install Python dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q prodigy==1.14.0 --extra-index-url https://$PRODIGY_LICENSE:@download.prodi.gy
pip install -q spacy==3.7.2 scikit-learn==1.4.0 pandas==2.1.4 jupyter==1.0.0

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_trf

# Create schemas
echo "Creating entity and relationship schemas..."
cat > annotation/schemas/entity_schema.json <<'EOF'
{
  "entity_schema_version": "1.0.0",
  "total_entities": 18,
  "entities": [
    {"label": "EQUIPMENT", "category": "technical", "color": "#FF6B6B"},
    {"label": "CVE", "category": "technical", "color": "#FF9F43"},
    {"label": "SECTOR", "category": "technical", "color": "#48C9B0"},
    {"label": "THREAT_ACTOR", "category": "technical", "color": "#8E44AD"},
    {"label": "TECHNIQUE", "category": "technical", "color": "#3498DB"},
    {"label": "ORGANIZATION", "category": "technical", "color": "#95A5A6"},
    {"label": "FACILITY", "category": "technical", "color": "#E74C3C"},
    {"label": "PROCESS", "category": "technical", "color": "#1ABC9C"},
    {"label": "MEASUREMENT", "category": "technical", "color": "#F39C12"},
    {"label": "PROPERTY", "category": "technical", "color": "#34495E"},
    {"label": "COGNITIVE_BIAS", "category": "psychological", "color": "#E91E63"},
    {"label": "EMOTION", "category": "psychological", "color": "#9C27B0"},
    {"label": "THREAT_PERCEPTION", "category": "psychological", "color": "#FF5722"},
    {"label": "ATTACKER_MOTIVATION", "category": "psychological", "color": "#795548"},
    {"label": "DEFENSE_MECHANISM", "category": "psychological", "color": "#607D8B"},
    {"label": "SECURITY_CULTURE", "category": "psychological", "color": "#009688"},
    {"label": "HISTORICAL_PATTERN", "category": "psychological", "color": "#FFC107"},
    {"label": "FUTURE_THREAT", "category": "psychological", "color": "#00BCD4"}
  ]
}
EOF

cat > annotation/schemas/relation_schema.json <<'EOF'
{
  "relationship_schema_version": "1.0.0",
  "total_relationships": 24,
  "relationships": [
    {"label": "EXHIBITS", "category": "psychological"},
    {"label": "CAUSED_BY", "category": "psychological"},
    {"label": "INFLUENCED_BY", "category": "psychological"},
    {"label": "PERCEIVES", "category": "psychological"},
    {"label": "MOTIVATED_BY", "category": "psychological"},
    {"label": "DEFENDS_WITH", "category": "psychological"},
    {"label": "SHAPED_BY", "category": "psychological"},
    {"label": "RESULTS_IN", "category": "psychological"},
    {"label": "EXPLOITS", "category": "technical"},
    {"label": "USES", "category": "technical"},
    {"label": "TARGETS", "category": "technical"},
    {"label": "AFFECTS", "category": "technical"},
    {"label": "LOCATED_IN", "category": "technical"},
    {"label": "BELONGS_TO", "category": "technical"},
    {"label": "CONTROLS", "category": "technical"},
    {"label": "MEASURES", "category": "technical"},
    {"label": "HAS_PROPERTY", "category": "technical"},
    {"label": "MITIGATES", "category": "technical"},
    {"label": "INCREASES_RISK", "category": "hybrid"},
    {"label": "EXPLOITED_VIA", "category": "hybrid"},
    {"label": "HISTORICALLY_LED_TO", "category": "hybrid"},
    {"label": "FUTURE_THREAT_TO", "category": "hybrid"},
    {"label": "LEARNED_FROM", "category": "hybrid"},
    {"label": "PREVENTS", "category": "hybrid"}
  ]
}
EOF

# Create pattern file
echo "Creating pre-annotation patterns..."
cat > annotation/entity_patterns.jsonl <<'EOF'
{"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "plc"}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "scada"}]}
{"label": "EQUIPMENT", "pattern": [{"LOWER": "hmi"}]}
{"label": "SECTOR", "pattern": [{"LOWER": "energy"}, {"LOWER": "sector"}]}
{"label": "COGNITIVE_BIAS", "pattern": [{"LOWER": "normalcy"}, {"LOWER": "bias"}]}
{"label": "COGNITIVE_BIAS", "pattern": [{"LOWER": "confirmation"}, {"LOWER": "bias"}]}
{"label": "THREAT_ACTOR", "pattern": [{"TEXT": {"REGEX": "APT\\d+"}}]}
EOF

# Configure Prodigy
echo "Configuring Prodigy..."
cat > prodigy.json <<'EOF'
{
  "db": "sqlite",
  "db_settings": {
    "sqlite": {
      "path": "annotation/prodigy.db"
    }
  },
  "custom_theme": {
    "cardMaxWidth": 1200,
    "labels": {
      "EQUIPMENT": "#FF6B6B",
      "CVE": "#FF9F43",
      "COGNITIVE_BIAS": "#E91E63",
      "THREAT_ACTOR": "#8E44AD"
    }
  }
}
EOF

# Copy Python scripts (assumes they exist in current directory)
echo "Copying Python scripts..."
cp prepare_corpus.py annotation/recipes/ 2>/dev/null || echo "⚠️  prepare_corpus.py not found"
cp relation_recipe.py annotation/recipes/ 2>/dev/null || echo "⚠️  relation_recipe.py not found"
cp quality_checks.py annotation/recipes/ 2>/dev/null || echo "⚠️  quality_checks.py not found"
cp iaa_calculator.py annotation/recipes/ 2>/dev/null || echo "⚠️  iaa_calculator.py not found"
cp test_agent.py annotation/recipes/ 2>/dev/null || echo "⚠️  test_agent.py not found"

# Create README
cat > annotation/README.md <<'EOF'
# ICS Security Corpus Annotation

## Quick Start

1. Prepare corpus:
   ```
   python annotation/recipes/prepare_corpus.py
   ```

2. Start entity annotation:
   ```
   prodigy ner.manual entities_batch00 annotation/batches/batch_00.jsonl --label EQUIPMENT,CVE,...
   ```

3. Start relationship annotation:
   ```
   prodigy ics-relations relations_batch00 annotation/batches/batch_00_entities.jsonl -F annotation/recipes/relation_recipe.py
   ```

## Documentation

See 03_ANNOTATION_WORKFLOW_v1.0.md for complete workflow details.
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Set PRODIGY_LICENSE environment variable"
echo "  2. Run: python annotation/recipes/prepare_corpus.py"
echo "  3. Start annotation: See annotation/README.md"
echo ""
echo "Project structure created in: ./annotation/"
