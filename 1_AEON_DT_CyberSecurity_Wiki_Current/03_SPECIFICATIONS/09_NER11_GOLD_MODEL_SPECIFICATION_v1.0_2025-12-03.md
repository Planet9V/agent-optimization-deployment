# NER11 Gold Standard Model - Complete Specification

**File**: 09_NER11_GOLD_MODEL_SPECIFICATION_v1.0_2025-12-03.md
**Created**: 2025-12-03 00:00:00 UTC
**Modified**: 2025-12-03 00:00:00 UTC
**Version**: v1.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete technical specification for NER11 Gold Standard Model
**Status**: ACTIVE

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ██╗███████╗██████╗ ██╗ ██╗     ██╗   ██╗██████╗                    ║
║   ████╗  ██║██╔════╝██╔══██╗██║███║     ██║   ██║╚════██╗                   ║
║   ██╔██╗ ██║█████╗  ██████╔╝██║╚██║     ██║   ██║ █████╔╝                   ║
║   ██║╚██╗██║██╔══╝  ██╔══██╗██║ ██║     ╚██╗ ██╔╝ ╚═══██╗                   ║
║   ██║ ╚████║███████╗██║  ██║██║ ██║      ╚████╔╝ ██████╔╝                   ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═╝       ╚═══╝  ╚═════╝                    ║
║                                                                              ║
║                    GOLD STANDARD MODEL SPECIFICATION                         ║
║                              Version 1.0                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Executive Summary

### 1.1 Model Identity

| Attribute | Value |
|-----------|-------|
| **Model ID** | `ner11_v3` |
| **Model Name** | NER11 Gold Standard |
| **Model Path** | `models/ner11_v3/model-best` |
| **Base Architecture** | spaCy Transformer (roberta-base) |
| **Training Framework** | spaCy v3.7.2+ |
| **Performance** | 94.12% F1 Score |
| **Entity Types** | 60 NER Labels, 566 Fine-Grained Types |
| **Status** | PRODUCTION |

### 1.2 Single Source of Truth

**CRITICAL**: This model (`ner11_v3`) is the ONLY approved production model for the AEON Cyber Digital Twin system. All other model versions (ner11_v1, ner11_v2, ner_v8, ner_v9) are DEPRECATED and archived.

---

## 2. Model Technical Specifications

### 2.1 Architecture Specification

```yaml
model_architecture:
  name: "NER11 Gold Standard"
  version: "v3"
  framework: "spaCy"
  framework_version: ">=3.7.2"

  base_model:
    name: "roberta-base"
    type: "transformer"
    hidden_size: 768
    attention_heads: 12
    hidden_layers: 12
    vocabulary_size: 50265
    max_position_embeddings: 514

  ner_component:
    type: "SpanCategorizer + EntityRecognizer"
    labels: 60
    fine_grained_types: 566
    transition_model: "BIO-tagging"

  training_config:
    optimizer: "AdamW"
    learning_rate: 5e-5
    warmup_steps: 1000
    batch_size: 16
    max_epochs: 50
    early_stopping: true
    patience: 5
```

### 2.2 File Structure Specification

```
models/ner11_v3/model-best/
├── meta.json                    # Model metadata (CHECKSUM: 0710e14d78a87d54866208cc6a5c8de3)
├── config.cfg                   # spaCy configuration
├── tokenizer                    # Tokenizer configuration
├── vocab/
│   ├── key2row                  # Vocabulary key mapping
│   ├── lookups.bin              # Lookup tables
│   ├── strings.json             # String store
│   ├── vectors                  # Word vectors
│   └── vectors.cfg              # Vector configuration
└── ner/
    ├── cfg                      # NER component config
    ├── model                    # NER weights (CHECKSUM: f326672a81a00c54be06422aae07ecf1)
    └── moves                    # Transition moves
```

### 2.3 Checksum Verification Specification

```yaml
checksum_verification:
  algorithm: "MD5"
  critical_files:
    - file: "meta.json"
      expected_checksum: "0710e14d78a87d54866208cc6a5c8de3"
      purpose: "Model metadata integrity"
    - file: "ner/model"
      expected_checksum: "f326672a81a00c54be06422aae07ecf1"
      purpose: "NER weights integrity"

  verification_timing:
    - "Server startup (mandatory)"
    - "Health check endpoint"
    - "On-demand validation"

  failure_behavior:
    checksum_mismatch: "Log warning, continue with degraded status"
    file_missing: "Fail startup, raise RuntimeError"
```

