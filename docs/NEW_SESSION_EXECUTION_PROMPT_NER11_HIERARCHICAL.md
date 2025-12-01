# 🤖 NEW SESSION EXECUTION PROMPT - NER11 Gold Hierarchical Integration

**PROMPT FOR**: Any LLM (Claude, GPT-4, etc.)
**SESSION TYPE**: Implementation
**ESTIMATED DURATION**: 12-16 hours (across multiple phases)
**COMPLEXITY**: HIGH - Requires precision, auditing, verification at each step

---

## 📋 YOUR MISSION

You are tasked with implementing the **NER11 Gold Standard hierarchical integration** with the AEON Digital Twin platform. This is a **CRITICAL PRODUCTION IMPLEMENTATION** that must preserve the full 566-entity hierarchical taxonomy while extending (NOT replacing) existing systems.

**SUCCESS = Working code + Passing tests + Zero data loss + Full audit trail**

---

## 🚨 CRITICAL CONTEXT (READ FIRST)

### The Hierarchical Structure You MUST Preserve

**NER11 Gold uses a 3-tier hierarchical taxonomy**:

```
TIER 1: 60 NER Model Labels
  ↓ (what the model detects)
TIER 2: 566 Fine-Grained Entity Types
  ↓ (extracted via text analysis & context)
TIER 3: Specific Instances
  ↓ (actual entity names: "WannaCry", "APT29", etc.)
```

**Example**:
```
Detection: "APT29 deployed WannaCry ransomware targeting Siemens S7-1500 PLCs"

Tier 1 (NER Labels): THREAT_ACTOR, MALWARE, DEVICE
Tier 2 (Fine-Grained): NATION_STATE, RANSOMWARE, PLC
Tier 3 (Specific): APT29, WannaCry, Siemens S7-1500

CRITICAL: ALL THREE TIERS must be captured and stored!
```

### What You're Integrating With (DO NOT REPLACE)

**Production Infrastructure** (ALL OPERATIONAL):
- `ner11-gold-api` (port 8000) - NER extraction API
- `openspg-neo4j` (ports 7474/7687) - Knowledge graph (570K nodes existing)
- `openspg-qdrant` (ports 6333-6334) - Vector database
- `aeon-saas-dev` (port 3000) - Next.js frontend with Clerk auth
- `openspg-server` (port 8887) - OpenSPG knowledge graph engine
- `aeon-postgres-dev` (port 5432) - Application state
- `openspg-mysql` (port 3306) - OpenSPG metadata

**ABSOLUTE RULE**: EXTEND these systems, NEVER create parallel/duplicate systems.

---

## 📚 REQUIRED READING (IN ORDER - 2 hours)

### Phase 0: Context Loading (MANDATORY)

**Read these files IN THIS EXACT ORDER before writing any code**:

#### 1. Governing Documents (30 min)
- [ ] `/1_AEON_DT_CyberSecurity_Wiki_Current/00_AEON_CONSTITUTION.md`
  - Read Article I (Foundational Principles)
  - Read Article I, Section 1.2 (Non-Negotiable Rules)
  - Note Rule #2: "ALWAYS USE EXISTING RESOURCES"
  - Note Rule #3: "NO DEVELOPMENT THEATER"

#### 2. Critical Hierarchy Documentation (45 min)
- [ ] `/docs/CRITICAL_NER11_HIERARCHICAL_STRUCTURE.md`
  - Understand 60 vs 566 entity structure
  - Review hierarchical mapping pattern
  - Note mandatory verification requirements

- [ ] `/6_NER11_Gold_Model_Enhancement/reference_docs/NEO4j_AEON_Schema/2026_11_26_real_schema_label_accounting/01_NER11_ENTITY_INVENTORY.md`
  - Complete 566 entity type list
  - Tier-by-tier organization
  - Fine-grained classification rules

- [ ] `/6_NER11_Gold_Model_Enhancement/reference_docs/NEO4j_AEON_Schema/2026_11_26_real_schema_label_accounting/08_HIERARCHICAL_LABEL_DESIGN_OPTIONS.md`
  - Option B (Domain Specialist) - RECOMMENDED APPROACH
  - 16 super labels with property discrimination
  - Example hierarchies

#### 3. Schema Specifications (30 min)
- [ ] `/6_NER11_Gold_Model_Enhancement/NER11_Gold_Model_Enhancement/neo4j_integration/01_SCHEMA_V3.1_SPECIFICATION.md`
  - 16 Super Labels definition
  - Property schemas for each label
  - Index requirements
  - Hierarchical property patterns

- [ ] `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/Neo4j-Schema-Enhanced.md`
  - Current schema v3.0 (11 node types, 16 relationships)
  - Customer & Tag nodes
  - MITRE ATT&CK integration

#### 4. Implementation Guides (15 min)
- [ ] `/docs/TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md`
  - Complete 4-phase implementation plan
  - Code examples for each task
  - Integration points
  - Verification procedures

- [ ] `/docs/NER11_GOLD_STATUS_REPORT_2025-12-01.md`
  - Current production status
  - API verification results
  - Infrastructure health

---

## ✅ PHASE 0: PRE-FLIGHT VERIFICATION (30 min)

### Step 0.1: Verify Infrastructure (10 min)

**Execute these commands and VERIFY all pass**:

```bash
# Check all containers running
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "ner11|neo4j|qdrant|aeon-saas"

# VERIFY OUTPUT includes:
# ner11-gold-api      Up X minutes (healthy)
# openspg-neo4j       Up X minutes (healthy)
# openspg-qdrant      Up X minutes
# aeon-saas-dev       Up X minutes (healthy)

# Test NER11 API
curl http://localhost:8000/health

# VERIFY: {"status":"healthy","model":"loaded"}

# Count NER labels
curl -s http://localhost:8000/info | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'Labels: {len(d[\"labels\"])}')"

# VERIFY: Labels: 60

# Test Qdrant
curl http://localhost:6333/collections

# VERIFY: JSON response with collections list

# Test Neo4j
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) as total"

# VERIFY: total > 500,000 (existing nodes)
```

