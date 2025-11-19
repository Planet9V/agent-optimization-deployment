# Critical Infrastructure Sector Processing & Training Strategy
## AEON Digital Twin Enhancement Plan

**File:** CRITICAL_INFRASTRUCTURE_PROCESSING_STRATEGY.md
**Created:** 2025-11-02
**Version:** 1.0.0
**Purpose:** Comprehensive strategy for processing 13 critical infrastructure sectors (388 subsectors) with enhanced NER, embeddings, and graph integration
**Status:** ACTIVE

---

## Executive Summary

### Strategic Context
- **Scope:** 13 critical infrastructure sectors, 388 subsector variations
- **Timeline:** 24-hour subsector build-out cycle with continuous retraining capability
- **Current State:** 2 MD files processed (154 entities, 141 relationships, 89.2% precision)
- **Target State:** Full multi-format processing (PDF, DOCX, HTML, MD) with 92-97% precision

### Core Objectives
**Aligned with AEON Digital Twin 8-Layer Architecture:**

1. **Vulnerability Intelligence** → Enhanced entity extraction (CVE, CWE, CAPEC, ATT&CK)
2. **Software/Vendor Mapping** → Domain-specific NER for infrastructure vendors/products
3. **Attack Surface Analysis** → Relationship extraction (CONTROLS, MONITORS, PROTECTS)
4. **Threat Actor Profiling** → Integrate with existing psychometric layer
5. **Infrastructure Modeling** → SAREF ontology integration (Energy, Water, Manufacturing, Grid)
6. **Intelligence Gathering** → Multi-source document processing with confidence scoring
7. **Deployment Context** → Network/zone extraction from technical specifications
8. **Provenance Tracking** → Document source credibility and temporal tracking

### Strategic Goals
- **Digital Twin:** Enable real-time infrastructure vulnerability modeling
- **Threat Simulation:** Support adversarial simulation on sector-specific models
- **Knowledge Graph:** Enrich Neo4j with 3,000-5,000 entities per sector (39K-65K total)
- **Query Capability:** Answer complex cross-sector vulnerability questions

---

## RECOMMENDATION 1: Multi-Format Document Processing Enhancement

### Overview
Establish comprehensive document processing pipeline supporting PDF, DOCX, HTML→Markdown conversion with re-ranking capabilities.

### Technical Approach

#### Core Libraries
```python
processing_stack = {
    "pdf": {
        "primary": "PyMuPDF (fitz)",  # 90-95% precision, fastest
        "tables": "Camelot",            # 95%+ table extraction
        "fallback": "pdfplumber"        # 85-95% precision, layout-aware
    },
    "docx": {
        "primary": "python-docx",       # 95%+ precision
        "conversion": "mammoth",        # 90-95% → Markdown
    },
    "html": {
        "primary": "BeautifulSoup4",    # 95%+ extraction
        "conversion": "markdownify",    # 90-95% → Markdown
    },
    "universal": {
        "fallback": "pandoc",           # 95%+ for 50+ formats
    },
    "re_ranking": {
        "search": "sentence-transformers (all-mpnet-base-v2)",  # 90-95%
        "precision": "cross-encoder/ms-marco-MiniLM-L-12-v2",  # 92-97%
    }
}
```

#### Installation Script
```bash
#!/bin/bash
# install_processing_libraries.sh

# Create dedicated processing environment
python3 -m venv /tmp/doc_processing_env
source /tmp/doc_processing_env/bin/activate

# Core processing libraries
pip install PyMuPDF==1.23.8          # PDF processing (fast, accurate)
pip install pdfplumber==0.10.3       # PDF layout analysis
pip install camelot-py[cv]==0.11.0   # PDF table extraction
pip install python-docx==1.1.0       # DOCX processing
pip install mammoth==1.6.0           # DOCX → Markdown
pip install beautifulsoup4==4.12.2   # HTML processing
pip install lxml==4.9.3              # HTML parser
pip install markdownify==0.11.6      # HTML → Markdown
pip install sentence-transformers==2.2.2  # Re-ranking
pip install pandas==2.1.4            # Table handling
pip install openpyxl==3.1.2          # Excel support

# Optional: pandoc for universal conversion
# apt-get install pandoc  # System-level installation

echo "✅ Document processing libraries installed"
echo "📁 Environment: /tmp/doc_processing_env"
echo "🚀 Activate with: source /tmp/doc_processing_env/bin/activate"
```

#### Processing Pipeline Architecture
```python
class EnhancedDocumentProcessor:
    """Multi-format processor with Markdown conversion and re-ranking"""

    def process_document(self, file_path):
        """Route to appropriate processor"""
        ext = Path(file_path).suffix.lower()

        if ext == '.pdf':
            return self._process_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self._process_docx(file_path)
        elif ext in ['.html', '.htm']:
            return self._process_html(file_path)
        elif ext in ['.md', '.txt']:
            return self._process_text(file_path)

    def _process_pdf(self, pdf_path):
        """Extract PDF with PyMuPDF, tables with Camelot"""
        import fitz  # PyMuPDF
        import camelot

        # Extract text
        doc = fitz.open(pdf_path)
        text = "\n\n".join([page.get_text() for page in doc])

        # Extract tables
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        table_md = self._tables_to_markdown(tables)

        return text + "\n\n" + table_md

    def _process_docx(self, docx_path):
        """Convert DOCX to Markdown with mammoth"""
        import mammoth

        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            return result.value

    def _process_html(self, html_path):
        """Convert HTML to Markdown with markdownify"""
        from bs4 import BeautifulSoup
        from markdownify import markdownify as md

        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'lxml')
        return md(str(soup), heading_style="ATX")
```

### SWOT Analysis

#### Strengths
- ✅ **Comprehensive Format Coverage**: PDF, DOCX, HTML, MD, TXT (95%+ of sources)
- ✅ **High Fidelity**: PyMuPDF (90-95%), mammoth (90-95%), markdownify (90-95%)
- ✅ **Table Preservation**: Camelot achieves 95%+ accuracy on structured tables
- ✅ **Markdown Normalization**: Uniform format for downstream NER processing
- ✅ **Re-ranking Capability**: Cross-encoder boosts precision to 92-97%

