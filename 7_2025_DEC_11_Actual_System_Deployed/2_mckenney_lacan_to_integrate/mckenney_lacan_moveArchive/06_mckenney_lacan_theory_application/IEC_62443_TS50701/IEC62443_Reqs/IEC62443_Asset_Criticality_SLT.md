# Asset Criticality and IEC 62443 SL-T Determination

**Author**: j.mckenney
**Document Date: October 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Critical Asset Lists Overview](#overview)
3. [Asset Registry and IEC 62443](#asset-registry)
4. [Reliability Critical Items (RCM) Integration](#rcm-integration)
5. [Safety Critical Items (SIS/SIL) Integration](#safety-integration)
6. [Criticality to SL-T Determination Framework](#sl-t-framework)
7. [Consequence Severity Assessment](#consequence-assessment)
8. [Zone Assignment Based on Criticality](#zone-assignment)
9. [Practical Implementation Guide](#implementation)
10. [Integration Workflows](#workflows)

---

## 1. Executive Summary 

**The Critical Connection**: Your organization likely already has lists of critical assets for reliability (RCM), safety (SIS/SIL), and operational purposes. These existing criticality assessments are **essential inputs** for IEC 62443 risk assessment and Security Level Target (SL-T) determination.

### Why This Matters

IEC 62443-3-2 requires determining **consequence severity** as a key factor in SL-T assignment. Your existing critical asset lists provide this information:

```
Existing Asset Criticality Lists
         ↓
   Consequence Severity Assessment
         ↓
   Threat Capability Assessment
         ↓
   Risk Level Determination
         ↓
   SL-T Assignment (1-4)
         ↓
   Zone Definition and Conduit Design
```

### Key Benefits of Integration

| Benefit | Description | Impact |
|---------|-------------|--------|
| **Accelerated Assessment** | Leverage existing criticality work | Reduces risk assessment time by 40-60% |
| **Consistent Methodology** | Aligns cyber risk with operational risk | Single source of truth for criticality |
| **Cross-Functional Buy-In** | Operations already understands critical assets | Easier stakeholder engagement |
| **Compliance Efficiency** | Single asset criticality serves multiple frameworks | Reduced duplication of effort |
| **Better Resource Allocation** | Focus cyber investment on truly critical assets | Optimized security spending |

### Three Critical Lists Explained

**1. Asset Registry (Baseline)**
- **Purpose**: Comprehensive inventory of all assets
- **IEC 62443 Use**: Foundation for zone/conduit partitioning
- **Key Attributes**: Location, function, connectivity

**2. Reliability Critical Items List (RCM)**
- **Purpose**: Assets whose failure significantly impacts operations
- **IEC 62443 Use**: Determines operational/economic consequence severity
- **Key Attributes**: Failure impact, downtime cost, production loss

**3. Safety Critical Items List (SIS/SIL)**
- **Purpose**: Assets that prevent or mitigate safety hazards
- **IEC 62443 Use**: Determines safety/environmental consequence severity
- **Key Attributes**: SIL level, safety function, hazard scenario

---

## 2. Critical Asset Lists Overview {#overview}

### 2.1 Asset Registry

**Definition**: A comprehensive, authoritative inventory of all physical and logical assets in the System under Consideration (SuC).

**Typical Sources**:
- CMDB (Configuration Management Database)
- EAM (Enterprise Asset Management) systems
- P&IDs (Process and Instrumentation Diagrams)
- Network discovery tools
- Procurement records

**Essential Attributes for IEC 62443**:

```yaml
Asset_Record:
  # Identity
  asset_id: ""
  asset_name: ""
  asset_type: ""
  
  # Function
  primary_function: ""
  business_process_supported: ""
  
  # Location
  physical_location: ""
  logical_location: ""  # Network segment
  
  # Connectivity
  network_connections: []
  protocols_used: []
  
  # Baseline Criticality
  operational_criticality: ""  # From RCM
  safety_criticality: ""       # From SIS analysis
  
  # IEC 62443 Attributes (to be determined)
  assigned_zone: ""
  sl_target: ""
  sl_capability: ""
```

### 2.2 Reliability Critical Items (RCM List)

**Definition**: Assets identified through Reliability-Centered Maintenance (RCM) analysis as having significant operational or economic consequences if they fail.

**RCM Criticality Classification** (typical):

| Criticality Level | Definition | Typical Consequence |
|-------------------|------------|---------------------|
| **Critical** | Failure causes immediate production stoppage | >$100K/hour loss or complete plant shutdown |
| **High** | Failure causes significant operational impact | $10K-$100K/hour loss or major production reduction |
| **Medium** | Failure causes moderate operational impact | $1K-$10K/hour loss or localized impact |
| **Low** | Failure has minimal operational impact | <$1K/hour loss or no production impact |

**RCM Failure Consequence Categories**:

1. **Operational Consequences**: Production loss, throughput reduction
2. **Economic Consequences**: Repair costs, lost revenue, penalties
3. **Hidden Failures**: Protective device failures (no immediate impact but increased risk)
4. **Non-Operational**: Comfort, efficiency, appearance (minimal consequence)

**Key RCM Outputs Used for IEC 62443**:

```yaml
RCM_Critical_Item:
  asset_id: ""
  failure_mode: ""
  failure_consequence_category: ""  # Operational, Economic, Hidden, Safety
  
  # Quantified Impacts
  production_loss_rate: ""          # Units/hour or $/hour
  mean_time_to_repair: ""           # Hours
  total_downtime_cost: ""           # $
  
  # Risk Ratings
  failure_probability: ""           # High/Medium/Low
  consequence_severity: ""          # Critical/High/Medium/Low
  risk_priority_number: 0           # Probability × Severity
  
  # Maintenance Strategy
  maintenance_strategy: ""          # Predictive, Preventive, Run-to-Failure
  inspection_frequency: ""
```

### 2.3 Safety Critical Items (SIS/SIL List)

**Definition**: Safety Instrumented Systems (SIS) and components that perform safety functions to prevent or mitigate hazards, classified by Safety Integrity Level (SIL).

**SIL Classification** (per IEC 61508/61511):

| SIL Level | Risk Reduction Factor | Probability of Failure on Demand (PFD) | Typical Applications |
|-----------|----------------------|----------------------------------------|---------------------|
| **SIL 4** | 10,000 to 100,000 | 0.00001 to 0.0001 | Nuclear, aerospace (rare in process industries) |
| **SIL 3** | 1,000 to 10,000 | 0.0001 to 0.001 | High-consequence process hazards |
| **SIL 2** | 100 to 1,000 | 0.001 to 0.01 | Moderate-consequence process hazards |
| **SIL 1** | 10 to 100 | 0.01 to 0.1 | Lower-consequence process hazards |

**Safety Consequence Categories**:

1. **Catastrophic**: Multiple fatalities, severe environmental damage
2. **Critical**: Single fatality or permanent disability, major environmental impact
3. **Serious**: Serious injury, significant environmental release
4. **Minor**: Minor injury, limited environmental impact

**Key SIS Outputs Used for IEC 62443**:

```yaml
SIS_Critical_Item:
  asset_id: ""
  sil_level: ""                     # 1-4
  safety_function: ""               # Description of protection provided
  
  # Hazard Information
  hazard_scenario: ""               # What hazard does this prevent
  consequence_without_sis: ""       # Catastrophic/Critical/Serious/Minor
  frequency_without_sis: ""         # Frequent/Probable/Occasional/Remote
  
  # Safety Requirements
  required_availability: ""         # 99.9%, etc.
  proof_test_interval: ""           # Months
  spurious_trip_tolerance: ""       # Acceptable false alarm rate
  
  # Certification
  certified_by: ""                  # TÜV, FM, etc.
  certification_date: ""
  recertification_required: ""      # If modifications made
```

---

## 3. Asset Registry and IEC 62443 {#asset-registry}

### 3.1 Asset Registry as Foundation

The asset registry serves as the **authoritative source** for:

1. **System Under Consideration (SuC) Definition** (IEC 62443-3-2 ZCR 1)
   - Defines boundaries and scope
   - Identifies all assets within scope
   - Documents interfaces to external systems

2. **Initial Zone Partitioning** (IEC 62443-3-2 ZCR 3)
   - Groups assets by location, function, or criticality
   - Identifies natural segmentation points
   - Documents communication requirements

3. **Conduit Identification** (IEC 62443-3-2 ZCR 3)
   - Maps communication paths between assets
   - Identifies protocols and data flows
   - Determines connectivity requirements

### 3.2 Mapping Asset Registry to IEC 62443

**Step 1: Enhance Asset Registry with IEC 62443 Attributes**

Add these fields to existing asset records:

| New Attribute | Purpose | Derived From |
|---------------|---------|--------------|
| `preliminary_zone` | Initial zone assignment | Asset location + function |
| `criticality_level` | Overall criticality | Max(RCM criticality, SIS criticality) |
| `consequence_category` | Impact category | RCM + SIS analysis |
| `availability_requirement` | Uptime needs | RCM + business requirements |
| `safety_related` | Safety system flag | SIS list membership |
| `sl_target_preliminary` | Initial SL-T estimate | Criticality-based lookup |

**Step 2: Tag Assets with Criticality Source**

```yaml
Asset_Enhanced:
  asset_id: "PLC-101"
  asset_name: "Production Line 1 PLC"
  
  # Existing attributes
  asset_type: "PLC"
  location: "Field Cabinet 1"
  
  # Criticality from RCM
  rcm_critical: true
  rcm_criticality_level: "Critical"
  rcm_consequence: "Operational"
  production_impact: "$50K/hour"
  
  # Criticality from SIS (if applicable)
  sis_critical: false
  sil_level: null
  
  # Derived IEC 62443 Attributes
  overall_criticality: "Critical"           # Max of RCM and SIS
  consequence_severity: "High"              # Maps to IEC 62443 scale
  preliminary_sl_target: 3                  # Based on criticality
  preliminary_zone: "ZONE-CTRL-PROD-01"     # Production control zone
```

### 3.3 Asset Registry Query Examples

**Query 1: All Critical Assets**
```sql
SELECT asset_id, asset_name, criticality_level, consequence_category
FROM asset_registry
WHERE rcm_critical = true OR sis_critical = true
ORDER BY consequence_severity DESC
```

**Query 2: Safety Critical Assets by SIL**
```sql
SELECT asset_id, asset_name, sil_level, safety_function
FROM asset_registry
WHERE sis_critical = true
ORDER BY sil_level DESC
```

**Query 3: Assets Requiring High SL-T**
```sql
SELECT asset_id, asset_name, preliminary_sl_target, rationale
FROM asset_registry
WHERE preliminary_sl_target >= 3
ORDER BY preliminary_sl_target DESC, criticality_level DESC
```

---

## 4. Reliability Critical Items (RCM) Integration {#rcm-integration}

### 4.1 RCM Criticality → IEC 62443 Consequence Severity

**Direct Mapping Approach**:

| RCM Criticality | RCM Failure Consequence | IEC 62443 Consequence Severity | Typical SL-T Range |
|-----------------|-------------------------|-------------------------------|-------------------|
| **Critical** | >$100K/hour, plant shutdown | **High to Severe** | SL 2-3 |
| **High** | $10K-$100K/hour, major impact | **Medium to High** | SL 2 |
| **Medium** | $1K-$10K/hour, moderate impact | **Low to Medium** | SL 1-2 |
| **Low** | <$1K/hour, minimal impact | **Low** | SL 1 |

**IEC 62443-3-2 Consequence Severity Scale**:

| Severity Level | Definition | Examples |
|----------------|------------|----------|
| **Severe** | Catastrophic safety or environmental impact OR major business disruption | Fatality, major environmental release, >$1M loss, complete plant shutdown |
| **High** | Serious safety/environmental impact OR significant business disruption | Serious injury, significant release, $100K-$1M loss, major production impact |
| **Medium** | Minor safety/environmental impact OR moderate business disruption | Minor injury, limited release, $10K-$100K loss, partial production impact |
| **Low** | Negligible safety/environmental/business impact | No injury, no release, <$10K loss, minimal impact |

### 4.2 RCM Failure Mode Analysis for Cyber Risk

**Translating RCM Failure Modes to Cyber Attack Scenarios**:

| RCM Failure Mode | Cyber Equivalent | Threat Scenario | Impact |
|------------------|------------------|-----------------|--------|
| **Equipment stops** | Controller shutdown/denial of service | Attacker crashes PLC or stops process | Production loss = RCM consequence |
| **Equipment produces off-spec product** | Setpoint manipulation | Attacker modifies recipes or setpoints | Quality loss + production loss |
| **Equipment over-speeds** | Control parameter manipulation | Attacker changes speed limits | Equipment damage + safety risk |
| **Protective device fails** | Safety interlock bypass | Attacker disables safety function | Hidden failure - elevated risk |
| **Spurious trip** | False alarm injection | Attacker triggers false shutdown | Unnecessary downtime |

**Example: Production Line PLC**

```yaml
RCM_Analysis:
  asset: "PLC-101 - Production Line 1 Controller"
  
  failure_mode_1:
    description: "PLC stops responding"
    rcm_consequence: "Immediate production stoppage"
    rcm_impact: "$75K/hour production loss"
    rcm_criticality: "Critical"
    mttr: "2-4 hours"
    
  cyber_equivalent:
    attack_scenario: "DoS attack on PLC or malware causing crash"
    cyber_consequence: "Identical to physical failure"
    cyber_impact: "$75K/hour × downtime hours"
    consequence_severity: "High"
    preliminary_sl_t: 3
    
  failure_mode_2:
    description: "PLC produces incorrect outputs"
    rcm_consequence: "Off-spec product requiring rework or scrap"
    rcm_impact: "$30K/hour + quality costs"
    rcm_criticality: "High"
    
  cyber_equivalent:
    attack_scenario: "Logic manipulation or setpoint tampering"
    cyber_consequence: "Controlled production of defective product"
    cyber_impact: "$30K/hour + brand damage (potentially higher)"
    consequence_severity: "High"
    preliminary_sl_t: 3
```

### 4.3 RCM Hidden Failures and Cyber Risk

**Critical Insight**: RCM identifies "hidden failures" - protective devices that fail silently, increasing risk.

**Cyber Implication**: If an attacker can disable protective functions without detection, they create a hidden failure state that enables subsequent attack stages.

**Example Scenario**:

```
Normal State:
  Process → Monitored by Safety PLC → Shuts down if unsafe

Hidden Failure (Cyber-Induced):
  Process → Safety PLC disabled by attacker → No protection
  
Attacker now can:
  → Cause unsafe condition (overpressure, overtemp, etc.)
  → No automatic shutdown occurs
  → Severe consequences possible
```

**Impact on SL-T**: Hidden failure assets require **elevated SL-T** to prevent attacker from creating hidden failure state.

| Asset Type | RCM Classification | Cyber Risk Consideration | SL-T Adjustment |
|------------|-------------------|--------------------------|-----------------|
| Safety PLC | Hidden failure critical | Attacker bypass enables severe consequences | +1 SL-T (e.g., SL 2 → SL 3) |
| Safety interlock | Hidden failure critical | Attacker disable removes protection layer | +1 SL-T |
| Critical alarm | Hidden failure critical | Attacker suppress prevents operator response | +0 to +1 SL-T |

---

## 5. Safety Critical Items (SIS/SIL) Integration {#safety-integration}

### 5.1 SIL Level → IEC 62443 SL-T Relationship

**Common Misconception**: SIL and SL are not equivalent, but they are related through consequence severity.

**Correct Relationship**:

```
SIL Level (Safety Integrity) → Indicates severity of hazard
                 ↓
Hazard Consequence Severity → Maps to IEC 62443 consequence scale
                 ↓
Combined with Threat Capability → Determines SL-T
```

**Recommended Mapping**:

| SIL Level | Hazard Consequence | IEC 62443 Consequence Severity | Minimum SL-T | Typical SL-T |
|-----------|-------------------|-------------------------------|--------------|--------------|
| **SIL 4** | Catastrophic (multiple fatalities) | **Severe** | 3 | **4** |
| **SIL 3** | Critical (fatality or permanent disability) | **Severe** | 2 | **3** |
| **SIL 2** | Serious (serious injury) | **High** | 2 | **2-3** |
| **SIL 1** | Minor (minor injury) | **Medium** | 1 | **2** |

**Key Principle**: Safety systems typically warrant **higher SL-T** because:
1. Consequence severity is inherently high (safety impact)
2. Attackers may specifically target safety systems to enable secondary attacks
3. Safety system compromise undermines multiple layers of protection

### 5.2 Safety Critical Asset Categories

**Category 1: Safety Instrumented Systems (SIS)**

Examples: Emergency shutdown systems, fire & gas systems, high-integrity pressure protection systems

```yaml
SIS_Asset_Type: "Safety PLC"
  typical_sil: 2-3
  consequence_if_compromised: "Severe - cannot perform safety shutdown"
  cyber_threat_scenarios:
    - "Attacker disables safety function"
    - "Attacker blocks safety activation"
    - "Attacker causes spurious trip (deny operations)"
  
  recommended_sl_t: 3-4
  rationale: |
    SIL 3 system protecting against fatality scenarios.
    Cyber compromise prevents safety function, elevating risk to unacceptable level.
    SL-T 3 provides defense against sophisticated attackers with IACS knowledge.
```

**Category 2: Basic Process Control System (BPCS) with Safety Credit**

Sometimes BPCS provides initial line of defense, with SIS as backup.

```yaml
BPCS_with_Safety_Credit:
  asset: "DCS Controller with Alarming"
  sil: "Not SIL-rated but provides operator alarming"
  safety_function: "Alerts operator to abnormal condition"
  
  consequence_if_compromised: "High - operator may not respond in time"
  cyber_threat_scenarios:
    - "Attacker suppresses alarms"
    - "Attacker floods with false alarms (alarm fatigue)"
  
  recommended_sl_t: 2-3
  rationale: |
    Not certified SIS, but performs critical alerting function.
    Compromise degrades layer of protection.
```

**Category 3: Safety Instrumented Functions (SIF) Components**

Individual sensors, logic solvers, and final elements that collectively implement safety function.

```yaml
SIF_Component:
  component_type: "Pressure Transmitter for SIS"
  part_of_sif: "High Pressure Shutdown"
  sil_contribution: "SIL 2"
  
  consequence_if_compromised: "Medium - Single point in SIF, but redundancy exists"
  cyber_threat_scenarios:
    - "Attacker spoofs sensor reading (low when actually high)"
    - "Attacker causes sensor to fail (detected, safe state)"
  
  recommended_sl_t: 2
  rationale: |
    Component of SIL 2 function. Redundancy provides some protection.
    SL-T 2 adequate for component-level protection.
```

### 5.3 IEC 61508/61511 and IEC 62443 Alignment

**Both Standards Address Risk Reduction**:

| IEC 61508/61511 (Safety) | IEC 62443 (Security) |
|--------------------------|---------------------|
| Identifies safety hazards | Identifies cyber threats |
| Assesses hazard severity and frequency | Assesses consequence severity and threat capability |
| Determines required SIL | Determines required SL-T |
| Implements safety functions to achieve SIL | Implements security controls to achieve SL-T |
| Validates through proof testing | Validates through security testing |

**Integrated Approach**: Organizations should conduct **unified risk assessment** considering both safety and security:

```
Hazard/Threat → Consequence Severity → Frequency/Capability → Risk Level → Mitigation Target (SIL and/or SL-T)
```

**Example: Overpressure Protection**

```yaml
Integrated_Risk_Assessment:
  hazard: "Reactor overpressure"
  
  safety_analysis:
    consequence_severity: "Catastrophic - explosion, multiple fatalities"
    frequency_without_protection: "Occasional (10^-3 per year)"
    required_risk_reduction: "1000x (SIL 3)"
    safety_mitigation: "Install SIL 3 pressure relief SIS"
    
  security_analysis:
    consequence_if_sis_compromised: "Severe - same as loss of safety function"
    threat_capability: "Sophisticated (competitor, disgruntled insider)"
    threat_likelihood: "Possible"
    required_security_protection: "SL-T 3"
    security_mitigation: |
      - Network segmentation (SIS isolated from BPCS)
      - Strong authentication on SIS (no shared accounts)
      - Change detection on SIS logic
      - Continuous monitoring of SIS health
  
  integrated_conclusion:
    sil: 3
    sl_t: 3
    rationale: "Both safety and security require high integrity protection"
```

---

## 6. Criticality to SL-T Determination Framework {#sl-t-framework}

### 6.1 IEC 62443-3-2 Risk Assessment Process

**Per IEC 62443-3-2 (ZCR 5)**, SL-T is determined by:

1. **Consequence Severity** (from criticality assessment)
2. **Threat Capability** (from threat assessment)
3. **Risk Tolerance** (from asset owner)

**Formula**:

```
SL-T = f(Consequence Severity, Threat Capability, Risk Tolerance)
```

### 6.2 Consequence Severity from Criticality Lists

**Integration Framework**:

```
Step 1: Identify all criticality sources for asset
  ↓
Step 2: Assess consequence in each category
  ├─ Safety consequence (from SIS list)
  ├─ Environmental consequence (from process hazard analysis)
  ├─ Financial/Operational consequence (from RCM list)
  └─ Regulatory/Legal consequence (from compliance requirements)
  ↓
Step 3: Select highest consequence severity
  ↓
Step 4: Document rationale
```

**Multi-Dimensional Consequence Assessment**:

| Asset | Safety Consequence | Environmental Consequence | Operational Consequence | Financial Consequence | Overall Consequence Severity |
|-------|-------------------|--------------------------|------------------------|----------------------|----------------------------|
| Safety PLC (SIL 3) | **Severe** (fatality possible) | High (major release) | High (plant shutdown) | High (>$1M) | **Severe** |
| Production PLC | Low (no safety function) | Low (contained) | **High** (line stoppage) | High ($75K/hour) | **High** |
| HMI Workstation | Low | Low | Medium (operator impact) | Medium ($20K/hour) | **Medium** |
| Temperature Sensor | Medium (alarm only) | Low | Low (alarming impact) | Low (<$5K/hour) | **Medium** |

### 6.3 Threat Capability Assessment

**IEC 62443 Threat Capability Levels**:

| Threat Level | Attacker Profile | Means | Resources | Skills | Motivation |
|--------------|------------------|-------|-----------|--------|------------|
| **Low** | Opportunistic, untargeted | Simple | Low | Generic IT | Low |
| **Medium** | Intentional, some planning | Simple to moderate | Limited | Basic ICS | Moderate |
| **High** | Sophisticated, targeted | Advanced | Moderate | IACS-specific | High |
| **Very High** | Nation-state, APT | Sophisticated | Extensive | Deep IACS expertise | Very high |

**Threat Capability by Industry and Asset**:

| Industry / Asset Type | Typical Threat Capability | Rationale |
|----------------------|---------------------------|-----------|
| **Critical Infrastructure** (water, power, gas) | High to Very High | Nation-state targets |
| **Chemical / Refining** (hazmat) | High | Terrorist targets, environmental impact |
| **Manufacturing** (commodity) | Medium | Competitor espionage, ransomware |
| **Manufacturing** (high-value IP) | High | Nation-state industrial espionage |
| **Safety Systems** (any industry) | +1 level | Attackers may target to enable secondary attacks |

### 6.4 SL-T Determination Matrix

**Standard Matrix** (per IEC 62443-3-2 guidance):

| Consequence Severity ↓ / Threat Capability → | Low | Medium | High | Very High |
|-----------------------------------------------|-----|--------|------|-----------|
| **Severe** | SL 2 | **SL 3** | **SL 4** | **SL 4** |
| **High** | SL 2 | **SL 2** | **SL 3** | **SL 3-4** |
| **Medium** | SL 1 | **SL 2** | **SL 2** | **SL 3** |
| **Low** | SL 1 | **SL 1** | **SL 1-2** | **SL 2** |

**Enhanced Matrix** (incorporating criticality sources):

| Asset Criticality Profile | Consequence Severity | Typical Threat | Recommended SL-T | Rationale |
|---------------------------|---------------------|----------------|------------------|-----------|
| **SIL 3-4 Safety System** | Severe | High | **SL 3-4** | Safety function loss = catastrophic |
| **SIL 1-2 Safety System** | High | High | **SL 2-3** | Safety function important but lower consequence |
| **RCM Critical Asset** (>$100K/hour) | High | Medium | **SL 2-3** | Significant financial/operational impact |
| **RCM High Asset** ($10K-$100K/hour) | Medium to High | Medium | **SL 2** | Moderate impact, standard protection |
| **RCM Medium Asset** | Medium | Medium | **SL 1-2** | Lower impact, basic protection adequate |
| **RCM Low Asset** | Low | Medium | **SL 1** | Minimal impact, minimal protection |
| **Non-Critical Asset** | Low | Low | **SL 0-1** | No special requirements |

### 6.5 Criticality-Based SL-T Assignment Worksheet

**Template for Each Asset**:

```markdown
# SL-T Determination Worksheet

**Asset**: [Asset ID and Name]

## Step 1: Criticality Assessment

### RCM Criticality
- [ ] Critical (>$100K/hour impact)
- [ ] High ($10K-$100K/hour)
- [ ] Medium ($1K-$10K/hour)
- [ ] Low (<$1K/hour)
- [ ] Not on RCM list

**RCM Impact**: $______/hour
**RCM Consequence Category**: ☐ Operational ☐ Economic ☐ Hidden ☐ Safety

### SIS Criticality
- [ ] SIL 4
- [ ] SIL 3
- [ ] SIL 2
- [ ] SIL 1
- [ ] Not safety-related

**Safety Function**: ________________
**Hazard if Compromised**: ________________

### Other Criticality
- [ ] Environmental consequence: ____________
- [ ] Regulatory consequence: ____________
- [ ] Reputational consequence: ____________

## Step 2: Consequence Severity Determination

Based on highest consequence from above:
- [ ] **Severe** - Catastrophic safety/environmental OR >$1M OR complete shutdown
- [ ] **High** - Serious safety/environmental OR $100K-$1M OR major impact
- [ ] **Medium** - Minor safety/environmental OR $10K-$100K OR moderate impact
- [ ] **Low** - Negligible impact

**Selected Consequence Severity**: __________

**Justification**: 
_______________________________________________________

## Step 3: Threat Capability Assessment

Industry: _______________
Asset Type: _______________
External Connectivity: ☐ Yes ☐ No

Assessed Threat Capability:
- [ ] **Very High** - Nation-state, critical infrastructure
- [ ] **High** - Sophisticated attacker, targeted attack likely
- [ ] **Medium** - Intentional attacker, moderate capability
- [ ] **Low** - Opportunistic, low capability

**Selected Threat Capability**: __________

**Threat Scenarios of Concern**:
1. _______________________________________________________
2. _______________________________________________________

## Step 4: SL-T Determination

Using matrix (Consequence Severity × Threat Capability):

**Recommended SL-T**: _______

**Adjustments**:
- [ ] +1 for safety system (enables secondary attacks)
- [ ] +1 for critical infrastructure sector
- [ ] -1 for air-gapped system with strong physical security
- [ ] Other: _______________

**Final SL-T**: _______

## Step 5: Approval

**Risk Owner**: _______________
**Security Reviewer**: _______________
**Date**: _______________
**Approved**: ☐ Yes ☐ No

**Notes/Conditions**: 
_______________________________________________________
```

---

## 7. Consequence Severity Assessment {#consequence-assessment}

### 7.1 Four Consequence Categories (IEC 62443-3-2)

**1. Health, Safety, and Environment (HSE)**

| Severity Level | Safety Impact | Environmental Impact | Examples |
|----------------|---------------|---------------------|----------|
| **Severe** | Death or multiple serious injuries | Major environmental release, long-term damage | Explosion, toxic release, major spill |
| **High** | Serious injury or single fatality | Significant release requiring cleanup | Fire, moderate chemical release |
| **Medium** | Minor injury requiring medical treatment | Limited release, short-term impact | Minor burn, small leak |
| **Low** | First aid only | Negligible environmental impact | Near-miss, contained minor incident |

**Source for Assessment**: 
- Safety critical items list (SIS/SIL)
- Process Hazard Analysis (PHA, HAZOP)
- Environmental risk assessments
- Historical incident data

**2. Financial and Economic**

| Severity Level | Financial Impact | Operational Impact | Business Continuity |
|----------------|------------------|-------------------|---------------------|
| **Severe** | >$10M or >10% annual revenue | Complete business cessation | Business viability threatened |
| **High** | $1M-$10M or 1-10% revenue | Major operational disruption | Significant customer impact |
| **Medium** | $100K-$1M or 0.1-1% revenue | Moderate disruption | Some customer impact |
| **Low** | <$100K or <0.1% revenue | Minimal disruption | No customer impact |

**Source for Assessment**:
- RCM critical items list
- Business impact analysis (BIA)
- Financial data (production rates, margins)
- Customer contract penalties

**3. Regulatory and Legal**

| Severity Level | Regulatory Consequence | Legal Exposure | Compliance Status |
|----------------|----------------------|----------------|-------------------|
| **Severe** | Major penalties, license revocation | Class action, criminal charges | Complete non-compliance |
| **High** | Significant fines, mandatory remediation | Civil lawsuits likely | Serious violations |
| **Medium** | Moderate fines, corrective actions | Possible civil action | Minor violations |
| **Low** | Warning notice, no fines | Unlikely legal action | Technical non-compliance |

**Source for Assessment**:
- Regulatory requirements list
- Legal/compliance department
- Industry regulations (NERC CIP, CFATS, etc.)
- Previous enforcement actions

**4. Reputational and Public Perception**

| Severity Level | Brand Impact | Media Attention | Customer Trust |
|----------------|--------------|-----------------|----------------|
| **Severe** | Permanent brand damage | National/international headlines | Mass customer defection |
| **High** | Significant brand damage | Regional media coverage | Significant customer concerns |
| **Medium** | Moderate brand impact | Local media coverage | Some customer questions |
| **Low** | Minimal brand impact | No media coverage | No customer impact |

**Source for Assessment**:
- Marketing/communications department
- Customer sensitivity analysis
- Historical crisis response data

### 7.2 Consequence Severity Calculation Methodology

**Approach 1: Maximum Consequence Method** (Conservative)

```
Consequence Severity = MAX(HSE Severity, Financial Severity, Regulatory Severity, Reputational Severity)
```

**Example**:
- HSE: High (serious injury possible)
- Financial: Medium ($500K/event)
- Regulatory: Low (warning likely)
- Reputational: Medium (local media)

**Result**: Consequence Severity = **High** (from HSE)

**Approach 2: Weighted Consequence Method** (Sophisticated)

Assign weights based on organizational priorities:

```
Consequence Severity = (W_HSE × HSE_Severity) + 
                       (W_Financial × Financial_Severity) + 
                       (W_Regulatory × Regulatory_Severity) + 
                       (W_Reputational × Reputational_Severity)

Where: W_HSE + W_Financial + W_Regulatory + W_Reputational = 1.0
```

**Example Weights** (Safety-focused organization):
- W_HSE = 0.50 (highest priority)
- W_Financial = 0.30
- W_Regulatory = 0.15
- W_Reputational = 0.05

**Severity Score Scale**:
- Severe = 4
- High = 3
- Medium = 2
- Low = 1

**Calculation**:
```
= (0.50 × 3) + (0.30 × 2) + (0.15 × 1) + (0.05 × 2)
= 1.5 + 0.6 + 0.15 + 0.1
= 2.35 (rounds to 2 = Medium, or threshold-based to 3 = High)
```

### 7.3 Consequence Severity Matrix Template

**Asset-Level Consequence Assessment**:

| Asset ID | Asset Name | HSE Severity | Financial Severity | Regulatory Severity | Reputational Severity | Overall Severity | Source |
|----------|------------|--------------|-------------------|--------------------|--------------------|------------------|--------|
| PLC-101 | Prod Line 1 PLC | Low | **High** ($75K/hr) | Low | Medium | **High** | RCM List |
| SIS-201 | ESD System | **Severe** (SIL 3) | High | High | High | **Severe** | SIS List |
| HMI-301 | Operator Station | Low | Medium ($20K/hr) | Low | Low | **Medium** | RCM List |
| FW-401 | Perimeter Firewall | Medium | High (entire plant) | Medium | High | **High** | Critical Infrastructure |

---

## 8. Zone Assignment Based on Criticality {#zone-assignment}

### 8.1 Criticality-Based Zone Strategy

**Principle**: Assets with similar criticality and security requirements should be grouped in the same zone.

**Zone Design Approach**:

```
Step 1: Classify assets by criticality
  ├─ Safety Critical (SIS)
  ├─ Reliability Critical (RCM)
  ├─ Business Critical
  └─ Non-Critical

Step 2: Consider operational grouping
  ├─ Production lines
  ├─ Utility systems
  ├─ Safety systems
  └─ Support systems

Step 3: Apply network/physical constraints
  ├─ Physical location
  ├─ Network segments
  └─ Existing architecture

Step 4: Assign preliminary zones
  Each zone contains assets with:
  ├─ Similar criticality level
  ├─ Similar SL-T requirements
  ├─ Similar operational function
  └─ Practical communication needs
```

### 8.2 Standard Zone Types by Criticality

| Zone Type | Typical Asset Criticality | Typical SL-T | Examples |
|-----------|--------------------------|--------------|----------|
| **Safety Systems Zone** | SIL 2-4 assets | SL 3-4 | ESD, F&G, HIPPS, SIS controllers |
| **Critical Production Zone** | RCM Critical | SL 2-3 | Primary production PLCs, critical DCS |
| **Production Zone** | RCM High | SL 2 | Standard production controllers, HMIs |
| **Support Systems Zone** | RCM Medium | SL 1-2 | Utility systems, non-critical monitoring |
| **Supervisory Zone** | RCM High (control & visibility) | SL 2-3 | SCADA, historians, engineering stations |
| **Industrial DMZ** | Critical data exchange | SL 2 | Data historians, application servers, gateways |
| **Field Devices Zone** | RCM Low-Medium | SL 1-2 | Sensors, actuators, field instrumentation |

### 8.3 Zone Assignment Decision Tree

```
For each asset:

Q1: Is asset safety-critical (on SIS list)?
    YES → Assign to SAFETY SYSTEMS ZONE (SL-T 3-4)
    NO → Continue to Q2

Q2: Is asset RCM Critical (>$100K/hour impact)?
    YES → Continue to Q3
    NO → Continue to Q4

Q3: Is asset a controller or has control authority?
    YES → Assign to CRITICAL PRODUCTION ZONE (SL-T 2-3)
    NO → Assign to CRITICAL SUPPORT ZONE (SL-T 2)

Q4: Is asset RCM High ($10K-$100K/hour impact)?
    YES → Assign to PRODUCTION ZONE (SL-T 2)
    NO → Continue to Q5

Q5: Does asset provide supervisory functions (HMI, SCADA, engineering)?
    YES → Assign to SUPERVISORY ZONE (SL-T 2)
    NO → Continue to Q6

Q6: Is asset a field device (sensor/actuator)?
    YES → Assign to FIELD DEVICES ZONE (SL-T 1-2)
    NO → Assign to SUPPORT SYSTEMS ZONE (SL-T 1)
```

### 8.4 Example Zone Assignment

**Facility**: Chemical Processing Plant

**Asset Criticality Summary**:
- 5 SIL 3 safety controllers
- 12 RCM Critical PLCs (production)
- 30 RCM High devices (production support)
- 50 RCM Medium/Low devices
- 3 SCADA servers
- 10 HMI workstations
- 200 field instruments

**Proposed Zones**:

```yaml
Zone_1_Safety_Systems:
  zone_id: "ZONE-SAFETY-01"
  sl_t: 4
  assets: 5 (all SIL 3 controllers)
  rationale: "Isolated safety systems, highest protection required"
  
Zone_2_Critical_Production:
  zone_id: "ZONE-CTRL-CRITICAL-01"
  sl_t: 3
  assets: 12 (RCM Critical PLCs)
  rationale: "Critical production controllers, >$100K/hour impact"
  
Zone_3_Production:
  zone_id: "ZONE-CTRL-PROD-01"
  sl_t: 2
  assets: 30 (RCM High devices)
  rationale: "Standard production equipment, $10K-$100K/hour impact"
  
Zone_4_Supervisory:
  zone_id: "ZONE-SCADA-01"
  sl_t: 2
  assets: 13 (3 SCADA servers + 10 HMIs)
  rationale: "Control and visibility over multiple production zones"
  
Zone_5_Industrial_DMZ:
  zone_id: "ZONE-DMZ-01"
  sl_t: 2
  assets: 5 (data historians, app servers)
  rationale: "Data exchange between OT and IT"
  
Zone_6_Field_Devices:
  zone_id: "ZONE-FIELD-01"
  sl_t: 1
  assets: 200 (field instruments)
  rationale: "Sensors and actuators, lower individual impact"
  
Zone_7_Support:
  zone_id: "ZONE-SUPPORT-01"
  sl_t: 1
  assets: 50 (RCM Medium/Low)
  rationale: "Non-critical support systems, minimal impact"
```

### 8.5 Zone-to-Asset Mapping Table

| Zone ID | Zone Name | SL-T | Asset Count | Criticality Profile | Key Assets |
|---------|-----------|------|-------------|-------------------|------------|
| ZONE-SAFETY-01 | Safety Systems | 4 | 5 | All SIL 3 | SIS-201 through SIS-205 |
| ZONE-CTRL-CRITICAL-01 | Critical Production Control | 3 | 12 | All RCM Critical | PLC-101 through PLC-112 |
| ZONE-CTRL-PROD-01 | Production Control | 2 | 30 | All RCM High | PLC-201 through PLC-230 |
| ZONE-SCADA-01 | Supervisory Control | 2 | 13 | RCM High (visibility/control) | SCADA-01, HMI-01 through HMI-10 |
| ZONE-DMZ-01 | Industrial DMZ | 2 | 5 | Critical data paths | HIST-01, APP-01, OPC-GW-01 |
| ZONE-FIELD-01 | Field Devices | 1 | 200 | RCM Low-Medium | Sensors, actuators |
| ZONE-SUPPORT-01 | Support Systems | 1 | 50 | RCM Medium/Low | Utility systems, monitoring |

---

## 9. Practical Implementation Guide {#implementation}

### 9.1 Step-by-Step Integration Process

**Phase 1: Inventory and Assessment (Weeks 1-4)**

**Week 1-2: Collect Existing Lists**
1. Obtain asset registry from IT/OT
2. Obtain RCM critical items list from reliability team
3. Obtain SIS/SIL critical items list from safety team
4. Obtain any other criticality assessments (business continuity, etc.)

**Week 3-4: Consolidate and Enhance**
5. Merge lists into single master asset list
6. Add missing IEC 62443 attributes
7. Flag discrepancies for resolution
8. Validate completeness with stakeholders

**Phase 2: Criticality Analysis (Weeks 5-8)**

**Week 5: Consequence Severity Assessment**
9. For each asset, assess consequence in all four categories (HSE, Financial, Regulatory, Reputational)
10. Use criticality lists as primary input
11. Document rationale
12. Obtain stakeholder agreement

**Week 6: Threat Capability Assessment**
13. Assess overall threat environment
14. Consider industry sector, geographic location, recent threats
15. Assign threat capability level
16. Document threat scenarios of concern

**Week 7-8: SL-T Determination**
17. Apply SL-T determination matrix
18. Document SL-T for each asset (preliminary)
19. Group assets by SL-T for zone design
20. Review and validate with risk owners

**Phase 3: Zone and Conduit Design (Weeks 9-12)**

**Week 9-10: Zone Partitioning**
21. Group assets by criticality and SL-T
22. Consider operational/physical constraints
23. Define preliminary zones
24. Document zone specifications

**Week 11: Conduit Identification**
25. Map communication paths between zones
26. Identify protocols and data flows
27. Assign SL-T to conduits (max of connected zones)
28. Document conduit specifications

**Week 12: Validation and Approval**
29. Review zone/conduit design with stakeholders
30. Validate against operational requirements
31. Obtain asset owner approval
32. Document final ZCR

### 9.2 Stakeholder Engagement Strategy

**Key Stakeholders and Their Inputs**:

| Stakeholder | Critical Input | Engagement Method |
|-------------|----------------|-------------------|
| **Reliability/Maintenance Team** | RCM list, failure impacts, MTTR | Workshop to review RCM criticality and translate to cyber consequence |
| **Safety Team** | SIS list, SIL levels, hazard scenarios | Workshop to understand safety functions and cyber attack implications |
| **Operations** | Production priorities, business impact | Interview to quantify downtime costs and operational dependencies |
| **IT/OT Engineering** | Network architecture, connectivity | Technical review of existing architecture and feasibility |
| **Finance** | Financial impact data, budget | Data provision and ROI discussion |
| **Risk Management** | Risk tolerance, risk acceptance authority | Risk workshop to align on SL-T selections |
| **Executive Leadership** | Strategic priorities, final approval | Presentation of risk assessment results and SL-T recommendations |

**Workshop Template: Criticality to SL-T Translation**

```
Duration: 4 hours
Participants: Reliability, Safety, Operations, Security, Engineering

Agenda:
1. Overview of IEC 62443 and SL-T concept (30 min)
2. Review of existing criticality lists (60 min)
   - Present RCM critical items
   - Present SIS critical items
   - Discuss any gaps or updates needed
3. Consequence severity assessment exercise (90 min)
   - For top 20 critical assets
   - Assess consequence in each category
   - Document rationale
   - BREAK (15 min)
4. Threat capability discussion (30 min)
   - Industry threat landscape
   - Specific threats of concern
   - Agree on threat capability level
5. SL-T determination exercise (45 min)
   - Apply matrix to top 20 assets
   - Discuss any disagreements
   - Document preliminary SL-T assignments
6. Next steps and action items (15 min)

Output: 
- Validated consequence severity for critical assets
- Agreed threat capability assessment
- Preliminary SL-T assignments for review
```

### 9.3 Data Management and Tooling

**Option 1: Spreadsheet-Based** (Small-Medium Facilities)

```
Master_Asset_Criticality_Register.xlsx
  Tabs:
  - Asset_Registry (all assets)
  - RCM_Critical_Items
  - SIS_Critical_Items
  - Consequence_Severity_Assessment
  - SL-T_Determination
  - Zone_Assignment
  - Conduit_Mapping
```

**Option 2: Database-Based** (Large Facilities)

```sql
-- Tables:
assets (asset_id, asset_name, type, location, ...)
rcm_criticality (asset_id, criticality_level, impact, ...)
sis_criticality (asset_id, sil_level, safety_function, ...)
consequence_assessment (asset_id, hse_severity, financial_severity, ...)
sl_t_determination (asset_id, consequence_severity, threat_capability, sl_t, ...)
zones (zone_id, zone_name, sl_t, ...)
zone_assets (zone_id, asset_id)
conduits (conduit_id, zone_a_id, zone_b_id, sl_t, ...)
```

**Option 3: GRC Platform Integration** (Enterprise)

Integrate with existing GRC tools:
- RSA Archer
- ServiceNow GRC
- MetricStream
- LogicGate
- Resolver

**Benefits**:
- Centralized asset and risk data
- Automated workflows
- Dashboards and reporting
- Audit trail
- Integration with other compliance frameworks

### 9.4 Quality Assurance Checklist

**Before Finalizing SL-T Assignments**:

- [ ] All assets in scope have been assessed
- [ ] RCM critical items all have SL-T assigned
- [ ] SIS critical items all have SL-T assigned
- [ ] Consequence severity rationale documented for all high/severe assets
- [ ] Threat capability assessment documented and validated
- [ ] SL-T assignments reviewed by cross-functional team
- [ ] Outliers (unexpected high or low SL-T) investigated and justified
- [ ] Zone assignments align with SL-T
- [ ] Conduit SL-T >= max of connected zones
- [ ] Asset owners have reviewed and approved SL-T for their areas
- [ ] Documentation complete and ready for audit

---

## 10. Integration Workflows {#workflows}

### 10.1 Complete Integration Workflow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│ EXISTING CRITICAL ASSET LISTS                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Asset        │  │ RCM Critical │  │ SIS Critical │        │
│  │ Registry     │  │ Items List   │  │ Items List   │        │
│  │              │  │              │  │ (SIL 1-4)    │        │
│  │ • All assets │  │ • $/hour     │  │              │        │
│  │ • Location   │  │ • MTTR       │  │ • Safety     │        │
│  │ • Function   │  │ • Criticality│  │   function   │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ CONSOLIDATION & ENHANCEMENT                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Enhanced Asset Register                               │    │
│  │                                                        │    │
│  │ For each asset:                                        │    │
│  │  • Asset ID, Name, Type, Location                      │    │
│  │  • RCM Criticality (if applicable)                     │    │
│  │  • SIS Criticality (if applicable)                     │    │
│  │  • Overall Criticality = Max(RCM, SIS, Other)          │    │
│  │  • Placeholder for IEC 62443 attributes                │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ CONSEQUENCE SEVERITY ASSESSMENT                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  For each asset, assess consequence if compromised:            │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ HSE          │  │ Financial    │  │ Regulatory/  │       │
│  │ Consequence  │  │ Consequence  │  │ Reputational │       │
│  │              │  │              │  │ Consequence  │       │
│  │ (from SIS)   │  │ (from RCM)   │  │              │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                  │                  │                │
│         └──────────────────┴──────────────────┘               │
│                            ↓                                   │
│              ┌─────────────────────────────┐                  │
│              │ Overall Consequence Severity │                  │
│              │  • Severe                    │                  │
│              │  • High                      │                  │
│              │  • Medium                    │                  │
│              │  • Low                       │                  │
│              └─────────────┬───────────────┘                  │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ THREAT CAPABILITY ASSESSMENT                                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Consider:                                                     │
│  • Industry sector (critical infrastructure?)                  │
│  • Geographic location                                         │
│  • Recent threat intelligence                                  │
│  • Regulatory environment                                      │
│  • Asset attractiveness to attackers                           │
│                                                                │
│              ┌─────────────────────────────┐                  │
│              │ Threat Capability Level     │                  │
│              │  • Very High (nation-state) │                  │
│              │  • High (sophisticated)     │                  │
│              │  • Medium (intentional)     │                  │
│              │  • Low (opportunistic)      │                  │
│              └─────────────┬───────────────┘                  │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ SL-T DETERMINATION (IEC 62443-3-2)                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Apply Matrix:                                                 │
│                                                                │
│  Consequence Severity × Threat Capability → SL-T               │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ SL-T Assignment Matrix                                │    │
│  │                                                        │    │
│  │   Consequence  │  Low  │ Medium │  High  │ Very High │    │
│  │   ────────────────────────────────────────────────── │    │
│  │   Severe       │  SL2  │  SL3   │  SL4   │   SL4     │    │
│  │   High         │  SL2  │  SL2   │  SL3   │   SL3-4   │    │
│  │   Medium       │  SL1  │  SL2   │  SL2   │   SL3     │    │
│  │   Low          │  SL1  │  SL1   │  SL1-2 │   SL2     │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                   │
│              ┌─────────────────────────────┐                  │
│              │ SL-T Assigned to Each Asset │                  │
│              └─────────────┬───────────────┘                  │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ ZONE AND CONDUIT DESIGN (IEC 62443-3-2 ZCR 3)                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Group assets by:                                              │
│  • Similar SL-T requirements                                   │
│  • Similar operational function                                │
│  • Communication needs                                         │
│  • Physical/logical location                                   │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Safety Zone  │  │ Production   │  │ Support Zone │       │
│  │              │  │ Zone         │  │              │       │
│  │ • SIL 2-4    │  │              │  │ • RCM Low-   │       │
│  │   assets     │  │ • RCM Crit/  │  │   Medium     │       │
│  │ • SL-T 3-4   │  │   High assets│  │ • SL-T 1-2   │       │
│  │              │  │ • SL-T 2-3   │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                │
│  Define Conduits between zones:                                │
│  • Conduit SL-T = Max(Zone A SL-T, Zone B SL-T)               │
│  • Document protocols, data flows, security controls            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ FINAL OUTPUTS                                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ✅ Zone Definitions with SL-T                                │
│  ✅ Conduit Definitions with SL-T                             │
│  ✅ Asset-to-Zone Mapping                                     │
│  ✅ Cybersecurity Requirements Specification (CRS)            │
│  ✅ Risk Assessment Documentation                             │
│  ✅ Zone/Conduit Diagrams                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 10.2 Example: Complete Integration for Sample Facility

**Scenario**: Manufacturing Plant with 100 Assets

**Step 1: Collect Existing Lists**

```
Asset Registry: 100 assets total
  - 60 production assets
  - 20 safety-related assets
  - 20 support assets

RCM Critical Items List: 25 assets
  - 5 Critical (>$100K/hour)
  - 10 High ($10K-$100K/hour)
  - 10 Medium ($1K-$10K/hour)

SIS Critical Items List: 8 assets
  - 2 SIL 3 (reactor safety system)
  - 4 SIL 2 (emergency shutdown systems)
  - 2 SIL 1 (fire & gas system)
```

**Step 2: Enhance Asset Registry**

| Asset ID | Asset Name | RCM? | RCM Level | SIS? | SIL | Overall Criticality |
|----------|------------|------|-----------|------|-----|---------------------|
| PLC-001 | Reactor Control PLC | Yes | Critical | No | - | **Critical** |
| SIS-001 | Reactor Safety PLC | No | - | Yes | SIL 3 | **Critical** |
| PLC-002 | Packaging PLC | Yes | High | No | - | **High** |
| HMI-001 | Control Room HMI | Yes | High | No | - | **High** |
| SENSOR-001 | Temperature Sensor | No | - | No | - | Low |
| ... | ... | ... | ... | ... | ... | ... |

**Step 3: Assess Consequence Severity**

| Asset ID | HSE Severity | Financial Severity | Overall Consequence | Source |
|----------|--------------|-------------------|---------------------|--------|
| PLC-001 | Medium (alarming) | **High** ($125K/hr) | **High** | RCM |
| SIS-001 | **Severe** (explosion risk) | High | **Severe** | SIS SIL 3 |
| PLC-002 | Low | Medium ($35K/hr) | **Medium** | RCM |
| HMI-001 | Low | Medium ($40K/hr blind ops) | **Medium** | RCM |
| SENSOR-001 | Low | Low (<$5K/hr) | **Low** | Default |

**Step 4: Assess Threat Capability**

```
Industry: Chemical Manufacturing
Location: North America
Recent Threats: Ransomware, nation-state interest in chemical sector
Assessment: HIGH threat capability
```

**Step 5: Determine SL-T**

| Asset ID | Consequence Severity | Threat Capability | SL-T | Rationale |
|----------|---------------------|-------------------|------|-----------|
| PLC-001 | High | High | **3** | Critical production asset, high financial impact |
| SIS-001 | Severe | High | **4** | SIL 3 safety system, severe consequences if compromised |
| PLC-002 | Medium | High | **2** | Moderate impact, standard protection adequate |
| HMI-001 | Medium | High | **2** | Supervisory visibility, moderate impact |
| SENSOR-001 | Low | High | **1-2** | Low impact, basic protection |

**Step 6: Design Zones**

```yaml
Zones_Designed:
  - zone_id: "ZONE-SAFETY-01"
    sl_t: 4
    assets: [SIS-001, SIS-002]
    count: 2
    rationale: "SIL 3 safety systems, isolated zone"
    
  - zone_id: "ZONE-CTRL-CRITICAL-01"
    sl_t: 3
    assets: [PLC-001, PLC-003, PLC-005]
    count: 5 (5 critical RCM PLCs)
    rationale: "Critical production controllers"
    
  - zone_id: "ZONE-CTRL-PROD-01"
    sl_t: 2
    assets: [PLC-002, PLC-004, ...]
    count: 10 (10 high RCM PLCs)
    rationale: "Standard production equipment"
    
  - zone_id: "ZONE-SCADA-01"
    sl_t: 2
    assets: [HMI-001, SCADA-01, ...]
    count: 8 (HMIs and SCADA)
    rationale: "Supervisory control and visibility"
    
  - zone_id: "ZONE-FIELD-01"
    sl_t: 1
    assets: [SENSOR-001, ...]
    count: 60 (field instruments)
    rationale: "Field devices, lower impact"
    
  - zone_id: "ZONE-SUPPORT-01"
    sl_t: 1
    assets: [...]
    count: 15 (support systems)
    rationale: "Non-critical support"
```

**Step 7: Define Conduits**

```yaml
Conduits:
  - conduit_id: "C-01"
    name: "Safety to Critical Production"
    zone_a: "ZONE-SAFETY-01"
    zone_b: "ZONE-CTRL-CRITICAL-01"
    sl_t: 4  # Max(4, 3) = 4
    protocol: "Proprietary SIS protocol"
    unidirectional: true
    security: "Data diode enforced"
    
  - conduit_id: "C-02"
    name: "Critical Production to SCADA"
    zone_a: "ZONE-CTRL-CRITICAL-01"
    zone_b: "ZONE-SCADA-01"
    sl_t: 3  # Max(3, 2) = 3
    protocol: "OPC UA"
    bidirectional: true
    security: "Firewall + deep packet inspection"
    
  - conduit_id: "C-03"
    name: "Production to Field Devices"
    zone_a: "ZONE-CTRL-PROD-01"
    zone_b: "ZONE-FIELD-01"
    sl_t: 2  # Max(2, 1) = 2
    protocol: "Modbus TCP, EtherNet/IP"
    bidirectional: true
    security: "Firewall + protocol filtering"
```

---

## Conclusion

**Key Takeaways**:

1. **Leverage Existing Work**: Your RCM and SIS critical items lists are **essential inputs** for IEC 62443 risk assessment, not separate efforts.

2. **Direct Mapping**: RCM criticality maps to operational/economic consequence; SIS/SIL criticality maps to safety/environmental consequence.

3. **Consequence Drives SL-T**: The higher the criticality of an asset, the higher the consequence severity, and typically the higher the required SL-T.

4. **Zone Design Follows Criticality**: Critical assets belong in zones with higher SL-T; less critical assets in zones with lower SL-T.

5. **Integration Saves Time**: Using existing criticality assessments can reduce IEC 62443 risk assessment effort by 40-60% while improving quality.

6. **Cross-Functional Collaboration**: Reliability, safety, operations, and cybersecurity teams must work together for effective integration.

**Benefits Realized**:
- ✅ Faster risk assessment (weeks instead of months)
- ✅ Better stakeholder buy-in (familiar concepts)
- ✅ More accurate consequence assessments (leverages domain expertise)
- ✅ Optimized security investment (protection proportional to criticality)
- ✅ Single source of truth for asset criticality
- ✅ Reduced duplication across compliance frameworks

**Next Steps**:
1. Collect your organization's RCM and SIS critical items lists
2. Consolidate into enhanced asset registry
3. Follow the integration framework in this guide
4. Engage cross-functional team in consequence assessment
5. Apply SL-T determination methodology
6. Design zones based on criticality groupings
7. Document and obtain approval

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**For Implementation Support**: Contact IEC 62443 consultant or ISAGCA resources

