# Hazard Register: Critical Infrastructure Cybersecurity Threats

## Overview
A Hazard Register is a living document that systematically records all identified hazards, their assessment, controls, and status. This register compiles cybersecurity threats to critical infrastructure with safety implications.

## Register Structure
- **Hazard ID**: Unique identifier for tracking
- **Asset**: Affected system or equipment
- **Threat**: Cyber attack pattern
- **Vulnerability**: Exploitable weakness
- **Hazard**: Undesired safety consequence
- **Consequence**: Potential impact
- **Existing Controls**: Current protective measures
- **Risk Rating**: Initial risk assessment
- **Additional Controls**: Recommended improvements
- **Residual Risk**: Risk after treatment
- **Status**: Open, In Progress, Closed, Monitoring
- **Owner**: Responsible party
- **Review Date**: Next assessment date

---

## HAZARD-001: Nuclear Reactor Protection System Compromise

**Asset**: [[EQUIPMENT: Nuclear reactor protection system]]
**Threat**: [[ATTACK_PATTERN: Safety PLC firmware manipulation]]
**Vulnerability**: [[VULNERABILITY: Maintenance port network access]]
**Hazard**: [[HAZARD: Loss of reactor safety function]]

**Consequence**: Core damage, radiation release, public health emergency
**Consequence Severity**: Catastrophic

**Existing Controls**:
- [[MITIGATION: Physical access control to reactor building]]
- [[ARCHITECTURE: Safety system isolation from control network]]
- [[MITIGATION: Personnel background checks]]

**Initial Risk Rating**: 5 (Catastrophic) × 1 (Rare) = **5 (LOW)**

**Additional Controls Recommended**:
- [[MITIGATION: Complete air gap enforcement]]
- [[ARCHITECTURE: N-version programming]]
- [[MITIGATION: Formal verification of safety logic]]
- [[ARCHITECTURE: Diverse actuation systems]]

**Residual Risk**: 5 × 1 = **5 (LOW)** - Acceptable with monitoring

**Status**: **MONITORING** - Controls adequate, continuous oversight required
**Owner**: Nuclear Safety Engineering
**Review Date**: Quarterly
**Threat Actor**: [[THREAT_ACTOR: Nation-state nuclear saboteur]]

---

## HAZARD-002: Water Treatment Chemical Overdose

**Asset**: [[EQUIPMENT: Municipal water treatment chlorine dosing system]]
**Threat**: [[ATTACK_PATTERN: SCADA setpoint manipulation]]
**Vulnerability**: [[VULNERABILITY: Weak VPN authentication]]
**Hazard**: [[HAZARD: Excessive chlorine injection into public water supply]]

**Consequence**: Mass public health impact, potential fatalities, loss of public trust
**Consequence Severity**: Critical

**Existing Controls**:
- [[MITIGATION: VPN access requirement]]
- [[ARCHITECTURE: SCADA network segmentation]]
- [[MITIGATION: Water quality monitoring alarms]]

**Initial Risk Rating**: 4 (Critical) × 4 (Likely) = **16 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: Multi-factor authentication for VPN]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Chemical dosing rate limiting interlock]]
- [[MITIGATION: Real-time toxicity monitoring]]
- [[ARCHITECTURE: Independent water quality verification]]

**Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable after implementation

**Status**: **IN PROGRESS** - MFA deployment underway
**Owner**: Water Utility Cybersecurity Manager
**Review Date**: Monthly until closed
**Threat Actor**: [[THREAT_ACTOR: Water infrastructure terrorist]]

---

## HAZARD-003: Power Grid Cascading Failure

**Asset**: [[EQUIPMENT: Transmission system protection relays]]
**Threat**: [[ATTACK_PATTERN: IEC 61850 GOOSE message spoofing]]
**Vulnerability**: [[VULNERABILITY: Unauthenticated substation communications]]
**Hazard**: [[HAZARD: Coordinated false trip commands causing cascade]]

**Consequence**: Regional blackout, critical services loss, economic impact
**Consequence Severity**: Critical