#### Weaknesses
- ⚠️ **Library Dependencies**: Requires multiple external packages (12+ dependencies)
- ⚠️ **OCR Limitation**: Scanned PDFs require Tesseract (70-85% accuracy)
- ⚠️ **Complex Layouts**: Technical diagrams may lose structure in conversion
- ⚠️ **Processing Speed**: Camelot table extraction is slower (5-10 sec/page)
- ⚠️ **Memory Usage**: Large PDFs (>50MB) may require streaming approach

#### Opportunities
- 💡 **Incremental Reprocessing**: Update only changed documents in 24-hour cycle
- 💡 **Parallel Processing**: Batch process sectors concurrently (10-15x speedup)
- 💡 **Quality Metrics**: Track precision per format/sector for continuous improvement
- 💡 **Caching Layer**: Store processed Markdown to avoid reprocessing
- 💡 **Integration Testing**: Validate against existing MD processing (89.2% baseline)

#### Threats
- 🚨 **Format Evolution**: New document types may require additional libraries
- 🚨 **Dependency Conflicts**: Library version mismatches in production
- 🚨 **License Restrictions**: Some PDF extractors have restrictive licenses
- 🚨 **Security Risks**: Malformed PDFs could exploit extraction libraries
- 🚨 **Data Quality**: Poor source documents limit extraction accuracy

### Implementation Priority: **HIGH** (Weeks 1-2)

---

## RECOMMENDATION 2: spaCy NER Training Strategies

### Overview
Four strategic approaches for training domain-specific spaCy NER models across 13 sectors and 388 subsectors.

---

### APPROACH 2A: Domain-Specific Training (Sector-Isolated Models)

#### Strategy
Train dedicated spaCy models for each of 13 sectors with sector-specific entity types and patterns.

#### Architecture
```python
sector_models = {
    "energy": {
        "entities": ["VENDOR", "PROTOCOL", "STANDARD", "COMPONENT", "MEASUREMENT",
                     "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER", "REACTOR_TYPE"],
        "training_data_size": "800-1000 examples per entity type",
        "expected_precision": "94-98%",
        "training_time": "2-4 hours (CPU), 30-60 min (GPU)"
    },
    "water": {
        "entities": ["VENDOR", "PROTOCOL", "STANDARD", "COMPONENT", "MEASUREMENT",
                     "TREATMENT_PROCESS", "WATER_QUALITY_PARAM", "ASSET_TYPE"],
        "training_data_size": "800-1000 examples per entity type",
        "expected_precision": "94-98%",
        "training_time": "2-4 hours (CPU), 30-60 min (GPU)"
    },
    # ... 11 more sectors
}
```

#### Training Pipeline
```python
# config_energy.cfg
[nlp]
lang = "en"
pipeline = ["tok2vec", "ner"]

[components.ner]
factory = "ner"
labels = ["VENDOR", "PROTOCOL", "STANDARD", "COMPONENT", "MEASUREMENT",
          "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER", "REACTOR_TYPE"]

[training]
max_epochs = 100
patience = 10
eval_frequency = 200
dropout = 0.2
```

#### SWOT Analysis

**Strengths:**
- ✅ **Highest Precision**: 94-98% (sector-specific patterns captured)
- ✅ **Domain Optimization**: Each model tuned to sector terminology
- ✅ **Subsector Flexibility**: Easy to add subsector-specific entities (388 variations)
- ✅ **Independent Evolution**: Sectors can be retrained independently
- ✅ **Clear Ownership**: Sector experts can validate/improve their model

**Weaknesses:**
- ⚠️ **Training Cost**: 13 separate training sessions (26-52 hours CPU total)
- ⚠️ **Annotation Burden**: 800-1000 examples × 8-9 entity types × 13 sectors = 83K-117K annotations
- ⚠️ **Maintenance Overhead**: 13 models to update in 24-hour retraining cycle
- ⚠️ **Storage Requirements**: 13 × 100-150MB models = 1.3-2GB total
- ⚠️ **Cross-Sector Queries**: Requires model ensemble for multi-sector analysis

**Opportunities:**
- 💡 **Progressive Rollout**: Start with Energy (pilot), expand to others
- 💡 **Transfer Learning**: Fine-tune from `en_core_web_trf` base (reduce training time 50%)
- 💡 **Active Learning**: Use Prodigy for efficient annotation (30-50% reduction)
- 💡 **Crowd Annotation**: Distribute sector annotation to domain experts
- 💡 **Model Compression**: Distill to smaller models for production (50% size reduction)

**Threats:**
- 🚨 **Annotation Quality**: Inconsistent labeling across sectors degrades performance
- 🚨 **Overfitting Risk**: Small training sets may overfit to specific document styles
- 🚨 **Drift Over Time**: Models degrade as sector terminology evolves
- 🚨 **Expert Availability**: Requires 13 sector experts for quality annotation
- 🚨 **Version Fragmentation**: Managing 13 model versions becomes complex

**Implementation Priority:** **MEDIUM** (Weeks 3-8)
**Best For:** Organizations with sector expertise and annotation resources

---

### APPROACH 2B: Multi-Sector Shared Model (Unified Training)

#### Strategy
Train single spaCy model on combined data from all sectors, using shared entity types.

#### Architecture
```python
unified_model = {
    "entities": [
        # Universal entities (all sectors)
        "VENDOR", "PROTOCOL", "STANDARD", "COMPONENT", "MEASUREMENT",
        "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER",

        # Sector-tagged variants
        "COMPONENT_ENERGY", "COMPONENT_WATER", "COMPONENT_MANUFACTURING",
        # ... or use entity._.sector metadata
    ],
    "training_data_size": "10K-13K examples (combined across sectors)",
    "expected_precision": "88-93%",
    "training_time": "8-12 hours (CPU), 2-3 hours (GPU)"
}
```

