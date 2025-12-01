# System Architecture Overview

**Created:** 2025-10-29
**Purpose:** Comprehensive architecture documentation for AEON DT CyberSec Threat Intelligence system

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph Source["External Data Sources"]
        NVD["NIST NVD API"]
        MITRE["MITRE ATT&CK API"]
        CISA["CISA Advisories"]
        Custom["Custom Documents<br/>PDF, DOCX, TXT"]
    end

    subgraph DataPipeline["Data Processing Pipeline"]
        Parser["Document Parser<br/>PDF, Word, Text"]
        EntityExt["Entity Extractor<br/>spaCy NLP"]
        RelationExt["Relationship Extractor<br/>Pattern Matching"]
        Validator["Validator<br/>Schema Check"]
    end

    subgraph Neo4j["Neo4j Cluster"]
        Primary["Primary<br/>Write Node"]
        Replica1["Replica 1<br/>Read Node"]
        Replica2["Replica 2<br/>Read Node"]
        Replica3["Replica 3<br/>Read Node"]
    end

    subgraph QueryLayer["Query & Analytics Layer"]
        CypherAPI["Cypher Query API<br/>REST Interface"]
        Analytics["Analytics Engine<br/>Graph Algorithms"]
        Cache["Query Cache<br/>Redis"]
    end

    subgraph Applications["Applications & Dashboards"]
        Dashboard["Risk Dashboard<br/>D3.js Visualization"]
        Reports["Report Generator<br/>PDF/HTML"]
        AlertSystem["Alert System<br/>Real-time Notifications"]
        API["REST API<br/>External Integration"]
    end

    subgraph External["External Systems"]
        CMDB["Configuration<br/>Management DB"]
        SIEM["SIEM System<br/>Splunk/ELK"]
        ThreatFeed["Threat Intel<br/>Feeds"]
    end

    %% Connections
    NVD -->|CVE Data| DataPipeline
    MITRE -->|ATT&CK Data| DataPipeline
    CISA -->|Advisories| DataPipeline
    Custom -->|Documents| DataPipeline

    Parser -->|Structured Text| EntityExt
    EntityExt -->|Entities| RelationExt
    RelationExt -->|Relationships| Validator
    Validator -->|Clean Data| Neo4j

    Primary <-->|Replication| Replica1
    Primary <-->|Replication| Replica2
    Primary <-->|Replication| Replica3

    Neo4j -->|Graph Data| QueryLayer
    QueryLayer -->|Results| Applications
    Cache -->|Cached Queries| QueryLayer

    Dashboard -->|Visualizations| Applications
    Reports -->|Generated Reports| Applications
    AlertSystem -->|Alerts| Applications
    API -->|Data Access| Applications

    CMDB -.->|Asset Data| Dashboard
    SIEM -.->|Security Events| Dashboard
    ThreatFeed -.->|IOCs| Dashboard

    style Source fill:#F8F9FA,stroke:#333
    style DataPipeline fill:#E8F5E9,stroke:#333
    style Neo4j fill:#E3F2FD,stroke:#333
    style QueryLayer fill:#FFF3E0,stroke:#333
    style Applications fill:#F3E5F5,stroke:#333
    style External fill:#FCE4EC,stroke:#333
