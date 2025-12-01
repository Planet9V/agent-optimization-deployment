# GAP-008 SCOPE DEFINITION - NER10 Training Upgrade

**File**: SCOPE_DEFINITION_GAP008.md
**Created**: 2025-11-19 00:00:00 UTC
**Version**: 1.0.0
**GAP**: GAP-008 (NER10 Training with Annotation Pipeline)
**Priority**: P2-MEDIUM
**Status**: DEFINITION PHASE

---

## EXECUTIVE SUMMARY

**Purpose**: Upgrade from NER9 to NER10 with comprehensive annotation pipeline and enhanced training data based on equipment deployments from GAP-004 and GAP-007

**Current State**:
- NER9: Current production model
- Training data: Exists but needs enhancement
- Annotation: Manual process, not formalized
- Equipment data: 1,600 nodes available (after GAP-007)

**Target State**:
- NER10: Production-ready model with improved F1 score
- Annotation pipeline: Automated/semi-automated process
- Training data: 1,000+ annotated examples
- Integration: Deployed to production pipeline

---

## SCOPE DEFINITION

### In-Scope

**1. Annotation Pipeline Development** ✅
- Research and select annotation tool (Label Studio, Prodigy, or BRAT)
- Design annotation schema for cybersecurity equipment entities
- Create annotation guidelines document
- Set up annotation environment
- Train annotators (if manual annotation required)

**2. Training Data Preparation** ✅
- Extract equipment descriptions from GAP-004 + GAP-007 (1,600 equipment)
- Generate synthetic training examples (augmentation)
- Annotate 500-1,000 examples (entities, attributes, relationships)
- Quality assurance for annotations (inter-annotator agreement)
- Split data: Train (80%), Dev (10%), Test (10%)

**3. NER10 Model Architecture** ✅
- Design transformer-based architecture (BERT/RoBERTa/DistilBERT)
- Implement model code (PyTorch or TensorFlow)
- Create training pipeline (data loading, batching, optimization)
- Configure hyperparameters (learning rate, batch size, epochs)
- Implement evaluation metrics (precision, recall, F1)

**4. Model Training** ✅
- Train NER10 model on annotated data
- Monitor training metrics (loss curves, accuracy)
- Perform hyperparameter tuning (grid search or Bayesian optimization)
- Implement early stopping (prevent overfitting)
- Save model checkpoints

**5. Evaluation & Comparison** ✅
- Evaluate NER10 on test set
- Compare NER10 vs NER9 performance
- Analyze entity-level performance (per equipment type)
- Generate performance report with charts

**6. Model Deployment** ✅
- Export trained model (ONNX or native format)
- Integrate with existing NER pipeline
- Create model API/service
- Deploy to production environment
- Monitor production performance

### Out-of-Scope

**NOT Included in GAP-008**:
- ❌ Relationship extraction (focus on entity recognition only)
- ❌ Multi-language support (English only)
- ❌ Real-time streaming (batch processing only)
- ❌ Active learning (future GAP-009)
- ❌ Model compression/quantization (future optimization)

---

## TECHNICAL REQUIREMENTS

### Annotation Tool Selection

**Option 1: Label Studio (RECOMMENDED)**
- ✅ Open-source, free
- ✅ Web-based UI
- ✅ NER annotation support
- ✅ Export to JSON, CoNLL formats
- ✅ Multi-user annotation
- ✅ Docker deployment

**Option 2: Prodigy**
- ✅ Advanced active learning
- ✅ Recipe-based workflows
- ❌ Commercial license ($390/year)
- ✅ spaCy integration

**Option 3: BRAT**
- ✅ Open-source
- ✅ Lightweight
- ❌ Older UI
- ❌ Limited export formats

**Decision**: Use Label Studio for cost-effectiveness and modern UI

### Entity Schema

**Equipment Entity Types**:
1. **EQUIPMENT** - Generic equipment entity
   - Attributes: equipmentId, name, type, sector
