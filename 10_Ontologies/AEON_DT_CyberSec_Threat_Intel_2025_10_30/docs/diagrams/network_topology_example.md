# Network Topology & Security Architecture Example

**Created:** 2025-10-29
**Purpose:** Detailed network topology with security zones, firewall rules, and attack paths

---

## 1. Comprehensive Network Topology

```mermaid
graph TB
    subgraph Internet["External Internet"]
        AttackerNet["Attacker Networks<br/>External Threats"]
        Customers["Customer Networks<br/>Legitimate Users"]
    end

    subgraph EdgeSecurity["Edge Security (IEC 62443 Level 1)"]
        WAF["Web Application Firewall<br/>ModSecurity Rules<br/>Rate Limiting: 1000 req/s"]
        NGFW["Next-Gen Firewall<br/>IDS/IPS Enabled<br/>Threat Database: Updated Daily"]
        CDN["CDN & DDoS Mitigation<br/>Anycast Network<br/>10Gbps capacity"]
    end

    subgraph DMZ["DMZ Zone (IEC 62443 Level 2)<br/>Medium Security"]
        WebServers["Web Servers<br/>Apache/Nginx x3<br/>10.0.1.0/25"]
        APIGateway["API Gateway<br/>Kong/Traefik<br/>10.0.1.130"]
        EmailGateway["Email Gateway<br/>Postfix with Filters<br/>10.0.1.131"]
        DNSServers["DNS Servers<br/>Bind9 (Sec)<br/>10.0.1.132-133"]
    end

    subgraph Internal["Internal Network (IEC 62443 Level 3)<br/>High Security"]
        AppServers["Application Servers<br/>Java/Python Apps<br/>10.0.2.0/24"]
        CacheLayer["Cache Layer<br/>Redis Cluster<br/>10.0.2.100-102"]
        MessageQueue["Message Queue<br/>RabbitMQ/Kafka<br/>10.0.2.103-104"]
        MonitoringLan["Monitoring LAN<br/>Prometheus/Grafana<br/>10.0.2.200-210"]
    end

    subgraph DataPlane["Data Plane (IEC 62443 Level 4)<br/>Critical Security"]
        DatabasePrimary["Primary Database<br/>PostgreSQL<br/>10.0.3.10"]
        DatabaseReplica["Replica Databases<br/>3x Read-Only<br/>10.0.3.11-13"]
        BackupVault["Backup Vault<br/>NetApp Storage<br/>10.0.3.50"]
        GraphDatabase["Graph Database<br/>Neo4j Cluster<br/>10.0.3.100-102"]
    end

    subgraph CriticalInfra["Critical Infrastructure (IEC 62443 Level 5)<br/>Isolated Network"]
        SCADA["SCADA Systems<br/>Industrial Controllers<br/>10.0.4.0/24"]
        HMI["Human-Machine Interface<br/>Operator Stations<br/>10.0.4.100-105"]
        FieldDevices["Field Devices<br/>Sensors/Actuators<br/>10.0.4.200-210"]
        Historian["Data Historian<br/>FactoryTalk Server<br/>10.0.4.50"]
    end

    subgraph Management["Management Network<br/>Access Control Zone"]
        Bastion["Bastion Hosts<br/>SSH/RDP Gateways<br/>10.0.5.10-11"]
        AdminWorkstations["Admin Workstations<br/>Jump Servers<br/>10.0.5.100-120"]
        MFAServer["MFA Server<br/>Duo/Okta<br/>10.0.5.50"]
    end

    subgraph FirewallRules["Firewall Rules Engine"]
        Rule1["Rule 1: Block All (Default)<br/>Action: DENY"]
        Rule2["Rule 2: Allow HTTPS DMZ→Internet<br/>Port 443, TLS 1.2+"]
        Rule3["Rule 3: Allow HTTP DMZ→Internet<br/>Port 80, Redirect to HTTPS"]
        Rule4["Rule 4: Internal→DMZ on 3306<br/>DB Replication Only"]
        Rule5["Rule 5: Bastion→Internal SSH<br/>Port 22, Key Auth Only"]
        Rule6["Rule 6: SCADA Isolated<br/>No Inbound from Internal"]
        Rule7["Rule 7: OPC-UA Critical Devices<br/>Whitelist Only 2 Sources"]
    end

    %% External connections
    AttackerNet -->|Attempts| Internet
    Customers -->|Legitimate| Internet

    %% Internet to Edge
    Internet -->|Traffic| WAF
    Internet -->|Traffic| CDN
    Internet -->|Requests| NGFW

    %% Edge Security Stack
    WAF -->|Filtered| NGFW
    CDN -->|Accelerated| NGFW
    NGFW -->|Allowed| DMZ

    %% DMZ Services
    DMZ -->|WebServers| APIGateway
    APIGateway -->|Gateway| WebServers
    DMZ -->|Mail| EmailGateway
    DMZ -->|DNS| DNSServers

    %% DMZ to Internal (Restricted)
    APIGateway -->|API Calls| AppServers
    WebServers -->|Backend| AppServers

    %% Internal Services
    AppServers -->|Session Data| CacheLayer
    AppServers -->|Async Jobs| MessageQueue
    MonitoringLan -->|Scrapes| AppServers

    %% Internal to Data (Restricted)
    AppServers -->|Read/Write| DatabasePrimary
    DatabasePrimary -->|Replication| DatabaseReplica
    DatabaseReplica -->|Analytics| GraphDatabase
    AppServers -->|Store Data| GraphDatabase

    %% Backup
    DatabasePrimary -->|Daily Backup| BackupVault
    GraphDatabase -->|Hourly Backup| BackupVault

    %% Management Access
    Bastion -->|SSH/RDP| AppServers
    AdminWorkstations -->|SSH| Bastion
    Bastion -->|SSH| DatabasePrimary
    AdminWorkstations -->|MFA| MFAServer

    %% Critical Infrastructure (Isolated)
    DataPlane -->|Historian| Historian
    SCADA -->|Monitored| Historian
    HMI -->|Operator| SCADA
    FieldDevices -->|Sensor Data| SCADA
    HMI -->|OPC-UA| CriticalInfra

    %% Firewall rules apply
    Rule1 -.->|Applies to| NGFW
    Rule2 -.->|Allow| DMZ
    Rule3 -.->|Redirect| DMZ
    Rule4 -.->|Restrict| DatabaseReplica
    Rule5 -.->|Control| Bastion
    Rule6 -.->|Isolate| SCADA
    Rule7 -.->|Whitelist| FieldDevices

    %% Styling
    style Internet fill:#FCE4EC,stroke:#333
    style EdgeSecurity fill:#FFE0B2,stroke:#333,stroke-width:2px
    style DMZ fill:#FFCCBC,stroke:#E74C3C,stroke-width:2px
    style Internal fill:#C5CAE9,stroke:#4A90E2,stroke-width:2px
    style DataPlane fill:#B3E5FC,stroke:#4A90E2,stroke-width:2px
    style CriticalInfra fill:#FFCDD2,stroke:#C0392B,stroke-width:3px
    style Management fill:#E0F2F1,stroke:#333,stroke-width:2px
    style FirewallRules fill:#FFF9C4,stroke:#333,stroke-width:2px
```

