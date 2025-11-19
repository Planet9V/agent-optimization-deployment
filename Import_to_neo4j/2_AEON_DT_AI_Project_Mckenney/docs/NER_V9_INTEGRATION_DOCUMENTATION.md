# NER v9 Model Integration Documentation

**File**: NER_V9_INTEGRATION_DOCUMENTATION.md
**Created**: 2025-11-11
**Purpose**: Document how NER v9 model integrates into the document processing pipeline
**Status**: COMPLETE - Based on codebase analysis

---

## Executive Summary

The AEON DT AI Project McKenney uses a **Pattern-Neural Hybrid NER Agent** (not a single v9 model endpoint) that combines rule-based pattern matching (95%+ precision) with spaCy neural NER (85-92% contextual accuracy) to extract 18 entity types from uploaded documents. The extracted entities are stored in Neo4j as nodes with relationships.

**Target Precision**: 92-96% combined precision

---

## NER Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Document Upload → NER → Neo4j Flow             │
└─────────────────────────────────────────────────────────────┘

1. Upload: File → MinIO Storage
   ↓
2. Queue: DocumentQueue (lib/queue/documentQueue.ts)
   ↓
3. Process: Python agents serial execution
   ├─ Step 1: classifier_agent.py (Classification)
   ├─ Step 2: ner_agent.py (Entity Extraction) ← HYBRID NER HERE
   └─ Step 3: ingestion_agent.py (Neo4j Storage)
```

---

## NER Agent Implementation

### Location
**File**: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents/ner_agent.py`

### Implementation Type
**Pattern-Neural Hybrid** - NOT a single API endpoint at localhost:8001/api/v9/ner/extract

### Components

#### 1. **Pattern-Based NER (Rule-Based)**
- **Precision**: 95%+ (high confidence)
- **Method**: Regular expressions and spaCy EntityRuler patterns
- **Source Code**: Lines 94-200 in `ner_agent.py`

**Example Patterns**:
```python
# VENDOR patterns
{"label": "VENDOR", "pattern": [{"LOWER": "siemens"}]}
{"label": "VENDOR", "pattern": [{"LOWER": "rockwell"}, {"LOWER": "automation"}]}

# PROTOCOL patterns
{"label": "PROTOCOL", "pattern": [{"LOWER": "modbus"}]}
{"label": "PROTOCOL", "pattern": [{"LOWER": "opc"}, {"LOWER": "ua"}]}

# STANDARD patterns (Regex)
{"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": "IEC\\s*\\d+"}}]}
{"label": "STANDARD", "pattern": [{"TEXT": {"REGEX": "IEEE\\s*\\d+"}}]}

# MEASUREMENT patterns (Regex)
{"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": "\\d+(\\.\\d+)?\\s*PSI"}}]}
{"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": "\\d+(\\.\\d+)?\\s*GPM"}}]}

# CVE patterns (Cybersecurity)
{"label": "CVE", "pattern": [{"TEXT": {"REGEX": "CVE-\\d{4}-\\d{4,7}"}}]}
```

