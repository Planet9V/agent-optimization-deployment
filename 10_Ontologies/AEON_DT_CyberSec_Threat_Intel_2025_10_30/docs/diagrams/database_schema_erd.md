# Entity-Relationship Diagrams & Database Schema

**Created:** 2025-10-29
**Purpose:** Comprehensive ER diagrams showing Neo4j property graph schema and relationships

---

## 1. Complete Entity-Relationship Diagram

```mermaid
erDiagram
    ORGANIZATION ||--o{ SITE : operates
    SITE ||--o{ TRAIN : hosts
    TRAIN ||--o{ COMPONENT : has_component
    COMPONENT ||--o{ SOFTWARE_INSTANCE : runs
    SOFTWARE_INSTANCE ||--o{ SOFTWARE : instance_of

    SITE ||--o{ NETWORK_ZONE : contains
    NETWORK_ZONE ||--o{ DEVICE : has_device
    DEVICE ||--o{ NETWORK_INTERFACE : has_interface
    DEVICE ||--o{ SERVICE : runs_service
    SERVICE ||--o{ NETWORK_INTERFACE : on_interface

    SOFTWARE ||--o{ VULNERABILITY : has_vulnerability
    SOFTWARE ||--o{ WEAKNESS : has_weakness
    COMPONENT ||--o{ CONFIGURATION : has_configuration
    WEAKNESS ||--o{ VULNERABILITY : manifests_as

    VULNERABILITY ||--o{ TECHNIQUE : exploited_by
    VULNERABILITY ||--o{ MALWARE : exploited_by
    TECHNIQUE ||--o{ ARTIFACT : uses_artifact
    MALWARE ||--o{ ARTIFACT : creates_artifact

    THREAT_ACTOR ||--o{ CAMPAIGN : executes
    CAMPAIGN ||--o{ TECHNIQUE : uses_technique
    CAMPAIGN ||--o{ MALWARE : deploys_malware

    SECURITY_CONTROL ||--o{ VULNERABILITY : mitigates
    SECURITY_CONTROL ||--o{ WEAKNESS : mitigates
    SECURITY_CONTROL ||--o{ TECHNIQUE : mitigates
    DEVICE ||--o{ SECURITY_CONTROL : has_control

    VULNERABILITY ||--o{ ADVISORY : referenced_in
    VULNERABILITY ||--o{ REPORT : referenced_in
    MALWARE ||--o{ REPORT : referenced_in
    THREAT_ACTOR ||--o{ REPORT : referenced_in
    CAMPAIGN ||--o{ REPORT : referenced_in
    TECHNIQUE ||--o{ DOCUMENT : referenced_in
    ADVISORY ||--o{ SOFTWARE : about_product

    THREAT_ACTOR ||--o{ ORGANIZATION : targets
    CAMPAIGN ||--o{ SOFTWARE : targets_industry
    MALWARE ||--o{ DEVICE : affects
    TECHNIQUE ||--o{ SOFTWARE : affects_asset
    ARTIFACT ||--o{ DEVICE : found_on

    MALWARE ||--o{ ARTIFACT : has_ioc
    CAMPAIGN ||--o{ ARTIFACT : has_ioc

    ORGANIZATION : organization_id PK
    ORGANIZATION : name
    ORGANIZATION : type
    ORGANIZATION : founded_date
    ORGANIZATION : industry
    ORGANIZATION : size
    ORGANIZATION : location

    SITE : site_id PK
    SITE : name
    SITE : location
    SITE : classification
    SITE : criticality
    SITE : last_assessed

    TRAIN : train_id PK
    TRAIN : name
    TRAIN : description
    TRAIN : ics_category
    TRAIN : criticality_level

    COMPONENT : component_id PK
    COMPONENT : name
    COMPONENT : type
    COMPONENT : manufacturer
    COMPONENT : model
    COMPONENT : serial_number
    COMPONENT : installation_date

    SOFTWARE : software_id PK
    SOFTWARE : name
    SOFTWARE : vendor
    SOFTWARE : product_type
    SOFTWARE : release_date
    SOFTWARE : cpe

    SOFTWARE_INSTANCE : instance_id PK
    SOFTWARE_INSTANCE : version
    SOFTWARE_INSTANCE : install_date
    SOFTWARE_INSTANCE : patch_level
    SOFTWARE_INSTANCE : license_type

    NETWORK_ZONE : zone_id PK
    NETWORK_ZONE : name
    NETWORK_ZONE : cidr
    NETWORK_ZONE : security_level
    NETWORK_ZONE : classification

    DEVICE : device_id PK
    DEVICE : hostname
    DEVICE : ip_address
    DEVICE : mac_address
    DEVICE : device_type
    DEVICE : os
    DEVICE : criticality

    NETWORK_INTERFACE : interface_id PK
    NETWORK_INTERFACE : name
    NETWORK_INTERFACE : ip_address
    NETWORK_INTERFACE : port
    NETWORK_INTERFACE : protocol
    NETWORK_INTERFACE : bandwidth

    SERVICE : service_id PK
    SERVICE : name
    SERVICE : port
    SERVICE : protocol
    SERVICE : version
    SERVICE : status

    VULNERABILITY : vuln_id PK
    VULNERABILITY : cve_id
    VULNERABILITY : cvss_score
    VULNERABILITY : cvss_vector
    VULNERABILITY : published_date
    VULNERABILITY : cwe_ids
    VULNERABILITY : description

    WEAKNESS : weakness_id PK
    WEAKNESS : cwe_id
    WEAKNESS : name
    WEAKNESS : description
    WEAKNESS : severity
    WEAKNESS : category

    CONFIGURATION : config_id PK
    CONFIGURATION : name
    CONFIGURATION : value
    CONFIGURATION : security_impact
    CONFIGURATION : status
    CONFIGURATION : last_verified

    SECURITY_CONTROL : control_id PK
    SECURITY_CONTROL : name
    SECURITY_CONTROL : type
    SECURITY_CONTROL : status
    SECURITY_CONTROL : effectiveness_percentage
    SECURITY_CONTROL : implementation_date

    THREAT_ACTOR : actor_id PK
    THREAT_ACTOR : name
    THREAT_ACTOR : aliases
    THREAT_ACTOR : country
    THREAT_ACTOR : capability_level
    THREAT_ACTOR : motivation

    CAMPAIGN : campaign_id PK
    CAMPAIGN : name
    CAMPAIGN : description
    CAMPAIGN : start_date
    CAMPAIGN : end_date
    CAMPAIGN : target_industry
    CAMPAIGN : success_rate

    TECHNIQUE : technique_id PK
    TECHNIQUE : mitre_id
    TECHNIQUE : name
    TECHNIQUE : tactic
    TECHNIQUE : platform
    TECHNIQUE : description

    MALWARE : malware_id PK
    MALWARE : name
    MALWARE : type
    MALWARE : family
    MALWARE : hash_sha256
    MALWARE : first_seen
    MALWARE : last_seen

    ARTIFACT : artifact_id PK
    ARTIFACT : type
    ARTIFACT : value
    ARTIFACT : hash_sha256
    ARTIFACT : file_name
    ARTIFACT : size
    ARTIFACT : confidence

    DOCUMENT : doc_id PK
    DOCUMENT : title
    DOCUMENT : doc_type
    DOCUMENT : published_date
    DOCUMENT : source
    DOCUMENT : url

    ADVISORY : advisory_id PK
    ADVISORY : advisory_number
    ADVISORY : issued_date
    ADVISORY : updated_date
    ADVISORY : affected_products
    ADVISORY : description

    REPORT : report_id PK
    REPORT : report_type
    REPORT : title
    REPORT : author
    REPORT : publish_date
    REPORT : severity_level
```