#### Training Pipeline
```python
# config_unified.cfg
[nlp]
lang = "en"
pipeline = ["tok2vec", "ner", "entity_ruler"]

[components.ner]
factory = "ner"
labels = ["VENDOR", "PROTOCOL", "STANDARD", "COMPONENT", "MEASUREMENT",
          "ORGANIZATION", "SAFETY_CLASS", "SYSTEM_LAYER", "ASSET"]

[components.entity_ruler]
# Post-processing rules for sector-specific disambiguation
@misc = "spacy.EntityRuler.v1"
overwrite_ents = false
```

#### SWOT Analysis

**Strengths:**
- ✅ **Single Model Management**: One model to train/deploy/update
- ✅ **Cross-Sector Transfer**: Learns patterns applicable across domains
- ✅ **Reduced Annotation**: 10K-13K total examples vs 83K-117K for isolated models
- ✅ **Faster Retraining**: 8-12 hours vs 26-52 hours for sector-specific approach
- ✅ **Unified Queries**: Natural cross-sector analysis without model switching

**Weaknesses:**
- ⚠️ **Lower Precision**: 88-93% vs 94-98% for domain-specific models
- ⚠️ **Generic Patterns**: May miss sector-specific terminology nuances
- ⚠️ **Disambiguation Challenges**: "Reactor" means different things in Energy vs Chemical
- ⚠️ **Training Data Imbalance**: Sectors with more documents dominate patterns
- ⚠️ **Subsector Variation Loss**: 388 subsector variations harder to capture

**Opportunities:**
- 💡 **Entity Ruler Augmentation**: Add sector-specific pattern rules (90-93% → 92-95%)
- 💡 **Metadata Tagging**: Use custom attributes (`ent._.sector`) for disambiguation
- 💡 **Ensemble with Patterns**: Combine with regex patterns for high-confidence entities
- 💡 **Continuous Learning**: Incrementally update as new sectors/subsectors added
- 💡 **Bootstrap Approach**: Use unified model to pre-annotate sector-specific training data

**Threats:**
- 🚨 **Catastrophic Forgetting**: Retraining on new sectors degrades old sector performance
- 🚨 **Entity Ambiguity**: Cross-sector entity conflicts (e.g., "Grid" in Energy vs Network)
- 🚨 **Performance Degradation**: 88-93% may be insufficient for critical infrastructure analysis
- 🚨 **Subsector Explosion**: 388 variations strain single model capacity
- 🚨 **Retraining Coordination**: 24-hour cycle requires careful data versioning

**Implementation Priority:** **HIGH** (Weeks 2-4)
**Best For:** Rapid deployment with acceptable precision trade-offs

---

### APPROACH 2C: Hybrid Approach with Adapters

#### Strategy
Base model + sector-specific adapter layers for efficient specialization without full retraining.

#### Architecture
```python
hybrid_architecture = {
    "base_model": "en_core_web_trf (transformer-based)",
    "adapters": {
        "energy_adapter": {
            "parameters": "5-10% of base model size",
            "training_time": "1-2 hours (GPU)",
            "specialization": "Energy-specific entities and patterns"
        },
        "water_adapter": {
            "parameters": "5-10% of base model size",
            "training_time": "1-2 hours (GPU)",
            "specialization": "Water-specific entities and patterns"
        },
        # ... 11 more adapters
    },
    "total_storage": "Base (500MB) + 13 adapters × 25MB = 825MB",
    "expected_precision": "91-95%",
    "inference": "Dynamic adapter loading per sector"
}
```

#### Implementation Example
```python
# Using spaCy 3.x with custom adapter architecture
import spacy
from spacy.tokens import Doc

class SectorAdapter:
    """Lightweight sector-specific layer"""

    def __init__(self, sector_name, adapter_path):
        self.sector = sector_name
        self.adapter = self._load_adapter(adapter_path)

    def __call__(self, doc: Doc) -> Doc:
        """Apply sector-specific entity adjustments"""
        for ent in doc.ents:
            if self._is_sector_specific(ent):
                # Apply adapter transformations
                ent = self.adapter.transform(ent)
        return doc

# Usage:
nlp = spacy.load("en_core_web_trf")  # Base model
energy_adapter = SectorAdapter("energy", "adapters/energy.bin")
nlp.add_pipe("sector_adapter", last=True, config={"adapter": energy_adapter})
```

#### SWOT Analysis

**Strengths:**
- ✅ **Best of Both Worlds**: 91-95% precision (better than unified, cheaper than isolated)
- ✅ **Efficient Training**: 1-2 hours per adapter vs 2-4 hours per full model
- ✅ **Shared Base Knowledge**: Leverage pre-trained transformer embeddings
- ✅ **Modular Specialization**: Add/update sector adapters independently
- ✅ **Storage Efficient**: 825MB total vs 1.3-2GB for isolated models
- ✅ **24-Hour Retraining**: Only retrain affected adapter, not entire model

**Weaknesses:**
- ⚠️ **Complexity**: Requires custom spaCy architecture implementation
- ⚠️ **Adapter Development**: Need to build adapter training infrastructure
- ⚠️ **Base Model Dependency**: All adapters tied to base model version
- ⚠️ **Adapter Interference**: Multiple adapters may conflict if activated together
- ⚠️ **Limited Ecosystem**: Fewer tools/libraries for adapter-based NER

**Opportunities:**
- 💡 **Progressive Enhancement**: Start with base model, add adapters incrementally
- 💡 **Multi-Task Learning**: Share representations across related sectors (Energy/Grid)
- 💡 **Adapter Composition**: Combine multiple adapters for multi-sector documents
- 💡 **Community Adapters**: Open-source adapters for other researchers
- 💡 **Zero-Shot Generalization**: Base model handles unseen sectors reasonably

**Threats:**
- 🚨 **Maintenance Burden**: Custom architecture requires ongoing spaCy version updates
- 🚨 **Adapter Drift**: Base model updates may require adapter retraining
- 🚨 **Training Complexity**: Requires expertise in adapter-based transfer learning
- 🚨 **Debugging Difficulty**: Issues harder to diagnose with multi-layer architecture
- 🚨 **Performance Overhead**: Adapter switching adds inference latency

