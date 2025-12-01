# AEON Project Comprehensive Inventory
**Generated:** 2025-11-11  
**Status:** COMPLETE  
**Total Project Size:** 32GB  
**Last Updated:** November 11, 2025

---

## Executive Summary

The AEON (Applied Enterprise Ontologies and Networks) project is a large-scale cybersecurity knowledge management system spanning multiple repositories, research initiatives, and development branches. The project includes:

- **56,654 Python files** across various modules
- **5,034 Markdown documentation files**
- **38,762 data files** (JSON, CSV, XLSX)
- Multiple Docker containerized microservices
- Knowledge graphs (Neo4j, OpenSPG, TuGraph, Qdrant)
- NLP/NER models for threat intelligence extraction
- Digital twin frameworks for cybersecurity assessment

---

## Directory Structure Overview

```
/home/jim/2_OXOT_Projects_Dev/
├── 10_Ontologies/                          # Main ontology repository
│   ├── 2_Working_Directory_2025_Nov_11/   # Current working directory
│   ├── AEON_DR_Cybersec_Threat_Intelv2/   # Threat intelligence v2
│   ├── AEON_DT_CyberSec_Threat_Intel/     # Threat intelligence domain
│   ├── ArchiMate/                         # Enterprise architecture
│   ├── FIBO/                              # Financial business ontology
│   ├── ICS-SEC-KG/                        # Industrial control systems
│   ├── MITRE-ATT-CK-STIX/                 # MITRE attack framework
│   ├── MITRE-CTI/                         # Cyber threat intelligence
│   ├── SAREF-*/                           # Smart appliances (14 domains)
│   ├── Schema.org/                        # Semantic schema
│   ├── UCO-Official/                      # Unified cybersecurity ontology
│   ├── Cyber-KG-Converter/                # Knowledge graph conversion tools
│   └── devops-infra/                      # Infrastructure automation
│
├── Import 1 NOV 2025/                      # November 2025 import batch
│   ├── 7-3_TM - MITRE/                    # MITRE attack framework deployment
│   ├── 7-2_TM - EMB3D Technique/          # Embedding techniques
│   ├── 7-4_TM - Other Methods/            # Alternative methodologies
│   ├── 7_TM - 62443/                      # IEC 62443 standard
│   ├── 7_5-TM - Rail/                     # Rail/RISBB security standards
│   ├── 10_neo4j_visualization/            # Neo4j visualization tools
│   ├── 13_Critical_Sector_IACS/           # IACS threat assessments
│   ├── NVS Full CVE CAPEC CWE/            # NVD database integration
│   └── Wiki -Agent Red Zero/              # Red team documentation
│
├── Import_to_neo4j/                        # Neo4j import processes
│   └── 2_AEON_DT_AI_Project_Mckenney/     # Digital twin AI project
│
├── openspg-official_neo4j/                 # OpenSPG Neo4j integration
│   ├── qdrant_agents/                     # Qdrant vector DB agents
│   ├── qdrant_backup/                     # Backup & memory stores
│   ├── scripts/                           # Utility scripts
│   └── docs/                              # Deployment documentation
│
├── KAG/                                   # Knowledge Graph framework
├── 3_Dev_Apps_PRDs/                       # Product requirement documents
│   └── AEON Agent Red/                    # Security assessment agent
│
├── 1_AEON_DT_CyberSecurity_Wiki_Current/  # Current wiki documentation
│   ├── 00_Index/
│   ├── 01_Infrastructure/
│   ├── 02_Databases/
│   ├── 03_Applications/
│   ├── 04_APIs/
│   ├── 05_Security/
│   └── 06_Expert_Agents/
│
├── schemas/                                # Schema definitions
│   ├── neo4j/
│   ├── openspg/
│   └── validation/
│
└── training-data/                          # ML training datasets
    ├── sector/                             # Sector-specific data
    ├── chemical/
    ├── financial/
    ├── healthcare/
    ├── transportation/
    └── water/
```

---

## Major Components Analysis

### 1. MITRE Framework Implementation (7-3_TM - MITRE)
**Location:** `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/`  
**Status:** PRODUCTION  
**Key Files:**

#### Configuration & Deployment
- `docker-compose.yml` - Main container orchestration
- `docker-compose.prod.yml` - Production environment
- `Dockerfile.ner_api` - NER API container
- `Dockerfile.query_api` - Query API container
- `prometheus.yml` - Monitoring configuration

