# PROC-143: Industrial Protocol Analysis ETL

**Metadata:**
- **Procedure ID**: PROC-143
- **Enhancement**: E16 - Industrial Protocol Analysis
- **Priority**: High
- **Frequency**: Weekly (threat-triggered for OT/ICS campaigns)
- **Dependencies**: PROC-142 (Vendor Equipment mapping)
- **Estimated Duration**: 40-55 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Extract, transform, and load industrial protocol analysis data to identify OT/ICS-specific attack patterns, protocol vulnerabilities, and threat actor targeting of critical infrastructure using behavioral analysis of industrial communication protocols.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: How do threat actors psychologically target industrial protocols?
- **Q7 (Organizational Dynamics)**: What organizational gaps enable industrial protocol attacks?
- **Q8 (Threat Actor Behavior)**: What are the behavioral signatures of OT/ICS threat actors?

### Business Value
- Early detection of OT/ICS-specific attack campaigns
- Protocol-level vulnerability identification
- Threat actor TTPs specific to industrial environments
- Improved incident response for industrial protocol attacks
- Enhanced threat intelligence for critical infrastructure

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Network protocol captures (Modbus, DNP3, PROFINET, EtherNet/IP, OPC-UA)
- [ ] OT/ICS asset inventory with protocol mappings
- [ ] Vendor equipment database (from PROC-142)
- [ ] MITRE ATT&CK for ICS framework mappings
- [ ] Threat intelligence feeds (ICS-CERT alerts, Dragos Worldviews)
- [ ] Industrial control system logs (PLC, HMI, SCADA)
- [ ] Baseline protocol traffic patterns (normal operations)
- [ ] Known OT/ICS vulnerabilities (CVE database, vendor advisories)

### System Requirements
- [ ] Neo4j database with temporal graph capabilities
- [ ] Python 3.9+ with Scapy, pyshark for protocol analysis
- [ ] Access to network packet capture systems
- [ ] Industrial protocol parsers (pymodbus, dnp3-python, opcua-python)

### Access Permissions
- [ ] Read access to OT network monitoring systems
- [ ] Read access to ICS asset inventory
- [ ] Read access to threat intelligence platforms
- [ ] Write access to Neo4j graph database

---

## 3. DATA SOURCES

### 3.1 Industrial Protocol Traffic

**Primary Sources:**
1. **Network Packet Captures** → Protocol-level behavioral analysis
2. **OT Network Monitoring** (Nozomi, Claroty, Dragos) → Industrial traffic baselines
3. **ICS Logs** (PLC, HMI, SCADA) → Control system activity

**Extraction Targets:**
- Protocol command sequences
- Anomalous protocol behavior (function code abuse, timing anomalies)
- Unauthorized protocol connections
- Protocol-specific attack indicators

### 3.2 OT/ICS Asset Context

**Primary Sources:**
1. **Asset Inventory** → Protocol support by device
2. **Vendor Equipment Database** (PROC-142) → Equipment-protocol mappings
3. **Network Topology** → Protocol communication paths

**Extraction Targets:**
- Asset-protocol relationships
- Protocol version vulnerabilities
- Inter-protocol dependencies

### 3.3 Threat Intelligence

**Primary Sources:**
1. **MITRE ATT&CK for ICS** → OT-specific TTPs
2. **ICS-CERT Advisories** → Industrial vulnerabilities
3. **Dragos Worldviews** → Threat actor industrial targeting
4. **Vendor Security Bulletins** → Protocol-specific CVEs

**Extraction Targets:**
- Known protocol exploits
- Threat actor protocol preferences
- Industrial campaign indicators

---

## 4. TRANSFORMATION LOGIC

### 4.1 Protocol Behavioral Analysis

