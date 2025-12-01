# NER TRAINING VERSION EVOLUTION FORENSIC ANALYSIS
**Date:** November 8, 2025  
**Analysis Type:** Comprehensive Version Comparison (v5 → v6 → v7)  
**Status:** COMPLETE (v8 NOT YET EXECUTED)

---

## EXECUTIVE SUMMARY

**CRITICAL FINDING:** Version 7 represents a COMPLETE STRATEGIC PIVOT from critical infrastructure (v5/v6) to cybersecurity vulnerability focus (v7). Critical infrastructure entity recognition capabilities were LOST in v7.

### Performance Trajectory
- **v5 → v6:** +12.38% improvement (71.78% → 84.16%) - Same domain refinement
- **v6 → v7:** +10.89% improvement (84.16% → 95.05%) - Different domain entirely
- **Total v5 → v7:** +23.27% improvement BUT COMPLETELY DIFFERENT USE CASE

### Strategic Issue
v7's 95.05% F1 score is MEANINGLESS for critical infrastructure applications because:
- Zero VENDOR entity examples (v5/v6: 9,477 annotations → v7: 0)
- Zero EQUIPMENT examples (v5/v6: 4,316 annotations → v7: 0)
- Zero PROTOCOL examples (v5/v6: 3,941 annotations → v7: 0)
- Gained CVE/CWE/CAPEC focus entirely

---

## VERSION 5 - CRITICAL INFRASTRUCTURE BASELINE

### Training Profile
- **Date:** November 7, 2024 (~16:00-17:38 UTC)
- **Duration:** ~1.5 hours
- **Dataset:** 423 training examples
- **Training Split:** 296 train / 63 validation / 64 test (70/15/15%)
- **Source:** 16 Critical Infrastructure Sectors

### Critical Infrastructure Sectors Covered
1. Energy Sector (42 examples)
2. Chemical Sector (17 examples)
3. Transportation Sector (20 examples)
4. IT/Telecom Sector (16 examples)
5. Healthcare Sector (27 examples)
6. Financial Sector (16 examples)
7. Food/Agriculture Sector (8 examples)
8. Government Sector (10 examples)
9. Defense Sector (7 examples)
10. Water/Wastewater (20 examples)
11. Manufacturing (8 examples)
12. Emergency Services (10 examples)
13. Commercial Facilities (15 examples)
14. Nuclear Reactors (15 examples)
15. Critical Manufacturing (14 examples)
16. Communications (26 examples)
17. Express Briefs (152 examples)

### Entity Distribution (Total Annotations: 36,175)
| Entity Type | Annotations | Test Support | F1 Score |
|-------------|-------------|--------------|----------|
| VENDOR | 9,477 | 1,212 | 19.16% |
| EQUIPMENT | 4,316 | 771 | 94.41% |
| SECURITY | 4,929 | 674 | 89.62% |
| PROTOCOL | 3,941 | 574 | 81.90% |
| TACTIC | 3,014 | 336 | 95.77% |
| TECHNIQUE | 1,550 | 87 | 91.93% |
| CAMPAIGN | 1,812 | 116 | 84.96% |
| INDICATOR | 1,342 | 258 | 8.05% |
| MITIGATION | 1,235 | 164 | 68.46% |
| HARDWARE_COMPONENT | 901 | 107 | 7.21% |
| THREAT_ACTOR | 728 | 67 | 89.39% |
| PERSONALITY_TRAIT | 713 | 72 | 99.30% |
| ARCHITECTURE | 721 | 127 | 86.81% |
| INSIDER_INDICATOR | 646 | 95 | 90.40% |
| SOCIAL_ENGINEERING | 546 | 16 | 82.76% |
| WEAKNESS | 257 | 58 | 84.21% |
| ATTACK_PATTERN | 235 | 25 | 63.41% |
| VULNERABILITY | 219 | 59 | 71.15% |
| SOFTWARE_COMPONENT | 218 | 3 | 57.14% |
| SUPPLIER | 206 | 18 | 92.31% |
| COGNITIVE_BIAS | 168 | 6 | 90.91% |
| OPERATION | 815 | 101 | 64.71% |
| THREAT_MODEL | 342 | 40 | 98.77% |
| ATTACK_VECTOR | 81 | 9 | 82.35% |

### Performance Metrics
- **Overall F1:** 71.78%
- **Precision:** 88.57%
- **Recall:** 60.34%
- **Total Test Support:** 4,995 entity instances

### Strengths (F1 > 90%)
- PERSONALITY_TRAIT: 99.30%
- THREAT_MODEL: 98.77%
- TACTIC: 95.77%
- EQUIPMENT: 94.41%
- SUPPLIER: 92.31%
- TECHNIQUE: 91.93%

