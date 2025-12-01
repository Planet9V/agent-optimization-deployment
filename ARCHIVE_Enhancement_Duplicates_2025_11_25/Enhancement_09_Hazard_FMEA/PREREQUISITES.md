# PREREQUISITES: Enhancement 9 - Hazard Analysis & FMEA

**File:** PREREQUISITES.md
**Created:** 2025-11-25
**Version:** v1.0.0
**Purpose:** Define required data files, dependencies, and preparation steps for FMEA integration
**Status:** ACTIVE

---

## Executive Summary

Enhancement 9 requires 10 FMEA (Failure Mode and Effects Analysis) data files containing equipment failure modes, severity/occurrence/detection ratings, and RPN calculations. Additionally, integration with Enhancements 1-8 requires existing knowledge graph nodes (CVE, Vulnerability, Equipment, Asset) to be present for cyber-physical linkage.

**Critical Dependencies:**
- 10 FMEA data files (CSV or Excel format)
- Enhancement 1 (Threat Intelligence) - CVE nodes
- Enhancement 2 (Vulnerability Management) - Vulnerability nodes
- Enhancement 7 (Asset Relationships) - Equipment and Asset nodes
- Neo4j database with write access
- Python 3.8+ with pandas, neo4j-driver libraries

---

## Required FMEA Data Files (10 Files)

### File 1: PLC_Failure_Modes.csv
**Description:** Failure modes for Programmable Logic Controllers (PLCs) used in critical process control.

**Required Columns:**
- `equipment_type` (string): "Programmable_Logic_Controller"
- `equipment_model` (string): Vendor and model (e.g., "Rockwell ControlLogix 5580")
- `failure_mode` (string): Name of failure mode (e.g., "CPU_Crash", "Memory_Corruption")
- `failure_description` (text): Detailed description of how failure manifests
- `severity` (integer 1-10): Severity rating per FMEA scale
- `severity_rationale` (text): Justification for severity rating
- `occurrence` (integer 1-10): Occurrence rating (base, before cyber adjustment)
- `occurrence_rationale` (text): Historical data or engineering judgment
- `detection` (integer 1-10): Detection rating
- `detection_rationale` (text): Current detection capabilities
- `rpn` (integer): Risk Priority Number (S × O × D)
- `safety_effect` (text): Impact on personnel safety
- `operational_effect` (text): Impact on production/operations
- `financial_effect` (integer): Estimated financial loss per occurrence ($)
- `environmental_effect` (text): Environmental consequences
- `cyber_induced` (boolean): True if cyber attack can cause this failure

**Expected Record Count:** 20-30 failure modes

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced
Programmable_Logic_Controller,Rockwell ControlLogix 5580,CPU_Crash,Complete loss of PLC processing capability,8,Loss of critical process control with potential runaway reaction,6,CVE-2022-1234 exploitable with public exploit available,7,Watchdog timer detects failure but not cyber cause,336,Potential loss of interlocks leading to overpressure,Immediate process shutdown requiring 4-8 hour recovery,500000,Potential venting if pressure relief activates,true
```

---

### File 2: SIS_Failure_Modes.csv
**Description:** Failure modes for Safety Instrumented Systems (SIS) including logic solvers and final elements.

**Required Columns:** Same as File 1, plus:
- `safety_integrity_level` (string): "SIL1", "SIL2", "SIL3", or "SIL4"
- `fail_safe_mode` (boolean): True if failure causes safe state
- `spurious_trip` (boolean): True if failure causes unnecessary shutdown

**Expected Record Count:** 15-25 failure modes

**Critical Failure Modes to Include:**
- Spurious trip (unnecessary shutdown)
- Failure to activate on demand (dangerous failure)
- Sensor drift or calibration error
- Logic solver CPU failure
- Final element (valve) stuck or slow response

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,safety_integrity_level,fail_safe_mode,spurious_trip
Safety_Instrumented_System,Triconex TMR,Failure_To_Activate_On_Demand,SIS logic solver fails to trigger shutdown when high pressure detected,9,Potential equipment rupture and personnel injury without shutdown,4,Hardware failure rate from FMEDA report,6,Proof testing every 12 months may not detect latent failure,216,Critical injury or fatality from overpressure event,Potential catastrophic equipment damage,2000000,Major chemical release exceeding permit limits,false,SIL3,false,false
```