**Implementation Priority:** **HIGH** (Weeks 4-8)
**Best For:** Technical teams comfortable with advanced spaCy customization

---

### APPROACH 2D: Pattern-Enhanced Neural Hybrid

#### Strategy
Combine high-precision regex patterns for deterministic entities with neural NER for contextual entities.

#### Architecture
```python
hybrid_ner_pipeline = {
    "pattern_layer": {
        "entities": ["VENDOR", "PROTOCOL", "STANDARD", "MEASUREMENT"],  # High-confidence patterns
        "precision": "95-98%",
        "recall": "85-90%",
        "implementation": "spaCy EntityRuler"
    },
    "neural_layer": {
        "entities": ["COMPONENT", "ORGANIZATION", "ASSET", "PROCESS"],  # Contextual entities
        "precision": "85-92%",
        "recall": "90-95%",
        "implementation": "spaCy NER (en_core_web_trf + fine-tuning)"
    },
    "integration": "EntityRuler (patterns_first=True) → NER (neural)",
    "combined_precision": "92-96%",
    "combined_recall": "88-93%"
}
```

#### Implementation
```python
import spacy
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_trf")

# Add pattern-based entities FIRST (high precision)
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    # VENDOR patterns (95%+ precision)
    {"label": "VENDOR", "pattern": [{"LOWER": {"IN": ["westinghouse", "emerson", "schneider", "siemens", "rockwell"]}}]},

    # PROTOCOL patterns (95%+ precision)
    {"label": "PROTOCOL", "pattern": [{"TEXT": {"REGEX": r"(MQTT|OPC\s*UA|Modbus|DNP3|IEC\s*61850)"}}]},

    # STANDARD patterns (90%+ precision)
    {"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": r"(IEC|IEEE|ISO|NRC|NIST)[\s\-]*([\d\.\-]+[A-Z]*)"}}]},

    # MEASUREMENT patterns (98%+ precision)
    {"label": "MEASUREMENT", "pattern": [{"SHAPE": "ddd"}, {"LOWER": {"IN": ["mw", "mwe", "kv", "hz", "gpm", "psi"]}}]},
]
ruler.add_patterns(patterns)

# Neural NER handles contextual entities (components, organizations, processes)
# Already in pipeline, will NOT overwrite pattern-based entities
```

#### SWOT Analysis

**Strengths:**
- ✅ **Best Precision**: 92-96% combined (leverages strengths of both approaches)
- ✅ **Deterministic Core**: High-confidence entities (VENDOR, PROTOCOL) at 95-98%
- ✅ **Contextual Flexibility**: Neural layer handles ambiguous entities
- ✅ **No Training for Patterns**: Regex patterns work immediately (zero annotation cost)
- ✅ **Interpretability**: Pattern-based entities are fully explainable
- ✅ **Rapid Deployment**: Can deploy pattern layer immediately, add neural layer later

**Weaknesses:**
- ⚠️ **Pattern Maintenance**: 388 subsectors require extensive pattern libraries
- ⚠️ **Pattern Brittleness**: Regex fails on spelling variations, abbreviations
- ⚠️ **Neural Dependency**: Still requires training data for contextual entities
- ⚠️ **Integration Complexity**: Requires careful orchestration to avoid conflicts
- ⚠️ **Recall Limitation**: Patterns miss novel entity mentions (85-90% recall)

**Opportunities:**
- 💡 **Incremental Enhancement**: Start with patterns, add neural layer progressively
- 💡 **Pattern Generation**: Use LLMs to generate comprehensive pattern sets
- 💡 **Active Learning**: Use pattern matches to bootstrap neural training data
- 💡 **Confidence Scoring**: Combine pattern confidence (binary) with neural confidence (probabilistic)
- 💡 **Domain Expert Validation**: Experts can validate/update patterns easily

**Threats:**
- 🚨 **Pattern Explosion**: 388 subsectors × 8-9 entity types = 3,000+ patterns to maintain
- 🚨 **False Positives**: Overly broad patterns capture non-entities
- 🚨 **Entity Ambiguity**: "Reactor" pattern can't disambiguate Energy vs Chemical context
- 🚨 **Version Conflicts**: Pattern updates may conflict with neural model behavior
- 🚨 **Scalability Issues**: Large pattern sets degrade inference speed

**Implementation Priority:** **IMMEDIATE** (Week 1)
**Best For:** Rapid deployment with iterative improvement capability

---

### spaCy Training Recommendation Summary

| Approach | Precision | Training Time | Annotation Cost | Best For | Priority |
|----------|-----------|---------------|-----------------|----------|----------|
| **2A: Domain-Specific** | 94-98% | 26-52 hours | 83K-117K examples | Sector expertise available, highest precision required | MEDIUM |
| **2B: Multi-Sector Unified** | 88-93% | 8-12 hours | 10K-13K examples | Rapid deployment, acceptable precision trade-off | HIGH |
| **2C: Hybrid Adapters** | 91-95% | 13-26 hours | 20K-30K examples | Technical teams, modular architecture preferred | HIGH |
| **2D: Pattern-Neural Hybrid** | 92-96% | 4-8 hours | 5K-10K examples | Immediate deployment, deterministic core entities | **IMMEDIATE** |

**Recommended Strategy:** Start with **2D (Pattern-Neural Hybrid)** for immediate deployment (Week 1), transition to **2C (Hybrid Adapters)** for optimal long-term performance (Weeks 4-8).

---

## RECOMMENDATION 3: Embedding Model Training Strategy

### Overview
Train specialized embedding models for semantic search, relationship inference, and graph embeddings across the AEON Digital Twin 8-layer architecture.

### APPROACH 3A: Sentence Transformer Fine-Tuning

#### Strategy
Fine-tune pre-trained sentence transformers on domain-specific cybersecurity/infrastructure data.

