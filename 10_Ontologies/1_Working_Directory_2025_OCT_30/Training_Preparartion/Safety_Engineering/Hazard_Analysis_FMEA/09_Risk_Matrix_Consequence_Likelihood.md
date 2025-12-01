# Risk Matrix: Cybersecurity Threat Consequence and Likelihood Assessment

## Overview
Risk matrices provide a visual framework for assessing risk by combining consequence severity with likelihood of occurrence. This document applies risk matrix methodology to cybersecurity threats in critical infrastructure with safety implications.

## Risk Matrix Framework

### Consequence Categories (Severity)
- **Catastrophic (5)**: Multiple fatalities, major environmental damage, critical infrastructure loss
- **Critical (4)**: Single fatality, significant injury, major system damage, extended outage
- **Serious (3)**: Serious injury, moderate equipment damage, significant operational disruption
- **Moderate (2)**: Minor injury, equipment damage, temporary operational impact
- **Minor (1)**: No injury, minimal damage, brief disruption

### Likelihood Categories (Probability)
- **Very Likely (5)**: Expected to occur frequently (>1/year)
- **Likely (4)**: Expected to occur occasionally (0.1-1/year)
- **Possible (3)**: Could occur (0.01-0.1/year)
- **Unlikely (2)**: Not expected but possible (0.001-0.01/year)
- **Rare (1)**: Very unlikely to occur (<0.001/year)

### Risk Rating (Consequence × Likelihood)
- **CRITICAL (20-25)**: Immediate action required, unacceptable risk
- **HIGH (12-16)**: Priority attention, risk reduction required
- **MEDIUM (6-10)**: Risk reduction as practical, monitor carefully
- **LOW (3-5)**: Accept with monitoring
- **VERY LOW (1-2)**: Broadly acceptable

---

## Risk Assessment Scenario 1: Nuclear Reactor Safety System Attack

**Asset**: [[EQUIPMENT: Nuclear reactor protection system]]
**Threat**: [[ATTACK_PATTERN: Safety PLC reprogramming]] via [[VULNERABILITY: Maintenance port access]]
**Hazard**: [[HAZARD: Loss of reactor protection during transient]]

**Consequence Analysis**:
- Potential core damage
- Radiation release risk
- Public health impact
- **Consequence Rating: Catastrophic (5)**

**Likelihood Analysis**:
- Physical access required
- Specialized knowledge needed
- Strong security measures
- **Likelihood Rating: Rare (1)**

**Risk Score**: 5 × 1 = **5 (LOW)**

**Risk Treatment**:
- [[MITIGATION: Air gap enforcement]] - Accepted with monitoring
- [[ARCHITECTURE: Independent safety channels]] - Maintains low risk
- Regular security assessments

**Threat Actor**: [[THREAT_ACTOR: Nation-state nuclear saboteur]]

---

## Risk Assessment Scenario 2: Water Treatment Chemical Overdose

**Asset**: [[EQUIPMENT: Water treatment chemical dosing system]]
**Threat**: [[ATTACK_PATTERN: SCADA dosing control manipulation]] via [[VULNERABILITY: Weak VPN authentication]]
**Hazard**: [[HAZARD: Toxic chemical contamination of public water]]

**Consequence Analysis**:
- Mass public health impact
- Potential fatalities
- Loss of public trust
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- Remote access vulnerability
- Phishing successful
- Limited authentication
- **Likelihood Rating: Likely (4)**

**Risk Score**: 4 × 4 = **16 (HIGH)**

**Risk Treatment**:
- **IMMEDIATE ACTION REQUIRED**
- [[MITIGATION: Multi-factor authentication]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Chemical flow rate limiting]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Water infrastructure terrorist]]

---

## Risk Assessment Scenario 3: Power Grid Cascading Failure

**Asset**: [[EQUIPMENT: Transmission system protection relays]]
**Threat**: [[ATTACK_PATTERN: IEC 61850 GOOSE message spoofing]] via [[VULNERABILITY: Unauthenticated substation communications]]
**Hazard**: [[HAZARD: Coordinated false trip causing cascade]]

**Consequence Analysis**:
- Regional blackout
- Critical services loss
- Economic impact
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- Known vulnerability
- Increasing capability
- Attractive target
- **Likelihood Rating: Possible (3)**

