# Cybersecurity Knowledge Base Architecture
**File:** Cybersecurity_KB_Architecture.md
**Created:** 2025-10-26
**Author:** System Architecture Designer
**Version:** 1.0.0
**Status:** ACTIVE

## Executive Summary

This document presents a comprehensive system architecture for a multi-tenant cybersecurity knowledge base platform designed for security consulting teams. The architecture leverages **OpenSPG with KAG (Knowledge Augmented Generation)** framework, **Neo4j Enterprise** for graph storage, and the **Unified Cybersecurity Ontology (UCO)** to deliver advanced threat analysis, risk assessment, penetration testing support, and compliance automation for IEC 62443 and ISO 57000 standards.

**Key Capabilities:**
- Multi-tenant data isolation with shared threat intelligence
- Autonomous penetration testing integration (Agent Zero)
- IEC 62443 gap analysis and compliance automation
- ISO 57000 rail security standards support
- Multi-hop reasoning for attack path analysis
- Automated document generation (reports, handovers, assessments)
- SOC integration and crisis management support

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Next.js 14 Frontend (App Router)                              │
│  - Consultant Dashboards    - Client Management                │
│  - Risk Assessment UI       - Threat Modeling                   │
│  - Pentest Coordination     - Report Generation                 │
│  - shadcn/ui Components     - Tailwind CSS                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTPS/REST/GraphQL
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Backend (Python 3.11+)                                │
│  - Multi-tenant Auth (JWT + SSO)  - RBAC & Policy Engine       │
│  - Client Segmentation            - Audit Logging               │
│  - RESTful APIs                   - GraphQL Endpoints           │
│  - Document Generation Pipeline   - External Integrations       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE GRAPH LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  OpenSPG + KAG Framework                                       │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │ SPG-Schema    │  │ KAG-Builder   │  │ KAG-Solver    │      │
│  │ - UCO Ontology│  │ - OneKE       │  │ - Logical Form│      │
│  │ - ICS Schema  │  │ - Entity Link │  │ - Multi-hop   │      │
│  │ - IEC 62443   │  │ - Normalization│  │ - Reasoning   │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16+              Neo4j Enterprise 5.x              │
│  - Client metadata           - Knowledge graph storage          │
│  - User accounts             - Multi-database (per client)      │
│  - Row-Level Security        - Shared threat intelligence DB    │
│  - Audit logs                - Graph algorithms (GDS)           │
│                                                                 │
│  Milvus Vector DB            Object Storage (MinIO)            │
│  - Semantic embeddings       - Document archives                │
│  - Similarity search         - Report templates                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  External Systems                    AI/ML Services             │
│  - Agent Zero (Pentest AI)          - OpenAI / Local LLM       │
│  - SIEM (Splunk, QRadar, Sentinel)  - Embedding Models         │
│  - CMMS / Asset Management          - OCR / Diagram Parser     │
│  - STIX/TAXII Feeds                 - NLP Extraction           │
│  - Network Discovery Tools          - Simulation Sandbox       │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles

1. **Multi-Tenancy First**: Complete data isolation between clients with shared threat intelligence
2. **Semantic Richness**: UCO ontology provides standardized cybersecurity knowledge representation
3. **Advanced Reasoning**: KAG framework enables multi-hop logical reasoning over complex attack paths
4. **Compliance Automation**: Built-in IEC 62443 and ISO 57000 assessment workflows
5. **AI-Native Design**: LLM integration for document extraction, query answering, and autonomous actions
6. **Extensibility**: Plugin architecture for new compliance frameworks, tools, and integrations

---

## 2. Data Architecture

### 2.1 UCO Ontology Mapping to OpenSPG

The **Unified Cybersecurity Ontology (UCO)** provides the semantic foundation. Mapping to OpenSPG SPG-Schema:

#### Core UCO Classes → OpenSPG Entity Types

```yaml
# Asset Domain
Asset:
  - Hardware: [Server, NetworkDevice, ICS_Component, Workstation]
  - Software: [Application, OperatingSystem, Firmware, Database]
  - Data: [Dataset, Configuration, Credential, Certificate]
  - Service: [WebService, DatabaseService, IndustrialProtocol]

# Vulnerability Domain
Vulnerability:
  - CVE: [CVE_Entry, NVD_Record]
  - CWE: [Weakness, WeaknessCategory]
  - CVSS: [CVSS_Vector, CVSS_Score]
  - CPE: [Product, Vendor, Version]

# Threat Domain
Threat:
  - ThreatActor: [APT_Group, Insider, Cybercriminal]
  - Campaign: [AttackCampaign, ThreatCampaign]
  - TTP: [Tactic, Technique, Procedure, SubTechnique]
  - Malware: [Trojan, Ransomware, RAT, Rootkit]

# Attack Domain
Attack:
  - AttackPattern: [CAPEC_Pattern, ICS_AttackPattern]
  - AttackPath: [PathSegment, AttackChain, KillChain]
  - Exploit: [ExploitCode, ExploitTechnique, Payload]
  - Indicator: [IoC, Artifact, Observable]

# Defense Domain
Defense:
  - Control: [TechnicalControl, ProcessControl, PhysicalControl]
  - Mitigation: [Patch, Configuration, Procedure]
  - Detection: [Signature, Rule, Heuristic, Behavior]
  - Response: [Playbook, Action, Remediation]

# Infrastructure Domain (Extended)
Infrastructure:
  - Network: [Zone, Conduit, Segment, VLAN]
  - ICS: [PLC, SCADA, HMI, DCS, Safety_System]
  - Cloud: [VPC, Container, VM, K8s_Cluster]
  - IT: [Domain_Controller, Active_Directory, DNS, DHCP]

# Compliance Domain (Extended)
Compliance:
  - Standard: [IEC_62443, ISO_57000, NIST_CSF, CIS_Controls]
  - Requirement: [SecurityLevel, ZoneRequirement, Capability]
  - Assessment: [GapAnalysis, RiskAssessment, AuditFinding]
  - Evidence: [Document, Configuration, TestResult]
```

#### Relationship Types (Predicates)

```yaml
# Asset Relationships
- dependsOn: Asset → Asset
- contains: Asset → Asset
- communicatesWith: Asset → Asset
- locatedIn: Asset → Zone
- managedBy: Asset → Person/System
- hasVulnerability: Asset → Vulnerability
- protectedBy: Asset → Control

# Vulnerability Relationships
- exploitedBy: Vulnerability → AttackPattern/Exploit
- mitigatedBy: Vulnerability → Mitigation
- affects: Vulnerability → Asset/Product
- relatedTo: Vulnerability → CWE
- hasScore: Vulnerability → CVSS_Score

# Threat Relationships
- uses: ThreatActor → TTP/Malware/Tool
- targets: ThreatActor → Asset/Organization/Sector
- implements: TTP → AttackPattern
- detectableBy: TTP → Detection
- mitigatedBy: TTP → Control

# Attack Relationships
- nextStep: AttackPath → AttackPath
- requires: AttackPattern → Prerequisite
- leverages: Exploit → Vulnerability
- generatesIndicator: Attack → IoC

# Compliance Relationships
- requiresControl: Requirement → Control
- assessedBy: Asset → Assessment
- hasEvidence: Requirement → Evidence
- satisfies: Control → Requirement
- appliesTo: Standard → Asset/Zone
```

### 2.2 Neo4j Graph Schema Design

#### Multi-Database Strategy

```
Neo4j Instance
├── shared_threat_intel (Database)
│   ├── CVE nodes (500K+)
│   ├── CWE nodes (1.4K+)
│   ├── CAPEC nodes (600+)
│   ├── MITRE ATT&CK (2K+ techniques)
│   ├── IEC 62443 standards
│   ├── ISO 57000 requirements
│   └── Public threat feeds
│
├── client_001 (Database)
│   ├── Assets (customer-specific)
│   ├── Infrastructure topology
│   ├── Vulnerabilities (instances)
│   ├── Assessments
│   ├── Incidents
│   └── Documents
│
├── client_002 (Database)
│   └── [Same structure as client_001]
│
└── client_NNN (Database)
    └── [Same structure as client_001]
```

#### Graph Node Labels and Properties

```cypher
// Asset Node Example
(:Asset:Server {
  id: "uuid",
  client_id: "client_001",
  name: "prod-db-01",
  ip_address: "10.1.2.5",
  os: "Windows Server 2019",
  zone: "Level_3_Operations",
  criticality: "High",
  owner: "IT Operations",
  created_at: timestamp,
  updated_at: timestamp
})

// CVE Node Example (in shared DB)
(:Vulnerability:CVE {
  id: "CVE-2024-12345",
  description: "Buffer overflow in...",
  cvss_base_score: 9.8,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  published_date: "2024-10-15",
  cwe_ids: ["CWE-119", "CWE-787"],
  affected_products: ["cpe:2.3:a:vendor:product:*:*:*:*:*:*:*:*"]
})

// MITRE Technique Node (in shared DB)
(:TTP:Technique {
  id: "T1190",
  name: "Exploit Public-Facing Application",
  tactic: "Initial Access",
  platforms: ["Windows", "Linux", "Network"],
  data_sources: ["Application Log", "Network Traffic"],
  mitigations: ["M1048", "M1030", "M1026"]
})

// IEC 62443 Requirement Node (in shared DB)
(:Compliance:IEC62443_Requirement {
  id: "SR-1.1",
  name: "Human User Identification and Authentication",
  security_level: "SL-1",
  category: "Identification and Authentication Control",
  description: "The control system shall provide...",
  rationale: "To ensure that...",
  supplemental_guidance: "..."
})

// Zone Node (client-specific)
(:Infrastructure:Zone {
  id: "zone_uuid",
  client_id: "client_001",
  name: "Level 3 - Manufacturing Execution",
  iec_level: "Level_3",
  security_level: "SL-2",
  description: "MES and SCADA servers",
  required_controls: ["SR-1.1", "SR-1.2", "SR-1.3", ...],
  conduits: ["conduit_001", "conduit_002"]
})
```

#### Relationship Examples