#### Architecture
```python
embedding_strategy = {
    "base_model": "all-mpnet-base-v2",  # 420MB, 768 dimensions
    "fine_tuning_data": {
        "positive_pairs": "15K-20K sentence pairs from technical documents",
        "hard_negatives": "3-5 negatives per positive pair",
        "source": "Energy sector specs, CVE descriptions, MITRE ATT&CK, SAREF docs"
    },
    "training_approach": "Contrastive learning (MultipleNegativesRankingLoss)",
    "training_time": "6-12 hours (GPU)",
    "expected_improvement": "+5-10% retrieval precision over base model",
    "use_cases": [
        "Semantic search across 180K+ CVEs",
        "Similar vulnerability detection",
        "Cross-sector pattern matching",
        "Document clustering by attack vectors"
    ]
}
```

#### Training Pipeline
```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Load base model
model = SentenceTransformer('all-mpnet-base-v2')

# Prepare training data
train_examples = [
    InputExample(texts=['CVE-2024-1234 allows remote code execution',
                        'Unauthenticated RCE vulnerability in Apache Struts']),
    InputExample(texts=['Siemens PLC firmware update process',
                        'Rockwell PLC patch deployment methodology']),
    # ... 15K-20K pairs
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.MultipleNegativesRankingLoss(model)

# Fine-tune
model.fit(train_objectives=[(train_dataloader, train_loss)],
          epochs=4,
          warmup_steps=1000,
          output_path='./fine_tuned_cyber_embedding')
```

#### SWOT Analysis

**Strengths:**
- ✅ **Domain Adaptation**: Learns cybersecurity/infrastructure terminology
- ✅ **Semantic Search**: Enables "find similar vulnerabilities" queries
- ✅ **Cross-Sector Transfer**: Single model works across all 13 sectors
- ✅ **Pre-trained Foundation**: Leverages general language understanding
- ✅ **Moderate Training Cost**: 6-12 hours (GPU) for significant improvement

**Weaknesses:**
- ⚠️ **Data Collection**: Requires 15K-20K high-quality sentence pairs
- ⚠️ **Hard Negative Mining**: Finding good negatives is labor-intensive
- ⚠️ **Domain Drift**: Model may forget general language if over-specialized
- ⚠️ **Evaluation Complexity**: Need benchmark datasets to measure improvement
- ⚠️ **GPU Requirements**: Training requires CUDA-capable GPU (16GB+ VRAM)

**Opportunities:**
- 💡 **Synthetic Data Generation**: Use GPT-4 to generate training pairs
- 💡 **Active Learning**: Iteratively mine hard negatives from Neo4j queries
- 💡 **Multi-Task Learning**: Train on retrieval + classification simultaneously
- 💡 **Cross-Lingual Transfer**: Extend to non-English infrastructure documents
- 💡 **Continuous Learning**: Incrementally update as new CVEs/documents added

**Threats:**
- 🚨 **Overfitting Risk**: Model memorizes training data instead of generalizing
- 🚨 **Evaluation Bias**: Improvement metrics may not reflect real-world performance
- 🚨 **Resource Intensive**: GPU costs for training and inference
- 🚨 **Maintenance Burden**: Requires periodic retraining as domain evolves
- 🚨 **Alternative Embeddings**: OpenAI/Cohere embeddings may outperform custom models

**Implementation Priority:** MEDIUM (Weeks 6-10)

---

### APPROACH 3B: Graph Embeddings for Neo4j Integration

#### Strategy
Train heterogeneous graph embeddings specifically for the AEON 8-layer Neo4j schema.

#### Architecture
```python
graph_embedding_strategy = {
    "algorithm": "Heterogeneous Graph Neural Network (HetGNN)",
    "node_types": [
        "CVE", "CWE", "CAPEC", "Technique", "ThreatActor",      # Layers 1-4
        "SAREFDevice", "InformationSource", "Network", "Claim"   # Layers 5-8
    ],
    "edge_types": [
        "HAS_CWE", "USES_TECHNIQUE", "AFFECTS_SOFTWARE",
        "DEPLOYED_ON", "HAS_VULNERABILITY", "LOCATED_IN", "CITES"
    ],
    "embedding_dim": 256,
    "training_data": "Neo4j graph (180K nodes, 1M+ relationships)",
    "expected_use_cases": [
        "Vulnerability propagation prediction",
        "Attack path discovery",
        "Infrastructure risk scoring",
        "Threat actor similarity"
    ]
}
```

#### Implementation with Neo4j GDS
```python
from neo4j import GraphDatabase

# Neo4j Graph Data Science library
# Create graph projection
CREATE_PROJECTION = """
CALL gds.graph.project(
    'aeon-graph',
    ['CVE', 'CWE', 'CAPEC', 'Technique', 'SAREFDevice', 'Network'],
    {
        HAS_CWE: {orientation: 'UNDIRECTED'},
        USES_TECHNIQUE: {orientation: 'UNDIRECTED'},
        HAS_VULNERABILITY: {orientation: 'UNDIRECTED'},
        DEPLOYED_ON: {orientation: 'UNDIRECTED'}
    }
)
"""

# Train heterogeneous GraphSAGE embeddings
TRAIN_EMBEDDINGS = """
CALL gds.beta.graphSage.train(
    'aeon-graph',
    {
        modelName: 'aeon-embeddings',
        featureProperties: ['cvss_score', 'exploit_maturity', 'sector'],
        embeddingDimension: 256,
        epochs: 10,
        sampleSizes: [25, 10]
    }
)
"""

# Generate embeddings for all nodes
GENERATE_EMBEDDINGS = """
CALL gds.beta.graphSage.stream(
    'aeon-graph',
    {
        modelName: 'aeon-embeddings'
    }
)
YIELD nodeId, embedding
RETURN gds.util.asNode(nodeId).id AS entityId, embedding
"""
```

#### SWOT Analysis

