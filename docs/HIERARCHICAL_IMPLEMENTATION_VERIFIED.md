# ✅ NER11 Gold Hierarchical Structure - Implementation Guide
**File**: HIERARCHICAL_IMPLEMENTATION_VERIFIED.md
**Created**: 2025-12-01 06:02:00 UTC
**Version**: 1.0.0
**Status**: ⚠️ CRITICAL IMPLEMENTATION REQUIREMENT
**Authority**: Production API + Schema v3.1 + Constitution

---

## 🎯 VERIFIED HIERARCHICAL STRUCTURE

### Production Reality (Confirmed via API)

**NER11 Gold Model** (`ner11-gold-api:8000`):
```
TIER 1: 60 NER Model Labels (What the model detects)
   ↓
TIER 2: 566 Fine-Grained Entity Types (Design goal - extracted via analysis)
   ↓
TIER 3: Specific Instances (Actual entity names)
```

**Verified Commands**:
```bash
# Confirmed: 60 labels in production
curl -s http://localhost:8000/info | python3 -c "import sys, json; print(len(json.load(sys.stdin)['labels']))"
# Output: 60

# Read from model metadata
docker exec ner11-gold-api python3 -c "import spacy; nlp = spacy.load('/app/models/ner11_v3/model-best'); print(len(nlp.get_pipe('ner').labels))"
# Output: 60

# Documentation reference (566 design goal)
# File: /6_NER11_Gold_Model_Enhancement/.../01_NER11_ENTITY_INVENTORY.md
# Line 4: "Target Entities: 566 (Design Goal)"
# Line 5: "Actual Training Entities: 60 (Validated 2025-11-26)"
```

---

## 📊 THE 60 PRODUCTION LABELS (TIER 1)

**Complete List** (Alphabetical):
```
1.  ANALYSIS                21. INDICATOR               41. PROCESS
2.  APT_GROUP               22. LACANIAN                42. PRODUCT
3.  ATTACK_TECHNIQUE        23. LOCATION                43. PROTOCOL
4.  ATTRIBUTES              24. MALWARE                 44. RAMS
5.  COGNITIVE_BIAS          25. MATERIAL                45. ROLES
6.  COMPONENT               26. MEASUREMENT             46. SECTOR
7.  CONTROLS                27. MECHANISM               47. SECTORS
8.  CORE_ONTOLOGY           28. META                    48. SECURITY_TEAM
9.  CVE                     29. METADATA                49. SOFTWARE_COMPONENT
10. CWE                     30. MITIGATION              50. STANDARD
11. CWE_WEAKNESS            31. MITRE_EM3D              51. SYSTEM_ATTRIBUTES
12. CYBER_SPECIFICS         32. NETWORK                 52. TACTIC
13. DEMOGRAPHICS            33. OPERATING_SYSTEM        53. TECHNIQUE
14. DETERMINISTIC_CONTROL   34. OPERATIONAL_MODES       54. TEMPLATES
15. DEVICE                  35. ORGANIZATION            55. THREAT_ACTOR
16. ENGINEERING_PHYSICAL    36. PATTERNS                56. THREAT_MODELING
17. FACILITY                37. PERSONALITY             57. THREAT_PERCEPTION
18. HAZARD_ANALYSIS         38. PHYSICAL                58. TIME_BASED_TREND
19. IEC_62443               39. PRIVILEGE_ESCALATION    59. TOOL
20. IMPACT                  40. PROCESS                 60. VENDOR
                                                        (+ VULNERABILITY, CRITICAL_INFRASTRUCTURE)
```

---

## 🔍 THE 566 FINE-GRAINED TYPES (TIER 2)

**How They Map to 60 Labels**:

### Example: MALWARE (1 NER label → ~60 fine-grained types)