**Risk Score**: 4 × 3 = **12 (HIGH)**

**Risk Treatment**:
- [[MITIGATION: IEC 62351 security implementation]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Defense-in-depth protection]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Nation-state grid warfare actor]]

---

## Risk Assessment Scenario 4: Manufacturing Robot Worker Injury

**Asset**: [[EQUIPMENT: Industrial welding robot]]
**Threat**: [[ATTACK_PATTERN: Robot program injection]] via [[VULNERABILITY: Unsecured robot controller]]
**Hazard**: [[HAZARD: Robot collision with worker]]

**Consequence Analysis**:
- Worker fatality potential
- Serious injury likely
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- Network access required
- Safety systems present
- **Likelihood Rating: Unlikely (2)**

**Risk Score**: 4 × 2 = **8 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: Robot controller authentication]] - Reduces likelihood to Rare (1)
- [[ARCHITECTURE: Safety light curtains]] - Already present
- **Residual Risk**: 4 × 1 = **4 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Disgruntled employee]]

---

## Risk Assessment Scenario 5: Railway Train Collision

**Asset**: [[EQUIPMENT: Railway interlocking controller]]
**Threat**: [[ATTACK_PATTERN: Signal aspect manipulation]] via [[VULNERABILITY: Legacy signaling protocol]]
**Hazard**: [[HAZARD: Conflicting signal aspects]]

**Consequence Analysis**:
- Multiple fatalities
- Train collision
- **Consequence Rating: Catastrophic (5)**

**Likelihood Analysis**:
- Legacy vulnerabilities
- Increasing attacks
- **Likelihood Rating: Unlikely (2)**

**Risk Score**: 5 × 2 = **10 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: Secure signaling protocol upgrade]] - Reduces likelihood to Rare (1)
- [[ARCHITECTURE: Automatic train protection]] - Reduces consequence to Critical (4)
- **Residual Risk**: 4 × 1 = **4 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Railway saboteur]]

---

## Risk Assessment Scenario 6: Chemical Plant Explosion

**Asset**: [[EQUIPMENT: Batch reactor control system]]
**Threat**: [[ATTACK_PATTERN: Temperature control manipulation]] via [[VULNERABILITY: DCS workstation compromise]]
**Hazard**: [[HAZARD: Runaway exothermic reaction]]

**Consequence Analysis**:
- Reactor explosion
- Worker fatalities
- Toxic release
- **Consequence Rating: Catastrophic (5)**

**Likelihood Analysis**:
- Workstation vulnerabilities
- Malware threats
- **Likelihood Rating: Possible (3)**

**Risk Score**: 5 × 3 = **15 (HIGH)**

**Risk Treatment**:
- [[MITIGATION: Workstation hardening]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Independent safety system]] - Reduces consequence to Critical (4)
- **Residual Risk**: 4 × 2 = **8 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Chemical plant saboteur]]

---

## Risk Assessment Scenario 7: Hospital Life Support Failure

**Asset**: [[EQUIPMENT: Medical gas control system]]
**Threat**: [[ATTACK_PATTERN: Building automation attack]] via [[VULNERABILITY: BACnet vulnerability]]
**Hazard**: [[HAZARD: Loss of patient oxygen supply]]

**Consequence Analysis**:
- Patient fatalities
- Medical emergency
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- BMS vulnerabilities common
- Healthcare targeting increasing
- **Likelihood Rating: Possible (3)**

**Risk Score**: 4 × 3 = **12 (HIGH)**

**Risk Treatment**:
- [[MITIGATION: BACnet Secure Connect]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Backup oxygen cylinders]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Healthcare infrastructure attacker]]

---

## Risk Assessment Scenario 8: Oil Pipeline Rupture

**Asset**: [[EQUIPMENT: Pipeline SCADA control system]]
**Threat**: [[ATTACK_PATTERN: Pressure control manipulation]] via [[VULNERABILITY: SCADA server compromise]]
**Hazard**: [[HAZARD: Pipeline overpressure and rupture]]

**Consequence Analysis**:
- Major oil spill
- Environmental damage
- Fire risk
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- SCADA vulnerabilities
- Motivated adversaries
- **Likelihood Rating: Possible (3)**

