# GAP-ML-003: NER11 Gold Pipeline Integration

**File:** 09_GAP-ML-003_NER11_PIPELINE.md
**Gap ID:** GAP-ML-003
**Created:** 2025-11-30
**Priority:** CRITICAL
**Phase:** 3 - Data Integration
**Effort:** XL (8+ weeks)
**Status:** IN PROGRESS (Model trained, pipeline incomplete)

---

## Problem Statement

**Current State:**
- NER11 Gold model trained and available (566+ entity types)
- Manual extraction from threat reports only
- No automated ingestion pipeline
- No streaming data integration

**Desired State:**
- Streaming ingestion from RSS, APIs, dark web sources
- Automatic entity-to-graph resolution
- Real-time graph hydration
- Entity linking with embedding similarity

---

## Current NER11 Status

### Model Capabilities
- **Entity Types:** 566+ (NER11 Gold Schema)
- **F1 Score:** ~99% on test set
- **Framework:** spaCy-based
- **Training Data:** Custom cybersecurity corpus

### Super Node Hierarchy (16 Super Labels)
```
SECTOR (16 CISA sectors)
├── FACILITY
│   ├── EQUIPMENT
│   │   ├── COMPONENT
│   │   │   └── PARAMETER
│   │   └── PROTOCOL
│   └── PERSONNEL
├── VULNERABILITY (CVE)
│   ├── CWE (Weakness)
│   └── CAPEC (Attack Pattern)
├── THREAT_ACTOR
│   ├── CAMPAIGN
│   └── TOOL
└── INDICATOR (IoC)
```

---

## Technical Specification

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NER11 Ingestion Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  Data Sources│         │  Kafka       │                 │
│  │  - RSS Feeds │────────▶│  Topics      │                 │
│  │  - APIs      │         │  - raw_docs  │                 │
│  │  - Dark Web  │         │  - entities  │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                  │                          │
│                           ┌──────▼───────┐                 │
│                           │  NER11 Gold  │                 │
│                           │  Extractor   │                 │
│                           │  (gRPC)      │                 │
│                           └──────┬───────┘                 │
│                                  │                          │
│                           ┌──────▼───────┐                 │
│                           │  Entity      │                 │
│                           │  Resolver    │                 │
│                           │  (Embeddings)│                 │
│                           └──────┬───────┘                 │
│                                  │                          │
│         ┌────────────────────────┼────────────────────┐    │
│         │                        │                    │    │
│  ┌──────▼───────┐   ┌──────▼───────┐   ┌──────▼───────┐  │
│  │  Neo4j       │   │  Qdrant      │   │  Event       │  │
│  │  (Graph)     │   │  (Vectors)   │   │  Stream      │  │
│  └──────────────┘   └──────────────┘   └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Entity Resolution with Embeddings

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

class EntityResolver:
    """
    Resolve extracted entities to existing graph nodes using embeddings.
    """

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qdrant = QdrantClient(url="http://172.18.0.6:6333")

    async def resolve_entity(
        self,
        entity_text: str,
        entity_type: str,
        threshold: float = 0.85
    ) -> dict:
        """
        Resolve extracted entity to existing node or create new.

        Args:
            entity_text: Extracted entity text
            entity_type: NER11 entity type
            threshold: Similarity threshold for matching

        Returns:
            {matched: bool, node_id: str, similarity: float, action: 'MATCHED'|'CREATED'}
        """
        # Generate embedding
        embedding = self.model.encode(entity_text).tolist()

        # Search existing entities
        results = self.qdrant.search(
            collection_name=f"entities_{entity_type.lower()}",
            query_vector=embedding,
            limit=5
        )

        if results and results[0].score >= threshold:
            return {
                'matched': True,
                'node_id': results[0].payload['node_id'],
                'similarity': results[0].score,
                'action': 'MATCHED'
            }
        else:
            # Create new entity
            new_id = await self.create_entity(entity_text, entity_type, embedding)
            return {
                'matched': False,
                'node_id': new_id,
                'similarity': 0,
                'action': 'CREATED'
            }
```

### Kafka Topic Schema

```yaml
# raw_docs topic
{
  "doc_id": "DOC-2025-001",
  "source": "RSS_FEED_CISA",
  "source_url": "https://...",
  "title": "...",
  "content": "...",
  "published_at": "2025-11-30T12:00:00Z",
  "ingested_at": "2025-11-30T12:05:00Z"
}

# entities topic
{
  "doc_id": "DOC-2025-001",
  "entities": [
    {
      "text": "CVE-2024-1234",
      "type": "VULNERABILITY",
      "start": 45,
      "end": 58,
      "confidence": 0.98
    },
    {
      "text": "APT28",
      "type": "THREAT_ACTOR",
      "start": 120,
      "end": 125,
      "confidence": 0.95
    }
  ],
  "extracted_at": "2025-11-30T12:05:30Z"
}

# graph_updates topic
{
  "operation": "MERGE",
  "node_type": "THREAT_ACTOR",
  "node_id": "APT28",
  "properties": {
    "name": "APT28",
    "aliases": ["Fancy Bear", "Sofacy"],
    "last_seen": "2025-11-30"
  },
  "relationships": [
    {
      "type": "EXPLOITED",
      "target_id": "CVE-2024-1234",
      "properties": {"observed_at": "2025-11-30"}
    }
  ]
}
```

---

## Implementation Steps

### Step 1: Kafka Infrastructure (Week 1-2)
- [ ] Set up Kafka cluster
- [ ] Create topics (raw_docs, entities, graph_updates)
- [ ] Configure retention and partitioning
- [ ] Set up monitoring

### Step 2: NER11 gRPC Service (Week 3-4)
- [ ] Deploy NER11 model as gRPC service
- [ ] Create Kafka consumer for raw_docs
- [ ] Implement entity extraction pipeline
- [ ] Produce to entities topic

### Step 3: Entity Resolution (Week 5-6)
- [ ] Create Qdrant collections for each entity type
- [ ] Implement EntityResolver service
- [ ] Build entity linking pipeline
- [ ] Handle entity merging/deduplication

### Step 4: Neo4j Integration (Week 7-8)
- [ ] Create Neo4j streaming import procedure
- [ ] Implement MERGE operations for entities
- [ ] Create relationship hydration
- [ ] Add event triggers for EWS

### Step 5: Data Sources (Week 8+)
- [ ] Integrate CISA RSS feeds
- [ ] Integrate NVD API
- [ ] Integrate MITRE ATT&CK updates
- [ ] Add monitoring and alerting

---

## Success Criteria

- [ ] NER11 processing >100 documents/hour
- [ ] Entity resolution accuracy >90%
- [ ] Real-time graph updates within 5 minutes of ingestion
- [ ] All 566+ entity types extractable
- [ ] Deduplication working correctly

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| NER11 accuracy degradation | High | Medium | Continuous monitoring, retraining pipeline |
| Entity resolution false positives | Medium | Medium | Manual review queue, threshold tuning |
| Kafka throughput bottleneck | Medium | Low | Horizontal scaling, partition tuning |

---

## Dependencies

- Kafka infrastructure
- NER11 Gold model deployed
- Qdrant operational
- Neo4j streaming import

---

## Memory Keys

- `gap-ml-003-pipeline`: Pipeline configuration
- `gap-ml-003-entity-types`: Entity type mappings
- `gap-ml-003-sources`: Data source configurations

---

## References

- NER11 Schema: `2_NER11_Gold_Schema_Architecture/`
- Entity Types: Enhancement documentation
- Neo4j Schema: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/01_MCKENNEY_LACAN_NEO4J_SCHEMA.cypher`
