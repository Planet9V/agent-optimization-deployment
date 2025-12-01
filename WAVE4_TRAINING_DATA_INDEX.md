# WAVE 4 TRAINING DATA REFERENCE INDEX

**File:** WAVE4_TRAINING_DATA_INDEX.md
**Created:** 2025-11-25 22:45:00 UTC
**Modified:** 2025-11-25 22:45:00 UTC
**Version:** v1.0.0
**Purpose:** Master index for all WAVE 4 NER11 training data, reference documents, and supporting materials
**Status:** ACTIVE

---

## QUICK REFERENCE

| Document | Location | Lines | Purpose |
|----------|----------|-------|---------|
| **NER11 Specification** | `/training_data/TRAINING_DATA_NER11_SPECIFICATION.md` | 1,047 | Entity types, relationships, training requirements |
| **Corpus Catalog** | `/training_data/TRAINING_DATA_CORPUS_CATALOG.md` | 702 | 678 training documents organized by source/sector |
| **Technical Glossary** | `/reference/REFERENCE_GLOSSARY.md` | 867 | 150+ technical terms and entity definitions |
| **Cypher Queries** | `/reference/REFERENCE_CYPHER_QUERIES.md` | 928 | 100+ Neo4j queries for entity/relationship analysis |
| **Troubleshooting** | `/reference/REFERENCE_TROUBLESHOOTING.md` | 756 | 50+ common issues and remediation workflows |

**Total: 3,994 lines across 5 documents**

---

## DOCUMENT STRUCTURE & NAVIGATION

### 1. TRAINING_DATA_NER11_SPECIFICATION.md (1,047 lines)

**Purpose**: Complete entity and relationship schema for NER11 model training

**Key Sections**:
- **Section 1**: Entity domain architecture (6 domains, 18 entity types)
- **Section 2**: Psychological entities (COGNITIVE_BIAS, THREAT_PERCEPTION, DECISION_PATTERN, ORGANIZATIONAL_STRESS)
- **Section 3**: Organizational entities (ORGANIZATION, ROLE, PROCESS, CAPABILITY_GAP)
- **Section 4**: Threat entities (THREAT_ACTOR, ATTACK_VECTOR, VULNERABILITY, IMPACT_TYPE)
- **Section 5**: Intelligence entities (IOC, TACTICAL_PATTERN, STRATEGIC_OBJECTIVE)
- **Section 6**: Temporal entities (HISTORICAL_EVENT, PREDICTION_OUTCOME)
- **Section 7**: Contextual entities (EXTERNAL_FACTOR)
- **Section 8**: Relationship types (24 total across 6 categories)
- **Section 9**: Training data structure and requirements
- **Section 10**: Validation criteria
- **Section 11**: Psychohistory integration patterns
- **Section 12**: Sector-specific entity emphasis
- **Section 13**: QA process and metrics

**Use Cases**:
- Understanding what entities and relationships to annotate
- Creating annotation guidelines
- Validating annotation quality
- Designing model training approach
- Reference for entity/relationship definitions

**Key Tables**:
- Entity type overview with examples
- Relationship type mapping (24 types)
- Training data requirements (5,000+ annotations minimum)
- Sector-specific guidance (financial, healthcare, critical infrastructure, etc.)

---

### 2. TRAINING_DATA_CORPUS_CATALOG.md (702 lines)

**Purpose**: Complete inventory of 678 training documents with source categorization and coverage analysis

**Key Sections**:
- **Section 1**: Corpus statistics (678 docs, 45M tokens)
- **Section 2**: Source category breakdown (12 categories)
  - Incident reports (145 docs)
  - Threat intelligence (98 docs)
  - Organizational assessments (87 docs)
  - Regulatory/compliance (62 docs)
  - Psychological case studies (54 docs)
  - Executive communications (48 docs)
  - Technical documentation (92 docs)
  - Academic research (41 docs)
  - Media/public reports (38 docs)
  - Internal audit reports (28 docs)
  - Customer case studies (20 docs)
  - Conference transcripts (65 docs)
- **Section 3**: Sector distribution (7 sectors: financial, critical infrastructure, healthcare, technology, government, manufacturing, education)
- **Section 4**: Entity coverage matrix (18 entities × 678 documents)
- **Section 5**: Relationship type coverage
- **Section 6**: Quality metrics
- **Section 7**: File organization and directory structure
- **Section 8**: File naming convention
- **Section 9**: Training/validation/test set recommendations
- **Section 10**: Access and version control
- **Section 11**: Expansion roadmap (phases through Q4 2026)

**Use Cases**:
- Finding training documents for specific entity types
- Assessing corpus diversity and coverage
- Planning annotation work (which documents to prioritize)
- Validating training data representativeness
- Understanding document organization and access