**Risk Score**: 4 × 3 = **12 (HIGH)**

**Risk Treatment**:
- [[MITIGATION: SCADA hardening]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Pressure relief system]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Energy infrastructure saboteur]]

---

## Risk Assessment Scenario 9: LNG Terminal Catastrophic Release

**Asset**: [[EQUIPMENT: LNG loading arm control system]]
**Threat**: [[ATTACK_PATTERN: Emergency shutdown disable]] via [[VULNERABILITY: Safety system network access]]
**Hazard**: [[HAZARD: Emergency release failure during ship departure]]

**Consequence Analysis**:
- Massive LNG spill
- Major fire
- Multiple fatalities
- **Consequence Rating: Catastrophic (5)**

**Likelihood Analysis**:
- Difficult attack
- Strong security
- **Likelihood Rating: Rare (1)**

**Risk Score**: 5 × 1 = **5 (LOW)**

**Risk Treatment**:
- [[MITIGATION: Complete air gap]] - Maintains rare likelihood
- [[ARCHITECTURE: Mechanical fusible link]] - Independent protection
- **Residual Risk**: 5 × 1 = **5 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Marine terminal terrorist]]

---

## Risk Assessment Scenario 10: Data Center Cooling Failure

**Asset**: [[EQUIPMENT: Data center CRAC control system]]
**Threat**: [[ATTACK_PATTERN: Cooling system manipulation]] via [[VULNERABILITY: Building automation vulnerability]]
**Hazard**: [[HAZARD: Server overheating and shutdown]]

**Consequence Analysis**:
- Service outage
- Equipment damage
- Data loss potential
- **Consequence Rating: Moderate (2)**

**Likelihood Analysis**:
- BMS vulnerabilities
- Ransomware targeting
- **Likelihood Rating: Likely (4)**

**Risk Score**: 2 × 4 = **8 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: BMS security hardening]] - Reduces likelihood to Possible (3)
- [[ARCHITECTURE: Redundant cooling]] - Reduces consequence to Minor (1)
- **Residual Risk**: 1 × 3 = **3 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Ransomware operator]]

---

## Risk Assessment Scenario 11: Airport Runway Lighting Failure

**Asset**: [[EQUIPMENT: Airfield lighting control system]]
**Threat**: [[ATTACK_PATTERN: Lighting control protocol attack]] via [[VULNERABILITY: Legacy protocol]]
**Hazard**: [[HAZARD: Loss of runway approach lighting]]

**Consequence Analysis**:
- Aircraft landing incident
- Potential hull loss
- Fatalities possible
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- Legacy systems
- Lower priority target
- **Likelihood Rating: Unlikely (2)**

**Risk Score**: 4 × 2 = **8 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: Protocol modernization]] - Reduces likelihood to Rare (1)
- [[ARCHITECTURE: ILS backup guidance]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 1 = **3 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Aviation infrastructure terrorist]]

---

## Risk Assessment Scenario 12: Smart Grid Manipulation

**Asset**: [[EQUIPMENT: Advanced metering infrastructure]]
**Threat**: [[ATTACK_PATTERN: Smart meter firmware attack]] via [[VULNERABILITY: Insecure firmware updates]]
**Hazard**: [[HAZARD: False demand data causing grid control errors]]

**Consequence Analysis**:
- Grid stability impact
- Equipment stress
- Localized outages
- **Consequence Rating: Serious (3)**

**Likelihood Analysis**:
- Large attack surface
- Increasing capability
- **Likelihood Rating: Possible (3)**

**Risk Score**: 3 × 3 = **9 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: Secure firmware]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Demand validation]] - Reduces consequence to Moderate (2)
- **Residual Risk**: 2 × 2 = **4 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Energy theft organization]]

---

## Risk Assessment Scenario 13: Pharmaceutical Contamination

**Asset**: [[EQUIPMENT: Clean room HVAC control]]
**Threat**: [[ATTACK_PATTERN: Pressure control manipulation]] via [[VULNERABILITY: BMS web vulnerability]]
**Hazard**: [[HAZARD: Cleanroom contamination]]

**Consequence Analysis**:
- Product contamination
- Patient harm potential
- Regulatory action
- **Consequence Rating: Serious (3)**

