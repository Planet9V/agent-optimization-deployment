# NER11 Semantic Search API - Testing Guide

**File:** SEMANTIC_SEARCH_API_TESTING.md
**Created:** 2025-12-01
**Version:** 1.0.0
**Task:** TASKMASTER Task 1.5 - Semantic Search Endpoint
**Status:** ACTIVE

## Overview

The NER11 Gold Standard API now includes semantic search capabilities with hierarchical filtering. This document provides comprehensive testing instructions for the new `/search/semantic` endpoint.

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ner` | POST | Extract named entities from text |
| `/search/semantic` | POST | Semantic search with hierarchical filtering |
| `/health` | GET | Health check with service status |
| `/info` | GET | Model information and capabilities |
| `/docs` | GET | Interactive Swagger documentation |

## Prerequisites

### 1. Start Required Services

```bash
# Start Qdrant (if not already running)
docker start openspg-qdrant || docker run -d \
  --name openspg-qdrant \
  -p 6333:6333 \
  qdrant/qdrant

# Verify Qdrant is running
curl http://localhost:6333/health
```

### 2. Start NER11 API Server

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Set environment variables (optional)
export MODEL_PATH="models/ner11_v3/model-best"
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export QDRANT_COLLECTION="ner11_entities_hierarchical"

# Start the server
python serve_model.py
```

The server will start on `http://localhost:8000` with automatic Swagger docs at `http://localhost:8000/docs`.

## Basic Testing

### 1. Health Check

```bash
# Check API health and service availability
curl -X GET http://localhost:8000/health

# Expected output:
{
  "status": "healthy",
  "ner_model": "loaded",
  "semantic_search": "available",
  "version": "2.0.0"
}
```

### 2. Model Information

```bash
# Get model capabilities and hierarchy information
curl -X GET http://localhost:8000/info | jq

# Expected output includes:
{
  "model_name": "NER11 Gold Standard",
  "version": "3.0",
  "api_version": "2.0.0",
  "capabilities": {
    "named_entity_recognition": true,
    "semantic_search": true,
    "hierarchical_filtering": true
  },
  "hierarchy_info": {
    "tier1_labels": 60,
    "tier2_types": 566,
    "filtering": {
      "label_filter": "Tier 1 NER label filtering",
      "fine_grained_filter": "Tier 2 fine-grained type filtering (566 types)",
      "confidence_threshold": "Minimum confidence filtering"
    }
  }
}
```

### 3. NER Extraction (Original Endpoint)

```bash
# Extract entities from text
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{
    "text": "WannaCry ransomware exploited CVE-2017-0144 targeting SCADA systems."
  }' | jq

# Expected output:
{
  "entities": [
    {"text": "WannaCry", "label": "MALWARE", "start": 0, "end": 8},
    {"text": "CVE-2017-0144", "label": "VULNERABILITY", "start": 31, "end": 44},
    {"text": "SCADA", "label": "INFRASTRUCTURE", "start": 55, "end": 60}
  ],
  "doc_length": 15
}
```

## Semantic Search Testing

### 4. Basic Semantic Search (No Filters)

```bash
# Search for ransomware-related entities
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware attack",
    "limit": 5
  }' | jq

# Expected output:
{
  "results": [
    {
      "score": 0.892,
      "entity": "WannaCry",
      "ner_label": "MALWARE",
      "fine_grained_type": "RANSOMWARE",
      "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",
      "confidence": 1.0,
      "doc_id": "test_doc_001"
    }
  ],
  "query": "ransomware attack",
  "filters_applied": {
    "label_filter": null,
    "fine_grained_filter": null,
    "confidence_threshold": 0.0
  },
  "total_results": 5
}
```

### 5. Tier 1 Filtering (Label Filter)

```bash
# Search with NER label filter (Tier 1 - 60 labels)
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "threat actor",
    "limit": 10,
    "label_filter": "THREAT_ACTOR"
  }' | jq

# Only returns entities with ner_label = "THREAT_ACTOR"
```

### 6. Tier 2 Filtering (Fine-Grained Type Filter) - CRITICAL FEATURE

