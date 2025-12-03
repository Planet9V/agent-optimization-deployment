# NER11 Gold Model Architecture - AEON Cyber Digital Twin

**File**: 08_NER11_GOLD_MODEL_ARCHITECTURE_v1.0_2025-12-03.md
**Created**: 2025-12-03 05:00:00 UTC
**Modified**: 2025-12-03 05:00:00 UTC
**Version**: v1.0.0
**Author**: AEON Architecture Team
**Purpose**: Comprehensive architecture documentation for the NER11 Gold Model - the SINGLE SOURCE OF TRUTH for Named Entity Recognition in the AEON Cyber Digital Twin system
**Status**: ACTIVE - PRODUCTION

---

## CRITICAL: SINGLE SOURCE OF TRUTH

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ██╗███████╗██████╗ ██╗ ██╗     ██╗   ██╗██████╗                     ║
║   ████╗  ██║██╔════╝██╔══██╗██║███║     ██║   ██║╚════██╗                    ║
║   ██╔██╗ ██║█████╗  ██████╔╝██║╚██║     ██║   ██║ █████╔╝                    ║
║   ██║╚██╗██║██╔══╝  ██╔══██╗██║ ██║     ╚██╗ ██╔╝ ╚═══██╗                    ║
║   ██║ ╚████║███████╗██║  ██║██║ ██║      ╚████╔╝ ██████╔╝                    ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═╝       ╚═══╝  ╚═════╝                     ║
║                                                                              ║
║   THE ONLY PRODUCTION MODEL: ner11_v3                                        ║
║   Model Path: models/ner11_v3/model-best                                     ║
║   F1 Score: 94.12%                                                           ║
║   Entity Types: 60                                                           ║
║                                                                              ║
║   ALL OTHER MODELS ARE DEPRECATED AND ARCHIVED                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Executive Summary

### 1.1 Purpose

The NER11 Gold Model is a spaCy transformer-based Named Entity Recognition (NER) model specifically trained for cybersecurity domain entity extraction. It serves as the core intelligence engine for the AEON Cyber Digital Twin system, enabling automated extraction of security-relevant entities from unstructured text.

### 1.2 Model Identity

| Property | Value |
|----------|-------|
| **Model ID** | `ner11_v3` |
| **Status** | PRODUCTION |
| **Version** | 3.0 |
| **F1 Score** | 94.12% |
| **Entity Types** | 60 |
| **Base Model** | `en_core_web_trf` (RoBERTa transformer) |
| **Model Path** | `models/ner11_v3/model-best` |
| **Docker Path** | `/app/models/ner11_v3/model-best` |
| **API Version** | 3.3.0 |

### 1.3 Critical Checksums (For Integrity Verification)

```
meta.json:   0710e14d78a87d54866208cc6a5c8de3 (MD5)
ner/model:   f326672a81a00c54be06422aae07ecf1 (MD5)
```

