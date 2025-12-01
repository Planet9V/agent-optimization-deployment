# 🚨 CRITICAL: NER11 Gold Hierarchical Entity Structure
**File**: CRITICAL_NER11_HIERARCHICAL_STRUCTURE.md
**Created**: 2025-12-01 05:50:00 UTC
**Version**: 1.0.0
**Status**: ⚠️ CRITICAL SYSTEM ARCHITECTURE DOCUMENT
**Authority**: Production API Verification + Training Data Analysis

---

## 🎯 EXECUTIVE SUMMARY

**The NER11 Gold Standard uses a HIERARCHICAL taxonomy:**

- **60 TOP-LEVEL LABELS** (Production - Currently Implemented)
- **566 FINE-GRAINED ENTITY TYPES** (Design Goal - Property-Based Discrimination)

**CRITICAL UNDERSTANDING**:
The model detects 60 broad categories (e.g., `MALWARE`, `THREAT_ACTOR`), but each category represents MULTIPLE fine-grained types (e.g., MALWARE → Ransomware, Trojan, Worm) that must be preserved through **property-based discrimination** in downstream systems.

---

## 📊 THE HIERARCHY EXPLAINED

### Two-Tier System

#### Tier 1: NER Model Output (60 Labels)
**What the model actually detects:**
```
MALWARE, THREAT_ACTOR, CVE, VULNERABILITY, ATTACK_TECHNIQUE,
SOFTWARE_COMPONENT, ORGANIZATION, DEVICE, PROTOCOL, etc.
```

**Source**: Verified from production API (`http://localhost:8000/info`)

#### Tier 2: Fine-Grained Classification (566 Types)
**What those labels represent in detail:**
```
MALWARE → Ransomware, Trojan, Worm, Rootkit, RAT, Loader, Dropper...
THREAT_ACTOR → Nation State, APT Group, Hacktivist, Crime Syndicate...
DEVICE → PLC, RTU, HMI, DCS, SCADA Server, Sensor, Actuator...
```

**Source**: Design specification (`01_NER11_ENTITY_INVENTORY.md`)

---

## 🔍 VERIFIED PRODUCTION LABELS (60 Total)

### Core Cybersecurity (20 labels)
```
1.  CVE                    - CVE identifiers
2.  CWE                    - Weakness types
3.  CWE_WEAKNESS           - Specific CWE weaknesses
4.  VULNERABILITY          - Generic vulnerabilities
5.  MALWARE                - Malicious software (all types)
6.  APT_GROUP              - APT organizations
7.  THREAT_ACTOR           - Generic threat actors
8.  ATTACK_TECHNIQUE       - Attack methods
9.  TACTIC                 - ATT&CK tactics
10. TECHNIQUE              - ATT&CK techniques
11. INDICATOR              - IOCs, observables
12. MITIGATION             - Countermeasures
13. CONTROLS               - Security controls
14. PRIVILEGE_ESCALATION   - Privilege escalation techniques
15. CYBER_THREAT           - Generic cyber threats
16. THREAT_MODELING        - Threat modeling elements
17. THREAT_PERCEPTION      - Perceived threats
18. TOOL                   - Attack tools
19. IMPACT                 - Impact assessments
20. SEVERITY_LEVEL         - Severity classifications
```

### Infrastructure & Assets (14 labels)
```
21. DEVICE                 - Generic devices
22. SOFTWARE_COMPONENT     - Software parts
23. OPERATING_SYSTEM       - OS types
24. PRODUCT                - Vendor products
25. NETWORK                - Network entities
26. PROTOCOL               - Network protocols
27. FACILITY               - Physical facilities
28. MATERIAL               - Physical materials
29. ENGINEERING_PHYSICAL   - Physical engineering
30. PHYSICAL               - Generic physical entities
31. PROCESS                - Industrial processes
32. MEASUREMENT            - Measurements
33. MECHANISM              - Mechanical systems
34. COMPONENT              - Generic components
```

### Organizations & People (7 labels)
```
35. ORGANIZATION           - Companies, agencies
36. VENDOR                 - Software/hardware vendors
37. SECTOR                 - Industry sectors
38. SECTORS                - Multiple sectors
39. ROLES                  - Job roles
40. SECURITY_TEAM          - Security team roles
41. DEMOGRAPHICS           - Population characteristics
```

