# 📋 Complete Task List - All Phases with Descriptions
**Date**: 2025-12-01 16:40 UTC
**Source**: Memory Bank + TASKMASTER v2.0
**Total Tasks**: 14 tasks across 4 phases
**Estimated Total Time**: 20-30 hours

---

## 🎯 PHASE 1: QDRANT VECTOR INTEGRATION (6-8 hours)

### Task 1.1: Create Hierarchical Entity Processor ⚡ BLOCKING
**Time**: 3-4 hours
**Priority**: 🔴 CRITICAL - Everything depends on this
**File**: `/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`

**What It Does**:
- Takes NER11 output (60 labels like "MALWARE", "DEVICE")
- Analyzes entity text + context to extract fine-grained type
- Example: "WannaCry" + context → identifies as RANSOMWARE (not just MALWARE)
- Enriches entity with 3-tier hierarchy:
  - Tier 1: MALWARE (NER label)
  - Tier 2: RANSOMWARE (566 fine-grained types)
  - Tier 3: WannaCry (specific instance)

**Input**: `{text: "WannaCry", label: "MALWARE", score: 1.0}`
**Output**: `{label: "MALWARE", fine_grained_type: "RANSOMWARE", specific_instance: "WannaCry", hierarchy_path: "MALWARE/RANSOMWARE/WannaCry"}`

**Why Critical**: Without this, you lose 506 entity types (only store 60 instead of 566)

**Validation**: Must prove tier2_types > tier1_labels

---

### Task 1.2: Configure Qdrant Collection
**Time**: 30 minutes
**Prerequisites**: None (can do in parallel with 1.1)
**File**: `/5_NER11_Gold_Model/pipelines/01_configure_qdrant_collection.py`

**What It Does**:
- Creates new Qdrant collection named `ner11_entities_hierarchical`
- Configures 384-dimension vectors (for sentence-transformers)
- Sets up indexes on:
  - `ner_label` (60 NER labels)
  - `fine_grained_type` (566 types) ← ENABLES SPECIFIC QUERIES
  - `specific_instance` (entity names)
  - `hierarchy_path` (full path strings)

**Result**: Empty Qdrant collection ready to receive entity embeddings

**Why Important**: Indexes enable fast queries like "find all RANSOMWARE" (not just "find all MALWARE")

---

### Task 1.3: Hierarchical Embedding Service
**Time**: 2-3 hours
**Prerequisites**: Tasks 1.1 (processor) and 1.2 (collection) complete
**File**: `/5_NER11_Gold_Model/pipelines/02_entity_embedding_service_hierarchical.py`

**What It Does**:
- Reads documents from corpus
- Calls NER11 API to extract entities (gets 60 labels)
- **CRITICAL**: Calls HierarchicalEntityProcessor to add 566-type classification
- Generates vector embeddings (384-dim) for each entity + context
- Stores in Qdrant with ALL 3 hierarchy tiers in payload
- Validates that tier2 > tier1 (hierarchy working)

**Example Flow**:
```
Document: "APT29 deployed WannaCry ransomware"
  ↓ NER11 API
Entities: [{text: "APT29", label: "THREAT_ACTOR"}, {text: "WannaCry", label: "MALWARE"}]
  ↓ HierarchicalEntityProcessor
Enriched: [
  {label: "THREAT_ACTOR", fine_grained: "NATION_STATE", instance: "APT29"},
  {label: "MALWARE", fine_grained: "RANSOMWARE", instance: "WannaCry"}
]
  ↓ Generate Embeddings
Vectors: [384-dim vector for each entity]
  ↓ Store in Qdrant
Saved with hierarchy_path: "THREAT_ACTOR/NATION_STATE/APT29"
```

**Result**: Entities in Qdrant with semantic search capability AND hierarchical filtering

---

### Task 1.4: Bulk Document Processing
**Time**: 1-2 hours
**Prerequisites**: Task 1.3 (embedding service) working
**File**: `/5_NER11_Gold_Model/pipelines/03_bulk_document_processor.py`

**What It Does**:
- Processes ~1,250 training documents through the pipeline
- For each document:
  - Extract entities via NER11 API
  - Enrich with hierarchy
  - Generate embeddings
  - Store in Qdrant
- Tracks progress with logs
- Maintains processing log (skip already processed)

**Result**: 10,000-15,000 entities in Qdrant, fully searchable

