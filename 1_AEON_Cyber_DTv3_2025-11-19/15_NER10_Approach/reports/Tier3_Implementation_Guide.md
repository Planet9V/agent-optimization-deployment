# Tier 3 Implementation Guide - Relationship Validation Execution

**Document Type**: Implementation Guide
**Created**: 2025-11-25
**Version**: v1.0.0
**Audience**: Quality Validators, NER Specialists
**Purpose**: Step-by-step guide for executing Tier 3 relationship validation

---

## Quick Start (15 minutes)

### For QA Validators
1. Read "5-Minute Validator Overview" below
2. Review validation rules (Section 2)
3. Use validation checklist (Section 6)
4. Execute on first batch

### For Project Leads
1. Review metrics thresholds (Section 3)
2. Review timeline (Section 8)
3. Assign validators
4. Schedule kickoff

---

## 1. 5-Minute Validator Overview

### What is Tier 3?
Tier 3 validates relationships - the connections between entities. A relationship is **valid** when:
1. Both entities exist in the document
2. Entity types match the schema
3. Direction is logically correct
4. No duplicates exist

### What You're Checking
- ✓ "APT28" entity exists → "EXPLOITS" relationship → "CVE-2024-1234" entity exists
- ✓ Head type (THREAT_ACTOR) matches schema for EXPLOITS
- ✓ Tail type (CVE) matches schema for EXPLOITS
- ✓ Direction is Attacker→CVE (not CVE→Attacker)
- ✗ Same relationship doesn't appear twice

### Key Metrics
| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Valid Entity Pairs | >= 95% | Both ends of relationship exist |
| Type Accuracy | >= 90% | Correct entity types for relationship |
| Directionality | >= 92% | Relationships flow in correct direction |
| **Overall F1** | **>= 0.75** | **MAIN GATE METRIC** |

### Time per Document
- Documents with few relationships (< 5): 2-3 minutes
- Documents with medium relationships (5-10): 5-8 minutes
- Documents with many relationships (10+): 10-15 minutes

**Expected throughput**: 5-8 documents/hour with experience

---

## 2. Validation Rules - Detailed

### Rule 1: Entity Existence

**What to check**: Both head and tail entities must exist as annotated text in document

**How to validate**:
```
1. Find head entity in source text
   ✓ "APT28" found at character position 145-150
   ✗ "Unknown Attacker" marked in relationship but not in text

2. Find tail entity in source text
   ✓ "CVE-2024-1234" found at character position 278-292
   ✗ Relationship references "vulnerability" but no CVE entity annotated

3. Record result: PASS or FAIL
```

**Common issues**:
- Relationship references entity by pronoun ("it", "the group") but entity not annotated
- Entity mentioned in caption or table but relationship marked from main text
- Implicit entity (not explicitly written) incorrectly linked

**Fix if failed**:
```
Option 1: Add missing entity annotation
  - Add entity to text span
  - Assign correct type
  - Update relationship with new entity ID

Option 2: Remove relationship
  - If entity truly not in document
  - Keep only relationships with both entities present
```

---

### Rule 2: Entity Type Matching

**What to check**: Entity types must match the relationship schema

**Valid combinations for EXPLOITS**:
```
✓ THREAT_ACTOR → EXPLOITS → CVE
✓ THREAT_ACTOR → EXPLOITS → VULNERABILITY
✗ CVE → EXPLOITS → THREAT_ACTOR (wrong! CVE cannot be head)
✗ PERSON → EXPLOITS → CVE (wrong! PERSON cannot use EXPLOITS)
```

**How to validate**:
```
1. Look up relationship type in 24-type schema
2. Check: Is head entity type in valid_head_types?
3. Check: Is tail entity type in valid_tail_types?
4. Record: TYPE_CORRECT or TYPE_MISMATCH
```

**Schema lookup example**:
```json
{
  "relationship_type": "EXPLOITS",
  "valid_head_types": ["THREAT_ACTOR", "ATTACKER", "APT"],
  "valid_tail_types": ["CVE", "VULNERABILITY"]
}
```

