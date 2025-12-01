# Bow-Tie Analysis: Cyber-Physical Security for Critical Infrastructure

## Overview
Bow-tie analysis visualizes the relationship between hazards, causes (threats), preventive barriers, consequences, and recovery/mitigation barriers. This document applies bow-tie methodology to cyber-physical threats in critical infrastructure.

## Bow-Tie Structure
```
THREATS → PREVENTIVE BARRIERS → HAZARD → RECOVERY BARRIERS → CONSEQUENCES
```

---

## Bow-Tie Scenario 1: Water Treatment Chemical Overdose

**Hazard**: [[HAZARD: Excessive chlorine injection]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: PLC ladder logic manipulation]] exploiting [[VULNERABILITY: Weak PLC authentication]]
  - Preventive Barrier: [[MITIGATION: Multi-factor authentication]]
  - Preventive Barrier: [[ARCHITECTURE: Network segmentation]]
  - Preventive Barrier: [[MITIGATION: Logic integrity checking]]

- **Threat 2**: [[ATTACK_PATTERN: HMI command injection]] through [[VULNERABILITY: SQL injection in HMI]]
  - Preventive Barrier: [[MITIGATION: Input validation]]
  - Preventive Barrier: [[MITIGATION: Prepared statements]]
  - Preventive Barrier: [[ARCHITECTURE: Web application firewall]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Public water contamination
  - Recovery Barrier: [[MITIGATION: High-level alarm system]]
  - Recovery Barrier: [[ARCHITECTURE: Emergency shutdown valve]]
  - Recovery Barrier: [[MITIGATION: Water quality monitoring]]

- **Consequence 2**: Regulatory violation
  - Recovery Barrier: [[MITIGATION: Incident response plan]]
  - Recovery Barrier: [[ARCHITECTURE: Backup water supply]]

**Central Equipment**: [[EQUIPMENT: Chemical dosing pump control system]]
**Threat Actor**: [[THREAT_ACTOR: Water infrastructure terrorist]]

---

## Bow-Tie Scenario 2: Power Grid Cascade Failure

**Hazard**: [[HAZARD: Transmission line overload]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: IEC 61850 GOOSE message spoofing]] exploiting [[VULNERABILITY: Unauthenticated multicast]]
  - Preventive Barrier: [[MITIGATION: IEC 62351 security]]
  - Preventive Barrier: [[ARCHITECTURE: VLAN isolation]]
  - Preventive Barrier: [[MITIGATION: Message authentication codes]]

- **Threat 2**: [[ATTACK_PATTERN: Protection relay false trip]] through [[VULNERABILITY: Firmware vulnerability]]
  - Preventive Barrier: [[MITIGATION: Firmware signing]]
  - Preventive Barrier: [[MITIGATION: Secure boot]]
  - Preventive Barrier: [[ARCHITECTURE: Physical relay room security]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Regional blackout
  - Recovery Barrier: [[MITIGATION: Load shedding procedures]]
  - Recovery Barrier: [[ARCHITECTURE: Islanding capability]]
  - Recovery Barrier: [[MITIGATION: Black start procedures]]

- **Consequence 2**: Equipment damage
  - Recovery Barrier: [[ARCHITECTURE: Fault current limiters]]
  - Recovery Barrier: [[MITIGATION: Protective relay backup]]

**Central Equipment**: [[EQUIPMENT: Transmission protection relay]]
**Threat Actor**: [[THREAT_ACTOR: Nation-state grid warfare actor]]

---

## Bow-Tie Scenario 3: Nuclear Reactor Coolant Loss

**Hazard**: [[HAZARD: Loss of reactor coolant flow]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: Safety PLC manipulation]] exploiting [[VULNERABILITY: Legacy safety system protocol]]
  - Preventive Barrier: [[MITIGATION: Air gap enforcement]]
  - Preventive Barrier: [[ARCHITECTURE: Unidirectional gateway]]
  - Preventive Barrier: [[MITIGATION: Physical access control]]

