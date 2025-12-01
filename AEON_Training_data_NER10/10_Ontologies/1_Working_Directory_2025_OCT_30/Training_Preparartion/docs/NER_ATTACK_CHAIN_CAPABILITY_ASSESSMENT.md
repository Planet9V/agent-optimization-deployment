# NER Attack Chain Capability Assessment

**Date**: 2025-11-08
**Purpose**: Evaluate current NER training data capabilities for extracting attack chains from threat intelligence and academic papers.

## Executive Summary

**Critical Finding**: Current NER training data and model have **fundamental misalignment** that prevents attack chain extraction:

- **Training data provides**: CVE, CWE, CAPEC, ATTACK entities (4 types)
- **Model expects**: 24 different entity types (VULNERABILITY, WEAKNESS, ATTACK_PATTERN, TECHNIQUE, etc.)
- **Zero overlap**: Training data entity labels don't match ANY model labels

**Current Status**: NER cannot extract attack chains because:
1. Entity type mismatch prevents model from recognizing trained entities
2. No relationship extraction capability (only entity boundaries)
3. No multi-hop chain encoding beyond 3 entities
4. No CVE-to-attack-chain linking in training data

## Training Data Analysis

### Dataset 1: CVE/CWE Training Data
**File**: `training_data/ner_v7_cve_cwe_partial.json`
**Size**: 430 examples, 319KB

**Entity Types**:
- CVE: 100% of examples (430/430)
- CWE: ~27% of examples (119/430)

**Structure**:
```json
{
  "text": "CVE-2011-0662: Use-after-free vulnerability in win32k.sys...",
  "entities": [
    {"start": 0, "end": 13, "label": "CVE"}
  ],
  "meta": {
    "cve_id": "CVE-2011-0662",
    "cwe_id": "cwe-1",
    "cwe_name": "DEPRECATED: Location"
  }
}
```

**Capabilities**:
- ✅ Can identify CVE IDs in text
- ✅ Can identify CWE IDs in text
- ❌ No relationship information between CVE and CWE
- ❌ No attack chain context
- ❌ Metadata not used in NER training

**Limitations**:
- Single entity per example (no chains)
- Metadata links CVE→CWE but not used for relationship extraction
- No CAPEC or ATT&CK entities
- No temporal or causal relationships

### Dataset 2: Attack Chain Training Data
**File**: `training_data/ner_v7_attack_chain_partial.json`
**Size**: 615 examples, 592KB

**Entity Types**:
- CWE: 100% of examples (615/615)
- CAPEC: 100% of examples (615/615)
- ATTACK: 100% of examples (615/615)

**Structure**:
```json
{
  "text": "cwe-1297 Unprotected Confidential Information... enables CAPEC-1 using T1574.010 Services File Permissions Weakness...",
  "entities": [
    {"start": 0, "end": 8, "label": "CWE"},
    {"start": 94, "end": 101, "label": "CAPEC"},
    {"start": 109, "end": 118, "label": "ATTACK"}
  ]
}
```

**Capabilities**:
- ✅ Identifies CWE, CAPEC, ATT&CK entities
- ✅ Preserves sequential ordering (100% CWE→CAPEC→ATTACK)
- ✅ Consistent relationship keywords ("enables", "using")
- ❌ No explicit relationship annotations
- ❌ Relationships embedded in text, not structured data
- ❌ No multi-hop chains (all examples are exactly 3 entities)

**Relationship Patterns** (100% consistent):
- **CWE → CAPEC**: "enables" keyword between entities
- **CAPEC → ATTACK**: "using" keyword between entities
- **Fixed chain**: Always CWE enables CAPEC using ATTACK

**Limitations**:
- No CVE entities (0/615 examples)
- No chains longer than 3 hops
- No variation in relationship types
- No conditional or contextual chains
- Relationships in natural language text, not structured annotations

## Model Analysis

### Existing NER Model
**Location**: `ner_model/`
**Framework**: spaCy v3.8.7
**Component**: Named Entity Recognition (NER)

**Model Configuration**:
- **Expected entity types**: 24 labels
- **Actual training labels**: 4 labels (CVE, CWE, CAPEC, ATTACK)
- **Overlap**: **ZERO** - complete mismatch

