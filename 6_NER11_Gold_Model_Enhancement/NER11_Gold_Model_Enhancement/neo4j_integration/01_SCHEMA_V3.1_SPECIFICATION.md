# Neo4j Schema v3.1 - Complete Specification

**Version**: 3.1 (Enhancement for NER11 Integration)  
**Date**: November 30, 2025  
**Status**: PRODUCTION-READY SPECIFICATION  
**Compatibility**: Neo4j 5.x+

---

## Executive Summary

This specification defines **Neo4j Schema v3.1**, designed to support the full 566 entity types from the NER11 Gold Standard model while maintaining database performance and query efficiency.

**Key Innovation**: **16 Super Labels** with **hierarchical property discriminators** to capture 100% of NER11 granularity without label explosion.

---

## 1. The 16 Super Labels

### Core Threat Intelligence (6 Labels)

#### 1.1 `ThreatActor`
**Purpose**: Nation-states, APT groups, hacktivists, cybercriminals

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  actorType: Enum["nation_state", "apt_group", "hacktivist", "crime_syndicate", "insider"],
  sophistication: Enum["low", "medium", "high", "advanced"],
  motivation: Enum["financial", "espionage", "disruption", "ideology"],
  first_seen: DateTime,
  last_seen: DateTime,
  aliases: [String],
  confidence: Float  // 0.0-1.0
}
```

**Indexes**:
```cypher
CREATE INDEX threat_actor_type FOR (n:ThreatActor) ON (n.actorType);
CREATE INDEX threat_actor_name FOR (n:ThreatActor) ON (n.name);
```

---

#### 1.2 `Malware`
**Purpose**: Ransomware, trojans, worms, rootkits, tools

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  malwareFamily: Enum["ransomware", "trojan", "worm", "rootkit", "rat", "loader", "dropper"],
  variant: String,
  platform: Enum["windows", "linux", "macos", "android", "ios", "iot"],
  capabilities: [String],  // ["persistence", "lateral_movement", "exfiltration"]
  first_seen: DateTime,
  hash_md5: String,
  hash_sha256: String
}
```

**Indexes**:
```cypher
CREATE INDEX malware_family FOR (n:Malware) ON (n.malwareFamily);
CREATE INDEX malware_hash FOR (n:Malware) ON (n.hash_sha256);
```

---

#### 1.3 `AttackPattern`
**Purpose**: MITRE ATT&CK techniques, tactics, procedures

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  patternType: Enum["technique", "tactic", "procedure", "capec"],
  mitre_id: String,  // "T1566.001"
  kill_chain_phase: String,
  description: Text,
  platforms: [String],
  data_sources: [String]
}
```

---

#### 1.4 `Vulnerability`
**Purpose**: CVEs, CWEs, zero-days, misconfigurations

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  vulnType: Enum["cve", "cwe", "zero_day", "misconfiguration"],
  cve_id: String,
  cvss_score: Float,
  severity: Enum["critical", "high", "medium", "low"],
  published_date: DateTime,
  patched: Boolean,
  affected_products: [String]
}
```

---

#### 1.5 `Indicator`
**Purpose**: IOCs, observables, artifacts

**Properties**:
```cypher
{
  id: UUID,
  value: String,
  indicatorType: Enum["ip", "domain", "url", "hash", "email", "file_path"],
  confidence: Float,
  first_seen: DateTime,
  last_seen: DateTime,
  tags: [String]
}
```

---

#### 1.6 `Campaign`
**Purpose**: Coordinated attack operations

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  campaignType: Enum["espionage", "ransomware", "supply_chain", "ddos"],
  start_date: DateTime,
  end_date: DateTime,
  objectives: [String],
  targets: [String]
}
```

---

### Infrastructure & Assets (3 Labels)

#### 2.1 `Asset`
**Purpose**: IT, OT, IoT, cloud resources

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  assetClass: Enum["IT", "OT", "IoT", "Cloud", "Facility"],
  deviceType: String,  // "plc", "server", "sensor", "substation"
  vendor: String,
  model: String,
  firmware_version: String,
  ip_address: String,
  mac_address: String,
  criticality: Enum["critical", "high", "medium", "low"],
  location_id: UUID  // FK to Location
}
```

