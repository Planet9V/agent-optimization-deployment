# MITRE ATT&CK STIX Data Structure Analysis
**Date:** 2025-11-08
**Purpose:** Research analysis for integration with existing threat modeling knowledge graph

---

## Executive Summary

MITRE ATT&CK data is available in STIX 2.1 JSON format with comprehensive structured threat intelligence covering three domains: Enterprise, Mobile, and ICS (Industrial Control Systems). The data model uses STIX relationship objects to connect tactics, techniques, threat actors, software, and mitigations - providing rich semantic relationships ready for knowledge graph integration.

**Key Finding:** MITRE ATT&CK relationships align well with existing schema relationship types (EXPLOITS, USES, TARGETS, ENABLES, MITIGATES) but introduce additional relationship semantics that can enhance the threat model.

---

## 1. Repository Structure

### Data Organization
```
attack-stix-data/
├── enterprise-attack/           # Windows, macOS, Linux, Cloud, Network (49MB)
│   ├── enterprise-attack.json  # Latest version (always current)
│   ├── enterprise-attack-18.0.json
│   └── [historical versions 1.0 - 18.0]
├── mobile-attack/              # iOS, Android platforms (4.8MB)
│   ├── mobile-attack.json
│   └── [versioned releases]
├── ics-attack/                 # Industrial Control Systems (3.4MB)
│   ├── ics-attack.json
│   └── [versioned releases]
├── index.json                  # Collection metadata
└── index.md                    # Human-readable index
```

### Version Information
- **Current Version:** 18.0 (October 28, 2025)
- **Version History:** Full historical versions from 1.0 onwards
- **Update Frequency:** Major releases approximately every 6 months with minor patches
- **Collection Format:** STIX 2.1 JSON with collection bundles

---

## 2. STIX 2.1 Data Model

### Core Object Types

The MITRE ATT&CK data uses STIX 2.1 standard with custom extensions:

| STIX Type | ATT&CK Concept | Description | Count (Enterprise) |
|-----------|----------------|-------------|-------------------|
| `attack-pattern` | Techniques & Sub-techniques | Adversary tactics, techniques, procedures | ~800+ |
| `course-of-action` | Mitigations | Defensive measures and security controls | ~50+ |
| `intrusion-set` | Threat Actor Groups | APT groups and threat actors | ~150+ |
| `malware` | Malicious Software | Malware families | ~700+ |
| `tool` | Legitimate Tools | Tools used by adversaries | ~100+ |
| `relationship` | Connections | Semantic relationships between objects | ~15,000+ |
| `x-mitre-tactic` | Tactics | High-level adversary goals | 14 |
| `x-mitre-matrix` | Attack Matrices | Tactic/technique organization | 3 |
| `x-mitre-collection` | Collection Metadata | Version and content tracking | 3 |
| `x-mitre-data-source` | Data Sources | Detection sources | ~40+ |
| `x-mitre-data-component` | Data Components | Specific detection artifacts | ~100+ |
| `x-mitre-detection-strategy` | Detection Strategies | Detection approaches | NEW in v18 |
| `campaign` | Campaigns | Specific threat campaigns | ~40+ |
| `identity` | MITRE Organization | Creator identity | 1 |
| `marking-definition` | TLP Markings | Traffic Light Protocol | 1 |

---

## 3. Sample Data Structures