**Common issues**:
- Entity classified as wrong type (ORGANIZATION instead of THREAT_ACTOR)
- Relationship type doesn't match entity types
- Entity type ambiguous (could be PERSON or ORGANIZATION)

**Fix if failed**:
```
Option 1: Re-classify entity
  - Change PERSON to THREAT_ACTOR (if context supports)
  - Update relationship

Option 2: Change relationship type
  - If type is wrong for entities
  - Select correct type from schema

Option 3: Remove relationship
  - If entity types fundamentally don't support relationship
```

---

### Rule 3: Correct Directionality

**What to check**: Relationship must flow in logically correct direction

**Direction examples**:
```
✓ Organization → EXHIBITS → Cognitive Bias (Org displays bias)
✗ Cognitive Bias → EXHIBITS → Organization (Wrong direction!)

✓ Threat Actor → EXPLOITS → CVE (Attacker exploits vulnerability)
✗ CVE → EXPLOITS → Threat Actor (Wrong direction!)

✓ Decision → INFLUENCED_BY → Cognitive Bias (Decision affected by bias)
✗ Cognitive Bias → INFLUENCED_BY → Decision (Wrong direction!)
```

**How to validate**:
```
1. Ask: Who/what is the "source" of this relationship?
   - Organization EXHIBITS bias = Organization is source
   - Decision INFLUENCED_BY bias = Bias is source (influences decision)

2. Ask: Who/what is the "target" or "affected"?
   - Organization EXHIBITS bias = Bias is target/result
   - Decision INFLUENCED_BY bias = Decision is affected

3. Check annotation matches semantic direction
   - head_entity should be source
   - tail_entity should be target/affected

4. Record: CORRECT or REVERSED
```

**Decision framework**:
```
Action verb determines direction:

EXHIBITS (org → bias):        Who displays it? (head) → What is displayed? (tail)
CAUSED_BY (incident → bias):  What resulted? (head) → What caused it? (tail)
INFLUENCED_BY (decision → bias): What was affected? (head) → What influenced it? (tail)
EXPLOITS (actor → cve):       Who exploits? (head) → What is exploited? (tail)
USES (actor → technique):     Who uses? (head) → What is used? (tail)
TARGETS (actor → sector):     Who targets? (head) → What is targeted? (tail)
```

**Common issues**:
- Annotator reversed head and tail
- Prepositions in text create confusion (e.g., "bias caused incident" vs "incident caused by bias")
- Passive voice obscures direction

**Fix if failed**:
```
Swap head and tail:
  Before: tail → EXPLOITS → head (WRONG)
  After:  head → EXPLOITS → tail (CORRECT)
```

---

### Rule 4: Uniqueness

**What to check**: No duplicate relationships in single document

**How to validate**:
```
1. Extract all relationships from document
   Rel #1: APT28 → EXPLOITS → CVE-2024-1234 (paragraph 2)
   Rel #2: APT28 → EXPLOITS → CVE-2024-1234 (paragraph 5)

2. Compare (head, type, tail) tuples
   Tuple #1: (APT28_ID, EXPLOITS, CVE_ID)
   Tuple #2: (APT28_ID, EXPLOITS, CVE_ID)
   MATCH = DUPLICATE

3. Record: UNIQUE or DUPLICATE
```

**Common causes**:
- Incident described in timeline then summarized later
- Same attack mentioned in introduction and detailed analysis
- Entity mentioned multiple times in different contexts

**Fix if failed**:
```
1. Keep only ONE instance:
   - Keep highest confidence version
   - Keep longest/most detailed mention
   - Keep earliest occurrence (temporal order)

2. Remove duplicates completely
3. Verify uniqueness by checking document again
```

---

### Rule 5: Logical Consistency

**What to check**: Relationship makes sense in document context

**How to validate**:
```
1. Read the sentence/paragraph containing relationship
2. Ask: Does this relationship make sense here?
   - ✓ "Company A exhibited cautious bias in procurement decisions"
      → Organization EXHIBITS Cognitive Bias ✓
   - ✗ "The database stores sensitive information"
      → Database EXHIBITS Cognitive Bias ✗ (doesn't make sense)

3. Check entity classification supports relationship type
   - ✓ Threat actor context + EXPLOITS relationship = consistent
   - ✗ Email body context + EXPLOITS relationship = suspicious

4. Record: CONSISTENT or INCONSISTENT
```