These checksums are verified at API startup to ensure model integrity.

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         AEON CYBER DIGITAL TWIN SYSTEM                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        NER11 GOLD MODEL API                              │   │
│  │                        (localhost:8000)                                  │   │
│  │                                                                          │   │
│  │  ┌────────────────────────────────────────────────────────────────────┐ │   │
│  │  │                    EXTRACTION PIPELINE                              │ │   │
│  │  │                                                                     │ │   │
│  │  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐   │ │   │
│  │  │   │   Pattern   │    │   Context   │    │   spaCy NER11_v3    │   │ │   │
│  │  │   │ Extraction  │    │ Augmentation│    │   Transformer       │   │ │   │
│  │  │   │ (Fallback)  │    │  (Short     │    │   Model             │   │ │   │
│  │  │   │             │    │   Text)     │    │                     │   │ │   │
│  │  │   │ Priority: 1 │    │ Priority: 2 │    │   Priority: 3       │   │ │   │
│  │  │   └──────┬──────┘    └──────┬──────┘    └──────────┬──────────┘   │ │   │
│  │  │          │                  │                      │              │ │   │
│  │  │          └──────────────────┴──────────────────────┘              │ │   │
│  │  │                             │                                      │ │   │
│  │  │                             ▼                                      │ │   │
│  │  │                   ┌─────────────────┐                             │ │   │
│  │  │                   │  Entity Merger  │                             │ │   │
│  │  │                   │  & Deduplication│                             │ │   │
│  │  │                   └────────┬────────┘                             │ │   │
│  │  │                            │                                       │ │   │
│  │  └────────────────────────────┼───────────────────────────────────────┘ │   │
│  │                               │                                          │   │
│  │  ┌────────────────────────────┼───────────────────────────────────────┐ │   │
│  │  │                   STORAGE LAYER                                     │ │   │
│  │  │                            │                                        │ │   │
│  │  │         ┌──────────────────┼──────────────────┐                    │ │   │
│  │  │         ▼                  ▼                  ▼                    │ │   │
│  │  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │ │   │
│  │  │  │   Qdrant    │    │   Neo4j     │    │ Claude-Flow │            │ │   │
│  │  │  │   Vector    │    │   Graph     │    │   Memory    │            │ │   │
│  │  │  │   Database  │    │   Database  │    │   Registry  │            │ │   │
│  │  │  │             │    │             │    │             │            │ │   │
│  │  │  │ 49,000+     │    │ 332,750     │    │ Model       │            │ │   │
│  │  │  │ vectors     │    │ nodes       │    │ checksums   │            │ │   │
│  │  │  │             │    │             │    │ validation  │            │ │   │
│  │  │  │ localhost:  │    │ localhost:  │    │ tests       │            │ │   │
│  │  │  │ 6333        │    │ 7687        │    │             │            │ │   │
│  │  │  └─────────────┘    └─────────────┘    └─────────────┘            │ │   │
│  │  │                                                                    │ │   │
│  │  └────────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                          │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Details

#### 2.2.1 NER11 Gold Model API (`serve_model.py`)

**Purpose**: FastAPI-based REST API that provides Named Entity Recognition services

**Key Features**:
- Multi-method entity extraction (pattern + model + context augmentation)
- Semantic search via Qdrant vector embeddings
- Graph database integration via Neo4j
- Model validation and checksum verification at startup
- Health monitoring endpoints

