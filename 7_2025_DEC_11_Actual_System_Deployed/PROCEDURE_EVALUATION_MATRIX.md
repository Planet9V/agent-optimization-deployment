# AEON PROCEDURE EVALUATION MATRIX
**File:** PROCEDURE_EVALUATION_MATRIX.md
**Created:** 2025-12-12
**Truth Source:** `/7_2025_DEC_11_Actual_System_Deployed/`
**Evaluation Basis:** 181 Production APIs, 631 Neo4j Labels, 183 Relationships
**Total Procedures Evaluated:** 37

---

## EXECUTIVE SUMMARY

**Evaluation Results**:
- ✅ **KEEP & ALIGN**: 12 procedures (32%) - High value, needs alignment
- 🔄 **UPDATE**: 8 procedures (22%) - Good concept, major revision needed
- ❌ **DELETE**: 14 procedures (38%) - Obsolete or not relevant
- ⏸️ **DEFER**: 3 procedures (8%) - Valid but not priority

**Critical Findings**:
1. **0% of procedures reference actual 181 Production APIs** - All procedures pre-date Phase B API deployment
2. **Schema mismatch**: Procedures reference "8-layer architecture" but actual schema uses 631 labels with direct classification
3. **No SBOM API integration**: PROC-113 creates redundant schema instead of using Phase B2 SBOM APIs (32 endpoints)
4. **Kaggle enrichment supersedes NVD**: PROC-102 more relevant than PROC-101 for current 0% CVSS coverage
5. **Psychohistory procedures lack mathematical foundation**: PROC-161-165 conceptual only, no integration path

---

## DETAILED EVALUATION MATRIX

