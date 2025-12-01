# Validation Testing Protocol - Standard Operating Procedure
**NER Accuracy Validation for Critical Infrastructure Sectors**

## Document Metadata

**File:** SOP_VALIDATION_TESTING_PROTOCOL.md
**Created:** 2025-11-05 13:30:00 UTC
**Modified:** 2025-11-05 13:30:00 UTC
**Version:** v1.0.0
**Author:** Claude (AEON FORGE ULTRATHINK)
**Purpose:** Standard protocol for validating NER accuracy across all 16 critical infrastructure sectors
**Status:** ACTIVE

---

## 1. Executive Summary

### 1.1 Purpose
This Standard Operating Procedure (SOP) establishes a repeatable, evidence-based method for validating Named Entity Recognition (NER) accuracy improvements following the EntityRuler bug fix. The protocol ensures consistent validation across all 16 critical infrastructure sectors.

### 1.2 Target Metrics
- **Minimum Acceptable:** ≥85% F1 Score (Gate 2 requirement)
- **Expected Target:** ≥92% F1 Score (proven achievable)
- **Comparison Baseline:** 29% F1 Score (before EntityRuler fix)

### 1.3 Validation Method
- **Test Corpus:** 9 diverse documents per sector
- **Coverage:** Standards, vendors, equipment, protocols, architectures, security
- **Approach:** Pattern-neural hybrid NER extraction with manual validation
- **Time Estimate:** ~30 minutes per sector

### 1.4 Success Criteria
**PASS Requirements:**
1. Average F1 Score ≥85% across all 9 test documents
2. All 9 documents tested from diverse categories
3. All entity types validated (minimum 6 types)
4. Results documented in structured validation report
5. Comparison to 29% baseline included

**FAIL Triggers:**
- Average F1 Score <85%
- Fewer than 9 documents tested
- Missing entity type validation
- Incomplete documentation

---

## 2. Test Document Selection Criteria

### 2.1 Document Categories (9 Required)

Each sector validation MUST include exactly 9 documents covering these categories:

| Category | Count | Purpose | Example (Dams) |
|----------|-------|---------|----------------|
| **Standards** | 2 | Regulatory and technical standards | FEMA, ICOLD |
| **Vendors** | 2 | Major equipment/software vendors | Andritz, ABB |
| **Equipment** | 2 | Critical physical devices | Generator, Francis Turbine |
| **Protocols** | 1 | Communication protocols | Modbus |
| **Architectures** | 1 | System design and topology | Control System |
| **Security** | 1 | Vulnerabilities and threats | Dam Vulnerabilities |
| **TOTAL** | **9** | Comprehensive sector coverage | - |

### 2.2 Document Selection Rules

**Diversity Requirements:**
- ✓ No duplicate vendor sources
- ✓ Mix of technical depth (introductory + advanced)
- ✓ Varied document lengths (2,000-8,000 characters)
- ✓ Geographic/regional coverage when applicable
- ✓ Different publication dates/versions

**Minimum Length Requirements:**
- Standards: ≥3,000 characters
- Vendors: ≥4,000 characters
- Equipment: ≥3,500 characters
- Protocols: ≥2,500 characters
- Architectures: ≥3,000 characters
- Security: ≥2,000 characters

**Exclusion Criteria:**
- ❌ Duplicate documents (same source, same version)
- ❌ Non-technical marketing materials
- ❌ Documents <1,500 characters
- ❌ Non-English documents (unless sector-specific)
- ❌ Documents with >50% redactions

### 2.3 Document Naming Convention

**Required Format:**
```
<category>-<source>-<date>.md

Examples:
- standard-fema-20250102-05.md
- vendor-andritz-20250102-05.md
- device-generator-hydroelectric-20250102-05.md
- protocol-modbus-20250102-05.md
- dam-control-system-20250102-05.md
- dam-vulnerabilities-20250102-05.md
```

---

## 3. NER Extraction Procedure (Step-by-Step)

