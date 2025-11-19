# Use Case Diagrams & Visualization Patterns

**Created:** 2025-10-29
**Purpose:** Visual documentation of the 7 primary use cases with graph patterns and data flows

---

## Use Case 1: Vulnerability Impact Assessment

**Objective:** Determine which assets are vulnerable to a specific CVE and calculate risk scores

### Graph Pattern

```mermaid
graph TD
    CVE["CVE-2024-1234<br/>CVSS: 9.8"]
    CWE["CWE-79<br/>Cross-site Scripting"]

    Soft["Software<br/>Apache Log4j<br/>v2.14.1"]
    Config["Configuration<br/>Logging Enabled"]

    SoftInst1["Instance 1<br/>prod-web-01<br/>v2.14.1"]
    SoftInst2["Instance 2<br/>staging-app-01<br/>v2.14.1"]
    SoftInst3["Instance 3<br/>dev-server-01<br/>v2.15.0<br/>PATCHED"]

    Device1["Device<br/>web-server-prod<br/>10.0.1.50"]
    Device2["Device<br/>app-server-staging<br/>10.0.2.40"]

    Zone["NetworkZone<br/>DMZ<br/>Exposure: HIGH"]

    Control1["Control<br/>WAF Rules<br/>Effectiveness: 60%"]
    Control2["Control<br/>IDS/IPS<br/>Effectiveness: 75%"]

    RiskScore1["Risk Score: 8.5<br/>CRITICAL"]
    RiskScore2["Risk Score: 7.2<br/>HIGH"]
    RiskScore3["Risk Score: 0<br/>SAFE"]

    CVE -->|HAS_WEAKNESS| CWE
    CVE -->|AFFECTS| Soft
    CVE -->|EXPLOITABLE_WITH_CONFIG| Config

    Soft -->|INSTANCE_RUNNING| SoftInst1
    Soft -->|INSTANCE_RUNNING| SoftInst2
    Soft -->|INSTANCE_RUNNING| SoftInst3

    SoftInst1 -->|ON_DEVICE| Device1
    SoftInst2 -->|ON_DEVICE| Device2
    SoftInst3 -->|PATCHED_VERSION| SoftInst3

    Device1 -->|IN_ZONE| Zone
    Device2 -->|IN_ZONE| Zone

    Control1 -->|MITIGATES| CVE
    Control2 -->|MITIGATES| CVE

    Device1 -->|HAS_CONTROL| Control1
    Device1 -->|HAS_CONTROL| Control2
    Device2 -->|HAS_CONTROL| Control2

    Device1 -->|RISK_SCORE| RiskScore1
    Device2 -->|RISK_SCORE| RiskScore2
    Device2 -->|RISK_SCORE| RiskScore3

    style CVE fill:#E74C3C,stroke:#8B2E1F,color:#fff
    style Soft fill:#F39C12,stroke:#985F0D,color:#fff
    style SoftInst1 fill:#E74C3C,color:#fff
    style SoftInst2 fill:#E74C3C,color:#fff
    style SoftInst3 fill:#50C878,color:#fff
    style Device1 fill:#E74C3C,color:#fff
    style Device2 fill:#E74C3C,color:#fff
    style Control1 fill:#4A90E2,color:#fff
    style Control2 fill:#4A90E2,color:#fff
    style RiskScore1 fill:#C0392B,color:#fff
    style RiskScore2 fill:#E74C3C,color:#fff
    style RiskScore3 fill:#27AE60,color:#fff
```

### Example Data Flow
```
MATCH (c:CVE {id: 'CVE-2024-1234'})
MATCH (s:Software)-[:HAS_VULNERABILITY]->(c)
MATCH (si:SoftwareInstance {version: '2.14.1'})-[:INSTANCE_OF]->(s)
MATCH (d:Device)<-[:ON_DEVICE]-(si)
OPTIONAL MATCH (c)<-[:MITIGATES]-(control:SecurityControl)
RETURN d.hostname, d.ip_address, c.cvss_score,
       count(control) as control_count
ORDER BY c.cvss_score DESC
```