2. **FACILITY** - Facility/location entity
   - Attributes: facilityId, name, type, sector, coordinates
3. **TECH_SPEC** - Technical specification entity
   - Attributes: specType, value, unit
4. **CRITICALITY** - Criticality level entity
   - Attributes: level (high, medium, critical)
5. **SECTOR** - Infrastructure sector entity
   - Attributes: sectorName, CISA_category

**Annotation Format** (CoNLL-style):
```
Los	B-FACILITY
Angeles	I-FACILITY
Water	I-FACILITY
Treatment	I-FACILITY
Plant	I-FACILITY
operates	O
a	O
high-capacity	B-TECH_SPEC
reverse	I-TECH_SPEC
osmosis	I-TECH_SPEC
system	I-TECH_SPEC
(	O
EQ-WATER-10001	B-EQUIPMENT
)	O
.	O
```

### Training Data Sources

**Source 1: GAP-004/007 Equipment (Primary)**
- 1,600 equipment nodes with descriptions
- Extract: equipmentId, name, type, sector, metadata
- Generate: Natural language descriptions
- Example: "The Los Angeles Water Treatment Plant operates a high-capacity reverse osmosis system (EQ-WATER-10001) serving 4 million residents."

**Source 2: MITRE ATT&CK (Secondary)**
- Extract attack patterns mentioning equipment
- Augment with cybersecurity context
- Example: "Attackers compromised the SCADA system (EQ-WATER-10005) controlling water distribution valves."

**Source 3: CVE Descriptions (Tertiary)**
- Extract CVE descriptions with equipment references
- Link to specific equipment types
- Example: "CVE-2024-1234 affects Siemens S7-1200 PLCs commonly used in chemical processing facilities."

**Source 4: Synthetic Generation (Augmentation)**
- Template-based generation
- Variation techniques (synonym replacement, paraphrasing)
- Target: 2,000-3,000 total examples (1,000 real + 1,000-2,000 synthetic)

### Model Architecture

**Base Model**: DistilBERT (distilbert-base-uncased)
- **Why**: Balance of performance and speed
- **Params**: 66M (vs BERT 110M)
- **Speed**: 2x faster than BERT
- **Accuracy**: 97% of BERT performance

**Fine-Tuning Approach**:
```python
# Pseudo-architecture
class NER10Model:
    def __init__(self):
        self.base_model = DistilBertForTokenClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=len(entity_labels)  # B-EQUIPMENT, I-EQUIPMENT, etc.
        )
        self.dropout = 0.1
        self.learning_rate = 2e-5

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        return outputs
```

**Training Configuration**:
- Learning rate: 2e-5 (standard for BERT fine-tuning)
- Batch size: 16 (GPU memory dependent)
- Epochs: 3-5 (with early stopping)
- Optimizer: AdamW
- Loss: CrossEntropyLoss
- Evaluation: Precision, Recall, F1 (entity-level)

---

## EXECUTION PHASES

### Phase 1: Annotation Pipeline (8 hours)

**Tasks**:
1. Install Label Studio (Docker): 30 minutes
2. Configure Label Studio for NER: 1 hour
3. Create annotation schema: 1 hour
4. Write annotation guidelines: 2 hours
5. Import equipment data: 1 hour
6. Test annotation workflow: 30 minutes
7. Document pipeline: 1 hour
8. Train annotators (if needed): 1 hour

**TASKMASTER**: 8 tasks

**Deliverables**:
- Label Studio running on `localhost:8080`
- Annotation schema configured
- Guidelines document (50+ pages)
- Equipment data imported (1,600 descriptions)

### Phase 2: Training Data Preparation (12 hours)

**Tasks**:
1. Extract equipment descriptions (GAP-007): 2 hours
2. Generate synthetic examples: 3 hours
3. Annotate 500 examples (manual): 4 hours
4. Quality assurance (IAA >0.8): 1 hour
5. Train/dev/test split: 30 minutes
6. Convert to model input format: 1 hour
7. Validate data quality: 30 minutes
8. Document dataset: 30 minutes

