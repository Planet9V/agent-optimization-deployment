# NER10 TASKMASTER - WEEKS 2-12 EXECUTION PROMPTS

**Purpose**: Copy/paste prompts for each remaining week
**Pattern**: Same as Week 1 - clear objectives, deliverables, validation
**Status**: Ready for sequential execution

---

## WEEK 2: ANNOTATION SPRINT - BATCH 1

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 2: ANNOTATION BATCH 1 (Files 1-100)

Objectives:
1. Annotate 100 high-priority files (Cognitive_Biases, Cybersecurity_Training)
2. Extract 18 entity types (8 psychological + 10 technical)
3. Annotate 20+ relationship types
4. Achieve inter-annotator agreement >0.85

Agent Swarm:
- Agent 1: Cognitive Bias Annotator (50 files)
- Agent 2: Equipment Entity Annotator (50 files)
- Agent 3: Relationship Annotator (all 100 files)
- Agent 4: Quality Validator (sample 20 files)
- Agent 5: Test Agent (verify F1 on 10 held-out files)

Tools:
- Prodigy for annotation interface
- Sequential-thinking for complex entity decisions
- Neural patterns for consistency

Deliverables:
- 100 files annotated (target: 1,500+ entities)
- Quality report (IAA >0.85 validation)
- Test results (F1 baseline on first batch)
- Qdrant storage (annotation metrics)

Validation:
- Test agent verifies 10 files
- Calculate IAA on overlapping annotations
- Verify all 18 entity types present
- Database: Store in Qdrant with week2-batch1 key

Update Wiki: Append progress to 15_NER10_Approach

Expected Time: 40-50 hours annotation
Expected Output: 100 annotated files + Week 3 prompt
```

---

## WEEK 3: ANNOTATION SPRINT - BATCH 2

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 3: ANNOTATION BATCH 2 (Files 101-250)

Objectives:
1. Annotate 150 files (all 16 CISA sectors)
2. Maintain IAA >0.85
3. Expand entity coverage (target: 3,000+ total entities)
4. Begin relationship annotation at scale

Agent Swarm:
- Agent 1-3: Parallel annotation (50 files each)
- Agent 4: Relationship specialist (150 files)
- Agent 5: Quality validator (sample 30 files)
- Agent 6: Test agent (verify on 15 held-out)

Deliverables:
- 150 files annotated (cumulative: 250/678 = 37%)
- Relationship coverage report (20+ types validated)
- IAA maintained >0.85
- F1 improvement tracking

Validation:
- Test agent verifies 15 files
- Compare Week 2 vs Week 3 IAA
- Verify relationship extraction quality
- Store in Qdrant with week3-batch2 key

Expected Time: 60-75 hours
Expected Output: 250 total annotated + Week 4 prompt
```

---

## WEEK 4: ANNOTATION COMPLETION + MODEL PREP

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 4: ANNOTATION COMPLETION

Objectives:
1. Complete remaining 428 files (250→678 = 100%)
2. Prepare training/dev/test splits (80/10/10)
3. Convert to spaCy DocBin format
4. Validate complete annotation coverage

Agent Swarm:
- Agent 1-5: Parallel annotation (85-86 files each)
- Agent 6: Data preparation specialist
- Agent 7: Split validator (stratified sampling)
- Agent 8: DocBin converter
- Agent 9: Final quality check
- Agent 10: Test agent (verify complete corpus)

Deliverables:
- 678/678 files annotated (100% ✅)
- Training: 542 files (80%)
- Dev: 68 files (10%)
- Test: 68 files (10%)
- DocBin files ready for spaCy

Validation:
- Verify all 18 entity types in test set
- Confirm stratification (entity distribution balanced)
- Test DocBin loading
- Calculate final IAA across full corpus
- Store in Qdrant with annotation-complete key