- **Threat 2**: [[ATTACK_PATTERN: Sensor data injection]] through [[VULNERABILITY: Analog signal vulnerability]]
  - Preventive Barrier: [[MITIGATION: Signal encryption]]
  - Preventive Barrier: [[ARCHITECTURE: Redundant sensor validation]]
  - Preventive Barrier: [[MITIGATION: Anomaly detection]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Core damage
  - Recovery Barrier: [[ARCHITECTURE: Emergency core cooling system]]
  - Recovery Barrier: [[MITIGATION: Reactor SCRAM system]]
  - Recovery Barrier: [[ARCHITECTURE: Containment structure]]

- **Consequence 2**: Radiation release
  - Recovery Barrier: [[MITIGATION: Radiation monitoring]]
  - Recovery Barrier: [[ARCHITECTURE: Emergency response plan]]

**Central Equipment**: [[EQUIPMENT: Reactor protection system]]
**Threat Actor**: [[THREAT_ACTOR: Nuclear facility saboteur]]

---

## Bow-Tie Scenario 4: Manufacturing Robot Injury

**Hazard**: [[HAZARD: Robot collision with worker]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: Robot program injection]] exploiting [[VULNERABILITY: Unsecured robot teach pendant]]
  - Preventive Barrier: [[MITIGATION: Robot controller authentication]]
  - Preventive Barrier: [[ARCHITECTURE: Program verification]]
  - Preventive Barrier: [[MITIGATION: Digital signature on programs]]

- **Threat 2**: [[ATTACK_PATTERN: Safety zone bypass]] through [[VULNERABILITY: Safety PLC vulnerability]]
  - Preventive Barrier: [[MITIGATION: Safety integrity level 3 compliance]]
  - Preventive Barrier: [[ARCHITECTURE: Hardwired safety circuits]]
  - Preventive Barrier: [[MITIGATION: Safety zone monitoring]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Worker injury
  - Recovery Barrier: [[ARCHITECTURE: Emergency stop system]]
  - Recovery Barrier: [[MITIGATION: Safety light curtains]]
  - Recovery Barrier: [[ARCHITECTURE: Collaborative robot safeguards]]

- **Consequence 2**: Production halt
  - Recovery Barrier: [[MITIGATION: Incident investigation procedure]]
  - Recovery Barrier: [[ARCHITECTURE: Backup manual processes]]

**Central Equipment**: [[EQUIPMENT: Industrial welding robot]]
**Threat Actor**: [[THREAT_ACTOR: Disgruntled manufacturing employee]]

---

## Bow-Tie Scenario 5: Railway Train Collision

**Hazard**: [[HAZARD: Signal showing incorrect aspect]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: Signaling protocol manipulation]] exploiting [[VULNERABILITY: Legacy signaling vulnerability]]
  - Preventive Barrier: [[MITIGATION: Protocol cryptographic signing]]
  - Preventive Barrier: [[ARCHITECTURE: Vital processing]]
  - Preventive Barrier: [[MITIGATION: Signaling network isolation]]

- **Threat 2**: [[ATTACK_PATTERN: Interlocking system attack]] through [[VULNERABILITY: Wayside equipment access]]
  - Preventive Barrier: [[MITIGATION: Physical tamper detection]]
  - Preventive Barrier: [[ARCHITECTURE: Secure wayside cabinets]]
  - Preventive Barrier: [[MITIGATION: Interlocking logic verification]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Train collision
  - Recovery Barrier: [[ARCHITECTURE: Automatic train protection]]
  - Recovery Barrier: [[MITIGATION: Cab signaling backup]]
  - Recovery Barrier: [[ARCHITECTURE: Train separation enforcement]]

- **Consequence 2**: Casualties
  - Recovery Barrier: [[MITIGATION: Emergency response coordination]]
  - Recovery Barrier: [[ARCHITECTURE: Train crashworthiness design]]

**Central Equipment**: [[EQUIPMENT: Railway interlocking controller]]
**Threat Actor**: [[THREAT_ACTOR: Rail infrastructure saboteur]]

---

## Bow-Tie Scenario 6: Chemical Plant Reactor Explosion

**Hazard**: [[HAZARD: Runaway exothermic reaction]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: DCS setpoint manipulation]] exploiting [[VULNERABILITY: Engineering workstation compromise]]
  - Preventive Barrier: [[MITIGATION: Engineering station hardening]]
  - Preventive Barrier: [[ARCHITECTURE: Change management system]]
  - Preventive Barrier: [[MITIGATION: Setpoint rate limiting]]