**Common issues**:
- Entity type correct but relationship wrong for context
- Implicit negation (relationship marked but text says "did NOT")
- Metaphorical or speculative language marked as fact

**Fix if failed**:
```
Option 1: Change relationship type
  - If context suggests different relationship

Option 2: Re-classify entity
  - If entity type doesn't match context

Option 3: Remove relationship
  - If relationship genuinely doesn't fit context
  - Document why it was removed
```

---

### Rule 6: No Self-Relations

**What to check**: Entity cannot relate to itself

**How to validate**:
```
1. Get head entity ID: head_entity_id
2. Get tail entity ID: tail_entity_id
3. Check: head_entity_id ≠ tail_entity_id
4. Record: VALID or SELF_RELATION
```

**Example of violation**:
```
✗ WRONG: APT28_001 → EXPLOITS → APT28_001
        (Threat actor can't exploit itself)

✓ CORRECT: APT28_001 → EXPLOITS → CVE_001
           (Threat actor exploits CVE)
```

**Common causes**:
- Entity mistakenly referenced twice (same ID)
- Two mentions of same entity not merged
- Annotation tool error in entity linking

**Fix if failed**:
```
1. Identify correct tail entity
   - Check: Is there another entity this should link to?
   - Look for related entities in document

2. Update relationship with correct tail entity ID

3. If no valid target exists, remove relationship
```

---

## 3. Quality Metrics - Detailed Calculation

### Metric 1: Valid Entity Pairs Percentage

**Definition**: Percentage of relationships where both entities exist

**Calculation**:
```
Total relationships marked: 150
Relationships with both entities: 145
Relationships with missing entity: 5

Valid_Entity_Pairs = (145 / 150) × 100 = 96.67%

Result: PASS (target >= 95%)
```

**What counts as "valid"**:
- Both entities exist in source text
- Entity spans match text exactly
- Entity IDs are correct

**What counts as "invalid"**:
- Head entity referenced but not annotated
- Tail entity referenced but not annotated
- Entity ID points to non-existent annotation

---

### Metric 2: Type Accuracy Percentage

**Definition**: Percentage of relationships with correct entity types

**Calculation**:
```
Total relationships: 150

Type validations:
- EXPLOITS relationships: 40
  - Correct (THREAT_ACTOR → CVE): 38
  - Incorrect: 2

- EXHIBITS relationships: 50
  - Correct (ORG → BIAS): 48
  - Incorrect: 2

- USES relationships: 30
  - Correct (THREAT_ACTOR → TECHNIQUE): 28
  - Incorrect: 2

- Other relationships: 30
  - Correct: 28
  - Incorrect: 2

Total correct: 38 + 48 + 28 + 28 = 142
Total incorrect: 2 + 2 + 2 + 2 = 8

Type_Accuracy = (142 / 150) × 100 = 94.67%

Result: PASS (target >= 90%)
```

**Detailed breakdown by relationship type**:
```
| Relationship | Total | Correct | Accuracy |
|--------------|-------|---------|----------|
| EXPLOITS     | 40    | 38      | 95%      |
| EXHIBITS     | 50    | 48      | 96%      |
| USES         | 30    | 28      | 93%      |
| CAUSED_BY    | 15    | 14      | 93%      |
| Other        | 15    | 14      | 93%      |
| TOTAL        | 150   | 142     | 94.67%   |
```

---

### Metric 3: Directionality Accuracy Percentage

**Definition**: Percentage of relationships with correct logical direction

**Calculation**:
```
Total relationships: 150

Directionality checks:
- EXPLOITS (40 rels): 38 correct direction, 2 reversed
- EXHIBITS (50 rels): 48 correct direction, 2 reversed
- USES (30 rels): 29 correct direction, 1 reversed
- CAUSED_BY (15 rels): 14 correct direction, 1 reversed
- Other (15 rels): 14 correct direction, 1 reversed

Total correct direction: 38 + 48 + 29 + 14 + 14 = 143
Total reversed: 2 + 2 + 1 + 1 + 1 = 7

Directionality_Accuracy = (143 / 150) × 100 = 95.33%

Result: PASS (target >= 92%)
```