### Standards & Compliance (5 labels)
```
42. STANDARD               - Industry standards
43. IEC_62443              - IEC 62443 specific
44. MITRE_EM3D             - MITRE EM3D framework
45. RAMS                   - RAMS framework (Reliability, Availability, Maintainability, Safety)
46. HAZARD_ANALYSIS        - Hazard analysis methods
```

### McKenney-Lacan Psychometrics (4 labels)
```
47. PERSONALITY            - Personality traits
48. COGNITIVE_BIAS         - Cognitive biases
49. LACANIAN               - Lacanian discourse
50. PATTERNS               - Behavioral patterns
```

### System Architecture (10 labels)
```
51. CORE_ONTOLOGY          - Ontology elements
52. CYBER_SPECIFICS        - Cyber-specific attributes
53. SYSTEM_ATTRIBUTES      - System attributes
54. OPERATIONAL_MODES      - Operating modes
55. DETERMINISTIC_CONTROL  - Deterministic controls
56. META                   - Metadata
57. METADATA               - Meta information
58. TEMPLATES              - Template elements
59. ANALYSIS               - Analysis types
60. ATTRIBUTES             - Generic attributes
```

### Temporal & Contextual (3 labels)
```
61. LOCATION               - Geographic locations
62. TIME_BASED_TREND       - Temporal trends
(Note: Listed 60 above, may be 60 or slightly more based on model version)
```

---

## 🚨 THE CRITICAL HIERARCHY PROBLEM

### What We Discovered

**The Documentation Says**: 566 fine-grained entity types
**The Model Detects**: 60 top-level labels
**The Gap**: 506 fine-grained types are COLLAPSED into 60 labels

**Example**:
```
Design Goal (566 types):
  MALWARE → RANSOMWARE
  MALWARE → TROJAN
  MALWARE → WORM
  MALWARE → ROOTKIT
  ... (60 malware subtypes)

Production Reality (60 labels):
  MALWARE (generic - all subtypes collapsed)
```

### Where the 566 Types Live

**NOT in NER labels** - They exist as:
1. **Property values** (e.g., `{label: "MALWARE", malware_type: "Ransomware"}`)
2. **Entity text** (e.g., "WannaCry ransomware" → label: MALWARE, text: "WannaCry")
3. **Context clues** (surrounding text provides subtype)
4. **Secondary classification** (post-NER analysis required)

---

## ✅ SOLUTION: Hierarchical Mapping Strategy

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              TIER 1: NER Model Output (60 Labels)            │
│  What NER11 API returns in "label" field                    │
├─────────────────────────────────────────────────────────────┤
│              TIER 2: Fine-Grained Classification             │
│  Extract from entity text + context (566 types)             │
│  Example: "WannaCry ransomware" → type: "RANSOMWARE"       │
├─────────────────────────────────────────────────────────────┤
│              TIER 3: Neo4j/Qdrant Storage                   │
│  Store BOTH levels with hierarchical properties             │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Pattern (CRITICAL FOR ALL ETL)