- **Threat 2**: [[ATTACK_PATTERN: Temperature sensor spoofing]] through [[VULNERABILITY: RTU communication vulnerability]]
  - Preventive Barrier: [[MITIGATION: Sensor signal validation]]
  - Preventive Barrier: [[ARCHITECTURE: Redundant temperature measurement]]
  - Preventive Barrier: [[MITIGATION: RTU authentication]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Reactor explosion
  - Recovery Barrier: [[ARCHITECTURE: Pressure relief system]]
  - Recovery Barrier: [[MITIGATION: Emergency cooling injection]]
  - Recovery Barrier: [[ARCHITECTURE: Blast-resistant control room]]

- **Consequence 2**: Toxic release
  - Recovery Barrier: [[MITIGATION: Emergency response plan]]
  - Recovery Barrier: [[ARCHITECTURE: Containment dikes]]

**Central Equipment**: [[EQUIPMENT: Batch reactor control system]]
**Threat Actor**: [[THREAT_ACTOR: Chemical plant saboteur]]

---

## Bow-Tie Scenario 7: Hospital Life Support Failure

**Hazard**: [[HAZARD: Loss of medical gas pressure]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: Building automation system attack]] exploiting [[VULNERABILITY: BACnet vulnerability]]
  - Preventive Barrier: [[MITIGATION: BACnet Secure Connect]]
  - Preventive Barrier: [[ARCHITECTURE: Medical gas system isolation]]
  - Preventive Barrier: [[MITIGATION: Network segmentation]]

- **Threat 2**: [[ATTACK_PATTERN: Valve control manipulation]] through [[VULNERABILITY: SNMP write access]]
  - Preventive Barrier: [[MITIGATION: SNMPv3 authentication]]
  - Preventive Barrier: [[ARCHITECTURE: Read-only SNMP]]
  - Preventive Barrier: [[MITIGATION: Valve position monitoring]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Patient harm
  - Recovery Barrier: [[ARCHITECTURE: Backup oxygen cylinders]]
  - Recovery Barrier: [[MITIGATION: Pressure alarm system]]
  - Recovery Barrier: [[ARCHITECTURE: Redundant gas sources]]

- **Consequence 2**: Medical malpractice
  - Recovery Barrier: [[MITIGATION: Emergency protocols]]
  - Recovery Barrier: [[ARCHITECTURE: Patient transfer capability]]

**Central Equipment**: [[EQUIPMENT: Medical gas control panel]]
**Threat Actor**: [[THREAT_ACTOR: Healthcare infrastructure attacker]]

---

## Bow-Tie Scenario 8: Airport Runway Lighting Failure

**Hazard**: [[HAZARD: Loss of runway approach lighting]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: Lighting control protocol attack]] exploiting [[VULNERABILITY: Legacy airfield protocol]]
  - Preventive Barrier: [[MITIGATION: Protocol modernization]]
  - Preventive Barrier: [[ARCHITECTURE: Lighting system network isolation]]
  - Preventive Barrier: [[MITIGATION: Access control lists]]

- **Threat 2**: [[ATTACK_PATTERN: Power distribution attack]] through [[VULNERABILITY: Unsecured PDU management]]
  - Preventive Barrier: [[MITIGATION: PDU authentication]]
  - Preventive Barrier: [[ARCHITECTURE: Redundant power circuits]]
  - Preventive Barrier: [[MITIGATION: Power monitoring]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Aircraft incident
  - Recovery Barrier: [[ARCHITECTURE: Instrument landing system]]
  - Recovery Barrier: [[MITIGATION: Alternate runway procedures]]
  - Recovery Barrier: [[ARCHITECTURE: Emergency lighting backup]]

- **Consequence 2**: Airport closure
  - Recovery Barrier: [[MITIGATION: Rapid repair procedures]]
  - Recovery Barrier: [[ARCHITECTURE: Portable lighting equipment]]

**Central Equipment**: [[EQUIPMENT: Airfield lighting control system]]
**Threat Actor**: [[THREAT_ACTOR: Aviation infrastructure terrorist]]

---

## Bow-Tie Scenario 9: Oil Pipeline Rupture

**Hazard**: [[HAZARD: Pipeline overpressure]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: SCADA command injection]] exploiting [[VULNERABILITY: Weak SCADA authentication]]
  - Preventive Barrier: [[MITIGATION: Strong authentication]]
  - Preventive Barrier: [[ARCHITECTURE: SCADA DMZ]]
  - Preventive Barrier: [[MITIGATION: Command validation]]

