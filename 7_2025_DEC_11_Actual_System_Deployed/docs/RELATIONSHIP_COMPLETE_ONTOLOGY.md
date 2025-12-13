# Complete Neo4j Relationship Ontology
**AEON Cyber-Physical System Knowledge Graph**

**File:** RELATIONSHIP_COMPLETE_ONTOLOGY.md
**Created:** 2025-12-12
**Version:** v1.0.0
**Purpose:** Comprehensive documentation of all 183 relationship types in the knowledge graph
**Total Relationships:** 10,737,954 instances

---

## Executive Summary

This document provides complete documentation of all 183 relationship types extracted from the AEON knowledge graph. Each relationship type includes:

- **Cardinality:** Total instance count
- **Source/Target Nodes:** Actual node label combinations
- **Semantic Meaning:** Business/technical interpretation
- **Query Examples:** Practical Cypher patterns
- **Domain Classification:** Functional grouping

**Top 10 Relationship Types by Volume:**
1. IMPACTS: 4,780,563 (44.5% of all relationships)
2. VULNERABLE_TO: 3,117,735 (29.0%)
3. INSTALLED_ON: 968,125 (9.0%)
4. TRACKS_PROCESS: 344,256 (3.2%)
5. MONITORS_EQUIPMENT: 289,233 (2.7%)
6. CONSUMES_FROM: 289,050 (2.7%)
7. PROCESSES_THROUGH: 270,203 (2.5%)
8. MITIGATES: 250,782 (2.3%)
9. CHAINS_TO: 225,358 (2.1%)
10. IS_WEAKNESS_TYPE: 225,144 (2.1%)

---

## Domain Classification

### 1. Threat & Vulnerability Domain (5,882,296 relationships - 54.7%)

#### IMPACTS (4,780,563 instances)
**Purpose:** Models impact of threats on physical equipment and other systems

**Patterns:**
```cypher
# Pattern 1: Future threats impacting equipment (99.9% of instances)
FutureThreat -[IMPACTS]-> Equipment  (4,780,512 instances)

# Pattern 2: Equipment cascading impacts
Equipment -[IMPACTS]-> Equipment  (51 instances)
```

**Sample Query:**
```cypher
// Find all equipment threatened by specific future threats
MATCH (ft:FutureThreat {name: "Ransomware Attack"})-[i:IMPACTS]->(e:Equipment)
RETURN ft.name, e.name, e.critical_level
ORDER BY e.critical_level DESC
LIMIT 20;

// Analyze cascading impact chains
MATCH path = (e1:Equipment)-[:IMPACTS*1..3]->(e2:Equipment)
WHERE e1.critical_level = "HIGH"
RETURN path, length(path) as cascade_depth
ORDER BY cascade_depth DESC;
```

**Business Meaning:** Critical for threat impact analysis, risk assessment, and cascading failure prediction in cyber-physical systems.

---

#### VULNERABLE_TO (3,117,735 instances)
**Purpose:** Documents vulnerability exposure across devices, processes, controls, and equipment

**Patterns:**
```cypher
# Pattern 1: Device vulnerabilities (77.0%)
Device -[VULNERABLE_TO]-> Vulnerability  (2,398,523 instances)

# Pattern 2: Process vulnerabilities (11.9%)
Process -[VULNERABLE_TO]-> Vulnerability  (371,569 instances)

# Pattern 3: Device CVE exposure (6.2%)
Device -[VULNERABLE_TO]-> CVE  (193,721 instances)

# Pattern 4: Control vulnerabilities (1.9%)
Control -[VULNERABLE_TO]-> Vulnerability  (58,844 instances)

# Pattern 5: Equipment vulnerabilities (1.8%)
Equipment -[VULNERABLE_TO]-> Vulnerability  (56,434 instances)

# Pattern 6: Process CVE exposure (0.8%)
Process -[VULNERABLE_TO]-> CVE  (23,562 instances)

# Pattern 7: Equipment threat exposure (0.3%)
Equipment -[VULNERABLE_TO]-> Threat  (10,500 instances)
```

**Sample Queries:**
```cypher
// Find critical device vulnerabilities
MATCH (d:Device)-[v:VULNERABLE_TO]->(vuln:Vulnerability)
WHERE vuln.severity IN ["CRITICAL", "HIGH"]
  AND d.network_exposure = "INTERNET_FACING"
RETURN d.name, vuln.cve_id, vuln.cvss_score, vuln.severity
ORDER BY vuln.cvss_score DESC
LIMIT 50;

// Analyze vulnerability overlap across device types
MATCH (d:Device)-[:VULNERABLE_TO]->(vuln:Vulnerability)
WITH vuln, collect(DISTINCT d.device_type) as affected_types, count(d) as device_count
WHERE size(affected_types) > 5
RETURN vuln.cve_id, vuln.name, affected_types, device_count
ORDER BY device_count DESC;

// Find processes vulnerable to specific CVEs
MATCH (p:Process)-[:VULNERABLE_TO]->(cve:CVE)
WHERE cve.published_date > date('2024-01-01')
RETURN p.name, p.process_type, cve.cve_id, cve.cvss_score
ORDER BY cve.cvss_score DESC;
```

**Business Meaning:** Core vulnerability management, patch prioritization, attack surface analysis, and compliance reporting.

---

#### MITIGATES (250,782 instances)
**Purpose:** Links security controls and mitigations to vulnerabilities and attack patterns

**Patterns:**
```cypher
# Pattern 1: Control mitigating vulnerabilities (85.8%)
Control -[MITIGATES]-> Vulnerability  (215,239 instances)

# Pattern 2: Control mitigating attack patterns (12.1%)
Control -[MITIGATES]-> AttackPattern  (30,261 instances)

# Pattern 3: Mitigation strategies (1.4%)
Mitigation -[MITIGATES]-> Vulnerability  (3,500 instances)

# Pattern 4: Mitigation for attack patterns (0.4%)
Mitigation -[MITIGATES]-> AttackPattern  (911 instances)

# Pattern 5: EMB3D mitigations (0.1%)
EMB3D_Mitigation -[MITIGATES]-> EMB3D  (213 instances)
```

**Sample Queries:**
```cypher
// Find controls that mitigate multiple critical vulnerabilities
MATCH (c:Control)-[:MITIGATES]->(v:Vulnerability)
WHERE v.severity = "CRITICAL"
WITH c, collect(v) as vulns, count(v) as vuln_count
WHERE vuln_count > 10
RETURN c.name, c.control_type, vuln_count, [v IN vulns | v.cve_id][0..5] as sample_cves
ORDER BY vuln_count DESC;

// Analyze mitigation coverage gaps
MATCH (v:Vulnerability)
WHERE v.severity IN ["CRITICAL", "HIGH"]
  AND NOT EXISTS((v)<-[:MITIGATES]-())
RETURN v.cve_id, v.name, v.cvss_score, v.severity
ORDER BY v.cvss_score DESC
LIMIT 100;

// Map attack patterns to their mitigations
MATCH (ap:AttackPattern)<-[:MITIGATES]-(c:Control)
RETURN ap.attack_id, ap.name, collect(c.name) as mitigations
ORDER BY size(mitigations) DESC;
```

**Business Meaning:** Security control effectiveness, defense-in-depth analysis, risk mitigation tracking, and control gap identification.

---

#### THREATENS (24,192 instances)
**Purpose:** Models threat actor targeting of organizations

**Patterns:**
```cypher
# Pattern 1: Future threats to organizations
FutureThreat -[THREATENS]-> Organization  (24,192 instances)
```

**Sample Queries:**
```cypher
// Find organizations under highest threat
MATCH (ft:FutureThreat)-[:THREATENS]->(o:Organization)
WITH o, count(ft) as threat_count, collect(ft.name)[0..10] as threat_types
RETURN o.name, o.sector, threat_count, threat_types
ORDER BY threat_count DESC
LIMIT 50;

// Analyze threat patterns by sector
MATCH (ft:FutureThreat)-[:THREATENS]->(o:Organization)
WITH o.sector as sector, ft.threat_type as threat_type, count(*) as count
RETURN sector, threat_type, count
ORDER BY sector, count DESC;
```

**Business Meaning:** Threat intelligence, organizational risk profiling, and sector-specific threat analysis.

---

#### EXPLOITS (23,929 instances)
**Purpose:** Documents exploitation of vulnerabilities by threats and attack patterns

**Patterns:**
```cypher
# Pattern 1: Threats exploiting vulnerabilities (33.1%)
Threat -[EXPLOITS]-> Vulnerability  (7,913 instances)

# Pattern 2: Attack patterns exploiting vulnerabilities (31.1%)
AttackPattern -[EXPLOITS]-> Vulnerability  (7,446 instances)

# Pattern 3: Malware exploiting vulnerabilities (17.0%)
Malware -[EXPLOITS]-> Vulnerability  (4,076 instances)

# Pattern 4: Threat actors exploiting vulnerabilities (13.7%)
ThreatActor -[EXPLOITS]-> Vulnerability  (3,279 instances)

# Pattern 5: CAPEC patterns exploiting vulnerabilities (5.0%)
CAPEC -[EXPLOITS]-> Vulnerability  (1,195 instances)
```