**AUDIT CHECKPOINT #0**:
```json
{
  "checkpoint": "pre-flight",
  "timestamp": "<current_time>",
  "containers_healthy": true,
  "ner11_api_operational": true,
  "ner11_labels_verified": 60,
  "neo4j_existing_nodes": "<count>",
  "qdrant_accessible": true,
  "ready_to_proceed": true
}
```

**ACTION**: Store checkpoint in `/5_NER11_Gold_Model/logs/audit_trail.jsonl`:
```bash
echo '<checkpoint_json>' >> /5_NER11_Gold_Model/logs/audit_trail.jsonl
```

### Step 0.2: Load Memory Bank (10 min)

```bash
# Retrieve session state
npx claude-flow memory list --namespace ner11-gold

# Get critical context
npx claude-flow memory retrieve --namespace ner11-gold --key hierarchical-structure-critical
npx claude-flow memory retrieve --namespace ner11-gold --key gap-002-commit
npx claude-flow memory retrieve --namespace ner11-gold --key api-status
```

**AUDIT CHECKPOINT #1**:
```json
{
  "checkpoint": "memory-loaded",
  "timestamp": "<current_time>",
  "memory_keys_found": "<count>",
  "gap_002_committed": true,
  "hierarchical_structure_documented": true,
  "previous_session_context": "loaded"
}
```

### Step 0.3: Create Audit Log (10 min)

**Create audit system** (MANDATORY for all operations):

```bash
# Create audit log file
mkdir -p /5_NER11_Gold_Model/logs
touch /5_NER11_Gold_Model/logs/audit_trail.jsonl
touch /5_NER11_Gold_Model/logs/hierarchy_verification.jsonl
touch /5_NER11_Gold_Model/logs/data_integrity.jsonl

# Initialize audit entry
cat > /5_NER11_Gold_Model/logs/session_start.json << 'EOF'
{
  "session_id": "ner11-hierarchical-<YYYYMMDD-HHMMSS>",
  "started_at": "<timestamp>",
  "mission": "NER11 Gold hierarchical integration (60 labels → 566 types)",
  "llm_model": "<your_model_name>",
  "taskmaster_version": "2.0.0",
  "constitution_version": "1.0.0",
  "schema_target": "v3.1 (16 super labels)",
  "hierarchy_requirement": "CRITICAL - preserve all 566 fine-grained types"
}
EOF
```

---

## 🎯 PHASE 1: HIERARCHICAL ENTITY PROCESSOR (CRITICAL - DO THIS FIRST)

**TIME**: 3-4 hours
**PRIORITY**: 🔴 BLOCKING - Nothing else can proceed without this

### Task 1.1: Create Hierarchical Entity Processor (2-3 hours)

**CREATE FILE**: `/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`

**REQUIREMENTS**:
1. Import the complete 566-entity taxonomy
2. Classify entities from 60 NER labels to 566 fine-grained types
3. Extract hierarchy from entity text + context
4. Provide validation functions

**IMPLEMENTATION TEMPLATE**: (You must complete this with full 566-type logic)

