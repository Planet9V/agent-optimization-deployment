# Qdrant Schema Update: Psychometric Tensors

**Enhancement**: E27-Tensor-Upgrade
**Collection**: `agent_memory`

## Overview
We are enhancing the `agent_memory` collection to support **Psychometric Tensors**. This allows agents to query memories not just by semantic content, but by "Emotional Resonance" (e.g., finding memories that match a specific high-stress/high-neuroticism state).

## Schema Definition

### Payload Extension
The existing payload will be extended with a `tensor` field.

```json
{
  "payload": {
    "agent_id": "string",
    "task_id": "string",
    "decision": "string",
    "rationale": "string",
    "timestamp": "datetime",
    "psychometric_tensor": {
      "disc": [0.8, 0.2, 0.5, 0.1], // Dominance, Influence, Steadiness, Conscientiousness
      "ocean": [0.7, 0.9, 0.3, 0.6, 0.2] // Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
    }
  }
}
```

### Vector Configuration
We will maintain the existing BERT embeddings (768-dim) for the *content* of the memory. The tensor data is currently stored as **Payload** for filtering, rather than a separate vector index, to avoid complex multi-vector setup in the current phase.

## Usage Example (Python Client)

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient("localhost", port=6333)

# Filter memories by High Conscientiousness (C > 0.8)
# Useful for finding "Best Practices" or "SOPs"
results = client.search(
    collection_name="agent_memory",
    query_vector=vector_embedding,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="payload.psychometric_tensor.ocean[1]", # Index 1 is Conscientiousness
                range=models.Range(gte=0.8)
            )
        ]
    ),
    limit=5
)
```