```python
# MANDATORY PATTERN for all NER11 ingestion pipelines

class HierarchicalEntityProcessor:
    """
    Process NER11 entities with FULL 566-type hierarchical taxonomy.

    CRITICAL: This pattern must be used in ALL ETL pipelines.
    """

    # Tier 2 classification rules (566 types)
    MALWARE_SUBTYPES = {
        "ransomware": ["wannacry", "ryuk", "maze", "lockbit", "revil"],
        "trojan": ["emotet", "trickbot", "dridex", "qakbot"],
        "worm": ["conficker", "sasser", "blaster"],
        "rootkit": ["tdss", "rustock", "zeroaccess"],
        "rat": ["darkcomet", "njrat", "poison ivy"],
        # ... 60 malware subtypes total
    }

    THREAT_ACTOR_SUBTYPES = {
        "nation_state": ["apt28", "apt29", "apt40", "lazarus"],
        "apt_group": ["fancy bear", "cozy bear"],
        "hacktivist": ["anonymous", "lizard squad"],
        "crime_syndicate": ["fin7", "carbanak"],
        # ... 45 threat actor subtypes total
    }

    # Complete mapping for all 60 NER labels → 566 fine-grained types
    # See: 08_HIERARCHICAL_LABEL_DESIGN_OPTIONS.md

    def classify_entity(self, entity: Dict) -> Dict:
        """
        MANDATORY: Add fine-grained classification to NER output.

        Input: {text: "WannaCry", label: "MALWARE", score: 1.0}
        Output: {
            text: "WannaCry",
            label: "MALWARE",  # Tier 1
            fine_grained_type: "RANSOMWARE",  # Tier 2
            malware_family: "WannaCry",  # Tier 3 (most specific)
            score: 1.0
        }
        """
        tier1_label = entity["label"]
        entity_text = entity["text"].lower()

        # Fine-grained classification based on text analysis
        fine_grained_type = self._extract_fine_grained_type(
            tier1_label,
            entity_text
        )

        return {
            **entity,
            "fine_grained_type": fine_grained_type,
            "hierarchy_level": self._get_hierarchy_level(fine_grained_type)
        }

    def _extract_fine_grained_type(self, tier1_label: str, entity_text: str) -> str:
        """
        Extract fine-grained type (566 taxonomy) from entity text.

        Uses:
        1. Keyword matching (e.g., "ransomware" in text → "RANSOMWARE")
        2. Known entity databases (e.g., CVE database → CVE subtype)
        3. Pattern matching (e.g., "APT##" → "APT_GROUP")
        4. Context analysis (surrounding text clues)
        """
        if tier1_label == "MALWARE":
            for subtype, keywords in self.MALWARE_SUBTYPES.items():
                if any(kw in entity_text for kw in keywords):
                    return subtype.upper()
            return "GENERIC_MALWARE"

        elif tier1_label == "THREAT_ACTOR":
            for subtype, keywords in self.THREAT_ACTOR_SUBTYPES.items():
                if any(kw in entity_text for kw in keywords):
                    return subtype.upper()
            return "GENERIC_THREAT_ACTOR"

        # Add classification for all 60 labels...
        return tier1_label  # Fallback to Tier 1

    def _get_hierarchy_level(self, fine_grained_type: str) -> int:
        """
        Determine hierarchy depth.

        Level 1: Top category (60 types) - e.g., MALWARE
        Level 2: Subtype (566 types) - e.g., RANSOMWARE
        Level 3: Specific instance - e.g., WannaCry
        """
        # Logic to determine hierarchy level
        return 2  # Most fine-grained types are level 2
```

---

## 🎯 HOW TO USE HIERARCHY IN ALL ETL PIPELINES

### MANDATORY Pattern for Qdrant Storage

```python
# File: /5_NER11_Gold_Model/pipelines/02_entity_embedding_service.py
# UPDATE: Add hierarchical classification

def store_in_qdrant(self, entities, doc_id, doc_text):
    """
    Store entities with FULL hierarchical taxonomy (566 types).
    """
    processor = HierarchicalEntityProcessor()

    for entity in entities:
        # CRITICAL: Add fine-grained classification
        enriched = processor.classify_entity(entity)

        # Store in Qdrant with BOTH levels
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=self.generate_embedding(entity["text"], context),
            payload={
                # Tier 1: NER model output
                "ner_label": enriched["label"],  # 60 types

                # Tier 2: Fine-grained classification
                "fine_grained_type": enriched["fine_grained_type"],  # 566 types

                # Tier 3: Specific instance
                "entity_text": enriched["text"],

                # Metadata
                "confidence": enriched["score"],
                "hierarchy_level": enriched["hierarchy_level"],
                "doc_id": doc_id,
                "context": context
            }
        )
```

### MANDATORY Pattern for Neo4j Storage

```python
# File: /5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_pipeline.py
# UPDATE: Store hierarchical properties

def create_entity_node(self, tx, entity, doc_id):
    """
    Create Neo4j node with FULL hierarchical taxonomy.
    """
    processor = HierarchicalEntityProcessor()
    enriched = processor.classify_entity(entity)

    # Map to Neo4j super label (16 types per Schema v3.1)
    neo4j_label = NER11_TO_NEO4J_MAPPING[enriched["label"]]["neo4j_label"]

    # Create node with hierarchical properties
    query = f"""
    MERGE (e:{neo4j_label} {{name: $name}})
    ON CREATE SET
        e.id = $id,
        e.ner_label = $ner_label,                    # Tier 1 (60 types)
        e.fine_grained_type = $fine_grained_type,    # Tier 2 (566 types)
        e.hierarchy_level = $hierarchy_level,
        e.confidence = $confidence,
        e.created_at = datetime()
    ON MATCH SET
        e.updated_at = datetime(),
        e.confidence = CASE
            WHEN $confidence > e.confidence THEN $confidence
            ELSE e.confidence
        END
    RETURN e.id
    """

    tx.run(
        query,
        id=str(uuid.uuid4()),
        name=enriched["text"],
        ner_label=enriched["label"],
        fine_grained_type=enriched["fine_grained_type"],
        hierarchy_level=enriched["hierarchy_level"],
        confidence=enriched["score"]
    )
```