```cypher
// Asset depends on another asset
(:Asset {id: "web-server-01"})-[:DEPENDS_ON {
  type: "network",
  protocol: "HTTPS",
  port: 443,
  criticality: "High"
}]->(:Asset {id: "db-server-01"})

// Asset has vulnerability
(:Asset {id: "web-server-01"})-[:HAS_VULNERABILITY {
  discovered_date: "2024-10-20",
  status: "Open",
  severity: "Critical",
  exploitable: true,
  mitigation_status: "Pending"
}]->(:CVE {id: "CVE-2024-12345"})

// Vulnerability exploited by attack pattern
(:CVE {id: "CVE-2024-12345"})-[:EXPLOITED_BY {
  difficulty: "Low",
  prerequisites: ["Network access", "No authentication"],
  typical_tools: ["Metasploit", "Custom exploit"]
}]->(:CAPEC {id: "CAPEC-100"})

// Attack pattern implements MITRE technique
(:CAPEC {id: "CAPEC-100"})-[:IMPLEMENTS]->(:Technique {id: "T1190"})

// Zone requires security control
(:Zone {id: "zone_uuid"})-[:REQUIRES_CONTROL {
  security_level: "SL-2",
  mandatory: true,
  assessment_status: "Gap"
}]->(:IEC62443_Requirement {id: "SR-1.1"})

// Asset located in zone
(:Asset {id: "plc-001"})-[:LOCATED_IN]->(:Zone {name: "Level 1 - Process Control"})

// Cross-database link (client to shared)
// Via Cypher federation or application-level join
MATCH (a:Asset {client_id: "client_001"})
MATCH (v:CVE {id: "CVE-2024-12345"}) // from shared DB
CREATE (a)-[:AFFECTED_BY]->(v)
```

### 2.3 PostgreSQL Schema Design

#### Multi-Tenant Tables with Row-Level Security

```sql
-- Enable Row-Level Security
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Clients table
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'active',
    neo4j_database VARCHAR(100) UNIQUE NOT NULL,
    metadata JSONB
);

-- Users table with client association
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- consultant, admin, readonly
    mfa_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Enable RLS on users
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY users_isolation_policy ON users
    FOR ALL
    USING (client_id = current_setting('app.current_client_id')::UUID);

-- Projects table (assessments, pentests, etc.)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- 'iec62443_assessment', 'pentest', 'threat_model'
    status VARCHAR(50), -- 'planning', 'active', 'completed'
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY projects_isolation_policy ON projects
    FOR ALL
    USING (client_id = current_setting('app.current_client_id')::UUID);

-- Assessments table
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id),
    project_id UUID REFERENCES projects(id),
    assessment_type VARCHAR(100), -- 'iec62443_gap', 'iso57000_compliance'
    target_asset_id VARCHAR(255), -- Neo4j node ID
    findings JSONB,
    recommendations JSONB,
    risk_score DECIMAL(3,1),
    status VARCHAR(50),
    assessed_by UUID REFERENCES users(id),
    assessed_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;

CREATE POLICY assessments_isolation_policy ON assessments
    FOR ALL
    USING (client_id = current_setting('app.current_client_id')::UUID);

-- Documents table (generated reports, evidence)
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES clients(id),
    project_id UUID REFERENCES projects(id),
    document_type VARCHAR(100), -- 'pentest_report', 'gap_analysis', 'handover'
    title VARCHAR(255),
    file_path VARCHAR(500), -- MinIO/S3 object key
    format VARCHAR(50), -- 'pdf', 'docx', 'md'
    generated_at TIMESTAMP DEFAULT NOW(),
    generated_by UUID REFERENCES users(id),
    metadata JSONB
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY documents_isolation_policy ON documents
    FOR ALL
    USING (client_id = current_setting('app.current_client_id')::UUID);

-- Audit logs (exempt from RLS for compliance)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID,
    user_id UUID,
    action VARCHAR(100), -- 'login', 'query_kg', 'generate_report', 'update_asset'
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    details JSONB
);

-- No RLS on audit logs (superuser access only)
CREATE INDEX idx_audit_logs_client ON audit_logs(client_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
```

---

## 3. Data Ingestion Pipeline

### 3.1 Data Source Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
├─────────────────────────────────────────────────────────────┤
│  Public Threat Intelligence      Client-Specific Data       │
│  - NVD CVE/CWE/CAPEC APIs       - Asset inventories (CMDB)  │
│  - MITRE ATT&CK (STIX 2.1)      - Network diagrams (PDF)    │
│  - IEC 62443 standards          - Security policies         │
│  - ISO 57000 requirements       - Vulnerability scans        │
│  - CISA advisories              - SIEM logs                  │
│  - STIX/TAXII feeds             - Pentest results            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                 INGESTION LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  Scheduled Jobs (Airflow/Celery)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ NVD Loader   │  │ ATT&CK Loader│  │ OneKE Parser │      │
│  │ - Daily CVE  │  │ - Quarterly  │  │ - PDF Reports│      │
│  │ - Delta sync │  │ - STIX 2.1   │  │ - Diagrams   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Asset Sync   │  │ CMMS API     │  │ Network Scan │      │
│  │ - CSV import │  │ - Safety SIL │  │ - Nmap/Nessus│      │
│  │ - API pull   │  │ - RAMS data  │  │ - Auto-parse │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│           TRANSFORMATION & NORMALIZATION                     │
├─────────────────────────────────────────────────────────────┤
│  SPG-Builder + OneKE Processing                             │
│  1. Entity Extraction (LLM-based + rules)                   │
│  2. Entity Linking (to UCO schema)                          │
│  3. Concept Normalization (synonyms, acronyms)              │
│  4. Relationship Inference (dependencies, impacts)           │
│  5. Quality Validation (schema compliance)                   │
│  6. Deduplication (cross-source entity resolution)           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│               KNOWLEDGE GRAPH STORAGE                        │
├─────────────────────────────────────────────────────────────┤
│  Neo4j Multi-Database Write                                 │
│  - Shared DB: CVE/CWE/CAPEC/ATT&CK/Standards                │
│  - Client DBs: Assets, topology, assessments                 │
│  - Transaction management (rollback on errors)               │
│  - Index updates (full-text, vector)                         │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 OneKE Document Processing Pipeline

```python
# Pseudocode for PDF/Document Ingestion
class OneKEDocumentProcessor:
    def process_pdf(self, pdf_path, client_id, document_type):
        """
        Extract structured knowledge from PDF documents
        (pentest reports, network diagrams, security policies)
        """
        # Step 1: Parse PDF with LlamaParse
        parsed_doc = llamaparse.parse(pdf_path)

        # Step 2: OneKE Schema-Guided Extraction
        schema = self.load_schema(document_type)
        # schema examples:
        # - "pentest_report": [Finding, CVE, Recommendation, Asset]
        # - "network_diagram": [Device, Connection, Zone, Protocol]
        # - "iec62443_gap": [Requirement, Control, Gap, Evidence]

        extraction_result = oneke_agent.extract(
            document=parsed_doc,
            schema=schema,
            language="en"
        )

        # Step 3: Entity Resolution
        entities = self.resolve_entities(
            extraction_result.entities,
            client_id
        )

        # Step 4: Knowledge Graph Ingestion
        for entity in entities:
            self.create_or_update_node(entity, client_id)

        for relationship in extraction_result.relationships:
            self.create_relationship(relationship, client_id)

        # Step 5: Link to Original Document
        self.store_document_reference(
            kg_node_ids=entities,
            document_path=pdf_path,
            client_id=client_id
        )

        return extraction_result
```

### 3.3 CVE/CWE/CAPEC Integration

```python
# Pseudocode for NVD Data Ingestion
class NVDDataLoader:
    def sync_cve_database(self):
        """Daily sync of CVE entries from NVD"""

        # Step 1: Fetch delta updates
        last_sync = self.get_last_sync_timestamp()
        new_cves = nvd_api.get_cves(
            modified_start_date=last_sync,
            modified_end_date=datetime.now()
        )

        # Step 2: Transform to UCO schema
        for cve_data in new_cves:
            cve_node = {
                "id": cve_data["id"],  # CVE-2024-12345
                "description": cve_data["descriptions"][0]["value"],
                "cvss_base_score": cve_data["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"],
                "cvss_vector": cve_data["metrics"]["cvssMetricV31"][0]["cvssData"]["vectorString"],
                "published_date": cve_data["published"],
                "last_modified": cve_data["lastModified"],
                "cwe_ids": [ref["cweId"] for ref in cve_data.get("weaknesses", [])],
                "affected_products": [cpe["criteria"] for cpe in cve_data.get("configurations", [])]
            }

            # Step 3: Write to shared Neo4j database
            self.neo4j_shared.create_or_merge_node(
                label="CVE",
                properties=cve_node
            )

            # Step 4: Create relationships
            for cwe_id in cve_node["cwe_ids"]:
                self.neo4j_shared.create_relationship(
                    from_node=("CVE", {"id": cve_node["id"]}),
                    to_node=("CWE", {"id": cwe_id}),
                    relationship_type="RELATED_TO"
                )

        # Step 5: Update CAPEC mappings
        self.link_capec_to_cwe()
```

---

## 4. Schema Design (OpenSPG SPG-Schema)

### 4.1 UCO-Based Entity Type Hierarchy

