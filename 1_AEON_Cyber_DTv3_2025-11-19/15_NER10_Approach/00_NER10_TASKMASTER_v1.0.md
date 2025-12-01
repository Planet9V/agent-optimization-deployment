# NER10 TASKMASTER v1.0 - 12-Week Execution Plan
**File:** 00_NER10_TASKMASTER_v1.0.md
**Created:** 2025-11-23
**Modified:** 2025-11-23
**Version:** v1.0.0
**Author:** AEON Cyber DT Project
**Purpose:** Master execution roadmap for NER10 psychometric extraction system
**Status:** ACTIVE

---

## EXECUTIVE SUMMARY

### Mission
Build a production-grade Named Entity Recognition (NER) system that extracts 18 custom entity types (8 psychological + 10 technical) from 678 cybersecurity documents, training a high-accuracy spaCy model, enriching a Neo4j knowledge graph with 20+ relationship types, and enabling real-time threat intelligence ingestion.

### Timeline
**12 Weeks** (4 phases)
- **Phase 1 (Weeks 1-3):** Data Preparation & Annotation Foundation
- **Phase 2 (Weeks 4-6):** Model Training & Validation
- **Phase 3 (Weeks 7-9):** Enrichment Pipeline & Relationship Building
- **Phase 4 (Weeks 10-12):** Real-Time APIs & Production Deployment

### Success Criteria
| Metric | Target | Baseline |
|--------|--------|----------|
| Annotated Files | 678 (100%) | 206 (28%) |
| Entity F1 Score | >0.80 per type | N/A |
| Relationship Types | 20+ types | 0 |
| Neo4j Enrichment | 15,000+ entities | 30 |
| Real-Time Latency | <2 seconds | N/A |
| System Availability | 99.9% | N/A |
| Inter-Annotator Agreement | >0.85 | N/A |

### Budget & Resources
| Item | Cost | Duration |
|------|------|----------|
| Annotation (80 hours @ $50/hr) | $4,000 | Weeks 1-3 |
| GPU Training (8 A100 hours) | $800 | Weeks 4-6 |
| Engineering (360 hours @ $100/hr) | $36,000 | All weeks |
| **Total** | **$40,800** | **12 weeks** |

**Team:** 10-agent swarm (see Agent Roster below)

---

## 10-AGENT SWARM ROSTER

### Annotation Team (3 agents)
1. **Primary Annotator** - Mark all 678 files with entity spans and labels
2. **Independent Validator** - Secondary annotation for 25% overlap (quality gate)
3. **Conflict Resolver** - Reconcile disagreements, document reasoning

### Training Team (2 agents)
4. **Data Engineer** - Prepare spaCy training format, data pipeline
5. **ML Training Specialist** - Model tuning, hyperparameter optimization, F1 tracking

### Enrichment Team (3 agents)
6. **Relationship Builder** - Extract and construct 20+ relationship types
7. **Entity Resolver** - Link extracted entities to existing Neo4j nodes
8. **Knowledge Architect** - Design graph schema, integration points

### Quality Team (2 agents)
9. **Test Validator** - Automated testing, F1 metrics, coverage analysis
10. **System Monitor** - Real-time performance tracking, bottleneck identification

---

## 12-WEEK PHASED EXECUTION

### PHASE 1: DATA PREPARATION & ANNOTATION (Weeks 1-3)

#### Week 1: Audit & Setup
**Goal:** Validate data quality, establish annotation infrastructure