---

## 2. Cypher Query Pattern Diagrams

### Pattern 1: Vulnerability Impact Path

```mermaid
graph LR
    CVE["MATCH<br/>Vulnerability<br/>CVE-2024-1234"]

    SWF["MATCH<br/>Software<br/>Affected"]

    INST["MATCH<br/>SoftwareInstance<br/>Running<br/>v2.14.1"]

    DEV["MATCH<br/>Device<br/>Vulnerable"]

    ZONE["MATCH<br/>NetworkZone<br/>Exposure<br/>Level"]

    RISK["RETURN<br/>Risk Score<br/>Sorted by<br/>CVSS DESC"]

    CVE -->|has_vulnerability| SWF
    SWF -->|instance_of| INST
    INST -->|on_device| DEV
    DEV -->|in_zone| ZONE
    ZONE -->|calculate| RISK

    style CVE fill:#E74C3C,color:#fff
    style SWF fill:#F39C12,color:#fff
    style INST fill:#F39C12,color:#fff
    style DEV fill:#E74C3C,color:#fff
    style ZONE fill:#4A90E2,color:#fff
    style RISK fill:#C0392B,color:#fff,stroke-width:2px
```

```cypher
MATCH (vuln:Vulnerability {id: 'CVE-2024-1234'})
MATCH (soft:Software)-[:HAS_VULNERABILITY]->(vuln)
MATCH (inst:SoftwareInstance)-[:INSTANCE_OF]->(soft)
WHERE inst.version = '2.14.1'
MATCH (dev:Device)-[:RUNS_SOFTWARE]->(inst)
MATCH (dev)-[:IN_ZONE]->(zone:NetworkZone)
OPTIONAL MATCH (vuln)<-[:MITIGATES]-(ctrl:SecurityControl)<-[:HAS_CONTROL]-(dev)
WITH dev, vuln, zone,
     coalesce(sum(ctrl.effectiveness), 0) as mitigation
RETURN
    dev.hostname,
    dev.ip_address,
    dev.criticality,
    vuln.cvss_score,
    zone.security_level,
    vuln.cvss_score * (1 - mitigation/100) as risk_score
ORDER BY risk_score DESC
```