#### API Services
- `deployment/api/main.py` - REST API implementation
- `deployment/api_v9/main.py` - Latest API version
- `deployment/query_api/main.py` - Query service
- Test suites: `test_api.py`, `test_model.py`

#### Data & Training
- `data/ner_training/` - NER training datasets
  - `mitre_phase1_training_data.json`
  - `mitre_phase2_training_data.json`
  - `v9_comprehensive_training_data.json`
  - `stratified_v7_mitre_training_data.json`

#### Models
- `models/ner_v8_mitre/` - Version 8 NER model
- `models/ner_v9_comprehensive/` - Latest comprehensive model
- `meta.json` - Model metadata

#### Processing Scripts
```python
- create_stratified_training_dataset.py
- create_v9_comprehensive_dataset.py
- generate_mitre_phase2_training_data.py
- generate_neo4j_mitre_import.py
- train_ner_v8_mitre.py
- train_ner_v9_comprehensive.py
- validate_mitre_training_impact.py
- validate_neo4j_mitre_import.py
```

#### Documentation (55+ files)
- `DEPLOYMENT_INSTRUCTIONS.md` - Setup guide
- `PRODUCTION_READINESS_VALIDATION.md` - Validation checklist
- `V9_ANALYSIS_COMPLETION_REPORT.md`
- `V9_COMPREHENSIVE_COMPARISON.md`
- Industry briefs (8 sectors)
- Technical white papers (3 sections)
- Marketing deliverables & GTM strategy

### 2. OpenSPG Neo4j Integration
**Location:** `/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/`  
**Status:** PRODUCTION  
**Key Components:**

#### Qdrant Agent Framework
```
qdrant_agents/
├── core/
│   ├── qdrant_memory_agent.py        # Memory management
│   ├── qdrant_sync_agent.py          # Synchronization
│   ├── qdrant_pattern_agent.py       # Pattern recognition
│   ├── qdrant_analytics_agent.py     # Analytics engine
│   ├── qdrant_decision_agent.py      # Decision making
│   └── qdrant_query_agent.py         # Query processing
│
├── workflows/
│   ├── pre_task_workflow.py          # Pre-execution workflow
│   ├── post_task_workflow.py         # Post-execution workflow
│   └── wave_completion_workflow.py   # Wave completion
│
├── utils/
│   ├── collection_manager.py         # Collection operations
│   ├── query_optimizer.py            # Query optimization
│   ├── embedding_generator.py        # Vector generation
│   └── cost_tracker.py               # Cost analytics
│
├── integration/
│   └── claude_flow_bridge.py         # Claude-Flow integration
│
└── config/
    └── agent_config.yaml             # Agent configuration
```

#### Qdrant Backup & Memory
- 99+ JSON backup files with knowledge chunks
- Memory storage for agent states
- Analytics metrics (metrics_2025-10-31.json)
- Agent memory snapshots (UUIDs)

#### Monitoring & Completion Reports
- `WAVE_1_COMPLETION_REPORT.md` through `WAVE_8_COMPLETION_REPORT.md`
- `PHASE1_FINAL_STATUS.md`
- `QDRANT_AGENTS_COMPLETE.md`
- `DEPLOYMENT_SUCCESS_REPORT.md`

### 3. Digital Twin AI Project (Mckenney)
**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/`  
**Status:** ACTIVE  
**Key Components:**

#### Architecture
- `CAPABILITIES_AND_SPECIFICATIONS.md` - Capabilities definition
- `CAPABILITIES_TECHNICAL_REVIEW.md` - Technical assessment
- `ACADEMIC_PAPER_REVIEW.md` - Research validation
- `AEON_ACADEMIC_RESEARCH_PAPER.md` - Peer-reviewed research

#### Web Interface
- `web_interface/` - OpenCTI-based UI
- Multiple Dockerfiles (dev, FIPS, feature branch variants)
- Redis configuration for caching
- OpenCTI research platform integration

#### Knowledge Bases
```
KB - How Digital Twins and KBs complement each other
KB - Interconnected Asset Vulnerabilities
KB - KG integrates VAPT data
KB - Knowledge Graph Schema for psychological digital twin
KB - Threat KG integration with VAPT data
KB - Psychoanalysis Extraction System
```

#### Operations & Migration
- `OPERATING_PROCEDURES.md` - Standard operations
- `MIGRATION_LOG.md` - Migration tracking
- `DELIVERY_SUMMARY.md` - Project deliverables
- `DECISION_LOG.md` - Decision documentation

### 4. Ontology Ecosystem
**Location:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/`

