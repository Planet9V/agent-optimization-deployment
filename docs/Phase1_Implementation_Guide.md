# Phase 1 Implementation Guide
**Cybersecurity Digital Twin - Core Schema Foundation**

**Created:** 2025-10-29
**Phase Duration:** Weeks 1-4
**Status:** 🔄 IN PROGRESS

---

## Executive Summary

Phase 1 establishes the foundational Neo4j schema for cybersecurity digital twin with support for 20+ hop multi-layer graph traversals. This phase focuses on core vulnerability intelligence (CVE/CWE/CAPEC/ATT&CK) integration and basic customer namespace isolation.

**Key Deliverables:**
- ✅ Neo4j schema with 8-layer architecture
- 🔄 NVD API connector for CVE ingestion (IN PROGRESS)
- ⏳ MITRE ATT&CK STIX 2.1 importer
- ⏳ Customer namespace isolation mechanism
- ⏳ 20+ hop attack path query templates

---

## Architecture Overview

### 8-Layer Schema Design

```
Layer 1: Physical Asset Layer
  ├─ PhysicalAsset (buildings, vehicles, fleets)
  ├─ Device (ICS/SCADA, IT hardware)
  ├─ HardwareComponent (modules, interfaces)
  └─ Location (geographic/hierarchical)

Layer 2: Network & Communication Layer
  ├─ NetworkInterface
  ├─ Network
  ├─ SecurityZone (IEC 62443)
  └─ Conduit (zone-to-zone communication)

Layer 3: Software & Application Layer
  ├─ Software
  ├─ SoftwareComponent (SBOM)
  ├─ Application
  └─ Firmware

Layer 4: Vulnerability & Threat Layer ⭐ CURRENT FOCUS
  ├─ CVE (Common Vulnerabilities and Exposures)
  ├─ CWE (Common Weakness Enumeration)
  ├─ CAPEC (Common Attack Pattern Enumeration)
  ├─ Technique (MITRE ATT&CK)
  ├─ ThreatActor
  ├─ ThreatActorProfile (psychometric)
  └─ Exploit

Layer 5: Attack Surface & Exposure Layer
  ├─ AttackSurface
  ├─ AttackPath
  └─ AttackPathStep

Layer 6: Organizational & Business Layer
  ├─ Organization
  ├─ BusinessProcess
  └─ Compliance

Layer 7: Failure Propagation & Impact Layer
  ├─ FailureMode
  ├─ FailureScenario
  └─ Impact

Layer 8: Mitigation & Remediation Layer
  ├─ Mitigation
  └─ Priority (Now/Next/Never)
```

---

## Implementation Steps

### Week 1-2: Foundation Setup ✅ COMPLETED

**1. Schema Definition Files Created:**
- ✅ `schemas/neo4j/00_constraints_indexes.cypher` - 40+ constraints, 20+ indexes
- ✅ `schemas/neo4j/01_layer_physical_asset.cypher` - Digital twin hierarchy
- ✅ `schemas/neo4j/04_layer_vulnerability_threat.cypher` - CVE/CWE/CAPEC/ATT&CK correlation

**2. Data Ingestion Infrastructure:**
- ✅ `src/ingestors/nvd_api_connector.py` - NVD API 2.0 client with rate limiting
- ✅ `config/neo4j_connection.env.example` - Environment configuration template

**3. Directory Structure:**
```
/home/jim/2_OXOT_Projects_Dev/
├── schemas/
│   ├── neo4j/          # Cypher schema files
│   ├── openspg/        # OpenSPG schema (Phase 6)
│   └── validation/     # Validation queries
├── src/
│   ├── ingestors/      # Data ingestion scripts
│   ├── connectors/     # External API connectors
│   └── utils/          # Shared utilities
├── config/             # Configuration files
└── docs/               # Documentation
```

### Week 3-4: Initial Data Ingestion 🔄 IN PROGRESS

**1. Deploy Neo4j Schema:**
```bash
# Connect to Neo4j
cypher-shell -u neo4j -p <password>

# Execute schema files in order
:source schemas/neo4j/00_constraints_indexes.cypher
:source schemas/neo4j/01_layer_physical_asset.cypher
:source schemas/neo4j/04_layer_vulnerability_threat.cypher
```