---

### File 3: HMI_Failure_Modes.csv
**Description:** Failure modes for Human-Machine Interfaces (HMI) and operator workstations.

**Required Columns:** Same as File 1, plus:
- `affects_operator_response` (boolean): True if failure impairs operator action
- `false_indication` (boolean): True if failure shows incorrect data

**Expected Record Count:** 15-20 failure modes

**Critical Failure Modes:**
- Display freeze or crash
- Incorrect data display (false indication)
- Input unresponsive (cannot control process)
- Communication loss to SCADA/DCS
- Unauthorized access or privilege escalation

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,affects_operator_response,false_indication
Human_Machine_Interface,Rockwell FactoryTalk View,False_Data_Display,HMI shows incorrect sensor values due to Modbus/TCP manipulation,6,Operator makes incorrect decisions based on false data,7,Modbus/TCP unencrypted and vulnerable to MITM attacks,8,Manual cross-check against field readings not routine,336,Incorrect operator response may delay emergency action,Poor decisions lead to quality issues or minor incidents,150000,Unlikely without compounding failures,true,true,true
```

---

### File 4: DCS_Failure_Modes.csv
**Description:** Failure modes for Distributed Control Systems (DCS) including controllers, I/O, and communication.

**Required Columns:** Same as File 1, plus:
- `affects_regulatory_control` (boolean): True if continuous control lost
- `cascade_potential` (boolean): True if failure can cascade to other systems

**Expected Record Count:** 20-30 failure modes

**Critical Failure Modes:**
- Controller module failure
- I/O card failure
- Network communication loss
- Engineering workstation compromise
- Configuration database corruption

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,affects_regulatory_control,cascade_potential
Distributed_Control_System,Emerson DeltaV,Network_Communication_Loss,Controller network disrupted preventing coordination between units,7,Loss of coordinated control may cause quality issues or minor upset,5,Network equipment aging and vulnerability to cyber attacks,4,Network monitoring alerts on communication loss within 1 minute,140,Minor risk if control loops operate autonomously,Production quality degradation or unit shutdown,300000,Unlikely unless prolonged,true,true,true
```

---

### File 5: Network_Equipment_Failures.csv
**Description:** Failure modes for network infrastructure (switches, routers, firewalls) supporting OT networks.

**Required Columns:** Same as File 1, plus:
- `network_segment` (string): "OT", "DMZ", "IT", "Safety"
- `affects_multiple_systems` (boolean): True if failure impacts multiple control systems

**Expected Record Count:** 15-20 failure modes

**Critical Failure Modes:**
- Switch or router failure (complete loss)
- Port exhaustion or bandwidth saturation
- Firewall rule misconfiguration
- Spanning tree loop
- DDoS attack on network infrastructure

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,network_segment,affects_multiple_systems
Network_Switch,Cisco IE-4000,Switch_Failure_Complete_Loss,Core OT network switch fails causing loss of communication to all connected PLCs,8,Loss of control and monitoring for entire production unit,3,Redundant switches in place but single points of failure remain,5,Network monitoring detects loss but recovery time 30+ minutes,120,Loss of interlocks if PLCs cannot communicate,Complete unit shutdown requiring manual restart,800000,Potential if shutdown not orderly,false,OT,true
```

---

### File 6: Sensor_Actuator_Failures.csv
**Description:** Failure modes for field devices including sensors (pressure, temperature, flow) and actuators (valves, motors).

**Required Columns:** Same as File 1, plus:
- `device_type` (string): "Sensor" or "Actuator"
- `safety_critical` (boolean): True if used in safety system
- `fail_position` (string): "Open", "Closed", "Last Position", "N/A"

**Expected Record Count:** 25-35 failure modes

**Critical Failure Modes:**
- Sensor drift or calibration error
- Sensor complete failure (stuck reading)
- Valve stuck open or closed
- Valve slow response or partial stroke
- Transmitter communication loss

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,device_type,safety_critical,fail_position
Pressure_Transmitter,Rosemount 3051,Sensor_Drift_Calibration_Error,Pressure transmitter reads 10% high causing controller to underpressure process,5,Underpressure leads to quality issues but safety systems prevent danger,6,Calibration every 12 months but drift occurs gradually,6,Process quality monitoring may detect deviation but not attribute to sensor,180,Low risk as safety systems independent,Production quality failures requiring rework,120000,Unlikely,false,Sensor,false,N/A
```