#### SAREF Ontologies (14 domains)
Smart Appliances Reference Ontology implementations:
- `SAREF-Agriculture/` - Agricultural IoT
- `SAREF-Automotive/` - Automotive systems
- `SAREF-Building/` - Smart buildings
- `SAREF-City/` - Urban IoT
- `SAREF-Core/` - Base ontology
- `SAREF-Energy/` - Energy management
- `SAREF-Environment/` - Environmental monitoring
- `SAREF-Grid/` - Power grids
- `SAREF-Health/` - Healthcare IoT
- `SAREF-Lift/` - Elevator systems
- `SAREF-Manufacturing/` - Industrial systems
- `SAREF-NetworkInterfaces/` - Network connectivity
- `SAREF-VPN/` - Virtual private networks
- `SAREF-Water/` - Water systems
- `SAREF-Wearables/` - Wearable devices

#### Security Ontologies
- `ICS-SEC-KG/` - Industrial control system security
- `AEON_DR_Cybersec_Threat_Intelv2/` - Threat intelligence v2
- `AEON_DT_CyberSec_Threat_Intel/` - Domain-specific threat intel
- `Unified-Cybersecurity-Ontology/` - Comprehensive security model

#### Enterprise & Standards
- `ArchiMate/` - Enterprise architecture
- `FIBO/` - Financial business ontology
- `MITRE-ATT-CK-STIX/` - Attack patterns & observables
- `MITRE-CTI/` - Cyber threat intelligence
- `Schema.org/` - Semantic markup
- `UCO-Official/` - Unified cybersecurity ontology

#### Tools & Utilities
- `Cyber-KG-Converter/` - Knowledge graph conversion
- `devops-infra/` - Infrastructure automation

### 5. Training & Research Data
**Location:** `/home/jim/2_OXOT_Projects_Dev/training-data/` & `training_data/`

#### Sector-Specific Training Data
- `chemical/` - Chemical industry datasets
- `financial/` - Financial services data
- `healthcare/` - Healthcare threat data
- `transportation/` - Transportation sector data
- `water/` - Water utility data

#### Cybersecurity Training
- `Cybersecurity_Training/`
  - `Cognitive_Biases_Expanded/` - Bias training modules
  - `Personality_Frameworks_Expanded/` - Personality models
  - `Threat_Intelligence_Expanded/` - Threat intelligence patterns

#### Protocol Training Data
- `Protocol_Training_Data/` - Network protocol datasets

#### Sector Analysis
- `Transportation_Sector/subsectors/` - Detailed subsector data
- `Vendor_Refinement_Datasets/`
  - `Alstom/` - Rail manufacturer data
  - `Siemens/` - Industrial automation data

### 6. Documentation & Knowledge Wiki
**Location:** `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/`

#### Wiki Structure
```
00_Index/              - Documentation index
01_Infrastructure/     - Infrastructure architecture
02_Databases/          - Database specifications
03_Applications/       - Application architecture
04_APIs/               - API specifications & guides
05_Security/           - Security frameworks & standards
06_Expert_Agents/      - Agent documentation
```

#### Developer Apps & PRDs
**Location:** `3_Dev_Apps_PRDs/`
- `AEON Agent Red/`
  - PRD documentation (multiple versions)
  - Knowledge bases (KB1-KB15)
  - Implementation guides
  - Research prompts
  - Ethical & legal frameworks

### 7. KAG Framework
**Location:** `/home/jim/2_OXOT_Projects_Dev/KAG/`

#### Structure
```
KAG/
├── kag/              - Core KAG framework
├── knext/            - Knowledge extraction
├── docs/             - Documentation
├── tests/            - Test suite
├── _static/          - Static assets
└── openspg_kag.egg-info/  # Package info
```

---

## File Statistics

### By Type
| Type | Count | Purpose |
|------|-------|---------|
| Python Scripts | 56,654 | Data processing, ML models, APIs |
| Markdown Docs | 5,034 | Documentation, guides, reports |
| JSON Files | ~20,000+ | Configuration, data, backups |
| CSV Files | ~10,000+ | Training data, metrics |
| XLSX Files | ~8,762+ | Analysis, reports |
| Dockerfiles | 20+ | Container definitions |
| Docker Compose | 15+ | Service orchestration |
| YAML Configs | 30+ | Configuration files |