#### 2. **Neural NER (spaCy)**
- **Model**: `en_core_web_lg` (spaCy's large English model)
- **Precision**: 85-92% (contextual understanding)
- **Method**: Pre-trained neural NER from spaCy
- **Source Code**: Lines 76-86 in `ner_agent.py`

**Loading Code**:
```python
if SPACY_AVAILABLE:
    try:
        self.logger.info("Loading spaCy model: en_core_web_lg")
        self.nlp = spacy.load("en_core_web_lg")
        self.entity_ruler = self.nlp.add_pipe("entity_ruler", after="ner")
        self.logger.info("spaCy model loaded successfully")
    except Exception as e:
        self.logger.warning(f"Could not load spaCy model: {e}")
        self.nlp = None
```

---

## 18 Entity Types Extracted

The NER agent extracts the following entity types:

### Industrial Control System Entities (Original 8)
1. **VENDOR** - Equipment/software vendors (Siemens, Rockwell, ABB, Schneider Electric, Honeywell, Emerson, Yokogawa, GE Digital)
2. **PROTOCOL** - Communication protocols (Modbus, OPC UA, Profinet, EtherCAT, HART, Foundation Fieldbus, DeviceNet, BACnet)
3. **STANDARD** - Industry standards (IEC 61508, IEEE 802.11, ISO 27001, ANSI, NFPA)
4. **COMPONENT** - Physical components (PLC, HMI, RTU, SCADA, transmitter, actuator, sensor, controller, VFD)
5. **MEASUREMENT** - Units and measurements (PSI, GPM, °C, °F, kW, HP, bar)
6. **ORGANIZATION** - Companies and organizations
7. **SAFETY_CLASS** - Safety integrity levels (SIL 1-4, ASIL A-D, CAT 1-4)
8. **SYSTEM_LAYER** - System architecture layers (L0-L5 Purdue Model, field level, control level)

### Cybersecurity Entities (Added 2025-11-04) (10 additional)
9. **CVE** - Common Vulnerabilities and Exposures (CVE-2024-12345)
10. **CWE** - Common Weakness Enumeration (CWE-79)
11. **CAPEC** - Common Attack Pattern Enumeration (CAPEC-1)
12. **THREAT_ACTOR** - Known threat actors (Lazarus Group, Fancy Bear, Cozy Bear, Equation Group, Sandworm, Dragonfly, Energetic Bear)
13. **CAMPAIGN** - Cyber campaign identifiers
14. **ATTACK_TECHNIQUE** - MITRE ATT&CK techniques (T1234, T1234.001)
15. **MALWARE** - Malware families (WannaCry, NotPetya, Stuxnet, Triton, Industroyer, BlackEnergy, Havex, TrickBot, Emotet)
16. **IOC** - Indicators of Compromise (IP addresses, MD5/SHA1/SHA256 hashes)
17. **APT_GROUP** - Advanced Persistent Threat groups (APT1, APT28, APT29, etc.)
18. **(Implied)** Additional contextual entities from spaCy neural NER

---

## Document Processing Pipeline Integration

### Step-by-Step Flow

#### 1. **File Upload** (Web Interface)
- **Component**: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/components/upload/UploadWizard.tsx`
- **API Endpoint**: `POST /api/upload`
- **Storage**: MinIO object storage at `openspg-minio:9000`
- **Path Format**: `uploads/YYYY-MM-DD_HH-MM-SS_filename.ext`

#### 2. **Job Queuing** (Document Queue)
- **Component**: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/lib/queue/documentQueue.ts`
- **Queue Type**: In-memory serial queue (production should use Redis)
- **Job Data Structure**:
```typescript
interface DocumentJobData {
  jobId: string;
  fileName: string;
  filePath: string;
  customer: string;
  tags: string[];
  classification: {
    sector: string;
    subsector?: string;
  };
  fileSize: number;
  fileType: string;
}
```

#### 3. **Agent Execution** (Serial Processing)

##### **Agent 1: Classifier Agent** (33% progress)
- **Script**: `agents/classifier_agent.py`
- **Purpose**: Document type classification, content analysis, sector/subsector validation
- **Input**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "sector": "Infrastructure",
  "subsector": "Water"
}
```

##### **Agent 2: NER Agent** (66% progress) ← **ENTITY EXTRACTION HERE**
- **Script**: `agents/ner_agent.py`
- **Purpose**: Named entity extraction, relationship identification, entity classification
- **Input**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "customer": "mckenney"
}
```

**NER Processing Steps**:
1. **Load spaCy Model**: `en_core_web_lg` neural model
2. **Apply Pattern Library**: Industrial/cybersecurity entity patterns
3. **Extract Entities**: Hybrid pattern + neural extraction
4. **Merge Duplicates**: Combine pattern and neural results
5. **Calculate Confidence**: Score entities based on source (pattern=0.95+, neural=0.85-0.92)
6. **Return Entities**: JSON array with text, label, confidence, source

