# NER v7 Training Data Validation Report
**Validation Date**: 2025-11-08
**Overall Status**: FAIL

## Executive Summary
❌ Quality issues detected requiring attention.

### Critical Warnings
- train: Format validation failed
- Doc 0, Entity 0: Unexpected label 'TACTIC'
- Doc 0, Entity 1: Unexpected label 'TACTIC'
- Doc 0, Entity 2: Unexpected label 'SECURITY'
- Doc 0, Entity 3: Unexpected label 'SECURITY'
- Doc 0, Entity 4: Unexpected label 'SECURITY'
- train: CAPEC diversity 0.000 below target 0.900
- train: CWE diversity 0.000 below target 0.250
- train: ATTACK diversity 0.000 below target 0.900
- train: CVE diversity 0.000 below target 0.250
- train: HARDWARE_COMPONENT severely underrepresented (0.7%)
- train: COGNITIVE_BIAS severely underrepresented (0.5%)
- train: INSIDER_INDICATOR severely underrepresented (1.8%)
- train: THREAT_MODEL severely underrepresented (0.9%)
- train: ARCHITECTURE severely underrepresented (2.2%)
- train: MITIGATION severely underrepresented (2.8%)
- train: OPERATION severely underrepresented (2.4%)
- train: ATTACK_PATTERN severely underrepresented (0.7%)
- train: WEAKNESS severely underrepresented (1.0%)
- train: ATTACK_VECTOR severely underrepresented (0.3%)
- train: SUPPLIER severely underrepresented (0.6%)
- train: SOFTWARE_COMPONENT severely underrepresented (0.5%)
- train: SOCIAL_ENGINEERING severely underrepresented (0.8%)
- train: VULNERABILITY severely underrepresented (0.6%)
- train: INDICATOR severely underrepresented (2.6%)
- train: THREAT_ACTOR severely underrepresented (2.7%)
- train: PERSONALITY_TRAIT severely underrepresented (2.9%)
- dev: Format validation failed
- Doc 0, Entity 0: Unexpected label 'PROTOCOL'
- Doc 0, Entity 1: Unexpected label 'PROTOCOL'
- Doc 0, Entity 2: Unexpected label 'CAMPAIGN'
- Doc 1, Entity 0: Unexpected label 'THREAT_ACTOR'
- Doc 1, Entity 1: Unexpected label 'SUPPLIER'
- dev: CAPEC diversity 0.000 below target 0.900
- dev: CWE diversity 0.000 below target 0.250
- dev: ATTACK diversity 0.000 below target 0.900
- dev: CVE diversity 0.000 below target 0.250
- dev: THREAT_ACTOR severely underrepresented (2.0%)
- dev: SUPPLIER severely underrepresented (0.8%)
- dev: SOCIAL_ENGINEERING severely underrepresented (0.8%)
- dev: INSIDER_INDICATOR severely underrepresented (1.8%)
- dev: ARCHITECTURE severely underrepresented (2.4%)
- dev: WEAKNESS severely underrepresented (0.2%)
- dev: OPERATION severely underrepresented (1.8%)
- dev: MITIGATION severely underrepresented (1.5%)
- dev: HARDWARE_COMPONENT severely underrepresented (0.2%)
- dev: VULNERABILITY severely underrepresented (1.3%)
- dev: PERSONALITY_TRAIT severely underrepresented (0.1%)
- dev: ATTACK_VECTOR severely underrepresented (0.1%)
- dev: THREAT_MODEL severely underrepresented (0.3%)
- dev: COGNITIVE_BIAS severely underrepresented (0.1%)
- dev: ATTACK_PATTERN severely underrepresented (0.2%)
- dev: SOFTWARE_COMPONENT severely underrepresented (2.4%)
- test: Format validation failed
- Doc 0, Entity 0: Unexpected label 'SECURITY'
- Doc 0, Entity 1: Unexpected label 'TACTIC'
- Doc 0, Entity 2: Unexpected label 'TACTIC'
- Doc 0, Entity 3: Unexpected label 'SECURITY'
- Doc 0, Entity 4: Unexpected label 'TACTIC'
- test: CAPEC diversity 0.000 below target 0.900
- test: CWE diversity 0.000 below target 0.250
- test: ATTACK diversity 0.000 below target 0.900
- test: CVE diversity 0.000 below target 0.250
- test: SOCIAL_ENGINEERING severely underrepresented (1.0%)
- test: INSIDER_INDICATOR severely underrepresented (2.5%)
- test: ARCHITECTURE severely underrepresented (1.2%)
- test: TECHNIQUE severely underrepresented (3.2%)
- test: VULNERABILITY severely underrepresented (0.9%)
- test: COGNITIVE_BIAS severely underrepresented (0.7%)
- test: MITIGATION severely underrepresented (3.3%)
- test: HARDWARE_COMPONENT severely underrepresented (0.7%)
- test: THREAT_MODEL severely underrepresented (2.6%)
- test: OPERATION severely underrepresented (3.8%)
- test: PERSONALITY_TRAIT severely underrepresented (2.1%)
- test: THREAT_ACTOR severely underrepresented (1.2%)
- test: WEAKNESS severely underrepresented (0.9%)
- test: ATTACK_PATTERN severely underrepresented (0.4%)
- test: ATTACK_VECTOR severely underrepresented (0.3%)
- test: SOFTWARE_COMPONENT severely underrepresented (0.1%)
- test: SUPPLIER severely underrepresented (0.8%)

