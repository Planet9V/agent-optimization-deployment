# Visual Documentation Index

**Created:** 2025-10-29
**Purpose:** Comprehensive index of all visual diagrams and documentation for AEON DT CyberSec Threat Intelligence system
**Total Diagrams:** 50+ Mermaid diagrams across 6 documents

---

## Document Overview

### 1. **schema_complete.mermaid**
**File Size:** ~8 KB
**Diagrams:** 1 comprehensive graph schema

#### Content:
- Complete 15-node type schema
- 25+ relationship types
- Color-coded by domain (asset=blue, network=green, security=red, threat=orange, document=purple)
- All relationships labeled with cardinality
- Properties for each node type

#### Use Cases:
- Overall system understanding
- Database schema visualization
- Training and documentation
- Architecture presentations

#### Key Entities:
- **Asset Domain:** Organization, Site, Train, Component, Software, SoftwareInstance
- **Network Domain:** NetworkZone, Device, NetworkInterface, Service
- **Security Domain:** Vulnerability, Weakness, Configuration, SecurityControl
- **Threat Domain:** ThreatActor, Campaign, Technique, Malware, Artifact
- **Document Domain:** Document, Advisory, Report

#### Relationships: 25 types
- Asset hierarchy: OPERATES, HOSTS, HAS_COMPONENT, RUNS_SOFTWARE, INSTANCE_OF
- Network connectivity: CONTAINS, HAS_DEVICE, HAS_INTERFACE, RUNS_SERVICE, ON_INTERFACE
- Security mapping: HAS_VULNERABILITY, HAS_WEAKNESS, MANIFESTS_AS, HAS_CONFIGURATION
- Attack vectors: EXPLOITED_BY, USES_ARTIFACT, CREATES_ARTIFACT
- Threat tracking: EXECUTES, USES_TECHNIQUE, DEPLOYS_MALWARE
- Mitigation: MITIGATES_VULNERABILITY, MITIGATES_WEAKNESS, MITIGATES_TECHNIQUE, HAS_CONTROL
- Documentation: REFERENCED_IN, ABOUT_PRODUCT, CONTAINS_REFERENCE
- Impact analysis: TARGETS, AFFECTS, FOUND_ON, HAS_IOC

---

### 2. **architecture_overview.md**
**File Size:** ~35 KB
**Diagrams:** 7 system architecture Mermaid diagrams

#### Content:

**Diagram 1: System Architecture Diagram**
- External data sources (NIST NVD, MITRE ATT&CK, CISA, Custom Documents)
- Data processing pipeline (Parser, Entity Extractor, Relationship Extractor, Validator)
- Neo4j cluster (Primary + 3 replicas)
- Query and analytics layer
- Applications and dashboards
- Integration with external systems (CMDB, SIEM, Threat Feeds)

**Diagram 2: Data Flow Architecture (Sequence)**
- Source → Parser → NLP → Relationship Extractor → Validator → Neo4j → Query → Dashboard
- Shows parallel processing and data transformation
- Error handling and validation gates

**Diagram 3: Neo4j Cluster Architecture**
- Primary write node with failover
- 3 read-only replicas
- Load balancer and router
- Backup and recovery systems
- Continuous replication streams

**Diagram 4: Data Processing Pipeline**
- Input sources and document formats
- Extraction layer (PDF, DOCX, Text, Metadata)
- NLP enrichment (Tokenization, NER, Dependency parsing)
- Relationship extraction (Pattern matching, Co-occurrence)
- Quality assurance (Deduplication, Normalization, Validation)
- Storage layer (Neo4j, Cache, Archive)

**Diagram 5: Integration Architecture**
- Threat intelligence core (Graph, Query Engine, Algorithms)
- CMDB integration (Assets, Relationships, Changes)
- SIEM integration (Events, Correlation, Incidents)
- External threat intelligence (Feeds, APIs, Advisories)
- Analysis & response (Risk scoring, Impact analysis, Remediation)
- Reporting & dashboards