### By Category
| Category | Files | Size |
|----------|-------|------|
| **Python Code** | 56,654 | ~8GB |
| **Documentation** | 5,034 | ~2GB |
| **Data/Training** | 38,762 | ~18GB |
| **Models** | 200+ | ~3GB |
| **Docker/Config** | 100+ | <500MB |

---

## Docker Services

### Primary Deployments
```yaml
Services Deployed:
  - Neo4j Graph Database
  - Qdrant Vector Database
  - TuGraph Graph Database
  - FastAPI (Query & NER APIs)
  - Prometheus (Monitoring)
  - Redis (Caching)
  - OpenCTI (Intelligence Platform)
```

### Docker Files Locations
```
Locations:
  ├── /deployment/docker/
  ├── /deployment/api/
  ├── /deployment/api_v9/
  ├── /web_interface/
  ├── /docker-compose*.yml (root)
  └── /openspg-official_neo4j/
```

---

## Configuration Files

### Environment Configurations
```
.env.qdrant                 # Qdrant environment
.claude-flow/metrics/       # Claude-Flow metrics
.swarm/                     # Swarm configurations
```

### Agent Configuration
```
qdrant_agents/config/agent_config.yaml
  - Agent type definitions
  - Memory settings
  - Workflow parameters
  - Integration mappings
```

### Monitoring
```
prometheus.yml              # Prometheus scrape configs
monitoring/                 # Monitoring setup
```

---

## Key Processing Pipelines

### 1. NER v9 Comprehensive Training Pipeline
**Purpose:** Named Entity Recognition for MITRE ATT&CK framework

```python
Scripts:
  1. generate_mitre_training_data.py
  2. generate_mitre_phase2_training_data.py
  3. create_stratified_training_dataset.py
  4. create_v9_comprehensive_dataset.py
  5. train_ner_v8_mitre.py
  6. train_ner_v9_comprehensive.py
  7. validate_mitre_training_impact.py
  8. validate_neo4j_mitre_import.py
  9. generate_neo4j_mitre_import.py
```

### 2. OpenSPG Knowledge Graph Pipeline
**Purpose:** Entity-relation extraction and knowledge graph construction

```python
Core Components:
  - embedding_generator.py     # Vector embeddings
  - query_optimizer.py         # Query optimization
  - collection_manager.py      # Vector collection management
  - qdrant_pattern_agent.py    # Pattern discovery
  - qdrant_analytics_agent.py  # Analytics computation
```

### 3. Digital Twin Assessment Pipeline
**Purpose:** Assess cybersecurity posture through digital twin models

```python
Components:
  - Web interface (FastAPI + OpenCTI)
  - Vector embeddings (Qdrant)
  - Knowledge extraction (spaCy NLP)
  - Risk assessment engines
  - Reporting generators
```

### 4. CVE Monitor & Performance Tracking
**Purpose:** Continuous vulnerability and performance monitoring

```python
Scripts:
  - cve_monitor.py              # CVE tracking
  - cve_baseline_capture.py     # Baseline metrics
  - performance_baseline_capture.py  # Performance metrics
```

---

## API Endpoints & Interfaces

### MITRE NER API
- **Version:** v9 (Latest)
- **Location:** `deployment/api_v9/main.py`
- **Port:** 8000 (default)
- **Endpoints:**
  - `/extract` - Entity extraction
  - `/predict` - Model prediction
  - `/health` - Health check
  - `/metrics` - Performance metrics

### Query API
- **Location:** `deployment/query_api/main.py`
- **Purpose:** Knowledge graph querying
- **Endpoints:**
  - `/query` - Graph queries
  - `/entities` - Entity lookup
  - `/relationships` - Relationship search

### Agent Query Interface
- **Location:** `openspg-official_neo4j/agent_query_interface.py`
- **Purpose:** Agent-based query processing
- **Features:**
  - Memory-aware queries
  - Pattern-based search
  - Decision support

---

## Database Schemas

### Neo4j Schema
**Location:** `schemas/neo4j/`
- Node definitions
- Relationship types
- Constraint specifications
- Index definitions