Expected Time: 170-210 hours (parallel execution)
Expected Output: Complete annotated corpus + Week 5 prompt
```

---

## WEEK 5: MODEL TRAINING - INITIAL

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 5: INITIAL MODEL TRAINING

Objectives:
1. Train NER10 model (base: en_core_web_trf)
2. 18 custom entity types
3. Target F1 >0.75 initial (will improve to >0.80)
4. GPU training (A100, 8-12 hours)

Agent Swarm:
- Agent 1: spaCy Trainer (execute training loop)
- Agent 2: Hyperparameter Tuner (optimize LR, batch size)
- Agent 3: F1 Monitor (track per-entity scores)
- Agent 4: Loss Analyzer (detect overfitting)
- Agent 5: Model Validator (test set evaluation)
- Agent 6: Test Agent (verify model loads, predicts)

Training Config:
- Batch size: 16
- Learning rate: 0.001
- Epochs: 30 (early stopping patience=5)
- Dropout: 0.3
- GPU: A100 40GB

Deliverables:
- NER10 model (v1.0)
- Training metrics (loss curves, F1 progression)
- Test set F1 scores (per entity type)
- Model artifacts (weights, config, vocab)
- Validation report

Validation:
- Test agent loads model
- Verify predictions on 20 unseen docs
- F1 >0.75 gate (must pass to continue)
- Store model metrics in Qdrant

Expected Time: 10-14 hours (training + validation)
Expected Output: NER10 v1.0 model + Week 6 prompt
```

---

## WEEK 6: MODEL OPTIMIZATION

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 6: MODEL OPTIMIZATION

Objectives:
1. Improve F1 from 0.75 to >0.80
2. Focus on weak entity types
3. Optimize hyperparameters
4. Validate on held-out data

Agent Swarm:
- Agent 1: Error Analyzer (identify weak entities)
- Agent 2: Data Augmenter (synthesize examples for weak types)
- Agent 3: Hyperparameter Tuner (grid search)
- Agent 4: Trainer (retrain with optimized config)
- Agent 5: Validator (test set evaluation)
- Agent 6: Test Agent (verify >0.80 F1)

Optimization Strategies:
- Increase weak entity training examples
- Adjust class weights
- Tune learning rate schedule
- Add context features

Deliverables:
- NER10 v2.0 (optimized model)
- F1 >0.80 per entity type
- Optimization report (what improved, why)
- Final test set evaluation

Validation:
- Test agent verifies F1 >0.80 on ALL entity types
- Precision >0.80, Recall >0.78
- No regression on strong entities
- Store final model in Qdrant

Expected Time: 12-16 hours
Expected Output: NER10 v2.0 (F1 >0.80) + Week 7 prompt
```

---

## WEEK 7-8: ENRICHMENT PIPELINE DEPLOYMENT

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEKS 7-8: ENRICHMENT PIPELINE

Objectives:
1. Deploy NER10 entity extraction pipeline
2. Process 678 annotated files + 400 cybersecurity reports
3. Extract 15,000-25,000 entities
4. Build initial relationships (20+ types)

Agent Swarm:
- Agent 1: Entity Extractor (process files with NER10)
- Agent 2: Entity Resolver (match to database nodes)
- Agent 3: Relationship Builder (construct 20+ types)
- Agent 4: Database Integrator (Neo4j insertion)
- Agent 5: Schema Validator (check 7-level alignment)
- Agent 6: Quality Monitor (track extraction F1)
- Agent 7: Test Agent (verify database state)

Pipeline Stages:
1. Text → NER10 → Entities (confidence >0.70)
2. Entities → Entity Resolution → Database IDs
3. Entities → Relationship Extraction → Graph edges
4. Graph → Neo4j Integration → Validation
5. Validation → Feedback → Correction Queue

Deliverables:
- 15,000-25,000 entities in Neo4j
- 20+ relationship types operational
- Entity extraction F1 report
- Database integration log
- Enrichment metrics

Validation:
- Test agent queries Neo4j (count entities by type)
- Verify 20+ relationship types exist
- Sample 100 entities for accuracy
- Calculate graph consistency score
- Store metrics in Qdrant

Expected Time: 80-100 hours (parallel processing)
Expected Output: Enriched database + Week 9 prompt
```