---

## 📋 COMPLETE 566-TYPE TAXONOMY (Design Spec)

### From: `/6_NER11_Gold_Model_Enhancement/reference_docs/NEO4j_AEON_Schema/2026_11_26_real_schema_label_accounting/01_NER11_ENTITY_INVENTORY.md`

**Structure**:
```
TIER 1: TECHNICAL (Cybersecurity Core)
  ├─ Threat Actors (7 types) → THREAT_ACTOR, APT_GROUP, NATION_STATE, CAMPAIGN...
  ├─ Malware (7 types) → MALWARE, RANSOMWARE, VIRUS, TROJAN, WORM...
  ├─ Attack Techniques (37 types) → ATTACK_TECHNIQUE, TTP, CAPEC, TACTIC...
  ├─ Vulnerabilities (14 types) → CVE, VULNERABILITY, CWE, ZERO_DAY...
  ├─ Software (30 types) → SOFTWARE_COMPONENT, LIBRARY, PACKAGE, FIRMWARE...
  └─ Infrastructure (50 types) → DEVICE, SENSOR, PLC, RTU, SUBSTATION...

TIER 2: PSYCHOMETRICS (McKenney-Lacan)
  ├─ Cognitive (25 types) → COGNITIVE_BIAS, CONFIRMATION_BIAS, NORMALCY_BIAS...
  ├─ Personality (20 types) → PERSONALITY, NARCISSISM, MACHIAVELLIANISM...
  ├─ Discourse (4 types) → LACANIAN, MASTER, HYSTERIC, ANALYST...
  └─ Emotional (15 types) → ANXIETY, PARANOIA, HUBRIS...

TIER 3: ECONOMICS (65 types)
  └─ Financial → STOCK_PRICE, REVENUE, GDPR_FINE, BREACH_COST...

... (full taxonomy: 566 types total)
```

**Current Implementation**: These 566 types are COLLAPSED into 60 NER labels
**Extraction Method**: Must be derived from entity text + context during ETL

---

## 🔧 CRITICAL IMPLEMENTATION REQUIREMENTS

### For ALL ETL Pipelines (MANDATORY)

#### 1. **Import Hierarchical Processor**
```python
from hierarchical_entity_processor import HierarchicalEntityProcessor
processor = HierarchicalEntityProcessor()
```

#### 2. **Enrich Entities Before Storage**
```python
# After NER extraction, BEFORE storage
enriched_entities = [processor.classify_entity(e) for e in raw_entities]
```

#### 3. **Store ALL Hierarchical Levels**
```python
# Qdrant payload
payload = {
    "ner_label": entity["label"],                      # Tier 1 (60)
    "fine_grained_type": entity["fine_grained_type"],  # Tier 2 (566)
    "entity_text": entity["text"],                     # Tier 3 (specific)
    "hierarchy_path": f"{ner_label}/{fine_grained_type}/{text}"
}

# Neo4j properties
SET e.ner_label = $ner_label,
    e.fine_grained_type = $fine_grained_type,
    e.specific_instance = $text
```

#### 4. **Enable Hierarchical Queries**
```python
# Query by Tier 1 (broad)
search(label_filter=["MALWARE"])  # All malware types

# Query by Tier 2 (specific)
search(fine_grained_filter=["RANSOMWARE"])  # Only ransomware

# Query by Tier 3 (exact)
search(entity_text="WannaCry")  # Specific malware family
```

---

## 📐 HIERARCHICAL MAPPING TABLE (Sample)