**Existing Controls**:
- [[ARCHITECTURE: Protection relay VLAN isolation]]
- [[MITIGATION: Relay access control]]
- [[ARCHITECTURE: System integrity protection schemes]]

**Initial Risk Rating**: 4 (Critical) × 3 (Possible) = **12 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: IEC 62351 security implementation]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Substation network microsegmentation]]
- [[MITIGATION: GOOSE message monitoring and validation]]
- [[ARCHITECTURE: Wide-area monitoring system integration]]

**Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable after implementation

**Status**: **IN PROGRESS** - IEC 62351 pilot deployment
**Owner**: Grid Operations Cybersecurity
**Review Date**: Bi-monthly
**Threat Actor**: [[THREAT_ACTOR: Nation-state grid warfare actor]]

---

## HAZARD-004: Manufacturing Robot Worker Injury

**Asset**: [[EQUIPMENT: Industrial welding robot]]
**Threat**: [[ATTACK_PATTERN: Robot program injection]]
**Vulnerability**: [[VULNERABILITY: Unsecured robot controller network]]
**Hazard**: [[HAZARD: Robot collision with worker]]

**Consequence**: Worker fatality or serious injury
**Consequence Severity**: Critical

**Existing Controls**:
- [[ARCHITECTURE: Physical safety fencing]]
- [[MITIGATION: Safety light curtain system]]
- [[ARCHITECTURE: Emergency stop buttons]]

**Initial Risk Rating**: 4 (Critical) × 2 (Unlikely) = **8 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: Robot controller network authentication]]
- [[ARCHITECTURE: Program digital signature verification]]
- [[MITIGATION: Redundant safety position monitoring]]
- [[ARCHITECTURE: Safety PLC independent of robot controller]]

**Residual Risk**: 4 × 1 = **4 (LOW)** - Acceptable after implementation

**Status**: **OPEN** - Awaiting budget approval
**Owner**: Manufacturing Safety Engineering
**Review Date**: Monthly
**Threat Actor**: [[THREAT_ACTOR: Disgruntled employee]]

---

## HAZARD-005: Railway Train Collision

**Asset**: [[EQUIPMENT: Railway interlocking controller]]
**Threat**: [[ATTACK_PATTERN: Signal aspect manipulation]]
**Vulnerability**: [[VULNERABILITY: Legacy signaling protocol]]
**Hazard**: [[HAZARD: Conflicting signal aspects]]

**Consequence**: Train collision, multiple fatalities, infrastructure damage
**Consequence Severity**: Catastrophic

**Existing Controls**:
- [[ARCHITECTURE: Interlocking logic verification]]
- [[MITIGATION: Vital processing]]
- [[ARCHITECTURE: Automatic train protection]]

**Initial Risk Rating**: 5 (Catastrophic) × 2 (Unlikely) = **10 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: Secure signaling protocol implementation]]
- [[ARCHITECTURE: Cryptographic message authentication]]
- [[MITIGATION: Signal aspect verification system]]
- [[ARCHITECTURE: Train separation enforcement enhancement]]

**Residual Risk**: 4 × 1 = **4 (LOW)** - Acceptable after implementation

**Status**: **IN PROGRESS** - Protocol upgrade project initiated
**Owner**: Railway Signaling Engineering
**Review Date**: Quarterly
**Threat Actor**: [[THREAT_ACTOR: Railway saboteur]]

---

## HAZARD-006: Chemical Plant Runaway Reaction

**Asset**: [[EQUIPMENT: Batch reactor control system]]
**Threat**: [[ATTACK_PATTERN: Reactor temperature control manipulation]]
**Vulnerability**: [[VULNERABILITY: DCS engineering workstation compromise]]
**Hazard**: [[HAZARD: Runaway exothermic reaction]]

**Consequence**: Reactor explosion, worker fatalities, toxic release, environmental damage
**Consequence Severity**: Catastrophic

**Existing Controls**:
- [[MITIGATION: Temperature high alarm]]
- [[ARCHITECTURE: Pressure relief system]]
- [[MITIGATION: Emergency cooling injection]]