**Why Important**: Populates Qdrant with actual data for semantic search

---

### Task 1.5: Semantic Search API Endpoint
**Time**: 1-2 hours
**Prerequisites**: Task 1.4 (Qdrant populated)
**File**: `/5_NER11_Gold_Model/serve_model.py` (EXTEND existing FastAPI app)

**What It Does**:
- Adds `POST /search/semantic` endpoint to existing NER11 API
- Takes query text: "Apache vulnerabilities"
- Generates embedding for query
- Searches Qdrant for similar entities
- Enables filtering by:
  - Tier 1 (NER labels): "MALWARE", "CVE"
  - Tier 2 (fine-grained): "RANSOMWARE", "PLC"
  - Confidence threshold
- Returns top-K results with similarity scores

**Example**:
```
Query: "ransomware attacking industrial systems"
Returns:
- WannaCry (MALWARE/RANSOMWARE) - similarity: 0.89
- Siemens PLC (DEVICE/PLC) - similarity: 0.82
- Critical infrastructure (SECTOR/ENERGY) - similarity: 0.78
```

**Result**: Semantic search capability for cybersecurity entities

---

## 🎯 PHASE 2: NEO4J KNOWLEDGE GRAPH (8-12 hours)

### Task 2.1: Neo4j Schema Migration to v3.1
**Time**: 1-2 hours
**Prerequisites**: Phase 1 complete (for context), Neo4j backup created
**File**: `/5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher`

**What It Does**:
- **FIRST**: Creates backup of existing 570K nodes (MANDATORY)
- Adds 6 NEW super labels to Neo4j:
  - `PsychTrait` (for COGNITIVE_BIAS, PERSONALITY, LACANIAN)
  - `EconomicMetric` (for financial impact data)
  - `Protocol` (for MODBUS, DNP3, IEC_61850)
  - `Role` (for CISO, Security Analyst)
  - `Software` (for applications, OS, components)
  - `Control` (for security controls, mitigations)
- Creates indexes on `fine_grained_type` property for all labels
- **DOES NOT** modify or delete existing 570K nodes

**Result**: Neo4j schema upgraded from v3.0 (11 labels) to v3.1 (16 labels + hierarchical properties)

**Why Important**: Enables storing psychometric, economic, and protocol entities from NER11

---

### Task 2.2: Entity Mapping (60 NER Labels → 16 Neo4j Labels)
**Time**: 2-3 hours
**Prerequisites**: Task 2.1 (schema v3.1) deployed
**File**: `/5_NER11_Gold_Model/pipelines/04_ner11_to_neo4j_mapper.py`

**What It Does**:
- Creates mapping table for all 60 NER labels
- Maps to 16 Neo4j super labels
- Defines property discriminators for 566 fine-grained types

**Example Mappings**:
```
NER "MALWARE" → Neo4j "Malware" {fine_grained_type: "RANSOMWARE"}
NER "COGNITIVE_BIAS" → Neo4j "PsychTrait" {fine_grained_type: "CONFIRMATION_BIAS"}
NER "DEVICE" → Neo4j "Asset" {assetClass: "OT", fine_grained_type: "PLC"}
NER "APT_GROUP" → Neo4j "ThreatActor" {actorType: "apt_group", fine_grained_type: "NATION_STATE"}
```

**Result**: Complete mapping logic for transforming NER output to Neo4j nodes

**Why Important**: Preserves 566-type granularity while using only 16 Neo4j labels (optimal for query performance)

---

### Task 2.3: Hierarchical Neo4j Pipeline
**Time**: 3-4 hours
**Prerequisites**: Tasks 2.1, 2.2 complete
**File**: `/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py`

**What It Does**:
- Reads documents
- Extracts entities via NER11 API (60 labels)
- **CRITICAL**: Enriches with HierarchicalEntityProcessor (adds 566 types)
- Maps to Neo4j super labels (16 labels)
- Creates nodes with hierarchical properties:
  ```cypher
  (:Malware {
    name: "WannaCry",
    ner_label: "MALWARE",
    fine_grained_type: "RANSOMWARE",
    specific_instance: "WannaCry",
    hierarchy_path: "MALWARE/RANSOMWARE/WannaCry"
  })
  ```