- **Threat 2**: [[ATTACK_PATTERN: Pressure relief valve disable]] through [[VULNERABILITY: Safety system network access]]
  - Preventive Barrier: [[MITIGATION: Safety system isolation]]
  - Preventive Barrier: [[ARCHITECTURE: Hardwired relief logic]]
  - Preventive Barrier: [[MITIGATION: Relief valve monitoring]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Pipeline rupture
  - Recovery Barrier: [[ARCHITECTURE: Block valve system]]
  - Recovery Barrier: [[MITIGATION: Leak detection system]]
  - Recovery Barrier: [[ARCHITECTURE: Emergency response plan]]

- **Consequence 2**: Environmental damage
  - Recovery Barrier: [[MITIGATION: Spill containment]]
  - Recovery Barrier: [[ARCHITECTURE: Pipeline monitoring]]

**Central Equipment**: [[EQUIPMENT: Pipeline SCADA master]]
**Threat Actor**: [[THREAT_ACTOR: Energy infrastructure saboteur]]

---

## Bow-Tie Scenario 10: Data Center Cooling Loss

**Hazard**: [[HAZARD: Server room overheating]]

**Left Side (Threat Prevention)**:
- **Threat 1**: [[ATTACK_PATTERN: CRAC unit attack]] exploiting [[VULNERABILITY: BACnet vulnerability]]
  - Preventive Barrier: [[MITIGATION: BACnet security extensions]]
  - Preventive Barrier: [[ARCHITECTURE: Facility network isolation]]
  - Preventive Barrier: [[MITIGATION: Cooling system monitoring]]

- **Threat 2**: [[ATTACK_PATTERN: Chilled water valve manipulation]] through [[VULNERABILITY: Building automation exposure]]
  - Preventive Barrier: [[MITIGATION: Valve control security]]
  - Preventive Barrier: [[ARCHITECTURE: Independent thermal monitoring]]
  - Preventive Barrier: [[MITIGATION: Valve position verification]]

**Right Side (Consequence Mitigation)**:
- **Consequence 1**: Server shutdown
  - Recovery Barrier: [[ARCHITECTURE: Thermal shutdown protection]]
  - Recovery Barrier: [[MITIGATION: Hot aisle containment]]
  - Recovery Barrier: [[ARCHITECTURE: Portable cooling units]]

- **Consequence 2**: Data loss
  - Recovery Barrier: [[MITIGATION: Data backup systems]]
  - Recovery Barrier: [[ARCHITECTURE: Redundant data centers]]

**Central Equipment**: [[EQUIPMENT: Data center cooling control]]
**Threat Actor**: [[THREAT_ACTOR: Data center saboteur]]

---

## Bow-Tie Summary Statistics
- **Total Scenarios**: 10 comprehensive bow-tie analyses
- **Hazards Analyzed**: 10 critical safety events
- **Threats Identified**: 20 attack patterns (2 per scenario)
- **Preventive Barriers**: 60 protective controls (avg 6 per scenario)
- **Consequences**: 20 potential outcomes (2 per scenario)
- **Recovery Barriers**: 50 mitigation measures (avg 5 per scenario)
- **Cross-References**: 10 EQUIPMENT, 20 ATTACK_PATTERNS, 20 VULNERABILITIES, 10 HAZARDS, 110 MITIGATIONS, 60 ARCHITECTURES, 10 THREAT_ACTORS

## Bow-Tie Analysis Value
- **Comprehensive View**: Shows complete threat-to-consequence pathway
- **Barrier Effectiveness**: Evaluates multiple layers of defense
- **Gap Analysis**: Identifies missing preventive or recovery controls
- **Risk Communication**: Visual representation for stakeholders
- **Prioritization**: Focuses on high-impact scenarios with weak barriers