---

### File 7: SCADA_Server_Failures.csv
**Description:** Failure modes for SCADA servers, historians, and application servers.

**Required Columns:** Same as File 1, plus:
- `data_loss_potential` (boolean): True if failure causes historical data loss
- `affects_remote_operations` (boolean): True if remote monitoring/control impacted

**Expected Record Count:** 15-20 failure modes

**Critical Failure Modes:**
- Server OS crash or freeze
- Database corruption
- Historian data loss
- SCADA application compromise
- Ransomware encryption

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,data_loss_potential,affects_remote_operations
SCADA_Historian,OSIsoft PI Server,Historian_Data_Loss,Historical process data lost due to database corruption or deletion,4,No immediate safety impact but trend analysis and optimization impaired,5,Database vulnerabilities and backup failures,6,Data integrity checks infrequent,120,None direct but impairs long-term safety analysis,Loss of optimization data and regulatory compliance records,80000,None direct,true,true,false
```

---

### File 8: Power_System_Failures.csv
**Description:** Failure modes for power systems including UPS, generators, and power distribution.

**Required Columns:** Same as File 1, plus:
- `backup_available` (boolean): True if backup power available
- `graceful_shutdown_time` (integer): Minutes of UPS runtime for orderly shutdown

**Expected Record Count:** 15-20 failure modes

**Critical Failure Modes:**
- Utility power loss
- UPS failure or battery depletion
- Generator failure to start
- Power distribution failure (breaker trip)
- Voltage sag or surge

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,backup_available,graceful_shutdown_time
Uninterruptible_Power_Supply,APC Symmetra,UPS_Battery_Depletion_Failure,UPS batteries depleted due to extended outage or maintenance failure,7,Loss of power to control systems causing uncontrolled shutdown,4,Utility reliability and battery maintenance program,3,Battery monitoring and low battery alarms provide advance warning,84,Uncontrolled shutdown may bypass safety procedures,Uncontrolled shutdown causing equipment damage and extended recovery,600000,Potential if process not secured properly,false,true,15
```

---

### File 9: Safety_System_Failures.csv
**Description:** Failure modes for safety systems including emergency shutdown (ESD), fire suppression, and gas detection.

**Required Columns:** Same as File 1, plus:
- `safety_function` (string): "Emergency Shutdown", "Fire Suppression", "Gas Detection", "Pressure Relief"
- `proof_test_interval` (integer): Months between functional tests
- `dangerous_failure` (boolean): True if failure prevents safety function

**Expected Record Count:** 15-25 failure modes