---

## 3. Entity Type Specification

### 3.1 Tier 1 - NER Labels (60 Types)

#### 3.1.1 Threat Intelligence Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `APT_GROUP` | Advanced Persistent Threat groups | APT29, Fancy Bear | 0.90 |
| `THREAT_ACTOR` | Named threat actors | Sandworm, Turla | 0.85 |
| `MALWARE` | Malware families and variants | Cobalt Strike, Emotet | 0.85 |
| `CAMPAIGN` | Cyber attack campaigns | SolarWinds, NotPetya | 0.80 |
| `RANSOMWARE` | Ransomware families | LockBit, REvil | 0.90 |
| `BACKDOOR` | Backdoor malware | Sunburst, ShadowPad | 0.85 |
| `EXPLOIT_KIT` | Exploit kit names | Angler, RIG | 0.80 |
| `BOTNET` | Botnet names | Mirai, Emotet | 0.85 |

#### 3.1.2 Vulnerability Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `CVE` | CVE identifiers | CVE-2024-12345 | 1.00 |
| `CWE` | CWE weakness identifiers | CWE-79 | 1.00 |
| `VULNERABILITY` | Named vulnerabilities | Log4Shell, Heartbleed | 0.85 |
| `ZERO_DAY` | Zero-day references | zero-day exploit | 0.75 |

#### 3.1.3 MITRE ATT&CK Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `TECHNIQUE` | ATT&CK techniques | T1566.001 | 1.00 |
| `TACTIC` | ATT&CK tactics | TA0001 | 1.00 |
| `ATTACK_PATTERN` | Attack patterns | Spear Phishing | 0.85 |
| `MITIGATION` | ATT&CK mitigations | M1049 | 0.90 |
| `SOFTWARE` | ATT&CK software | S0154 | 0.90 |

#### 3.1.4 Industrial Control System (ICS/OT) Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `ICS_ASSET` | Industrial control assets | PLC, RTU, SCADA | 0.85 |
| `PROTOCOL` | Industrial protocols | Modbus, OPC-UA, DNP3 | 0.90 |
| `IEC_62443` | IEC 62443 references | SR 1.1, FR-2 | 0.85 |
| `MITRE_EM3D` | EMB3D threat references | TID-001, MIT-001 | 1.00 |
| `SAFETY_SYSTEM` | Safety instrumented systems | SIS, SIF, SIL | 0.80 |
| `DCS` | Distributed control systems | DCS, Honeywell | 0.85 |
| `HMI` | Human-machine interface | HMI, SCADA display | 0.85 |
| `PLC` | Programmable logic controllers | Siemens PLC, Allen-Bradley | 0.85 |

#### 3.1.5 Infrastructure Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `IP_ADDRESS` | IP addresses | 192.168.1.1 | 0.95 |
| `DOMAIN` | Domain names | example.com | 0.90 |
| `URL` | Full URLs | https://example.com/path | 0.90 |
| `EMAIL` | Email addresses | user@example.com | 0.95 |
| `FILE_HASH` | File hashes (MD5, SHA) | a1b2c3... | 0.95 |
| `NETWORK_ZONE` | Network segments | DMZ, OT Network | 0.80 |
| `PORT` | Network ports | port 443, TCP/22 | 0.85 |

#### 3.1.6 Compliance and Standards Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `COMPLIANCE` | Compliance frameworks | NIST, ISO 27001 | 0.85 |
| `REGULATION` | Regulations | GDPR, HIPAA | 0.85 |
| `STANDARD` | Security standards | IEC 62443, NERC CIP | 0.85 |
| `CONTROL` | Security controls | AC-1, SC-7 | 0.80 |
| `REQUIREMENT` | Requirements | SL-2 requirement | 0.75 |