**2. Install Python Dependencies:**
```bash
cd /home/jim/2_OXOT_Projects_Dev
python3 -m venv venv
source venv/bin/activate
pip install requests neo4j python-dotenv tqdm
```

**3. Configure Environment:**
```bash
cp config/neo4j_connection.env.example .env
# Edit .env with actual credentials
nano .env
```

**4. Run NVD CVE Ingestion:**
```bash
# Fetch CVEs from last 30 days (incremental)
python3 src/ingestors/nvd_api_connector.py

# Or fetch all CRITICAL CVEs from last year
# Modify script parameters as needed
```

**Expected Output:**
- 2,000-5,000 CVEs ingested (last 30 days)
- CVE → CWE relationships established
- CVSS severity distribution validated

---

## Customer Namespace Isolation

### Namespace Strategy

**Shared Global Knowledge (is_shared: true):**
- `shared:nvd` - CVE/CPE/CVSS data
- `shared:cwe` - Common Weakness Enumeration
- `shared:capec` - Attack patterns
- `shared:attack` - MITRE ATT&CK techniques
- `shared:threat-intel` - Threat actors
- `shared:exploits` - Public exploits
- `shared:industry` - Industry reference architectures

**Customer-Specific Data (is_shared: false):**
- `customer:ABC` - Customer ABC's devices, software, configurations
- `customer:XYZ` - Customer XYZ's infrastructure
- `customer:EnterpriseCorp` - Enterprise Corporation

### Namespace Query Patterns

**Example 1: Customer-isolated vulnerability scan**
```cypher
// Find all CRITICAL vulnerabilities in customer ABC's software
MATCH (s:Software {customer_namespace: 'customer:ABC'})
  -[:HAS_VULNERABILITY]->(cve:CVE {is_shared: true})
WHERE cve.cvssV3Severity = 'CRITICAL'
  AND cve.hasExploit = true
RETURN s.name AS software,
       s.version AS version,
       cve.cveId AS vulnerability,
       cve.cvssV3BaseScore AS severity
ORDER BY cve.cvssV3BaseScore DESC;
```

**Example 2: Cross-customer threat intelligence (shared knowledge only)**
```cypher
// Find threat actors targeting specific industry (shared data)
MATCH (ta:ThreatActor {is_shared: true})-[:USES_TTP]->(t:Technique)
WHERE 'energy' IN ta.targeted_sectors
RETURN ta.name AS threat_actor,
       ta.sophistication AS sophistication,
       collect(DISTINCT t.name) AS techniques;
```

---

## Multi-Hop Attack Chain Examples

### Example 1: Component → Vulnerability → Threat Actor (8 hops)

```cypher
// Find attack chains from train brake component to threat actors
MATCH path = (comp:HardwareComponent {name: 'Electronic Brake Control Unit'})
  -[:INSTALLED_IN]->(device:Device)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:HAS_EXPLOIT]->(exploit:Exploit)
  -[:USED_BY_THREAT_ACTOR]->(ta:ThreatActor)
  -[:HAS_PROFILE]->(profile:ThreatActorProfile)
WHERE cve.cvssV3BaseScore >= 7.0
RETURN comp.name AS component,
       device.name AS installed_in,
       fw.version AS firmware_version,
       cve.cveId AS vulnerability,
       cve.cvssV3BaseScore AS severity,
       ta.name AS threat_actor,
       profile.intent_primary AS actor_intent,
       length(path) AS total_hops;
```

### Example 2: Fleet → Component Vulnerabilities (20+ hop aggregation)

```cypher
// Find all vulnerabilities in regional rail fleet
MATCH path = (fleet:PhysicalAsset {id: 'asset-fleet-regional'})
  <-[:PART_OF_FLEET*1..5]-(asset:PhysicalAsset)
  <-[:PART_OF_SUBSYSTEM]-(device:Device)
  <-[:INSTALLED_IN]-(comp:HardwareComponent)
  -[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssV3Severity IN ['HIGH', 'CRITICAL']
RETURN fleet.name AS fleet,
       count(DISTINCT asset) AS affected_assets,
       count(DISTINCT device) AS affected_devices,
       count(DISTINCT comp) AS affected_components,
       count(DISTINCT cve) AS unique_vulnerabilities,
       avg(cve.cvssV3BaseScore) AS avg_severity,
       max(length(path)) AS max_hop_depth;
```