### 3.1 Attack Pattern (Technique)

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--0042a9f5-f053-4769-b3ef-9ad018dfa298",
  "created": "2020-01-14T17:18:32.126Z",
  "modified": "2025-10-24T17:48:19.059Z",
  "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
  "name": "Extra Window Memory Injection",
  "description": "Adversaries may inject malicious code...",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "url": "https://attack.mitre.org/techniques/T1055/011",
      "external_id": "T1055.011"  // ATT&CK ID
    },
    {
      "source_name": "Microsoft Window Classes",
      "description": "Microsoft. (n.d.). About Window Classes...",
      "url": "https://msdn.microsoft.com/..."
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "defense-evasion"  // Links to tactic
    },
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "privilege-escalation"
    }
  ],
  "x_mitre_attack_spec_version": "3.2.0",
  "x_mitre_deprecated": false,
  "x_mitre_detection": "",  // Detection guidance
  "x_mitre_domains": ["enterprise-attack"],
  "x_mitre_is_subtechnique": true,  // Indicates parent-child relationship
  "x_mitre_platforms": ["Windows"],  // Target platforms
  "x_mitre_version": "1.1"
}
```

**Key Fields for Integration:**
- `external_id`: ATT&CK ID (e.g., "T1055.011") - primary reference
- `kill_chain_phases`: Links techniques to tactics
- `x_mitre_is_subtechnique`: Hierarchical technique relationships
- `x_mitre_platforms`: Target technology platforms
- `external_references`: Rich citations for provenance

###  3.2 Relationship Object

```json
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--00038d0e-7fc7-41c3-9055-edb4d87ea912",
  "created": "2021-04-27T01:56:35.810Z",
  "modified": "2025-04-28T15:31:30.051Z",
  "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
  "relationship_type": "uses",
  "source_ref": "malware--6a21e3a4-5ffe-4581-af9a-6a54c7536f44",  // Explosive malware
  "target_ref": "attack-pattern--707399d6-ab3e-4963-9315-d9d3818cd6a0",  // Technique
  "description": "[Explosive] has collected the MAC address from the victim's machine.",
  "external_references": [
    {
      "source_name": "CheckPoint Volatile Cedar March 2015",
      "description": "Threat Intelligence and Research...",
      "url": "https://media.kasperskycontenthub.com/..."
    }
  ],
  "x_mitre_deprecated": false,
  "x_mitre_attack_spec_version": "3.2.0"
}
```

**Relationship Types in MITRE ATT&CK:**
- `uses` - Primary relationship (threat actor uses technique, malware uses technique)
- `mitigates` - Mitigation controls techniques
- `subtechnique-of` - Hierarchical technique relationships
- `detects` - Detection strategy detects technique
- `attributed-to` - Campaign attributed to threat actor
- `revoked-by` - Object replacement tracking

### 3.3 Intrusion Set (Threat Actor Group)

```json
{
  "type": "intrusion-set",
  "spec_version": "2.1",
  "id": "intrusion-set--01e28736-2ffc-455b-9880-ed4d1407ae07",
  "created": "2021-01-06T17:46:35.134Z",
  "modified": "2024-10-28T19:11:56.485Z",
  "name": "Indrik Spider",
  "description": "[Indrik Spider] is a Russia-based cybercriminal group...",
  "aliases": [
    "Indrik Spider",
    "Evil Corp",
    "Manatee Tempest",
    "DEV-0243",
    "UNC2165"
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "url": "https://attack.mitre.org/groups/G0119",
      "external_id": "G0119"
    },
    {
      "source_name": "Crowdstrike Indrik November 2018",
      "description": "Frankoff, S., Hartley, B...",
      "url": "https://www.crowdstrike.com/..."
    }
  ],
  "x_mitre_contributors": [
    "Jennifer Kim Roman, CrowdStrike",
    "Liran Ravich, CardinalOps"
  ],
  "x_mitre_deprecated": false,
  "x_mitre_version": "4.1",
  "x_mitre_domains": ["enterprise-attack"]
}
```

**Key Features:**
- `aliases`: Multiple names for same threat actor (critical for entity resolution)
- `x_mitre_contributors`: Attribution and provenance
- Rich citations linking to threat intelligence reports

### 3.4 Course of Action (Mitigation)

```json
{
  "type": "course-of-action",
  "spec_version": "2.1",
  "id": "course-of-action--00d7d21b-69d6-4797-88a2-c86f3fc97651",
  "created": "2018-10-17T00:14:20.652Z",
  "modified": "2025-04-18T17:59:39.912Z",
  "name": "Password Filter DLL Mitigation",
  "description": "Ensure only valid password filters are registered...",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "url": "https://attack.mitre.org/mitigations/T1174",
      "external_id": "T1174"
    },
    {
      "source_name": "Microsoft Install Password Filter n.d",
      "description": "Microsoft. (n.d.). Installing and Registering...",
      "url": "https://msdn.microsoft.com/..."
    }
  ],
  "x_mitre_deprecated": true,  // Important: deprecated objects remain for historical reference
  "x_mitre_domains": ["enterprise-attack"],
  "x_mitre_version": "1.0"
}
```

---

## 4. Relationship Semantics

### 4.1 MITRE ATT&CK Relationship Types

Based on STIX relationships in the data:

| Relationship Type | Source Type | Target Type | Description | Mapping to Current Schema |
|-------------------|-------------|-------------|-------------|---------------------------|
| `uses` | intrusion-set, campaign | attack-pattern | Threat actor uses technique | **EXPLOITS** |
| `uses` | malware, tool | attack-pattern | Software implements technique | **EXPLOITS** |
| `uses` | intrusion-set, campaign | malware, tool | Threat actor uses software | **USES** |
| `mitigates` | course-of-action | attack-pattern | Mitigation addresses technique | **MITIGATES** |
| `subtechnique-of` | attack-pattern | attack-pattern | Technique hierarchy | NEW - Parent/child |
| `detects` | x-mitre-detection-strategy | attack-pattern | Detection method finds technique | **ENABLES** (detection) |
| `attributed-to` | campaign | intrusion-set | Campaign attribution | NEW - Attribution |
| `revoked-by` | any | any | Object superseded by another | NEW - Lifecycle |

### 4.2 Comparison with Current Schema Relationships

**Existing Schema:**
- EXPLOITS: Threat uses vulnerability/weakness
- USES: Tool/malware uses component
- TARGETS: Attack targets asset/system
- ENABLES: Vulnerability enables attack
- MITIGATES: Control reduces risk

**MITRE ATT&CK Additions:**
1. **Hierarchical Techniques:** `subtechnique-of` relationship creates technique taxonomy
2. **Detection Relationships:** Links detection strategies to techniques
3. **Campaign Attribution:** Connects campaigns to threat actors
4. **Lifecycle Management:** `revoked-by` tracks object evolution

### 4.3 Proposed Integration Mapping

```
MITRE Relationship → Current Schema Relationship