```

## 2. Data Flow Architecture

```mermaid
sequenceDiagram
    actor Source as Data Sources<br/>NVD/MITRE/Custom
    participant Parser as Document Parser
    participant NLP as NLP Engine
    participant Relation as Relation Extractor
    participant Validation as Schema Validator
    participant Neo4j as Neo4j Database
    participant Query as Query API
    participant Dashboard as Dashboard/Reports

    Source->>Parser: Raw documents/APIs
    activate Parser
    Parser->>Parser: Extract text, metadata, structure
    Parser->>NLP: Structured content
    deactivate Parser

    activate NLP
    NLP->>NLP: Named Entity Recognition
    NLP->>NLP: Confidence scoring
    NLP->>Relation: Identified entities
    deactivate NLP

    activate Relation
    Relation->>Relation: Dependency parsing
    Relation->>Relation: Pattern matching
    Relation->>Relation: Co-occurrence analysis
    Relation->>Validation: Entity-relationship pairs
    deactivate Relation

    activate Validation
    Validation->>Validation: Schema compliance check
    Validation->>Validation: Reference integrity
    Validation->>Validation: Deduplication
    Validation->>Neo4j: Valid graph data
    deactivate Validation

    activate Neo4j
    Neo4j->>Neo4j: Create/update nodes
    Neo4j->>Neo4j: Create relationships
    Neo4j->>Neo4j: Replicate to read nodes
    deactivate Neo4j

    Query->>Neo4j: Cypher queries
    Neo4j->>Query: Query results
    Query->>Dashboard: Enriched results
    Dashboard->>Dashboard: Visualize & analyze
```

## 3. Neo4j Cluster Architecture

```mermaid
graph TB
    subgraph Cluster["Neo4j Cluster"]
        Primary["PRIMARY<br/>bolt://localhost:7687<br/>Write Operations<br/>Transaction Leader"]

        Read1["READ REPLICA 1<br/>bolt://replica1:7687<br/>Read-Only<br/>High Availability"]

        Read2["READ REPLICA 2<br/>bolt://replica2:7687<br/>Read-Only<br/>Load Balancing"]

        Read3["READ REPLICA 3<br/>bolt://replica3:7687<br/>Read-Only<br/>Backup"]
    end

    subgraph LB["Load Balancing"]
        Router["Neo4j Router<br/>Connection Pooling<br/>Automatic Failover"]
    end

    subgraph Backup["Backup & Recovery"]
        BackupStore["Backup Storage<br/>Daily snapshots<br/>Point-in-time recovery"]
    end

    Primary -->|Continuous Replication| Read1
    Primary -->|Continuous Replication| Read2
    Primary -->|Continuous Replication| Read3

    Router -->|Route Writes| Primary
    Router -->|Route Reads| Read1
    Router -->|Route Reads| Read2
    Router -->|Route Reads| Read3

    Primary -->|Backup Stream| BackupStore

    Read1 -.->|Replica Sync| Primary
    Read2 -.->|Replica Sync| Primary
    Read3 -.->|Replica Sync| Primary

    style Primary fill:#4A90E2,stroke:#2E5C8A,color:#fff,stroke-width:3px
    style Read1 fill:#50C878,stroke:#2E7D4E,color:#fff
    style Read2 fill:#50C878,stroke:#2E7D4E,color:#fff
    style Read3 fill:#50C878,stroke:#2E7D4E,color:#fff
    style Router fill:#F39C12,stroke:#985F0D,color:#fff
    style BackupStore fill:#E74C3C,stroke:#8B2E1F,color:#fff