```yaml
# SPG-Schema Definition (YAML representation)
namespace: CyberGraphPlatform
version: 1.0.0

entity_types:
  Asset:
    base_type: SPGType.Basic
    description: "Any IT or OT asset in client infrastructure"
    properties:
      - name: asset_id
        type: String
        required: true
        unique: true
      - name: name
        type: String
        required: true
      - name: asset_type
        type: Enum
        values: [Server, NetworkDevice, ICS_Device, Workstation, Application, Database]
      - name: ip_address
        type: String
        pattern: "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"
      - name: mac_address
        type: String
      - name: zone
        type: Reference
        target: Zone
      - name: criticality
        type: Enum
        values: [Critical, High, Medium, Low]
      - name: client_id
        type: String
        required: true
        index: true

  Vulnerability:
    base_type: SPGType.Basic
    description: "CVE, CWE, or custom vulnerability"
    properties:
      - name: vuln_id
        type: String
        required: true
        unique: true
      - name: vuln_type
        type: Enum
        values: [CVE, CWE, CustomVuln]
      - name: description
        type: Text
      - name: cvss_score
        type: Float
        range: [0.0, 10.0]
      - name: cvss_vector
        type: String
      - name: published_date
        type: DateTime
      - name: affected_products
        type: List<String>
      - name: exploitable
        type: Boolean
      - name: exploit_available
        type: Boolean

  TTP:
    base_type: SPGType.Basic
    description: "MITRE ATT&CK Tactic, Technique, or Procedure"
    properties:
      - name: mitre_id
        type: String
        required: true
        unique: true
      - name: name
        type: String
      - name: ttp_type
        type: Enum
        values: [Tactic, Technique, SubTechnique, Procedure]
      - name: tactic
        type: String
      - name: platforms
        type: List<String>
      - name: data_sources
        type: List<String>
      - name: mitigations
        type: List<Reference>
        target: Mitigation

  Zone:
    base_type: SPGType.Basic
    description: "IEC 62443 security zone"
    properties:
      - name: zone_id
        type: String
        required: true
      - name: name
        type: String
      - name: iec_level
        type: Enum
        values: [Level_0, Level_1, Level_2, Level_3, Level_4, Level_5]
      - name: security_level
        type: Enum
        values: [SL-1, SL-2, SL-3, SL-4]
      - name: description
        type: Text
      - name: required_controls
        type: List<Reference>
        target: IEC62443_Requirement
      - name: client_id
        type: String
        required: true

  IEC62443_Requirement:
    base_type: SPGType.Basic
    description: "IEC 62443 security requirement"
    properties:
      - name: requirement_id
        type: String
        required: true
        unique: true
      - name: name
        type: String
      - name: security_level
        type: Enum
        values: [SL-1, SL-2, SL-3, SL-4]
      - name: category
        type: String
      - name: description
        type: Text
      - name: rationale
        type: Text
      - name: supplemental_guidance
        type: Text

relationship_types:
  dependsOn:
    source: Asset
    target: Asset
    properties:
      - name: dependency_type
        type: Enum
        values: [Network, Data, Process, Authentication]
      - name: protocol
        type: String
      - name: port
        type: Integer
      - name: criticality
        type: Enum
        values: [Critical, High, Medium, Low]

  hasVulnerability:
    source: Asset
    target: Vulnerability
    properties:
      - name: discovered_date
        type: DateTime
      - name: status
        type: Enum
        values: [Open, InProgress, Mitigated, Closed, FalsePositive]
      - name: exploitable
        type: Boolean
      - name: mitigation_status
        type: String

  exploitedBy:
    source: Vulnerability
    target: AttackPattern
    properties:
      - name: difficulty
        type: Enum
        values: [Low, Medium, High]
      - name: prerequisites
        type: List<String>
      - name: typical_tools
        type: List<String>

  implements:
    source: AttackPattern
    target: TTP
    description: "CAPEC attack pattern implements MITRE technique"

  locatedIn:
    source: Asset
    target: Zone
    properties:
      - name: placement_rationale
        type: String

  requiresControl:
    source: Zone
    target: IEC62443_Requirement
    properties:
      - name: mandatory
        type: Boolean
      - name: assessment_status
        type: Enum
        values: [NotAssessed, Compliant, PartiallyCompliant, Gap]

constraints:
  - type: cardinality
    rule: "An Asset must belong to at least one Zone"
    entity: Asset
    relationship: locatedIn
    min: 1

  - type: validation
    rule: "CVSS score must match vector string calculation"
    entity: Vulnerability
    properties: [cvss_score, cvss_vector]
```

### 4.2 IEC 62443 Security Requirements Schema

```python
# IEC 62443 Foundational Requirements (FR) Structure
IEC_62443_REQUIREMENTS = {
    "FR-1": {
        "name": "Identification and Authentication Control",
        "requirements": [
            {
                "id": "SR-1.1",
                "name": "Human User Identification and Authentication",
                "sl_1": "Required",
                "sl_2": "Required",
                "sl_3": "Required",
                "sl_4": "Required",
                "description": "The control system shall provide the capability to identify and authenticate all human users...",
                "rationale": "To ensure that only authorized users can access...",
                "supplemental_guidance": "This requirement applies to all human user interfaces..."
            },
            {
                "id": "SR-1.2",
                "name": "Software Process and Device Identification and Authentication",
                "sl_1": "Not Selected",
                "sl_2": "Required",
                "sl_3": "Required",
                "sl_4": "Required"
            },
            # ... more SR-1.x requirements
        ]
    },
    "FR-2": {
        "name": "Use Control",
        "requirements": [
            {"id": "SR-2.1", "name": "Authorization Enforcement"},
            {"id": "SR-2.2", "name": "Wireless Use Control"},
            # ... more SR-2.x requirements
        ]
    },
    # FR-3 through FR-7...
}

# Each requirement becomes a node in the knowledge graph
# Zones link to required SRs based on their target Security Level
```

---

## 5. Integration Design

### 5.1 Agent Zero Integration Architecture

**Agent Zero** is an autonomous penetration testing AI that uses the knowledge graph to intelligently plan and execute attacks.

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ZERO                               │
│  Autonomous Penetration Testing AI                          │
└─────────────────────────────────────────────────────────────┘
                          ↓ REST API (< 500ms p95)
┌─────────────────────────────────────────────────────────────┐
│              CGIP BACKEND - AGENT ZERO API                  │
├─────────────────────────────────────────────────────────────┤
│  Endpoints:                                                  │
│  - POST /api/v1/agent-zero/query-kg                         │
│    → Query knowledge graph for attack planning              │
│                                                              │
│  - POST /api/v1/agent-zero/update-kg                        │
│    → Update KG with pentest findings                        │
│                                                              │
│  - POST /api/v1/agent-zero/select-attack-path               │
│    → Get ranked attack paths for target                     │
│                                                              │
│  - POST /api/v1/agent-zero/match-exploit                    │
│    → Find applicable exploits for vulnerabilities           │
│                                                              │
│  - POST /api/v1/agent-zero/simulate                         │
│    → Run attack simulation in sandbox                       │
│                                                              │
│  - POST /api/v1/agent-zero/learn                            │
│    → Feedback loop for reinforcement learning               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              KNOWLEDGE GRAPH QUERY ENGINE                   │
│                 (KAG-Solver)                                │
├─────────────────────────────────────────────────────────────┤
│  Attack Path Analysis:                                      │
│  1. Multi-hop graph traversal                               │
│  2. Constraint satisfaction (access level, prerequisites)   │
│  3. Risk scoring (CVSS * asset criticality * exploitability)│
│  4. Path ranking (shortest, highest impact, stealthiest)    │
│                                                              │
│  Exploit Matching:                                          │
│  1. Query: MATCH (a:Asset)-[:HAS_VULNERABILITY]->(v:CVE)   │
│     WHERE a.id = $target_asset                              │
│  2. Link CVE → CWE → CAPEC → Exploit Database              │
│  3. Filter by Agent Zero's current access level             │
│  4. Rank by success probability and impact                  │
└─────────────────────────────────────────────────────────────┘
```

#### Agent Zero API Specification

```yaml
# POST /api/v1/agent-zero/query-kg
Request:
  client_id: "client_001"
  query_type: "attack_path" | "exploit_lookup" | "asset_topology" | "defense_analysis"
  parameters:
    target_asset_id: "asset_uuid"
    current_access_level: "user" | "admin" | "system"
    constraints: ["stealth", "no_dos", "no_data_exfiltration"]

Response:
  results: [
    {
      type: "attack_path",
      path: [
        {"step": 1, "action": "exploit_cve", "target": "web-server-01", "cve": "CVE-2024-12345"},
        {"step": 2, "action": "privilege_escalation", "technique": "T1068"},
        {"step": 3, "action": "lateral_movement", "target": "db-server-01", "technique": "T1021"}
      ],
      risk_score: 8.7,
      estimated_success_rate: 0.85,
      required_tools: ["metasploit", "mimikatz"],
      prerequisites: ["network_access", "valid_credentials"]
    }
  ]
  metadata:
    query_time_ms: 245
    kg_nodes_traversed: 1847
    reasoning_steps: 12

# POST /api/v1/agent-zero/update-kg
Request:
  client_id: "client_001"
  findings: [
    {
      type: "new_vulnerability",
      asset_id: "plc-005",
      cve_id: "CVE-2024-99999",
      cvss_score: 9.1,
      exploitable: true,
      evidence: "Screenshot path or log excerpt"
    },
    {
      type: "successful_exploit",
      attack_path_id: "path_uuid",
      step_completed: 2,
      outcome: "success",
      access_gained: "admin",
      timestamp: "2024-10-26T14:32:00Z"
    }
  ]

Response:
  updated_nodes: ["asset_uuid_1", "vuln_uuid_2"]
  updated_relationships: ["rel_uuid_3"]
  status: "success"
```

#### Attack Path Ranking Algorithm

```python
# Pseudocode for Attack Path Selection
class AttackPathSelector:
    def rank_attack_paths(self, target_asset_id, current_access, constraints):
        """
        Multi-hop Cypher query to find all paths from current position to target
        with ranking based on multiple factors
        """

        cypher_query = """
        MATCH path = (start:Asset {id: $current_asset})
                     -[r*1..5]->
                     (target:Asset {id: $target_asset})
        WHERE ALL(rel IN relationships(path)
                  WHERE rel.exploitable = true)

        WITH path,
             [rel in relationships(path) | rel.cvss_score] AS cvss_scores,
             [node in nodes(path) | node.criticality] AS criticalities,
             [rel in relationships(path) | rel.difficulty] AS difficulties

        RETURN path,
               REDUCE(s = 0, score IN cvss_scores | s + score) / SIZE(cvss_scores) AS avg_cvss,
               SIZE(relationships(path)) AS path_length,
               REDUCE(p = 1.0, diff IN difficulties |
                      p * CASE diff WHEN 'Low' THEN 0.9
                                    WHEN 'Medium' THEN 0.6
                                    WHEN 'High' THEN 0.3
                          END) AS success_probability

        ORDER BY (avg_cvss * 0.4 + (1.0 / path_length) * 0.3 + success_probability * 0.3) DESC
        LIMIT 10
        """

        paths = self.neo4j.run_query(cypher_query, {
            "current_asset": self.get_current_asset(current_access),
            "target_asset": target_asset_id
        })

        # Apply constraint filtering (stealth, no DoS, etc.)
        filtered_paths = self.apply_constraints(paths, constraints)

        # Enhance with MITRE ATT&CK technique mappings
        enriched_paths = self.map_to_attack_techniques(filtered_paths)

        return enriched_paths