### Risk Assessment Calculation
- **Base Risk**: CVSS Score (9.8)
- **Exposure**: Network Zone classification (DMZ = HIGH)
- **Mitigation**: Active controls effectiveness
- **Final Score**: 8.5 = 9.8 × (1 - 0.6) × 0.95 (DMZ multiplier)

---

## Use Case 2: Threat Actor Campaign Tracking

**Objective:** Track a threat actor's campaigns, techniques, and malware deployments

### Graph Pattern

```mermaid
graph TD
    TA["ThreatActor<br/>APT28<br/>Capability: Advanced<br/>Country: Russia"]

    Cam1["Campaign<br/>Campaign-2024-Q3<br/>Start: 2024-09-01<br/>Target: Finance"]
    Cam2["Campaign<br/>Campaign-2024-Q4<br/>Start: 2024-10-01<br/>Target: Energy"]

    Tech1["Technique<br/>T1566.002<br/>Phishing: Spearphishing<br/>Tactic: Initial Access"]
    Tech2["Technique<br/>T1055<br/>Process Injection<br/>Tactic: Defense Evasion"]
    Tech3["Technique<br/>T1547.001<br/>Registry Run Keys<br/>Tactic: Persistence"]

    Malware1["Malware<br/>Emotet<br/>Type: Banking Trojan<br/>First Seen: 2024-09-15"]
    Malware2["Malware<br/>Cobalt Strike<br/>Type: RAT<br/>First Seen: 2024-09-20"]

    IOC1["Artifact<br/>C&C Server<br/>192.168.1.100"]
    IOC2["Artifact<br/>File Hash<br/>sha256:abc123..."]
    IOC3["Artifact<br/>Domain<br/>malicious.example.com"]

    Org1["Organization<br/>Financial Corp<br/>Industry: Finance"]
    Org2["Organization<br/>Energy Corp<br/>Industry: Energy"]

    Advisory1["Advisory<br/>CISA-2024-1001<br/>Published: 2024-10-05"]

    TA -->|EXECUTES| Cam1
    TA -->|EXECUTES| Cam2

    Cam1 -->|USES_TECHNIQUE| Tech1
    Cam1 -->|USES_TECHNIQUE| Tech2
    Cam2 -->|USES_TECHNIQUE| Tech2
    Cam2 -->|USES_TECHNIQUE| Tech3

    Cam1 -->|DEPLOYS| Malware1
    Cam1 -->|DEPLOYS| Malware2
    Cam2 -->|DEPLOYS| Malware2

    Tech1 -->|USES_ARTIFACT| IOC1
    Malware1 -->|CONTACTS| IOC1
    Malware1 -->|HAS_HASH| IOC2
    Malware1 -->|REGISTERED_DOMAIN| IOC3

    Cam1 -->|TARGETS| Org1
    Cam2 -->|TARGETS| Org2

    Malware1 -->|REFERENCED_IN| Advisory1
    Tech1 -->|REFERENCED_IN| Advisory1
    TA -->|REFERENCED_IN| Advisory1

    Timeline["Timeline<br/>Sep 15: Emotet Detection<br/>Sep 20: Cobalt Strike Found<br/>Oct 1: New Campaign Phase"]

    Cam1 -.->|Events| Timeline
    Malware1 -.->|Events| Timeline

    style TA fill:#F39C12,stroke:#985F0D,color:#fff,stroke-width:3px
    style Cam1 fill:#F39C12,stroke:#985F0D,color:#fff
    style Cam2 fill:#F39C12,stroke:#985F0D,color:#fff
    style Tech1 fill:#E74C3C,color:#fff
    style Tech2 fill:#E74C3C,color:#fff
    style Tech3 fill:#E74C3C,color:#fff
    style Malware1 fill:#C0392B,color:#fff,stroke-width:2px
    style Malware2 fill:#C0392B,color:#fff,stroke-width:2px
    style IOC1 fill:#8E44AD,color:#fff
    style IOC2 fill:#8E44AD,color:#fff
    style IOC3 fill:#8E44AD,color:#fff
    style Org1 fill:#4A90E2,color:#fff
    style Org2 fill:#4A90E2,color:#fff
    style Advisory1 fill:#9B59B6,color:#fff
    style Timeline fill:#F39C12,stroke:#985F0D,color:#fff
```