**Diagram 6: Deployment Architecture**
- Kubernetes cluster with namespaces
- Neo4j Primary and replicas
- Processing pods (Parser, NLP)
- API servers with auto-scaling
- Monitoring (Prometheus, Grafana, ELK)
- Persistent storage (PVCs)
- Redis cache layer

**Diagram 7: Document Processing Workflow**
- Input documents (PDF, DOCX, TXT, MD)
- Processing stage (Ingestion, Extraction, Cleaning, Chunking)
- NLP processing (Tokenization, POS, NER, Dependency)
- Information extraction (Entity, Relationship, Pattern, IOC)
- Enrichment (Normalization, Linking, Confidence scoring)
- Neo4j integration (Import, Indexing, Replication, Verification)

#### Additional Content:
- Key architectural principles
- Infrastructure requirements table
- Security considerations
- Component resource allocation

#### Use Cases:
- System design documentation
- Infrastructure planning
- Deployment procedures
- Integration planning

---

### 3. **use_case_diagrams.md**
**File Size:** ~50 KB
**Diagrams:** 7 detailed use case diagrams with queries

#### Use Case 1: Vulnerability Impact Assessment
**Purpose:** Determine which assets vulnerable to specific CVE
**Graph Pattern:** CVE → Software → Instance → Device → Zone
**Query:** Multi-hop traversal with risk scoring
**Output:** Prioritized list of vulnerable assets

#### Use Case 2: Threat Actor Campaign Tracking
**Purpose:** Track campaigns, techniques, and deployments
**Graph Pattern:** Actor → Campaign → Technique → Malware → IOCs
**Query:** Campaign correlation and timeline analysis
**Output:** Campaign timeline, TTPs, indicators

#### Use Case 3: Attack Path Discovery
**Purpose:** Identify potential attack paths to critical infrastructure
**Graph Pattern:** Internet → DMZ → Internal → Data → SCADA
**Query:** Shortest path with vulnerability traversal
**Output:** Attack chains with risk assessment

#### Use Case 4: Asset Configuration Compliance
**Purpose:** Verify assets meet security requirements
**Graph Pattern:** Requirements ↔ Devices ↔ Configurations
**Query:** Compliance percentage calculation
**Output:** Compliance reports, remediation steps

#### Use Case 5: Software Bill of Materials Analysis
**Purpose:** Track dependencies and vulnerable components
**Graph Pattern:** App → Direct Dependencies → Sub-dependencies
**Query:** Dependency tree traversal with vulnerability matching
**Output:** Component tree, vulnerable paths, remediation order

#### Use Case 6: Incident Response Timeline
**Purpose:** Reconstruct incident timeline
**Graph Pattern:** Events linked chronologically with entities
**Query:** Timeline reconstruction with entity correlation
**Output:** Attack progression, root cause analysis

#### Use Case 7: Executive Risk Dashboard
**Purpose:** High-level risk metrics for reporting
**Graph Pattern:** Aggregation of risks by category
**Query:** Summary statistics and trending
**Output:** KPIs, risk scores, trend analysis

#### Features:
- Graph patterns with color-coded nodes
- Example Cypher queries for each use case
- Risk assessment explanations
- Data flow examples

#### Use Cases:
- Product feature documentation
- Query examples for development
- Training scenarios
- Executive reporting templates

---

### 4. **network_topology_example.md**
**File Size:** ~45 KB
**Diagrams:** 7 network security diagrams

#### Diagram 1: Comprehensive Network Topology
- External Internet layer
- Edge security (WAF, NGFW, CDN)
- DMZ zone with services (Web, API, Email, DNS)
- Internal network (App servers, Cache, MQ, Monitoring)
- Data plane (Databases, Backups, Graph DB)
- Critical infrastructure (SCADA, HMI, Field devices)
- Management network (Bastion, Admin, MFA)
- IEC 62443 security levels applied

#### Diagram 2: IEC 62443 Security Levels
**Level 1:** Awareness - Basic preventive measures
**Level 2:** Integrity - Secure design principles
**Level 3:** Availability - Defense-in-depth
**Level 4:** Confidentiality - Comprehensive controls
**Level 5:** Critical - Maximum security