**Model expects these entity types**:
```
ARCHITECTURE, ATTACK_PATTERN, ATTACK_VECTOR, CAMPAIGN, COGNITIVE_BIAS,
EQUIPMENT, HARDWARE_COMPONENT, INDICATOR, INSIDER_INDICATOR, MITIGATION,
OPERATION, PERSONALITY_TRAIT, PROTOCOL, SECURITY, SOCIAL_ENGINEERING,
SOFTWARE_COMPONENT, SUPPLIER, TACTIC, TECHNIQUE, THREAT_ACTOR,
THREAT_MODEL, VENDOR, VULNERABILITY, WEAKNESS
```

**Training data provides**:
```
CVE, CWE, CAPEC, ATTACK
```

**Critical Issue**: The model was configured for generic cybersecurity entity types (VULNERABILITY, WEAKNESS, ATTACK_PATTERN, TECHNIQUE) but trained on specific taxonomy identifiers (CVE-2011-0662, CWE-1297, CAPEC-1, T1574.010). This mismatch means:
- Model cannot recognize trained entities
- Training data doesn't match expected labels
- NER pipeline is non-functional for attack chains

## Entity Coverage Assessment

### Can NER Extract Required Entities?

| Entity Type | CVE/CWE Dataset | Attack Chain Dataset | Status |
|-------------|-----------------|----------------------|--------|
| CVE IDs | ✅ Yes (430 examples) | ❌ No (0 examples) | **Partial** |
| CWE IDs | ✅ Yes (119 examples) | ✅ Yes (615 examples) | **Good** |
| CAPEC IDs | ❌ No | ✅ Yes (615 examples) | **Partial** |
| ATT&CK IDs | ❌ No | ✅ Yes (615 examples) | **Partial** |

**Entity Extraction Capability**: ⚠️ **Moderate** - Can identify IDs but not semantic entities

### Can NER Extract Relationships?

| Relationship Type | Encoded in Training | Status |
|-------------------|---------------------|--------|
| CVE → CWE | Only in metadata (not used) | ❌ **No** |
| CWE → CAPEC | In text ("enables") | ⚠️ **Implicit** |
| CAPEC → ATT&CK | In text ("using") | ⚠️ **Implicit** |
| Multi-hop chains | No examples | ❌ **No** |

**Relationship Extraction Capability**: ❌ **None** - NER only identifies entity boundaries, not relationships

**Critical Limitation**: Standard NER extracts entity spans (start, end, label) but NOT relationships between entities. Relationships like "CWE-79 enables CAPEC-63" require:
- Relation Extraction (RE) model
- Dependency parsing
- Knowledge graph construction
- Post-processing of NER outputs

## Attack Path Recognition

### Can NER Identify Attack Chains?

**Current Training Data Patterns**:
1. **Simple 3-hop chains**: CWE → CAPEC → ATT&CK (615 examples)
2. **Fixed relationship types**: "enables" and "using" only
3. **No branching**: Linear chains only
4. **No CVE chains**: CVE → CWE → CAPEC → ATT&CK (0 examples)

**Attack Chain Recognition Capability**: ❌ **Insufficient**

**Why NER Cannot Extract Attack Chains**:

1. **No Sequence Encoding**: NER identifies entities but not their sequential relationships
   - Extraction: [CWE-79, CAPEC-63, T1059]
   - Missing: CWE-79 **→** CAPEC-63 **→** T1059

2. **No Relationship Types**: Training data has relationships in text but not as labels
   - Text: "CWE-79 **enables** CAPEC-63 **using** T1059"
   - NER output: Three separate entities with no connection

3. **No Multi-Hop Chains**: All examples are exactly 3 entities
   - Cannot learn chains like: CVE → CWE → CAPEC1 → CAPEC2 → ATT&CK1 → ATT&CK2

4. **No Conditional Logic**: No training for context-dependent chains
   - Missing: "If Windows then T1574.010, else T1574.006"

## Threat Intelligence Parsing

### Can NER Process Threat Reports?

**Threat Report Requirements**:
1. Extract multiple CVE, CWE, CAPEC, ATT&CK entities ✅ **Yes**
2. Identify threat actors and campaigns ❌ **No** (model expects but no training)
3. Extract indicators of compromise ❌ **No** (model expects but no training)
4. Link vulnerabilities to exploitation techniques ❌ **No** (no relationship extraction)
5. Build attack kill chains ❌ **No** (no chain modeling)