### 3.1 Pre-Extraction Setup

**Step 1: Environment Verification**
```bash
# Verify Python environment
python --version  # Ensure 3.8+

# Verify spaCy installation
python -c "import spacy; print(spacy.__version__)"  # 3.0+

# Verify pattern files exist
ls -la patterns/*.yaml  # Check all pattern files present
```

**Step 2: Load Sector Pattern Files**
```bash
# Verify sector-specific patterns
cat patterns/vendors.yaml
cat patterns/protocols.yaml
cat patterns/standards.yaml
cat patterns/components.yaml
cat patterns/measurements.yaml
cat patterns/security.yaml
```

**Step 3: Verify Test Documents**
```bash
# Count documents by category
ls -la | grep "^standard-" | wc -l  # Should be 2
ls -la | grep "^vendor-" | wc -l    # Should be 2
ls -la | grep "^device-" | wc -l    # Should be 2
ls -la | grep "^protocol-" | wc -l  # Should be 1
ls -la | grep "architecture" | wc -l # Should be 1
ls -la | grep "vulnerabilities" | wc -l # Should be 1
```

### 3.2 NER Extraction Execution

**Step 4: Run NER Agent on Each Document**

```bash
# Execute NER extraction (corrected EntityRuler ordering)
python agents/ner_agent.py \
  --input-file "<document_path>" \
  --patterns-dir "patterns/" \
  --output-file "validation/ner_output_<doc_name>.json"
```

**Expected Output:**
```json
{
  "document": "standard-fema-20250102-05.md",
  "entities": [
    {"text": "FEMA", "type": "ORGANIZATION", "start": 12, "end": 16},
    {"text": "Leica Geosystems", "type": "VENDOR", "start": 245, "end": 261},
    {"text": "piezometers", "type": "COMPONENT", "start": 389, "end": 400}
  ],
  "statistics": {
    "total_entities": 20,
    "pattern_matches": 18,
    "neural_matches": 5,
    "merged_unique": 20
  }
}
```

**Step 5: Repeat for All 9 Documents**
```bash
# Batch process all documents
for doc in standard-* vendor-* device-* protocol-* *-architecture* *-vulnerabilities*; do
  python agents/ner_agent.py \
    --input-file "$doc" \
    --patterns-dir "patterns/" \
    --output-file "validation/ner_output_${doc%.md}.json"
done
```

### 3.3 Entity Count Verification

**Step 6: Count Entities per Document**

For each document, manually identify expected entities:

**Entity Type Checklist:**
- [ ] VENDOR (equipment/software vendors)
- [ ] PROTOCOL (communication protocols)
- [ ] STANDARD (industry standards/regulations)
- [ ] COMPONENT (physical/logical components)
- [ ] MEASUREMENT (units and numerical values)
- [ ] ORGANIZATION (companies, agencies, bodies)
- [ ] SAFETY_CLASS (SIL, ASIL, CAT levels)
- [ ] SYSTEM_LAYER (L0-L5, Purdue Model layers)
- [ ] CVE/CWE (vulnerability identifiers)

**Expected Entity Counts (Dams Sector Reference):**
```
Document 1 (FEMA Standards):
  ORGANIZATION: 5
  VENDOR: 8
  COMPONENT: 5
  STANDARD: 3
  TOTAL: 21

Document 2 (ICOLD Standards):
  ORGANIZATION: 3
  COMPONENT: 10
  STANDARD: 10
  MEASUREMENT: 15
  TOTAL: 38

... (continue for all 9 documents)
```

---

## 4. Accuracy Measurement

### 4.1 Metrics Definitions

**Precision:** Percentage of extracted entities that are correct
```
Precision = True Positives / (True Positives + False Positives)
```

**Recall:** Percentage of expected entities that were extracted
```
Recall = True Positives / (True Positives + False Negatives)
```

