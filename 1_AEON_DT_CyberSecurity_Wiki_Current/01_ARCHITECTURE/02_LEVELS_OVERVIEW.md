# AEON Digital Twin - 7-Level Architecture Overview

**File:** 02_LEVELS_OVERVIEW.md
**Created:** 2025-11-29 04:45:00 UTC
**Version:** 1.0.0
**Author:** AEON Architecture Team
**Purpose:** Consolidated 7-Level Knowledge Architecture reference for AEON Cyber Digital Twin
**Status:** ACTIVE - AUTHORITATIVE LEVEL REFERENCE

---

## EXECUTIVE SUMMARY

The AEON Cyber Digital Twin implements a **7-Level hierarchical knowledge architecture** (Levels 0-6) that models critical infrastructure from foundational concepts through psychohistory predictions. This architecture enables McKenney's 8 Strategic Questions (Q1-Q8) and is fully integrated with Enhancement 27 (Entity Expansion + Psychohistory).

**Total System Scale**:
- **Nodes**: 1,104,066+ (verified from Neo4j)
- **Relationships**: 11,998,401+ edges
- **CVEs**: 315,208 (72.6% EPSS enriched)
- **Sectors**: 16 CISA critical infrastructure sectors
- **Equipment**: 1,067,754 documented equipment instances

---

## LEVEL ARCHITECTURE DIAGRAM

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                    AEON 7-LEVEL KNOWLEDGE ARCHITECTURE                         │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  LEVEL 6: PREDICTIONS & PSYCHOHISTORY                   McKenney Q7-Q8        │
│  ├── Seldon Crisis Detection (3 crisis types: SC001-SC003)                    │
│  ├── Epidemic Threshold: R₀ = β/γ × λmax(A) (malware spread)                  │
│  ├── Granovetter Cascade: r(t+1) = N × F(r(t)/N)                              │
│  ├── NOW/NEXT/NEVER Triage (1.4% NOW, 18% NEXT, 80.6% NEVER)                  │
│  └── 24,409 prediction nodes                                                   │
│                                                                                 │
│  LEVEL 5: INFORMATION STREAMS                            McKenney Q5-Q6        │
│  ├── Real-time CVE feeds (NVD, VulnCheck, OSV)                                │
│  ├── EPSS scores (FIRST.org daily updates)                                    │
│  ├── Threat intelligence feeds (STIX/TAXII)                                   │
│  ├── News & RSS aggregation                                                   │
│  └── 5,547 information stream nodes                                           │
│                                                                                 │
│  LEVEL 4: PSYCHOLOGY & BEHAVIOR                          McKenney Q4           │
│  ├── 30 Cognitive Biases (via PsychTrait Super Label)                         │
│  ├── Big Five Personality Model                                               │
│  ├── Lacanian Framework (Real/Imaginary/Symbolic)                             │
│  ├── Dark Triad (Narcissism/Machiavellism/Psychopathy)                        │
│  └── Fear-Reality Gap Analysis ($7.3M misallocation)                          │
│                                                                                 │
│  LEVEL 3: THREAT INTELLIGENCE                            McKenney Q2-Q3        │
│  ├── 315,208 CVE vulnerabilities (NER11 Gold)                                 │
│  ├── 691 MITRE ATT&CK techniques (via AttackPattern Super Label)              │
│  ├── APT groups (via ThreatActor Super Label)                                 │
│  ├── Malware families (via Malware Super Label)                               │
│  └── STIX 2.1 threat intelligence integration                                 │
│                                                                                 │
│  LEVEL 2: SOFTWARE & SBOM                                McKenney Q3           │
│  ├── ~140,000 SBOM component nodes                                            │
│  ├── Library-level vulnerability tracking (Log4Shell, etc.)                   │
│  ├── SPDX & CycloneDX format support                                          │
│  ├── ~40,000 dependency relationships                                         │
│  └── Software Super Label (library/application/firmware/os)                   │
│                                                                                 │
│  LEVEL 1: CUSTOMER EQUIPMENT                             McKenney Q1           │
│  ├── 48,288 deployed equipment instances                                      │
│  ├── ~5,000 facilities across 16 CISA sectors                                 │
│  ├── Asset Super Label (IT/OT/IoT classification)                             │
│  ├── Organization ownership mapping                                           │
│  └── Location/Facility geographic data                                        │
│                                                                                 │
│  LEVEL 0: FOUNDATION CATALOG                             Ontology Base         │
│  ├── 6 Core Concepts: Infrastructure, Vulnerability, Threat, Event,          │
│  │                     Decision, Prediction                                    │
│  ├── ~6,000 equipment product catalog nodes                                   │
│  ├── 100+ major vendors (Siemens, ABB, Cisco, etc.)                          │
│  ├── Protocol specifications (Modbus, DNP3, IEC 61850)                        │
│  └── E27 Super Label taxonomy foundation                                      │
│                                                                                 │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## LEVEL 0: FOUNDATION CATALOG