**Indexes**:
```cypher
CREATE INDEX asset_class_device FOR (n:Asset) ON (n.assetClass, n.deviceType);
CREATE INDEX asset_criticality FOR (n:Asset) ON (n.criticality);
```

**Example Mappings**:
- NER `PLC` → `Asset {assetClass: "OT", deviceType: "programmable_logic_controller"}`
- NER `SUBSTATION` → `Asset {assetClass: "Facility", deviceType: "substation"}`
- NER `SERVER` → `Asset {assetClass: "IT", deviceType: "server"}`

---

#### 2.2 `Organization`
**Purpose**: Companies, vendors, agencies, sectors

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  orgType: Enum["vendor", "target", "government", "ngo", "sector"],
  industry: String,
  country: String,
  size: Enum["small", "medium", "large", "enterprise"],
  revenue: Float  // Optional
}
```

---

#### 2.3 `Location`
**Purpose**: Geographic and physical locations

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  locationType: Enum["country", "region", "city", "facility", "datacenter"],
  latitude: Float,
  longitude: Float,
  address: String
}
```

---

### Human Factors (3 Labels)

#### 3.1 `PsychTrait`
**Purpose**: Cognitive biases, personality traits, emotional states

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  traitType: Enum["CognitiveBias", "Personality", "Emotion", "LacanianDiscourse", "Perception"],
  subtype: String,  // "confirmation_bias", "narcissism", "anxiety"
  intensity: Float,  // 0.0-1.0
  description: Text,
  associated_user_id: UUID  // FK to User or ThreatActor
}
```

**Indexes**:
```cypher
CREATE INDEX psych_trait_subtype FOR (n:PsychTrait) ON (n.traitType, n.subtype);
```

**Example Mappings**:
- NER `CONFIRMATION_BIAS` → `PsychTrait {traitType: "CognitiveBias", subtype: "confirmation_bias"}`
- NER `NARCISSISM` → `PsychTrait {traitType: "Personality", subtype: "dark_triad_narcissism"}`
- NER `ANXIETY` → `PsychTrait {traitType: "Emotion", subtype: "anxiety"}`

---

#### 3.2 `Role`
**Purpose**: Job roles, responsibilities, access levels

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  roleType: Enum["security", "it", "executive", "operational", "administrative"],
  title: String,  // "CISO", "SOC Analyst", "CEO"
  privilege_level: Enum["low", "medium", "high", "admin"],
  department: String
}
```

**Example Mappings**:
- NER `CISO` → `Role {roleType: "security", title: "CISO", privilege_level: "high"}`
- NER `SYSADMIN` → `Role {roleType: "it", title: "System Administrator", privilege_level: "admin"}`

---

#### 3.3 `User`
**Purpose**: Individuals, accounts, identities

**Properties**:
```cypher
{
  id: UUID,
  username: String,
  email: String,
  role_id: UUID,  // FK to Role
  organization_id: UUID,  // FK to Organization
  is_insider_threat: Boolean,
  risk_score: Float  // 0.0-1.0
}
```

---

### Technical & Operational (4 Labels)

#### 4.1 `Protocol`
**Purpose**: Network and ICS communication protocols

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  protocolType: Enum["ICS", "Network", "Application", "Proprietary"],
  standard: String,  // "Modbus", "IEC 61850", "HTTPS"
  port: Integer,
  encryption: Boolean,
  vulnerabilities: [String]  // CVE IDs
}
```

**Example Mappings**:
- NER `MODBUS` → `Protocol {protocolType: "ICS", standard: "Modbus", port: 502}`
- NER `IEC_61850` → `Protocol {protocolType: "ICS", standard: "IEC 61850"}`
- NER `HTTPS` → `Protocol {protocolType: "Network", standard: "TLS/SSL", port: 443}`

---

#### 4.2 `Software`
**Purpose**: Applications, libraries, packages, SBOM

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  softwareType: Enum["application", "library", "framework", "os", "firmware"],
  version: String,
  vendor: String,
  cpe: String,  // Common Platform Enumeration
  license: String
}
```