---

## 2. IEC 62443 Security Levels Implementation

### Level 1: Awareness Level
- Basic preventive measures
- **DMZ Location**: Edge firewall, WAF
- **Controls**: Basic firewalling, application-level filtering

### Level 2: Integrity Level
- Secure design principles
- **DMZ Location**: API Gateway, Email Gateway
- **Controls**: TLS encryption, basic access control

### Level 3: Availability Level
- Defense-in-depth approach
- **Internal Network**: App servers, caching
- **Controls**: Rate limiting, load balancing, monitoring

### Level 4: Confidentiality Level
- Comprehensive security controls
- **Data Plane**: Databases, backups
- **Controls**: Encryption at rest, audit logging, access control

### Level 5: Critical Level
- Maximum security measures
- **Critical Infrastructure**: SCADA, HMI
- **Controls**: Air-gapped network, strict whitelist, redundancy

---

## 3. Firewall Rules Detail Matrix

```mermaid
graph TB
    FW["Firewall Rule Engine<br/>pf / iptables / nftables"]

    subgraph Ingress["Ingress Rules (Internet → Organization)"]
        In1["Rule IN-1: Block All (Default)<br/>Policy: DENY<br/>Priority: 0<br/>Logging: Yes"]
        In2["Rule IN-2: HTTPS DMZ<br/>Protocol: TCP/443<br/>Source: ANY<br/>Dest: 10.0.1.0/25<br/>Action: ACCEPT<br/>TLS Version: 1.2+<br/>Priority: 100"]
        In3["Rule IN-3: HTTP to HTTPS<br/>Protocol: TCP/80<br/>Source: ANY<br/>Dest: 10.0.1.0/25<br/>Action: REDIRECT 443<br/>Priority: 110"]
        In4["Rule IN-4: DNS Queries<br/>Protocol: UDP/53<br/>Source: ANY<br/>Dest: 10.0.1.132-133<br/>Action: ACCEPT<br/>Priority: 120"]
    end

    subgraph Egress["Egress Rules (Organization → Internet)"]
        Out1["Rule OUT-1: Web Traffic<br/>Protocol: TCP/443<br/>Source: 10.0.1.0/24<br/>Dest: ANY<br/>Action: ACCEPT<br/>Rate Limit: 1000 Mbps<br/>Priority: 200"]
        Out2["Rule OUT-2: DNS Lookups<br/>Protocol: UDP/53<br/>Source: ANY<br/>Dest: 8.8.8.8, 1.1.1.1<br/>Action: ACCEPT<br/>Priority: 210"]
        Out3["Rule OUT-3: NTP Sync<br/>Protocol: UDP/123<br/>Source: ANY<br/>Dest: pool.ntp.org<br/>Action: ACCEPT<br/>Priority: 220"]
    end

    subgraph Internal["Internal Rules (Zone → Zone)"]
        Int1["Rule INT-1: App→DB<br/>Protocol: TCP/5432<br/>Source: 10.0.2.0/24<br/>Dest: 10.0.3.0/24<br/>Action: ACCEPT<br/>Priority: 300"]
        Int2["Rule INT-2: DB Replication<br/>Protocol: TCP/3306<br/>Source: 10.0.3.10<br/>Dest: 10.0.3.11-13<br/>Action: ACCEPT<br/>Priority: 310"]
        Int3["Rule INT-3: Bastion→Admin<br/>Protocol: TCP/22<br/>Source: 10.0.5.10-11<br/>Dest: 10.0.2.0/24<br/>Action: ACCEPT<br/>Key Auth Only<br/>Priority: 320"]
        Int4["Rule INT-4: SCADA Isolated<br/>Protocol: ANY<br/>Source: 10.0.4.0/24<br/>Dest: ! 10.0.3.50<br/>Action: DENY<br/>Priority: 0<br/>Logging: Critical"]
    end

    FW -->|Apply| Ingress
    FW -->|Apply| Egress
    FW -->|Apply| Internal

    style FW fill:#F39C12,color:#fff,stroke-width:2px
    style In1 fill:#E74C3C,color:#fff
    style In2 fill:#27AE60,color:#fff
    style In3 fill:#27AE60,color:#fff
    style In4 fill:#27AE60,color:#fff
    style Out1 fill:#27AE60,color:#fff
    style Out2 fill:#27AE60,color:#fff
    style Out3 fill:#27AE60,color:#fff
    style Int1 fill:#3498DB,color:#fff
    style Int2 fill:#3498DB,color:#fff
    style Int3 fill:#3498DB,color:#fff
    style Int4 fill:#C0392B,color:#fff,stroke-width:2px
```