### Pattern 2: Attack Path Discovery

```mermaid
graph LR
    Start["Start<br/>Internet<br/>Attacker"]
    Path["Find Path<br/>Max 5 hops<br/>Via Vulns"]
    End["Target<br/>Critical<br/>Asset"]
    Risk["Calculate<br/>Risk Along<br/>Path"]

    Start -->|allShortestPaths| Path
    Path -->|leads to| End
    Path -->|assess| Risk

    style Start fill:#C0392B,color:#fff
    style Path fill:#E74C3C,color:#fff
    style End fill:#8B2E1F,color:#fff,stroke-width:2px
    style Risk fill:#F39C12,color:#fff
```

```cypher
MATCH (start:Device {exposure: 'PUBLIC'}),
      (target:Device {criticality: 'CRITICAL'})
CALL apoc.algo.allShortestPaths(start, target,
     'CONNECTED_TO|VULN_PATH', 5)
YIELD path
WITH path,
     reduce(risk = 0, rel in relationships(path) |
            risk + coalesce(rel.risk_score, 0)) as path_risk
WHERE path_risk > 0
RETURN
    [n in nodes(path) | n.hostname] as attack_path,
    length(path) as hops,
    path_risk,
    [r in relationships(path) | r.type] as attack_techniques
ORDER BY path_risk DESC
LIMIT 10
```

### Pattern 3: Campaign Attribution

```mermaid
graph TD
    IOCs["Collect<br/>All IOCs<br/>From Incidents"]

    Correlate["Correlate<br/>IOC Patterns<br/>Similarity >80%"]

    Techniques["Match<br/>MITRE TTPs<br/>Technique Set"]

    Infrastructure["Link<br/>Infrastructure<br/>C2 IP/Domain"]

    Malware["Compare<br/>Malware<br/>Code Similarity"]

    Attribution["Attribution<br/>Threat Actor<br/>Confidence"]

    IOCs -->|group| Correlate
    Correlate -->|match| Techniques
    Correlate -->|link| Infrastructure
    Infrastructure -->|analyze| Malware
    Techniques -->|cross-ref| Attribution
    Malware -->|validate| Attribution

    style IOCs fill:#E74C3C,color:#fff
    style Correlate fill:#F39C12,color:#fff
    style Techniques fill:#F39C12,color:#fff
    style Infrastructure fill:#F39C12,color:#fff
    style Malware fill:#F39C12,color:#fff
    style Attribution fill:#4A90E2,color:#fff,stroke-width:2px
```

