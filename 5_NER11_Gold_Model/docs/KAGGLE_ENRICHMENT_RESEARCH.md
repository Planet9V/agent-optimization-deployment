# Kaggle Dataset Enrichment Research Report

**File**: KAGGLE_ENRICHMENT_RESEARCH.md
**Created**: 2025-12-10
**Version**: v1.0.0
**Author**: Research Agent
**Purpose**: Document Kaggle datasets for CVE and threat actor enrichment in E30 pipeline
**Status**: ACTIVE

---

## Executive Summary

This report identifies **5 high-value Kaggle datasets** and **3 external APT malware datasets** for enriching PROC-101 (CVE enrichment) and PROC-501 (threat actor enrichment) within the E30 ingestion pipeline. The datasets provide CVSS scores, CWE mappings, MITRE ATT&CK technique coverage, and threat actor behavioral profiles.

**Key Finding**: Kaggle hosts comprehensive CVE/CWE datasets (215,780+ CVEs from 1999-2025) but limited APT threat actor profile datasets. Primary APT behavioral data resides in GitHub repositories and academic sources.

---

## PROC-101 CVE Enrichment - Kaggle Datasets

### 1. CVE & CWE Dataset (1999 – 2025) ⭐ **PRIMARY RECOMMENDATION**

**Source**: [Kaggle - CVE & CWE Dataset (1999-2025)](https://www.kaggle.com/datasets/stanislavvinokur/cve-and-cwe-dataset-1999-2025)

**Coverage**:
- **Time Range**: CVE-1999-0001 through May 30, 2025
- **Estimated Records**: ~215,780 CVE entries (complete NVD coverage)
- **File Format**: CSV (compressed as ZIP, ~22.9 MB)

**Data Fields**:
| Field | Description | PROC-101 Mapping |
|-------|-------------|------------------|
| `CVE-ID` | Official CVE identifier | `:CVE {id}` |
| `CVSS-V4` | CVSS v4 base score | `cvssV4BaseScore` (NEW) |
| `CVSS-V3` | CVSS v3 base score | `cvssV31BaseScore` |
| `CVSS-V2` | CVSS v2 base score | `cvssV2BaseScore` |
| `SEVERITY` | Qualitative severity (LOW/MEDIUM/HIGH/CRITICAL) | `cvssV31BaseSeverity` |
| `DESCRIPTION` | Normalized English description | `description` |
| `CWE-ID` | CWE code (e.g., CWE-79) | `:IS_WEAKNESS_TYPE` relationship |

**Enrichment Value**:
- ✅ **Complete CVSS version history** (v2, v3, v4) for 215,780 CVEs
- ✅ **Direct CWE mappings** for `IS_WEAKNESS_TYPE` relationships (McKenney Q8)
- ✅ **Severity classifications** for risk prioritization
- ✅ **May 2025 coverage** - most current dataset available

**Integration Plan**:
```cypher
// Enrich existing CVEs with CVSS scores and CWE mappings
LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row
MATCH (cve:CVE {id: row.`CVE-ID`})
SET
  cve.cvssV31BaseScore = toFloat(row.`CVSS-V3`),
  cve.cvssV31BaseSeverity = row.SEVERITY,
  cve.cvssV2BaseScore = toFloat(row.`CVSS-V2`),
  cve.cvssV4BaseScore = toFloat(row.`CVSS-V4`),
  cve.description = row.DESCRIPTION

// Create CWE relationships
WITH cve, row
WHERE row.`CWE-ID` IS NOT NULL AND row.`CWE-ID` <> 'NVD-CWE-Other'
MERGE (cwe:CWE {id: row.`CWE-ID`})
MERGE (cve)-[:IS_WEAKNESS_TYPE]->(cwe)
```

**McKenney Alignment**: Q3 (CVSS enrichment), Q5 (CWE mappings), Q7 (severity scoring), Q8 (weakness taxonomy)

---

### 2. CVE 2024 Database: Exploits, CVSS, OS

**Source**: [Kaggle - CVE 2024 Database](https://www.kaggle.com/datasets/manavkhambhayata/cve-2024-database-exploits-cvss-os)

**Coverage**:
- **Time Range**: January 1-15, 2024 (live-extracted from NVD)
- **Records**: 1,314 CVE entries
- **File Format**: CSV (ZIP, 118 KB)

**Data Fields**:
| Field | PROC-101 Mapping |
|-------|------------------|
| `CVE ID` | `:CVE {id}` |
| `Description` | `description` |
| `CVSS Score` | `cvssV31BaseScore` (version unspecified ⚠️) |
| `Attack Vector` | `attackVector` (NEW attribute) |
| `Affected OS` | `:AFFECTS` → `:Platform` relationships (NEW) |

**Enrichment Value**:
- ✅ **Attack vector classification** (Network/Local/Adjacent/Physical)
- ✅ **OS impact mapping** for platform-specific vulnerability tracking
- ⚠️ **CVSS version ambiguity** (not specified if v3.0/v3.1)

**Integration Plan**:
```cypher
// Enrich with attack vectors and OS platforms
LOAD CSV WITH HEADERS FROM 'file:///cve_2024_database.csv' AS row
MATCH (cve:CVE {id: row.`CVE ID`})
SET cve.attackVector = row.`Attack Vector`

// Create platform relationships
WITH cve, row
UNWIND split(row.`Affected OS`, ',') AS os
MERGE (p:Platform {name: trim(os)})
MERGE (cve)-[:AFFECTS]->(p)
```

**Use Case**: Supplement Dataset #1 with attack vector and platform data for 2024 CVEs.

---

### 3. CVSS v3.1 Dataset

**Source**: [Kaggle - CVSS v3.1](https://www.kaggle.com/datasets/thumb8432/cvss-v31)

**Coverage**:
- **Time Range**: 2021 (older snapshot)
- **Records**: Unknown (pre-2021 CVEs)
- **File Format**: CSV

**Data Fields**:
- Vulnerability descriptions
- CVSS v3.1 base metrics evaluation results

**Enrichment Value**:
- ⚠️ **Superseded by Dataset #1** (CVE & CWE 1999-2025 has newer data)
- Use only if Dataset #1 is unavailable

---

## PROC-501 Threat Actor Enrichment - Datasets

### 4. Cybersec MITRE Tactics & Techniques Instruction Data ⭐ **PRIMARY RECOMMENDATION**

**Source**: [Kaggle - MITRE Tactics & Techniques](https://www.kaggle.com/datasets/tejaswara/cybersec-mitre-tactics-techniques-instruction-data)

**Coverage**:
- **MITRE ATT&CK Framework**: Tactics, Techniques, Procedures (TTPs)
- **File Format**: ZIP (Q&A format for LLM training)
- **File Size**: 383 KB
- **Last Updated**: 2024-07-05

**Data Structure**:
- **Tactics**: High-level attack categories (e.g., Initial Access, Execution)
- **Techniques**: Specific attack methods (e.g., T1059.001 - PowerShell)
- **Descriptions**: Detailed explanations of each technique
- **Detection Methods**: How to identify technique usage
- **Targeted Platforms**: Affected OS/systems

**Enrichment Value**:
- ✅ **MITRE ATT&CK technique coverage** for `:USES` relationships
- ✅ **Detection indicators** for blue team defensive mapping
- ✅ **Platform targeting** for cross-referencing with CVE platform data
- ⚠️ **Q&A format** (requires parsing for Neo4j ingestion)

**Integration Plan**:
```cypher
// Parse Q&A format to extract techniques and map to threat actors
// Example: "Question: What is T1059.001? Answer: PowerShell execution..."
LOAD CSV WITH HEADERS FROM 'file:///mitre_tactics_techniques.csv' AS row
WITH row WHERE row.question CONTAINS 'T1059'
MERGE (t:Technique {id: extractTechniqueID(row.question)})
SET
  t.name = extractTechniqueName(row.answer),
  t.description = row.answer,
  t.detection = row.detection_method,
  t.platform = row.targeted_platforms

// Link to existing threat actors via STIX data (from PROC-501)
MATCH (ta:ThreatActor)-[:USES]->(t:Technique)
RETURN ta.name, t.id, t.name
```

**McKenney Alignment**: Q9 (ATT&CK technique linkage), Q10 (behavioral profiling)

---

### 5. APT Malware Datasets (External - NOT Kaggle)

**Note**: Kaggle has **limited APT threat actor profile datasets**. Primary sources are GitHub and academic repositories.

#### Dataset 5A: GitHub APTMalware (cyber-research)

**Source**: [GitHub - APTMalware Dataset](https://github.com/cyber-research/APTMalware)

**Coverage**:
- **Malware Samples**: 3,500+ state-sponsored malware samples
- **APT Groups**: 12 groups (APT1, APT10, APT19, APT21, APT28, APT29, APT30, Dark Hotel, Energetic Bear, Equation Group, Gorgon Group, Winnti)
- **Nation-State Attribution**: 5 different nation-states

**Enrichment Value**:
- ✅ **Threat actor to malware mapping** for behavioral profiling
- ✅ **Nation-state attribution** for geopolitical context
- ⚠️ **Malware samples only** (no direct TTP profiles)

**Integration Plan**:
```cypher
// Create malware families and link to threat actors
MERGE (ta:ThreatActor {name: "APT28"})
MERGE (m:Malware {family: "X-Agent", source: "APTMalware-GitHub"})
MERGE (ta)-[:USES_MALWARE]->(m)
SET m.samples = 350, m.nationState = "Russia"
```

---

#### Dataset 5B: ADAPT Dataset (SecPriv)

**Source**: [GitHub - ADAPT Attribution Dataset](https://github.com/SecPriv/adapt)

**Coverage**:
- **APT Samples**: 6,134 malware samples
- **Threat Groups**: 92 distinct APT groups
- **Label Standardization**: Consistent group naming across datasets

**Enrichment Value**:
- ✅ **Largest labeled APT dataset** (92 groups vs. 12 in Dataset 5A)
- ✅ **Machine learning ready** (label-standardized)
- ⚠️ **Requires researcher contact** (samples not publicly downloadable)

**Integration Plan**:
```cypher
// Enrich threat actor nodes with sample counts and standardized names
LOAD CSV WITH HEADERS FROM 'file:///adapt_labels.csv' AS row
MERGE (ta:ThreatActor {name: row.standardized_group_name})
SET
  ta.sampleCount = toInteger(row.sample_count),
  ta.datasetSource = "ADAPT-SecPriv",
  ta.labelVariants = split(row.alias_names, ';')
```

---

#### Dataset 5C: Large APT Malware Dataset (ScienceDirect)

**Source**: [ScienceDirect - APT Malware Features](https://www.sciencedirect.com/science/article/abs/pii/S0167404821000262)

**Coverage**:
- **Total Samples**: 19,457 malware samples
  - APT: 1,497 samples
  - Non-APT: 17,960 samples
- **Features**: 1,944 features (static, dynamic, network traffic analysis)

**Enrichment Value**:
- ✅ **Behavioral feature vectors** for psychometric profiling (McKenney-Lacan integration)
- ✅ **APT vs. non-APT classification** data
- ⚠️ **Academic paywall** (not freely accessible)

---

## Integration Strategy for E30 Pipeline

### Phase 1: CVE Enrichment (PROC-101)

**Dataset Priority**:
1. **CVE & CWE Dataset (1999-2025)** → Primary CVSS/CWE enrichment
2. **CVE 2024 Database** → Attack vector and platform supplementation

**Implementation**:
```bash
# Download datasets
kaggle datasets download stanislavvinokur/cve-and-cwe-dataset-1999-2025
kaggle datasets download manavkhambhayata/cve-2024-database-exploits-cvss-os

# Unzip and place in Neo4j import directory
unzip cve-and-cwe-dataset-1999-2025.zip -d /var/lib/neo4j/import/
unzip cve-2024-database.zip -d /var/lib/neo4j/import/

# Run Cypher enrichment scripts (see Dataset #1 and #2 above)
```

**Expected Enrichment**:
- **215,780 CVEs** with CVSS v2/v3/v4 scores
- **~150,000 CWE relationships** (estimated 70% CVEs have CWE mappings)
- **1,314 CVEs** with attack vector and platform data

---

### Phase 2: Threat Actor Enrichment (PROC-501)

**Dataset Priority**:
1. **MITRE Tactics & Techniques** → ATT&CK technique coverage
2. **GitHub APTMalware** → Malware-to-actor mapping
3. **ADAPT Dataset** → 92 APT group standardized labels

**Implementation**:
```bash
# Download Kaggle MITRE dataset
kaggle datasets download tejaswara/cybersec-mitre-tactics-techniques-instruction-data

# Clone GitHub APT repositories
git clone https://github.com/cyber-research/APTMalware.git
git clone https://github.com/SecPriv/adapt.git

# Parse Q&A format for MITRE techniques
python scripts/parse_mitre_qa_to_neo4j.py

# Import APT group labels
python scripts/import_apt_labels.py
```

**Expected Enrichment**:
- **~600 MITRE ATT&CK techniques** with detection methods
- **12 APT groups** with 3,500 malware samples (GitHub)
- **92 APT groups** with standardized naming (ADAPT)
- **150+ threat actors** with behavioral profiles (existing PROC-501 + new data)

---

### Phase 3: Cross-Validation & McKenney Alignment

**Validation Queries**:

```cypher
// Q3: CVSS enrichment coverage
MATCH (cve:CVE)
WITH count(cve) AS total,
     count(cve.cvssV31BaseScore) AS enriched
RETURN total, enriched, 100.0 * enriched / total AS coverage_pct

// Q5: CWE relationship coverage
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
WITH count(DISTINCT cve) AS cves_with_cwe,
     count(DISTINCT cwe) AS unique_cwes
RETURN cves_with_cwe, unique_cwes

// Q8: Threat actor technique usage
MATCH (ta:ThreatActor)-[:USES]->(t:Technique)
RETURN ta.name, count(t) AS technique_count
ORDER BY technique_count DESC
LIMIT 10

// Q9: Attack vector distribution
MATCH (cve:CVE)
WHERE cve.attackVector IS NOT NULL
RETURN cve.attackVector, count(*) AS count
ORDER BY count DESC
```

---

## Data Quality Assessment

### Strengths

| Dataset | Quality Rating | Strengths |
|---------|----------------|-----------|
| CVE & CWE (1999-2025) | ⭐⭐⭐⭐⭐ | Complete NVD coverage, multi-version CVSS, clean CWE mappings |
| CVE 2024 Database | ⭐⭐⭐⭐ | Attack vector data, OS platforms, active maintenance |
| MITRE Tactics & Techniques | ⭐⭐⭐⭐ | Official ATT&CK coverage, detection methods, LLM-ready format |
| GitHub APTMalware | ⭐⭐⭐ | Nation-state attribution, real malware samples |
| ADAPT Dataset | ⭐⭐⭐⭐⭐ | Largest APT coverage (92 groups), label standardization |

### Limitations

| Dataset | Limitations | Mitigation |
|---------|-------------|------------|
| CVE 2024 Database | CVSS version unspecified | Cross-reference with NVD API or Dataset #1 |
| MITRE Tactics & Techniques | Q&A format (not structured) | Parse with NLP or regex extraction |
| GitHub APTMalware | Limited to 12 APT groups | Supplement with ADAPT (92 groups) |
| ADAPT Dataset | Samples not publicly available | Use label data only, request samples separately |
| All APT datasets | No direct psychometric profiles | Infer from technique usage patterns (McKenney-Lacan) |

---

## McKenney Research Question Coverage

| Question | Dataset(s) | Enrichment Type |
|----------|-----------|-----------------|
| Q3: CVSS scoring | CVE & CWE (1999-2025) | CVSS v2/v3/v4 base scores |
| Q5: Vulnerability classification | CVE & CWE (1999-2025) | CWE taxonomy mappings |
| Q7: Risk prioritization | CVE & CWE (1999-2025), CVE 2024 | Severity + attack vector |
| Q8: Weakness patterns | CVE & CWE (1999-2025) | `:IS_WEAKNESS_TYPE` relationships |
| Q9: Threat actor TTPs | MITRE Tactics & Techniques | `:USES` → `:Technique` relationships |
| Q10: Behavioral profiling | GitHub APTMalware, ADAPT | Malware families + technique patterns |

---

## Recommendations

### Immediate Actions (E30 Completion)

1. **Download and ingest CVE & CWE Dataset (1999-2025)** for comprehensive CVSS/CWE enrichment
2. **Download MITRE Tactics & Techniques** for ATT&CK technique coverage
3. **Clone GitHub APTMalware repository** for threat actor-malware mappings

### Short-Term (E31 Extension)

4. **Request ADAPT dataset samples** from SecPriv researchers for 92-group coverage
5. **Develop Q&A parser** for MITRE dataset to extract structured technique data
6. **Implement attack vector enrichment** from CVE 2024 Database

### Long-Term (E32+ Future Work)

7. **Integrate IEEE DataPort MITRE dataset** (1,427 nodes, 2,543 relationships) for graph-native enrichment
8. **Explore Splunk Attack Data** for real-world attack telemetry
9. **Develop McKenney-Lacan psychometric inference** from technique usage patterns

---

## Sources

### Kaggle Datasets
- [CVE & CWE Dataset (1999 – 2025)](https://www.kaggle.com/datasets/stanislavvinokur/cve-and-cwe-dataset-1999-2025)
- [CVE 2024 Database: Exploits, CVSS, OS](https://www.kaggle.com/datasets/manavkhambhayata/cve-2024-database-exploits-cvss-os)
- [CVSS v3.1](https://www.kaggle.com/datasets/thumb8432/cvss-v31)
- [Cybersec MITRE Tactics & Techniques Instruction Data](https://www.kaggle.com/datasets/tejaswara/cybersec-mitre-tactics-techniques-instruction-data)
- [CVE and CWE Mapping Dataset (2021)](https://www.kaggle.com/datasets/krooz0/cve-and-cwe-mapping-dataset)

### External APT Datasets
- [GitHub - APTMalware Dataset](https://github.com/cyber-research/APTMalware)
- [GitHub - ADAPT Attribution Dataset](https://github.com/SecPriv/adapt)
- [ScienceDirect - APT Malware Feature Analysis](https://www.sciencedirect.com/science/article/abs/pii/S0167404821000262)
- [Papers with Code - APT-Malware Dataset](https://paperswithcode.com/dataset/apt-malware)

### MITRE ATT&CK Resources
- [MITRE ATT&CK Official](https://attack.mitre.org/)
- [GitHub - MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data)
- [IEEE DataPort - MITRE Attack Dataset](https://ieee-dataport.org/documents/mitre-attack-dataset-knowledge-graph-enhanced-rag-cyber-threat-intelligence)

### Research Papers
- [ADAPT it! Automating APT Campaign Attribution](https://dl.acm.org/doi/fullHtml/10.1145/3678890.3678909)
- [Advanced Persistent Threat Attribution Survey](https://arxiv.org/html/2409.11415v1)
- [Cyber Science Lab - APT Malware Dataset](https://cybersciencelab.com/advanced-persistent-threat-apt-malware-dataset/)

---

**Report Complete** | Research Agent | 2025-12-10