### Example Query
```
MATCH (ta:ThreatActor {name: 'APT28'})
MATCH (ta)-[:EXECUTES]->(campaign:Campaign)
MATCH (campaign)-[:USES_TECHNIQUE]->(technique:Technique)
MATCH (campaign)-[:DEPLOYS]->(malware:Malware)
MATCH (malware)-[:HAS_ARTIFACT]->(artifact:Artifact)
RETURN
    campaign.name,
    collect(distinct technique.name) as techniques,
    collect(distinct malware.name) as malware_used,
    collect(distinct artifact.type) as artifacts,
    campaign.start_date
ORDER BY campaign.start_date DESC
```

### Timeline Analysis
- **Phase 1 (Sep 15)**: Initial access via phishing, Emotet deployment
- **Phase 2 (Sep 20)**: Lateral movement, Cobalt Strike for persistence
- **Phase 3 (Oct 1)**: New campaign phase targeting energy sector

---

## Use Case 3: Attack Path Discovery

**Objective:** Identify potential attack paths from internet-facing assets to critical infrastructure

### Graph Pattern

```mermaid
graph LR
    subgraph Internet["Internet / External"]
        Attacker["Attacker"]
    end

    subgraph DMZ["DMZ Zone<br/>Exposure: Public"]
        WebApp["WebApp<br/>10.0.1.10<br/>Port 443"]
        WebVuln["Vulnerability<br/>CVE-2024-5678<br/>RCE"]
    end

    subgraph Internal["Internal Network<br/>Exposure: Private"]
        WebServer["Web Server<br/>10.0.2.20<br/>Port 8080"]
        AppServer["App Server<br/>10.0.2.30<br/>Port 3000"]
        DBServer["Database Server<br/>10.0.3.40<br/>Port 5432"]
    end

    subgraph Critical["Critical Infrastructure<br/>Exposure: None"]
        SCADA["SCADA System<br/>10.0.4.50<br/>Port 502"]
        Historian["Data Historian<br/>10.0.4.60<br/>Port 3306"]
    end

    subgraph Vulnerabilities["Vulnerabilities in Path"]
        AppVuln["CVE-2024-9999<br/>Auth Bypass"]
        DBVuln["CVE-2024-1111<br/>Privilege Escalation"]
        SCADAVuln["CVE-2024-2222<br/>Buffer Overflow"]
    end

    Attacker -->|Network Path| WebApp
    WebApp -->|Vulnerable| WebVuln
    WebVuln -->|Exploitation| WebServer

    WebServer -->|Network Path| AppServer
    AppServer -->|Vulnerable| AppVuln
    AppVuln -->|Exploitation| DBServer

    DBServer -->|Vulnerable| DBVuln
    DBVuln -->|Lateral Movement| SCADA
    SCADA -->|Vulnerable| SCADAVuln

    DBServer -->|Network Path| Historian

    WebVuln -.->|Referenced In| Vulnerabilities
    AppVuln -.->|Referenced In| Vulnerabilities
    DBVuln -.->|Referenced In| Vulnerabilities
    SCADAVuln -.->|Referenced In| Vulnerabilities

    style Attacker fill:#C0392B,stroke:#8B2E1F,color:#fff
    style WebApp fill:#E74C3C,color:#fff
    style WebServer fill:#F39C12,color:#fff
    style AppServer fill:#F39C12,color:#fff
    style DBServer fill:#F39C12,color:#fff
    style SCADA fill:#C0392B,color:#fff,stroke-width:3px
    style Historian fill:#C0392B,color:#fff
    style WebVuln fill:#E74C3C,color:#fff
    style AppVuln fill:#E74C3C,color:#fff
    style DBVuln fill:#E74C3C,color:#fff
    style SCADAVuln fill:#C0392B,color:#fff
```