---

### Metric 4-6: F1 Scores by Relationship Category

**Psychological Relationships F1**:
```
Precision = Correct psychological rels / All marked psychological
          = 38 / (38 + 2) = 38/40 = 0.95

Recall = Correct psychological rels / All actual psychological
       = 38 / 42 = 0.905

F1 = 2 × (0.95 × 0.905) / (0.95 + 0.905)
   = 2 × 0.86025 / 1.855
   = 1.7205 / 1.855
   = 0.927

Result: PASS (target >= 0.85)
```

**Technical Relationships F1**:
```
Precision = 75 / 80 = 0.9375
Recall = 75 / 82 = 0.915
F1 = 2 × (0.9375 × 0.915) / (0.9375 + 0.915) = 0.926

Result: PASS (target >= 0.82)
```

**Hybrid Relationships F1**:
```
Precision = 29 / 32 = 0.906
Recall = 29 / 34 = 0.853
F1 = 2 × (0.906 × 0.853) / (0.906 + 0.853) = 0.878

Result: PASS (target >= 0.80)
```

---

### Metric 7: Overall Relationship F1 (CRITICAL)

**Definition**: Weighted average F1 across all relationship categories

**Calculation**:
```
Psychological F1 (50% of corpus): 0.927 × 0.50 = 0.464
Technical F1 (35% of corpus):     0.926 × 0.35 = 0.324
Hybrid F1 (15% of corpus):        0.878 × 0.15 = 0.132

Overall_F1 = 0.464 + 0.324 + 0.132 = 0.920

Result: PASS (target >= 0.75, achieved 0.92)

Status: EXCELLENT - Well above threshold
```

---

## 4. Batch-by-Batch Workflow

### For Each Batch (BATCH_01, BATCH_02, etc.)

**Step 1: Prepare Documents (15 minutes)**
```
□ Load 50 annotated documents from batch
□ Extract all relationship annotations
□ Count total relationships in batch
□ Initialize validation log
□ Record batch metadata (name, tier, date)
```

**Step 2: Entity Pair Validation (2 hours)**
```
For each relationship:
  □ Find head entity in document
  □ Find tail entity in document
  □ Record: PASS (both exist) or FAIL (missing)
  □ Log any missing entities with details

Calculate metric:
  □ Count: relationships with both entities
  □ Calculate percentage
  □ Compare to threshold (>= 95%)
  □ Record result in batch log
```

**Step 3: Type Validation (2 hours)**
```
For each relationship:
  □ Check head entity type
  □ Check tail entity type
  □ Look up valid types in schema
  □ Record: PASS (types match) or FAIL (mismatch)
  □ Log mismatches with details

Calculate metric:
  □ Count: type-correct relationships
  □ Calculate percentage
  □ Compare to threshold (>= 90%)
  □ Record result in batch log
```

**Step 4: Directionality Validation (2 hours)**
```
For each relationship:
  □ Analyze semantic direction
  □ Check annotation direction
  □ Record: PASS (correct) or FAIL (reversed)
  □ Log any reversed relationships

Calculate metric:
  □ Count: directionally-correct relationships
  □ Calculate percentage
  □ Compare to threshold (>= 92%)
  □ Record result in batch log
```

**Step 5: Semantic & Uniqueness Validation (1.5 hours)**
```
□ Check for duplicate relationships
  - Keep highest confidence
  - Remove redundant entries

□ Check semantic consistency
  - Does each relationship make sense in context?
  - Any contradictions?

□ Check for self-relations
  - No entity should relate to itself

□ Record counts: duplicates, inconsistencies
```

**Step 6: Correction Implementation (2 hours)**
```
For each failed validation:
  □ Implement correction
    - Add/fix/remove entities
    - Change relationship type
    - Reverse directionality
    - Remove duplicates

□ Update annotations with corrections
□ Document changes with rationale
□ Re-validate corrected relationships
```