---

#### 4.3 `Event`
**Purpose**: Security incidents, breaches, alerts

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  eventType: Enum["incident", "breach", "alert", "anomaly"],
  severity: Enum["critical", "high", "medium", "low"],
  timestamp: DateTime,
  status: Enum["open", "investigating", "contained", "resolved"],
  affected_assets: [UUID]
}
```

---

#### 4.4 `Control`
**Purpose**: Security controls, mitigations, safeguards

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  controlType: Enum["preventive", "detective", "corrective", "compensating"],
  framework: String,  // "NIST CSF", "ISO 27001"
  effectiveness: Float,  // 0.0-1.0
  implementation_status: Enum["planned", "partial", "full"]
}
```

---

### Economics & Impact (1 Label)

#### 5.1 `EconomicMetric`
**Purpose**: Financial impact, costs, market data

**Properties**:
```cypher
{
  id: UUID,
  name: String,
  metricType: Enum["Market", "Loss", "Penalty", "Investment", "Revenue"],
  category: String,  // "stock_valuation", "breach_cost", "ransom_amount"
  amount: Float,
  currency: String,  // "USD", "EUR"
  timestamp: DateTime,
  organization_id: UUID  // FK to Organization
}
```

**Example Mappings**:
- NER `STOCK_PRICE` → `EconomicMetric {metricType: "Market", category: "stock_valuation"}`
- NER `BREACH_COST` → `EconomicMetric {metricType: "Loss", category: "incident_cost"}`
- NER `GDPR_FINE` → `EconomicMetric {metricType: "Penalty", category: "regulatory_fine"}`

---

## 2. Relationship Types

### Core Relationships

```cypher
// Threat Actor Relationships
(:ThreatActor)-[:USES]->(:Malware)
(:ThreatActor)-[:EXPLOITS]->(:Vulnerability)
(:ThreatActor)-[:TARGETS]->(:Asset|Organization)
(:ThreatActor)-[:EMPLOYS]->(:AttackPattern)
(:ThreatActor)-[:EXHIBITS]->(:PsychTrait)
(:ThreatActor)-[:CONDUCTS]->(:Campaign)

// Malware Relationships
(:Malware)-[:TARGETS]->(:Asset)
(:Malware)-[:EXPLOITS]->(:Vulnerability)
(:Malware)-[:COMMUNICATES_VIA]->(:Protocol)
(:Malware)-[:DROPS]->(:Indicator)

// Asset Relationships
(:Asset)-[:LOCATED_AT]->(:Location)
(:Asset)-[:OWNED_BY]->(:Organization)
(:Asset)-[:RUNS]->(:Software)
(:Asset)-[:USES_PROTOCOL]->(:Protocol)
(:Asset)-[:PROTECTED_BY]->(:Control)
(:Asset)-[:VULNERABLE_TO]->(:Vulnerability)

// User/Role Relationships
(:User)-[:HAS_ROLE]->(:Role)
(:User)-[:WORKS_FOR]->(:Organization)
(:User)-[:EXHIBITS]->(:PsychTrait)
(:User)-[:ACCESSES]->(:Asset)

// Event Relationships
(:Event)-[:AFFECTS]->(:Asset)
(:Event)-[:ATTRIBUTED_TO]->(:ThreatActor)
(:Event)-[:INVOLVES]->(:Malware)
(:Event)-[:RESULTS_IN]->(:EconomicMetric)

// Economic Relationships
(:EconomicMetric)-[:IMPACTS]->(:Organization)
(:EconomicMetric)-[:CAUSED_BY]->(:Event)
```

---

## 3. Performance Optimization

### Composite Indexes