## Dataset Metrics

### TRAIN
**File**: `train.spacy`
**Format Valid**: ❌ No
**Quality Status**: ⚠️ NEEDS REVIEW

| Metric | Value |
|--------|-------|
| Total Examples | 296 |
| Total Entities | 21033 |
| Avg Entities/Doc | 71.06 |
| Avg Text Length | 17776 chars |

**Entity Distribution**:
- **ARCHITECTURE**: 457 total, 164 unique (diversity: 0.000, 2.2% of dataset)
- **ATTACK_PATTERN**: 149 total, 28 unique (diversity: 0.000, 0.7% of dataset)
- **ATTACK_VECTOR**: 55 total, 14 unique (diversity: 0.000, 0.3% of dataset)
- **CAMPAIGN**: 1215 total, 643 unique (diversity: 0.000, 5.8% of dataset)
- **COGNITIVE_BIAS**: 111 total, 26 unique (diversity: 0.000, 0.5% of dataset)
- **EQUIPMENT**: 3304 total, 2374 unique (diversity: 0.000, 15.7% of dataset)
- **HARDWARE_COMPONENT**: 144 total, 26 unique (diversity: 0.000, 0.7% of dataset)
- **INDICATOR**: 555 total, 463 unique (diversity: 0.000, 2.6% of dataset)
- **INSIDER_INDICATOR**: 381 total, 24 unique (diversity: 0.000, 1.8% of dataset)
- **MITIGATION**: 588 total, 48 unique (diversity: 0.000, 2.8% of dataset)
- **OPERATION**: 502 total, 224 unique (diversity: 0.000, 2.4% of dataset)
- **PERSONALITY_TRAIT**: 600 total, 19 unique (diversity: 0.000, 2.9% of dataset)
- **PROTOCOL**: 2489 total, 147 unique (diversity: 0.000, 11.8% of dataset)
- **SECURITY**: 3030 total, 328 unique (diversity: 0.000, 14.4% of dataset)
- **SOCIAL_ENGINEERING**: 165 total, 27 unique (diversity: 0.000, 0.8% of dataset)
- **SOFTWARE_COMPONENT**: 102 total, 68 unique (diversity: 0.000, 0.5% of dataset)
- **SUPPLIER**: 132 total, 58 unique (diversity: 0.000, 0.6% of dataset)
- **TACTIC**: 1857 total, 47 unique (diversity: 0.000, 8.8% of dataset)
- **TECHNIQUE**: 1157 total, 323 unique (diversity: 0.000, 5.5% of dataset)
- **THREAT_ACTOR**: 565 total, 66 unique (diversity: 0.000, 2.7% of dataset)
- **THREAT_MODEL**: 199 total, 12 unique (diversity: 0.000, 0.9% of dataset)
- **VENDOR**: 2944 total, 51 unique (diversity: 0.000, 14.0% of dataset)
- **VULNERABILITY**: 128 total, 73 unique (diversity: 0.000, 0.6% of dataset)
- **WEAKNESS**: 204 total, 39 unique (diversity: 0.000, 1.0% of dataset)