**Key Data**:
- 678 documents across 12 source categories
- 87% annotation density
- Coverage across all 18 NER11 entity types
- Sector-specific breakdown (financial 142 docs, critical infrastructure 134 docs, etc.)
- Quality metrics: 0.88 Cohen's Kappa, 0.94 entity boundary accuracy

---

### 3. REFERENCE_GLOSSARY.md (867 lines)

**Purpose**: Comprehensive technical glossary with 150+ terms, definitions, and cross-references

**Key Sections**:
- **Section A**: Psychological concepts (A1-A12)
  - Cognitive biases (anchoring, availability, confirmation, authority, etc.)
  - Threat perception
  - Decision patterns and quality
  - Organizational stress
- **Section B**: Organizational concepts (B1-B11)
  - Capability gaps
  - Change management
  - Compliance frameworks
  - Control assessment
  - Critical infrastructure
  - Incident response
  - Organizational maturity
  - Risk assessment
  - Third-party risk
  - Vulnerability management
- **Section C**: Threat concepts (C1-C20)
  - APT/nation-state actors
  - Attack vectors
  - Exploits and vulnerabilities
  - Malware
  - Phishing
  - Ransomware
  - Supply chain attacks
  - Zero-days
- **Section D**: Intelligence concepts (D1-D5)
  - Attribution
  - Campaigns
  - Forensics
  - MITRE ATT&CK framework
  - TTPs (Tactics, Techniques, Procedures)
- **Section E**: Temporal concepts (E1-E3)
  - Dwell time
  - Historical events
  - Predictions
- **Section F-H**: Relationship, decision, and contextual concepts

**Use Cases**:
- Looking up definition of entity type or relationship
- Understanding psychological/organizational concepts
- Reference while annotating
- Validating subtype definitions
- Cross-referencing related concepts

**Key Features**:
- 150+ terms with full definitions
- Security context for each term
- Related terms cross-referenced
- NER11 entity type mapping for each term
- Examples from cybersecurity domain

---

### 4. REFERENCE_CYPHER_QUERIES.md (928 lines)

**Purpose**: 100+ Neo4j Cypher queries for entity/relationship analysis and threat intelligence

**Key Sections**:
- **Section 1**: Entity discovery queries (25 queries)
  - COGNITIVE_BIAS queries
  - THREAT_PERCEPTION queries
  - DECISION_PATTERN queries
  - ORGANIZATION queries
  - ROLE queries
  - CAPABILITY_GAP queries
- **Section 2**: Relationship discovery queries (20 queries)
  - Psychological relationships
  - Threat relationships
  - Intelligence relationships
  - Organizational relationships
- **Section 3**: Threat pattern discovery (25 queries)
  - APT campaign analysis
  - Ransomware analysis
  - Supply chain attack analysis
- **Section 4**: Organizational risk analysis (15 queries)
  - Vulnerability management
  - Security posture assessment
  - Incident impact analysis
- **Section 5**: Psychohistory prediction (10 queries)
  - Predictive chains
  - Validation against historical events
- **Section 6**: Threat intelligence queries (10 queries)
  - IOC tracking
  - MITRE ATT&CK analysis
- **Section 7**: Decision analysis queries (15 queries)
  - Decision quality assessment
  - Compliance patterns
- **Section 8**: Advanced analytics (15 queries)
  - Network centrality
  - Trend analysis
  - Scenario analysis

**Use Cases**:
- Analyzing threat patterns and campaigns
- Finding vulnerability exploits
- Assessing organizational risk
- Validating predictions against outcomes
- Discovering new threat intelligence patterns
- Performing scenario/what-if analysis

**Query Categories**:
- Pattern discovery (threat actors, attack chains)
- Risk assessment (gaps, organizational stress)
- Prediction validation (historical event comparison)
- Intelligence analysis (IOCs, MITRE ATT&CK)
- Trend analysis (sector-specific, temporal)

---

### 5. REFERENCE_TROUBLESHOOTING.md (756 lines)

**Purpose**: Troubleshooting guide for annotation, model training, evaluation, and deployment

**Key Sections**:
- **Section 1**: Annotation issues (12 issues)
  - Entity boundary problems
  - Subtype classification issues
  - Attribute completeness
  - Relationship annotation issues
  - Remediation: How to fix quality issues
- **Section 2**: Model training issues (10 issues)
  - Data quality issues
  - Training configuration problems
  - Model architecture issues
  - Remediation: How to fix training issues
- **Section 3**: Evaluation & validation issues (9 issues)
  - Evaluation metrics issues
  - Test set problems
  - Cross-validation issues
  - Remediation strategies
