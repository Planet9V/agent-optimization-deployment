# v6 Performance Targets
**Version:** 6.0.0
**Created:** 2025-11-06
**Purpose:** Baseline, projected, and target metrics for v6 NER model
**Status:** Active Development

## Executive Summary

v6 aims to achieve a **207% relative improvement** in VENDOR F1 score while maintaining or improving overall model quality. This document establishes baseline performance, projected improvements, and success criteria for v6 validation.

---

## Table of Contents

1. [Baseline Performance (v4)](#baseline-performance-v4)
2. [Projected Performance (v5)](#projected-performance-v5)
3. [Target Performance (v6)](#target-performance-v6)
4. [Success Metrics](#success-metrics)
5. [Quality Gates](#quality-gates)
6. [Comparison Summary](#comparison-summary)

---

## Baseline Performance (v4)

**Model:** v4 (current production model)
**Date:** 2025-11-05
**Test Set:** 39 ICS/OT security documents
**Training Data:** Label Studio annotations (pre-v5 improvements)

### Overall Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Precision** | 89.57% | High precision, good quality predictions |
| **Recall** | 68.57% | Moderate recall, missing entities |
| **F1 Score** | **77.67%** | Baseline for improvement |

**Key Observations:**
- Strong precision indicates model makes accurate predictions when it does predict
- Lower recall suggests model is conservative, missing valid entities
- Overall F1 acceptable but below target for production deployment

### Per-Entity Performance

| Entity | Precision | Recall | F1 Score | Support | Status |
|--------|-----------|--------|----------|---------|--------|
| **VENDOR** | 53.11% | 15.87% | **24.44%** | 189 | 🔴 Critical |
| **EQUIPMENT** | 94.14% | 91.57% | **92.83%** | 261 | ✅ Good |
| **PROTOCOL** | 86.70% | 74.24% | **80.02%** | 132 | 🟡 Acceptable |
| **SECURITY** | - | - | - | - | ⚪ New |
| **MITIGATION** | - | - | - | - | ⚪ New |
| **THREAT** | - | - | - | - | ⚪ New |
| **VULNERABILITY** | - | - | - | - | ⚪ New |

**Critical Issues:**

1. **VENDOR Performance Crisis**
   - F1: 24.44% (far below acceptable)
   - Precision: 53.11% (high false positive rate)
   - Recall: 15.87% (missing 84% of VENDOR mentions)
   - **Root Cause:** Feature competition with EQUIPMENT, annotation deduplication issues

2. **EQUIPMENT Over-Performance**
   - F1: 92.83% (excellent)
   - Likely absorbing VENDOR mentions
   - **Hypothesis:** Model preferring EQUIPMENT label when ambiguous

3. **PROTOCOL Moderate Performance**
   - F1: 80.02% (acceptable but improvable)
   - Confusion with EQUIPMENT likely
   - Boundary errors suspected

### Training Issues (v4)

**Errors Encountered:**
```
[E103] Trying to set conflicting doc.ents
- 361 documents with overlapping entity spans
- Blocked training with clean data

[W030] Some entities could not be aligned
- Entity span misalignment with token boundaries
- Partial word matches causing alignment failures
```

**Impact:**
- Could not train on 85.3% of documents (361/423)
- Significant data loss
- Inconsistent entity boundaries

### Confusion Patterns (v4)

**Estimated Confusion Matrix:**
| Gold ↓ \ Pred → | VENDOR | EQUIPMENT | PROTOCOL | Other |
|-----------------|--------|-----------|----------|-------|
| **VENDOR** | 30 (15.87%) | ~120 (63%) | ~10 (5%) | ~29 (15%) |
| **EQUIPMENT** | ~5 (2%) | 239 (91.57%) | ~10 (4%) | ~7 (3%) |
| **PROTOCOL** | ~2 (1.5%) | ~25 (19%) | 98 (74.24%) | ~7 (5%) |

**Key Findings:**
- **VENDOR → EQUIPMENT:** ~63% misclassification (critical issue)
- **PROTOCOL → EQUIPMENT:** ~19% misclassification (moderate issue)
- EQUIPMENT predictions are dominating the model

---

## Projected Performance (v5)

**Model:** v5 (overlap resolution implemented)
**Status:** Development (Phase 1 complete)
**Expected Improvements:** Entity recovery, reduced data loss

### Phase 1 Impact: Overlap Resolution

**Implemented:**
- Conflict resolution for overlapping spans
- 361 documents recovered for training
- Clean entity annotations (zero overlaps)

**Agent 1 Results:**
- ✅ 5/5 test cases passing
- ✅ Conflict resolver functional
- ✅ Ready for pipeline integration

### Projected Overall Metrics (v5)

| Metric | v4 Baseline | v5 Projection | Improvement |
|--------|-------------|---------------|-------------|
| **Precision** | 89.57% | 90-92% | +0.5 to +2.5% |
| **Recall** | 68.57% | 75-80% | **+6.5 to +11.5%** |
| **F1 Score** | 77.67% | **82-85%** | **+4.5 to +7.5%** |

**Rationale:**
- Overlap resolution recovers lost entities → increased recall
- More training data → improved generalization
- Slight precision improvement from cleaner data

### Projected Per-Entity Metrics (v5)

| Entity | v4 F1 | v5 Projected F1 | Improvement | Rationale |
|--------|-------|-----------------|-------------|-----------|
| **VENDOR** | 24.44% | **55-65%** | **+125-166%** | Entity recovery, deduplication fix |
| **EQUIPMENT** | 92.83% | **93-94%** | +0.2-1.2% | Maintain performance, slight improvement |
| **PROTOCOL** | 80.02% | **82-84%** | +2-4% | Better boundaries, more training data |

**VENDOR Improvement Breakdown:**
- **Deduplication Fix:** Recovered 9,788 VENDOR entities (114% of target)
- **Overlap Resolution:** Clean training data, no conflicting spans
- **Expected Impact:**
  - Recall improvement: 15.87% → 45-55% (+30-40%)
  - Precision improvement: 53.11% → 60-70% (+7-17%)
  - F1 improvement: 24.44% → 55-65% (+126-166%)

**Remaining Challenges (v5):**
- Feature competition (VENDOR vs EQUIPMENT) not yet addressed
- Boundary standardization not yet implemented
- No class weighting or training optimization
- **Limitation:** v5 alone will NOT achieve 75% VENDOR F1 target

---

## Target Performance (v6)

**Model:** v6 (comprehensive quality framework)
**Status:** Design phase (Phases 2-6 planned)
**Goal:** Production-ready NER model for ICS/OT security domain

### Overall Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Precision** | ≥ 95% | Production-grade accuracy, minimize false positives |
| **Recall** | ≥ 89% | Comprehensive entity detection, minimize false negatives |
| **F1 Score** | **≥ 92%** | Balance precision/recall, industry-leading performance |

**Comparison to Baseline:**
- Precision: +5.4% (89.57% → 95%)
- Recall: +20.4% (68.57% → 89%)
- F1: +14.3% (77.67% → 92%)

### Per-Entity Performance Targets

| Entity | Precision Target | Recall Target | F1 Target | v4 Baseline | Improvement |
|--------|------------------|---------------|-----------|-------------|-------------|
| **VENDOR** | ≥ 80% | ≥ 70% | **≥ 75%** | 24.44% | **+207%** |
| **EQUIPMENT** | ≥ 95% | ≥ 91% | **≥ 93%** | 92.83% | +0.2% |
| **PROTOCOL** | ≥ 88% | ≥ 82% | **≥ 85%** | 80.02% | +6.2% |
| **SECURITY** | ≥ 90% | ≥ 85% | **≥ 87%** | - | New entity |
| **MITIGATION** | ≥ 85% | ≥ 80% | **≥ 82%** | - | New entity |
| **THREAT** | ≥ 88% | ≥ 83% | **≥ 85%** | - | New entity |
| **VULNERABILITY** | ≥ 87% | ≥ 82% | **≥ 84%** | - | New entity |

### Critical Performance Requirements

#### VENDOR (Primary Goal)

**Target:** F1 ≥ 75%

**Components:**
- **Precision ≥ 80%:** Reduce false positives (EQUIPMENT misclassified as VENDOR)
- **Recall ≥ 70%:** Detect majority of VENDOR mentions

**Required Improvements:**
1. **Entity Disambiguation** (Phase 3)
   - Separate VENDOR from EQUIPMENT using context + syntax
   - Projected impact: +30-40% recall, +15-25% precision

2. **Boundary Standardization** (Phase 4)
   - Fix partial matches and boundary errors
   - Projected impact: +10-15% precision

3. **Training Optimization** (Phase 5)
   - Class weighting to boost VENDOR learning
   - Projected impact: +5-10% F1

**Success Criteria:**
- VENDOR F1 ≥ 75%
- No regression in other entities (EQUIPMENT F1 ≥ 92%)
- VENDOR→EQUIPMENT misclassification < 10%

#### EQUIPMENT (Maintain Excellence)

**Target:** F1 ≥ 93%

**Strategy:**
- Maintain current high performance
- Prevent regression during VENDOR improvements
- Acceptable regression: ≤ 2% F1 drop (to 90.83%)

**Monitoring:**
- Track precision/recall during v6 development
- Alert if EQUIPMENT F1 drops below 92%
- Root cause analysis if regression occurs

#### PROTOCOL (Moderate Improvement)

**Target:** F1 ≥ 85%

**Improvements:**
- Better PROTOCOL vs EQUIPMENT separation
- Boundary standardization for protocol names
- Context-aware classification

**Expected Gains:**
- Precision: +1-2% (86.70% → 88%)
- Recall: +8-10% (74.24% → 82%)
- F1: +5% (80.02% → 85%)

### Training Error Targets

**Zero Tolerance Errors:**
```
[E103] Overlapping spans: MUST be zero
[W030] Alignment failures: MUST be zero
[E999] Any training failures: MUST be zero
```

**Acceptable Warnings:**
```
[W033] Training evaluation warnings: Acceptable (informational)
[W108] Low-confidence predictions: < 5% of predictions
```

### Generalization Targets

**Train/Dev Performance Gap:**
- Target: Dev F1 within 5% of Train F1
- Indicates good generalization, not overfitting

**Example:**
```
Train F1: 93%
Dev F1: 90%
Gap: 3% ✓ (within acceptable range)
```

**Cross-Domain Robustness:**
- Model should generalize across ICS/OT vendors
- No vendor-specific overfitting
- Consistent performance on diverse document types

---

## Success Metrics

### Primary Success Criteria

**Must-Pass Requirements:**

1. **VENDOR F1 ≥ 75%**
   - **Current:** 24.44%
   - **Target:** ≥ 75%
   - **Improvement:** +207% (3.07x better)
   - **Status:** 🔴 Critical Priority

2. **Overall F1 ≥ 92%**
   - **Current:** 77.67%
   - **Target:** ≥ 92%
   - **Improvement:** +14.3%
   - **Status:** 🟡 High Priority

3. **Zero Training Errors**
   - **Current:** E103 (361 docs), W030 (alignment issues)
   - **Target:** Zero errors
   - **Status:** 🟡 High Priority

### Secondary Success Criteria

**Should-Pass Requirements:**

1. **EQUIPMENT F1 ≥ 93%**
   - Maintain or improve current performance
   - Maximum acceptable regression: 2%

2. **PROTOCOL F1 ≥ 85%**
   - Improve from 80.02%
   - +6.2% improvement

3. **Confusion Reduction**
   - VENDOR→EQUIPMENT < 10% (from ~63%)
   - PROTOCOL→EQUIPMENT < 5% (from ~19%)

4. **Boundary Accuracy**
   - False positive rate < 20% (from 47%)
   - Word boundary alignment: 100%

### Quality Indicators

**Desired Characteristics:**

1. **Balanced Performance**
   - No entity type <75% F1
   - Precision/Recall gap <15% for all entities

2. **Consistent Quality**
   - Standard deviation across entities <10% F1

3. **Production Readiness**
   - No critical warnings
   - Stable across diverse inputs
   - Explainable predictions

---

## Quality Gates

### Pre-Training Quality Gates

**Gate 1: Data Quality**
```yaml
Overlap Detection:
  overlapping_spans: 0
  status: PASS/FAIL

Boundary Alignment:
  word_boundary_errors: 0
  punctuation_inconsistencies: 0
  status: PASS/FAIL

Entity Distribution:
  VENDOR_count: ≥ 100
  EQUIPMENT_count: ≥ 50
  all_entities_represented: true
  status: PASS/FAIL
```

**Blocking Conditions:**
- Any overlap detected → BLOCK
- Boundary errors >0 → BLOCK
- VENDOR count <100 → WARNING (continue with caution)

### Training Quality Gates

**Gate 2: Training Convergence**
```yaml
Loss Monitoring:
  final_loss: < 10.0
  loss_explosion: false
  convergence_achieved: true
  status: PASS/FAIL

Early Stopping:
  triggered: false (or due to convergence)
  reason: "Convergence" (acceptable) or "Loss explosion" (failure)
  status: PASS/FAIL
```

**Blocking Conditions:**
- Loss >10.0 → BLOCK
- Loss increasing >3 epochs → BLOCK
- No convergence after max epochs → BLOCK

### Post-Training Quality Gates

**Gate 3: Performance Targets**
```yaml
Overall Performance:
  precision: ≥ 0.95
  recall: ≥ 0.89
  f1: ≥ 0.92
  status: PASS/FAIL

Per-Entity Performance:
  VENDOR:
    precision: ≥ 0.80
    recall: ≥ 0.70
    f1: ≥ 0.75
    status: PASS/FAIL
  EQUIPMENT:
    f1: ≥ 0.93
    status: PASS/FAIL
  PROTOCOL:
    f1: ≥ 0.85
    status: PASS/FAIL
```

**Blocking Conditions:**
- Overall F1 <92% → BLOCK
- VENDOR F1 <75% → BLOCK
- Any entity F1 <70% → WARNING
- EQUIPMENT regression >2% → WARNING

**Gate 4: Confusion Analysis**
```yaml
Confusion Limits:
  VENDOR_to_EQUIPMENT: < 0.10
  PROTOCOL_to_EQUIPMENT: < 0.05
  any_confusion: < 0.15
  status: PASS/FAIL

Boundary Errors:
  false_positive_rate: < 0.20
  partial_match_rate: < 0.10
  status: PASS/FAIL
```

**Blocking Conditions:**
- VENDOR→EQUIPMENT >10% → BLOCK
- FP rate >20% → WARNING
- Any critical confusion pattern → BLOCK

---

## Comparison Summary

### Model Evolution Timeline

```
v4 (Baseline) → v5 (Overlap Fix) → v6 (Comprehensive Framework)
```

### Overall Performance Progression

| Version | Precision | Recall | F1 Score | Status |
|---------|-----------|--------|----------|--------|
| **v4** | 89.57% | 68.57% | **77.67%** | Baseline |
| **v5 (projected)** | 90-92% | 75-80% | **82-85%** | Development |
| **v6 (target)** | ≥95% | ≥89% | **≥92%** | Goal |

**Improvements (v4 → v6):**
- Precision: +5.4%
- Recall: +20.4%
- F1: +14.3%

### VENDOR Performance Progression

| Version | Precision | Recall | F1 Score | Status |
|---------|-----------|--------|----------|--------|
| **v4** | 53.11% | 15.87% | **24.44%** | 🔴 Critical |
| **v5 (projected)** | 60-70% | 45-55% | **55-65%** | 🟡 Improving |
| **v6 (target)** | ≥80% | ≥70% | **≥75%** | ✅ Target |

**Improvements (v4 → v6):**
- Precision: +26.9%
- Recall: +54.1%
- F1: **+207%** (3.07x better)

### Key Milestones

**v4 → v5 (Phase 1: Overlap Resolution)**
- **Achievement:** Data quality improvement
- **Impact:** +31% recall (entity recovery)
- **Projected VENDOR F1:** 55-65% (+126-166%)

**v5 → v6 (Phases 2-6: Quality Framework)**
- **Achievement:** Comprehensive quality + optimization
- **Impact:** +15-20% F1 (disambiguation, boundaries, training)
- **Target VENDOR F1:** 75%+ (+207% vs v4)

### Critical Success Factors

**For v6 to succeed:**

1. ✅ **Phase 1 Complete:** Overlap resolution (DONE)
2. 🔄 **Phase 2:** Quality gates (prevent training issues)
3. 🔄 **Phase 3:** Entity disambiguation (fix VENDOR→EQUIPMENT)
4. 🔄 **Phase 4:** Boundary standardization (reduce FP rate)
5. 🔄 **Phase 5:** Training optimization (boost VENDOR learning)
6. 🔄 **Phase 6:** Comprehensive validation (ensure targets met)

**Risk Mitigation:**
- Each phase independently validated
- Progressive improvement tracking
- Rollback plan if any phase causes regression
- Quality gates at each stage

---

## Validation Requirements

### Pre-Deployment Checklist

Before v6 can be deployed to production:

- [ ] All quality gates passed (pre, during, post-training)
- [ ] Overall F1 ≥ 92%
- [ ] VENDOR F1 ≥ 75%
- [ ] EQUIPMENT F1 ≥ 93% (no regression)
- [ ] PROTOCOL F1 ≥ 85%
- [ ] Zero training errors (E103, W030)
- [ ] Confusion analysis complete (VENDOR→EQUIPMENT <10%)
- [ ] Boundary error rate <20%
- [ ] Manual review of 100 sample predictions
- [ ] Documentation complete
- [ ] Evaluation report generated
- [ ] Lessons learned documented
- [ ] A/B testing vs v4 complete
- [ ] Stakeholder approval obtained

### Success Declaration

**v6 is considered successful when:**
1. All checklist items above are complete
2. VENDOR F1 ≥ 75% (primary goal)
3. Overall F1 ≥ 92% (secondary goal)
4. No critical regressions in other entities
5. Production readiness validated

**Expected Date:** TBD (after Phase 6 completion)

---

## Appendix: Detailed Calculations

### VENDOR Improvement Calculation

**v4 Baseline:**
```
Precision: 53.11%
Recall: 15.87%
F1: 24.44%
```

**v6 Target:**
```
Precision: 80%
Recall: 70%
F1: 75%
```

**Absolute Improvements:**
```
Precision: +26.89%
Recall: +54.13%
F1: +50.56%
```

**Relative Improvements:**
```
Precision: (80 - 53.11) / 53.11 = +50.6%
Recall: (70 - 15.87) / 15.87 = +341%
F1: (75 - 24.44) / 24.44 = +207%
```

### Expected Support Counts

**Gold Standard (39 documents):**
```
VENDOR: 189 mentions
EQUIPMENT: 261 mentions
PROTOCOL: 132 mentions
Total annotated: 582 entities
```

**After v5 Overlap Resolution:**
```
VENDOR: ~500-600 mentions (deduplication fix)
EQUIPMENT: ~260-280 mentions (maintained)
PROTOCOL: ~130-150 mentions (slight increase)
Total annotated: ~900-1000 entities
```

### Confusion Rate Calculation

**v4 VENDOR→EQUIPMENT Confusion:**
```
VENDOR gold standard: 189 mentions
VENDOR recall: 15.87%
Correctly predicted: 189 * 0.1587 = 30

Missing VENDOR: 189 - 30 = 159
Estimated EQUIPMENT misclassification: ~120 (63%)

VENDOR→EQUIPMENT rate: 120 / 189 = 63.5%
```

**v6 Target:**
```
VENDOR→EQUIPMENT rate: <10%
Max misclassifications: 189 * 0.10 = 19
```

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Active - Ready for Validation