**TASKMASTER**: 8 tasks

**Deliverables**:
- `data/ner10/train.json` (800 examples)
- `data/ner10/dev.json` (100 examples)
- `data/ner10/test.json` (100 examples)
- `data/ner10/README.md` (dataset documentation)

### Phase 3: Model Architecture (10 hours)

**Tasks**:
1. Set up PyTorch environment: 1 hour
2. Implement NER10Model class: 3 hours
3. Create data loaders: 2 hours
4. Implement training loop: 2 hours
5. Implement evaluation metrics: 1 hour
6. Configure hyperparameters: 30 minutes
7. Test model pipeline: 30 minutes
8. Document architecture: 30 minutes

**TASKMASTER**: 8 tasks

**Deliverables**:
- `src/ner10/model.py` (NER10Model class)
- `src/ner10/data_loader.py` (DataLoader)
- `src/ner10/train.py` (Training script)
- `src/ner10/evaluate.py` (Evaluation script)
- `src/ner10/config.yaml` (Hyperparameters)

### Phase 4: Model Training (15 hours)

**Tasks**:
1. Initial training run (Epoch 1): 3 hours
2. Monitor and adjust: 1 hour
3. Epoch 2 training: 3 hours
4. Epoch 3 training: 3 hours
5. Hyperparameter tuning: 3 hours
6. Final training run: 2 hours

**TASKMASTER**: 6 tasks

**Monitoring**:
- Training loss curve
- Validation F1 score
- Per-entity performance
- GPU utilization
- Training time per epoch

**Deliverables**:
- `models/ner10_v1.0.0/model.pth` (trained model)
- `models/ner10_v1.0.0/training_log.txt`
- `models/ner10_v1.0.0/metrics.json`

### Phase 5: Evaluation & Deployment (5 hours)

**Tasks**:
1. Evaluate on test set: 1 hour
2. Compare NER10 vs NER9: 1 hour
3. Analyze per-entity performance: 1 hour
4. Deploy model to production: 1 hour
5. Create model documentation: 1 hour

**TASKMASTER**: 5 tasks

**Evaluation Metrics**:
- Overall F1: Target >0.85
- Per-entity F1: Target >0.80
- Precision: Target >0.85
- Recall: Target >0.82
- Improvement over NER9: Target +5% F1

**Deliverables**:
- `docs/gap_rebuild/GAP-008/ner10_evaluation_report.md`
- `docs/gap_rebuild/GAP-008/ner9_vs_ner10_comparison.md`
- `src/ner10/api/` (model serving API)

---

## RESOURCE REQUIREMENTS

### Compute Resources
- **CPU**: 8+ cores (for data processing)
- **RAM**: 16GB+ (for model training)
- **GPU**: Optional but recommended (10x speedup)
  - NVIDIA with CUDA 11.x+
  - 8GB+ VRAM
- **Storage**: 50GB (datasets + models + checkpoints)

### Software Dependencies
```yaml
python: ">=3.8"
pytorch: ">=2.0.0"
transformers: ">=4.30.0"
datasets: ">=2.12.0"
label-studio: ">=1.9.0"
scikit-learn: ">=1.3.0"
pandas: ">=2.0.0"
numpy: ">=1.24.0"
```

### Time Resources
- **Total Time**: 50 hours
- **Timeline**: 3-4 weeks (with GPU)
- **Timeline**: 5-6 weeks (CPU only)

---

## SUCCESS CRITERIA

**Phase 1 Success**:
- ✅ Label Studio operational
- ✅ Annotation schema configured
- ✅ Guidelines document complete
- ✅ Test annotation workflow successful

**Phase 2 Success**:
- ✅ 1,000+ annotated examples
- ✅ Train/dev/test split complete
- ✅ Inter-annotator agreement >0.8
- ✅ Data quality validated