```

## 4. Data Processing Pipeline

```mermaid
graph LR
    subgraph Input["Input Sources"]
        Files["Document Files<br/>PDF, DOCX, TXT"]
        APIs["API Feeds<br/>NVD, MITRE, CISA"]
        Streams["Live Streams<br/>Syslog, SNMP"]
    end

    subgraph Extract["Extraction Layer"]
        DocParse["PDF/DOCX Parser"]
        TextExt["Text Extraction"]
        MetaExt["Metadata Extraction"]
    end

    subgraph EnrichNLP["NLP Enrichment"]
        Tokenize["Tokenization"]
        NER["Named Entity<br/>Recognition"]
        DependencyParse["Dependency<br/>Parsing"]
    end

    subgraph Relations["Relationship Layer"]
        PatternMatch["Pattern Matching"]
        CoOccur["Co-occurrence<br/>Analysis"]
        Suggest["Relationship<br/>Suggestion"]
    end

    subgraph Quality["Quality Assurance"]
        Dedup["Deduplication"]
        Normalize["Normalization"]
        Validate["Schema<br/>Validation"]
    end

    subgraph Storage["Storage Layer"]
        GraphDB["Neo4j<br/>Property Graph"]
        Cache["Redis Cache"]
        Archive["Document Archive"]
    end

    Files -->|Input| Input
    APIs -->|Input| Input
    Streams -->|Input| Input

    Input -->|Feed| Extract
    DocParse -->|Parsed Text| Extract
    TextExt -->|Content| Extract
    MetaExt -->|Properties| Extract

    Extract -->|Text| EnrichNLP
    Tokenize -->|Tokens| EnrichNLP
    NER -->|Entities| EnrichNLP
    DependencyParse -->|Dependencies| EnrichNLP

    EnrichNLP -->|Entities| Relations
    PatternMatch -->|Relationships| Relations
    CoOccur -->|Co-occurrences| Relations
    Suggest -->|Suggestions| Relations

    Relations -->|Data| Quality
    Dedup -->|Deduplicated| Quality
    Normalize -->|Normalized| Quality
    Validate -->|Validated| Quality

    Quality -->|Graph Data| Storage
    GraphDB -->|Indexed| Storage
    Cache -->|Cached| Storage
    Archive -->|Archived| Storage

    style Input fill:#FCE4EC,stroke:#333
    style Extract fill:#E8F5E9,stroke:#333
    style EnrichNLP fill:#E3F2FD,stroke:#333
    style Relations fill:#FFF3E0,stroke:#333
    style Quality fill:#F3E5F5,stroke:#333
    style Storage fill:#E0F2F1,stroke:#333
```

## 5. Integration Architecture

```mermaid
graph TB
    subgraph ThreatIntel["Threat Intelligence Core"]
        Graph["Knowledge Graph<br/>Neo4j"]
        Query["Query Engine<br/>Cypher"]
        Algo["Graph Algorithms<br/>Pathfinding, Ranking"]
    end

    subgraph CMDB["Configuration Management"]
        Assets["Asset Registry<br/>Servers, Software, Config"]
        Relationships["Asset Relationships<br/>Dependencies"]
        Changes["Change History<br/>Audit Trail"]
    end

    subgraph SIEM["Security Information Event Management"]
        Events["Security Events<br/>Logs, Alerts"]
        Correlation["Event Correlation<br/>Detection"]
        Incident["Incident Management<br/>Ticketing"]
    end

    subgraph ExternalTI["External Threat Intelligence"]
        Feeds["Threat Feeds<br/>IOCs, Indicators"]
        APIs["Threat APIs<br/>Reputation, Attribution"]
        Advisories["Public Advisories<br/>CVEs, CISAs"]
    end

    subgraph Analysis["Analysis & Response"]
        RiskScore["Risk Scoring<br/>Multi-factor"]
        Impact["Impact Analysis<br/>Blast Radius"]
        Remediation["Remediation<br/>Planning"]
    end

    subgraph Reporting["Reporting & Dashboards"]
        Dashboard["Executive Dashboard<br/>Risk Overview"]
        Reports["Detailed Reports<br/>PDF/HTML"]
        Metrics["KPIs & Metrics<br/>Trending"]
    end

    %% Internal connections
    Graph <-->|Stores & Queries| Query
    Query -->|Executes| Algo

    %% CMDB Integration
    CMDB -->|Asset Data| Graph
    Graph -->|Enriches| CMDB
    Assets -->|Sources| Relationships

    %% SIEM Integration
    SIEM -->|Raw Events| Correlation
    Correlation -->|Correlated Events| Graph
    Incident -->|Tracks| Incident

    %% External TI Integration
    Feeds -->|IOCs| Graph
    APIs -->|Reputation Data| Graph
    Advisories -->|CVE Data| Graph

    %% Analysis
    Graph -->|Threat Data| Analysis
    Algo -->|Ranking| RiskScore
    Query -->|Impact Queries| Impact

    %% Reporting
    RiskScore -->|Scores| Reporting
    Impact -->|Results| Reporting
    Remediation -->|Actions| Reporting

    style ThreatIntel fill:#E3F2FD,stroke:#333,stroke-width:2px
    style CMDB fill:#E8F5E9,stroke:#333,stroke-width:2px
    style SIEM fill:#FFF3E0,stroke:#333,stroke-width:2px
    style ExternalTI fill:#F3E5F5,stroke:#333,stroke-width:2px
    style Analysis fill:#FCE4EC,stroke:#333,stroke-width:2px
    style Reporting fill:#E0F2F1,stroke:#333,stroke-width:2px