**Critical Failure Modes:**
- ESD system failure to activate
- Fire suppression spurious activation
- Gas detector sensor failure
- Emergency isolation valve stuck
- Pressure relief valve failure to open

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,safety_function,proof_test_interval,dangerous_failure
Emergency_Shutdown_System,Emerson SIS,ESD_Failure_To_Activate,ESD logic solver compromised via cyber attack preventing emergency shutdown initiation,9,Failure to shutdown during emergency could result in fatality or major equipment damage,3,Requires sophisticated cyber attack on SIS network,5,Proof testing detects latent failures but not active cyber compromise,135,Critical injury or fatality risk without emergency shutdown,Catastrophic equipment damage from uncontrolled upset,3000000,Major environmental release without containment,true,Emergency Shutdown,12,true
```

---

### File 10: Cascade_Failure_Scenarios.csv
**Description:** Multi-system cascade failure scenarios where initial failure triggers secondary and tertiary failures.

**Required Columns:** Same as File 1, plus:
- `initiating_failure` (string): Name of initial failure mode
- `secondary_failure` (string): Name of next failure in cascade
- `tertiary_failure` (string): Name of final failure (if applicable)
- `cascade_probability` (float 0-1): Likelihood of cascade progression
- `cascade_time` (string): Time from initial to final failure

**Expected Record Count:** 10-15 cascade scenarios

**Critical Cascade Scenarios:**
- Cooling system failure → server overheating → network infrastructure failure
- Power loss → control system failure → safety system failure
- Cyber attack → HMI compromise → operator error → physical damage
- Network attack → DCS failure → cascade to dependent processes

**Sample Row:**
```csv
equipment_type,equipment_model,failure_mode,failure_description,severity,severity_rationale,occurrence,occurrence_rationale,detection,detection_rationale,rpn,safety_effect,operational_effect,financial_effect,environmental_effect,cyber_induced,initiating_failure,secondary_failure,tertiary_failure,cascade_probability,cascade_time
Cascade_Scenario,Multi-System,Cooling_System_Cascade,Cyber attack disables HVAC → server room overheating → network equipment failure → loss of plant-wide monitoring,8,Loss of all monitoring creates blind spots for operators,4,Requires HVAC system cyber access and disabling temperature alarms,5,Server temperature alarms provide some warning but cyber cause obscured,160,Monitoring loss prevents early detection of developing hazards,Complete loss of remote monitoring and data collection,450000,Indirect if other failures occur undetected,true,HVAC_Cyber_Compromise,Server_Overheating_Thermal_Shutdown,Network_Infrastructure_Failure,0.8,30-60 minutes
```

---

## Knowledge Graph Prerequisites

### Enhancement 1: Threat Intelligence (CVE Nodes)
**Required for:** Cyber-physical failure linkage

**Validation Query:**
```cypher
MATCH (cve:CVE)
WHERE cve.cve_id STARTS WITH 'CVE-'
RETURN count(cve) AS cve_count
```

**Expected:** ≥ 50 CVE nodes related to industrial control systems

**Critical CVEs for FMEA:**
- Rockwell Automation PLC vulnerabilities
- Siemens SCADA vulnerabilities
- Schneider Electric SIS vulnerabilities
- Generic Modbus/TCP, DNP3 protocol vulnerabilities

**Fallback:** If CVE nodes missing, Agent 3 creates temporary CVE placeholder nodes from public NVD database.

---

### Enhancement 2: Vulnerability Management (Vulnerability Nodes)
**Required for:** Occurrence rating adjustments based on patch status

**Validation Query:**
```cypher
MATCH (v:Vulnerability)
WHERE v.cvss_base_score >= 7.0
RETURN count(v) AS high_severity_vulns, avg(v.cvss_base_score) AS avg_cvss
```

**Expected:** ≥ 30 Vulnerability nodes with CVSS scores

**Usage:** Unpatched vulnerabilities with CVSS ≥ 7.0 increase occurrence rating by +2.

---

### Enhancement 7: Asset Relationships (Equipment & Asset Nodes)
**Required for:** Equipment-to-failure-mode mapping, cascade failure analysis

**Validation Query:**
```cypher
MATCH (eq:Equipment)
RETURN count(eq) AS equipment_count,
       collect(DISTINCT eq.equipment_type)[0..10] AS sample_types