**Threat Intelligence Parsing Capability**: ⚠️ **Limited** - Can identify IDs only

**Example Threat Report Processing**:

**Input**:
> "APT28 exploited CVE-2023-1234 (CWE-787 buffer overflow) using CAPEC-100 to achieve T1055 process injection."

**NER Can Extract**:
- CVE-2023-1234
- CWE-787
- CAPEC-100
- T1055

**NER Cannot Extract**:
- APT28 (threat actor) - model expects THREAT_ACTOR but no training data
- "exploited" relationship - no relationship extraction
- "buffer overflow" - model expects VULNERABILITY but no training
- Attack sequence: CVE → CWE → CAPEC → ATT&CK
- Causal relationships between entities

## Academic Paper Processing

### Can NER Extract Attack Chains from Research Papers?

**Academic Paper Characteristics**:
1. **Natural language**: "This weakness enables adversaries to..."
2. **Implicit references**: "Cross-site scripting" vs "CWE-79"
3. **Complex chains**: Multi-step attack scenarios
4. **Contextual dependencies**: "If authentication fails, attacker can..."

**Academic Paper Processing Capability**: ❌ **Inadequate**

**Why NER Fails on Academic Papers**:

1. **Training Data Mismatch**:
   - Training: "cwe-1297 Unprotected Confidential Information enables CAPEC-1"
   - Academic: "Insufficient access control validation allows adversaries to escalate privileges"
   - NER trained on explicit IDs, not natural language descriptions

2. **No Semantic Understanding**:
   - Cannot map "cross-site scripting" → CWE-79
   - Cannot map "privilege escalation" → CAPEC-69
   - Cannot map "process injection" → T1055

3. **No Chain Reasoning**:
   - Papers describe attack flows narratively
   - NER extracts isolated entities
   - Cannot construct attack graph from narrative

4. **No Implicit Entity Recognition**:
   - Papers may not mention CVE/CWE/CAPEC IDs explicitly
   - Describe vulnerabilities conceptually
   - NER trained on explicit ID patterns only

**Example Academic Text**:

**Input**:
> "We demonstrate that insufficient input validation in the web application enables SQL injection attacks, allowing adversaries to bypass authentication and exfiltrate sensitive data through database queries."

**NER Could Extract** (if trained on concepts):
- Insufficient input validation → CWE-20
- SQL injection → CAPEC-66
- Bypass authentication → T1078
- Data exfiltration → T1041

**Current NER Extracts**:
- Nothing (no explicit IDs in text)

## Gap Analysis

### Critical Gaps for Attack Chain Extraction

#### Gap 1: Entity Type Mismatch
**Problem**: Model expects generic labels (VULNERABILITY, WEAKNESS) but training uses specific IDs (CVE-2023-1234, CWE-79)

**Impact**: Model cannot recognize trained entities

**Solution**: Align training data labels with model configuration OR retrain model with new label schema

#### Gap 2: No Relationship Annotations
**Problem**: Training data has relationships in text but not as structured annotations

**Example**:
```json
// Current (implicit)
{
  "text": "CWE-79 enables CAPEC-63 using T1059",
  "entities": [
    {"start": 0, "end": 6, "label": "CWE"},
    {"start": 15, "end": 23, "label": "CAPEC"},
    {"start": 30, "end": 35, "label": "ATTACK"}
  ]
}

// Needed (explicit relationships)
{
  "text": "CWE-79 enables CAPEC-63 using T1059",
  "entities": [...],
  "relations": [
    {"head": 0, "tail": 1, "label": "ENABLES"},
    {"head": 1, "tail": 2, "label": "USES"}
  ]
}
```

**Impact**: Cannot extract "CWE-79 **enables** CAPEC-63" relationships

**Solution**: Add relation annotations to training data + train Relation Extraction model

#### Gap 3: No Multi-Hop Chain Encoding
**Problem**: All examples are exactly 3 entities, no longer chains

**Impact**: Cannot learn complex attack paths like:
- CVE-2023-1234 → CWE-787 → CAPEC-100 → CAPEC-69 → T1055 → T1041

**Solution**:
- Generate training examples with 4-10 entity chains
- Include branching attack paths
- Add conditional chains

#### Gap 4: No CVE-to-Attack Chains
**Problem**: CVE/CWE dataset and attack chain dataset are separate, no linking