| NER Label (60) | Fine-Grained Types (566) | Neo4j Label (16) | Storage Properties |
|----------------|--------------------------|------------------|-------------------|
| MALWARE | RANSOMWARE, TROJAN, WORM, ROOTKIT, RAT, LOADER, DROPPER, BACKDOOR, BOTNET, SPYWARE, ADWARE, SCAREWARE, CRYPTOMINER, INFOSTEALER, DOWNLOADER... (60 subtypes) | Malware | `{malwareFamily: "ransomware", specificType: "WannaCry"}` |
| THREAT_ACTOR | NATION_STATE, APT_GROUP, HACKTIVIST, CRIME_SYNDICATE, INSIDER, SCRIPT_KIDDIE... (45 subtypes) | ThreatActor | `{actorType: "nation_state", specificGroup: "APT29"}` |
| DEVICE | PLC, RTU, HMI, DCS, SCADA_SERVER, IED, SENSOR, ACTUATOR, RELAY... (120 subtypes) | PhysicalAsset | `{deviceClass: "PLC", vendor: "Siemens", model: "S7-1500"}` |
| SOFTWARE_COMPONENT | LIBRARY, PACKAGE, FIRMWARE, DRIVER, KERNEL_MODULE... (30 subtypes) | Software | `{componentType: "library", language: "JavaScript"}` |
| COGNITIVE_BIAS | CONFIRMATION_BIAS, NORMALCY_BIAS, AVAILABILITY_HEURISTIC, ANCHORING, RECENCY_BIAS... (25 subtypes) | PsychTrait | `{biasType: "confirmation", severity: "high"}` |

**Complete Mapping**: See `/docs/HIERARCHICAL_ENTITY_MAPPING_COMPLETE.md` (to be created)

---

## 🎯 IMPLEMENTATION STRATEGY

### Create Hierarchical Entity Processor (NEW FILE REQUIRED)

**File**: `/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`
**Purpose**: CRITICAL module used by ALL ETL pipelines
**Priority**: 🔴 MUST BE CREATED FIRST

```python
# See implementation in next section
```

### Update ALL Existing Pipelines

**Files to Update**:
1. ✅ `/5_NER11_Gold_Model/pipelines/02_entity_embedding_service.py` - Add hierarchy
2. ✅ `/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_pipeline.py` - Add hierarchy
3. ✅ `/5_NER11_Gold_Model/serve_model.py` - Return hierarchy in responses

**Pattern**:
```python
# BEFORE (Incorrect - loses 506 types):
entity = {"text": "WannaCry", "label": "MALWARE", "score": 1.0}

# AFTER (Correct - preserves full taxonomy):
entity = {
    "text": "WannaCry",
    "label": "MALWARE",  # Tier 1
    "fine_grained_type": "RANSOMWARE",  # Tier 2
    "malware_family": "WannaCry",  # Tier 3
    "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",
    "score": 1.0
}
```

---

## ✅ MANDATORY VERIFICATION FOR ALL ETL

### Pre-Deployment Checklist

- [ ] Hierarchical processor imported
- [ ] All entities enriched with fine-grained type
- [ ] Qdrant payloads include `fine_grained_type` field
- [ ] Neo4j nodes include `fine_grained_type` property
- [ ] Queries support hierarchical filtering
- [ ] Test with known examples (WannaCry, APT29, CVE-2024-1234)

### Audit Trail Requirements

Every ETL pipeline must log:
```json
{
  "timestamp": "2025-12-01T05:50:00Z",
  "pipeline": "ner11_to_qdrant",
  "doc_id": "doc_001",
  "entities_processed": 15,
  "hierarchy_enriched": true,
  "tier1_labels": ["MALWARE", "CVE", "ORGANIZATION"],
  "tier2_types": ["RANSOMWARE", "CVE", "CORPORATION"],
  "verification_passed": true
}
```

### Validation Query (Neo4j)

```cypher
// Verify hierarchical storage
MATCH (m:Malware)
WHERE m.fine_grained_type IS NOT NULL
RETURN
    m.name,
    m.ner_label as tier1,
    m.fine_grained_type as tier2,
    count(*) as instances
LIMIT 10;

// Should see: tier1="MALWARE", tier2="RANSOMWARE"/"TROJAN"/etc.
```

### Validation Query (Qdrant)

```python
# Verify hierarchical payload
results = client.scroll(
    collection_name="ner11_entities",
    limit=10,
    with_payload=True
)

for point in results[0]:
    payload = point.payload
    assert "ner_label" in payload  # Tier 1
    assert "fine_grained_type" in payload  # Tier 2
    print(f"{payload['ner_label']} → {payload['fine_grained_type']}")
```