```

**Expected:** ≥ 100 Equipment nodes with types matching FMEA data files

**Critical Equipment Types:**
- Programmable_Logic_Controller
- Safety_Instrumented_System
- Human_Machine_Interface
- Distributed_Control_System
- Network_Switch
- Pressure_Transmitter
- Emergency_Shutdown_System

**Fallback:** If Equipment nodes missing, create from FMEA data files (equipment_model column).

---

### Enhancement 5: Critical Infrastructure Dependencies
**Required for:** Cascade failure modeling

**Validation Query:**
```cypher
MATCH (asset1:Asset)-[:DEPENDS_ON]->(asset2:Asset)
RETURN count(*) AS dependency_count
```

**Expected:** ≥ 20 dependency relationships

**Usage:** Dependency relationships inform CASCADE_TO relationships between failure modes.

---

## Software and Environment Prerequisites

### Neo4j Database
**Version:** Neo4j 4.4+ or Neo4j AuraDB
**Configuration:**
- Write access enabled
- APOC procedures installed (for batch operations)
- Minimum 4GB heap memory allocated
- Graph Data Science (GDS) library optional but recommended

**Validation:**
```cypher
CALL dbms.components() YIELD name, versions, edition
RETURN name, versions[0] AS version, edition
```

---

### Python Environment
**Version:** Python 3.8 or higher

**Required Libraries:**
```bash
pip install pandas>=1.3.0
pip install neo4j>=4.4.0
pip install openpyxl>=3.0.0  # For Excel file parsing
pip install numpy>=1.21.0
```

**Validation:**
```python
import pandas as pd
import neo4j
print(f"pandas: {pd.__version__}")
print(f"neo4j: {neo4j.__version__}")
```

---

### Environment Variables
**Required:**
```bash
export NEO4J_URI="bolt://localhost:7687"  # or neo4j+s://xxxxx.databases.neo4j.io
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
export FMEA_DATA_PATH="/path/to/fmea/data/files"
```

**Validation:**
```bash
echo $NEO4J_URI
echo $FMEA_DATA_PATH
```

---

## Data Quality Requirements

### Mandatory Field Completeness
**All FMEA files must have:**
- ≥ 95% completeness for: equipment_type, failure_mode, severity, occurrence, detection, rpn
- ≥ 80% completeness for: severity_rationale, occurrence_rationale, detection_rationale
- ≥ 70% completeness for: safety_effect, operational_effect, financial_effect

**Validation Script:**
```python
import pandas as pd

df = pd.read_csv('PLC_Failure_Modes.csv')

mandatory_fields = ['equipment_type', 'failure_mode', 'severity', 'occurrence', 'detection', 'rpn']
completeness = {}

for field in mandatory_fields:
    completeness[field] = (df[field].notna().sum() / len(df)) * 100

print("Field Completeness:")
for field, pct in completeness.items():
    status = "✅ PASS" if pct >= 95 else "❌ FAIL"
    print(f"{field}: {pct:.1f}% {status}")
```

---

### RPN Calculation Consistency
**All records must satisfy:** `rpn = severity × occurrence × detection`

**Validation Query (post-import):**
```cypher
MATCH (fm:FailureMode)
WHERE fm.rpn <> (fm.severity * fm.occurrence * fm.detection)
RETURN fm.name, fm.rpn AS recorded, (fm.severity * fm.occurrence * fm.detection) AS calculated
```

**Tolerance:** 0 mismatches allowed (must be exact).

---

### Severity Justification for High-Risk Failures
**All records with severity ≥ 8 must have:**
- Non-empty `safety_effect` field
- Non-empty `severity_rationale` field

**Validation:**
```python
high_severity = df[df['severity'] >= 8]
missing_justification = high_severity[
    (high_severity['safety_effect'].isna()) |
    (high_severity['severity_rationale'].isna())
]

if len(missing_justification) > 0:
    print(f"❌ FAIL: {len(missing_justification)} high-severity failures missing justification")
else:
    print("✅ PASS: All high-severity failures documented")
