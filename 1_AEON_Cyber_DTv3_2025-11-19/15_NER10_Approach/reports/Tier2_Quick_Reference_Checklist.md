# Tier 2 Entity Type Validation - Quick Reference Checklist

**For Rapid Execution When Tier 1 Complete**
**File**: Tier2_Quick_Reference_Checklist.md
**Created**: 2025-11-25

---

## Pre-Execution Checklist

- [ ] Tier 1 boundary review COMPLETE
- [ ] Tier1_Boundary_Corrections.json available
- [ ] Prodigy database accessible OR JSONL files available
- [ ] Expert reviewer assigned (NLP + psychology expertise)
- [ ] Python environment ready (pandas, sklearn, spacy)
- [ ] Validation interface prepared (spreadsheet or custom UI)

---

## Execution Checklist (8 Steps)

### Step 1: Load Tier 1 Data
- [ ] Load Tier1_Boundary_Corrections.json
- [ ] Verify 678 files present
- [ ] Check entity structure: text, label, start, end, attributes
- [ ] Create DataFrame with entity_id, file_source, context

**Command**:
```python
import pandas as pd
import json

with open('Tier1_Boundary_Corrections.json') as f:
    data = json.load(f)
df = pd.DataFrame(data['entities'])
print(f"Loaded {len(df)} entities from {df['file_source'].nunique()} files")
```

### Step 2: Random Sampling
- [ ] Stratified random sample 169 files (25%)
- [ ] Stratification by: category, length, entity density
- [ ] Save sample file list
- [ ] Verify stratification balance

**Command**:
```python
from sklearn.model_selection import train_test_split

files = df['file_source'].unique()
sample_files, _ = train_test_split(files, test_size=0.75, stratify=categories, random_state=42)
print(f"Sampled {len(sample_files)} files")
```

### Step 3: Entity Extraction
- [ ] Extract entities from sampled files
- [ ] Target: ~2,535 entities
- [ ] Include context window (±50 chars)
- [ ] Save entity validation dataset

**Command**:
```python
validation_df = df[df['file_source'].isin(sample_files)].copy()
print(f"Extracted {len(validation_df)} entities for validation")
```

### Step 4: Manual Type Review
- [ ] Review each entity with context
- [ ] Check type against schema guidelines
- [ ] Validate attributes (bias_type, perception_type, motivation_type)
- [ ] Log corrections with rationale
- [ ] Track time per entity (target: 2 min/entity)

**Review Questions Per Type**:

**COGNITIVE_BIAS**:
- [ ] Is bias one of 30 defined types?
- [ ] Is bias_type attribute correct?
- [ ] Is bias_category correct?

**THREAT_PERCEPTION**:
- [ ] Is perception_type Real|Imaginary|Symbolic?
- [ ] Is evidence_level appropriate?

**ATTACKER_MOTIVATION**:
- [ ] Fits MICE or additional motives?
- [ ] motivation_type correct?

**EMOTION**:
- [ ] Distinguishable from DEFENSE_MECHANISM?

**EQUIPMENT**:
- [ ] ICS-specific, not general IT?
- [ ] Not confused with FACILITY?

**CVE**:
- [ ] Matches CVE-YYYY-NNNNN format?

**TECHNIQUE**:
- [ ] Not confused with PROCESS?

**THREAT_ACTOR**:
- [ ] Not confused with ORGANIZATION?

### Step 5: Automated Checks
- [ ] Run attribute completeness check
- [ ] Run CVE format validation
- [ ] Run bias_type vocabulary check
- [ ] Run perception_type vocabulary check
- [ ] Run entity distribution check
- [ ] Flag anomalies for review

**Command**:
```python
# Attribute completeness
cognitive_bias = validation_df[validation_df['label'] == 'COGNITIVE_BIAS']
missing_bias_type = cognitive_bias[cognitive_bias['attributes'].apply(lambda x: 'bias_type' not in x)]
print(f"Missing bias_type: {len(missing_bias_type)} entities")

# CVE format
import re
cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')
cves = validation_df[validation_df['label'] == 'CVE']
invalid_cves = cves[~cves['text'].str.match(cve_pattern)]
print(f"Invalid CVE format: {len(invalid_cves)} entities")
```

### Step 6: Confusion Matrix
- [ ] Create 18x18 confusion matrix
- [ ] Calculate precision per type
- [ ] Calculate recall per type
- [ ] Calculate F1 per type
- [ ] Generate heatmap visualization
- [ ] Export as Tier2_Confusion_Matrix.png

**Command**:
```python
from sklearn.metrics import confusion_matrix, classification_report, f1_score
import seaborn as sns
import matplotlib.pyplot as plt

y_true = validation_df['correct_type']  # From manual review
y_pred = validation_df['label']  # Original annotation

cm = confusion_matrix(y_true, y_pred, labels=entity_types)
report = classification_report(y_true, y_pred, target_names=entity_types)

print(report)

# Heatmap
plt.figure(figsize=(15, 12))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=entity_types, yticklabels=entity_types)
plt.title('Tier 2 Entity Type Confusion Matrix')
plt.savefig('Tier2_Confusion_Matrix.png', dpi=300, bbox_inches='tight')
```

### Step 7: Apply Corrections
- [ ] Load correction log from manual review
- [ ] Update entity types in annotation data
- [ ] Update attributes where needed
- [ ] Validate updates applied correctly
- [ ] Export Tier2_Corrected_Annotations.jsonl

**Command**:
```python
# Apply corrections
for idx, row in corrections_df.iterrows():
    entity_id = row['entity_id']
    new_type = row['corrected_type']
    new_attributes = row['corrected_attributes']

    df.loc[df['entity_id'] == entity_id, 'label'] = new_type
    df.loc[df['entity_id'] == entity_id, 'attributes'] = new_attributes

# Export
df.to_json('Tier2_Corrected_Annotations.jsonl', orient='records', lines=True)
print(f"Exported {len(df)} corrected entities")
```