uses (actor→technique) → EXPLOITS
uses (actor→software) → USES
uses (software→technique) → EXPLOITS
mitigates → MITIGATES
subtechnique-of → PARENT_OF / CHILD_OF (new)
detects → ENABLES (with type=detection)
attributed-to → ATTRIBUTED_TO (new)
```

---

## 5. Integration Opportunities

### 5.1 Direct Mappings

**High Confidence Mappings:**

1. **ATT&CK Techniques → Threat Actors:**
   - MITRE `uses` relationship (intrusion-set → attack-pattern)
   - Maps to: `EXPLOITS` relationship
   - Confidence: **HIGH** - Direct semantic match

2. **ATT&CK Mitigations → Techniques:**
   - MITRE `mitigates` relationship (course-of-action → attack-pattern)
   - Maps to: `MITIGATES` relationship
   - Confidence: **HIGH** - Direct semantic match

3. **Software → Techniques:**
   - MITRE `uses` relationship (malware/tool → attack-pattern)
   - Maps to: `EXPLOITS` or `USES`
   - Confidence: **MEDIUM** - Context-dependent

### 5.2 Enrichment Opportunities

**New Relationships to Add:**

1. **Technique Hierarchy:**
   ```cypher
   CREATE (parent:Technique)-[:PARENT_OF]->(child:Technique)
   CREATE (child)-[:SUBTECHNIQUE_OF]->(parent)
   ```
   - Enables technique taxonomy navigation
   - Supports hierarchical attack pattern analysis

2. **Detection Mappings:**
   ```cypher
   CREATE (data_source:DataSource)-[:DETECTS]->(technique:Technique)
   CREATE (detection_strategy:DetectionStrategy)-[:IDENTIFIES]->(technique)
   ```
   - Links defensive capabilities to threats
   - Supports detection gap analysis

3. **Campaign Attribution:**
   ```cypher
   CREATE (campaign:Campaign)-[:ATTRIBUTED_TO]->(actor:ThreatActor)
   CREATE (campaign)-[:USES]->(technique:Technique)
   ```
   - Tracks specific threat campaigns
   - Enables temporal threat analysis

### 5.3 Data Enrichment

**ATT&CK Provides:**
- **Rich Descriptions:** Detailed technique descriptions with examples
- **Citations:** External references to threat intelligence reports
- **Platform Mapping:** Techniques mapped to affected platforms (Windows, Linux, macOS, Cloud, etc.)
- **Tactic Classification:** Techniques organized by adversary goals (14 tactics)
- **Detection Guidance:** Detection approaches and data sources
- **Mitigation Recommendations:** Defensive controls for each technique
- **Software Profiles:** Detailed malware and tool capabilities
- **Threat Actor Profiles:** Group aliases, motivations, targeting patterns

---

## 6. Schema Integration Recommendations

### 6.1 Phased Integration Approach

**Phase 1: Core Relationships (High Priority)**
```
Priority: HIGH
Timeline: Immediate
Effort: Low