```

### 5.2 MITRE ATT&CK and STIX 2.1 Integration

```python
# Pseudocode for MITRE ATT&CK STIX 2.1 Ingestion
class MITREAttackLoader:
    def load_stix_bundle(self, stix_bundle_path):
        """
        Load MITRE ATT&CK from STIX 2.1 JSON bundle
        """
        with open(stix_bundle_path, 'r') as f:
            bundle = json.load(f)

        for stix_object in bundle["objects"]:
            if stix_object["type"] == "attack-pattern":
                self.create_technique_node(stix_object)
            elif stix_object["type"] == "course-of-action":
                self.create_mitigation_node(stix_object)
            elif stix_object["type"] == "intrusion-set":
                self.create_threat_actor_node(stix_object)
            elif stix_object["type"] == "malware":
                self.create_malware_node(stix_object)
            elif stix_object["type"] == "relationship":
                self.create_relationship(stix_object)

    def create_technique_node(self, stix_object):
        """
        Transform STIX attack-pattern to Neo4j Technique node
        """
        technique_id = stix_object["external_references"][0]["external_id"]  # e.g., T1190

        node_properties = {
            "id": technique_id,
            "name": stix_object["name"],
            "description": stix_object.get("description", ""),
            "tactic": self.extract_tactic(stix_object),
            "platforms": stix_object.get("x_mitre_platforms", []),
            "data_sources": stix_object.get("x_mitre_data_sources", []),
            "detection": stix_object.get("x_mitre_detection", ""),
            "created": stix_object["created"],
            "modified": stix_object["modified"]
        }

        self.neo4j_shared.create_node("Technique", node_properties)

    def create_relationship(self, stix_rel):
        """
        Create Neo4j relationship from STIX relationship object
        """
        if stix_rel["relationship_type"] == "uses":
            # Threat actor uses technique
            self.neo4j_shared.create_relationship(
                from_id=stix_rel["source_ref"],
                to_id=stix_rel["target_ref"],
                rel_type="USES"
            )
        elif stix_rel["relationship_type"] == "mitigates":
            # Mitigation mitigates technique
            self.neo4j_shared.create_relationship(
                from_id=stix_rel["source_ref"],
                to_id=stix_rel["target_ref"],
                rel_type="MITIGATES"
            )
```

### 5.3 CMMS and Asset Management Integration

```python
# Pseudocode for CMMS/Asset Management Integration
class AssetManagementIntegration:
    def sync_with_cmms(self, client_id):
        """
        Synchronize assets from CMMS/EAM system
        Brings in asset criticality, safety ratings (SIL), RAMS data
        """
        cmms_api = CMSClient(
            base_url=self.get_client_cmms_url(client_id),
            api_key=self.get_client_cmms_key(client_id)
        )

        # Fetch all assets for client
        assets = cmms_api.get_assets()

        for asset_data in assets:
            # Transform to UCO Asset schema
            asset_node = {
                "id": asset_data["asset_id"],
                "client_id": client_id,
                "name": asset_data["asset_name"],
                "asset_type": self.map_asset_type(asset_data["category"]),
                "location": asset_data["location"],
                "criticality": self.calculate_criticality(asset_data),
                "safety_integrity_level": asset_data.get("sil_rating"),  # SIL 1-4
                "rams_data": {
                    "reliability": asset_data.get("mtbf"),
                    "availability": asset_data.get("availability_target"),
                    "maintainability": asset_data.get("mttr"),
                    "safety": asset_data.get("safety_rating")
                },
                "owner": asset_data["responsible_person"],
                "vendor": asset_data.get("manufacturer"),
                "model": asset_data.get("model_number"),
                "serial_number": asset_data.get("serial"),
                "installation_date": asset_data.get("commissioned_date")
            }

            # Create or update in client's Neo4j database
            self.neo4j_client_db(client_id).merge_node("Asset", asset_node)

            # Link to zone if location mapping exists
            if zone_id := self.map_location_to_zone(asset_data["location"], client_id):
                self.neo4j_client_db(client_id).create_relationship(
                    from_node=("Asset", {"id": asset_node["id"]}),
                    to_node=("Zone", {"id": zone_id}),
                    rel_type="LOCATED_IN"
                )

    def calculate_criticality(self, asset_data):
        """
        Calculate asset criticality from RAMS and operational data
        """
        factors = {
            "safety_impact": asset_data.get("sil_rating", 0) * 2.5,  # SIL 1-4 → 2.5-10
            "availability_requirement": asset_data.get("availability_target", 0.95) * 10,
            "financial_impact": min(asset_data.get("replacement_cost", 0) / 100000, 10),
            "operational_impact": self.assess_operational_impact(asset_data)
        }

        total_score = sum(factors.values()) / len(factors)

        if total_score >= 8.0:
            return "Critical"
        elif total_score >= 6.0:
            return "High"
        elif total_score >= 4.0:
            return "Medium"
        else:
            return "Low"
```

### 5.4 SOC Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SIEM / SOC Platform                       │
│          (Splunk, QRadar, Sentinel, Chronicle)              │
└─────────────────────────────────────────────────────────────┘
                          ↓ Webhook / API
┌─────────────────────────────────────────────────────────────┐
│              CGIP - SOC INTEGRATION SERVICE                 │
├─────────────────────────────────────────────────────────────┤
│  Alert Enrichment Pipeline:                                 │
│  1. Receive alert (IP, CVE, hash, domain, etc.)            │
│  2. Query knowledge graph for context                       │
│  3. Enrich with:                                            │
│     - Asset criticality and dependencies                    │
│     - Known vulnerabilities and CVEs                        │
│     - MITRE ATT&CK technique mapping                       │
│     - Historical incidents on same asset                    │
│     - Attack path analysis (reachable targets)              │
│     - Recommended mitigations                               │
│  4. Return enriched alert to SIEM                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                KNOWLEDGE GRAPH QUERY                        │
│  Example: Alert for CVE-2024-12345 on asset web-server-01  │
├─────────────────────────────────────────────────────────────┤
│  MATCH (a:Asset {id: 'web-server-01'})                     │
│        -[:HAS_VULNERABILITY]->(v:CVE {id: 'CVE-2024-12345'})│
│  MATCH (v)-[:RELATED_TO]->(cwe:CWE)                        │
│  MATCH (v)-[:EXPLOITED_BY]->(capec:CAPEC)                  │
│        -[:IMPLEMENTS]->(ttp:Technique)                      │
│  MATCH (a)-[:DEPENDS_ON*1..3]->(deps:Asset)                │
│  MATCH (a)-[:LOCATED_IN]->(z:Zone)                         │
│  RETURN a, v, cwe, capec, ttp, deps, z                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│               ENRICHED ALERT OUTPUT                         │
├─────────────────────────────────────────────────────────────┤
│  {                                                          │
│    "alert_id": "SOC-2024-10-26-1234",                      │
│    "original_alert": { ... },                               │
│    "enrichment": {                                          │
│      "asset_context": {                                     │
│        "criticality": "High",                               │
│        "zone": "DMZ - Level 4",                            │
│        "dependencies": [                                    │
│          {"name": "db-server-01", "criticality": "Critical"},│
│          {"name": "auth-server-01", "criticality": "High"} │
│        ]                                                    │
│      },                                                     │
│      "vulnerability_details": {                             │
│        "cvss_score": 9.8,                                   │
│        "exploitable": true,                                 │
│        "exploit_available": true,                           │
│        "cwe": "CWE-787 (Out-of-bounds Write)",             │
│        "attack_patterns": ["CAPEC-100"]                     │
│      },                                                     │
│      "threat_intelligence": {                               │
│        "mitre_technique": "T1190 - Exploit Public-Facing Application",│
│        "tactic": "Initial Access",                          │
│        "known_threat_actors": ["APT41", "Lazarus Group"]   │
│      },                                                     │
│      "impact_analysis": {                                   │
│        "reachable_critical_assets": 7,                      │
│        "potential_data_loss": "Customer database",          │
│        "estimated_downtime": "4-8 hours"                    │
│      },                                                     │
│      "recommended_actions": [                               │
│        "Immediate: Isolate web-server-01 from network",    │
│        "Apply patch: vendor_patch_2024-10-25.rpm",         │
│        "Monitor db-server-01 for lateral movement",        │
│        "Review firewall rules for zone boundary"            │
│      ]                                                      │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Query Design and Reasoning

### 6.1 KAG-Solver Logical Reasoning

The **KAG-Solver** provides multi-hop logical reasoning capabilities beyond simple graph traversal:

```python
# Example: Complex Risk Assessment Query
query = """
For client XYZ Corp, identify all critical ICS assets
that have unpatched vulnerabilities with CVSS > 7.0
AND are reachable from the internet
AND lack required IEC 62443 SL-2 controls,
then calculate the aggregate risk score considering
asset criticality, vulnerability exploitability,
and attack path feasibility.
"""

# KAG-Solver Logical Form Decomposition
logical_form = {
    "sub_question_1": {
        "operation": "retrieval",
        "query": "Find all ICS assets for client XYZ with criticality=Critical",
        "dependencies": []
    },
    "sub_question_2": {
        "operation": "retrieval",
        "query": "Find vulnerabilities with CVSS > 7.0 AND patch_status=Unpatched",
        "dependencies": []
    },
    "sub_question_3": {
        "operation": "reasoning",
        "query": "For each asset from SQ1, check if ANY path exists from internet-facing assets",
        "dependencies": ["sub_question_1"]
    },
    "sub_question_4": {
        "operation": "retrieval",
        "query": "Get required IEC 62443 SL-2 controls for ICS zones",
        "dependencies": []
    },
    "sub_question_5": {
        "operation": "reasoning",
        "query": "For each asset, check compliance with SL-2 controls from SQ4",
        "dependencies": ["sub_question_1", "sub_question_4"]
    },
    "sub_question_6": {
        "operation": "mathematical",
        "query": "Calculate aggregate risk: CVSS * exploitability * asset_criticality * path_feasibility * (1 - control_coverage)",
        "dependencies": ["sub_question_1", "sub_question_2", "sub_question_3", "sub_question_5"]
    }
}