**Likelihood Analysis**:
- Web vulnerabilities
- Targeted attacks
- **Likelihood Rating: Possible (3)**

**Risk Score**: 3 × 3 = **9 (MEDIUM)**

**Risk Treatment**:
- [[MITIGATION: Web security hardening]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Environmental monitoring]] - Reduces consequence to Moderate (2)
- **Residual Risk**: 2 × 2 = **4 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Pharmaceutical saboteur]]

---

## Risk Assessment Scenario 14: Mining Ventilation Failure

**Asset**: [[EQUIPMENT: Mine ventilation control system]]
**Threat**: [[ATTACK_PATTERN: Ventilation fan VFD attack]] via [[VULNERABILITY: Unsecured drive communications]]
**Hazard**: [[HAZARD: Toxic gas accumulation]]

**Consequence Analysis**:
- Miner fatalities
- Mine evacuation
- **Consequence Rating: Catastrophic (5)**

**Likelihood Analysis**:
- Remote location
- Limited access
- **Likelihood Rating: Rare (1)**

**Risk Score**: 5 × 1 = **5 (LOW)**

**Risk Treatment**:
- [[MITIGATION: VFD communication security]] - Maintains rare likelihood
- [[ARCHITECTURE: Redundant ventilation]] - Additional protection
- **Residual Risk**: 5 × 1 = **5 (LOW)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Mining saboteur]]

---

## Risk Assessment Scenario 15: Food Processing Contamination

**Asset**: [[EQUIPMENT: Pasteurization control system]]
**Threat**: [[ATTACK_PATTERN: Temperature controller manipulation]] via [[VULNERABILITY: Unprotected controller]]
**Hazard**: [[HAZARD: Inadequate pasteurization]]

**Consequence Analysis**:
- Foodborne illness outbreak
- Public health impact
- **Consequence Rating: Critical (4)**

**Likelihood Analysis**:
- Food sector targeting
- Accessible systems
- **Likelihood Rating: Possible (3)**

**Risk Score**: 4 × 3 = **12 (HIGH)**

**Risk Treatment**:
- [[MITIGATION: Controller authentication]] - Reduces likelihood to Unlikely (2)
- [[ARCHITECTURE: Temperature verification]] - Reduces consequence to Serious (3)
- **Residual Risk**: 3 × 2 = **6 (MEDIUM)** - Acceptable

**Threat Actor**: [[THREAT_ACTOR: Food safety saboteur]]

---

## Risk Matrix Summary

### Initial Risk Profile
- **Critical Risk (20-25)**: 0 scenarios
- **High Risk (12-16)**: 5 scenarios (33%)
- **Medium Risk (6-10)**: 8 scenarios (53%)
- **Low Risk (3-5)**: 2 scenarios (14%)

### Residual Risk Profile (After Treatment)
- **Critical Risk (20-25)**: 0 scenarios
- **High Risk (12-16)**: 0 scenarios
- **Medium Risk (6-10)**: 6 scenarios (40%)
- **Low Risk (3-5)**: 9 scenarios (60%)

### Risk Reduction Effectiveness
- **Average Initial Risk Score**: 9.5
- **Average Residual Risk Score**: 4.9
- **Risk Reduction**: 48% average decrease
- **All High Risks Mitigated**: 5/5 reduced to Medium or Low

### Cross-Reference Statistics
- **EQUIPMENT Types**: 15 critical infrastructure systems
- **ATTACK_PATTERNS**: 15 distinct cyber threats
- **VULNERABILITIES**: 15 security weaknesses
- **HAZARDS**: 15 safety consequences
- **MITIGATIONS**: 30 (15 initial + 15 additional)
- **ARCHITECTURES**: 30 defense architectures
- **THREAT_ACTORS**: 15 adversary profiles

### Key Findings
1. **High Consequence Systems Prioritized**: Nuclear, chemical, railway receive strongest controls
2. **Likelihood Reduction Primary Strategy**: Most treatments focus on attack prevention
3. **Defense-in-Depth Effective**: Multiple layers provide consequence reduction
4. **All Risks Acceptable Post-Treatment**: Comprehensive risk management achieved
5. **Residual Risk Monitoring Essential**: Ongoing assessment required for maintained safety