**Format Issues** (21033 total):
- Doc 0, Entity 0: Unexpected label 'TACTIC'
- Doc 0, Entity 1: Unexpected label 'TACTIC'
- Doc 0, Entity 2: Unexpected label 'SECURITY'
- Doc 0, Entity 3: Unexpected label 'SECURITY'
- Doc 0, Entity 4: Unexpected label 'SECURITY'
- Doc 0, Entity 5: Unexpected label 'HARDWARE_COMPONENT'
- Doc 1, Entity 0: Unexpected label 'COGNITIVE_BIAS'
- Doc 1, Entity 1: Unexpected label 'COGNITIVE_BIAS'
- Doc 1, Entity 2: Unexpected label 'COGNITIVE_BIAS'
- Doc 1, Entity 3: Unexpected label 'COGNITIVE_BIAS'
- ... and 21023 more

### DEV
**File**: `dev.spacy`
**Format Valid**: ❌ No
**Quality Status**: ⚠️ NEEDS REVIEW

| Metric | Value |
|--------|-------|
| Total Examples | 63 |
| Total Entities | 3980 |
| Avg Entities/Doc | 63.17 |
| Avg Text Length | 16266 chars |

**Entity Distribution**:
- **ARCHITECTURE**: 94 total, 59 unique (diversity: 0.000, 2.4% of dataset)
- **ATTACK_PATTERN**: 6 total, 4 unique (diversity: 0.000, 0.2% of dataset)
- **ATTACK_VECTOR**: 5 total, 1 unique (diversity: 0.000, 0.1% of dataset)
- **CAMPAIGN**: 324 total, 202 unique (diversity: 0.000, 8.1% of dataset)
- **COGNITIVE_BIAS**: 2 total, 2 unique (diversity: 0.000, 0.1% of dataset)
- **EQUIPMENT**: 511 total, 423 unique (diversity: 0.000, 12.8% of dataset)
- **HARDWARE_COMPONENT**: 7 total, 1 unique (diversity: 0.000, 0.2% of dataset)
- **INDICATOR**: 271 total, 260 unique (diversity: 0.000, 6.8% of dataset)
- **INSIDER_INDICATOR**: 73 total, 11 unique (diversity: 0.000, 1.8% of dataset)
- **MITIGATION**: 60 total, 23 unique (diversity: 0.000, 1.5% of dataset)
- **OPERATION**: 70 total, 49 unique (diversity: 0.000, 1.8% of dataset)
- **PERSONALITY_TRAIT**: 3 total, 3 unique (diversity: 0.000, 0.1% of dataset)
- **PROTOCOL**: 686 total, 95 unique (diversity: 0.000, 17.2% of dataset)
- **SECURITY**: 604 total, 104 unique (diversity: 0.000, 15.2% of dataset)
- **SOCIAL_ENGINEERING**: 32 total, 10 unique (diversity: 0.000, 0.8% of dataset)
- **SOFTWARE_COMPONENT**: 95 total, 80 unique (diversity: 0.000, 2.4% of dataset)
- **SUPPLIER**: 30 total, 16 unique (diversity: 0.000, 0.8% of dataset)
- **TACTIC**: 349 total, 25 unique (diversity: 0.000, 8.8% of dataset)
- **TECHNIQUE**: 227 total, 20 unique (diversity: 0.000, 5.7% of dataset)
- **THREAT_ACTOR**: 80 total, 31 unique (diversity: 0.000, 2.0% of dataset)
- **THREAT_MODEL**: 11 total, 7 unique (diversity: 0.000, 0.3% of dataset)
- **VENDOR**: 379 total, 22 unique (diversity: 0.000, 9.5% of dataset)
- **VULNERABILITY**: 52 total, 33 unique (diversity: 0.000, 1.3% of dataset)
- **WEAKNESS**: 9 total, 4 unique (diversity: 0.000, 0.2% of dataset)

**Format Issues** (3980 total):
- Doc 0, Entity 0: Unexpected label 'PROTOCOL'
- Doc 0, Entity 1: Unexpected label 'PROTOCOL'
- Doc 0, Entity 2: Unexpected label 'CAMPAIGN'
- Doc 1, Entity 0: Unexpected label 'THREAT_ACTOR'
- Doc 1, Entity 1: Unexpected label 'SUPPLIER'
- Doc 1, Entity 2: Unexpected label 'CAMPAIGN'
- Doc 1, Entity 3: Unexpected label 'TECHNIQUE'
- Doc 1, Entity 4: Unexpected label 'TACTIC'
- Doc 1, Entity 5: Unexpected label 'THREAT_ACTOR'
- Doc 1, Entity 6: Unexpected label 'TECHNIQUE'
- ... and 3970 more