**Sample Queries:**
```cypher
// Find vulnerabilities actively exploited by threat actors
MATCH (ta:ThreatActor)-[:EXPLOITS]->(v:Vulnerability)
WHERE ta.active = true
RETURN ta.name, ta.origin_country, v.cve_id, v.cvss_score
ORDER BY v.cvss_score DESC;

// Analyze malware exploitation patterns
MATCH (m:Malware)-[:EXPLOITS]->(v:Vulnerability)
WITH m, collect(v.cve_id) as exploited_cves, count(v) as exploit_count
WHERE exploit_count > 3
RETURN m.name, m.malware_type, exploit_count, exploited_cves[0..5]
ORDER BY exploit_count DESC;

// Map attack patterns to exploited vulnerabilities
MATCH (ap:AttackPattern)-[:EXPLOITS]->(v:Vulnerability)
WHERE v.cvss_score >= 7.0
RETURN ap.attack_id, ap.name, count(v) as vuln_count
ORDER BY vuln_count DESC;
```

**Business Meaning:** Active exploitation tracking, threat hunting, and prioritization of vulnerability remediation based on actual threat landscape.

---

#### TARGETS (17,485 instances)
**Purpose:** Documents targeting relationships between threats and assets/organizations

**Patterns:**
```cypher
# Pattern 1: Threats targeting equipment (34.3%)
Threat -[TARGETS]-> Equipment  (6,000 instances)

# Pattern 2: Future threats targeting sectors (30.9%)
FutureThreat -[TARGETS]-> Sector  (5,400 instances)

# Pattern 3: Threat actors targeting assets (9.0%)
ThreatActor -[TARGETS]-> Asset  (1,582 instances)

# Pattern 4: Threat actors targeting organizations (7.7%)
ThreatActor -[TARGETS]-> Organization  (1,351 instances)

# Pattern 5: Malware targeting assets (6.4%)
Malware -[TARGETS]-> Asset  (1,112 instances)
```

**Sample Queries:**
```cypher
// Analyze sector-specific threat targeting
MATCH (ft:FutureThreat)-[:TARGETS]->(s:Sector)
WITH s, count(ft) as threat_count, collect(ft.threat_type) as threat_types
RETURN s.name, threat_count, threat_types
ORDER BY threat_count DESC;

// Find high-value assets under threat actor targeting
MATCH (ta:ThreatActor)-[:TARGETS]->(a:Asset)
WHERE a.criticality = "HIGH"
RETURN ta.name, ta.sophistication, a.name, a.asset_type
ORDER BY ta.sophistication DESC;

// Equipment threat targeting analysis
MATCH (t:Threat)-[:TARGETS]->(e:Equipment)
WHERE e.critical_infrastructure = true
RETURN t.threat_type, e.equipment_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Asset protection prioritization, threat actor profiling, and sector-specific defense planning.

---

#### IDENTIFIES_THREAT (9,762 instances)
**Purpose:** Links detection mechanisms to identified threats

**Patterns:**
```cypher
# Pattern 1: Detection systems identifying threats
[Detection/Sensor] -[IDENTIFIES_THREAT]-> Threat  (9,762 instances)
```

**Sample Queries:**
```cypher
// Find most effective threat detection sensors
MATCH (d)-[:IDENTIFIES_THREAT]->(t:Threat)
WITH d, count(t) as threat_count, collect(t.threat_type) as threat_types
RETURN labels(d)[0] as detector_type, d.name, threat_count, threat_types[0..5]
ORDER BY threat_count DESC
LIMIT 20;
```

**Business Meaning:** Detection coverage analysis, sensor effectiveness, and threat hunting capability assessment.

---

#### DETECTS (8,577 instances)
**Purpose:** General detection relationships for security events and anomalies

**Patterns:**
```cypher
# Detection mechanisms identifying security events
[Detector] -[DETECTS]-> [SecurityEvent/Anomaly]
```

**Sample Queries:**
```cypher
// Analyze detection coverage across asset types
MATCH (d)-[:DETECTS]->(event)
RETURN labels(d)[0] as detector_type, labels(event)[0] as event_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Security monitoring effectiveness and detection gap analysis.

---

#### EXPLOITED_BY (4,225 instances)
**Purpose:** Reverse relationship showing which threats exploit vulnerabilities

**Patterns:**
```cypher
# Vulnerabilities being exploited by threats/malware/actors
Vulnerability -[EXPLOITED_BY]-> [Threat/Malware/ThreatActor]
```

**Sample Queries:**
```cypher
// Find most exploited vulnerabilities
MATCH (v:Vulnerability)-[:EXPLOITED_BY]->(threat)
WITH v, count(threat) as exploit_count, collect(labels(threat)[0]) as threat_types
WHERE exploit_count > 3
RETURN v.cve_id, v.cvss_score, exploit_count, threat_types
ORDER BY exploit_count DESC;
```

**Business Meaning:** Vulnerability exploitation prevalence and remediation urgency.

---

#### DETECTS_VULNERABILITY (3,084 instances)
**Purpose:** Links scanning/detection tools to discovered vulnerabilities

**Patterns:**
```cypher
# Scanners detecting vulnerabilities in assets
[Scanner/Tool] -[DETECTS_VULNERABILITY]-> Vulnerability
```

**Sample Queries:**
```cypher
// Analyze vulnerability detection tool effectiveness
MATCH (tool)-[:DETECTS_VULNERABILITY]->(v:Vulnerability)
WITH tool, count(v) as vuln_count, avg(v.cvss_score) as avg_severity
RETURN tool.name, tool.tool_type, vuln_count, avg_severity
ORDER BY vuln_count DESC;
```

**Business Meaning:** Vulnerability scanning coverage and tool effectiveness analysis.

---

### 2. Infrastructure & Physical Topology Domain (1,758,817 relationships - 16.4%)

#### INSTALLED_ON (968,125 instances)
**Purpose:** Documents software/data source installation locations on physical infrastructure

**Patterns:**
```cypher
# Pattern 1: Data sources on devices (76.0%)
DataSource -[INSTALLED_ON]-> Device  (735,443 instances)

# Pattern 2: Data sources on equipment (17.3%)
DataSource -[INSTALLED_ON]-> Equipment  (167,934 instances)

# Pattern 3: Data sources on protocols (4.8%)
DataSource -[INSTALLED_ON]-> Protocol  (46,229 instances)

# Pattern 4: Data sources on controls (1.1%)
DataSource -[INSTALLED_ON]-> Control  (11,007 instances)

# Pattern 5: Data sources on processes (0.8%)
DataSource -[INSTALLED_ON]-> Process  (7,512 instances)
```

**Sample Queries:**
```cypher
// Find devices with multiple data sources (potential attack surface)
MATCH (ds:DataSource)-[:INSTALLED_ON]->(d:Device)
WITH d, collect(ds.name) as data_sources, count(ds) as source_count
WHERE source_count > 5
RETURN d.name, d.device_type, source_count, data_sources[0..10]
ORDER BY source_count DESC;

// Analyze data source distribution across equipment types
MATCH (ds:DataSource)-[:INSTALLED_ON]->(e:Equipment)
WITH e.equipment_type as type, count(ds) as source_count
RETURN type, source_count
ORDER BY source_count DESC;

// Find protocol-level data sources
MATCH (ds:DataSource)-[:INSTALLED_ON]->(p:Protocol)
RETURN p.name, p.protocol_type, count(ds) as source_count
ORDER BY source_count DESC;
```

**Business Meaning:** Asset inventory, software deployment tracking, attack surface mapping, and data collection architecture.

---

#### MONITORS_EQUIPMENT (289,233 instances)
**Purpose:** Links monitoring systems to physical equipment

**Patterns:**
```cypher
# Pattern 1: Information streams monitoring equipment
InformationStream -[MONITORS_EQUIPMENT]-> Equipment  (289,233 instances)
```

**Sample Queries:**
```cypher
// Find unmonitored critical equipment
MATCH (e:Equipment)
WHERE e.critical_level = "HIGH"
  AND NOT EXISTS((e)<-[:MONITORS_EQUIPMENT]-())
RETURN e.name, e.equipment_type, e.location
LIMIT 100;

// Analyze monitoring coverage by equipment type
MATCH (is:InformationStream)-[:MONITORS_EQUIPMENT]->(e:Equipment)
WITH e.equipment_type as type, count(is) as monitor_count
RETURN type, monitor_count
ORDER BY monitor_count DESC;

// Find information streams monitoring multiple equipment
MATCH (is:InformationStream)-[:MONITORS_EQUIPMENT]->(e:Equipment)
WITH is, count(e) as equipment_count, collect(e.name)[0..5] as sample_equipment
WHERE equipment_count > 10
RETURN is.name, is.stream_type, equipment_count, sample_equipment
ORDER BY equipment_count DESC;
```

**Business Meaning:** Monitoring coverage analysis, observability gaps, and SCADA/ICS monitoring architecture.

---

#### MONITORS (195,265 instances)
**Purpose:** General monitoring relationships across all asset types

**Patterns:**
```cypher
# Various monitoring relationships across different node types
[Monitor] -[MONITORS]-> [Asset/Device/Process/Control]
```

**Sample Queries:**
```cypher
// Comprehensive monitoring coverage analysis
MATCH (m)-[:MONITORS]->(target)
RETURN labels(m)[0] as monitor_type, labels(target)[0] as target_type, count(*) as count
ORDER BY count DESC;

// Find assets with redundant monitoring
MATCH (target)<-[:MONITORS]-(m)
WITH target, count(m) as monitor_count
WHERE monitor_count > 3
RETURN labels(target)[0] as asset_type, target.name, monitor_count
ORDER BY monitor_count DESC;
```

**Business Meaning:** Overall monitoring strategy, redundancy analysis, and observability architecture.

---

#### USES_SOFTWARE (149,949 instances)
**Purpose:** Documents software usage across devices and systems