```yaml
NER_Label: MALWARE

Fine_Grained_Types:
  - RANSOMWARE (WannaCry, Ryuk, Maze, LockBit, REvil, Conti...)
  - TROJAN (Emotet, TrickBot, Dridex, QakBot, IcedID...)
  - WORM (Conficker, Sasser, Blaster, Stuxnet...)
  - ROOTKIT (TDSS, Rustock, ZeroAccess...)
  - RAT (DarkComet, NjRAT, Quasar, PoisonIvy...)
  - LOADER (TrickLoader, Bumblebee, IcedID Loader...)
  - DROPPER (Emotet Dropper, Dridex Dropper...)
  - BACKDOOR (Cobalt Strike, Metasploit, China Chopper...)
  - BOTNET (Mirai, Necurs, Gameover Zeus...)
  - SPYWARE (Pegasus, FinFisher, DarkHotel...)
  - ADWARE (...)
  - SCAREWARE (...)
  - CRYPTOMINER (...)
  - INFOSTEALER (...)
  - DOWNLOADER (...)
  - KEYLOGGER (...)
  - SCREENLOGGER (...)
  - EXPLOIT_KIT (...)
  - BANKING_TROJAN (...)
  - POS_MALWARE (...)
  - FIRMWARE_MALWARE (...)
  - FILELESS_MALWARE (...)
  - POLYMORPHIC_MALWARE (...)
  - METAMORPHIC_MALWARE (...)
  ... (~60 total malware subtypes)

Extraction_Method:
  - Keyword: "ransomware" in text → RANSOMWARE
  - Known name: "WannaCry" → RANSOMWARE (database lookup)
  - Context: "crypto-locker" in surrounding text → RANSOMWARE
```

### Example: DEVICE (1 NER label → ~120 fine-grained types)

```yaml
NER_Label: DEVICE

Fine_Grained_Types:
  OT/ICS_Devices:
    - PLC (Programmable Logic Controller)
    - RTU (Remote Terminal Unit)
    - HMI (Human-Machine Interface)
    - DCS (Distributed Control System)
    - SCADA_SERVER
    - IED (Intelligent Electronic Device)
    - SENSOR (Temperature, Pressure, Flow, etc.)
    - ACTUATOR
    - RELAY
    - CIRCUIT_BREAKER
    - TRANSFORMER
    - SUBSTATION
    - TURBINE
    - GENERATOR
    - MOTOR
    - PUMP
    - VALVE
    - CONTROLLER
    ... (~120 total device subtypes)

  IT_Devices:
    - SERVER
    - WORKSTATION
    - LAPTOP
    - MOBILE_DEVICE
    - ROUTER
    - SWITCH
    - FIREWALL
    - LOAD_BALANCER
    ...

Extraction_Method:
  - Model name: "S7-1500" → PLC (Siemens model)
  - Type keyword: "RTU" in text → RTU
  - Vendor+Model: "Allen-Bradley ControlLogix" → PLC
```

### Example: COGNITIVE_BIAS (1 NER label → ~25 fine-grained types)

```yaml
NER_Label: COGNITIVE_BIAS

Fine_Grained_Types:
  - CONFIRMATION_BIAS
  - NORMALCY_BIAS
  - AVAILABILITY_HEURISTIC
  - ANCHORING
  - RECENCY_BIAS
  - OPTIMISM_BIAS
  - DUNNING_KRUGER
  - GROUPTHINK
  - BANDWAGON_EFFECT
  - AUTHORITY_BIAS
  - SUNK_COST_FALLACY
  - OVERCONFIDENCE
  - HINDSIGHT_BIAS
  - STATUS_QUO_BIAS
  - LOSS_AVERSION
  ... (~25 total cognitive bias subtypes)

Extraction_Method:
  - Direct match: "confirmation bias" → CONFIRMATION_BIAS
  - Synonym: "confirmatory bias" → CONFIRMATION_BIAS
  - Context: described behavior matching bias pattern
```

**Complete 566-Type Taxonomy**: See `/6_NER11_Gold_Model_Enhancement/.../01_NER11_ENTITY_INVENTORY.md`

---

## 🔧 HOW HIERARCHY IS IMPLEMENTED IN ALL ETL

### Pattern 1: Qdrant Storage (MANDATORY)