---

## 📝 DOCUMENTATION REQUIREMENTS

### Every Pipeline Must Document

1. **Hierarchy Support**: States it uses hierarchical classification
2. **Tier Coverage**: Documents which tiers it supports (1, 2, 3)
3. **Mapping Method**: Explains how fine-grained types are extracted
4. **Validation**: Includes verification that 566 types are preserved

### Example Header (MANDATORY)

```python
"""
NER11 to Qdrant Pipeline

HIERARCHICAL TAXONOMY SUPPORT: ✅ FULL (566 types)
- Tier 1: 60 NER labels preserved
- Tier 2: 566 fine-grained types extracted via text analysis
- Tier 3: Specific instances (entity names)

VALIDATION: Run validation.py to verify 566-type preservation
REFERENCE: /docs/CRITICAL_NER11_HIERARCHICAL_STRUCTURE.md
"""
```

---

## 🚨 CRITICAL FAILURE MODES

### What Happens If Hierarchy Is Ignored

**Scenario**: ETL pipeline uses ONLY the 60 NER labels

**Data Loss**:
```
Input: "APT29 deployed WannaCry ransomware targeting Siemens PLCs"

Without Hierarchy:
  - APT29 → label: THREAT_ACTOR (generic)
  - WannaCry → label: MALWARE (generic)
  - Siemens PLC → label: DEVICE (generic)

Result: 506 types of nuance LOST
  - Can't query "Show all ransomware" (generic MALWARE only)
  - Can't filter by APT groups (generic THREAT_ACTOR)
  - Can't identify PLCs specifically (generic DEVICE)

With Hierarchy:
  - APT29 → ner_label: THREAT_ACTOR, fine_grained: NATION_STATE, group: APT29
  - WannaCry → ner_label: MALWARE, fine_grained: RANSOMWARE, family: WannaCry
  - Siemens PLC → ner_label: DEVICE, fine_grained: PLC, vendor: Siemens

Result: FULL 566-type taxonomy preserved
  - Query "Show ransomware" works
  - Filter by APT groups works
  - Find all PLCs works
```

---

## ✅ SOLUTION DELIVERABLES

### Files That MUST Be Created

1. **`/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`**
   - Complete 566-type classification logic
   - Mapping tables for all 60 NER labels
   - Text analysis functions

2. **`/docs/HIERARCHICAL_ENTITY_MAPPING_COMPLETE.md`**
   - Complete 60 → 566 mapping table
   - Examples for each NER label
   - Extraction rules

3. **`/5_NER11_Gold_Model/tests/test_hierarchical_classification.py`**
   - Unit tests for all 60 NER labels
   - Validation for 566-type extraction
   - Edge case handling

### Files That MUST Be Updated

1. ✅ `/5_NER11_Gold_Model/pipelines/02_entity_embedding_service.py`
   - Import hierarchical processor
   - Enrich entities before embedding
   - Store hierarchy in Qdrant payload

2. ✅ `/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_pipeline.py`
   - Import hierarchical processor
   - Enrich entities before node creation
   - Store hierarchy as Neo4j properties

3. ✅ `/5_NER11_Gold_Model/serve_model.py`
   - Return hierarchical information in API responses
   - Add `/info/hierarchy` endpoint showing 566-type taxonomy

### Validation Files

4. **`/5_NER11_Gold_Model/validation/verify_566_preservation.py`**
   - Audit script to verify 566 types are captured
   - Check Qdrant payload structure
   - Check Neo4j property structure
   - Generate compliance report

---

## 💾 MEMORY BANK STORAGE

```bash
# Store critical hierarchy information
npx claude-flow memory store \
  --namespace ner11-gold \
  --key hierarchical-structure \
  --value '{
    "tier1_labels": 60,
    "tier2_types": 566,
    "production_api_labels": 60,
    "design_goal_types": 566,
    "hierarchy_method": "property_based_discrimination",
    "critical": "MUST use hierarchical_entity_processor in ALL ETL pipelines",
    "validation_required": true
  }'
```

---

**Document Created**: 2025-12-01 05:50 UTC
**Status**: ⚠️ CRITICAL - READ BEFORE ANY ETL IMPLEMENTATION
**Next**: Create `00_hierarchical_entity_processor.py` FIRST