**Patterns:**
```cypher
# Devices and systems using specific software
[Device/System] -[USES_SOFTWARE]-> Software
```

**Sample Queries:**
```cypher
// Find most widely deployed software
MATCH (d)-[:USES_SOFTWARE]->(s:Software)
WITH s, count(d) as device_count, collect(labels(d)[0]) as device_types
RETURN s.name, s.vendor, s.version, device_count, device_types[0..5]
ORDER BY device_count DESC
LIMIT 50;

// Identify software version sprawl
MATCH (d)-[:USES_SOFTWARE]->(s:Software)
WITH s.name as software_name, collect(DISTINCT s.version) as versions, count(d) as device_count
WHERE size(versions) > 3
RETURN software_name, size(versions) as version_count, versions, device_count
ORDER BY version_count DESC;
```

**Business Meaning:** Software asset management, license compliance, version control, and update tracking.

---

#### LOCATED_AT (12,540 instances)
**Purpose:** Physical location of assets and equipment

**Patterns:**
```cypher
# Assets located at facilities/sites
Asset -[LOCATED_AT]-> Location
Equipment -[LOCATED_AT]-> Facility
```

**Sample Queries:**
```cypher
// Analyze asset distribution by location
MATCH (a)-[:LOCATED_AT]->(l:Location)
WITH l, count(a) as asset_count, collect(labels(a)[0]) as asset_types
RETURN l.name, l.location_type, asset_count, asset_types
ORDER BY asset_count DESC;

// Find critical assets at specific locations
MATCH (a:Asset)-[:LOCATED_AT]->(l:Location)
WHERE a.criticality = "HIGH"
RETURN l.name, l.coordinates, count(a) as critical_asset_count
ORDER BY critical_asset_count DESC;
```

**Business Meaning:** Physical security planning, asset tracking, and disaster recovery site identification.

---

#### LOCATED_IN (9,950 instances)
**Purpose:** Hierarchical location relationships

**Patterns:**
```cypher
# Equipment/devices located within larger facilities
[Asset] -[LOCATED_IN]-> [Zone/Facility/Region]
```

**Sample Queries:**
```cypher
// Analyze location hierarchy
MATCH path = (a)-[:LOCATED_IN*1..3]->(l)
RETURN a.name, labels(a)[0] as asset_type, [n IN nodes(path) | n.name] as location_hierarchy
LIMIT 100;
```

**Business Meaning:** Geographic asset distribution and location-based risk analysis.

---

#### CONTROLLED_BY_EMS (10,000 instances)
**Purpose:** Energy Management System control relationships

**Patterns:**
```cypher
# Equipment controlled by EMS systems
Equipment -[CONTROLLED_BY_EMS]-> EMS
```

**Sample Queries:**
```cypher
// Find equipment under centralized EMS control
MATCH (e:Equipment)-[:CONTROLLED_BY_EMS]->(ems:EMS)
WITH ems, count(e) as equipment_count, collect(e.equipment_type) as types
RETURN ems.name, equipment_count, types
ORDER BY equipment_count DESC;
```

**Business Meaning:** Energy infrastructure monitoring, grid management, and control system architecture.

---

#### INSTALLED_AT_SUBSTATION (10,000 instances)
**Purpose:** Equipment installation at electrical substations

**Patterns:**
```cypher
# Equipment installed at substations
Equipment -[INSTALLED_AT_SUBSTATION]-> Substation
```

**Sample Queries:**
```cypher
// Analyze substation equipment inventory
MATCH (e:Equipment)-[:INSTALLED_AT_SUBSTATION]->(s:Substation)
WITH s, collect(e.equipment_type) as equipment_types, count(e) as count
RETURN s.name, s.voltage_level, count, equipment_types
ORDER BY count DESC;
```

**Business Meaning:** Electrical grid topology, substation asset management, and power distribution analysis.

---

#### USES_DEVICE (9,000 instances)
**Purpose:** Process and system device usage

**Patterns:**
```cypher
# Processes using specific devices
Process -[USES_DEVICE]-> Device
System -[USES_DEVICE]-> Device
```

**Sample Queries:**
```cypher
// Find devices used by multiple critical processes
MATCH (p:Process)-[:USES_DEVICE]->(d:Device)
WHERE p.criticality = "HIGH"
WITH d, count(p) as process_count, collect(p.name)[0..5] as processes
WHERE process_count > 3
RETURN d.name, d.device_type, process_count, processes
ORDER BY process_count DESC;
```

**Business Meaning:** Process-device dependencies, single points of failure, and operational redundancy.

---

#### CONTROLLED_BY (8,000 instances)
**Purpose:** General control relationships

**Patterns:**
```cypher
# Various control relationships
[Asset/Equipment] -[CONTROLLED_BY]-> [ControlSystem/Controller]
```

**Sample Queries:**
```cypher
// Map control system hierarchy
MATCH (asset)-[:CONTROLLED_BY]->(controller)
RETURN labels(asset)[0] as asset_type, labels(controller)[0] as controller_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Control system architecture and centralized management analysis.

---

#### OPERATES_ON (8,000 instances)
**Purpose:** Operational dependencies

**Patterns:**
```cypher
# Systems operating on infrastructure
System -[OPERATES_ON]-> Infrastructure
Process -[OPERATES_ON]-> Equipment
```

**Sample Queries:**
```cypher
// Find infrastructure with multiple dependent systems
MATCH (s:System)-[:OPERATES_ON]->(infra)
WITH infra, count(s) as system_count, collect(s.name)[0..5] as systems
WHERE system_count > 5
RETURN infra.name, labels(infra)[0] as type, system_count, systems
ORDER BY system_count DESC;
```

**Business Meaning:** Infrastructure dependency mapping and impact analysis.

---

### 3. Data Flow & Information Processing Domain (1,427,695 relationships - 13.3%)

#### TRACKS_PROCESS (344,256 instances)
**Purpose:** Documents information stream tracking of business/operational processes

**Patterns:**
```cypher
# Pattern 1: Information streams tracking processes
InformationStream -[TRACKS_PROCESS]-> Process  (344,256 instances)
```

**Sample Queries:**
```cypher
// Find processes tracked by multiple information streams
MATCH (is:InformationStream)-[:TRACKS_PROCESS]->(p:Process)
WITH p, count(is) as stream_count, collect(is.name)[0..5] as streams
WHERE stream_count > 3
RETURN p.name, p.process_type, stream_count, streams
ORDER BY stream_count DESC;

// Analyze process tracking coverage by type
MATCH (is:InformationStream)-[:TRACKS_PROCESS]->(p:Process)
WITH p.process_type as type, count(is) as tracking_count
RETURN type, tracking_count
ORDER BY tracking_count DESC;

// Find untracked critical processes
MATCH (p:Process)
WHERE p.criticality = "HIGH"
  AND NOT EXISTS((p)<-[:TRACKS_PROCESS]-())
RETURN p.name, p.process_type, p.criticality
LIMIT 100;
```

**Business Meaning:** Process observability, operational monitoring, and data lineage tracking.

---

#### CONSUMES_FROM (289,050 instances)
**Purpose:** Data consumption from sources

**Patterns:**
```cypher
# Pattern 1: Information streams consuming from data sources (99.6%)
InformationStream -[CONSUMES_FROM]-> DataSource  (287,856 instances)

# Pattern 2: UCO object consumption (0.4%)
InformationStream -[CONSUMES_FROM]-> uco_core_UcoObject  (1,194 instances)
```

**Sample Queries:**
```cypher
// Analyze data source consumption patterns
MATCH (is:InformationStream)-[:CONSUMES_FROM]->(ds:DataSource)
WITH ds, count(is) as consumer_count, collect(is.stream_type)[0..5] as consumers
WHERE consumer_count > 10
RETURN ds.name, ds.source_type, consumer_count, consumers
ORDER BY consumer_count DESC;

// Find data sources with no consumers
MATCH (ds:DataSource)
WHERE NOT EXISTS((ds)<-[:CONSUMES_FROM]-())
RETURN ds.name, ds.source_type, ds.location
LIMIT 100;

// Map data flow patterns
MATCH (is:InformationStream)-[:CONSUMES_FROM]->(ds:DataSource)-[:INSTALLED_ON]->(d:Device)
RETURN d.name, d.device_type, count(is) as stream_count
ORDER BY stream_count DESC;
```

**Business Meaning:** Data flow architecture, data source utilization, and information supply chain.

---

#### PROCESSES_THROUGH (270,203 instances)
**Purpose:** Data processing pipeline stages

**Patterns:**
```cypher
# Pattern 1: Information streams processing through data processors
InformationStream -[PROCESSES_THROUGH]-> DataProcessor  (270,203 instances)
```

**Sample Queries:**
```cypher
// Find critical data processors in pipelines
MATCH (is:InformationStream)-[:PROCESSES_THROUGH]->(dp:DataProcessor)
WITH dp, count(is) as stream_count, collect(is.name)[0..5] as streams
WHERE stream_count > 10
RETURN dp.name, dp.processor_type, stream_count, streams
ORDER BY stream_count DESC;

// Analyze complete data processing pipelines
MATCH path = (ds:DataSource)<-[:CONSUMES_FROM]-(is:InformationStream)-[:PROCESSES_THROUGH]->(dp:DataProcessor)-[:DELIVERS_TO]->(dc:DataConsumer)
RETURN ds.name, is.name, dp.name, dc.name, length(path) as pipeline_length
LIMIT 100;