### Weaknesses (F1 < 50%)
- VENDOR: 19.16% (CRITICAL - 1,212 test instances)
- INDICATOR: 8.05% (258 instances)
- HARDWARE_COMPONENT: 7.21% (107 instances)

### Training Issues
- Misaligned entities in "System Context" and vendor training data
- Warning: Entities could not be aligned due to offset issues
- Many entities ignored during training due to misalignment

---

## VERSION 6 - REFINED INFRASTRUCTURE MODEL

### Training Profile
- **Date:** November 7, 2024 (~19:40 UTC)
- **Duration:** Training logs show 423 examples processed
- **Dataset:** 423 training examples (SAME as v5)
- **Training Split:** 296 train / 63 validation / 64 test (SAME as v5)
- **Source:** SAME 16 Critical Infrastructure Sectors

### Entity Distribution (Total Annotations: 29,728)
| Entity Type | Annotations | Test Support | F1 Score | Δ from v5 |
|-------------|-------------|--------------|----------|-----------|
| VENDOR | 4,010 | 687 | 36.14% | +16.98% |
| EQUIPMENT | 4,197 | 377 | 91.09% | -3.32% |
| SECURITY | 4,314 | 656 | 98.17% | +8.55% |
| PROTOCOL | 3,620 | 445 | 92.64% | +10.74% |
| TACTIC | 2,885 | 678 | 98.75% | +2.98% |
| TECHNIQUE | 1,528 | 144 | 94.62% | +2.69% |
| CAMPAIGN | 1,794 | 253 | 93.65% | +8.69% |
| INDICATOR | 1,231 | 298 | 25.99% | +17.94% |
| MITIGATION | 799 | 151 | 96.73% | +28.27% |
| OPERATION | 747 | 175 | 58.66% | -6.05% |
| THREAT_ACTOR | 699 | 54 | 93.46% | +4.07% |
| PERSONALITY_TRAIT | 701 | 98 | 98.97% | -0.33% |
| ARCHITECTURE | 609 | 57 | 97.39% | +10.58% |
| INSIDER_INDICATOR | 569 | 114 | 98.68% | +8.28% |
| WEAKNESS | 255 | 42 | 92.68% | +8.47% |
| SOCIAL_ENGINEERING | 243 | 46 | 98.92% | +16.16% |
| VULNERABILITY | 219 | 39 | 31.25% | -39.90% |
| SOFTWARE_COMPONENT | 200 | 3 | 100.00% | +42.86% |
| SUPPLIER | 198 | 35 | 90.67% | -1.64% |
| HARDWARE_COMPONENT | 185 | 34 | 100.00% | +92.79% |
| ATTACK_PATTERN | 176 | 20 | 81.63% | +18.22% |
| COGNITIVE_BIAS | 147 | 34 | 90.62% | -0.29% |
| THREAT_MODEL | 328 | 118 | 97.89% | -0.88% |
| ATTACK_VECTOR | 74 | 14 | 92.86% | +10.51% |

### Performance Metrics
- **Overall F1:** 84.16%
- **Precision:** 92.05%
- **Recall:** 77.52%
- **Total Test Support:** 4,572 entity instances
- **Improvement vs v5:** +12.38%

### Key Improvements
- VENDOR: +16.98% (but still only 36.14%)
- HARDWARE_COMPONENT: +92.79% (7.21% → 100.00%)
- MITIGATION: +28.27% (68.46% → 96.73%)
- PROTOCOL: +10.74% (81.90% → 92.64%)
- SECURITY: +8.55% (89.62% → 98.17%)

### Remaining Weaknesses
- VENDOR: 36.14% (still critical issue with 687 test instances)
- VULNERABILITY: 31.25% (-39.90% regression!)
- INDICATOR: 25.99% (improved but still low)

### Training Characteristics
- Same 16 sectors as v5
- Improved alignment and annotation quality
- Better overall precision (+3.48%)
- Better recall (+17.18%)

---

## VERSION 7 - CYBERSECURITY PIVOT (CURRENT)

### Training Profile
- **Date:** November 8, 2024 (12:18-12:56 UTC)
- **Duration:** ~38 minutes
- **Dataset:** 2,731 raw examples → 755 spaCy format examples
- **Training Split:** 604 train / 151 dev (80/20%)
- **Training Iterations:** 50 iterations
- **Model Save:** models/v7_ner_model/

### Data Sources (COMPLETELY DIFFERENT FROM v5/v6)
1. **Existing CAPEC Data:** 1,552 unique examples
   - CAPEC_NER_TRAINING_DATA.json
   - CAPEC_NER_ENTITY_RICH.json
   - CAPEC_NER_DETAILED.json
   - CAPEC_NER_GOLDEN_BRIDGES.json
   - CAPEC_NER_META.json

