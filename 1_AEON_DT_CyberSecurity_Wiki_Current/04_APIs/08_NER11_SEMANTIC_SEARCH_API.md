# API Specification: NER11 Semantic Search
**API ID**: API-08
**Version**: 2.0.0
**Status**: ✅ IMPLEMENTED (Phase 1 Complete)
**Base URL**: http://localhost:8000
**Technology**: FastAPI + Qdrant + sentence-transformers
**Authentication**: None (internal API)
**Related Enhancement**: E30 - NER11 Gold Hierarchical Integration

---

## OVERVIEW

The NER11 Semantic Search API provides semantic vector search capabilities over cybersecurity entities extracted by the NER11 Gold Standard model, with hierarchical filtering supporting the complete 566 fine-grained entity type taxonomy.

**Key Innovation**: Three-tier hierarchical filtering enables precise entity type queries (e.g., "find RANSOMWARE" not just "find MALWARE") while maintaining semantic search capabilities.

---

## ENDPOINTS

### POST /search/semantic

**Purpose**: Semantic search over NER11-extracted entities with hierarchical filtering

**Request**:
```json
{
  "query": "string (required, 1-1000 characters)",
  "limit": "integer (optional, 1-100, default 10)",
  "label_filter": "string (optional, Tier 1: 60 NER labels)",
  "fine_grained_filter": "string (optional, Tier 2: 566 types)",
  "confidence_threshold": "float (optional, 0.0-1.0, default 0.7)"
}
```

**Response**:
```json
{
  "results": [
    {
      "text": "string",
      "label": "string",
      "fine_grained_type": "string",
      "specific_instance": "string",
      "hierarchy_path": "string",
      "similarity": "float",
      "confidence": "float",
      "doc_id": "string",
      "context": "string"
    }
  ],
  "query": "string",
  "total_found": "integer"
}
```

**Status Codes**:
- 200: Success
- 400: Invalid request (query too long, invalid filters)
- 500: Server error (Qdrant unavailable, embedding model error)

---

## HIERARCHICAL FILTERING

### Tier 1: NER Label Filtering (60 Labels)

**Parameter**: `label_filter`
**Values**: Any of 60 NER labels (MALWARE, THREAT_ACTOR, DEVICE, CVE, etc.)

**Example**:
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{"query": "attacks", "label_filter": "MALWARE"}'
# Returns: Only malware entities, not threat actors or other types
```

### Tier 2: Fine-Grained Type Filtering (566 Types) ⭐ KEY FEATURE

**Parameter**: `fine_grained_filter`
**Values**: Any of 566 fine-grained types (RANSOMWARE, PLC, NATION_STATE, etc.)

**Example**:
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{"query": "industrial systems", "fine_grained_filter": "PLC"}'
# Returns: Only PLCs, not RTUs, HMIs, or other devices
```

**Common Fine-Grained Filters**:
- Malware: RANSOMWARE, TROJAN, WORM, RAT, ROOTKIT
- Threat Actors: NATION_STATE, APT_GROUP, HACKTIVIST, CRIME_SYNDICATE
- Devices: PLC, RTU, HMI, DCS, SCADA_SERVER
- Biases: CONFIRMATION_BIAS, NORMALCY_BIAS, AVAILABILITY_HEURISTIC
- Protocols: MODBUS, DNP3, IEC_61850, PROFINET

### Tier 3: Entity Instance

**Implicit**: Searches match against specific_instance field
**Example**: Query "WannaCry" will find the specific WannaCry entity

---

## EXAMPLE QUERIES

### Basic Semantic Search
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware attacks on critical infrastructure",
    "limit": 10
  }'
```

### Tier 1 Filtering (Broad Category)
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{
    "query": "vulnerabilities in web servers",
    "label_filter": "CVE",
    "limit": 20
  }'
```

### Tier 2 Filtering (Specific Type) - MOST POWERFUL
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{
    "query": "control system vulnerabilities",
    "fine_grained_filter": "PLC",
    "confidence_threshold": 0.85,
    "limit": 15
  }'
```

### Psychometric Analysis Query
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{
    "query": "decision making errors in security teams",
    "label_filter": "COGNITIVE_BIAS",
    "fine_grained_filter": "CONFIRMATION_BIAS"
  }'
```

### Industrial Protocol Search
```bash
curl -X POST http://localhost:8000/search/semantic \
  -d '{
    "query": "SCADA communication vulnerabilities",
    "fine_grained_filter": "MODBUS",
    "confidence_threshold": 0.8
  }'
```