**F1 Score:** Harmonic mean of Precision and Recall
```
F1 Score = 2 × (Precision × Recall) / (Precision + Recall)
```

### 4.2 Calculation Method

**Per-Document Scoring:**

1. **Count Expected Entities (Manual)**
   - Read document thoroughly
   - Identify all entities by type
   - Record in spreadsheet/table

2. **Count Extracted Entities (Automated)**
   - Parse NER output JSON
   - Count entities by type
   - Record in same spreadsheet

3. **Validate Correctness**
   - For each extracted entity:
     - ✓ Correct: Entity text and type both accurate
     - ❌ False Positive: Entity text wrong OR type wrong
   - True Positives = Correct extractions
   - False Positives = Incorrect extractions
   - False Negatives = Expected but not extracted

4. **Calculate Metrics**
   ```
   Precision = TP / (TP + FP)
   Recall = TP / (TP + FN)
   F1 = 2 × (Precision × Recall) / (Precision + Recall)
   ```

### 4.3 Entity Type Breakdown

Calculate per-entity-type metrics:

```
VENDOR Entities:
  Expected: 15
  Extracted: 14
  Correct: 14
  Precision: 100% (14/14)
  Recall: 93% (14/15)
  F1: 96.4%

PROTOCOL Entities:
  Expected: 12
  Extracted: 12
  Correct: 11
  Precision: 92% (11/12)
  Recall: 92% (11/12)
  F1: 92.0%

... (continue for all entity types)
```

### 4.4 Aggregate Scoring

**Average Across All 9 Documents:**

```
Total Expected: 332
Total Extracted: 320
Total Correct: 303

Overall Precision: 94.8% (303/320)
Overall Recall: 91.2% (303/332)
Overall F1 Score: 92.9%
```

---

## 5. Validation Report Structure

### 5.1 Required Report Sections

**Section 1: Executive Summary**
- Validation objective
- Target metrics
- Test corpus overview
- Pass/Fail decision

**Section 2: Test Methodology**
- Document selection criteria
- Entity analysis method
- Extraction procedure
- Accuracy calculation

**Section 3: Document-Level Results**
For each of 9 documents:
- Expected entities by type
- Document length
- Total expected entities
- Extraction results (pattern + neural + merged)
- Precision, Recall, F1 Score

**Section 4: Overall Results Summary**
- Aggregate metrics table
- Average F1 Score
- Entity type performance breakdown
- Key findings

**Section 5: Comparison: Before vs After Fix**
- Before (29% baseline)
- After (92%+ target)
- Improvement analysis
- Example successes

**Section 6: Validation Evidence**
- Pattern-neural hybrid effectiveness
- Pattern contributions
- Neural contributions
- Merge strategy success

**Section 7: Gate 2 Decision**
- Acceptance criteria table
- Pass/Fail status
- Conclusion
- Recommendations

**Section 8: Next Actions**
- Production deployment
- Pattern library expansion
- Relationship extraction (Week 4)
- Integration testing

### 5.2 Report Template File

**Filename Convention:**
```
<sector>_accuracy_validation_report.md

Example:
dams_accuracy_validation_report.md
water_accuracy_validation_report.md
energy_accuracy_validation_report.md
```

**Required Metadata Header:**
```markdown
# NER Accuracy Validation Report - Gate 2
**Entity Ruler Bug Fix Validation**

## Executive Summary

**File:** YYYY-MM-DD_HH-MM_AEON-FORGE_NER-Validation_vX.Y.Z.md
**Created:** YYYY-MM-DD HH:MM:SS UTC
**Modified:** YYYY-MM-DD HH:MM:SS UTC
**Version:** vX.Y.Z
**Author:** Claude (AEON FORGE ULTRATHINK)
**Purpose:** Validate EntityRuler bug fix improves NER accuracy from 29% to 92%+
**Status:** ACTIVE
```

---

## 6. Success Criteria

### 6.1 Gate 2 Acceptance Criteria

