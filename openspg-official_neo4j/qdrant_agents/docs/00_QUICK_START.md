# Qdrant Agents System - Quick Start Guide

**Get started with Qdrant agents in 5 minutes**

## Prerequisites

- Python 3.8+
- Qdrant running at `http://localhost:6333`
- OpenAI API key
- Qdrant API key

## Installation

```bash
# Navigate to project
cd /home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j

# Install dependencies
pip install -r qdrant_agents/requirements.txt

# Set environment variables
export QDRANT_API_KEY="your-qdrant-key"
export OPENAI_API_KEY="your-openai-key"
```

## Basic Usage

### 1. Use the Claude-Flow Bridge (Recommended)

```python
from qdrant_agents.integration import get_bridge

bridge = get_bridge()

# Search knowledge
result = bridge.search_knowledge(
    query="SAREF building sensors",
    wave=3,
    top_k=5
)

print(f"Found {result['count']} results")
for item in result['results']:
    print(f"  - {item['source_file']}: {item['score']:.3f}")
```

### 2. Store Agent Findings

```python
# Store a discovery
result = bridge.store_finding(
    finding="Property chains enable complex sensor queries",
    agent_name="coder",
    wave=4,
    tags=["pattern", "sensors"]
)

print(f"Stored with ID: {result['finding_id']}")
```

### 3. Record Decisions

```python
# Record an implementation decision
result = bridge.record_decision(
    decision="Use owl:ObjectProperty for sensor relationships",
    rationale="Enables transitive reasoning",
    wave=4,
    made_by="architect"
)

print(f"Decision ID: {result['decision_id']}")
```

## Hook Integration

### Pre-Task Hook

```bash
# Automatically retrieve knowledge before tasks
./qdrant_agents/hooks/pre_task_hook.sh \
  "Implement SAREF building sensors" \
  3 \
  "coder"
```

### Post-Task Hook

```bash
# Automatically store findings after tasks
export FINDING="Successfully implemented sensor hierarchy"
./qdrant_agents/hooks/post_task_hook.sh \
  "Implement SAREF building sensors" \
  3 \
  "coder" \
  "success"
```

### Wave Completion

```bash
# Process wave completion
./qdrant_agents/hooks/wave_complete_hook.sh 3 "SAREF Energy"
```

## CLI Usage

All agents have CLI interfaces for testing:

```bash
# Query agent
python3 qdrant_agents/core/qdrant_query_agent.py \
  "temperature measurement" \
  --wave 3 \
  --top-k 5

# Memory agent
python3 qdrant_agents/core/qdrant_memory_agent.py store \
  "Multi-level hierarchies work well" \
  --agent coder \
  --wave 4

# Analytics agent
python3 qdrant_agents/core/qdrant_analytics_agent.py metrics
```

## Next Steps

1. **[Architecture Overview](01_ARCHITECTURE.md)** - Understand system design
2. **[API Reference](02_API_REFERENCE.md)** - Complete API documentation
3. **[Integration Guide](03_INTEGRATION_GUIDE.md)** - Detailed integration patterns
4. **[Usage Examples](04_USAGE_EXAMPLES.md)** - Real-world examples

## Common Issues

**Issue**: `No module named 'structlog'`
**Solution**: `pip install structlog`

**Issue**: `The api_key client option must be set`
**Solution**: Set `export OPENAI_API_KEY="your-key"`

**Issue**: Search returns 0 results
**Solution**: Ensure Qdrant is running and collections are populated

## Support

- Documentation: `qdrant_agents/docs/`
- Issues: Check `QDRANT_AGENTS_COMPLETE.md`
- Logs: Structured logging via `structlog`