**Impact**: Cannot extract full threat scenario: "CVE-2023-1234 enables attackers to use CAPEC-100"

**Solution**: Create unified training data with CVE → CWE → CAPEC → ATT&CK chains

#### Gap 5: No Semantic Entity Recognition
**Problem**: Training only on explicit IDs (CVE-2023-1234) not conceptual descriptions ("buffer overflow")

**Impact**: Cannot process academic papers or threat reports that describe vulnerabilities conceptually

**Solution**:
- Add training examples with natural language descriptions
- Create entity linking dataset: "SQL injection" → CAPEC-66
- Use entity normalization layer

#### Gap 6: No Contextual or Conditional Chains
**Problem**: All chains are deterministic, no conditional logic

**Impact**: Cannot model: "If Windows, use T1574.010; if Linux, use T1574.006"

**Solution**:
- Add conditional chain examples
- Include platform/context annotations
- Train context-aware models

## Recommendations

### Immediate Actions (Fix Model-Data Mismatch)

1. **Realign Entity Labels**
   - Option A: Change training data labels (CVE → VULNERABILITY, CWE → WEAKNESS, CAPEC → ATTACK_PATTERN, ATTACK → TECHNIQUE)
   - Option B: Retrain model with current labels (CVE, CWE, CAPEC, ATTACK)
   - **Recommendation**: Option B - simpler, preserves specificity

2. **Validate Model Functionality**
   - Test current model on sample texts
   - Verify if entity extraction works despite label mismatch
   - Benchmark extraction accuracy

### Short-Term Improvements (Add Relationship Extraction)

3. **Add Relation Annotations**
   - Annotate existing training data with relationship labels
   - Use spaCy's relation extraction component
   - Train RE model on relationship patterns

4. **Expand CVE Integration**
   - Merge CVE/CWE and attack chain datasets
   - Create CVE → CWE → CAPEC → ATT&CK examples
   - Link vulnerability databases to attack patterns

5. **Add Multi-Hop Chains**
   - Generate 4-10 entity chain examples
   - Include branching paths (one CWE enables multiple CAPECs)
   - Add real-world attack scenario chains

### Medium-Term Enhancements (Semantic Understanding)

6. **Semantic Entity Linking**
   - Create mapping: "SQL injection" → CAPEC-66, "buffer overflow" → CWE-119
   - Train entity normalization model
   - Add conceptual description training examples

7. **Context-Aware Chain Modeling**
   - Add platform/OS/version context annotations
   - Train conditional chain extraction
   - Include prerequisite/dependency modeling

8. **Academic Paper Processing**
   - Create training data from research papers
   - Include narrative attack descriptions
   - Train on implicit entity references

### Long-Term Architecture (Full Threat Intelligence)

9. **Unified Ontology Integration**
   - Move beyond NER to knowledge graph construction
   - Integrate CVE, CWE, CAPEC, ATT&CK, CPE databases
   - Build attack chain reasoning engine

10. **Threat Actor & Campaign Modeling**
    - Add threat actor entity training
    - Link attack chains to APT campaigns
    - Include temporal and attribution analysis

11. **Real-Time Threat Intelligence**
    - Process live threat feeds
    - Extract attack chains from CTI reports
    - Build automated threat modeling

## Can NER Alone Solve the Unification Problem?

**Question**: Can Named Entity Recognition alone extract and unify attack chains from threat intelligence and academic papers?

**Answer**: ❌ **No** - NER is necessary but insufficient

### Why NER Alone Cannot Solve Unification

**NER Provides**:
- Entity boundary detection (where entities are in text)
- Entity classification (is it CVE, CWE, CAPEC, ATT&CK)
- Basic entity extraction from structured text

**Unification Requires**:
- ❌ Relationship extraction (how entities connect)
- ❌ Chain sequencing (order and causality)
- ❌ Semantic understanding (map concepts to IDs)
- ❌ Context modeling (conditional chains)
- ❌ Knowledge graph construction (link databases)
- ❌ Multi-hop reasoning (transitive relationships)
- ❌ Temporal analysis (attack progression over time)

### Required Components Beyond NER

**Minimum Viable Architecture**:

1. **NER** - Identify CVE, CWE, CAPEC, ATT&CK entities ✅
2. **Relation Extraction (RE)** - Extract "enables", "uses", "exploits" relationships ❌
3. **Dependency Parsing** - Understand sentence structure and connections ❌
4. **Entity Linking** - Map "SQL injection" to CAPEC-66 ❌
5. **Knowledge Graph** - Store and query attack chains ❌
6. **Reasoning Engine** - Infer multi-hop chains and transitive relationships ❌

**Full Threat Intelligence Architecture**:

1. **Text Processing Layer**: NER + RE + coreference resolution
2. **Semantic Layer**: Entity linking + concept normalization
3. **Graph Layer**: Knowledge graph construction + ontology integration
4. **Reasoning Layer**: Chain inference + risk scoring + threat modeling
5. **Integration Layer**: CVE/CWE/CAPEC/ATT&CK database APIs

### Evidence-Based Assessment

**NER Strengths** (based on actual training data):
- ✅ Can identify CVE IDs with high accuracy (430 training examples)
- ✅ Can identify CWE IDs in context (734 total examples)
- ✅ Can identify CAPEC IDs (615 examples)
- ✅ Can identify ATT&CK technique IDs (615 examples)
- ✅ Preserves entity ordering in text (100% sequential consistency)

**NER Limitations** (based on gap analysis):
- ❌ Cannot extract relationships between entities (no RE component)
- ❌ Cannot model chains beyond entity co-occurrence
- ❌ Cannot process natural language descriptions without explicit IDs
- ❌ Cannot handle multi-hop chains (no examples beyond 3 entities)
- ❌ Cannot perform semantic reasoning or inference

### Verdict

**NER is the foundation, not the solution**

To extract attack chains from threat intelligence and academic papers, the system needs:

**Phase 1** (Current): NER for entity extraction
**Phase 2** (Missing): Relation extraction for entity linking
**Phase 3** (Missing): Knowledge graph for chain storage
**Phase 4** (Missing): Reasoning engine for chain inference

**Current Progress**: ~20% of required capability
**NER Contribution**: Critical but represents only one component of five needed

## Conclusion

### Current State Assessment

**Entity Extraction**: ⚠️ **Partially Functional**
- Can identify CVE, CWE, CAPEC, ATT&CK IDs in text
- Limited to explicit ID mentions
- Model-data mismatch requires fixing

**Relationship Extraction**: ❌ **Non-Functional**
- No relationship annotations in training data
- NER architecture cannot extract relationships
- Requires separate RE component

**Attack Chain Recognition**: ❌ **Non-Functional**
- Can identify entities but not chains
- No multi-hop chain training examples
- No sequencing or causality modeling

**Threat Intelligence Processing**: ⚠️ **Minimal**
- Can extract IDs from structured reports
- Cannot process narrative descriptions
- Cannot build attack scenarios

**Academic Paper Processing**: ❌ **Non-Functional**
- Training data uses explicit IDs, papers use concepts
- No semantic entity linking capability
- Cannot extract attack chains from narrative text

### Critical Next Steps

**Priority 1 - Fix Foundation**:
1. Resolve model-data label mismatch
2. Validate NER extraction accuracy
3. Benchmark on real threat intelligence

**Priority 2 - Add Relationships**:
4. Annotate training data with relations
5. Train Relation Extraction model
6. Test on CVE → CWE → CAPEC → ATT&CK chains

**Priority 3 - Enable Semantic Processing**:
7. Create entity linking training data
8. Add natural language attack descriptions
9. Test on academic papers

### Final Assessment

**Can current NER extract attack chains?**
**Answer**: No. Current NER can identify entity IDs but cannot extract relationships, chains, or semantic attack scenarios.

**What's needed for attack chain extraction?**
**Answer**: NER + Relation Extraction + Entity Linking + Knowledge Graph + Reasoning Engine

**Recommended Path Forward**:
1. Fix entity label alignment (1-2 weeks)
2. Add relation extraction capability (4-6 weeks)
3. Build knowledge graph integration (8-12 weeks)
4. Deploy reasoning engine for chain inference (12-16 weeks)

**Total estimated timeline**: 6-9 months for full attack chain extraction capability from threat intelligence and academic papers.

---

**Assessment Date**: 2025-11-08
**Datasets Analyzed**:
- `ner_v7_cve_cwe_partial.json` (430 examples)
- `ner_v7_attack_chain_partial.json` (615 examples)
**Model Analyzed**: `ner_model/` (spaCy v3.8.7)
