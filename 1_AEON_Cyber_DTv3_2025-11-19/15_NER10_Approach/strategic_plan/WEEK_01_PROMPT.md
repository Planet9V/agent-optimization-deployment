# WEEK 1 EXECUTION PROMPT - NER10 TASKMASTER
## Training Data Audit & Gap Analysis

**Date Created:** 2025-11-23
**Duration:** Week 1 (8-12 hours)
**Status:** READY FOR EXECUTION

---

## COPY/PASTE PROMPT FOR CLAUDE-FLOW SWARM EXECUTION

```
EXECUTE NER10 TASKMASTER - WEEK 1: TRAINING DATA AUDIT

PROJECT CONTEXT:
- Base Model: spaCy Transformer (en_core_web_trf)
- Target F1 Score: 0.78-0.84 (production-grade NER)
- Timeline: 8-12 weeks (Weeks 2-5 = annotation, Weeks 6-8 = extraction, Weeks 9-12 = enrichment)
- Current State: 678 training files (1.28M words), 2,137 existing annotations, 28% annotated
- Goal: Extract psychometric entities (cognitive biases, threat perception, emotions, defense mechanisms)

WEEK 1 OBJECTIVE: Complete Training Data Audit
└─ Audit all 678 files in AEON_Training_data_NER10/
└─ Identify annotation gaps for full schema coverage
└─ Create annotation priority list for Week 2-3

EXECUTE WITH CLAUDE-SWARM + QDRANT:

TASK 1: DATA INVENTORY AGENT
├─ Objective: Catalog all 678 training files
├─ Actions:
│  ├─ Directory tree: AEON_Training_data_NER10/ (count files by category)
│  ├─ File types: Document format analysis (.txt, .md, .json, etc.)
│  ├─ Size distribution: Words per file, total corpus size
│  ├─ Content categories: Cognitive_Biases, Incidents, Threat_Reports, Policy_Docs, etc.
│  └─ Store results in Qdrant with metadata vector embeddings
├─ Deliverable: Training_Data_Inventory.json (4,389 files cataloged)
└─ Validation: File count = 678 ✓

TASK 2: ANNOTATION GAP ANALYSIS AGENT
├─ Objective: Identify missing annotations for complete schema
├─ Current Schema (18 Entity Types):
│  1. COGNITIVE_BIAS (7 subtypes: Availability, Confirmation, Anchoring, Normalcy, Dunning-Kruger, Sunk Cost, Groupthink)
│  2. THREAT_PERCEPTION (Real/Imaginary/Symbolic)
│  3. EMOTION (Anxiety, Panic, Denial, Complacency, Confidence, Curiosity)
│  4. ATTACKER_MOTIVATION (MICE: Money, Ideology, Coercion, Ego)
│  5. DEFENSE_MECHANISM (Denial, Projection, Rationalization, Displacement)
│  6. SECURITY_CULTURE (Risk-aware, Compliant, Innovative, Legacy-bound)
│  7. HISTORICAL_PATTERN (Repetition, Escalation, De-escalation, Breakthrough)
│  8. FUTURE_THREAT_PREDICTION (Projected threat level, confidence, timeframe)
│  9. ORGANIZATIONAL_CONTEXT (Sector, Size, Maturity, Risk Profile)
│  10. INCIDENT_CHARACTERISTIC (Attack type, Impact, Detection lag, Response time)
│  11. STAKEHOLDER_ROLE (CISO, CFO, CEO, IT Manager, Board Member)
│  12. DECISION_FACTOR (Budget, Risk tolerance, Compliance, Politics)
│  13. THREAT_VECTOR (APT, Ransomware, Insider, Supply Chain, Natural)
│  14. DETECTION_METHOD (Behavioral, Signature, Anomaly, Intelligence)
│  15. MITIGATION_ACTION (Technical, Organizational, Strategic, Behavioral)
│  16. COMMUNICATION_PATTERN (Transparent, Hidden, Exaggerated, Minimized)
│  17. BEHAVIORAL_INDICATOR (Hesitation, Confidence, Contradiction, Conviction)
│  18. LACANIAN_AXIS (Real Threat, Imaginary Threat, Symbolic Response)
├─ Actions:
│  ├─ Sample analysis: Random 50 files for entity coverage check
│  ├─ Count existing annotations by entity type
│  ├─ Identify files with <5 annotations (priority for annotation)
│  ├─ Identify files with >50 annotations (already comprehensive)
│  ├─ Identify missing entity types (which categories have zero annotations?)
│  ├─ Create coverage matrix: (entity type × file category)
│  └─ Query Qdrant for semantic similarity (group files by topic)
├─ Deliverable: Gap_Analysis_Report.json
│  └─ Target metrics:
│    ├─ Current: 2,137 annotations across 678 files (avg 3.15 per file)
│    ├─ Target: 15,000-25,000 annotations (avg 22-37 per file)
│    ├─ Gap: 12,863-22,863 annotations needed
│    ├─ Entity distribution: All 18 types represented with >200 examples each
│    └─ Coverage: ≥95% files have ≥5 annotations
└─ Validation: All 18 entity types identified in sample ✓

TASK 3: QUALITY BASELINE AGENT
├─ Objective: Assess current annotation accuracy
├─ Actions:
│  ├─ Parse existing annotations in 678 files
│  ├─ Sample 50 files with existing annotations
│  ├─ Manual verification: Compare annotation to source text
│  ├─ Accuracy metrics:
│  │  ├─ Entity boundary accuracy (did annotation span match intent?)
│  │  ├─ Entity type accuracy (was the right entity type assigned?)
│  │  ├─ Relationship accuracy (are linked entities correctly paired?)
│  │  └─ Consistency score (are similar examples annotated the same way?)
│  ├─ Inter-annotator agreement (if multiple annotators exist)
│  └─ Identify problematic examples needing re-annotation
├─ Deliverable: Quality_Baseline_Report.json
│  └─ Metrics:
│    ├─ Entity boundary F1: [target >0.85]
│    ├─ Entity type F1: [target >0.80]
│    ├─ Consistency score: [target >0.90]
│    └─ Examples needing QA: [list files]
└─ Validation: Sample verified and metrics calculated ✓

TASK 4: ANNOTATION PRIORITY PLANNING AGENT
├─ Objective: Create batch sequence for Week 2-3 annotation work
├─ Actions:
│  ├─ Rank files by strategic value:
│  │  ├─ Priority 1: Cognitive bias examples (652 files - Week 2-3 focus)
│  │  ├─ Priority 2: Real incident reports (highest quality examples)
│  │  ├─ Priority 3: Policy documents (organizational context)
│  │  └─ Priority 4: Threat reports (external intelligence)
│  ├─ Group into annotation batches (20-25 files per batch)
│  ├─ Estimate annotation time per batch (avg 80 hours total):
│  │  └─ Batch 1: Cognitive biases (most critical, 30-40 hours)
│  │  └─ Batch 2: Incidents + biases (25-30 hours)
│  │  └─ Batch 3: Supporting documents (15-20 hours)
│  ├─ Identify dependency order (foundation knowledge first)
│  └─ Create Gantt-style timeline for Weeks 2-5
├─ Deliverable: Annotation_Priority_Plan.json
│  └─ Structure:
│    ├─ Batch breakdown (specific files in each batch)
│    ├─ Time estimates (per batch, per entity type)
│    ├─ Resource requirements (annotators needed, tools)
│    ├─ Weekly milestones (target annotations per week)
│    └─ Quality checkpoints (validation points)
└─ Validation: Plan covers all 678 files with realistic time estimates ✓

TASK 5: DATABASE PERSISTENCE AGENT
├─ Objective: Store audit findings in Qdrant
├─ Actions:
│  ├─ Create Qdrant collections:
│  │  ├─ "training_files" (document metadata + embeddings)
│  │  ├─ "annotations_current" (existing annotations)
│  │  ├─ "entity_gaps" (missing annotations by type)
│  │  ├─ "quality_metrics" (baseline accuracy scores)
│  │  └─ "annotation_batches" (planned batches for execution)
│  ├─ Embed file content (semantic vectors for similarity search)
│  ├─ Index by:
│  │  ├─ Entity type coverage
│  │  ├─ Annotation density
│  │  ├─ File category
│  │  └─ Quality baseline
│  ├─ Create query index for Week 2 retrieval
│  └─ Enable semantic search ("find all files about APT threats")
├─ Deliverable: Qdrant database populated with audit results
└─ Validation: Collections created, data persisted, queries working ✓

TASK 6: WIKI DOCUMENTATION AGENT
├─ Objective: Update 15_NER10_Approach wiki with Week 1 findings
├─ Actions:
│  ├─ Append to Wiki Section: "WEEK 1: TRAINING DATA AUDIT"
│  ├─ Document:
│  │  ├─ Inventory summary (4,389 files organized by category)
│  │  ├─ Annotation gaps (entity distribution, coverage analysis)
│  │  ├─ Quality baseline (current accuracy metrics)
│  │  ├─ Priority ranking (batch sequence for annotation)
│  │  └─ Next steps (Week 2 annotation tool setup)
│  ├─ Include metrics dashboard:
│  │  ├─ Progress visualization (files audited: 678/678)
│  │  ├─ Gap analysis chart (entities by coverage %)
│  │  ├─ Quality metrics (F1 baseline: X.XX)
│  │  └─ Timeline (annotation batches Week 2-5)
│  └─ Link to all deliverable files
├─ File: 15_NER10_Approach/NER10_Approach.md
└─ Validation: Wiki updated with complete Week 1 summary ✓

VALIDATION CHECKLIST:
┌─ File Inventory
│  ├─ 678 files counted and categorized ✓
│  ├─ File types identified ✓
│  └─ Size distribution calculated ✓
├─ Annotation Analysis
│  ├─ All 18 entity types identified in sample ✓
│  ├─ Gap matrix created (entity × category) ✓
│  ├─ Priority ranking established ✓
│  └─ 50-file quality sample verified ✓
├─ Database
│  ├─ Qdrant collections created ✓
│  ├─ Data persisted with embeddings ✓
│  ├─ Query index operational ✓
│  └─ Semantic search enabled ✓
├─ Documentation
│  ├─ Wiki updated with findings ✓
│  ├─ Metrics dashboard complete ✓
│  ├─ Week 2 prompt prepared ✓
│  └─ All deliverables linked ✓
└─ Readiness
   ├─ Week 2 annotation batches defined ✓
   ├─ Annotation tool identified (Label Studio or Prodigy) ✓
   ├─ Team resources allocated ✓
   └─ Success metrics established ✓

EXPECTED OUTPUTS:
├─ Training_Data_Inventory.json (4,389 files cataloged)
├─ Gap_Analysis_Report.json (entity coverage analysis)
├─ Quality_Baseline_Report.json (accuracy metrics)
├─ Annotation_Priority_Plan.json (52 batches × 20-25 files each)
├─ Qdrant Database (populated with audit results)
├─ Updated Wiki (NER10_Approach.md with Week 1 section)
└─ Week_02_PROMPT.md (annotation execution plan - READY FOR COPY/PASTE)

SUCCESS CRITERIA:
├─ All 678 files audited and inventoried
├─ Gap analysis identifies specific files needing annotation
├─ Quality baseline established (F1 scores for existing annotations)
├─ Annotation plan realistic (≤80 hours for 652 cognitive bias files)
├─ Database persisted (Qdrant searchable for Week 2)
├─ Wiki updated (complete narrative of Week 1)
└─ Next prompt ready (Week 2 copy/paste for annotation execution)

EXPECTED TIME: 8-12 hours
EXPECTED COST: $0 (local swarm execution, no external APIs)
DEPENDENCIES: None (standalone audit)
DELIVERABLES LOCATION: 15_NER10_Approach/reports/
```

---

## QUICK START CHECKLIST

- [ ] Clone/copy this prompt
- [ ] Run with: `npx claude-flow sparc run batch "EXECUTE NER10 TASKMASTER - WEEK 1: TRAINING DATA AUDIT"`
- [ ] Monitor progress in Claude-Flow dashboard
- [ ] Validate all 6 tasks complete
- [ ] Verify Qdrant database populated
- [ ] Check Wiki updated
- [ ] Approve for Week 2 (or adjust audit scope)

---

## WEEK 2 READINESS

Upon Week 1 completion, Week 2 Prompt will be automatically generated and will include:

- **Annotation Tool Setup** (Label Studio or Prodigy configuration)
- **Batch 1-5 Annotation Tasks** (652 cognitive bias examples)
- **Inter-Annotator Agreement** (quality control workflow)
- **Real-time Database Updates** (Qdrant sync during annotation)
- **Progress Metrics** (daily tracking dashboard)

The Week 2 prompt will follow the same format as this Week 1 prompt.

---

**READY TO EXECUTE** ✓
Copy this entire prompt and paste into Claude-Flow Swarm command interface.