```

## 6. Deployment Architecture

```mermaid
graph TB
    subgraph K8s["Kubernetes Cluster"]
        subgraph NS1["threat-intelligence namespace"]
            Neo4jPod["Neo4j Primary Pod<br/>4 CPU, 8GB RAM<br/>100GB Storage"]
            ReplicaPods["Replica Pods x3<br/>2 CPU, 4GB RAM each<br/>50GB Storage each"]
            ParserPod["Parser Pod<br/>2 CPU, 4GB RAM<br/>10GB Temp"]
            NLPPod["NLP Pod<br/>4 CPU, 8GB RAM<br/>20GB Models"]
            APIPod["API Pod<br/>2 CPU, 2GB RAM<br/>Auto-scaled 1-3"]
        end

        subgraph NS2["monitoring namespace"]
            Prometheus["Prometheus<br/>Metrics Collection"]
            Grafana["Grafana<br/>Visualization"]
            ELK["ELK Stack<br/>Logging"]
        end

        subgraph Ingress["Ingress & Load Balancing"]
            LB["Load Balancer<br/>Layer 4 TCP"]
            Ingress["Nginx Ingress<br/>Layer 7 HTTP"]
        end
    end

    subgraph Storage["Persistent Storage"]
        PVC1["PVC: Neo4j Data<br/>100GB SSD"]
        PVC2["PVC: Archives<br/>500GB HDD"]
        PVC3["PVC: Backups<br/>1TB Archive"]
    end

    subgraph Cache["Caching Layer"]
        Redis["Redis Cache<br/>32GB<br/>Query Results"]
    end

    %% Pod connections
    Neo4jPod -->|Replicate| ReplicaPods
    ParserPod -->|Process| NLPPod
    NLPPod -->|Push Data| Neo4jPod
    APIPod -->|Query| Neo4jPod
    APIPod -->|Cache| Redis

    %% Storage
    Neo4jPod -->|Mount| PVC1
    NLPPod -->|Write| PVC2
    Neo4jPod -->|Backup| PVC3

    %% Monitoring
    Neo4jPod -->|Metrics| Prometheus
    ReplicaPods -->|Metrics| Prometheus
    APIPod -->|Metrics| Prometheus
    Prometheus -->|Dashboard| Grafana

    %% Logging
    Neo4jPod -->|Logs| ELK
    APIPod -->|Logs| ELK
    ParserPod -->|Logs| ELK

    %% Ingress
    LB -->|External| Ingress
    Ingress -->|Route| APIPod
    Ingress -->|Route| Grafana

    style K8s fill:#F5F5F5,stroke:#333,stroke-width:2px
    style NS1 fill:#E3F2FD,stroke:#333
    style NS2 fill:#E8F5E9,stroke:#333
    style Ingress fill:#FFF3E0,stroke:#333
    style Storage fill:#FCE4EC,stroke:#333
    style Cache fill:#E0F2F1,stroke:#333