**Phase 3 Success**:
- ✅ NER10Model implemented
- ✅ Training pipeline operational
- ✅ Evaluation metrics implemented
- ✅ Architecture documented

**Phase 4 Success**:
- ✅ Model trained (3-5 epochs)
- ✅ Training loss converged
- ✅ Validation F1 >0.80
- ✅ Model checkpoints saved

**Phase 5 Success**:
- ✅ Test F1 >0.85
- ✅ NER10 > NER9 (+5% F1)
- ✅ Model deployed to production
- ✅ Documentation complete

**Overall GAP-008 Success**:
- ✅ NER10 model operational
- ✅ F1 score improvement validated
- ✅ Production deployment successful
- ✅ Pipeline documented
- ✅ 6 git commits made

---

## INTEGRATION WITH OTHER GAPS

### Data Sources (Inputs)

**From GAP-004**:
- Equipment node descriptions
- Facility metadata
- Sector classifications
- Equipment type taxonomies

**From GAP-007**:
- 1,600 equipment nodes
- Geographic metadata
- 5-dimensional tagging
- Operational context

**From Existing Data**:
- MITRE ATT&CK patterns
- CVE descriptions
- Threat intelligence reports

### Data Consumers (Outputs)

**To Production Pipeline**:
- NER10 model for entity extraction
- Enhanced entity recognition in threat intel
- Improved equipment identification in logs

**To Future GAPs**:
- GAP-009: Active learning pipeline
- GAP-010: Relationship extraction
- GAP-011: Event correlation

---

## ANNOTATION SCHEMA DESIGN

### Entity Types (BIO Tagging)

**Primary Entities**:
1. **EQUIPMENT** - Physical or virtual equipment
   - Examples: "Siemens S7-1200 PLC", "reverse osmosis system"
   - Tags: B-EQUIPMENT, I-EQUIPMENT

2. **FACILITY** - Infrastructure facility
   - Examples: "Los Angeles Water Treatment Plant", "Memorial Hospital"
   - Tags: B-FACILITY, I-FACILITY

3. **TECH_SPEC** - Technical specifications
   - Examples: "high-capacity", "10Gbps network interface"
   - Tags: B-TECH_SPEC, I-TECH_SPEC

4. **VULNERABILITY** - Security vulnerabilities
   - Examples: "CVE-2024-1234", "authentication bypass"
   - Tags: B-VULN, I-VULN

5. **SECTOR** - Infrastructure sector
   - Examples: "Water sector", "Healthcare"
   - Tags: B-SECTOR, I-SECTOR

**Total Tags**: 11 (B/I for 5 entity types + O for outside)

### Annotation Guidelines (Summary)

**Equipment Entity Rules**:
- Include manufacturer and model number
- Include equipment type (PLC, SCADA, sensor)
- Exclude generic references ("the system")
- Handle acronyms (SCADA, HMI, RTU)

**Boundary Cases**:
- Nested entities: Annotate outermost span
- Coordinated entities: Annotate separately
- Partial mentions: Annotate if identifiable

---

## TRAINING DATA STATISTICS

### Target Dataset Composition

| Split | Examples | Tokens | Entities | Avg Entities/Example |
|-------|----------|--------|----------|---------------------|
| **Train** | 800 | ~240K | ~6,400 | 8 |
| **Dev** | 100 | ~30K | ~800 | 8 |
| **Test** | 100 | ~30K | ~800 | 8 |
| **TOTAL** | **1,000** | **~300K** | **~8,000** | **8** |

### Entity Distribution Target

| Entity Type | Count | Percentage | Examples |
|-------------|-------|------------|----------|
| **EQUIPMENT** | 4,000 | 50% | PLCs, sensors, SCADA systems |
| **FACILITY** | 2,000 | 25% | Plants, hospitals, substations |
| **TECH_SPEC** | 1,200 | 15% | Capacity, network specs, voltages |
| **VULNERABILITY** | 600 | 7.5% | CVEs, exploits, weaknesses |
| **SECTOR** | 200 | 2.5% | Water, Healthcare, Energy |
| **TOTAL** | **8,000** | **100%** | - |