**Output Structure**:
```json
{
  "entities": [
    {
      "text": "Siemens S7-1500",
      "label": "VENDOR",
      "confidence": 0.95,
      "source": "pattern",
      "start": 10,
      "end": 25
    },
    {
      "text": "Modbus TCP",
      "label": "PROTOCOL",
      "confidence": 0.96,
      "source": "pattern",
      "start": 45,
      "end": 55
    },
    {
      "text": "IEC 61508 SIL 2",
      "label": "STANDARD",
      "confidence": 0.97,
      "source": "pattern",
      "start": 120,
      "end": 135
    }
  ],
  "entity_count": 45,
  "by_type": {
    "VENDOR": 12,
    "PROTOCOL": 8,
    "STANDARD": 5,
    "COMPONENT": 15,
    "MEASUREMENT": 5
  },
  "precision_estimate": 0.93
}
```

##### **Agent 3: Ingestion Agent** (100% progress)
- **Script**: `agents/ingestion_agent.py`
- **Purpose**: Neo4j node creation, relationship mapping, property assignment, graph integration
- **Input**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "customer": "mckenney",
  "tags": ["tag-critical", "tag-technical"],
  "classification": {
    "sector": "Infrastructure",
    "subsector": "Water"
  }
}
```

---

## Neo4j Storage Pattern

### Entity Storage

**Cypher Query Pattern**:
```cypher
// Create Document node
CREATE (d:Document {
  id: randomUUID(),
  content: $content,
  char_count: $char_count,
  line_count: $line_count
})

// Merge Metadata with SHA256 deduplication
MERGE (m:Metadata {sha256: $sha256})
ON CREATE SET
  m.file_path = $file_path,
  m.file_name = $file_name,
  m.file_ext = $file_ext,
  m.file_size = $file_size,
  m.processed_at = $processed_at
CREATE (m)-[:METADATA_FOR]->(d)

// Insert entities with deduplication
UNWIND $entities as entity
MERGE (e:Entity {text: entity.text, label: entity.label})
ON CREATE SET
  e.created_at = datetime(),
  e.count = 1
ON MATCH SET
  e.count = coalesce(e.count, 0) + 1
CREATE (d)-[:CONTAINS_ENTITY {
  start: entity.start,
  end: entity.end,
  type: entity.type,
  confidence: entity.confidence,
  source: entity.source
}]->(e)
```

### Graph Structure

```
┌─────────────┐
│  Metadata   │
│ (sha256)    │
└─────┬───────┘
      │ METADATA_FOR
      ↓
┌─────────────┐     CONTAINS_ENTITY      ┌─────────────┐
│  Document   │─────────────────────────→│   Entity    │
│   (UUID)    │  {start, end, type,      │ (text,label)│
│             │   confidence, source}    │             │
└─────────────┘                          └─────────────┘
      │
      │ HAS_TAG
      ↓
┌─────────────┐
│     Tag     │
│  (id, name) │
└─────────────┘
```

### Entity Deduplication

**Key**: `(text, label)` composite
- **Example**: `("Siemens", "VENDOR")` is unique
- **Counter**: Each occurrence increments `count` property
- **Creation Time**: `created_at` timestamp on first occurrence

### Indexes and Constraints

```cypher
-- Unique constraints
CREATE CONSTRAINT metadata_sha256 IF NOT EXISTS
  FOR (m:Metadata) REQUIRE m.sha256 IS UNIQUE;

CREATE CONSTRAINT document_id IF NOT EXISTS
  FOR (d:Document) REQUIRE d.id IS UNIQUE;

-- Performance indexes
CREATE INDEX entity_text IF NOT EXISTS
  FOR (e:Entity) ON (e.text);

CREATE INDEX entity_label IF NOT EXISTS
  FOR (e:Entity) ON (e.label);

CREATE INDEX entity_composite IF NOT EXISTS
  FOR (e:Entity) ON (e.text, e.label);

