# Qdrant Memory Manager Documentation

## Overview

The `QdrantMemoryManager` provides persistent memory and state tracking for the AEON system using Qdrant vector database. It enables:

- **Agent Activity Tracking**: Record all agent operations with full context
- **State Checkpoints**: Save and restore system state for recovery
- **Classification Learning**: Store user feedback to improve accuracy over time
- **Document Similarity**: Find similar documents using semantic embeddings
- **Cross-Session Persistence**: Maintain context across system restarts

## Architecture

### Storage Collections

1. **agent_activities**: All agent operations and their outcomes
2. **checkpoints**: System state snapshots for recovery
3. **classification_memory**: Classification decisions with user feedback
4. **document_embeddings**: Document vectors for similarity search

### Graceful Degradation

The manager automatically falls back to in-memory storage if:
- Qdrant server is unavailable
- `qdrant-client` is not installed
- Connection fails during operation

This ensures the system continues operating even without Qdrant.

## Installation

### Required Dependencies

```bash
pip install qdrant-client>=1.7.0 sentence-transformers>=2.2.0
```

### Optional: Run Qdrant Server

#### Docker (Recommended)
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

#### Docker Compose
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
```

## Usage

### Basic Initialization

```python
from memory.qdrant_memory_manager import QdrantMemoryManager

# Initialize with Qdrant server
memory = QdrantMemoryManager(host="localhost", port=6333)

# Initialize without Qdrant (in-memory mode)
memory = QdrantMemoryManager(use_qdrant=False)
```

### Track Agent Activities

```python
# Record agent activity
activity_id = memory.track_agent_activity(
    agent_name="ClassificationAgent",
    activity_type="document_classification",
    data={
        "file": "contract_001.pdf",
        "sector": "General Contractor",
        "confidence": 0.92
    },
    metadata={"model_version": "1.0"}
)

# Retrieve agent history
history = memory.get_agent_history("ClassificationAgent", limit=100)
for activity in history:
    print(f"{activity['timestamp']}: {activity['activity_type']}")
```

### Store and Restore Checkpoints

```python
# Save state checkpoint
checkpoint_id = memory.store_checkpoint(
    checkpoint_name="processing_batch_1",
    state_data={
        "total_files": 100,
        "processed_files": 50,
        "current_file": "document_051.pdf",
        "errors": []
    },
    metadata={"batch_number": 1}
)

# Restore from checkpoint
state = memory.retrieve_checkpoint("processing_batch_1")
if state:
    processed_files = state["state_data"]["processed_files"]
    current_file = state["state_data"]["current_file"]
    # Resume processing...
```

### Learn from Classification Decisions

```python
# Store classification with user feedback
decision_id = memory.store_classification_decision(
    file_path="documents/contract_abc.pdf",
    sector="General Contractor",
    subsector="Commercial Construction",
    confidence=0.88,
    user_feedback="Correct classification"
)

# Store correction
decision_id = memory.store_classification_decision(
    file_path="documents/subcontractor_xyz.pdf",
    sector="Subcontractor",
    subsector="Electrical",
    confidence=0.65,
    user_feedback="Incorrect - should be HVAC",
    metadata={"corrected": True, "correct_subsector": "HVAC"}
)
```

### Document Similarity Search

```python
# Generate embedding for new document
text = "Commercial construction contract for office building"
embedding = memory._generate_embedding(text)

# Store document embedding
memory.store_document_embedding(
    document_id="doc_001",
    embedding=embedding,
    metadata={
        "filename": "contract_abc.pdf",
        "sector": "General Contractor"
    }
)

# Find similar documents
similar_docs = memory.search_similar_documents(embedding, top_k=5)
for doc_id, score, metadata in similar_docs:
    print(f"Document {doc_id}: similarity={score:.3f}")
    print(f"  {metadata['filename']} - {metadata['sector']}")
```

## Integration with Agents

### BaseAgent Pattern

```python
from agents.base_agent import BaseAgent
from memory.qdrant_memory_manager import QdrantMemoryManager

class ClassificationAgent(BaseAgent):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.memory = QdrantMemoryManager()

    def _setup(self):
        """Agent-specific setup"""
        # Restore previous state if available
        checkpoint = self.memory.retrieve_checkpoint(f"{self.name}_state")
        if checkpoint:
            self.logger.info(f"Restored from checkpoint: {checkpoint['timestamp']}")

    def execute(self, input_data: Any) -> Any:
        """Main execution with memory tracking"""
        # Track start
        self.memory.track_agent_activity(
            agent_name=self.name,
            activity_type="execution_start",
            data={"input": str(input_data)[:100]}
        )

        try:
            result = self._process(input_data)

            # Track success
            self.memory.track_agent_activity(
                agent_name=self.name,
                activity_type="execution_success",
                data={"result": str(result)[:100]}
            )

            return result

        except Exception as e:
            # Track error
            self.memory.track_agent_activity(
                agent_name=self.name,
                activity_type="execution_error",
                data={"error": str(e)}
            )
            raise

    def save_state(self):
        """Save agent state"""
        self.memory.store_checkpoint(
            checkpoint_name=f"{self.name}_state",
            state_data={
                "processed_count": self.processed_count,
                "last_file": self.last_file,
                "errors": self.errors
            }
        )