---

## RESPONSE FORMAT

### Success Response (200 OK):
```json
{
  "results": [
    {
      "text": "WannaCry",
      "label": "MALWARE",
      "fine_grained_type": "RANSOMWARE",
      "specific_instance": "WannaCry",
      "hierarchy_path": "MALWARE/RANSOMWARE/WannaCry",
      "similarity": 0.89,
      "confidence": 1.0,
      "doc_id": "training_doc_042",
      "context": "...WannaCry ransomware spread globally affecting..."
    }
  ],
  "query": "ransomware attacks on critical infrastructure",
  "total_found": 1
}
```

### Error Response (400 Bad Request):
```json
{
  "detail": "Query text exceeds maximum length of 1000 characters"
}
```

### Error Response (500 Internal Server Error):
```json
{
  "detail": "Qdrant connection failed: Connection refused"
}
```

---

## INTEGRATION WITH OTHER APIS

### Complements:
- **API-01**: Equipment API (can query for specific device types via fine_grained_filter)
- **API-02**: Vulnerabilities API (semantic search for CVEs)
- **E27**: Psychohistory API (cognitive bias search enabled)

### Future Enhancement:
- **Phase 3**: Hybrid search (combine this API with Neo4j graph traversal)

---

## PERFORMANCE

### Response Time Targets:
- **Simple query**: <100ms
- **Filtered query**: <150ms
- **Complex query** (multiple filters): <200ms

### Throughput:
- **Concurrent requests**: 100+ requests/second
- **Max query latency**: 500ms (99th percentile)

### Scalability:
- **Tested**: 670 entities
- **Designed**: 1M+ entities
- **Qdrant**: Scales to 100M+ vectors

---

## TESTING

### Automated Test Suite:
**Script**: `/5_NER11_Gold_Model/scripts/test_semantic_search.sh`

```bash
# Run all tests
cd /5_NER11_Gold_Model
chmod +x scripts/test_semantic_search.sh
./scripts/test_semantic_search.sh
```

### Manual Testing:
**Swagger UI**: http://localhost:8000/docs
- Interactive API explorer
- Try queries in browser
- See request/response formats

### Test Examples:
See `/5_NER11_Gold_Model/docs/SEMANTIC_SEARCH_API_TESTING.md` for 60+ test cases

---

## MAINTENANCE

### Update Procedures:

**When to Update This Specification**:
- When fine_grained_filter options change
- When new filtering capabilities added
- When response format changes
- When performance characteristics change

**Related Documents to Update**:
- Enhancement E30 blotter (task status)
- Master specification (Section 8.2)
- Implementation documentation

### Monitoring:

**Metrics to Track**:
- Query latency (p50, p95, p99)
- Result relevance (user feedback)
- Tier 2 filter usage (which types queried most)
- Error rate

**Log Location**: Standard FastAPI logs + Qdrant query logs

---

## APPENDIX: COMPLETE FINE-GRAINED TYPE REFERENCE

### Malware Types (60+):
RANSOMWARE, TROJAN, WORM, ROOTKIT, RAT, LOADER, DROPPER, BACKDOOR, BOTNET, SPYWARE, ADWARE, SCAREWARE, CRYPTOMINER, INFOSTEALER, DOWNLOADER, KEYLOGGER, and 44 more

### Threat Actor Types (45):
NATION_STATE, APT_GROUP, HACKTIVIST, CRIME_SYNDICATE, INSIDER, SCRIPT_KIDDIE, STATE_SPONSORED, TERRORIST_GROUP, and 37 more

### Device Types (120):
PLC, RTU, HMI, DCS, SCADA_SERVER, IED, SENSOR, ACTUATOR, RELAY, CIRCUIT_BREAKER, TRANSFORMER, SUBSTATION, and 108 more

### Cognitive Bias Types (25):
CONFIRMATION_BIAS, NORMALCY_BIAS, AVAILABILITY_HEURISTIC, ANCHORING_BIAS, RECENCY_BIAS, OPTIMISM_BIAS, DUNNING_KRUGER, GROUPTHINK, and 17 more

**Complete List**: See HierarchicalEntityProcessor taxonomy (799 types total)

---

**API Status**: ✅ PRODUCTION-READY
**Implementation**: Phase 1 Complete
**Next**: Phase 3 will add hybrid search (semantic + graph)