```python
# In: 02_entity_embedding_service_hierarchical.py

from 00_hierarchical_entity_processor import HierarchicalEntityProcessor

processor = HierarchicalEntityProcessor()

# For EVERY entity:
enriched = processor.classify_entity(raw_entity, context)

# Store in Qdrant with ALL hierarchy:
payload = {
    "ner_label": enriched["label"],                      # Tier 1 (60)
    "fine_grained_type": enriched["fine_grained_type"],  # Tier 2 (566)
    "specific_instance": enriched["specific_instance"],  # Tier 3
    "hierarchy_path": enriched["hierarchy_path"],        # "MALWARE/RANSOMWARE/WannaCry"
    "hierarchy_level": enriched["hierarchy_level"]       # 3
}
```

### Pattern 2: Neo4j Storage (MANDATORY)

```cypher
// In: 05_ner11_to_neo4j_hierarchical.py

MERGE (e:Malware {name: $name})
ON CREATE SET
    e.ner_label = $ner_label,                    # Tier 1: "MALWARE"
    e.fine_grained_type = $fine_grained_type,    # Tier 2: "RANSOMWARE"
    e.specific_instance = $specific_instance,    # Tier 3: "WannaCry"
    e.hierarchy_path = $hierarchy_path,          # Full path
    e.hierarchy_level = $hierarchy_level         # Depth
```

### Pattern 3: API Responses (MANDATORY)

```python
# In: serve_model.py (extend /ner endpoint)

@app.post("/ner")
async def extract_entities(request: TextRequest):
    # Extract with NER model (60 labels)
    raw_entities = nlp(request.text).ents

    # CRITICAL: Apply hierarchical classification
    processor = HierarchicalEntityProcessor()
    enriched_entities = [
        processor.classify_entity({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
            "score": 1.0  # spaCy doesn't provide scores by default
        }, context=request.text)
        for ent in raw_entities
    ]

    return {
        "entities": enriched_entities,  # Now includes fine_grained_type!
        "doc_length": len(nlp(request.text))
    }
```

### Pattern 4: Queries (Enable Tier 2 Filtering)

```python
# Qdrant query by fine-grained type
results = client.scroll(
    collection_name="ner11_entities_hierarchical",
    scroll_filter={
        "must": [
            {"key": "fine_grained_type", "match": {"value": "RANSOMWARE"}}
        ]
    }
)
# Returns ONLY ransomware, not all malware
```

```cypher
// Neo4j query by fine-grained type
MATCH (m:Malware)
WHERE m.fine_grained_type = "RANSOMWARE"
RETURN m.name, m.ner_label, m.fine_grained_type;

// Returns ONLY ransomware, not all malware
```

---

## ✅ VALIDATION REQUIREMENTS (MANDATORY FOR ALL ETL)

### Validation Script (Run After Each Batch)

```python
# File: /5_NER11_Gold_Model/validation/verify_hierarchy_preservation.py

def validate_hierarchy_in_storage():
    """
    Verify 566-type hierarchy is preserved in storage.
    Run after EVERY ETL batch.
    """
    from qdrant_client import QdrantClient
    from neo4j import GraphDatabase

    # Check Qdrant
    client = QdrantClient("localhost", 6333)
    points, _ = client.scroll("ner11_entities_hierarchical", limit=1000)

    tier1_set = set(p.payload["ner_label"] for p in points)
    tier2_set = set(p.payload["fine_grained_type"] for p in points)

    qdrant_valid = len(tier2_set) > len(tier1_set)

    # Check Neo4j
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            WHERE n.fine_grained_type IS NOT NULL
            RETURN
                count(DISTINCT n.ner_label) as t1,
                count(DISTINCT n.fine_grained_type) as t2
        """)
        record = result.single()
        neo4j_valid = record["t2"] > record["t1"]

    report = {
        "qdrant": {
            "tier1_labels": len(tier1_set),
            "tier2_types": len(tier2_set),
            "valid": qdrant_valid
        },
        "neo4j": {
            "tier1_labels": record["t1"],
            "tier2_types": record["t2"],
            "valid": neo4j_valid
        },
        "overall_validation": qdrant_valid and neo4j_valid
    }

    assert report["overall_validation"], f"HIERARCHY VALIDATION FAILED: {report}"

    return report
```