### Purpose
Universal equipment product catalog providing standardized equipment types, manufacturers, product lines, and vendor intelligence serving all higher levels.

### Node Types
```cypher
(:Concept {name: "Infrastructure", level: 0})
(:Concept {name: "Vulnerability", level: 0})
(:Concept {name: "Threat", level: 0})
(:Concept {name: "Event", level: 0})
(:Concept {name: "Decision", level: 0})
(:Concept {name: "Prediction", level: 0})

(:EquipmentProduct {productId, productName, manufacturer, category})
(:ProtocolSpecification {protocolName, version, standardBody, securityFeatures})
```

### E27 Integration
- **Asset Super Label**: Equipment catalog → Asset {assetClass, deviceType}
- **Protocol Super Label**: Protocol specs → Protocol {protocolType: "ics|network|application"}

### Key Statistics
| Metric | Value |
|--------|-------|
| Equipment Products | ~6,000 |
| Vendors Tracked | 100+ |
| Protocol Standards | 20+ |
| Serves Equipment | 1,067,754 instances |

---

## LEVEL 1: CUSTOMER EQUIPMENT

### Purpose
Deployed equipment instances representing actual physical/virtual assets at customer facilities across 16 CISA critical infrastructure sectors.

### Node Types
```cypher
(:Asset {
  id: String,
  assetClass: "OT|IT|IoT",
  deviceType: "plc|rtu|scada|firewall|server|...",
  manufacturer: String,
  facilityId: String,
  sector: String
})

(:Organization {name, orgType: "utility|manufacturer|sector"})
(:Location {locationType: "facility|city|state|country"})
```

### E27 Integration
- **Asset Super Label**: Consolidates 7 OT device labels into unified taxonomy
- **Organization Super Label**: Ownership mapping (LADWP, Duke Energy, etc.)
- **Location Super Label**: Geographic facility data

### Key Statistics
| Metric | Value |
|--------|-------|
| Equipment Instances | 48,288 |
| Facilities | ~5,000 |
| CISA Sectors | 16 |
| Sector Coverage | 61.6% with relationships |

### LADWP Example
```
1,247 water pumps     → Asset {assetClass: "OT", deviceType: "pump"}
847 control valves    → Asset {assetClass: "OT", deviceType: "valve"}
432 SCADA RTUs        → Asset {assetClass: "OT", deviceType: "rtu"}
156 firewalls         → Asset {assetClass: "IT", deviceType: "firewall"}
1,247 PLCs            → Asset {assetClass: "OT", deviceType: "plc"}
```

---

## LEVEL 2: SOFTWARE & SBOM

### Purpose
Software Bill of Materials and library-level vulnerability tracking enabling deep software supply chain analysis.

### Node Types
```cypher
(:Software {
  name: String,
  version: String,
  softwareType: "library|application|firmware|operating_system",
  purl: String,  // Package URL
  ecosystem: String
})

(:Vulnerability {
  vulnType: "cve|cwe|exploit",
  cveID: String,
  cvssScore: Float,
  epssScore: Float  // FIRST.org EPSS
})
```

### E27 Integration
- **Software Super Label**: library/application/firmware/os discrimination
- **Vulnerability Super Label**: CVE/CWE/Exploit consolidation

### Key Statistics
| Metric | Value |
|--------|-------|
| CVE Vulnerabilities | 315,208 |
| SBOM Components | ~140,000 |
| Dependencies | ~40,000 |
| EPSS Coverage | 72.6% |

### Cross-Level Query Example
```cypher
// Find equipment affected by Log4Shell
MATCH (vuln:Vulnerability {cveID: "CVE-2021-44228"})
      <-[:HAS_VULNERABILITY]-(soft:Software {name: "log4j-core"})
      <-[:RUNS_SOFTWARE]-(asset:Asset)
RETURN asset.id, asset.assetClass, asset.deviceType
```

---

## LEVEL 3: THREAT INTELLIGENCE