```

## 7. Document Processing Workflow

```mermaid
graph TD
    subgraph Input["Input Documents"]
        PDF["PDF Files"]
        DOCX["Word Documents"]
        TXT["Text Files"]
        MD["Markdown Files"]
    end

    subgraph Processing["Processing Stage"]
        Ingest["Document Ingestion"]
        Extract["Content Extraction"]
        Clean["Text Cleaning"]
        Chunk["Chunking<br/>Page/Section Level"]
    end

    subgraph NLPStage["NLP Processing"]
        Tokenize["Tokenization"]
        POS["POS Tagging"]
        NER["Entity Recognition"]
        Dep["Dependency Parsing"]
    end

    subgraph Extraction["Information Extraction"]
        EntityExt["Entity Extraction"]
        RelExt["Relationship Extraction"]
        PatternMatch["Pattern Matching"]
        IOCExt["IOC Extraction"]
    end

    subgraph Enrichment["Enrichment"]
        TypeNorm["Type Normalization<br/>CVE, CWE, CAPEC"]
        Linking["Entity Linking<br/>Deduplication"]
        Confidence["Confidence Scoring"]
        Graph["Graph Building<br/>Neo4j Ready"]
    end

    subgraph Integration["Neo4j Integration"]
        Import["Batch Import"]
        Index["Indexing"]
        Replicate["Replication"]
        Verify["Verification"]
    end

    PDF --> Ingest
    DOCX --> Ingest
    TXT --> Ingest
    MD --> Ingest

    Ingest --> Extract
    Extract --> Clean
    Clean --> Chunk

    Chunk --> Tokenize
    Tokenize --> POS
    POS --> NER
    NER --> Dep

    Dep --> EntityExt
    EntityExt --> RelExt
    RelExt --> PatternMatch
    PatternMatch --> IOCExt

    IOCExt --> TypeNorm
    TypeNorm --> Linking
    Linking --> Confidence
    Confidence --> Graph

    Graph --> Import
    Import --> Index
    Index --> Replicate
    Replicate --> Verify

    style Input fill:#FCE4EC,stroke:#333
    style Processing fill:#E8F5E9,stroke:#333
    style NLPStage fill:#E3F2FD,stroke:#333
    style Extraction fill:#FFF3E0,stroke:#333
    style Enrichment fill:#F3E5F5,stroke:#333
    style Integration fill:#E0F2F1,stroke:#333
```

## Key Architectural Principles

### 1. **Scalability**
- Horizontal scaling via Neo4j cluster read replicas
- Kubernetes auto-scaling for processing pods
- Redis caching for query optimization

### 2. **Reliability**
- Multi-node Neo4j cluster with automatic failover
- Point-in-time backup and recovery
- Health checks and monitoring

### 3. **Performance**
- Document chunking for context preservation
- Batch processing with parallel workers
- Query result caching with TTL

### 4. **Data Quality**
- Schema validation at ingestion
- Deduplication and normalization
- Confidence scoring for extracted entities

### 5. **Integration**
- RESTful API for external access
- CMDB integration for asset data
- SIEM integration for security events
- External threat feed integration

### 6. **Monitoring & Observability**
- Prometheus metrics collection
- Grafana visualization dashboards
- ELK stack for centralized logging
- Performance tracking and alerting

## Infrastructure Requirements

| Component | Resources | Storage | Network |
|-----------|-----------|---------|---------|
| Neo4j Primary | 4 CPU, 8GB RAM | 100GB SSD | Private |
| Read Replicas (x3) | 2 CPU, 4GB RAM | 50GB SSD | Private |
| Processing Pods | 2-4 CPU, 4-8GB RAM | 10-50GB Temp | Private |
| API Servers | 2 CPU, 2GB RAM | - | Public |
| Redis Cache | - | 32GB RAM | Private |
| Monitoring | 2 CPU, 4GB RAM | 50GB | Private |
| Backups | - | 1TB Archive | Offline |

## Security Considerations

1. **Network Isolation**: Neo4j cluster on private subnet
2. **Authentication**: Neo4j user/password authentication
3. **Encryption**: TLS for all external connections
4. **Access Control**: RBAC for Neo4j and Kubernetes
5. **Audit Logging**: All database operations logged
6. **Data Backup**: Encrypted backups with offsite replication