```cypher
MATCH (campaign:Campaign)
MATCH (campaign)-[:HAS_ARTIFACT]->(artifact:Artifact)
MATCH (campaign)-[:USES_TECHNIQUE]->(technique:Technique)
MATCH (campaign)-[:DEPLOYS_MALWARE]->(malware:Malware)
WITH campaign,
     collect(DISTINCT artifact.value) as artifacts,
     collect(DISTINCT technique.mitre_id) as techniques,
     collect(DISTINCT malware.hash_sha256) as malware_hashes

MATCH (other_campaign:Campaign)
WHERE other_campaign <> campaign

// Calculate correlation score
WITH campaign, other_campaign,
     gds.similarity.jaccard(artifacts,
     [oc in (other_campaign)-[:HAS_ARTIFACT]->(a:Artifact) | a.value])
     as artifact_sim,
     gds.similarity.jaccard(techniques,
     [ot in (other_campaign)-[:USES_TECHNIQUE]->(t:Technique) | t.mitre_id])
     as technique_sim

WHERE (artifact_sim + technique_sim) / 2 > 0.80

RETURN campaign.name, other_campaign.name,
       round((artifact_sim + technique_sim) / 2, 2) as correlation_score
ORDER BY correlation_score DESC
```

---

## 3. Neo4j Index Strategy

```mermaid
graph TB
    subgraph Indexes["Index Configuration"]
        Idx1["Index: vuln_cve<br/>Type: Single<br/>Label: Vulnerability<br/>Property: cve_id<br/>Purpose: Fast CVE lookup"]

        Idx2["Index: device_ip<br/>Type: Single<br/>Label: Device<br/>Property: ip_address<br/>Purpose: Asset discovery"]

        Idx3["Index: artifact_hash<br/>Type: Single<br/>Label: Artifact<br/>Property: hash_sha256<br/>Purpose: IOC matching"]

        Idx4["Index: campaign_date<br/>Type: Composite<br/>Label: Campaign<br/>Properties: start_date,end_date<br/>Purpose: Timeline queries"]

        Idx5["Index: technique_tactic<br/>Type: Composite<br/>Label: Technique<br/>Properties: mitre_id,tactic<br/>Purpose: TTP analysis"]

        Idx6["Index: fulltext_doc<br/>Type: Full-text<br/>Label: Document<br/>Properties: title,content<br/>Purpose: Document search"]

        Idx7["Index: rel_exploits<br/>Type: Relationship<br/>Relationship: EXPLOITED_BY<br/>Purpose: Exploit chains"]

        Idx8["Index: rel_targets<br/>Type: Relationship<br/>Relationship: TARGETS<br/>Purpose: Campaign tracking"]
    end

    subgraph Constraints["Unique Constraints"]
        Con1["Constraint: org_id<br/>Label: Organization<br/>Property: organization_id<br/>Type: UNIQUE"]

        Con2["Constraint: device_hostname<br/>Label: Device<br/>Property: hostname<br/>Type: UNIQUE"]

        Con3["Constraint: campaign_id<br/>Label: Campaign<br/>Property: campaign_id<br/>Type: UNIQUE"]

        Con4["Constraint: actor_name<br/>Label: ThreatActor<br/>Property: name<br/>Type: UNIQUE"]
    end

    subgraph Performance["Performance Tuning"]
        Perf1["Query Optimization<br/>- Use indexes<br/>- Limit result sets<br/>- Cache patterns<br/>- Profile queries"]

        Perf2["Data Modeling<br/>- Denormalize relationships<br/>- Cache hot data<br/>- Partition large graphs<br/>- Archive old data"]

        Perf3["Scaling Strategy<br/>- Read replicas<br/>- Sharding by zone<br/>- Connection pooling<br/>- Memory management"]
    end

    Idx1 -->|Creates| Performance
    Idx2 -->|Creates| Performance
    Idx3 -->|Creates| Performance
    Idx4 -->|Creates| Performance
    Idx5 -->|Creates| Performance
    Idx6 -->|Creates| Performance
    Idx7 -->|Creates| Performance
    Idx8 -->|Creates| Performance

    Con1 -->|Enforces| Constraints
    Con2 -->|Enforces| Constraints
    Con3 -->|Enforces| Constraints
    Con4 -->|Enforces| Constraints

    style Indexes fill:#E3F2FD,stroke:#333
    style Constraints fill:#FFF3E0,stroke:#333
    style Performance fill:#E8F5E9,stroke:#333
```