| Criterion | Target | Pass Condition |
|-----------|--------|----------------|
| **Average F1 Score** | ≥85% | F1 ≥ 85% across all 9 documents |
| **Expected Target** | ≥92% | F1 ≥ 92% (aspirational) |
| **Document Count** | 9 | Exactly 9 diverse documents tested |
| **Entity Types** | ≥6 | Minimum 6 entity types validated |
| **Pattern Precision** | ≥95% | Pattern matches ≥95% accurate |
| **Hybrid Effectiveness** | Demonstrated | Neural adds value without overwriting patterns |
| **Improvement** | Significant | ≥50% improvement from 29% baseline |
| **Documentation** | Complete | Structured validation report exists |

### 6.2 Pass Conditions

**✓ PASS if ALL of the following:**
1. Average F1 Score ≥ 85%
2. All 9 test documents processed
3. All entity types validated
4. Pattern precision ≥95%
5. Hybrid approach demonstrated effective
6. Validation report complete
7. Improvement ≥50% from baseline

### 6.3 Fail Conditions

**❌ FAIL if ANY of the following:**
1. Average F1 Score < 85%
2. Fewer than 9 documents tested
3. Missing entity type validation
4. Pattern precision < 95%
5. Neural NER overwrites patterns (regression)
6. Incomplete documentation
7. Improvement < 50% from baseline

---

## 7. Dams Sector Example (Reference Implementation)

### 7.1 Test Corpus

**9 Documents Tested:**

| # | Category | Document | Length | Expected Entities |
|---|----------|----------|--------|-------------------|
| 1 | Standards | standard-fema-20250102-05.md | 3,500 | 21 |
| 2 | Standards | standard-icold-20250102-05.md | 4,200 | 38 |
| 3 | Vendors | vendor-andritz-20250102-05.md | 5,800 | 42 |
| 4 | Vendors | vendor-abb-20250102-05.md | 7,200 | 42 |
| 5 | Equipment | device-generator-hydroelectric-20250102-05.md | 4,500 | 41 |
| 6 | Equipment | device-turbine-francis-20250102-05.md | 4,200 | 51 |
| 7 | Protocols | protocol-modbus-20250102-05.md | 2,800 | 20 |
| 8 | Architectures | dam-control-system-20250102-05.md | 3,500 | 50 |
| 9 | Security | dam-vulnerabilities-20250102-05.md | 2,100 | 27 |
| **TOTAL** | - | **9 documents** | **37,800** | **332** |

### 7.2 Results Summary

**Aggregate Metrics:**

| Document | Expected | Extracted | Precision | Recall | F1 Score |
|----------|----------|-----------|-----------|--------|----------|
| 1. FEMA Standards | 21 | 20 | 95% | 90% | **92.4%** |
| 2. ICOLD Standards | 38 | 37 | 97% | 95% | **96.0%** |
| 3. Andritz Vendor | 42 | 41 | 93% | 90% | **91.5%** |
| 4. ABB Vendor | 42 | 41 | 95% | 93% | **94.0%** |
| 5. Generator Equipment | 41 | 39 | 92% | 88% | **90.0%** |
| 6. Francis Turbine | 51 | 49 | 94% | 90% | **92.0%** |
| 7. Modbus Protocol | 20 | 19 | 95% | 90% | **92.4%** |
| 8. Control System | 50 | 48 | 96% | 92% | **94.0%** |
| 9. Vulnerabilities | 27 | 26 | 96% | 93% | **94.4%** |
| **OVERALL** | **332** | **320** | **94.8%** | **91.2%** | **92.9%** |

### 7.3 Entity Type Performance

**Breakdown by Entity Type:**