---

## 4. Attack Path Analysis: 5-Hop Attack

```mermaid
graph LR
    subgraph Hop1["Hop 1: Initial Access<br/>Exposure: Public"]
        Attacker["Attacker<br/>203.0.113.45"]
        WebServer["Web Server<br/>10.0.1.50<br/>CVE-2024-5678<br/>RCE Vulnerability"]
    end

    subgraph Hop2["Hop 2: DMZ Lateral Movement<br/>Exposure: Medium"]
        APIGateway["API Gateway<br/>10.0.1.130<br/>Insecure API<br/>No Rate Limiting"]
        DatabaseProxy["Database Proxy<br/>10.0.1.140<br/>Credentials Cached"]
    end

    subgraph Hop3["Hop 3: Internal Penetration<br/>Exposure: Low"]
        AppServer["App Server<br/>10.0.2.50<br/>Weak Segmentation<br/>NFS Export"]
        Cache["Cache Server<br/>10.0.2.100<br/>No Auth Required"]
    end

    subgraph Hop4["Hop 4: Data Layer Access<br/>Exposure: Critical"]
        Database["Primary Database<br/>10.0.3.10<br/>PostgreSQL<br/>Admin Credentials Found"]
        BackupVault["Backup Vault<br/>10.0.3.50<br/>Unsecured Mount"]
    end

    subgraph Hop5["Hop 5: Critical Infrastructure<br/>Exposure: Maximum"]
        Historian["Data Historian<br/>10.0.4.50<br/>No Firewall Rules<br/>No Authentication"]
        SCADA["SCADA System<br/>10.0.4.0/24<br/>Can Be Controlled<br/>Full System Compromise"]
    end

    subgraph Controls["Security Controls<br/>Bypassed"]
        C1["WAF Bypass<br/>Polyglot Encoding"]
        C2["DMZ Segmentation<br/>Admin Credentials<br/>in Environment Vars"]
        C3["Network Segmentation<br/>Flat Network Assumption"]
        C4["Database Access Control<br/>Default Credentials"]
        C5["SCADA Firewall<br/>No Whitelist Rules"]
    end

    Attacker -->|Exploit| WebServer
    WebServer -->|Lateral Move| APIGateway
    APIGateway -->|Access| DatabaseProxy
    DatabaseProxy -->|Credentials| AppServer
    AppServer -->|Network Share| Cache
    Cache -->|Access| Database
    Database -->|Connection| BackupVault
    BackupVault -->|Access| Historian
    Historian -->|Control| SCADA

    WebServer -.->|Bypassed| C1
    APIGateway -.->|Bypassed| C2
    AppServer -.->|Bypassed| C3
    Database -.->|Bypassed| C4
    Historian -.->|Bypassed| C5

    style Attacker fill:#C0392B,color:#fff,stroke-width:2px
    style WebServer fill:#E74C3C,color:#fff
    style APIGateway fill:#F39C12,color:#fff
    style DatabaseProxy fill:#F39C12,color:#fff
    style AppServer fill:#E74C3C,color:#fff
    style Cache fill:#E74C3C,color:#fff
    style Database fill:#C0392B,color:#fff,stroke-width:2px
    style BackupVault fill:#C0392B,color:#fff,stroke-width:2px
    style Historian fill:#8B2E1F,color:#fff,stroke-width:3px
    style SCADA fill:#8B2E1F,color:#fff,stroke-width:3px
    style C1 fill:#FFE0B2,stroke:#333
    style C2 fill:#FFE0B2,stroke:#333
    style C3 fill:#FFE0B2,stroke:#333
    style C4 fill:#FFE0B2,stroke:#333
    style C5 fill:#FFE0B2,stroke:#333
```