### TEST
**File**: `test.spacy`
**Format Valid**: ❌ No
**Quality Status**: ⚠️ NEEDS REVIEW

| Metric | Value |
|--------|-------|
| Total Examples | 64 |
| Total Entities | 4563 |
| Avg Entities/Doc | 71.30 |
| Avg Text Length | 16898 chars |

**Entity Distribution**:
- **ARCHITECTURE**: 57 total, 33 unique (diversity: 0.000, 1.2% of dataset)
- **ATTACK_PATTERN**: 20 total, 10 unique (diversity: 0.000, 0.4% of dataset)
- **ATTACK_VECTOR**: 14 total, 7 unique (diversity: 0.000, 0.3% of dataset)
- **CAMPAIGN**: 253 total, 179 unique (diversity: 0.000, 5.5% of dataset)
- **COGNITIVE_BIAS**: 34 total, 16 unique (diversity: 0.000, 0.7% of dataset)
- **EQUIPMENT**: 377 total, 308 unique (diversity: 0.000, 8.3% of dataset)
- **HARDWARE_COMPONENT**: 34 total, 1 unique (diversity: 0.000, 0.7% of dataset)
- **INDICATOR**: 289 total, 270 unique (diversity: 0.000, 6.3% of dataset)
- **INSIDER_INDICATOR**: 114 total, 17 unique (diversity: 0.000, 2.5% of dataset)
- **MITIGATION**: 151 total, 30 unique (diversity: 0.000, 3.3% of dataset)
- **OPERATION**: 175 total, 112 unique (diversity: 0.000, 3.8% of dataset)
- **PERSONALITY_TRAIT**: 98 total, 9 unique (diversity: 0.000, 2.1% of dataset)
- **PROTOCOL**: 445 total, 38 unique (diversity: 0.000, 9.8% of dataset)
- **SECURITY**: 656 total, 130 unique (diversity: 0.000, 14.4% of dataset)
- **SOCIAL_ENGINEERING**: 46 total, 17 unique (diversity: 0.000, 1.0% of dataset)
- **SOFTWARE_COMPONENT**: 3 total, 2 unique (diversity: 0.000, 0.1% of dataset)
- **SUPPLIER**: 35 total, 26 unique (diversity: 0.000, 0.8% of dataset)
- **TACTIC**: 678 total, 30 unique (diversity: 0.000, 14.9% of dataset)
- **TECHNIQUE**: 144 total, 26 unique (diversity: 0.000, 3.2% of dataset)
- **THREAT_ACTOR**: 54 total, 27 unique (diversity: 0.000, 1.2% of dataset)
- **THREAT_MODEL**: 118 total, 14 unique (diversity: 0.000, 2.6% of dataset)
- **VENDOR**: 687 total, 33 unique (diversity: 0.000, 15.1% of dataset)
- **VULNERABILITY**: 39 total, 26 unique (diversity: 0.000, 0.9% of dataset)
- **WEAKNESS**: 42 total, 17 unique (diversity: 0.000, 0.9% of dataset)

**Format Issues** (4563 total):
- Doc 0, Entity 0: Unexpected label 'SECURITY'
- Doc 0, Entity 1: Unexpected label 'TACTIC'
- Doc 0, Entity 2: Unexpected label 'TACTIC'
- Doc 0, Entity 3: Unexpected label 'SECURITY'
- Doc 0, Entity 4: Unexpected label 'TACTIC'
- Doc 0, Entity 5: Unexpected label 'SECURITY'
- Doc 0, Entity 6: Unexpected label 'SOCIAL_ENGINEERING'
- Doc 0, Entity 7: Unexpected label 'SECURITY'
- Doc 0, Entity 8: Unexpected label 'SECURITY'
- Doc 0, Entity 9: Unexpected label 'SECURITY'
- ... and 4553 more

## Recommendations

- Review format validation errors and fix entity spans
- Increase diversity by adding more unique examples
- Balance label distribution across entity types
- Ensure minimum thresholds met for production readiness

## Conclusion

Training data validation **FAILED**. Address warnings and recommendations before proceeding with model training.