**API Endpoints**:
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ner` | POST | Extract entities from text |
| `/search` | POST | Semantic search for entities |
| `/hybrid` | POST | Combined semantic + graph search |
| `/health` | GET | Health check with validation status |

**Current Version**: 3.3.0

#### 2.2.2 Pattern Extraction Module (`utils/context_augmentation.py`)

**Purpose**: Regex-based fallback extraction for known entity formats

**Supported Patterns**:
- CVE IDs: `CVE-YYYY-NNNNN`
- CWE IDs: `CWE-NNN`
- APT Groups: `APT-NN`, `APT NN`, named groups
- MITRE Techniques: `TNNNN`, `TNNNN.NNN`
- MITRE Tactics: `TANNNN`
- Malware families: Known malware names
- IEC 62443 references: `SR/FR/RE/CR-N.N`
- MITRE EMB3D: `TID-NNN`, `MIT-NNN`
- Protocol names: Modbus, OPC-UA, DNP3, etc.
- Operating systems: Windows, Linux, macOS, etc.

#### 2.2.3 Context Augmentation Module

**Purpose**: Address context-dependency issues with short text inputs

**Problem Solved**: Transformer models require contextual information. Short inputs like "APT29" lack sufficient context for reliable extraction.

**Solution**: Domain-specific context templates are prepended to short inputs:
- APT/Threat actor context
- CVE/Vulnerability context
- Malware context
- Technique context
- ICS/OT context
- Generic cybersecurity context

#### 2.2.4 Model Validator (`utils/model_validator.py`)

**Purpose**: Ensure model integrity and correct loading

**Features**:
1. **Checksum Verification**: MD5 checksums for `meta.json` and `ner/model`
2. **Entity Extraction Tests**: 8 critical test cases validated at startup
3. **Registry Integration**: Claude-Flow memory and Qdrant for persistent registry
4. **Health Check Support**: Status information for monitoring

**Critical Validation Tests**:
| Test ID | Input | Expected Label | Min Confidence |
|---------|-------|----------------|----------------|
| T001 | APT29 | APT_GROUP | 0.90 |
| T002 | CVE-2024-12345 | CVE | 1.00 |
| T003 | T1566.001 | TECHNIQUE | 1.00 |
| T004 | CWE-79 | CWE | 1.00 |
| T005 | Cobalt Strike | MALWARE | 0.90 |
| T006 | TA0001 | TACTIC | 1.00 |
| T007 | IEC 62443-3-3 | IEC_62443 | 0.85 |
| T008 | TID-001 | MITRE_EM3D | 1.00 |

---

## 3. Entity Type Taxonomy

### 3.1 Complete Entity Type List (60 Types)

The NER11 Gold Model recognizes the following 60 entity types, organized by category:

#### 3.1.1 Threat Intelligence Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| APT_GROUP | Advanced Persistent Threat groups | APT29, Fancy Bear |
| THREAT_ACTOR | Named threat actors | Sandworm, Turla |
| MALWARE | Malware families and tools | Cobalt Strike, Emotet |
| RANSOMWARE | Ransomware-specific families | LockBit, REvil |
| CAMPAIGN | Attack campaigns | SolarWinds |
| INTRUSION_SET | Intrusion set identifiers | |

#### 3.1.2 Vulnerability Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| CVE | CVE identifiers | CVE-2024-12345 |
| CWE | Common Weakness Enumeration | CWE-79 |
| VULNERABILITY | Generic vulnerability mentions | buffer overflow |
| EXPLOIT | Exploit references | EternalBlue |

#### 3.1.3 MITRE Framework Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| TECHNIQUE | ATT&CK techniques | T1566.001 |
| TACTIC | ATT&CK tactics | TA0001 |
| MITIGATION | ATT&CK mitigations | M1049 |
| PROCEDURE | ATT&CK procedures | |
| ATTACK_PATTERN | Generic attack patterns | phishing |

#### 3.1.4 Standards and Frameworks

| Entity Type | Description | Example |
|-------------|-------------|---------|
| IEC_62443 | IEC 62443 references | SR 1.1, FR 2.1 |
| MITRE_EM3D | EMB3D threat IDs | TID-001 |
| NIST_CONTROL | NIST control references | AC-1 |
| ISO_27001 | ISO 27001 controls | A.5.1.1 |
| CAPEC | CAPEC attack patterns | CAPEC-66 |

#### 3.1.5 Technical Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| PROTOCOL | Network protocols | Modbus, OPC-UA |
| OPERATING_SYSTEM | Operating systems | Windows 10 |
| SOFTWARE | Software applications | Microsoft Exchange |
| HARDWARE | Hardware references | PLC, RTU |
| PORT | Network ports | port 443 |
| IP_ADDRESS | IP addresses | 192.168.1.1 |
| DOMAIN | Domain names | example.com |
| URL | URLs | https://... |
| FILE_HASH | File hashes (MD5, SHA) | |
| FILE_PATH | File system paths | /etc/passwd |
| REGISTRY_KEY | Windows registry keys | HKLM\... |

#### 3.1.6 Industrial Control System (ICS) Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| ICS_ASSET | ICS assets | HMI, PLC |
| SCADA | SCADA systems | |
| DCS | DCS systems | |
| INDUSTRIAL_PROTOCOL | ICS protocols | S7comm |
| SAFETY_SYSTEM | Safety systems | SIS |

#### 3.1.7 Organization and Location Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| ORGANIZATION | Organizations | Microsoft |
| VENDOR | Vendors | Siemens |
| SECTOR | Industry sectors | Energy |
| COUNTRY | Countries | Russia |
| LOCATION | Geographic locations | |

#### 3.1.8 Indicator Entities

| Entity Type | Description | Example |
|-------------|-------------|---------|
| INDICATOR | Generic indicators | |
| IOC | Indicators of compromise | |
| SIGNATURE | Detection signatures | YARA rule |

---

## 4. Integration Architecture

### 4.1 Data Flow

```
                              ┌─────────────────────────┐
                              │    External Sources     │
                              │ (Documents, APIs, Logs) │
                              └───────────┬─────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   Ingestion Scripts     │
                              │ • chunked_ingest.py     │
                              │ • rate_limited_ingest   │
                              │ • load_taxonomy.py      │
                              └───────────┬─────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           NER11 API (localhost:8000)                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────────────────────┐ │
│  │ POST /ner     │     │ POST /search  │     │ POST /hybrid                  │ │
│  │ Entity        │     │ Semantic      │     │ Semantic + Graph Search       │ │
│  │ Extraction    │     │ Search        │     │                               │ │
│  └───────┬───────┘     └───────┬───────┘     └───────────────┬───────────────┘ │
│          │                     │                             │                 │
└──────────┼─────────────────────┼─────────────────────────────┼─────────────────┘
           │                     │                             │
           ▼                     ▼                             ▼