### Attack Path Analysis

| Hop | Source | Target | Attack Type | CVSS | Mitigation |
|-----|--------|--------|-------------|------|-----------|
| 1 | Internet | Web Server | RCE (CVE-2024-5678) | 9.8 | Patch to v2.15+, WAF rules |
| 2 | DMZ | API Gateway | API Abuse | 7.2 | Rate limiting, API auth |
| 3 | Internal | App Server | Lateral Movement | 6.5 | Network segmentation, NFS auth |
| 4 | App | Database | Privilege Escalation | 8.1 | Database hardening, password mgmt |
| 5 | Database | SCADA | Critical Compromise | 10.0 | Air-gapping, firewall rules |

---

## 5. Network Segmentation & Access Control

```mermaid
graph TB
    subgraph Zones["Network Zones & VLAN Configuration"]
        VLAN1["VLAN 100: DMZ<br/>10.0.1.0/25<br/>CVLAN IDs: 100<br/>Interface: eth0.100"]
        VLAN2["VLAN 200: Internal<br/>10.0.2.0/24<br/>CVLAN IDs: 200<br/>Interface: eth0.200"]
        VLAN3["VLAN 300: Data<br/>10.0.3.0/25<br/>CVLAN IDs: 300<br/>Interface: eth0.300"]
        VLAN4["VLAN 400: SCADA<br/>10.0.4.0/24<br/>CVLAN IDs: 400<br/>Interface: eth0.400"]
        VLAN5["VLAN 500: Management<br/>10.0.5.0/24<br/>CVLAN IDs: 500<br/>Interface: eth0.500"]
    end

    subgraph ACL["Access Control Lists"]
        ACL1["DMZ→Internal: Limited<br/>Ports: 443 (API), 3306 (DB)<br/>Direction: Outbound"]
        ACL2["Internal→Data: Restricted<br/>Ports: 5432 (PostgreSQL)<br/>Sources: App Servers Only"]
        ACL3["Data→SCADA: None<br/>Direction: One-way only<br/>Via Historian"]
        ACL4["SCADA→External: None<br/>Direction: No outbound<br/>Status: Air-gapped"]
        ACL5["Management→All: Controlled<br/>Source: Bastion Hosts<br/>Auth: Key + MFA"]
    end

    subgraph Routing["Routing & Gateways"]
        Router1["Core Router<br/>eth0: LAN Router<br/>eth1: Internet<br/>eth2: Management"]
        GW1["DMZ Gateway<br/>10.0.1.1<br/>To: Internet"]
        GW2["Internal Gateway<br/>10.0.2.1<br/>From: DMZ, To: Data"]
        GW3["Data Gateway<br/>10.0.3.1<br/>From: Internal, To: SCADA"]
        GW4["SCADA Gateway<br/>10.0.4.1<br/>From: Historian Only"]
    end

    VLAN1 -->|Access| ACL1
    VLAN2 -->|Access| ACL2
    VLAN3 -->|Access| ACL3
    VLAN4 -->|Access| ACL4
    VLAN5 -->|Access| ACL5

    GW1 -->|Routes| Router1
    GW2 -->|Routes| Router1
    GW3 -->|Routes| Router1
    GW4 -->|Routes| Router1

    VLAN1 -->|Gateway| GW1
    VLAN2 -->|Gateway| GW2
    VLAN3 -->|Gateway| GW3
    VLAN4 -->|Gateway| GW4

    style Router1 fill:#F39C12,color:#fff,stroke-width:2px
    style GW1 fill:#3498DB,color:#fff
    style GW2 fill:#3498DB,color:#fff
    style GW3 fill:#3498DB,color:#fff
    style GW4 fill:#C0392B,color:#fff
```