```python
"""
Hierarchical Entity Processor for NER11 Gold Standard

CRITICAL COMPONENT: Used by ALL ETL pipelines
HIERARCHY: 60 NER labels → 566 fine-grained types → specific instances
VALIDATION: MANDATORY - verify 566-type preservation

Authority: /docs/CRITICAL_NER11_HIERARCHICAL_STRUCTURE.md
Reference: /6_NER11_Gold_Model_Enhancement/.../01_NER11_ENTITY_INVENTORY.md
"""

from typing import Dict, List, Optional
import re

class HierarchicalEntityProcessor:
    """
    Process NER11 entities with full 566-type hierarchical taxonomy.

    MUST BE USED IN:
    - Qdrant ingestion
    - Neo4j ingestion
    - API responses
    - All entity processing

    VALIDATION: Run verify_566_preservation() after each batch
    """

    def __init__(self):
        # Load complete 566-type taxonomy
        self.taxonomy = self._load_taxonomy()

    def _load_taxonomy(self) -> Dict:
        """
        Load complete 566-entity taxonomy organized by 60 NER labels.

        Structure:
        {
          "MALWARE": {
            "fine_grained_types": ["RANSOMWARE", "TROJAN", "WORM", ...],
            "keywords": {
              "RANSOMWARE": ["ransomware", "crypto-locker", "wannacry", "ryuk"],
              "TROJAN": ["trojan", "backdoor", "emotet", "trickbot"],
              ...
            }
          },
          ... (all 60 labels)
        }
        """
        return {
            "MALWARE": {
                "fine_grained_types": [
                    "RANSOMWARE", "TROJAN", "WORM", "ROOTKIT", "RAT",
                    "LOADER", "DROPPER", "BACKDOOR", "BOTNET", "SPYWARE",
                    "ADWARE", "SCAREWARE", "CRYPTOMINER", "INFOSTEALER",
                    "DOWNLOADER", "KEYLOGGER", "SCREENLOGGER", "EXPLOIT_KIT",
                    "BANKING_TROJAN", "POS_MALWARE", "FIRMWARE_MALWARE",
                    "FILELESS_MALWARE", "POLYMORPHIC_MALWARE", "METAMORPHIC_MALWARE",
                    # ... continue for all ~60 malware subtypes
                ],
                "keywords": {
                    "RANSOMWARE": ["ransomware", "crypto", "locker", "wannacry", "ryuk", "maze", "lockbit", "revil", "conti", "darkside"],
                    "TROJAN": ["trojan", "emotet", "trickbot", "dridex", "qakbot", "icedid"],
                    "WORM": ["worm", "conficker", "sasser", "blaster", "stuxnet"],
                    "RAT": ["rat", "remote access", "darkcomet", "njrat", "quasar"],
                    # ... complete for all types
                }
            },

            "THREAT_ACTOR": {
                "fine_grained_types": [
                    "NATION_STATE", "APT_GROUP", "HACKTIVIST", "CRIME_SYNDICATE",
                    "INSIDER", "SCRIPT_KIDDIE", "STATE_SPONSORED", "TERRORIST_GROUP",
                    # ... continue for all ~45 threat actor subtypes
                ],
                "keywords": {
                    "NATION_STATE": ["nation state", "state-sponsored", "government"],
                    "APT_GROUP": ["apt", "apt28", "apt29", "apt40", "fancy bear", "cozy bear", "lazarus"],
                    "HACKTIVIST": ["anonymous", "lizard squad", "hacktivist"],
                    "CRIME_SYNDICATE": ["fin7", "carbanak", "cobalt", "crime"],
                    # ... complete for all types
                }
            },

            "DEVICE": {
                "fine_grained_types": [
                    "PLC", "RTU", "HMI", "DCS", "SCADA_SERVER", "IED", "SENSOR",
                    "ACTUATOR", "RELAY", "BREAKER", "TRANSFORMER", "SUBSTATION",
                    "TURBINE", "GENERATOR", "MOTOR", "PUMP", "VALVE", "CONTROLLER",
                    # ... continue for all ~120 device subtypes
                ],
                "keywords": {
                    "PLC": ["plc", "programmable logic controller", "s7-", "controllogix"],
                    "RTU": ["rtu", "remote terminal unit"],
                    "HMI": ["hmi", "human machine interface", "scada screen"],
                    "DCS": ["dcs", "distributed control system"],
                    # ... complete for all types
                }
            },

            "COGNITIVE_BIAS": {
                "fine_grained_types": [
                    "CONFIRMATION_BIAS", "NORMALCY_BIAS", "AVAILABILITY_HEURISTIC",
                    "ANCHORING", "RECENCY_BIAS", "OPTIMISM_BIAS", "DUNNING_KRUGER",
                    # ... continue for all ~25 cognitive bias subtypes
                ],
                "keywords": {
                    "CONFIRMATION_BIAS": ["confirmation bias", "confirmatory"],
                    "NORMALCY_BIAS": ["normalcy bias", "normality bias"],
                    "AVAILABILITY_HEURISTIC": ["availability heuristic", "availability bias"],
                    # ... complete for all types
                }
            },

            # ... CONTINUE FOR ALL 60 NER LABELS
            # Full taxonomy available in:
            # /6_NER11_Gold_Model_Enhancement/.../01_NER11_ENTITY_INVENTORY.md
        }

    def classify_entity(self, entity: Dict, context: str = "") -> Dict:
        """
        Add hierarchical classification to NER output.

        Input (from NER11 API):
          {
            "text": "WannaCry",
            "label": "MALWARE",  # Tier 1 (60 types)
            "start": 0,
            "end": 8,
            "score": 1.0
          }

        Output (hierarchically enriched):
          {
            "text": "WannaCry",
            "label": "MALWARE",  # Tier 1
            "fine_grained_type": "RANSOMWARE",  # Tier 2 (566 types)
            "specific_instance": "WannaCry",  # Tier 3
            "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",
            "hierarchy_level": 3,
            "start": 0,
            "end": 8,
            "score": 1.0,
            "classification_method": "keyword_match",  # or "context_analysis", "database_lookup"
            "classification_confidence": 0.95
          }

        MANDATORY: Every entity MUST have fine_grained_type populated
        """
        tier1_label = entity["label"]
        entity_text = entity["text"].lower()

        # Get taxonomy for this NER label
        if tier1_label not in self.taxonomy:
            # Unmapped NER label - use generic
            return {
                **entity,
                "fine_grained_type": tier1_label,
                "specific_instance": entity["text"],
                "hierarchy_path": f"{tier1_label}/{tier1_label}/{entity['text']}",
                "hierarchy_level": 1,
                "classification_method": "unmapped",
                "classification_confidence": 0.5
            }

        label_taxonomy = self.taxonomy[tier1_label]

        # Extract fine-grained type via keyword matching
        fine_grained_type = self._extract_fine_grained_type(
            entity_text,
            context,
            label_taxonomy
        )

        # Build enriched entity
        enriched = {
            **entity,
            "fine_grained_type": fine_grained_type,
            "specific_instance": entity["text"],
            "hierarchy_path": f"{tier1_label}/{fine_grained_type}/{entity['text']}",
            "hierarchy_level": 3 if fine_grained_type != tier1_label else 1,
            "classification_method": self._get_classification_method(entity_text, fine_grained_type, label_taxonomy),
            "classification_confidence": self._calculate_classification_confidence(entity_text, fine_grained_type, label_taxonomy)
        }

        return enriched

    def _extract_fine_grained_type(
        self,
        entity_text: str,
        context: str,
        label_taxonomy: Dict
    ) -> str:
        """
        Extract fine-grained type (Tier 2) from entity text and context.

        Methods (in priority order):
        1. Keyword matching in entity text
        2. Keyword matching in context
        3. Pattern matching (e.g., CVE-YYYY-NNNNN → CVE)
        4. Database lookup (for known entities)
        5. Default to NER label if no match
        """
        # Method 1: Direct keyword match in entity text
        for fine_type, keywords in label_taxonomy.get("keywords", {}).items():
            if any(kw in entity_text for kw in keywords):
                return fine_type

        # Method 2: Context keyword match
        if context:
            context_lower = context.lower()
            for fine_type, keywords in label_taxonomy.get("keywords", {}).items():
                if any(kw in context_lower for kw in keywords):
                    return fine_type

        # Method 3: Pattern matching
        # Example: APT## → APT_GROUP
        if re.match(r'apt\d+', entity_text):
            return "APT_GROUP"

        # Example: CVE-YYYY-NNNNN → CVE
        if re.match(r'cve-\d{4}-\d+', entity_text):
            return "CVE"

        # Method 4: Database lookup (implement for known entities)
        # TODO: Check against known entity databases

        # Method 5: Default to first fine-grained type or NER label
        return label_taxonomy["fine_grained_types"][0] if label_taxonomy.get("fine_grained_types") else None

    def _get_classification_method(self, entity_text: str, fine_grained: str, taxonomy: Dict) -> str:
        """Determine how classification was performed."""
        # Implementation logic
        return "keyword_match"  # or "pattern_match", "database_lookup", "default"

    def _calculate_classification_confidence(self, entity_text: str, fine_grained: str, taxonomy: Dict) -> float:
        """Calculate confidence in fine-grained classification (0.0-1.0)."""
        # High confidence: Direct keyword match
        # Medium: Context match
        # Low: Default/fallback
        return 0.85  # Placeholder

    def verify_566_preservation(self, enriched_entities: List[Dict]) -> Dict:
        """
        MANDATORY VALIDATION: Verify 566-type hierarchy is preserved.

        Returns: Validation report
        """
        tier1_labels = set(e["label"] for e in enriched_entities)
        tier2_types = set(e["fine_grained_type"] for e in enriched_entities)
        tier3_instances = set(e["specific_instance"] for e in enriched_entities)

        report = {
            "total_entities": len(enriched_entities),
            "tier1_labels_used": len(tier1_labels),
            "tier2_types_extracted": len(tier2_types),
            "tier3_instances": len(tier3_instances),
            "hierarchy_preserved": tier2_types != tier1_labels,  # Should have MORE tier2 than tier1
            "coverage_566": len(tier2_types),  # Should approach 566 with large corpus
            "validation_passed": len(tier2_types) > len(tier1_labels)
        }

        # Log validation
        if not report["validation_passed"]:
            print(f"⚠️ HIERARCHY VALIDATION FAILED: Only {len(tier2_types)} fine-grained types found!")
            print(f"   Expected: > {len(tier1_labels)} (more than NER labels)")
            print(f"   This indicates hierarchy is NOT being preserved!")

        return report


# MANDATORY TESTS
if __name__ == "__main__":
    processor = HierarchicalEntityProcessor()

    # Test 1: Basic classification
    test_entity = {
        "text": "WannaCry",
        "label": "MALWARE",
        "start": 0,
        "end": 8,
        "score": 1.0
    }

    enriched = processor.classify_entity(test_entity, "The WannaCry ransomware spread globally")

    assert enriched["fine_grained_type"] == "RANSOMWARE", f"Expected RANSOMWARE, got {enriched['fine_grained_type']}"
    assert "hierarchy_path" in enriched
    print(f"✅ Test 1 passed: {enriched}")

    # Test 2: Batch validation
    test_batch = [
        {"text": "APT29", "label": "THREAT_ACTOR", "score": 1.0},
        {"text": "Emotet", "label": "MALWARE", "score": 1.0},
        {"text": "Siemens S7-1500", "label": "DEVICE", "score": 1.0},
    ]

    enriched_batch = [processor.classify_entity(e) for e in test_batch]
    validation = processor.verify_566_preservation(enriched_batch)

    assert validation["validation_passed"], "Hierarchy validation failed!"
    print(f"✅ Test 2 passed: {validation}")

    print("\n🎯 Hierarchical Entity Processor: VALIDATED")
```