**Step 7: Metrics Calculation (1 hour)**
```
□ Calculate 7 metrics for batch
□ Compare each to threshold
□ Determine batch status: PASS / CONDITIONAL / FAIL
□ Record all metrics in batch report
```

**Step 8: Batch Summary (30 minutes)**
```
□ Total relationships: ___
□ Valid entity pairs: __% (target >= 95%)
□ Type accuracy: __% (target >= 90%)
□ Directionality accuracy: __% (target >= 92%)
□ Relationship F1: __ (target >= 0.75)
□ Errors corrected: ___
□ Batch status: ☐ PASS ☐ CONDITIONAL ☐ FAIL
```

---

## 5. Error Documentation Template

### For Each Error Found

```
=== ERROR LOG ===
Date: 2025-11-25
Batch: BATCH_01
Document: /path/to/document.md

Error Type: [Choose one]
  ☐ MISSING_ENTITY
  ☐ TYPE_MISMATCH
  ☐ WRONG_DIRECTION
  ☐ DUPLICATE
  ☐ CONTEXT_MISMATCH
  ☐ SELF_RELATION

Severity: [Choose one]
  ☐ CRITICAL (must fix)
  ☐ HIGH (should fix)
  ☐ MEDIUM (address if time)
  ☐ LOW (note for future)

Details:
  Relationship Type: ________________
  Head Entity: ________________ (Type: __________)
  Tail Entity: ________________ (Type: __________)
  Error Description:
  _____________________________________________________________
  _____________________________________________________________

Correction Applied:
  ☐ Added missing entity
  ☐ Re-classified entity
  ☐ Changed relationship type
  ☐ Reversed directionality
  ☐ Removed duplicate
  ☐ Removed relationship

Correction Details:
  _____________________________________________________________

Validator: ________________
Timestamp: ________________
Status: ☐ CORRECTED ☐ VERIFIED
=================
```

---

## 6. Validation Checklist (Per Document)

Use this checklist for each document validated:

```
Document: ________________________________
Batch: __________________________________
Validator: _______________________________
Date: ___________________________________

ENTITY VALIDATION:
☐ All marked entities exist in source text
☐ No overlapping entity spans
☐ Entity types correct
☐ Confidence scores recorded

RELATIONSHIP VALIDATION:
☐ Both entities in each relationship exist
☐ Entity types match relationship schema
☐ Directionality is logically correct
☐ No duplicate relationships
☐ No self-relations
☐ Relationships make sense in context

METRICS:
☐ Valid entity pairs: ___% (target >= 95%)
☐ Type accuracy: ___% (target >= 90%)
☐ Directionality accuracy: ___% (target >= 92%)
☐ Relationship F1: ___ (target >= 0.75)

CORRECTIONS:
☐ Errors documented: ___
☐ Corrections implemented: ___
☐ Corrections verified: ___

SIGN-OFF:
Document status: ☐ PASS ☐ CONDITIONAL ☐ FAIL
Validator signature: ________________________
Timestamp: ________________________________
```

---

## 7. Timeline and Resource Planning

### Timeline for Tier 3 Validation

**Week 1: Preparation**
- Day 1-2: Team training on schema and rules
- Day 3-4: Process setup and tool configuration
- Day 5: Practice on sample batch

**Week 2-3: Main Validation (Tier 1 - Cognitive Biases)**
- BATCH_01 through BATCH_04 (100% validation)
- Expected: 200 relationships
- Time: ~40 hours
- Validators: 2 full-time

**Week 4-5: Scaling (Tier 2 - Incident Reports)**
- BATCH_05 through BATCH_10 (75-100% validation)
- Expected: 600 relationships
- Time: ~120 hours (75% validation = 90 hours)
- Validators: 2-3 full-time

**Week 6: Quality Gates**
- Process corrections
- Calculate final metrics
- Make go/no-go decisions
- Document learnings

### Resource Requirements