**Initial Risk Rating**: 5 (Catastrophic) × 3 (Possible) = **15 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: Engineering workstation hardening]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Application whitelisting]]
- [[MITIGATION: Setpoint rate limiting]]
- [[ARCHITECTURE: Independent SIL 3 safety system]]

**Residual Risk**: 4 × 2 = **8 (MEDIUM)** - Acceptable after implementation

**Status**: **IN PROGRESS** - Workstation hardening phase 1 complete
**Owner**: Chemical Plant Process Safety
**Review Date**: Monthly
**Threat Actor**: [[THREAT_ACTOR: Chemical plant saboteur]]

---

## HAZARD-007: Hospital Medical Gas System Failure

**Asset**: [[EQUIPMENT: Hospital medical gas control system]]
**Threat**: [[ATTACK_PATTERN: Building automation system attack]]
**Vulnerability**: [[VULNERABILITY: BACnet protocol vulnerability]]
**Hazard**: [[HAZARD: Loss of patient oxygen supply]]

**Consequence**: Patient fatalities, medical emergency, regulatory violations
**Consequence Severity**: Critical

**Existing Controls**:
- [[MITIGATION: Building management network isolation]]
- [[ARCHITECTURE: Backup oxygen cylinders at bedside]]
- [[MITIGATION: Low pressure alarm system]]

**Initial Risk Rating**: 4 (Critical) × 3 (Possible) = **12 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: BACnet Secure Connect implementation]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Medical system network complete separation]]
- [[MITIGATION: Valve position monitoring]]
- [[ARCHITECTURE: Redundant gas supply sources]]

**Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable after implementation

**Status**: **IN PROGRESS** - BACnet security upgrade in design
**Owner**: Hospital Facilities & Biomedical Engineering
**Review Date**: Monthly
**Threat Actor**: [[THREAT_ACTOR: Healthcare facility attacker]]

---

## HAZARD-008: Oil Pipeline Rupture

**Asset**: [[EQUIPMENT: Crude oil pipeline SCADA control]]
**Threat**: [[ATTACK_PATTERN: Pipeline pressure control manipulation]]
**Vulnerability**: [[VULNERABILITY: SCADA master server vulnerability]]
**Hazard**: [[HAZARD: Pipeline overpressure and rupture]]

**Consequence**: Major oil spill, environmental damage, fire risk, cleanup costs
**Consequence Severity**: Critical

**Existing Controls**:
- [[ARCHITECTURE: SCADA DMZ architecture]]
- [[MITIGATION: Firewall protection]]
- [[ARCHITECTURE: Mechanical pressure relief valves]]

**Initial Risk Rating**: 4 (Critical) × 3 (Possible) = **12 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: SCADA server hardening]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Pressure setpoint validation logic]]
- [[MITIGATION: Leak detection system enhancement]]
- [[ARCHITECTURE: Block valve automation for isolation]]

**Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable after implementation

**Status**: **OPEN** - Security assessment scheduled
**Owner**: Pipeline Operations & Cybersecurity
**Review Date**: Bi-monthly
**Threat Actor**: [[THREAT_ACTOR: Energy infrastructure saboteur]]

---

## HAZARD-009: LNG Terminal Catastrophic Release

**Asset**: [[EQUIPMENT: LNG marine loading arm control system]]
**Threat**: [[ATTACK_PATTERN: Emergency shutdown system disable]]
**Vulnerability**: [[VULNERABILITY: Safety system network connection]]
**Hazard**: [[HAZARD: Emergency release failure during ship departure]]

**Consequence**: Massive LNG spill, major fire, vapor cloud explosion, mass casualties
**Consequence Severity**: Catastrophic

**Existing Controls**:
- [[ARCHITECTURE: Mechanical fusible link backup]]
- [[MITIGATION: Breakaway coupling]]
- [[ARCHITECTURE: Manual emergency release]]

**Initial Risk Rating**: 5 (Catastrophic) × 1 (Rare) = **5 (LOW)**

