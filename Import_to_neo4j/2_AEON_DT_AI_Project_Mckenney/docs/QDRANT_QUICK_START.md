# Qdrant Memory Manager - Quick Start Guide

## 🚀 Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install qdrant-client>=1.7.0 sentence-transformers>=2.2.0
```

### Step 2: Start Qdrant Server (Optional)
```bash
# Docker (recommended)
docker run -d -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    --name qdrant \
    qdrant/qdrant
```

> **Note**: System works without Qdrant server using in-memory fallback

## 📝 Basic Usage (2 minutes)

### Initialize
```python
from memory.qdrant_memory_manager import QdrantMemoryManager

# With Qdrant server
memory = QdrantMemoryManager()

# Without Qdrant (in-memory mode)
memory = QdrantMemoryManager(use_qdrant=False)
```

### Track Activities
```python
# Record agent activity
activity_id = memory.track_agent_activity(
    agent_name="ClassificationAgent",
    activity_type="classification",
    data={"file": "contract.pdf", "result": "GC"}
)

# Get history
history = memory.get_agent_history("ClassificationAgent", limit=10)
```

### Save/Restore State
```python
# Save checkpoint
memory.store_checkpoint(
    checkpoint_name="batch_1",
    state_data={"processed": 50, "current": "file_051.pdf"}
)

# Restore checkpoint
state = memory.retrieve_checkpoint("batch_1")
```

## 🔧 Integration with BaseAgent (3 minutes)

```python
from agents.base_agent import BaseAgent
from memory.qdrant_memory_manager import QdrantMemoryManager

class MyAgent(BaseAgent):
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.memory = QdrantMemoryManager()

    def _setup(self):
        # Restore previous state
        checkpoint = self.memory.retrieve_checkpoint(f"{self.name}_state")
        if checkpoint:
            self.restore_from(checkpoint)

    def execute(self, input_data: Any) -> Any:
        # Track execution start
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
        self.memory.store_checkpoint(
            checkpoint_name=f"{self.name}_state",
            state_data=self.get_state()
        )
```

## 📊 Common Patterns

### Pattern 1: Batch Processing with Checkpoints
```python
def process_batch(files, memory, batch_name):
    # Restore progress if exists
    checkpoint = memory.retrieve_checkpoint(batch_name)
    start_idx = checkpoint["state_data"]["processed"] if checkpoint else 0

    for i, file in enumerate(files[start_idx:], start=start_idx):
        try:
            process_file(file)

            # Save progress every 10 files
            if i % 10 == 0:
                memory.store_checkpoint(
                    checkpoint_name=batch_name,
                    state_data={"processed": i, "total": len(files)}
                )
        except Exception as e:
            memory.track_agent_activity(
                agent_name="BatchProcessor",
                activity_type="error",
                data={"file": file, "error": str(e)}
            )
```

### Pattern 2: Learning from Feedback
```python
def classify_with_learning(document, memory):
    # Classify
    sector, subsector, confidence = classify_document(document)

    # Show to user
    user_feedback = get_user_feedback(document, sector, subsector)

    # Store decision
    memory.store_classification_decision(
        file_path=document.path,
        sector=sector,
        subsector=subsector,
        confidence=confidence,
        user_feedback=user_feedback,
        metadata={
            "corrected": user_feedback.startswith("Incorrect"),
            "timestamp": datetime.now().isoformat()
        }
    )
```

### Pattern 3: Multi-Agent Coordination
```python
class WorkflowCoordinator:
    def __init__(self):
        self.memory = QdrantMemoryManager()

    def run_workflow(self, workflow_name, agents):
        # Create workflow checkpoint
        workflow_id = f"workflow_{workflow_name}_{datetime.now().isoformat()}"

        self.memory.store_checkpoint(
            checkpoint_name=workflow_id,
            state_data={
                "steps": [agent.name for agent in agents],
                "current_step": 0,
                "status": "started"
            }
        )

        # Run each agent
        for i, agent in enumerate(agents):
            try:
                result = agent.run()

                # Update workflow progress
                self.memory.track_agent_activity(
                    agent_name="WorkflowCoordinator",
                    activity_type="step_complete",
                    data={"step": i, "agent": agent.name, "result": result}
                )

            except Exception as e:
                # Save error state
                self.memory.store_checkpoint(
                    checkpoint_name=workflow_id,
                    state_data={
                        "status": "failed",
                        "failed_step": i,
                        "error": str(e)
                    }
                )
                raise
```

## 🔍 Debugging & Monitoring

### Check Status
```python
# Get statistics
stats = memory.get_statistics()
print(f"Mode: {stats['mode']}")  # 'qdrant' or 'in-memory'

# Check collections (if using Qdrant)
if "collections" in stats:
    for name, info in stats["collections"].items():
        print(f"{name}: {info['points_count']} items")
```

### View Agent History
```python
# Get recent activities
history = memory.get_agent_history("MyAgent", limit=20)
for activity in history:
    print(f"{activity['timestamp']}: {activity['activity_type']}")
    print(f"  Data: {activity['data']}")
```

### Clear Data (Development Only)
```python
# Clear a collection (use with caution!)
memory.clear_collection("agent_activities")
```

## 🎯 Best Practices

### 1. Checkpoint Naming
```python
# ✅ Good: Descriptive, hierarchical
"batch_processing_2024_11_02_batch_5"
"agent_state_classification_v1"

# ❌ Bad: Generic, unclear
"checkpoint1"
"state"
```

### 2. Activity Types
```python
# ✅ Use consistent activity type constants
ACTIVITY_TYPES = {
    "execution_start",
    "execution_success",
    "execution_error",
    "classification",
    "validation"
}

activity_id = memory.track_agent_activity(
    agent_name="MyAgent",
    activity_type=ACTIVITY_TYPES["execution_start"],
    data=data
)
```

### 3. Error Handling
```python
# ✅ Always handle memory operations gracefully
try:
    memory.track_agent_activity(...)
except Exception as e:
    logger.warning(f"Memory tracking failed: {e}")
    # Continue processing - don't fail on memory issues
```

## 📚 More Resources

- **Full Documentation**: `/docs/QDRANT_MEMORY_MANAGER.md`
- **Test Examples**: `/tests/test_qdrant_memory_manager.py`
- **Complete Examples**: `/examples/qdrant_memory_example.py`
- **Implementation Summary**: `/docs/QDRANT_IMPLEMENTATION_SUMMARY.md`

## 🐛 Troubleshooting

### Issue: "sentence-transformers not available"
```bash
pip install sentence-transformers>=2.2.0
```

### Issue: Qdrant connection failed
```bash
# Check if Qdrant is running
curl http://localhost:6333/

# System will automatically use in-memory fallback
# Check with: stats = memory.get_statistics()
```

### Issue: Slow embedding generation
```python
# Use smaller model or disable embeddings for high-throughput
memory = QdrantMemoryManager(embedding_model=None)  # Disables embeddings
```

## ⚡ Performance Tips

1. **Batch Checkpoints**: Save state every N operations, not every single operation
2. **Activity Filtering**: Track only important activities, not every minor step
3. **Metadata Limits**: Keep metadata concise, don't store large objects
4. **In-Memory Mode**: Use for development/testing, Qdrant for production

## 🎉 You're Ready!

Start integrating QdrantMemoryManager into your agents:

```python
from memory.qdrant_memory_manager import QdrantMemoryManager

memory = QdrantMemoryManager()

# Track everything your agents do
# Never lose state again
# Learn from user feedback
# Find similar documents instantly
```

Happy coding! 🚀