---

## Validation Gates (Phase 1 Completion Criteria)

### ✅ Schema Validation

**Constraints Deployed:**
```cypher
SHOW CONSTRAINTS;
// Expected: 20+ unique constraints across all node types
```

**Indexes Deployed:**
```cypher
SHOW INDEXES;
// Expected: 25+ indexes including customer_namespace, cpe, cvss_score
```

### 📊 Data Quality Validation

**CVE Ingestion:**
```cypher
// Total CVE count
MATCH (cve:CVE) RETURN count(cve) AS total_cves;
// Expected: 2,000-5,000 CVEs (30-day incremental)

// CVE severity distribution
MATCH (cve:CVE)
RETURN cve.cvssV3Severity AS severity, count(*) AS count
ORDER BY count DESC;
// Expected: Distribution across LOW, MEDIUM, HIGH, CRITICAL
```

**CVE → CWE Relationships:**
```cypher
// Verify CVE-CWE linkage
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN count(*) AS total_cve_cwe_links;
// Expected: 70-80% of CVEs have CWE mappings
```

### ⚡ Performance Validation

**Query Performance Target: < 2 seconds (95th percentile)**

```cypher
// Test multi-hop query performance
PROFILE
MATCH path = (s:Software)-[:HAS_VULNERABILITY*1..3]->(cve:CVE)
  -[:IS_WEAKNESS_TYPE]->(cwe:CWE)
WHERE s.customer_namespace = 'customer:ABC'
RETURN count(path) AS total_paths;
// Expected: < 2000ms for 3-hop query
```

### 🔒 Namespace Isolation Validation

**Customer Data Isolation:**
```cypher
// Verify no customer data leakage across namespaces
MATCH (n)
WHERE n.customer_namespace STARTS WITH 'customer:'
  AND n.is_shared = true
RETURN count(n) AS leaked_nodes;
// Expected: 0 (customer data should never be marked shared)
```

---

## Known Limitations (Phase 1)

1. **SBOM Integration:** Not yet implemented (Phase 3)
2. **IEC 62443 Security Zones:** Schema defined, no data ingestion yet
3. **Attack Path Materialization:** Manual queries only, no automated path enumeration
4. **OpenSPG Integration:** Deferred to Phase 6
5. **Agent Zero Integration:** Deferred to Phase 7

---

## Next Steps (Phase 2 Preview)

**Phase 2: Cyber-Physical Integration (Weeks 5-8)**
- SAREF ontology loader for IoT/ICS device modeling
- ICS-SEC-KG integration for SCADA/DCS systems
- IEC 62443 security zone population
- Digital twin firmware-to-device correlation

---

## Troubleshooting

### Issue: NVD API Rate Limiting

**Symptom:** `429 Too Many Requests` errors

**Solution:**
```bash
# Register for NVD API key (increases limit 10x)
# https://nvd.nist.gov/developers/request-an-api-key

# Add to .env file
echo "NVD_API_KEY=your_api_key_here" >> .env
```

### Issue: Neo4j Connection Refused

**Symptom:** `ServiceUnavailable: Could not perform discovery`

**Solution:**
```bash
# Check Neo4j status
sudo systemctl status neo4j

# Start Neo4j if stopped
sudo systemctl start neo4j

# Verify connection
cypher-shell -u neo4j -p <password> "RETURN 'Connected' AS status;"
```

### Issue: Memory Exhaustion During Ingestion

**Symptom:** `java.lang.OutOfMemoryError: Java heap space`

**Solution:**
```bash
# Increase Neo4j heap size in neo4j.conf
sudo nano /etc/neo4j/neo4j.conf

# Add/modify:
dbms.memory.heap.initial_size=2g
dbms.memory.heap.max_size=4g

# Restart Neo4j
sudo systemctl restart neo4j
```

---

## Contact & Support

**Project Lead:** [Your Name]
**Phase 1 Timeline:** Weeks 1-4 (Oct 29 - Nov 25, 2025)
**Next Review:** End of Week 4 (Validation Gate)

**Documentation:**
- `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/README.md` - Ontology inventory
- `/home/jim/2_OXOT_Projects_Dev/docs/Ontology_Integration_Research_Report.md` - OSINT research

---

**Status:** 🔄 Phase 1 Implementation In Progress
**Last Updated:** 2025-10-29