**Cypher Index Creation:**

```cypher
-- Single Property Indexes
CREATE INDEX idx_vuln_cve FOR (v:Vulnerability) ON (v.cve_id);
CREATE INDEX idx_device_ip FOR (d:Device) ON (d.ip_address);
CREATE INDEX idx_artifact_hash FOR (a:Artifact) ON (a.hash_sha256);
CREATE INDEX idx_org_name FOR (o:Organization) ON (o.name);
CREATE INDEX idx_threat_actor FOR (t:ThreatActor) ON (t.name);

-- Composite Indexes
CREATE INDEX idx_campaign_date FOR (c:Campaign) ON (c.start_date, c.end_date);
CREATE INDEX idx_technique_tactic FOR (t:Technique) ON (t.mitre_id, t.tactic);
CREATE INDEX idx_device_zone FOR (d:Device) ON (d.ip_address, d.zone_id);

-- Full-text Index
CREATE INDEX idx_fulltext_document FOR (d:Document) ON EACH [d.title, d.content];

-- Unique Constraints
CREATE CONSTRAINT org_id_unique FOR (o:Organization) REQUIRE o.organization_id IS UNIQUE;
CREATE CONSTRAINT device_hostname_unique FOR (d:Device) REQUIRE d.hostname IS UNIQUE;
CREATE CONSTRAINT campaign_id_unique FOR (c:Campaign) REQUIRE c.campaign_id IS UNIQUE;
CREATE CONSTRAINT threat_actor_unique FOR (t:ThreatActor) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT cve_id_unique FOR (v:Vulnerability) REQUIRE v.cve_id IS UNIQUE;

-- Relationship Indexes
CREATE INDEX idx_exploited_by FOR ()-[r:EXPLOITED_BY]->() ON (r.cvss_score);
CREATE INDEX idx_targets FOR ()-[r:TARGETS]->() ON (r.success_rate);
```

---

## 4. Data Volume & Storage Estimation

| Entity Type | Expected Count | Avg Properties | Storage (GB) |
|-------------|------------------|----------------|-------------|
| Organization | 5,000 | 8 | 0.05 |
| Site | 50,000 | 10 | 0.25 |
| Device | 500,000 | 15 | 1.5 |
| Software | 100,000 | 12 | 0.3 |
| SoftwareInstance | 1,500,000 | 10 | 3.0 |
| Vulnerability (CVE) | 200,000 | 20 | 1.0 |
| Malware | 50,000 | 18 | 0.3 |
| Technique (MITRE) | 600 | 12 | 0.01 |
| ThreatActor | 2,000 | 10 | 0.02 |
| Campaign | 5,000 | 15 | 0.05 |
| **Total Graph Storage** | | | **~6 GB** |
| Index Storage (15%) | | | **~0.9 GB** |
| Replication (3x) | | | **~20.7 GB** |
| **Total DB Size** | | | **~27 GB** |

---

## 5. Data Consistency & ACID Properties