# Execution yields enriched answer with reasoning trace
```

### 6.2 Common Cybersecurity Use Case Queries

#### Use Case 1: IEC 62443 Gap Analysis

```cypher
// Identify gaps in IEC 62443 compliance for a zone
MATCH (z:Zone {client_id: $client_id, name: $zone_name})
MATCH (z)-[:REQUIRES_CONTROL]->(req:IEC62443_Requirement)
WHERE req.security_level <= z.security_level

// Find implemented controls
OPTIONAL MATCH (z)<-[:LOCATED_IN]-(a:Asset)
                 -[:PROTECTED_BY]->(ctrl:Control)
                 -[:SATISFIES]->(req)

// Aggregate compliance status
WITH z, req,
     COUNT(DISTINCT a) AS assets_in_zone,
     COUNT(DISTINCT ctrl) AS implemented_controls,
     CASE WHEN COUNT(DISTINCT ctrl) > 0 THEN 'Compliant' ELSE 'Gap' END AS status

RETURN req.id AS requirement_id,
       req.name AS requirement_name,
       req.security_level AS sl_requirement,
       assets_in_zone,
       implemented_controls,
       status
ORDER BY status DESC, req.id
```

#### Use Case 2: Attack Surface Analysis

```cypher
// Find all internet-facing assets and their inbound attack paths
MATCH (internet:Asset {name: 'Internet_Boundary'})
MATCH path = (internet)-[:CAN_REACH*1..5]->(target:Asset {client_id: $client_id})
WHERE target.criticality IN ['Critical', 'High']

// Get vulnerabilities on path
MATCH (asset_in_path)-[:HAS_VULNERABILITY]->(v:CVE)
WHERE asset_in_path IN nodes(path)
  AND v.cvss_score >= 7.0
  AND v.exploitable = true

// Calculate attack path risk
WITH path, target,
     COLLECT(DISTINCT v) AS vulnerabilities,
     LENGTH(path) AS hops,
     REDUCE(s=0, v IN COLLECT(v.cvss_score) | s + v) / COUNT(v) AS avg_cvss

RETURN target.name AS target_asset,
       target.criticality AS criticality,
       hops AS distance_from_internet,
       SIZE(vulnerabilities) AS vuln_count,
       avg_cvss AS average_cvss,
       vulnerabilities AS exposed_vulnerabilities,
       (avg_cvss * SIZE(vulnerabilities) / hops) AS risk_score

ORDER BY risk_score DESC
LIMIT 20
```

#### Use Case 3: Threat Modeling - STRIDE Analysis

```cypher
// STRIDE threat analysis for an asset
MATCH (a:Asset {id: $asset_id})
MATCH (a)-[:LOCATED_IN]->(z:Zone)
MATCH (a)-[dep:DEPENDS_ON]->(dependency:Asset)

// Find applicable threat patterns
MATCH (ttp:Technique)
WHERE ttp.platforms CONTAINS a.os
   OR 'Network' IN ttp.platforms

// Match to STRIDE categories
WITH a, z, COLLECT(DISTINCT dependency) AS dependencies,
     COLLECT(DISTINCT ttp) AS applicable_ttps,
     [
       {category: 'Spoofing', techniques: [t IN applicable_ttps WHERE t.tactic = 'Credential Access' | t.id]},
       {category: 'Tampering', techniques: [t IN applicable_ttps WHERE t.tactic = 'Impact' | t.id]},
       {category: 'Repudiation', techniques: [t IN applicable_ttps WHERE t.tactic = 'Defense Evasion' | t.id]},
       {category: 'Information Disclosure', techniques: [t IN applicable_ttps WHERE t.tactic = 'Collection' | t.id]},
       {category: 'Denial of Service', techniques: [t IN applicable_ttps WHERE t.tactic = 'Impact' AND t.name CONTAINS 'Denial' | t.id]},
       {category: 'Elevation of Privilege', techniques: [t IN applicable_ttps WHERE t.tactic = 'Privilege Escalation' | t.id]}
     ] AS stride_threats

RETURN a.name AS asset,
       z.name AS zone,
       dependencies AS critical_dependencies,
       stride_threats AS threat_model
```

#### Use Case 4: Vulnerability Propagation Analysis

```cypher
// Calculate vulnerability impact propagation through infrastructure
MATCH (source:Asset {id: $vulnerable_asset_id})
MATCH (source)-[:HAS_VULNERABILITY]->(v:CVE {id: $cve_id})

// Find all assets dependent on vulnerable asset (up to 3 hops)
MATCH path = (source)<-[:DEPENDS_ON*1..3]-(affected:Asset)

// Calculate propagation risk
WITH source, v, affected, path,
     LENGTH(path) AS distance,
     REDUCE(crit=0, n IN nodes(path) |
            crit + CASE n.criticality
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 1 END
     ) AS cumulative_criticality

// Aggregate by distance
WITH distance,
     COUNT(DISTINCT affected) AS affected_assets,
     AVG(cumulative_criticality) AS avg_criticality,
     COLLECT(DISTINCT affected.name) AS asset_names

RETURN distance AS propagation_hops,
       affected_assets AS assets_at_risk,
       avg_criticality AS average_impact_score,
       asset_names

ORDER BY distance
```

### 6.3 Multi-Hop Reasoning Patterns

**Pattern 1: CVE → CWE → CAPEC → MITRE Technique Traversal**

```cypher
// Full threat intelligence chain for a CVE
MATCH (cve:CVE {id: 'CVE-2024-12345'})
MATCH (cve)-[:RELATED_TO]->(cwe:CWE)
MATCH (cwe)<-[:EXPLOITS]-(capec:CAPEC)
MATCH (capec)-[:IMPLEMENTS]->(ttp:Technique)
MATCH (ttp)<-[:USES]-(actor:ThreatActor)
MATCH (ttp)-[:MITIGATED_BY]->(mitigation:Mitigation)

RETURN cve.id AS vulnerability,
       COLLECT(DISTINCT cwe.id) AS weaknesses,
       COLLECT(DISTINCT capec.id) AS attack_patterns,
       COLLECT(DISTINCT ttp.id) AS mitre_techniques,
       COLLECT(DISTINCT actor.name) AS known_threat_actors,
       COLLECT(DISTINCT mitigation.id) AS available_mitigations
```

**Pattern 2: Asset Impact Radius**

```cypher
// Find all assets within N hops of a compromised asset
MATCH path = (compromised:Asset {id: $compromised_asset_id})
             -[:DEPENDS_ON|:COMMUNICATES_WITH*1..4]-(neighbor:Asset)

WITH compromised, neighbor,
     MIN(LENGTH(path)) AS shortest_distance,
     neighbor.criticality AS criticality

RETURN neighbor.id AS asset_id,
       neighbor.name AS asset_name,
       criticality,
       shortest_distance,
       CASE shortest_distance
         WHEN 1 THEN 'Immediate Risk'
         WHEN 2 THEN 'High Risk'
         WHEN 3 THEN 'Medium Risk'
         ELSE 'Low Risk'
       END AS risk_category

ORDER BY shortest_distance, criticality DESC
```

---

## 7. Document Generation Pipeline

### 7.1 Automated Report Generation

```python
# Pseudocode for IEC 62443 Gap Analysis Report Generation
class IEC62443ReportGenerator:
    def generate_gap_analysis_report(self, client_id, project_id, zones):
        """
        Generate comprehensive IEC 62443 gap analysis report with evidence
        """

        # Step 1: Query KG for compliance data
        compliance_data = self.query_compliance_status(client_id, zones)

        # Step 2: Structure report sections
        report_structure = {
            "executive_summary": self.generate_executive_summary(compliance_data),
            "scope_and_methodology": self.generate_scope_section(zones),
            "zone_conduit_analysis": self.analyze_zones_conduits(client_id, zones),
            "gap_analysis": self.detailed_gap_analysis(compliance_data),
            "risk_assessment": self.calculate_risk_scores(compliance_data),
            "remediation_roadmap": self.generate_remediation_plan(compliance_data),
            "appendices": {
                "asset_inventory": self.get_asset_inventory(client_id, zones),
                "vulnerability_summary": self.get_vulnerability_summary(client_id),
                "evidence_artifacts": self.collect_evidence(project_id)
            }
        }

        # Step 3: Render to document format
        doc = self.render_to_docx(report_structure, template="IEC62443_Gap_Analysis_Template.docx")

        # Step 4: Generate PDF
        pdf_path = self.convert_to_pdf(doc)

        # Step 5: Store in PostgreSQL + MinIO
        self.store_document(
            client_id=client_id,
            project_id=project_id,
            document_type="iec62443_gap_analysis",
            file_path=pdf_path,
            metadata=report_structure
        )

        return pdf_path

    def generate_executive_summary(self, compliance_data):
        """
        Use LLM to generate executive summary from compliance data
        """
        prompt = f"""
        Generate a professional executive summary for an IEC 62443 compliance gap analysis:

        Overall Compliance: {compliance_data['overall_compliance']}%
        Total Requirements Assessed: {compliance_data['total_requirements']}
        Gaps Identified: {compliance_data['total_gaps']}
        Critical Gaps: {compliance_data['critical_gaps']}

        Zones Assessed:
        {json.dumps(compliance_data['zones_summary'], indent=2)}

        Write a 3-paragraph executive summary highlighting key findings, risks, and recommendations.
        """

        summary = self.llm_client.generate(prompt)
        return summary