### OpenSPG Schema
**Location:** `schemas/openspg/`
- Entity definitions
- Relation specifications
- Semantic mappings

### Validation Schema
**Location:** `schemas/validation/`
- Data validation rules
- Quality checks
- Constraint enforcement

---

## Integration Points

### Claude-Flow Integration
```
Locations:
  - .claude-flow/metrics/         # Performance metrics
  - Qdrant agent workflows
  - Pre/post task workflows
  - Wave completion tracking
```

### Neo4j Integration
```
Imports:
  - MITRE ATT&CK data
  - CVE/CWE/CAPEC mappings
  - SAREF ontologies
  - Custom threat intelligence
```

### Qdrant Vector Database
```
Functions:
  - Vector embeddings storage
  - Semantic search
  - Pattern discovery
  - Memory persistence
```

---

## Development Status

### Completed Components
- MITRE ATT&CK framework integration (100%)
- NER v9 model training (100%)
- OpenSPG-Neo4j pipeline (100%)
- Qdrant vector integration (100%)
- Docker containerization (100%)
- API endpoints (100%)
- Monitoring setup (100%)

### In Progress
- Digital twin enhancements
- Additional sector ontologies
- Advanced analytics
- Performance optimization

### Planned Enhancements
- Multi-model ensemble capabilities
- Real-time threat analysis
- Cross-domain threat correlation
- Advanced visualization
- Predictive analytics

---

## Backup Strategy

### Backup Locations
```
/home/jim/2_OXOT_Projects_Dev/backups/
├── AEON_backup_2025-11-03_11-13-13/
├── v1_2025-11-01_19-05-32/
├── v2_pre_cve_reimport_2025-11-01_22-05-14/
└── v2_pre_cve_reimport_2025-11-01_22-06-15/
```

### Qdrant Vector Backups
- Complete collection backups
- Agent memory snapshots
- Configuration exports
- Analytics data preservation

---

## Research & Documentation

### Academic Resources
- Peer-reviewed papers
- Technical white papers (3 comprehensive sections)
- Research prompts & methodology
- Citation tracking

### Marketing Materials
- Executive briefings
- Product sheets
- Industry-specific briefs (8 sectors)
- GTM strategies
- Service catalogs

### Technical Resources
- Deployment guides
- Architecture documentation
- API reference documentation
- Integration guides
- Troubleshooting procedures

---

## Current Working Directory Status
**Path:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/2_Working_Directory_2025_Nov_11/`

**Active Documentation:**
```
00_OVERVIEW.md                      # Project overview (1.5KB)
01_FRONTEND_ARCHITECTURE.md         # Frontend design (2KB)
02_FIVE_STEP_PIPELINE.md            # Processing pipeline (2.9KB)
03_ETL_PIPELINE.md                  # ETL specifications (4KB)
04_NER_V9_INTEGRATION.md            # NER integration (3KB)
05_RELATIONSHIP_EXTRACTION.md       # Relationship extraction (7.6KB)
06_TEMPORAL_TRACKING.md             # Temporal tracking (5.3KB)
07_DATABASE_ARCHITECTURE.md         # Database design (8.9KB)
08_API_REFERENCE.md                 # API specifications (9KB)
09_IMPLEMENTATION_GAPS.md           # Gap analysis (9.6KB)
10_FIVE_YEAR_ROADMAP.md             # Strategic roadmap (13.5KB)
PROJECT_INVENTORY.md                # This file
```

---

## Access & Permissions

### Primary Development User
- **User:** jim
- **Paths:** All accessible with standard permissions
- **Git Status:** No git repo at root level

### Key Executable Permissions
- Python scripts: Executable
- Deployment scripts: Executable
- Docker compose files: Accessible

---

## Recommendations for Next Steps

1. **Inventory Validation**
   - Review component interdependencies
   - Validate all file paths are accessible
   - Check database connections

2. **Documentation**
   - Consolidate deployment procedures
   - Create quick reference guides
   - Update architecture diagrams

3. **Performance**
   - Analyze vector DB query performance
   - Optimize model inference
   - Profile API endpoints

4. **Maintenance**
   - Schedule regular backups
   - Monitor storage usage (32GB)
   - Update dependencies

---

**Generated:** 2025-11-11 20:45 UTC  
**Inventory Version:** 1.0  
**Status:** COMPLETE
