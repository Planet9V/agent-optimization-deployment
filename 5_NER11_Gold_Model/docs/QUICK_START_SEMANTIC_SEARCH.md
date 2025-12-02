# NER11 Semantic Search - Quick Start Guide

**Version:** 1.0.0
**Task:** TASKMASTER Task 1.5
**Status:** ACTIVE

## 🚀 Quick Start (3 Steps)

### 1. Start Services

```bash
# Start Qdrant
docker start openspg-qdrant

# Start NER11 API
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python serve_model.py
```

### 2. Verify Health

```bash
curl http://localhost:8000/health
# Should show: "semantic_search": "available"
```

### 3. Run First Search

```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "ransomware attack", "limit": 5}' | jq
```

## 📝 Essential Commands

### Basic Search
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "limit": 10}' | jq
```

### Tier 1 Filter (60 NER Labels)
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "YOUR_QUERY",
    "label_filter": "MALWARE"
  }' | jq
```

### Tier 2 Filter (566 Fine-Grained Types) ⭐ KEY FEATURE
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "YOUR_QUERY",
    "fine_grained_filter": "RANSOMWARE"
  }' | jq
```

### Combined Filters
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "control system",
    "label_filter": "INFRASTRUCTURE",
    "fine_grained_filter": "SCADA_SERVER",
    "confidence_threshold": 0.8
  }' | jq
```

## 🎯 Common Use Cases

### ICS/SCADA Search
```bash
# Find SCADA systems
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "industrial control", "fine_grained_filter": "SCADA_SERVER"}' | jq

# Find PLCs
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "programmable controller", "fine_grained_filter": "PLC"}' | jq
```

### Malware Search
```bash
# Ransomware families
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "encryption malware", "fine_grained_filter": "RANSOMWARE"}' | jq

# APT groups
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "advanced threat", "fine_grained_filter": "APT_GROUP"}' | jq
```

### Protocol Search
```bash
# Modbus TCP
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "industrial protocol", "fine_grained_filter": "MODBUS_TCP"}' | jq
```

## 📊 Available Fine-Grained Types (566 Total)

### Top Categories
- **MALWARE** (42 types): RANSOMWARE, TROJAN, WORM, BACKDOOR, ROOTKIT, APT_MALWARE, etc.
- **INFRASTRUCTURE** (52 types): PLC, SCADA_SERVER, HMI, RTU, DCS, INDUSTRIAL_ROUTER, etc.
- **PROTOCOL** (45 types): MODBUS_TCP, DNP3, PROFINET, OPC_UA, IEC_61850, etc.
- **THREAT_ACTOR** (32 types): APT_GROUP, NATION_STATE, RANSOMWARE_GROUP, etc.
- **ATTACK_PATTERN** (38 types): PHISHING, SQL_INJECTION, PRIVILEGE_ESCALATION, etc.
- **VULNERABILITY** (28 types): CVE, ZERO_DAY, MEMORY_CORRUPTION, etc.
- **TOOL** (35 types): EXPLOITATION_FRAMEWORK, SCANNER, C2_FRAMEWORK, etc.
- **INDICATOR** (24 types): IP_ADDRESS, DOMAIN, FILE_HASH, YARA_RULE, etc.

### View All Types
```bash
# Get full type list from API
curl http://localhost:8000/info | jq '.hierarchy_info'
```

## 🔍 Understanding Results

```json
{
  "score": 0.8952,              // Semantic similarity (0-1)
  "entity": "WannaCry",          // Entity text
  "ner_label": "MALWARE",        // Tier 1 (60 labels)
  "fine_grained_type": "RANSOMWARE",  // Tier 2 (566 types) ⭐
  "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",  // Full path
  "confidence": 1.0,             // NER confidence
  "doc_id": "doc_abc123"         // Source document
}
```

## 🌐 Interactive Testing

**Swagger UI:** http://localhost:8000/docs
- Visual interface for testing
- Auto-generated documentation
- Request/response examples

## 🔧 Troubleshooting

### No Results?
1. Load test data: `python pipelines/02_entity_embedding_service_hierarchical.py`
2. Check Qdrant: `curl http://localhost:6333/collections/ner11_entities_hierarchical`

### Service Unavailable?
1. Start Qdrant: `docker start openspg-qdrant`
2. Check health: `curl http://localhost:8000/health`

### Import Errors?
```bash
pip install sentence-transformers qdrant-client
```

## 📚 Full Documentation

- **Comprehensive Guide:** `docs/SEMANTIC_SEARCH_API_TESTING.md`
- **API Spec:** `serve_model.py`
- **Pipeline Details:** `pipelines/02_entity_embedding_service_hierarchical.py`
- **TASKMASTER:** Task 1.5

---

**Key Feature:** Tier 2 filtering with 566 fine-grained types enables precision searches beyond basic NER labels!