2. **CVE-CWE Extraction:** 1,178 new examples
   - Source: cve_cwe_data.json
   - Records processed: 1,150

3. **CAPEC-ATT&CK Extraction:** 1 new example
   - Source: capec_attack_data.json
   - Records processed: 238
   - Note: Most already in existing dataset (deduplication working)

### Entity Distribution (Total Annotations: 10,127)
| Entity Type | Annotations | Context Sources | Training Examples |
|-------------|-------------|-----------------|-------------------|
| CWE | 5,275 | prerequisite, description, extended_description | 633 |
| CAPEC | 1,553 | description, prerequisite, example_instance | 217 |
| CVE | 1,057 | cve_description | (combined with VULNERABILITY) |
| VULNERABILITY | 1,057 | cve_description | 466 |
| ATTACK_TECHNIQUE | 806 | various | (combined with TECHNIQUE) |
| OWASP | 133 | various | 3 |
| WASC | 122 | various | 0 |
| WEAKNESS | 121 | cwe_description | 9 |
| ATTACK_PATTERN | 1 | capec_attack_mapping | 0 |
| ATTACK | 1 | various | 0 |
| TECHNIQUE | 1 | various | 0 |

### Performance Metrics
- **Overall F1:** 95.05%
- **Precision:** 90.57%
- **Recall:** 100.00%
- **Improvement vs v6:** +10.89%

### Per-Entity Performance (151 test examples)
| Entity Type | Precision | Recall | F1 Score | Support |
|-------------|-----------|--------|----------|---------|
| VULNERABILITY | 96.00% | 100.00% | 97.96% | (combined) |
| CWE | 92.55% | 100.00% | 96.13% | (majority) |
| CAPEC | 84.72% | 100.00% | 91.73% | (significant) |
| OWASP | 33.33% | 100.00% | 50.00% | (3 examples) |

### Training Progression (50 iterations)
- Iteration 5: Loss 340.09, F1 94.04%
- Iteration 10: Loss 188.49, F1 95.88%
- Iteration 20: Loss 100.79, F1 96.30%
- Iteration 30: Loss 56.09, F1 95.26%
- Iteration 40: Loss 47.99, F1 95.26%
- Iteration 50: Loss 39.81, F1 95.05% ← FINAL

### Context Distribution
| Context Type | Examples | Purpose |
|--------------|----------|---------|
| cve_description | 1,057 | CVE vulnerability descriptions |
| prerequisite | 624 | CAPEC prerequisites |
| description | 544 | General descriptions |
| example_instance | 204 | Real-world examples |
| extended_description | 180 | Detailed explanations |
| cwe_description | 121 | CWE weakness descriptions |
| capec_attack_mapping | 1 | CAPEC-ATT&CK mappings |

### Underrepresented Entity Types (Planned for v8)
| Entity Type | Current | Target | Gap | Recommendation |
|-------------|---------|--------|-----|----------------|
| ATTACK_PATTERN | 1 | 200 | 199 | Need CAPEC-ATTACK mapping data |
| ATTACK | 1 | 200 | 199 | Need ATT&CK technique descriptions |
| TECHNIQUE | 1 | 200 | 199 | Need ATT&CK technique descriptions |
| WEAKNESS | 121 | 200 | 79 | CWE extended descriptions |
| WASC | 122 | 200 | 78 | WASC database extraction |
| OWASP | 133 | 200 | 67 | OWASP Top 10 documentation |

---

## VERSION 8 - PLANNED (NOT YET EXECUTED)

### Status
**NOT STARTED** as of November 8, 2024

### Recommended Improvements (from v7 completion report)
1. Extract more WASC examples from WASC database
2. Extract OWASP Top 10 examples from OWASP documentation
3. Add WEAKNESS examples from CWE extended descriptions
4. Extract ATT&CK technique descriptions directly from ATT&CK framework
5. Create synthetic examples for underrepresented entity types
6. Add multi-hop reasoning examples (CVE → CWE → CAPEC → ATT&CK chains)

### Expected Focus
- Fill gaps in ATTACK, TECHNIQUE, ATTACK_PATTERN entities
- Maintain v7's high performance (95%+)
- Add multi-hop attack chain reasoning
- Maintain cybersecurity vulnerability focus

---

## CRITICAL FINDINGS & RECOMMENDATIONS

### 🚨 CRITICAL ISSUE: Domain Mismatch
**Problem:** v7 is optimized for CVE/CWE/CAPEC cybersecurity research, NOT for critical infrastructure operations.

