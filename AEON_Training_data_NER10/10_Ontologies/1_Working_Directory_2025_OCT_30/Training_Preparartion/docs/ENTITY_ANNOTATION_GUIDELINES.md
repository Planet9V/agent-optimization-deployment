# Entity Annotation Guidelines
**Version:** 6.0.0
**Created:** 2025-11-06
**Purpose:** Comprehensive decision trees for resolving annotation ambiguities
**Scope:** ICS/OT security domain NER annotations

## Overview

These guidelines provide systematic decision-making frameworks for ambiguous entity classification cases. Use these decision trees when annotating or disambiguating entities to ensure consistency and accuracy.

---

## Table of Contents

1. [VENDOR vs EQUIPMENT](#vendor-vs-equipment)
2. [PROTOCOL vs EQUIPMENT](#protocol-vs-equipment)
3. [SECURITY vs MITIGATION](#security-vs-mitigation)
4. [Boundary Rules](#boundary-rules)
5. [Multi-Entity Contexts](#multi-entity-contexts)
6. [Edge Cases](#edge-cases)

---

## VENDOR vs EQUIPMENT

### Primary Decision Tree

```
┌─────────────────────────────────────────────┐
│ Is the mention a standalone company name?  │
│ (no product model/type suffix)             │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴───────┐
      │ YES           │ NO
      │               │
      ▼               ▼
  ┌────────┐    ┌─────────────────────────────┐
  │ VENDOR │    │ Does it include product     │
  └────────┘    │ model/type?                  │
                │ (S7-1500, PLC, HMI, etc.)   │
                └───────┬──────────────────────┘
                        │
                ┌───────┴───────┐
                │ YES           │ NO
                │               │
                ▼               ▼
           ┌───────────┐   ┌──────────────────┐
           │ EQUIPMENT │   │ Check Context    │
           └───────────┘   │ (see below)      │
                           └──────────────────┘
```

### Context-Based Decision

**When syntax is ambiguous (e.g., "Siemens" could be either), check surrounding context:**

#### VENDOR Indicators (Strong Signals)

**Attribution Phrases:**
- "manufactured by [ENTITY]"
- "produced by [ENTITY]"
- "developed by [ENTITY]"
- "[ENTITY]'s product"
- "from [ENTITY]"
- "[ENTITY] supplies/provides"

**Corporate Context:**
- Near company headquarters/locations
- In supplier/vendor lists
- With corporate suffixes (Inc, LLC, GmbH, Ltd)
- In contract/procurement contexts

**Example:**
```
"The SCADA system was manufactured by Siemens in Germany."
                                      ^^^^^^^ VENDOR
Context: "manufactured by" = strong VENDOR indicator
```

#### EQUIPMENT Indicators (Strong Signals)

**Technical Context:**
- "[ENTITY] device/controller/system"
- "configure/program [ENTITY]"
- "[ENTITY] firmware/software"
- "[ENTITY] running version X"
- "[ENTITY] specifications/features"

**Operational Context:**
- In equipment lists/inventories
- With technical specifications
- In operational procedures
- With installation/configuration instructions

**Example:**
```
"The Siemens S7-1500 PLC controls the assembly line."
    ^^^^^^^^^^^^^^^^^^^^ EQUIPMENT
Context: Product model + "PLC" suffix = strong EQUIPMENT indicator
```

### Syntactic Patterns

#### VENDOR Patterns
| Pattern | Example | Classification |
|---------|---------|----------------|
| Standalone company name | "Siemens" | VENDOR |
| Company + legal suffix | "Rockwell Automation LLC" | VENDOR |
| Company in possessive | "Schneider's products" | VENDOR |
| Company as manufacturer | "made by Allen-Bradley" | VENDOR |

#### EQUIPMENT Patterns
| Pattern | Example | Classification |
|---------|---------|----------------|
| Company + Model | "Siemens S7-1500" | EQUIPMENT |
| Company + Device Type | "Allen-Bradley PLC" | EQUIPMENT |
| Brand + Product | "FactoryTalk View" | EQUIPMENT |
| Product + Version | "TIA Portal v16" | EQUIPMENT |

### Resolution Strategy

**For Compound Mentions:**

```
Example: "The Siemens SCADA system was manufactured by Siemens in Germany."

Two entities present:
1. "Siemens SCADA system"
   → Compound: Company + Product Type
   → Classification: EQUIPMENT

2. "Siemens" (second occurrence)
   → Context: "manufactured by [ENTITY]"
   → Classification: VENDOR
```

**Annotation:**
```json
[
  {
    "text": "Siemens SCADA system",
    "label": "EQUIPMENT",
    "rationale": "Company + device type (SCADA system)"
  },
  {
    "text": "Siemens",
    "label": "VENDOR",
    "rationale": "Standalone company in attribution phrase"
  }
]
```

### Difficult Cases

#### Case 1: Brand Names Used as Modifiers
```
Text: "Siemens technology"

Analysis:
- "Siemens" = Company name
- "technology" = Generic term (not specific product)

Decision: VENDOR
Rationale: "Technology" is too generic to constitute equipment
```

#### Case 2: Product Families
```
Text: "Rockwell Automation ControlLogix"

Analysis:
- "Rockwell Automation" = Company
- "ControlLogix" = Product family

Decision: EQUIPMENT
Rationale: ControlLogix is a specific product line, not just company name
```

#### Case 3: Abbreviated Forms
```
Text: "AB PLCs"

Analysis:
- "AB" = Allen-Bradley abbreviation
- "PLCs" = Device type

Decision: EQUIPMENT
Rationale: Abbreviation + device type = equipment reference
```

---

## PROTOCOL vs EQUIPMENT

### Primary Decision Tree

```
┌─────────────────────────────────────────────┐
│ Is the mention a communication standard    │
│ or protocol name?                           │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴───────┐
      │ YES           │ NO
      │               │
      ▼               ▼
  ┌────────────┐  ┌─────────────────────────┐
  │ Is it a    │  │ Does it describe a      │
  │ hardware   │  │ physical device?        │
  │ device?    │  └─────────┬───────────────┘
  └─────┬──────┘            │
        │              ┌────┴────┐
        │              │ YES     │ NO
        │              │         │
        ▼              ▼         ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │EQUIPMENT │  │EQUIPMENT │  │ PROTOCOL │
   └──────────┘  └──────────┘  └──────────┘
```

### Classification Rules

#### PROTOCOL Examples
- **Communication Standards:** Modbus, DNP3, IEC-61850, OPC-UA
- **Network Protocols:** TCP/IP, HTTP, MQTT, SNMP
- **Industrial Protocols:** PROFINET, EtherNet/IP, DeviceNet
- **Protocol Variants:** Modbus TCP, Modbus RTU, DNP3 over IP

**Key Indicators:**
- Standard specification numbers (IEC-61850, IEEE 802.3)
- Protocol family names (Modbus, PROFIBUS)
- Communication method descriptors (TCP, RTU, Serial)

#### EQUIPMENT Examples
- **Hardware Devices:** Modbus gateway, DNP3 concentrator, IEC-61850 relay
- **Physical Products:** EtherNet/IP switch, PROFINET device, OPC server
- **Devices implementing protocols:** Modbus RTU sensor, DNP3 RTU

**Key Indicators:**
- Hardware suffixes (gateway, relay, device, sensor)
- Physical product names
- Device type descriptors (concentrator, server, switch)

### Decision Examples

#### Example 1: Modbus
```
Case A: "The system uses Modbus for communication."
        ^^^^^^ PROTOCOL
Rationale: Communication standard, no hardware reference

Case B: "Install the Modbus gateway in the network."
        ^^^^^^^^^^^^^^^ EQUIPMENT
Rationale: "gateway" = hardware device implementing Modbus

Case C: "Configure the Modbus TCP connection."
        ^^^^^^^^^ PROTOCOL
Rationale: Protocol variant (TCP = transport layer)
```

#### Example 2: IEC-61850
```
Case A: "Compliant with IEC-61850 standard."
        ^^^^^^^^^ PROTOCOL
Rationale: Standard specification reference

Case B: "The IEC-61850 relay protects the substation."
        ^^^^^^^^^^^^^^ EQUIPMENT
Rationale: "relay" = physical protective device

Case C: "IEC-61850 GOOSE messaging enables fast communication."
        ^^^^^^^^^ PROTOCOL
Rationale: Protocol feature (GOOSE = messaging type)
```

#### Example 3: DNP3
```
Case A: "DNP3 protocol provides secure communication."
        ^^^^ PROTOCOL
Rationale: Protocol in context of communication method

Case B: "The DNP3 RTU collects field data."
        ^^^^^^^^ EQUIPMENT
Rationale: "RTU" = Remote Terminal Unit (hardware)

Case C: "Configure DNP3 outstation parameters."
        ^^^^ PROTOCOL
Rationale: Protocol configuration, not device reference
```

### Hyphenated Forms

#### Guideline for [Protocol]-[Suffix] Forms

**PROTOCOL if suffix is:**
- Version identifier: "Modbus-TCP", "DNP3-LAN"
- Transport layer: "OPC-UA", "MQTT-SN"
- Variant specification: "PROFIBUS-DP", "EtherNet/IP"

**EQUIPMENT if suffix is:**
- Device type: "Modbus-Gateway", "DNP3-Concentrator"
- Hardware descriptor: "IEC-61850-Relay", "OPC-Server"
- Product model: "DeviceNet-Scanner", "PROFINET-Switch"

### Complex Cases

#### Case 1: Protocol-Enabled Devices
```
Text: "IEC-61850-enabled relay"

Analysis:
- "IEC-61850" = Protocol
- "enabled" = Implementation descriptor
- "relay" = Device type

Decision: Do not annotate "IEC-61850-enabled relay" as single entity
Annotate separately:
- "IEC-61850" → PROTOCOL
- "relay" → Could be EQUIPMENT (context-dependent)
```

#### Case 2: Protocol Stacks
```
Text: "Modbus over TCP/IP stack"

Analysis:
- "Modbus" = Application layer protocol
- "TCP/IP" = Transport/Network layer protocols
- "stack" = Software component

Decision:
- "Modbus" → PROTOCOL
- "TCP/IP" → PROTOCOL
Do not annotate "stack" (non-entity descriptor)
```

---

## SECURITY vs MITIGATION

### Primary Decision Tree

```
┌─────────────────────────────────────────────┐
│ Does the mention describe a threat,        │
│ vulnerability, or security concern?         │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴───────┐
      │ YES           │ NO
      │               │
      ▼               ▼
  ┌─────────┐   ┌──────────────────────────┐
  │SECURITY │   │ Does it describe a       │
  └─────────┘   │ countermeasure or fix?   │
                └────────┬─────────────────┘
                         │
                   ┌─────┴─────┐
                   │ YES       │ NO
                   │           │
                   ▼           ▼
              ┌──────────┐  ┌────────────┐
              │MITIGATION│  │ Not Entity │
              └──────────┘  └────────────┘
```

### Classification Guidelines

#### SECURITY (Threats, Vulnerabilities, Attacks)

**Problem-Focused Entities:**
- Vulnerabilities: "buffer overflow", "SQL injection", "zero-day"
- Attack vectors: "phishing", "man-in-the-middle", "DDoS attack"
- Threat actors: "APT28", "ransomware", "malware"
- Security weaknesses: "weak encryption", "default passwords"

**Linguistic Indicators:**
- Describes negative security state
- Identifies weakness or exposure
- Names attack method
- Specifies threat type

#### MITIGATION (Countermeasures, Fixes, Controls)

**Solution-Focused Entities:**
- Security controls: "firewall rules", "access control lists", "encryption"
- Protective measures: "patch management", "network segmentation"
- Detection mechanisms: "intrusion detection", "anomaly detection"
- Remediation actions: "software update", "security hardening"

**Linguistic Indicators:**
- Describes protective action
- Identifies security control
- Specifies defensive measure
- Names remediation method

### Decision Examples

#### Example 1: Encryption
```
Case A: "The system lacks encryption."
        ^^^^^^^^^^ SECURITY (vulnerability)
Context: "lacks" indicates security weakness

Case B: "Implement AES-256 encryption for data protection."
        ^^^^^^^^^^^^^^^^^^^ MITIGATION
Context: "implement" indicates security control

Case C: "Weak encryption enables eavesdropping."
        ^^^^^^^^^^^^^^ SECURITY (vulnerability)
Context: "weak" indicates security flaw
```

#### Example 2: Authentication
```
Case A: "Default credentials pose a security risk."
        ^^^^^^^^^^^^^^^^^^^ SECURITY (vulnerability)
Context: Default credentials = weakness

Case B: "Multi-factor authentication prevents unauthorized access."
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^ MITIGATION
Context: Preventive measure = control

Case C: "Authentication bypass vulnerability discovered."
        ^^^^^^^^^^^^^^^^^^^^^^^^^ SECURITY (vulnerability)
Context: Bypass = attack vector
```

#### Example 3: Network Security
```
Case A: "Network segmentation isolates critical assets."
        ^^^^^^^^^^^^^^^^^^^^ MITIGATION
Context: Protective architecture = control

Case B: "Flat network topology increases attack surface."
        ^^^^^^^^^^^^^^^^^^^^ SECURITY (weakness)
Context: Vulnerability-inducing architecture

Case C: "Deploy DMZ to protect internal network."
        ^^^ MITIGATION
Context: Protective zone = security control
```

### Ambiguous Cases

#### Case 1: Dual-Context Terms
```
Text: "firewall"

Context A: "The firewall blocks malicious traffic."
           ^^^^^^^^ MITIGATION
Rationale: Active protective measure

Context B: "Missing firewall exposes the network."
           ^^^^^^^^ (implied) SECURITY
Rationale: Absence indicates vulnerability
→ Annotate "Missing firewall" as SECURITY issue
```

#### Case 2: Patch Management
```
Text: "unpatched systems"

Analysis:
- "unpatched" = Lacking security updates
- Describes vulnerable state

Decision: SECURITY (vulnerability)
Rationale: Describes security weakness, not the solution

Contrast:
Text: "patch management program"
      ^^^^^^^^^^^^^^^^^^^^^^^^ MITIGATION
Rationale: Describes remediation process
```

#### Case 3: Monitoring Systems
```
Text: "intrusion detection system"

Analysis:
- Detects attacks (reactive)
- But prevents damage (protective)

Decision: MITIGATION
Rationale: Detection = security control/countermeasure

Contrast:
Text: "intrusion detected in network"
      ^^^^^^^^^ SECURITY (threat event)
Rationale: Describes security incident, not control
```

---

## Boundary Rules

### Word Boundary Enforcement

**Rule 1: Entities must start and end on word boundaries**

#### Valid Boundaries
```
✓ "SCADA system"
✓ "IEC-61850"
✓ "multi-factor authentication"
✓ "SQL injection"
```

#### Invalid Boundaries (Require Adjustment)
```
✗ "the SCADA sys" → Adjust to "SCADA system"
✗ "IEC-618" → Adjust to "IEC-61850"
✗ "authentica" → Adjust to "authentication"
```

**Exception: Hyphenated Compounds**
- Treat hyphenated words as single tokens
- "IEC-61850" = one word (don't break at hyphen)
- "multi-factor" = one word
- "man-in-the-middle" = one compound

### Article and Preposition Handling

**Rule 2: Exclude leading articles and prepositions**

#### Articles to Exclude
- "the", "a", "an"

```
Before: "the SCADA system"
After: "SCADA system"
Removed: "the "
```

#### Prepositions to Exclude
- "of", "in", "on", "at", "for", "with", "by"

```
Before: "in IEC-61850"
After: "IEC-61850"
Removed: "in "

Before: "of Siemens"
After: "Siemens"
Removed: "of "
```

**Exception: Prepositions within entity**
```
✓ "man-in-the-middle attack" (keep "in-the")
✓ "end-to-end encryption" (keep "to")
Rationale: Part of compound term, not leading preposition
```

### Punctuation Standardization

**Rule 3: Consistent punctuation handling**

#### Quotes

**Include if part of product name:**
```
✓ "FactoryTalk" (with quotes if that's the official name)
✓ "WinCC" (with quotes if stylized)
```

**Exclude if wrapping emphasis:**
```
Before: The "SCADA" system
After: SCADA (exclude wrapping quotes)

Before: Mention of "Siemens"
After: Siemens (exclude citation quotes)
```

**Decision Tree for Quotes:**
```
Are quotes part of official name?
├─ YES → Include quotes
└─ NO → Are they emphasis/citation?
       ├─ YES → Exclude quotes
       └─ UNCLEAR → Check official documentation
```

#### Parentheses

**Include if part of acronym expansion:**
```
✓ "ICS (Industrial Control System)"
✓ "SCADA (Supervisory Control and Data Acquisition)"
```

**Exclude if wrapping clarification:**
```
Before: The system (SCADA) controls the plant.
After: SCADA
Rationale: Parentheses wrap appositive, not part of term

Before: Siemens (the manufacturer)
After: Siemens
Rationale: Parentheses add clarification, not part of entity
```

**Decision Tree for Parentheses:**
```
Do parentheses contain acronym expansion?
├─ YES → Include full phrase "TERM (EXPANSION)"
└─ NO → Are they wrapping appositive?
       ├─ YES → Exclude parentheses
       └─ Uncertain → Exclude by default
```

### Multi-Word Entity Coherence

**Rule 4: Multi-word entities must be semantically coherent**

#### Valid Multi-Word Patterns

**Company + Product:**
```
✓ "Siemens S7-1500"
✓ "Allen-Bradley ControlLogix"
✓ "Schneider Electric Modicon"
```

**Protocol + Variant:**
```
✓ "Modbus TCP"
✓ "DNP3 over IP"
✓ "IEC 61850"
```

**Device + Type:**
```
✓ "SCADA system"
✓ "PLC controller"
✓ "HMI interface"
```

#### Invalid Multi-Word Extensions

**Including Non-Entity Words:**
```
✗ "SCADA system running"
Reason: "running" = verb, not part of entity
Correct: "SCADA system"

✗ "Siemens PLC that controls"
Reason: Relative clause, not entity component
Correct: "Siemens PLC"
```

**Partial Phrases:**
```
✗ "security vulnerability in"
Reason: "in" = preposition, not entity end
Correct: "security vulnerability"

✗ "firewall protecting the"
Reason: "protecting the" = additional context
Correct: "firewall"
```

### Whitespace Normalization

**Rule 5: Trim leading and trailing whitespace**

```
Before: " SCADA system "
After: "SCADA system"

Before: "  Modbus TCP  "
After: "Modbus TCP"
```

**Internal whitespace:**
- Preserve single spaces between words
- Collapse multiple spaces to single space

```
Before: "SCADA    system"
After: "SCADA system"
```

---

## Multi-Entity Contexts

### Handling Multiple Entities in Proximity

#### Case 1: Sequential Entities
```
Text: "Siemens S7-1500 PLC uses Modbus TCP protocol"

Entities:
1. "Siemens S7-1500 PLC" → EQUIPMENT
2. "Modbus TCP" → PROTOCOL

Do NOT create overlapping spans
Do NOT merge into single entity
```

#### Case 2: Nested Entities
```
Text: "Siemens SCADA system manufactured by Siemens"

Entities:
1. "Siemens SCADA system" → EQUIPMENT (company + product)
2. "Siemens" → VENDOR (manufacturer reference)

Two separate entity mentions, different contexts
```

#### Case 3: Coordinated Entities
```
Text: "Modbus, DNP3, and IEC-61850 protocols"

Entities:
1. "Modbus" → PROTOCOL
2. "DNP3" → PROTOCOL
3. "IEC-61850" → PROTOCOL

Annotate each separately
Do NOT include "protocols" in entity spans
```

### Entity Lists

**Rule: Annotate each item separately**

```
Text: "Common PLCs include Siemens S7-1500, Allen-Bradley ControlLogix, and Schneider Modicon."

Entities:
1. "Siemens S7-1500" → EQUIPMENT
2. "Allen-Bradley ControlLogix" → EQUIPMENT
3. "Schneider Modicon" → EQUIPMENT

Do NOT annotate "Common PLCs"
Do NOT include punctuation (, and) in spans
```

### Appositive Constructions

**Rule: Annotate primary mention, not appositive**

```
Text: "The ICS, a critical infrastructure system, requires protection."

Entity: "ICS" → (appropriate label based on context)

Do NOT annotate "a critical infrastructure system" separately
Rationale: Appositive provides definition, not separate mention
```

**Exception: Both are entities of different types**
```
Text: "Siemens, a German manufacturer, produces S7-1500 PLCs."

Entities:
1. "Siemens" → VENDOR
2. "S7-1500 PLCs" → EQUIPMENT

Do NOT annotate "a German manufacturer"
Rationale: Descriptive appositive, not entity type
```

---

## Edge Cases

### Acronyms and Abbreviations

#### First Mention with Expansion
```
Text: "Industrial Control System (ICS)"

Options:
A. Annotate entire phrase: "Industrial Control System (ICS)"
B. Annotate acronym only: "ICS"
C. Annotate expanded form only: "Industrial Control System"

Recommended: **Option A**
Rationale: Captures both forms, provides full context
```

#### Subsequent Mentions
```
First mention: "Industrial Control System (ICS)" → Full annotation
Later mentions: "ICS" → Annotate acronym only
```

### Possessive Forms

**Rule: Exclude possessive markers**

```
Before: "Siemens's PLC"
After: "Siemens" (VENDOR) + "PLC" (could be EQUIPMENT)
Exclude: "'s"

Before: "Modbus's advantages"
After: "Modbus" (PROTOCOL)
Exclude: "'s"
```

### Plural Forms

**Rule: Include plural markers**

```
✓ "PLCs"
✓ "firewalls"
✓ "vulnerabilities"

Rationale: Plural form is grammatical part of entity
```

### Hyphenated Company Names

**Rule: Keep hyphens as part of entity**

```
✓ "Allen-Bradley"
✓ "Emerson-Electric"
✓ "Rockwell-Automation"
```

### Version Numbers

**Rule: Include if part of product name, exclude if modifier**

```
Include: "TIA Portal v16" → "TIA Portal v16" (EQUIPMENT)
Rationale: Version identifies specific product

Exclude: "using Modbus version 2.0" → "Modbus" (PROTOCOL)
Rationale: Version is additional information, not entity name
```

### Compound Technical Terms

**Rule: Include technical modifiers if standard terminology**

```
✓ "SQL injection" (complete attack name)
✓ "buffer overflow" (complete vulnerability type)
✓ "man-in-the-middle attack" (complete attack method)

✗ "serious SQL injection" (exclude "serious")
✗ "critical buffer overflow" (exclude "critical")
Rationale: Severity descriptors are not part of entity
```

### Geographic Modifiers

**Rule: Exclude geographic descriptors unless part of official name**

```
Exclude: "German company Siemens" → "Siemens" (VENDOR)
Rationale: Geographic descriptor, not entity component

Include: "Siemens Germany" → "Siemens Germany" (if official subsidiary name)
Rationale: Geographic part of official entity name
```

---

## Annotation Workflow

### Step-by-Step Process

**Step 1: Identify candidate entity**
- Read sentence/paragraph for context
- Identify potential entity mention

**Step 2: Classify entity type**
- Apply decision trees for entity type
- Consider context clues and syntactic patterns
- Resolve ambiguities using guidelines

**Step 3: Determine boundaries**
- Apply word boundary rules
- Remove leading articles/prepositions
- Standardize punctuation
- Validate multi-word coherence

**Step 4: Validate annotation**
- Check against examples in guidelines
- Ensure consistency with previous annotations
- Verify no overlapping spans

**Step 5: Document reasoning (if ambiguous)**
- Note decision rationale
- Reference guideline section
- Flag for quality review if uncertain

### Quality Checklist

Before finalizing annotations, verify:

- [ ] Entity type correct per decision trees
- [ ] Boundaries on word boundaries
- [ ] No leading articles/prepositions
- [ ] Punctuation standardized
- [ ] Multi-word entities coherent
- [ ] No whitespace issues
- [ ] No overlapping spans
- [ ] Consistent with similar cases

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 6.0.0 | 2025-11-06 | Initial comprehensive guidelines for v6 |

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Active - Ready for Use