```

---

## Data Location

### Expected Directory Structure
```
/path/to/fmea/data/files/
├── PLC_Failure_Modes.csv
├── SIS_Failure_Modes.csv
├── HMI_Failure_Modes.csv
├── DCS_Failure_Modes.csv
├── Network_Equipment_Failures.csv
├── Sensor_Actuator_Failures.csv
├── SCADA_Server_Failures.csv
├── Power_System_Failures.csv
├── Safety_System_Failures.csv
└── Cascade_Failure_Scenarios.csv
```

### Alternative Locations (Agent 2 will search in order)
1. `$FMEA_DATA_PATH` environment variable
2. `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/FMEA_Data/`
3. `/home/jim/2_OXOT_Projects_Dev/Enhancement_09_Hazard_FMEA/data/`
4. Project root `/data/fmea/`

---

## Preparation Checklist

### Pre-Execution Checklist (Agent 0 validates)
- [ ] Neo4j database accessible and write-enabled
- [ ] Python 3.8+ installed with required libraries
- [ ] Environment variables set (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, FMEA_DATA_PATH)
- [ ] 10 FMEA data files present at expected location
- [ ] FMEA files pass data quality validation (≥95% mandatory field completeness)
- [ ] RPN calculations consistent across all files
- [ ] Enhancement 1 (CVE nodes) available OR fallback plan accepted
- [ ] Enhancement 7 (Equipment nodes) available OR fallback plan accepted
- [ ] Disk space sufficient (≥ 500MB for Neo4j data growth)
- [ ] Network connectivity to Neo4j stable

### Validation Execution
**Agent 0 runs this before starting Phase 2:**
```bash
# Test Neo4j connectivity
python3 -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('$NEO4J_URI', auth=('$NEO4J_USER', '$NEO4J_PASSWORD')); driver.verify_connectivity(); print('✅ Neo4j connection successful')"