```

### 7.2 Document Templates

**Available Templates:**

1. **IEC 62443 Gap Analysis Report**
   - Executive Summary
   - Scope and Methodology
   - Zone and Conduit Analysis
   - Security Level Assessment (SL-1 through SL-4)
   - Detailed Gap Analysis (by Foundational Requirement)
   - Risk Assessment and Prioritization
   - Remediation Roadmap
   - Appendices (Asset Inventory, Vulnerabilities, Evidence)

2. **Penetration Test Report**
   - Executive Summary
   - Scope and Rules of Engagement
   - Methodology (PTES, OWASP, etc.)
   - Findings (by severity)
   - Attack Paths and Exploitation Details
   - Impact Analysis
   - Remediation Recommendations
   - Appendices (Evidence, Screenshots, Logs)

3. **ISO 57000 Security Report (Rail)**
   - Executive Summary
   - Regulatory Context (ISO 57000 series)
   - Asset Classification (signaling, rolling stock, infrastructure)
   - Threat Landscape for Rail Operations
   - Vulnerability Assessment
   - Compliance Status (ISO 57001, 57003, 57004)
   - Recommendations and Roadmap

4. **ISO 57000 Handover Document**
   - System Description
   - Security Architecture
   - Implemented Security Controls
   - Residual Risks
   - Operations and Maintenance Requirements
   - Security Monitoring Procedures
   - Incident Response Protocols
   - Acceptance Criteria

5. **Threat Model Document**
   - System Overview and Architecture
   - Data Flow Diagrams
   - Trust Boundaries
   - STRIDE Analysis
   - Attack Trees
   - Threat Scenarios
   - Mitigation Strategies
   - Monitoring and Detection

---

## 8. Implementation Strategy

### 8.1 Phased Deployment Plan

**Phase 0: Foundation (Weeks 1-2)**
- Team assembly and role assignment
- Development environment setup
- Git repository initialization
- CI/CD pipeline configuration
- Standards and conventions documentation

**Phase 1: Infrastructure (Weeks 3-5)**
- Docker Compose for local development
- Kubernetes cluster setup (production)
- PostgreSQL with RLS configuration
- Neo4j Enterprise multi-database setup
- MinIO object storage
- Monitoring stack (Prometheus, Grafana, ELK)

**Phase 2: Backend Core (Weeks 6-9)**
- FastAPI skeleton with auth middleware
- Multi-tenant context management
- PostgreSQL migrations (Alembic)
- RBAC implementation
- Audit logging
- RESTful API endpoints (users, clients, projects)
- GraphQL endpoint foundation

**Phase 3: Knowledge Graph Schema (Weeks 10-13)**
- UCO ontology implementation in SPG-Schema
- ICS and IEC 62443 schema extensions
- ISO 57000 requirement schema
- Schema validation and testing
- Neo4j schema constraints and indexes
- Cross-database linking patterns

**Phase 4: Data Ingestion (Weeks 14-18)**
- NVD CVE/CWE/CAPEC loader (scheduled daily)
- MITRE ATT&CK STIX 2.1 ingestion
- IEC 62443 standards loader
- ISO 57000 requirements loader
- OneKE document processing pipeline
- CMMS/Asset Management connectors
- STIX/TAXII feed integration

**Phase 5: Knowledge Construction (Weeks 19-23)**
- Entity resolution algorithms
- Semantic alignment (concept normalization)
- Relationship inference rules
- Data quality validation
- Incremental update mechanisms
- Vector embeddings generation (Milvus)

**Phase 6: Reasoning & Analytics (Weeks 24-27)**
- KAG-Solver configuration and tuning
- Attack path analysis algorithms
- Risk propagation models
- Compliance checking logic
- Graph analytics (centrality, community detection)
- Agent Zero API implementation

**Phase 7: Frontend Development (Weeks 28-33)**
- Next.js App Router setup
- shadcn/ui component library integration
- Consultant dashboard (multi-client view)
- Client-specific dashboards
- Risk assessment UI
- Threat modeling interface
- Pentest coordination UI
- Document generation UI
- Visualization components (graph, charts)

**Phase 8: API & Integration (Weeks 34-37)**
- Complete RESTful API
- GraphQL API with subscriptions
- SIEM integration endpoints
- Agent Zero webhook handlers
- CMMS synchronization service
- Network discovery tool integrations
- Document export API (PDF, DOCX, CSV)

**Phase 9: Security Hardening (Weeks 38-40)**
- Security audit and penetration testing
- RBAC verification
- Multi-tenant isolation testing
- SSO integration (SAML, OIDC)
- MFA enforcement
- Secrets management (Vault)
- Data encryption verification

**Phase 10: QA & Testing (Weeks 41-44)**
- Unit testing (>80% coverage)
- Integration testing
- End-to-end testing (Playwright)
- Performance testing (load, stress)
- Security testing (OWASP Top 10)
- Compliance validation
- User acceptance testing

**Phase 11: Documentation & Training (Weeks 45-46)**
- User documentation (consultants, admins)
- API documentation (Swagger/OpenAPI)
- System administration guide
- Deployment runbooks
- Training materials and videos
- Knowledge base articles

**Phase 12: Production Deployment (Weeks 47-48)**
- Production environment provisioning
- Data migration (if applicable)
- High-availability configuration
- Backup and disaster recovery testing
- Monitoring and alerting setup
- Go-live and handoff
- Post-deployment support

**Total Duration: 48 weeks (~12 months)**

### 8.2 Team Structure and Roles

```yaml
Team Composition (15-20 people):

Leadership:
  - Project Manager (1)
  - Technical Architect (1)
  - Cybersecurity Domain Expert (1)

Backend Development:
  - Backend Lead (1)
  - Backend Developers (3)
  - Database Administrator (1)

Knowledge Graph Engineering:
  - KG Engineer Lead (1)
  - KG Engineers (2)
  - Ontology Designer (1)

Frontend Development:
  - Frontend Lead (1)
  - Frontend Developers (2)
  - UX/UI Designer (1)

DevOps & Infrastructure:
  - DevOps Engineer (1)
  - Site Reliability Engineer (1)

Data & Integration:
  - Data Engineer (1)
  - Integration Specialist (1)

Quality & Security:
  - QA Lead (1)
  - QA Engineers (2)
  - Security Engineer (1)

Documentation & Training:
  - Technical Writer (1)
  - Training Specialist (1)
```

### 8.3 Technology Stack Summary

```yaml
Frontend:
  framework: Next.js 14+ (App Router)
  ui_library: shadcn/ui
  styling: Tailwind CSS
  state: Zustand
  data_fetching: React Query / SWR
  visualization: D3.js, Recharts, React Flow

Backend:
  framework: FastAPI (Python 3.11+)
  orm: SQLAlchemy
  migrations: Alembic
  validation: Pydantic
  async: asyncio, aiohttp

Knowledge Graph:
  engine: OpenSPG (latest stable)
  reasoning: KAG Framework
  extraction: OneKE
  storage: Neo4j Enterprise 5.x
  ontology: Unified Cybersecurity Ontology (UCO)

Databases:
  relational: PostgreSQL 16+ (Row-Level Security)
  graph: Neo4j Enterprise 5.x (multi-database)
  vector: Milvus or Qdrant
  cache: Redis

Storage:
  object_storage: MinIO (S3-compatible)

AI/ML:
  llm: OpenAI GPT-4 / Azure OpenAI / Local (LLaMA, Qwen)
  embeddings: OpenAI text-embedding-3-large / Local
  ocr: Tesseract, Azure Document Intelligence
  diagram_parsing: Custom AI model + OneKE

Messaging & Events:
  message_broker: RabbitMQ or Apache Kafka
  task_queue: Celery with Redis backend

Monitoring & Observability:
  metrics: Prometheus
  dashboards: Grafana
  logging: ELK Stack (Elasticsearch, Logstash, Kibana)
  tracing: OpenTelemetry
  apm: Sentry

Infrastructure:
  containers: Docker
  orchestration: Kubernetes (production), Docker Compose (dev)
  ci_cd: GitHub Actions or GitLab CI
  secrets: HashiCorp Vault
  registry: Docker Hub or Harbor

Testing:
  unit: pytest (Python), Jest (JavaScript)
  integration: pytest with fixtures
  e2e: Playwright
  load: Locust or k6
  security: OWASP ZAP, Bandit

Documentation:
  api: OpenAPI (Swagger UI)
  code: Sphinx (Python), JSDoc (JavaScript)
  user: Markdown, Docusaurus
```

---

## 9. Data Flow Diagrams

### 9.1 End-to-End Query Flow

```
┌──────────────┐
│  Consultant  │
│  Dashboard   │
└──────┬───────┘
       │ Natural Language Query:
       │ "What are the critical ICS assets with unpatched CVEs in Zone Level 1?"
       ↓
┌──────────────────────────────────┐
│  Next.js Frontend                │
│  - Parse query                   │
│  - Set client context            │
│  - Send to API                   │
└──────┬───────────────────────────┘
       │ POST /api/v1/query/natural-language
       │ Authorization: Bearer <JWT>
       │ X-Client-ID: client_001
       ↓
┌──────────────────────────────────┐
│  FastAPI Backend                 │
│  - Validate JWT                  │
│  - Set tenant context (RLS)      │
│  - Route to KAG service          │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│  KAG-Solver                      │
│  - Logical form decomposition    │
│  - Query planning                │
│  - Knowledge boundary detection  │
└──────┬───────────────────────────┘
       │ Multi-hop Cypher queries
       ↓
┌──────────────────────────────────┐
│  Neo4j (Client Database)         │
│  - Execute graph traversal       │
│  - Join with shared threat DB    │
│  - Return structured results     │
└──────┬───────────────────────────┘
       │ Results
       ↓
┌──────────────────────────────────┐
│  KAG-Model                       │
│  - Synthesize answer             │
│  - Generate natural language     │
│  - Include evidence links        │
└──────┬───────────────────────────┘
       │ Enriched Answer
       ↓
┌──────────────────────────────────┐
│  FastAPI Response Formatting     │
│  - Add metadata                  │
│  - Log to audit table            │
│  - Cache if appropriate          │
└──────┬───────────────────────────┘
       │ JSON Response
       ↓
┌──────────────────────────────────┐
│  Next.js Frontend                │
│  - Render answer                 │
│  - Display graph visualization   │
│  - Show evidence links           │
│  - Enable drill-down             │
└──────────────────────────────────┘
       │
       ↓
┌──────────────┐
│  Consultant  │
│  Views Result│
└──────────────┘
```

### 9.2 Document Generation Flow

```
┌──────────────┐
│  Consultant  │
│  Initiates   │
│  Report Gen  │
└──────┬───────┘
       │ "Generate IEC 62443 Gap Analysis for Client XYZ, Zones 1-3"
       ↓