### Step 8: Validation Report
- [ ] Calculate final F1 scores per type
- [ ] Summarize correction statistics
- [ ] Identify top confusion patterns
- [ ] Document guideline recommendations
- [ ] Generate Tier2_Type_Validation_Report.json

---

## Quality Metric Checklist

### Type F1 Scores
- [ ] **PRIMARY GOAL**: 16+ types achieve F1 > 0.80
- [ ] COGNITIVE_BIAS: F1 > 0.75 (acceptable if challenging)
- [ ] THREAT_PERCEPTION: F1 > 0.80
- [ ] EMOTION: F1 > 0.80
- [ ] ATTACKER_MOTIVATION: F1 > 0.85
- [ ] EQUIPMENT: F1 > 0.85
- [ ] CVE: F1 > 0.95
- [ ] TECHNIQUE: F1 > 0.80
- [ ] THREAT_ACTOR: F1 > 0.85
- [ ] (Check all 18 types)

### Attribute Accuracy
- [ ] bias_type accuracy > 0.90
- [ ] perception_type accuracy > 0.90
- [ ] motivation_type accuracy > 0.90

### Overall Metrics
- [ ] Overall classification accuracy > 0.85
- [ ] Inter-reviewer agreement (Cohen's Kappa) > 0.85
- [ ] Correction rate < 0.20 (acceptable up to 20%)

---

## Common Confusions to Watch For

### Technical Confusions
- [ ] EQUIPMENT vs FACILITY (location vs device)
- [ ] TECHNIQUE vs PROCESS (attack vs workflow)
- [ ] ORGANIZATION vs THREAT_ACTOR (legitimate vs malicious)

### Psychological Confusions
- [ ] EMOTION vs DEFENSE_MECHANISM (feeling vs coping)
- [ ] COGNITIVE_BIAS vs DEFENSE_MECHANISM (thinking error vs protection)
- [ ] THREAT_PERCEPTION subtypes (Real vs Imaginary vs Symbolic)

---

## Escalation Triggers

### File-Level Escalation
- [ ] >20% of entities in file require reclassification
- **Action**: Flag file for complete re-annotation

### Type-Level Escalation
- [ ] >30% of specific entity type misclassified
- **Action**: Review guidelines, re-train annotators

### Confusion-Level Escalation
- [ ] >15% systematic confusion between two types
- **Action**: Add disambiguation examples to guidelines

---

## Deliverables Checklist

- [ ] **Tier2_Corrected_Annotations.jsonl** (main output)
- [ ] **Tier2_Type_Validation_Report.json** (comprehensive report)
- [ ] **Tier2_Confusion_Matrix.png** (heatmap visualization)
- [ ] **Tier2_Correction_Log.csv** (detailed correction log)
- [ ] **Tier2_Guideline_Recommendations.md** (improvement suggestions)

---

## Pass/Fail Decision

### 🟢 GREEN LIGHT (Pass)
- [ ] F1 > 0.80 for 16+ entity types
- [ ] Overall accuracy > 0.85
- [ ] Attribute accuracy > 0.90
- **Action**: Proceed to Tier 3 (Relationship Validation)

### 🟡 YELLOW LIGHT (Conditional Pass)
- [ ] F1 0.75-0.80 for 13-15 types
- [ ] Overall accuracy 0.80-0.85
- **Action**: Targeted guideline improvements + re-annotate problem types

### 🔴 RED LIGHT (Fail)
- [ ] F1 < 0.75 for >5 types
- [ ] Overall accuracy < 0.80
- **Action**: Major guideline revision + re-annotate all files

---

## Time Tracking

- [ ] Day 1: Load data, sampling, extraction (complete by EOD)
- [ ] Day 2: Manual review entities 1-1200 (target: 1200/day)
- [ ] Day 3: Manual review entities 1201-2535 (complete by EOD)
- [ ] Day 4: Automated checks, confusion matrix (complete by EOD)
- [ ] Day 5: Apply corrections, generate reports (complete by EOD)
- [ ] Day 6-7: Quality review, guideline recommendations (buffer)

**Total Duration**: 5-7 days

---

## Quick Validation Commands

### Load and Inspect
```python
import pandas as pd
df = pd.read_json('Tier2_Corrected_Annotations.jsonl', lines=True)
print(df.groupby('label').size())
```

### F1 Calculation
```python
from sklearn.metrics import f1_score
entity_types = df['label'].unique()
for etype in entity_types:
    binary_df = df.copy()
    binary_df['is_type'] = binary_df['label'] == etype
    binary_df['correct_is_type'] = binary_df['correct_type'] == etype
    f1 = f1_score(binary_df['correct_is_type'], binary_df['is_type'])
    print(f"{etype}: F1 = {f1:.3f}")
```

### Confusion Matrix
```python
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(df['correct_type'], df['label'])
print(cm)
```

---

## Notes & Tips

1. **Take breaks during manual review** - Type validation is cognitively demanding
2. **Document ambiguous cases** - These inform guideline improvements
3. **Flag systematic patterns early** - Don't wait until full review complete
4. **Use context liberally** - ±50 chars often insufficient, read full paragraph
5. **When in doubt, consult schema** - Guidelines are the source of truth
6. **Track correction rationale** - Future annotators benefit from your reasoning

---

**File**: /home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/15_NER10_Approach/reports/Tier2_Quick_Reference_Checklist.md
**Related**: Tier2_Type_Review.json, Tier2_Type_Review_Summary.md
**Execute When**: Tier 1 complete