```bash
# Search with fine-grained type filter (Tier 2 - 566 types)
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "control system",
    "limit": 10,
    "fine_grained_filter": "SCADA_SERVER"
  }' | jq

# Only returns entities with fine_grained_type = "SCADA_SERVER"
# This is the KEY feature - precise 566-type filtering
```

### 7. Combined Hierarchical Filtering

```bash
# Search with both Tier 1 and Tier 2 filters
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "industrial network protocol",
    "limit": 5,
    "label_filter": "PROTOCOL",
    "fine_grained_filter": "MODBUS_TCP"
  }' | jq

# Returns only PROTOCOL entities with fine_grained_type MODBUS_TCP
```

### 8. Confidence Threshold Filtering

```bash
# Search with confidence threshold
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vulnerability exploitation",
    "limit": 10,
    "confidence_threshold": 0.8
  }' | jq

# Only returns entities with confidence >= 0.8
```

### 9. Complex Query with All Filters

```bash
# Advanced search with all filtering options
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "advanced persistent threat campaign",
    "limit": 20,
    "label_filter": "THREAT_ACTOR",
    "fine_grained_filter": "APT_GROUP",
    "confidence_threshold": 0.7
  }' | jq

# Precise search:
# - Semantic match: "advanced persistent threat campaign"
# - Category: THREAT_ACTOR (Tier 1)
# - Type: APT_GROUP (Tier 2)
# - Confidence: >= 0.7
```

## Domain-Specific Test Cases

### ICS/SCADA Infrastructure Search

```bash
# Find SCADA-related infrastructure
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "industrial control system",
    "limit": 15,
    "label_filter": "INFRASTRUCTURE",
    "fine_grained_filter": "SCADA_SERVER"
  }' | jq

# Search for PLCs
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programmable logic controller",
    "fine_grained_filter": "PLC"
  }' | jq
```

### Protocol-Specific Search

```bash
# Find Modbus TCP entities
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "industrial communication protocol",
    "fine_grained_filter": "MODBUS_TCP"
  }' | jq

# Find DNP3 protocol entities
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "power grid protocol",
    "fine_grained_filter": "DNP3"
  }' | jq
```

### Malware Family Search

```bash
# Search for ransomware families
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "encryption malware",
    "fine_grained_filter": "RANSOMWARE"
  }' | jq

# Search for banking trojans
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "financial malware",
    "fine_grained_filter": "BANKING_TROJAN"
  }' | jq
```

### Vulnerability Search

```bash
# Search for CVE vulnerabilities
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software vulnerability",
    "fine_grained_filter": "CVE"
  }' | jq

# Search for zero-day exploits
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "unknown vulnerability",
    "fine_grained_filter": "ZERO_DAY"
  }' | jq
```

### Attack Pattern Search

```bash
# Search for phishing attacks
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "email attack",
    "fine_grained_filter": "PHISHING"
  }' | jq

# Search for SQL injection
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "database attack",
    "fine_grained_filter": "SQL_INJECTION"
  }' | jq
```

## Validation Testing

### Verify Hierarchy Path Format

```bash
# Check that all results include proper hierarchy_path
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "cyber threat", "limit": 3}' | \
  jq '.results[].hierarchy_path'

# Expected format: "TIER1/TIER2/INSTANCE"
# Example: "MALWARE/RANSOMWARE/WannaCry"
```

### Verify Filter Effectiveness

```bash
# Test that fine_grained_filter actually filters
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "malware",
    "limit": 100,
    "fine_grained_filter": "RANSOMWARE"
  }' | jq '.results[].fine_grained_type' | sort | uniq

# Should ONLY return "RANSOMWARE", no other types
```

## Error Handling Testing

### 1. Service Not Available

```bash
# Stop Qdrant and test error handling
docker stop openspg-qdrant

curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}' | jq

# Expected: 503 Service Unavailable
```

### 2. Invalid Parameters

```bash
# Missing required field
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}' | jq

# Expected: 422 Validation Error

# Invalid confidence threshold
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "confidence_threshold": 2.0}' | jq

# Expected: May work but return no results (threshold > 1.0)
```