-- Full-text search
CREATE FULLTEXT INDEX document_fulltext IF NOT EXISTS
  FOR (d:Document) ON EACH [d.content];
```

---

## NLP Ingestion Pipeline (Alternative)

**File**: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/nlp_ingestion_pipeline.py`

This is a **standalone pipeline** that can process documents directly (not called by the web interface):

### Features
1. **Multi-format Support**: MD, TXT, PDF, DOCX, JSON
2. **spaCy NLP**: Entity extraction via spaCy NER
3. **Custom Patterns**: Cybersecurity entities (CVE, CWE, CAPEC, IPs, hashes)
4. **Relationship Extraction**: Subject-Verb-Object triples via dependency parsing
5. **Table Extraction**: Markdown table parsing
6. **Neo4j Batch Insertion**: Efficient batch inserts with deduplication
7. **Progress Tracking**: Resumability via `.ingestion_progress.json`

### Usage
```bash
python nlp_ingestion_pipeline.py input_file.md \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password password \
  --spacy-model en_core_web_lg \
  --batch-size 100
```

### Entity Types (NLP Pipeline)
- **Standard NER**: From spaCy (PERSON, ORG, GPE, DATE, etc.)
- **Custom Cybersecurity**: CVE, CAPEC, CWE, TECHNIQUE (T1234), IP_ADDRESS, HASH, URL

---

## Example: Complete Upload → NER → Neo4j Flow

### 1. Upload Document
```bash
curl -X POST http://localhost:3000/api/upload \
  -F "files=@technical_spec.pdf"
```

**Response**:
```json
{
  "success": true,
  "files": [{
    "originalName": "technical_spec.pdf",
    "path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
    "bucket": "aeon-documents",
    "size": 1024000,
    "type": "application/pdf"
  }],
  "count": 1
}
```

### 2. Submit for Processing
```bash
curl -X POST http://localhost:3000/api/pipeline/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{
      "path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
      "name": "technical_spec.pdf",
      "size": 1024000,
      "type": "application/pdf"
    }],
    "customer": "mckenney",
    "tags": ["tag-critical"],
    "classification": {
      "sector": "Infrastructure",
      "subsector": "Water"
    }
  }'
```

**Response**:
```json
{
  "success": true,
  "jobs": [{
    "jobId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "queued",
    "progress": 0,
    "message": "Queued: technical_spec.pdf"
  }],
  "message": "Started processing 1 file(s)"
}
```

### 3. Monitor Progress
```bash
curl http://localhost:3000/api/pipeline/status/550e8400-e29b-41d4-a716-446655440000
```

**Response During NER Extraction** (66% progress):
```json
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "technical_spec.pdf",
  "status": "extracting",
  "progress": 66,
  "message": "Entity extraction complete, starting ingestion",
  "steps": {
    "classification": { "status": "complete", "progress": 100 },
    "ner": { "status": "running", "progress": 50 },
    "ingestion": { "status": "pending", "progress": 0 }
  }
}
```

### 4. Query Neo4j for Extracted Entities
```cypher
// Find document
MATCH (m:Metadata {file_name: "technical_spec.pdf"})-[:METADATA_FOR]->(d:Document)

// Get all entities
MATCH (d)-[r:CONTAINS_ENTITY]->(e:Entity)
RETURN e.text, e.label, r.confidence, r.source, e.count
ORDER BY r.confidence DESC
```

**Sample Results**:
```
e.text              | e.label     | r.confidence | r.source | e.count
--------------------|-------------|--------------|----------|--------
Siemens S7-1500     | VENDOR      | 0.95         | pattern  | 3
Modbus TCP          | PROTOCOL    | 0.96         | pattern  | 2
IEC 61508 SIL 2     | STANDARD    | 0.97         | pattern  | 1
150 PSI             | MEASUREMENT | 0.95         | pattern  | 4
Foundation Fieldbus | PROTOCOL    | 0.96         | pattern  | 1
```