---

## WEEK 9-10: RELATIONSHIP BUILDER

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEKS 9-10: RELATIONSHIP BUILDER

Objectives:
1. Build deep 20+ relationship types
2. Create multi-hop paths (20+ hop capability)
3. Temporal relationship tracking
4. Causal chain construction

Agent Swarm:
- Agent 1: Grammatical Relationship Extractor
- Agent 2: Domain Pattern Matcher (EXHIBITS, CAUSED_BY, etc.)
- Agent 3: Temporal Relationship Builder (PRECEDES, FOLLOWS)
- Agent 4: Causal Chain Constructor (LEADS_TO, PREVENTS)
- Agent 5: Evidence Chain Builder (BASED_ON, SUPPORTS)
- Agent 6: Database Relationship Inserter
- Agent 7: Test Agent (verify relationship quality)

20+ Relationship Types:
- Psychological: EXHIBITS, CAUSED_BY, INFLUENCED_BY, ACTIVATES
- Technical: EXPLOITS, USES, TARGETS, AFFECTS, THREATENS
- Temporal: PRECEDES, FOLLOWS, RECURS_WITH
- Causal: LEADS_TO, PREVENTS, MITIGATES, ENABLES
- Evidence: BASED_ON, SUPPORTS, PREDICTS, INFORMS

Deliverables:
- 50,000-100,000 relationships created
- 20+ relationship types validated
- Multi-hop path analysis (up to 20 hops)
- Relationship extraction F1 >0.75
- Graph connectivity report

Validation:
- Test agent runs 20+ relationship queries
- Verify multi-hop traversals work
- Calculate relationship F1 scores
- Check schema compliance
- Store in Qdrant

Expected Time: 60-80 hours
Expected Output: Complete relationship graph + Week 11 prompt
```

---

## WEEK 11-12: REAL-TIME INGESTION APIS

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEKS 11-12: REAL-TIME APIs

Objectives:
1. Deploy real-time ingestion APIs
2. Integrate VulnCheck, NVD, MITRE, CISA, news sources
3. Enable continuous enrichment (<5 min latency)
4. Establish feedback loop for production

Agent Swarm:
- Agent 1: API Developer (FastAPI, webhooks)
- Agent 2: Kafka Queue Manager
- Agent 3: NER10 Processor (real-time extraction)
- Agent 4: Database Integrator (streaming inserts)
- Agent 5: Quality Monitor (track production F1)
- Agent 6: Feedback Loop Manager (corrections → retraining)
- Agent 7: Test Agent (end-to-end validation)

Data Sources:
- VulnCheck webhook (CVE updates)
- NVD polling (every 2 hours)
- MITRE updates (weekly)
- CISA KEV (daily)
- News APIs (hourly)
- GDELT events (15 min)

Deliverables:
- 6 ingestion endpoints operational
- Kafka queue processing <2 sec
- NER10 extraction <500ms per document
- Database insertion <1 sec
- End-to-end latency <5 min
- 99.9% availability

Validation:
- Test agent sends test events through pipeline
- Verify entities extracted correctly
- Check database updated
- Measure latency at each stage
- Validate feedback loop working
- Store production metrics in Qdrant

Expected Time: 80-100 hours
Expected Output: Production system operational + completion report
```

---

## COMPLETION: NER10 SYSTEM OPERATIONAL

After Week 12, system ready for:
- Continuous data ingestion (VulnCheck, NVD, MITRE, news, events)
- Automated entity extraction (15K-25K entities growing daily)
- Real-time relationship building (20+ types)
- Feedback loop for continuous improvement (weekly retraining)
- Wiki updated with complete NER10 documentation

---

**All prompts are COPY/PASTE READY for sequential execution.**