- Extracts relationships (CVE→Software, ThreatActor→Malware, etc.)
- Creates relationships in graph
- **PRESERVES** existing 570K nodes (extends, doesn't replace)

**Result**: Entities added to Neo4j knowledge graph with full hierarchy

---

### Task 2.4: Bulk Graph Ingestion
**Time**: 2-3 hours
**Prerequisites**: Task 2.3 (pipeline) working
**File**: `/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py`

**What It Does**:
- Processes entire document corpus through Neo4j pipeline
- Creates 15,000+ entity nodes
- Creates 5,000+ relationships
- Tracks progress with logs
- Validates hierarchy after each batch

**Example**:
```
Process 1,250 documents
  ↓
Extract 18,000 entities
  ↓
Enrich with hierarchy
  ↓
Create 15,000 Neo4j nodes (some are duplicates merged)
  ↓
Create 8,000 relationships
  ↓
Verify: 570K original nodes + 15K new = 585K total
```

**Result**: Complete knowledge graph with hierarchical entities

**Why Important**: Enables complex queries like "Show attack chains affecting PLCs"

---

## 🎯 PHASE 3: HYBRID SEARCH SYSTEM (3-4 hours)

### Task 3.1: Hybrid Search Implementation
**Time**: 3-4 hours
**Prerequisites**: Phases 1 & 2 complete
**File**: `/5_NER11_Gold_Model/serve_model.py` (EXTEND with new endpoint)

**What It Does**:
- Adds `POST /search/hybrid` endpoint
- Combines Qdrant (semantic similarity) + Neo4j (graph relationships)
- Algorithm:
  1. User query: "Apache vulnerabilities affecting critical infrastructure"
  2. Qdrant semantic search → finds relevant entities (CVEs, Apache, etc.)
  3. Neo4j graph expansion → finds related entities (affected systems, sectors)
  4. Re-ranks by: similarity score + graph centrality
  5. Returns unified results

**Example Query**:
```json
POST /search/hybrid
{
  "query": "APT29 ransomware attacks",
  "expand_graph": true,
  "hop_depth": 2
}

Returns:
{
  "entity": "APT29 (THREAT_ACTOR/NATION_STATE)",
  "similarity": 0.95,
  "related_entities": [
    "WannaCry (MALWARE/RANSOMWARE)",
    "Energy Sector (ORGANIZATION/SECTOR)",
    "Siemens PLC (DEVICE/PLC)"
  ],
  "attack_path": "APT29 → WannaCry → CVE-2024-1234 → Siemens PLC"
}
```

**Result**: Powerful hybrid search combining vector similarity + knowledge graph

**Why Important**: Answers complex questions that need both semantic relevance AND relationship context

---

## 🎯 PHASE 4: MCKENNEY-LACAN PSYCHOHISTORY (Research - 4-6 hours)

### Task 4.1: Psychometric Entity Analysis
**Time**: 4-6 hours
**Prerequisites**: Phase 2 complete (PsychTrait nodes exist)
**File**: `/5_NER11_Gold_Model/analytics/psychometric_analyzer.py`

**What It Does**:
- Analyzes psychological entities extracted by NER11:
  - COGNITIVE_BIAS (25 subtypes)
  - PERSONALITY (20 subtypes)
  - THREAT_PERCEPTION patterns
  - LACANIAN discourse analysis

**Example Analyses**:
```
1. "Which cognitive biases appear most in security incidents?"
   Query Neo4j for PsychTrait nodes linked to incidents

2. "What personality traits characterize APT groups?"
   Build psychological profiles of threat actors

3. "How does confirmation bias correlate with breach severity?"
   Statistical analysis of bias patterns vs CVE severity
```

**Result**: Psychological insights into cybersecurity behavior

**Why Important**: Answers McKenney's 8 Strategic Questions about human factors in cyber

---

### Task 4.2: Threat Actor Personality Profiling
**Time**: Included in 4.1

**What It Does**:
- Builds personality profiles for known threat actors
- Correlates traits with attack patterns
- Applies McKenney-Lacan calculus framework
- Creates "personality tensors" for actors

**Example**:
```
APT29 Profile:
- Sophistication: Advanced
- Traits: [STRATEGIC_PLANNING, PERSISTENCE, STEALTH]
- Discourse Position: UNIVERSITY (Lacanian)
- Behavior Pattern: PATIENT_RECONNAISSANCE
```

**Result**: Behavioral models of threat actors

---

### Task 4.3: Musical Notation System (Optional Research)
**Time**: Variable
**File**: Experimental

**What It Does**:
- Represents team interactions as musical scores
- Models dialogue dynamics using GNN (Graph Neural Network)
- Applies symphonic calculus to security team behaviors

**Purpose**: Advanced research into team dynamics modeling

---

## 📊 COMPLETE TASK SUMMARY TABLE

| Phase | Task | What It Does | Time | Priority | Blocks Others |
|-------|------|--------------|------|----------|---------------|
| **1** | **1.1** | **Enrich 60 labels → 566 types** | **3-4h** | **🔴 CRITICAL** | **YES** |
| 1 | 1.2 | Create Qdrant collection | 30m | 🔴 HIGH | Partially |
| 1 | 1.3 | Build embedding pipeline | 2-3h | 🔴 HIGH | Yes |
| 1 | 1.4 | Process bulk documents | 1-2h | 🟡 MEDIUM | No |
| 1 | 1.5 | Add semantic search API | 1-2h | 🟡 MEDIUM | No |
| **2** | **2.1** | **Upgrade Neo4j schema** | **1-2h** | **🔴 CRITICAL** | **YES** |
| 2 | 2.2 | Map 60→16 labels | 2-3h | 🔴 HIGH | Yes |
| 2 | 2.3 | Build Neo4j pipeline | 3-4h | 🔴 HIGH | Yes |
| 2 | 2.4 | Ingest bulk to graph | 2-3h | 🟡 MEDIUM | No |
| **3** | **3.1** | **Hybrid search** | **3-4h** | **🟢 MEDIUM** | **No** |
| 4 | 4.1 | Psychometric analysis | 4-6h | 🔵 LOW | No |
| 4 | 4.2 | Personality profiling | Included | 🔵 LOW | No |
| 4 | 4.3 | Musical notation | Variable | 🔵 RESEARCH | No |

**Total**: ~20-30 hours for Phases 1-3 (production-ready)

---

## 🔄 TASK DEPENDENCIES

### Critical Path (Must Do In Order):
```
1.1 (Processor)
  ↓
1.3 (Embedding Service)
  ↓
2.1 (Schema Migration)
  ↓
2.3 (Neo4j Pipeline)
  ↓
3.1 (Hybrid Search)
```

### Can Do in Parallel:
```
1.1 + 1.2 (Processor + Qdrant collection)
1.4 + 1.5 (Bulk processing + Search API)
2.2 + 2.3 (Mapping + Pipeline)
```

---

## 📋 DETAILED TASK DESCRIPTIONS

### PHASE 1 DEEP DIVE

#### What Phase 1 Achieves:
- **Semantic Search**: Find entities by meaning, not just keywords
- **Hierarchical Filtering**: Query by specific types (RANSOMWARE not just MALWARE)
- **Context Preservation**: Each entity stored with surrounding text
- **Fast Queries**: <100ms response time
- **Scalable**: Handle 100K+ entities

#### What You Can Do After Phase 1:
```
Search: "vulnerabilities in web servers"
Get: CVE-2024-1234 (CVE), Apache Tomcat (SOFTWARE_COMPONENT)
  with similarity scores and context

Search: "PLC malware"
Get: Specific malware targeting PLCs (filtered by DEVICE/PLC fine-grained type)

Search: "APT groups from China"
Get: Specific NATION_STATE actors with APT classification
```

---

### PHASE 2 DEEP DIVE

#### What Phase 2 Achieves:
- **Knowledge Graph**: Entity relationships mapped
- **Attack Paths**: CVE → Software → ThreatActor chains
- **Graph Queries**: Multi-hop traversal
- **Hierarchical Nodes**: All nodes have 3-tier taxonomy
- **Preserved Data**: 570K existing nodes untouched

#### What You Can Do After Phase 2:
```cypher
// Find attack chains
MATCH path = (apt:ThreatActor)-[:USES]->(m:Malware)-[:EXPLOITS]->(cve:CVE)-[:AFFECTS]->(s:Software)
WHERE apt.fine_grained_type = "NATION_STATE"
  AND m.fine_grained_type = "RANSOMWARE"
  AND s.fine_grained_type = "PLC"
RETURN path

// Find all ransomware (not just MALWARE)
MATCH (m:Malware)
WHERE m.fine_grained_type = "RANSOMWARE"
RETURN m.name, m.malware_family

// Psychometric analysis
MATCH (bias:PsychTrait {fine_grained_type: "CONFIRMATION_BIAS"})<-[:EXHIBITS]-(actor:ThreatActor)
RETURN actor.name, bias.name
```

---

### PHASE 3 DEEP DIVE

#### What Phase 3 Achieves:
- **Best of Both Worlds**: Semantic + Graph combined
- **Smart Search**: Finds relevant entities THEN expands via relationships
- **Contextual Results**: Entities with their relationship context
- **Advanced Queries**: "Find similar threats AND their targets"

#### Example Use Case:
```
User: "Show me ransomware attacks similar to WannaCry and what they targeted"

System:
1. Qdrant search: Find entities similar to "WannaCry ransomware"
   → Returns: Ryuk, Maze, LockBit (all RANSOMWARE fine-grained type)

2. Neo4j expansion: For each found malware, traverse graph
   → Find: What they EXPLOIT (CVEs)
   → Find: What they AFFECT (Software, Assets)
   → Find: Who USES them (ThreatActors)

3. Return: Complete attack context for each similar ransomware
```

**Result**: Intelligent search that understands both meaning AND context

---

### PHASE 4 DEEP DIVE

#### What Phase 4 Achieves:
- **Behavioral Analysis**: Understand threat actor psychology
- **Cognitive Bias Detection**: Identify decision-making flaws
- **Predictive Modeling**: Forecast based on psychological patterns
- **Team Dynamics**: Model security team interactions

#### McKenney's 8 Questions Answered:
1. How do cyber threats evolve? → Pattern analysis
2. What psychological factors drive incidents? → Bias correlation
3. Can we predict organizational vulnerability? → Psychometric modeling
4. How do teams respond? → Interaction analysis
5. What cultural factors matter? → Discourse analysis
6. Can we model threat actor decisions? → Personality profiling
7. How do biases create gaps? → Statistical correlation
8. What is cyber psychohistory? → Complete framework integration

---

## 🎯 THE BIG PICTURE - WHY EACH PHASE MATTERS

### Phase 1 (Qdrant):
**Enables**: "Find things similar to X" (semantic search)
**Example**: Find vulnerabilities similar to a known exploit

### Phase 2 (Neo4j):
**Enables**: "How are things connected?" (relationship queries)
**Example**: Trace attack path from APT group to compromised system

### Phase 3 (Hybrid):
**Enables**: "Find similar things AND show their connections"
**Example**: Find similar attacks AND see what they targeted

### Phase 4 (Psychohistory):
**Enables**: "Why do attacks succeed?" (human factors analysis)
**Example**: Correlate cognitive biases with successful attacks

---

## ✅ STARTING CHECKLIST

Before beginning Task 1.1:

- [ ] On correct branch: `gap-002-clean-VERIFIED`
- [ ] Infrastructure verified: All containers healthy
- [ ] Documentation read: TASKMASTER v2.0 Section "Task 1.1"
- [ ] Dependencies installed: sentence-transformers, qdrant-client
- [ ] Working directories created: pipelines/, logs/, validation/

**Then**: Create `00_hierarchical_entity_processor.py` using TASKMASTER template

---

## 📚 KEY DOCUMENTATION FOR EACH TASK

**Task 1.1**: TASKMASTER v2.0 + CRITICAL_NER11_HIERARCHICAL_STRUCTURE.md
**Task 1.2**: TASKMASTER v2.0 + Qdrant docs
**Task 1.3**: TASKMASTER v2.0 + 01_NER11_ENTITY_INVENTORY.md
**Task 2.1**: Schema v3.1 spec + Neo4j migration guide
**Task 2.3**: TASKMASTER v2.0 + Neo4j pipeline guide
**Task 3.1**: Hybrid architecture design docs

**All Available**: In `/docs/` and on GitHub

---

## 🎯 BOTTOM LINE

**Total Tasks**: 14 (10 production, 4 research)
**Critical Path**: 5 tasks (1.1, 1.3, 2.1, 2.3, 3.1)
**Time to Production**: 15-20 hours
**Blockers**: NONE
**Ready**: ✅ START NOW

**First Task**: Create HierarchicalEntityProcessor (Task 1.1)
**Est. Time**: 3-4 hours
**Location**: `/5_NER11_Gold_Model/pipelines/00_hierarchical_entity_processor.py`

---

**Created**: 2025-12-01 16:40 UTC
**Based On**: Memory bank (30 keys) + Qdrant (11 entries) + TASKMASTER v2.0
**Status**: Ready for execution