**Per 50-document batch**:
- Relationships to validate: ~300-400
- Validation time: 40-50 hours
- Validators needed: 1-2 people
- Cost: $1,500-2,000 (at $40/hour)

**For full Tier 3 (14 batches)**:
- Total relationships: ~4,000-5,000
- Total validation time: ~500 hours
- Validators: 2-3 FTE × 6 weeks
- Budget: $20,000-25,000

---

## 8. Risk Mitigation

### Common Pitfalls and Prevention

**Pitfall 1: Validator Fatigue**
```
Risk: After 8+ hours of validation, quality drops
Mitigation:
  • 4-hour shifts with 1-hour break
  • Rotate between document types
  • Pair validation (2 validators → compare)
```

**Pitfall 2: Scope Creep**
```
Risk: Adding new relationship types mid-validation
Mitigation:
  • Lock schema before starting
  • Document any schema changes
  • Re-validate affected batches
```

**Pitfall 3: Inconsistent Corrections**
```
Risk: Different validators correct same error differently
Mitigation:
  • Shared decision log
  • Weekly calibration meetings
  • Second-pass review for consistency
```

**Pitfall 4: Missing Context**
```
Risk: Validator doesn't understand document context
Mitigation:
  • Read full document before validating
  • Understand domain terminology
  • Ask domain experts when confused
```

**Pitfall 5: False Positives**
```
Risk: Marking valid relationships as errors
Mitigation:
  • Strict adherence to validation rules
  • When unsure, escalate to lead
  • Document questionable cases
```

---

## 9. Quality Control Steps

### Daily Standup (15 minutes)
```
Each validator reports:
1. Batches completed yesterday
2. Metrics achieved vs targets
3. Top 3 error types encountered
4. Blockers or escalations needed
5. Today's plan
```

### Weekly Calibration (1 hour)
```
Team meets to:
1. Review tricky cases encountered
2. Discuss error patterns
3. Verify consistent corrections
4. Update guidelines if needed
5. Plan next week
```

### Validation Audit (2 hours)
```
Lead reviewer:
1. Re-validates 10% of completed batch
2. Compares with validator results
3. Calculates inter-validator agreement
4. Identifies training needs
```

### Metrics Review (30 minutes)
```
Weekly metrics analysis:
1. Trend analysis (improving or declining?)
2. Metric by relationship type
3. Metric by document category
4. Identification of weak areas
5. Recommendations for focus
```

---

## 10. Success Indicators

### You're on track when...

- [ ] Valid Entity Pairs consistently > 94%
- [ ] Type Accuracy consistently > 88%
- [ ] Directionality Accuracy consistently > 90%
- [ ] Relationship F1 trending toward >= 0.75
- [ ] Inter-validator agreement > 0.80
- [ ] Error correction rate > 85%
- [ ] Timeline on schedule
- [ ] Team morale positive
- [ ] No critical blockers

### Red flags requiring intervention...

- [ ] Metrics dropping below 80% of target
- [ ] Validators disagreeing on > 15% of cases
- [ ] Batch completion > 2 days late
- [ ] Validator burnout signals
- [ ] Schema ambiguity causing errors
- [ ] High volume of CONTEXT_MISMATCH errors

---

## Final Notes

### Key Reminders

1. **Quality over speed**: Better to be 20% late with 95% accuracy than on-time with 70%
2. **Communication**: Ask questions before marking things wrong
3. **Documentation**: Every error should be logged with rationale
4. **Validation**: Have someone else spot-check your work
5. **Learning**: Keep improving based on patterns you see

### Escalation Path

When uncertain, escalate to:
1. Batch Lead (schema interpretation)
2. Project Manager (timeline/resource issues)
3. NER Specialist (technical entity questions)
4. Subject Matter Expert (domain-specific cases)

### Success Definition

**Tier 3 is COMPLETE when**:
- Overall Relationship F1 >= 0.75
- All 7 metrics meet targets
- All corrections documented
- Ready to proceed to Tier 4

---

**Ready to start?** Begin with Section 1 (5-Minute Overview), then jump to Section 4 (Batch Workflow) for your first batch.

Good luck with validation!