#### 3.1.7 Organizational Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `ORGANIZATION` | Organizations | Microsoft, CISA | 0.85 |
| `VENDOR` | Vendors | Siemens, Rockwell | 0.85 |
| `INDUSTRY` | Industries | Energy, Healthcare | 0.80 |
| `COUNTRY` | Countries | United States, China | 0.90 |
| `REGION` | Regions | APAC, EMEA | 0.80 |

#### 3.1.8 Technical Entities

| Label | Description | Example | Confidence Threshold |
|-------|-------------|---------|---------------------|
| `OPERATING_SYSTEM` | OS names | Windows 10, Linux | 0.85 |
| `SOFTWARE_PRODUCT` | Software names | Apache, nginx | 0.85 |
| `HARDWARE_PRODUCT` | Hardware names | Cisco ASA | 0.85 |
| `PROGRAMMING_LANGUAGE` | Languages | Python, JavaScript | 0.85 |
| `TOOL` | Security tools | Nmap, Metasploit | 0.85 |
| `ENCRYPTION` | Encryption methods | AES-256, RSA | 0.85 |

### 3.2 Tier 2 - Fine-Grained Types (566 Types)

Fine-grained types provide sub-classification within Tier 1 labels. Examples:

```yaml
fine_grained_hierarchy:
  MALWARE:
    - RANSOMWARE_VARIANT    # e.g., LockBit 3.0
    - TROJAN                # e.g., Emotet loader
    - WORM                  # e.g., WannaCry
    - RAT                   # e.g., Cobalt Strike beacon
    - ROOTKIT               # e.g., TDL-4
    - SPYWARE               # e.g., Pegasus
    - CRYPTOMINER           # e.g., XMRig

  ICS_ASSET:
    - PLC_SIEMENS           # Siemens S7 series
    - PLC_ALLEN_BRADLEY     # Rockwell PLCs
    - RTU_SCHNEIDER         # Schneider RTUs
    - SCADA_SERVER          # SCADA systems
    - DCS_HONEYWELL         # Honeywell DCS
    - HMI_WONDERWARE        # Wonderware HMI
    - HISTORIAN_PI          # OSIsoft PI

  PROTOCOL:
    - MODBUS_TCP            # Modbus/TCP
    - MODBUS_RTU            # Modbus/RTU
    - OPC_UA                # OPC Unified Architecture
    - DNP3                  # Distributed Network Protocol
    - IEC104                # IEC 60870-5-104
    - PROFINET              # PROFINET
    - ETHERNET_IP           # EtherNet/IP
    - BACNET                # BACnet
```

---

## 4. API Specification

### 4.1 Endpoint Specifications

#### 4.1.1 Entity Extraction Endpoint

```yaml
endpoint: POST /ner
description: "Extract named entities from text"
request:
  content_type: "application/json"
  body:
    text: string (required)

response:
  content_type: "application/json"
  body:
    entities:
      - text: string       # Entity text
        label: string      # NER label (Tier 1)
        start: integer     # Character start position
        end: integer       # Character end position
        score: float       # Confidence score (0.0-1.0)
    doc_length: integer    # Document token count

performance:
  latency_p50: "<50ms"
  latency_p99: "<200ms"
  throughput: ">100 req/s"
```

#### 4.1.2 Semantic Search Endpoint

```yaml
endpoint: POST /search/semantic
description: "Semantic similarity search with hierarchical filtering"
request:
  content_type: "application/json"
  body:
    query: string (required)
    limit: integer (default: 10, max: 100)
    label_filter: string (optional)         # Tier 1 filter
    fine_grained_filter: string (optional)  # Tier 2 filter
    confidence_threshold: float (default: 0.0)

response:
  content_type: "application/json"
  body:
    results:
      - score: float           # Similarity score
        entity: string         # Entity text
        ner_label: string      # Tier 1 label
        fine_grained_type: string  # Tier 2 type
        hierarchy_path: string # Full hierarchy path
        confidence: float      # Extraction confidence
        doc_id: string         # Source document ID
    query: string
    filters_applied: object
    total_results: integer

performance:
  latency_p50: "<100ms"
  latency_p99: "<500ms"
```

#### 4.1.3 Hybrid Search Endpoint