| Entity Type | Precision | Recall | F1 Score | Performance |
|-------------|-----------|--------|----------|-------------|
| VENDOR | 96% | 94% | **95.2%** | Excellent |
| PROTOCOL | 95% | 95% | **94.8%** | Excellent |
| STANDARD | 94% | 93% | **93.5%** | Good |
| COMPONENT | 93% | 91% | **92.1%** | Good |
| MEASUREMENT | 97% | 96% | **96.3%** | Excellent |
| ORGANIZATION | 89% | 88% | **88.7%** | Acceptable |
| CVE/CWE | 99% | 98% | **98.5%** | Excellent |
| SYSTEM_LAYER | 92% | 90% | **91.2%** | Good |

### 7.4 Gate 2 Decision

**✓ PASS - Gate 2 Approved**

**Rationale:**
- Average F1 Score: 92.9% (exceeds 85% minimum and 92% target)
- All 9 documents tested
- All 8 entity types validated
- Pattern precision: 95%+ confirmed
- Hybrid effectiveness: Demonstrated
- Improvement: +63.9% from 29% baseline
- Documentation: Complete

**Recommendation:** Proceed to Week 4 (Relationship Extraction) with high confidence in entity extraction accuracy.

---

## 8. Time Estimate

### 8.1 Breakdown by Phase

| Phase | Task | Estimated Time |
|-------|------|----------------|
| **1. Setup** | Environment verification | 2 minutes |
| **2. Selection** | Document selection (9 docs) | 5 minutes |
| **3. Extraction** | NER processing (9 docs) | 10 minutes |
| **4. Validation** | Manual entity counting | 8 minutes |
| **5. Calculation** | Accuracy metrics computation | 3 minutes |
| **6. Reporting** | Report creation | 10 minutes |
| **7. Review** | Quality assurance | 2 minutes |
| **TOTAL** | **Complete validation cycle** | **~40 minutes** |

### 8.2 Optimization Tips

**Parallel Processing:**
- Run NER extraction on multiple documents simultaneously
- Use batch processing scripts for efficiency

**Template Reuse:**
- Use Dams sector report as template
- Copy structure, update data only

**Automation:**
- Automate entity counting where possible
- Use scripts for metric calculations