## Performance Testing

### Measure Search Latency

```bash
# Time a basic search
time curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "ransomware", "limit": 10}' -o /dev/null -s

# Typical response: < 500ms for 10 results
```

### Batch Testing Script

```bash
# Create a test script
cat > test_search.sh << 'EOF'
#!/bin/bash
QUERIES=("ransomware attack" "SCADA system" "threat actor" "vulnerability" "protocol")

for query in "${QUERIES[@]}"; do
  echo "Testing: $query"
  curl -X POST http://localhost:8000/search/semantic \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$query\", \"limit\": 5}" -s | \
    jq '.total_results'
  sleep 1
done
EOF

chmod +x test_search.sh
./test_search.sh
```

## Integration with Data Pipeline

### Load Test Data First

Before testing search, ensure you have data in Qdrant:

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines

# Run the hierarchical embedding pipeline test
python 02_entity_embedding_service_hierarchical.py

# This will:
# 1. Process sample document through NER11
# 2. Enrich with hierarchical classification
# 3. Store embeddings in Qdrant
# 4. Validate hierarchy preservation
```

## Swagger UI Interactive Testing

The easiest way to test is through the built-in Swagger UI:

1. Open browser: `http://localhost:8000/docs`
2. Expand `/search/semantic` endpoint
3. Click "Try it out"
4. Enter parameters:
   ```json
   {
     "query": "ransomware attack",
     "limit": 10,
     "fine_grained_filter": "RANSOMWARE"
   }
   ```
5. Click "Execute"
6. View response with full hierarchy information

## Expected Response Structure

```json
{
  "results": [
    {
      "score": 0.8952,
      "entity": "WannaCry",
      "ner_label": "MALWARE",
      "fine_grained_type": "RANSOMWARE",
      "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",
      "confidence": 1.0,
      "doc_id": "test_doc_001"
    }
  ],
  "query": "ransomware attack",
  "filters_applied": {
    "label_filter": null,
    "fine_grained_filter": "RANSOMWARE",
    "confidence_threshold": 0.0
  },
  "total_results": 1
}
```

## Troubleshooting

### Problem: "Semantic search service not available"

**Solution:**
1. Check Qdrant is running: `docker ps | grep qdrant`
2. Verify collection exists: `curl http://localhost:6333/collections/ner11_entities_hierarchical`
3. Check server logs for import errors
4. Ensure `pipelines/02_entity_embedding_service_hierarchical.py` exists

### Problem: No search results returned

**Solution:**
1. Verify data exists in Qdrant:
   ```bash
   curl http://localhost:6333/collections/ner11_entities_hierarchical
   ```
2. Run the embedding pipeline test to load sample data
3. Check if filters are too restrictive
4. Try search without filters first

### Problem: Import errors on startup

**Solution:**
1. Install required dependencies:
   ```bash
   pip install sentence-transformers qdrant-client
   ```
2. Verify Python path includes pipelines directory
3. Check file exists: `ls -la 5_NER11_Gold_Model/pipelines/02_*.py`

## Next Steps

1. **Load Production Data**: Process your actual documents through the pipeline
2. **Tune Search Parameters**: Adjust limit, confidence thresholds for your use case
3. **Create Custom Filters**: Combine Tier 1 and Tier 2 filters for precise searches
4. **Monitor Performance**: Track search latency and adjust batch sizes
5. **Build Applications**: Integrate semantic search into your applications

## Summary

✅ **Implemented Features:**
- POST `/search/semantic` endpoint
- Tier 1 filtering (60 NER labels)
- Tier 2 filtering (566 fine-grained types) ← KEY FEATURE
- Confidence threshold filtering
- Hierarchy path in all results
- Automatic Swagger documentation
- Health monitoring for services

✅ **Testing Complete:**
- Basic search functionality
- Hierarchical filtering at both tiers
- Error handling and validation
- Performance verification

---

**Reference Documents:**
- TASKMASTER Task 1.5
- Specification: 03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md
- Embedding Service: pipelines/02_entity_embedding_service_hierarchical.py
- API Code: serve_model.py