### Path Discovery Query
```
MATCH path = (start:Device {exposure: 'Public'})
-[*1..5]->(end:Device {critical: true})
WHERE all(node in nodes(path)
          WHERE (node)-[:HAS_VULNERABILITY]->())
RETURN
    [n in nodes(path) | n.hostname] as attack_path,
    length(path) as hop_count,
    reduce(risk=0, rel in relationships(path) | risk + rel.risk_score) as total_risk
ORDER BY total_risk DESC
```

### Risk Assessment
- **Exposure**: DMZ device exposed to internet
- **Entry Point**: RCE vulnerability (CVSS 9.8)
- **Lateral Movement**: Web → App → Database → SCADA
- **Impact**: Critical SCADA compromise
- **Risk Level**: CRITICAL

---

## Use Case 4: Asset Configuration Compliance

**Objective:** Verify that critical assets meet security configuration requirements

### Graph Pattern

```mermaid
graph TD
    subgraph Requirements["Security Requirements"]
        Req1["Requirement: TLS 1.2+<br/>Severity: HIGH"]
        Req2["Requirement: Firewall Rules<br/>Severity: HIGH"]
        Req3["Requirement: Log Aggregation<br/>Severity: MEDIUM"]
        Req4["Requirement: No Default Creds<br/>Severity: CRITICAL"]
    end

    subgraph Assets["Assets to Audit"]
        Device1["Device: web-prod<br/>Type: Web Server"]
        Device2["Device: db-prod<br/>Type: Database"]
        Device3["Device: app-staging<br/>Type: App Server"]
    end

    subgraph Configurations["Actual Configurations"]
        Config1["TLS 1.1<br/>Status: NON-COMPLIANT"]
        Config2["TLS 1.3<br/>Status: COMPLIANT"]
        Config3["Firewall Rules<br/>Status: COMPLIANT"]
        Config4["No Logging<br/>Status: NON-COMPLIANT"]
        Config5["Admin/Admin<br/>Status: CRITICAL"]
    end

    subgraph Results["Compliance Results"]
        Result1["Device: web-prod<br/>Compliance: 25%<br/>Status: CRITICAL"]
        Result2["Device: db-prod<br/>Compliance: 100%<br/>Status: COMPLIANT"]
        Result3["Device: app-staging<br/>Compliance: 50%<br/>Status: NON-COMPLIANT"]
    end

    Req1 -->|Check Configuration| Config1
    Req1 -->|Check Configuration| Config2
    Req2 -->|Check Configuration| Config3
    Req3 -->|Check Configuration| Config4
    Req4 -->|Check Configuration| Config5

    Device1 -->|Has Configuration| Config1
    Device1 -->|Has Configuration| Config4
    Device1 -->|Has Configuration| Config5
    Device2 -->|Has Configuration| Config2
    Device2 -->|Has Configuration| Config3
    Device3 -->|Has Configuration| Config1
    Device3 -->|Has Configuration| Config4

    Device1 -->|Audit Result| Result1
    Device2 -->|Audit Result| Result2
    Device3 -->|Audit Result| Result3

    style Req1 fill:#4A90E2,color:#fff
    style Req2 fill:#4A90E2,color:#fff
    style Req3 fill:#4A90E2,color:#fff
    style Req4 fill:#4A90E2,color:#fff
    style Config1 fill:#E74C3C,color:#fff
    style Config2 fill:#27AE60,color:#fff
    style Config3 fill:#27AE60,color:#fff
    style Config4 fill:#E74C3C,color:#fff
    style Config5 fill:#C0392B,color:#fff
    style Result1 fill:#C0392B,color:#fff
    style Result2 fill:#27AE60,color:#fff
    style Result3 fill:#E74C3C,color:#fff
```

### Compliance Query
```
MATCH (requirement:SecurityRequirement)
MATCH (device:Device)
OPTIONAL MATCH (device)-[:HAS_CONFIGURATION]->(config:Configuration)
WHERE config.name = requirement.name
WITH device, requirement, config,
     CASE WHEN config.status = 'COMPLIANT' THEN 1 ELSE 0 END as compliant
RETURN
    device.hostname,
    device.type,
    count(requirement) as total_requirements,
    sum(compliant) as compliant_count,
    round(100.0 * sum(compliant) / count(requirement), 2) as compliance_percentage,
    collect(requirement.name + ': ' + coalesce(config.status, 'MISSING')) as details
ORDER BY compliance_percentage
```