**Strengths:**
- ✅ **Graph-Native**: Embeddings capture graph structure (CVE→CWE→ATT&CK paths)
- ✅ **Relationship-Aware**: Encodes multi-hop relationships natively
- ✅ **Heterogeneous Support**: Different node/edge types handled explicitly
- ✅ **Neo4j Integration**: Direct integration with existing database
- ✅ **Predictive Power**: Enables link prediction, node classification

**Weaknesses:**
- ⚠️ **Training Complexity**: Requires Neo4j GDS license (enterprise feature)
- ⚠️ **Cold Start Problem**: New nodes require retraining or feature engineering
- ⚠️ **Computational Cost**: Embedding 180K+ nodes is resource-intensive
- ⚠️ **Feature Engineering**: Requires node features (cvss_score, etc.) as input
- ⚠️ **Scalability**: Performance degrades with very large graphs (>1M nodes)

**Opportunities:**
- 💡 **Attack Path Prediction**: Predict likely attack chains before they occur
- 💡 **Vulnerability Clustering**: Automatically group similar CVEs
- 💡 **Infrastructure Risk Maps**: Visualize high-risk device clusters
- 💡 **Anomaly Detection**: Identify unusual relationships in threat data
- 💡 **Recommendation System**: Suggest relevant mitigations based on graph structure

**Threats:**
- 🚨 **License Costs**: Neo4j GDS enterprise license required (~$50K/year)
- 🚨 **Open-Source Alternatives**: PyTorch Geometric may offer similar capabilities free
- 🚨 **Embedding Drift**: Graph structure changes require frequent retraining
- 🚨 **Interpretability Loss**: Graph embeddings are less explainable than text embeddings
- 🚨 **Integration Overhead**: Coordinating embeddings with NER/document processing

**Implementation Priority:** LOW (Weeks 12-16, after core NER/document processing stable)

---

### Embedding Model Recommendation Summary

| Approach | Use Case | Training Time | Resource Needs | Priority |
|----------|----------|---------------|----------------|----------|
| **3A: Sentence Transformers** | Semantic search, document similarity | 6-12 hours | GPU (16GB), 15K pairs | **MEDIUM** |
| **3B: Graph Embeddings** | Attack path prediction, risk scoring | 4-8 hours | Neo4j GDS license, 180K nodes | LOW |

**Recommended Strategy:** Implement **3A (Sentence Transformers)** for immediate semantic search capability (Weeks 6-10). Defer **3B (Graph Embeddings)** until core data ingestion is stable (Weeks 12-16+).

---

## RECOMMENDATION 4: Sector-by-Sector Processing Plan

### Phase 1: Energy Sector (Pilot) - Weeks 1-4

#### Objectives
- Validate full processing pipeline on 55 Energy sector files
- Establish baseline metrics for other sectors
- Train initial spaCy model (Pattern-Neural Hybrid approach)
- Test re-ranking and quality metrics

#### Execution
```bash
# Week 1: Document Processing Setup
./install_processing_libraries.sh
python process_sector.py --sector energy --formats pdf,docx,html,md \
  --output-dir /tmp/energy_processed

# Week 2: spaCy Pattern Layer Deployment
python deploy_patterns.py --sector energy --entity-types VENDOR,PROTOCOL,STANDARD,COMPONENT

# Week 3: Neural NER Training (if needed)
python -m spacy train config_energy_neural.cfg \
  --output ./models/energy_neural \
  --paths.train energy_train.spacy \
  --paths.dev energy_dev.spacy

# Week 4: Neo4j Ingestion + Validation
python nlp_ingestion_pipeline.py /tmp/energy_processed \
  --neo4j-password $NEO4J_PWD \
  --spacy-model ./models/energy_hybrid
```

#### Success Metrics
- ✅ All 55 files processed (PDF, DOCX, HTML, MD)
- ✅ 3,000-5,000 unique entities extracted
- ✅ 92-96% precision (pattern-neural hybrid)
- ✅ 2,000-3,000 relationships inferred
- ✅ < 5% duplicate entity rate after deduplication

---

### Phase 2: Water & Manufacturing Sectors - Weeks 5-8

#### Objectives
- Apply validated pipeline to 2 additional sectors
- Test subsector variation handling (Energy has ~50 subsectors)
- Refine pattern libraries based on Energy learnings
- Begin multi-sector queries

#### Execution
```bash
# Parallel processing of Water and Manufacturing
./process_sector.py --sector water --use-energy-patterns --adapt
./process_sector.py --sector manufacturing --use-energy-patterns --adapt

# Validate cross-sector entity disambiguation
python validate_cross_sector.py --sectors energy,water,manufacturing
```

#### Success Metrics
- ✅ Water sector: 2,500-4,000 entities, 90-95% precision
- ✅ Manufacturing sector: 3,500-5,500 entities, 90-95% precision
- ✅ Cross-sector queries functional (e.g., "SCADA vulnerabilities across all sectors")
- ✅ Pattern library reuse >60% (Energy→Water, Energy→Manufacturing)

---

### Phase 3: Remaining 10 Sectors - Weeks 9-16

#### Execution Strategy
**Batch 1 (Weeks 9-12):** Transportation, Chemical, Communications, Healthcare
**Batch 2 (Weeks 13-16):** Critical Manufacturing, Commercial Facilities, Dams, Emergency Services, Food & Agriculture, Nuclear

#### Parallel Processing Architecture
```python
# Process 4 sectors concurrently (if resources allow)
from multiprocessing import Pool

sectors = ["transportation", "chemical", "communications", "healthcare"]

with Pool(processes=4) as pool:
    pool.map(process_sector_pipeline, sectors)
```

#### Success Metrics
- ✅ All 13 sectors processed and ingested into Neo4j
- ✅ 39K-65K total unique entities
- ✅ 25K-40K total relationships
- ✅ Average precision 91-95% across sectors
- ✅ Query response time <500ms for 5-hop graph queries

---

### Phase 4: 388 Subsector Integration - Weeks 17-24

#### Strategy
As subsectors are built out over the 24-hour cycle, incrementally process and integrate.