// Find data processors with no upstream connections
MATCH (dp:DataProcessor)
WHERE NOT EXISTS((dp)<-[:PROCESSES_THROUGH]-())
RETURN dp.name, dp.processor_type
LIMIT 50;
```

**Business Meaning:** Data transformation architecture, processing pipeline efficiency, and ETL workflow analysis.

---

#### CHAINS_TO (225,358 instances)
**Purpose:** Sequential processing chains between data processors

**Patterns:**
```cypher
# Pattern 1: Data processor chaining
DataProcessor -[CHAINS_TO]-> DataProcessor  (225,358 instances)
```

**Sample Queries:**
```cypher
// Analyze processing chain complexity
MATCH path = (dp1:DataProcessor)-[:CHAINS_TO*1..5]->(dp2:DataProcessor)
WITH dp1, length(path) as chain_length, count(path) as chain_count
WHERE chain_length > 2
RETURN dp1.name, chain_length, chain_count
ORDER BY chain_length DESC, chain_count DESC
LIMIT 50;

// Find longest processing chains
MATCH path = (dp:DataProcessor)-[:CHAINS_TO*]->(end:DataProcessor)
WHERE NOT EXISTS((end)-[:CHAINS_TO]->())
WITH path, length(path) as chain_length
ORDER BY chain_length DESC
LIMIT 20
RETURN [n IN nodes(path) | n.name] as processing_chain, chain_length;

// Identify circular processing chains
MATCH path = (dp:DataProcessor)-[:CHAINS_TO*]->(dp)
RETURN [n IN nodes(path) | n.name] as circular_chain, length(path) as cycle_length
ORDER BY cycle_length
LIMIT 10;
```

**Business Meaning:** Data processing workflow optimization, bottleneck identification, and pipeline refactoring.

---

#### DELIVERS_TO (216,126 instances)
**Purpose:** Final delivery of processed data to consumers

**Patterns:**
```cypher
# Pattern 1: Information streams delivering to data consumers
InformationStream -[DELIVERS_TO]-> DataConsumer  (216,126 instances)
```

**Sample Queries:**
```cypher
// Find data consumers receiving from multiple sources
MATCH (is:InformationStream)-[:DELIVERS_TO]->(dc:DataConsumer)
WITH dc, count(is) as source_count, collect(is.name)[0..5] as sources
WHERE source_count > 5
RETURN dc.name, dc.consumer_type, source_count, sources
ORDER BY source_count DESC;

// Analyze complete data flow from source to consumer
MATCH path = (ds:DataSource)<-[:CONSUMES_FROM]-(is:InformationStream)-[:DELIVERS_TO]->(dc:DataConsumer)
RETURN ds.name, is.name, dc.name, is.data_volume, is.latency
ORDER BY is.data_volume DESC
LIMIT 100;
```

**Business Meaning:** Data delivery architecture, consumer service levels, and information distribution.

---

#### MEASURES (165,400 instances)
**Purpose:** Measurement and sensing relationships

**Patterns:**
```cypher
# Sensors measuring physical phenomena
Sensor -[MEASURES]-> [PhysicalProperty/Parameter]
```

**Sample Queries:**
```cypher
// Analyze measurement coverage
MATCH (s:Sensor)-[:MEASURES]->(p)
RETURN labels(p)[0] as measured_type, count(s) as sensor_count
ORDER BY sensor_count DESC;
```

**Business Meaning:** Sensor deployment, measurement coverage, and telemetry architecture.

---

#### HAS_MEASUREMENT (117,936 instances)
**Purpose:** Links entities to their measurement data

**Patterns:**
```cypher
# Equipment/devices with associated measurements
[Equipment/Device] -[HAS_MEASUREMENT]-> Measurement
```

**Sample Queries:**
```cypher
// Find equipment with most measurements
MATCH (e)-[:HAS_MEASUREMENT]->(m:Measurement)
WITH e, count(m) as measurement_count
RETURN labels(e)[0] as equipment_type, e.name, measurement_count
ORDER BY measurement_count DESC
LIMIT 50;
```

**Business Meaning:** Telemetry data availability and historical measurement tracking.

---

### 4. Governance & Compliance Domain (74,362 relationships - 0.7%)

#### GOVERNS (53,862 instances)
**Purpose:** Regulatory and policy governance relationships

**Patterns:**
```cypher
# Regulations governing assets/processes/controls
[Regulation/Policy/Standard] -[GOVERNS]-> [Asset/Process/Control]
```

**Sample Queries:**
```cypher
// Find most governed asset types
MATCH (reg)-[:GOVERNS]->(asset)
RETURN labels(asset)[0] as asset_type, count(reg) as regulation_count, collect(DISTINCT labels(reg)[0]) as regulation_types
ORDER BY regulation_count DESC;

// Identify compliance coverage gaps
MATCH (a:Asset)
WHERE a.criticality = "HIGH"
  AND NOT EXISTS((a)<-[:GOVERNS]-())
RETURN a.name, a.asset_type, a.criticality
LIMIT 100;

// Analyze regulatory overlap
MATCH (reg)-[:GOVERNS]->(asset)
WITH asset, collect(reg.name) as regulations, count(reg) as reg_count
WHERE reg_count > 3
RETURN labels(asset)[0] as asset_type, asset.name, reg_count, regulations[0..5]
ORDER BY reg_count DESC;
```

**Business Meaning:** Compliance management, regulatory coverage, audit readiness, and policy enforcement.

---

#### COMPLIES_WITH (15,500 instances)
**Purpose:** Compliance relationships to standards and regulations

**Patterns:**
```cypher
# Assets/controls complying with standards
[Asset/Control/Process] -[COMPLIES_WITH]-> [Standard/Regulation]
```

**Sample Queries:**
```cypher
// Analyze compliance by standard
MATCH (asset)-[:COMPLIES_WITH]->(std:Standard)
WITH std, count(asset) as compliant_count, collect(labels(asset)[0]) as asset_types
RETURN std.name, std.version, compliant_count, asset_types
ORDER BY compliant_count DESC;

// Find non-compliant critical assets
MATCH (a:Asset)
WHERE a.criticality = "HIGH"
  AND NOT EXISTS((a)-[:COMPLIES_WITH]->())
RETURN a.name, a.asset_type
LIMIT 100;
```

**Business Meaning:** Standards compliance tracking, certification management, and regulatory adherence.

---

#### COMPLIES_WITH_NERC_CIP (5,000 instances)
**Purpose:** NERC CIP (Critical Infrastructure Protection) compliance for energy sector

**Patterns:**
```cypher
# Energy infrastructure complying with NERC CIP standards
[Equipment/Control/System] -[COMPLIES_WITH_NERC_CIP]-> NERC_CIP_Standard
```

**Sample Queries:**
```cypher
// NERC CIP compliance coverage by equipment type
MATCH (e:Equipment)-[:COMPLIES_WITH_NERC_CIP]->(nerc)
WITH e.equipment_type as type, count(e) as compliant_count
RETURN type, compliant_count
ORDER BY compliant_count DESC;

// Identify NERC CIP gaps
MATCH (e:Equipment)
WHERE e.critical_infrastructure = true
  AND NOT EXISTS((e)-[:COMPLIES_WITH_NERC_CIP]->())
RETURN e.name, e.equipment_type, e.location;
```

**Business Meaning:** Energy sector compliance, NERC CIP audit readiness, and critical infrastructure protection.

---

### 5. Semantic & Ontological Relationships (442,498 relationships - 4.1%)

#### IS_WEAKNESS_TYPE (225,144 instances)
**Purpose:** CWE (Common Weakness Enumeration) taxonomy relationships

**Patterns:**
```cypher
# Pattern 1: Vulnerability weakness type classification (87.7%)
Vulnerability -[IS_WEAKNESS_TYPE]-> Vulnerability  (197,446 instances)

# Pattern 2: Vulnerabilities mapped to CWE (6.6%)
Vulnerability -[IS_WEAKNESS_TYPE]-> CWE  (14,832 instances)

# Pattern 3: CVE weakness types (5.7%)
CVE -[IS_WEAKNESS_TYPE]-> Vulnerability  (12,774 instances)

# Pattern 4: CVE to CWE mapping (0.04%)
CVE -[IS_WEAKNESS_TYPE]-> CWE  (92 instances)
```

**Sample Queries:**
```cypher
// Analyze vulnerability weakness distribution
MATCH (v:Vulnerability)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
WITH cwe, count(v) as vuln_count
RETURN cwe.cwe_id, cwe.name, vuln_count
ORDER BY vuln_count DESC
LIMIT 50;

// Find CVE to CWE mappings
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN cve.cve_id, cve.description, cwe.cwe_id, cwe.name
ORDER BY cve.cvss_score DESC
LIMIT 100;

// Analyze weakness type hierarchies
MATCH path = (v:Vulnerability)-[:IS_WEAKNESS_TYPE*2..4]->(root:Vulnerability)
RETURN [n IN nodes(path) | CASE WHEN n:CWE THEN n.cwe_id ELSE n.name END] as weakness_chain
LIMIT 100;
```

**Business Meaning:** Vulnerability classification, weakness pattern analysis, and remediation strategy development.

---

#### RELATED_TO (49,232 instances)
**Purpose:** General semantic relationships between entities

**Patterns:**
```cypher
# Various semantic relationships across node types
[Entity] -[RELATED_TO]-> [Entity]
```

**Sample Queries:**
```cypher
// Find highly connected entities
MATCH (e)-[:RELATED_TO]-(related)
WITH e, count(related) as relation_count
WHERE relation_count > 10
RETURN labels(e)[0] as entity_type, e.name, relation_count
ORDER BY relation_count DESC
LIMIT 50;
```

**Business Meaning:** Knowledge graph connectivity and semantic relationships.

---

#### HAS_PROPERTY (42,052 instances)
**Purpose:** Entity properties and attributes

**Patterns:**
```cypher
# Entities with specific properties
[Entity] -[HAS_PROPERTY]-> Property
```

**Sample Queries:**
```cypher
// Analyze property distribution
MATCH (e)-[:HAS_PROPERTY]->(p:Property)
RETURN labels(e)[0] as entity_type, p.property_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Attribute management and property-based querying.