┌─────────────────┐    ┌─────────────────┐           ┌─────────────────┐
│     Qdrant      │    │     Qdrant      │           │     Neo4j       │
│  Entity Store   │    │  Vector Search  │           │  Graph Query    │
│  localhost:6333 │    │                 │           │  localhost:7687 │
└─────────────────┘    └─────────────────┘           └─────────────────┘
```

### 4.2 Storage Layer Details

#### 4.2.1 Qdrant Vector Database

**Connection**: `localhost:6333`

**Collection**: `ner11_entities_hierarchical`

**Schema**:
```json
{
  "vector_size": 384,
  "distance": "Cosine",
  "payload_schema": {
    "text": "keyword",
    "label": "keyword",
    "source_file": "keyword",
    "created_at": "datetime"
  }
}
```

**Current Stats**:
- Vectors: 49,000+
- Embedding Model: all-MiniLM-L6-v2 (384 dimensions)

#### 4.2.2 Neo4j Graph Database

**Connection**: `bolt://localhost:7687`

**Authentication**: `neo4j` / `neo4j@openspg`

**Node Labels**:
- `Entity` - Generic extracted entities
- `CVE` - CVE nodes
- `CWE` - CWE nodes
- `Technique` - MITRE ATT&CK techniques
- `Tactic` - MITRE ATT&CK tactics
- `CAPEC` - CAPEC attack patterns
- `EMB3DThreat` - EMB3D threat IDs
- `EMB3DMitigation` - EMB3D mitigations
- `KEV` - Known Exploited Vulnerabilities

**Current Stats**:
- Nodes: 332,750
- Relationships: 11.2M

#### 4.2.3 Claude-Flow Memory Registry

**Namespace**: `ner11_model_registry`

**Stored Data**:
| Key | Description |
|-----|-------------|
| `model_inventory` | Complete list of all model versions |
| `model_checksums` | MD5 checksums for integrity verification |
| `validation_suite` | Test cases for startup validation |
| `loading_config` | Model loading configuration |
| `gold_model_v3` | Production model metadata |
| `validation_tests` | Quick validation test definitions |
| `validation_integration_complete` | Integration status |
| `final_validation_status` | Latest validation results |

---

## 5. Model Version History

### 5.1 Production Model: ner11_v3

| Property | Value |
|----------|-------|
| **Status** | PRODUCTION |
| **F1 Score** | 94.12% |
| **Entity Types** | 60 |
| **Created** | 2025-12-02 |
| **Path** | `models/ner11_v3/model-best` |
| **Size** | 976 MB |

### 5.2 Deprecated Models (ARCHIVED)

The following models are deprecated and have been archived to:
`D:\1_Apps_to_Build\AEON_Cyber_Digital_Twin_backups\deprecated_models\`

| Model ID | Status | Original F1 | Archive Date |
|----------|--------|-------------|--------------|
| ner11_v2 | DEPRECATED | 89% | 2025-12-03 |
| ner11_v1 | DEPRECATED | 82% | 2025-12-03 |
| ner11_v1_resumed | DEPRECATED | 84% | 2025-12-03 |
| ner_v9_comprehensive | LEGACY | N/A | 2025-12-03 |
| ner_v8_mitre | LEGACY | N/A | 2025-12-03 |

**IMPORTANT**: These models should NEVER be used in production. Only `ner11_v3` is supported.

---

## 6. Configuration Reference

### 6.1 Environment Variables

```bash
# Model Configuration
MODEL_PATH=models/ner11_v3/model-best       # Production model path
PRODUCTION_MODEL_ID=ner11_v3                # Model identifier

# Qdrant Configuration
QDRANT_HOST=localhost                       # Qdrant host
QDRANT_PORT=6333                            # Qdrant port
QDRANT_COLLECTION=ner11_entities_hierarchical  # Collection name

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687             # Neo4j connection URI
NEO4J_USER=neo4j                            # Neo4j username
NEO4J_PASSWORD=neo4j@openspg                # Neo4j password