# Validate FMEA files present
ls -lh $FMEA_DATA_PATH/*.csv | wc -l  # Should be 10

# Check CVE nodes available
echo "MATCH (cve:CVE) RETURN count(cve)" | cypher-shell -u $NEO4J_USER -p $NEO4J_PASSWORD  # Should be ≥ 50
```

---

## Fallback Plans

### Fallback 1: FMEA Data Files Not Available
**Trigger:** Fewer than 10 files found at expected locations

**Action:** Agent 2 generates synthetic FMEA data from industry standards
**Standards Used:**
- IEC 61508 (Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems)
- ISA TR84.00.02 (Safety Instrumented Functions - Safety Integrity Level Evaluation Techniques)
- ISO 14224 (Petroleum and Natural Gas Industries - Collection and Exchange of Reliability and Maintenance Data)

**Synthetic Data Approach:**
1. Extract failure mode examples from standards
2. Apply typical severity/occurrence/detection ratings from published case studies
3. Generate 200+ synthetic failure modes covering all 10 equipment categories
4. Flag as synthetic data in metadata

**Validation:** Synthetic data still meets data quality requirements (RPN consistency, field completeness).

---

### Fallback 2: CVE Nodes Not Available
**Trigger:** Fewer than 20 CVE nodes in knowledge graph

**Action:** Agent 3 creates temporary CVE nodes from NVD database
**Data Source:** NIST National Vulnerability Database (NVD) API
**CVE Selection Criteria:**
- ICS-specific keywords (SCADA, PLC, HMI, DCS, industrial)
- CVSS Base Score ≥ 7.0
- Published in last 5 years

**Temporary Node Creation:**
```cypher
CREATE (cve:CVE {
  cve_id: 'CVE-2023-XXXXX',
  description: 'Temporary node from NVD',
  cvss_base_score: 8.5,
  exploited_in_wild: true,
  data_source: 'NVD_API',
  temporary: true
})
```

**Backfill Requirement:** Enhancement 1 must be completed to replace temporary nodes with full threat intelligence.

---

### Fallback 3: Equipment Nodes Not Available
**Trigger:** Fewer than 50 Equipment nodes in knowledge graph

**Action:** Agent 2 creates Equipment nodes from FMEA data files
**Data Source:** `equipment_model` column from FMEA files

**Equipment Node Creation:**
```cypher
CREATE (eq:Equipment {
  name: 'PLC_001',
  equipment_type: 'Programmable_Logic_Controller',
  manufacturer: 'Rockwell Automation',
  model: 'ControlLogix 5580',
  data_source: 'FMEA_Import',
  temporary: false
})
```

**Enrichment Requirement:** Enhancement 7 should enrich with location, criticality, dependencies.

---

## Post-Ingestion Validation

### Validation Query Suite (Agent 9 executes)

#### Query 1: Node Count Validation
```cypher
MATCH (fm:FailureMode) RETURN count(fm) AS failure_mode_count
UNION
MATCH (fc:FailureCause) RETURN count(fc) AS failure_cause_count
UNION
MATCH (fe:FailureEffect) RETURN count(fe) AS failure_effect_count
UNION
MATCH (dc:DetectionControl) RETURN count(dc) AS detection_control_count
UNION
MATCH (m:Mitigation) RETURN count(m) AS mitigation_count
```

**Expected:**
- FailureMode: ≥ 200
- FailureCause: ≥ 50
- FailureEffect: ≥ 100
- DetectionControl: ≥ 50
- Mitigation: ≥ 40

---

#### Query 2: RPN Distribution
```cypher
MATCH (fm:FailureMode)
WITH fm,
     CASE
       WHEN fm.rpn >= 500 THEN 'Critical/High'
       WHEN fm.rpn >= 200 THEN 'Medium'
       WHEN fm.rpn >= 100 THEN 'Low'
       ELSE 'Very Low'
     END AS risk_tier
RETURN risk_tier, count(fm) AS count
ORDER BY risk_tier
```

**Expected Distribution:**
- Critical/High (≥500): 10-20%
- Medium (200-499): 30-40%
- Low (100-199): 30-40%
- Very Low (<100): 10-20%

---

#### Query 3: Cyber-Physical Linkage Validation
```cypher
MATCH (cve:CVE)-[:EXPLOITS|ENABLES*1..2]->(fc:FailureCause)
      -[:CAUSES]->(fm:FailureMode)
RETURN count(DISTINCT cve) AS cves_linked,
       count(DISTINCT fc) AS failure_causes_linked,
       count(DISTINCT fm) AS failure_modes_linked
```

**Expected:**
- CVEs linked: ≥ 30
- FailureCauses linked: ≥ 50
- FailureModes linked: ≥ 80

---

#### Query 4: Data Completeness Validation
```cypher
MATCH (fm:FailureMode)
WHERE fm.severity >= 8
RETURN count(fm) AS high_severity_total,
       sum(CASE WHEN fm.safety_effect IS NOT NULL AND fm.safety_effect <> '' THEN 1 ELSE 0 END) AS with_safety_effect,
       (sum(CASE WHEN fm.safety_effect IS NOT NULL AND fm.safety_effect <> '' THEN 1 ELSE 0 END) * 100.0 / count(fm)) AS completeness_percent
```

**Expected:** completeness_percent = 100% (all high-severity failures documented)

---

## Summary

**Total Prerequisites:**
- 10 FMEA data files (200+ failure modes total)
- Enhancement 1 (CVE nodes) or fallback plan
- Enhancement 7 (Equipment nodes) or fallback plan
- Neo4j database with write access
- Python 3.8+ environment
- Environment variables configured

**Validation Gate:** Agent 0 validates all prerequisites before spawning Agent 2 (Data Ingestion).

**Fallback Strategy:** Synthetic data generation if files unavailable, temporary nodes if dependencies missing.

**Quality Assurance:** Agent 9 validates completeness, consistency, and integration after all agents complete.

---

**PREREQUISITES COMPLETE:** All requirements documented for Enhancement 9 execution.