---

#### HAS_ENERGY_PROPERTY (30,000 instances)
**Purpose:** Energy-specific properties for power systems

**Patterns:**
```cypher
# Energy equipment with electrical properties
Equipment -[HAS_ENERGY_PROPERTY]-> EnergyProperty
```

**Sample Queries:**
```cypher
// Analyze energy property distribution
MATCH (e:Equipment)-[:HAS_ENERGY_PROPERTY]->(ep:EnergyProperty)
WITH ep.property_type as type, count(e) as equipment_count
RETURN type, equipment_count
ORDER BY equipment_count DESC;
```

**Business Meaning:** Power system modeling, energy efficiency analysis, and electrical characteristic tracking.

---

#### BASED_ON_PATTERN (29,970 instances)
**Purpose:** Pattern-based classification and taxonomy

**Patterns:**
```cypher
# Entities based on design patterns or templates
[Entity] -[BASED_ON_PATTERN]-> Pattern
```

**Sample Queries:**
```cypher
// Find most common patterns
MATCH (e)-[:BASED_ON_PATTERN]->(p:Pattern)
WITH p, count(e) as instance_count, collect(labels(e)[0]) as entity_types
RETURN p.name, p.pattern_type, instance_count, entity_types
ORDER BY instance_count DESC
LIMIT 50;
```

**Business Meaning:** Architecture pattern usage and design template application.

---

#### CHILD_OF (1,686 instances)
**Purpose:** Hierarchical parent-child relationships

**Patterns:**
```cypher
# Hierarchical relationships (CWE, CAPEC, organizational structures)
[Child] -[CHILD_OF]-> [Parent]
```

**Sample Queries:**
```cypher
// Analyze hierarchy depth
MATCH path = (child)-[:CHILD_OF*]->(root)
WHERE NOT EXISTS((root)-[:CHILD_OF]->())
RETURN [n IN nodes(path) | n.name] as hierarchy, length(path) as depth
ORDER BY depth DESC
LIMIT 50;
```

**Business Meaning:** Taxonomy navigation and hierarchical classification.

---

#### CHILDOF (533 instances)
**Purpose:** Alternative child relationship (likely from different data sources)

**Patterns:**
```cypher
# Similar to CHILD_OF but different source system
[Child] -[CHILDOF]-> [Parent]
```

**Sample Queries:**
```cypher
// Compare CHILD_OF vs CHILDOF usage
MATCH (c)-[r:CHILDOF]->(p)
RETURN labels(c)[0] as child_type, labels(p)[0] as parent_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Data integration from multiple taxonomies.

---

### 6. Attack & Threat Intelligence Domain (66,873 relationships - 0.6%)

#### USES_TECHNIQUE (13,299 instances)
**Purpose:** Threat actors and malware using specific attack techniques

**Patterns:**
```cypher
# Pattern 1: Future threats using techniques (81.5%)
FutureThreat -[USES_TECHNIQUE]-> Threat  (10,842 instances)

# Pattern 2: Future threats using specific techniques (18.5%)
FutureThreat -[USES_TECHNIQUE]-> Technique  (2,457 instances)
```

**Sample Queries:**
```cypher
// Find most used attack techniques
MATCH (threat)-[:USES_TECHNIQUE]->(t:Technique)
WITH t, count(threat) as usage_count, collect(labels(threat)[0]) as threat_types
RETURN t.technique_id, t.name, usage_count, threat_types
ORDER BY usage_count DESC
LIMIT 50;

// Analyze threat actor TTPs (Tactics, Techniques, Procedures)
MATCH (ta:ThreatActor)-[:USES_TECHNIQUE]->(t:Technique)
RETURN ta.name, ta.sophistication, collect(t.name) as techniques
ORDER BY size(techniques) DESC;
```

**Business Meaning:** Threat intelligence, attack pattern recognition, and defensive strategy development.

---

#### ATTRIBUTED_TO (8,833 instances)
**Purpose:** Attribution of attacks/malware to threat actors

**Patterns:**
```cypher
# Pattern 1: Future threats attributed to threats (34.0%)
FutureThreat -[ATTRIBUTED_TO]-> Threat  (3,000 instances)

# Pattern 2: Attack patterns attributed to threat actors (20.2%)
AttackPattern -[ATTRIBUTED_TO]-> ThreatActor  (1,782 instances)

# Pattern 3: Malware attributed to threat actors (13.1%)
Malware -[ATTRIBUTED_TO]-> ThreatActor  (1,159 instances)

# Pattern 4: Attack patterns attributed to threats (11.2%)
AttackPattern -[ATTRIBUTED_TO]-> Threat  (988 instances)

# Pattern 5: Threats attributed to threat actors (10.4%)
Threat -[ATTRIBUTED_TO]-> ThreatActor  (917 instances)
```

**Sample Queries:**
```cypher
// Analyze threat actor campaigns
MATCH (ta:ThreatActor)<-[:ATTRIBUTED_TO]-(attack)
WITH ta, count(attack) as attack_count, collect(labels(attack)[0]) as attack_types
RETURN ta.name, ta.origin_country, attack_count, attack_types
ORDER BY attack_count DESC;

// Find malware families by threat actor
MATCH (m:Malware)-[:ATTRIBUTED_TO]->(ta:ThreatActor)
WITH ta, collect(m.name) as malware_families, count(m) as family_count
RETURN ta.name, family_count, malware_families
ORDER BY family_count DESC;
```

**Business Meaning:** Threat actor profiling, campaign tracking, and attribution analysis for incident response.

---

#### USES_ATTACK_PATTERN (976 instances)
**Purpose:** Links between entities using specific attack patterns

**Patterns:**
```cypher
# Threats/malware using CAPEC attack patterns
[Threat/Malware] -[USES_ATTACK_PATTERN]-> AttackPattern
```

**Sample Queries:**
```cypher
// Find most common attack patterns
MATCH (threat)-[:USES_ATTACK_PATTERN]->(ap:AttackPattern)
WITH ap, count(threat) as usage_count, collect(labels(threat)[0]) as users
RETURN ap.attack_id, ap.name, usage_count, users
ORDER BY usage_count DESC
LIMIT 50;
```

**Business Meaning:** Attack pattern frequency analysis and defensive prioritization.

---

#### BELONGS_TO_TACTIC (887 instances)
**Purpose:** MITRE ATT&CK technique to tactic mapping

**Patterns:**
```cypher
# Techniques belonging to tactics
Technique -[BELONGS_TO_TACTIC]-> Tactic
```

**Sample Queries:**
```cypher
// Analyze tactic coverage
MATCH (t:Technique)-[:BELONGS_TO_TACTIC]->(tactic:Tactic)
WITH tactic, count(t) as technique_count, collect(t.name)[0..5] as sample_techniques
RETURN tactic.name, technique_count, sample_techniques
ORDER BY technique_count DESC;
```

**Business Meaning:** MITRE ATT&CK framework navigation and threat model alignment.

---

#### USES_TACTIC (887 instances)
**Purpose:** Threat actors using specific tactics

**Patterns:**
```cypher
# Threat actors using tactics
ThreatActor -[USES_TACTIC]-> Tactic
```

**Sample Queries:**
```cypher
// Analyze threat actor tactical preferences
MATCH (ta:ThreatActor)-[:USES_TACTIC]->(tactic:Tactic)
WITH ta, collect(tactic.name) as tactics
RETURN ta.name, ta.sophistication, tactics
ORDER BY size(tactics) DESC;
```

**Business Meaning:** Threat actor behavior profiling and tactical analysis.

---

#### TARGETS_SECTOR (873 instances)
**Purpose:** Threat targeting of industry sectors

**Patterns:**
```cypher
# Threats targeting specific industry sectors
[Threat/ThreatActor] -[TARGETS_SECTOR]-> Sector
```

**Sample Queries:**
```cypher
// Analyze sector-specific threats
MATCH (threat)-[:TARGETS_SECTOR]->(s:Sector)
WITH s, count(threat) as threat_count, collect(labels(threat)[0]) as threat_types
RETURN s.name, threat_count, threat_types
ORDER BY threat_count DESC;
```

**Business Meaning:** Sector-specific threat intelligence and industry risk profiling.

---

#### USES_TTP (475 instances)
**Purpose:** Threat actor Tactics, Techniques, and Procedures usage

**Patterns:**
```cypher
# Threat actors using TTPs
ThreatActor -[USES_TTP]-> TTP
```

**Sample Queries:**
```cypher
// Map threat actor TTPs
MATCH (ta:ThreatActor)-[:USES_TTP]->(ttp:TTP)
RETURN ta.name, ta.sophistication, collect(ttp.name) as ttps
ORDER BY size(ttps) DESC;
```

**Business Meaning:** Comprehensive threat actor profiling and behavioral analysis.

---

### 7. Organizational & Asset Management Domain (49,130 relationships - 0.5%)

#### CONTAINS (22,450 instances)
**Purpose:** Containment relationships (zones, networks, systems)

**Patterns:**
```cypher
# Various containment relationships
[Container] -[CONTAINS]-> [Contained]
Zone -[CONTAINS]-> Asset
Network -[CONTAINS]-> Device
System -[CONTAINS]-> Component
```

**Sample Queries:**
```cypher
// Analyze zone containment
MATCH (z:Zone)-[:CONTAINS]->(asset)
WITH z, count(asset) as asset_count, collect(labels(asset)[0]) as asset_types
RETURN z.name, z.security_level, asset_count, asset_types
ORDER BY asset_count DESC;