```yaml
endpoint: POST /search/hybrid
description: "Combined semantic + graph expansion search"
request:
  content_type: "application/json"
  body:
    query: string (required)
    limit: integer (default: 10)
    expand_graph: boolean (default: true)
    hop_depth: integer (default: 2, range: 1-3)
    label_filter: string (optional)
    fine_grained_filter: string (optional)
    confidence_threshold: float (default: 0.0)
    relationship_types: array[string] (optional)
      # Options: EXPLOITS, USES, TARGETS, AFFECTS,
      #          ATTRIBUTED_TO, MITIGATES, INDICATES

response:
  content_type: "application/json"
  body:
    results:
      - score: float
        entity: string
        ner_label: string
        fine_grained_type: string
        hierarchy_path: string
        confidence: float
        doc_id: string
        related_entities:
          - name: string
            label: string
            hop_distance: integer
            relationship: string
            relationship_direction: string
        graph_context: object
    query: string
    filters_applied: object
    total_semantic_results: integer
    total_graph_entities: integer
    graph_expansion_enabled: boolean
    hop_depth: integer
    performance_ms: float

performance:
  latency_p50: "<200ms"
  latency_p99: "<500ms"
  target: "<500ms"
```

#### 4.1.4 Health Check Endpoint

```yaml
endpoint: GET /health
description: "Service health and model status"
response:
  content_type: "application/json"
  body:
    status: string              # healthy | unhealthy
    ner_model_custom: string    # loaded | not_loaded
    ner_model_fallback: string  # loaded | not_loaded
    model_checksum: string      # verified | not_verified
    model_validator: string     # available | not_available
    pattern_extraction: string  # enabled | disabled
    ner_extraction: string      # enabled | disabled
    semantic_search: string     # available | not_available
    neo4j_graph: string         # connected | not_connected
    version: string             # API version
```

### 4.2 Error Response Specification

```yaml
error_responses:
  400_bad_request:
    status_code: 400
    body:
      detail: "Validation error description"

  422_unprocessable_entity:
    status_code: 422
    body:
      detail:
        - loc: ["body", "field"]
          msg: "Error message"
          type: "error_type"

  500_internal_error:
    status_code: 500
    body:
      detail: "Internal error description"

  503_service_unavailable:
    status_code: 503
    body:
      detail: "Service not available: {reason}"
```

---

## 5. Integration Specifications

### 5.1 Qdrant Vector Database Integration

```yaml
qdrant_integration:
  host: "localhost"
  port: 6333
  collection: "ner11_entities_hierarchical"

  vector_configuration:
    dimensions: 384
    distance_metric: "cosine"
    embedding_model: "all-MiniLM-L6-v2"

  payload_schema:
    text: string              # Entity text
    label: string             # NER label (Tier 1)
    fine_grained_type: string # Fine-grained type (Tier 2)
    hierarchy_path: string    # Full hierarchy path
    confidence: float         # Extraction confidence
    source_file: string       # Source document
    created_at: string        # Timestamp
    doc_id: string            # Document identifier

  indexing:
    type: "HNSW"
    m: 16
    ef_construct: 100

  filtering:
    tier1_filter: "label"
    tier2_filter: "fine_grained_type"
    confidence_filter: "confidence"
```

### 5.2 Neo4j Graph Database Integration

```yaml
neo4j_integration:
  uri: "bolt://localhost:7687"
  user: "neo4j"
  password: "${NEO4J_PASSWORD}"

  supported_labels:
    - CVE
    - CWE
    - CAPEC
    - Technique
    - Tactic
    - EMB3DThreat
    - EMB3DMitigation
    - Entity
    - KEV

  supported_relationships:
    - EXPLOITS
    - USES
    - TARGETS
    - AFFECTS
    - ATTRIBUTED_TO
    - MITIGATES
    - INDICATES
    - HAS_WEAKNESS
    - RELATED_TO

  graph_expansion:
    max_hop_depth: 3
    max_results_per_hop: 20
    timeout: 5000ms
```

### 5.3 Claude-Flow Memory Integration

```yaml
claude_flow_integration:
  memory_namespace: "ner11_model_registry"

  stored_metadata:
    - key: "production_model"
      value: "ner11_v3"
    - key: "model_status"
      value: "PRODUCTION"
    - key: "f1_score"
      value: "0.9412"
    - key: "entity_types"
      value: "60"
    - key: "checksums"
      value: "{meta_json: '...', ner_model: '...'}"
    - key: "validation_timestamp"
      value: "ISO8601 timestamp"
```