```

### Multi-Agent Coordination

```python
class AgentCoordinator:
    def __init__(self):
        self.memory = QdrantMemoryManager()
        self.agents = {}

    def track_workflow(self, workflow_name: str, steps: List[str]):
        """Track multi-agent workflow"""
        workflow_id = f"workflow_{workflow_name}_{datetime.now().isoformat()}"

        self.memory.store_checkpoint(
            checkpoint_name=workflow_id,
            state_data={
                "workflow_name": workflow_name,
                "steps": steps,
                "current_step": 0,
                "status": "started"
            }
        )

        return workflow_id

    def update_workflow(self, workflow_id: str, step_index: int, status: str):
        """Update workflow progress"""
        checkpoint = self.memory.retrieve_checkpoint(workflow_id)
        if checkpoint:
            state = checkpoint["state_data"]
            state["current_step"] = step_index
            state["status"] = status

            self.memory.store_checkpoint(
                checkpoint_name=workflow_id,
                state_data=state
            )
```

## API Reference

### QdrantMemoryManager

#### Constructor

```python
QdrantMemoryManager(
    host: str = "localhost",
    port: int = 6333,
    use_qdrant: bool = True,
    embedding_model: str = "all-MiniLM-L6-v2"
)
```

#### Methods

##### track_agent_activity
```python
track_agent_activity(
    agent_name: str,
    activity_type: str,
    data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> str
```
Track agent activity and return activity ID.

##### store_checkpoint
```python
store_checkpoint(
    checkpoint_name: str,
    state_data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> str
```
Store state checkpoint and return checkpoint ID.

##### retrieve_checkpoint
```python
retrieve_checkpoint(checkpoint_name: str) -> Optional[Dict[str, Any]]
```
Retrieve checkpoint by name.

##### store_classification_decision
```python
store_classification_decision(
    file_path: str,
    sector: str,
    subsector: str,
    confidence: float,
    user_feedback: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str
```
Store classification decision with user feedback.

##### search_similar_documents
```python
search_similar_documents(
    document_embedding: List[float],
    top_k: int = 5
) -> List[Tuple[str, float, Dict[str, Any]]]
```
Search for similar documents. Returns list of (document_id, score, metadata).

##### get_agent_history
```python
get_agent_history(
    agent_name: str,
    limit: int = 100
) -> List[Dict[str, Any]]
```
Get activity history for specific agent.

##### store_document_embedding
```python
store_document_embedding(
    document_id: str,
    embedding: List[float],
    metadata: Dict[str, Any]
) -> bool
```
Store document embedding for similarity search.

##### get_statistics
```python
get_statistics() -> Dict[str, Any]
```
Get memory manager statistics and status.

##### clear_collection
```python
clear_collection(collection_name: str) -> bool
```
Clear all data from a collection (use with caution).

## Performance Considerations

### Embedding Generation
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Speed: ~50ms per document on CPU
- Quality: Good balance of speed and accuracy

### Vector Search
- Top-K search: ~1-5ms for collections up to 100K documents
- Scales to millions of documents with proper indexing
- HNSW algorithm provides fast approximate nearest neighbor search

### Memory Usage
- Embeddings: ~1.5 KB per document (384 floats)
- Metadata: Varies by content, typically 1-5 KB
- In-memory fallback: Limited by RAM, suitable for < 10K items

## Best Practices

### 1. Checkpoint Naming
Use descriptive, hierarchical names:
```python
# Good
"batch_processing_2024_11_02_batch_5"
"classification_agent_state_v1"

# Bad
"checkpoint1"
"state"
```

### 2. Activity Types
Use consistent activity type naming:
```python
ACTIVITY_TYPES = {
    "execution_start",
    "execution_success",
    "execution_error",
    "classification",
    "validation",
    "preprocessing"
}
```

### 3. Metadata Structure
Include useful metadata for querying:
```python
metadata = {
    "version": "1.0",
    "environment": "production",
    "batch_id": "batch_123",
    "priority": "high"
}
```

### 4. Error Handling
Always handle Qdrant unavailability gracefully:
```python
try:
    activity_id = memory.track_agent_activity(...)
except Exception as e:
    logger.warning(f"Memory tracking failed: {e}")
    # Continue without tracking
```

## Troubleshooting

### Connection Issues
```python
# Check statistics to see actual mode
stats = memory.get_statistics()
print(f"Mode: {stats['mode']}")  # 'qdrant' or 'in-memory'

# If in-memory when expecting Qdrant
if stats['mode'] == 'in-memory' and stats['qdrant_available']:
    print("Qdrant client available but not connected")
    # Check server: curl http://localhost:6333/
```

### Embedding Issues
```python
# Check if embeddings are available
if not memory.embedding_model:
    print("Install: pip install sentence-transformers")
```

### Collection Management
```python
# Clear corrupted collection
memory.clear_collection("agent_activities")

# Check collection status
stats = memory.get_statistics()
if "collections" in stats:
    for name, info in stats["collections"].items():
        print(f"{name}: {info['points_count']} points")
```

## Examples

See `/examples/qdrant_memory_example.py` for comprehensive usage examples.

## Testing

Run tests:
```bash
pytest tests/test_qdrant_memory_manager.py -v
```

## Future Enhancements

- [ ] Batch operations for bulk inserts
- [ ] Async support for high-throughput scenarios
- [ ] Custom embedding models per collection
- [ ] Time-based data retention policies
- [ ] Query builder for complex searches
- [ ] Integration with monitoring systems