---

## Use Case 5: Software Bill of Materials (SBOM) Analysis

**Objective:** Track all software components and identify vulnerable dependencies

### Graph Pattern

```mermaid
graph TD
    App["Application<br/>MyWebApp v1.0.0"]

    Direct1["Dependency<br/>Express v4.17.1"]
    Direct2["Dependency<br/>React v16.13.0"]
    Direct3["Dependency<br/>PostgreSQL-Driver v2.2.0"]

    Sub1["Sub-Dependency<br/>Body-Parser v1.19.0"]
    Sub2["Sub-Dependency<br/>React-DOM v16.13.0"]
    Sub3["Sub-Dependency<br/>lodash v4.17.15"]
    Sub4["Sub-Dependency<br/>serializer v2.0.0"]

    Vuln1["Vulnerability<br/>CVE-2021-3129<br/>Code Injection"]
    Vuln2["Vulnerability<br/>CVE-2021-3807<br/>Regex DoS"]
    Vuln3["Vulnerability<br/>CVE-2018-16487<br/>Prototype Pollution"]
    Vuln4["Vulnerability<br/>CVE-2021-23358<br/>Prototype Pollution"]

    DeployInstance["Deployment Instance<br/>prod-web-01<br/>Status: VULNERABLE"]

    App -->|DEPENDS_ON| Direct1
    App -->|DEPENDS_ON| Direct2
    App -->|DEPENDS_ON| Direct3

    Direct1 -->|DEPENDS_ON| Sub1
    Direct1 -->|DEPENDS_ON| Sub3
    Direct2 -->|DEPENDS_ON| Sub2
    Direct3 -->|DEPENDS_ON| Sub4
    Sub2 -->|DEPENDS_ON| Sub3

    Direct1 -->|HAS_VULNERABILITY| Vuln1
    Sub1 -->|HAS_VULNERABILITY| Vuln2
    Sub3 -->|HAS_VULNERABILITY| Vuln3
    Sub3 -->|HAS_VULNERABILITY| Vuln4
    Sub4 -->|HAS_VULNERABILITY| Vuln2

    App -->|DEPLOYED_ON| DeployInstance

    style App fill:#4A90E2,color:#fff,stroke-width:2px
    style Direct1 fill:#F39C12,color:#fff
    style Direct2 fill:#F39C12,color:#fff
    style Direct3 fill:#F39C12,color:#fff
    style Sub1 fill:#E74C3C,color:#fff
    style Sub2 fill:#E74C3C,color:#fff
    style Sub3 fill:#C0392B,color:#fff,stroke-width:2px
    style Sub4 fill:#E74C3C,color:#fff
    style Vuln1 fill:#C0392B,color:#fff
    style Vuln2 fill:#C0392B,color:#fff
    style Vuln3 fill:#C0392B,color:#fff
    style Vuln4 fill:#C0392B,color:#fff
    style DeployInstance fill:#E74C3C,color:#fff
```

### SBOM Query
```
MATCH (app:Application {name: 'MyWebApp'})
MATCH (dep:Dependency)-[*0..5]->(app)
OPTIONAL MATCH (dep)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WITH dep, vuln, app
RETURN
    dep.name + '@' + dep.version as component,
    CASE WHEN vuln IS NOT NULL THEN 'VULNERABLE'
         ELSE 'SAFE' END as status,
    collect({
        id: vuln.id,
        cvss: vuln.cvss_score
    }) as vulnerabilities,
    dep.license
ORDER BY coalesce(vuln.cvss_score, 0) DESC
```

---

## Use Case 6: Incident Response Timeline

**Objective:** Reconstruct incident timeline using logs, alerts, and threat intelligence

### Graph Pattern