```mermaid
graph TD
    subgraph ACID["ACID Compliance"]
        A["Atomicity<br/>- Transactions all-or-nothing<br/>- Property updates atomic<br/>- Relationship creation atomic"]

        C["Consistency<br/>- Constraints enforced<br/>- Unique indexes validated<br/>- Referential integrity"]

        I["Isolation<br/>- MVCC isolation<br/>- Read committed level<br/>- Dirty reads prevented"]

        D["Durability<br/>- WAL logging<br/>- Fsync on commit<br/>- Point-in-time recovery"]
    end

    subgraph Guarantees["Transaction Guarantees"]
        G1["Write Ordering<br/>- FIFO queue<br/>- Transaction ID tracking<br/>- Consistent ordering"]

        G2["Read Consistency<br/>- Causal consistency<br/>- Strong consistency option<br/>- Replication ordering"]

        G3["Conflict Resolution<br/>- Last-write-wins<br/>- Explicit version tracking<br/>- Merge strategies"]
    end

    A -->|Provides| Guarantees
    C -->|Provides| Guarantees
    I -->|Provides| Guarantees
    D -->|Provides| Guarantees

    style A fill:#4A90E2,color:#fff
    style C fill:#4A90E2,color:#fff
    style I fill:#4A90E2,color:#fff
    style D fill:#4A90E2,color:#fff
    style Guarantees fill:#E3F2FD,stroke:#333
```

---

## 6. Backup & Recovery Schema

```mermaid
graph TB
    subgraph Backup["Backup Strategy"]
        Full["Full Backup<br/>- Daily 00:00 UTC<br/>- Complete graph dump<br/>- Size: ~6.5 GB<br/>- Duration: 45 min"]

        Incremental["Incremental Backup<br/>- Hourly 6:00, 12:00, 18:00<br/>- Changed data only<br/>- Size: ~500 MB avg<br/>- Duration: 15 min"]

        WAL["Write-Ahead Log<br/>- Continuous logging<br/>- Point-in-time recovery<br/>- 7-day retention<br/>- Compressed storage"]
    end

    subgraph Recovery["Recovery Options"]
        Recover1["Full Recovery<br/>- From daily full backup<br/>- Restore time: 30 min<br/>- Data loss: < 1 hour"]

        Recover2["Incremental Recovery<br/>- Full + incremental<br/>- Restore time: 45 min<br/>- Data loss: < 10 min"]

        Recover3["Point-in-Time<br/>- Use WAL replay<br/>- Any timestamp<br/>- Restore time: 1 hour<br/>- Zero data loss"]

        Recover4["Cross-Region<br/>- Async replication<br/>- RPO: 5 minutes<br/>- RTO: 15 minutes"]
    end

    subgraph Storage["Storage Locations"]
        Local["Local Storage<br/>- Primary backup<br/>- NAS location<br/>- Retention: 30 days<br/>- Accessible: 5 min"]

        Offsite["Offsite Backup<br/>- Secondary backup<br/>- Cloud storage (S3)<br/>- Retention: 90 days<br/>- Accessible: 2 hours"]

        Vault["Cold Vault<br/>- Archival backup<br/>- Glacier/Archive<br/>- Retention: 1 year<br/>- Accessible: 12 hours"]
    end

    Full -->|Generates| Backup
    Incremental -->|Generates| Backup
    WAL -->|Generates| Backup

    Recover1 -->|Uses| Full
    Recover2 -->|Uses| Incremental
    Recover3 -->|Uses| WAL
    Recover4 -->|Uses| Backup

    Backup -->|Stored in| Local
    Backup -->|Replicated to| Offsite
    Offsite -->|Archived to| Vault

    style Backup fill:#E8F5E9,stroke:#333
    style Recovery fill:#E3F2FD,stroke:#333
    style Storage fill:#FFF3E0,stroke:#333
```

---

## Summary: Database Architecture

### Key Characteristics
- **Graph Model:** Property graph with labeled nodes and relationships
- **Node Types:** 15 (Organization, Device, Vulnerability, Campaign, etc.)
- **Relationship Types:** 25+ (HAS_VULNERABILITY, EXPLOITED_BY, TARGETS, etc.)
- **Scale:** ~2-3M nodes, ~5-10M relationships
- **Storage:** ~27 GB with replication (3x primary)

### Performance Targets
- **Query latency:** <100ms for 95th percentile
- **Throughput:** 1000+ queries/second
- **Backup time:** 45 minutes (full)
- **Recovery time:** 30 minutes (full) to 2 hours (point-in-time)

### Reliability
- **Availability:** 99.95% uptime (4 hours/year)
- **Data durability:** 99.999% (RPO < 10 minutes)
- **Consistency:** Strong consistency guarantee
- **Failover:** Automatic (< 30 seconds)