**AUDIT CHECKPOINT #2**:
```bash
# After creating processor, run tests
cd /5_NER11_Gold_Model/pipelines
python 00_hierarchical_entity_processor.py

# VERIFY OUTPUT:
# ✅ Test 1 passed: {...fine_grained_type: RANSOMWARE...}
# ✅ Test 2 passed: {...validation_passed: true...}
# 🎯 Hierarchical Entity Processor: VALIDATED

# Log checkpoint
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "hierarchical-processor-created",
  "timestamp": "<current_time>",
  "file": "00_hierarchical_entity_processor.py",
  "tests_passed": true,
  "hierarchy_validation": true,
  "tier2_types_functional": true,
  "ready_for_etl": true
}
EOF
```

**STOPPING POINT**: DO NOT proceed to Phase 2 until this checkpoint passes!

---

## 🎯 PHASE 2: QDRANT INTEGRATION WITH HIERARCHY (HIGH PRIORITY)

**TIME**: 3-4 hours
**PREREQUISITES**: Phase 1 complete, checkpoint #2 passed

### Task 2.1: Configure Qdrant Collection (30 min)

**CREATE FILE**: `/5_NER11_Gold_Model/pipelines/01_configure_qdrant_collection.py`

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# REUSE existing Qdrant (DO NOT deploy new container)
client = QdrantClient(host="localhost", port=6333)

collection_name = "ner11_entities_hierarchical"

# Create collection with hierarchical payload indexes
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# CRITICAL: Index ALL hierarchy levels
client.create_payload_index(collection_name, "ner_label", "keyword")  # Tier 1 (60)
client.create_payload_index(collection_name, "fine_grained_type", "keyword")  # Tier 2 (566)
client.create_payload_index(collection_name, "specific_instance", "keyword")  # Tier 3
client.create_payload_index(collection_name, "hierarchy_path", "keyword")
client.create_payload_index(collection_name, "hierarchy_level", "integer")

