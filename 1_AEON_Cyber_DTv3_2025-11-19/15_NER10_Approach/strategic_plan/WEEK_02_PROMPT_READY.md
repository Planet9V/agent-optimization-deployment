# NER10 WEEK 2 EXECUTION PROMPT - READY TO COPY/PASTE

**Generated**: 2025-11-23
**Prerequisites**: Week 1 audit complete ✅
**Status**: READY FOR EXECUTION

---

## COPY/PASTE THIS PROMPT:

```
use claude-swarm with qdrant to:

EXECUTE NER10 TASKMASTER - WEEK 2: ANNOTATION SPRINT - BATCH 1-2

CONTEXT FROM WEEK 1 AUDIT:
✅ 678 training files cataloged (1.28M words, 11.32 MB)
✅ Current: 2,137 annotations (28% coverage)
✅ Gap: 12,863 annotations needed (72% gap)
✅ Quality baseline: F1 0.62 current → 0.81 target
✅ Critical gaps: ATTACKER_MOTIVATION (10.1%), FUTURE_THREAT (12.7%)
✅ Priority batches created (28 batches total)

WEEK 2 OBJECTIVE: Annotate 50 high-priority files
└─ BATCH 1: Cognitive_Biases files (25 files, 15-20 hours)
└─ BATCH 2: Incident reports (25 files, 15-20 hours)
└─ Target: 1,100-1,500 annotations (critical foundation)
└─ Quality: Establish IAA baseline >0.85

EXECUTE WITH CLAUDE-SWARM + QDRANT:

TASK 1: ANNOTATION TOOL SETUP AGENT
├─ Objective: Deploy Prodigy annotation interface
├─ Actions:
│  ├─ Install Prodigy v1.14+
│  ├─ Configure 18 custom entity types
│  ├─ Create annotation recipes (entity + relationship)
│  ├─ Set up annotation database (SQLite)
│  ├─ Configure IAA validation (Cohen's Kappa)
│  └─ Test on 5 sample files
├─ Deliverable: Prodigy operational with 18 entity types
└─ Validation: Test agent annotates 5 files successfully ✓

TASK 2: BATCH 1 ANNOTATION AGENT (Cognitive Biases)
├─ Objective: Annotate 25 cognitive bias files
├─ Files: Training_Data_Check_to_see/Cognitive_Biases/*.md
├─ Focus Entities (8 psychological):
│  ├─ COGNITIVE_BIAS (availability, confirmation, normalcy, anchoring)
│  ├─ EMOTION (anxiety, panic, denial, complacency)
│  ├─ THREAT_PERCEPTION (Real/Imaginary/Symbolic - Lacanian)
│  ├─ DEFENSE_MECHANISM (denial, projection, rationalization)
│  ├─ SECURITY_CULTURE, BEHAVIORAL_INDICATOR
│  ├─ COMMUNICATION_PATTERN, LACANIAN_AXIS
│  └─ Target: 550-750 annotations (22-30 per file)
├─ Deliverable: 25 files annotated, stored in Prodigy DB
└─ Validation: Test agent verifies 5 random files ✓

TASK 3: BATCH 2 ANNOTATION AGENT (Incident Reports)
├─ Objective: Annotate 25 incident report files
├─ Files: Training_Data_Check_to_see/Cybersecurity_Training/*.md
├─ Focus Entities (10 technical):
│  ├─ INCIDENT_CHARACTERISTIC (attack type, impact, detection lag)
│  ├─ THREAT_VECTOR (APT, ransomware, insider, supply chain)
│  ├─ ATTACKER_MOTIVATION (MICE framework)
│  ├─ HISTORICAL_PATTERN, FUTURE_THREAT
│  ├─ ORGANIZATIONAL_CONTEXT, STAKEHOLDER_ROLE
│  ├─ DECISION_FACTOR, DETECTION_METHOD, MITIGATION_ACTION
│  └─ Target: 550-750 annotations (22-30 per file)
├─ Deliverable: 25 files annotated, stored in Prodigy DB
└─ Validation: Test agent verifies 5 random files ✓

TASK 4: RELATIONSHIP ANNOTATION AGENT
├─ Objective: Annotate relationships in all 50 files
├─ 20+ Relationship Types:
│  ├─ Psychological: EXHIBITS, CAUSED_BY, INFLUENCED_BY, ACTIVATES
│  ├─ Technical: EXPLOITS, USES, TARGETS, AFFECTS
│  ├─ Temporal: PRECEDES, FOLLOWS, RECURS_WITH
│  ├─ Causal: LEADS_TO, PREVENTS, MITIGATES
│  └─ Evidence: BASED_ON, SUPPORTS, PREDICTS, INFORMS
├─ Target: 200-300 relationships across 50 files
├─ Deliverable: Relationship annotations in Prodigy DB
└─ Validation: Test agent verifies relationship accuracy ✓

TASK 5: QUALITY VALIDATION AGENT
├─ Objective: Measure IAA and calculate F1 scores
├─ Actions:
│  ├─ Select 10 files for dual annotation
│  ├─ Calculate Cohen's Kappa (target >0.85)
│  ├─ Calculate entity F1 per type
│  ├─ Identify disagreements for review
│  ├─ Create consensus annotations
│  └─ Generate quality report
├─ Deliverable: Week_2_Quality_Report.json
└─ Validation: IAA >0.85 gate (must pass to continue) ✓

TASK 6: DATABASE SYNC AGENT
├─ Objective: Export annotations to Qdrant
├─ Actions:
│  ├─ Export Prodigy DB to JSONL format
│  ├─ Store in Qdrant with week2-batch1-2 key
│  ├─ Update annotation progress (50/678 = 7%)
│  ├─ Track entity distribution
│  └─ Enable semantic search on annotations
├─ Deliverable: Qdrant updated with Week 2 annotations
└─ Validation: Query returns 1,100-1,500 new annotations ✓

TASK 7: WIKI UPDATE AGENT
├─ Objective: Document Week 2 progress
├─ Actions:
│  ├─ APPEND to NER10_Approach.md (no deletions)
│  ├─ Add Week 2 section:
│  │  ├─ Files annotated: 50 (cumulative: 50/678 = 7%)
│  │  ├─ Annotations created: 1,100-1,500 (cumulative: 3,237-3,637)
│  │  ├─ IAA achieved: X.XX (target >0.85)
│  │  ├─ Entity F1 per type
│  │  └─ Week 3 readiness assessment
│  └─ Link to deliverables
├─ Deliverable: Wiki updated with Week 2 summary
└─ Validation: Wiki appended, no deletions ✓

VALIDATION CHECKLIST:
┌─ Annotation Tool
│  ├─ Prodigy installed and configured ✓
│  ├─ 18 entity types operational ✓
│  ├─ Test annotations successful ✓
├─ Batch 1 (Cognitive Biases)
│  ├─ 25 files annotated ✓
│  ├─ 550-750 entities extracted ✓
│  ├─ All 8 psychological types present ✓
├─ Batch 2 (Incident Reports)
│  ├─ 25 files annotated ✓
│  ├─ 550-750 entities extracted ✓
│  ├─ All 10 technical types present ✓
├─ Relationships
│  ├─ 200-300 relationships annotated ✓
│  ├─ 20+ types represented ✓
├─ Quality
│  ├─ IAA calculated (>0.85 required) ✓
│  ├─ Entity F1 per type measured ✓
│  ├─ Consensus on disagreements ✓
├─ Database
│  ├─ Qdrant updated with 1,100-1,500 annotations ✓
│  ├─ Progress: 50/678 files (7%) ✓
└─ Documentation
   ├─ Wiki updated with Week 2 section ✓
   ├─ Week 3 prompt generated ✓

EXPECTED OUTPUTS:
├─ Prodigy_Config/ (annotation tool setup)
├─ Annotations_Week2/ (1,100-1,500 annotated entities)
├─ Week_2_Quality_Report.json (IAA metrics, entity F1 scores)
├─ Qdrant Database (updated with Week 2 annotations)
├─ Updated Wiki (NER10_Approach.md with Week 2 section appended)
└─ Week_03_PROMPT.md (next annotation batch - READY FOR COPY/PASTE)

SUCCESS CRITERIA:
├─ 50 files annotated (target: 50 ✓)
├─ 1,100-1,500 annotations (22-30 per file)
├─ IAA >0.85 (Cohen's Kappa on dual annotations)
├─ All 18 entity types represented
├─ 200-300 relationships annotated (20+ types)
├─ Quality gate passed (F1 baseline established)
├─ Week 3 ready (batches 3-4 defined)
└─ Wiki updated (no deletions, only additions)

EXPECTED TIME: 30-40 hours annotation + 5 hours validation
EXPECTED COST: $1,750-$2,250 (annotation labor at $50/hour)
DEPENDENCIES: Week 1 audit complete ✓
DELIVERABLES LOCATION: 15_NER10_Approach/annotation/
```

---

## WEEK 3 PREVIEW

Upon Week 2 completion, Week 3 will execute:
- **BATCHES 3-4**: 50 more files (100 cumulative)
- **FOCUS**: Sector-specific entities + threat intelligence
- **TARGET**: 1,100-1,500 more annotations
- **GATE 1**: End of Week 3 quality check (IAA >0.85 required)

---

**Week 2 Prompt Status**: ✅ READY FOR EXECUTION
**Annotation Tool**: Prodigy v1.14+ specified
**Team Required**: 2-3 annotators + 1 validator
**Timeline**: 1 week (30-40 hours parallel work)