---

## 6. Environment Configuration Specification

### 6.1 Required Environment Variables

```yaml
required_environment:
  MODEL_PATH:
    description: "Path to NER11 model"
    default: "models/ner11_v3/model-best"
    required: true

  NEO4J_URI:
    description: "Neo4j Bolt connection URI"
    default: "bolt://localhost:7687"
    required: true

  NEO4J_USER:
    description: "Neo4j username"
    default: "neo4j"
    required: true

  NEO4J_PASSWORD:
    description: "Neo4j password"
    default: "neo4j@openspg"
    required: true
    sensitive: true

  QDRANT_HOST:
    description: "Qdrant server hostname"
    default: "localhost"
    required: true

  QDRANT_PORT:
    description: "Qdrant server port"
    default: "6333"
    required: true

  QDRANT_COLLECTION:
    description: "Qdrant collection name"
    default: "ner11_entities_hierarchical"
    required: true
```

### 6.2 Optional Environment Variables

```yaml
optional_environment:
  FALLBACK_MODEL:
    description: "Fallback NER model"
    default: "en_core_web_trf"

  USE_FALLBACK_NER:
    description: "Enable fallback model"
    default: "true"

  NER_API_URL:
    description: "NER API URL for embedding service"
    default: "http://localhost:8000"

  LOG_LEVEL:
    description: "Logging verbosity"
    default: "INFO"
    options: ["DEBUG", "INFO", "WARNING", "ERROR"]
```

---

## 7. Performance Specifications

### 7.1 Latency Requirements

| Operation | P50 | P95 | P99 | Maximum |
|-----------|-----|-----|-----|---------|
| Entity Extraction | 50ms | 100ms | 200ms | 500ms |
| Semantic Search | 100ms | 200ms | 300ms | 500ms |
| Hybrid Search | 200ms | 350ms | 500ms | 1000ms |
| Health Check | 10ms | 20ms | 50ms | 100ms |

### 7.2 Throughput Requirements

| Operation | Minimum | Target | Peak |
|-----------|---------|--------|------|
| Entity Extraction | 50 req/s | 100 req/s | 200 req/s |
| Semantic Search | 20 req/s | 50 req/s | 100 req/s |
| Hybrid Search | 10 req/s | 25 req/s | 50 req/s |

### 7.3 Resource Requirements

```yaml
resource_requirements:
  minimum:
    cpu: 2 cores
    memory: 4 GB
    disk: 5 GB

  recommended:
    cpu: 4 cores
    memory: 8 GB
    disk: 20 GB
    gpu: "optional (CUDA 11.x)"

  production:
    cpu: 8 cores
    memory: 16 GB
    disk: 50 GB
    gpu: "NVIDIA T4/V100 (recommended)"
```

---

## 8. Security Specifications

### 8.1 Authentication and Authorization

```yaml
security_requirements:
  api_authentication:
    current: "None (internal use)"
    planned: "API key or JWT"

  network_security:
    binding: "0.0.0.0:8000 (container)"
    exposure: "localhost only (production)"
    tls: "Required for external access"

  credential_management:
    neo4j_password: "Environment variable only"
    api_keys: "Environment variable only"
    no_hardcoding: "MANDATORY"
```

### 8.2 Input Validation

```yaml
input_validation:
  text_input:
    max_length: 1000000  # 1MB
    encoding: "UTF-8"
    sanitization: "HTML entity encoding"

  query_parameters:
    limit_max: 100
    hop_depth_max: 3
    confidence_range: [0.0, 1.0]
```

---

## 9. Validation Test Specifications

### 9.1 Critical Validation Tests

The following tests MUST pass for model validation:

```yaml
critical_tests:
  - id: "T001"
    input: "APT29"
    expected_label: "APT_GROUP"
    confidence_min: 0.9
    method: "pattern"

  - id: "T002"
    input: "CVE-2024-12345"
    expected_label: "CVE"
    confidence_min: 1.0
    method: "pattern"

  - id: "T003"
    input: "T1566.001"
    expected_label: "TECHNIQUE"
    confidence_min: 1.0
    method: "pattern"

  - id: "T004"
    input: "CWE-79"
    expected_label: "CWE"
    confidence_min: 1.0
    method: "pattern"

  - id: "T005"
    input: "Cobalt Strike"
    expected_label: "MALWARE"
    confidence_min: 0.9
    method: "pattern"

  - id: "T006"
    input: "TA0001"
    expected_label: "TACTIC"
    confidence_min: 1.0
    method: "pattern"

  - id: "T007"
    input: "IEC 62443-3-3"
    expected_label: "IEC_62443"
    confidence_min: 0.85
    method: "pattern"

  - id: "T008"
    input: "TID-001"
    expected_label: "MITRE_EM3D"
    confidence_min: 1.0
    method: "pattern"
```

### 9.2 Pattern Extraction Specifications

```yaml
pattern_specifications:
  CVE:
    pattern: '\bCVE-\d{4}-\d{4,7}\b'
    confidence: 1.0
    examples:
      - "CVE-2024-12345"
      - "CVE-2021-44228"

  CWE:
    pattern: '\bCWE-\d{1,4}\b'
    confidence: 1.0
    examples:
      - "CWE-79"
      - "CWE-1234"

  APT_GROUP:
    pattern: '\bAPT[-\s]?\d{1,3}\b'
    confidence: 0.95
    examples:
      - "APT29"
      - "APT-33"
      - "APT 28"

  TECHNIQUE:
    pattern: '\bT\d{4}(?:\.\d{3})?\b'
    confidence: 1.0
    examples:
      - "T1566"
      - "T1566.001"

  TACTIC:
    pattern: '\bTA\d{4}\b'
    confidence: 1.0
    examples:
      - "TA0001"
      - "TA0010"

  MITRE_EM3D:
    pattern: '\bTID-\d{3,4}\b|\bMIT-\d{3,4}\b'
    confidence: 1.0
    examples:
      - "TID-001"
      - "MIT-001"
```

---

## 10. Versioning and Deprecation

### 10.1 Version History

| Version | Status | Release Date | Notes |
|---------|--------|--------------|-------|
| ner11_v3 | PRODUCTION | 2025-11 | Gold Standard - Current |
| ner11_v2 | DEPRECATED | 2025-10 | Archived to backup |
| ner11_v1 | DEPRECATED | 2025-09 | Archived to backup |
| ner_v9 | DEPRECATED | 2025-08 | Archived to backup |
| ner_v8_mitre | DEPRECATED | 2025-07 | Archived to backup |

### 10.2 Deprecation Policy

```yaml
deprecation_policy:
  notification_period: "30 days"
  archive_location: "D:/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups"

  deprecated_models:
    - model: "ner11_v1"
      deprecated_date: "2025-11-01"
      removal_date: "2025-12-01"
      reason: "Superseded by ner11_v3"

    - model: "ner11_v2"
      deprecated_date: "2025-11-01"
      removal_date: "2025-12-01"
      reason: "Superseded by ner11_v3"

    - model: "ner_v9"
      deprecated_date: "2025-11-01"
      removal_date: "2025-12-01"
      reason: "Legacy model, not production quality"

    - model: "ner_v8_mitre"
      deprecated_date: "2025-11-01"
      removal_date: "2025-12-01"
      reason: "Legacy model, not production quality"
```

---

## 11. Related Documentation

| Document | Path | Description |
|----------|------|-------------|
| Architecture | `01_ARCHITECTURE/08_NER11_GOLD_MODEL_ARCHITECTURE_v1.0_2025-12-03.md` | System architecture |
| Procedures | `13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md` | Operational procedures |
| Data Flow | `01_ARCHITECTURE/07_DATA_FLOW_ARCHITECTURE_v4.0_2025-12-02.md` | Data flow architecture |
| Neo4j Schema | `03_SPECIFICATIONS/08_NEO4J_SECURITY_TAXONOMY_SCHEMA_v4.0_2025-12-02.md` | Graph database schema |
| Hierarchical Integration | `03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md` | Hierarchical taxonomy |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-12-03 | Initial comprehensive specification |

---

**Document End**