**Additional Controls Recommended**:
- [[MITIGATION: Complete safety system air gap verification]]
- [[ARCHITECTURE: Diverse release mechanisms testing]]
- [[MITIGATION: Regular ESD system functional testing]]
- [[ARCHITECTURE: Independent safety monitoring]]

**Residual Risk**: 5 × 1 = **5 (LOW)** - Acceptable with monitoring

**Status**: **MONITORING** - Controls adequate, regular testing performed
**Owner**: LNG Terminal Safety Engineering
**Review Date**: Semi-annual
**Threat Actor**: [[THREAT_ACTOR: Marine terminal terrorist]]

---

## HAZARD-010: Data Center Cooling Failure

**Asset**: [[EQUIPMENT: Data center CRAC control system]]
**Threat**: [[ATTACK_PATTERN: Building automation cooling manipulation]]
**Vulnerability**: [[VULNERABILITY: BMS network exposure]]
**Hazard**: [[HAZARD: Server overheating and shutdown]]

**Consequence**: Service outage, equipment damage, data loss, revenue impact
**Consequence Severity**: Moderate

**Existing Controls**:
- [[MITIGATION: Temperature monitoring system]]
- [[ARCHITECTURE: Redundant CRAC units]]
- [[MITIGATION: Server thermal shutdown protection]]

**Initial Risk Rating**: 2 (Moderate) × 4 (Likely) = **8 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: BMS network segmentation]]
- [[ARCHITECTURE: Cooling setpoint validation]]
- [[MITIGATION: Anomaly detection for temperature changes]]
- [[ARCHITECTURE: Portable emergency cooling equipment]]

**Residual Risk**: 1 × 3 = **3 (LOW)** - Acceptable after implementation

**Status**: **IN PROGRESS** - Network segmentation project
**Owner**: Data Center Operations
**Review Date**: Quarterly
**Threat Actor**: [[THREAT_ACTOR: Ransomware operator]]

---

## HAZARD-011: Airport Runway Lighting Failure

**Asset**: [[EQUIPMENT: Airfield lighting control system]]
**Threat**: [[ATTACK_PATTERN: Lighting control protocol attack]]
**Vulnerability**: [[VULNERABILITY: Legacy lighting protocol]]
**Hazard**: [[HAZARD: Loss of runway approach lighting]]

**Consequence**: Aircraft landing incident, potential hull loss, fatalities
**Consequence Severity**: Critical

**Existing Controls**:
- [[ARCHITECTURE: Dedicated lighting network]]
- [[MITIGATION: Lighting status monitoring]]
- [[ARCHITECTURE: Emergency lighting backup battery]]

**Initial Risk Rating**: 4 (Critical) × 2 (Unlikely) = **8 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: Protocol modernization to secure standard]]
- [[ARCHITECTURE: Lighting command validation logic]]
- [[MITIGATION: RF spectrum monitoring]]
- [[ARCHITECTURE: ILS independent approach guidance]]

**Residual Risk**: 3 × 1 = **3 (LOW)** - Acceptable after implementation

**Status**: **OPEN** - Awaiting FAA guidance on protocol upgrade
**Owner**: Airport Operations & Engineering
**Review Date**: Quarterly
**Threat Actor**: [[THREAT_ACTOR: Aviation infrastructure terrorist]]

---

## HAZARD-012: Smart Grid Demand Manipulation

**Asset**: [[EQUIPMENT: Advanced metering infrastructure]]
**Threat**: [[ATTACK_PATTERN: Smart meter firmware compromise]]
**Vulnerability**: [[VULNERABILITY: Insecure firmware update mechanism]]
**Hazard**: [[HAZARD: False demand data causing grid control errors]]

**Consequence**: Grid instability, equipment stress, localized outages
**Consequence Severity**: Serious

**Existing Controls**:
- [[MITIGATION: Meter data validation]]
- [[ARCHITECTURE: AMI head-end monitoring]]
- [[MITIGATION: Firmware update authentication]]