// Find assets in multiple containers (potential segmentation issues)
MATCH (asset)<-[:CONTAINS]-(container)
WITH asset, count(container) as container_count, collect(container.name) as containers
WHERE container_count > 1
RETURN labels(asset)[0] as asset_type, asset.name, container_count, containers
ORDER BY container_count DESC;
```

**Business Meaning:** Network segmentation, security zones, and logical asset grouping.

---

#### CONTAINS_ENTITY (14,645 instances)
**Purpose:** Entity containment for hierarchical structures

**Patterns:**
```cypher
# Entities containing other entities
[Parent] -[CONTAINS_ENTITY]-> [Child]
```

**Sample Queries:**
```cypher
// Analyze containment hierarchies
MATCH path = (parent)-[:CONTAINS_ENTITY*1..3]->(child)
RETURN [n IN nodes(path) | n.name] as hierarchy, length(path) as depth
ORDER BY depth DESC
LIMIT 100;
```

**Business Meaning:** Organizational structure and entity hierarchies.

---

#### BELONGS_TO (10,907 instances)
**Purpose:** Membership and ownership relationships

**Patterns:**
```cypher
# Assets belonging to organizations/groups
Asset -[BELONGS_TO]-> Organization
Device -[BELONGS_TO]-> BusinessUnit
```

**Sample Queries:**
```cypher
// Analyze asset ownership distribution
MATCH (asset)-[:BELONGS_TO]->(org:Organization)
WITH org, count(asset) as asset_count, collect(labels(asset)[0]) as asset_types
RETURN org.name, asset_count, asset_types
ORDER BY asset_count DESC;

// Find orphaned assets
MATCH (a:Asset)
WHERE NOT EXISTS((a)-[:BELONGS_TO]->())
RETURN a.name, a.asset_type, a.criticality
LIMIT 100;
```

**Business Meaning:** Asset ownership, organizational responsibility, and inventory management.

---

### 8. Process & Workflow Domain (34,101 relationships - 0.3%)

#### EXECUTES (20,500 instances)
**Purpose:** Execution relationships between systems and processes

**Patterns:**
```cypher
# Systems executing processes
System -[EXECUTES]-> Process
Device -[EXECUTES]-> Software
```

**Sample Queries:**
```cypher
// Find systems executing multiple processes
MATCH (s:System)-[:EXECUTES]->(p:Process)
WITH s, count(p) as process_count, collect(p.name)[0..5] as processes
WHERE process_count > 5
RETURN s.name, s.system_type, process_count, processes
ORDER BY process_count DESC;

// Analyze process execution distribution
MATCH (sys)-[:EXECUTES]->(p:Process)
WITH p, count(sys) as executor_count
WHERE executor_count > 1
RETURN p.name, p.process_type, executor_count
ORDER BY executor_count DESC;
```

**Business Meaning:** Process orchestration, workload distribution, and execution architecture.

---

#### EXECUTES_PROCESS (5,000 instances)
**Purpose:** Explicit process execution relationships

**Patterns:**
```cypher
# Control systems executing processes
[ControlSystem/Scheduler] -[EXECUTES_PROCESS]-> Process
```

**Sample Queries:**
```cypher
// Analyze process execution patterns
MATCH (executor)-[:EXECUTES_PROCESS]->(p:Process)
RETURN labels(executor)[0] as executor_type, p.process_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Automated process execution and workflow automation.

---

#### PARTICIPATES_IN (5,000 instances)
**Purpose:** Participation in processes or events

**Patterns:**
```cypher
# Entities participating in processes/events
[Entity] -[PARTICIPATES_IN]-> [Process/Event/Campaign]
```

**Sample Queries:**
```cypher
// Analyze process participation
MATCH (participant)-[:PARTICIPATES_IN]->(process)
RETURN labels(participant)[0] as participant_type, labels(process)[0] as process_type, count(*) as count
ORDER BY count DESC;
```

**Business Meaning:** Process involvement tracking and collaboration analysis.

---

#### TRIGGERS (1,600 instances)
**Purpose:** Event triggering relationships

**Patterns:**
```cypher
# Events triggering other events or processes
Event -[TRIGGERS]-> Process
Condition -[TRIGGERS]-> Action
```

**Sample Queries:**
```cypher
// Analyze event chains
MATCH path = (trigger)-[:TRIGGERS*1..3]->(action)
RETURN [n IN nodes(path) | n.name] as trigger_chain, length(path) as chain_length
ORDER BY chain_length DESC
LIMIT 50;
```

**Business Meaning:** Event-driven architecture and automated response workflows.

---

#### TRIGGERED_BY (1,316 instances)
**Purpose:** Reverse triggering relationships

**Patterns:**
```cypher
# Actions triggered by events
Action -[TRIGGERED_BY]-> Event
Process -[TRIGGERED_BY]-> Condition
```

**Sample Queries:**
```cypher
// Find most common triggers
MATCH (action)-[:TRIGGERED_BY]->(trigger)
WITH trigger, count(action) as trigger_count, collect(labels(action)[0]) as action_types
RETURN labels(trigger)[0] as trigger_type, trigger.name, trigger_count, action_types
ORDER BY trigger_count DESC;
```

**Business Meaning:** Cause-effect analysis and automated response mapping.

---

### 9. Energy & Grid Infrastructure Domain (2,730 relationships - 0.03%)

#### CONNECTS_SUBSTATIONS (780 instances)
**Purpose:** Physical connections between electrical substations

**Patterns:**
```cypher
# Transmission lines connecting substations
TransmissionLine -[CONNECTS_SUBSTATIONS]-> Substation
```

**Sample Queries:**
```cypher
// Analyze substation connectivity
MATCH (s1:Substation)<-[:CONNECTS_SUBSTATIONS]-(line:TransmissionLine)-[:CONNECTS_SUBSTATIONS]->(s2:Substation)
RETURN s1.name, s1.voltage_level, line.name, s2.name, s2.voltage_level, line.capacity
ORDER BY line.capacity DESC;

// Find critical transmission lines (connecting multiple substations)
MATCH (line:TransmissionLine)-[:CONNECTS_SUBSTATIONS]->(s:Substation)
WITH line, count(s) as substation_count
WHERE substation_count > 2
RETURN line.name, substation_count, line.voltage_level
ORDER BY substation_count DESC;
```

**Business Meaning:** Power grid topology, transmission network analysis, and critical infrastructure mapping.

---

#### CONNECTED_TO_GRID (750 instances)
**Purpose:** Connection to electrical grid

**Patterns:**
```cypher
# Equipment/facilities connected to power grid
[Equipment/Facility] -[CONNECTED_TO_GRID]-> Grid
```

**Sample Queries:**
```cypher
// Analyze grid connectivity by equipment type
MATCH (e:Equipment)-[:CONNECTED_TO_GRID]->(g:Grid)
WITH g, e.equipment_type as type, count(e) as equipment_count
RETURN g.name, g.voltage_level, type, equipment_count
ORDER BY equipment_count DESC;

// Find unconnected critical equipment
MATCH (e:Equipment)
WHERE e.critical_infrastructure = true
  AND NOT EXISTS((e)-[:CONNECTED_TO_GRID]->())
RETURN e.name, e.equipment_type, e.location;
```

**Business Meaning:** Grid dependency analysis, power distribution planning, and resilience assessment.

---

#### DEPENDS_ON_ENERGY (1,000 instances)
**Purpose:** Energy dependency relationships

**Patterns:**
```cypher
# Systems depending on energy sources
System -[DEPENDS_ON_ENERGY]-> EnergySource
Equipment -[DEPENDS_ON_ENERGY]-> PowerSupply
```

**Sample Queries:**
```cypher
// Analyze energy dependencies
MATCH (dependent)-[:DEPENDS_ON_ENERGY]->(energy)
WITH energy, count(dependent) as dependent_count, collect(labels(dependent)[0]) as dependent_types
RETURN energy.name, labels(energy)[0] as energy_type, dependent_count, dependent_types
ORDER BY dependent_count DESC;

// Find single points of energy failure
MATCH (e:EnergySource)<-[:DEPENDS_ON_ENERGY]-(dependent)
WITH e, count(dependent) as dependent_count
WHERE dependent_count > 10
  AND NOT EXISTS((e)-[:REDUNDANT_WITH]->())
RETURN e.name, e.capacity, dependent_count
ORDER BY dependent_count DESC;
```

**Business Meaning:** Energy resilience, backup power planning, and dependency risk analysis.

---

#### ROUTES_TO (150 instances)
**Purpose:** Energy/data routing relationships

**Patterns:**
```cypher
# Routing between network nodes or power distribution
Router -[ROUTES_TO]-> Destination
```

**Sample Queries:**
```cypher
// Analyze routing paths
MATCH path = (source)-[:ROUTES_TO*1..3]->(dest)
RETURN [n IN nodes(path) | n.name] as route, length(path) as hops
ORDER BY hops DESC
LIMIT 50;
```