#### Subsector Handling Approach
```python
subsector_config = {
    "energy": {
        "nuclear_large": {"entity_additions": ["GEN_IV_REACTOR", "ADVANCED_SMR"]},
        "nuclear_medium": {"entity_additions": ["PWR", "BWR"]},
        "nuclear_small": {"entity_additions": ["MICRO_REACTOR"]},
        "solar_utility": {"entity_additions": ["INVERTER_TYPE", "PANEL_TECH"]},
        # ... 46 more energy subsectors
    },
    # ... 12 more sectors
}
```

#### Incremental Retraining
```bash
# Daily retraining script (triggered by new subsector additions)
#!/bin/bash
# retrain_daily.sh

# Detect new subsector files added in last 24 hours
NEW_FILES=$(find /sectors -name "*.md" -mtime -1)

if [ -n "$NEW_FILES" ]; then
    echo "New subsector files detected, retraining..."

    # Extract entities from new files
    python extract_entities.py --files "$NEW_FILES" --output new_training_data.jsonl

    # Incremental training (update existing model)
    python -m spacy train config.cfg \
      --output ./models/latest \
      --paths.train existing_train.spacy,new_training_data.jsonl \
      --initialize.init_tok2vec ./models/previous/tok2vec

    # Deploy updated model
    cp -r ./models/latest /production/models/active
fi
```

#### Success Metrics
- ✅ All 388 subsectors processed within 48 hours of creation
- ✅ Daily retraining completes in <2 hours
- ✅ No precision degradation with subsector additions (maintain 91-95%)
- ✅ Subsector-specific queries functional (e.g., "Gen IV reactor vulnerabilities")

---

### Processing Timeline Summary

| Phase | Weeks | Sectors | Output | Cumulative Entities |
|-------|-------|---------|--------|---------------------|
| **Phase 1: Energy Pilot** | 1-4 | Energy (55 files) | 3K-5K entities, pipeline validation | 3K-5K |
| **Phase 2: Expansion** | 5-8 | Water, Manufacturing | 6K-9.5K entities | 9K-14.5K |
| **Phase 3: Batch Rollout** | 9-16 | Remaining 10 sectors | 30K-50.5K entities | 39K-65K |
| **Phase 4: Subsectors** | 17-24 | 388 subsector variations | Incremental additions | 45K-75K |

---

## RECOMMENDATION 5: Alignment with AEON Digital Twin Goals

### Strategic Alignment Matrix

| AEON Layer | Enhanced Capability | Processing Impact | Entity Examples |
|------------|---------------------|-------------------|-----------------|
| **L1: Vulnerability Foundation** | CVE/CWE/CAPEC extraction from sector docs | +15K CVE mentions, +500 CWE references | CVE-2024-1234, CWE-89 |
| **L2: Software/Vendor** | Vendor/product NER at 95%+ precision | +2K vendor mentions, +5K product refs | Westinghouse, Emerson, Schneider |
| **L3: Threat Intelligence** | ATT&CK technique extraction | +800 technique mentions | T1190, T1078.001 |
| **L4: Threat Actor** | Integrate with existing psychometric layer | Reference threat actors in sector docs | (Existing layer) |
| **L5: SAREF Infrastructure** | Device/component extraction for 7 ontologies | +20K device mentions across sectors | SAREFDevice, WaterMeter, Generator |
| **L6: Social Media** | Document source credibility scoring | Provenance tracking for all docs | ConfidenceScore, SourceReputation |
| **L7: Network/Geospatial** | Zone/network extraction | +1K network zone mentions | DMZ, OT Network, Air-Gapped |
| **L8: Confidence/Provenance** | Precision metrics per entity type | Per-entity confidence scores | 0.92 (VENDOR), 0.88 (COMPONENT) |

### Digital Twin Simulation Enablement

#### Capability: Sector-Specific Threat Modeling
```cypher
// Example Query: Simulate ransomware attack on Energy sector
MATCH path = (cve:CVE)-[:HAS_CWE]->(cwe:CWE)-[:MAPS_TO]->(technique:Technique)
WHERE cve.sector = 'Energy' AND technique.tactic = 'Initial Access'
MATCH (device:SAREFDevice)-[:HAS_VULNERABILITY]->(cve)
WHERE device.sector = 'Energy' AND device.criticality = 'High'
RETURN path, device
ORDER BY cve.cvssV3BaseScore DESC
LIMIT 100
```

This query enables:
- 🎯 **Attack Surface Mapping:** Identify entry points in energy infrastructure
- 🎯 **Cascade Analysis:** Predict multi-hop attack paths through infrastructure
- 🎯 **Risk Prioritization:** Score devices by vulnerability + criticality
- 🎯 **Countermeasure Simulation:** Test mitigation effectiveness before deployment

#### Capability: Cross-Sector Dependency Analysis
```cypher
// Example Query: Map Energy-to-Water sector dependencies
MATCH (energy_device:SAREFDevice {sector: 'Energy'})
-[:SUPPLIES_POWER]->
(water_device:SAREFDevice {sector: 'Water'})
MATCH (water_device)-[:HAS_VULNERABILITY]->(cve:CVE)
RETURN energy_device, water_device, cve
```

Enables simulation of cascade failures (e.g., energy grid attack → water treatment disruption).

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- ✅ Install document processing libraries
- ✅ Deploy Pattern-Neural Hybrid NER (Recommendation 2D)
- ✅ Process Energy sector (55 files) as pilot
- ✅ Validate precision metrics (target: 92-96%)
- ✅ Ingest into Neo4j with relationship extraction

### Phase 2: Expansion (Weeks 5-8)
- ✅ Process Water and Manufacturing sectors
- ✅ Refine pattern libraries based on Energy learnings
- ✅ Test cross-sector queries
- ✅ Begin sentence transformer fine-tuning (optional)

### Phase 3: Scale-Out (Weeks 9-16)
- ✅ Process remaining 10 sectors in 2 batches
- ✅ Transition to Hybrid Adapter approach (Recommendation 2C) if needed
- ✅ Implement daily retraining pipeline for subsector additions
- ✅ Deploy re-ranking for improved semantic search