**Tasks:**
- [ ] Audit 678 training files (1.28M words total)
- [ ] Validate existing 206 annotated files for consistency
- [ ] Set up Label Studio or Prodigy instance
- [ ] Create entity type guidelines (18 types, with examples)
- [ ] Configure inter-annotator agreement validation (Cohen's Kappa)
- [ ] Create 14 annotation batches (50 files each)

**Deliverable:** Annotation infrastructure ready, guidelines documented
**Success Metric:** >85% IAA on test batch of 10 files

**Copy/Paste Prompt for Week 1:**
```
WEEK 1 EXECUTION PROMPT:
Task: Audit 678 training files and establish annotation infrastructure

ACTUAL WORK:
1. Read /Training_Data/ directory completely
   - Count files by type
   - Validate markdown structure
   - Extract statistics (word count, existing annotations)

2. Set up Label Studio instance
   - Create project with 18 entity types
   - Import 206 pre-annotated files
   - Configure validation rules

3. Create annotation guidelines
   - Define each of 18 entity types
   - Provide 3+ examples per type
   - Document edge cases and overlaps

4. Generate inter-annotator agreement protocol
   - Select 10-file test batch
   - Distribute to 2 annotators independently
   - Calculate Cohen's Kappa
   - Document disagreement patterns

EVIDENCE: Annotation system operational, test IAA recorded

DO NOT: Build frameworks or tools. ANNOTATE ACTUAL FILES.
```

---

#### Weeks 2-3: Annotation Execution
**Goal:** Annotate 472 remaining files (28% → 100% coverage)

**Tasks (Week 2):**
- [ ] Annotate Batches 1-5 (250 files): 2 days
- [ ] Validate Batch 1-2 (100 files): 1 day
- [ ] Reconcile conflicts, update guidelines: 1 day
- [ ] Track metrics: IAA, entity distribution, annotation time

**Tasks (Week 3):**
- [ ] Annotate Batches 6-9 (200 files): 2 days
- [ ] Validate Batches 3-5 (150 files): 1 day
- [ ] Final conflict resolution: 1 day
- [ ] Export to spaCy DocBin format (training-ready)

**Deliverable:** 678 fully-annotated files in spaCy format
**Success Metrics:**
- Inter-annotator agreement >0.85
- >2,100 total annotated entities
- 0 missing required fields

**Copy/Paste Prompt for Week 2:**
```
WEEK 2 EXECUTION PROMPT:
Task: Annotate 250 files (Batches 1-5) with 18 entity types

PRIMARY ANNOTATOR AGENT:
1. Open Label Studio
2. Load Batch 1 (50 files)
3. For each file:
   - Read full content
   - Identify all entity spans matching 18 types
   - Tag with entity type + metadata (confidence, reasoning)
   - Save and move to next file
4. Complete Batches 1-5
5. Export to CSV (id, text, entities, confidence)

VALIDATION AGENT (25% overlap):
1. Independently annotate Batch 1 (50 files)
2. Compare with Primary Annotator results
3. Calculate Cohen's Kappa per entity type
4. Record all disagreements

CONFLICT RESOLVER:
1. Review disagreements (Cohen's Kappa < 0.80)
2. Re-read source text in context
3. Make final decision or mark for discussion
4. Update guidelines if new pattern discovered

METRICS TO TRACK:
- Files annotated per day
- Entities per file
- IAA by entity type
- Time per file

EVIDENCE: 250 files annotated in Label Studio, CSV export ready, IAA recorded
```

**Copy/Paste Prompt for Week 3:**
```
WEEK 3 EXECUTION PROMPT:
Task: Complete annotation of remaining 222 files + full export

COMPLETION SCHEDULE:
Mon-Tue: Annotate Batches 6-7 (100 files)
Wed: Annotate Batch 8 (50 files)
Thu: Annotate Batch 9 (50 files) + Batch 10-14 partial (22 files)
Fri: Final validation pass, conflict resolution, spaCy export

ANNOTATION AGENTS:
1. Load Label Studio project
2. Continue from Week 2 progress
3. Follow entity guidelines strictly
4. Mark confidence scores for borderline cases

EXPORT PIPELINE:
1. Extract all annotated documents
2. Convert to spaCy DocBin format (v3.7 compatible)
3. Validate no missing required fields
4. Create train/test/val splits (70/15/15)
5. Generate annotation statistics

FINAL DELIVERABLE:
- annotations.spacy (full dataset)
- train.spacy, test.spacy, val.spacy (splits)
- annotation_stats.json (metrics)
- guidelines_final.md (updated)

EVIDENCE: All 678 files annotated, spaCy format ready, IAA >0.85
```

---

### PHASE 2: MODEL TRAINING & VALIDATION (Weeks 4-6)

#### Week 4: Data Pipeline & Model Initialization
**Goal:** Prepare training data, initialize base model

**Tasks:**
- [ ] Convert 678 annotated files to spaCy training format
- [ ] Create data validation pipeline (check entity consistency)
- [ ] Download en_core_web_trf (transformer model, 562MB)
- [ ] Set up training environment (GPU, deps, monitoring)
- [ ] Configure hyperparameters for 18-entity model
- [ ] Create baseline evaluation on 50-file test set

**Deliverable:** Training pipeline ready, baseline metrics recorded
**Success Metrics:**
- 0 training data validation errors
- Baseline F1 >0.60 on test set
- Training environment ready (GPU memory check)

**Copy/Paste Prompt for Week 4:**
```
WEEK 4 EXECUTION PROMPT:
Task: Prepare spaCy training pipeline and initialize model

DATA ENGINEER AGENT:
1. Read train.spacy, test.spacy, val.spacy
2. Validate all entity spans:
   - Check IOB2 tag consistency
   - Verify entity types match schema (18 types)
   - Check for overlapping entities
   - Validate character offsets
3. Create validation report (errors, warnings, stats)
4. Fix any validation issues
5. Generate entity distribution plots
   - Entities per file
   - Entity type frequencies
   - Entity length distribution

SETUP AGENT:
1. Check GPU availability (A100 40GB minimum)
2. Install spaCy 3.7+ with transformers
3. Download en_core_web_trf (base model)
4. Create training config file:
   - Training corpus path
   - Validation corpus path
   - Entity types (18)
   - Learning rate, batch size, epochs
   - Early stopping criteria
5. Create training script template

BASELINE AGENT:
1. Fine-tune model on 50 files only
2. Evaluate on test set
3. Report per-entity F1 scores
4. Record baseline metrics

OUTPUT:
- train.spacy, test.spacy, val.spacy (validated)
- data_validation_report.json
- baseline_metrics.json
- config.cfg (training config)
- training_script.py

EVIDENCE: Training data validated, environment ready, baseline recorded
```

---

#### Weeks 5-6: Model Training & Optimization
**Goal:** Train NER model, achieve F1 >0.80 per entity type

**Week 5 Tasks:**
- [ ] Train model on 70% of data (475 files)
- [ ] Monitor F1 scores, loss curves
- [ ] Implement early stopping (patience=5)
- [ ] Evaluate on validation set (105 files)
- [ ] Adjust hyperparameters based on F1

**Week 6 Tasks:**
- [ ] Fine-tune model with adjusted hyperparameters
- [ ] Evaluate on held-out test set (98 files)
- [ ] Per-entity type F1 analysis
- [ ] Error analysis: confusion matrix, failure modes
- [ ] Package production model

**Deliverable:** Production-ready model with F1 >0.80
**Success Metrics:**
- Per-entity F1 >0.80 (minimum)
- Macro-averaged F1 >0.82
- <5% false positive rate on validation

**Copy/Paste Prompt for Week 5:**
```
WEEK 5 EXECUTION PROMPT:
Task: Train NER model on 475 annotated files, target F1 >0.80

ML TRAINING SPECIALIST:
1. Execute training script on GPU:
   python -m spacy train config.cfg \
     --output /models \
     --gpu-id 0 \
     --paths.train train.spacy \
     --paths.dev val.spacy

2. Monitor training in real-time:
   - Loss curve (should decrease smoothly)
   - Entity F1 scores per type
   - Precision/Recall per entity
   - Early stopping trigger if plateau

3. After training completes:
   - Evaluate on test set (98 files)
   - Generate per-entity metrics:
     * Entity type F1 scores
     * Precision, Recall
     * Confusion matrix
     * Top error patterns

4. Log all metrics to training_metrics.json

HYPERPARAMETER TRACKING:
Document current settings:
- Learning rate: 0.001
- Batch size: 32
- Epochs: 30
- Early stopping: patience=5

If F1 < 0.78, prepare for Week 6 adjustments:
- Increase batch size to 64
- Reduce learning rate to 0.0005
- Increase epochs to 40

OUTPUT:
- model_epoch_30/
- training_metrics.json (F1 scores, loss)
- per_entity_f1.json (detailed breakdown)
- test_evaluation.json

SUCCESS: F1 >0.78 on test set
```

**Copy/Paste Prompt for Week 6:**
```
WEEK 6 EXECUTION PROMPT:
Task: Optimize model hyperparameters, achieve F1 >0.80, package for production

OPTIMIZATION PHASE:
1. Review Week 5 results:
   - Which entity types underperform? (<0.75 F1)
   - False positive patterns?
   - Training curve plateau point?

2. Adjust hyperparameters:
   - If F1 stalled: increase epochs to 40, use early stopping
   - If overfitting: add dropout=0.2
   - If underfitting: increase learning rate to 0.002

3. Re-train on full 475-file dataset with new params

4. Evaluate final model on 98-file test set

ERROR ANALYSIS:
1. Generate confusion matrix per entity type
2. Identify top 20 failure cases:
   - What entity was missed?
   - What entity was incorrectly predicted?
   - Any patterns (entity length, context)?
3. Document findings for Phase 3

PRODUCTION PACKAGING:
1. Select best epoch model (highest validation F1)
2. Test inference speed:
   - Time to process 1 file
   - Target: <100ms per file
3. Create model card (README):
   - Entity types (18)
   - F1 scores per type
   - Known limitations
   - Training data summary
4. Package as Python package (spacy-ner10)

FINAL DELIVERABLE:
- model/ (production-ready spaCy model)
- model/meta.json (documentation)
- final_metrics.json (F1 >0.80 per entity)
- inference_benchmark.json (latency)
- error_analysis.json (failure patterns)

SUCCESS CRITERIA:
✓ Macro F1 >0.82
✓ All entity types F1 >0.78
✓ <100ms inference per file
✓ Production package ready
```

---

### PHASE 3: ENRICHMENT PIPELINE & RELATIONSHIP BUILDING (Weeks 7-9)

#### Week 7: Batch Extraction & Entity Resolution
**Goal:** Extract 15,000-25,000 entities from all 678 files

**Tasks:**
- [ ] Run model inference on all 678 files
- [ ] Extract entity mentions with confidence scores
- [ ] Resolve entity references (e.g., "APT1" → "APT1/Comment Crew")
- [ ] Create entity master list (deduplicated)
- [ ] Link to existing Neo4j nodes (Equipment, CVE, Sector)

**Deliverable:** 15,000-25,000 extracted entities, ready for graph loading
**Success Metrics:**
- 0 confidence score errors
- >90% entity resolution accuracy (manual spot check)
- All entities linked to Neo4j

**Copy/Paste Prompt for Week 7:**
```
WEEK 7 EXECUTION PROMPT:
Task: Extract 15,000-25,000 entities from 678 files using trained model

EXTRACTION AGENT:
1. Load production model from Week 6
2. Batch process all 678 files:
   for file in training_files:
     - Read file content
     - Run model inference: nlp(text)
     - Extract entities with confidence scores
     - Save to extraction_results.jsonl

3. Output format for each entity:
   {
     "file_id": "source_file.md",
     "entity_text": "ransomware",
     "entity_type": "THREAT_TYPE",
     "confidence": 0.92,
     "start_char": 1523,
     "end_char": 1533,
     "context_left": "The organization faced...",
     "context_right": "...attack in Q4 2024"
   }

4. Generate extraction statistics:
   - Total entities extracted: X
   - Entities per file (average)
   - Entity type distribution
   - Confidence score distribution

ENTITY RESOLUTION AGENT:
1. Load extraction_results.jsonl (all extracted entities)
2. Create entity master list:
   - Group by normalized text (lowercase, no punctuation)
   - Keep highest confidence mention
   - Deduplicate variants (e.g., "APT-1", "APT1", "Comment Crew")

3. Link to existing Neo4j nodes:
   - THREAT_TYPE → existing CVE or THREAT nodes
   - ORGANIZATION → existing ORG nodes
   - ATTACKER_GROUP → existing ATTACKER nodes
   - SECTOR → existing SECTOR nodes
   - ATTACK_TECHNIQUE → existing MITRE ATT&CK nodes

4. Output:
   - entity_master.json (deduplicated list)
   - entity_to_neo4j_mapping.json (Neo4j node IDs)
   - resolution_confidence.json (accuracy metrics)

DELIVERABLE:
- extraction_results.jsonl (all 15K-25K entities)
- entity_master.json (deduplicated)
- extraction_stats.json (distributions, counts)

EVIDENCE: All 678 files processed, entities extracted, Neo4j mapping ready
```

---

#### Week 8: Relationship Extraction & Graph Construction
**Goal:** Build 20+ relationship types, enrich Neo4j

**Tasks:**
- [ ] Extract relationships using dependency parsing + custom patterns
- [ ] Define 20+ relationship types (EXHIBITS, CAUSES_BY, TARGETS, etc.)
- [ ] Validate relationship consistency
- [ ] Create Neo4j Cypher scripts for bulk loading
- [ ] Load into Neo4j (create edges)

**Deliverable:** 20+ relationship types loaded in Neo4j
**Success Metrics:**
- All 15K-25K entities represented in Neo4j
- 20+ relationship types created
- Graph integrity checks pass (no orphaned nodes)

**Copy/Paste Prompt for Week 8:**
```
WEEK 8 EXECUTION PROMPT:
Task: Extract 20+ relationship types and load into Neo4j

RELATIONSHIP BUILDER AGENT:
1. Define 20 relationship types:
   - ORGANIZATION EXHIBITS COGNITIVE_BIAS
   - INCIDENT CAUSED_BY COGNITIVE_BIAS
   - DECISION INFLUENCED_BY AVAILABILITY_BIAS
   - ATTACKER_GROUP TARGETS SECTOR
   - CVE AFFECTS EQUIPMENT_TYPE
   - THREAT_TYPE EXPLOITS VULNERABILITY
   - ORGANIZATION HAS DEFENSE_MECHANISM
   - INCIDENT INVOLVES THREAT_TYPE
   - SECTOR FACES THREAT_TYPE
   - EQUIPMENT VULNERABLE_TO CVE
   [+ 10 more relationship types]

2. Extract relationships from files:
   - Use spaCy dependency parsing
   - Apply custom regex patterns
   - Use entity co-occurrence in sentences
   - Rule-based extraction for technical relationships

3. Output format:
   {
     "source_entity": "Outlook",
     "source_type": "SOFTWARE",
     "relationship_type": "VULNERABLE_TO",
     "target_entity": "CVE-2024-1234",
     "target_type": "CVE",
     "confidence": 0.88,
     "evidence": "Outlook is vulnerable to CVE-2024-1234..."
   }

4. Generate relationship statistics

KNOWLEDGE ARCHITECT AGENT:
1. Review extracted relationships
2. Design Neo4j schema:
   - Relationship properties (source_text, confidence)
   - Cardinality constraints
   - Validation rules

3. Create Cypher script for bulk loading:
   LOAD CSV FROM 'relationships.csv'
   MATCH (source), (target)
   WHERE source.id = row.source_id AND target.id = row.target_id
   CREATE (source)-[r:EXHIBITS]->(target)
   SET r.confidence = row.confidence

4. Test on Neo4j dev instance
5. Load to production Neo4j

DELIVERABLE:
- relationships.jsonl (20+ types, 10K+ edges)
- neo4j_load_script.cypher
- relationship_type_counts.json

EVIDENCE: Relationships extracted, Neo4j script ready, test load successful
```

---

#### Week 9: Validation & Enrichment Finalization
**Goal:** Validate enrichment quality, document results

**Tasks:**
- [ ] Validate graph integrity (no orphaned nodes/edges)
- [ ] Spot-check relationship accuracy (manual review of 100 relationships)
- [ ] Generate graph statistics (node counts, edge density)
- [ ] Document entity schema and relationship ontology
- [ ] Create enrichment report

**Deliverable:** Validated, enriched Neo4j knowledge graph
**Success Metrics:**
- Graph integrity: 0 validation errors
- Relationship accuracy >85% (spot check)
- Complete documentation ready

**Copy/Paste Prompt for Week 9:**
```
WEEK 9 EXECUTION PROMPT:
Task: Validate Neo4j enrichment, finalize Phase 3

VALIDATION AGENT:
1. Run graph integrity checks:
   - Check for orphaned nodes: MATCH (n) WHERE NOT (n)--()
   - Check for duplicate edges: MATCH (a)-[r]->(b) WITH a, b, r, count(r) as cnt WHERE cnt > 1
   - Verify node type consistency
   - Check relationship cardinality

2. Spot-check 100 random relationships:
   - Sample 100 edges from each relationship type
   - Manually verify accuracy
   - Document false positives/negatives
   - Calculate accuracy percentage

3. Generate final statistics:
   - Total nodes: should be ~1.1M (existing) + 15K-25K (new)
   - Total edges: count by relationship type
   - Node type distribution
   - Entity coverage: % of entities linked to Neo4j

DOCUMENTATION AGENT:
1. Document final enrichment:
   - Entity schema (18 types, definitions, counts)
   - Relationship ontology (20+ types, examples)
   - Data quality metrics (F1 scores, IAA, accuracy)
   - Known limitations

2. Create graph visualization:
   - Sample subgraph showing key entity types
   - Relationship type network diagram
   - Entity distribution charts

3. Write enrichment summary:
   - What was added to Neo4j
   - Improvement from baseline
   - Ready for production use

DELIVERABLE:
- graph_validation_report.json
- enrichment_statistics.json
- entity_schema.md (final)
- relationship_ontology.md (final)
- enrichment_summary.md

EVIDENCE: Graph validated, 100 relationships spot-checked, documentation complete
```

---

### PHASE 4: REAL-TIME APIs & PRODUCTION DEPLOYMENT (Weeks 10-12)

#### Week 10: API Development & Testing
**Goal:** Build real-time ingestion APIs

**Tasks:**
- [ ] Design 5-step ingestion pipeline (webhook → queue → processing → validation → Neo4j)
- [ ] Build Express.js API with /ingest, /status, /results endpoints
- [ ] Set up Kafka queue for event streaming
- [ ] Integrate NER10 model for real-time extraction
- [ ] Create rate limiting & auth middleware
- [ ] Write API tests

**Deliverable:** REST API operational, tested, documented
**Success Metrics:**
- API endpoints respond <2 seconds
- Kafka queue throughput >10,000 events/day
- 95%+ test coverage

**Copy/Paste Prompt for Week 10:**
```
WEEK 10 EXECUTION PROMPT:
Task: Build production REST API for real-time threat intelligence ingestion

API DEVELOPER AGENT:
1. Create Express.js application structure:
   /api
   ├── index.js (main server)
   ├── routes/
   │  ├── ingest.js (webhook receiver)
   │  ├── status.js (job status)
   │  └── results.js (get extracted entities)
   ├── middleware/
   │  ├── auth.js (API key validation)
   │  ├── rateLimit.js (100 req/min per key)
   │  └── validation.js (input schema)
   ├── services/
   │  ├── ner.js (model inference)
   │  ├── kafka.js (queue publishing)
   │  ├── neo4j.js (graph updates)
   │  └── entityResolution.js
   └── config/
      └── settings.js

2. Implement 5-step pipeline:
   Step 1: Webhook receiver
   - POST /api/ingest
   - Parse JSON payload
   - Validate source and content

   Step 2: Rate limiting & auth
   - Check API key
   - Enforce rate limits
   - Log request

   Step 3: Queue to Kafka
   - Publish event to Kafka topic
   - Return job ID to client
   - Respond with 202 Accepted

   Step 4: NER extraction (async worker)
   - Listen to Kafka topic
   - Run model inference
   - Extract entities with confidence

   Step 5: Graph update (async worker)
   - Resolve entities to Neo4j nodes
   - Create edges
   - Update timestamps

3. Create endpoints:
   POST /api/ingest
   GET /api/status/:jobId
   GET /api/results/:jobId

TESTING AGENT:
1. Write tests for all endpoints:
   - Happy path: valid input → 202 response
   - Auth failure: invalid key → 401
   - Rate limit: >100 req/min → 429
   - Validation error: missing fields → 400

2. Integration tests:
   - End-to-end: webhook → extraction → Neo4j
   - Measure latency per step

3. Load test:
   - Simulate 1,000 requests/hour
   - Measure response times
   - Check for memory leaks

DELIVERABLE:
- api/ (complete Express app)
- tests/ (comprehensive test suite)
- README.md (API documentation)
- postman_collection.json (request examples)

EVIDENCE: All endpoints tested, load test passing, ready for deployment
```

---

#### Week 11: Integration & Documentation
**Goal:** Integrate with existing systems, complete documentation

**Tasks:**
- [ ] Connect API to production Neo4j instance
- [ ] Set up data source integrations (VulnCheck, NVD, CISA, news feeds)
- [ ] Configure webhooks for real-time updates
- [ ] Create OpenAPI/Swagger documentation
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Write deployment guide

**Deliverable:** Complete integration, documented, monitored
**Success Metrics:**
- All data sources connected
- Monitoring dashboards operational
- Documentation >95% complete

**Copy/Paste Prompt for Week 11:**
```
WEEK 11 EXECUTION PROMPT:
Task: Integrate APIs with production systems and complete documentation

INTEGRATION ENGINEER:
1. Connect API to production Neo4j:
   - Update connection string to prod instance
   - Test entity resolution with real data
   - Verify relationship creation

2. Set up data source webhooks:
   - VulnCheck webhook → API /ingest
   - Configure polling for NVD (daily)
   - Set up MITRE ATT&CK feed (weekly)
   - Connect news API (hourly)

3. Test end-to-end pipeline:
   - Send sample threat intel through /ingest
   - Monitor extraction in real-time
   - Verify Neo4j update
   - Check API /results endpoint

MONITORING AGENT:
1. Set up Prometheus metrics:
   - Request latency (p50, p95, p99)
   - Queue depth
   - Model inference time
   - Neo4j write latency

2. Create Grafana dashboards:
   - System health (CPU, memory, requests/sec)
   - Pipeline metrics (events processed, failures)
   - Model performance (F1 scores, confidence)
   - Data quality (entities per day, types)

3. Configure alerting:
   - Alert if latency >2 seconds
   - Alert if error rate >1%
   - Alert if queue depth >1000

DOCUMENTATION AGENT:
1. Create OpenAPI specification:
   - All endpoints documented
   - Example requests/responses
   - Error codes and messages

2. Write deployment guide:
   - System requirements
   - Installation steps
   - Configuration (env vars)
   - Running tests
   - Monitoring setup

3. Create user guide:
   - How to get API key
   - Rate limit policy
   - Integration examples
   - Troubleshooting

DELIVERABLE:
- openapi.yaml (API specification)
- DEPLOYMENT.md (deployment guide)
- USER_GUIDE.md (usage documentation)
- MONITORING.md (monitoring setup)
- Grafana dashboard JSON

EVIDENCE: Production connected, webhooks configured, monitoring operational
```

---

#### Week 12: Deployment & Handoff
**Goal:** Deploy to production, finalize documentation

**Tasks:**
- [ ] Deploy API to production (Docker containers, K8s if applicable)
- [ ] Run final system tests (load, security, functionality)
- [ ] Create runbook for operations team
- [ ] Document known limitations and future enhancements
- [ ] Conduct knowledge transfer with stakeholders

**Deliverable:** Production system operational, fully documented
**Success Metrics:**
- System availability 99.9% (measured over first 7 days)
- <5 production incidents
- Complete documentation and runbook

**Copy/Paste Prompt for Week 12:**
```
WEEK 12 EXECUTION PROMPT:
Task: Deploy to production, finalize project

DEVOPS AGENT:
1. Build Docker image:
   - Create Dockerfile for API
   - Build and test image locally
   - Push to container registry

2. Deploy to production:
   - Create K8s deployment manifests (if applicable)
   - Or: EC2/ECS configuration
   - Set up load balancer
   - Configure TLS/HTTPS

3. Verify production deployment:
   - Health checks passing
   - All endpoints responding
   - Monitoring connected
   - Logging configured

4. Create disaster recovery plan:
   - Database backups
   - State restoration procedures
   - Failover procedures

SYSTEM MONITOR:
1. Run final system tests:
   - Load test: 10,000 events/day
   - Security test: API key validation, rate limiting
   - Functionality test: end-to-end extraction
   - Performance test: latency <2 seconds

2. Measure baseline metrics:
   - Throughput (events/hour)
   - Latency (p50, p95, p99)
   - Error rate
   - Model performance (F1 scores in production)

3. Create operations runbook:
   - Common issues and solutions
   - Monitoring dashboard URLs
   - Escalation procedures
   - Log locations

DOCUMENTATION FINALIZATION:
1. Create final project summary:
   - Objectives: ✓ Completed
   - Timeline: Weeks 1-12 ✓
   - Budget: $40,800 ✓
   - Metrics achieved (F1 >0.80, 678 files, etc.)

2. Document lessons learned:
   - What worked well
   - What could be improved
   - Recommendations for Phase 2

3. Create knowledge transfer guide:
   - Key contacts
   - System architecture overview
   - How to interpret metrics
   - Support procedures

DELIVERABLE:
- production deployment verified
- Dockerfile, K8s manifests
- operations_runbook.md
- project_completion_summary.md
- system_metrics_baseline.json

FINAL SUCCESS CRITERIA:
✓ NER10 model trained (F1 >0.80)
✓ 678 files annotated
✓ 15K-25K entities extracted
✓ 20+ relationships in Neo4j
✓ Real-time API operational
✓ <2 second latency
✓ 99.9% availability
✓ Complete documentation
✓ Operations team trained
```

---

## SUCCESS METRICS & VALIDATION FRAMEWORK

### Entity Recognition Metrics
| Metric | Target | Validation |
|--------|--------|------------|
| Per-Entity F1 | >0.80 | Run spaCy test suite |
| Macro F1 | >0.82 | Average across all 18 types |
| Confidence Calibration | ±5% | Compare predicted vs actual |
| False Positive Rate | <5% | Manual spot-check 100 samples |
| False Negative Rate | <10% | Manual spot-check 100 samples |

### Enrichment Metrics
| Metric | Target | Validation |
|--------|--------|------------|
| Annotated Files | 678 (100%) | File count in spaCy format |
| Extracted Entities | 15K-25K | Count in extraction_results.jsonl |
| Entity Resolution Accuracy | >90% | Manual spot-check 100 entities |
| Relationship Types | 20+ | Count in Neo4j |
| Graph Integrity | 100% | Run Cypher validation queries |

### API Performance Metrics
| Metric | Target | Validation |
|--------|--------|------------|
| Ingestion Latency | <500ms | Webhook to Kafka publish |
| Processing Latency | <2s | Queue to graph update |
| API Response Time | <1s | /status endpoint |
| Throughput | 10,000+ events/day | Sustained load test |
| Availability | 99.9% | Monitor for 30 days |
| Error Rate | <1% | Log analysis |

### Quality Assurance
| Checkpoint | Week | Owner | Success Criteria |
|-----------|------|-------|------------------|
| Annotation Setup | 1 | Annotator | Label Studio operational, IAA >0.85 |
| Annotation Complete | 3 | Validator | 678 files annotated, spaCy format ready |
| Model Baseline | 4 | ML Specialist | F1 >0.60 on test set |
| Model Trained | 6 | ML Specialist | F1 >0.80 per entity, <100ms inference |
| Extraction Complete | 7 | Data Engineer | 15K-25K entities extracted, resolved |
| Relationships Built | 8 | Architect | 20+ types, 10K+ edges created |
| Enrichment Validated | 9 | Validator | Graph integrity 100%, accuracy >85% |
| API Tested | 10 | Developer | All endpoints tested, load test passing |
| Integration Complete | 11 | Integration Eng | Production connected, monitoring operational |
| Production Ready | 12 | DevOps | Deployed, tested, documented |

---

## KEY REFERENCE DOCUMENTS

### Detailed Specifications
1. **Implementation Plan** (2,850 lines)
   `/implementation/01_NER10_IMPLEMENTATION_PLAN_v1.0.md`
   - Complete multi-agent architecture
   - 20+ agent definitions with roles
   - MCP tools integration
   - Data flow diagrams

2. **Annotation Workflow** (2,600 lines)
   `/annotation/03_ANNOTATION_WORKFLOW_v1.0.md`
   - Entity schema (18 types)
   - Relationship schema (24 types)
   - Annotation interface setup
   - Quality control procedures

3. **Model Architecture** (1,880 lines)
   `/training/04_NER10_MODEL_ARCHITECTURE_v1.0.md`
   - spaCy transformer configuration
   - Training pipeline
   - Evaluation framework
   - Performance optimization

4. **Real-Time API** (1,847 lines)
   `/api_ingestion/06_REALTIME_INGESTION_API_v1.0.md`
   - API endpoints and specs
   - 5-step processing pipeline
   - Kafka queue architecture
   - Neo4j integration

### Current State (Baseline)
- **Annotated Files:** 206 of 678 (28%)
- **Database:** 1.1M nodes (equipment, CVE, techniques)
- **Existing Entities:** ~30 cognitive bias nodes
- **Timeline:** 12 weeks to full completion
- **Budget:** $40,800

---

## EXECUTION CHECKLIST

### Phase 1: Data Prep & Annotation (Weeks 1-3)
- [ ] Week 1: Infrastructure setup, IAA validation
- [ ] Week 2: Annotate Batches 1-5 (250 files)
- [ ] Week 3: Annotate Batches 6-14 (222 files + partial), spaCy export

### Phase 2: Model Training (Weeks 4-6)
- [ ] Week 4: Data pipeline, baseline model
- [ ] Week 5: Model training, F1 tracking
- [ ] Week 6: Optimization, production packaging

### Phase 3: Enrichment (Weeks 7-9)
- [ ] Week 7: Batch extraction, entity resolution
- [ ] Week 8: Relationship extraction, graph loading
- [ ] Week 9: Validation, documentation

### Phase 4: Deployment (Weeks 10-12)
- [ ] Week 10: API development, testing
- [ ] Week 11: Integration, monitoring, documentation
- [ ] Week 12: Production deployment, handoff

---

## RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Annotation IAA <0.85 | Medium | High | Provide clearer guidelines, inter-annotator discussion |
| Model F1 <0.78 | Medium | High | Additional training data, hyperparameter tuning |
| Neo4j loading errors | Low | High | Validate data format, test Cypher scripts |
| API latency >2s | Low | Medium | Profile bottlenecks, optimize inference |
| Team unavailability | Low | Medium | Cross-train agents, document procedures |

---

## NEXT STEPS

### Immediate Actions (This Week)
1. Copy/paste **Week 1 Execution Prompt** above
2. Initiate Annotation Team agent spawning
3. Set up Label Studio instance
4. Begin file audit

### Success Indicators
- Label Studio operational by EOD
- Entity guidelines documented
- Test batch (10 files) annotated with IAA >0.85
- Ready for Week 2 scaling

**Contact:** AEON Cyber DT Project Lead
**Status:** ACTIVE - Ready for execution
**Last Updated:** 2025-11-23

---

*This TASKMASTER synthesizes 4 detailed specifications (2,850 + 2,600 + 1,880 + 1,847 lines) into actionable 12-week execution plan with copy/paste prompts for each major week. Follow sequentially for guaranteed project completion.*