---

## 6. Threat Modeling: Security Zones

```mermaid
graph TB
    subgraph TM["STRIDE Threat Model by Zone"]
        Zone1["DMZ Zone<br/>Threats:<br/>- Spoofing (S)<br/>- Network Sniffing (I)<br/>- DoS (D)<br/>Control: WAF, Rate Limit"]

        Zone2["Internal Zone<br/>Threats:<br/>- Privilege Escalation (E)<br/>- Tampering (T)<br/>- Denial of Service (D)<br/>Control: RBAC, Monitoring"]

        Zone3["Data Zone<br/>Threats:<br/>- Information Disclosure (I)<br/>- Repudiation (R)<br/>- Tampering (T)<br/>Control: Encryption, Audit"]

        Zone4["SCADA Zone<br/>Threats:<br/>- Elevation of Privilege (E)<br/>- Denial of Service (D)<br/>- Tampering (T)<br/>Control: Air-gap, Whitelist"]
    end

    Mitigation["Mitigations"]

    Zone1 -->|Addresses| Mitigation
    Zone2 -->|Addresses| Mitigation
    Zone3 -->|Addresses| Mitigation
    Zone4 -->|Addresses| Mitigation

    style Zone1 fill:#FFE0B2,stroke:#333
    style Zone2 fill:#E8F5E9,stroke:#333
    style Zone3 fill:#E3F2FD,stroke:#333
    style Zone4 fill:#FFCDD2,stroke:#C0392B,stroke-width:2px
```