```mermaid
graph LR
    subgraph Timeline["Incident Timeline: 2024-10-15"]
        T1["09:15 - Phishing Email<br/>Target: user@company.com<br/>Subject: 'Invoice Review'"]
        T2["10:30 - Email Opened<br/>Attachment: invoice.exe<br/>Action: Downloaded"]
        T3["10:32 - Process Execution<br/>Process: invoice.exe<br/>PID: 2847"]
        T4["10:35 - Network Connection<br/>Destination: 192.168.1.100:8080<br/>Protocol: HTTP"]
        T5["10:40 - Registry Modified<br/>Key: HKLM\\\\Run<br/>Value: malware.exe"]
        T6["10:45 - Persistence Achieved<br/>Service: Windows Update Checker<br/>Status: Installed"]
        T7["11:00 - Data Exfiltration<br/>Volume: 2.3 GB<br/>Destination: C&C Server"]
        T8["13:30 - Alert Triggered<br/>Type: Unusual Process<br/>Action: Investigation"]
        T9["14:00 - Incident Detected<br/>Status: CRITICAL<br/>Response: Initiated"]
    end

    %% Entities
    Phish["Malicious Email<br/>From: spoof@gmail.com"]
    Attachment["Attachment<br/>invoice.exe<br/>Hash: abc123"]
    Process["Process<br/>invoice.exe<br/>PID: 2847"]
    Network["Network Connection<br/>192.168.1.100:8080"]
    Malware["Malware<br/>TrickBot v2<br/>C2: example.com"]
    ThreatActor["Threat Actor<br/>Unknown Group<br/>ATT&CK: T1566.002"]

    T1 -->|Email| Phish
    T2 -->|Download| Attachment
    T3 -->|Execute| Process
    T4 -->|Connect| Network
    T5 -->|Modify Registry| T6
    T7 -->|Exfil| Malware

    Phish -->|Associated With| ThreatActor
    Attachment -->|Is| Malware
    Process -->|Run| Attachment
    Network -->|Connect| Malware

    T1 -.->|Timeline| T2
    T2 -.->|Timeline| T3
    T3 -.->|Timeline| T4
    T4 -.->|Timeline| T5
    T5 -.->|Timeline| T6
    T6 -.->|Timeline| T7
    T7 -.->|Timeline| T8
    T8 -.->|Timeline| T9

    style T1 fill:#F39C12,color:#fff
    style T2 fill:#E74C3C,color:#fff
    style T3 fill:#C0392B,color:#fff
    style T4 fill:#C0392B,color:#fff
    style T5 fill:#C0392B,color:#fff
    style T6 fill:#C0392B,color:#fff
    style T7 fill:#C0392B,color:#fff
    style T8 fill:#9B59B6,color:#fff
    style T9 fill:#8E44AD,color:#fff,stroke-width:3px
```

### Incident Timeline Query
```
MATCH (incident:Incident {id: 'INC-2024-1001'})
MATCH (incident)-[:CONTAINS_EVENT]->(event:Event)
WITH event
ORDER BY event.timestamp
MATCH (event)-[:INVOLVES]->(entity)
RETURN
    event.timestamp,
    event.type,
    event.description,
    collect(entity.name) as affected_entities,
    event.severity
ORDER BY event.timestamp
```

---

## Use Case 7: Executive Risk Dashboard

**Objective:** Provide high-level risk metrics and trends for executive reporting

### Graph Pattern