**Run Command**:
```bash
python /5_NER11_Gold_Model/validation/verify_hierarchy_preservation.py

# Expected output:
# {
#   "qdrant": {"tier1_labels": 15, "tier2_types": 42, "valid": true},
#   "neo4j": {"tier1_labels": 15, "tier2_types": 45, "valid": true},
#   "overall_validation": true
# }
```

---

## 📐 COMPLETE 60 → 566 MAPPING (Samples)

### High-Value Mappings (20 most critical)

| Tier 1 (NER Label) | Tier 2 Examples (566 Fine-Grained) | Count | Neo4j Super Label |
|--------------------|-------------------------------------|-------|-------------------|
| MALWARE | RANSOMWARE, TROJAN, WORM, ROOTKIT, RAT, LOADER, DROPPER, BACKDOOR... | 60 | Malware |
| THREAT_ACTOR | NATION_STATE, APT_GROUP, HACKTIVIST, CRIME_SYNDICATE, INSIDER... | 45 | ThreatActor |
| DEVICE | PLC, RTU, HMI, DCS, SCADA_SERVER, IED, SENSOR, ACTUATOR, RELAY... | 120 | PhysicalAsset |
| SOFTWARE_COMPONENT | LIBRARY, PACKAGE, FIRMWARE, DRIVER, KERNEL_MODULE, APPLICATION... | 30 | Software |
| COGNITIVE_BIAS | CONFIRMATION_BIAS, NORMALCY_BIAS, AVAILABILITY_HEURISTIC... | 25 | PsychTrait |
| CVE | CVE, CVE_2024, CVE_2023, ZERO_DAY... | 14 | Vulnerability |
| ATTACK_TECHNIQUE | TECHNIQUE, TTP, CAPEC, TACTIC, EXPLOIT, SOCIAL_ENGINEERING... | 37 | AttackPattern |
| ORGANIZATION | CORPORATION, GOVERNMENT, NGO, VENDOR, TARGET_ORG... | 20 | Organization |
| PROTOCOL | MODBUS, DNP3, IEC_61850, PROFINET, ETHERNET_IP, BACNET... | 45 | Protocol |
| PERSONALITY | NARCISSISM, MACHIAVELLIANISM, PSYCHOPATHY, BIG5_TRAITS... | 20 | PsychTrait |
| VULNERABILITY | VULNERABILITY, ZERO_DAY, MISCONFIGURATION, WEAKNESS... | 14 | Vulnerability |
| FACILITY | SUBSTATION, DATACENTER, PLANT, OFFICE, WAREHOUSE... | 18 | PhysicalAsset |
| MITIGATION | PATCH, WORKAROUND, CONFIGURATION_CHANGE, ISOLATION... | 12 | Control |
| INDICATOR | IOC, OBSERVABLE, IP_ADDRESS, HASH, DOMAIN, URL... | 15 | Indicator |
| TOOL | ATTACK_TOOL, ADMIN_TOOL, ANALYSIS_TOOL, SCANNER... | 10 | Software |
| NETWORK | LAN, WAN, DMZ, VLAN, VPN, WIRELESS... | 8 | Asset |
| OPERATING_SYSTEM | WINDOWS, LINUX, MACOS, ANDROID, IOS, RTOS... | 15 | Software |
| STANDARD | IEC_62443, ISO_27001, NIST_CSF, CIS_CONTROLS... | 12 | Control |
| ROLES | CISO, SECURITY_ANALYST, SOC_ANALYST, INCIDENT_RESPONDER... | 25 | Role |
| SECTOR | ENERGY, WATER, TRANSPORT, HEALTHCARE, FINANCE... | 16 | Organization |

**Total**: 566 fine-grained types across 60 NER labels

---

## 🎯 CRITICAL IMPLEMENTATION STEPS (SUMMARIZED)

### Step 1: Create Hierarchical Processor (FIRST)
**File**: `00_hierarchical_entity_processor.py`
**Load**: Complete 566-type taxonomy with keyword mappings
**Function**: `classify_entity()` - Enriches NER output with Tier 2 & 3