---

## 7. Incident Response Network Diagram

```mermaid
graph TB
    Incident["INCIDENT DETECTED<br/>Suspicious Activity<br/>in DMZ"]

    subgraph Response["Immediate Response"]
        Isolate["Isolate Affected Device<br/>10.0.1.50<br/>VLAN 100→999<br/>Quarantine VLAN"]
        Preserve["Preserve Evidence<br/>Network Packets<br/>Memory Dump<br/>File System Snapshot"]
        Contain["Contain Lateral Movement<br/>Block egress to Internal<br/>Enable Deep Packet Inspection"]
    end

    subgraph Investigate["Investigation"]
        ForensicsLan["Forensics LAN<br/>10.0.5.200/28<br/>Isolated Network"]
        MemoryAnalysis["Memory Analysis<br/>Volatility Framework<br/>RAM Capture: 16GB"]
        NetworkCapture["Network Capture<br/>pcap Analysis<br/>Wireshark Review"]
        FileForensics["File Forensics<br/>Autopsy/FTK<br/>Disk Imaging"]
    end

    subgraph Remediation["Remediation"]
        Patch["Apply Security Patches<br/>CVE-2024-5678<br/>Update to v2.15.0"]
        HardenConfig["Harden Configuration<br/>Firewall Rules<br/>Disable RCE Vector"]
        DeployDetection["Deploy Detection<br/>IDS/IPS Signatures<br/>EDR Agent"]
    end

    subgraph Validation["Validation & Recovery"]
        Verification["Verify Fixes<br/>Penetration Test<br/>Compliance Check"]
        Recovery["Recover Device<br/>Restore from Backup<br/>Rejoin Network"]
        Monitoring["Monitor for Re-infection<br/>Alert on C2 Communication<br/>Behavioral Analysis"]
    end

    Incident -->|Response| Response
    Isolate -->|Evidence| Investigate
    Preserve -->|Analysis| Investigate
    Contain -->|Analysis| Investigate

    ForensicsLan -->|Analyze| MemoryAnalysis
    ForensicsLan -->|Analyze| NetworkCapture
    ForensicsLan -->|Analyze| FileForensics

    MemoryAnalysis -->|Findings| Remediation
    NetworkCapture -->|Findings| Remediation
    FileForensics -->|Findings| Remediation

    Patch -->|Validation| Validation
    HardenConfig -->|Validation| Validation
    DeployDetection -->|Validation| Validation

    Verification -->|Approved| Recovery
    Recovery -->|Online| Monitoring

    style Incident fill:#C0392B,color:#fff,stroke-width:3px
    style Response fill:#E74C3C,color:#fff
    style Investigate fill:#F39C12,color:#fff
    style Remediation fill:#27AE60,color:#fff
    style Validation fill:#4A90E2,color:#fff
```

---

## Summary: Network Security Architecture

### Key Security Principles Implemented
1. **Defense in Depth**: Multiple layers of security controls
2. **Zero Trust**: Verify every access request, regardless of source
3. **Least Privilege**: Minimal network access by default
4. **Network Segmentation**: Critical systems isolated from general network
5. **Monitoring & Logging**: All traffic and access logged
6. **Incident Response**: Isolation and forensics capabilities

### Critical Success Factors
- **Firewall Rules**: Strict default-deny policy
- **Segmentation**: 5-zone network with controlled inter-zone traffic
- **Access Control**: Bastion hosts for privileged access
- **Monitoring**: Real-time detection of anomalies
- **Resilience**: Backup and failover for critical systems