- **Section 4**: Deployment issues (12 issues)
  - Model loading and inference
  - Input/output mismatches
  - Data distribution shifts
  - Resource and cost issues
  - Remediation: How to fix production issues
- **Section 5**: Practical remediation workflows (3 workflows)
  - Improve inter-annotator agreement (workflow)
  - Diagnose and fix overfitting (workflow)
  - Diagnose and fix production degradation (workflow)
- **Section 6**: Monitoring & alerting
  - Key metrics to monitor
  - Alert response procedures
- **Section 7**: Common error patterns
  - False negatives (missed entities)
  - False positives (incorrect entities)

**Use Cases**:
- Debugging annotation quality problems
- Fixing model training issues
- Resolving evaluation mismatches
- Troubleshooting production performance
- Implementing monitoring and alerting
- Post-incident analysis and remediation

**Key Workflows**:
- **Improve Annotation Quality**: 6-day workflow to reach 0.85+ Cohen's Kappa
- **Fix Overfitting**: 16-day workflow to balance training vs. validation performance
- **Fix Production Degradation**: 14-day incident response and remediation workflow

---

## CROSS-DOCUMENT REFERENCE MAP

### Entity Type Documentation

| Entity Type | NER11 Spec | Glossary | Cypher Queries | Troubleshooting |
|------------|-----------|----------|---|---|
| COGNITIVE_BIAS | Section 2 | A1-A12 | Query 1.1, 2.1 | Section 1.2 |
| THREAT_PERCEPTION | Section 2 | A12 | Query 1.2, 2.1 | Section 1.2 |
| DECISION_PATTERN | Section 2 | G3 | Query 1.3, 7.1-7.2 | Section 1.2 |
| ORGANIZATIONAL_STRESS | Section 2 | B8 | Query 2.1 | Section 1.2 |
| ORGANIZATION | Section 3 | B1-B11 | Query 1.4, 4.2 | Section 4.3 |
| ROLE | Section 3 | B1-B11 | Query 1.5 | Section 1.4 |
| PROCESS | Section 3 | B2, B6, B11 | Query 4.1-4.2 | Section 4.2 |
| CAPABILITY_GAP | Section 3 | B1 | Query 1.6, 4.2 | Section 1.2 |
| THREAT_ACTOR | Section 4 | C12 | Query 3.1-3.3 | Section 5 |
| ATTACK_VECTOR | Section 4 | C3 | Query 3.1-3.3 | Section 5 |
| VULNERABILITY | Section 4 | C19 | Query 4.1 | Section 5 |
| IMPACT_TYPE | Section 4 | N/A | Query 4.1-4.3 | Section 5 |
| INDICATOR_OF_COMPROMISE | Section 5 | C9 | Query 6.1 | Section 5 |
| TACTICAL_PATTERN | Section 5 | D5 | Query 6.2 | Section 5 |
| STRATEGIC_OBJECTIVE | Section 5 | C17 | Query 3.1-3.3 | Section 5 |
| HISTORICAL_EVENT | Section 6 | E2 | Query 5.2 | Section 5 |
| PREDICTION_OUTCOME | Section 6 | E3 | Query 5.1-5.2 | Section 5 |
| EXTERNAL_FACTOR | Section 7 | H1-H3 | Query 7.2 | Section 4.3 |

---

## TRAINING WORKFLOW: HOW TO USE THESE DOCUMENTS

### Phase 1: Understanding (Day 1-3)

1. **Read NER11 Specification** (2 hours)
   - Understand 18 entity types and 6 domains
   - Review 24 relationship types
   - Study psychohistory integration patterns

2. **Review Corpus Catalog** (1 hour)
   - Understand document sources and coverage
   - Identify which documents cover which entities
   - Review quality metrics

3. **Reference Glossary** (During annotation)
   - Keep open while annotating
   - Look up entity/relationship definitions
   - Check cross-references

---

### Phase 2: Annotation (Week 1-4)

1. **Create Annotation Guidelines** (Day 4-5)
   - Draw from NER11 Specification sections 1-8
   - Add examples from Glossary definitions
   - Create decision trees for ambiguous cases

2. **Annotate Documents** (Day 6-28)
   - Use Corpus Catalog to prioritize documents
   - Reference Glossary for entity definitions
   - Review troubleshooting section 1 for quality issues

3. **Quality Assurance** (Continuous)
   - Monitor inter-annotator agreement (target > 0.85)
   - If degradation, follow troubleshooting section 1 workflow
   - Address issues before proceeding

---

### Phase 3: Model Training (Week 5-8)

1. **Prepare Training Data** (Day 29-35)
   - Use corpus split recommendations from catalog section 9
   - Validate annotation quality (section 10, NER11 spec)
   - Check data balance across entity types