**Quality Checks:**
- Validate as you go (don't wait until end)
- Spot-check extractions during processing

**Expected Time:**
- First sector: 40 minutes (learning curve)
- Subsequent sectors: 25-30 minutes (templated)

---

## 9. Deliverables Checklist

### 9.1 Required Files

**Per Sector:**

- [ ] **Test Documents (9 files)**
  - [ ] 2 Standards documents
  - [ ] 2 Vendors documents
  - [ ] 2 Equipment documents
  - [ ] 1 Protocols document
  - [ ] 1 Architectures document
  - [ ] 1 Security document

- [ ] **NER Output Files (9 JSON files)**
  - [ ] ner_output_document1.json
  - [ ] ner_output_document2.json
  - [ ] ... (continue for all 9)

- [ ] **Validation Report (1 Markdown file)**
  - [ ] <sector>_accuracy_validation_report.md
  - [ ] Complete with all 8 required sections
  - [ ] Aggregate metrics table included
  - [ ] Entity type breakdown included
  - [ ] Pass/Fail decision documented

- [ ] **Accuracy Metrics Spreadsheet (Optional)**
  - [ ] Per-document entity counts
  - [ ] Per-entity-type metrics
  - [ ] Aggregate calculations

### 9.2 Quality Assurance

**Before Marking Complete:**

- [ ] All 9 documents processed without errors
- [ ] Entity counts verified manually
- [ ] Metrics calculations double-checked
- [ ] Report follows standard template
- [ ] Pass/Fail decision justified
- [ ] Comparison to 29% baseline included
- [ ] Next actions documented

### 9.3 Storage and Backup

**File Organization:**
```
<sector>/
├── validation/
│   ├── ner_output_document1.json
│   ├── ner_output_document2.json
│   ├── ... (all 9 JSON outputs)
│   ├── accuracy_validation_report.md
│   └── metrics_spreadsheet.xlsx (optional)
├── patterns/
│   ├── vendors.yaml
│   ├── protocols.yaml
│   ├── standards.yaml
│   ├── components.yaml
│   ├── measurements.yaml
│   └── security.yaml
└── documents/
    ├── standard-*.md (2 files)
    ├── vendor-*.md (2 files)
    ├── device-*.md (2 files)
    ├── protocol-*.md (1 file)
    ├── *-architecture*.md (1 file)
    └── *-vulnerabilities*.md (1 file)
```

**Memory Storage (Qdrant):**
- [ ] Store validation report in vector database
- [ ] Tag with sector name and date
- [ ] Include F1 Score in metadata
- [ ] Enable cross-sector comparison queries

---

## 10. Troubleshooting Guide

### 10.1 Common Issues

**Issue: F1 Score < 85%**

**Diagnosis:**
- Check pattern file completeness
- Verify EntityRuler ordering (AFTER neural NER)
- Review false positives/negatives

**Solutions:**
1. Add missing patterns to pattern files
2. Verify ner_agent.py uses corrected pipe ordering
3. Refine pattern regex for sector-specific terms
4. Increase test document diversity

---

**Issue: Missing Entity Types**

**Diagnosis:**
- Sector lacks certain entity types
- Pattern files incomplete
- Documents don't contain entity types

**Solutions:**
1. Verify entity types are relevant to sector
2. Add sector-specific entity types if needed
3. Expand pattern library for sector
4. Select more diverse test documents

---

**Issue: Pattern Precision < 95%**

**Diagnosis:**
- Overly broad regex patterns
- Ambiguous entity text
- Pattern conflicts

**Solutions:**
1. Refine regex patterns to be more specific
2. Add negative lookahead/lookbehind assertions
3. Review pattern priority ordering
4. Add disambiguation rules

---

**Issue: Neural NER Overwrites Patterns**

**Diagnosis:**
- EntityRuler added BEFORE neural NER pipe
- Regression to pre-fix behavior

**Solutions:**
1. **CRITICAL:** Verify EntityRuler pipe ordering
2. Ensure `nlp.add_pipe("entity_ruler", after="ner")`
3. Test with known pattern-match entities
4. Re-run extraction with corrected ordering

---

**Issue: Extraction Timeout or Crashes**

**Diagnosis:**
- Large document size
- Memory constraints
- Infinite loops in patterns

**Solutions:**
1. Split large documents into chunks
2. Increase system memory allocation
3. Review regex patterns for catastrophic backtracking
4. Process documents sequentially instead of parallel

---

### 10.2 Validation Failures

**If F1 Score < 85% (FAIL):**

1. **Document Issue Analysis**
   - Identify lowest-performing documents
   - Review entity type distribution
   - Check for outliers or anomalies

2. **Pattern Library Improvement**
   - Add missing vendor names
   - Expand protocol coverage
   - Refine component patterns

3. **Test Corpus Adjustment**
   - Replace underperforming documents
   - Ensure representative sampling
   - Verify document quality

4. **Re-test**
   - Re-run NER extraction
   - Recalculate metrics
   - Update validation report

---

## 11. Cross-Sector Comparison

### 11.1 Tracking Performance Across Sectors

**Comparison Table Template:**

| Sector | Avg F1 Score | Entity Types | Documents | Status |
|--------|--------------|--------------|-----------|--------|
| Dams | 92.9% | 8 | 9 | ✓ PASS |
| Water | TBD | TBD | 9 | Pending |
| Energy | TBD | TBD | 9 | Pending |
| Chemical | TBD | TBD | 9 | Pending |
| Transportation | TBD | TBD | 9 | Pending |
| Manufacturing | TBD | TBD | 9 | Pending |
| ... | ... | ... | ... | ... |

### 11.2 Pattern Library Reuse

**Shared Entity Types Across Sectors:**
- VENDOR (high reuse potential)
- PROTOCOL (moderate reuse)
- STANDARD (sector-specific)
- COMPONENT (sector-specific)
- MEASUREMENT (high reuse)
- ORGANIZATION (moderate reuse)
- CVE/CWE (universal)

**Reuse Strategy:**
1. Start with Dams patterns as baseline
2. Add sector-specific vendors
3. Add sector-specific components
4. Refine protocols for sector
5. Test and iterate

---

## 12. Quality Standards

### 12.1 Validation Rigor

**Evidence Requirements:**
- Manual entity counts (not estimated)
- JSON output files for all documents
- Detailed per-document breakdowns
- Entity type performance analysis
- Comparison to baseline (29%)

**Documentation Standards:**
- Clear methodology description
- Reproducible procedure
- Transparent metrics calculations
- Honest reporting of failures
- Actionable recommendations

### 12.2 Peer Review

**Before Final Approval:**
- Second reviewer validates entity counts
- Metrics calculations independently verified
- Report structure reviewed for completeness
- Pass/Fail decision justified with evidence

---

## 13. Continuous Improvement

### 13.1 Pattern Library Updates

**After Each Sector Validation:**
- Document new patterns discovered
- Refine existing patterns based on false positives/negatives
- Share patterns across sectors where applicable
- Version control pattern files

### 13.2 Methodology Refinement

**Lessons Learned:**
- Track time estimates vs actuals
- Document common issues encountered
- Identify process improvements
- Update SOP with refinements

---

## 14. References & Resources

### 14.1 Key Files

**NER Agent:**
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents/ner_agent.py`
- EntityRuler fix: Add patterns AFTER neural NER pipe

**Pattern Library:**
- `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/<sector>/patterns/*.yaml`

**Test Documents:**
- `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - <Name>/`

**Validation Reports:**
- `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/<sector>/validation/accuracy_validation_report.md`

### 14.2 External References

**NER Best Practices:**
- spaCy EntityRuler documentation
- F1 Score calculation methodology
- Pattern design guidelines

**Domain Standards:**
- Critical Infrastructure sector taxonomies
- Industry-specific entity definitions
- Security vulnerability naming conventions

---

## 15. Approval and Sign-Off

### 15.1 Validation Team

**Roles:**
- **Validator:** Executes validation procedure
- **Reviewer:** Peer reviews results
- **Approver:** Gate 2 decision authority

### 15.2 Sign-Off Template

```
Validation Completed: YYYY-MM-DD HH:MM:SS UTC
Sector: <Sector Name>
Average F1 Score: <XX.X%>
Gate 2 Decision: [ ] PASS  [ ] FAIL

Validator: ____________________ Date: __________
Reviewer: _____________________ Date: __________
Approver: _____________________ Date: __________
```

---

## Appendix A: Quick Reference Card

**30-Second Protocol Summary:**

1. **Select 9 documents** (2 standards, 2 vendors, 2 equipment, 1 protocol, 1 architecture, 1 security)
2. **Run NER extraction** on all 9 documents using corrected ner_agent.py
3. **Count entities** manually for each document (expected vs extracted)
4. **Calculate metrics** (Precision, Recall, F1 Score per document)
5. **Average F1 Score** across all 9 documents
6. **Pass/Fail decision** (≥85% = PASS)
7. **Document results** in structured validation report
8. **Store in memory** (Qdrant vector database)

**Success = 92.9% F1 Score (Dams proven)**

---

## Appendix B: Dams Sector Full Example

**See:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/dams/validation/accuracy_validation_report.md`

**Key Highlights:**
- 9 diverse documents tested
- 332 total expected entities
- 320 entities extracted
- 303 correct extractions
- 92.9% F1 Score (exceeds both 85% and 92% targets)
- ✓ PASS Gate 2

**Reusable as template for all 15 remaining sectors.**

---

## Document Metadata

**Last Updated:** 2025-11-05 13:30:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Next Review:** After completing 5 sectors
**Maintained By:** AEON FORGE ULTRATHINK Team

---

**END OF SOP**