```cypher
// Critical for query performance
CREATE INDEX asset_class_device FOR (n:Asset) ON (n.assetClass, n.deviceType);
CREATE INDEX psych_trait_subtype FOR (n:PsychTrait) ON (n.traitType, n.subtype);
CREATE INDEX malware_family FOR (n:Malware) ON (n.malwareFamily);
CREATE INDEX threat_actor_type FOR (n:ThreatActor) ON (n.actorType);
CREATE INDEX vulnerability_severity FOR (n:Vulnerability) ON (n.severity, n.cvss_score);
CREATE INDEX economic_metric_type FOR (n:EconomicMetric) ON (n.metricType, n.category);
```

### Full-Text Search Indexes

```cypher
CREATE FULLTEXT INDEX threat_actor_search FOR (n:ThreatActor) ON EACH [n.name, n.aliases];
CREATE FULLTEXT INDEX malware_search FOR (n:Malware) ON EACH [n.name, n.variant];
CREATE FULLTEXT INDEX asset_search FOR (n:Asset) ON EACH [n.name, n.vendor, n.model];
```

---

## 4. Migration from v3.0 to v3.1

### New Labels Added

- `PsychTrait` (NEW)
- `EconomicMetric` (NEW)
- `Protocol` (NEW)
- `Role` (NEW)
- `Software` (NEW)
- `Control` (NEW)

### Enhanced Labels

- `Asset`: Added `assetClass` and `deviceType` properties
- `ThreatActor`: Added `actorType` property
- `Malware`: Added `malwareFamily` property

### Backward Compatibility

All v3.0 queries will continue to work. New properties are optional and can be added incrementally.

---

## 5. Query Examples

### Example 1: Find All PLCs Vulnerable to Specific CVE

```cypher
MATCH (a:Asset)-[:VULNERABLE_TO]->(v:Vulnerability)
WHERE a.assetClass = 'OT' 
  AND a.deviceType = 'programmable_logic_controller'
  AND v.cve_id = 'CVE-2023-12345'
RETURN a.name, a.vendor, a.model, v.cvss_score
```

### Example 2: Detect Insider Threats with Narcissistic Traits

```cypher
MATCH (u:User)-[:EXHIBITS]->(p:PsychTrait)
WHERE p.traitType = 'Personality' 
  AND p.subtype = 'dark_triad_narcissism'
  AND u.risk_score > 0.7
RETURN u.username, u.email, p.intensity, u.risk_score
ORDER BY u.risk_score DESC
```

### Example 3: Calculate Total Breach Cost by Organization

```cypher
MATCH (o:Organization)<-[:IMPACTS]-(em:EconomicMetric)
WHERE em.metricType = 'Loss'
RETURN o.name, 
       sum(em.amount) as total_loss,
       count(em) as incident_count
ORDER BY total_loss DESC
```

### Example 4: Find Threat Actors Targeting Energy Sector via Modbus

```cypher
MATCH (ta:ThreatActor)-[:TARGETS]->(a:Asset)-[:USES_PROTOCOL]->(p:Protocol)
WHERE a.assetClass = 'OT'
  AND p.standard = 'Modbus'
MATCH (a)-[:OWNED_BY]->(o:Organization)
WHERE o.industry = 'Energy'
RETURN ta.name, count(DISTINCT a) as targeted_assets, collect(DISTINCT o.name) as organizations
```

---

## 6. Data Validation Rules

### Required Properties

- All nodes MUST have: `id`, `name`
- `Asset` MUST have: `assetClass`, `deviceType`
- `PsychTrait` MUST have: `traitType`, `subtype`
- `EconomicMetric` MUST have: `metricType`, `amount`, `currency`

### Enum Validation

All enum properties MUST use predefined values (enforced at application layer).

### Referential Integrity

Foreign key properties (e.g., `organization_id`) MUST reference existing nodes.

---

## 7. Schema Versioning

**Current Version**: 3.1  
**Previous Version**: 3.0  
**Next Planned**: 3.2 (Q2 2026)

**Changelog**:
- v3.1 (2025-11-30): Added 6 new labels, enhanced properties for NER11 integration
- v3.0 (2025-11-19): Initial AEON schema with 18 labels

---

**Status**: ✅ Production-Ready  
**Approval**: Pending Executive Review  
**Implementation**: Ready for Migration