Actions:
1. Import ATT&CK Techniques as attack patterns
2. Map uses(actor→technique) to EXPLOITS relationships
3. Map mitigates(mitigation→technique) to MITIGATES relationships
4. Import external_references for provenance tracking
```

**Phase 2: Technique Taxonomy (Medium Priority)**
```
Priority: MEDIUM
Timeline: After Phase 1
Effort: Medium

Actions:
1. Create parent-child technique relationships
2. Import tactic classifications (kill chain phases)
3. Add platform mappings to techniques
4. Enrich with detection guidance
```

**Phase 3: Advanced Integration (Lower Priority)**
```
Priority: LOW
Timeline: After Phase 2
Effort: High

Actions:
1. Import campaigns and attribution relationships
2. Add detection strategies and data sources
3. Integrate with existing CVE/CWE mappings
4. Create cross-domain analysis capabilities
```

### 6.2 Proposed Schema Extensions

**New Node Types:**
```cypher
// Technique hierarchy
(:Technique {
  attack_id: "T1055",           // ATT&CK ID
  name: "Process Injection",
  is_subtechnique: false,
  platforms: ["Windows", "Linux"],
  tactics: ["defense-evasion", "privilege-escalation"],
  mitre_version: "18.0",
  deprecated: false
})

// Detection capabilities
(:DetectionStrategy {
  name: "Process Monitoring",
  description: "Monitor process creation...",
  data_sources: ["Process", "File"]
})

(:DataSource {
  name: "Process",
  description: "Information about instances of computer programs..."
})

(:DataComponent {
  name: "Process Creation",
  data_source: "Process"
})
```

**New Relationship Types:**
```cypher
// Technique taxonomy
(parent:Technique)-[:PARENT_OF]->(child:Technique)
(child:Technique)-[:SUBTECHNIQUE_OF]->(parent:Technique)

// Detection relationships
(data_source:DataSource)-[:PROVIDES]->(data_component:DataComponent)
(data_component:DataComponent)-[:DETECTS]->(technique:Technique)
(detection_strategy:DetectionStrategy)-[:IDENTIFIES]->(technique:Technique)

// Campaign tracking
(campaign:Campaign)-[:ATTRIBUTED_TO]->(actor:ThreatActor)
(campaign:Campaign)-[:USES]->(technique:Technique)
(campaign:Campaign)-[:USES]->(software:Malware|Tool)
```

### 6.3 Data Quality Considerations

**Strengths:**
- ✅ **Well-structured:** Consistent STIX 2.1 format
- ✅ **Versioned:** Full historical versions available
- ✅ **Cited:** Rich external references for provenance
- ✅ **Maintained:** Regular updates from MITRE
- ✅ **Standardized:** Industry-standard taxonomy

**Challenges:**
- ⚠️ **Large Dataset:** 49MB for enterprise alone (15,000+ objects)
- ⚠️ **Deprecated Objects:** Historical objects marked deprecated but retained
- ⚠️ **Aliases:** Multiple names for same entities (requires deduplication)
- ⚠️ **Version Management:** Need strategy for updates without breaking existing relationships

---

## 7. Technical Implementation Guide

### 7.1 Data Access

**Recommended Approach:**
```python
# Using stix2 Python library
from stix2 import MemoryStore
import requests

# Load latest version
def load_attack_data(domain='enterprise-attack'):
    url = f"https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/{domain}/{domain}.json"
    stix_data = requests.get(url).json()
    return MemoryStore(stix_data=stix_data["objects"])

src = load_attack_data()

# Query techniques
from stix2 import Filter
techniques = src.query([Filter('type', '=', 'attack-pattern')])

# Query relationships
uses_relationships = src.query([
    Filter('type', '=', 'relationship'),
    Filter('relationship_type', '=', 'uses')
])
```

### 7.2 Neo4j Import Strategy

**Batch Import Approach:**
```cypher
// 1. Import techniques
UNWIND $techniques AS tech
MERGE (t:Technique:AttackPattern {attack_id: tech.external_id})
SET t.stix_id = tech.id,
    t.name = tech.name,
    t.description = tech.description,
    t.platforms = tech.platforms,
    t.tactics = [phase.phase_name | phase IN tech.kill_chain_phases],
    t.is_subtechnique = tech.is_subtechnique,
    t.deprecated = tech.deprecated,
    t.mitre_version = tech.version,
    t.created = tech.created,
    t.modified = tech.modified

// 2. Import threat actors
UNWIND $actors AS actor
MERGE (a:ThreatActor {attack_id: actor.external_id})
SET a.stix_id = actor.id,
    a.name = actor.name,
    a.aliases = actor.aliases,
    a.description = actor.description