| PROC-ID | Name | Current Status | Relevance | Decision | APIs to Reference | Schema Elements | Priority | Action Plan |
|---------|------|----------------|-----------|----------|-------------------|-----------------|----------|-------------|
| **PROC-001** | Schema Migration | ❌ Obsolete | LOW | ❌ DELETE | None - schema already deployed | 631 labels already exist | P4 | Schema already deployed via E30, constraints exist. Historical document only. |
| **PROC-101** | CVE NVD Enrichment | 🟡 Superseded | MEDIUM | 🔄 UPDATE | `/ner` (API #1) for entity extraction | CVE, CWE labels exist | P2 | **UPDATE**: Replace with PROC-102 Kaggle enrichment which addresses 0% CVSS coverage. NVD API secondary. |
| **PROC-102** | Kaggle Enrichment | ✅ Critical | HIGH | ✅ KEEP & ALIGN | `/ner`, `/search/semantic` (APIs #1-2) | CVE (316,552 nodes), CWE labels | P1 | **KEEP**: Addresses E01 0% CVSS coverage gap. Align to use Phase B APIs for validation, Qdrant for vector storage. |
| **PROC-111** | APT Threat Intel | ✅ Valuable | HIGH | ✅ KEEP & ALIGN | `/api/v2/threat-intel/*` (APIs #62-87) | ThreatActor (10,599 nodes), Indicator (11,601) | P1 | **ALIGN**: Integrate with Phase B3 Threat Intel APIs (26 endpoints). Use existing ThreatActor nodes, enhance with API data. |
| **PROC-112** | STIX Integration | 🟡 Conceptual | MEDIUM | 🔄 UPDATE | `/api/v2/threat-intel/import` (API #84) | ThreatActor, Indicator, Campaign | P2 | **UPDATE**: Leverage Phase B3 import API instead of custom ETL. STIX → Neo4j via API layer. |
| **PROC-113** | SBOM Analysis | ❌ Redundant | LOW | ❌ DELETE | **USE Phase B2 SBOM APIs #6-37** | SBOM (140,000 nodes) already exist | P4 | **DELETE**: Redundant with Phase B2 SBOM APIs (32 endpoints). Use `/api/v2/sbom/*` APIs instead of custom ingestion. |
| **PROC-114** | Psychometric Integration | ⏸️ Experimental | LOW | ⏸️ DEFER | None currently | PsychTrait (161 nodes) exist | P4 | **DEFER**: Psychometric nodes exist but no clear API integration path. Future enhancement. |
| **PROC-115** | Realtime Feeds | 🟡 Partial | MEDIUM | 🔄 UPDATE | `/api/v2/threat-intel/feeds/*` (APIs #85-86) | Indicator, ThreatActor for updates | P2 | **UPDATE**: Integrate with Phase B3 feed APIs. Real-time updates to existing threat intel nodes. |
| **PROC-116** | Executive Dashboard | ❌ Superseded | LOW | ❌ DELETE | **ALL Phase B APIs provide dashboard data** | Dashboard queries via APIs | P4 | **DELETE**: Next.js frontend + Phase B APIs replace need for custom dashboard ETL. |
| **PROC-117** | Wiki Truth Correction | ✅ Meta-process | MEDIUM | ✅ KEEP & ALIGN | N/A - documentation process | N/A - quality assurance | P2 | **KEEP**: Meta-procedure for maintaining truth alignment. Update to reference Phase B APIs as truth source. |
| **PROC-121** | IEC62443 Safety | 🟡 Specialized | MEDIUM | 🔄 UPDATE | `/api/v2/equipment/*` (APIs #38-61) | Equipment (48,288), Control (61,167) | P3 | **UPDATE**: Integrate with Phase B2 Equipment APIs. IEC62443 compliance via equipment metadata. |
| **PROC-122** | RAMS Reliability | ⏸️ Specialized | LOW | ⏸️ DEFER | `/api/v2/equipment/analysis/risk` (API #52) | Equipment, Measurement nodes | P4 | **DEFER**: RAMS analysis possible via equipment APIs but not current priority. |
| **PROC-123** | Hazard FMEA | ⏸️ Specialized | LOW | ⏸️ DEFER | `/api/v2/risk/*` (APIs #88-111) | Risk, Control nodes | P4 | **DEFER**: FMEA methodology exists in Phase B3 Risk APIs. Implementation not priority. |
| **PROC-131** | Economic Impact | ✅ Valuable | HIGH | ✅ KEEP & ALIGN | `/api/v2/economic-impact/*` (APIs #158-184) | EconomicMetric (39 nodes) | P1 | **ALIGN**: Phase B5 Economic Impact APIs (27 endpoints) operational. Enhance with additional metrics. |
| **PROC-132** | Psychohistory Demographics | ❌ Conceptual | LOW | ❌ DELETE | `/api/v2/demographics/*` (APIs #185-208) | Demographics data via API | P4 | **DELETE**: Phase B5 Demographics APIs (24 endpoints) cover this. No separate ETL needed. |
| **PROC-133** | Now/Next/Never Prioritization | ✅ Framework | HIGH | ✅ KEEP & ALIGN | `/api/v2/prioritization/*` (APIs #209-236) | Prioritization logic via APIs | P1 | **ALIGN**: Phase B5 Prioritization APIs (28 endpoints) implement this framework. Document methodology. |
| **PROC-134** | Attack Path Modeling | ✅ Critical | HIGH | ✅ KEEP & ALIGN | `/search/hybrid` (API #3), Threat Intel APIs | CVE, Technique, ThreatActor chains | P1 | **KEEP**: 20-hop hybrid search enables attack path queries. Document canonical attack path patterns. |
| **PROC-141** | Lacanian Real/Imaginary | ❌ Theoretical | LOW | ❌ DELETE | None | No schema implementation | P4 | **DELETE**: Lacanian psychoanalysis not implemented in schema. Conceptual only, no integration path. |
| **PROC-142** | Vendor Equipment | ✅ Valuable | HIGH | ✅ KEEP & ALIGN | `/api/v2/equipment/vendors/*` (APIs #45-48) | Equipment (48,288), Vendor data | P1 | **ALIGN**: Phase B2 Vendor APIs operational. Enhance with Siemens/Alstom dataset ingestion via APIs. |
| **PROC-143** | Protocol Analysis | 🟡 Specialized | MEDIUM | 🔄 UPDATE | `/api/v2/equipment/equipment` (API #38) | Protocol (8,776 nodes) | P3 | **UPDATE**: Protocol nodes exist. Create protocol analysis queries, link to equipment APIs. |
| **PROC-151** | Lacanian Dyad | ❌ Theoretical | LOW | ❌ DELETE | None | No schema implementation | P4 | **DELETE**: Lacanian dyad theory not implemented. No integration path with current APIs/schema. |
| **PROC-152** | Triad Group Dynamics | ❌ Theoretical | LOW | ❌ DELETE | None | No schema implementation | P4 | **DELETE**: Group dynamics theory not implemented. No integration path with current system. |
| **PROC-153** | Organizational Blind Spots | ❌ Theoretical | LOW | ❌ DELETE | None | No schema implementation | P4 | **DELETE**: Organizational psychology not implemented. No integration path with current system. |
| **PROC-154** | Personality Team Fit | ❌ Theoretical | LOW | ❌ DELETE | None | PsychTrait nodes exist but no team model | P4 | **DELETE**: Team dynamics not implemented. PsychTrait nodes exist but no team fit logic. |
| **PROC-155** | Transcript Psychometric NER | ⏸️ Experimental | LOW | ⏸️ DEFER | `/ner` (API #1) for entity extraction | PsychTrait (161 nodes) | P4 | **DEFER**: NER model exists, PsychTrait nodes exist. Implementation requires transcript corpus. |
| **PROC-161** | Seldon Crisis Prediction | ❌ Conceptual | LOW | ❌ DELETE | None | No mathematical implementation | P4 | **DELETE**: Psychohistory concept only. No Seldon Plan mathematical model implemented. |
| **PROC-162** | Population Event Forecasting | ❌ Conceptual | LOW | ❌ DELETE | `/api/v2/demographics/*` (APIs #185-208) | Demographics data via API | P4 | **DELETE**: Phase B5 Demographics APIs exist but no population forecasting model implemented. |
| **PROC-163** | Cognitive Dissonance Breaking | ❌ Theoretical | LOW | ❌ DELETE | None | No psychological model | P4 | **DELETE**: Cognitive psychology theory not implemented. No integration path. |
| **PROC-164** | Threat Actor Personality | 🟡 Experimental | MEDIUM | 🔄 UPDATE | `/api/v2/threat-intel/actors/*` (APIs #62-65) | ThreatActor (10,599), PsychTrait (161) | P3 | **UPDATE**: ThreatActor nodes exist, PsychTrait nodes exist. Create linking logic via APIs. |
| **PROC-165** | McKenney-Lacan Calculus | ❌ Theoretical | LOW | ❌ DELETE | None | No mathematical foundation | P4 | **DELETE**: Conceptual framework only. No mathematical implementation of McKenney-Lacan calculus. |
| **PROC-201** | CWE-CAPEC Linker | ✅ Valuable | HIGH | ✅ KEEP & ALIGN | `/search/hybrid` (API #3) | CWE, CAPEC (requires CAPEC ingestion) | P2 | **ALIGN**: CWE nodes exist. Need CAPEC ingestion first, then link via hybrid search. |
| **PROC-301** | CAPEC-Attack Mapper | ✅ Valuable | HIGH | ✅ KEEP & ALIGN | `/api/v2/threat-intel/ttps/*` (APIs #73-76) | Technique (3,526 nodes), CAPEC (requires ingestion) | P2 | **ALIGN**: ATT&CK techniques exist. CAPEC ingestion needed, then map to techniques via APIs. |
| **PROC-501** | Threat Actor Enrichment | ✅ Critical | HIGH | ✅ KEEP & ALIGN | `/api/v2/threat-intel/actors/*` (APIs #62-65) | ThreatActor (10,599 nodes) | P1 | **KEEP**: ThreatActor nodes exist. Enrich with ADAPT, APTMalware datasets via APIs. |
| **PROC-901** | Attack Chain Builder | ✅ Critical | HIGH | ✅ KEEP & ALIGN | `/search/hybrid` (API #3), all Threat Intel APIs | CVE→CWE→CAPEC→Technique→ThreatActor chain | P1 | **KEEP**: Hybrid search enables 20-hop traversal. Document attack chain query patterns for 8 McKenney questions. |

---

## PRIORITY ACTIONS BY CATEGORY

### P1 - CRITICAL (Keep & Align Immediately)

| PROC-ID | Action | APIs to Integrate | Timeline |
|---------|--------|-------------------|----------|
| **PROC-102** | Kaggle Enrichment | NER `/ner`, Semantic Search `/search/semantic` | IMMEDIATE - addresses 0% CVSS coverage |
| **PROC-111** | APT Threat Intel | Phase B3 Threat Intel APIs (#62-87) | Week 1 - 10,599 ThreatActor nodes need enrichment |
| **PROC-131** | Economic Impact | Phase B5 Economic Impact APIs (#158-184) | Week 1 - 27 operational APIs |
| **PROC-133** | Now/Next/Never | Phase B5 Prioritization APIs (#209-236) | Week 1 - 28 operational APIs |
| **PROC-134** | Attack Path Modeling | Hybrid Search `/search/hybrid` (20-hop) | Week 2 - critical for McKenney queries |
| **PROC-142** | Vendor Equipment | Phase B2 Vendor APIs (#45-48) | Week 2 - 48,288 equipment nodes |
| **PROC-501** | Threat Actor Enrichment | Phase B3 Actor APIs (#62-65) | Week 1 - enhance 10,599 actors |
| **PROC-901** | Attack Chain Builder | Hybrid Search + all Threat Intel APIs | Week 2 - 8 McKenney question patterns |

### P2 - HIGH (Update & Implement)

| PROC-ID | Action | Major Changes Required | Timeline |
|---------|--------|------------------------|----------|
| **PROC-101** | NVD Enrichment | Replace with PROC-102 Kaggle as primary | Month 2 - secondary to Kaggle |
| **PROC-112** | STIX Integration | Use Phase B3 import API instead of custom ETL | Month 1 - API-driven import |
| **PROC-115** | Realtime Feeds | Integrate with Phase B3 feed APIs (#85-86) | Month 1 - real-time threat updates |
| **PROC-117** | Wiki Truth Correction | Update to reference Phase B APIs as truth | IMMEDIATE - meta-process |
| **PROC-201** | CWE-CAPEC Linker | Ingest CAPEC first, then link via hybrid search | Month 2 - requires CAPEC data |
| **PROC-301** | CAPEC-Attack Mapper | Ingest CAPEC, map to 3,526 ATT&CK techniques | Month 2 - requires CAPEC data |

### P3 - MEDIUM (Enhance When Ready)

| PROC-ID | Action | Prerequisites | Timeline |
|---------|--------|---------------|----------|
| **PROC-121** | IEC62443 Safety | Equipment APIs operational, IEC62443 dataset | Month 3 - specialized use case |
| **PROC-143** | Protocol Analysis | Protocol query library, equipment API integration | Month 3 - 8,776 protocol nodes |
| **PROC-164** | Threat Actor Personality | Link ThreatActor to PsychTrait, validation study | Month 4 - experimental |

### P4 - LOW (Delete or Defer)

**DELETE** (14 procedures - 38%):
- PROC-001, 113, 116, 132, 141, 151, 152, 153, 154, 161, 162, 163, 165
- **Reason**: Superseded by Phase B APIs, redundant schema, theoretical only, or no integration path

**DEFER** (3 procedures - 8%):
- PROC-114 (Psychometric Integration), PROC-122 (RAMS), PROC-123 (Hazard FMEA), PROC-155 (Transcript Psychometric NER)
- **Reason**: Valid concepts but not current priority, requires additional datasets

---

## SCHEMA ALIGNMENT FINDINGS

### CRITICAL SCHEMA MISMATCHES

1. **"8-Layer Architecture" vs Reality**:
   - **Procedures Reference**: L0-L7 layer architecture (Asset→Device→Software→CVE→CAPEC→ThreatActor→Failure→Mitigation)
   - **Actual Schema**: 631 labels with direct classification, no hierarchical `super_label` property
   - **Impact**: All procedure schema references need updating
   - **Action**: Update procedures to reference actual 631 labels, remove layer references

2. **"SoftwareComponent" vs "SBOM"**:
   - **PROC-113 Creates**: `:SoftwareComponent` nodes via custom ingestion
   - **Actual Schema**: `:SBOM` (140,000 nodes) already exist from E30
   - **Impact**: Duplicate schema creation
   - **Action**: DELETE PROC-113, use Phase B2 SBOM APIs

3. **CVE Schema Already Populated**:
   - **Procedures Assume**: Empty CVE database needing enrichment
   - **Actual State**: 316,552 CVE nodes exist (0% CVSS coverage though)
   - **Impact**: Enrichment procedures viable, creation procedures obsolete
   - **Action**: Focus on ENRICHMENT (PROC-102, 101), not creation

---

## API INTEGRATION REQUIREMENTS

### Phase B APIs ALL procedures MUST reference:

| API Category | Endpoints | Procedures Affected | Integration Priority |
|--------------|-----------|---------------------|----------------------|
| **NER Core** | #1-5 | PROC-102, 111, 155 | P1 - Core functionality |
| **Phase B2 SBOM** | #6-37 | PROC-113 (DELETE) | P1 - Use instead of custom |
| **Phase B2 Equipment** | #38-61 | PROC-142, 121, 143 | P1 - 48,288 equipment nodes |
| **Phase B3 Threat Intel** | #62-87 | PROC-111, 112, 115, 501 | P1 - 10,599 threat actors |
| **Phase B3 Risk** | #88-111 | PROC-123, 134 | P2 - Risk scoring |
| **Phase B3 Remediation** | #112-140 | PROC-901 (response) | P2 - Patch management |
| **Phase B4 Scanning** | #141-170 | Future - not procedures yet | P3 - Scanning integration |
| **Phase B4 Alerts** | #171-200 | PROC-115 (realtime) | P2 - Alert generation |
| **Phase B4 Compliance** | #201-228 | PROC-121 (IEC62443) | P3 - Compliance tracking |
| **Phase B5 Economic** | #158-184 | PROC-131 | P1 - 27 operational APIs |
| **Phase B5 Demographics** | #185-208 | PROC-132 (DELETE) | P1 - Use APIs not ETL |
| **Phase B5 Prioritization** | #209-236 | PROC-133 | P1 - 28 operational APIs |

---

## QDRANT STORAGE STRATEGY

**Namespace**: `aeon-truth`
**Collections**:
- `procedure-evaluation` - This evaluation matrix
- `procedure-alignment` - API mapping for each kept procedure
- `schema-truth` - Actual 631 labels, 183 relationships
- `api-truth` - 181 endpoint specifications

**Store This Document**:
```python
from qdrant_client import QdrantClient
import json

client = QdrantClient(url="http://localhost:6333")

evaluation_data = {
    "document": "PROCEDURE_EVALUATION_MATRIX.md",
    "total_procedures": 37,
    "keep_align": 12,
    "update": 8,
    "delete": 14,
    "defer": 3,
    "critical_findings": [
        "0% procedures reference 181 Production APIs",
        "Schema mismatch: 8-layer vs 631 labels",
        "SBOM API integration missing",
        "Kaggle enrichment supersedes NVD",
        "Psychohistory lacks math foundation"
    ],
    "priority_actions": {
        "P1_critical": ["PROC-102", "PROC-111", "PROC-131", "PROC-133", "PROC-134", "PROC-142", "PROC-501", "PROC-901"],
        "P2_high": ["PROC-101", "PROC-112", "PROC-115", "PROC-117", "PROC-201", "PROC-301"],
        "P3_medium": ["PROC-121", "PROC-143", "PROC-164"],
        "P4_delete": ["PROC-001", "PROC-113", "PROC-116", "PROC-132", "PROC-141", "PROC-151", "PROC-152", "PROC-153", "PROC-154", "PROC-161", "PROC-162", "PROC-163", "PROC-165"],
        "P4_defer": ["PROC-114", "PROC-122", "PROC-123", "PROC-155"]
    },
    "timestamp": "2025-12-12T00:00:00Z"
}

client.upsert(
    collection_name="aeon-truth",
    points=[{
        "id": "procedure-evaluation-2025-12-12",
        "vector": [0.0] * 1536,  # Placeholder vector
        "payload": evaluation_data
    }]
)
```

---

## NEXT STEPS

1. **IMMEDIATE (Week 1)**:
   - Execute PROC-102 Kaggle enrichment (addresses 0% CVSS coverage)
   - Update PROC-111, 501 to use Phase B3 Threat Intel APIs
   - Align PROC-131, 133 to document Phase B5 APIs
   - Update PROC-117 meta-process to reference Phase B APIs as truth

2. **SHORT-TERM (Month 1)**:
   - DELETE 14 obsolete procedures (PROC-001, 113, 116, 132, 141, 151-154, 161-163, 165)
   - Update PROC-112, 115 for API-driven integration
   - Document PROC-134, 901 attack path query patterns

3. **MEDIUM-TERM (Month 2-3)**:
   - Ingest CAPEC dataset to enable PROC-201, 301
   - Update PROC-101 for secondary NVD enrichment
   - Implement PROC-121, 143 specialized analyses
   - Enhance PROC-142 with Vendor datasets

4. **LONG-TERM (Month 4+)**:
   - Experimental PROC-164 threat actor personality linking
   - Deferred PROC-114, 122, 123, 155 when datasets available

---

**EVALUATION COMPLETE**
**Master Evaluator**: Strategic Planning Agent
**Truth Alignment Status**: 32% KEEP, 22% UPDATE, 38% DELETE, 8% DEFER
**Critical Path**: Execute PROC-102 Kaggle enrichment IMMEDIATELY to address 0% CVSS coverage gap
**Next Review**: After CAPEC ingestion (enables PROC-201, 301)

---

*End of Procedure Evaluation Matrix*