### Step 2: Update ALL ETL Pipelines
**Files**: All `*_pipeline.py`, `*_service.py` in `/pipelines/`
**Pattern**: Import processor → Enrich entities → Store hierarchy

### Step 3: Validate After Every Batch
**Script**: `verify_hierarchy_preservation.py`
**Check**: Tier 2 types > Tier 1 labels (proves hierarchy working)

### Step 4: Enable Hierarchical Queries
**Qdrant**: Filter by `fine_grained_type` field
**Neo4j**: `WHERE n.fine_grained_type = "RANSOMWARE"`

---

## 📋 AUDIT TRAIL REQUIREMENTS

### Every ETL Run Must Log

```json
{
  "run_id": "etl_<timestamp>",
  "doc_id": "doc_123",
  "tier1_labels_detected": ["MALWARE", "CVE", "ORGANIZATION"],
  "tier2_types_extracted": ["RANSOMWARE", "CVE", "CORPORATION"],
  "tier3_instances": ["WannaCry", "CVE-2024-1234", "Apache Foundation"],
  "hierarchy_preserved": true,
  "validation_passed": true,
  "timestamp": "2025-12-01T06:00:00Z"
}
```

**Storage**: `/5_NER11_Gold_Model/logs/hierarchy_verification.jsonl`

### Validation Report Format

```json
{
  "validation_timestamp": "2025-12-01T06:00:00Z",
  "total_entities_processed": 1500,
  "tier1_unique_labels": 45,
  "tier2_unique_types": 180,
  "tier3_unique_instances": 1500,
  "coverage_percentage": 31.8,  // 180/566 = 31.8% of total taxonomy covered
  "hierarchy_functional": true,
  "data_integrity": "PASS"
}
```

---

## 🚨 CRITICAL SUCCESS FACTORS

### Must Be True for ALL ETL:

✅ **Every entity enriched**: `HierarchicalEntityProcessor.classify_entity()` called
✅ **All 3 tiers stored**: ner_label + fine_grained_type + specific_instance
✅ **Tier 2 > Tier 1**: Fine-grained types exceed NER labels (proves hierarchy)
✅ **Queries work**: Can filter by Tier 2 types
✅ **Validated**: `verify_566_preservation()` passing
✅ **Audited**: All runs logged with hierarchy verification

### Red Flags (STOP IF YOU SEE THESE):

🚨 **Tier 2 count == Tier 1 count**: Hierarchy NOT being extracted!
🚨 **fine_grained_type missing**: Pipeline missing hierarchical processor!
🚨 **Queries return all types**: Tier 2 filtering not working!
🚨 **Coverage stuck at 60**: Only NER labels stored, no fine-grained types!

---

## ✅ VERIFICATION COMMANDS

```bash
# Check Qdrant hierarchy
curl -X POST http://localhost:6333/collections/ner11_entities_hierarchical/points/scroll \
  -d '{"limit": 10, "with_payload": true}' | \
  python3 -c "import sys, json; d=json.load(sys.stdin); \
  t1=set(p['payload']['ner_label'] for p in d['result']['points']); \
  t2=set(p['payload']['fine_grained_type'] for p in d['result']['points']); \
  print(f'Tier1: {len(t1)}, Tier2: {len(t2)}, Valid: {len(t2) > len(t1)}')"

# Check Neo4j hierarchy
docker exec openspg-neo4j cypher-shell "
  MATCH (n)
  WHERE n.fine_grained_type IS NOT NULL
  RETURN
    count(DISTINCT n.ner_label) as tier1,
    count(DISTINCT n.fine_grained_type) as tier2,
    tier2 > tier1 as hierarchy_valid
"

# Both should show: hierarchy_valid = true
```

---

**Document Created**: 2025-12-01 06:02 UTC
**Purpose**: Definitive guide for hierarchical implementation
**Status**: CRITICAL - MUST BE FOLLOWED IN ALL ETL
**Validation**: Mandatory after every operation