# API Configuration
API_HOST=0.0.0.0                            # API listen address
API_PORT=8000                               # API port
API_WORKERS=4                               # Uvicorn workers
```

### 6.2 Docker Configuration

```yaml
# docker-compose.yml excerpt
services:
  ner11-api:
    image: ner11-gold-model:latest
    container_name: ner11-api
    ports:
      - "8000:8000"
    volumes:
      - ./models/ner11_v3:/app/models/ner11_v3:ro
    environment:
      - MODEL_PATH=/app/models/ner11_v3/model-best
      - QDRANT_HOST=qdrant
      - NEO4J_URI=bolt://neo4j:7687
    depends_on:
      - qdrant
      - neo4j
```

---

## 7. Security Considerations

### 7.1 Model Integrity

1. **Checksum Verification**: All model files are verified at startup
2. **Read-Only Mounting**: Model directory is mounted read-only in Docker
3. **Version Control**: Only `ner11_v3` is authorized for production use

### 7.2 API Security

1. **Input Validation**: All inputs are validated before processing
2. **Rate Limiting**: Consider implementing rate limiting for production
3. **Authentication**: Add authentication layer for external access

### 7.3 Data Security

1. **Credential Management**: Database credentials stored in environment variables
2. **Network Isolation**: Services communicate over internal Docker network
3. **Audit Logging**: All entity extractions can be logged for audit

---

## 8. Performance Characteristics

### 8.1 Extraction Performance

| Text Length | Avg Response Time | Throughput |
|-------------|-------------------|------------|
| < 100 chars | ~50ms | 20 req/s |
| 100-500 chars | ~100ms | 10 req/s |
| 500-2000 chars | ~200ms | 5 req/s |
| > 2000 chars | ~500ms | 2 req/s |

### 8.2 Search Performance

| Operation | Avg Response Time |
|-----------|-------------------|
| Qdrant vector search | ~10ms |
| Neo4j graph query | ~50ms |
| Hybrid search | ~100ms |

### 8.3 Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| GPU | Optional | NVIDIA with CUDA |
| Storage | 10 GB | 20 GB |

---

## 9. Troubleshooting Guide

### 9.1 Common Issues

#### Issue: Model fails to load
**Symptoms**: API returns 500 error on startup
**Solution**:
1. Verify model path exists: `ls -la models/ner11_v3/model-best/`
2. Check checksums: `python3 utils/model_validator.py --checksum-only`
3. Verify spaCy installation: `python3 -c "import spacy; print(spacy.__version__)"`

#### Issue: Low entity extraction accuracy
**Symptoms**: Expected entities not extracted
**Solution**:
1. Check if pattern extraction is enabled
2. Verify context augmentation for short text
3. Run validation tests: `python3 utils/model_validator.py --tests-only`

#### Issue: Checksum verification fails
**Symptoms**: Warning in startup logs about checksum mismatch
**Solution**:
1. Model may have been modified or corrupted
2. Re-download or restore from backup
3. Update checksums in `model_validator.py` if intentional change

### 9.2 Diagnostic Commands

```bash
# Check API health
curl http://localhost:8000/health

# Run validation tests
python3 utils/model_validator.py --api-url http://localhost:8000

# Check model checksums
python3 utils/model_validator.py --checksum-only

# Test entity extraction
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 exploited CVE-2024-1234"}'
```

---

## 10. Related Documentation

### 10.1 Wiki Documentation (1_AEON_DT_CyberSecurity_Wiki_Current)

| Location | Document | Description |
|----------|----------|-------------|
| 01_ARCHITECTURE | This document | Architecture overview |
| 01_Infrastructure | E30_NER11_INFRASTRUCTURE.md | Infrastructure setup |
| 03_SPECIFICATIONS | 09_NER11_MODEL_SPECIFICATION.md | Model specifications |
| 13_Procedures | 01_NER11_OPERATIONS_PROCEDURES.md | Operational procedures |

### 10.2 Code Documentation (5_NER11_Gold_Model)

| File | Description |
|------|-------------|
| serve_model.py | Main API server |
| utils/model_validator.py | Model validation module |
| utils/context_augmentation.py | Context augmentation and pattern extraction |

### 10.3 Registry Locations

| Registry | Location | Content |
|----------|----------|---------|
| Claude-Flow Memory | `ner11_model_registry` namespace | Model inventory, checksums, validation tests |
| Qdrant Collection | `ner11_model_registry` | Searchable model metadata |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-12-03 | Initial comprehensive architecture documentation |

---

**Document Owner**: AEON Architecture Team
**Review Cycle**: Monthly
**Next Review**: 2026-01-03