// 3. Import relationships
UNWIND $relationships AS rel
MATCH (source {stix_id: rel.source_ref})
MATCH (target {stix_id: rel.target_ref})
CALL apoc.create.relationship(source, rel.relationship_type, {
  description: rel.description,
  created: rel.created,
  modified: rel.modified,
  citations: [ref.url | ref IN rel.external_references]
}, target) YIELD rel as r
RETURN count(r)
```

### 7.3 Update Strategy

**Recommended Update Cycle:**
1. **Quarterly:** Check for new MITRE ATT&CK versions
2. **On Release:** Import new objects and relationships
3. **Preserve:** Keep deprecated objects with deprecated flag
4. **Link:** Use `revoked-by` relationships to track updates

---

## 8. Integration with Current Schema

### 8.1 Crosswalk Analysis

**Current Schema → MITRE ATT&CK**

| Current Concept | MITRE ATT&CK Equivalent | Mapping Type | Integration Complexity |
|----------------|-------------------------|--------------|----------------------|
| Vulnerability | attack-pattern | **Semantic** | MEDIUM - CVE/CWE linking needed |
| Threat Actor | intrusion-set | **Direct** | LOW - 1:1 mapping |
| Exploit | attack-pattern + technique | **Semantic** | MEDIUM - Contextual |
| Control/Mitigation | course-of-action | **Direct** | LOW - 1:1 mapping |
| Asset | platform (x_mitre_platforms) | **Attribute** | LOW - Property mapping |
| Software | malware, tool | **Direct** | LOW - Type differentiation |

### 8.2 Relationship Crosswalk

**Existing Relationships → MITRE Mappings**

| Current Relationship | MITRE Equivalent | Notes |
|---------------------|------------------|-------|
| EXPLOITS | uses (actor→technique) | Direct mapping |
| USES | uses (actor→software) | Direct mapping |
| MITIGATES | mitigates | Direct mapping |
| TARGETS | platform attribute | Indirect - use x_mitre_platforms |
| ENABLES | subtechnique-of + detects | Multiple MITRE relationships |

### 8.3 Data Quality Alignment

**Provenance Tracking:**
```
MITRE ATT&CK Provides:
- external_references: Full citations with URLs
- created_by_ref: Identity reference to MITRE
- x_mitre_contributors: Attribution to researchers
- x_mitre_version: Object version tracking
- modified timestamp: Last update tracking