---

## MODEL PERFORMANCE TARGETS

### Baseline (NER9)
- **Overall F1**: 0.80 (assumed, needs verification)
- **Precision**: 0.82
- **Recall**: 0.78
- **Entity-level**: 0.75-0.85 (varies by type)

### Target (NER10)
- **Overall F1**: >0.85 (+5% improvement)
- **Precision**: >0.87
- **Recall**: >0.83
- **Entity-level**: >0.80 (all types)

### Minimum Acceptable
- **Overall F1**: >0.82 (+2% improvement)
- **Precision**: >0.84
- **Recall**: >0.80
- **No degradation** on any entity type

---

## EXECUTION TIMELINE

### Week 1: Annotation Pipeline (8 hours)
**Day 1-2**:
- Install and configure Label Studio
- Design annotation schema
- Write annotation guidelines
- Import equipment data

**TASKMASTER Tracking**: 8 tasks, 1 commit

### Week 2-3: Training Data Preparation (12 hours)
**Day 1-2**: Extract and generate examples (5 hours)
**Day 3-5**: Annotation work (4 hours)
**Day 6-7**: QA and dataset split (3 hours)

**TASKMASTER Tracking**: 8 tasks, 1 commit

### Week 4: Model Development (10 hours)
**Day 1-2**: Environment setup and model implementation (5 hours)
**Day 3-4**: Training pipeline (4 hours)
**Day 5**: Testing and validation (1 hour)

**TASKMASTER Tracking**: 8 tasks, 1 commit

### Week 5-6: Training & Tuning (15 hours)
**Week 5**: Initial training (3 epochs, 9 hours)
**Week 6**: Hyperparameter tuning (6 hours)

**TASKMASTER Tracking**: 6 tasks, 1 commit

### Week 7: Evaluation & Deployment (5 hours)
**Day 1-2**: Evaluation and comparison (2 hours)
**Day 3**: Deployment (1 hour)
**Day 4-5**: Documentation and monitoring (2 hours)

**TASKMASTER Tracking**: 5 tasks, 2 commits

**Total Timeline**: 7 weeks, 50 hours

---

## DEPENDENCIES

### Requires (Blockers)
- ✅ GAP-004: Schema deployed (Equipment, Facility node types)
- ✅ GAP-007: Equipment deployment complete (1,600 nodes for training data)
- ✅ Python environment with PyTorch
- ✅ GPU access (optional but recommended)

### Enables (Downstream)
- GAP-009: Active learning for continuous improvement
- GAP-010: Relationship extraction
- Production NER pipeline enhancement

---

## RISK ANALYSIS

### Technical Risks

**Risk 1: Insufficient Training Data Quality**
- **Probability**: MEDIUM
- **Impact**: HIGH (poor model performance)
- **Mitigation**: Rigorous annotation QA, inter-annotator agreement >0.8
- **Contingency**: Generate more synthetic examples, use data augmentation

**Risk 2: Model Doesn't Improve Over NER9**
- **Probability**: LOW
- **Impact**: HIGH (wasted effort)
- **Mitigation**: Baseline NER9 first, iterative training with validation
- **Contingency**: Architectural changes, more training data

**Risk 3: Compute Resources Insufficient**
- **Probability**: MEDIUM
- **Impact**: MEDIUM (longer training time)
- **Mitigation**: Use cloud GPU (Colab, AWS, Azure)
- **Contingency**: Smaller model (DistilBERT → MobileBERT)

### Process Risks

**Risk 4: Annotation Too Time-Consuming**
- **Probability**: MEDIUM
- **Impact**: MEDIUM (timeline delay)
- **Mitigation**: Use pre-annotation with existing NER9, semi-automated workflow
- **Contingency**: Reduce dataset size to 500 examples