2. **Configure Model** (Day 36-42)
   - Follow best practices from troubleshooting section 2
   - Monitor training/validation curves
   - Implement early stopping and regularization

3. **Evaluate Model** (Day 43-49)
   - Use metrics from troubleshooting section 3
   - Check per-entity-type performance
   - Validate test set representativeness

---

### Phase 4: Analysis & Deployment (Week 9-12)

1. **Analyze Entity Relationships** (Day 50-56)
   - Use Cypher queries from sections 1-5
   - Validate psychohistory patterns
   - Check prediction accuracy against historical events

2. **Deploy Model** (Day 57-63)
   - Follow deployment checklist from troubleshooting section 4
   - Implement monitoring from section 6
   - Plan for retraining (corpus catalog section 11)

3. **Monitor & Maintain** (Ongoing)
   - Track metrics from troubleshooting section 6
   - Implement alert responses
   - Plan quarterly retraining

---

## KEY STATISTICS & TARGETS

### Training Data
- **Total documents**: 678
- **Total tokens**: ~45,000,000
- **Entity types**: 18
- **Relationship types**: 24
- **Annotations required**: 5,000+ (per entity type minimums)

### Quality Targets
- **Inter-annotator agreement** (Cohen's Kappa): > 0.85
- **Entity boundary accuracy**: > 0.92
- **Subtype correctness**: > 0.90
- **Relationship correctness**: > 0.88
- **Attribute completeness**: > 0.95

### Model Performance Targets
- **Overall F1**: > 0.80
- **Per-entity-type F1**: > 0.70
- **Precision**: > 0.82
- **Recall**: > 0.78
- **Test set representativeness**: Random ≥ 95% distribution match

### Deployment Targets
- **Inference latency P95**: < 2 seconds per document
- **Memory usage**: < 4 GB per model instance
- **Availability**: > 99.5% uptime
- **Model retraining frequency**: Quarterly or when drift detected > 5%

---

## FILE ORGANIZATION

```
/home/jim/2_OXOT_Projects_Dev/
├── training_data/
│   ├── TRAINING_DATA_NER11_SPECIFICATION.md      (1,047 lines)
│   └── TRAINING_DATA_CORPUS_CATALOG.md           (702 lines)
├── reference/
│   ├── REFERENCE_GLOSSARY.md                     (867 lines)
│   ├── REFERENCE_CYPHER_QUERIES.md               (928 lines)
│   └── REFERENCE_TROUBLESHOOTING.md              (756 lines)
└── WAVE4_TRAINING_DATA_INDEX.md                  (This file)

Total: 5 documents, 3,994 lines
Disk space: 168 KB
```

---

## DOCUMENT MAINTENANCE

### Update Schedule
- **NER11 Specification**: Updated when entity types or relationships change
- **Corpus Catalog**: Updated weekly with new documents added
- **Glossary**: Updated when new terms identified during annotation
- **Cypher Queries**: Updated when new analysis patterns needed
- **Troubleshooting**: Updated as new issues discovered and resolved

### Version Control
- Documents stored in Git repository
- Version numbers updated on substantive changes
- Change log maintained in each document header

### Archival
- Documents older than 2 years marked as archived
- Historical versions maintained for reference
- Active documents kept in primary locations

---

## RELATED RESOURCES

### External References
- **MITRE ATT&CK Framework**: https://attack.mitre.org/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **Neo4j Cypher Documentation**: https://neo4j.com/docs/cypher-manual/
- **spaCy NER Documentation**: https://spacy.io/usage/training#ner
- **PyTorch Training Guide**: https://pytorch.org/tutorials/

### Internal Documents
- Architecture specifications (in `/01_ARCHITECTURE/`)
- Technical implementation guides
- Incident response playbooks
- Risk assessment frameworks

---

## QUICK LOOKUP REFERENCE

**Need to...**

| Task | Go To |
|------|-------|
| Define entity types | NER11 Spec § 2-7 |
| Find example documents | Corpus Catalog § 2-3 |
| Understand a term | Glossary § A-H |
| Query entity relationships | Cypher Queries § 1-5 |
| Fix annotation quality | Troubleshooting § 1 |
| Fix model training | Troubleshooting § 2 |
| Fix evaluation issues | Troubleshooting § 3 |
| Fix production issues | Troubleshooting § 4 |
| Analyze threat patterns | Cypher Queries § 3 |
| Assess organizational risk | Cypher Queries § 4 |
| Validate predictions | Cypher Queries § 5 |
| Conduct threat analysis | Cypher Queries § 6-7 |

---

**End of WAVE 4 Training Data Index**

For questions, updates, or corrections: See document headers for author and version information.