print("✅ Qdrant collection created with hierarchical indexes")
```

**EXECUTE & VERIFY**:
```bash
python 01_configure_qdrant_collection.py

# Verify collection
curl http://localhost:6333/collections/ner11_entities_hierarchical | python3 -m json.tool

# AUDIT CHECKPOINT #3
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "qdrant-collection-created",
  "timestamp": "<current_time>",
  "collection": "ner11_entities_hierarchical",
  "indexes": ["ner_label", "fine_grained_type", "specific_instance", "hierarchy_path"],
  "vector_size": 384,
  "ready_for_ingestion": true
}
EOF
```

### Task 2.2: Hierarchical Embedding Service (2-3 hours)

**CREATE FILE**: `/5_NER11_Gold_Model/pipelines/02_entity_embedding_service_hierarchical.py`

**REQUIREMENTS**:
1. Import `HierarchicalEntityProcessor` (from Phase 1)
2. Enrich ALL entities before embedding
3. Store ALL hierarchy levels in Qdrant payload
4. Validate 566-type preservation

```python
"""
Hierarchical Entity Embedding Service

CRITICAL: Uses HierarchicalEntityProcessor for ALL entities
VALIDATES: 566-type preservation after each batch
"""

import requests
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from typing import List, Dict
from 00_hierarchical_entity_processor import HierarchicalEntityProcessor

class HierarchicalEmbeddingService:
    def __init__(self):
        self.ner_api_url = "http://localhost:8000"
        self.qdrant_client = QdrantClient(host="localhost", port=6333)
        self.collection_name = "ner11_entities_hierarchical"
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # CRITICAL: Initialize hierarchical processor
        self.hierarchy_processor = HierarchicalEntityProcessor()

    def process_document(self, doc_id: str, doc_text: str) -> Dict:
        """
        Complete pipeline with MANDATORY hierarchical enrichment.

        Steps:
        1. Extract entities via NER11 API (60 labels)
        2. ⚠️ CRITICAL: Enrich with hierarchical processor (566 types)
        3. Generate embeddings
        4. Store in Qdrant with ALL hierarchy levels
        5. Validate 566-type preservation
        """
        # Step 1: NER extraction
        response = requests.post(f"{self.ner_api_url}/ner", json={"text": doc_text})
        raw_entities = response.json()["entities"]

        # Step 2: HIERARCHICAL ENRICHMENT (MANDATORY)
        enriched_entities = []
        for entity in raw_entities:
            # Extract context (±200 chars)
            start = max(0, entity["start"] - 200)
            end = min(len(doc_text), entity["end"] + 200)
            context = doc_text[start:end]

            # CRITICAL: Apply hierarchical classification
            enriched = self.hierarchy_processor.classify_entity(entity, context)
            enriched["context"] = context
            enriched_entities.append(enriched)

        # Step 3: Generate embeddings
        points = []
        for entity in enriched_entities:
            embedding = self.embedding_model.encode(f"{entity['text']} {entity['context']}")

            # Step 4: Store with COMPLETE hierarchy
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    # TIER 1: NER label (60 types)
                    "ner_label": entity["label"],

                    # TIER 2: Fine-grained type (566 types) - CRITICAL
                    "fine_grained_type": entity["fine_grained_type"],

                    # TIER 3: Specific instance
                    "specific_instance": entity["specific_instance"],

                    # HIERARCHY METADATA
                    "hierarchy_path": entity["hierarchy_path"],
                    "hierarchy_level": entity["hierarchy_level"],

                    # ORIGINAL DATA
                    "text": entity["text"],
                    "confidence": entity["score"],
                    "doc_id": doc_id,
                    "context": entity["context"],

                    # CLASSIFICATION METADATA
                    "classification_method": entity["classification_method"],
                    "classification_confidence": entity["classification_confidence"]
                }
            )
            points.append(point)

        # Store in Qdrant
        self.qdrant_client.upsert(self.collection_name, points)

        # Step 5: MANDATORY VALIDATION
        validation = self.hierarchy_processor.verify_566_preservation(enriched_entities)

        # Log validation results
        with open("/5_NER11_Gold_Model/logs/hierarchy_verification.jsonl", "a") as f:
            import json
            f.write(json.dumps({
                "doc_id": doc_id,
                "validation": validation,
                "timestamp": "<current_time>"
            }) + "\n")

        if not validation["validation_passed"]:
            raise Exception(f"⚠️ HIERARCHY VALIDATION FAILED for {doc_id}: {validation}")

        return {
            "doc_id": doc_id,
            "entities_extracted": len(raw_entities),
            "entities_enriched": len(enriched_entities),
            "entities_stored": len(points),
            "tier1_labels": validation["tier1_labels_used"],
            "tier2_types": validation["tier2_types_extracted"],
            "validation_passed": validation["validation_passed"]
        }


# MANDATORY TESTS
if __name__ == "__main__":
    service = HierarchicalEmbeddingService()

    test_doc = """
    APT29 deployed WannaCry ransomware targeting Siemens S7-1500 PLCs.
    The attack exploited CVE-2024-1234 in Apache Tomcat 9.0.x.
    Security teams exhibited confirmation bias when dismissing initial warnings.
    """

    result = service.process_document("test_hierarchical_001", test_doc)

    # VALIDATE hierarchical storage
    assert result["tier2_types"] > result["tier1_labels"], \
        "Fine-grained types must exceed NER labels!"

    print(f"✅ Hierarchical embedding service validated:")
    print(f"   Tier 1 labels: {result['tier1_labels']}")
    print(f"   Tier 2 types: {result['tier2_types']} (should be > Tier 1)")
    print(f"   Validation: {result['validation_passed']}")