---

## Configuration Requirements

### Environment Variables (.env.local)
```bash
# MinIO Configuration
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
MINIO_BUCKET=aeon-documents

# Python Agents
PYTHON_PATH=python3
AGENTS_PATH=/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### Python Dependencies (NER Agent)
```bash
# spaCy and model
pip install spacy
python -m spacy download en_core_web_lg

# Additional dependencies
pip install neo4j pandas tqdm
```

---

## Testing NER Agent

### Test Files
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/tests/test_ner_agent.py`
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/tests/test_ner_validation.py`
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/tests/test_ner_relationships.py`
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/tests/test_ner_direct.py`

### Run Tests
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney

# Test NER agent
python tests/test_ner_agent.py

# Test pattern extraction
python -c "
from agents.ner_agent import NERAgent

agent = NERAgent({})
result = agent.run({
    'text': 'The Siemens S7-1500 PLC uses Modbus TCP protocol at 150 PSI.',
    'sector': 'industrial'
})

print(f'Extracted {result[\"entity_count\"]} entities:')
for ent in result['entities']:
    print(f'  - {ent[\"text\"]:20s} [{ent[\"label\"]:12s}] conf={ent[\"confidence\"]:.2f}')
"
```

---

## Performance Metrics

### NER Agent Statistics
- **Pattern Entities**: 95%+ precision (high confidence)
- **Neural Entities**: 85-92% precision (contextual)
- **Combined Precision Target**: 92-96%
- **Processing Speed**: ~1-2 seconds per document page
- **Entity Types**: 18 total (8 industrial + 10 cybersecurity)

### Pipeline Performance
- **Queue Type**: Serial (in-memory)
- **Batch Size**: 100 entities per Neo4j insert
- **Timeout**: 5 minutes per agent
- **Deduplication**: SHA256 hash + entity (text, label) composite

---

## Key Findings

1. **NO v9 API Endpoint**: The system does NOT call `http://localhost:8001/api/v9/ner/extract`. The NER functionality is implemented as a Python agent using spaCy and pattern matching.

2. **Hybrid Approach**: Combines rule-based patterns (95%+ precision) with spaCy neural NER (85-92% precision) for optimal accuracy.

3. **18 Entity Types**: 8 industrial control system entities + 10 cybersecurity entities.

4. **Serial Processing**: Documents are processed serially through 3 agents: classifier → NER → ingestion.

5. **Neo4j Storage**: Entities stored as nodes with deduplication based on `(text, label)` composite key.

6. **Web Interface Integration**: Upload wizard (5 steps) → document queue → Python agents → Neo4j.

---

## Next Steps for Development

1. **Production Queue**: Replace in-memory Map with Redis-based job queue
2. **Parallel Processing**: Implement worker processes for parallel agent execution
3. **Real-time Updates**: WebSocket support for live progress updates
4. **Entity Linking**: Link extracted entities to external knowledge bases (DBpedia, Wikidata)
5. **Relationship Extraction**: Enhance SVO triple extraction for better graph relationships
6. **Confidence Tuning**: Train custom spaCy models for domain-specific entity recognition
7. **API Endpoint**: If needed, expose NER agent as REST API at `http://localhost:8001/api/v9/ner/extract`

---

## Support

**Documentation**:
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/docs/UPLOAD_PIPELINE.md`
- `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/docs/UPLOAD_IMPLEMENTATION_SUMMARY.md`

**Source Code**:
- NER Agent: `agents/ner_agent.py`
- Document Queue: `web_interface/lib/queue/documentQueue.ts`
- NLP Pipeline: `nlp_ingestion_pipeline.py`

**Tests**:
- `tests/test_ner_agent.py`
- `tests/test_ner_validation.py`
- `tests/test_ner_relationships.py`
- `tests/test_ner_direct.py`

---

**RESEARCH COMPLETE**
*Documented complete NER v9 integration flow from upload to Neo4j storage*