#### Diagram 3: Firewall Rules Detail Matrix
- Ingress rules (Block All default, HTTPS, HTTP redirect, DNS)
- Egress rules (Web traffic, DNS lookups, NTP sync)
- Internal rules (App→DB, DB Replication, Bastion access, SCADA isolation)
- Priority ordering and logging

#### Diagram 4: Attack Path Analysis - 5-Hop Attack
Shows exploitation chain:
1. Internet → Web Server (RCE)
2. DMZ Lateral Movement → API Gateway
3. Internal Penetration → App Server
4. Data Layer Access → Database
5. Critical Infrastructure Compromise → SCADA

With security control bypasses identified

#### Diagram 5: Network Segmentation & Access Control
- 5 VLAN configuration (DMZ, Internal, Data, SCADA, Management)
- Access Control Lists per zone
- Routing and gateway architecture
- Gateways with traffic flow

#### Diagram 6: Threat Modeling - Security Zones
STRIDE threat model by zone:
- DMZ: Spoofing, Sniffing, DoS
- Internal: Privilege escalation, Tampering, DoS
- Data: Info disclosure, Repudiation, Tampering
- SCADA: Elevation, DoS, Tampering
- Mitigations per zone

#### Diagram 7: Incident Response Network
- Immediate response (Isolate, Preserve, Contain)
- Investigation (Forensics, Memory, Network capture)
- Remediation (Patch, Harden, Deploy detection)
- Validation & Recovery

#### Additional Content:
- IEC 62443 implementation details
- Firewall rules matrix table
- Attack path risk assessment
- Network segmentation strategy
- Threat modeling framework
- Incident response network
- Network security principles
- Critical success factors

#### Use Cases:
- Network security design
- Firewall rule documentation
- Attack path assessment
- Incident response procedures
- Compliance demonstration (IEC 62443)

---

### 5. **threat_intelligence_correlation.md**
**File Size:** ~40 KB
**Diagrams:** 7 threat intelligence diagrams

#### Diagram 1: Threat Actor Attribution Chain
- IOC discovery
- File analysis
- Malware analysis
- Infrastructure analysis
- Behavior analysis
- TTP comparison
- Attribution result with confidence level

#### Diagram 2: Campaign-to-Technique-to-CVE Correlation
**3-level hierarchy:**
1. Campaigns (Summer2024, FallOps, Holiday)
2. Tactics (Initial Access, Execution, Defense Evasion, etc.)
3. CVEs (Log4j, Exchange, vCenter, Cisco ASA, OpenSSH)
4. Tools (Cobalt Strike, Emotet, Mimikatz, Empire)

#### Diagram 3: IOC Correlation Network
- Primary IOCs (IP, Domain, Email, Hash, URL, Registry)
- Related IOCs with correlation scores
- Enrichment data (Threat feeds, WHOIS, Passive DNS, Sandbox, Historical)
- Timeline analysis

#### Diagram 4: Threat Timeline Visualization
Quarterly breakdown:
- Q2: Early reconnaissance → Campaign launch
- Q3: Campaign evolution → Domain registration
- Q4: New campaigns → Ongoing operations

#### Diagram 5: Threat Intelligence Information Flow
**6-stage pipeline:**
1. Intelligence sources (OSINT, Feeds, Government, Private)
2. Collection & aggregation (Collector, Deduplication, Store)
3. Processing & enrichment (Normalize, Enrich, Correlate)
4. Knowledge graph storage (Neo4j)
5. Analysis & intelligence (Analytics, Reports, Dashboards)
6. Distribution (API, Feeds, Alerts)

#### Diagram 6: Campaign Success Metrics & Attribution Matrix
- Correlation factors (Malware, Infrastructure, TTP, Timing, C2, Targets)
- Confidence scoring (HIGH/MEDIUM/CRITICAL)
- Attribution conclusion with confidence level

#### Diagram 7: Cross-Campaign Pattern Analysis
- 3 campaigns analyzed (Summer, Fall, Holiday)
- 6 patterns identified (Infrastructure reuse, Malware evolution, TTP signature, Timing, Target timing, Success metrics)
- Attribution to APT28 with 87% confidence