### Purpose
Threat intelligence including APT groups, attack techniques, malware families, and vulnerability exploitation patterns.

### Node Types
```cypher
(:ThreatActor {
  name: String,
  actorType: "nation_state|apt|criminal|hacktivist|insider",
  motivations: [String],
  targetedSectors: [String]
})

(:AttackPattern {
  patternType: "technique|tactic|capec",
  mitreID: String,
  name: String
})

(:Malware {
  name: String,
  malwareFamily: "ransomware|trojan|wiper|botnet|rat|rootkit"
})
```

### E27 Integration
- **ThreatActor Super Label**: APT29, Sandworm, LockBit → unified actor model
- **AttackPattern Super Label**: 691 MITRE ATT&CK techniques
- **Malware Super Label**: Family-based classification

### Key Statistics
| Metric | Value |
|--------|-------|
| MITRE Techniques | 691 |
| MITRE Tactics | 14 |
| APT Groups | 140+ |
| Malware Families | 700+ |

---

## LEVEL 4: PSYCHOLOGY & BEHAVIOR

### Purpose
Psychological, behavioral, and personality factors affecting cybersecurity decision-making, including cognitive biases and organizational psychology.

### Node Types
```cypher
(:PsychTrait {
  traitType: "cognitive_bias|personality|lacanian",
  subtype: String,
  name: String,
  cybersecurity_impact: "HIGH|MODERATE|LOW"
})
```

### E27 Integration
- **PsychTrait Super Label**: Foundation for ALL psychological modeling
- 30 cognitive biases with inter-bias relationships
- Lacanian Real/Imaginary/Symbolic framework

### 30 Cognitive Biases Implemented
| Category | Biases |
|----------|--------|
| Perception | Availability, Confirmation, Anchoring, Framing, Contrast, Primacy, Representativeness |
| Memory | Recency, Hindsight, Peak-End |
| Decision | Optimism, Overconfidence, Loss Aversion, Status Quo, Sunk Cost |
| Social | Bandwagon, In-Group, Authority |
| Cognitive | Dunning-Kruger, Blind Spot, Complexity, Normalcy |
| Motivational | Self-Serving, Defensive Attribution |

### Key Statistics
| Metric | Value |
|--------|-------|
| Cognitive Biases | 30 |
| Inter-Bias Relationships | 18,870 |
| Personality Models | 3 (Big Five, MBTI, Dark Triad) |
| Fear-Reality Gap | $7.3M misallocation |

---

## LEVEL 5: INFORMATION STREAMS

### Purpose
Real-time intelligence feeds aggregating vulnerability disclosures, threat intelligence, news, and external data sources.

### Node Types
```cypher
(:Event {
  eventType: "incident|breach|detection|remediation",
  timestamp: DateTime,
  severity: String
})

(:Campaign {
  campaignType: "apt_campaign|ransomware_wave|botnet_recruitment",
  startDate: Date,
  attribution: String
})
```

### Data Sources
| Source | Type | Update Frequency |
|--------|------|------------------|
| NVD (NIST) | CVE data | Daily |
| FIRST.org | EPSS scores | Daily |
| VulnCheck KEV | Exploited vulns | Real-time |
| MITRE ATT&CK | Techniques | Quarterly |
| STIX/TAXII | Threat intel | Real-time |
| RSS/News | Industry news | Continuous |

### E27 Integration
- **Event Super Label**: Incident/breach/detection tracking
- **Campaign Super Label**: APT campaign correlation

### Key Statistics
| Metric | Value |
|--------|-------|
| Information Nodes | 5,547 |
| CVE Sources | 4,100+ |
| MITRE Nodes | 1,200+ |
| News Events | 147 |

---

## LEVEL 6: PREDICTIONS & PSYCHOHISTORY

### Purpose
Predictive analytics and psychohistory-based forecasting enabling Seldon Crisis detection and NOW/NEXT/NEVER vulnerability triage.

### Psychohistory Equations (5 Models)
```yaml
Epidemic_Threshold:
  equation: "R₀ = β/γ × λmax(A)"
  application: "Malware spread prediction"

Ising_Dynamics:
  equation: "dm/dt = -m + tanh(β(Jzm + h))"
  application: "Cognitive bias adoption propagation"

Granovetter_Threshold:
  equation: "r(t+1) = N × F(r(t)/N)"
  application: "Attack technique adoption cascade"

Bifurcation_Crisis:
  equation: "dx/dt = μ + x²"
  application: "Seldon Crisis detection (tipping points)"

Critical_Slowing:
  equation: "ρ(lag) → 1, σ² → ∞"
  application: "Early warning signals before crisis"
```