Integration Benefit:
- Rich provenance for all threat intelligence
- Ability to trace claims to source reports
- Version control for evolving threat landscape
```

---

## 9. Benefits and Risks

### 9.1 Benefits

**Immediate Value:**
1. **Standardized Taxonomy:** Industry-standard technique names and IDs
2. **Rich Context:** Detailed descriptions with real-world examples
3. **Threat Intelligence:** Curated threat actor and malware profiles
4. **Detection Guidance:** Linked detection methods and data sources
5. **Mitigation Recommendations:** Security control mappings
6. **Community Alignment:** Compatible with security tools and frameworks

**Long-term Value:**
1. **Continuous Updates:** Regular MITRE releases with new threats
2. **Cross-organization Compatibility:** Common language for threat intelligence sharing
3. **Tool Integration:** Many security tools support ATT&CK natively
4. **Compliance Alignment:** Referenced in various compliance frameworks

### 9.2 Risks and Mitigation

**Risk 1: Data Volume**
- **Risk:** 15,000+ objects may impact query performance
- **Mitigation:** Index STIX IDs and ATT&CK IDs; use graph projections for analysis

**Risk 2: Update Management**
- **Risk:** Quarterly updates may introduce breaking changes
- **Mitigation:** Implement versioning strategy; maintain deprecated objects

**Risk 3: Semantic Overlap**
- **Risk:** MITRE concepts may conflict with existing definitions
- **Mitigation:** Create clear mapping documentation; use namespaces

**Risk 4: Maintenance Burden**
- **Risk:** Keeping data synchronized with MITRE releases
- **Mitigation:** Automate import process; implement change detection

---

## 10. Recommendations

### 10.1 Immediate Actions

**Priority 1: Proof of Concept**
1. Import 50 top techniques from Enterprise ATT&CK
2. Load relationships for 10 major threat actor groups
3. Test integration with existing CVE data
4. Validate query performance

**Priority 2: Schema Extension**
1. Add Technique node type with ATT&CK properties
2. Implement PARENT_OF/SUBTECHNIQUE_OF relationships
3. Extend existing EXPLOITS relationships with ATT&CK mappings
4. Add DetectionStrategy and DataSource nodes

**Priority 3: Tool Development**
1. Create Python import scripts using stix2 library
2. Build Neo4j APOC procedures for batch import
3. Develop update detection and synchronization logic
4. Implement validation and quality checks

### 10.2 Long-term Strategy

**Year 1: Foundation**
- Complete Phase 1 integration (core relationships)
- Establish update cadence aligned with MITRE releases
- Build query library for common threat analysis patterns
- Train users on ATT&CK taxonomy

**Year 2: Enhancement**
- Complete Phase 2 (technique taxonomy)
- Integrate detection strategies and data sources
- Link ATT&CK to CVE/CWE/CAPEC where applicable
- Develop advanced analytics capabilities

**Year 3: Maturity**
- Complete Phase 3 (campaigns and attribution)
- Implement cross-domain analysis (Enterprise + Mobile + ICS)
- Build automated threat landscape reporting
- Contribute findings back to MITRE community

---

## 11. Conclusion

MITRE ATT&CK STIX data provides a comprehensive, well-structured, and industry-standard threat intelligence source that aligns well with the existing schema. The integration effort is manageable with high-value returns:

**Strengths:**
- ✅ Direct mapping to existing EXPLOITS, USES, MITIGATES relationships
- ✅ Rich semantic relationships ready for knowledge graph
- ✅ Extensive provenance with external citations
- ✅ Regular updates from authoritative source (MITRE)
- ✅ Industry adoption and tool compatibility

**Integration Recommendation:** **PROCEED**
**Risk Level:** **LOW-MEDIUM**
**Value:** **HIGH**
**Effort:** **MEDIUM** (phased approach over 12-18 months)

The primary challenge is data volume and update synchronization, both manageable with proper automation and tooling. The semantic alignment with existing schema reduces integration friction significantly.

---

## Appendices

### Appendix A: Useful Resources

**Official Documentation:**
- STIX 2.1 Specification: https://docs.oasis-open.org/cti/stix/v2.1/
- ATT&CK STIX Data Repository: https://github.com/mitre-attack/attack-stix-data
- ATT&CK Website: https://attack.mitre.org
- TAXII Server: https://github.com/mitre-attack/attack-workbench-taxii-server

**Python Libraries:**
- stix2: https://github.com/oasis-open/cti-python-stix2
- taxii2-client: https://github.com/oasis-open/cti-taxii-client
- mitreattack-python: https://github.com/mitre-attack/mitreattack-python

**Neo4j Integration:**
- APOC Graph Algorithms: https://neo4j.com/labs/apoc/
- Python Driver: https://neo4j.com/docs/python-manual/current/

### Appendix B: Sample Queries

**Get all techniques used by a specific threat actor:**
```python
from stix2 import Filter

actor_id = "intrusion-set--..."
relationships = src.query([
    Filter('type', '=', 'relationship'),
    Filter('relationship_type', '=', 'uses'),
    Filter('source_ref', '=', actor_id)
])
technique_ids = [r.target_ref for r in relationships]
techniques = src.query([
    Filter('type', '=', 'attack-pattern'),
    Filter('id', 'in', technique_ids)
])
```

**Get all mitigations for a technique:**
```python
technique_id = "attack-pattern--..."
relationships = src.query([
    Filter('type', '=', 'relationship'),
    Filter('relationship_type', '=', 'mitigates'),
    Filter('target_ref', '=', technique_id)
])
mitigation_ids = [r.source_ref for r in relationships]
mitigations = src.query([
    Filter('type', '=', 'course-of-action'),
    Filter('id', 'in', mitigation_ids)
])
```

### Appendix C: Object Count Summary

| Object Type | Enterprise | Mobile | ICS | Total |
|-------------|-----------|---------|-----|-------|
| Techniques | ~800 | ~60 | ~80 | ~940 |
| Sub-techniques | ~400 | ~40 | ~20 | ~460 |
| Mitigations | ~50 | ~15 | ~20 | ~85 |
| Threat Actors | ~150 | ~10 | ~5 | ~165 |
| Malware | ~700 | ~100 | ~50 | ~850 |
| Tools | ~100 | ~20 | ~10 | ~130 |
| Relationships | ~15,000 | ~2,000 | ~1,500 | ~18,500 |
| **Total Objects** | **~17,200** | **~2,245** | **~1,685** | **~21,130** |

---

**End of Analysis**