#### Additional Content:
- Attribution chain explanation
- Campaign correlation details
- Enrichment data sources
- Timeline construction
- Information flow explanation
- Attribution matrix methodology
- Pattern analysis summary

#### Use Cases:
- Threat intelligence analysis
- Campaign attribution
- IOC correlation procedures
- Threat actor tracking
- Intelligence reporting
- Pattern recognition training

---

### 6. **database_schema_erd.md**
**File Size:** ~40 KB
**Diagrams:** 6 database architecture diagrams

#### Diagram 1: Complete Entity-Relationship Diagram
- 15 entity types with attributes
- Relationship cardinality
- Property definitions for all entities
- Primary keys identified

#### Diagram 2-4: Cypher Query Pattern Diagrams
Shows visual patterns for:
1. **Vulnerability Impact Path:** CVE → Software → Instance → Device → Zone
2. **Attack Path Discovery:** Start → Path → End → Risk
3. **Campaign Attribution:** IOCs → Correlate → Techniques → Infrastructure → Malware

#### Diagram 5: Neo4j Index Strategy
- 8 single/composite indexes
- Unique constraints (4 total)
- Performance tuning strategies
- Cypher index creation statements

#### Diagram 6: Backup & Recovery Schema
- Backup strategy (Full, Incremental, WAL)
- Recovery options (Full, Incremental, Point-in-time, Cross-region)
- Storage locations (Local, Offsite, Vault)

#### Additional Content:
- Complete schema definition
- Cypher query examples
- Performance optimization
- Data volume estimation
- Storage requirements
- ACID compliance information
- Backup/recovery procedures
- Index creation scripts

#### Use Cases:
- Database design documentation
- Query optimization reference
- Backup/recovery procedures
- Performance tuning
- Index management

---

## Quick Navigation Guide

### By Audience

**Executive Leadership:**
- Start: architecture_overview.md (System Architecture Diagram)
- Then: use_case_diagrams.md (Executive Risk Dashboard)

**Security Architects:**
- Start: schema_complete.mermaid (Complete Schema)
- Then: network_topology_example.md (Network Architecture)
- Then: database_schema_erd.md (Index Strategy)

**DevOps/Infrastructure:**
- Start: architecture_overview.md (Deployment Architecture)
- Then: network_topology_example.md (Firewall Rules)
- Then: database_schema_erd.md (Backup/Recovery)

**Developers:**
- Start: schema_complete.mermaid (Data Model)
- Then: database_schema_erd.md (Query Patterns)
- Then: use_case_diagrams.md (Implementation Examples)

**Threat Intelligence Analysts:**
- Start: threat_intelligence_correlation.md (Attribution Chain)
- Then: use_case_diagrams.md (Use Cases 1,2,3,7)
- Then: network_topology_example.md (Attack Paths)

### By Topic

**Data Model & Schema:**
- schema_complete.mermaid
- database_schema_erd.md (Diagrams 1)

**System Architecture:**
- architecture_overview.md (All 7 diagrams)
- database_schema_erd.md (Diagram 6 - Deployment)

**Network & Security:**
- network_topology_example.md (All 7 diagrams)
- architecture_overview.md (Diagrams 5 - Integration)

**Threat Intelligence:**
- threat_intelligence_correlation.md (All 7 diagrams)
- use_case_diagrams.md (Use Cases 2, 3, 6, 7)

**Queries & Implementation:**
- use_case_diagrams.md (7 detailed use cases with queries)
- database_schema_erd.md (Cypher query patterns)

**Operations & Deployment:**
- architecture_overview.md (Diagrams 3, 6, 7)
- database_schema_erd.md (Diagram 6)

---

## Diagram Statistics