### Seldon Crisis Types
| Crisis ID | Name | Description |
|-----------|------|-------------|
| SC001 | Infrastructure Cascade | Critical infrastructure domino failure |
| SC002 | Cognitive Epidemic | Mass cognitive bias adoption |
| SC003 | Economic Collapse | Market/supply chain disruption |

### NOW/NEXT/NEVER Triage
| Category | % of CVEs | Action |
|----------|-----------|--------|
| NOW | 1.4% (~4,400) | Immediate patching required |
| NEXT | 18% (~56,700) | Scheduled patching within SLA |
| NEVER | 80.6% (~254,100) | Low risk, monitor only |

### Key Statistics
| Metric | Value |
|--------|-------|
| Prediction Nodes | 24,409 |
| Breach Predictions | 8,900 |
| Decision Scenarios | 524 |
| Bias Influences | 15,485 |

---

## McKENNEY'S 8 STRATEGIC QUESTIONS MAPPING

| Question | Level | Implementation |
|----------|-------|----------------|
| **Q1**: What equipment do we have? | Level 1 | Asset Super Label |
| **Q2**: Who threatens us? | Level 3 | ThreatActor Super Label |
| **Q3**: What vulnerabilities exist? | Level 2-3 | Vulnerability Super Label |
| **Q4**: How do we make decisions? | Level 4 | PsychTrait Super Label |
| **Q5**: What's happening now? | Level 5 | Event/Campaign Super Labels |
| **Q6**: What's the impact? | Level 5-6 | Economic impact calculations |
| **Q7**: What will happen? | Level 6 | Psychohistory predictions |
| **Q8**: What should we do? | Level 6 | NOW/NEXT/NEVER triage |

---

## E27 SUPER LABEL SUMMARY

Enhancement 27 consolidates 24 labels into 16 Super Labels via hierarchical properties:

| Super Label | Discriminator | Level | Subtypes |
|-------------|---------------|-------|----------|
| Asset | assetClass, deviceType | 0-1 | OT, IT, IoT + 20 device types |
| Software | softwareType | 2 | library, application, firmware, os |
| Protocol | protocolType | 0 | ics, network, application |
| Vulnerability | vulnType | 2-3 | cve, cwe, exploit, zero_day |
| ThreatActor | actorType | 3 | nation_state, apt, criminal, hacktivist, insider |
| AttackPattern | patternType | 3 | technique, tactic, capec |
| Malware | malwareFamily | 3 | ransomware, trojan, wiper, botnet, rat, rootkit |
| PsychTrait | traitType, subtype | 4 | cognitive_bias, personality, lacanian |
| Event | eventType | 5 | incident, breach, detection, remediation |
| Campaign | campaignType | 5 | apt_campaign, ransomware_wave, botnet_recruitment |
| Organization | orgType | 1 | sector, utility, manufacturer |
| Location | locationType | 1 | facility, city, state, country |
| Control | controlType | 3 | mitigation, compliance, nerc_cip |
| Indicator | indicatorType | 1-5 | measurement, energy_property, water_property |
| EconomicMetric | metricType | 5-6 | market, loss, penalty, insurance |
| Role | roleType | 4 | ot_engineer, security_analyst, executive, operator |

---

## RELATED DOCUMENTATION

- **Architecture Details**: [01_COMPREHENSIVE_ARCHITECTURE.md](01_COMPREHENSIVE_ARCHITECTURE.md)
- **E27 Level Integration**: [../08_Planned_Enhancements/Enhancement_27_Entity_Expansion_Psychohistory/audit_reports/E27_LEVEL_INTEGRATION_MAPPING.md](../08_Planned_Enhancements/Enhancement_27_Entity_Expansion_Psychohistory/audit_reports/E27_LEVEL_INTEGRATION_MAPPING.md)
- **API Documentation**: [../04_APIs/00_API_STATUS_AND_ROADMAP.md](../04_APIs/00_API_STATUS_AND_ROADMAP.md)
- **OpenSPG API**: [../04_APIs/API_OPENSPG.md](../04_APIs/API_OPENSPG.md)
- **Psychohistory API**: [../04_APIs/E27_PSYCHOHISTORY_API.md](../04_APIs/E27_PSYCHOHISTORY_API.md)

---

*Last Updated: 2025-11-29 | Status: VERIFIED FROM CODEBASE*