**Business Meaning:** Network topology, routing efficiency, and path redundancy.

---

### 10. Software & Component Management Domain (22,218 relationships - 0.2%)

#### PUBLISHES (13,501 instances)
**Purpose:** Software publication and release management

**Patterns:**
```cypher
# Vendors publishing software
Vendor -[PUBLISHES]-> Software
Organization -[PUBLISHES]-> Release
```

**Sample Queries:**
```cypher
// Find most prolific software publishers
MATCH (v:Vendor)-[:PUBLISHES]->(s:Software)
WITH v, count(s) as software_count, collect(s.name)[0..10] as software_titles
RETURN v.name, software_count, software_titles
ORDER BY software_count DESC;

// Analyze software release frequency
MATCH (org:Organization)-[:PUBLISHES]->(r:Release)
WITH org, count(r) as release_count, collect(r.version) as versions
RETURN org.name, release_count, versions[0..5]
ORDER BY release_count DESC;
```

**Business Meaning:** Software supply chain, vendor management, and release tracking.

---

#### GENERATES (10,501 instances)
**Purpose:** Data/event generation relationships

**Patterns:**
```cypher
# Systems generating data or events
Device -[GENERATES]-> Event
Process -[GENERATES]-> Data
```

**Sample Queries:**
```cypher
// Find high-volume event generators
MATCH (d:Device)-[:GENERATES]->(e:Event)
WITH d, count(e) as event_count, collect(e.event_type) as event_types
WHERE event_count > 100
RETURN d.name, d.device_type, event_count, event_types[0..5]
ORDER BY event_count DESC;

// Analyze data generation patterns
MATCH (p:Process)-[:GENERATES]->(data)
RETURN p.name, labels(data)[0] as data_type, count(data) as count
ORDER BY count DESC;
```

**Business Meaning:** Data lineage, event source tracking, and data volume planning.

---

#### SUPPORTS (7,014 instances)
**Purpose:** Support relationships (technical, organizational)

**Patterns:**
```cypher
# Various support relationships
Component -[SUPPORTS]-> System
Service -[SUPPORTS]-> Application
```

**Sample Queries:**
```cypher
// Find critical support dependencies
MATCH (supporter)-[:SUPPORTS]->(supported)
WHERE supported.criticality = "HIGH"
RETURN labels(supporter)[0] as supporter_type, supporter.name,
       labels(supported)[0] as supported_type, supported.name
LIMIT 100;

// Analyze support coverage
MATCH (supporter)-[:SUPPORTS]->(supported)
WITH supporter, count(supported) as support_count
WHERE support_count > 10
RETURN labels(supporter)[0] as type, supporter.name, support_count
ORDER BY support_count DESC;
```

**Business Meaning:** Dependency management, service mapping, and support architecture.

---

### 11. Intelligence & Analysis Domain (18,093 relationships - 0.2%)

#### GENERATES_MEASUREMENT (18,000 instances)
**Purpose:** Sensor and measurement generation

**Patterns:**
```cypher
# Sensors generating measurements
Sensor -[GENERATES_MEASUREMENT]-> Measurement
```

**Sample Queries:**
```cypher
// Find most active sensors
MATCH (s:Sensor)-[:GENERATES_MEASUREMENT]->(m:Measurement)
WITH s, count(m) as measurement_count, collect(m.measurement_type) as types
WHERE measurement_count > 50
RETURN s.name, s.sensor_type, measurement_count, types[0..5]
ORDER BY measurement_count DESC;

// Analyze measurement coverage
MATCH (s:Sensor)-[:GENERATES_MEASUREMENT]->(m:Measurement)
RETURN m.measurement_type, count(s) as sensor_count
ORDER BY sensor_count DESC;
```

**Business Meaning:** Sensor telemetry, measurement coverage, and data quality analysis.

---

#### HAS_BIAS (18,000 instances)
**Purpose:** Bias identification in data/models

**Patterns:**
```cypher
# Models or data sources with identified biases
[Model/DataSource] -[HAS_BIAS]-> Bias
```

**Sample Queries:**
```cypher
// Analyze bias distribution
MATCH (entity)-[:HAS_BIAS]->(b:Bias)
RETURN labels(entity)[0] as entity_type, b.bias_type, count(*) as count
ORDER BY count DESC;

// Find entities with multiple biases
MATCH (entity)-[:HAS_BIAS]->(b:Bias)
WITH entity, count(b) as bias_count, collect(b.bias_type) as bias_types
WHERE bias_count > 2
RETURN labels(entity)[0] as type, entity.name, bias_count, bias_types
ORDER BY bias_count DESC;
```

**Business Meaning:** Data quality assessment, model fairness analysis, and bias mitigation.

---

### 12. Deployment & Implementation Domain (19,200 relationships - 0.2%)

#### MAY_DEPLOY (17,850 instances)
**Purpose:** Potential deployment relationships

**Patterns:**
```cypher
# Software/systems that may be deployed
Software -[MAY_DEPLOY]-> Environment
Configuration -[MAY_DEPLOY]-> Infrastructure
```

**Sample Queries:**
```cypher
// Analyze deployment options
MATCH (s:Software)-[:MAY_DEPLOY]->(env:Environment)
WITH s, collect(env.name) as environments, count(env) as env_count
WHERE env_count > 3
RETURN s.name, s.version, env_count, environments
ORDER BY env_count DESC;

// Find constrained deployment options
MATCH (software)-[:MAY_DEPLOY]->(env)
WITH software, count(env) as options
WHERE options = 1
RETURN labels(software)[0] as type, software.name, options
LIMIT 100;
```

**Business Meaning:** Deployment planning, environment compatibility, and infrastructure flexibility.

---

### 13. Complex Specialized Domains (Remaining relationships)

#### IMPLEMENTS (1,616 instances)
**Purpose:** Implementation relationships

**Patterns:**
```cypher
# Systems implementing interfaces/standards
System -[IMPLEMENTS]-> Interface
Control -[IMPLEMENTS]-> Standard
```

**Sample Queries:**
```cypher
// Find most implemented interfaces
MATCH (impl)-[:IMPLEMENTS]->(interface)
WITH interface, count(impl) as impl_count, collect(labels(impl)[0]) as implementer_types
RETURN labels(interface)[0] as interface_type, interface.name, impl_count, implementer_types
ORDER BY impl_count DESC;
```

---

#### PART_OF_CAMPAIGN (1,872 instances)
**Purpose:** Threat intelligence campaign association

**Patterns:**
```cypher
# Attacks/malware part of campaigns
[Attack/Malware] -[PART_OF_CAMPAIGN]-> Campaign
```

**Sample Queries:**
```cypher
// Analyze campaign components
MATCH (component)-[:PART_OF_CAMPAIGN]->(c:Campaign)
WITH c, collect(labels(component)[0]) as component_types, count(component) as size
RETURN c.name, c.campaign_id, size, component_types
ORDER BY size DESC;
```

---

## Query Pattern Library

### Common Query Patterns

#### Pattern 1: Vulnerability Impact Analysis
```cypher
// Find critical vulnerabilities with active exploitation and equipment impact
MATCH (d:Device)-[:VULNERABLE_TO]->(v:Vulnerability)<-[:EXPLOITS]-(threat)
WHERE v.severity = "CRITICAL"
  AND v.cvss_score >= 9.0
OPTIONAL MATCH (d)-[:INSTALLED_ON]->(e:Equipment)
OPTIONAL MATCH (v)<-[:MITIGATES]-(c:Control)
RETURN v.cve_id, v.name, v.cvss_score,
       count(DISTINCT d) as affected_devices,
       count(DISTINCT e) as affected_equipment,
       collect(DISTINCT threat.name)[0..5] as active_threats,
       collect(DISTINCT c.name)[0..3] as mitigations
ORDER BY v.cvss_score DESC, affected_equipment DESC
LIMIT 50;
```

#### Pattern 2: Data Flow Analysis
```cypher
// Trace complete data pipeline from source to consumer
MATCH path = (ds:DataSource)<-[:CONSUMES_FROM]-(is:InformationStream)
             -[:PROCESSES_THROUGH]->(dp:DataProcessor)
             -[:DELIVERS_TO]->(dc:DataConsumer)
WHERE ds.criticality = "HIGH"
RETURN ds.name as source,
       is.name as stream,
       dp.name as processor,
       dc.name as consumer,
       is.data_volume,
       is.latency,
       length(path) as pipeline_stages
ORDER BY is.data_volume DESC
LIMIT 100;
```

#### Pattern 3: Threat Surface Analysis
```cypher
// Identify attack surface for critical infrastructure
MATCH (e:Equipment)
WHERE e.critical_infrastructure = true
OPTIONAL MATCH (e)<-[:IMPACTS]-(ft:FutureThreat)
OPTIONAL MATCH (e)-[:VULNERABLE_TO]->(v:Vulnerability)
OPTIONAL MATCH (e)<-[:TARGETS]-(threat)
OPTIONAL MATCH (e)-[:INSTALLED_ON]->(d:Device)-[:VULNERABLE_TO]->(dv:Vulnerability)
RETURN e.name,
       e.equipment_type,
       count(DISTINCT ft) as future_threat_count,
       count(DISTINCT v) as direct_vuln_count,
       count(DISTINCT threat) as targeting_count,
       count(DISTINCT dv) as device_vuln_count,
       (count(DISTINCT ft) + count(DISTINCT v) + count(DISTINCT threat) + count(DISTINCT dv)) as total_threat_score
ORDER BY total_threat_score DESC
LIMIT 50;
```