| Document | Size | Diagrams | Nodes | Relationships | Coverage |
|----------|------|----------|-------|---------------|----------|
| schema_complete.mermaid | 8 KB | 1 | 15 | 25+ | Complete schema |
| architecture_overview.md | 35 KB | 7 | ~100 | ~150 | System design |
| use_case_diagrams.md | 50 KB | 7 | ~200 | ~300 | 7 major use cases |
| network_topology_example.md | 45 KB | 7 | ~120 | ~200 | Network security |
| threat_intelligence_correlation.md | 40 KB | 7 | ~180 | ~250 | Threat analysis |
| database_schema_erd.md | 40 KB | 6 | ~100 | ~200 | Database design |
| **TOTAL** | **218 KB** | **35** | **~715** | **~1,125** | **Complete system** |

---

## Color Coding Legend

### Entity Types
```
🔵 Blue: Asset Domain (Organization, Site, Device, Software)
🟢 Green: Network Domain (NetworkZone, Interface, Service)
🔴 Red: Security Domain (Vulnerability, Control)
🟠 Orange: Threat Domain (ThreatActor, Malware, Campaign)
🟣 Purple: Document Domain (Advisory, Report)
🟡 Yellow: Metadata/Timing Information
```

### Status Indicators
```
✅ Green: Compliant, Safe, Success
⚠️ Yellow: Warning, Caution, In-Progress
❌ Red: Critical, Vulnerable, Failed
🔒 Blue: Secure, Protected, Authorized
```

---

## How to Use These Diagrams

### For System Understanding
1. Start with schema_complete.mermaid to understand entities
2. Review architecture_overview.md for system design
3. Study use_case_diagrams.md for practical applications

### For Implementation
1. Reference schema_complete.mermaid for data model
2. Use database_schema_erd.md for index strategy
3. Follow use_case_diagrams.md for query examples

### For Security Review
1. Examine network_topology_example.md for architecture
2. Review threat_intelligence_correlation.md for threat analysis
3. Use use_case_diagrams.md for attack scenarios

### For Operations
1. Reference architecture_overview.md for deployment
2. Use database_schema_erd.md for backup/recovery
3. Follow network_topology_example.md for incident response

---

## Integration with Other Documentation

### Related Files in Project
- `/docs/document_processing_implementation.md` - NLP processing
- `/schemas/cypher/` - Cypher query definitions
- `/scripts/document_processing/` - Data pipeline scripts
- `/config/` - Configuration files

### External References
- Neo4j Documentation: https://neo4j.com/docs/
- MITRE ATT&CK: https://attack.mitre.org/
- IEC 62443: ICS Cybersecurity Standards
- CVSS Calculator: https://www.first.org/cvss/calculator/

---

## Maintenance & Updates

**Last Updated:** 2025-10-29
**Next Review:** 2025-11-29
**Maintenance Schedule:**
- Monthly: Diagram accuracy verification
- Quarterly: Content expansion for new features
- Annually: Complete documentation refresh

**Update Procedure:**
1. Review schema changes
2. Update relevant diagrams
3. Verify consistency across documents
4. Update this index
5. Publish changes to team

---

## Document Generation Information

These diagrams were created using:
- **Mermaid:** Open-source diagramming and charting tool
- **Format:** Markdown with embedded Mermaid syntax
- **Compatibility:** GitHub, GitLab, Notion, most documentation platforms
- **Export Options:** PNG, SVG, PDF (via Mermaid CLI)

### Rendering
All diagrams render in:
- GitHub preview
- GitLab wiki
- Markdown editors with Mermaid support
- Online Mermaid editor: https://mermaid.live

### Exporting Diagrams
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Convert to PNG
mmdc -i diagram.mermaid -o diagram.png

# Convert to SVG
mmdc -i diagram.mermaid -o diagram.svg

# Convert to PDF
mmdc -i diagram.mermaid -o diagram.pdf
```

---

## Feedback & Contributions

For updates, corrections, or new diagrams:
1. Review the current documentation
2. Propose changes with clear rationale
3. Update diagrams and this index
4. Document version changes
5. Notify team of updates

---

**Total Documentation:** 6 comprehensive documents with 35+ Mermaid diagrams
**Visual Coverage:** Complete system from data model to network security to threat intelligence
**Audience:** Executives, architects, developers, operators, security teams