**Initial Risk Rating**: 3 (Serious) × 3 (Possible) = **9 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: Secure firmware signing and encryption]]
- [[ARCHITECTURE: Meter attestation system]]
- [[MITIGATION: Demand data anomaly detection]]
- [[ARCHITECTURE: Cross-validation with grid sensors]]

**Residual Risk**: 2 × 2 = **4 (LOW)** - Acceptable after implementation

**Status**: **IN PROGRESS** - Firmware security enhancement project
**Owner**: Smart Grid Technology
**Review Date**: Quarterly
**Threat Actor**: [[THREAT_ACTOR: Energy theft organization]]

---

## HAZARD-013: Pharmaceutical Clean Room Contamination

**Asset**: [[EQUIPMENT: Pharmaceutical clean room HVAC control]]
**Threat**: [[ATTACK_PATTERN: Clean room pressure control manipulation]]
**Vulnerability**: [[VULNERABILITY: BMS web interface SQL injection]]
**Hazard**: [[HAZARD: Loss of positive pressure causing contamination]]

**Consequence**: Product contamination, patient harm, regulatory action, recall
**Consequence Severity**: Serious

**Existing Controls**:
- [[MITIGATION: Differential pressure monitoring]]
- [[ARCHITECTURE: HEPA filtration system]]
- [[MITIGATION: Environmental monitoring program]]

**Initial Risk Rating**: 3 (Serious) × 3 (Possible) = **9 (MEDIUM)**

**Additional Controls Recommended**:
- [[MITIGATION: Web interface vulnerability remediation]]
- [[ARCHITECTURE: BMS network isolation from corporate]]
- [[MITIGATION: Pressure deviation alarms]]
- [[ARCHITECTURE: Backup filtration capacity]]

**Residual Risk**: 2 × 2 = **4 (LOW)** - Acceptable after implementation

**Status**: **IN PROGRESS** - Web security audit complete, remediation planned
**Owner**: Pharmaceutical Quality Assurance
**Review Date**: Monthly
**Threat Actor**: [[THREAT_ACTOR: Pharmaceutical saboteur]]

---

## HAZARD-014: Mining Ventilation System Failure

**Asset**: [[EQUIPMENT: Underground mine ventilation control]]
**Threat**: [[ATTACK_PATTERN: Ventilation fan VFD frequency attack]]
**Vulnerability**: [[VULNERABILITY: Unsecured Modbus communications]]
**Hazard**: [[HAZARD: Inadequate mine ventilation causing toxic gas accumulation]]

**Consequence**: Miner fatalities, mine evacuation, rescue operations
**Consequence Severity**: Catastrophic

**Existing Controls**:
- [[MITIGATION: Gas concentration monitoring]]
- [[ARCHITECTURE: Backup ventilation fans]]
- [[MITIGATION: Mine evacuation system]]

**Initial Risk Rating**: 5 (Catastrophic) × 1 (Rare) = **5 (LOW)**

**Additional Controls Recommended**:
- [[MITIGATION: Modbus protocol encryption]]
- [[ARCHITECTURE: VFD network segmentation]]
- [[MITIGATION: Fan speed verification monitoring]]
- [[ARCHITECTURE: Independent gas monitoring system]]

**Residual Risk**: 5 × 1 = **5 (LOW)** - Acceptable with monitoring

**Status**: **MONITORING** - Controls adequate for remote location
**Owner**: Mine Safety Engineering
**Review Date**: Semi-annual
**Threat Actor**: [[THREAT_ACTOR: Mining operation saboteur]]

---

## HAZARD-015: Food Processing Pasteurization Failure

**Asset**: [[EQUIPMENT: Food pasteurization control system]]
**Threat**: [[ATTACK_PATTERN: Pasteurization temperature controller manipulation]]
**Vulnerability**: [[VULNERABILITY: Unprotected temperature controller access]]
**Hazard**: [[HAZARD: Inadequate heat treatment allowing pathogen survival]]

**Consequence**: Foodborne illness outbreak, public health impact, product recall
**Consequence Severity**: Critical