**Risk 5: Model Deployment Issues**
- **Probability**: LOW
- **Impact**: MEDIUM (production delay)
- **Mitigation**: Test deployment in staging first
- **Contingency**: Keep NER9 as fallback

---

## SUCCESS METRICS

### Annotation Quality
- ✅ Inter-annotator agreement: >0.8
- ✅ Annotation coverage: 100% of dataset
- ✅ Entity diversity: All 5 types represented
- ✅ Guidelines compliance: >95%

### Model Performance
- ✅ Test F1: >0.85
- ✅ Improvement over NER9: +5% F1
- ✅ Precision: >0.87
- ✅ Recall: >0.83
- ✅ No entity type <0.80 F1

### Deployment Success
- ✅ Model inference <100ms per example
- ✅ Production integration tested
- ✅ Monitoring operational
- ✅ Documentation complete

### Process Metrics
- ✅ 6 git commits made
- ✅ 35 TASKMASTER tasks tracked
- ✅ All phases documented
- ✅ Zero work loss

---

## DELIVERABLES CHECKLIST

### Code Deliverables
- [ ] `scripts/gap008_annotation/setup_label_studio.sh`
- [ ] `scripts/gap008_annotation/import_equipment_data.py`
- [ ] `src/ner10/model.py` (NER10Model class)
- [ ] `src/ner10/data_loader.py`
- [ ] `src/ner10/train.py`
- [ ] `src/ner10/evaluate.py`
- [ ] `src/ner10/inference.py`
- [ ] `src/ner10/api/app.py` (FastAPI service)

### Data Deliverables
- [ ] `data/ner10/train.json` (800 examples)
- [ ] `data/ner10/dev.json` (100 examples)
- [ ] `data/ner10/test.json` (100 examples)
- [ ] `data/ner10/annotation_guidelines.md` (50+ pages)
- [ ] `data/ner10/dataset_statistics.md`

### Model Deliverables
- [ ] `models/ner10_v1.0.0/model.pth`
- [ ] `models/ner10_v1.0.0/config.yaml`
- [ ] `models/ner10_v1.0.0/tokenizer/`
- [ ] `models/ner10_v1.0.0/training_log.txt`
- [ ] `models/ner10_v1.0.0/metrics.json`

### Documentation Deliverables
- [ ] `docs/gap_rebuild/GAP-008/annotation_pipeline_guide.md`
- [ ] `docs/gap_rebuild/GAP-008/training_data_report.md`
- [ ] `docs/gap_rebuild/GAP-008/model_architecture_design.md`
- [ ] `docs/gap_rebuild/GAP-008/training_report.md`
- [ ] `docs/gap_rebuild/GAP-008/ner9_vs_ner10_comparison.md`
- [ ] `docs/gap_rebuild/GAP-008/deployment_guide.md`

---

## NEXT STEPS

**After GAP-007 Complete**:
1. Extract equipment descriptions for annotation
2. Set up Label Studio environment
3. Begin Phase 1: Annotation Pipeline

**Weekly Checkpoints**:
- Week 1: Annotation pipeline operational
- Week 2-3: Training data prepared and validated
- Week 4: Model architecture implemented
- Week 5-6: Model trained and tuned
- Week 7: Model evaluated and deployed

**Final Milestone**:
- NER10 v1.0.0 deployed to production
- Performance improvement over NER9 validated
- Documentation complete
- TASKMASTER all tasks closed

---

**Scope Definition Status**: ✅ COMPLETE
**Ready for Execution**: After GAP-007
**Estimated Timeline**: 7 weeks, 50 hours
**Dependencies**: GAP-004 (schema), GAP-007 (equipment data)

---

*Scope defined with machine learning best practices and evidence-based planning*
*TASKMASTER integration: 35 tasks across 5 phases*
*Quality focus: Rigorous annotation, validated performance improvement, production deployment*