┌──────────────────────────────────┐
│  Frontend - Report UI            │
│  - Select template               │
│  - Choose zones/assets           │
│  - Set report options            │
└──────┬───────────────────────────┘
       │ POST /api/v1/documents/generate
       ↓
┌──────────────────────────────────┐
│  FastAPI - Document Service      │
│  - Validate permissions          │
│  - Create task in Celery         │
│  - Return task_id                │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│  Celery Worker - Doc Generator   │
│  Step 1: Query compliance data   │
└──────┬───────────────────────────┘
       │ Multi-hop KG queries
       ↓
┌──────────────────────────────────┐
│  Neo4j + PostgreSQL              │
│  - Compliance status             │
│  - Asset inventory               │
│  - Vulnerability data            │
│  - Assessment history            │
└──────┬───────────────────────────┘
       │ Structured data
       ↓
┌──────────────────────────────────┐
│  Celery Worker                   │
│  Step 2: LLM-based text generation│
└──────┬───────────────────────────┘
       │ Executive summary, recommendations
       ↓
┌──────────────────────────────────┐
│  OpenAI / Local LLM              │
│  - Generate prose sections      │
│  - Summarize findings            │
│  - Create recommendations        │
└──────┬───────────────────────────┘
       │ Generated text
       ↓
┌──────────────────────────────────┐
│  Celery Worker                   │
│  Step 3: Document assembly       │
│  - Merge data + generated text   │
│  - Apply DOCX template           │
│  - Insert charts/graphs          │
│  - Add evidence artifacts        │
└──────┬───────────────────────────┘
       │ DOCX file
       ↓
┌──────────────────────────────────┐
│  PDF Converter                   │
│  - Convert DOCX to PDF           │
│  - Add watermarks/headers        │
└──────┬───────────────────────────┘
       │ PDF file
       ↓
┌──────────────────────────────────┐
│  MinIO Object Storage            │
│  - Store PDF                     │
│  - Generate presigned URL        │
└──────┬───────────────────────────┘
       │ S3 path
       ↓
┌──────────────────────────────────┐
│  PostgreSQL - Documents Table    │
│  - Insert metadata record        │
│  - Link to project/client        │
└──────┬───────────────────────────┘
       │ Document ID
       ↓
┌──────────────────────────────────┐
│  Celery Worker                   │
│  - Mark task complete            │
│  - Notify via WebSocket          │
└──────┬───────────────────────────┘
       │ WebSocket message
       ↓
┌──────────────────────────────────┐
│  Frontend - Real-time Update     │
│  - Show notification             │
│  - Enable download button        │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────┐
│  Consultant  │
│  Downloads   │
│  Report PDF  │
└──────────────┘
```

---

## 10. Non-Functional Requirements

### 10.1 Performance Requirements

- **Query Response Time**: < 2 seconds (90th percentile) for standard KG queries
- **Complex Reasoning**: < 5 seconds (90th percentile) for multi-hop attack path analysis
- **NL Query Latency**: < 3 seconds (95th percentile) end-to-end
- **Agent Zero API**: < 500ms (95th percentile) for KG query/update operations
- **Document Generation**: < 2 minutes for 50-page compliance reports
- **Graph Scale**: Support 50M+ nodes, 200M+ relationships per client database
- **Concurrent Users**: 50+ consultants working simultaneously
- **Data Ingestion**: Process 10K+ CVE updates per day without service degradation

### 10.2 Scalability Requirements

- **Client Scalability**: Support 100+ concurrent client databases
- **Asset Scaling**: Handle 100K+ assets per client organization
- **Vulnerability Database**: 500K+ CVE entries with daily updates
- **Horizontal Scaling**: Ability to add compute nodes for query processing
- **Storage Growth**: 10TB+ total graph data with efficient query performance
- **Agent Parallelization**: 10+ concurrent Agent Zero pentesting sessions

### 10.3 Availability Requirements

- **System Uptime**: 99.5% during business hours (9am-6pm local time)
- **Planned Maintenance**: < 4 hours per month during off-peak hours
- **Backup Frequency**: Nightly incremental, weekly full backups
- **Recovery Time Objective (RTO)**: < 4 hours for critical services
- **Recovery Point Objective (RPO)**: < 24 hours (daily backup window)
- **Disaster Recovery**: Multi-region failover capability (production)

### 10.4 Security Requirements

- **Authentication**: Multi-factor authentication (MFA) required for all users
- **Authorization**: Role-based access control (RBAC) with least privilege
- **Data Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Multi-Tenancy**: Complete data isolation between clients (PostgreSQL RLS + Neo4j multi-DB)
- **Audit Logging**: 7-year retention of all data access and modifications
- **Vulnerability Scanning**: Weekly automated scans of application and infrastructure
- **Penetration Testing**: Annual third-party security assessments
- **Compliance**: SOC 2 Type II, GDPR, IEC 62443 security requirements applicable to tool itself

### 10.5 Compliance Requirements

- **IEC 62443 Evidence**: Automatic collection and storage of compliance evidence artifacts
- **ISO 57000**: Built-in templates and workflows for rail security standards
- **Audit Trails**: Immutable logs of all consultant actions and KG modifications
- **Data Retention**: Configurable per-client retention policies (default: 7 years)
- **Export Capabilities**: Full data export in standard formats (JSON, CSV, STIX) for portability
- **Right to Deletion**: GDPR-compliant mechanisms for client data deletion requests

---

## 11. Architecture Decision Records (ADRs)

### ADR-001: Multi-Tenant Database Strategy

**Status**: Accepted
**Date**: 2025-10-26
**Decision**: Hybrid multi-tenancy with PostgreSQL schema-per-tenant + RLS and Neo4j multi-database

**Context**: Need complete data isolation between clients while sharing common threat intelligence.

**Options Considered**:
1. Single shared database with tenant_id filtering
2. Separate database per client (PostgreSQL + Neo4j)
3. Hybrid: Shared threat DB + per-client databases

**Decision**: Option 3 (Hybrid)

**Rationale**:
- PostgreSQL RLS provides strong isolation with query-level enforcement
- Neo4j multi-database allows shared threat intel (CVE, ATT&CK) accessible to all clients
- Client-specific graphs remain completely isolated
- Simplifies threat intelligence updates (single shared DB)
- Enables cross-client analytics while preserving privacy

**Consequences**:
- ✅ Strong tenant isolation guarantees
- ✅ Efficient threat intelligence sharing
- ✅ Simplified compliance with data privacy regulations
- ⚠️ Increased complexity in query routing
- ⚠️ Neo4j Enterprise required for multi-database feature

---

### ADR-002: OpenSPG + KAG Framework vs. Pure Neo4j

**Status**: Accepted
**Date**: 2025-10-26
**Decision**: Use OpenSPG with KAG framework as primary knowledge graph platform, with Neo4j as storage backend

**Context**: Need advanced reasoning, semantic alignment, and LLM integration for cybersecurity knowledge graph.

**Options Considered**:
1. Pure Neo4j with custom reasoning layer
2. Apache Jena (RDF/OWL) with SPARQL
3. OpenSPG + KAG with Neo4j storage

**Decision**: Option 3 (OpenSPG + KAG)

**Rationale**:
- KAG-Solver provides logical form-guided multi-hop reasoning out-of-the-box
- SPG-Schema enables semantic modeling with UCO ontology
- OneKE optimized for document extraction from security reports
- Semantic alignment reduces false positives from entity extraction
- Knowledge boundary detection optimizes LLM vs. KG retrieval
- Neo4j storage provides performance and visualization
- Active development by Ant Group with enterprise backing

**Consequences**:
- ✅ Advanced reasoning capabilities without custom development
- ✅ Built-in LLM integration and optimization
- ✅ Semantic alignment and concept normalization
- ✅ Leverage Neo4j ecosystem (Bloom, GDS)
- ⚠️ Smaller community compared to pure Neo4j
- ⚠️ Learning curve for SPG framework concepts
- ⚠️ Potential abstraction overhead vs. direct Neo4j queries

---

### ADR-003: Unified Cybersecurity Ontology (UCO) as Schema Foundation

**Status**: Accepted
**Date**: 2025-10-26
**Decision**: Adopt UCO as the base ontology, extended with ICS/IEC 62443/ISO 57000 concepts

**Context**: Need standardized, interoperable schema for cybersecurity knowledge representation.

**Options Considered**:
1. Custom proprietary ontology
2. MITRE ATT&CK-only schema
3. UCO (Unified Cybersecurity Ontology) + extensions

**Decision**: Option 3 (UCO + extensions)

**Rationale**:
- UCO developed by academic/industry collaboration (University of Maryland, Johns Hopkins, MITRE)
- Covers broad cybersecurity domains (assets, vulnerabilities, threats, attacks, defenses)
- Interoperable with STIX 2.1, MITRE ATT&CK, CVE, CWE
- Extensible design allows domain-specific additions (ICS, rail)
- Growing adoption in cybersecurity research and tools

**Consequences**:
- ✅ Standards-based, interoperable schema
- ✅ Proven coverage of core cybersecurity concepts
- ✅ Active development and community support
- ✅ Easier integration with external threat intelligence
- ⚠️ Requires extension for ICS and compliance domains
- ⚠️ May need mapping for some existing internal schemas

---

### ADR-004: Agent Zero Integration via RESTful API

**Status**: Accepted
**Date**: 2025-10-26
**Decision**: Integrate Agent Zero autonomous pentesting AI through dedicated RESTful API with sub-500ms SLA

**Context**: Need real-time knowledge graph access for AI-driven penetration testing with attack path planning.

**Options Considered**:
1. Direct Neo4j Cypher queries from Agent Zero
2. GraphQL API with subscriptions
3. RESTful API with optimized endpoints

**Decision**: Option 3 (RESTful API)

**Rationale**:
- RESTful API provides clear contract and versioning
- Dedicated endpoints can be highly optimized for specific use cases (attack path selection, exploit matching)
- Easier to implement rate limiting and security controls
- Simpler authentication and authorization model
- Caching layer can be inserted transparently
- Sub-500ms latency achievable with proper indexing and query optimization

**Consequences**:
- ✅ Clear API contract for Agent Zero integration
- ✅ Performance optimization through specialized endpoints
- ✅ Simplified security and rate limiting
- ✅ Easier to evolve independently from general KG API
- ⚠️ Additional API endpoints to maintain
- ⚠️ Need careful performance tuning to meet latency SLA

---

## 12. Deployment Architecture

### 12.1 Development Environment

```yaml
# docker-compose.yml (Development)
version: '3.8'