```

**EXECUTE & AUDIT**:
```bash
python 02_entity_embedding_service_hierarchical.py

# VERIFY OUTPUT shows:
# ✅ Hierarchical embedding service validated:
#    Tier 1 labels: 5-8
#    Tier 2 types: 8-12 (MUST be > Tier 1)
#    Validation: True

# Query Qdrant to verify hierarchy stored
curl -X POST http://localhost:6333/collections/ner11_entities_hierarchical/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"limit": 5, "with_payload": true}' | python3 -m json.tool

# VERIFY payload contains:
# - ner_label (Tier 1)
# - fine_grained_type (Tier 2)
# - specific_instance (Tier 3)
# - hierarchy_path

# AUDIT CHECKPOINT #4
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "qdrant-hierarchical-service-validated",
  "timestamp": "<current_time>",
  "tier1_labels": <count>,
  "tier2_types": <count>,
  "tier3_instances": <count>,
  "validation_passed": true,
  "hierarchy_verified_in_qdrant": true
}
EOF
```

**STOPPING POINT**: Verify checkpoint #4 passes before continuing!

---

## 🎯 PHASE 3: NEO4J INTEGRATION WITH HIERARCHY (CRITICAL)

**TIME**: 4-6 hours
**PREREQUISITES**: Phase 1 & 2 complete

### Task 3.1: Neo4j Schema Migration (1 hour)

**EXECUTE FILE**: `/5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher`

From TASKMASTER v2.0 - section "Task 2.1: Neo4j Schema Migration"

**CRITICAL PRE-MIGRATION**:
```bash
# 1. BACKUP EXISTING DATABASE (570K nodes)
docker exec openspg-neo4j neo4j-admin database dump neo4j --to-stdout > /tmp/neo4j_backup_$(date +%Y%m%d_%H%M%S).dump

# 2. Verify backup size
ls -lh /tmp/neo4j_backup_*.dump
# Should be 100MB-2GB

# 3. Count existing nodes (MUST preserve these)
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) as total"
# Record this number: <existing_node_count>

# AUDIT CHECKPOINT #5
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "pre-neo4j-migration",
  "timestamp": "<current_time>",
  "backup_created": true,
  "backup_file": "<filename>",
  "existing_nodes": <count>,
  "existing_edges": <count>,
  "ready_for_migration": true
}
EOF
```

**EXECUTE MIGRATION**:
```bash
# Run schema upgrade
docker exec -i openspg-neo4j cypher-shell < /5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher

# VERIFY new labels created
docker exec openspg-neo4j cypher-shell "CALL db.labels() YIELD label RETURN label ORDER BY label"

# MUST see: PsychTrait, EconomicMetric, Protocol, Role, Software, Control
# PLUS: All original labels (Document, Entity, etc.)

# VERIFY node count UNCHANGED
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) as total"
# Should match <existing_node_count> from backup

# AUDIT CHECKPOINT #6
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "neo4j-migration-complete",
  "timestamp": "<current_time>",
  "new_labels_created": ["PsychTrait", "EconomicMetric", "Protocol", "Role", "Software", "Control"],
  "existing_nodes_preserved": true,
  "node_count_before": <before>,
  "node_count_after": <after>,
  "data_loss": false,
  "migration_successful": true
}
EOF
```

**ROLLBACK IF ISSUES**:
```bash
# If migration fails:
docker stop openspg-neo4j
docker exec -i openspg-neo4j neo4j-admin database load neo4j --from-stdin < /tmp/neo4j_backup_YYYYMMDD_HHMMSS.dump
docker start openspg-neo4j
```

### Task 3.2: Hierarchical Neo4j Pipeline (3-4 hours)

**CREATE FILE**: `/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py`

Use implementation from TASKMASTER v2.0 "Task 2.3" WITH MODIFICATIONS:

```python
# CRITICAL MODIFICATION: Import and use hierarchical processor

from 00_hierarchical_entity_processor import HierarchicalEntityProcessor

class HierarchicalNeo4jPipeline:
    def __init__(self):
        # ... (neo4j connection code)

        # CRITICAL: Initialize hierarchy processor
        self.hierarchy_processor = HierarchicalEntityProcessor()

    def process_document(self, doc_id, doc_text):
        # Step 1: Extract (60 labels)
        raw_entities = self.extract_entities(doc_text)

        # Step 2: HIERARCHICAL ENRICHMENT (566 types)
        enriched_entities = []
        for entity in raw_entities:
            # Get context
            start = max(0, entity["start"] - 200)
            end = min(len(doc_text), entity["end"] + 200)
            context = doc_text[start:end]

            # CRITICAL: Apply hierarchy
            enriched = self.hierarchy_processor.classify_entity(entity, context)
            enriched_entities.append(enriched)

        # Step 3: Create Neo4j nodes with ALL hierarchy levels
        with self.driver.session() as session:
            for entity in enriched_entities:
                session.write_transaction(
                    self._create_hierarchical_node,
                    entity,
                    doc_id
                )

        # Step 4: MANDATORY VALIDATION
        validation = self.hierarchy_processor.verify_566_preservation(enriched_entities)

        if not validation["validation_passed"]:
            raise Exception(f"Hierarchy validation FAILED: {validation}")

        return validation

    def _create_hierarchical_node(self, tx, entity, doc_id):
        """
        Create Neo4j node with COMPLETE hierarchical properties.

        MANDATORY PROPERTIES:
        - ner_label (Tier 1)
        - fine_grained_type (Tier 2)
        - specific_instance (Tier 3)
        - hierarchy_path
        - hierarchy_level
        """
        # Map to Neo4j super label (16 types)
        neo4j_label = self._map_to_super_label(entity["fine_grained_type"])

        query = f"""
        MERGE (e:{neo4j_label} {{name: $name}})
        ON CREATE SET
            e.id = $id,
            e.ner_label = $ner_label,
            e.fine_grained_type = $fine_grained_type,
            e.specific_instance = $specific_instance,
            e.hierarchy_path = $hierarchy_path,
            e.hierarchy_level = $hierarchy_level,
            e.confidence = $confidence,
            e.created_at = datetime()
        ON MATCH SET
            e.updated_at = datetime()
        WITH e
        MERGE (d:Document {{id: $doc_id}})
        MERGE (d)-[r:MENTIONS]->(e)
        ON CREATE SET r.confidence = $confidence
        """

        tx.run(
            query,
            id=str(uuid.uuid4()),
            name=entity["text"],
            ner_label=entity["label"],
            fine_grained_type=entity["fine_grained_type"],
            specific_instance=entity["specific_instance"],
            hierarchy_path=entity["hierarchy_path"],
            hierarchy_level=entity["hierarchy_level"],
            confidence=entity["score"],
            doc_id=doc_id
        )