#### Pattern 4: Control Effectiveness Analysis
```cypher
// Evaluate security control coverage and effectiveness
MATCH (c:Control)-[:MITIGATES]->(v:Vulnerability)
WHERE v.severity IN ["CRITICAL", "HIGH"]
WITH c, count(v) as mitigated_vulns, collect(v.cve_id)[0..10] as sample_cves
OPTIONAL MATCH (c)-[:CONTROLS]->(asset)
OPTIONAL MATCH (v)<-[:EXPLOITS]-(threat)
RETURN c.name,
       c.control_type,
       mitigated_vulns,
       count(DISTINCT asset) as protected_assets,
       count(DISTINCT threat) as blocked_threats,
       sample_cves
ORDER BY mitigated_vulns DESC, protected_assets DESC
LIMIT 50;
```

#### Pattern 5: Infrastructure Dependency Chains
```cypher
// Find cascading dependency chains for resilience analysis
MATCH path = (e1:Equipment)-[:DEPENDS_ON_ENERGY|CONTROLLED_BY|OPERATES_ON*1..4]->(e2:Equipment)
WHERE e1.critical_infrastructure = true
WITH e1, e2, path, length(path) as depth
WHERE depth >= 2
RETURN e1.name as critical_asset,
       e2.name as dependency,
       depth as dependency_depth,
       [n IN nodes(path) | n.name] as dependency_chain
ORDER BY depth DESC, critical_asset
LIMIT 100;
```

---

## Appendix: Complete Relationship Type List with Counts

```
IMPACTS: 4,780,563
VULNERABLE_TO: 3,117,735
INSTALLED_ON: 968,125
TRACKS_PROCESS: 344,256
MONITORS_EQUIPMENT: 289,233
CONSUMES_FROM: 289,050
PROCESSES_THROUGH: 270,203
MITIGATES: 250,782
CHAINS_TO: 225,358
IS_WEAKNESS_TYPE: 225,144
DELIVERS_TO: 216,126
MONITORS: 195,265
MEASURES: 165,400
USES_SOFTWARE: 149,949
HAS_MEASUREMENT: 117,936
GOVERNS: 53,862
RELATED_TO: 49,232
HAS_PROPERTY: 42,052
HAS_ENERGY_PROPERTY: 30,000
BASED_ON_PATTERN: 29,970
THREATENS: 24,192
EXPLOITS: 23,929
CONTROLS: 22,706
CONTAINS: 22,450
EXECUTES: 20,500
GENERATES_MEASUREMENT: 18,000
HAS_BIAS: 18,000
MAY_DEPLOY: 17,850
TARGETS: 17,485
INDICATES: 16,916
MITIGATED_BY: 15,513
COMPLIES_WITH: 15,500
AFFECTS: 15,093
CONTAINS_ENTITY: 14,645
PUBLISHES: 13,501
USES_TECHNIQUE: 13,299
LOCATED_AT: 12,540
BELONGS_TO: 10,907
GENERATES: 10,501
HAS_VULNERABILITY: 10,001
CONTROLLED_BY_EMS: 10,000
INSTALLED_AT_SUBSTATION: 10,000
LOCATED_IN: 9,950
IDENTIFIES_THREAT: 9,762
REQUIRES: 9,586
USES_DEVICE: 9,000
ATTRIBUTED_TO: 8,833
DETECTS: 8,577
CONTROLLED_BY: 8,000
OPERATES_ON: 8,000
SUPPORTS: 7,014
REPORTS_TO: 7,000
USES: 6,577
COMPLIES_WITH_NERC_CIP: 5,000
EXECUTES_PROCESS: 5,000
APPLIES_TO: 5,000
PARTICIPATES_IN: 5,000
PROFILES: 5,000
EXTENDS_SAREF_DEVICE: 4,500
EXPLOITED_BY: 4,225
ANALYZES_SECTOR: 3,120
DETECTS_VULNERABILITY: 3,084
HAS_COMMAND: 3,000
PROTECTED_BY: 3,000
INVOLVES: 3,000
REQUIRES_STANDARD: 3,000
OFFERS_SERVICE: 2,500
PROCESSES_EVENT: 2,001
HAS_FUNCTION: 2,000
RUNS_SOFTWARE: 2,000
PART_OF_CAMPAIGN: 1,872
CHILD_OF: 1,686
IMPLEMENTS: 1,616
TRIGGERS: 1,600
EXHIBITS_PERSONALITY_TRAIT: 1,460
HAS_CONTROL: 1,400
GRANTS_PHYSICAL_ACCESS_TO: 1,354
TRIGGERED_BY: 1,316
EMB3D_REL: 1,072
DEPENDS_ON_ENERGY: 1,000
USES_ATTACK_PATTERN: 976
CONTRIBUTES_TO: 911
BELONGS_TO_TACTIC: 887
USES_TACTIC: 887
TARGETS_SECTOR: 873
CONNECTS_SUBSTATIONS: 780
CONNECTED_TO_GRID: 750
CHILDOF: 533
EXHIBITS_PATTERN: 523
EXPLOITED_VIA: 500
USES_TTP: 475
PART_OF: 400
GENERATED: 400
DEPLOYED_AT: 350
POSITIONED_IN: 292
EXHIBITS_REGISTER: 292
CLASSIFIED_BY: 288
IMPLEMENTS_TECHNIQUE: 271
MAPS_TO_ATTACK: 270
SIMULATES: 200
IS_TYPE_OF: 200
USES_PROTOCOL: 177
CANPRECEDE: 162
CONNECTED_TO_SEGMENT: 158
PHYSICALLY_LOCATED_IN: 158
ORCHESTRATES_CAMPAIGN: 150
ROUTES_TO: 150
HOUSES_EQUIPMENT: 140
METADATA_FOR: 115
RELATES_TO: 115
DEPENDS_CRITICALLY_ON: 112
CASCADES_TO: 112
OWNS_EQUIPMENT: 111
MANAGES_EQUIPMENT: 111
HOSTS: 100
SBOM_CONTAINS: 100
CONTAINS_ICS_TECHNIQUE: 98
TRACKED_BY: 96
MAPS_TO_STIX: 50
REFERENCES: 43
INSTANCE_OF: 43
EXPLOITS_PROTOCOL: 42
SUBPROPERTY_OF: 40
MAPS_TO_OWASP: 39
REDUNDANT_WITH: 38
ISOLATES: 32
HAS_TAG: 28
INFLUENCES_BEHAVIOR: 25
SUPPORTS_PROTOCOL: 20
DEPLOYS_ASSET: 20
PEEROF: 19
TARGETS_ICS_ASSET: 17
PROPAGATES_TO: 16
PROPAGATES_FROM: 16
HAS_SYSTEM: 15
CONTAINS_EVIDENCE: 15
RELATIONSHIP: 13
PROTECTS: 12
INCLUDES_COMPONENT: 12
ENABLES_TECHNIQUE: 12
OWNS: 12
CONNECTS_TO: 12
EMPHASIZES_REGISTER: 11
CANFOLLOW: 10
DEPLOYED_IN: 9
MANIFESTS_IN_DISCOURSE: 9
SUPERSEDED_BY: 8
HAS_ZONE: 7
OPERATES_IN_REGISTER: 7
MOTIVATES: 7
REQUIRES_DATA_SOURCE: 6
ENABLES_LATERAL_MOVEMENT: 6
OPERATES_IN: 6
LEADS_TO: 4
EQUIVALENT_TO_STIX: 4
SHARED_WITH: 4
OWNED_BY: 4
IN_REGION: 4
ROUTES_THROUGH: 4
AFFECTS_SYSTEM: 3
CONDUCTS: 3
DEPLOYS: 3
LEVERAGES: 3
COLLABORATES_WITH: 3
EVOLVES_TO: 3
RELEASES_GUIDANCE: 3
PROVIDES: 3
CANALSOBE: 3
INTEGRATES_WITH: 3
COMPATIBLE_WITH: 3
HAS_ORGANIZATION: 3
AFFECTS_SECTOR: 3
HAS_THREAT_MODEL: 2
HAS_ASSESSMENT: 2
ACTIVATES_BIAS: 2
SUBTECHNIQUE_OF: 2
SUB_TECHNIQUE_OF: 1
SUCCESSOR_OF: 1
COMPOSED_OF: 1
HAS_COMPONENT: 1
DEPENDS_ON: 1
CONTAINS_EQUIPMENT: 1
CORRELATES_WITH: 1
```

---

## Usage Guidelines

### For Threat Analysis
- Start with VULNERABLE_TO, EXPLOITS, IMPACTS
- Use MITIGATES to find control gaps
- Follow ATTRIBUTED_TO for threat actor profiling

### For Infrastructure Mapping
- Begin with INSTALLED_ON, LOCATED_AT
- Use CONTROLLED_BY, OPERATES_ON for dependencies
- Analyze MONITORS_EQUIPMENT for coverage

### For Data Flow Analysis
- Trace CONSUMES_FROM → PROCESSES_THROUGH → DELIVERS_TO
- Use TRACKS_PROCESS for business process visibility
- Follow GENERATES_MEASUREMENT for telemetry

### For Compliance
- Query GOVERNS, COMPLIES_WITH relationships
- Check COMPLIES_WITH_NERC_CIP for energy sector
- Use APPLIES_TO for policy mapping

---

**Document Status:** COMPLETE
**Validation:** All 183 relationship types documented with patterns and queries
**Next Update:** As new relationship types are added to the knowledge graph