**Existing Controls**:
- [[MITIGATION: Temperature recording charts]]
- [[ARCHITECTURE: Quality control microbial testing]]
- [[MITIGATION: Operator monitoring]]

**Initial Risk Rating**: 4 (Critical) × 3 (Possible) = **12 (HIGH)**

**Additional Controls Recommended**:
- [[MITIGATION: Controller authentication and access control]] - **PRIORITY ACTION**
- [[ARCHITECTURE: Redundant temperature measurement]]
- [[MITIGATION: Pasteurization validation logic]]
- [[ARCHITECTURE: Independent safety recording]]

**Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable after implementation

**Status**: **OPEN** - Security assessment planned
**Owner**: Food Safety & Quality Assurance
**Review Date**: Monthly
**Threat Actor**: [[THREAT_ACTOR: Food terrorism actor]]

---

## Hazard Register Summary Statistics

### Status Distribution
- **OPEN**: 4 hazards (27%) - Action planning phase
- **IN PROGRESS**: 8 hazards (53%) - Mitigation implementation underway
- **MONITORING**: 3 hazards (20%) - Acceptable risk with ongoing oversight
- **CLOSED**: 0 hazards (0%) - None fully resolved yet

### Risk Rating Distribution
**Initial Risk**:
- **Critical (20-25)**: 0 hazards
- **High (12-16)**: 5 hazards (33%)
- **Medium (6-10)**: 8 hazards (53%)
- **Low (3-5)**: 2 hazards (14%)

**Residual Risk** (After planned controls):
- **Critical (20-25)**: 0 hazards
- **High (12-16)**: 0 hazards
- **Medium (6-10)**: 6 hazards (40%)
- **Low (3-5)**: 9 hazards (60%)

### Consequence Severity
- **Catastrophic (5)**: 5 hazards - Nuclear, chemical, railway, LNG, mining
- **Critical (4)**: 7 hazards - Water, power, robot, hospital, pipeline, airport, food
- **Serious (3)**: 2 hazards - Smart grid, pharmaceutical
- **Moderate (2)**: 1 hazard - Data center

### Cross-Reference Inventory
- **EQUIPMENT**: 15 unique critical infrastructure systems
- **ATTACK_PATTERNS**: 15 distinct cyber threat vectors
- **VULNERABILITIES**: 15 security weaknesses requiring remediation
- **HAZARDS**: 15 safety consequences with potential for harm
- **MITIGATIONS**: 75 total (45 existing + 30 recommended)
- **ARCHITECTURES**: 75 defense architecture elements
- **THREAT_ACTORS**: 15 adversary profiles

### Priority Actions Required
1. **HAZARD-002** (Water Treatment) - MFA implementation
2. **HAZARD-003** (Power Grid) - IEC 62351 deployment
3. **HAZARD-006** (Chemical Plant) - Workstation hardening
4. **HAZARD-007** (Hospital) - BACnet security upgrade
5. **HAZARD-008** (Pipeline) - SCADA hardening
6. **HAZARD-015** (Food Processing) - Controller security

### Review Schedule
- **Monthly Reviews**: 6 hazards requiring close monitoring
- **Bi-monthly Reviews**: 2 hazards in active implementation
- **Quarterly Reviews**: 4 hazards with lower risk profile
- **Semi-annual Reviews**: 3 hazards with adequate controls

### Key Insights
1. **53% of hazards in active mitigation** - Significant cybersecurity investment underway
2. **All high-risk items have action plans** - No unmanaged critical risks
3. **Defense-in-depth approach** - Multiple layers of protection for each hazard
4. **Risk reduction effectiveness** - 48% average risk score reduction planned
5. **Continuous improvement** - Regular review cycle ensures ongoing risk management

### Register Maintenance
- **Update Frequency**: All hazards reviewed at specified intervals
- **New Hazard Addition**: Process for identifying and adding new cyber-physical threats
- **Status Changes**: Tracked with date stamps and justification
- **Lessons Learned**: Incidents feed back into register for enhanced controls
- **Regulatory Alignment**: Controls mapped to applicable standards (NERC CIP, NIST, IEC 62443)