```mermaid
graph TB
    subgraph Metrics["Key Risk Metrics"]
        M1["Critical Vulnerabilities<br/>Count: 47<br/>Trend: ↑ +12"]
        M2["Exposed Assets<br/>Count: 23<br/>Trend: ↑ +5"]
        M3["Active Campaigns<br/>Count: 8<br/>Trend: ↔ 0"]
        M4["Mean Time to Remediate<br/>Days: 45<br/>Trend: ↓ -5"]
    end

    subgraph RiskScores["Risk Scores by Category"]
        R1["Vulnerability Risk<br/>Score: 8.2<br/>Status: CRITICAL"]
        R2["Threat Risk<br/>Score: 7.5<br/>Status: HIGH"]
        R3["Configuration Risk<br/>Score: 6.8<br/>Status: HIGH"]
        R4["Overall Risk<br/>Score: 7.5<br/>Status: HIGH"]
    end

    subgraph Top10["Top 10 Risks"]
        Risk1["CVE-2024-1234<br/>Affecting: 45 assets<br/>CVSS: 9.8"]
        Risk2["CVE-2024-5678<br/>Affecting: 23 assets<br/>CVSS: 9.1"]
        Risk3["Weak Password Policy<br/>Affecting: 156 users<br/>Risk: 7.2"]
        Risk4["APT28 Campaign<br/>Targeting: Finance<br/>Risk: 8.1"]
    end

    subgraph Trending["Trending Issues"]
        T1["CVE Disclosure Rate<br/>Month: 847 new CVEs<br/>vs 712 last month"]
        T2["Active Threats<br/>Week: 12 new campaigns<br/>vs 8 last week"]
        T3["Compliance Drift<br/>Week: -3% compliance<br/>Issues found: 8"]
    end

    M1 -->|Contributes| R1
    M2 -->|Contributes| R2
    M3 -->|Contributes| R2
    M4 -->|Contributes| R3

    R1 -->|Combined| R4
    R2 -->|Combined| R4
    R3 -->|Combined| R4

    Risk1 -->|In Top 10| R1
    Risk2 -->|In Top 10| R1
    Risk3 -->|In Top 10| R3
    Risk4 -->|In Top 10| R2

    T1 -->|Trending| Metrics
    T2 -->|Trending| Top10
    T3 -->|Trending| Metrics

    style M1 fill:#C0392B,color:#fff,stroke-width:2px
    style M2 fill:#E74C3C,color:#fff,stroke-width:2px
    style M3 fill:#F39C12,color:#fff
    style M4 fill:#27AE60,color:#fff
    style R1 fill:#C0392B,color:#fff,stroke-width:2px
    style R2 fill:#E74C3C,color:#fff,stroke-width:2px
    style R3 fill:#E74C3C,color:#fff,stroke-width:2px
    style R4 fill:#C0392B,color:#fff,stroke-width:3px
    style Risk1 fill:#C0392B,color:#fff
    style Risk2 fill:#C0392B,color:#fff
    style Risk3 fill:#E74C3C,color:#fff
    style Risk4 fill:#E74C3C,color:#fff
```

### Executive Dashboard Query
```
MATCH (org:Organization)
WITH org

// Critical vulnerabilities
MATCH (vuln:Vulnerability {severity: 'CRITICAL'})
MATCH (vuln)-[:AFFECTS]->(asset:Asset)-[:OWNED_BY]->(org)
WITH org, count(distinct vuln) as critical_vulns

// Exposed assets
MATCH (asset:Asset)-[:IN_ZONE]->(zone:NetworkZone {exposure: 'PUBLIC'})
MATCH (asset)-[:OWNED_BY]->(org)
WITH org, critical_vulns, count(distinct asset) as exposed_assets

// Active campaigns
MATCH (campaign:Campaign {status: 'ACTIVE'})
MATCH (campaign)-[:TARGETS]->(target)-[:OWNED_BY]->(org)
WITH org, critical_vulns, exposed_assets, count(distinct campaign) as campaigns

RETURN
    org.name,
    critical_vulns,
    exposed_assets,
    campaigns,
    (critical_vulns + exposed_assets * 0.5 + campaigns * 2) / 10 as risk_score
```

---

## Summary Table

| Use Case | Key Entities | Primary Query Type | Output |
|----------|--------------|-------------------|--------|
| Vulnerability Impact | CVE, Software, Device | Shortest path | Risk scores, affected assets |
| Campaign Tracking | ThreatActor, Campaign, Technique | Graph traversal | IOCs, timeline, targets |
| Attack Path | Device, Vulnerability, NetworkZone | Path finding | Attack chain, risk assessment |
| Compliance | Device, Configuration, Requirement | Pattern matching | Compliance percentage, gaps |
| SBOM Analysis | Application, Dependency, Vulnerability | Tree traversal | Component tree, vulnerable deps |
| Incident Timeline | Event, Entity, Timestamp | Chronological | Timeline reconstruction, root cause |
| Risk Dashboard | All entities | Aggregate functions | Metrics, scores, trends |