```

**TEST & AUDIT**:
```bash
python 05_ner11_to_neo4j_hierarchical.py

# Verify in Neo4j Browser
# Query: Check hierarchical properties stored
MATCH (m:Malware)
WHERE m.fine_grained_type IS NOT NULL
RETURN
    m.name,
    m.ner_label,
    m.fine_grained_type,
    m.hierarchy_path,
    m.hierarchy_level
LIMIT 10;

# MUST SEE:
# ner_label: "MALWARE" (Tier 1)
# fine_grained_type: "RANSOMWARE" or "TROJAN" etc. (Tier 2)
# hierarchy_path: "MALWARE/RANSOMWARE/WannaCry"

# Query: Verify hierarchy enables filtering
MATCH (e)
WHERE e.fine_grained_type = "RANSOMWARE"
RETURN count(e);

# Should return ONLY ransomware, not all malware

# AUDIT CHECKPOINT #7
cat >> /5_NER11_Gold_Model/logs/audit_trail.jsonl << 'EOF'
{
  "checkpoint": "neo4j-hierarchical-ingestion",
  "timestamp": "<current_time>",
  "nodes_created": <count>,
  "hierarchical_properties_verified": true,
  "tier2_filtering_functional": true,
  "existing_570k_nodes_preserved": true,
  "data_integrity": "PASS"
}
EOF
```

---

## ✅ MANDATORY AUDITING & VERIFICATION

### After EACH Phase Complete

**Hierarchy Preservation Verification**:
```python
# File: /5_NER11_Gold_Model/validation/verify_hierarchy_preservation.py

def verify_complete_hierarchy():
    """
    MANDATORY: Run after each ETL batch
    """
    from qdrant_client import QdrantClient
    from neo4j import GraphDatabase

    client_q = QdrantClient(host="localhost", port=6333)
    driver_n = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    # Test 1: Qdrant hierarchy check
    points, _ = client_q.scroll("ner11_entities_hierarchical", limit=100)

    tier1_labels = set()
    tier2_types = set()
    tier3_instances = set()

    for point in points:
        p = point.payload
        assert "ner_label" in p, "Missing Tier 1!"
        assert "fine_grained_type" in p, "Missing Tier 2!"
        assert "specific_instance" in p, "Missing Tier 3!"

        tier1_labels.add(p["ner_label"])
        tier2_types.add(p["fine_grained_type"])
        tier3_instances.add(p["specific_instance"])

    assert len(tier2_types) > len(tier1_labels), \
        f"HIERARCHY BROKEN: Tier2 ({len(tier2_types)}) must exceed Tier1 ({len(tier1_labels)})"

    print(f"✅ Qdrant Hierarchy Verified:")
    print(f"   Tier 1 (NER labels): {len(tier1_labels)}")
    print(f"   Tier 2 (Fine-grained): {len(tier2_types)}")
    print(f"   Tier 3 (Instances): {len(tier3_instances)}")

    # Test 2: Neo4j hierarchy check
    with driver_n.session() as session:
        result = session.run("""
            MATCH (n)
            WHERE n.fine_grained_type IS NOT NULL
            RETURN
                count(DISTINCT n.ner_label) as tier1,
                count(DISTINCT n.fine_grained_type) as tier2,
                count(DISTINCT n.specific_instance) as tier3
        """)

        record = result.single()
        assert record["tier2"] > record["tier1"], "Neo4j hierarchy broken!"

        print(f"✅ Neo4j Hierarchy Verified:")
        print(f"   Tier 1: {record['tier1']}")
        print(f"   Tier 2: {record['tier2']}")
        print(f"   Tier 3: {record['tier3']}")

    return {
        "qdrant": {"tier1": len(tier1_labels), "tier2": len(tier2_types), "tier3": len(tier3_instances)},
        "neo4j": {"tier1": record["tier1"], "tier2": record["tier2"], "tier3": record["tier3"]},
        "validation": "PASS"
    }


if __name__ == "__main__":
    report = verify_complete_hierarchy()
    print(f"\n🎯 Complete Hierarchy Verification: {report['validation']}")
```

**RUN AFTER EVERY ETL BATCH**:
```bash
python /5_NER11_Gold_Model/validation/verify_hierarchy_preservation.py