```python
def analyze_protocol_behavior(packet_captures, baseline_patterns, protocol_type):
    """Detect anomalous industrial protocol behavior."""

    anomalies = []

    for capture in packet_captures:
        # Parse protocol-specific commands
        if protocol_type == 'modbus':
            commands = parse_modbus_commands(capture)
            baseline = baseline_patterns['modbus']

            for cmd in commands:
                # Modbus function code abuse detection
                if cmd['function_code'] in [0x06, 0x10]:  # Write coil/register
                    if cmd['source_ip'] not in baseline['authorized_writers']:
                        anomalies.append({
                            "type": "unauthorized_write",
                            "protocol": "modbus",
                            "function_code": cmd['function_code'],
                            "source_ip": cmd['source_ip'],
                            "target_device": cmd['destination_ip'],
                            "severity": "Critical",
                            "ttp": "T0836 - Modify Parameter"  # MITRE ICS
                        })

                # Rapid scanning detection
                if cmd['timing_delta'] < 0.1:  # <100ms between commands
                    anomalies.append({
                        "type": "rapid_scanning",
                        "protocol": "modbus",
                        "scan_rate": 1 / cmd['timing_delta'],
                        "source_ip": cmd['source_ip'],
                        "severity": "High",
                        "ttp": "T0840 - Network Connection Enumeration"
                    })

        elif protocol_type == 'dnp3':
            commands = parse_dnp3_commands(capture)
            baseline = baseline_patterns['dnp3']

            for cmd in commands:
                # DNP3 control relay output block abuse
                if cmd['function'] == 'CROB':
                    if not validate_crob_sequence(cmd, baseline):
                        anomalies.append({
                            "type": "crob_abuse",
                            "protocol": "dnp3",
                            "control_code": cmd['control_code'],
                            "target_point": cmd['point_index'],
                            "severity": "Critical",
                            "ttp": "T0800 - Modify Control Logic"
                        })

        elif protocol_type == 'opcua':
            commands = parse_opcua_commands(capture)

            for cmd in commands:
                # OPC-UA method invocation anomalies
                if cmd['service'] == 'Call':
                    if cmd['method_id'] not in baseline_patterns['opcua']['allowed_methods']:
                        anomalies.append({
                            "type": "unauthorized_method_call",
                            "protocol": "opcua",
                            "method_id": cmd['method_id'],
                            "object_id": cmd['object_id'],
                            "severity": "High",
                            "ttp": "T0871 - Execution through API"
                        })

    return {
        "protocol_anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "severity_distribution": categorize_by_severity(anomalies),
        "ttp_distribution": categorize_by_ttp(anomalies)
    }
```

### 4.2 Threat Actor Protocol Profiling

```python
def profile_threat_actor_protocols(threat_intel, observed_anomalies):
    """Link protocol anomalies to known threat actor behaviors."""

    actor_indicators = []

    # Known threat actor protocol preferences
    actor_signatures = {
        "XENOTIME": {
            "protocols": ["Modbus", "OPC-UA"],
            "ttps": ["T0836", "T0871"],
            "function_codes": [0x06, 0x10],  # Modbus write operations
            "timing_patterns": "slow_and_deliberate"
        },
        "TRITON": {
            "protocols": ["TriStation"],
            "ttps": ["T0800", "T0873"],
            "targeting": "safety_systems",
            "timing_patterns": "reconnaissance_heavy"
        },
        "PIPEDREAM": {
            "protocols": ["Modbus", "OPC-UA", "CoDeSys"],
            "ttps": ["T0836", "T0871", "T0874"],
            "function_codes": [0x06, 0x10, 0x17],
            "timing_patterns": "automated_tooling"
        }
    }

    for anomaly in observed_anomalies:
        for actor, signature in actor_signatures.items():
            match_score = 0

            # Protocol match
            if anomaly['protocol'].lower() in [p.lower() for p in signature['protocols']]:
                match_score += 0.3

            # TTP match
            if anomaly.get('ttp') and anomaly['ttp'].split(' - ')[0] in signature['ttps']:
                match_score += 0.4

            # Function code match (Modbus-specific)
            if anomaly['protocol'] == 'modbus' and anomaly.get('function_code') in signature.get('function_codes', []):
                match_score += 0.2

            # Timing pattern match
            timing_pattern = classify_timing_pattern(anomaly)
            if timing_pattern == signature.get('timing_patterns'):
                match_score += 0.1

            if match_score > 0.5:  # Threshold for actor attribution
                actor_indicators.append({
                    "threat_actor": actor,
                    "confidence": match_score,
                    "anomaly_id": anomaly.get('id'),
                    "matching_indicators": identify_matching_indicators(anomaly, signature)
                })

    return {
        "threat_actor_attributions": actor_indicators,
        "high_confidence_matches": [a for a in actor_indicators if a['confidence'] > 0.7],
        "attribution_summary": summarize_attributions(actor_indicators)
    }
```