services:
  cgip-frontend:
    image: node:20-alpine
    volumes:
      - ./cgip-frontend:/app
    ports:
      - "3000:3000"
    command: npm run dev
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

  cgip-api:
    image: python:3.11-slim
    volumes:
      - ./cgip-api:/app
    ports:
      - "8000:8000"
    command: uvicorn main:app --reload --host 0.0.0.0
    environment:
      - DATABASE_URL=postgresql://cgip:cgip@postgres:5432/cgip
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=cgip_neo4j_password
    depends_on:
      - postgres
      - neo4j
      - redis

  postgres:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=cgip
      - POSTGRES_USER=cgip
      - POSTGRES_PASSWORD=cgip

  neo4j:
    image: neo4j:5-enterprise
    volumes:
      - neo4j_data:/data
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/cgip_neo4j_password
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
      - NEO4J_server_memory_heap_initial__size=2G
      - NEO4J_server_memory_heap_max__size=4G

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  openspg-server:
    image: openspg/openspg:0.5.0
    ports:
      - "8887:8887"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=cgip_neo4j_password
    depends_on:
      - neo4j

  milvus:
    image: milvusdb/milvus:latest
    ports:
      - "19530:19530"
    volumes:
      - milvus_data:/var/lib/milvus

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=cgip
      - MINIO_ROOT_PASSWORD=cgip_minio_password
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  neo4j_data:
  milvus_data:
  minio_data:
```

### 12.2 Production Kubernetes Architecture

```yaml
# High-level Kubernetes deployment structure

Namespace: cgip-production

Deployments:
  - cgip-frontend (3 replicas)
    - Next.js application
    - Resources: 2 CPU, 2GB RAM per pod
    - Horizontal Pod Autoscaler: 3-10 pods based on CPU/memory

  - cgip-api (5 replicas)
    - FastAPI application
    - Resources: 4 CPU, 8GB RAM per pod
    - HPA: 5-20 pods

  - openspg-server (3 replicas)
    - OpenSPG knowledge graph engine
    - Resources: 8 CPU, 16GB RAM per pod
    - HPA: 3-10 pods

  - celery-workers (10 replicas)
    - Document generation and async tasks
    - Resources: 4 CPU, 8GB RAM per pod
    - HPA: 10-50 pods

StatefulSets:
  - postgres-primary (1 replica)
    - PostgreSQL 16 with RLS
    - Resources: 16 CPU, 64GB RAM
    - Persistent Volume: 1TB SSD

  - postgres-replicas (2 replicas)
    - Read replicas for query load distribution

  - neo4j-cluster (3 replicas)
    - Neo4j Enterprise cluster
    - Resources: 32 CPU, 128GB RAM per instance
    - Persistent Volume: 2TB SSD per instance

  - redis-cluster (3 replicas)
    - Redis for caching and Celery broker
    - Resources: 8 CPU, 16GB RAM per instance

Services:
  - LoadBalancer:
    - cgip-frontend-lb (HTTPS, port 443)
    - cgip-api-lb (HTTPS, port 443)

  - ClusterIP:
    - postgres-svc
    - neo4j-svc
    - redis-svc
    - openspg-svc
    - minio-svc
    - milvus-svc

Ingress:
  - NGINX Ingress Controller
  - TLS termination with Let's Encrypt
  - Rate limiting (1000 req/min per IP)
  - WAF rules (OWASP ModSecurity CRS)

ConfigMaps:
  - application-config (env vars, feature flags)
  - neo4j-config (database tuning)
  - nginx-config (ingress rules)

Secrets:
  - database-credentials (managed by HashiCorp Vault)
  - api-keys (OpenAI, external services)
  - tls-certificates

Persistent Volumes:
  - postgres-pv: 1TB SSD (primary), 500GB SSD (replicas)
  - neo4j-pv: 2TB SSD per cluster node
  - minio-pv: 5TB object storage
  - milvus-pv: 1TB SSD
```

---

## 13. Monitoring and Observability

### 13.1 Metrics Collection

```yaml
# Prometheus metrics to collect

Application Metrics:
  # API Performance
  - http_request_duration_seconds (histogram)
  - http_requests_total (counter)
  - active_requests (gauge)

  # Knowledge Graph
  - kg_query_duration_seconds (histogram)
  - kg_query_errors_total (counter)
  - kg_nodes_traversed (histogram)
  - kg_reasoning_steps (histogram)

  # Agent Zero Integration
  - agent_zero_api_latency (histogram)
  - agent_zero_attack_paths_generated (counter)
  - agent_zero_exploits_matched (counter)

  # Document Generation
  - document_generation_duration_seconds (histogram)
  - documents_generated_total (counter)
  - document_generation_errors (counter)

  # Multi-Tenancy
  - active_clients (gauge)
  - queries_per_client (counter)
  - client_data_size_bytes (gauge)

Infrastructure Metrics:
  # Database
  - postgres_connections_active (gauge)
  - postgres_query_duration_seconds (histogram)
  - neo4j_heap_memory_usage (gauge)
  - neo4j_page_cache_hit_ratio (gauge)

  # Kubernetes
  - pod_cpu_usage (gauge)
  - pod_memory_usage (gauge)
  - pod_restart_count (counter)
  - hpa_current_replicas (gauge)
```

### 13.2 Grafana Dashboards

**Dashboard 1: Platform Overview**
- Total active clients
- Total consultants online
- Requests per second
- Average response time
- Error rate
- Top queries by frequency

**Dashboard 2: Knowledge Graph Health**
- Query latency (p50, p95, p99)
- Neo4j cluster status
- Graph size (nodes, relationships)
- Ingestion rate (CVE updates/day)
- Reasoning performance
- Cache hit rates

**Dashboard 3: Multi-Tenant Metrics**
- Clients by activity level
- Storage usage per client
- Query distribution by client
- Tenant isolation verification
- Cross-tenant performance comparison

**Dashboard 4: Agent Zero Integration**
- Active pentest sessions
- Attack paths analyzed
- Exploits matched per session
- API latency (KG query/update)
- Success rate of simulations
- Learning feedback metrics

**Dashboard 5: Compliance & Audit**
- IEC 62443 assessments completed
- ISO 57000 reports generated
- Documents generated per type
- Compliance evidence artifacts collected
- Audit log entries per day

---

## 14. Disaster Recovery and Business Continuity

### 14.1 Backup Strategy

```yaml
PostgreSQL Backups:
  Full Backup:
    frequency: Weekly (Sunday 2am UTC)
    retention: 4 weeks
    method: pg_dump with compression
    destination: S3 bucket with versioning

  Incremental Backup:
    frequency: Daily (2am UTC)
    retention: 7 days
    method: WAL archiving
    destination: S3 bucket

  Point-in-Time Recovery:
    capability: Yes (via WAL archiving)
    max_recovery_window: 7 days

Neo4j Backups:
  Full Backup:
    frequency: Daily (3am UTC)
    retention: 14 days
    method: neo4j-admin database dump
    destination: S3 bucket with versioning

  Client Database Rotation:
    frequency: Weekly per client database
    retention: 4 weeks per client

  Shared Threat Intel DB:
    frequency: After each major ingestion
    retention: Last 10 versions

MinIO Object Storage:
  Versioning: Enabled (all documents)
  Replication: Cross-region to DR site
  Retention: Permanent (unless client deletion request)

Disaster Recovery Testing:
  frequency: Quarterly
  scope: Full restore to DR environment
  RTO validation: < 4 hours
  RPO validation: < 24 hours
```

### 14.2 Failover Procedures

```yaml
Primary Site Failure Scenario:

Detection:
  - Prometheus alerts on site unavailability
  - Automatic health checks fail (3 consecutive)
  - Ops team paged (PagerDuty)

Failover Steps:
  1. Verify primary site is unrecoverable (< 5 minutes)
  2. Activate DR site in secondary region (automated)
  3. Update DNS to point to DR site (Route53 health checks)
  4. Restore PostgreSQL from latest backup if needed
  5. Restore Neo4j from latest backup if needed
  6. Verify application functionality (smoke tests)
  7. Communicate to stakeholders (status page)

Expected Downtime: 2-4 hours

Fallback Plan:
  - Read-only mode if partial failure
  - Manual intervention if automated failover fails
  - Degraded mode with cached data
```

---

## Conclusion

This architecture document provides a comprehensive blueprint for building a state-of-the-art, multi-tenant cybersecurity knowledge base platform. By leveraging **OpenSPG with KAG framework** for advanced reasoning, **Neo4j Enterprise** for scalable graph storage, and the **Unified Cybersecurity Ontology (UCO)** for semantic richness, the system will deliver:

✅ **Advanced Threat Analysis**: Multi-hop attack path reasoning and risk propagation
✅ **Compliance Automation**: IEC 62443 and ISO 57000 assessment workflows
✅ **Autonomous Penetration Testing**: Agent Zero integration for AI-driven security testing
✅ **Multi-Tenant Security**: Complete data isolation with shared threat intelligence
✅ **Automated Documentation**: AI-powered report generation for consultants
✅ **Enterprise Scalability**: Support 50M+ nodes, 100+ clients, 50+ concurrent users

**Implementation Timeline**: 12 months
**Team Size**: 15-20 people
**Technology Stack**: Next.js, FastAPI, PostgreSQL, Neo4j, OpenSPG, KAG, OneKE, UCO

**Next Steps:**
1. Assemble development team
2. Set up development infrastructure (Phase 0-1)
3. Begin UCO schema design and validation (Phase 3)
4. Implement data ingestion pipelines (Phase 4)
5. Iterate through phases 5-12 according to timeline

---

**Document Status**: COMPLETE
**Ready for Development**: YES
**Review Status**: Pending Stakeholder Approval
**Version Control**: Git repository to be initialized in Phase 0

For questions or clarifications, contact the Architecture Team.
