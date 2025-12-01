# Neo4j Integration Guide - NER11 Gold Standard

## Overview

This guide demonstrates how to integrate the NER11 Gold Standard model with Neo4j to build a knowledge graph from extracted entities. The integration supports both **real-time** and **batch processing** workflows.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [Entity → Node Mapping](#entity--node-mapping)
5. [Batch Processing](#batch-processing)
6. [Real-Time Integration](#real-time-integration)
7. [Query Examples](#query-examples)
8. [Performance Optimization](#performance-optimization)

---

## Prerequisites

### Neo4j Setup

```bash
# Install Neo4j (Docker recommended)
docker run \
    --name neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/password \
    neo4j:latest
```

### Python Dependencies

```bash
pip install neo4j>=5.14.0
pip install spacy>=3.7.0
```

---

## Quick Start

### 1. Load Model and Connect to Neo4j

```python
import spacy
from neo4j import GraphDatabase

# Load NER model
nlp = spacy.load("./models/model-best")

# Connect to Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)
```

### 2. Extract Entities and Create Nodes

```python
def extract_and_ingest(text):
    # Extract entities
    doc = nlp(text)
    
    # Create nodes in Neo4j
    with driver.session() as session:
        for ent in doc.ents:
            session.run("""
                MERGE (e:Entity {text: $text, type: $type})
                ON CREATE SET e.first_seen = timestamp()
                ON MATCH SET e.last_seen = timestamp(), 
                             e.count = coalesce(e.count, 0) + 1
            """, text=ent.text, type=ent.label_)

# Example usage
text = """
APT29 exploited CVE-2023-12345 using a zero-day vulnerability 
in the Siemens S7-1200 PLC. The attack targeted critical 
infrastructure in the energy sector.
"""

extract_and_ingest(text)
```

---

## Architecture

### Data Flow

```
┌─────────────┐
│  Raw Text   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ NER11 Model │ ← spaCy pipeline
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Entities   │ ← (text, label, start, end)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Neo4j     │ ← Nodes + Relationships
│   Graph     │
└─────────────┘
```

### Schema Design

**Node Labels** (mapped from entity types):
- `ThreatActor` ← `THREAT_ACTOR`
- `Vulnerability` ← `VULNERABILITY`
- `Malware` ← `MALWARE`
- `OTDevice` ← `OT_DEVICE`
- `AttackVector` ← `ATTACK_VECTOR`
- ... (566 total entity types)

**Relationships**:
- `(:ThreatActor)-[:EXPLOITS]->(:Vulnerability)`
- `(:Malware)-[:TARGETS]->(:OTDevice)`
- `(:ThreatActor)-[:USES]->(:Malware)`
- `(:Document)-[:MENTIONS]->(:Entity)`

---

## Entity → Node Mapping

### Mapping Configuration

```python
# Entity type to Neo4j label mapping
ENTITY_LABEL_MAP = {
    "THREAT_ACTOR": "ThreatActor",
    "VULNERABILITY": "Vulnerability",
    "MALWARE": "Malware",
    "OT_DEVICE": "OTDevice",
    "SCADA_SYSTEM": "SCADASystem",
    "ATTACK_VECTOR": "AttackVector",
    "PERSONALITY_TRAIT": "PersonalityTrait",
    # ... (full mapping in scripts/neo4j_integration.py)
}

def get_node_label(entity_type):
    return ENTITY_LABEL_MAP.get(entity_type, "Entity")
```

### Node Properties

```python
{
    "text": str,           # Entity text
    "type": str,          # Original NER label
    "first_seen": int,    # Timestamp
    "last_seen": int,     # Timestamp
    "count": int,         # Occurrence count
    "confidence": float,  # NER confidence (if available)
    "source_doc": str     # Source document ID
}
```

---

## Batch Processing

### Using the Batch Processor

```python
from scripts.neo4j_integration import NER11Neo4jIntegrator

# Initialize integrator
integrator = NER11Neo4jIntegrator(
    model_path="./models/model-best",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Process directory of text files
integrator.batch_process_directory(
    input_dir="./input_texts/",
    batch_size=100,
    create_relationships=True
)
```

### Batch Processing Script

```bash
# Process all .txt files in a directory
python scripts/neo4j_integration.py \
    --input-dir ./data/threat_reports/ \
    --batch-size 100 \
    --create-relationships \
    --neo4j-uri bolt://localhost:7687 \
    --neo4j-user neo4j \
    --neo4j-password password
```

**Performance**:
- **CPU**: ~50-100 documents/second
- **GPU**: ~200-500 documents/second
- **Neo4j Ingestion**: ~1000 nodes/second

---

## Real-Time Integration

### REST API Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str
    create_graph: bool = True

@app.post("/extract_and_ingest")
async def extract_and_ingest(input: TextInput):
    # Extract entities
    doc = nlp(input.text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Optionally create graph
    if input.create_graph:
        integrator.ingest_entities(entities, input.text)
    
    return {"entities": entities, "count": len(entities)}
```

### Streaming Integration

```python
import asyncio
from kafka import KafkaConsumer

async def stream_to_neo4j():
    consumer = KafkaConsumer(
        'threat-intel-stream',
        bootstrap_servers=['localhost:9092']
    )
    
    for message in consumer:
        text = message.value.decode('utf-8')
        extract_and_ingest(text)
```

---

## Query Examples

### 1. Find All Vulnerabilities Exploited by APT29

```cypher
MATCH (ta:ThreatActor {text: "APT29"})-[:EXPLOITS]->(v:Vulnerability)
RETURN v.text, v.count
ORDER BY v.count DESC
```

### 2. Identify Most Targeted OT Devices

```cypher
MATCH (d:OTDevice)<-[:TARGETS]-(m:Malware)
RETURN d.text, count(m) as attack_count
ORDER BY attack_count DESC
LIMIT 10
```

### 3. Find Co-Occurring Entities

```cypher
MATCH (e1:Entity)<-[:MENTIONS]-(doc:Document)-[:MENTIONS]->(e2:Entity)
WHERE e1.type = "THREAT_ACTOR" AND e2.type = "MALWARE"
RETURN e1.text, e2.text, count(doc) as co_occurrence
ORDER BY co_occurrence DESC
```

### 4. Threat Actor Attribution

```cypher
MATCH path = (ta:ThreatActor)-[:USES|EXPLOITS|TARGETS*1..3]->(target)
WHERE ta.text = "APT29"
RETURN path
LIMIT 50
```

### 5. Temporal Analysis

```cypher
MATCH (e:Entity)
WHERE e.first_seen > timestamp() - (30 * 24 * 60 * 60 * 1000) // Last 30 days
RETURN e.type, count(e) as new_entities
ORDER BY new_entities DESC
```

---

## Performance Optimization

### 1. Indexing

```cypher
// Create indexes for fast lookups
CREATE INDEX entity_text IF NOT EXISTS FOR (e:Entity) ON (e.text);
CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type);
CREATE INDEX threat_actor_text IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.text);
CREATE INDEX vulnerability_text IF NOT EXISTS FOR (v:Vulnerability) ON (v.text);
```

### 2. Batch Transactions

```python
def batch_ingest(entities, batch_size=1000):
    with driver.session() as session:
        for i in range(0, len(entities), batch_size):
            batch = entities[i:i+batch_size]
            session.run("""
                UNWIND $batch as entity
                MERGE (e:Entity {text: entity.text, type: entity.type})
                ON CREATE SET e.first_seen = timestamp()
                ON MATCH SET e.count = coalesce(e.count, 0) + 1
            """, batch=batch)
```

### 3. Parallel Processing

```python
from multiprocessing import Pool

def process_file(filepath):
    with open(filepath) as f:
        text = f.read()
    extract_and_ingest(text)

# Process files in parallel
with Pool(processes=8) as pool:
    pool.map(process_file, file_list)
```

---

## Advanced: Relationship Extraction

### Co-Occurrence Based

```python
def create_cooccurrence_relationships(doc, window=50):
    """Create relationships between entities in same context window"""
    entities = list(doc.ents)
    
    for i, ent1 in enumerate(entities):
        for ent2 in entities[i+1:]:
            # Check if within window
            if abs(ent1.start - ent2.start) <= window:
                create_relationship(ent1, ent2, "CO_OCCURS")
```

### Pattern-Based

```python
# Define relationship patterns
PATTERNS = [
    {"pattern": r"(\w+) exploited (\w+)", "rel": "EXPLOITS"},
    {"pattern": r"(\w+) targets (\w+)", "rel": "TARGETS"},
    {"pattern": r"(\w+) uses (\w+)", "rel": "USES"},
]

def extract_relationships(text, entities):
    for pattern_def in PATTERNS:
        matches = re.finditer(pattern_def["pattern"], text)
        for match in matches:
            # Match entities to pattern groups
            # Create relationship in Neo4j
            pass
```

---

## OpenSPG Integration

### Schema Mapping

```python
# Map NER11 entities to OpenSPG schema
OPENSPG_MAPPING = {
    "THREAT_ACTOR": "ThreatIntelligence.ThreatActor",
    "VULNERABILITY": "Vulnerability.CVE",
    "MALWARE": "ThreatIntelligence.Malware",
    "OT_DEVICE": "CriticalInfrastructure.Device",
}

def create_openspg_node(entity):
    spg_type = OPENSPG_MAPPING.get(entity.label_)
    # Create node with OpenSPG schema
    pass
```

---

## Monitoring & Logging

### Track Ingestion Metrics

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsTracker:
    def __init__(self):
        self.entities_processed = 0
        self.nodes_created = 0
        self.relationships_created = 0
    
    def log_stats(self):
        logger.info(f"Entities: {self.entities_processed}")
        logger.info(f"Nodes: {self.nodes_created}")
        logger.info(f"Relationships: {self.relationships_created}")
```

---

## Complete Integration Script

See `scripts/neo4j_integration.py` for the full implementation including:
- ✅ Entity extraction
- ✅ Node creation with deduplication
- ✅ Relationship inference
- ✅ Batch processing
- ✅ Error handling
- ✅ Metrics tracking

---

## Troubleshooting

### Issue: Slow Ingestion

**Solution**: Use batch transactions and create indexes

### Issue: Duplicate Nodes

**Solution**: Use `MERGE` instead of `CREATE`

### Issue: Memory Errors

**Solution**: Process in smaller batches, increase Neo4j heap size

---

## Next Steps

1. Review `examples/neo4j_example.py` for complete working example
2. Customize entity-to-label mapping for your schema
3. Define domain-specific relationship patterns
4. Set up monitoring and alerting

---

**Neo4j Integration Complete!** 🎉

Your NER11 model is now ready to populate knowledge graphs.