### Phase 4: Subsector Integration (Weeks 17-24)
- ✅ Process 388 subsector variations as they're created
- ✅ Incremental model updates (24-hour cycle)
- ✅ Advanced graph embeddings (optional, for attack path prediction)
- ✅ Full digital twin simulation capabilities online

### Phase 5: Continuous Improvement (Ongoing)
- ✅ Monitor precision metrics per sector/subsector
- ✅ Active learning for annotation efficiency
- ✅ Community feedback integration
- ✅ Quarterly model retraining with accumulated data

---

## Resource Requirements

### Personnel
- **NLP Engineer** (1 FTE, Weeks 1-16): spaCy training, embedding models
- **DevOps Engineer** (0.5 FTE, Weeks 1-24): Pipeline automation, Neo4j optimization
- **Domain Experts** (13 × 0.25 FTE, Weeks 2-8): Annotation validation per sector
- **Data Scientist** (0.5 FTE, Weeks 6-16): Embedding fine-tuning, re-ranking

### Infrastructure
- **Compute:** GPU instance (NVIDIA T4/V100, 16GB VRAM) for training - $1-2/hour × 100 hours = $100-200
- **Storage:** 500GB for processed documents + models = $10-20/month
- **Neo4j:** Enterprise license for GDS (optional) = $50K/year OR use Community + PyTorch Geometric (free)
- **Annotation Tools:** Prodigy license = $390/user OR use doccano (free)

### Total Budget Estimate
- **Minimal:** $500-1K (open-source tools, CPU training, no external annotation)
- **Optimal:** $5K-10K (GPU training, Prodigy, incremental expert validation)
- **Enterprise:** $60K+ (Neo4j GDS, full-time annotators, dedicated infrastructure)

---

## Success Metrics & KPIs

### Document Processing
- ✅ **Format Coverage:** 95%+ of documents processable (PDF, DOCX, HTML, MD)
- ✅ **Processing Speed:** 20-30 documents/hour (with GPU acceleration)
- ✅ **Markdown Fidelity:** 90-95% table preservation, 95%+ text accuracy

### Entity Extraction
- ✅ **Precision:** 92-96% (pattern-neural hybrid)
- ✅ **Recall:** 88-93% (estimated via manual validation on 500-sample subset)
- ✅ **Entity Yield:** 3K-5K entities per sector × 13 sectors = 39K-65K total
- ✅ **Deduplication Rate:** <5% duplicates after fuzzy matching

### Relationship Extraction
- ✅ **Relationship Density:** 0.5-0.8 relationships per entity
- ✅ **Relationship Types:** CONTROLS, MONITORS, PROTECTS, INTEGRATES_WITH, USES, COMPLIES_WITH
- ✅ **Cross-Sector Relationships:** 500-1K relationships linking different sectors

### Neo4j Integration
- ✅ **Query Performance:** <500ms for 5-hop graph traversals
- ✅ **Index Coverage:** 95%+ of entities indexed
- ✅ **Data Quality:** <2% broken relationships, <1% orphaned nodes

### Digital Twin Capabilities
- ✅ **Attack Path Queries:** Return results in <1 second for 3-hop attack chains
- ✅ **Vulnerability Coverage:** 95%+ of known CVEs linked to sector infrastructure
- ✅ **Simulation Accuracy:** 85%+ correlation with real-world attack patterns (validate against historical incidents)

---

## Risk Mitigation

### Technical Risks
- 🚨 **PDF Extraction Failures:** Mitigation: Multi-library fallback (PyMuPDF → pdfplumber → Camelot)
- 🚨 **spaCy Training Divergence:** Mitigation: Validation set monitoring, early stopping at 95% dev set accuracy
- 🚨 **Neo4j Performance Degradation:** Mitigation: Index optimization, query profiling, potential sharding for >1M nodes
- 🚨 **Model Drift:** Mitigation: Monthly precision audits, incremental retraining pipeline

### Operational Risks
- 🚨 **24-Hour Retraining Window:** Mitigation: Automated pipelines, failure notifications, rollback capability
- 🚨 **Annotation Quality:** Mitigation: Inter-annotator agreement metrics (>0.8 Cohen's kappa), expert review
- 🚨 **Resource Constraints:** Mitigation: Start with Pattern-Neural Hybrid (minimal resources), upgrade incrementally

### Strategic Risks
- 🚨 **Subsector Explosion:** Mitigation: Hierarchical annotation (sector → subsector inheritance), pattern reuse
- 🚨 **Cross-Sector Consistency:** Mitigation: Unified entity ontology, regular cross-sector validation queries

---

## Conclusion

This strategic plan provides **four complementary recommendations** for enhancing the AEON Digital Twin knowledge graph:

1. **Multi-Format Processing:** Achieve 95%+ document coverage with high-fidelity Markdown conversion
2. **spaCy NER Training:** Four approaches (Domain-Specific, Unified, Hybrid Adapters, Pattern-Neural) with detailed SWOT analysis
3. **Embedding Models:** Sentence transformers for semantic search, graph embeddings for attack prediction
4. **Sector-by-Sector Plan:** Phased rollout from Energy pilot (Weeks 1-4) to full 388 subsectors (Week 24)

**Recommended Immediate Actions:**
1. **Week 1:** Install processing libraries, deploy Pattern-Neural Hybrid NER
2. **Weeks 2-4:** Process Energy sector as pilot, validate precision metrics
3. **Weeks 5-8:** Expand to Water and Manufacturing, refine patterns
4. **Weeks 9-16:** Scale to all 13 sectors with parallel processing
5. **Weeks 17+:** Incremental subsector integration with daily retraining

This approach balances **rapid deployment** (Pattern-Neural Hybrid available Week 1) with **long-term optimization** (Hybrid Adapters by Week 8), aligned with the 24-hour subsector build cycle and AEON Digital Twin simulation goals.

**Next Steps:** Approval to proceed with Phase 1 (Foundation) and resource allocation for GPU training infrastructure.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-02
**Status:** PENDING APPROVAL