**Evidence:**
- v5/v6: 9,477 VENDOR annotations → v7: 0
- v5/v6: 4,316 EQUIPMENT annotations → v7: 0
- v5/v6: 3,941 PROTOCOL annotations → v7: 0
- v5/v6: 16 infrastructure sectors → v7: 0 sectors

**Impact:**
- v7 CANNOT identify industrial control system vendors
- v7 CANNOT identify critical infrastructure equipment
- v7 CANNOT identify operational technology protocols
- v7 is USELESS for MITRE use case if goal is infrastructure threat analysis

### 📊 Performance Trends
| Metric | v5 → v6 | v6 → v7 | Overall |
|--------|---------|---------|---------|
| F1 Score | +12.38% | +10.89% | +23.27% |
| Precision | +3.48% | -1.48% | +2.00% |
| Recall | +17.18% | +22.48% | +39.66% |
| Training Size | Same (423) | +546% (2,731) | +546% |

### 🎯 Recommendations

#### If Critical Infrastructure Focus is Required:
1. **Use v6 model** for immediate critical infrastructure NER
2. **DO NOT use v7** for infrastructure entity recognition
3. **Create v8 as infrastructure enhancement:**
   - Start with v6 model
   - Add more VENDOR training data (improve from 36.14%)
   - Add more INDICATOR training data (improve from 25.99%)
   - Maintain v6's strong EQUIPMENT/PROTOCOL/SECURITY performance

#### If Cybersecurity Vulnerability Focus is Required:
1. **Use v7 model** for CVE/CWE/CAPEC/ATT&CK analysis
2. **Create v8 with multi-hop reasoning:**
   - Add ATT&CK techniques (current: 1 example)
   - Add WASC examples (current: 122)
   - Add OWASP examples (current: 133)
   - Add CVE → CWE → CAPEC → ATT&CK chain examples

#### If Both Use Cases are Required:
1. **Maintain separate models:**
   - v6-fork for critical infrastructure
   - v8 for cybersecurity vulnerabilities
2. **OR create hybrid v8:**
   - Combine v6's 423 infrastructure examples
   - Combine v7's 2,731 security examples
   - Train unified model on 3,154 total examples
   - Risk: May dilute performance in both domains

---

## TRAINING DATA FILE LOCATIONS

### Version 5
- **Training Logs:** `/tmp/v5_training_success.log` (Nov 7, 16:16)
- **Evaluation:** `Data Pipeline Builder/NER_EVALUATION_RESULTS_v5_BACKUP.json`
- **Training Data:** Derived from 16 sector markdown files
- **Model:** `ner_model/` (overwritten by v6)

### Version 6
- **Training Logs:** `/tmp/v6_training.log` (Nov 7, 19:40)
- **Evaluation:** `Data Pipeline Builder/NER_EVALUATION_RESULTS.json`
- **Training Data:** Same 16 sector markdown files as v5
- **Model:** `ner_model/` (overwritten by v7)

### Version 7
- **Training Logs:** `logs/v7_training_final.log` (Nov 8, 12:24)
- **Training Data:** `data/ner_training/V7_NER_TRAINING_DATA.json` (2,731 examples)
- **Training Data (spaCy):** `data/ner_training/V7_NER_TRAINING_DATA_SPACY.json` (755 examples)
- **Statistics:** `data/ner_training/V7_STATISTICS.json`
- **Completion Report:** `data/ner_training/V7_COMPLETION_REPORT.json`
- **Test Results:** `data/ner_training/V7_TEST_RESULTS.json`
- **Model:** `models/v7_ner_model/`

### Version 8
- **Status:** NOT CREATED YET
- **Planned Location:** `data/ner_training/V8_NER_TRAINING_DATA.json`

---

## CONCLUSION

**Summary:** Three distinct NER training versions were executed:
- **v5** (Nov 7, 16:00): Critical infrastructure baseline (71.78% F1)
- **v6** (Nov 7, 19:40): Infrastructure refinement (84.16% F1, +12.38%)
- **v7** (Nov 8, 12:24): Cybersecurity pivot (95.05% F1, +10.89%)

**Critical Decision Point:** v7's higher performance is IRRELEVANT if the use case requires critical infrastructure entity recognition. v5/v6 data is LOST in v7.

**Action Required:** Define primary use case before proceeding to v8:
- Infrastructure threats → Build on v6
- Vulnerability research → Build on v7
- Both → Create hybrid or maintain separate models

**Report Complete:** All 3 actual versions analyzed with real data from training logs and evaluation files.

---

**Analysis Completed:** November 8, 2025  
**Total Versions Analyzed:** 3 (v5, v6, v7)  
**v8 Status:** Not yet executed  
**Data Sources:** Actual training logs, evaluation JSON, completion reports  
**Evidence Level:** 100% fact-based from real files