# Log results
cat >> /5_NER11_Gold_Model/logs/hierarchy_verification.jsonl << 'EOF'
{
  "timestamp": "<current_time>",
  "verification": "pass",
  "qdrant_tier2": <count>,
  "neo4j_tier2": <count>,
  "coverage_566": <percentage>
}
EOF
```

---

## 📊 FINAL AUDIT CHECKLIST

Before marking ANY phase complete:

### Data Integrity Audit
- [ ] Existing 570K Neo4j nodes UNCHANGED
- [ ] All new nodes have hierarchical properties
- [ ] Qdrant payloads include all 3 tiers
- [ ] Validation scripts passing

### Hierarchy Audit
- [ ] Tier 1 (60 NER labels): Preserved
- [ ] Tier 2 (566 fine-grained): Extracted and stored
- [ ] Tier 3 (specific instances): Captured
- [ ] Queries work at all hierarchy levels

### Performance Audit
- [ ] Qdrant search < 100ms
- [ ] Neo4j queries < 500ms
- [ ] Hierarchical filtering functional
- [ ] No performance degradation from hierarchy

### Code Quality Audit
- [ ] All files have hierarchy processor imported
- [ ] All ETL uses classify_entity()
- [ ] All storage includes hierarchical properties
- [ ] Tests verify 566-type preservation

---

## 💾 MEMORY BANK COMMANDS (Use Throughout)

```bash
# Store progress after each task
npx claude-flow memory store \
  --namespace ner11-gold \
  --key phase-<N>-task-<N>-complete \
  --value '<task_completion_json>'

# Store hierarchy verification results
npx claude-flow memory store \
  --namespace ner11-gold \
  --key hierarchy-verification-<timestamp> \
  --value '<verification_results_json>'

# Store audit checkpoints
npx claude-flow memory store \
  --namespace ner11-gold \
  --key audit-checkpoint-<N> \
  --value '<checkpoint_json>'
```

---

## 🎯 YOUR SUCCESS CRITERIA

### Must Achieve ALL of These:

✅ **Hierarchy Preserved**:
- 60 NER labels → 566 fine-grained types → specific instances
- All ETL pipelines use HierarchicalEntityProcessor
- Qdrant and Neo4j store all 3 tiers

✅ **Data Integrity**:
- Existing 570K Neo4j nodes UNCHANGED
- No data loss during migration
- All original relationships preserved

✅ **Functional**:
- Hierarchical queries work (filter by Tier 2 types)
- Semantic search functional
- Graph traversal functional
- Hybrid search operational

✅ **Audited**:
- Audit trail complete (/logs/audit_trail.jsonl)
- All checkpoints passed (min 12 checkpoints)
- Verification scripts passing
- Memory bank updated

✅ **Documented**:
- All code has hierarchy comments
- Validation results logged
- Session summary created
- Next steps documented

---

## 🚨 FAILURE MODES TO AVOID

### Critical Mistake #1: Ignoring Hierarchy
**Symptom**: Only 60 entity types stored (same as NER labels)
**Detection**: `tier2_types == tier1_labels` in validation
**Prevention**: Use HierarchicalEntityProcessor in ALL pipelines
**Recovery**: Re-process all documents with hierarchy enabled

### Critical Mistake #2: Creating Parallel Systems
**Symptom**: New Neo4j container, new Qdrant instance, new API service
**Detection**: `docker ps` shows duplicate services
**Prevention**: Read Constitution Rule #2 before creating anything
**Recovery**: Remove parallel systems, integrate with existing

### Critical Mistake #3: Data Loss
**Symptom**: Neo4j node count decreases
**Detection**: Pre vs post migration count comparison
**Prevention**: ALWAYS backup before migrations
**Recovery**: Restore from backup

### Critical Mistake #4: Incomplete Validation
**Symptom**: "Complete" reported but verification not run
**Detection**: Missing audit checkpoints in logs
**Prevention**: Run verification after EVERY task
**Recovery**: Re-run all validations before proceeding

---

## 📝 FINAL DELIVERABLES CHECKLIST

Before ending session, ensure ALL exist:

### Code Files
- [ ] `00_hierarchical_entity_processor.py` (created, tested)
- [ ] `01_configure_qdrant_collection.py` (created, executed)
- [ ] `02_entity_embedding_service_hierarchical.py` (created, tested)
- [ ] `05_ner11_to_neo4j_hierarchical.py` (created, tested)
- [ ] `verify_hierarchy_preservation.py` (created, passing)

### Audit Logs
- [ ] `/5_NER11_Gold_Model/logs/audit_trail.jsonl` (min 12 checkpoints)
- [ ] `/5_NER11_Gold_Model/logs/hierarchy_verification.jsonl` (validation results)
- [ ] `/5_NER11_Gold_Model/logs/data_integrity.jsonl` (integrity checks)

### Memory Bank
- [ ] All checkpoints stored in `ner11-gold` namespace
- [ ] Hierarchy verification results stored
- [ ] Session summary stored

### Documentation
- [ ] Session completion report created
- [ ] Issues log (if any issues encountered)
- [ ] Next steps documented

---

## 🚀 BEGIN EXECUTION

**START HERE**:
1. Read required documents (2 hours)
2. Execute Phase 0 verification (30 min)
3. Create hierarchical processor (3-4 hours)
4. Implement Qdrant integration (3-4 hours)
5. Implement Neo4j integration (4-6 hours)
6. Run complete validation suite
7. Generate audit report

**REMEMBER**:
- EXTEND existing systems (never replace)
- PRESERVE all 566 fine-grained types
- AUDIT after every task
- VERIFY before marking complete

**YOU ARE READY. BEGIN PHASE 0!** 🚀

---

**Prompt Version**: 1.0.0
**Created**: 2025-12-01 06:00 UTC
**For Session**: NER11 Gold Hierarchical Integration
**Estimated Completion**: 12-16 hours across phases