### 4.3 Protocol Vulnerability Assessment

```python
def assess_protocol_vulnerabilities(asset_inventory, protocol_versions, cve_database):
    """Map protocol versions to known vulnerabilities."""

    vulnerabilities = []

    for asset in asset_inventory:
        for protocol in asset['supported_protocols']:
            protocol_name = protocol['name']
            protocol_version = protocol['version']

            # Check CVE database for protocol vulnerabilities
            relevant_cves = query_cves(protocol_name, protocol_version, cve_database)

            for cve in relevant_cves:
                vulnerabilities.append({
                    "asset_id": asset['id'],
                    "protocol": protocol_name,
                    "version": protocol_version,
                    "cve_id": cve['id'],
                    "cvss_score": cve['cvss_score'],
                    "exploitability": cve['exploitability'],
                    "description": cve['description'],
                    "vendor_patch_available": check_patch_availability(cve, asset['vendor']),
                    "severity": categorize_cvss(cve['cvss_score'])
                })

    return {
        "total_vulnerabilities": len(vulnerabilities),
        "critical_count": len([v for v in vulnerabilities if v['severity'] == 'Critical']),
        "high_count": len([v for v in vulnerabilities if v['severity'] == 'High']),
        "vulnerabilities_by_protocol": group_by_protocol(vulnerabilities),
        "unpatched_criticals": [v for v in vulnerabilities if v['severity'] == 'Critical' and not v['vendor_patch_available']]
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**IndustrialProtocol**
```cypher
CREATE (ip:IndustrialProtocol {
  id: STRING,  // "Modbus_TCP"
  protocol_name: STRING,  // "Modbus"
  protocol_type: STRING,  // "TCP", "RTU", "ASCII"
  port: INT,  // 502
  osi_layer: INT,  // 7 (Application)
  encryption_supported: BOOLEAN,
  authentication_supported: BOOLEAN,
  common_uses: LIST<STRING>,  // ["PLC communication", "SCADA"]
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**ProtocolAnomaly**
```cypher
CREATE (pa:ProtocolAnomaly {
  id: STRING,
  type: STRING,  // "unauthorized_write", "rapid_scanning", "crob_abuse"
  protocol: STRING,  // "modbus", "dnp3", "opcua"
  source_ip: STRING,
  target_device: STRING,
  severity: STRING,  // "Critical", "High", "Medium"
  ttp: STRING,  // "T0836 - Modify Parameter"
  timestamp: DATETIME,
  function_code: INT,  // Protocol-specific
  description: STRING,
  created_at: DATETIME
})
```

**ProtocolVulnerability**
```cypher
CREATE (pv:ProtocolVulnerability {
  id: STRING,
  cve_id: STRING,  // "CVE-2021-12345"
  protocol: STRING,
  affected_versions: LIST<STRING>,
  cvss_score: FLOAT,
  exploitability: STRING,  // "High", "Medium", "Low"
  description: STRING,
  vendor_patch_available: BOOLEAN,
  patch_version: STRING,
  published_date: DATE,
  created_at: DATETIME
})
```

**OTThreatActor**
```cypher
CREATE (ta:OTThreatActor {
  id: STRING,  // "XENOTIME"
  name: STRING,
  aliases: LIST<STRING>,
  target_sectors: LIST<STRING>,  // ["Oil_Gas", "Electric_Power"]
  preferred_protocols: LIST<STRING>,  // ["Modbus", "OPC-UA"]
  sophistication: STRING,  // "Advanced", "Moderate"
  motivation: STRING,  // "Sabotage", "Espionage"
  known_campaigns: LIST<STRING>,
  first_observed: DATE,
  last_observed: DATE,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

### Relationships

**USES_PROTOCOL**
```cypher
CREATE (device:EquipmentModel)-[up:USES_PROTOCOL {
  implementation_version: STRING,
  required_for_operation: BOOLEAN,
  security_hardening_applied: BOOLEAN,
  created_at: DATETIME
}]->(protocol:IndustrialProtocol)
```

**HAS_VULNERABILITY**
```cypher
CREATE (protocol:IndustrialProtocol)-[hv:HAS_VULNERABILITY {
  affects_version: STRING,
  exploited_in_wild: BOOLEAN,
  mitre_ics_technique: STRING,
  created_at: DATETIME
}]->(vuln:ProtocolVulnerability)
```

**DETECTED_IN**
```cypher
CREATE (anomaly:ProtocolAnomaly)-[di:DETECTED_IN {
  detection_timestamp: DATETIME,
  confidence: FLOAT,
  false_positive_likelihood: FLOAT,
  created_at: DATETIME
}]->(protocol:IndustrialProtocol)
```

**ATTRIBUTED_TO**
```cypher
CREATE (anomaly:ProtocolAnomaly)-[at:ATTRIBUTED_TO {
  attribution_confidence: FLOAT,  // 0-1
  matching_indicators: LIST<STRING>,
  attribution_method: STRING,  // "TTP_match", "timing_pattern", "function_code"
  created_at: DATETIME
}]->(actor:OTThreatActor)
```

**TARGETS_PROTOCOL**
```cypher
CREATE (actor:OTThreatActor)-[tp:TARGETS_PROTOCOL {
  campaign_count: INT,
  preference_score: FLOAT,  // How often actor targets this protocol
  known_exploits: LIST<STRING>,
  created_at: DATETIME
}]->(protocol:IndustrialProtocol)
```

---

## 6. EXECUTION STEPS

### Step 1: Capture and Parse Protocol Traffic
```bash
python /scripts/capture_industrial_protocols.py \
  --interface eth1 \
  --protocols modbus,dnp3,opcua,profinet \
  --duration 3600 \
  --output /data/staging/protocol_captures.pcap
```

### Step 2: Analyze Protocol Behavior
```bash
python /scripts/analyze_protocol_behavior.py \
  --captures /data/staging/protocol_captures.pcap \
  --baseline /data/baselines/protocol_baselines.json \
  --output /data/staging/protocol_anomalies.json
```

### Step 3: Profile Threat Actors
```bash
python /scripts/profile_ot_threat_actors.py \
  --anomalies /data/staging/protocol_anomalies.json \
  --threat_intel /data/threat_intel/ot_actors.json \
  --output /data/staging/actor_attributions.json
```

### Step 4: Assess Protocol Vulnerabilities
```bash
python /scripts/assess_protocol_vulnerabilities.py \
  --asset_inventory /data/ot_asset_inventory.json \
  --cve_database /data/cve_feeds/industrial_cves.json \
  --output /data/staging/protocol_vulnerabilities.json
```

### Step 5: Correlate with Vendor Equipment
```bash
python /scripts/correlate_protocol_equipment.py \
  --equipment_db /data/vendor_equipment_db.json \
  --protocol_data /data/staging/protocol_anomalies.json \
  --output /data/staging/protocol_equipment_correlation.json
```

### Step 6: Load to Neo4j
```bash
python /scripts/load_protocol_analysis_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

---

## 7. CYPHER QUERIES

### 7.1 Identify Critical Protocol Anomalies
```cypher
MATCH (pa:ProtocolAnomaly)-[di:DETECTED_IN]->(protocol:IndustrialProtocol)
WHERE pa.severity = 'Critical'
RETURN pa.type AS anomaly_type,
       protocol.protocol_name AS protocol,
       pa.source_ip AS attacker_ip,
       pa.target_device AS target,
       pa.ttp AS mitre_technique,
       pa.timestamp AS when_detected
ORDER BY pa.timestamp DESC
LIMIT 10
```

### 7.2 Attribute Anomalies to Threat Actors
```cypher
MATCH (pa:ProtocolAnomaly)-[at:ATTRIBUTED_TO]->(actor:OTThreatActor)
WHERE at.attribution_confidence > 0.7
RETURN actor.name AS threat_actor,
       actor.sophistication AS actor_sophistication,
       count(pa) AS anomaly_count,
       collect(pa.protocol)[0..5] AS targeted_protocols,
       avg(at.attribution_confidence) AS avg_confidence
ORDER BY anomaly_count DESC
```

### 7.3 Find Vulnerable Protocols in Use
```cypher
MATCH (device:EquipmentModel)-[up:USES_PROTOCOL]->(protocol:IndustrialProtocol)-[hv:HAS_VULNERABILITY]->(vuln:ProtocolVulnerability)
WHERE vuln.cvss_score >= 7.0 AND vuln.vendor_patch_available = false
RETURN device.manufacturer AS vendor,
       device.model AS equipment_model,
       protocol.protocol_name AS vulnerable_protocol,
       vuln.cve_id AS cve,
       vuln.cvss_score AS severity,
       vuln.description AS vulnerability_description
ORDER BY vuln.cvss_score DESC
LIMIT 15
```

### 7.4 Map Threat Actor Protocol Preferences
```cypher
MATCH (actor:OTThreatActor)-[tp:TARGETS_PROTOCOL]->(protocol:IndustrialProtocol)
RETURN actor.name AS threat_actor,
       collect(protocol.protocol_name) AS preferred_protocols,
       actor.target_sectors AS targeted_industries,
       actor.sophistication AS capability_level
ORDER BY actor.sophistication DESC
```

### 7.5 Detect Rapid Protocol Scanning
```cypher
MATCH (pa:ProtocolAnomaly)
WHERE pa.type = 'rapid_scanning'
  AND pa.timestamp > datetime() - duration('PT24H')
RETURN pa.source_ip AS scanner_ip,
       pa.protocol AS scanned_protocol,
       count(*) AS scan_events,
       collect(pa.target_device)[0..10] AS scanned_devices,
       min(pa.timestamp) AS scan_start,
       max(pa.timestamp) AS scan_end
ORDER BY count(*) DESC
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Protocol Anomaly Completeness
```cypher
MATCH (pa:ProtocolAnomaly)
WHERE pa.protocol IS NOT NULL
  AND pa.severity IN ['Critical', 'High', 'Medium', 'Low']
  AND pa.ttp IS NOT NULL
RETURN count(pa) AS valid_anomalies
```

### 8.2 Check Attribution Confidence Ranges
```cypher
MATCH ()-[at:ATTRIBUTED_TO]->()
WHERE at.attribution_confidence < 0 OR at.attribution_confidence > 1
RETURN count(at) AS invalid_confidences
// Expected: 0
```

### 8.3 Count Data Loads
```cypher
MATCH (pa:ProtocolAnomaly)-[di:DETECTED_IN]->(protocol:IndustrialProtocol)
OPTIONAL MATCH (pa)-[at:ATTRIBUTED_TO]->(actor:OTThreatActor)
OPTIONAL MATCH (protocol)-[hv:HAS_VULNERABILITY]->(vuln:ProtocolVulnerability)
RETURN protocol.protocol_name AS protocol,
       count(DISTINCT pa) AS anomaly_count,
       count(DISTINCT actor) AS attributed_actors,
       count(DISTINCT vuln) AS vulnerability_count
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
MATCH (pa:ProtocolAnomaly)
WHERE pa.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (pa)-[r]-()
DELETE r, pa

UNION

MATCH (pv:ProtocolVulnerability)
WHERE pv.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (pv)-[r]-()
DELETE r, pv
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 40-55 minutes for 1 hour of protocol traffic
- **Data Volume**: ~10,000 protocol packets analyzed
- **Graph Nodes Created**: 50-100 per analysis (anomalies, vulnerabilities)
- **Quality Score**: >0.87

**Success Criteria:**
- All protocol anomalies have severity classification
- Attribution confidence scores within [0, 1]
- All CVEs mapped to affected protocols
- At least 3 threat actor attributions with >0.5 confidence

---

## 11. TROUBLESHOOTING

**Issue**: High false positive rate in anomaly detection
- **Cause**: Baseline patterns incomplete or outdated
- **Fix**: Update baselines with recent normal traffic, tune detection thresholds

**Issue**: Low threat actor attribution confidence
- **Cause**: Insufficient threat intelligence or novel actor TTPs
- **Fix**: Enrich threat intel sources, use behavioral clustering

**Issue**: Missing protocol vulnerabilities
- **Cause**: CVE database outdated or incomplete
- **Fix**: Update CVE feeds, cross-reference with vendor advisories

---

## 12. RELATED PROCEDURES
- **PROC-142**: Vendor Equipment Mapping (equipment-protocol relationships)
- **PROC-141**: Lacanian RSI Foundations (threat actor psychological profiling)
- **PROC-151**: Lacanian Dyad Analysis (attacker-defender protocol dynamics)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
